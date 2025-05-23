import streamlit as st
import together
from datetime import datetime
import json
import time
import re
import sys
import os
from dotenv import load_dotenv

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.fraud_detector import FraudDetector
from services.eligibility import EligibilityChecker
from services.llm_service import DeepSeekLLM
from database import SessionLocal
from database.models import Applicant, ClaimHistory

# Load environment variables
load_dotenv()

# Initialize Together client
together.api_key = os.getenv("TOGETHER_API_KEY")

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "🌞 Good morning!"
    elif 12 <= hour < 17: return "☀️ Good afternoon!" 
    else: return "🌙 Good evening!"

def generate_response(messages):
    """Handle free tier rate limits with retries"""
    max_retries = 3
    # Convert messages to a prompt string
    prompt = ""
    for m in messages:
        prompt += f"{m['role']}: {m['content']}\n"
    for attempt in range(max_retries):
        try:
            response = together.Complete.create(
                prompt=prompt,
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                temperature=0.5,
                max_tokens=150,
                stop=["\n\n"] 
            )
            if 'choices' in response and response['choices']:
                return response['choices'][0]['text'].strip()
            else:
                st.error(f"LLM response missing 'choices' key: {response}")
                return "I apologize, but I'm having trouble generating a response right now. Please try again later."
        except Exception as e:
            if "rate limit" in str(e).lower():
                wait_time = (2 ** attempt) + 0.5
                st.warning(f"Processing... (attempt {attempt+1}/3)")
                time.sleep(wait_time)
            else:
                st.error(f"Error: {str(e)}")
                return None
    return "I'm currently overwhelmed with requests. Please try again in a minute."

def analyze_claim(claim_data):
    try:
        # Convert earnings to float
        if 'earnings' in claim_data:
            claim_data['earnings'] = float(claim_data['earnings'])
        if 'employment_months' in claim_data:
            claim_data['employment_months'] = int(claim_data['employment_months'])
            
        # Initialize services
        fraud_detector = FraudDetector()
        eligibility_checker = EligibilityChecker()
        
        # Perform checks
        fraud_result = fraud_detector.analyze_claim(claim_data)
        failed_rules = eligibility_checker.evaluate(claim_data)
        
        # Determine final status
        status = "approved" if not failed_rules else "denied"
        
        # Generate explanation
        llm = DeepSeekLLM()
        explanation_context = {
            "status": status,
            "fraud_analysis": {
                "score": fraud_result["score"],
                "patterns": fraud_result["patterns"],
                "hard_rule_violations": fraud_result["hard_rule_violations"],
                "temporal_redflags": fraud_result["temporal_redflags"],
                "is_anomaly": fraud_result["is_anomaly"],
            },
            "eligibility": {
                "failed_rules": [r["message"] for r in failed_rules]
            },
            "user_data": {
                "months": claim_data.get("employment_months"),
                "earnings": claim_data.get("earnings"),
                "employer": claim_data.get("employer"),
                "reason": claim_data.get("separation_reason")
            }
        }
        
        base_prompt = """You're Joy, a friendly unemployment insurance assistant. 
        Provide exactly ONE clear explanation for this decision:

        Status: {status}
        Context: {context}

        Rules:
        - Provide ONLY ONE explanation (2-3 sentences max)
        - Do not repeat yourself
        - Use simple, clear language
        - Format as: "Explanation: [your text]"
"""
        
        explanation = llm.generate_explanation(
            base_prompt.format(status=status, context=json.dumps(explanation_context))
        )
        explanation = clean_response(explanation)  # Add this line
                
        # Format the response - only show status and explanation
        formatted_response = f"""
        **Status**: {status.upper()}

        **Explanation**:  
        {explanation.split('Explanation:')[-1].strip()}
        """
        return formatted_response
    except Exception as e:
        st.error(f"Error processing claim: {str(e)}")
        return None


def clean_response(text):
    # Remove duplicate explanations
    sentences = text.split('. ')
    unique_sentences = []
    seen = set()
    
    for sentence in sentences:
        clean_sentence = sentence.strip()
        if clean_sentence and clean_sentence not in seen:
            seen.add(clean_sentence)
            unique_sentences.append(clean_sentence)
    
    # Join back with periods and ensure proper ending
    cleaned = '. '.join(unique_sentences)
    if not cleaned.endswith('.'):
        cleaned += '.'
    return cleaned


def detect_claim_intent(text):
    """Detects natural language requests to start claims"""
    patterns = [
        r"(start|begin|file).*(claim|application|unemployment)",
        r"i (need|want) to (apply|file|submit)",
        r"help me with (my|a) claim",
        r"unemployment (benefits|application)"
    ]
    return any(re.search(pattern, text.lower()) for pattern in patterns)

def reset_claim():
    st.session_state.claim_data = {}
    st.session_state.current_step = 0
    st.session_state.claim_in_progress = False

def main():
    st.set_page_config(page_title="Unemployment Assistant", layout="wide")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant", 
            "content": f"{get_greeting()} I'm your claims assistant. Type 'start claim' to begin or ask me questions."
        }]
        reset_claim()
    
    # Define claim steps
    CLAIM_STEPS = [
        {"prompt": "First, I'll need the last 4 digits of your SSN.", "field": "ssn_last4", "validation": lambda x: len(x) == 4 and x.isdigit()},
        {"prompt": "Which company did you last work for?", "field": "employer"},
        {"prompt": "What was the reason for your separation?", "field": "separation_reason"},
        {"prompt": "What were your total earnings in the last 6 months (USD)?", "field": "earnings", "validation": lambda x: x.replace('.','',1).isdigit()},
        {"prompt": "How many months were you employed there?", "field": "employment_months", "validation": lambda x: x.isdigit()}
    ]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Handle user input
    if prompt := st.chat_input("Type here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Initialize response variable
        response = None
        
        # Detect claim intent in natural language
        if (not st.session_state.claim_in_progress and 
            detect_claim_intent(prompt)):
            st.session_state.claim_in_progress = True
            response = "I can help with that! Just type: 'start claim'\n\nOr say 'continue' to begin now."
        
        # Handle direct command
        elif (not st.session_state.claim_in_progress and 
              "start claim" in prompt.lower()):
            st.session_state.claim_in_progress = True
            response = CLAIM_STEPS[0]["prompt"]
        
        # Handle continuation
        elif (not st.session_state.claim_in_progress and 
              "continue" in prompt.lower() and 
              "claim" in st.session_state.messages[-2]["content"].lower()):
            st.session_state.claim_in_progress = True
            response = CLAIM_STEPS[0]["prompt"]
        
        # Continue existing claim
        elif st.session_state.claim_in_progress:
            current_step = CLAIM_STEPS[st.session_state.current_step]
            
            # Validate input
            if "validation" in current_step and not current_step["validation"](prompt):
                response = f"Please enter a valid value. {current_step['prompt']}"
            else:
                # Store validated data
                st.session_state.claim_data[current_step["field"]] = prompt
                st.session_state.current_step += 1
                
                # If more steps remain
                if st.session_state.current_step < len(CLAIM_STEPS):
                    response = CLAIM_STEPS[st.session_state.current_step]["prompt"]
                else:
                    # Process complete claim
                    with st.spinner("Reviewing your claim..."):
                        decision = analyze_claim(st.session_state.claim_data)
                        st.session_state.messages.append({"role": "assistant", "content": decision})
                        st.chat_message("assistant").write(decision)
                    
                    response = "To file another claim, just say: 'start claim'"
                    reset_claim()
        
        # General conversation
        else:
            messages = [
                {"role": "system", "content": """You're a friendly unemployment assistant. Keep responses under 2 sentences. 
                When claims are mentioned, clearly show the command 'start claim' as an option."""},
                {"role": "user", "content": prompt}
            ]
            with st.spinner("Thinking..."):
                response = generate_response(messages)
                
                # Enhance claim-related responses
                if detect_claim_intent(prompt):
                    response += "\n\nYou can start by typing: 'start claim'"
        
        # Add response to chat
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
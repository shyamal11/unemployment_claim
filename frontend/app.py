import streamlit as st
import together
from datetime import datetime
import json
import time
import re
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

# Initialize Together client
together.api_key = settings.TOGETHER_API_KEY

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
                max_tokens=300
            )
            return response['output']['choices'][0]['text'].strip()
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
    messages = [
        {
            "role": "system",
            "content": """You are an unemployment claims analyzer. Respond ONLY in this format:
            
**Status**: APPROVED/DENIED/FLAGGED  
**Reason**: [1-2 sentence explanation]  
**Next Steps**: [clear instructions]

Rules:
1. Never repeat yourself
2. Use bold for section headers only
3. Maximum 3 sentences total
4. If unsure, say "Please contact a claims specialist\""""
        },
        {
            "role": "user", 
            "content": json.dumps(claim_data)
        }
    ]
    return generate_response(messages)

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
        {"prompt": "First, I'll need the last 4 digits of your SSN.", "field": "ssn", "validation": lambda x: len(x) == 4 and x.isdigit()},
        {"prompt": "Which company did you last work for?", "field": "employer"},
        {"prompt": "What was the reason for your separation?", "field": "reason"},
        {"prompt": "What were your total earnings in the last 6 months (USD)?", "field": "earnings", "validation": lambda x: x.replace('.','',1).isdigit()},
        {"prompt": "How many months were you employed there?", "field": "months", "validation": lambda x: x.isdigit()}
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

        # Add assistant response
        if response:
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
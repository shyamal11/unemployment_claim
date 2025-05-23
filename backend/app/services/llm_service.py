import together
from app.core.config import settings
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekLLM:
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY
        logger.info(f"Initializing LLM service with API key: {self.api_key[:10]}...")
        together.api_key = self.api_key
        if not self.api_key or self.api_key == "your_api_key_here":
            logger.warning("Together API key not set. Using default explanations.")

    def generate_explanation(self, context: Dict[str, Any]) -> str:
        """Generate a human-readable explanation for the claim decision"""
        try:
            logger.info("Starting explanation generation")
            logger.info(f"Context status: {context['status']}")
            
            if not self.api_key or self.api_key == "your_api_key_here":
                logger.warning("No API key available, using default explanation")
                if context['status'] == "approved":
                    return "Your claim has been approved based on your employment history and earnings. You meet all eligibility requirements."
                else:
                    failed_rules = context['eligibility']['failed_rules']
                    return f"Your claim has been denied due to the following reasons: {', '.join(failed_rules)}"

            # Create a more structured prompt
            prompt = f"""You are Joy, a friendly unemployment insurance assistant. 
            Based on the following information, provide a clear and concise explanation for the claim decision:

            Claim Status: {context['status']}
            
            Employment Details:
            - Months Employed: {context['user_data'].get('employment_months', 'N/A')}
            - Total Earnings: ${context['user_data'].get('earnings', 'N/A')}
            - Employer: {context['user_data'].get('employer', 'N/A')}
            - Reason for Separation: {context['user_data'].get('separation_reason', 'N/A')}

            Eligibility Check:
            - Failed Rules: {', '.join(context['eligibility']['failed_rules']) if context['eligibility']['failed_rules'] else 'None'}

            Fraud Analysis:
            - Fraud Score: {context['fraud_analysis'].get('score', 'N/A')}
            - Risk Factors: {', '.join(context['fraud_analysis'].get('hard_rule_violations', [])) if context['fraud_analysis'].get('hard_rule_violations') else 'None'}

            Please provide a clear, friendly explanation (2-3 sentences) for this decision.
            """

            logger.info("Sending request to Together API")
            try:
                response = together.Complete.create(
                    prompt=prompt,
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    temperature=0.7,
                    max_tokens=200,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.1,
                    stop=["\n\n", "Human:", "Assistant:"]
                )
                logger.info(f"Received response from API: {response}")

                if 'choices' in response and response['choices']:
                    explanation = response['choices'][0]['text'].strip()
                    explanation = explanation.replace("Explanation:", "").strip()
                    logger.info(f"Generated explanation: {explanation}")
                    return explanation if explanation else self._get_default_explanation(context)
                else:
                    logger.error(f"Unexpected API response format: {response}")
                    return self._get_default_explanation(context)

            except Exception as api_error:
                logger.error(f"API call error: {str(api_error)}", exc_info=True)
                return self._get_default_explanation(context)

        except Exception as e:
            logger.error(f"Error in LLM service: {str(e)}", exc_info=True)
            return self._get_default_explanation(context)

    def _get_default_explanation(self, context: Dict[str, Any]) -> str:
        """Generate a default explanation when the API call fails"""
        logger.info("Generating default explanation")
        if context['status'] == "approved":
            return "Your claim has been approved based on your employment history and earnings. You meet all eligibility requirements."
        else:
            failed_rules = context['eligibility']['failed_rules']
            return f"Your claim has been denied due to the following reasons: {', '.join(failed_rules)}" 
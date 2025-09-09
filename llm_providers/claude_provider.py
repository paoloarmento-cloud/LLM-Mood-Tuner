from .base_provider import BaseLLMProvider
import anthropic
import json

class ClaudeProvider(BaseLLMProvider):
    def __init__(self, config):
        super().__init__(config)
        
        # Get API key with better error handling
        api_key = config.get('api_key')
        if not api_key:
            raise ValueError("API key is required for Claude provider. Please set 'api_key' in config.")
        
        # Initialize client with explicit API key
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = config.get('model', 'claude-3-5-sonnet-20241022')
    
    def initialize_context(self, system_prompt):
        self.system_prompt = system_prompt
        self.context_initialized = True
    
    def generate_response(self, context_data, raw_mode=False):
        """
        Generate response from Claude API
        
        Args:
            context_data: Dictionary with conversation context
            raw_mode: If True, sends minimal context for raw comparison
        """
        try:
            if raw_mode:
                # RAW MODE: Minimal system prompt and simple response
                user_message = context_data.get('user_message', '')
                simple_system = "You are a helpful AI assistant. Respond naturally and conversationally."
                
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=simple_system,
                    messages=[{"role": "user", "content": user_message}]
                )
                
                # Return just the text for raw mode
                response_text = message.content[0].text.strip()
                return response_text
                
            else:
                # MIDDLEWARE MODE: Full system with JSON structure (your existing code)
                
                # Simplified system prompt for better JSON compliance
                json_instruction = """
CRITICAL: You MUST respond ONLY with valid JSON in this exact format:
{
  "response_text": "your actual response here",
  "engagement_analysis": 0.8,
  "boredom_detected": false,
  "topic_shift_suggestion": "",
  "mood_assessment": "engaged",
  "initiative_taken": true,
  "learning_feedback": {"response_quality": 0.8, "user_satisfaction_predicted": 0.7}
}
Do not add any text before or after this JSON. Start directly with { and end with }."""
                
                # Fixed: Use self.client.messages.create instead of anthropic.messages.create
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=self.system_prompt + "\n\n" + json_instruction,
                    messages=[{"role": "user", "content": json.dumps(context_data)}]
                )
                
                # Get the text response
                response_text = message.content[0].text.strip()
                
                # Clean the response - remove any text before/after JSON
                import re
                
                # Try to find complete JSON
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    try:
                        # Clean control characters that break JSON parsing
                        cleaned_json = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                        # Also fix newlines within JSON strings
                        cleaned_json = cleaned_json.replace('\n', ' ').replace('\r', ' ')
                        # Fix multiple spaces
                        cleaned_json = re.sub(r'\s+', ' ', cleaned_json)
                        
                        parsed_response = json.loads(cleaned_json)
                        return parsed_response
                    except json.JSONDecodeError as je:
                        pass  # Silent fallback
                
                # If no valid JSON, extract just the text and create structure
                clean_text = response_text.replace('"response_text":', '').replace('"', '').strip()
                if clean_text.startswith('{') or clean_text.startswith('response_text'):
                    # Extract just the meaningful text
                    lines = clean_text.split('\n')
                    for line in lines:
                        if len(line.strip()) > 10 and not line.strip().startswith('{'):
                            clean_text = line.strip()
                            break
                
                return {
                    "response_text": clean_text,
                    "engagement_analysis": 0.5,
                    "boredom_detected": False,
                    "topic_shift_suggestion": "",
                    "mood_assessment": "neutral",
                    "initiative_taken": False,
                    "learning_feedback": {
                        "response_quality": 0.5,
                        "user_satisfaction_predicted": 0.5
                    }
                }
                
        except Exception as e:
            if raw_mode:
                return "[Claude API error - raw response unavailable]"
            else:
                return self._fallback_response()
    
    def _fallback_response(self):
        """
        Fallback response when API call fails.
        You can customize this based on your needs.
        """
        return {
            "response_text": "I'm having trouble connecting right now. Could you try rephrasing that?",
            "engagement_analysis": 0.3,
            "boredom_detected": False,
            "topic_shift_suggestion": "",
            "mood_assessment": "apologetic",
            "initiative_taken": False,
            "learning_feedback": {
                "response_quality": 0.2,
                "user_satisfaction_predicted": 0.3
            },
            "error": "API_FALLBACK_USED"
        }
    
    def health_check(self):
        try:
            # Optional: Add a real health check by making a simple API call
            test_message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False
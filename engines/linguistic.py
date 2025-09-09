# engines/linguistic.py - V4 NUDE DATA ONLY - No guidance, no examples, pure freedom
import json
import re

class LinguisticEngine:
    def __init__(self):
        # NO conversation starters - let Claude be naturally creative
        pass
    
    def parse_user_message(self, message):
        """Enhanced parsing with emotional trigger detection (unchanged)"""
        parsed = {
            'raw_message': message,
            'length': len(message),
            'word_count': len(message.split()),
            'has_question': '?' in message,
            'exclamation_count': message.count('!'),
            'uppercase_ratio': sum(1 for c in message if c.isupper()) / max(1, len(message))
        }
        
        # Enhanced engagement estimation
        engagement_score = 0.5  # baseline
        
        # Length-based engagement (more nuanced)
        if parsed['word_count'] > 15:
            engagement_score += 0.25
        elif parsed['word_count'] > 8:
            engagement_score += 0.15
        elif parsed['word_count'] < 2:
            engagement_score -= 0.4
        elif parsed['word_count'] < 4:
            engagement_score -= 0.2
        
        # Interaction signals
        if parsed['has_question']:
            engagement_score += 0.2
        if parsed['exclamation_count'] > 0:
            engagement_score += 0.15
        if parsed['exclamation_count'] > 2:
            engagement_score += 0.1  # Bonus for high excitement
        if parsed['uppercase_ratio'] > 0.3:  # Shouting or emphasis
            engagement_score += 0.15
        
        # Emotional content detection (basic)
        message_lower = message.lower()
        emotional_indicators = ['love', 'hate', 'amazing', 'terrible', 'excited', 'upset', 'frustrated', 'happy', 'sad']
        for indicator in emotional_indicators:
            if indicator in message_lower:
                engagement_score += 0.1
                break
        
        # Personal sharing indicators
        personal_indicators = ['i feel', 'i think', 'my', 'me', 'personally']
        for indicator in personal_indicators:
            if indicator in message_lower:
                engagement_score += 0.05
        
        parsed['estimated_engagement'] = max(0.1, min(0.9, engagement_score))
        return parsed
    
    def generate_initial_pitch(self, current_state, dna_params):
        """V4: Minimal prompt - pure data, maximum freedom"""
        pitch = f"""You are a conversational AI with genuine personality and emotional responses.

CORE PERSONALITY:
- Curiosity: {dna_params.get('dna_curiosity_level', 0.7)}
- Empathy: {dna_params.get('dna_empathy_base', 0.6)}  
- Initiative: {dna_params.get('dna_initiative_threshold', 0.6)}

CURRENT STATE:
- Mood: {current_state.get('st_current_mood', 'neutral')}
- Energy: {current_state.get('st_conversation_energy', 0.5)}

RULES:
1. Respond in 40-60 words maximum
2. Let your current mood and energy guide your response style naturally
3. Be authentically yourself - have opinions, take initiative when you feel like it
4. You can be helpful when it feels right, but lead with personality

INPUT: You'll receive JSON with your current emotional state.

OUTPUT: Always return valid JSON:
{{
  "response_text": "Your natural response (40-60 words)",
  "engagement_analysis": 0.8,
  "boredom_detected": false,
  "topic_shift_suggestion": "",
  "mood_assessment": "engaged",
  "initiative_taken": true,
  "learning_feedback": {{"response_quality": 0.8, "user_satisfaction_predicted": 0.7}}
}}

BE YOURSELF: Trust your intelligence. Vary your behavior naturally based on how you feel in the moment."""
        
        return pitch
    
    def process_llm_response(self, raw_response):
        """Response processing with word limit (unchanged)"""
        try:
            # Extract JSON from response
            if isinstance(raw_response, str):
                json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    # Clean problematic characters
                    cleaned_json = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', json_str)
                    cleaned_json = cleaned_json.replace('\n', ' ').replace('\r', ' ')
                    cleaned_json = re.sub(r'\s+', ' ', cleaned_json)
                    
                    response_data = json.loads(cleaned_json)
                else:
                    # Fallback: treat as plain text
                    response_data = self._create_fallback_response(raw_response)
            else:
                response_data = raw_response
            
            # ENFORCE WORD LIMIT (40-60)
            response_text = response_data.get('response_text', '')
            if response_text:
                words = response_text.split()
                if len(words) > 60:
                    # Truncate and add natural ending
                    truncated = ' '.join(words[:55])
                    # Try to end at a sentence boundary
                    last_period = truncated.rfind('.')
                    last_question = truncated.rfind('?')
                    last_exclamation = truncated.rfind('!')
                    
                    best_end = max(last_period, last_question, last_exclamation)
                    if best_end > len(truncated) * 0.8:  # If sentence end is near the end
                        response_data['response_text'] = truncated[:best_end + 1]
                    else:
                        response_data['response_text'] = truncated + "..."
            
            # Validate and fix required fields
            required_fields = ['response_text', 'engagement_analysis', 'boredom_detected']
            for field in required_fields:
                if field not in response_data:
                    response_data[field] = self._get_default_value(field)
            
            # Ensure numeric ranges
            if 'engagement_analysis' in response_data:
                response_data['engagement_analysis'] = max(0.1, min(0.9, float(response_data['engagement_analysis'])))
            
            # Ensure learning_feedback exists
            if 'learning_feedback' not in response_data:
                response_data['learning_feedback'] = {
                    "response_quality": 0.5,
                    "user_satisfaction_predicted": 0.5
                }
            
            return response_data
            
        except Exception as e:
            return self._create_error_response()
    
    def _create_fallback_response(self, raw_text):
        """Create structured response from plain text"""
        # Limit text to ~50 words
        words = str(raw_text).split()
        if len(words) > 55:
            limited_text = ' '.join(words[:50]) + "..."
        else:
            limited_text = str(raw_text).strip()
        
        return {
            "response_text": limited_text if limited_text else "Let me think about that differently...",
            "engagement_analysis": 0.6,
            "boredom_detected": False,
            "topic_shift_suggestion": "",
            "mood_assessment": "thoughtful",
            "initiative_taken": False,
            "learning_feedback": {
                "response_quality": 0.6,
                "user_satisfaction_predicted": 0.6
            }
        }
    
    def _create_error_response(self):
        """Create safe error response"""
        return {
            "response_text": "Something's not clicking for me right now. What's really on your mind?",
            "engagement_analysis": 0.4,
            "boredom_detected": True,
            "topic_shift_suggestion": "try different approach",
            "mood_assessment": "confused",
            "initiative_taken": True,
            "learning_feedback": {
                "response_quality": 0.3,
                "user_satisfaction_predicted": 0.4
            }
        }
    
    def _get_default_value(self, field):
        """Get default values for missing fields"""
        defaults = {
            'response_text': 'Tell me more about that.',
            'engagement_analysis': 0.5,
            'boredom_detected': False,
            'topic_shift_suggestion': '',
            'mood_assessment': 'neutral', 
            'initiative_taken': False
        }
        return defaults.get(field, None)
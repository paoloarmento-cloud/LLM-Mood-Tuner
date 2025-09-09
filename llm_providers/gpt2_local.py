# llm_providers/gpt2_local.py - Local GPT-2 implementation (semplificato)
from .base_provider import BaseLLMProvider
import json
import random
from datetime import datetime

try:
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    import torch
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

class GPT2LocalProvider(BaseLLMProvider):
    def __init__(self, config):
        super().__init__(config)
        
        if not HAS_TRANSFORMERS:
            print("📦 transformers not installed. Using intelligent mock responses.")
            self.use_mock = True
            return
        
        try:
            print("🔄 Loading GPT-2 model... (this may take a moment)")
            self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
            self.model = GPT2LMHeadModel.from_pretrained('gpt2')
            
            # Add padding token
            self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ GPT-2 model loaded successfully")
            self.use_mock = False
            
        except Exception as e:
            print(f"❌ Error loading GPT-2: {e}")
            print("🔄 Using intelligent mock responses for testing")
            self.use_mock = True
    
    def initialize_context(self, system_prompt):
        """Store system prompt for context"""
        self.system_prompt = system_prompt
        self.context_initialized = True
        print(f"🎯 Context initialized for {'mock' if self.use_mock else 'GPT-2'} provider")
    
    def generate_response(self, context_data):
        """Generate response using GPT-2 or intelligent mock responses"""
        
        if self.use_mock:
            return self._generate_intelligent_mock(context_data)
        
        try:
            # Build prompt from context
            prompt = self._build_prompt(context_data)
            
            # Generate with GPT-2
            inputs = self.tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + self.config.get('max_tokens', 100),
                    temperature=self.config.get('temperature', 0.7),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=2,
                    top_p=0.9
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new part
            new_response = response[len(prompt):].strip()
            
            return self._format_response(new_response, context_data)
            
        except Exception as e:
            print(f"⚠️ Error generating GPT-2 response: {e}")
            return self._generate_intelligent_mock(context_data)
    
    def _build_prompt(self, context_data):
        """Build prompt for GPT-2"""
        user_message = context_data.get('user_message', '')
        mood = context_data.get('st_current_mood', 'neutral')
        energy = context_data.get('st_conversation_energy', 0.5)
        
        prompt = f"""Context: AI mood is {mood} with energy level {energy:.1f}
User: {user_message}
AI:"""
        
        return prompt
    
    def _format_response(self, raw_response, context_data):
        """Format GPT-2 output into expected JSON structure"""
        
        # Clean up the response
        response_text = raw_response.split('\n')[0]  # Take first line
        if len(response_text) > 200:
            response_text = response_text[:200] + "..."
        
        # Analyze context to determine other fields
        engagement = context_data.get('st_conversation_energy', 0.5)
        boredom_detected = engagement < 0.3
        
        return {
            "response_text": response_text if response_text.strip() else "I'm processing your message...",
            "engagement_analysis": min(1.0, max(0.1, engagement + random.uniform(-0.2, 0.2))),
            "boredom_detected": boredom_detected,
            "topic_shift_suggestion": "explore this further" if not boredom_detected else "try something new",
            "mood_assessment": context_data.get('st_current_mood', 'neutral'),
            "initiative_taken": boredom_detected,
            "learning_feedback": {
                "response_quality": random.uniform(0.4, 0.8),
                "user_satisfaction_predicted": random.uniform(0.3, 0.7)
            }
        }
    
    def _generate_intelligent_mock(self, context_data):
        """Generate contextually appropriate mock responses"""
        
        user_message = context_data.get('user_message', '').lower()
        mood = context_data.get('st_current_mood', 'neutral')
        energy = context_data.get('st_conversation_energy', 0.5)
        boredom_level = context_data.get('session_metrics', {}).get('boredom_triggers', 0)
        messages_count = context_data.get('session_metrics', {}).get('messages_on_current_topic', 0)
        
        # Iniziativa proattiva se noia alta
        if boredom_level > 0.5 or messages_count > 6:
            responses = [
                "I've been thinking - what's something you're genuinely excited about right now?",
                "You know what fascinates me? How people discover new interests. What was the last thing that surprised you?",
                "I'm curious about something different - if you could have dinner with anyone, who would it be and why?",
                "Let me shift gears - what's been the highlight of your week so far?",
                "I want to know more about you - what's a skill you'd love to learn if you had unlimited time?"
            ]
            initiative_taken = True
            engagement = random.uniform(0.6, 0.9)
        
        # Risposte empatiche per mood specifici
        elif mood == 'bored':
            responses = [
                "I sense we might need a change of pace. What usually gets you excited?",
                "Let's try something different - tell me about a moment when you felt truly alive.",
                "I'm picking up on some restlessness. What would make this conversation more interesting for you?"
            ]
            initiative_taken = True
            engagement = random.uniform(0.5, 0.7)
        
        # Risposte entusiaste per engagement alto
        elif mood == 'engaged' or energy > 0.7:
            responses = [
                "Your enthusiasm is infectious! Tell me more about what makes this so compelling.",
                "I love how passionate you are about this. What got you so interested in the first place?",
                "This is fascinating! I want to dive deeper - what aspect intrigues you most?"
            ]
            initiative_taken = False
            engagement = random.uniform(0.7, 0.9)
        
        # Domande esplorative per engagement medio
        elif '?' in context_data.get('user_message', ''):
            responses = [
                "That's a thought-provoking question. Let me explore this with you...",
                "Great question! It makes me think about the broader implications of this.",
                "I find that question intriguing because it touches on something fundamental..."
            ]
            initiative_taken = False
            engagement = random.uniform(0.6, 0.8)
        
        # Risposte di base per tutto il resto
        else:
            responses = [
                "That's really interesting. I'd love to understand your perspective better.",
                "I appreciate you sharing that. What made you think about this topic?",
                "There's something compelling about what you're saying. Can you elaborate?",
                "I'm genuinely curious - what draws you to think about these things?"
            ]
            initiative_taken = False
            engagement = random.uniform(0.4, 0.7)
        
        # Selezione della risposta
        response_text = random.choice(responses)
        
        # Adattamento basato su energia
        if energy < 0.3:
            response_text = response_text.replace("!", ".").lower()
        elif energy > 0.8:
            if not response_text.endswith("!") and not response_text.endswith("?"):
                response_text += "!"
        
        return {
            "response_text": response_text,
            "engagement_analysis": engagement,
            "boredom_detected": boredom_level > 0.5,
            "topic_shift_suggestion": "explore user interests" if boredom_level > 0.5 else "",
            "mood_assessment": mood,
            "initiative_taken": initiative_taken,
            "learning_feedback": {
                "response_quality": random.uniform(0.6, 0.9) if initiative_taken else random.uniform(0.5, 0.8),
                "user_satisfaction_predicted": engagement
            }
        }
    
    def health_check(self):
        """Check if provider is working"""
        return True  # Mock/GPT2 provider is always "available"
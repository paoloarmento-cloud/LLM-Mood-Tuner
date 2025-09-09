# main.py - V4 Pure data approach - clean version for GitHub
import json
import time
from datetime import datetime
from config import Config
from engines.memory import MemoryManager
from engines.linguistic import LinguisticEngine
from engines.emotional import EmotionalEngine
from engines.behavioral import BehavioralEngine
from llm_providers.provider_factory import LLMProviderFactory

class ExperientialMiddleware:
    def __init__(self):
        self.config = Config()
        self.memory = MemoryManager(self.config.excel_file)
        self.linguistic = LinguisticEngine()
        self.emotional = EmotionalEngine()
        self.behavioral = BehavioralEngine()
        self.llm_provider = LLMProviderFactory.create_provider(self.config.llm_config)
        
        # Initialize session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.memory.load_session_state()
        
        print(f"🤖 Experiential AI Middleware v4.0 - PURE DATA")
        print(f"📊 Session ID: {self.session_id}")
        print(f"🧠 LLM Provider: {self.config.llm_config['provider']}")
        print(f"💾 Memory file: {self.config.excel_file}")
        print("="*60)
    
    def run_conversation(self):
        """Main conversation loop with pure data approach"""
        print("\n🚀 Starting conversation... (type 'quit' to exit)")
        print("💡 AI receives only pure emotional data - zero guidance!")
        
        # Send initial pitch to LLM
        self._initialize_llm_context()
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not user_input:
                    continue
                
                # Process user message with pure data approach
                response = self._process_pure_data_message(user_input)
                print(f"\nAI: {response}")
                
                # Small delay to make it feel more natural
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"\n⚠️ Error: {e}")
                continue
        
        # Save session before exit
        self.memory.save_session_state()
        print(f"\n💾 Session saved. Total messages: {self.memory.get_message_count()}")
        print("👋 Goodbye!")
    
    def _initialize_llm_context(self):
        """Send minimal system prompt to LLM"""
        system_prompt = self.linguistic.generate_initial_pitch(
            self.memory.get_current_state(),
            self.memory.get_dna_parameters()
        )
        
        # Initialize LLM with minimal context
        self.llm_provider.initialize_context(system_prompt)
    
    def _process_pure_data_message(self, user_message):
        """Pure data processing - no behavioral guidance"""
        
        # 1. Parse user input
        parsed_message = self.linguistic.parse_user_message(user_message)
        
        # 2. Update emotional state
        old_mood = self.emotional.get_current_mood()
        self.emotional.update_mood_from_input(parsed_message)
        new_mood = self.emotional.get_current_mood()
        
        # 3. Behavioral analysis (for logging only - no guidance generation)
        behavior_context = self.behavioral.analyze_conversation_state(
            self.memory.get_recent_messages(),
            new_mood
        )
        
        # 4. Build PURE DATA context (no guidance whatsoever)
        llm_context = self._build_pure_data_context(user_message, new_mood, behavior_context)
        
        # 5. Get RAW LLM response for comparison
        raw_llm_response = self._get_raw_llm_response(user_message)
        
        # 6. Get PURE DATA LLM response (no behavioral instructions)
        processed_llm_response = self.llm_provider.generate_response(llm_context)
        
        # 7. Process final response
        final_processed_response = self.linguistic.process_llm_response(processed_llm_response)
        
        # 8. Update learning systems
        self._update_pure_learning_systems(user_message, final_processed_response, behavior_context)
        
        # 9. Log everything
        self._log_pure_interaction(user_message, final_processed_response, llm_context, 
                                 raw_llm_response, processed_llm_response)
        
        return final_processed_response.get('response_text', 'Let me think about this differently...')
    
    def _build_pure_data_context(self, user_message, emotional_state, behavior_context):
        """Build context with ONLY pure data - zero guidance"""
        
        current_state = self.memory.get_current_state()
        dna_params = self.memory.get_dna_parameters()
        recent_context = self.memory.get_recent_messages(limit=3)
        
        # PURE DATA ONLY - no guidance, no instructions, no examples
        pure_context = {
            "user_message": user_message,
            
            # Raw emotional data
            "current_mood": emotional_state['primary_emotion'],
            "energy_level": emotional_state['energy_level'],
            "engagement_level": emotional_state['engagement_level'],
            "curiosity_level": emotional_state['curiosity_level'],
            
            # Behavioral metrics (data only)
            "boredom_level": behavior_context.get('boredom_level', 0),
            "topic_persistence": behavior_context.get('topic_persistence', 0),
            "conversation_energy": behavior_context.get('conversation_energy', 0.5),
            
            # Memory context
            "conversation_history": recent_context,
            "user_interests": self.memory.get_user_interests(),
            
            # DNA traits (numbers only)
            "personality_curiosity": dna_params.get('dna_curiosity_level', 0.7),
            "personality_empathy": dna_params.get('dna_empathy_base', 0.6),
            "personality_initiative": dna_params.get('dna_initiative_threshold', 0.6),
            
            # Session metrics (pure numbers)
            "messages_count": self.memory.get_message_count(),
            "topic_freshness": max(0, 1 - (behavior_context.get('topic_persistence', 0) / 8))
        }
        
        return pure_context
    
    def _get_raw_llm_response(self, user_message):
        """Get raw LLM response for comparison"""
        debug_info = {}
        
        try:
            raw_provider = LLMProviderFactory.create_provider(self.config.llm_config)
            debug_info['raw_provider_created'] = True
            
            minimal_context = {
                "user_message": user_message,
                "conversation_history": [],
                "system_instruction": "You are a helpful AI assistant."
            }
            debug_info['raw_context_keys'] = len(minimal_context)
            
            raw_response = raw_provider.generate_response(minimal_context, raw_mode=True)
            debug_info['raw_response_length'] = len(str(raw_response))
            debug_info['raw_call_success'] = True
            
            if isinstance(raw_response, dict):
                result = raw_response.get('response_text', str(raw_response))
            else:
                result = str(raw_response)
                
            debug_info['raw_response_preview'] = result[:100] + "..." if len(result) > 100 else result
            self.current_raw_debug = debug_info
            return result
                
        except Exception as e:
            debug_info['raw_call_success'] = False
            debug_info['raw_error'] = str(e)
            self.current_raw_debug = debug_info
            return "[Raw response unavailable]"
    
    def _update_pure_learning_systems(self, user_message, ai_response, behavior_context):
        """Pure learning without guidance interference"""
        
        # Extract feedback
        feedback_score = ai_response.get('learning_feedback', {}).get('response_quality', 0.5)
        engagement_score = ai_response.get('engagement_analysis', 0.5)
        initiative_taken = ai_response.get('initiative_taken', False)
        
        # Update learning systems
        self.emotional.learn_from_feedback(engagement_score, feedback_score)
        self.behavioral.learn_from_outcome(initiative_taken, engagement_score)
        
        # Update experiential memory
        self.memory.update_experiential_learning({
            'user_message': user_message,
            'ai_response': ai_response.get('response_text', ''),
            'engagement_score': engagement_score,
            'feedback_score': feedback_score,
            'initiative_taken': initiative_taken,
            'boredom_level': behavior_context.get('boredom_level', 0),
            'pure_data_approach': True
        })
        
        # Update current state
        debug_info = {}
        
        current_emotional_state = self.emotional.get_current_mood()
        current_state = self.memory.get_current_state()
        
        # Update mood
        old_mood = current_state.get('st_current_mood')
        new_mood_value = current_emotional_state['primary_emotion']
        debug_info['mood_change'] = f"'{old_mood}' -> '{new_mood_value}'"
        self.memory.update_current_state('st_current_mood', new_mood_value)
        
        # Update energy
        old_energy = current_state.get('st_conversation_energy')
        new_energy_value = current_emotional_state['energy_level']
        debug_info['energy_change'] = f"{old_energy} -> {new_energy_value}"
        self.memory.update_current_state('st_conversation_energy', new_energy_value)
        
        # Standard state updates
        message_count = self.memory.get_message_count()
        self.memory.update_current_state('st_messages_count', message_count)
        
        boredom_level = behavior_context.get('boredom_level', 0)
        self.memory.update_current_state('st_boredom_level', boredom_level)
        
        # Engagement tracking
        engagement_level = current_emotional_state['engagement_level']
        if engagement_level > 0.7:
            engagement_trend = 'high'
        elif engagement_level > 0.4:
            engagement_trend = 'stable'
        else:
            engagement_trend = 'low'
        
        debug_info['engagement_trend'] = f"{engagement_trend} (level={engagement_level})"
        self.memory.update_current_state('st_engagement_trend', engagement_trend)
        
        # Update initiative tracking
        self.memory.update_current_state('st_initiative_taken', initiative_taken)
        
        # Store debug info
        self.current_debug_info = debug_info
    
    def _log_pure_interaction(self, user_message, ai_response, context, raw_response, processed_llm_response):
        """Pure data logging"""
        
        middleware_debug = getattr(self, 'current_debug_info', {})
        raw_debug = getattr(self, 'current_raw_debug', {})
        
        # Response difference calculation
        difference_metrics = self._calculate_pure_response_difference(raw_response, ai_response.get('response_text', ''))
        
        # Pure data log entry
        log_entry = {
            # Basic conversation data
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'user_message': user_message,
            'raw_llm_response': raw_response,
            'processed_llm_response': str(processed_llm_response)[:500] + "..." if len(str(processed_llm_response)) > 500 else str(processed_llm_response),
            'final_ai_response': ai_response.get('response_text', ''),
            
            # Pure emotional state
            'mood_state': context.get('current_mood'),
            'energy_level': context.get('energy_level', 0.5),
            'engagement_level': ai_response.get('engagement_analysis', 0),
            'curiosity_level': context.get('curiosity_level', 0.7),
            'boredom_level': context.get('boredom_level', 0),
            
            # Behavioral metrics (no guidance)
            'initiative_taken': ai_response.get('initiative_taken', False),
            'topic_persistence': context.get('topic_persistence', 0),
            'topic_freshness': context.get('topic_freshness', 1.0),
            'pure_data_approach': True,
            
            # Word count tracking
            'response_word_count': len(ai_response.get('response_text', '').split()),
            'word_limit_enforced': len(ai_response.get('response_text', '').split()) <= 60,
            
            # Debug information
            'debug_raw_call_success': raw_debug.get('raw_call_success', False),
            'debug_mood_change': middleware_debug.get('mood_change', ''),
            'debug_energy_change': middleware_debug.get('energy_change', ''),
            'debug_engagement_trend': middleware_debug.get('engagement_trend', ''),
            
            # Comparison metrics
            'comparison_length_difference': difference_metrics.get('length_difference', 0),
            'comparison_word_similarity': difference_metrics.get('word_similarity', 0),
            'comparison_significant_change': difference_metrics.get('significant_change', False),
            'natural_variety_score': difference_metrics.get('natural_variety', 0),
            
            # Context summary
            'context_summary': {
                'mood': context.get('current_mood'),
                'energy': context.get('energy_level'),
                'data_only': True
            }
        }
        
        self.memory.log_interaction(log_entry)
    
    def _calculate_pure_response_difference(self, raw_response, final_response):
        """Calculate response differences with natural variety scoring"""
        try:
            raw_len = len(str(raw_response))
            final_len = len(str(final_response))
            
            raw_words = set(str(raw_response).lower().split())
            final_words = set(str(final_response).lower().split())
            
            # Basic similarity
            if raw_words and final_words:
                overlap = len(raw_words.intersection(final_words))
                union = len(raw_words.union(final_words))
                similarity = overlap / union if union > 0 else 0
            else:
                similarity = 0
            
            # Natural variety scoring (no repetitive patterns)
            final_lower = str(final_response).lower()
            natural_variety = 0
            
            # Check for absence of repetitive patterns
            repetitive_patterns = ['wait', 'hold on', 'hold up', 'you know what']
            pattern_found = any(pattern in final_lower for pattern in repetitive_patterns)
            
            if not pattern_found:
                natural_variety += 0.5
            
            # Lexical diversity
            words = final_lower.split()
            if words:
                unique_ratio = len(set(words)) / len(words)
                natural_variety += unique_ratio * 0.3
            
            # Natural conversation flow
            if not final_lower.startswith(('wait', 'hold', 'you know')):
                natural_variety += 0.2
            
            return {
                'length_difference': final_len - raw_len,
                'length_ratio': final_len / raw_len if raw_len > 0 else 0,
                'word_similarity': similarity,
                'significant_change': similarity < 0.5,
                'natural_variety': min(1.0, natural_variety)
            }
        except Exception as e:
            return {'error': str(e)}

if __name__ == "__main__":
    middleware = ExperientialMiddleware()
    middleware.run_conversation()
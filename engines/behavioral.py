# engines/behavioral.py - V3 with less prescriptive, more inspirational guidance
from datetime import datetime, timedelta
import random

class BehavioralEngine:
    def __init__(self):
        self.conversation_topics = []
        self.topic_performance = {}
        self.initiative_history = []
        self.current_topic = None
        self.topic_start_time = datetime.now()
        self.messages_on_topic = 0
        
        # More balanced behavioral parameters
        self.behavioral_params = {
            'initiative_threshold': 0.35,  # Slightly higher than V2
            'topic_change_frequency': 4,   # Between V1 and V2
            'curiosity_drive': 0.7,        # Maintained
            'empathy_response': 0.6,       # Maintained
            'boredom_tolerance': 0.4       # Slightly higher tolerance
        }
        
        # Less prescriptive action categories - more like suggestions
        self.initiative_suggestions = {
            'gentle': [
                "show_curiosity", "ask_question", "share_perspective"
            ],
            'moderate': [
                "explore_topic", "challenge_gently", "change_direction"
            ],
            'strong': [
                "break_pattern", "be_provocative", "take_lead"
            ]
        }
    
    def analyze_conversation_state(self, recent_messages, emotional_state):
        """Enhanced analysis with less aggressive triggers"""
        
        # Update message count for current topic
        if recent_messages:
            self.messages_on_topic += 1
        
        # Calculate engagement
        avg_engagement = emotional_state.get('engagement_level', 0.5)
        
        # More nuanced boredom calculation
        boredom_level = self._calculate_boredom_level(emotional_state, recent_messages)
        
        # Topic persistence analysis
        topic_persistence = self.messages_on_topic
        time_on_topic = (datetime.now() - self.topic_start_time).seconds / 60
        
        # More nuanced initiative analysis
        initiative_analysis = self._analyze_initiative_needs(
            boredom_level, avg_engagement, topic_persistence, emotional_state
        )
        
        return {
            'avg_engagement': avg_engagement,
            'boredom_level': boredom_level,
            'topic_persistence': topic_persistence,
            'time_since_change': time_on_topic,
            'initiative_recommended': initiative_analysis['needed'],
            'initiative_type': initiative_analysis['type'],
            'initiative_intensity': initiative_analysis['intensity'],
            'conversation_energy': emotional_state.get('energy_level', 0.5),
            'pattern_break_needed': self._detect_repetitive_pattern(recent_messages),
            'behavioral_mode': self._determine_behavioral_mode(emotional_state)
        }
    
    def _calculate_boredom_level(self, emotional_state, recent_messages):
        """More balanced boredom detection"""
        boredom_score = 0.0
        
        # Emotional state boredom (less sensitive)
        engagement = emotional_state.get('engagement_level', 0.5)
        if engagement < 0.4:
            boredom_score += 0.3  # Reduced from 0.4
        elif engagement < 0.6:
            boredom_score += 0.1
        
        # Energy level boredom
        energy = emotional_state.get('energy_level', 0.5)
        if energy < 0.3:
            boredom_score += 0.2
        
        # Message analysis (more balanced)
        if recent_messages:
            recent_lengths = []
            for msg in recent_messages[-3:]:
                content = msg.get('content', '')
                if content:
                    recent_lengths.append(len(content.split()))
            
            if recent_lengths:
                avg_length = sum(recent_lengths) / len(recent_lengths)
                if avg_length < 4:
                    boredom_score += 0.2
                elif avg_length < 6:
                    boredom_score += 0.1
        
        # Topic persistence (more gradual)
        if self.messages_on_topic > self.behavioral_params['topic_change_frequency']:
            excess = self.messages_on_topic - self.behavioral_params['topic_change_frequency']
            boredom_score += min(0.3, excess * 0.1)  # More gradual escalation
        
        # Emotional stagnation
        if emotional_state.get('primary_emotion') in ['bored', 'tired']:
            boredom_score += 0.2
        
        return min(1.0, boredom_score)
    
    def _analyze_initiative_needs(self, boredom_level, engagement, topic_persistence, emotional_state):
        """More nuanced initiative analysis"""
        
        initiative_score = 0.0
        triggers = []
        
        # Boredom trigger (more balanced)
        if boredom_level > 0.5:
            initiative_score += 0.3  # Reduced from 0.4
            triggers.append('MODERATE_BOREDOM')
        elif boredom_level > 0.3:
            initiative_score += 0.15
            triggers.append('MILD_BOREDOM')
        
        # Engagement trigger (more conservative)
        if engagement < self.behavioral_params['initiative_threshold']:
            initiative_score += 0.25
            triggers.append('LOW_ENGAGEMENT')
        
        # Topic persistence (less aggressive)
        if topic_persistence > self.behavioral_params['topic_change_frequency'] * 1.5:
            initiative_score += 0.25
            triggers.append('TOPIC_FATIGUE')
        elif topic_persistence > self.behavioral_params['topic_change_frequency']:
            initiative_score += 0.1
            triggers.append('TOPIC_AGING')
        
        # Emotional state triggers (more nuanced)
        primary_emotion = emotional_state.get('primary_emotion', 'neutral')
        if primary_emotion in ['bored', 'tired']:
            initiative_score += 0.3
            triggers.append('NEGATIVE_EMOTION')
        elif primary_emotion in ['contemplative', 'reflective']:
            initiative_score += 0.1  # Gentle nudge for thoughtful states
            triggers.append('THOUGHTFUL_MOMENT')
        elif primary_emotion == 'neutral' and engagement < 0.5:
            initiative_score += 0.15
            triggers.append('EMOTIONAL_FLATNESS')
        
        # Curiosity-driven actions (more moderate)
        if random.random() < (self.behavioral_params['curiosity_drive'] * 0.1):
            initiative_score += 0.15
            triggers.append('SPONTANEOUS_CURIOSITY')
        
        # Determine initiative type and intensity (more gradual)
        if initiative_score >= 0.5:
            initiative_type = 'strong'
            intensity = min(0.8, initiative_score)  # Cap at 0.8 instead of 0.9
        elif initiative_score >= 0.25:
            initiative_type = 'moderate'
            intensity = initiative_score
        elif initiative_score > 0.05:  # Lower threshold for gentle
            initiative_type = 'gentle'
            intensity = initiative_score
        else:
            initiative_type = 'none'
            intensity = 0
        
        return {
            'needed': initiative_score > 0.05,  # Very low threshold
            'type': initiative_type,
            'intensity': intensity,
            'score': initiative_score,
            'triggers': triggers
        }
    
    def _detect_repetitive_pattern(self, recent_messages):
        """Detect if conversation is stuck in a pattern"""
        if len(recent_messages) < 4:
            return False
        
        # Simple pattern detection - similar message lengths or content
        ai_messages = [msg for msg in recent_messages if msg.get('role') == 'assistant']
        if len(ai_messages) >= 3:
            lengths = [len(msg.get('content', '').split()) for msg in ai_messages[-3:]]
            # If all messages are very similar length, might be pattern
            if max(lengths) - min(lengths) < 5:  # More tolerance
                return True
        
        return False
    
    def _determine_behavioral_mode(self, emotional_state):
        """Determine behavioral mode based on emotional state"""
        emotion = emotional_state.get('primary_emotion', 'neutral')
        energy = emotional_state.get('energy_level', 0.5)
        engagement = emotional_state.get('engagement_level', 0.5)
        
        if emotion in ['contemplative', 'reflective', 'thoughtful']:
            return 'contemplative'
        elif emotion in ['tired'] or energy < 0.3:
            return 'low_energy'
        elif emotion in ['excited'] and energy > 0.7:
            return 'energetic'
        elif engagement > 0.7:
            return 'engaged'
        elif engagement < 0.3:
            return 'disengaged'
        else:
            return 'balanced'
    
    def get_initiative_guidance(self, context):
        """Generate GUIDANCE instead of commands - less prescriptive"""
        
        initiative_type = context.get('initiative_type', 'none')
        behavioral_mode = context.get('behavioral_mode', 'balanced')
        triggers = context.get('initiative_triggers', [])
        
        guidance = []
        
        # Mode-based guidance (inspirational, not commanding)
        if behavioral_mode == 'contemplative':
            guidance.append("MOOD_CONTEMPLATIVE")  # Let Claude interpret this
        elif behavioral_mode == 'low_energy':
            guidance.append("MOOD_LOW_ENERGY")
        elif behavioral_mode == 'energetic':
            guidance.append("MOOD_ENERGETIC")
        elif behavioral_mode == 'disengaged':
            guidance.append("ENGAGEMENT_LOW")
        
        # Initiative-level guidance (suggestive, not commanding)
        if initiative_type == 'strong':
            guidance.append("TAKE_INITIATIVE")  # Generic, let Claude decide how
        elif initiative_type == 'moderate':
            guidance.append("SHOW_INTEREST")
        elif initiative_type == 'gentle':
            guidance.append("BE_CURIOUS")
        
        # Specific situation guidance (still generic)
        if 'TOPIC_FATIGUE' in triggers:
            guidance.append("TOPIC_STALE")
        if 'MODERATE_BOREDOM' in triggers:
            guidance.append("CONVERSATION_STAGNANT")
        if context.get('pattern_break_needed', False):
            guidance.append("BREAK_PATTERN")
        
        return guidance
    
    def learn_from_outcome(self, initiative_taken, engagement_result):
        """More gradual learning with stronger parameter adjustments"""
        
        # Record initiative attempt with more detail
        self.initiative_history.append({
            'timestamp': datetime.now(),
            'initiative_taken': initiative_taken,
            'engagement_result': engagement_result,
            'success': engagement_result > 0.6,
            'strong_success': engagement_result > 0.8
        })
        
        # Keep history manageable
        if len(self.initiative_history) > 20:
            self.initiative_history = self.initiative_history[-10:]
        
        # More gradual parameter adaptation
        if len(self.initiative_history) >= 4:
            recent_initiatives = [h for h in self.initiative_history[-5:] if h['initiative_taken']]
            
            if recent_initiatives:
                success_rate = sum(1 for h in recent_initiatives if h['success']) / len(recent_initiatives)
                
                # More conservative adjustments
                if success_rate > 0.8:
                    # Initiative works very well, be slightly more proactive
                    self.behavioral_params['initiative_threshold'] = min(0.6, 
                        self.behavioral_params['initiative_threshold'] + 0.05)
                elif success_rate < 0.3:
                    # Initiative not working, be more conservative
                    self.behavioral_params['initiative_threshold'] = max(0.2,
                        self.behavioral_params['initiative_threshold'] - 0.05)
    
    def suggest_conversation_actions(self, context):
        """Less prescriptive action suggestions"""
        actions = []
        
        boredom_level = context.get('boredom_level', 0)
        engagement = context.get('avg_engagement', 0.5)
        behavioral_mode = context.get('behavioral_mode', 'balanced')
        
        # Mode-based suggestions (let Claude interpret)
        if behavioral_mode == 'contemplative':
            actions.extend(["thoughtful_question", "deeper_exploration"])
        elif behavioral_mode == 'low_energy':
            actions.extend(["gentle_nudge", "quiet_interest"])
        elif behavioral_mode == 'energetic':
            actions.extend(["enthusiastic_response", "dynamic_question"])
        
        # Situation-based suggestions
        if boredom_level > 0.5:
            actions.extend(["refresh_conversation", "new_perspective"])
        elif engagement < 0.3:
            actions.extend(["spark_interest", "find_connection"])
        
        return actions
    
    def update_topic_tracking(self, new_topic_detected=False, topic_name=None):
        """Enhanced topic tracking with performance metrics"""
        if new_topic_detected:
            # Record performance of previous topic
            if self.current_topic:
                duration = (datetime.now() - self.topic_start_time).seconds / 60
                self.topic_performance[self.current_topic] = {
                    'messages': self.messages_on_topic,
                    'duration_minutes': duration,
                    'last_used': datetime.now(),
                    'engagement_per_message': self.messages_on_topic / max(1, duration),
                    'success_score': max(0, min(1, (self.messages_on_topic - 2) / 5))
                }
            
            # Start tracking new topic
            self.current_topic = topic_name or f"topic_{datetime.now().strftime('%H%M%S')}"
            self.topic_start_time = datetime.now()
            self.messages_on_topic = 0
    
    def get_behavioral_context(self):
        """Enhanced behavioral state for LLM context"""
        recent_success_rate = self._get_recent_success_rate()
        
        return {
            'current_topic': self.current_topic,
            'messages_on_topic': self.messages_on_topic,
            'time_on_topic_minutes': (datetime.now() - self.topic_start_time).seconds / 60,
            'initiative_threshold': self.behavioral_params['initiative_threshold'],
            'recent_initiative_success': recent_success_rate,
            'curiosity_drive': self.behavioral_params['curiosity_drive'],
            'boredom_tolerance': self.behavioral_params['boredom_tolerance'],
            'topic_change_readiness': min(1.0, self.messages_on_topic / self.behavioral_params['topic_change_frequency'])
        }
    
    def _get_recent_success_rate(self):
        """Calculate recent initiative success rate"""
        if len(self.initiative_history) < 2:
            return 0.5  # Default
        
        recent = [h for h in self.initiative_history[-5:] if h['initiative_taken']]
        if not recent:
            return 0.5
        
        return sum(1 for h in recent if h['success']) / len(recent)
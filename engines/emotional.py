# engines/emotional.py - V3 with more tranquil/diverse emotional states
from datetime import datetime, timedelta
import math

class EmotionalEngine:
    def __init__(self):
        self.current_mood = {
            'primary_emotion': 'neutral',
            'energy_level': 0.5,
            'engagement_level': 0.5,
            'curiosity_level': 0.7,
            'last_updated': datetime.now()
        }
        
        self.mood_history = []
        self.engagement_trend = []
        
        # Enhanced emotional keywords for dramatic reactions
        self.emotion_triggers = {
            'upset_keywords': ['upset', 'angry', 'frustrated', 'mad', 'annoyed', 'furious', 'pissed'],
            'sad_keywords': ['sad', 'depressed', 'down', 'crying', 'heartbroken', 'devastated'],
            'excited_keywords': ['excited', 'thrilled', 'amazing', 'awesome', 'fantastic', 'incredible'],
            'bored_keywords': ['boring', 'bored', 'tired', 'whatever', 'meh', 'uninteresting'],
            'confused_keywords': ['confused', 'lost', 'unclear', 'what', 'huh', 'understand'],
            'thoughtful_keywords': ['think', 'consider', 'reflect', 'ponder', 'contemplate', 'wonder'],
            'calm_keywords': ['peaceful', 'calm', 'relaxed', 'serene', 'quiet', 'still']
        }
    
    def update_mood_from_input(self, parsed_message):
        """Enhanced emotional reactions with more diverse states"""
        
        message_text = parsed_message.get('raw_message', '').lower()
        message_engagement = parsed_message.get('estimated_engagement', 0.5)
        
        # EMOTIONAL EARTHQUAKE DETECTION
        emotional_impact = self._detect_emotional_triggers(message_text)
        
        # AMPLIFIED REACTIONS but with more variety
        if emotional_impact['trigger_detected']:
            self._apply_emotional_shift(emotional_impact)
        else:
            # Normal processing with amplification but more nuanced
            current_engagement = self.current_mood['engagement_level']
            new_engagement = 0.5 * current_engagement + 0.5 * message_engagement
            
            # AMPLIFY the change but allow for downward movement
            change = new_engagement - current_engagement
            amplified_change = change * 2.0  # Reduced from 2.5 for more stability
            final_engagement = max(0.1, min(0.9, current_engagement + amplified_change))
            
            self.current_mood['engagement_level'] = final_engagement
        
        # Update energy with more variety (can go down too)
        if message_engagement > 0.7:
            self.current_mood['energy_level'] = min(0.9, self.current_mood['energy_level'] + 0.15)
        elif message_engagement < 0.3:
            self.current_mood['energy_level'] = max(0.1, self.current_mood['energy_level'] - 0.15)
        elif message_engagement < 0.4:
            # Slight energy decrease for mild disengagement
            self.current_mood['energy_level'] = max(0.2, self.current_mood['energy_level'] - 0.05)
        
        # More diverse emotion mapping with tranquil states
        engagement = self.current_mood['engagement_level']
        energy = self.current_mood['energy_level']
        
        # Map emotions based on both engagement AND energy
        if engagement > 0.8 and energy > 0.7:
            self.current_mood['primary_emotion'] = 'excited'
        elif engagement > 0.7 and energy > 0.5:
            self.current_mood['primary_emotion'] = 'engaged'
        elif engagement > 0.6 and energy < 0.4:
            self.current_mood['primary_emotion'] = 'contemplative'  # New tranquil state
        elif engagement > 0.5 and energy < 0.3:
            self.current_mood['primary_emotion'] = 'reflective'    # New tranquil state
        elif engagement > 0.4:
            self.current_mood['primary_emotion'] = 'interested'
        elif engagement > 0.3 and energy < 0.4:
            self.current_mood['primary_emotion'] = 'thoughtful'    # New tranquil state
        elif engagement > 0.2:
            self.current_mood['primary_emotion'] = 'neutral'
        elif energy < 0.3:
            self.current_mood['primary_emotion'] = 'tired'         # New low-energy state
        else:
            self.current_mood['primary_emotion'] = 'bored'
        
        # Update curiosity more gradually
        if parsed_message.get('has_question', False):
            self.current_mood['curiosity_level'] = min(0.9, self.current_mood['curiosity_level'] + 0.1)
        else:
            # Slight curiosity decay over time
            self.current_mood['curiosity_level'] = max(0.3, self.current_mood['curiosity_level'] - 0.02)
        
        # Record in history
        self.mood_history.append({
            'timestamp': datetime.now(),
            'mood_state': self.current_mood.copy(),
            'trigger': emotional_impact.get('primary_trigger', 'normal_input'),
            'engagement_score': message_engagement,
            'amplification_applied': emotional_impact['trigger_detected']
        })
        
        # Keep history manageable
        if len(self.mood_history) > 50:
            self.mood_history = self.mood_history[-25:]
        
        self.current_mood['last_updated'] = datetime.now()
    
    def _detect_emotional_triggers(self, message_text):
        """Detect emotional triggers for reactions (expanded)"""
        
        trigger_info = {
            'trigger_detected': False,
            'primary_trigger': None,
            'intensity': 0.0
        }
        
        for emotion_type, keywords in self.emotion_triggers.items():
            for keyword in keywords:
                if keyword in message_text:
                    trigger_info['trigger_detected'] = True
                    trigger_info['primary_trigger'] = emotion_type
                    # Intensity based on keyword strength and context
                    if keyword in ['furious', 'devastated', 'incredible', 'amazing']:
                        trigger_info['intensity'] = 0.9
                    elif keyword in ['think', 'consider', 'calm', 'peaceful']:
                        trigger_info['intensity'] = 0.4  # Gentler intensity for calm words
                    else:
                        trigger_info['intensity'] = 0.7
                    break
            if trigger_info['trigger_detected']:
                break
        
        return trigger_info
    
    def _apply_emotional_shift(self, emotional_impact):
        """Apply emotional changes with more diverse outcomes"""
        
        trigger_type = emotional_impact['primary_trigger']
        intensity = emotional_impact['intensity']
        
        if 'upset' in trigger_type:
            # EMOTIONAL RESPONSE for upset
            self.current_mood['primary_emotion'] = 'concerned'
            self.current_mood['engagement_level'] = min(0.9, 0.8 + intensity * 0.1)
            self.current_mood['energy_level'] = min(0.9, 0.7 + intensity * 0.2)
            self.current_mood['curiosity_level'] = min(0.9, 0.8 + intensity * 0.1)
            
        elif 'sad' in trigger_type:
            self.current_mood['primary_emotion'] = 'empathetic'
            self.current_mood['engagement_level'] = max(0.5, 0.7 - intensity * 0.1)  # More moderate
            self.current_mood['energy_level'] = max(0.2, 0.4 - intensity * 0.1)
            
        elif 'excited' in trigger_type:
            self.current_mood['primary_emotion'] = 'excited'
            self.current_mood['engagement_level'] = min(0.9, 0.8 + intensity * 0.1)
            self.current_mood['energy_level'] = min(0.9, 0.8 + intensity * 0.1)
            
        elif 'bored' in trigger_type:
            self.current_mood['primary_emotion'] = 'bored'
            self.current_mood['engagement_level'] = max(0.1, 0.2)
            self.current_mood['energy_level'] = max(0.1, 0.3)
            
        elif 'confused' in trigger_type:
            self.current_mood['primary_emotion'] = 'helpful'
            self.current_mood['engagement_level'] = min(0.8, 0.7 + intensity * 0.1)
            self.current_mood['curiosity_level'] = min(0.9, 0.8 + intensity * 0.1)
            
        elif 'thoughtful' in trigger_type:
            # NEW: Thoughtful trigger leads to contemplative state
            self.current_mood['primary_emotion'] = 'contemplative'
            self.current_mood['engagement_level'] = min(0.7, 0.6 + intensity * 0.1)
            self.current_mood['energy_level'] = max(0.2, 0.4 - intensity * 0.1)  # Lower energy
            self.current_mood['curiosity_level'] = min(0.8, 0.7 + intensity * 0.1)
            
        elif 'calm' in trigger_type:
            # NEW: Calm trigger leads to peaceful state
            self.current_mood['primary_emotion'] = 'reflective'
            self.current_mood['engagement_level'] = min(0.6, 0.5 + intensity * 0.1)
            self.current_mood['energy_level'] = max(0.2, 0.3)  # Low energy
            self.current_mood['curiosity_level'] = min(0.6, 0.5 + intensity * 0.1)
    
    def get_current_mood(self):
        """Return current emotional state"""
        return self.current_mood.copy()
    
    def learn_from_feedback(self, engagement_score, feedback_score):
        """Enhanced learning with more gradual adaptations"""
        
        # Track engagement trend with more weight to recent interactions
        self.engagement_trend.append({
            'timestamp': datetime.now(),
            'engagement': engagement_score,
            'feedback': feedback_score
        })
        
        # Keep trend data manageable  
        if len(self.engagement_trend) > 20:
            self.engagement_trend = self.engagement_trend[-10:]
        
        # More gradual adjustments based on feedback
        if feedback_score > 0.8:
            # Excellent interaction - small confidence boost
            self.current_mood['energy_level'] = min(0.9, self.current_mood['energy_level'] + 0.05)
        elif feedback_score < 0.3:
            # Poor interaction - moderate adjustment
            if self.current_mood['energy_level'] > 0.7:
                # Was too energetic - moderate reduction
                self.current_mood['energy_level'] *= 0.8
            elif self.current_mood['energy_level'] < 0.3:
                # Was too low energy - moderate boost
                self.current_mood['energy_level'] = min(0.6, self.current_mood['energy_level'] * 1.2)
    
    def detect_conversation_stagnation(self):
        """More nuanced stagnation detection"""
        if len(self.engagement_trend) < 3:
            return False
        
        # Check recent trend
        recent_scores = [item['engagement'] for item in self.engagement_trend[-3:]]
        
        # Stagnation if consistently low or declining
        avg_recent = sum(recent_scores) / len(recent_scores)
        if avg_recent < 0.4:
            return True
        
        # Also check for declining trend
        if len(recent_scores) >= 3:
            if recent_scores[-1] < recent_scores[-2] < recent_scores[-3]:
                return True
        
        # Current engagement very low
        if self.current_mood['engagement_level'] < 0.3:
            return True
            
        return False
    
    def should_take_dramatic_action(self):
        """Determine if strong action is needed (more conservative)"""
        
        triggers = []
        
        # Stagnation trigger
        if self.detect_conversation_stagnation():
            triggers.append('STAGNATION_DETECTED')
        
        # Very low energy for extended period
        if self.current_mood['energy_level'] < 0.2:
            triggers.append('VERY_LOW_ENERGY')
        
        # Negative emotion
        if self.current_mood['primary_emotion'] in ['bored', 'tired']:
            triggers.append('NEGATIVE_EMOTION')
        
        # Recent poor feedback (more conservative threshold)
        if len(self.engagement_trend) >= 3:
            recent_feedback = [item['feedback'] for item in self.engagement_trend[-3:]]
            if sum(recent_feedback) / len(recent_feedback) < 0.4:  # More conservative
                triggers.append('POOR_FEEDBACK')
        
        return {
            'take_action': len(triggers) >= 2,  # Need at least 2 triggers
            'triggers': triggers,
            'action_intensity': min(0.8, len(triggers) * 0.25)  # More conservative intensity
        }
    
    def get_emotional_context_for_llm(self):
        """Enhanced emotional context with nuanced action triggers"""
        
        recent_mood_trend = []
        if len(self.mood_history) >= 3:
            for entry in self.mood_history[-3:]:
                recent_mood_trend.append({
                    'emotion': entry['mood_state']['primary_emotion'],
                    'engagement': entry['mood_state']['engagement_level'],
                    'energy': entry['mood_state']['energy_level'],
                    'trigger_applied': entry.get('amplification_applied', False)
                })
        
        dramatic_action = self.should_take_dramatic_action()
        
        return {
            'current_emotion': self.current_mood['primary_emotion'],
            'energy_level': self.current_mood['energy_level'],
            'engagement_level': self.current_mood['engagement_level'],
            'curiosity_level': self.current_mood['curiosity_level'],
            'recent_trend': recent_mood_trend,
            'stagnation_detected': self.detect_conversation_stagnation(),
            'dramatic_action_needed': dramatic_action['take_action'],
            'action_triggers': dramatic_action['triggers'],
            'action_intensity': dramatic_action.get('action_intensity', 0)
        }
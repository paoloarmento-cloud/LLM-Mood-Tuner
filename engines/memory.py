# ============================================================================
# engines/memory.py - Memory management with Excel storage
import pandas as pd
from datetime import datetime
import json
from pathlib import Path

class MemoryManager:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.current_state = {}
        self.dna_parameters = {}
        self.experiential_memory = {}
        self._initialize_excel_structure()
    
    def _initialize_excel_structure(self):
        """Create Excel file with proper structure if it doesn't exist"""
        if not Path(self.excel_file).exists():
            # Create initial DNA parameters
            dna_data = {
                'parameter': ['dna_curiosity_level', 'dna_empathy_base', 'dna_humor_level', 
                             'dna_formality_level', 'dna_initiative_threshold'],
                'value': [0.7, 0.6, 0.5, 0.4, 0.6],
                'description': ['How curious and questioning', 'Base empathy level', 
                               'Tendency to use humor', 'How formal vs casual',
                               'Threshold for taking initiative']
            }
            
            # Create initial state
            state_data = {
            'parameter': ['st_current_mood', 'st_conversation_energy', 'st_topic_focus',
                         'st_messages_count', 'st_last_initiative', 'st_boredom_level', 
                         'st_engagement_trend', 'st_initiative_taken'],
            'value': ['neutral', 0.5, 'general', 0, 'never', 0.0, 'stable', False],
            'updated': [datetime.now().isoformat()] * 8
            }
            
            # Create empty experiential memory
            exp_data = {
                'category': [], 'key': [], 'value': [], 
                'confidence': [], 'last_updated': []
            }
            
            # Write to Excel
            with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
                pd.DataFrame(dna_data).to_excel(writer, sheet_name='DNA', index=False)
                pd.DataFrame(state_data).to_excel(writer, sheet_name='Current_State', index=False)  
                pd.DataFrame(exp_data).to_excel(writer, sheet_name='Experience', index=False)
                pd.DataFrame().to_excel(writer, sheet_name='Chat_Log', index=False)  # Empty log
            
            print(f"ðŸ“ Created new memory file: {self.excel_file}")
    
    def load_session_state(self):
        """Load current state from Excel"""
        try:
            # Load DNA parameters
            dna_df = pd.read_excel(self.excel_file, sheet_name='DNA')
            self.dna_parameters = dict(zip(dna_df['parameter'], dna_df['value']))
            
            # Load current state
            state_df = pd.read_excel(self.excel_file, sheet_name='Current_State')
            self.current_state = dict(zip(state_df['parameter'], state_df['value']))
            
            # Load experiential memory
            exp_df = pd.read_excel(self.excel_file, sheet_name='Experience')
            if not exp_df.empty:
                for _, row in exp_df.iterrows():
                    key = f"{row['category']}.{row['key']}"
                    self.experiential_memory[key] = {
                        'value': row['value'],
                        'confidence': row['confidence'],
                        'last_updated': row['last_updated']
                    }
            
            print(f"ðŸ’¾ Loaded session state: {len(self.dna_parameters)} DNA params, {len(self.experiential_memory)} experiences")
            
        except Exception as e:
            print(f"âš ï¸ Error loading session state: {e}")
            self._initialize_excel_structure()
    
    def save_session_state(self):
        """Save current state back to Excel"""
        try:
            with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                # Update current state
                state_data = []
                for param, value in self.current_state.items():
                    state_data.append({
                        'parameter': param,
                        'value': value,
                        'updated': datetime.now().isoformat()
                    })
                pd.DataFrame(state_data).to_excel(writer, sheet_name='Current_State', index=False)
                
                # Update experiential memory
                exp_data = []
                for key, data in self.experiential_memory.items():
                    category, subkey = key.split('.', 1) if '.' in key else ('general', key)
                    exp_data.append({
                        'category': category,
                        'key': subkey,
                        'value': data['value'],
                        'confidence': data['confidence'],
                        'last_updated': data['last_updated']
                    })
                
                if exp_data:
                    pd.DataFrame(exp_data).to_excel(writer, sheet_name='Experience', index=False)
            
            print(f"ðŸ’¾ Session state saved to {self.excel_file}")
            
        except Exception as e:
            print(f"âŒ Error saving session state: {e}")
    
    def get_current_state(self):
        return self.current_state.copy()
    
    def get_dna_parameters(self):
        return self.dna_parameters.copy()
    
    def update_current_state(self, key, value):
        self.current_state[key] = value
    
    def get_user_interests(self):
        """Extract user interests from experiential memory"""
        interests = []
        for key, data in self.experiential_memory.items():
            if key.startswith('user.interest.') and data['confidence'] > 0.6:
                interests.append(data['value'])
        return interests[:5]  # Top 5 interests
    
    def get_successful_topics(self):
        """Get topics that had high engagement"""
        topics = []
        for key, data in self.experiential_memory.items():
            if key.startswith('topic.success.') and data['confidence'] > 0.7:
                topics.append(data['value'])
        return topics[:3]  # Top 3 successful topics
    
    def get_recent_messages(self, limit=5):
        """Get recent conversation context"""
        try:
            chat_df = pd.read_excel(self.excel_file, sheet_name='Chat_Log')
            if chat_df.empty:
                return []
            
            recent = chat_df.tail(limit * 2)  # Get recent user + AI messages
            messages = []
            for _, row in recent.iterrows():
                messages.append({
                    'role': 'user' if 'user_message' in row and pd.notna(row['user_message']) else 'assistant',
                    'content': row.get('user_message', '') or row.get('ai_response', ''),
                    'timestamp': row.get('timestamp', '')
                })
            return messages
            
        except Exception as e:
            print(f"âš ï¸ Error loading recent messages: {e}")
            return []
    
    def get_message_count(self):
        """Get total number of messages in current session"""
        try:
            chat_df = pd.read_excel(self.excel_file, sheet_name='Chat_Log')
            return len(chat_df)
        except:
            return 0
    
    def update_experiential_learning(self, interaction_data):
        """Update experiential memory based on interaction outcome"""
        timestamp = datetime.now().isoformat()
        
        # Update engagement patterns
        engagement_key = f"engagement.score"
        current_engagement = self.experiential_memory.get(engagement_key, {'value': 0.5, 'confidence': 0.1})
        new_engagement = 0.8 * current_engagement['value'] + 0.2 * interaction_data['engagement_score']
        
        self.experiential_memory[engagement_key] = {
            'value': new_engagement,
            'confidence': min(1.0, current_engagement['confidence'] + 0.1),
            'last_updated': timestamp
        }
        
        # Learn user response patterns
        if interaction_data['engagement_score'] > 0.7:
            # This was a good interaction, remember what worked
            response_type = "positive_response" if interaction_data['initiative_taken'] else "good_follow_up"
            key = f"pattern.{response_type}"
            
            pattern_data = self.experiential_memory.get(key, {'value': 0, 'confidence': 0})
            self.experiential_memory[key] = {
                'value': pattern_data['value'] + 1,
                'confidence': min(1.0, pattern_data['confidence'] + 0.05),
                'last_updated': timestamp
            }
    
    def log_interaction(self, log_entry):
        """Append interaction to chat log"""
        try:
            # Read existing log
            try:
                chat_df = pd.read_excel(self.excel_file, sheet_name='Chat_Log')
            except:
                chat_df = pd.DataFrame()
            
            # Append new entry
            new_row = pd.DataFrame([log_entry])
            chat_df = pd.concat([chat_df, new_row], ignore_index=True)
            
            # Save back to Excel
            with pd.ExcelWriter(self.excel_file, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                chat_df.to_excel(writer, sheet_name='Chat_Log', index=False)
                
        except Exception as e:
            print(f"âš ï¸ Error logging interaction: {e}")
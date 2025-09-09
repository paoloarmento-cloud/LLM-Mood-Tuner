# llm_providers/base_provider.py - Abstract LLM interface
from abc import ABC, abstractmethod

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Definisce l'interfaccia standard che tutti i provider devono implementare.
    """
    
    def __init__(self, config):
        """
        Initialize provider with configuration.
        
        Args:
            config (dict): Configuration dictionary containing:
                - provider: string identifier for the provider
                - model: model name/identifier 
                - api_key: API key if required
                - max_tokens: maximum tokens for response
                - temperature: creativity/randomness setting
        """
        self.config = config
        self.context_initialized = False
        self.system_prompt = ""
    
    @abstractmethod
    def initialize_context(self, system_prompt):
        """
        Initialize the LLM with system context/prompt.
        
        Args:
            system_prompt (str): System prompt that sets the AI's behavior and context
        
        This method should:
        - Store the system prompt
        - Set context_initialized to True
        - Perform any provider-specific initialization
        """
        pass
    
    @abstractmethod
    def generate_response(self, context_data):
        """
        Generate response from LLM given context data.
        
        Args:
            context_data (dict): Dictionary containing:
                - user_message: The user's input
                - st_*: Current state parameters
                - exp_*: Experiential memory data
                - dna_*: Personality DNA parameters
                - session_metrics: Current session metrics
        
        Returns:
            dict: Response dictionary with required fields:
                - response_text: The actual response text
                - engagement_analysis: Float 0-1 indicating user engagement
                - boredom_detected: Boolean if conversation seems stale
                - topic_shift_suggestion: String suggesting new direction
                - mood_assessment: String describing interaction mood
                - initiative_taken: Boolean if AI drove the conversation
                - learning_feedback: Dict with response_quality and user_satisfaction_predicted
        """
        pass
    
    @abstractmethod
    def health_check(self):
        """
        Check if the LLM provider is available and working.
        
        Returns:
            bool: True if provider is healthy, False otherwise
        """
        pass
    
    def get_provider_info(self):
        """
        Get information about this provider.
        
        Returns:
            dict: Provider information
        """
        return {
            'provider_type': self.config.get('provider', 'unknown'),
            'model': self.config.get('model', 'unknown'),
            'context_initialized': self.context_initialized,
            'max_tokens': self.config.get('max_tokens', 1000),
            'temperature': self.config.get('temperature', 0.7)
        }
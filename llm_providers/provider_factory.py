# llm_providers/provider_factory.py - Factory for creating LLM providers (semplificato)
from .gpt2_local import GPT2LocalProvider

class LLMProviderFactory:
    @staticmethod
    def create_provider(config):
        """Create appropriate LLM provider based on config"""
        
        provider_type = config.get('provider', 'local')
        
        if provider_type == 'local':
            # print("🔧 Using GPT2 Local Provider (Mock responses)")
            return GPT2LocalProvider(config)
        elif provider_type == 'claude':
            try:
                from .claude_provider import ClaudeProvider
                # print("🔧 Using Claude API Provider")
                return ClaudeProvider(config)
            except ImportError as e:
                print(f"⚠️ Claude provider not available: {e}")
                print("🔄 Falling back to GPT2 Local Provider")
                return GPT2LocalProvider(config)
            except Exception as e:
                print(f"⚠️ Error initializing Claude provider: {e}")
                print("🔄 Falling back to GPT2 Local Provider")
                return GPT2LocalProvider(config)
        else:
            print(f"⚠️ Unknown provider type: {provider_type}")
            print("🔄 Falling back to GPT2 Local Provider")
            return GPT2LocalProvider(config)

# Per aggiungere un nuovo provider:
# 1. Crea un nuovo file (es: openai_provider.py) nella cartella llm_providers/
# 2. Implementa la classe che eredita da BaseLLMProvider
# 3. Aggiungi un elif qui sopra con il nome del provider
# 4. Cambia solo config.py riga 10: "provider": "nome_nuovo_provider"
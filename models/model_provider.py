import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic


def get_google_api_key():
    """Get API key from Colab secrets or fallback"""
    try:
        from google.colab import userdata
        return userdata.get('GOOGLE_API_KEY')
    except:
        # Fallback to environment variable
        return os.getenv('GOOGLE_API_KEY')

class HybridModelProvider:
    """Provides unified interface for Gemini and Claude models"""
    
    def __init__(self):
        self.backend = os.getenv("LLM_BACKEND", "gemini").lower()
        self.model_cache = {}

    def get_llm(self, backend: Optional[str] = None, **kwargs):
        """Get LLM instance based on backend selection"""
        backend = backend or self.backend
        
        if backend == "gemini":
            return self._get_gemini_llm(**kwargs)
        elif backend == "claude":
            return self._get_claude_llm(**kwargs)
        else:
            raise ValueError(f"Unsupported backend: {backend}. Use 'gemini' or 'claude'")

    def _get_gemini_llm(self, **kwargs):
        """Initialize Google Gemini model with Colab secrets support"""
        api_key = get_google_api_key()
        if not api_key:
            raise ValueError("Google API key not found in Colab secrets or environment")
        
        model_name = kwargs.get("model_name", "gemini-2.5-flash")
        temperature = kwargs.get("temperature", 0.1)
        
        print(f"🚀 Loading Gemini model: {model_name}")
        
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            google_api_key=api_key,
            convert_system_message_to_human=True
        )

    def _get_claude_llm(self, **kwargs):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")

        model = kwargs.get("model_name", "claude-3-haiku-20240307")   # safe default
        temperature = kwargs.get("temperature", 0.1)

        # NEVER pass 'tools' here – LangChain adds them later
        return ChatAnthropic(
            anthropic_api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=1024,
        )

# Global instance for easy access
model_provider = HybridModelProvider()

def get_llm(backend: Optional[str] = None, **kwargs):
    """Convenience function to get LLM instance"""
    return model_provider.get_llm(backend, **kwargs)
import abc
from typing import Optional
from src.core.logger import logger
from src.core.config import settings

class LLMClient(abc.ABC):
    @abc.abstractmethod
    def ask_cultural_explanation(self, term: str, context: str) -> str:
        pass

class ClaudeClient(LLMClient):
    def ask_cultural_explanation(self, term: str, context: str) -> str:
        if not settings.ANTHROPIC_API_KEY:
            logger.warning("Claude API Key missing")
            return "Error: No API Key"
        return f"[Claude Explanation for {term} in context {context}]"

class GPT4Client(LLMClient):
    def ask_cultural_explanation(self, term: str, context: str) -> str:
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API Key missing")
            return "Error: No API Key"
        return f"[GPT-4 Explanation for {term} in context {context}]"

class OllamaClient(LLMClient):
    def ask_cultural_explanation(self, term: str, context: str) -> str:
        return f"[Ollama local explanation for {term} in context {context}]"

class LLMManager:
    def __init__(self):
        self.clients = [
            ClaudeClient(),
            GPT4Client(),
            OllamaClient()
        ]

    def get_explanation(self, term: str, context: str) -> str:
        # Fallback chain: Claude -> GPT-4 -> Ollama
        for client in self.clients:
            try:
                result = client.ask_cultural_explanation(term, context)
                if "Error" not in result:
                    return result
            except Exception as e:
                logger.error(f"LLM Client {client.__class__.__name__} failed: {e}")
        
        return "Unable to fetch cultural explanation."

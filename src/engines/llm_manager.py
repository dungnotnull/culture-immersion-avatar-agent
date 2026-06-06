import abc
import asyncio
import json
import httpx
from typing import Optional, List
from anthropic import Anthropic
from openai import OpenAI
from src.core.logger import logger
from src.core.config import settings

class LLMClient(abc.ABC):
    @abc.abstractmethod
    async def ask_cultural_explanation(self, term: str, context: str, country: str = "Japan", genre: str = "Anime") -> str:
        pass

class ClaudeClient(LLMClient):
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def ask_cultural_explanation(self, term: str, context: str, country: str = "Japan", genre: str = "Anime") -> str:
        if not settings.ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API Key missing")

        prompt = (
            f"System: You are a Regional Cultural Encyclopedia Expert with deep knowledge of {country} popular culture, "
            f"history, language, and subcultures. You are watching {genre} content together with the viewer.\n"
            f"Task: Explain the cultural significance of '{term}' in 2-3 sentences.\n"
            f"Context: '{context}'\n"
            f"Include: (1) literal meaning, (2) cultural layer/connotation, (3) why it matters in this scene."
        )
        
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude API Error: {e}")
            return f"Error fetching explanation from Claude: {e}"

class OpenAIClient(LLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def ask_cultural_explanation(self, term: str, context: str, country: str = "Japan", genre: str = "Anime") -> str:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API Key missing")

        prompt = (
            f"You are a Regional Cultural Encyclopedia Expert. Explain the cultural significance "
            f"of '{term}' in 2-3 sentences based on this context: '{context}'. "
            f"Mention the literal meaning, cultural connotation, and relevance to the scene."
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "You are a cultural expert."},
                          {"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return f"Error fetching explanation from OpenAI: {e}"

class OllamaClient(LLMClient):
    async def ask_cultural_explanation(self, term: str, context: str, country: str = "Japan", genre: str = "Anime") -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.OLLAMA_HOST}/api/generate",
                    json={
                        "model": "mistral",
                        "prompt": f"Explain the cultural term '{term}' in the context of {country} {genre}: {context}",
                        "stream": False
                    }
                )
                result = response.json()
                return result.get("response", "Ollama could not provide an explanation.")
        except Exception as e:
            logger.error(f"Ollama API Error: {e}")
            return f"Error fetching explanation from local Ollama: {e}"

class LLMManager:
    def __init__(self):
        self.clients: List[LLMClient] = []
        
        # Build chain based on key availability
        if settings.ANTHROPIC_API_KEY:
            self.clients.append(ClaudeClient())
        if settings.OPENAI_API_KEY:
            self.clients.append(OpenAIClient())
        self.clients.append(OllamaClient())

    async def get_explanation(self, term: str, context: str) -> str:
        # Fallback chain logic
        for client in self.clients:
            try:
                explanation = await client.ask_cultural_explanation(term, context)
                if "Error" not in explanation:
                    return explanation
            except Exception as e:
                logger.warning(f"Client {client.__class__.__name__} failed: {e}. Trying next...")
        
        return "Unable to fetch cultural explanation from any backend."

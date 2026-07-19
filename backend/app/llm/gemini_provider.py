from pydantic import BaseModel
from .base import LLMProvider
class GeminiProvider(LLMProvider):
    def generate(self,task:str,output_model:type[BaseModel])->BaseModel:
        raise RuntimeError("Gemini provider requires the optional google-genai adapter; use mock or OpenAI-compatible mode")

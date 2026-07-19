from .base import LLMProvider, OutputT
class GeminiProvider(LLMProvider):
    def generate(self,task:str,output_model:type[OutputT])->OutputT:
        raise RuntimeError("Gemini provider requires the optional google-genai adapter; use mock or OpenAI-compatible mode")

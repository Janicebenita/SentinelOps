import json
import os
import httpx
from pydantic import BaseModel, ValidationError
from .base import LLMProvider
class OpenAIProvider(LLMProvider):
    def generate(self,task:str,output_model:type[BaseModel])->BaseModel:
        url=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1").rstrip("/")+"/chat/completions"
        payload={"model":os.getenv("OPENAI_MODEL","gpt-4.1-mini"),"messages":[{"role":"system","content":"Return JSON only matching this schema: "+json.dumps(output_model.model_json_schema())},{"role":"user","content":task}],"response_format":{"type":"json_object"}}
        last:Exception|None=None
        for _ in range(2):
            try:
                response=httpx.post(url,json=payload,headers={"Authorization":f"Bearer {os.environ['OPENAI_API_KEY']}"},timeout=60); response.raise_for_status(); return output_model.model_validate_json(response.json()["choices"][0]["message"]["content"])
            except (ValidationError,KeyError,httpx.HTTPError) as exc: last=exc
        raise ValueError("Model output failed validation twice") from last

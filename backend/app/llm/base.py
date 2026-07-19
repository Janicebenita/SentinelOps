from abc import ABC, abstractmethod
from pydantic import BaseModel
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, task:str, output_model:type[BaseModel])->BaseModel: ...

# LLM抽象层
from config import Config
from prompt import SYSTEM_PROMPT
from openai import OpenAI

class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.API_KEY,
            base_url=Config.BASE_URL
        )
        self.model_name = Config.Model_NAME

    def chat(self, message: str):
    
        # 调用api
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
        )
        return {
            "content": response.choices[0].message.content,
            "token": response.usage.total_tokens
        }

    
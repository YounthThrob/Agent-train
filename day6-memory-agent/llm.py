from openai import OpenAI
from config import Config

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=Config.API_KEY, base_url=Config.BASE_URL)
        self.model = Config.MODE

    def chat(self, messages, temperature=0) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return {
            "content": response.choices[0].message.content,
            "token": response.usage.total_tokens if response.usage else 0
        }
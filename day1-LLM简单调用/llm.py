# LLM抽象层
from config import Config
from prompt import SYSTEM_PROMPT
from openai import OpenAI

class SimpleLLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=Config.API_KEY,
            base_url=Config.BASE_URL
        )
        self.model_name = Config.Model_NAME

    def chat(self,user_input: str):
        """
        模拟一个简单的聊天模型，返回一个固定的响应。
        """
        message =[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
        # 调用api
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0.7,
        )
        return {
            "content": response.choices[0].message.content,
            "raw": message,
            "token": response.usage.total_tokens
        }

    
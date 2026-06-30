from openai import OpenAI
from config import Config
import time
from core.logger import get_logger

logger = get_logger(__name__)

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=Config.API_KEY, base_url=Config.BASE_URL)
        self.model = Config.MODE

    def chat(self, messages, temperature=0) -> str:
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )

            latency = round(time.time() - start_time, 4)
            token_usage = response.usage.total_tokens if response.usage else 0
            content = response.choices[0].message.content

            logger.info(
                f"LLM call success | model: {self.model} | latency: {latency}s | tokens: {token_usage}"
            )
            return{
                "content": content,
                "latency": latency,
                "tokens": token_usage,
                "model": self.model
            }
        except Exception as e:
            latency = round(time.time() - start_time, 4)
            logger.error(
                f"LLM call failed | model: {self.model} | latency: {latency}s | error: {str(e)}"
            )
            raise
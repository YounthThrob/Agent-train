import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # ============== 模型配置 =================
    Model_NAME = os.getenv("Model_NAME")
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
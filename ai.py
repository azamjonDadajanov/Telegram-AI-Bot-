from dotenv import load_dotenv
from google import genai

import os

load_dotenv()

ai = genai.Client(api_key=os.getenv("AI_API_KEY"))
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

KEY = os.getenv("API_KEY")

model= "gemini-2.0-flash"
prompt = "Explain how AI works in a few words"

client = genai.Client(api_key=KEY)

response = client.models.generate_content(
    model, prompt
)
print(response.text)
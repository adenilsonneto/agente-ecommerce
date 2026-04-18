import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

resposta = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="Olá! Responda em português: o que é SQL?"
)

print(resposta.text)
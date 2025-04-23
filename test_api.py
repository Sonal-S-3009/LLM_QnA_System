from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.7
)
try:
    response = llm.invoke("Hello, Gemini!")
    print(response.content)
except Exception as e:
    print(f"API Error: {str(e)}")
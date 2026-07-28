import os
from langchain_google_genai import ChatGoogleGenerativeAI
for model_name in ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-2.0-flash", "gemini-pro", "gemini-2.0-flash-exp"]:
    try:
        llm = ChatGoogleGenerativeAI(model=model_name)
        llm.invoke("Hello")
        print(f"{model_name} works!")
        break
    except Exception as e:
        print(f"{model_name} failed: {e}")

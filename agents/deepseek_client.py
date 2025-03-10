# agents/deepseek_client.py

import os
from dotenv import load_dotenv
import openai

load_dotenv()  # Load environment variables from .env

def deepseek_analyze(prompt):
    """
    Connects to the Deepseek API to analyze the given prompt and returns the generated response.
    """
    try:
        client = openai.OpenAI(
            api_key=os.environ.get("DEEPSEEK_API_KEY"),
            base_url='https://api.deepseek.com',
        )
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes Python code and generates detailed documentation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="deepseek-chat",  # Adjust if needed
            temperature=0.0
        )
        if (response.choices and len(response.choices) > 0 and 
            response.choices[0].message and response.choices[0].message.content):
            return response.choices[0].message.content.strip()
        else:
            return "No documentation generated."
    except Exception as e:
        return f"Error connecting to Deepseek API: {e}"

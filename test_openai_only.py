import openai
import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    print("Testing OpenAI...")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("No API key found in .env")
        return
        
    client = openai.OpenAI(api_key=key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'confirmed' if you can hear me."}],
            max_tokens=10
        )
        print(f"OpenAI Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"OpenAI failed: {e}")

if __name__ == "__main__":
    test_openai()

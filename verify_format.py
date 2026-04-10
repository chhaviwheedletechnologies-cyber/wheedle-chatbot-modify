import requests
import os
from dotenv import load_dotenv

load_dotenv()

def verify_format():
    key = os.getenv("API_KEY_SECRET", "MY_SUPER_SECRET_KEY")
    url = "http://127.0.0.1:5000/chat"
    headers = {"x-api-key": key}
    data = {"message": "What services do you offer?"}
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            reply = response.json().get("reply", "")
            print("\n--- RENDERED OUTPUT START ---")
            print(reply)
            print("--- RENDERED OUTPUT END ---\n")
            print("Raw JSON:", response.text)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == "__main__":
    verify_format()

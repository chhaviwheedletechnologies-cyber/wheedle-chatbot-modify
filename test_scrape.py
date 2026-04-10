import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import openai
import os
from dotenv import load_dotenv

load_dotenv()

from selenium.webdriver.common.by import By # Added import

def test_scrape():
    print("Testing scraping...")
    driver = None # Initialize driver
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Use default installed Chrome if possible, avoiding hardcoded paths that might be wrong
    # chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        url = "https://wheedletechnologies.ai/blog"
        print(f"Visiting {url}...")
        driver.get(url)
        time.sleep(5) # Increased wait time
        
        title = driver.title
        print(f"Page title: {driver.title}")
    
        # Debug: Print all links found
        links = driver.find_elements(By.TAG_NAME, "a")
        print("\n--- Links Found ---")
        for link in links:
            href = link.get_attribute('href')
            text = link.text.strip()
            if href:
                print(f"Text: '{text}' | Href: '{href}'")
        print("-------------------\n")

        print("Scraping successful!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Scraping failed: {e}")
    finally:
        if driver:
            driver.quit()

def test_openai():
    print("\nTesting OpenAI...")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("No API key found.")
        return
        
    client = openai.OpenAI(api_key=key)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"OpenAI Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"OpenAI failed: {e}")

if __name__ == "__main__":
    test_scrape()
    test_openai()

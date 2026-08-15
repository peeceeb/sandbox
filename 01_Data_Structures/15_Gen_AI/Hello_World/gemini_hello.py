import time
from google import genai
from google.genai.errors import ServerError

client = genai.Client()

def generate_text_with_retry():
    for attempt in range(3): # Try up to 3 times
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=["Explain the concept of quantum entanglement in simple terms."]
            )
            print(response.text)
            return
        except ServerError as e:
            if e.code == 503:
                print(f"Server busy (Attempt {attempt + 1}/3). Retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise e # Raise other server errors immediately

generate_text_with_retry()

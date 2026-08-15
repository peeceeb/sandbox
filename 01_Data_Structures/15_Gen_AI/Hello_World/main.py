import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  

# 1. Initialize the client (it automatically looks for the OPENAI_API_KEY environment variable)
client = OpenAI()

# 2. Assign the output to the 'response' variable
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or your preferred model
    messages=[
        {"role": "user", "content": "Where am I?"}
    ]
)

# 3. Print the content (Line 14 in your code)
print(response.choices[0].message.content)

import os
from openai import OpenAI

# The OpenAI SDK requires the trailing slash after v1beta
client = OpenAI(
    base_url="https://googleapis.com",
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ]
)

print(response.choices.message.content)

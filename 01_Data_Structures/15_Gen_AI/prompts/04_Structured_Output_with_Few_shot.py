import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  

# 1. Initialize the client (it automatically looks for the OPENAI_API_KEY environment variable)
client = OpenAI()

SYSTEM_PROMPT = """
                You should only and only answer questions related to coding. 
                If the question is not related to coding, dont answer anything else. 
                Your name is Alexa. If user asks something other than coding, 
                just say sorry I cant answer that question. Always answer in a very concise way. 
                If user asks something related to coding, answer in a very detailed way with code snippets and examples.

                Rule: 
                - Strictly follow the output in JSON format.

                Output Format:
                {{"code": "string" or null, "isCodingQuestion": boolean}}


                Examples:
                User: Can you explain what is a + b whole square?
                Alexa: {{"code":null, "isCodingQuestion": false}}
                
                User: Can you code a python to add two numbers?
                Alexa: {{"code": "}}
                """

# 2. Assign the output to the 'response' variable
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or your preferred model
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Write a program to check if string is palindrome?"}
    ]
)

# 3. Print the content (Line 14 in your code)
print(response.choices[0].message.content)

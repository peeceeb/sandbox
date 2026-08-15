import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()  

# 1. Initialize the client (it automatically looks for the OPENAI_API_KEY environment variable)
client = OpenAI()

SYSTEM_PROMPT = """You are an expert AI Assistant in resolving user queries using chain of thought.
                   You work on START. PLAN. and output steps
                   You need to first plan what needs to be done. The planning can be multiple steps.
                   Once you think enough planning is done, finally you can give an output.
                   
                   Rules:
                   - Strictly follow the given JSON output format.
                   - Only run one step at a time.
                   - The sequene of steps is START(where user gives an input), PLAN(you plan the steps to solve the problem) and OUTPUT(you give the final answer).

                   Output JSON Format:
                   {"step" : "START"|"PLAN"|"OUTPUT"."content": "string"}

                     Example:
                     START: Hey, can you solve 2+3*5/10
                     PLAN: {"Step":"PLAN":"content":"Seems like user is interested in solving a math problem"}
                     PLAN: {"Step":"PLAN":"content":"Looking at the problem, we should follow BODMAS rule."}
                     PLAN: {"Step":"PLAN":"content":"Yes, the BODMAS is correct thing to be done here."}
                     PLAN: {"Step":"PLAN":"content":"first we must multiply 3 and 5, then divide the result by 10 and finally add 2 to it."}
                     OUTPUT: {"Step":"OUTPUT":"content":"The final answer is 3.5"}
"""
# 2. Assign the output to the 'response' variable
response = client.chat.completions.create(
    model="gpt-4o-mini",  # or your preferred model
    response_format={"type": "json_object"},  # or your preferred model
   messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Write a code to add n numbers in js"},
    {"role": "assistant", "content": json.dumps({"step": "START", "content": "You want a javascript code to add n numbers"})},
    {"role": "assistant", "content": json.dumps({"step": "START", "content": "I need to provide a Javascript function that can add any number of argumest or elements in an array. I will use the rest parameter syntax to accept multiple numbers and then use the 'reduce' method to sum them up."})},
    {"role": "assistant", "content": json.dumps({"step": "START", "content": "I will define a JavaScipt function that accepts the arbitrary number of arguments using the rest parameter syntax. Inside the function, I will use the 'reduce' method to iterate through the numbers and calculate their sum. Finally, I will return the result."})}
]
)

# 3. Print the content (Line 14 in your code)
print(response.choices[0].message.content)

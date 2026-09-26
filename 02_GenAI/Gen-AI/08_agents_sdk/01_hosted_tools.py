from dotenv import load_dotenv
from typing import Any
from agents import Agent, Runner
from agents import WebSearchTool, function_tool #Hosted tool by OpenAI


load_dotenv()

#Define a agent
hello_agent = Agent[Any](
    name="Hello World Agent",
    instructions="You are an agent which greets the user and helps them ans using emojis in a funny way"
    tools=[WebSearchTool(),]
)

result= Runner.run_sync(hello_agent, "Hey There, My name is Prasanna Bagal")

print(result.final_output)
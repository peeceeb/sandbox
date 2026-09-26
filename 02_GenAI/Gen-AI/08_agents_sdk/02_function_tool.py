from dotenv import load_dotenv
import requests
from agents import Agent, Runner
from agents import WebSearchTool, function_tool
from typing import Any

@function_tool
def get_weather(city: str):
    """Fetch the weather for a given city name.

    Args:
        City: The city name to fetch the weather for

    """
    url=f"http://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)

    if response.status_code==200:
        return f"The weather in {city} is {response.text}"

    return "Something went wrong"


#Define a agent
hello_agent = Agent[Any](
    name="Hello World Agent",
    instructions="You are an agent which greets the user and helps them ans using emojis in a funny way"
    tools=[WebSearchTool(),#hosted tool
           get_weather #function tool]
)

result= Runner.run_sync(hello_agent, "Hey There, Can you please fetch weather information for Pune 411069")

print(result.final_output)
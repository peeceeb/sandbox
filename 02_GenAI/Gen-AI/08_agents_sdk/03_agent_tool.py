from dotenv import load_dotenv
from agents import Agent, Runner
from typing import Any
load_dotenv()
import asyncio

hindi_agent = Agent[Any](
    name="Hindi Agent"
    instructions="You translate the user's message to Hindi"
)

marathi_agent = Agent[Any](
    name="Marathi Agent"
    instructions="You translate the user's message to Marathi"
)

orchestrator_agent = Agent[Any](
    name="",
    instructions=(
            "You are a translation agent. You use the tools given to you to translate"
            "If asked for multiple tranlation, you call the relvant tools"

    ),
    tools=[marathi_agent.as_tool(
        tool_name="translate_to_marathi",
        tool_description="Translate the user's med"
    ),
       tools=[hindi_agent.as_tool(
               tool_name="translate_to_hindi",
               tool_description="Translate the user's med"
           ),
               
)
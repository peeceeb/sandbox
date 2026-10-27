import asyncio
import os
import sys

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

async def main():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or not groq_api_key.strip():
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to the .env file or set it in the environment."
        )

    client = MultiServerMCPClient(
        {
            "math": {
                "command": sys.executable,
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable-http",
            },
        }
    )

    tools = await client.get_tools()
    model = ChatGroq(model="qwen-qwq-32b", api_key=groq_api_key)

    agent = create_react_agent(
        model=model,
        tools=tools,
    )


    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is (10 + 20) * 3 - 10 / 2 + 5?"}]}
    )

    print("Math Response:", math_response['messages'][-1]['content'])
 
asyncio.run(main())

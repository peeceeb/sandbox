import os
from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.agents.agent import Agent

# 1. Initialize the client targeting your local Llama Stack server
port = os.getenv("LLAMA_STACK_PORT", "8321")
model_name = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
base_url = f"http://localhost:{port}"

client = LlamaStackClient(
    base_url=base_url
)

# 2. Define the Agent targeting your inhouse Qwen model
agent = Agent(
    client,
    model=model_name,
    instructions="You are a helpful, precise in-house system automation agent.",
    tools=[],
)

# 4. Start a new persistent conversation session
try:
    session_id = agent.create_session("inhouse_automation_task")
except Exception as error:
    raise SystemExit(
        f"Could not connect to Llama Stack at {base_url}. "
        "Start the server or set LLAMA_STACK_PORT to the correct port."
    ) from error

print("Agent Created Successfully")
print(f"Session Started. ID: {session_id}\n")

# 5. Execute an agentic turn (Interaction)
user_prompt = "Provide a 3-bullet checklist for deploying a Docker container securely."

print(f"User: {user_prompt}\n")
print("Agent Response:")

# Create a turn and stream the response chunk by chunk
turn_stream = agent.create_turn(
    session_id=session_id,
    messages=[
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    stream=True
)

for chunk in turn_stream:
    event = getattr(chunk, "event", None)
    delta = getattr(event, "delta", None)
    text = getattr(delta, "text", None)
    if text:
        print(text, end="", flush=True)
print("\n")

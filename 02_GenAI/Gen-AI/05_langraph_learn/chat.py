from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai"
)


#Think of a state as a "memory box" for the chatbot
class State(TypedDict):
    messages: Annotated[list, add_messages]
""" 
	"Class State Creates a chatbot memory box."
	"Inside, it creates a field called messages."
	"That field stores a list of message in dictionaries."
	"Whenever new messages arrive, append them instead of replacing the old ones."
"""
"""
# Create a chatbot node that has access to the state and can return response state
# Let say we have initial state as { messages: ["Hey there"] }
# The chatbot node will take the state, process the messages, and return a new state with the response "Hi, This is a message from ChatBot Node".
# Both the input and output will be stored in the state, so the next node can access the updated state and continue the conversation.
# State={"messages": ["Hey there"]} -> chatbot(state) -> State={"messages": ["Hey there", "Hi, This is a message from ChatBot Node"]}
"""
def chatbot(state: State):
    print("\n\nInside chatbot node", state)
    return { "messages": ["Hi, This is a message from ChatBot Node"] }

def samplenode(state: State):
    print("\n\nInside samplenode node", state)
    return { "messages": ["Sample Message Appended"] }
"""
#Think of StateGraph as the manager of your chatbot workflow.
When you write:
graph_builder = StateGraph(State)
you're telling LangGraph:
Build a workflow where every step (node) shares and updates this State memory."
So every node can:
	• 📖 Read from messages
	• ✍️ Add new messages
	• 📦 Pass the updated memory to the next node
"""
graph_builder = StateGraph(State)

#Hey manager/graph_builder, can you please register the nodes in the workflow? We have two nodes: "chatbot" and "samplenode". Each node will take the current state, process it, and return an updated state. Let's add them to the graph.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)

#Hey builder can you please add edge for me
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

#Finally, please compile the graph so that it can be executed. This will create a workflow where the state is passed from one node to the next, allowing for a seamless conversation flow.
graph = graph_builder.compile()


#I am invoking the graph and  passing the initial state to the graph and invoking it. The graph will process the state through the nodes in the order defined by the edges, and return the final updated state.
updated_state = graph.invoke(State({"messages": ["What is my name?"]}))
print("\n\nupdated_state", updated_state)

# (START) -> chatbot -> samplenode -> (END)

# state = { messages: ["Hey there"] }
# node runs: chatbot(state: ["Hey There"]) -> ["Hi, This is a message from ChatBot Node"]
# state = { "messages": ["Hey there", "Hi, This is a message from ChatBot Node"]  }
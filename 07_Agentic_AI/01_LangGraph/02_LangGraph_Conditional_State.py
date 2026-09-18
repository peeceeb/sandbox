import operator
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional

load_dotenv()


client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def bot1(state: State):
    print("\n\n Hi I am Bot1...Thinking Now ", state)
    response = client.invoke([
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=state.get("user_query", "")),
    ])

    state["llm_output"] = str(response.content)
    return state

def evaluate_bot1(state: State) -> Literal["chatbot_gemini", "__end__"]:
    print("\n\n Evaluating Bot1 Output... ", state)
    if True:
        state["is_good"] = True

    return "chatbot_gemini"


def chatbot_gemini(state: State):
    print("\n\n Hi I am Chatbot_Gemini...Thinking Now ", state)
    response = client.invoke([
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=state.get("user_query", "")),
    ])
    state["llm_output"] = str(response.content)
    return state

def endnode(state: State):
    print("\n\n Hi I am EndNode...Finalizing Now ", state)
    return state

    
graph_builder = StateGraph(State)

graph_builder.add_node("bot1", bot1)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)
graph_builder.add_node("endnode", endnode)


graph_builder.add_edge(START, "bot1")
graph_builder.add_conditional_edges("bot1", evaluate_bot1)

graph_builder.add_edge("chatbot_gemini", "endnode")
graph_builder.add_edge("endnode", END)


graph = graph_builder.compile()

updated_state =graph.invoke(State({
    "user_query": "What is 493*76?",
    "llm_output": None,
    "is_good": None,
}))

print("\n\n Updated State after Graph Execution:", updated_state)








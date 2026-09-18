import operator
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7)

# 1. Define the State Schema with Reducers
class State(TypedDict):
    # 'add_messages' reducer appends new messages rather than overwriting existing ones
    messages: Annotated[list[BaseMessage], add_messages]
    # 'operator.add' reducer accumulates integer values across node updates
    retry_count: Annotated[int, operator.add]
    # Standard field without reducer gets replaced on update
    status: str


def bot1(state: State):
    response = llm.invoke(state.get("messages"))
    print("\n\n Hi I am Bot1...Thinking Now ", state)
    return {"messages": [response], "retry_count": 1, "status": "bot1_executed"}


def bot2(state: State):
    response = llm.invoke(state.get("messages"))
    print("\n\n Hi I am Bot2...Planning Now ", state)
    return {"messages": [response], "retry_count": 1, "status": "bot2_executed"} 

def bot3(state: State):
    response = llm.invoke(state.get("messages"))
    print("\n\n Hi I am Bot3...Executing Now ", state)
    return {"messages": [response], "retry_count": 1, "status": "bot3_executed"} 

graph_builder = StateGraph(State)

graph_builder.add_node("bot1", bot1)
graph_builder.add_node("bot2", bot2)
graph_builder.add_node("bot3", bot3)

graph_builder.add_edge(START, "bot1")
graph_builder.add_edge("bot1", "bot2")
graph_builder.add_edge("bot2", "bot3")
graph_builder.add_edge("bot3", END)

graph = graph_builder.compile()

updated_state = graph.invoke({
    "messages": [HumanMessage(content="Hi, My name is Prasanna")],
    "retry_count": 0,
    "status": "started",
})
print("\n\n Updated State after Graph Execution:", updated_state)
                       

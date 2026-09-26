from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.graph import END, START, MessagesState, StateGraph

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
)

DB_URI = "mongodb://admin:admin@localhost:27017/?authSource=admin"


class State(MessagesState):
    pass


def chatbot(state: State):
    response = chat_model.invoke(state["messages"])
    return {"messages": [response]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "prasanna"}}

    ask_question = input("Chat with me: ")

    for chunk in graph_with_checkpointer.stream(
        {"messages": [HumanMessage(content=ask_question)]},
        config,
        stream_mode="values",
    ):
        chunk["messages"][-1].pretty_print()

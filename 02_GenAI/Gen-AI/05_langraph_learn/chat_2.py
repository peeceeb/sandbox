# Import environment variable loader to read .env file (e.g., API keys)
from dotenv import load_dotenv
# Import TypedDict for type-safe dictionary definitions
from typing_extensions import TypedDict
# Import typing utilities: Optional (value can be None), Literal (fixed set of values)
from typing import Optional, Literal
# Import LangGraph components: StateGraph (workflow builder), START/END (flow markers)
from langgraph.graph import StateGraph, START, END
# Import OpenAI client for API calls
from openai import OpenAI

# Load environment variables from .env file (contains API keys and credentials)
load_dotenv()

# Initialize OpenAI client (uses OPENAI_API_KEY from environment)
client = OpenAI()

# Define the data structure passed through the workflow graph
# - user_query: the original question from the user
# - llm_output: the AI model's response (optional, set by nodes)
# - is_good: boolean flag to track response quality (optional, for future use)
class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

# First node: Send user query to GPT-4.1-mini model
def chatbot(state: State):
    # Print current state for debugging/monitoring
    print("ChatBot Node", state)
    # Call OpenAI API with GPT-4.1-mini (faster, cheaper model)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",  # Smaller, faster model for initial response
        messages=[
            # Create a message with user's query
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    # Extract the text content from the AI response and store in state
    state["llm_output"] = response.choices[0].message.content
    # Return updated state for next node in workflow
    return state

# Conditional router node: Decides which node to go to next based on response quality
# Returns one of two options: "chatbot_gemini" or "endnode"
def evalaute_response(state: State) -> Literal["chatbot_gemini", "endnode"]:
    # Print state for debugging
    print("evalaute_response Node", state)
    # Check if response meets quality criteria (currently always False)
    if False:
        # If response is bad, skip to end (this condition is never met in current code)
        return "endnode"
    
    # Default: route to Gemini model for a second opinion (better model, slower)
    return "chatbot_gemini"

# Second node: Send user query to GPT-4.1 model (more advanced, used for validation)
def chatbot_gemini(state: State):
    # Print current state for debugging
    print("chatbot_gemini Node", state)
    # Call OpenAI API with GPT-4.1 (more powerful model for refined response)
    response = client.chat.completions.create(
        model="gpt-4.1",  # Larger, more capable model for better quality
        messages=[
            # Create a message with the same user query
            { "role": "user", "content": state.get("user_query") }
        ]
    )

    # Extract the text content from the AI response and store in state (overwrites previous response)
    state["llm_output"] = response.choices[0].message.content
    # Return updated state for next node
    return state

# Final node: Terminal node that marks the end of workflow (passes state through unchanged)
def endnode(state: State):
    # Print final state for debugging
    print("endnode Node", state)
    # Return state as-is to complete the workflow
    return state

# Initialize the workflow graph with State as the shared data structure
graph_builder = StateGraph(State)

# Add nodes to the graph: each node is a function that processes the state
graph_builder.add_node("chatbot", chatbot)  # First LLM call (GPT-4.1-mini)
graph_builder.add_node("chatbot_gemini", chatbot_gemini)  # Second LLM call (GPT-4.1)
graph_builder.add_node("endnode", endnode)  # Final node


# Define the edges (connections between nodes)
# Connect START marker to first node (chatbot runs first)
graph_builder.add_edge(START, "chatbot")
# After chatbot, run the conditional evaluator to choose next path
graph_builder.add_conditional_edges("chatbot", evalaute_response)

# After chatbot_gemini node, always go to endnode
graph_builder.add_edge("chatbot_gemini", "endnode")
# After endnode, workflow ends (go to END marker)
graph_builder.add_edge("endnode", END)

# Compile the graph into an executable workflow
graph = graph_builder.compile()

# Test the workflow: pass a user query and get the final result
# The state flows through: START -> chatbot -> evaluate -> chatbot_gemini -> endnode -> END
updated_state = graph.invoke(State({"user_query": "Hey, Who are the founding fathers of the United States?"}))
# Print the final state with the LLM's response
print(updated_state)
print("Starting w_crew.py imports")
from typing import Dict, TypedDict, Annotated
from langgraph.graph import Graph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY

print(f"Using API key in w_crew: {GOOGLE_API_KEY}")

# Set up Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7
)

# Define state type
class AgentState(TypedDict):
    message: str
    processed_message: str
    wiki_info: str
    final_response: str

# Define processing nodes
def process_message(state: AgentState) -> AgentState:
    response = llm.invoke(f"Extract key meaning from: {state['message']}")
    state['processed_message'] = response.content
    return state

def get_wiki_info(state: AgentState) -> AgentState:
    response = llm.invoke(f"If this contains a famous name, provide a brief bio, otherwise say 'no bio needed': {state['processed_message']}")
    state['wiki_info'] = response.content
    return state

def format_response(state: AgentState) -> AgentState:
    context = f"Message: {state['processed_message']}\nWiki info: {state['wiki_info']}"
    response = llm.invoke(f"Generate a friendly response using this context: {context}")
    state['final_response'] = response.content
    return state

# Create workflow graph
workflow = Graph()

# Add nodes
workflow.add_node("process_message", process_message)
workflow.add_node("get_wiki_info", get_wiki_info)
workflow.add_node("format_response", format_response)

# Define edges
workflow.add_edge("process_message", "get_wiki_info")
workflow.add_edge("get_wiki_info", "format_response")
workflow.add_edge("format_response", END)

# Set entry point
workflow.set_entry_point("process_message")

# Compile graph
whatsapp_crew = workflow.compile()

print("w_crew.py fully loaded")
print("Starting w_crew.py imports")
from typing import Dict, TypedDict
from langgraph.graph import Graph, END
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up HuggingFace client
hf_token = os.getenv('HUGGINGFACE_API_KEY')
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.1",  # Changed model
    token=hf_token
)

# Define preferred models in order of preference
MODELS = [
    "google/flan-t5-large",  # Your original model
    "google/flan-t5-base",   # Fallback option
    "facebook/bart-large-cnn" # Second fallback
]

def generate_text(prompt, max_retries=2):
    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=150,
            temperature=0.7
        )
        return str(response)
    except Exception as e:
        print(f"Error generating text: {e}")
        return "I couldn't process that request at the moment."

print("HuggingFace model configured")

# Define state type
class AgentState(TypedDict):
    message: str
    processed_message: str
    wiki_info: str
    final_response: str

# Define processing nodes
def process_message(state: AgentState) -> AgentState:
    try:
        prompt = f"Extract key meaning from: {state['message']}"
        response = generate_text(prompt)
        state['processed_message'] = response
    except Exception as e:
        print(f"Error in process_message: {e}")
        state['processed_message'] = "Extracted content from user message."
    return state

def get_wiki_info(state: AgentState) -> AgentState:
    try:
        prompt = f"If this contains a famous name, provide a brief bio, otherwise say 'no bio needed': {state['processed_message']}"
        response = generate_text(prompt)
        state['wiki_info'] = response
    except Exception as e:
        print(f"Error in get_wiki_info: {e}")
        state['wiki_info'] = "No additional information needed."
    return state

def format_response(state: AgentState) -> AgentState:
    try:
        context = f"Message: {state['processed_message']}\nWiki info: {state['wiki_info']}"
        prompt = f"Generate a friendly response using this context: {context}"
        response = generate_text(prompt)
        state['final_response'] = response
    except Exception as e:
        print(f"Error in format_response: {e}")
        state['final_response'] = "Thanks for your message! I've processed your request."
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
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get Google API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found in environment variables")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

print(f"API Key loaded and configured: {GOOGLE_API_KEY[:10]}...")

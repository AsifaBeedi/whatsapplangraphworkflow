# marketing_helper.py
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import time
import random
from transformers import pipeline
import openai

# Load environment variables
load_dotenv()

# Get API token from environment variables
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize the Hugging Face inference client
client = InferenceClient(token=HF_TOKEN)

# Initialize the local text generation pipeline once
generator = pipeline("text-generation", model="distilgpt2")


# Template messages for fallback scenarios
FALLBACK_TEMPLATES = [
    "🔥 Special offer! {product} now available at amazing prices! Reply INFO to learn more! #LimitedTimeOffer",
    "✨ Don't miss out on our {product}! Exclusive deals for our WhatsApp customers! Reply YES for details.",
    "👋 Hey there! We've got exciting news about {product}! Check it out now and save big! Reply for details.",
    "⚡ FLASH SALE on {product}! Get yours before they're gone! Reply NOW to claim your discount!"
]

def generate_marketing_text(prompt, max_retries=2):
   
    try:
        result = generator(
            prompt,
            max_new_tokens=60,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=50256
        )
        # Remove the prompt from the output if present
        text = result[0]['generated_text']
        if text.startswith(prompt):
            text = text[len(prompt):].strip()
        return text
    except Exception as e:
        print(f"Error with local model: {str(e)}")
        template = random.choice(FALLBACK_TEMPLATES)
        return template.format(product="our products")

def create_marketing_message(product_info, campaign_type="promotion"):
    prompt = (
        f"Create a short, engaging WhatsApp marketing message for the following product promotion:\n"
        f"Product: {product_info}\n\n"
        "The message should:\n"
        "- Be brief (under 280 characters)\n"
        "- Include emojis\n"
        "- Have a clear call-to-action\n"
        "- Create urgency\n"
        "- Be friendly and exciting"
    )
    # Only return the generated message, not any explanation
    message = generate_marketing_text_groq(prompt)
    # If the model returns extra explanation, keep only the first quoted or first line
    if "\n" in message:
        # Try to extract the first quoted string, else just the first line
        import re
        match = re.search(r'["“](.+?)["”]', message, re.DOTALL)
        if match:
            return match.group(1).strip()
        return message.split('\n')[0].strip()
    return message.strip()

def create_ab_test_variations(product_info, campaign_type="promotion", num_variations=2):
    """Create multiple diverse variations for A/B testing using Groq LLMs"""
    prompts = [
        f"Write a short, urgent WhatsApp marketing message for this product: {product_info}. Use a strong call-to-action, create urgency, and include emojis. Make it sound exciting and exclusive.",
        f"Write a friendly WhatsApp marketing message for this product: {product_info}. Start with a question to spark curiosity, highlight a unique benefit, and include emojis.",
        f"Write a WhatsApp marketing message for this product: {product_info}. Mention how many customers love it (social proof), use a warm tone, and include emojis.",
        f"Write a WhatsApp marketing message for this product: {product_info}. Emphasize a limited-time offer, use a bold statement, and include emojis.",
        f"Write a personalized WhatsApp marketing message for this product: {product_info}. Address the customer directly, make it feel exclusive, and include emojis."
    ]
    variations = []
    for i in range(num_variations):
        prompt = prompts[i % len(prompts)]
        message = generate_marketing_text_groq(prompt)
        variations.append(message)
    return variations

def generate_marketing_text_groq(prompt, model="llama3-8b-8192", max_tokens=120):
    """Generate marketing text using Groq LLMs (Llama-3, Mixtral, Gemma)"""
    if not GROQ_API_KEY:
        print("Groq API key not found.")
        return "API key missing."
    try:
        client = openai.OpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq API error: {e}")
        template = random.choice(FALLBACK_TEMPLATES)
        return template.format(product="our products")

# Testing function
if __name__ == "__main__":
    product = "eco-friendly water bottles that keep drinks cold for 24 hours"
    print("Testing marketing message creation...")
    message = create_marketing_message(product, "promotion")
    print(f"Marketing message: {message}")
    
    print("\nTesting A/B variations...")
    variations = create_ab_test_variations(product, "promotion", 2)
    for i, var in enumerate(variations, 1):
        print(f"Variation {i}: {var}")
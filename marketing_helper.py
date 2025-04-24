# marketing_helper.py
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
import time
import random

# Load environment variables
load_dotenv()

# Get API token from environment variables
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")

# Initialize the Hugging Face inference client
client = InferenceClient(token=HF_TOKEN)

# Define preferred models in order of preference
MARKETING_MODELS = [
    "google/flan-t5-large",  
    "facebook/bart-large-cnn",
    "sshleifer/distilbart-cnn-12-6",
    "google/flan-t5-base"
]

# Template messages for fallback scenarios
FALLBACK_TEMPLATES = [
    "🔥 Special offer! {product} now available at amazing prices! Reply INFO to learn more! #LimitedTimeOffer",
    "✨ Don't miss out on our {product}! Exclusive deals for our WhatsApp customers! Reply YES for details.",
    "👋 Hey there! We've got exciting news about {product}! Check it out now and save big! Reply for details.",
    "⚡ FLASH SALE on {product}! Get yours before they're gone! Reply NOW to claim your discount!"
]

def generate_marketing_text(prompt, max_retries=2):
    """Generate marketing text using Hugging Face models"""
    for retry in range(max_retries):
        for model in MARKETING_MODELS:
            try:
                print(f"Trying marketing model: {model}")
                response = client.text_generation(
                    prompt=prompt,
                    model=model,
                    max_new_tokens=150,
                    temperature=0.8
                )
                return response.strip()
            except Exception as e:
                print(f"Error with model {model}: {str(e)}")
                time.sleep(1)  # Brief pause before trying again
    
    # Return a fallback template if all models fail
    template = random.choice(FALLBACK_TEMPLATES)
    return template.format(product="our products")

def create_marketing_message(product_info, campaign_type="promotion"):
    """Create a marketing message based on product info and campaign type"""
    try:
        # Build prompt based on campaign type
        if campaign_type == "promotion":
            prompt = f"""
            Create a short, engaging WhatsApp marketing message for the following product promotion:
            Product: {product_info}
            
            The message should:
            - Be brief (under 280 characters)
            - Include emojis
            - Have a clear call-to-action
            - Create urgency
            - Be friendly and exciting
            """
        elif campaign_type == "announcement":
            prompt = f"""
            Create a short, engaging WhatsApp announcement message for:
            Product/Service: {product_info}
            
            The message should:
            - Be brief (under 280 characters)
            - Include emojis
            - Build excitement
            - Have a clear next step for customers
            - Sound professional but friendly
            """
        else:  # reminder or default
            prompt = f"""
            Create a short, friendly WhatsApp reminder message about:
            {product_info}
            
            The message should:
            - Be brief (under 280 characters)
            - Include emojis
            - Gently encourage action
            - Be helpful and not pushy
            - Include a simple call-to-action
            """
        
        # Generate the marketing content
        message = generate_marketing_text(prompt)
        
        # Clean up the message (remove quotation marks if present)
        message = message.strip('"\'')
        
        return message
    except Exception as e:
        print(f"Error creating marketing message: {e}")
        template = random.choice(FALLBACK_TEMPLATES)
        return template.format(product=product_info[:20] if product_info else "our products")

def create_ab_test_variations(product_info, campaign_type="promotion", num_variations=2):
    """Create multiple variations for A/B testing"""
    variations = []
    
    # Different emphasis points for variations
    emphasis_points = {
        "promotion": ["price", "limited time", "exclusive deal", "value proposition"],
        "announcement": ["new features", "launch date", "benefits", "excitement"],
        "reminder": ["deadline", "benefits", "simple process", "friendly reminder"]
    }
    
    # Get relevant emphasis points
    points = emphasis_points.get(campaign_type, emphasis_points["promotion"])
    
    # Generate variations
    for i in range(min(num_variations, len(points))):
        try:
            emphasis = points[i]
            prompt = f"""
            Create a short WhatsApp marketing message for {product_info}.
            Campaign type: {campaign_type}
            Emphasize: {emphasis}
            
            The message should be brief, include emojis, and have a clear call-to-action.
            """
            
            message = generate_marketing_text(prompt)
            variations.append(message.strip('"\''))
        except Exception as e:
            print(f"Error creating variation {i+1}: {e}")
            template = random.choice(FALLBACK_TEMPLATES)
            variations.append(template.format(product=product_info[:20] if product_info else "our products"))
    
    return variations

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
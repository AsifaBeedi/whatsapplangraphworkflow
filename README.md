# WhatsApp Marketing Assistant

A Flask-based web application that combines chat assistance and marketing content generation using Groq LLMs (Llama-3, Mixtral, Gemma) and local fallback models. The system supports A/B testing, campaign-specific messaging, and emoji-rich content.

## Features

- **Chat Assistant**: Process and respond to user messages intelligently.
- **Marketing Generator**: Create engaging marketing content with:
  - Campaign-specific messaging
  - A/B test variations (using Groq LLMs for diverse outputs)
  - Emoji-rich content
  - Different campaign types (promotion, announcement, reminder)
- **Local Fallback**: Uses a local model (distilgpt2) if Groq or API-based generation is unavailable.

## Tech Stack

- Python 3.9+
- Flask (Web Framework)
- Groq LLMs via OpenAI-compatible API (`llama3-8b-8192`, `mixtral-8x7b-32768`, etc.)
- Hugging Face Transformers (for local fallback)
- LangGraph (Workflow Orchestration)
- Langchain (AI Framework)
- PyMuPDF (PDF Processing)
- PyTube (YouTube Integration)
- Ngrok (Tunnel Service)
- Docker (Containerization)

## Architecture

The application uses LangGraph to implement an agentic workflow where each step is a specialized agent:

1. **Message Processor Agent**: 
   - Extracts key meaning from input messages
   - Uses LLMs for natural language understanding
   - Identifies key topics and entities

2. **Wiki Info Agent**: 
   - Gathers relevant biographical information if needed
   - Checks for famous names or entities
   - Provides contextual background information

3. **Response Formatter Agent**: 
   - Generates final contextual responses
   - Combines information from previous agents
   - Ensures coherent and helpful responses

4. **Marketing Helper**:
   - Generates marketing messages and A/B test variations using Groq LLMs
   - Falls back to local templates or models if needed

This multi-agent approach allows for:
- Modular processing steps
- Clear separation of concerns
- Easy addition of new capabilities
- Robust error handling

## Project Structure

```
workflow/
├── app.py                # Flask application entry point
├── workflow.py           # LangGraph workflow definitions
├── w_crew.py             # Agent implementations and workflow crew
├── marketing_helper.py   # Marketing content generation (Groq & local)
├── config.py             # Configuration and environment setup
├── pdf_summary.py        # PDF processing utilities
├── youtube.py            # YouTube integration
├── ngrok.py              # Ngrok tunnel setup
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # Project documentation
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/whatsapp-marketing-assistant.git
cd whatsapp-marketing-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here  # (optional, for local fallback)
```

4. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### 1. Process Message
- **URL**: `/process_message`
- **Method**: `POST`
- **Body**:
```json
{
    "message": "Your message here"
}
```

### 2. Generate Marketing Content
- **URL**: `/generate_marketing`
- **Method**: `POST`
- **Body**:
```json
{
    "product_info": "Product description",
    "campaign_type": "promotion"
}
```

## How A/B Testing Works

- The app generates multiple, distinct marketing messages for the same product using Groq LLMs with different prompts (tone, urgency, social proof, etc.).
- If Groq is unavailable, it falls back to local templates or models.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Groq for providing fast, free LLM inference
- Hugging Face for open-source models and tools
- LangGraph for workflow orchestration
- Langchain for the AI framework
- Flask community for the web framework

## Author

Asifa Bandulal Beedi  
- GitHub: [@AsifaBeedi](https://github.com/AsifaBeedi)

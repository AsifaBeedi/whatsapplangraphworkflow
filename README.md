# WhatsApp Marketing Assistant

A Flask-based web application for small business owners to generate, test, and send WhatsApp marketing messages using Groq LLMs (Llama-3, Mixtral, Gemma) and local fallback models. The app supports A/B testing, campaign-specific messaging, emoji-rich content, and direct WhatsApp integration.

---

## Features

- **Marketing Generator**: Create engaging WhatsApp marketing content with:
  - Campaign-specific messaging (promotion, announcement, reminder)
  - A/B test variations (using Groq LLMs for diverse outputs)
  - Emoji-rich, concise messages
  - Direct "Send to WhatsApp" button for easy sharing
- **Chat Assistant**: Powered by Groq LLMs, provides smart, contextual chat responses for business/customer queries.
- **Local Fallback**: Uses a local model (distilgpt2) if Groq or API-based generation is unavailable.

---

## WhatsApp Integration

- After generating a marketing message, a **"Send to WhatsApp"** button appears.
- Clicking the button opens WhatsApp Web (or the app) with the message pre-filled.
- You can optionally set a default phone number or let users enter one.
- This is a manual, privacy-friendly approach—no WhatsApp API approval needed.

---

## Tech Stack

- Python 3.9+
- Flask (Web Framework)
- Groq LLMs via OpenAI-compatible API (`llama3-8b-8192`, `mixtral-8x7b-32768`, etc.)
- Hugging Face Transformers (for local fallback)
- LangGraph (Workflow Orchestration)
- Langchain (AI Framework)
- Docker (optional, for containerization)

---

## Architecture

- **Multi-agent workflow** using LangGraph and Langchain:
  1. **Message Processor Agent**: Extracts meaning and context from user input.
  2. **Wiki Info Agent**: Gathers relevant background info if needed.
  3. **Response Formatter Agent**: Generates final, contextual responses.
  4. **Marketing Helper**: Generates marketing messages and A/B test variations using Groq LLMs, with local fallback.

---

## Project Structure

```
workflow/
├── app.py                # Flask application (UI, API, WhatsApp integration)
├── workflow.py           # LangGraph workflow definitions
├── w_crew.py             # Agent implementations and workflow crew
├── marketing_helper.py   # Marketing content generation (Groq & local)
├── config.py             # Configuration and environment setup
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # Project documentation
```

---

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/YOUR_USERNAME/whatsapp-marketing-assistant.git
    cd whatsapp-marketing-assistant
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Create a `.env` file with your API keys:**
    ```
    GROQ_API_KEY=your_groq_api_key_here
    HUGGINGFACE_API_KEY=your_huggingface_api_key_here  # (optional, for local fallback)
    ```

4. **Run the application:**
    ```sh
    python app.py
    ```
    The server will start at `http://localhost:5000`

---

## Usage

- **Generate Marketing Content:**  
  Enter your product/campaign info, select a campaign type, and click "Generate Marketing Content".  
  Review the generated message and A/B test variations.

- **Send to WhatsApp:**  
  Click the "Send to WhatsApp" button to open WhatsApp Web/app with your message pre-filled.

- **Chat Assistant:**  
  Use the Chat tab to ask business/customer questions and get smart, LLM-powered responses.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details

---

## Acknowledgments

- Groq for providing fast, free LLM inference
- Hugging Face for open-source models and tools
- LangGraph for workflow orchestration
- Langchain for the AI framework
- Flask community for the web framework

---

## Author

Asifa Bandulal Beedi  
- GitHub: [@AsifaBeedi](https://github.com/AsifaBeedi)

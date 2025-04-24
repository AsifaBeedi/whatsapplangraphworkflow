# WhatsApp Marketing Assistant

A Flask-based web application that combines chat assistance and marketing content generation using Hugging Face's AI models.

## Features

- **Chat Assistant**: Process and respond to user messages intelligently
- **Marketing Generator**: Create engaging marketing content with:
  - Campaign-specific messaging
  - A/B test variations
  - Emoji-rich content
  - Different campaign types (promotion, announcement, reminder)

## Tech Stack

- Python 3.9+
- Flask
- Hugging Face AI Models
- LangGraph for workflow management
- HTML/CSS/JavaScript for frontend

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

3. Create a `.env` file with your API key:
```
HUGGINGFACE_API_KEY=your_api_key_here
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

## Project Structure

- `app.py`: Main Flask application
- `w_crew.py`: AI workflow management
- `marketing_helper.py`: Marketing content generation
- `requirements.txt`: Project dependencies

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Google Gemini AI for providing the language model
- LangGraph for the workflow orchestration framework
- Langchain for the AI framework
- Flask community for the web framework

## Author

Asifa Bandulal Beedi
- GitHub: [@AsifaBeedi](https://github.com/AsifaBeedi)
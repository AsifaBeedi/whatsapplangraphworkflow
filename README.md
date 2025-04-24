# AI-Powered Workflow Assistant

A Flask-based application that implements an agentic workflow using LangGraph and Hugging Face to provide intelligent, context-aware responses. The system processes messages through multiple specialized agents to generate comprehensive and contextual responses.

## Features

- Agentic workflow architecture using LangGraph
- Multi-step message processing pipeline:
  - Initial message understanding
  - Context gathering
  - Wiki information lookup
  - Final response formulation
- Message processing with Gemini AI
- PDF text extraction and summarization
- YouTube video search integration
- Ngrok tunnel support for public access
- Dockerized deployment option

## Tech Stack

- Python 3.9+
- Flask (Web Framework)
- LangGraph (Workflow Orchestration)
- Langchain (AI Framework)
- HugingFace -Inference Client(Text Generation)
- PyMuPDF (PDF Processing)
- PyTube (YouTube Integration)
- Ngrok (Tunnel Service)
- Docker (Containerization)

## Architecture

The application uses LangGraph to implement an agentic workflow where each step is a specialized agent:

1. **Message Processor Agent**: 
   - Extracts key meaning from input messages
   - Uses Gemini AI for natural language understanding
   - Identifies key topics and entities

2. **Wiki Info Agent**: 
   - Gathers relevant biographical information if needed
   - Checks for famous names or entities
   - Provides contextual background information

3. **Response Formatter Agent**: 
   - Generates final contextual responses
   - Combines information from previous agents
   - Ensures coherent and helpful responses

This multi-agent approach allows for:
- Modular processing steps
- Clear separation of concerns
- Easy addition of new capabilities
- Robust error handling

## Project Structure

The project structure is organized as follows:
workflow/
├── app.py # Flask application entry point
├── workflow.py # LangGraph workflow definitions
├── w_crew.py # Agent implementations and workflow crew
├── config.py # Configuration and environment setup
├── pdf_summary.py # PDF processing utilities
├── youtube.py # YouTube integration
├── ngrok.py # Ngrok tunnel setup
├── Dockerfile # Docker configuration
├── requirements.txt # Python dependencies
└── .env.example # Example environment variables


## Setup

1. Clone the repository:

bash
git clone https://github.com/yourusername/workflow.git
cd workflow

2. Create and activate virtual environment:

bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:

bash
pip install -r requirements.txt


4. Set up environment variables:
bash
cp .env.example .env

Edit .env and add your Google API key

5. Run the application:

bash
python app.py


## API Endpoints

### Process Message
- **URL**: `/`
- **Method**: `POST`
- **Body**:

json
{
"message": "Your message here"
}
- **Response**:
json
{
"response": "AI-generated response with context"
}

## Environment Variables

Required environment variables:
GOOGLE_API_KEY=your-gemini-api-key-here


## Docker Deployment

Build and run with Docker:
bash
docker build -t workflow .
docker run -p 5000:5000 workflow


## Development

The workflow is built using LangGraph's agentic framework:

1. **State Management**:
python
class AgentState(TypedDict):
message: str
processed_message: str
wiki_info: str
final_response: str


2. **Agent Functions**:
- `process_message`: Initial message processing
- `get_wiki_info`: Biographical information lookup
- `format_response`: Final response generation

3. **Workflow Graph**:
- Sequential processing through agents
- Error handling at each step
- State management between steps

## Error Handling

The application includes robust error handling:
- API key validation
- Request validation
- Agent processing errors
- Response formatting errors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the language model
- LangGraph for the workflow orchestration framework
- Langchain for the AI framework
- Flask community for the web framework

## Author

Asifa Bandulal Beedi
- GitHub: [@AsifaBeedi](https://github.com/AsifaBeedi)

FastAPI Local AI Server with Ollama
![alt text](https://img.shields.io/badge/Python-3.9+-blue.svg)

![alt text](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)

![alt text](https://img.shields.io/badge/Ollama-ready-lightgrey.svg)

![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)
This project provides a ready-to-use backend server built with FastAPI to serve powerful AI models locally using Ollama. It exposes a set of RESTful APIs for various AI tasks, turning your local machine into a personal AI powerhouse.
✨ Features
💬 Conversational AI: A chat endpoint powered by Google's Gemma 2 model.
📝 RAG Document Search: Upload documents and ask questions about their content using Retrieval-Augmented Generation.
🖼️ Image Understanding: Describe the content of any image using the LLaVA multi-modal model.
📹 Video Understanding: (Advanced) Analyze video frames to generate a summary.
💻 Code Review: Get instant feedback and suggestions on your code snippets.
🏛️ Architecture
The system is composed of three main parts:
Ollama: The engine running in the background on your machine. It serves the LLMs (gemma2) and Multi-modal Models (llava) via a local REST API on port 11434.
FastAPI Application: Our Python backend. It exposes several endpoints (e.g., /chat, /describe-image, /query-document). When a request hits an endpoint, our FastAPI code calls the Ollama service to perform the AI task.
Client/API Docs: You can interact with the server through any HTTP client or the built-in interactive documentation provided by FastAPI.
🚀 Getting Started
Follow these steps to get the project up and running on your local machine.
1. Prerequisites: Install Ollama & Models
This part is crucial and ensures your AI models are ready to be served.
Install Ollama: Go to ollama.com and install the application for your OS (Windows, macOS, Linux).
Pull Required Models: Open your terminal (or Command Prompt) and pull the necessary models. We'll need one for text, one for vision, and one for embeddings (for document search).
Generated bash
# Pull Google's Gemma 2 for text generation
ollama pull gemma2

# Pull LLaVA for image understanding
ollama pull llava

# Pull a good embedding model for RAG (Retrieval-Augmented Generation)
ollama pull nomic-embed-text
Use code with caution.
Bash
Verify Installation: You can verify the models are installed with ollama list. Make sure the Ollama application is running in the background.
2. Project Installation
Clone the Repository:
Generated bash
git clone https://github.com/your-username/fast_api_gemini_1.5.git
cd fast_api_gemini_1.5
Use code with caution.
Bash
Create a Virtual Environment:
Generated bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
Use code with caution.
Bash
Install Python Libraries:
Generated bash
pip install -r requirements.txt
Use code with caution.
Bash
(The requirements.txt file contains all necessary libraries like fastapi, uvicorn, ollama, langchain, pypdf, faiss-cpu, and opencv-python).
3. Project Structure
To keep things organized, create the following folders in your project root if they don't exist. The application is designed to use them.
Generated code
/fast_api_gemini_1.5/
|-- venv/
|-- docs/             # Store PDFs for your RAG system here
|-- uploads/          # Temporarily stores uploaded videos
|-- vector_store/     # Saves the generated FAISS vector index
|-- main.py           # Our main FastAPI application file
|-- requirements.txt  # Project dependencies
`-- README.md
Use code with caution.
🏃‍♀️ Running the Application
In your project's root directory, run the following command in your terminal:
Generated bash
uvicorn main:app --reload
Use code with caution.
Bash
main: Refers to the main.py file.
app: Refers to the app = FastAPI() object inside main.py.
--reload: This tells the server to automatically restart whenever you save changes to your code.
The server will be running at http://localhost:8000.
🧪 Testing the API Endpoints
FastAPI automatically generates interactive documentation for you. This is the best way to test your endpoints.
Open your web browser and go to: http://localhost:8000/docs
You will see a beautiful interface where you can:
Expand each endpoint (e.g., /describe-image).
Click "Try it out".
Upload files, enter text, and execute the request directly from your browser.
See the exact response from your API.
Recommended Testing Workflow:
Test /chat:
Expand the /chat endpoint.
Enter a prompt in the request body (e.g., "What is FastAPI?").
Execute and see Gemma2's response.
Test /describe-image:
Expand the /describe-image endpoint.
Click "Try it out".
Upload an image file (.jpg, .png).
Execute and see LLaVA's description of the image.
Test Document RAG:
Step 1: Ingest: Use the /ingest-document endpoint to upload a PDF file from your docs/ folder.
Step 2: Query: Use the /query-document endpoint to ask a question related to the content of the PDF you just uploaded.
Test /summarize-video:
Upload a short video file (.mp4).
Execute the request. Be patient, as this process involves extracting frames and analyzing them one by one, which can take time.

# FastAPI Local AI Server with Ollama

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-ready-lightgrey.svg)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-Apache2.0-yellow.svg)](https://opensource.org/licenses/Apache2.0)
[![Ollama](https://img.shields.io/badge/Ollama-ready-lightgrey.svg)](https://ollama.com/)

This project provides a ready-to-use backend server built with **FastAPI** to serve powerful AI models locally using **Ollama**. It exposes a set of RESTful APIs for various AI tasks, turning your local machine into a personal AI powerhouse.

## ✨ Features

-   💬 **Conversational AI**: A chat endpoint powered by Google's Gemma 3n model.
-   📝 **RAG Document Search**: Upload documents and ask questions about their content using Retrieval-Augmented Generation.
-   🖼️ **Image Understanding**: Describe the content of any image using the Gemma 3n multi-modal model.
-   📹 **Video Understanding**: (Advanced) Analyze video frames to generate a summary.
-   💻 **Code Review**: Get instant feedback and suggestions on your code snippets.

## 🏛️ Architecture

The system is composed of three main parts:

1.  **Ollama**: The engine running in the background on your machine. It serves the LLMs (`Gemma 3n`) and Multi-modal Models (`Gemma 3n`) via a local REST API on port `11434`.
2.  **FastAPI Application**: Our Python backend. It exposes several endpoints (e.g., `/chat`, `/describe-image`, `/query-document`). When a request hits an endpoint, our FastAPI code calls the Ollama service to perform the AI task.
3.  **Client/API Docs**: You can interact with the server through any HTTP client or the built-in interactive documentation provided by FastAPI.

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites: Install Ollama & Models

This part is crucial and ensures your AI models are ready to be served.

1.  **Install Ollama**: Go to [ollama.com](https://ollama.com/) and install the application for your OS (Windows, macOS, Linux).

2.  **Pull Required Models**: Open your terminal (or Command Prompt) and pull the necessary models. We'll need one for text, one for vision, and one for embeddings (for document search).

    ```bash
    # Pull Google's Gemma 2 for text generation
    ollama pull Gemma 3n

    # Pull a good embedding model for RAG (Retrieval-Augmented Generation)
    ollama pull nomic-embed-text
    ```

3.  **Verify Installation**: You can verify the models are installed with `ollama list`. Make sure the Ollama application is running in the background.

### 2. Project Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/Nano-cd/fast_api_gemmman3.git
    cd fast_api_gemmman3
    ```

2.  **Create a Virtual Environment**:
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Python Libraries**:
    ```bash
    pip install -r requirements.txt
    ```
    *(The `requirements.txt` file contains all necessary libraries like fastapi, uvicorn, ollama, langchain, pypdf, faiss-cpu, and opencv-python).*

### 3. Project Structure

To keep things organized, create the following folders in your project root if they don't exist. The application is designed to use them.

```
/fast_api_gemini_1.5/
|-- venv/
|-- docs/             # Store PDFs for your RAG system here
|-- uploads/          # Temporarily stores uploaded videos
|-- vector_store/     # Saves the generated FAISS vector index
|-- main.py           # Our main FastAPI application file
|-- requirements.txt  # Project dependencies
`-- README.md
```

## 🏃‍♀️ Running the Application

In your project's root directory, run the following command in your terminal:

```bash
uvicorn main:app --reload
```

-   `main`: Refers to the `main.py` file.
-   `app`: Refers to the `app = FastAPI()` object inside `main.py`.
-   `--reload`: This tells the server to automatically restart whenever you save changes to your code.

The server will be running at `http://localhost:8000`.

## 🧪 Testing the API Endpoints

FastAPI automatically generates interactive documentation for you. This is the best way to test your endpoints.

**Open your web browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)**

You will see a beautiful interface where you can:
1.  Expand each endpoint (e.g., `/describe-image`).
2.  Click "Try it out".
3.  Upload files, enter text, and execute the request directly from your browser.
4.  See the exact response from your API.

### Recommended Testing Workflow:

1.  **Test `/chat`**:
    -   Expand the `/chat` endpoint.
    -   Enter a prompt in the request body (e.g., `"What is FastAPI?"`).
    -   Execute and see Gemma 3n's response.

2.  **Test `/describe-image`**:
    -   Expand the `/describe-image` endpoint.
    -   Click "Try it out".
    -   Upload an image file (`.jpg`, `.png`).
    -   Execute and see Gemma 3n's description of the image.

3.  **Test Document RAG**:
    -   **Step 1: Ingest**: Use the `/ingest-document` endpoint to upload a PDF file from your `docs/` folder.
    -   **Step 2: Query**: Use the `/query-document` endpoint to ask a question related to the content of the PDF you just uploaded.

4.  **Test `/summarize-video`**:
    -   Upload a **short** video file (`.mp4`).
    -   Execute the request. Be patient, as this process involves extracting frames and analyzing them one by one, which can take time.

## 💻 Code Implementation (`main.py`)

## 📄 License

This project is licensed under the Apache2.0 License. See the `LICENSE` file for details.

@article{gemma_3n_2025,
    title={Gemma 3n},
    url={https://ai.google.dev/gemma/docs/gemma-3n},
    publisher={Google DeepMind},
    author={Gemma Team},
    year={2025}
}

# fast_api_gemman3
用fast-api构建基于gemman3的快速应用：实现功能：1）RAG文档搜索  2）图片理解 3）视频理解 4）代码审查 5）对话

Using FastAPI to build a rapid application based on Gemini 1.5: Implementation features:  RAG document search  Image understanding  Video understanding  Code review  Conversational interaction


FastAPI with Gemini 1.5 & Ollama Integration
This project demonstrates how to build a FastAPI application that leverages Gemini 1.5 models through Ollama for various AI-powered capabilities. The system provides endpoints for document search, image understanding, video analysis, code review, and conversational interactions.

Features
RAG Document Search: Query documents using retrieval-augmented generation

Image Understanding: Get detailed descriptions of images

Video Understanding: Analyze and summarize video content

Code Review: Get AI-powered code analysis and suggestions

Conversational AI: Chat with Gemma 2 model

Architecture Overview
text
┌──────────────────────┐       ┌──────────────────────┐
│                      │       │                      │
│  FastAPI Application ├───────►     Ollama Service   │
│  (main.py)           │       │  (port 11434)        │
│                      ◄───────┤                      │
└──────────▲───────────┘       └──────────────────────┘
           │
           │ HTTP Requests
           │
┌──────────┴───────────┐
│                      │
│    API Client        │
│ (Browser/Postman)    │
│                      │
└──────────────────────┘
Prerequisites
Python 3.9+

Ollama installed (download)

Setup Instructions
1. Install Ollama and Pull Models
bash
# Install Ollama (see official site for OS-specific instructions)
# Then pull required models:

# Text generation model
ollama pull gemma2

# Multi-modal vision model
ollama pull llava

# Embedding model for RAG
ollama pull nomic-embed-text
Verify installation with:

bash
ollama list
2. Create Project and Install Dependencies
bash
# Create project directory
mkdir fastapi_local_ai
cd fastapi_local_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install required packages
pip install fastapi "uvicorn[standard]" ollama langchain langchain_community langchain-ollama pypdf faiss-cpu opencv-python python-multipart
3. Project Structure
Create the following directories:

bash
mkdir -p docs uploads vector_store
Final structure:

text
/fastapi_local_ai/
├── venv/
├── docs/           # For document storage
├── uploads/        # For video uploads
├── vector_store/   # For FAISS vector index
└── main.py         # Main application file
Running the Application
Start the FastAPI server:

bash
uvicorn main:app --reload
Access the interactive API documentation at:
http://localhost:8000/docs

API Endpoints
Endpoint	Method	Description	Parameters
/chat	POST	Chat with Gemma 2	prompt: User message
/describe-image	POST	Analyze an image	image: Image file
/ingest-document	POST	Add document to RAG system	file: PDF file
/query-document	POST	Query documents	question: Your question
/summarize-video	POST	Analyze and summarize video	video: Video file
/review-code	POST	Analyze and review code	code: Code snippet

import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import ollama
import cv2
import base64
import json
import requests


# LangChain components for RAG
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.chains import RetrievalQA

# --- App & Configuration ---
app = FastAPI(
    title="Local AI API with Gemma & Ollama",
    description="An API for interacting with local AI models for text, images, videos, documents, and code review.",
    version="1.1.0" # Version bump!
)

# --- Constants ---
UPLOADS_DIR = "uploads"
DOCS_DIR = "docs"
VECTOR_STORE_PATH = "vector_store"
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)

# --- Pydantic Models for Request Bodies ---
class ChatRequest(BaseModel):
    prompt: str
    model: str = "gemma3n:e4b"

# --- API Endpoints ---

@app.get("/", summary="Root endpoint to check if the API is running.")
def read_root():
    return {"status": "Local AI API is running!"}

# ... (keep all the existing endpoints: /chat, /describe-image, etc.) ...

@app.post("/chat", summary="Chat with a text-based model like gemma3n:e4b.")
async def chat_with_model(request: ChatRequest):
    try:
        response = ollama.chat(
            model=request.model,
            messages=[{'role': 'user', 'content': request.prompt}]
        )
        return {"response": response['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/describe-image", summary="Describe an image using a multimodal model like llava.")
async def describe_image(
    image: UploadFile = File(..., description="Image file to describe."),
    prompt: str = Form("What is in this image?", description="Prompt to guide the description.")
):
    try:
        image_bytes = await image.read()
        response = ollama.chat(
            model='gemma3n:e4b',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [image_bytes]
            }]
        )
        return {"description": response['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- NEW: Code Review Endpoint ---

@app.post("/review-code", summary="Perform an expert code review using gemma3n:e4b.")
async def review_code(
    language: str = Form(..., description="The programming language of the code (e.g., 'python', 'javascript')."),
    code: str = Form(..., description="The code snippet you want to have reviewed.")
):
    """
    Accepts language and code as form data and returns a detailed
    code review from the 'gemma3n:e4b' model.

    This method is robust against multi-line code input.
    """
    # 我们的 prompt 模板需要从 request 对象中获取 language 和 code
    # 但现在它们是直接的函数参数，所以代码更简洁了！
    prompt = f"""
    As an expert senior software engineer, please provide a thorough and constructive code review for the following {language} code.

    Your review should cover the following aspects:
    1.  **Correctness**: Identify any potential bugs, logical errors, or edge cases that are not handled.
    2.  **Best Practices**: Check for adherence to common language-specific conventions and best practices.
    3.  **Readability & Maintainability**: Comment on code clarity, variable naming, function length, and overall structure.
    4.  **Performance**: Point out any potential performance bottlenecks or inefficient code patterns.
    5.  **Security**: Look for common security vulnerabilities (e.g., injection flaws, insecure defaults).

    Provide actionable feedback. For each point, explain the issue and suggest a specific improvement, including a corrected code snippet if applicable.
    Format your entire response in Markdown for better readability.

    --- CODE TO REVIEW ---
    ```
    {code}
    ```
    """
    try:
        response = ollama.chat(
            model='gemma3n:e4b', # Using the specialized model
            messages=[{'role': 'user', 'content': prompt}]
        )
        return {"review": response['message']['content']}
    except Exception as e:
        if "model 'codegemma' not found" in str(e):
            raise HTTPException(
                status_code=404,
                detail="Model 'gemma3n:e4b' not found. Please pull it first by running: ollama pull codegemma"
            )
        raise HTTPException(status_code=500, detail=str(e))


# --- Document and Video Endpoints (No changes needed here) ---

@app.post("/ingest-document", summary="Ingest a PDF document for querying (RAG).")
async def ingest_document(file: UploadFile = File(..., description="PDF document to process.")):
    file_path = os.path.join(DOCS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(VECTOR_STORE_PATH)
        return JSONResponse(content={"message": f"Document '{file.filename}' ingested successfully. You can now query it."}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {e}")

@app.post("/query-document", summary="Query an ingested document using RAG.")
async def query_document(question: str = Form(..., description="Question about the document.")):
    if not os.path.exists(VECTOR_STORE_PATH) or not os.listdir(VECTOR_STORE_PATH):
        raise HTTPException(status_code=404, detail="No document ingested. Please use the /ingest-document endpoint first.")
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        llm = OllamaLLM(model="gemma3n:e4b")
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
        response = qa_chain.invoke(question)
        return {"answer": response['result']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query document: {e}")

@app.post("/summarize-video", summary="Summarize a video by analyzing its frames.")
async def summarize_video(
    video: UploadFile = File(..., description="Video file to summarize."),
    seconds_per_frame: int = Form(5, description="Extract one frame every N seconds.")
):
    video_path = os.path.join(UPLOADS_DIR, video.filename)
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)
    try:
        vidcap = cv2.VideoCapture(video_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frame_descriptions = []
        frame_count = 0
        while vidcap.isOpened():
            success, image = vidcap.read()
            if not success: break
            if frame_count % (int(fps) * seconds_per_frame) == 0:
                _, buffer = cv2.imencode('.jpg', image)
                image_bytes = buffer.tobytes()
                frame_response = ollama.chat(
                    model='gemma3n:e4b', messages=[{'role': 'user', 'content': 'Describe this scene in one sentence.', 'images': [image_bytes]}]
                )
                description = frame_response['message']['content']
                frame_descriptions.append(description)
            frame_count += 1
        vidcap.release()
        os.remove(video_path)
        if not frame_descriptions: return {"summary": "Could not extract any frames from the video."}
        combined_descriptions = "\n".join(frame_descriptions)
        summary_prompt = f"Based on these sequential frame descriptions from a video, provide a concise summary of the video's content:\n\n{combined_descriptions}\n\nSummary:"
        summary_response = ollama.chat(model='gemma3n:e4b', messages=[{'role': 'user', 'content': summary_prompt}])
        return {"summary": summary_response['message']['content'], "frame_descriptions": frame_descriptions}
    except Exception as e:
        if os.path.exists(video_path): os.remove(video_path)
        raise HTTPException(status_code=500, detail=f"Failed to process video: {e}")

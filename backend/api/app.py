# backend/api/app.py

import os
import uvicorn
import logging
from typing import Dict, List, Optional, Any, Union
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import tempfile
import uuid
import json
import time

from model.summarizer import DocumentSummarizer
from utils.file_handler import FileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Document Summarization API",
    description="API for extractive document summarization using TextRank and TF-IDF",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Cache for summarizers
summarizer_cache = {}

# Model classes
class SummarizationRequest(BaseModel):
    text: str
    model_type: str = Field(default="ensemble", description="Summarization model type")
    ratio: float = Field(default=0.3, ge=0.1, le=0.9, description="Target ratio of summary to original text")
    language: str = Field(default="english", description="Language of the text")

class SummarizationResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    compression_ratio: float
    model_used: str
    sentence_count: int
    processing_time: float

class ModelInfo(BaseModel):
    model_type: str
    language: str
    weights: Dict[str, float]
    parameters: Dict[str, Any]

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "api": "Document Summarization API",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "API information"},
            {"path": "/summarize", "method": "POST", "description": "Summarize text"},
            {"path": "/summarize/file", "method": "POST", "description": "Summarize uploaded file"},
            {"path": "/models", "method": "GET", "description": "List available models"},
            {"path": "/models/{model_id}", "method": "GET", "description": "Get model information"}
        ]
    }

def get_summarizer(model_type: str = "ensemble", language: str = "english") -> DocumentSummarizer:
    """
    Get or create a summarizer instance from cache.
    
    Args:
        model_type (str): Type of summarization model
        language (str): Language of the text
        
    Returns:
        DocumentSummarizer: Summarizer instance
    """
    cache_key = f"{model_type}_{language}"
    
    if cache_key not in summarizer_cache:
        # Create a new summarizer
        summarizer = DocumentSummarizer(model_type=model_type, language=language)
        summarizer_cache[cache_key] = summarizer
    
    return summarizer_cache[cache_key]

@app.post("/summarize", response_model=SummarizationResponse)
async def summarize_text(request: SummarizationRequest):
    """
    Summarize text using specified model and parameters.
    
    Args:
        request (SummarizationRequest): Summarization request
        
    Returns:
        SummarizationResponse: Summarization results
    """
    # Get or create summarizer
    summarizer = get_summarizer(request.model_type, request.language)
    
    # Measure processing time
    start_time = time.time()
    
    try:
        # Generate summary
        result = summarizer.summarize(request.text, ratio=request.ratio)
        
        # Add processing time
        result['processing_time'] = time.time() - start_time
        
        return result
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

@app.post("/summarize/file", response_model=SummarizationResponse)
async def summarize_file(
    file: UploadFile = File(...),
    model_type: str = Form("ensemble"),
    ratio: float = Form(0.3),
    language: str = Form("english")
):
    """
    Summarize an uploaded file.
    
    Args:
        file (UploadFile): Uploaded file
        model_type (str): Type of summarization model
        ratio (float): Target ratio of summary to original text
        language (str): Language of the text
        
    Returns:
        SummarizationResponse: Summarization results
    """
    # Measure processing time
    start_time = time.time()
    
    # Save uploaded file to temporary location
    temp_file_path = tempfile.mktemp()
    try:
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Read the file content
        text = FileHandler.read_text_file(temp_file_path)
        
        # Get or create summarizer
        summarizer = get_summarizer(model_type, language)
        
        # Generate summary
        result = summarizer.summarize(text, ratio=ratio)
        
        # Add processing time
        result['processing_time'] = time.time() - start_time
        
        return result
    except Exception as e:
        logger.error(f"File summarization error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"File summarization failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.get("/models", response_model=List[str])
async def list_models():
    """
    List available summarization models.
    
    Returns:
        List[str]: List of available model types
    """
    return ["textrank", "tfidf", "ensemble"]

@app.get("/models/{model_type}", response_model=ModelInfo)
async def get_model_info(model_type: str, language: str = "english"):
    """
    Get information about a specific model.
    
    Args:
        model_type (str): Type of summarization model
        language (str): Language of the model
        
    Returns:
        ModelInfo: Model information
    """
    if model_type not in ["textrank", "tfidf", "ensemble"]:
        raise HTTPException(status_code=404, detail=f"Model {model_type} not found")
    
    # Get or create summarizer
    summarizer = get_summarizer(model_type, language)
    
    # Get model parameters
    textrank_params = summarizer.textrank_summarizer.get_params()
    tfidf_params = summarizer.tfidf_summarizer.get_params()
    
    return {
        "model_type": model_type,
        "language": language,
        "weights": summarizer.model_weights,
        "parameters": {
            "textrank": textrank_params,
            "tfidf": tfidf_params
        }
    }

# @app.post("/benchmark")
# async def benchmark_models(request: SummarizationRequest, background_tasks: BackgroundTasks):
#     """
#     Benchmark different summarization models on the same text.
    
#     Args:
#         request (SummarizationRequest): Summarization request
        
#     Returns:
#         Dict: Benchmark results
#     """
#     models = ["textrank", "tfidf", "ensemble"]
#     results = {}
    
#     for model_type in models:
#         # Get or create summarizer
#         summarizer = get_summarizer(model_type, request.language)
        
#         # Measure processing time
#         start_time = time.time()
        
#         # Generate summary
#         result = summarizer.summarize(request.text, ratio=request.ratio)
        
#         # Add processing time
#         result['processing_time'] = time.time() - start_time
        
#         results[model_type] = result
    
#     return results
@app.post("/summarize/file", response_model=SummarizationResponse)
async def summarize_file(
    file: UploadFile = File(...),
    model_type: str = Form("ensemble"),
    ratio: float = Form(0.3),
    language: str = Form("english")
):
    """
    Summarize an uploaded file.
    
    Args:
        file (UploadFile): Uploaded file
        model_type (str): Type of summarization model
        ratio (float): Target ratio of summary to original text
        language (str): Language of the text
        
    Returns:
        SummarizationResponse: Summarization results
    """
    # Measure processing time
    start_time = time.time()
    
    # Save uploaded file to temporary location
    temp_file_path = tempfile.mktemp(suffix=os.path.splitext(file.filename)[1])
    try:
        logger.info(f"Saving uploaded file to {temp_file_path}")
        content = await file.read()
        with open(temp_file_path, "wb") as f:
            f.write(content)
        
        # Read the file content
        logger.info(f"Reading content from {temp_file_path}")
        text = FileHandler.read_text_file(temp_file_path)
        
        if not text or text.startswith("Error:"):
            raise Exception(f"Failed to extract text from file: {text}")
        
        # Get or create summarizer
        summarizer = get_summarizer(model_type, language)
        
        # Generate summary
        logger.info(f"Generating summary with {model_type} model")
        result = summarizer.summarize(text, ratio=ratio)
        
        # Add processing time
        result['processing_time'] = time.time() - start_time
        
        return result
    except Exception as e:
        logger.error(f"File summarization error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"File summarization failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def start_api_server(host: str = "0.0.0.0", port: int = 8000):
    """
    Start the FastAPI server.
    
    Args:
        host (str): Host to bind the server to
        port (int): Port to bind the server to
    """
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_api_server()
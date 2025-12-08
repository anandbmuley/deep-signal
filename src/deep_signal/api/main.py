from fastapi import FastAPI, File, UploadFile, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import os
import logging
from deep_signal.services.pdf_parser import parse_uploaded_resume, PDFParseException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Deep Signal API",
    description="API for Deep Signal Resume Analysis System",
    version="0.1.0"
)

# Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validates the API key from the header.
    In a real app, this would check against a database or environment variable.
    For MVP, we'll check against a simple env var or allow 'test_key' if not set.
    """
    expected_key = os.getenv("DEEP_SIGNAL_API_KEY", "test_secret_key")
    
    if api_key_header == expected_key:
        return api_key_header
    
    raise HTTPException(
        status_code=403,
        detail="Could not validate credentials"
    )

class ResumeResponse(BaseModel):
    filename: str
    content_length: int
    text_preview: str
    message: str

@app.get("/")
async def root():
    return {"message": "Deep Signal API is running"}

@app.post("/resumes/file", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key)
):
    """
    Upload a resume PDF (multipart/form-data) and get the parsed text.
    """
    logger.info(f"Received file upload: {file.filename}")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        text_content = await parse_uploaded_resume(file)
        
        # Log success (but don't log full content for privacy)
        logger.info(f"Successfully parsed {file.filename}, length: {len(text_content)} chars")
        
        return ResumeResponse(
            filename=file.filename,
            content_length=len(text_content),
            text_preview=text_content[:200] + "..." if len(text_content) > 200 else text_content,
            message="Successfully parsed resume PDF"
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except PDFParseException as pe:
        logger.error(f"PDF Parsing error: {pe}")
        raise HTTPException(status_code=500, detail="Failed to parse PDF file")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import logging
from typing import Optional
import pdfplumber
from pathlib import Path
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class PDFParseException(Exception):
    """Custom exception for PDF parsing errors."""
    pass

def parse_pdf_bytes(file_bytes: bytes) -> str:
    """
    Parses a PDF file from bytes and returns the extracted text.
    
    Args:
        file_bytes: The raw bytes of the PDF file.
        
    Returns:
        The extracting text content.
        
    Raises:
        PDFParseException: If the PDF cannot be processed.
    """
    try:
        from io import BytesIO
        
        text_content = []
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
                    
        return "\n".join(text_content)
        
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}")
        raise PDFParseException(f"Failed to parse PDF: {str(e)}")

async def parse_uploaded_resume(file: UploadFile) -> str:
    """
    Helper to process an uploaded file directly.
    """
    if file.content_type != "application/pdf":
        raise ValueError("File must be a PDF.")
        
    content = await file.read()
    return parse_pdf_bytes(content)

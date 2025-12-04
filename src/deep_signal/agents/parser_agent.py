"""Parser Agent - Extracts structured data from resumes/job descriptions."""

import os
from typing import Dict, Any, List
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import SystemMessage, HumanMessage

from datetime import datetime
from ..state import GraphState
from ..models.candidate import CandidateProfile, Skill
from ..models.state import AgentName
from ..utils.llm import get_llm


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file."""
    try:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        text = "\n\n".join([page.page_content for page in pages])
        return text
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return ""


def parser_agent(state: GraphState) -> Dict[str, Any]:
    """
    Parser Agent - Extracts structured data from resumes/job descriptions.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state dictionary with parsed content
    """
    print("=" * 60)
    print("🔍 PARSER AGENT ACTIVATED")
    print("=" * 60)
    
    input_data = state.get("input_data")
    print(f"Input data: {input_data}")
    
    # Check if input is a valid file
    if not input_data or not os.path.exists(input_data):
        print(f"❌ Input file not found: {input_data}")
        # For demo purposes, if file doesn't exist, we might still want to fail gracefully
        # But if it's the "sample_resume.pdf" string from main.py and it doesn't exist,
        # we should probably warn the user.
        return {
            "parsed_content": None,
            "parse_status": "failed",
            "current_agent": AgentName.PARSER,
            "error": f"Input file not found: {input_data}",
            "messages": [{"role": "system", "content": f"Parser failed: File {input_data} not found"}],
        }

    # 1. Extract Text
    print(f"📄 Extracting text from {input_data}...")
    text_content = extract_text_from_pdf(input_data)
    
    if not text_content:
        return {
            "parsed_content": None,
            "parse_status": "failed",
            "current_agent": AgentName.PARSER,
            "error": "Failed to extract text from PDF",
            "messages": [{"role": "system", "content": "Parser failed: No text extracted"}],
        }
    
    print(f"✅ Extracted {len(text_content)} characters.")
    
    # 2. Structure Data with LLM
    print("🤖 Calling Gemini to structure data...")
    
    try:
        llm = get_llm(temperature=0.0)
        structured_llm = llm.with_structured_output(CandidateProfile)
        
        system_prompt = """You are an expert resume parser. 
        Extract relevant information from the resume text into the structured format.
        Extract Name, Email, and Phone into their respective fields.
        Extract skills, work experience, and education details accurately.
        IMPORTANT: Format all dates as ISO 8601 strings (YYYY-MM-DD). If only month/year is available, use the first day of the month (YYYY-MM-01).
        IMPORTANT: For 'Present' or 'Current' dates, use today's date (2025-12-04)."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Resume Text:\n{text_content}")
        ]
        
        parsed_profile = structured_llm.invoke(messages)
        
        # Enrich with metadata
        if not parsed_profile.metadata:
            parsed_profile.metadata = {}
        parsed_profile.metadata["type"] = "resume"
        parsed_profile.metadata["source"] = "pdf_upload"
        
        print(f"✅ Parsing complete! Created profile for {parsed_profile.name or 'Unknown'}")
        print(f"Document type: {parsed_profile.metadata.get('type', 'resume')}")
        print()
        
        return {
            "parsed_content": parsed_profile,
            "parse_status": "success",
            "current_agent": AgentName.PARSER,
            "messages": [{"role": "system", "content": "Parser agent completed successfully"}],
        }
        
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        return {
            "parsed_content": None,
            "parse_status": "failed",
            "current_agent": AgentName.PARSER,
            "error": str(e),
            "messages": [SystemMessage(content=f"Parser failed: {e}")]
        }

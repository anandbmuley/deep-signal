"""
LLM Utility module for Deep Signal.

This module provides a centralized way to get configured LLM instances.
Currently supports Google Gemini.
"""

import os
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_llm(model_name: str = "gemini-2.5-flash", temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """
    Get a configured instance of Google Gemini.
    
    Args:
        model_name: Name of the Gemini model to use (default: gemini-2.5-flash)
        temperature: Temperature for generation (default: 0.0)
        
    Returns:
        Configured ChatGoogleGenerativeAI instance
        
    Raises:
        ValueError: If GOOGLE_API_KEY is not set in environment
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")
        
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        google_api_key=api_key,
        convert_system_message_to_human=True # Helpful for some Gemini versions
    )
    
    return llm

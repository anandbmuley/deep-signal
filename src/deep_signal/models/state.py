"""State models for the Tri-Agent workflow."""

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class AgentName(str, Enum):
    """Enumeration of agent names."""
    PARSER = "parser"
    ANALYZER = "analyzer"
    MATCHER = "matcher"
    NONE = "none"


class AnalysisOutput(BaseModel):
    """Output from the Analyzer Agent."""
    
    result: Dict[str, Any] = Field(..., description="Full analysis result")
    key_skills: List[str] = Field(default_factory=list, description="Extracted key skills")
    experience_level: str = Field(..., description="Determined experience level")
    status: str = Field("pending", description="Status of analysis")


class MatcherOutput(BaseModel):
    """Output from the Matcher Agent."""
    
    result: Dict[str, Any] = Field(..., description="Full match result")
    score: float = Field(..., description="Overall match score")
    status: str = Field("pending", description="Status of matching")
    top_match: Optional[str] = Field(None, description="Name of the top matching job/candidate")

"""LangGraph State definition for the Tri-Agent workflow."""

from typing import Annotated, TypedDict, Optional, List
from langgraph.graph.message import add_messages


class GraphState(TypedDict):
    """State for the Tri-Agent workflow.
    
    This state is passed between agents in the workflow and maintains
    the complete context of the job matching process.
    """
    
    # Input data
    input_data: str  # Raw input (will be PDF path in the future)
    
    # Parser Agent outputs
    parsed_content: Optional[dict]  # Parsed resume/job data
    parse_status: str  # Status of parsing (success, failed, pending)
    
    # Analyzer Agent outputs
    analysis_result: Optional[dict]  # Analysis of the parsed content
    key_skills: Optional[List[str]]  # Extracted skills
    experience_level: Optional[str]  # Experience level
    analysis_status: str  # Status of analysis
    
    # Matcher Agent outputs
    match_result: Optional[dict]  # Matching results
    match_score: Optional[float]  # Overall match score
    recommendations: Optional[List[str]]  # Recommendations
    match_status: str  # Status of matching
    
    # Workflow control
    messages: Annotated[list, add_messages]  # Conversation history
    current_agent: str  # Currently active agent
    workflow_complete: bool  # Whether the workflow has completed
    error: Optional[str]  # Any error that occurred

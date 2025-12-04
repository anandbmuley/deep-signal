"""LangGraph State definition for the Tri-Agent workflow."""

from typing import Annotated, TypedDict, Optional, List
import operator
from langgraph.graph.message import add_messages
from ..models.candidate import CandidateProfile
from ..models.state import MatcherOutput, AgentName
from ..models.report import AgentReport, AnalysisReport


class GraphState(TypedDict):
    """State for the Tri-Agent workflow.
    
    This state is passed between agents in the workflow and maintains
    the complete context of the job matching process.
    """
    
    # Input data
    input_data: str  # Raw input (will be PDF path in the future)
    
    # Parser Agent outputs
    parsed_content: Optional[CandidateProfile]  # Structured candidate data
    parse_status: str  # Status of parsing (pending, success, failed)
    
    # Agent Report outputs
    skill_decay_report: Optional[AgentReport]  # Output from Skill Decay Agent
    github_report: Optional[AgentReport]  # Output from GitHub Agent
    synthesis_report: Optional[AnalysisReport]  # Output from Synthesis Agent
    
    # Matcher Agent outputs
    matching: Optional[MatcherOutput]  # Structured matching output
    recommendations: Annotated[List[str], operator.add]  # Recommendations (appended by agents)
    
    # Workflow control
    messages: Annotated[list, add_messages]  # Conversation history
    current_agent: AgentName  # Currently active agent
    workflow_complete: bool  # Whether the workflow has completed
    error: Optional[str]  # Any error that occurred

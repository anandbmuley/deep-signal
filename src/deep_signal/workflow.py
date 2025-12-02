"""LangGraph workflow orchestration for the Tri-Agent system."""

from typing import Literal
from langgraph.graph import StateGraph, END
from .state import GraphState
from .agents import parser_agent, analyzer_agent, matcher_agent


def create_workflow() -> StateGraph:
    """
    Creates the LangGraph workflow with the Tri-Agent architecture.
    
    The workflow follows this sequence:
    1. Parser Agent: Parses input documents (PDFs)
    2. Analyzer Agent: Analyzes parsed content
    3. Matcher Agent: Matches against jobs/candidates
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the StateGraph
    workflow = StateGraph(GraphState)
    
    # Add nodes for each agent
    workflow.add_node("parser", parser_agent)
    workflow.add_node("analyzer", analyzer_agent)
    workflow.add_node("matcher", matcher_agent)
    
    # Define the workflow edges (sequential flow)
    workflow.set_entry_point("parser")
    
    # Parser -> Analyzer (conditional on success)
    workflow.add_conditional_edges(
        "parser",
        lambda state: "analyzer" if state["parse_status"] == "success" else "end",
        {
            "analyzer": "analyzer",
            "end": END,
        }
    )
    
    # Analyzer -> Matcher (conditional on success)
    workflow.add_conditional_edges(
        "analyzer",
        lambda state: "matcher" if state["analysis_status"] == "success" else "end",
        {
            "matcher": "matcher",
            "end": END,
        }
    )
    
    # Matcher -> End
    workflow.add_edge("matcher", END)
    
    # Compile the workflow
    return workflow.compile()


def run_workflow(input_data: str) -> dict:
    """
    Execute the Tri-Agent workflow with the given input.
    
    Args:
        input_data: Input data (will be PDF path in the future)
        
    Returns:
        Final state after workflow completion
    """
    print("🚀 Starting Tri-Agent Workflow")
    print("=" * 60)
    print()
    
    # Initialize the state
    initial_state = {
        "input_data": input_data,
        "parsed_content": None,
        "parse_status": "pending",
        "analysis_result": None,
        "key_skills": None,
        "experience_level": None,
        "analysis_status": "pending",
        "match_result": None,
        "match_score": None,
        "recommendations": None,
        "match_status": "pending",
        "messages": [],
        "current_agent": "none",
        "workflow_complete": False,
        "error": None,
    }
    
    # Create and run the workflow
    app = create_workflow()
    
    # Execute the workflow using invoke to get the complete final state
    final_state = app.invoke(initial_state)
    
    print("=" * 60)
    print("✨ Workflow Complete!")
    print("=" * 60)
    
    return final_state

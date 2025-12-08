"""LangGraph workflow orchestration for the Tri-Agent system."""

import os
from langgraph.graph import StateGraph, END
from .state import GraphState
from .models.state import AgentName
from .agents import parser_agent, matcher_agent
from .agents.skill_decay_analysis_agent import skill_decay_agent
from .agents.github_analysis_agent import github_agent
from .agents.synthesis_agent import synthesis_agent


def create_workflow() -> StateGraph:
    """
    Creates the LangGraph workflow with the Tri-Agent architecture.
    
    The workflow follows this sequence:
    1. Parser Agent: Parses input documents (PDFs) and extracts candidate's information
    2. Analysis Phase (Parallel):
       - Skill Decay Agent: Verifies resume skills
       - GitHub Agent: Analyzes GitHub profile
    3. Synthesis Agent: Combines insights into a credit score
    4. Matcher Agent: Matches against jobs/candidates
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Initialize the StateGraph
    workflow = StateGraph(GraphState)
    
    # Add nodes for each agent
    workflow.add_node("parser", parser_agent)
    workflow.add_node("skill_decay", skill_decay_agent)
    workflow.add_node("github", github_agent)
    workflow.add_node("synthesis", synthesis_agent)
    workflow.add_node("matcher", matcher_agent)
    
    # Define the workflow edges
    workflow.set_entry_point("parser")
    
    # Parser -> Skill Decay & GitHub (Parallel)
    # We use conditional edges to route to both if parsing succeeded
    
    def route_after_parser(state):
        if state["parse_status"] == "success":
            return ["skill_decay", "github"]
        return "end"

    workflow.add_conditional_edges(
        "parser",
        route_after_parser,
        {
            "skill_decay": "skill_decay",
            "github": "github",
            "end": END,
        }
    )
    
    # Analysis Agents -> Synthesis
    workflow.add_edge("skill_decay", "synthesis")
    workflow.add_edge("github", "synthesis")
    
    # Synthesis -> Matcher (conditional on success)
    workflow.add_conditional_edges(
        "synthesis",
        lambda state: "matcher" if state.get("synthesis_report") else "end",
        {
            "matcher": "matcher",
            "end": END,
        }
    )
    
    # Matcher -> End
    workflow.add_edge("matcher", END)
    
    # Compile the workflow
    return workflow.compile()


def log_state_update(state: dict):
    """Log relevant state updates based on the current agent."""
    if os.getenv("LOG_WORKFLOW_STATE", "false").lower() == "true":
        # Check for specific agent outputs to log progress
        if state.get("current_agent") == AgentName.PARSER:
             parsed = state.get("parsed_content")
             name = parsed.name if parsed else "Unknown"
             print(f"📋 [State Update] Parser finished. Extracted profile for: {name}")
             
        # Check for parallel agents (they don't update current_agent)
        if state.get("skill_decay_report"):
            score = state["skill_decay_report"].score
            print(f"📋 [State Update] Skill Decay Agent finished. Score: {score}")
            
        if state.get("github_report"):
            score = state["github_report"].score
            print(f"📋 [State Update] GitHub Agent finished. Score: {score}")
            
        if state.get("current_agent") == AgentName.SYNTHESIS:
            report = state.get("synthesis_report")
            score = report.candidate_credit_score if report else 0.0
            print(f"📋 [State Update] Synthesis Agent finished. Credit Score: {score}")

        if state.get("current_agent") == AgentName.MATCHER:
            matching = state.get("matching")
            score = matching.score if matching else 0.0
            print(f"📋 [State Update] Matcher finished. Match Score: {score * 100:.1f}%")


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
        "analysis": None,
        "matching": None,
        "recommendations": [],
        "messages": [],
        "current_agent": AgentName.NONE,
        "workflow_complete": False,
        "error": None,
    }
    
    # Create and run the workflow
    app = create_workflow()
    
    # Execute the workflow using stream to get intermediate states
    final_state = initial_state
    
    # stream_mode="values" returns the full state at each step
    for step_state in app.stream(initial_state, stream_mode="values"):
        # Update final_state with the latest step
        final_state = step_state
        
        # Log the update
        log_state_update(step_state)
    
    print("=" * 60)
    print("✨ Workflow Complete!")
    print("=" * 60)
    
    return final_state

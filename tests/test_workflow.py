"""Tests for the Tri-Agent workflow."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deep_signal.workflow import run_workflow


def test_workflow_completes_successfully():
    """Test that the workflow runs to completion with placeholder agents."""
    input_data = "test_resume.pdf"
    
    # Run the workflow
    final_state = run_workflow(input_data)
    
    # Verify we got output
    assert final_state is not None
    
    # With invoke(), we get the full state directly
    state_data = final_state
    
    # Verify workflow completed
    assert state_data["workflow_complete"] is True
    
    # Verify all agents ran successfully
    assert state_data["parse_status"] == "success"
    assert state_data["analysis_status"] == "success"
    assert state_data["match_status"] == "success"
    
    # Verify no errors occurred
    assert state_data["error"] is None


def test_workflow_has_parsed_content():
    """Test that the parser agent produces output."""
    input_data = "test_resume.pdf"
    final_state = run_workflow(input_data)
    
    state_data = final_state
    
    # Verify parsed content exists
    assert state_data["parsed_content"] is not None
    assert isinstance(state_data["parsed_content"], dict)
    assert "type" in state_data["parsed_content"]


def test_workflow_has_analysis_results():
    """Test that the analyzer agent produces output."""
    input_data = "test_resume.pdf"
    final_state = run_workflow(input_data)
    
    state_data = final_state
    
    # Verify analysis results exist
    assert state_data["analysis_result"] is not None
    assert state_data["key_skills"] is not None
    assert state_data["experience_level"] is not None


def test_workflow_has_match_results():
    """Test that the matcher agent produces output."""
    input_data = "test_resume.pdf"
    final_state = run_workflow(input_data)
    
    state_data = final_state
    
    # Verify match results exist
    assert state_data["match_result"] is not None
    assert state_data["match_score"] is not None
    assert state_data["recommendations"] is not None
    
    # Verify match score is a valid percentage
    assert 0.0 <= state_data["match_score"] <= 1.0

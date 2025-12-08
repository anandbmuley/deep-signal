import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from deep_signal.agents.parser_agent import parser_agent
# from deep_signal.state import GraphState # GraphState is a TypedDict, we can just use a dict

def test_parser_agent():
    # Path to sample resume
    sample_resume_path = os.path.join(os.path.dirname(__file__), "../sample_resume.pdf")
    
    if not os.path.exists(sample_resume_path):
        print(f"Error: {sample_resume_path} does not exist.")
        return

    print(f"Testing parser_agent with {sample_resume_path}")
    
    # Mock state
    state = {
        "input_data": sample_resume_path,
        "parsed_content": None,
        "parse_status": "pending",
        "current_agent": "start",
        "messages": []
    }
    
    # Run agent
    result = parser_agent(state)
    
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    test_parser_agent()

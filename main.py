#!/usr/bin/env python3
"""
Main execution script for the Deep Signal Tri-Agent workflow.

This script demonstrates the "Iron Skeleton" - a complete architecture
with placeholder agents that proves the workflow structure is valid.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deep_signal.workflow import run_workflow
from deep_signal.utils.llm import get_llm


def print_results(final_state: dict):
    """Print the final results from the workflow."""
    print()
    print("📊 FINAL RESULTS")
    print("=" * 60)
    
    # Get the actual state data (now using invoke, so we get the full state directly)
    if final_state:
        state_data = final_state
        
        print(f"Workflow Status: {'✅ Complete' if state_data.get('workflow_complete') else '⚠️  Incomplete'}")
        print()
        
        if state_data.get('error'):
            print(f"❌ Error: {state_data['error']}")
            print()
            return
        
        # Parse results
        if parsed := state_data.get('parsed_content'):
            print("📄 Parsed Content:")
            print(f"   Name: {parsed.get('name')}")
            print(f"   Type: {parsed.get('type')}")
            print(f"   Status: {state_data.get('parse_status')}")
            print()
        
        # Analysis results
        if analysis := state_data.get('analysis_result'):
            print("🧠 Analysis Results:")
            print(f"   Experience Level: {state_data.get('experience_level')}")
            print(f"   Key Skills: {', '.join(state_data.get('key_skills', [])[:3])}...")
            print(f"   Status: {state_data.get('analysis_status')}")
            print()
        
        # Match results
        if match := state_data.get('match_result'):
            print("🎯 Match Results:")
            print(f"   Overall Score: {state_data.get('match_score', 0) * 100:.1f}%")
            print(f"   Top Match: {match['top_matching_jobs'][0]['title']} at {match['top_matching_jobs'][0]['company']}")
            print(f"   Status: {state_data.get('match_status')}")
            print()
            
            if recommendations := state_data.get('recommendations'):
                print("💡 Recommendations:")
                for rec in recommendations[:3]:
                    print(f"   • {rec}")
                print()
    
    print("=" * 60)


def main():
    """Main execution function."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    DEEP SIGNAL                               ║
║         Tri-Agent AI Job Matching Platform                   ║
║                  Iron Skeleton v0.1.0                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    print("This is the Iron Skeleton - proving our architecture works!")
    print("No PDFs will be parsed today. All agents use placeholder logic.")
    print()

    # Verify LLM connection
    print("🤖 Verifying Gemini Connection...")
    try:
        llm = get_llm()
        response = llm.invoke("Say 'Hello from Gemini!' if you can hear me.")
        print(f"✅ Gemini Response: {response.content}")
    except Exception as e:
        print(f"⚠️  Gemini Connection Failed: {e}")
        print("   (Did you set GOOGLE_API_KEY in .env?)")
    print()
    
    # Simulate input data (will be PDF path in the future)
    input_data = "sample_resume.pdf"
    
    try:
        # Run the workflow
        final_state = run_workflow(input_data)
        
        # Print results
        print_results(final_state)
        
        print("🎉 SUCCESS! The Iron Skeleton is complete!")
        print("Architecture validated. Ready for real implementations.")
        
    except Exception as e:
        print(f"❌ Error running workflow: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

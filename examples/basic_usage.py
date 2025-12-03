"""
Basic usage example for DeepSignal.

This example demonstrates how to:
1. Create an anonymized candidate profile (NO PII)
2. Run the DeepSignal analysis
3. Interpret the results
"""

from datetime import datetime, timedelta
import json
import sys
import os

# Add src to path for local development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from deep_signal import DeepSignalOrchestrator, CandidateProfile
from deep_signal.models.candidate import Skill, WorkExperience


def create_sample_candidate() -> CandidateProfile:
    """Create a sample candidate profile with anonymized data."""
    
    # IMPORTANT: Use anonymous identifiers, NO PII
    candidate = CandidateProfile(
        candidate_id="CAND-2024-001",
        github_username="example-developer",  # Public GitHub username is OK
        skills=[
            Skill(
                name="Python",
                proficiency="expert",
                last_used=datetime.utcnow() - timedelta(days=30),
                years_experience=5.0,
            ),
            Skill(
                name="JavaScript",
                proficiency="intermediate",
                last_used=datetime.utcnow() - timedelta(days=60),
                years_experience=3.0,
            ),
            Skill(
                name="Java",
                proficiency="intermediate",
                last_used=datetime.utcnow() - timedelta(days=730),  # 2 years ago
                years_experience=2.0,
            ),
            Skill(
                name="Docker",
                proficiency="intermediate",
                last_used=datetime.utcnow() - timedelta(days=45),
                years_experience=2.5,
            ),
        ],
        work_experience=[
            WorkExperience(
                company="Tech Company A",  # Anonymized
                position="Senior Developer",
                start_date=datetime(2020, 1, 1),
                end_date=datetime(2023, 6, 30),
                skills_used=["Python", "JavaScript", "Docker"],
            ),
            WorkExperience(
                company="Tech Company B",  # Anonymized
                position="Software Engineer",
                start_date=datetime(2023, 7, 1),
                end_date=None,  # Current position
                skills_used=["Python", "Docker"],
            ),
        ],
    )
    
    return candidate


def main():
    """Run the DeepSignal analysis example."""
    
    print("=" * 80)
    print("DeepSignal: Autonomous Tri-Agent AI Screener")
    print("=" * 80)
    print()
    
    # Initialize orchestrator
    # Note: GitHub token can be provided via environment variable GITHUB_TOKEN
    orchestrator = DeepSignalOrchestrator()
    
    # Check agent status
    print("Agent Status:")
    status = orchestrator.get_agent_status()
    for agent_key, agent_info in status.items():
        print(f"  {agent_info['name']}: {agent_info['status']}")
    print()
    
    # Create sample candidate
    print("Creating sample candidate profile...")
    candidate = create_sample_candidate()
    print(f"Candidate ID: {candidate.candidate_id}")
    print(f"Skills: {len(candidate.skills)}")
    print(f"Work Experience: {len(candidate.work_experience)} positions")
    print()
    
    # Run analysis
    print("Running comprehensive analysis...")
    print("-" * 80)
    
    try:
        report = orchestrator.analyze_candidate(candidate)
        
        print("\n" + "=" * 80)
        print("ANALYSIS REPORT")
        print("=" * 80)
        
        # Display credit score
        print(f"\nCandidate Credit Score: {report.candidate_credit_score}/100")
        print(f"Overall Risk Level: {report.overall_risk_level.value.upper()}")
        print()
        
        # Display agent scores
        print("Agent Scores:")
        for agent_name, agent_report in report.agent_reports.items():
            print(f"  {agent_report.agent_name}")
            print(f"    Score: {agent_report.score}/100")
            print(f"    Confidence: {agent_report.confidence}")
            print(f"    Risk Factors: {len(agent_report.risk_factors)}")
        print()
        
        # Display key findings
        print("Key Findings:")
        for i, finding in enumerate(report.key_findings, 1):
            print(f"  {i}. {finding}")
        print()
        
        # Display recommendations
        print("Recommendations:")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"  {i}. {rec}")
        print()
        
        # Display risk factors
        if any(len(r.risk_factors) > 0 for r in report.agent_reports.values()):
            print("Risk Factors Identified:")
            for agent_name, agent_report in report.agent_reports.items():
                if agent_report.risk_factors:
                    print(f"\n  From {agent_report.agent_name}:")
                    for risk in agent_report.risk_factors:
                        print(f"    - [{risk.severity.value.upper()}] {risk.description}")
                        print(f"      Score Impact: {risk.score_impact}")
            print()
        
        # Display detailed signals (optional)
        print("\n" + "=" * 80)
        print("DETAILED SIGNALS (for technical review)")
        print("=" * 80)
        print(json.dumps(
            {k: v.signals for k, v in report.agent_reports.items()},
            indent=2,
            default=str
        ))
        
        print("\n" + "=" * 80)
        print("Analysis complete!")
        print("=" * 80)
        
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("\nPlease ensure candidate profile uses anonymous identifiers only.")
    except Exception as e:
        print(f"\nERROR during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

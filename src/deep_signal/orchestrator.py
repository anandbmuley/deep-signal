"""
DeepSignal Orchestrator.

Coordinates the three AI agents for comprehensive candidate analysis.
Ensures no PII persistence by operating on anonymized data only.
"""

from typing import Optional

from .models.candidate import CandidateProfile
from .models.report import AnalysisReport
from .agents.agent_a_resume import ResumeVerificationAgent
from .agents.agent_b_github import GitHubAnalysisAgent
from .agents.agent_c_synthesis import CreditScoreSynthesizer


class DeepSignalOrchestrator:
    """
    Orchestrator for the DeepSignal Tri-Agent system.
    
    Coordinates Agent A (Resume Verification), Agent B (GitHub Analysis),
    and Agent C (Credit Score Synthesis) to produce comprehensive candidate analysis.
    
    IMPORTANT: This system is designed to work with ANONYMIZED data only.
    No PII (Personally Identifiable Information) should be stored or persisted.
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the DeepSignal orchestrator.
        
        Args:
            github_token: Optional GitHub API token for Agent B analysis
        """
        self.agent_a = ResumeVerificationAgent()
        self.agent_b = GitHubAnalysisAgent(github_token=github_token)
        self.agent_c = CreditScoreSynthesizer()
    
    def analyze_candidate(self, candidate: CandidateProfile) -> AnalysisReport:
        """
        Perform comprehensive candidate analysis using all three agents.
        
        This method:
        1. Runs Agent A to verify resume and calculate skill decay
        2. Runs Agent B to analyze GitHub profile for green-washing
        3. Runs Agent C to synthesize results into a credit score
        
        Args:
            candidate: CandidateProfile with anonymized data (NO PII)
            
        Returns:
            AnalysisReport with comprehensive findings and recommendations
            
        Note:
            The candidate profile should contain only anonymized identifiers.
            This ensures no PII persistence as per system requirements.
        """
        # Validate that candidate is using anonymous ID
        self._validate_no_pii(candidate)
        
        # Execute Agent A: Resume Verification
        resume_report = self.agent_a.analyze(candidate)
        
        # Execute Agent B: GitHub Analysis
        github_report = self.agent_b.analyze(candidate)
        
        # Collect all agent reports
        agent_reports = {
            "resume": resume_report,
            "github": github_report,
        }
        
        # Execute Agent C: Synthesize final score and report
        final_report = self.agent_c.synthesize(candidate, agent_reports)
        
        return final_report
    
    def _validate_no_pii(self, candidate: CandidateProfile) -> None:
        """
        Validate that candidate profile contains no obvious PII.
        
        This is a basic check - users should ensure proper anonymization
        before using this system.
        
        Args:
            candidate: Candidate profile to validate
            
        Raises:
            ValueError: If obvious PII is detected
        """
        # Check for email-like patterns in candidate_id
        if "@" in candidate.candidate_id:
            raise ValueError(
                "Candidate ID appears to contain email address. "
                "Use anonymous identifiers only (e.g., 'CAND-12345')"
            )
        
        # Check for phone-like patterns
        if any(char.isdigit() for char in candidate.candidate_id) and "-" in candidate.candidate_id:
            digit_count = sum(1 for c in candidate.candidate_id if c.isdigit())
            if digit_count >= 10:
                # Could be a phone number
                import re
                if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', candidate.candidate_id):
                    raise ValueError(
                        "Candidate ID appears to contain phone number. "
                        "Use anonymous identifiers only (e.g., 'CAND-12345')"
                    )
        
        # Warning about names in work experience (we don't fail, just warn conceptually)
        # In production, this should be logged or monitored
        pass
    
    def get_agent_status(self) -> dict:
        """
        Get status of all agents.
        
        Returns:
            Dictionary with agent status information
        """
        return {
            "agent_a": {
                "name": self.agent_a.agent_name,
                "status": "ready",
            },
            "agent_b": {
                "name": self.agent_b.agent_name,
                "status": "ready" if self.agent_b.github_client else "limited (no GitHub token)",
            },
            "agent_c": {
                "name": self.agent_c.agent_name,
                "status": "ready",
            },
        }

"""Agent implementations for the Tri-Agent workflow."""

from .parser_agent import parser_agent
from .analyzer_agent import analyzer_agent
from .matcher_agent import matcher_agent

__all__ = ["parser_agent", "analyzer_agent", "matcher_agent"]
"""AI Agents for candidate analysis."""

from .agent_a_resume import ResumeVerificationAgent
from .agent_b_github import GitHubAnalysisAgent
from .agent_c_synthesis import CreditScoreSynthesizer

__all__ = [
    "ResumeVerificationAgent",
    "GitHubAnalysisAgent",
    "CreditScoreSynthesizer",
]

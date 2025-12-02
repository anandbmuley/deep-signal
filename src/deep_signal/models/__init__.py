"""Data models for DeepSignal."""

from .candidate import CandidateProfile, Skill, WorkExperience
from .report import AnalysisReport, AgentReport, RiskFactor

__all__ = [
    "CandidateProfile",
    "Skill",
    "WorkExperience",
    "AnalysisReport",
    "AgentReport",
    "RiskFactor",
]

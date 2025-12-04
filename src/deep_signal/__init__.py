"""
DeepSignal: Autonomous Tri-Agent AI Screener for Forensic Candidate Analysis.

This package provides three specialized agents:
- Agent A: Resume Verification Agent (Skill Decay Score)
- Agent B: GitHub Analysis Agent (Code Green-Washing Detection)
- Agent C: Candidate Credit Score Synthesizer
"""

__version__ = "0.1.0"

from .models.candidate import CandidateProfile
from .models.report import AnalysisReport

__all__ = [
    "CandidateProfile",
    "AnalysisReport",
]

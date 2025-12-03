"""Tests for data models."""

from datetime import datetime, timedelta
import pytest

from deep_signal.models.candidate import CandidateProfile, Skill, WorkExperience
from deep_signal.models.report import AnalysisReport, AgentReport, RiskFactor, RiskLevel


def test_skill_model():
    """Test Skill model creation."""
    skill = Skill(
        name="Python",
        proficiency="expert",
        last_used=datetime.utcnow(),
        years_experience=5.0,
        verified=True
    )
    assert skill.name == "Python"
    assert skill.proficiency == "expert"
    assert skill.years_experience == 5.0
    assert skill.verified is True


def test_work_experience_model():
    """Test WorkExperience model creation."""
    exp = WorkExperience(
        company="Tech Co",
        position="Developer",
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2023, 1, 1),
        skills_used=["Python", "JavaScript"]
    )
    assert exp.company == "Tech Co"
    assert exp.position == "Developer"
    assert len(exp.skills_used) == 2


def test_candidate_profile_model():
    """Test CandidateProfile model creation."""
    candidate = CandidateProfile(
        candidate_id="CAND-001",
        skills=[
            Skill(name="Python", proficiency="expert")
        ],
        github_username="testuser"
    )
    assert candidate.candidate_id == "CAND-001"
    assert len(candidate.skills) == 1
    assert candidate.github_username == "testuser"


def test_risk_factor_model():
    """Test RiskFactor model creation."""
    risk = RiskFactor(
        category="skill_decay",
        severity=RiskLevel.HIGH,
        description="Test risk",
        score_impact=-10.0
    )
    assert risk.category == "skill_decay"
    assert risk.severity == RiskLevel.HIGH
    assert risk.score_impact == -10.0


def test_agent_report_model():
    """Test AgentReport model creation."""
    report = AgentReport(
        agent_name="Test Agent",
        score=75.0,
        confidence=0.9,
        risk_factors=[],
        signals={"test": "data"}
    )
    assert report.agent_name == "Test Agent"
    assert report.score == 75.0
    assert report.confidence == 0.9
    assert report.signals["test"] == "data"


def test_analysis_report_model():
    """Test AnalysisReport model creation."""
    agent_report = AgentReport(
        agent_name="Test Agent",
        score=75.0,
        confidence=0.9
    )
    
    report = AnalysisReport(
        candidate_id="CAND-001",
        candidate_credit_score=70.0,
        agent_reports={"test": agent_report},
        overall_risk_level=RiskLevel.LOW,
        key_findings=["Finding 1"],
        recommendations=["Recommendation 1"]
    )
    
    assert report.candidate_id == "CAND-001"
    assert report.candidate_credit_score == 70.0
    assert report.overall_risk_level == RiskLevel.LOW
    assert len(report.key_findings) == 1
    assert len(report.recommendations) == 1

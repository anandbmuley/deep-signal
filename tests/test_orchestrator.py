"""Tests for DeepSignal Orchestrator."""

from datetime import datetime, timedelta
import pytest

from deep_signal import DeepSignalOrchestrator, CandidateProfile
from deep_signal.models.candidate import Skill, WorkExperience


def test_orchestrator_initialization():
    """Test orchestrator initialization."""
    orchestrator = DeepSignalOrchestrator()
    
    assert orchestrator.agent_a is not None
    assert orchestrator.agent_b is not None
    assert orchestrator.agent_c is not None


def test_get_agent_status():
    """Test getting agent status."""
    orchestrator = DeepSignalOrchestrator()
    status = orchestrator.get_agent_status()
    
    assert "agent_a" in status
    assert "agent_b" in status
    assert "agent_c" in status
    
    assert status["agent_a"]["status"] == "ready"
    assert status["agent_c"]["status"] == "ready"


def test_orchestrator_full_analysis():
    """Test complete orchestrated analysis."""
    orchestrator = DeepSignalOrchestrator()
    
    candidate = CandidateProfile(
        candidate_id="CAND-001",
        skills=[
            Skill(
                name="Python",
                proficiency="expert",
                last_used=datetime.utcnow() - timedelta(days=30),
                years_experience=5.0
            ),
            Skill(
                name="JavaScript",
                proficiency="intermediate",
                last_used=datetime.utcnow() - timedelta(days=60),
                years_experience=3.0
            ),
        ],
        work_experience=[
            WorkExperience(
                company="Tech Company A",
                position="Senior Developer",
                start_date=datetime(2020, 1, 1),
                end_date=datetime(2023, 6, 30),
                skills_used=["Python", "JavaScript"]
            ),
        ],
        github_username="example-user"
    )
    
    report = orchestrator.analyze_candidate(candidate)
    
    # Check report structure
    assert report.candidate_id == "CAND-001"
    assert 0 <= report.candidate_credit_score <= 100
    assert report.overall_risk_level is not None
    
    # Check agent reports present
    assert "resume" in report.agent_reports
    assert "github" in report.agent_reports
    
    # Check findings and recommendations
    assert len(report.key_findings) > 0
    assert len(report.recommendations) > 0
    
    # Check metadata
    assert "agents_used" in report.metadata
    assert len(report.metadata["agents_used"]) == 2


def test_pii_validation_email():
    """Test PII validation rejects email addresses."""
    orchestrator = DeepSignalOrchestrator()
    
    candidate = CandidateProfile(
        candidate_id="user@example.com",  # Email address - should fail
        skills=[]
    )
    
    with pytest.raises(ValueError, match="email"):
        orchestrator.analyze_candidate(candidate)


def test_pii_validation_phone():
    """Test PII validation rejects phone numbers."""
    orchestrator = DeepSignalOrchestrator()
    
    candidate = CandidateProfile(
        candidate_id="123-456-7890",  # Phone number - should fail
        skills=[]
    )
    
    with pytest.raises(ValueError, match="phone"):
        orchestrator.analyze_candidate(candidate)


def test_pii_validation_valid_id():
    """Test PII validation accepts valid anonymous IDs."""
    orchestrator = DeepSignalOrchestrator()
    
    candidate = CandidateProfile(
        candidate_id="CAND-2024-001",  # Valid anonymous ID
        skills=[
            Skill(
                name="Python",
                last_used=datetime.utcnow() - timedelta(days=30)
            )
        ]
    )
    
    # Should not raise an exception
    report = orchestrator.analyze_candidate(candidate)
    assert report.candidate_id == "CAND-2024-001"


def test_orchestrator_minimal_data():
    """Test orchestrator with minimal candidate data."""
    orchestrator = DeepSignalOrchestrator()
    
    candidate = CandidateProfile(
        candidate_id="CAND-MIN-001",
        skills=[],
        work_experience=[]
    )
    
    report = orchestrator.analyze_candidate(candidate)
    
    # Should still produce a report, even with minimal data
    assert report.candidate_id == "CAND-MIN-001"
    assert report.candidate_credit_score is not None
    assert report.overall_risk_level is not None

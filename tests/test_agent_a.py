"""Tests for Agent A: Resume Verification Agent."""

from datetime import datetime, timedelta
import pytest

from deep_signal.agents.agent_a_resume import ResumeVerificationAgent
from deep_signal.models.candidate import CandidateProfile, Skill, WorkExperience
from deep_signal.models.report import RiskLevel


def test_agent_a_initialization():
    """Test Agent A initialization."""
    agent = ResumeVerificationAgent()
    assert agent.agent_name == "Agent A: Resume Verification"
    assert agent.decay_half_life_months == 18


def test_skill_decay_calculation():
    """Test skill decay score calculation."""
    agent = ResumeVerificationAgent()
    
    # Recent skill (30 days ago)
    recent_skill = Skill(
        name="Python",
        last_used=datetime.utcnow() - timedelta(days=30)
    )
    
    # Old skill (2 years ago)
    old_skill = Skill(
        name="Java",
        last_used=datetime.utcnow() - timedelta(days=730)
    )
    
    # No date skill
    no_date_skill = Skill(name="JavaScript")
    
    scores = agent._calculate_skill_decay([recent_skill, old_skill, no_date_skill])
    
    assert scores["Python"] > 90  # Recent skill should have high score
    assert scores["Java"] < 45  # Old skill should have low score (2 years = ~40% decay)
    assert scores["JavaScript"] == 50.0  # Default score


def test_skill_verification():
    """Test skill verification against work experience."""
    agent = ResumeVerificationAgent()
    
    candidate = CandidateProfile(
        candidate_id="CAND-001",
        skills=[
            Skill(name="Python"),
            Skill(name="JavaScript"),
            Skill(name="Ruby"),  # Not in work experience
        ],
        work_experience=[
            WorkExperience(
                company="Tech Co",
                position="Developer",
                start_date=datetime(2020, 1, 1),
                skills_used=["Python", "JavaScript"]
            )
        ]
    )
    
    verification = agent._verify_skills_against_experience(candidate)
    
    assert verification["total_skills"] == 3
    assert verification["verified_count"] == 2
    assert verification["unverified_count"] == 1
    assert "Ruby" in verification["unverified_skills"]
    assert verification["verification_rate"] > 60


def test_agent_a_analysis():
    """Test complete Agent A analysis."""
    agent = ResumeVerificationAgent()
    
    candidate = CandidateProfile(
        candidate_id="CAND-001",
        skills=[
            Skill(
                name="Python",
                last_used=datetime.utcnow() - timedelta(days=30),
                years_experience=5.0
            ),
            Skill(
                name="JavaScript",
                last_used=datetime.utcnow() - timedelta(days=60),
                years_experience=3.0
            ),
        ],
        work_experience=[
            WorkExperience(
                company="Tech Co",
                position="Developer",
                start_date=datetime(2020, 1, 1),
                skills_used=["Python", "JavaScript"]
            )
        ]
    )
    
    report = agent.analyze(candidate)
    
    assert report.agent_name == "Agent A: Resume Verification"
    assert 0 <= report.score <= 100
    assert 0 <= report.confidence <= 1
    assert "skill_decay_scores" in report.signals
    assert "skill_verification" in report.signals


def test_identify_skill_risks():
    """Test risk identification."""
    agent = ResumeVerificationAgent()
    
    # Low decay scores should create risks
    skill_scores = {"Python": 95.0, "Java": 10.0}
    verification = {
        "unverified_count": 2,
        "unverified_skills": ["Ruby", "Go"],
        "verification_rate": 40.0
    }
    
    risks = agent._identify_skill_risks(skill_scores, verification)
    
    # Should have risks for decayed skill and unverified skills
    assert len(risks) >= 2
    
    risk_categories = [r.category for r in risks]
    assert "skill_decay" in risk_categories
    assert "unverified_skills" in risk_categories


def test_confidence_calculation():
    """Test confidence calculation."""
    agent = ResumeVerificationAgent()
    
    # Good candidate data
    good_candidate = CandidateProfile(
        candidate_id="CAND-001",
        skills=[
            Skill(name="Python", last_used=datetime.utcnow()),
            Skill(name="JavaScript", last_used=datetime.utcnow()),
        ],
        work_experience=[
            WorkExperience(
                company="Tech Co",
                position="Developer",
                start_date=datetime(2020, 1, 1),
                skills_used=["Python"]
            ),
            WorkExperience(
                company="Tech Co 2",
                position="Developer",
                start_date=datetime(2021, 1, 1),
                skills_used=["JavaScript"]
            ),
        ]
    )
    
    confidence = agent._calculate_confidence(good_candidate)
    assert confidence > 0.5  # Should have decent confidence
    
    # Poor candidate data
    poor_candidate = CandidateProfile(
        candidate_id="CAND-002",
        skills=[Skill(name="Python")],  # No last_used
        work_experience=[]
    )
    
    confidence = agent._calculate_confidence(poor_candidate)
    assert confidence < 0.5  # Should have low confidence

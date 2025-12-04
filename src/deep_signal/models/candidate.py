"""Candidate data models."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Skill(BaseModel):
    """Represents a skill with metadata."""
    
    name: str = Field(..., description="Name of the skill")
    proficiency: Optional[str] = Field(None, description="Proficiency level (e.g., beginner, intermediate, expert)")
    last_used: Optional[datetime] = Field(None, description="Last time the skill was used")
    years_experience: Optional[float] = Field(None, description="Years of experience with this skill")
    verified: bool = Field(False, description="Whether the skill has been verified")


class WorkExperience(BaseModel):
    """Represents work experience."""
    
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position")
    start_date: datetime = Field(..., description="Start date of employment")
    end_date: Optional[datetime] = Field(None, description="End date of employment (None if current)")
    description: Optional[str] = Field(None, description="Job description")
    skills_used: List[str] = Field(default_factory=list, description="Skills used in this role")


class CandidateProfile(BaseModel):
    """
    Candidate profile for analysis.
    
    Note: This model is designed to contain NO PII (Personally Identifiable Information).
    Use anonymous identifiers only.
    """
    
    candidate_id: str = Field(..., description="Anonymous candidate identifier")
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    skills: List[Skill] = Field(default_factory=list, description="List of skills")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="Work experience history")
    github_username: Optional[str] = Field(None, description="GitHub username for analysis")
    resume_text: Optional[str] = Field(None, description="Anonymized resume text for analysis")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "candidate_id": "CAND-12345",
                "skills": [
                    {
                        "name": "Python",
                        "proficiency": "expert",
                        "last_used": "2023-10-01T00:00:00",
                        "years_experience": 5.0,
                        "verified": False
                    }
                ],
                "github_username": "johndoe",
            }
        }

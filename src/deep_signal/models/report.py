"""Report data models."""

from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    """Risk level enumeration."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskFactor(BaseModel):
    """Represents a risk factor identified during analysis."""
    
    category: str = Field(..., description="Category of risk (e.g., 'skill_decay', 'green_washing')")
    severity: RiskLevel = Field(..., description="Severity level of the risk")
    description: str = Field(..., description="Description of the risk factor")
    score_impact: float = Field(..., description="Impact on overall score (-100 to 0)")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")


class AgentReport(BaseModel):
    """Report from a single agent."""
    
    agent_name: str = Field(..., description="Name of the agent")
    score: float = Field(..., description="Score from this agent (0-100)")
    confidence: float = Field(..., description="Confidence level (0-1)")
    risk_factors: List[RiskFactor] = Field(default_factory=list, description="Identified risk factors")
    signals: Dict[str, Any] = Field(default_factory=dict, description="Actionable signals and metrics")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class AnalysisReport(BaseModel):
    """
    Comprehensive analysis report from all agents.
    
    This is the final output of the DeepSignal system.
    """
    
    candidate_id: str = Field(..., description="Anonymous candidate identifier")
    candidate_credit_score: float = Field(..., description="Overall candidate credit score (0-100)")
    agent_reports: Dict[str, AgentReport] = Field(default_factory=dict, description="Reports from each agent")
    overall_risk_level: RiskLevel = Field(..., description="Overall risk assessment")
    key_findings: List[str] = Field(default_factory=list, description="Key findings and insights")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations for hiring decision")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Report generation timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "candidate_id": "CAND-12345",
                "candidate_credit_score": 75.5,
                "overall_risk_level": "low",
                "key_findings": [
                    "Strong technical skills with recent activity",
                    "Genuine GitHub contributions verified"
                ],
                "recommendations": [
                    "Proceed with technical interview",
                    "Verify specific project claims"
                ]
            }
        }

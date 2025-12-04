"""
Agent A: Resume Verification Agent.

This agent analyzes resumes and calculates skill decay scores based on:
- Time since last usage of each skill
- Consistency of skill usage across work history
- Verification of claimed skills against work experience
"""

from datetime import datetime
from typing import List, Dict, Any
import math

from ..models.candidate import CandidateProfile, Skill
from ..models.report import AgentReport, RiskFactor, RiskLevel
from ..state import GraphState
from ..models.state import AgentName


class ResumeVerificationAgent:
    """Agent A: Verifies resumes and calculates skill decay scores."""
    
    def __init__(self):
        """Initialize the resume verification agent."""
        self.agent_name = "Agent A: Resume Verification"
        # Decay parameters: skills lose value over time if not used
        self.decay_half_life_months = 18  # Skills decay by 50% after 18 months of non-use
        
    def analyze(self, candidate: CandidateProfile) -> AgentReport:
        """
        Analyze candidate resume and calculate skill decay scores.
        
        Args:
            candidate: Candidate profile to analyze
            
        Returns:
            AgentReport with skill verification results
        """
        risk_factors = []
        signals = {}
        
        # Calculate skill decay scores
        skill_scores = self._calculate_skill_decay(candidate.skills)
        signals["skill_decay_scores"] = skill_scores
        
        # Calculate average skill decay
        if skill_scores:
            avg_decay = sum(score for score in skill_scores.values()) / len(skill_scores)
            signals["average_skill_decay_score"] = round(avg_decay, 2)
        else:
            avg_decay = 0
            signals["average_skill_decay_score"] = 0
        
        # Verify skills against work experience
        skill_verification = self._verify_skills_against_experience(candidate)
        signals["skill_verification"] = skill_verification
        
        # Identify risk factors
        risk_factors.extend(self._identify_skill_risks(skill_scores, skill_verification))
        
        # Calculate overall score (0-100)
        # Higher score = better (more recent skills, well-verified)
        base_score = avg_decay
        verification_penalty = (skill_verification["unverified_count"] * 5)
        score = max(0, min(100, base_score - verification_penalty))
        
        # Calculate confidence based on data availability
        confidence = self._calculate_confidence(candidate)
        
        return AgentReport(
            agent_name=self.agent_name,
            score=round(score, 2),
            confidence=round(confidence, 2),
            risk_factors=risk_factors,
            signals=signals
        )
    
    def _calculate_skill_decay(self, skills: List[Skill]) -> Dict[str, float]:
        """
        Calculate decay score for each skill.
        
        Score = 100 * exp(-lambda * months_since_last_used)
        where lambda = ln(2) / half_life
        
        Args:
            skills: List of skills to analyze
            
        Returns:
            Dictionary mapping skill names to decay scores (0-100)
        """
        current_time = datetime.utcnow()
        decay_constant = math.log(2) / self.decay_half_life_months
        skill_scores = {}
        
        for skill in skills:
            if skill.last_used:
                months_since_used = (current_time - skill.last_used).days / 30.0
                decay_score = 100 * math.exp(-decay_constant * months_since_used)
                skill_scores[skill.name] = round(decay_score, 2)
            else:
                # No last_used date: assume moderate decay
                skill_scores[skill.name] = 50.0
        
        return skill_scores
    
    def _verify_skills_against_experience(self, candidate: CandidateProfile) -> Dict[str, Any]:
        """
        Verify that claimed skills appear in work experience.
        
        Args:
            candidate: Candidate profile
            
        Returns:
            Dictionary with verification statistics
        """
        claimed_skills = {skill.name for skill in candidate.skills}
        experience_skills = set()
        
        for exp in candidate.work_experience:
            experience_skills.update(exp.skills_used)
        
        verified_skills = claimed_skills & experience_skills
        unverified_skills = claimed_skills - experience_skills
        
        return {
            "total_skills": len(claimed_skills),
            "verified_skills": list(verified_skills),
            "verified_count": len(verified_skills),
            "unverified_skills": list(unverified_skills),
            "unverified_count": len(unverified_skills),
            "verification_rate": round(len(verified_skills) / len(claimed_skills) * 100, 2) if claimed_skills else 0
        }
    
    def _identify_skill_risks(
        self, 
        skill_scores: Dict[str, float], 
        verification: Dict[str, Any]
    ) -> List[RiskFactor]:
        """
        Identify risk factors based on skill analysis.
        
        Args:
            skill_scores: Skill decay scores
            verification: Skill verification results
            
        Returns:
            List of identified risk factors
        """
        risks = []
        
        # Check for significantly decayed skills
        for skill_name, score in skill_scores.items():
            if score < 30:
                risks.append(RiskFactor(
                    category="skill_decay",
                    severity=RiskLevel.HIGH if score < 15 else RiskLevel.MEDIUM,
                    description=f"Skill '{skill_name}' shows significant decay (score: {score})",
                    score_impact=-10 if score < 15 else -5,
                    details={"skill": skill_name, "decay_score": score}
                ))
        
        # Check for unverified skills
        if verification["unverified_count"] > 0:
            severity = RiskLevel.HIGH if verification["verification_rate"] < 50 else RiskLevel.MEDIUM
            risks.append(RiskFactor(
                category="unverified_skills",
                severity=severity,
                description=f"{verification['unverified_count']} skill(s) not verified in work experience",
                score_impact=-verification["unverified_count"] * 3,
                details={
                    "unverified_skills": verification["unverified_skills"],
                    "verification_rate": verification["verification_rate"]
                }
            ))
        
        return risks
    
    def _calculate_confidence(self, candidate: CandidateProfile) -> float:
        """
        Calculate confidence level based on data availability.
        
        Args:
            candidate: Candidate profile
            
        Returns:
            Confidence score (0-1)
        """
        confidence_factors = []
        
        # Has skills with last_used dates
        if candidate.skills:
            skills_with_dates = sum(1 for s in candidate.skills if s.last_used)
            confidence_factors.append(skills_with_dates / len(candidate.skills))
        
        # Has work experience
        if candidate.work_experience:
            confidence_factors.append(min(len(candidate.work_experience) / 3, 1.0))
        
        # Has skill usage in work experience
        if candidate.work_experience:
            exp_with_skills = sum(1 for e in candidate.work_experience if e.skills_used)
            confidence_factors.append(exp_with_skills / len(candidate.work_experience))
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.5


def skill_decay_agent(state: GraphState) -> Dict[str, Any]:
    """
    Skill Decay Analysis Agent Node.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with skill decay report
    """
    print("=" * 60)
    print("📉 SKILL DECAY AGENT ACTIVATED")
    print("=" * 60)
    
    parsed_content = state.get("parsed_content")
    if not parsed_content:
        print("❌ No parsed content available!")
        return {
            "skill_decay_report": None,
            "current_agent": AgentName.SKILL_DECAY,
            "error": "No parsed content to analyze"
        }
    
    agent = ResumeVerificationAgent()
    report = agent.analyze(parsed_content)
    
    print(f"✅ Analysis complete! Score: {report.score}")
    print(f"Risks identified: {len(report.risk_factors)}")
    print()
    
    return {
        "skill_decay_report": report,
        # "current_agent": AgentName.SKILL_DECAY,  # Removed to avoid parallel update conflict
        "messages": [{"role": "system", "content": "Skill decay analysis completed"}]
    }

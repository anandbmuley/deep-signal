"""
Agent C: Candidate Credit Score Synthesizer.

This agent synthesizes insights from Agent A (Resume Verification) and Agent B (GitHub Analysis)
to produce a comprehensive Candidate Credit Score with risk assessment and actionable recommendations.
"""

from typing import Dict, List, Any
from statistics import mean

from ..models.candidate import CandidateProfile
from ..models.report import AgentReport, AnalysisReport, RiskFactor, RiskLevel
from ..state import GraphState
from ..models.state import AgentName


class CreditScoreSynthesizer:
    """Agent C: Synthesizes candidate credit score from all agent inputs."""
    
    def __init__(self):
        """Initialize the credit score synthesizer."""
        self.agent_name = "Agent C: Credit Score Synthesis"
        
        # Weights for combining agent scores
        self.weights = {
            "resume": 0.5,  # Resume verification weight
            "github": 0.5,  # GitHub analysis weight
        }
    
    def synthesize(
        self,
        candidate: CandidateProfile,
        agent_reports: Dict[str, AgentReport]
    ) -> AnalysisReport:
        """
        Synthesize final candidate credit score and generate comprehensive report.
        
        Args:
            candidate: Candidate profile
            agent_reports: Dictionary of reports from other agents
            
        Returns:
            Comprehensive AnalysisReport
        """
        # Calculate weighted credit score
        credit_score = self._calculate_credit_score(agent_reports)
        
        # Determine overall risk level
        overall_risk = self._determine_overall_risk(agent_reports, credit_score)
        
        # Generate key findings
        key_findings = self._generate_key_findings(agent_reports)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(credit_score, overall_risk, agent_reports)
        
        # Collect metadata
        metadata = self._collect_metadata(agent_reports)
        
        return AnalysisReport(
            candidate_id=candidate.candidate_id if candidate.candidate_id else "UNKNOWN",
            candidate_credit_score=round(credit_score, 2),
            agent_reports=agent_reports,
            overall_risk_level=overall_risk,
            key_findings=key_findings,
            recommendations=recommendations,
            metadata=metadata
        )
    
    def _calculate_credit_score(self, agent_reports: Dict[str, AgentReport]) -> float:
        """
        Calculate weighted candidate credit score.
        
        Args:
            agent_reports: Reports from all agents
            
        Returns:
            Credit score (0-100)
        """
        weighted_scores = []
        
        # Get resume score (Agent A)
        if "resume" in agent_reports and agent_reports["resume"]:
            resume_report = agent_reports["resume"]
            weighted_score = resume_report.score * resume_report.confidence * self.weights["resume"]
            weighted_scores.append(weighted_score)
        
        # Get GitHub score (Agent B)
        if "github" in agent_reports and agent_reports["github"]:
            github_report = agent_reports["github"]
            weighted_score = github_report.score * github_report.confidence * self.weights["github"]
            weighted_scores.append(weighted_score)
        
        # Calculate base credit score
        if weighted_scores:
            total_weight = sum(
                self.weights[key] * agent_reports[key].confidence
                for key in ["resume", "github"]
                if key in agent_reports and agent_reports[key]
            )
            base_score = sum(weighted_scores) / total_weight if total_weight > 0 else 50.0
        else:
            base_score = 50.0  # Default neutral score
        
        # Apply risk penalties
        total_penalty = 0
        for report in agent_reports.values():
            if report:
                for risk in report.risk_factors:
                    total_penalty += abs(risk.score_impact)
        
        final_score = max(0, min(100, base_score - total_penalty))
        
        return final_score
    
    def _determine_overall_risk(
        self,
        agent_reports: Dict[str, AgentReport],
        credit_score: float
    ) -> RiskLevel:
        """
        Determine overall risk level.
        
        Args:
            agent_reports: Reports from all agents
            credit_score: Calculated credit score
            
        Returns:
            Overall risk level
        """
        # Count high and critical risks
        critical_count = 0
        high_count = 0
        medium_count = 0
        
        for report in agent_reports.values():
            if report:
                for risk in report.risk_factors:
                    if risk.severity == RiskLevel.CRITICAL:
                        critical_count += 1
                    elif risk.severity == RiskLevel.HIGH:
                        high_count += 1
                    elif risk.severity == RiskLevel.MEDIUM:
                        medium_count += 1
        
        # Determine risk level based on counts and credit score
        if critical_count > 0 or credit_score < 40:
            return RiskLevel.CRITICAL
        elif high_count >= 2 or credit_score < 55:
            return RiskLevel.HIGH
        elif high_count >= 1 or medium_count >= 2 or credit_score < 70:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _generate_key_findings(self, agent_reports: Dict[str, AgentReport]) -> List[str]:
        """
        Generate key findings from all agent reports.
        
        Args:
            agent_reports: Reports from all agents
            
        Returns:
            List of key findings
        """
        findings = []
        
        # Resume findings (Agent A)
        if "resume" in agent_reports and agent_reports["resume"]:
            resume_report = agent_reports["resume"]
            signals = resume_report.signals
            
            if "average_skill_decay_score" in signals:
                decay_score = signals["average_skill_decay_score"]
                if decay_score >= 70:
                    findings.append(f"Strong skill currency with average decay score of {decay_score}/100")
                elif decay_score < 40:
                    findings.append(f"Concerning skill decay detected (avg score: {decay_score}/100)")
            
            if "skill_verification" in signals:
                verification = signals["skill_verification"]
                if verification["verification_rate"] >= 80:
                    findings.append(f"High skill verification rate ({verification['verification_rate']}%)")
                elif verification["verification_rate"] < 50:
                    findings.append(f"Low skill verification rate ({verification['verification_rate']}%)")
        
        # GitHub findings (Agent B)
        if "github" in agent_reports and agent_reports["github"]:
            github_report = agent_reports["github"]
            signals = github_report.signals
            
            if "greenwashing_score" in signals:
                gw_score = signals["greenwashing_score"]["score"]
                if gw_score < 30:
                    findings.append("Genuine GitHub contributions verified - low green-washing risk")
                elif gw_score > 60:
                    findings.append(f"High green-washing indicators detected ({gw_score}/100)")
            
            if "repositories" in signals:
                repos = signals["repositories"]
                if repos.get("owned_repos", 0) > 10 and repos.get("total_stars", 0) > 50:
                    findings.append(f"Strong GitHub presence with {repos['owned_repos']} owned repos and {repos['total_stars']} stars")
                
                if repos.get("fork_ratio", 0) > 70:
                    findings.append(f"High fork ratio ({repos['fork_ratio']}%) - limited original work")
        
        # If no specific findings, provide a general statement
        if not findings:
            findings.append("Limited data available for detailed analysis")
        
        return findings
    
    def _generate_recommendations(
        self,
        credit_score: float,
        overall_risk: RiskLevel,
        agent_reports: Dict[str, AgentReport]
    ) -> List[str]:
        """
        Generate actionable recommendations.
        
        Args:
            credit_score: Calculated credit score
            overall_risk: Overall risk level
            agent_reports: Reports from all agents
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Score-based recommendations
        if credit_score >= 80:
            recommendations.append("Strong candidate - proceed with interview process")
        elif credit_score >= 65:
            recommendations.append("Good candidate - verify key technical claims in interview")
        elif credit_score >= 50:
            recommendations.append("Moderate candidate - conduct thorough technical assessment")
        else:
            recommendations.append("Proceed with caution - significant concerns identified")
        
        # Risk-based recommendations
        if overall_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            recommendations.append("Recommend detailed reference checks and skill verification")
        
        # Agent-specific recommendations
        for report in agent_reports.values():
            if report:
                for risk in report.risk_factors:
                    if risk.severity in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                        if risk.category == "skill_decay":
                            recommendations.append(f"Verify current proficiency in {risk.details.get('skill', 'key skills')}")
                        elif risk.category == "green_washing":
                            recommendations.append("Request specific code samples and conduct live coding assessment")
                        elif risk.category == "unverified_skills":
                            recommendations.append("Ask for specific project examples demonstrating claimed skills")
        
        # Ensure we have at least one recommendation
        if not recommendations:
            recommendations.append("Standard interview process recommended")
        
        return recommendations
    
    def _collect_metadata(self, agent_reports: Dict[str, AgentReport]) -> Dict[str, any]:
        """
        Collect metadata from all agent reports.
        
        Args:
            agent_reports: Reports from all agents
            
        Returns:
            Metadata dictionary
        """
        valid_reports = [r for r in agent_reports.values() if r]
        
        metadata = {
            "agents_used": list(agent_reports.keys()),
            "total_risk_factors": sum(len(r.risk_factors) for r in valid_reports),
            "average_confidence": round(
                mean([r.confidence for r in valid_reports]),
                2
            ) if valid_reports else 0,
        }
        
        return metadata


def synthesis_agent(state: GraphState) -> Dict[str, Any]:
    """
    Synthesis Agent Node.
    
    Args:
        state: Current graph state
        
    Returns:
        Updated state with synthesis report
    """
    print("=" * 60)
    print("🔬 SYNTHESIS AGENT ACTIVATED")
    print("=" * 60)
    
    parsed_content = state.get("parsed_content")
    skill_decay_report = state.get("skill_decay_report")
    github_report = state.get("github_report")
    
    if not parsed_content:
        return {
            "synthesis_report": None,
            "current_agent": AgentName.SYNTHESIS,
            "error": "No parsed content to synthesize"
        }
    
    # Collect reports
    agent_reports = {}
    if skill_decay_report:
        agent_reports["resume"] = skill_decay_report
    if github_report:
        agent_reports["github"] = github_report
        
    agent = CreditScoreSynthesizer()
    report = agent.synthesize(parsed_content, agent_reports)
    
    print(f"✅ Synthesis complete! Credit Score: {report.candidate_credit_score}")
    print(f"Overall Risk: {report.overall_risk_level}")
    print()
    
    # Add recommendations to the main list
    recommendations = report.recommendations
    
    return {
        "synthesis_report": report,
        "recommendations": recommendations,
        "current_agent": AgentName.SYNTHESIS,
        "messages": [{"role": "system", "content": "Synthesis completed"}]
    }

"""
Agent B: GitHub Analysis Agent.

This agent analyzes GitHub profiles to detect "Green-Washing" - superficial contributions
that inflate a profile without demonstrating genuine technical capability. It evaluates:
- Contribution patterns and consistency
- Code quality indicators
- Repository ownership vs. contributions
- Commit message quality
- Fork/copy-paste patterns
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from ..models.candidate import CandidateProfile
from ..models.report import AgentReport, RiskFactor, RiskLevel


class GitHubAnalysisAgent:
    """Agent B: Analyzes GitHub profiles to detect code green-washing."""
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHub analysis agent.
        
        Args:
            github_token: GitHub API token (optional, uses env var if not provided)
        """
        self.agent_name = "Agent B: GitHub Analysis"
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.github_client = None
        
        if GITHUB_AVAILABLE and self.github_token:
            try:
                self.github_client = Github(self.github_token)
            except Exception:
                pass
    
    def analyze(self, candidate: CandidateProfile) -> AgentReport:
        """
        Analyze candidate's GitHub profile for green-washing indicators.
        
        Args:
            candidate: Candidate profile to analyze
            
        Returns:
            AgentReport with GitHub analysis results
        """
        risk_factors = []
        signals = {}
        
        if not candidate.github_username:
            return self._create_no_data_report(
                "No GitHub username provided",
                signals
            )
        
        if not self.github_client:
            return self._create_no_data_report(
                "GitHub API not available (missing token or PyGithub)",
                signals
            )
        
        try:
            # Get GitHub user
            user = self.github_client.get_user(candidate.github_username)
            
            # Analyze user profile
            profile_analysis = self._analyze_profile(user)
            signals["profile"] = profile_analysis
            
            # Analyze repositories
            repo_analysis = self._analyze_repositories(user)
            signals["repositories"] = repo_analysis
            
            # Analyze contribution patterns
            contribution_analysis = self._analyze_contributions(user)
            signals["contributions"] = contribution_analysis
            
            # Detect green-washing patterns
            greenwashing_score = self._detect_greenwashing(
                profile_analysis,
                repo_analysis,
                contribution_analysis
            )
            signals["greenwashing_score"] = greenwashing_score
            
            # Identify risk factors
            risk_factors.extend(
                self._identify_github_risks(
                    profile_analysis,
                    repo_analysis,
                    contribution_analysis,
                    greenwashing_score
                )
            )
            
            # Calculate overall score (0-100, higher = better)
            score = self._calculate_github_score(
                profile_analysis,
                repo_analysis,
                contribution_analysis,
                greenwashing_score
            )
            
            confidence = 0.85  # High confidence when we have GitHub data
            
        except GithubException as e:
            return self._create_no_data_report(
                f"GitHub API error: {str(e)}",
                signals
            )
        except Exception as e:
            return self._create_no_data_report(
                f"Analysis error: {str(e)}",
                signals
            )
        
        return AgentReport(
            agent_name=self.agent_name,
            score=round(score, 2),
            confidence=round(confidence, 2),
            risk_factors=risk_factors,
            signals=signals
        )
    
    def _analyze_profile(self, user) -> Dict[str, Any]:
        """Analyze GitHub user profile."""
        return {
            "username": user.login,
            "public_repos": user.public_repos,
            "followers": user.followers,
            "following": user.following,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "account_age_days": (datetime.utcnow() - user.created_at).days if user.created_at else 0,
            "has_bio": bool(user.bio),
            "has_company": bool(user.company),
        }
    
    def _analyze_repositories(self, user) -> Dict[str, Any]:
        """Analyze user's repositories."""
        repos = list(user.get_repos())
        
        owned_repos = [r for r in repos if not r.fork]
        forked_repos = [r for r in repos if r.fork]
        
        # Analyze owned repositories
        total_stars = sum(r.stargazers_count for r in owned_repos)
        total_forks = sum(r.forks_count for r in owned_repos)
        
        # Language distribution
        languages = {}
        for repo in owned_repos[:20]:  # Limit to first 20 for performance
            try:
                repo_langs = repo.get_languages()
                for lang, bytes_count in repo_langs.items():
                    languages[lang] = languages.get(lang, 0) + bytes_count
            except Exception:
                continue
        
        # Identify primary languages
        if languages:
            total_bytes = sum(languages.values())
            primary_languages = {
                lang: round(count / total_bytes * 100, 1)
                for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        else:
            primary_languages = {}
        
        return {
            "total_repos": len(repos),
            "owned_repos": len(owned_repos),
            "forked_repos": len(forked_repos),
            "fork_ratio": round(len(forked_repos) / len(repos) * 100, 1) if repos else 0,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "primary_languages": primary_languages,
            "avg_stars_per_repo": round(total_stars / len(owned_repos), 1) if owned_repos else 0,
        }
    
    def _analyze_contributions(self, user) -> Dict[str, Any]:
        """Analyze contribution patterns."""
        # Note: GitHub API has limited contribution data access
        # This is a simplified analysis
        
        repos = list(user.get_repos())[:10]  # Sample first 10 repos
        
        commit_data = {
            "recent_commit_count": 0,
            "commit_messages_analyzed": 0,
            "low_quality_commits": 0,
        }
        
        # Analyze recent commits in owned repos
        for repo in repos:
            if repo.fork:
                continue
            try:
                commits = list(repo.get_commits(author=user, since=datetime.utcnow() - timedelta(days=90))[:20])
                commit_data["recent_commit_count"] += len(commits)
                
                for commit in commits:
                    message = commit.commit.message.lower()
                    commit_data["commit_messages_analyzed"] += 1
                    
                    # Check for low-quality commit messages
                    if (
                        len(message) < 10 or
                        message in ["update", "fix", "changes", "wip", "test", "."] or
                        message.startswith("merge pull request")
                    ):
                        commit_data["low_quality_commits"] += 1
            except Exception:
                continue
        
        # Calculate commit quality ratio
        if commit_data["commit_messages_analyzed"] > 0:
            commit_data["low_quality_ratio"] = round(
                commit_data["low_quality_commits"] / commit_data["commit_messages_analyzed"] * 100,
                1
            )
        else:
            commit_data["low_quality_ratio"] = 0
        
        return commit_data
    
    def _detect_greenwashing(
        self,
        profile: Dict[str, Any],
        repos: Dict[str, Any],
        contributions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Detect green-washing patterns.
        
        Returns a score where higher = more likely to be green-washing.
        """
        indicators = []
        greenwashing_score = 0
        
        # High fork ratio suggests copy-paste behavior
        if repos["fork_ratio"] > 70:
            indicators.append("high_fork_ratio")
            greenwashing_score += 30
        elif repos["fork_ratio"] > 50:
            indicators.append("moderate_fork_ratio")
            greenwashing_score += 15
        
        # Low stars/engagement despite many repos
        if repos["owned_repos"] > 5 and repos["avg_stars_per_repo"] < 1:
            indicators.append("low_engagement")
            greenwashing_score += 20
        
        # New account with many repos (rapid repo creation)
        if profile["account_age_days"] < 180 and repos["owned_repos"] > 20:
            indicators.append("rapid_repo_creation")
            greenwashing_score += 25
        
        # High low-quality commit ratio
        if contributions["low_quality_ratio"] > 60:
            indicators.append("poor_commit_quality")
            greenwashing_score += 20
        
        # Few recent commits
        if contributions["recent_commit_count"] < 5:
            indicators.append("low_recent_activity")
            greenwashing_score += 15
        
        return {
            "score": min(greenwashing_score, 100),
            "indicators": indicators,
            "risk_level": (
                "high" if greenwashing_score > 60 else
                "medium" if greenwashing_score > 30 else
                "low"
            )
        }
    
    def _identify_github_risks(
        self,
        profile: Dict[str, Any],
        repos: Dict[str, Any],
        contributions: Dict[str, Any],
        greenwashing: Dict[str, Any]
    ) -> List[RiskFactor]:
        """Identify risk factors from GitHub analysis."""
        risks = []
        
        if greenwashing["score"] > 60:
            risks.append(RiskFactor(
                category="green_washing",
                severity=RiskLevel.HIGH,
                description=f"High green-washing score detected ({greenwashing['score']})",
                score_impact=-25,
                details=greenwashing
            ))
        elif greenwashing["score"] > 30:
            risks.append(RiskFactor(
                category="green_washing",
                severity=RiskLevel.MEDIUM,
                description=f"Moderate green-washing indicators detected ({greenwashing['score']})",
                score_impact=-15,
                details=greenwashing
            ))
        
        if repos["fork_ratio"] > 70:
            risks.append(RiskFactor(
                category="fork_ratio",
                severity=RiskLevel.MEDIUM,
                description=f"Very high fork ratio ({repos['fork_ratio']}%) - mostly copied repositories",
                score_impact=-10,
                details={"fork_ratio": repos["fork_ratio"], "forked_repos": repos["forked_repos"]}
            ))
        
        if contributions["low_quality_ratio"] > 60:
            risks.append(RiskFactor(
                category="commit_quality",
                severity=RiskLevel.MEDIUM,
                description=f"High ratio of low-quality commits ({contributions['low_quality_ratio']}%)",
                score_impact=-10,
                details={"low_quality_ratio": contributions["low_quality_ratio"]}
            ))
        
        return risks
    
    def _calculate_github_score(
        self,
        profile: Dict[str, Any],
        repos: Dict[str, Any],
        contributions: Dict[str, Any],
        greenwashing: Dict[str, Any]
    ) -> float:
        """Calculate overall GitHub quality score."""
        score = 50  # Base score
        
        # Positive factors
        score += min(repos["owned_repos"] * 2, 20)  # Up to +20 for repos
        score += min(repos["total_stars"] / 10, 15)  # Up to +15 for stars
        score += min(contributions["recent_commit_count"], 15)  # Up to +15 for activity
        
        # Negative factors
        score -= greenwashing["score"] * 0.5  # Penalize green-washing
        score -= repos["fork_ratio"] * 0.2  # Penalize high fork ratio
        score -= contributions["low_quality_ratio"] * 0.3  # Penalize low-quality commits
        
        return max(0, min(100, score))
    
    def _create_no_data_report(self, reason: str, signals: Dict[str, Any]) -> AgentReport:
        """Create a report when GitHub data is not available."""
        signals["error"] = reason
        signals["data_available"] = False
        
        return AgentReport(
            agent_name=self.agent_name,
            score=50.0,  # Neutral score when no data
            confidence=0.1,  # Very low confidence
            risk_factors=[
                RiskFactor(
                    category="no_data",
                    severity=RiskLevel.MEDIUM,
                    description=f"GitHub analysis unavailable: {reason}",
                    score_impact=-10,
                    details={"reason": reason}
                )
            ],
            signals=signals
        )

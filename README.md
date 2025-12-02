# DeepSignal: Autonomous Tri-Agent AI Screener

DeepSignal is an autonomous, Tri-Agent AI screener that performs forensic candidate analysis. It provides deep, actionable signals and risk factors, prioritizing verifiable data over keywords, all while ensuring no PII (Personally Identifiable Information) persistence.

## 🎯 Overview

DeepSignal employs three specialized AI agents that work together to provide comprehensive candidate assessment:

### **Agent A: Resume Verification Agent**
- Verifies resume claims against work history
- Calculates **Skill Decay Score** based on last usage dates
- Identifies skill gaps and inconsistencies
- Validates claimed expertise against documented experience

### **Agent B: GitHub Analysis Agent**
- Detects code **"Green-Washing"** - superficial contributions that inflate profiles
- Analyzes contribution patterns and consistency
- Evaluates repository quality and ownership
- Identifies genuine technical capability vs. copy-paste behavior
- Assesses commit quality and engagement metrics

### **Agent C: Credit Score Synthesizer**
- Synthesizes inputs from Agents A and B
- Generates quantifiable **Candidate Credit Score** (0-100)
- Produces comprehensive risk assessment
- Provides actionable hiring recommendations

## 🔒 Privacy & Security

**NO PII PERSISTENCE**: DeepSignal is designed to work exclusively with anonymized candidate identifiers. The system validates inputs to prevent PII storage and operates on de-identified data only.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/anandbmuley/deep-signal.git
cd deep-signal

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Basic Usage

```python
from datetime import datetime, timedelta
from deep_signal import DeepSignalOrchestrator, CandidateProfile
from deep_signal.models.candidate import Skill, WorkExperience

# Create candidate profile (use anonymous IDs only!)
candidate = CandidateProfile(
    candidate_id="CAND-2024-001",  # Anonymous identifier
    github_username="example-user",
    skills=[
        Skill(
            name="Python",
            proficiency="expert",
            last_used=datetime.utcnow() - timedelta(days=30),
            years_experience=5.0,
        ),
    ],
    work_experience=[
        WorkExperience(
            company="Tech Company A",  # Anonymized
            position="Senior Developer",
            start_date=datetime(2020, 1, 1),
            end_date=datetime(2023, 6, 30),
            skills_used=["Python", "JavaScript"],
        ),
    ],
)

# Initialize orchestrator
orchestrator = DeepSignalOrchestrator(github_token="your_github_token")

# Run analysis
report = orchestrator.analyze_candidate(candidate)

# View results
print(f"Credit Score: {report.candidate_credit_score}/100")
print(f"Risk Level: {report.overall_risk_level}")
print(f"Key Findings: {report.key_findings}")
print(f"Recommendations: {report.recommendations}")
```

### Run Example

```bash
# Set GitHub token (optional, but recommended for Agent B)
export GITHUB_TOKEN=your_github_token_here

# Run the example
python examples/basic_usage.py
```

## 📊 What Gets Analyzed

### Skill Decay Analysis (Agent A)
- **Decay Score**: Exponential decay based on time since last use (half-life: 18 months)
- **Verification Rate**: Percentage of skills verified against work experience
- **Risk Factors**: Identifies decayed skills and unverified claims

### GitHub Green-Washing Detection (Agent B)
- **Fork Ratio**: Percentage of forked vs. owned repositories
- **Contribution Quality**: Commit message quality and patterns
- **Engagement Metrics**: Stars, forks, and community engagement
- **Activity Patterns**: Recent commit frequency and consistency
- **Green-Washing Score**: Composite indicator of superficial vs. genuine contributions

### Credit Score Synthesis (Agent C)
- **Weighted Scoring**: Combines Agent A and B scores with confidence weighting
- **Risk Assessment**: Categorizes overall risk (LOW, MEDIUM, HIGH, CRITICAL)
- **Key Findings**: Extracts most significant insights
- **Actionable Recommendations**: Provides specific hiring guidance

## 🏗️ Architecture

```
DeepSignal Orchestrator
├── Agent A: Resume Verification
│   ├── Skill Decay Calculator
│   ├── Experience Verifier
│   └── Risk Identifier
├── Agent B: GitHub Analysis
│   ├── Profile Analyzer
│   ├── Repository Evaluator
│   ├── Contribution Assessor
│   └── Green-Washing Detector
└── Agent C: Credit Score Synthesizer
    ├── Score Calculator
    ├── Risk Aggregator
    ├── Finding Generator
    └── Recommendation Engine
```

## 🔧 Configuration

### Environment Variables

```bash
# GitHub API token for Agent B (optional but recommended)
GITHUB_TOKEN=your_github_token_here
```

### Agent Configuration

Agents can be customized during initialization:

```python
# Custom GitHub token
orchestrator = DeepSignalOrchestrator(github_token="custom_token")

# Access individual agents
orchestrator.agent_a  # Resume Verification Agent
orchestrator.agent_b  # GitHub Analysis Agent
orchestrator.agent_c  # Credit Score Synthesizer
```

## 📈 Output Format

The system produces an `AnalysisReport` containing:

```python
{
    "candidate_id": "CAND-2024-001",
    "candidate_credit_score": 75.5,
    "overall_risk_level": "low",
    "key_findings": [
        "Strong technical skills with recent activity",
        "Genuine GitHub contributions verified"
    ],
    "recommendations": [
        "Proceed with technical interview",
        "Verify specific project claims"
    ],
    "agent_reports": {
        "resume": { /* Agent A details */ },
        "github": { /* Agent B details */ }
    }
}
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=deep_signal tests/
```

## 📝 Development

### Project Structure

```
deep-signal/
├── src/deep_signal/
│   ├── __init__.py
│   ├── orchestrator.py          # Main orchestrator
│   ├── agents/
│   │   ├── agent_a_resume.py    # Resume verification
│   │   ├── agent_b_github.py    # GitHub analysis
│   │   └── agent_c_synthesis.py # Credit score synthesis
│   ├── models/
│   │   ├── candidate.py         # Candidate data models
│   │   └── report.py            # Report data models
│   └── utils/
├── examples/
│   └── basic_usage.py           # Usage example
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please ensure:
- No PII is introduced or persisted
- Code follows existing patterns
- Tests are included for new features
- Documentation is updated

## 📄 License

This project is available under the MIT License.

## ⚠️ Important Notes

1. **PII Protection**: Always use anonymous identifiers. Never include real names, emails, or phone numbers.
2. **GitHub Token**: Agent B requires a GitHub token for full functionality. Without it, GitHub analysis will be limited.
3. **Data Privacy**: This system is designed for pre-screened, anonymized data only.
4. **Risk Assessment**: Use results as input to decision-making, not as sole determinant.

## 🔮 Future Enhancements

- Additional agents for specific skill domains
- Machine learning-based pattern detection
- Integration with more data sources (LinkedIn, Stack Overflow, etc.)
- Real-time monitoring and alerts
- API endpoint for integration with ATS systems

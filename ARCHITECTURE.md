# DeepSignal Architecture

## System Overview

DeepSignal is a Tri-Agent AI system designed to perform forensic candidate analysis. The system prioritizes verifiable data over keywords and ensures no PII persistence.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   DeepSignal Orchestrator                   │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Agent A   │  │  Agent B   │  │  Agent C   │            │
│  │   Resume   │  │   GitHub   │  │   Credit   │            │
│  │Verification│  │  Analysis  │  │   Score    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│        │               │               │                    │
│        └───────────────┴───────────────┘                    │
│                        │                                    │
└────────────────────────┼────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────┐
              │  Analysis Report │
              │  - Credit Score  │
              │  - Risk Factors  │
              │  - Findings      │
              │  - Recommendations│
              └──────────────────┘
```

## Components

### 1. DeepSignal Orchestrator

**Location:** `src/deep_signal/orchestrator.py`

**Responsibilities:**
- Coordinates execution of all three agents
- Validates input for PII protection
- Aggregates results into final report
- Ensures proper data flow between agents

**Key Methods:**
- `analyze_candidate(candidate)` - Main entry point for analysis
- `get_agent_status()` - Returns status of all agents
- `_validate_no_pii(candidate)` - Validates that input contains no PII

### 2. Agent A: Resume Verification Agent

**Location:** `src/deep_signal/agents/agent_a_resume.py`

**Purpose:** Verifies resume claims and calculates skill decay scores

**Key Features:**
- **Skill Decay Calculation**: Uses exponential decay model with 18-month half-life
- **Experience Verification**: Cross-references skills with work history
- **Risk Identification**: Flags outdated skills and unverified claims

**Algorithm:**
```python
skill_decay_score = 100 * exp(-lambda * months_since_last_used)
where lambda = ln(2) / half_life_months
```

**Output:**
- Skill decay scores (0-100 per skill)
- Verification rate (percentage of verified skills)
- Risk factors for decayed or unverified skills
- Overall score incorporating all factors

### 3. Agent B: GitHub Analysis Agent

**Location:** `src/deep_signal/agents/agent_b_github.py`

**Purpose:** Detects code "green-washing" and evaluates genuine technical contributions

**Key Features:**
- **Profile Analysis**: Account age, repository count, follower metrics
- **Repository Evaluation**: Owned vs. forked ratio, stars, engagement
- **Contribution Assessment**: Commit quality, message analysis, activity patterns
- **Green-Washing Detection**: Identifies patterns of superficial contributions

**Green-Washing Indicators:**
- High fork ratio (>70% forked repositories)
- Low engagement despite many repos
- Rapid repo creation on new accounts
- Poor commit message quality
- Minimal recent activity

**Output:**
- GitHub quality score (0-100)
- Green-washing risk score (0-100, higher = more risk)
- Repository and contribution metrics
- Risk factors for identified issues

### 4. Agent C: Credit Score Synthesizer

**Location:** `src/deep_signal/agents/agent_c_synthesis.py`

**Purpose:** Synthesizes inputs from Agents A and B into comprehensive assessment

**Key Features:**
- **Weighted Scoring**: Combines agent scores with confidence weighting
- **Risk Aggregation**: Collects and categorizes all risk factors
- **Finding Generation**: Extracts key insights from all agents
- **Recommendation Engine**: Provides actionable hiring guidance

**Scoring Formula:**
```python
credit_score = weighted_sum(agent_scores) - total_risk_penalties
where:
  weighted_sum = sum(score * confidence * weight) / sum(confidence * weight)
  total_risk_penalties = sum(abs(risk.score_impact))
```

**Risk Levels:**
- **CRITICAL**: Credit score < 40 or critical risks present
- **HIGH**: Credit score < 55 or 2+ high risks
- **MEDIUM**: Credit score < 70 or 1+ high risk or 2+ medium risks
- **LOW**: Credit score >= 70 with no major risks

**Output:**
- Candidate credit score (0-100)
- Overall risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Key findings (synthesized insights)
- Actionable recommendations

## Data Models

### CandidateProfile

**Location:** `src/deep_signal/models/candidate.py`

**Purpose:** Represents candidate data for analysis (NO PII)

**Fields:**
- `candidate_id`: Anonymous identifier (e.g., "CAND-2024-001")
- `skills`: List of Skill objects with proficiency and usage data
- `work_experience`: List of WorkExperience objects
- `github_username`: Public GitHub username (optional)
- `resume_text`: Anonymized resume text (optional)

### AnalysisReport

**Location:** `src/deep_signal/models/report.py`

**Purpose:** Final comprehensive analysis report

**Fields:**
- `candidate_id`: Anonymous identifier
- `candidate_credit_score`: Overall score (0-100)
- `agent_reports`: Dictionary of reports from each agent
- `overall_risk_level`: Aggregated risk level
- `key_findings`: List of key insights
- `recommendations`: List of actionable recommendations
- `metadata`: Additional context and statistics

## Data Flow

```
1. Input (CandidateProfile)
   ↓
2. PII Validation
   ↓
3. Agent A Analysis (Resume Verification)
   ↓
4. Agent B Analysis (GitHub Analysis)
   ↓
5. Agent C Synthesis (Credit Score)
   ↓
6. Output (AnalysisReport)
```

## Security & Privacy

### No PII Persistence

The system is designed to prevent PII storage through:

1. **Input Validation**: Checks for email/phone patterns in candidate IDs
2. **Anonymous Identifiers**: Requires use of non-identifying IDs
3. **Data Model Design**: Models don't capture PII fields
4. **Processing Only**: No database persistence layer
5. **Clear Documentation**: Explicit warnings about PII

### Recommended Practices

1. Use anonymous candidate IDs (e.g., "CAND-YYYY-NNN")
2. Anonymize company names in work experience
3. Remove names, emails, phone numbers from all inputs
4. Keep GitHub usernames as public identifiers only
5. Store reports with anonymous identifiers only

## Extension Points

### Adding New Agents

To add a new agent:

1. Create agent class in `src/deep_signal/agents/`
2. Implement `analyze(candidate)` method returning `AgentReport`
3. Register agent in orchestrator
4. Update weights in Agent C if needed
5. Add tests for new agent

### Customizing Scoring

To customize scoring:

1. **Agent A**: Modify `decay_half_life_months` for different skill decay rates
2. **Agent B**: Adjust green-washing thresholds in `_detect_greenwashing`
3. **Agent C**: Update `weights` dictionary to change agent importance

### Adding Data Sources

To integrate new data sources:

1. Create new agent following Agent A/B pattern
2. Define relevant signals and risk factors
3. Integrate into orchestrator
4. Update Agent C to incorporate new signals

## Performance Considerations

- **GitHub API**: Rate-limited; use authentication token for higher limits
- **Caching**: Consider caching GitHub data for repeated analyses
- **Async Processing**: Agents could be run in parallel for improved performance
- **Batch Processing**: Multiple candidates can be analyzed sequentially

## Testing Strategy

- **Unit Tests**: Test each agent independently (`tests/test_agent_*.py`)
- **Model Tests**: Validate data models (`tests/test_models.py`)
- **Integration Tests**: Test orchestrator with full workflow (`tests/test_orchestrator.py`)
- **Edge Cases**: PII validation, missing data, API failures

## Future Enhancements

1. **Machine Learning Integration**: Train models on historical hiring outcomes
2. **Real-time Monitoring**: Track candidate skill changes over time
3. **Additional Agents**: LinkedIn analysis, Stack Overflow reputation, etc.
4. **API Server**: REST API for integration with ATS systems
5. **Dashboard**: Web UI for viewing and comparing candidates
6. **Batch Processing**: Analyze multiple candidates efficiently
7. **Custom Risk Profiles**: Configurable risk thresholds per organization

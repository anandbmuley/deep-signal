# DeepSignal Scoring Guide

This guide explains how DeepSignal calculates scores and identifies risks.

## Overall Candidate Credit Score

**Range:** 0-100 (higher is better)

The Candidate Credit Score is calculated by:
1. Taking weighted scores from each agent
2. Adjusting for agent confidence levels
3. Applying penalties for identified risk factors

### Score Interpretation

| Score Range | Interpretation | Recommended Action |
|-------------|----------------|-------------------|
| 80-100 | Excellent candidate | Proceed with interview |
| 65-79 | Good candidate | Verify key technical claims |
| 50-64 | Moderate candidate | Conduct thorough assessment |
| 0-49 | Concerning issues | Proceed with caution |

## Agent A: Resume Verification Score

**Focus:** Skill currency and verification

### Skill Decay Score

Uses exponential decay with **18-month half-life**:

```
Score = 100 × e^(-λt)
where:
  λ = ln(2) / 18 (decay constant)
  t = months since last skill usage
```

**Examples:**
- Recent (1 month ago): ~96/100
- 6 months ago: ~79/100
- 18 months ago: ~50/100 (half-life)
- 36 months ago: ~25/100
- 60+ months ago: <10/100

### Skill Verification

Compares claimed skills against work experience:

- **Verified Skills**: Appear in documented work history
- **Unverified Skills**: Claimed but not documented

**Impact:**
- Each unverified skill: -5 points
- Verification rate < 50%: HIGH risk
- Verification rate 50-80%: MEDIUM risk
- Verification rate > 80%: LOW risk

### Agent A Scoring Formula

```
Agent A Score = Average Skill Decay Score - (Unverified Count × 5)
```

## Agent B: GitHub Analysis Score

**Focus:** Genuine technical contribution vs. "green-washing"

### Green-Washing Indicators

| Indicator | Threshold | Points Added |
|-----------|-----------|--------------|
| High fork ratio | > 70% | +30 |
| Moderate fork ratio | > 50% | +15 |
| Low engagement | < 1 star/repo (with 5+ repos) | +20 |
| Rapid repo creation | 20+ repos in < 6 months | +25 |
| Poor commit quality | > 60% low-quality commits | +20 |
| Low recent activity | < 5 commits in 90 days | +15 |

**Green-Washing Score Range:**
- 0-30: LOW risk (genuine contributions)
- 31-60: MEDIUM risk (mixed signals)
- 61-100: HIGH risk (likely green-washing)

### Low-Quality Commit Examples

- Messages < 10 characters
- Generic: "update", "fix", "changes", "wip"
- Merge commits (auto-generated)
- Single character: "."

### GitHub Scoring Formula

```
Base Score = 50
+ Repository contribution (+0 to +20)
+ Star count bonus (+0 to +15)
+ Recent activity (+0 to +15)
- Green-washing penalty (0 to -50)
- Fork ratio penalty (0 to -20)
- Commit quality penalty (0 to -30)
```

### Repository Quality Factors

**Positive:**
- Owned (non-forked) repositories
- Stars and forks from community
- Consistent commit history
- Quality commit messages
- Active maintenance

**Negative:**
- High percentage of forks
- No community engagement
- Sporadic or no recent activity
- Auto-generated or poor commits
- Many repos with minimal work

## Agent C: Credit Score Synthesis

**Focus:** Holistic assessment combining all signals

### Weighting

Default weights:
- Resume (Agent A): **50%**
- GitHub (Agent B): **50%**

Formula:
```
Credit Score = 
  (AgentA_Score × AgentA_Confidence × 0.5 + 
   AgentB_Score × AgentB_Confidence × 0.5) /
  (AgentA_Confidence × 0.5 + AgentB_Confidence × 0.5)
  - Total Risk Penalties
```

### Risk Level Determination

| Risk Level | Criteria |
|------------|----------|
| **CRITICAL** | Credit score < 40 OR any critical-severity risks |
| **HIGH** | Credit score < 55 OR 2+ high-severity risks |
| **MEDIUM** | Credit score < 70 OR 1 high OR 2+ medium risks |
| **LOW** | Credit score ≥ 70 AND no major risks |

### Confidence Factors

Agent confidence depends on data availability:

**Agent A Confidence:**
- Has skills with usage dates: +33%
- Has work experience: +33%
- Skills match experience: +34%

**Agent B Confidence:**
- GitHub data available: 85%
- GitHub data unavailable: 10%

Lower confidence reduces that agent's impact on final score.

## Risk Factors

### Risk Categories

1. **skill_decay**: Skills that have decayed significantly
2. **unverified_skills**: Skills not documented in experience
3. **green_washing**: Superficial GitHub contributions
4. **fork_ratio**: Mostly copied/forked repositories
5. **commit_quality**: Poor quality commit messages
6. **no_data**: Missing or unavailable data

### Risk Severity

| Severity | Description | Score Impact |
|----------|-------------|--------------|
| **CRITICAL** | Immediate concern | -20 to -30 |
| **HIGH** | Significant issue | -10 to -20 |
| **MEDIUM** | Notable concern | -5 to -10 |
| **LOW** | Minor issue | -1 to -5 |

## Recommendations

DeepSignal generates actionable recommendations based on:

### Score-Based

- **80+**: "Strong candidate - proceed with interview"
- **65-79**: "Good candidate - verify key claims"
- **50-64**: "Moderate candidate - thorough assessment"
- **<50**: "Proceed with caution - significant concerns"

### Risk-Based

- **HIGH/CRITICAL risk**: "Detailed reference checks required"
- **Skill decay**: "Verify current proficiency in [skill]"
- **Green-washing**: "Request code samples and live coding"
- **Unverified skills**: "Ask for specific project examples"

## Example Scenarios

### Scenario 1: Strong Candidate

```
Skills: Python (95), JavaScript (92), Docker (94)
Verification: 100%
GitHub: 15 repos, 100 stars, active commits
Green-washing: LOW (15)

Agent A: 90/100 (confidence: 0.95)
Agent B: 80/100 (confidence: 0.85)
Credit Score: 85/100
Risk Level: LOW
```

### Scenario 2: Moderate Candidate

```
Skills: Python (70), Java (30), Ruby (85)
Verification: 67% (Ruby unverified)
GitHub: 5 repos, 2 stars, moderate activity
Green-washing: MEDIUM (45)

Agent A: 65/100 (confidence: 0.85)
Agent B: 55/100 (confidence: 0.85)
Credit Score: 58/100
Risk Level: MEDIUM
```

### Scenario 3: Concerning Candidate

```
Skills: Python (40), JavaScript (35), Multiple (25-45)
Verification: 40%
GitHub: 50 repos (80% forked), 5 stars total
Green-washing: HIGH (75)

Agent A: 45/100 (confidence: 0.70)
Agent B: 30/100 (confidence: 0.85)
Credit Score: 35/100
Risk Level: CRITICAL
```

## Interpreting Results

### Green Flags ✅

- High skill decay scores (>80)
- High verification rate (>80%)
- Low green-washing score (<30)
- Recent, consistent GitHub activity
- Quality commit messages
- Community engagement (stars/forks)

### Yellow Flags ⚠️

- Moderate skill decay (50-80)
- Moderate verification (50-80%)
- Some unverified skills
- Moderate green-washing (30-60)
- Inconsistent activity patterns

### Red Flags 🚩

- Significant skill decay (<50)
- Low verification rate (<50%)
- High green-washing score (>60)
- High fork ratio (>70%)
- Poor commit quality
- No recent activity
- Many unverified claims

## Best Practices

1. **Don't rely solely on scores**: Use them as one input to your decision
2. **Review detailed signals**: Look at the raw data behind scores
3. **Consider context**: Career transitions, industry changes, etc.
4. **Verify critical skills**: Test key technical abilities in interviews
5. **Request code samples**: For roles requiring specific expertise
6. **Check references**: Especially for concerning patterns
7. **Look at trends**: Recent improvements or declines

## Customization

Organizations can adjust:
- **Decay half-life**: Default 18 months (modifiable in Agent A)
- **Agent weights**: Default 50/50 (adjustable in Agent C)
- **Risk thresholds**: Custom risk tolerances
- **Score ranges**: Organization-specific interpretations

## Limitations

DeepSignal scores should be understood with these limitations:

1. **Public data only**: Only analyzes public GitHub profiles
2. **Historical bias**: Recent activity weighted more heavily
3. **No context**: Cannot assess soft skills, culture fit, etc.
4. **Gaming potential**: Sophisticated users might game metrics
5. **Data availability**: Requires candidate cooperation for full analysis
6. **Privacy constraints**: NO PII - analysis on anonymous profiles only

## Support

For questions about scoring:
- Review the [ARCHITECTURE.md](../ARCHITECTURE.md) for technical details
- Check [README.md](../README.md) for usage examples
- Open an issue for specific questions

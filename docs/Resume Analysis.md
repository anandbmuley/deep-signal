# 📝 Feature Implementation Document: Smart Resume Analyst

**Product Feature:** AI-Powered, Unbiased Resume Analysis
**Target Role Focus:** Software Developer and Technical Leader
**Goal:** To move beyond legacy ATS keyword matching and provide a deep, conceptual evaluation of a candidate's resume, similar to a highly skilled human analyst.

-----

## 1\. Feature Definition & Scoring Breakdown

The system will generate a multi-dimensional score card based on three primary analysis categories. All scores are normalized to a **0-100 scale**.

### 1.1. Core Scoring Categories

| Category | Purpose | Key Metrics Calculated (via Code) |
| :--- | :--- | :--- |
| **Technical Depth & Breadth** | Evaluates specific skill mastery, version recency, and diversity of knowledge. | Recency & Version Score, Experience Confidence Score, Breadth & Synergy Score. |
| **Role Fit & Specialization** | Assesses the candidate's primary development archetype (Backend, Full Stack) against the role's needs. | Skill Ratio Weightage (Backend Dominance), Role Context Score. |
| **Leadership Persona & Mindset** | Analyzes the *style* and *conceptual thinking* demonstrated, mitigating keyword stuffing bias. | Leadership Split Score (L-Split), Conceptual Foundation Score, Team-Centric Tone Score. |

-----

## 2\. Implementation Plan & Architecture

The system uses a **Hybrid AI/Code Architecture** to ensure the core algorithms are deterministic and bias-free, while leveraging AI for complex Natural Language Understanding (NLU).

### Phase 1: Semantic Data Extraction (AI as Parser)

**Objective:** Convert the raw, unstructured resume PDF/DOCX into a clean, predictable JSON object using semantic understanding, avoiding simple text errors.

**Process Flow:**

1.  **Ingestion:** User uploads resume (PDF/DOCX).
2.  **Conversion:** PDF Reader (e.g., PDFplumber) converts to raw text.
3.  **Semantic Parsing (AI Agent):** The raw text is passed to the LLM (AI Agent) with a prompt mandating adherence to a defined **JSON Schema**. The AI’s task is to *semantically* understand the text and populate the fields accurately, rather than just matching section headers.

**Required JSON Schema (Output from AI Agent):**

```json
{
  "CandidateID": "UUID",
  "PersonalInfo": {
    "FullName": "string",
    "TotalYOE": "number"
  },
  "Skills": [
    {
      "Name": "string",
      "Type": "enum(Programming, DevOps, Frontend, Database, Other)",
      "Version": "string",
      "InferredYOE": "number",
      "ConfidenceScore": "number"
    }
  ],
  "Experience": [
    {
      "Organization": "string",
      "Title": "string",
      "DurationMonths": "number",
      "IsLeadershipRole": "boolean",
      "ResponsibilitiesText": "string",
      "AI_PreAnalysis": {
        "ImpliedSkills": "array[string]",
        "ToneType": "enum(Individual, Collaborative, Strategic)",
        "RawMetric_I_vs_We": "number"
      }
    }
  ]
}
```

### Phase 2: Core Analysis & Scoring (Code & Configurable Logic)

**Objective:** Execute the unbiased, weighted algorithms using the structured JSON data and configurable parameters. This is the **Code-Only** phase to ensure predictability.

#### 2.1. Configurable Weights Database Schema

The weightings for the scoring must be externally configurable and auditable.

| Table Name | Column Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Config_Weights` | `WeightName` | VARCHAR (100) | Unique identifier (e.g., `W_TECH_RECENCY`, `W_LEADERSHIP_SPLIT`). |
| | `WeightValue` | DECIMAL (5,3) | The numerical multiplier for the calculation (e.g., 0.15, 0.80). |
| | `Category` | VARCHAR (50) | The score category (e.g., `Technical`, `Leadership`). |
| | `ShortExplanation` | TEXT | **User-facing explanation** for the weight (e.g., "80% hands-on split is ideal for a Senior Developer."). |
| | `LastUpdatedBy` | VARCHAR (50) | User who last changed the weight. |

#### 2.2. Core Algorithm Logic (Simplified Examples)

1.  **Technical Depth (Recency):**
      * $S_{\text{Recency}} = W_{\text{Latest}} \times (\text{Score for v25}) + W_{\text{Legacy}} \times (\text{Score for v1.8})$
      * *(Scores for versions are hardcoded or set in a separate config table based on organization standards.)*
2.  **Leadership Split Score (L-Split):**
      * **Input:** `RawMetric_I_vs_We` and `IsLeadershipRole` (from Phase 1 JSON).
      * **Logic:** If `IsLeadershipRole` is true, compare `RawMetric_I_vs_We` against the configurable `TargetSplit` (e.g., $W_{\text{L-SPLIT}}$). Score deviation from the target split is penalized.
3.  **Bias Mitigation/Gating:**
      * **Rule:** A high **Team-Centric Tone Score** (AI-derived) can only be applied if the **Conceptual Foundation Score** (AI-derived analysis of "why" and "framework choice") is above a minimum threshold (e.g., 70/100).
      * **Code Implementation:**
        ```
        IF ConceptualFoundationScore < MIN_FOUNDATION_THRESHOLD:
            LeadershipPersonaScore = MIN(LeadershipPersonaScore, CAPPED_MAX_SCORE)
        ```

### Phase 3: Score Card Generation & Audit (Transparency & Persistence)

**Objective:** Store every calculation detail and present the findings transparently, like an educational progress report.

#### 3.1. Audit Log Database Schema (Persistence for Traceability)

| Table Name | Column Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Scoring_AuditLog` | `AuditID` | UUID | Primary Key. |
| | `CandidateID` | UUID | Foreign Key to the candidate record. |
| | `MetricName` | VARCHAR (100) | Name of the calculated metric (e.g., `JavaRecencyScore`, `ConceptualFoundationScore`). |
| | `ScoreValue` | DECIMAL (5,2) | The raw score calculated (e.g., 92.5). |
| | `WeightApplied` | DECIMAL (5,3) | The configured weight used in this calculation. |
| | `WeightedResult` | DECIMAL (5,2) | The final result of (Score \* Weight). |
| | `InputTraceData` | TEXT | **The exact textual evidence** from the resume that led to the score (e.g., "Responsible for Microservices implementation using Java 25 and Spring Boot 3.2"). |
| | `CalculationTime` | TIMESTAMP | When the score was calculated. |

#### 3.2. Score Card UI (The "Progress Report")

  * **Display:** A main dashboard showing the three primary category scores (Technical Depth, Role Fit, Leadership).
  * **Drill-Down:** Each category score is clickable, opening a modal that displays the `Scoring_AuditLog` data.
  * **Explanation on Demand:** For each metric in the drill-down, the UI shows:
      * **Raw Score:** (e.g., 95/100).
      * **Weight Used:** (e.g., $0.15$).
      * **Why (User-facing Explanation):** Displays the `ShortExplanation` from the `Config_Weights` table (e.g., "Newer version Java 25 detected, providing a 15% bonus to overall technical score.").
      * **Evidence:** Displays the `InputTraceData` from the `Scoring_AuditLog` (the actual resume text).

This complete document defines the product features, the hybrid AI/Code architecture, the critical data structures, and the persistence required to ensure an intelligent, yet unbiased and auditable, resume analysis system.


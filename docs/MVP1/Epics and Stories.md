📜 Epic and Story Breakdown

The following is a breakdown of the Epics into User Stories for your initial backlog, prioritizing the MVP (Release 1) features.

Epic 1: Semantic Data Extraction & Parsing (AI as Parser)

Goal: Securely ingest resume files and translate them into a structured, reliable JSON object.

User Stories (MVP Priority):

P1/MVP: As a system, I need a secure endpoint that accepts a PDF file upload and converts it to raw text using a PDF Reader (e.g., PDFplumber).

P1/MVP: As the AI Agent, I must be given a fixed JSON Schema and a prompt to semantically populate the Skills and Experience arrays from the raw text.


P2: As a user, I want the system to handle common resume formatting errors (e.g., broken bullet points) without the AI failing to parse key sections.

Epic 2: Core Analysis & Scoring Engine (Code & Logic)

Goal: Implement the deterministic, auditable scoring algorithms.

User Stories (MVP Priority):

P1/MVP: As the system, I need to implement the Technical Depth Recency Score logic, which calculates a weighted score based on inferred skill version and experience.




P2: As the system, I need to implement the Leadership Split Score (L-Split) logic by comparing the AI-derived RawMetric_I_vs_We against the TargetSplit.



P3: As the system, I need to implement the Bias Mitigation Gating Rule that caps the LeadershipPersonaScore if the ConceptualFoundationScore is below a minimum threshold.


Epic 3: Configuration & Auditability

Goal: Ensure all scoring is auditable and configurable.



User Stories (MVP Priority):

P1/MVP: As the system, I must create and persist data to the Scoring_AuditLog table for every core metric calculation, storing the ScoreValue, WeightApplied, and the InputTraceData (text evidence).

P2: As a developer, I need to define and create the Config_Weights database schema to hold all configurable multipliers and their explanations.

P3: As a system admin, I need a basic admin UI to view, edit, and update the WeightValue in the Config_Weights table.

Epic 4: Score Card Generation & UI

Goal: Provide transparent and educational feedback to the user.


User Stories (MVP Priority):

P1/MVP: As a system, I must expose an API endpoint that returns the three primary category scores and the top-level audit log entry.

P2: As a user, I want a main dashboard to clearly display the overall final score and the scores for the three primary categories: Technical Depth, Role Fit, and Leadership.

P3: As a user, I want to click on any category score to drill down and see the Scoring_AuditLog details, including the Raw Score, Weight Used, Why (ShortExplanation), and Evidence (InputTraceData).
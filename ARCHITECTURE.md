# Deep Signal Architecture Documentation

## Overview

Deep Signal is an AI-powered job matching platform that uses a Tri-Agent architecture orchestrated by LangGraph. This document describes the architectural decisions, workflow design, and future implementation plans.

## Design Philosophy

The "Iron Skeleton" approach allows us to:
1. **Validate Architecture Early**: Prove the workflow structure before investing in complex implementations
2. **Incremental Development**: Replace placeholders with real implementations one agent at a time
3. **Clear Separation of Concerns**: Each agent has a single, well-defined responsibility
4. **State Management**: LangGraph handles state transitions and workflow control

## State Machine Design

### GraphState Schema

The `GraphState` TypedDict serves as the central data structure passed between agents:

```python
GraphState:
  # Input
  - input_data: str (PDF path or document identifier)
  
  # Parser Agent State
  - parsed_content: dict (structured document data)
  - parse_status: str (success/failed/pending)
  
  # Analyzer Agent State
  - analysis_result: dict (insights and extracted data)
  - key_skills: List[str] (identified skills)
  - experience_level: str (career level)
  - analysis_status: str (success/failed/pending)
  
  # Matcher Agent State
  - match_result: dict (matching results)
  - match_score: float (0.0 to 1.0)
  - recommendations: List[str]
  - match_status: str (success/failed/pending)
  
  # Control Flow
  - messages: List (LangGraph message history)
  - current_agent: str (active agent identifier)
  - workflow_complete: bool
  - error: Optional[str]
```

### Workflow Graph

```
START
  │
  ├──> [Parser Agent]
  │         │
  │         ├──> (parse_status == "success") ──> [Analyzer Agent]
  │         │                                          │
  │         │                                          ├──> (analysis_status == "success") ──> [Matcher Agent]
  │         │                                          │                                             │
  │         │                                          └──> (analysis_status == "failed") ──> END
  │         │
  │         └──> (parse_status == "failed") ──> END
  │
  └──> [Matcher Agent] ──> END
```

## Agent Specifications

### 1. Parser Agent

**Responsibility**: Extract structured data from unstructured documents (PDFs)

**Current Implementation**: Placeholder with mock data
- Simulates PDF text extraction
- Returns structured fields (name, contact, skills, experience)

**Future Implementation**:
- PDF parsing using PyPDF2 or pdfplumber
- OCR for scanned documents (Tesseract)
- Section identification using NLP
- Entity extraction for names, emails, dates
- Format normalization

**Input**: `input_data` (file path)
**Output**: `parsed_content` (dict), `parse_status`

### 2. Analyzer Agent

**Responsibility**: Analyze parsed content to extract meaningful insights

**Current Implementation**: Placeholder with mock analysis
- Simulates skill extraction
- Returns experience level and key attributes

**Future Implementation**:
- LLM-powered content analysis (GPT-4, Claude)
- Skill taxonomy mapping
- Experience level classification
- Soft skill inference
- Career trajectory analysis
- Domain expertise identification

**Input**: `parsed_content`
**Output**: `analysis_result` (dict), `key_skills`, `experience_level`, `analysis_status`

### 3. Matcher Agent

**Responsibility**: Match candidates with jobs based on analysis

**Current Implementation**: Placeholder with mock matching
- Simulates compatibility scoring
- Returns mock job matches and recommendations

**Future Implementation**:
- Vector similarity matching (embeddings)
- Multi-criteria scoring (skills, experience, culture)
- Ranking algorithm
- Gap analysis
- Recommendation generation
- Database integration for job listings

**Input**: `analysis_result`, `key_skills`, `experience_level`
**Output**: `match_result` (dict), `match_score`, `recommendations`, `match_status`

## Technology Decisions

### LangGraph
- **Why**: Built-in state management, conditional routing, streaming support
- **Alternatives Considered**: Direct LangChain, custom orchestration
- **Benefits**: Proven workflow orchestration, easy debugging, visualization support

### Pydantic
- **Why**: Type safety, validation, clear contracts between agents
- **Benefits**: Catch errors early, self-documenting code

### Python 3.11+
- **Why**: Modern Python features, better performance, type hints
- **Benefits**: Pattern matching, better error messages, async improvements

## Error Handling Strategy

Each agent independently reports success/failure through status fields:
- `parse_status`, `analysis_status`, `match_status`
- Conditional edges route to END on failure
- `error` field captures error messages
- Workflow can be resumed or retried from any point

## Future Enhancements

### Phase 1: Real Implementations
- [ ] Implement PDF parsing with PyPDF2
- [ ] Integrate OpenAI/Anthropic for analysis
- [ ] Build vector database for matching

### Phase 2: Database & API
- [ ] PostgreSQL for job listings and candidates
- [ ] FastAPI REST endpoints
- [ ] Authentication and authorization

### Phase 3: Advanced Features
- [ ] Real-time matching notifications
- [ ] Batch processing for multiple resumes
- [ ] Admin dashboard
- [ ] Analytics and reporting

### Phase 4: Production Readiness
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Monitoring and logging
- [ ] Rate limiting and caching
- [ ] Documentation and API specs

## Development Guidelines

1. **Maintain the Skeleton**: Keep placeholder agents functional as fallbacks
2. **Test Each Agent**: Unit tests for each agent independently
3. **Integration Tests**: Test the full workflow end-to-end
4. **State Validation**: Ensure state schema is always respected
5. **Error Recovery**: Graceful degradation when agents fail

## Performance Considerations

- **Async Operations**: Future agents should use async/await
- **Caching**: Cache parsed documents and analysis results
- **Batch Processing**: Process multiple documents in parallel
- **Streaming**: Use LangGraph streaming for real-time updates

## Security Considerations

- **API Keys**: Store in environment variables, never commit
- **Data Privacy**: Encrypt sensitive resume data
- **Access Control**: Role-based permissions for job postings
- **Rate Limiting**: Prevent API abuse
- **Input Validation**: Sanitize all user inputs

## Monitoring & Observability

Future implementations should include:
- Agent execution time tracking
- Success/failure rates per agent
- State transition logging
- Error aggregation and alerting
- User journey tracking

---

**Document Version**: 1.0  
**Last Updated**: 2025-12-02  
**Status**: Iron Skeleton Complete

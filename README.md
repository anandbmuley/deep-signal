# Deep Signal

Agentic AI enabled job portal or talent hunt platform powered by LangGraph.

## 🏗️ Iron Skeleton v0.1.0

This repository contains the "Iron Skeleton" - a complete architectural proof-of-concept for the Tri-Agent AI workflow. The skeleton demonstrates that our architecture is valid with placeholder agents, ready to be filled with real implementations.

## 🎯 Architecture

The Deep Signal platform uses a **Tri-Agent** architecture orchestrated by LangGraph:

```
┌─────────────────────────────────────────────────────────┐
│                     Input Document                      │
│                    (Resume/Job PDF)                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   🔍 Parser Agent      │
        │  Extracts structured   │
        │  data from documents   │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │  🧠 Analyzer Agent     │
        │  Analyzes content,     │
        │  extracts insights     │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │  🎯 Matcher Agent      │
        │  Matches candidates    │
        │  with jobs             │
        └──────────┬─────────────┘
                   │
                   ▼
        ┌────────────────────────┐
        │   📊 Match Results     │
        │   & Recommendations    │
        └────────────────────────┘
```

### Agent Responsibilities

1. **Parser Agent**: Extracts structured data from PDF documents (resumes, job descriptions)
2. **Analyzer Agent**: Analyzes parsed content to extract skills, experience, and key insights
3. **Matcher Agent**: Matches candidates with jobs based on analysis results

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/anandbmuley/deep-signal.git
cd deep-signal

# Install dependencies
pip install -r requirements.txt

# (Optional) Set up environment variables
cp .env.example .env
# Edit .env with your API keys if needed
```

### Running the Iron Skeleton

```bash
python main.py
```

This will run the complete Tri-Agent workflow with placeholder logic, demonstrating that the architecture is valid.

## 📁 Project Structure

```
deep-signal/
├── src/
│   └── deep_signal/
│       ├── __init__.py
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── parser_agent.py      # Parser agent implementation
│       │   ├── analyzer_agent.py    # Analyzer agent implementation
│       │   └── matcher_agent.py     # Matcher agent implementation
│       ├── state/
│       │   ├── __init__.py
│       │   └── graph_state.py       # LangGraph state definition
│       └── workflow.py              # LangGraph workflow orchestration
├── tests/                           # Test directory
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project configuration
└── README.md                        # This file
```

## 🔧 Technology Stack

- **LangGraph**: Workflow orchestration and state management
- **LangChain**: AI agent framework
- **Pydantic**: Data validation and settings management
- **Python 3.11+**: Core language

## 🎯 Current Status: Iron Skeleton

✅ **Completed:**
- Project structure set up
- LangGraph state machine defined
- Tri-Agent architecture implemented with placeholders
- Workflow orchestration functional
- Main execution script working
- Architecture validated

🚧 **Next Steps:**
- Implement real PDF parsing in Parser Agent
- Add AI-powered analysis in Analyzer Agent
- Build job matching logic in Matcher Agent
- Add database integration
- Create web API
- Build frontend interface

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest tests/
```

## 📝 License

[Add license information]

## 🤝 Contributing

[Add contribution guidelines]

## 📧 Contact

Anand Muley - [GitHub](https://github.com/anandbmuley)

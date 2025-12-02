# Quick Start Guide - Deep Signal Iron Skeleton

This guide will help you get started with the Deep Signal Tri-Agent workflow.

## What is the Iron Skeleton?

The Iron Skeleton is a complete, working implementation of the Tri-Agent architecture with placeholder logic. It proves that the workflow structure is valid before investing time in complex implementations.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/anandbmuley/deep-signal.git
   cd deep-signal
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if you plan to add AI features later
   ```

## Running the Iron Skeleton

Simply run the main script:

```bash
python main.py
```

You should see output like this:

```
╔══════════════════════════════════════════════════════════════╗
║                    DEEP SIGNAL                               ║
║         Tri-Agent AI Job Matching Platform                   ║
║                  Iron Skeleton v0.1.0                        ║
╚══════════════════════════════════════════════════════════════╝

🚀 Starting Tri-Agent Workflow
============================================================

🔍 PARSER AGENT ACTIVATED
...
✅ Parsing complete!

🧠 ANALYZER AGENT ACTIVATED
...
✅ Analysis complete!

🎯 MATCHER AGENT ACTIVATED
...
✅ Matching complete!

✨ Workflow Complete!
============================================================

📊 FINAL RESULTS
...
🎉 SUCCESS! The Iron Skeleton is complete!
```

## Running Tests

Verify everything works correctly:

```bash
pytest tests/ -v
```

All 4 tests should pass:
- ✅ Workflow completes successfully
- ✅ Parser agent produces output
- ✅ Analyzer agent produces output
- ✅ Matcher agent produces output

## Understanding the Architecture

### The Three Agents

1. **Parser Agent** (`src/deep_signal/agents/parser_agent.py`)
   - **Purpose:** Extract structured data from PDFs
   - **Current:** Returns mock parsed resume data
   - **Future:** Will parse real PDFs using PyPDF2/pdfplumber

2. **Analyzer Agent** (`src/deep_signal/agents/analyzer_agent.py`)
   - **Purpose:** Analyze content and extract insights
   - **Current:** Returns mock analysis with skills and experience
   - **Future:** Will use LLMs (GPT-4, Claude) for deep analysis

3. **Matcher Agent** (`src/deep_signal/agents/matcher_agent.py`)
   - **Purpose:** Match candidates with jobs
   - **Current:** Returns mock matching scores and recommendations
   - **Future:** Will use vector similarity and ranking algorithms

### The Workflow

The workflow is orchestrated by LangGraph in `src/deep_signal/workflow.py`:

```
Input → Parser → Analyzer → Matcher → Results
```

Each agent:
1. Receives the current state
2. Performs its task (currently with mock data)
3. Updates the state with results
4. Passes control to the next agent

### The State

The `GraphState` (in `src/deep_signal/state/graph_state.py`) maintains all data:
- Input data
- Parsed content
- Analysis results
- Match results
- Status flags
- Error information

## Next Steps

Now that the Iron Skeleton is working, you can:

1. **Replace Parser Agent**: Implement real PDF parsing
   ```python
   # In parser_agent.py
   import pdfplumber
   with pdfplumber.open(input_data) as pdf:
       text = pdf.pages[0].extract_text()
   ```

2. **Replace Analyzer Agent**: Add AI-powered analysis
   ```python
   # In analyzer_agent.py
   from langchain_openai import ChatOpenAI
   llm = ChatOpenAI(model="gpt-4")
   ```

3. **Replace Matcher Agent**: Build matching logic
   ```python
   # In matcher_agent.py
   from langchain_community.vectorstores import FAISS
   ```

4. **Add Database**: Store jobs and candidates
5. **Build API**: Create FastAPI endpoints
6. **Add Frontend**: Build a web interface

## Troubleshooting

### Import Errors
If you get import errors, make sure you're running from the project root:
```bash
cd /path/to/deep-signal
python main.py
```

### Missing Dependencies
Install all requirements:
```bash
pip install -r requirements.txt
```

### Tests Failing
Make sure you have pytest installed:
```bash
pip install pytest pytest-asyncio
```

## Documentation

- **README.md**: Project overview and setup
- **ARCHITECTURE.md**: Detailed architectural documentation
- **This file**: Quick start guide

## Support

For issues or questions:
- Create an issue on GitHub
- Check the ARCHITECTURE.md for detailed explanations
- Review the code comments in each file

---

**Happy Coding! 🚀**

The Iron Skeleton is your foundation. Now build something amazing!

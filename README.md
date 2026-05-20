# 🔍 Local Code Sentry

A fully local, multi-agent AI code review pipeline built with OpenClaw and Ollama.
Zero cloud. Zero cost per run. Your code never leaves your machine.

## What it does

Point it at any Python file and get a full automated code review in under 2 minutes.

    python pipeline.py yourfile.py

Three specialized AI agents work together:

- **Agent 1 — Code Architect** — Finds bugs, security risks, and style issues
- **Agent 2 — Test Engineer** — Automatically writes and runs pytest tests  
- **Agent 3 — Technical Lead** — Produces a final Markdown report with a verdict

## Tech Stack

- Python 3.12
- OpenClaw — agent management framework
- Ollama — local LLM runner (phi3:mini)
- pytest — automated testing

## How to run

1. Install Ollama from https://ollama.com and pull the model:

        ollama pull phi3:mini

2. Install Python dependencies:

        pip install ollama pytest

3. Run on any Python file:

        python pipeline.py yourfile.py

## Project Structure

    code_sentry/
    ├── agents/
    │   ├── agent1_architect.md   ← Code Architect prompt
    │   ├── agent2_engineer.md    ← Test Engineer prompt
    │   └── agent3_lead.md        ← Technical Lead prompt
    ├── sample_code/
    │   ├── calculator.py         ← Buggy sample file 1
    │   └── bank_account.py       ← Buggy sample file 2
    ├── tools/
    │   ├── file_reader.py        ← Safe file reading tool
    │   └── test_runner.py        ← Safe test runner tool
    ├── pipeline.py               ← Main orchestration script
    └── REVIEW_REPORT.md          ← Auto-generated review report

## What I learned

- Multi-agent AI orchestration
- Secure tool design with least-privilege principles
- Local LLM integration with Ollama
- Automated testing with pytest
- Software development lifecycle in practice

## Sample output

Agent 1 found these issues in a test file:

    [SECURITY] Hardcoded password on line 8
    [BUG] Division by zero — no check on line 21
    [BUG] Crashes on empty list on line 30
    VERDICT: CHANGES REQUESTED
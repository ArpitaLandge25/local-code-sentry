"""
pipeline.py
Main orchestration script for Local Code Sentry.

Usage:
    python pipeline.py calculator.py
    python pipeline.py C:\\Users\\Arpita\\Documents\\myproject\\app.py
    python pipeline.py C:\\any\\folder\\anyfile.py
"""

import ollama
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tools"))

from file_reader import read_python_file
from test_runner import run_pytest

# ── Configuration ──────────────────────────────────────────────────────────────
MODEL       = "phi3:mini"
REPORT_FILE = "REVIEW_REPORT.md"


# ── Helper: read agent system prompt ───────────────────────────────────────────
def load_prompt(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), "agents", filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── Helper: ask the model ──────────────────────────────────────────────────────
def ask_agent(system_prompt: str, user_message: str) -> str:
    print("  Thinking...\n")
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ]
    )
    return response["message"]["content"]


# ── Helper: safely read ANY .py file from ANY location ────────────────────────
def read_any_python_file(filepath: str) -> dict:
    """
    Read any .py file from any location on the computer.
    """
    # Get absolute path
    abs_path = os.path.abspath(filepath)

    # Must be a .py file
    if not abs_path.endswith(".py"):
        return {
            "success": False,
            "error": f"Blocked: only .py files are allowed. Got '{filepath}'."
        }

    # Must exist
    if not os.path.isfile(abs_path):
        return {
            "success": False,
            "error": f"File not found: '{abs_path}'"
        }

    # Size cap 50KB
    size = os.path.getsize(abs_path)
    if size > 50_000:
        return {
            "success": False,
            "error": f"File too large: {size} bytes exceeds 50KB limit."
        }

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "content": content}
    except OSError as e:
        return {"success": False, "error": f"OS error: {e}"}


# ── Agent 1: Code Architect ────────────────────────────────────────────────────
def run_agent1(filepath: str) -> str:
    print("=" * 50)
    print(f"AGENT 1 — Code Architect")
    print(f"Reviewing: {filepath}")
    print("=" * 50)

    result = read_any_python_file(filepath)
    if not result["success"]:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    source_code = result["content"]
    print(f"Read file successfully ({len(source_code)} characters)\n")

    system_prompt = load_prompt("agent1_architect.md")
    user_message  = f"Please review this Python code:\n\n{source_code}"
    findings      = ask_agent(system_prompt, user_message)

    print("FINDINGS FROM AGENT 1:")
    print(findings)
    print()

    return findings


# ── Agent 2: Test Engineer ─────────────────────────────────────────────────────
def run_agent2(filepath: str) -> str:
    print("=" * 50)
    print(f"AGENT 2 — Test Engineer")
    print(f"Testing: {filepath}")
    print("=" * 50)

    result = read_any_python_file(filepath)
    if not result["success"]:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    source_code   = result["content"]
    system_prompt = load_prompt("agent2_engineer.md")
    user_message  = f"Write pytest tests for this Python code:\n\n{source_code}"
    test_code     = ask_agent(system_prompt, user_message)

    # Strip markdown if model wrapped code in backticks
    if "```python" in test_code:
        test_code = test_code.split("```python")[1].split("```")[0].strip()
    elif "```" in test_code:
        test_code = test_code.split("```")[1].split("```")[0].strip()

    # Save test file next to the original file
    original_dir  = os.path.dirname(os.path.abspath(filepath))
    base_name     = os.path.splitext(os.path.basename(filepath))[0]
    test_filename = f"test_{base_name}.py"
    test_path     = os.path.join(original_dir, test_filename)

    with open(test_path, "w", encoding="utf-8") as f:
        f.write(test_code)
    print(f"Saved test file to {test_path}\n")

    # Run the tests
    print("Running tests...\n")
    result = run_pytest(test_path)

    if result["error"]:
        test_results = f"ERROR: {result['error']}"
    else:
        test_results = result["stdout"]
        if result["stderr"]:
            test_results += "\nSTDERR:\n" + result["stderr"]

    print("TEST RESULTS:")
    print(test_results)
    print()

    return test_results


# ── Agent 3: Technical Lead ────────────────────────────────────────────────────
def run_agent3(filepath: str, findings: str, test_results: str) -> str:
    print("=" * 50)
    print(f"AGENT 3 — Technical Lead")
    print(f"Writing report for: {filepath}")
    print("=" * 50)

    system_prompt = load_prompt("agent3_lead.md")
    user_message  = f"""
File reviewed: {filepath}

Findings from Code Architect (Agent 1):
{findings}

Test results from Test Engineer (Agent 2):
{test_results}

Please write the final review report.
"""

    report = ask_agent(system_prompt, user_message)

    print("FINAL REPORT FROM AGENT 3:")
    print(report)
    print()

    return report


# ── Main pipeline ──────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python pipeline.py myfile.py")
        print("  python pipeline.py C:\\Users\\Arpita\\Documents\\app.py")
        sys.exit(1)

    filepath = sys.argv[1]

    # Confirm file exists before starting
    if not os.path.isfile(os.path.abspath(filepath)):
        print(f"\nERROR: File not found — '{filepath}'")
        print("Please check the path and try again.")
        sys.exit(1)

    print(f"\n🔍 Local Code Sentry — Starting Pipeline")
    print(f"   File  : {os.path.abspath(filepath)}")
    print(f"   Model : {MODEL}\n")

    findings     = run_agent1(filepath)
    test_results = run_agent2(filepath)
    report       = run_agent3(filepath, findings, test_results)

    # Save report next to the reviewed file
    report_path = os.path.join(
        os.path.dirname(os.path.abspath(filepath)),
        REPORT_FILE
    )

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("=" * 50)
    print(f"✅ Pipeline complete!")
    print(f"   Report saved to: {report_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
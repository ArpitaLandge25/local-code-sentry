"""
Tool: test_runner.py
Agent: Test Engineer (Agent 2)
Purpose: Run pytest on a test file and capture the results.
"""

import os
import subprocess
import sys

TIMEOUT_SECONDS = 30


def run_pytest(test_filepath: str) -> dict:
    """
    Run pytest on a test file. Accepts full path or just filename.
    """
    # Get absolute path
    abs_path = os.path.abspath(test_filepath)

    # Must end in .py
    if not abs_path.endswith(".py"):
        return _blocked(f"Only .py files allowed. Got: '{test_filepath}'")

    # Filename must start with test_
    base = os.path.basename(abs_path)
    if not base.startswith("test_"):
        return _blocked(f"Test files must be named test_*.py. Got: '{base}'")

    # Must exist
    if not os.path.isfile(abs_path):
        return _blocked(f"Test file not found: '{abs_path}'")

    command = [
        sys.executable, "-m", "pytest",
        abs_path,
        "-v",
        "--tb=short",
        "--no-header",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=os.path.dirname(abs_path),
        )
        return {
            "success":    result.returncode == 0,
            "returncode": result.returncode,
            "stdout":     result.stdout,
            "stderr":     result.stderr,
            "error":      "",
        }

    except subprocess.TimeoutExpired:
        return {
            "success":    False,
            "returncode": -1,
            "stdout":     "", "stderr": "",
            "error":      f"Timed out after {TIMEOUT_SECONDS} seconds.",
        }
    except FileNotFoundError:
        return {
            "success":    False,
            "returncode": -1,
            "stdout":     "", "stderr": "",
            "error":      "pytest not found. Run: pip install pytest",
        }


def _blocked(reason: str) -> dict:
    return {
        "success":    False,
        "returncode": -1,
        "stdout":     "", "stderr": "",
        "error":      f"Blocked: {reason}",
    }
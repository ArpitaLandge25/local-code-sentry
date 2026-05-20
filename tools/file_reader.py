"""
Tool: file_reader.py
Agent: Code Architect (Agent 1)
Purpose: Safely read a Python source file for analysis.
"""

import os

ALLOWED_BASE_DIR = os.path.abspath("sample_code")
MAX_FILE_SIZE_BYTES = 50_000


def read_python_file(relative_path: str) -> dict:

    if not relative_path.endswith(".py"):
        return {
            "success": False,
            "error": f"Blocked: only .py files are allowed. Got '{relative_path}'.",
        }

    target_path = os.path.realpath(os.path.join(ALLOWED_BASE_DIR, relative_path))
    allowed_root = os.path.realpath(ALLOWED_BASE_DIR)

    if not target_path.startswith(allowed_root + os.sep) and target_path != allowed_root:
        return {
            "success": False,
            "error": "Blocked: directory traversal is not permitted.",
        }

    if not os.path.isfile(target_path):
        return {
            "success": False,
            "error": f"File not found: '{relative_path}' does not exist.",
        }

    size = os.path.getsize(target_path)
    if size > MAX_FILE_SIZE_BYTES:
        return {
            "success": False,
            "error": f"File too large: {size} bytes exceeds the limit.",
        }

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"success": True, "content": content}
    except OSError as e:
        return {"success": False, "error": f"OS error: {e}"}


if __name__ == "__main__":
    print("=== file_reader.py self-test ===\n")

    tests = [
        ("Normal read",         "calculator.py"),
        ("Directory traversal", "../../etc/passwd"),
        ("Wrong extension",     "notes.txt"),
        ("Missing file",        "ghost.py"),
    ]

    for label, path in tests:
        result = read_python_file(path)
        print(f"[{label}]: {result}\n")
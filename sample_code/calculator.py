"""
calculator.py
This file has 4 intentional bugs hidden inside it.
The pipeline agents will find and report them.
"""

# BUG 1 — Hardcoded password (security risk)
DB_PASSWORD = "supersecret123"


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    # BUG 2 — No check if b is zero, will crash
    return a / b


def average(numbers):
    # BUG 3 — Crashes if the list is empty
    return sum(numbers) / len(numbers)


def find_max(items):
    # BUG 4 — Returns None silently on empty list instead of raising an error
    if len(items) == 0:
        return None
    max_val = items[0]
    for item in items:
        if item > max_val:
            max_val = item
    return max_val
"""
bank_account.py
A simple bank account system.
Contains intentional bugs for pipeline testing.
"""

# BUG 1 — Hardcoded secret key (security risk)
SECRET_KEY = "mybank_admin_1234"


class BankAccount:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        # BUG 2 — No check for negative deposits
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        # BUG 3 — No check if balance is enough
        self.balance -= amount
        return self.balance

    def get_balance(self):
        return self.balance

    def transfer(self, amount, target_account):
        # BUG 4 — No validation that amount is positive
        self.balance -= amount
        target_account.balance += amount

    def transaction_history(self, records):
        # BUG 5 — Crashes if records list is empty
        return records[0]
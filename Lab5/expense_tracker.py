"""Personal monthly expense tracker for the Lab 5 static analysis exercise.

Records expenses by category, rejects invalid amounts, totals spending per
category, tracks the remaining monthly budget, reports the biggest expense
and verifies a bank-sync password supplied through the environment.
"""

import hmac
import os
import tempfile
import webbrowser
from datetime import datetime

BANK_SYNC_ENV_VAR = "BANK_SYNC_PASSWORD"
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")
DEFAULT_MONTHLY_BUDGET = 20000

EXPENSES = []
_BUDGET = {"monthly": DEFAULT_MONTHLY_BUDGET}


def add_expense(amount, category="Misc", note=""):
    """Record one expense, or reject a non-positive amount.

    Returns True when the expense was recorded, False when it was ignored.
    """
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    EXPENSES.append({
        "amount": amount,
        "category": category,
        "note": note,
        "time": datetime.now().isoformat(),
    })
    return True


def total_by_category():
    """Return a mapping of category name to the total spent in it."""
    totals = {}
    for expense in EXPENSES:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Replace the monthly budget with new_budget."""
    _BUDGET["monthly"] = new_budget


def remaining_budget():
    """Return how much of the monthly budget is still unspent."""
    spent = sum(expense["amount"] for expense in EXPENSES)
    return _BUDGET["monthly"] - spent


def biggest_expense():
    """Return the largest recorded expense, or None when none are recorded."""
    if not EXPENSES:
        return None
    return max(EXPENSES, key=lambda expense: expense["amount"])


def print_ledger():
    """Print every recorded expense with a 1-based index."""
    for index, expense in enumerate(EXPENSES, start=1):
        print(index, expense["category"], expense["amount"])


def check_sync_password(password):
    """Compare password against the bank-sync secret held in the environment.

    Returns False when no secret is configured. The comparison is constant
    time so that it does not leak the secret through its timing.
    """
    expected = os.environ.get(BANK_SYNC_ENV_VAR, "")
    if not expected:
        return False
    return hmac.compare_digest(password, expected)


def export_report():
    """Create an empty report file securely and return its path."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    handle, report_path = tempfile.mkstemp(suffix=".txt", dir=REPORT_DIR)
    os.close(handle)
    return report_path


def open_statement(path):
    """Open a statement file with the desktop's default application."""
    webbrowser.open(f"file://{os.path.abspath(path)}")


def main():
    """Run a short demonstration of the tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:", len(EXPENSES),
        "expenses recorded against a budget of", _BUDGET["monthly"],
    )


if __name__ == "__main__":
    main()

# Lab 5 — Static Code Analysis

**Name:** ES Sukruth
**SRN:** PES1UG24CS160
**Source script from:** `SETAPESU26/L5_32_expense_tracker`
**Submitted in:** `SUKRUTH-ES/UE24CS341A-Software-Engineering`
**Script analysed:** `expense_tracker.py` (Personal Expense Tracker)

## Results

| Tool | Before | After | Target | Met |
|---|---|---|---|---|
| Pylint | 5.27/10 (26 messages) | **10.00/10** (0 messages) | > 9.5 | ✅ |
| Bandit | 4 issues — 1 High, 2 Medium, 1 Low | **0 issues** | all handled | ✅ |
| Flake8 | 4 style errors | **0 errors** | all handled | ✅ |

13 distinct issues documented and fixed (minimum required: 4). The program's
console output is byte-for-byte identical before and after the fixes.

## Deliverables

| Deliverable | File |
|---|---|
| Cleaned script | `expense_tracker.py` |
| Issue documentation table | `issues.md` |
| Reflection answers | `reflection.md` |
| Pylint report (before / after) | `before/pylint_report.txt`, `after/pylint_report.txt` |
| Bandit report (before / after) | `before/bandit_report.txt`, `after/bandit_report.txt` |
| Flake8 report (before / after) | `before/flake8_report.txt`, `after/flake8_report.txt` |
| Original program output (behaviour baseline) | `program_output_before.txt` |
| Intermediate commit stages | `stages/` |

## Security issues fixed (Bandit)

| ID | Severity | Issue | Fix |
|---|---|---|---|
| B605 | **High** | `os.system("xdg-open " + path)` — command injection (CWE-78) | Replaced with `webbrowser.open()`; no shell involved |
| B306 | Medium | `tempfile.mktemp()` — symlink race (CWE-377) | Replaced with `tempfile.mkstemp()` |
| B108 | Medium | Hardcoded `/tmp` directory | `tempfile.gettempdir()` at runtime |
| B105 | Low | Bank-sync password committed in plaintext (CWE-259) | Read from environment; `hmac.compare_digest()` comparison |

## Reproducing

```bash
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8

python expense_tracker.py                       # demo run

pylint expense_tracker.py > pylint_report.txt
bandit -r expense_tracker.py > bandit_report.txt
flake8 expense_tracker.py > flake8_report.txt
```

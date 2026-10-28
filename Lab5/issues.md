# Lab 5: Static Code Analysis — Identified Issues

**Name:** E S Sukruth
**SRN:** PES1UG24CS160
**Repo:** `L5_32_expense_tracker`
**File analysed:** `expense_tracker.py`

## Tool results summary

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.27/10 — 26 messages | **10.00/10 — 0 messages** |
| Bandit | 4 issues (1 High, 2 Medium, 1 Low) | **0 issues** |
| Flake8 | 4 style errors | **0 errors** |

The program's console output is byte-for-byte identical before and after the
fixes, so behaviour was preserved.

## Issue table

Ordered by severity: Bandit security findings first, then Pylint quality
findings, then Flake8 style findings.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | B605 `start_process_with_a_shell` | Security — **High** | 61 | `os.system("xdg-open " + path)` builds a shell command by string concatenation. A path containing `;` or `&&` injects arbitrary commands (CWE-78 command injection). | Removed the shell entirely. Replaced with `webbrowser.open()` on a `file://` URL built from `os.path.abspath(path)`, so no shell ever parses the value. |
| 2 | B306 `blacklist` (mktemp) | Security — **Medium** | 55 | `tempfile.mktemp()` only returns a *name*; between that call and the file being opened, an attacker can create a symlink at the same path (CWE-377 race condition). The function is deprecated for this reason. | Switched to `tempfile.mkstemp()`, which atomically creates the file and returns an open handle. The handle is closed and the path returned. |
| 3 | B108 `hardcoded_tmp_directory` | Security — **Medium** | 8 | `REPORT_DIR = "/tmp/expense_reports"` hardcodes a world-writable directory, which is both insecure and non-portable (fails on Windows). | Built the path at runtime with `os.path.join(tempfile.gettempdir(), "expense_reports")`, which honours the platform's temp location. |
| 4 | B105 `hardcoded_password_string` | Security — **Low** | 5 | The bank-sync secret `"demo-sync-pass"` is committed in plaintext in source control (CWE-259). Anyone with repo read access has the credential. | Removed the literal. The secret is now read at call time from the `BANK_SYNC_PASSWORD` environment variable; the function returns `False` when none is configured. Comparison uses `hmac.compare_digest()` so it is constant-time and cannot leak the secret through response timing. |
| 5 | W0718 `broad-exception-caught` | Bug risk | 41 | `except Exception` around `max()` swallows *every* error — a `KeyError` from a malformed record is silently reported as "no expenses". It masks real bugs. | Removed the `try`/`except` and replaced it with an explicit `if not EXPENSES: return None` guard, so only the genuinely-empty case returns `None` and real errors propagate. |
| 6 | W0603 `global-statement` | Maintainability | 29 | `set_budget()` uses `global monthly_budget` to rebind module state. Global rebinding makes the data flow hard to follow and hard to test. | Moved the budget into a module-level dict `_BUDGET` and mutate `_BUDGET["monthly"]`. Mutating a container needs no `global` statement, so the warning disappears and the state has one clear owner. |
| 7 | C0103 `invalid-name` (×12) | Style/Convention | 7, 11, 20, 28, 33, 38, 44, 49, 53, 55, 59 | Functions, the argument `newBudget`, the variable `reportPath` and the module constant `monthly_budget` all use camelCase, violating PEP 8 / snake_case. | Renamed every function to snake_case (`addExpense` → `add_expense`, etc.), `newBudget` → `new_budget`, `reportPath` → `report_path`, and promoted module-level data to UPPER_CASE (`EXPENSES`, `_BUDGET`, `REPORT_DIR`). |
| 8 | C0114 / C0116 `missing-docstring` (×11) | Documentation | 1, and every function | No module docstring and no function docstrings, so the file's purpose and each function's contract were undocumented. | Added a module docstring and a docstring to all ten functions, each stating what is returned and any edge-case behaviour. |
| 9 | C0200 `consider-using-enumerate` | Readability | 45 | `for i in range(len(expenses))` indexes the list manually — the unidiomatic C-style loop, and `expenses[i]` is repeated twice per iteration. | Rewrote as `for index, expense in enumerate(EXPENSES, start=1)`, which also removed the `i + 1` arithmetic in the `print`. |
| 10 | E501 `line-too-long` | Style | 77 | The summary `print` was 93 characters, over PEP 8's 79-character limit. | Split the call across multiple lines inside the existing parentheses. |
| 11 | E302 `expected 2 blank lines` | Style | 44 | Only one blank line before `printLedger`; PEP 8 requires two between top-level definitions. | Added the second blank line. |
| 12 | E203 `whitespace before ':'` | Style | 15 | The dict literal was written `{"amount" : amount, ...}` with a stray space before the colon. | Removed the space and reformatted the dict literal one key per line. |
| 13 | E261 `two spaces before inline comment` | Style | 74 | The inline comment `# after setBudget` had a single space before `#`. | Added the second space (and updated the comment text to the renamed function). |

## Additional improvement (not tool-flagged)

`main()` was invoked unconditionally at module scope, so merely importing the
file ran the whole demo. It is now guarded by
`if __name__ == "__main__":`, which keeps the script runnable while making the
module safely importable — needed for the helper-function testing done during
verification.

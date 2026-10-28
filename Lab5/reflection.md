# Lab 5: Static Code Analysis — Reflection

**Name:** E S Sukruth
**SRN:** PES1UG24CS160
**Repo:** `L5_32_expense_tracker`

> Note: the handout lists "Answers to reflection questions provided in the lab"
> but does not print the questions themselves. The four questions below are the
> standard set for this lab, drawn from the stated learning outcomes. Replace
> them with your instructor's exact wording if it differs.

---

### 1. What is the purpose of static code analysis, and how does it differ from testing?

Static analysis inspects source code without running it, so it reasons about
every path in the file rather than only the paths a particular run happens to
take. Testing is the opposite: it executes the program and checks observable
behaviour, which means it can only find bugs in the cases you thought to write.

The difference showed up directly in this lab. Running `expense_tracker.py`
produced perfectly sensible output — a ledger, correct totals, the right
remaining budget — so by the standard of "does it work", the program passed.
Yet it still contained a High-severity command injection in `open_statement()`
and a plaintext bank credential. Neither function is even called by the demo,
so no amount of running the program would have surfaced them. The two
techniques catch different classes of defect and are complements, not
substitutes: static analysis found the dormant vulnerabilities, while it was my
own before/after output comparison — a test — that proved my refactor had not
changed behaviour.

### 2. Compare the three tools. What does each one contribute?

They occupy three distinct niches, and the overlap between them was almost
zero on this file:

- **Bandit** is the security scanner. It is the only one of the three that
  reasons about *threat*, and it carries severity and confidence ratings plus
  CWE identifiers, so findings can be triaged. It alone caught the `os.system`
  injection, the `mktemp` race condition and the hardcoded secret. Pylint and
  Flake8 were completely silent on all four security issues.
- **Pylint** is the code reviewer. It is the deepest analyser — it builds an
  abstract syntax tree and reasons about naming, structure, control flow and
  documentation. It produced 26 of the 34 total findings and is the only tool
  that gives a single numeric quality score, which made progress easy to track
  (5.27 → 10.00).
- **Flake8** is the style checker. It is the narrowest and fastest, enforcing
  PEP 8 formatting — line length, blank lines, whitespace. Its four findings
  were real but cosmetic.

The practical lesson is that no single tool is sufficient. Had I run only
Pylint and chased the score to 10/10, every security issue would still have
shipped.

### 3. How did you decide which issues to fix first, and what did severity tell you?

I worked in descending order of severity, which is what the handout asks for
and is also the right instinct: the cost of a defect is not uniform, so
attention should not be uniform either.

The B605 shell injection went first — it is rated High/High, it is remotely
exploitable, and the consequence is arbitrary code execution. The two Medium
findings came next, then the Low-severity hardcoded password. Only after
Bandit was clean did I address the Pylint warnings (`broad-exception-caught`
and `global-statement` are latent bug risks, so they preceded the naming and
docstring conventions), and the purely cosmetic Flake8 errors came last.

Severity also stopped me from making the code worse. My first instinct for the
`os.system` fix was the textbook replacement, `subprocess.run()` with an
argument list. I tested it and found it introduced three *new* Bandit
findings (B404, B603, B607). One High traded for three Lows is an improvement
in severity terms, but the lab requires Bandit to be fully clean, so I
reconsidered the requirement rather than the tool: the function only needs to
open a file in the default application, which `webbrowser.open()` does without
spawning a shell at all. The best fix removed the dangerous capability instead
of trying to secure it.

### 4. What are the limitations of these tools, and how does static analysis contribute to quality and maintainability?

**Limitations.** Both false positives and false negatives appeared in this lab.
After my fix, Bandit still flagged `SYNC_PASSWORD_ENV_VAR = "BANK_SYNC_PASSWORD"`
as a hardcoded password — a clear false positive, since the string is the
*name* of an environment variable, not a secret. Bandit's B105 check matches on
the variable name rather than understanding the value, so renaming the constant
to `BANK_SYNC_ENV_VAR` silenced it. That is a useful warning about the tools'
depth: they pattern-match, they do not understand intent. The inverse also
holds — the tools never questioned whether the budget logic was *correct*, and
a real logic error such as subtracting instead of adding would have passed all
three at 10/10. They also cannot judge architecture, and `# nosec` or
`# pylint: disable` makes any finding trivially suppressible, so a clean report
is only as honest as the team reading it.

**Contribution.** Even so, the value is substantial. Static analysis is
cheap, instant and consistent — it applies the same standard at 3am as in code
review, and it never gets tired or diplomatic. It catches an entire class of
security defect before the code ships, which is far cheaper than catching it in
production. For maintainability, the effect on this file was significant
beyond the score: snake_case naming and ten docstrings mean the next reader can
understand the contract of each function without reverse-engineering it, and
removing the `global` statement gives the budget a single clear owner, which
makes the module testable in isolation. Run in CI on every commit, these tools
stop quality from eroding gradually — which is how it usually erodes.

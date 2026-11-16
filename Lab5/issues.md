# Lab 5: Static Code Analysis — Issues Found

The line numbers below refer to the **original** `premium_calculator.py` uploaded with the initial reports.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe TAR extraction | Security — High | 63–67 | `extractall()` extracts customer-provided archive members without checking whether paths escape the destination. | Resolve each target path and reject paths outside the destination; reject links/devices and use the `data` extraction filter. |
| TLS certificate verification disabled | Security — Medium | 59–61 | `_create_unverified_context()` disables certificate and hostname checks, allowing an untrusted endpoint to impersonate the rate server. | Use Python's default verified TLS context, restrict the URL to HTTPS, and set a timeout. |
| Unsafe XML parser for untrusted input | Security — Medium | 9, 49–50 | `xml.etree.ElementTree` parses supplied XML without protections against XML-based attacks. | Use `defusedxml.ElementTree` and handle expected malformed-field exceptions specifically. |
| Hardcoded underwriter token | Security — Low (Bandit B105) | 15, 75–76 | A credential embedded in source code can be exposed to anyone who can read the file or repository. | Read the token from an environment variable and fail closed if it is not configured. |
| Mutable default argument | Correctness / maintainability | 19, 29 | `discounts=[]` is a shared list across calls, and `discounts.append(500)` mutates it. This can make otherwise identical quotes differ. | Use `None` as the default and treat missing discounts as an empty list without mutating caller data. |
| Age calculation ignores birthday | Logic bug | 32–36 | Subtracting birth year from current year overstates age when the birthday has not happened yet this year. | Compare the current month/day with the birth month/day before finalizing the age. |
| Leap-day renewal can fail | Logic bug | 81–83 | Replacing the year on a February 29 date raises `ValueError` when the target year is not a leap year. | Define a consistent rule, such as moving the renewal to February 28 in non-leap years. |
| Bare exception handler | Code quality / robustness | 54–56 | `except:` catches every exception, including exceptions that should not be silently swallowed. | Catch only expected conversion errors such as `TypeError` and `ValueError`. |
| Zero or negative instalment months | Logic bug / input validation | 69–73 | Zero is specially handled, but negative values produce an invalid instalment instead of a clear error. | Require `months > 0`, otherwise raise `ValueError`. |
| Inaccurate smoker input in demo | Logic bug / demonstration | 94 | The string `"no"` is truthy in Python, so the premium function treats this example as a smoker. | Pass the boolean `False` for a non-smoker. |
| File handle and encoding not managed | Code quality | 41–46 | The log file is manually opened and closed without an explicit encoding; an exception can leave it open. | Use a `with` block and specify UTF-8 encoding. |
| Naming, documentation, and formatting violations | Style | Multiple | CamelCase names, missing docstrings, long lines, and inconsistent blank lines triggered Pylint/Flake8 findings. | Use snake_case names, add docstrings, wrap long lines, and follow PEP 8 spacing. |

## Notes on the original reports

- Bandit reported 1 high, 5 medium, and 4 low-severity findings in the uploaded report. The TAR extraction issue was its high-severity finding.
- Flake8 reported line-length, blank-line, and bare-except issues.
- Pylint rated the original file 5.73/10 and reported the mutable default, missing docstrings, naming, file-handling, and other maintainability issues.
- The line numbers above are from the original file and will change after edits.

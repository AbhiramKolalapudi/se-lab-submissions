# Lab 5: Static Code Analysis — Reflection

## 1. What did the static analysis tools identify?

Pylint identified code-quality and maintainability issues, including missing docstrings, naming problems, and excessive function arguments. The initial Pylint score was 5.73/10. Flake8 reported formatting and style violations, while Bandit identified potential security risks, including unsafe archive extraction and potentially unsafe network and XML handling.

## 2. Which issues were most important to fix, and why?

The unsafe archive extraction issue was particularly important because malicious archive paths could potentially cause files to be written outside the intended directory. Other important issues included unsafe XML parsing and network requests that could expose the application to security risks. Addressing these issues helped improve the program's security and reliability.

## 3. What changes did you make, and what were the final results?

I improved the code by using safer XML parsing, validating archive paths, checking that rate-download URLs use HTTPS, adding a network timeout, and reading the underwriter token from an environment variable. I also improved input validation, exception handling, documentation, and formatting. After these changes, Pylint improved from 5.73/10 to 9.83/10, exceeding the required score of 9.5. Flake8 produced an empty report, indicating no reported style violations, and Bandit reported no issues, although one check was explicitly suppressed using `# nosec B310`.

## 4. What did you learn about static analysis and its limitations?

I learned that static analysis tools help identify potential bugs, security weaknesses, and style problems without executing the program. Each tool has a different purpose: Pylint focuses on code quality, Flake8 checks style, and Bandit identifies potentially insecure coding patterns. However, passing these tools does not guarantee that a program is completely correct or secure. Findings require human review, and the code should also be tested with normal and edge-case inputs.

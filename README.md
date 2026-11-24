# GenAI-Assisted Content Standardization Workflow

A small, dependency-free Python CLI for conservative text cleanup and
repeatable quality checks. It can also generate a review prompt to use in an
approved Microsoft Copilot experience.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run

From this directory:

```powershell
python app.py samples\sample_input.txt
```

The standardized output is written beside the input as
`sample_input.standardized.txt`. To choose paths and generate optional artifacts:

```powershell
python app.py samples\sample_input.txt `
  --output standardized.txt `
  --report quality-report.txt `
  --copilot-prompt copilot-review.txt
```

The script does not connect to Copilot or send data anywhere. The prompt file
contains the processed text; share it only with an approved Copilot service and
only when permitted by your organization's data-handling rules. Copilot output
requires human review, especially for factual accuracy.

See [documentation/workflow.md](documentation/workflow.md) and
[documentation/quality_checklist.md](documentation/quality_checklist.md) for
the process and review criteria.

## Tests

```powershell
python -m unittest discover -s tests
```

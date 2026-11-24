# Content Standardization Workflow

## Purpose

Use the local Python workflow for repeatable formatting cleanup and mechanical
quality checks. Use Microsoft Copilot as an optional editorial assistant; a
human remains responsible for confirming meaning and factual accuracy.

## Steps

1. Save the source as a UTF-8 `.txt` file and keep the original unchanged.
2. Run `python app.py samples\sample_input.txt` from the project directory.
   The workflow creates `samples\sample_input.standardized.txt`.
3. Review the printed quality report. Resolve flagged placeholders and
   duplicated paragraphs; manually assess long lines where applicable.
4. For an assisted editorial pass, run
   `python app.py <input-file> --copilot-prompt copilot-review.txt`.
5. Paste the generated prompt into an approved Microsoft Copilot experience.
   Review its proposed edits against the source; do not accept unsupported
   changes to facts, figures, names, or dates.
6. Save the approved version, rerun the quality checks, and have the content
   owner approve the final output.

## What the script changes

The script normalizes Unicode to NFC, removes a leading byte-order mark,
normalizes line endings, trims line-edge whitespace, collapses repeated
horizontal whitespace, and limits consecutive blank lines. It does not rewrite
sentences, punctuation, or factual content.

The standard library quality checks flag empty content, likely placeholders,
repeated paragraphs, and lines longer than 120 characters. They are prompts for
review, not proof of an error or of accuracy.

## Example

```powershell
python app.py samples\sample_input.txt --report quality-report.txt --copilot-prompt copilot-review.txt
```

See [quality_checklist.md](quality_checklist.md) for final review criteria.

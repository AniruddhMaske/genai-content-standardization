"""Quality checks for common, mechanically detectable content problems."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class QualityIssue:
    code: str
    message: str
    line: int | None = None


_PLACEHOLDER = re.compile(
    r"\b(?:TODO|TBD|FIXME|lorem ipsum)\b|\[(?:insert|add|replace)\b[^\]]*\]",
    re.IGNORECASE,
)


def check_quality(
    text: str,
    *,
    max_line_length: int = 120
) -> list[QualityIssue]:

    """Report likely editorial follow-ups."""

    if max_line_length < 1:
        raise ValueError("max_line_length must be positive.")

    issues: list[QualityIssue] = []

    if not text.strip():
        return [QualityIssue("empty", "Content is empty.")]

    seen_paragraphs: set[str] = set()
    paragraph_lines: list[str] = []
    paragraph_start_line = 1

    def record_paragraph() -> None:
        if not paragraph_lines:
            return

        normalized = " ".join(paragraph_lines).casefold()

        if normalized in seen_paragraphs:
            issues.append(
                QualityIssue(
                    "duplicate_paragraph",
                    "Paragraph is repeated.",
                    paragraph_start_line,
                )
            )
        else:
            seen_paragraphs.add(normalized)

        paragraph_lines.clear()

    for line_number, line in enumerate(text.splitlines(), start=1):

        if len(line) > max_line_length:
            issues.append(
                QualityIssue(
                    "long_line",
                    f"Line has {len(line)} characters "
                    f"(limit: {max_line_length}).",
                    line_number,
                )
            )

        if _PLACEHOLDER.search(line):
            issues.append(
                QualityIssue(
                    "placeholder",
                    "Possible placeholder text remains.",
                    line_number,
                )
            )

        if line.strip():
            if not paragraph_lines:
                paragraph_start_line = line_number

            paragraph_lines.append(line.strip())
        else:
            record_paragraph()

    record_paragraph()

    return issues
def format_quality_report(
    input_path: Path,
    output_path: Path,
    text: str,
    issues: list[QualityIssue],
) -> str:
    """Render a concise, human-readable workflow report."""

    word_count = len(text.split())

    lines = [
        "Content standardization report",
        f"Input: {input_path}",
        f"Output: {output_path}",
        f"Words: {word_count}",
    ]

    if issues:
        lines.append(f"Findings: {len(issues)}")

        for issue in issues:
            location = (
                f" (line {issue.line})"
                if issue.line is not None
                else ""
            )

            lines.append(
                f"- [{issue.code}]{location} {issue.message}"
            )
    else:
        lines.append("Findings: none")

    lines.append(
        "Note: automated checks cannot verify factual accuracy."
    )

    return "\n".join(lines)

"""Command-line entry point for the content standardization workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from modules.ai_reviewer import build_review_prompt
from modules.content_standardizer import standardize_text
from modules.quality_checker import check_quality, format_quality_report


def _default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.standardized{input_path.suffix}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Clean and standardize text, then run practical quality checks."
    )
    parser.add_argument("input", type=Path, help="UTF-8 text file to process")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="destination for standardized text (default: <name>.standardized<ext>)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="write the quality report to this file (it is also printed)",
    )
    parser.add_argument(
        "--copilot-prompt",
        type=Path,
        help="write a review prompt containing the standardized text for Microsoft Copilot",
    )
    args = parser.parse_args(argv)
    output_path = args.output or _default_output_path(args.input)

    destinations = [output_path]
    if args.report:
        destinations.append(args.report)
    if args.copilot_prompt:
        destinations.append(args.copilot_prompt)
    protected_paths = {args.input.resolve()}
    if len({path.resolve() for path in destinations}) != len(destinations):
        parser.error("Output, report, and Copilot prompt paths must be different.")
    if any(path.resolve() in protected_paths for path in destinations):
        parser.error("Generated files must not overwrite the input.")

    try:
        raw_text = args.input.read_text(encoding="utf-8-sig")
        standardized = standardize_text(raw_text)
        issues = check_quality(standardized)
        report = format_quality_report(args.input, output_path, standardized, issues)

        output_path.write_text(standardized, encoding="utf-8", newline="\n")
        if args.report:
            args.report.write_text(report, encoding="utf-8", newline="\n")
        if args.copilot_prompt:
            prompt = build_review_prompt(standardized)
            args.copilot_prompt.write_text(prompt, encoding="utf-8", newline="\n")
    except (OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(report)
    if args.copilot_prompt:
        print(f"\nCopilot review prompt saved to: {args.copilot_prompt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

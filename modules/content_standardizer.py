
"""Field-aware content standardization rules."""

import re

from modules.text_cleaner import clean_text


FIELD_PATTERN = re.compile(
    r"^\s*([A-Za-z][A-Za-z ]*?)\s*[:\-]\s*(.*?)\s*$"
)

LABELS = {
    "employee name": "Employee Name",
    "department": "Department",
    "joining date": "Joining Date",
    "email id": "Email ID",
    "email": "Email ID",
    "status": "Status",
}


def format_field_value(label: str, value: str) -> str:
    """Apply formatting rules based on the field type."""

    value = value.strip()

    if label == "Employee Name":
        return value.title()

    if label == "Department":
        return value.title()

    if label == "Email ID":
        return value.lower()

    if label == "Status":
        return value.title()

    # Preserve dates and unknown field values.
    return value


def standardize_text(text: str) -> str:
    """Clean text and standardize recognized employee fields."""

    cleaned = clean_text(text)
    lines = cleaned.splitlines()

    standardized_lines = []
    index = 0

    while index < len(lines):

        line = lines[index].strip()

        # Preserve blank lines.
        if not line:
            standardized_lines.append("")
            index += 1
            continue

        # Handle employee responsibility statements.
        responsibility_match = re.match(
            r"^employee\s+is\s+responsible\s+for\s+",
            line,
            re.IGNORECASE,
        )

        if responsibility_match:
            content_parts = [
                line[responsibility_match.end():].strip()
            ]

            index += 1

            # Join wrapped continuation lines.
            while index < len(lines) and lines[index].strip():
                content_parts.append(lines[index].strip())
                index += 1

            responsibility = " ".join(content_parts).strip()

            if responsibility:
                responsibility = (
                    responsibility[0].upper() + responsibility[1:]
                )

                if responsibility[-1] not in ".!?":
                    responsibility += "."

                standardized_lines.append(
                    f"Responsibilities: {responsibility}"
                )

            continue

        # Handle structured fields.
        match = FIELD_PATTERN.match(line)

        if match:
            raw_label = match.group(1).strip()
            value = match.group(2).strip()

            normalized_key = raw_label.casefold()
            label = LABELS.get(
                normalized_key,
                raw_label.title(),
            )

            formatted_value = format_field_value(label, value)

            standardized_lines.append(
                f"{label}: {formatted_value}"
            )

        else:
            # Preserve unrecognized content.
            standardized_lines.append(line)

        index += 1

    return "\n".join(standardized_lines).strip()

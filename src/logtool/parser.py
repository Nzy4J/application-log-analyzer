"""Read JSON Lines logs and validate application records."""

import json
import re
from datetime import datetime


def read_lines(path):
    """Read UTF-8 JSON Lines and print validated records with line numbers.

    Ignore blank lines. Report malformed JSON, non-object values, and
    record-validation errors, then continue. File-opening and decoding
    errors propagate to the caller.
    """
    with open(path, encoding="utf-8") as log_file:
        # Count every physical line so diagnostics match positions in the source file.
        for line_number, line in enumerate(log_file, start=1):
            if not line.strip():
                continue
            try:
                log_entry = json.loads(line)
            except json.JSONDecodeError as error:
                print(line_number, "Invalid JSON:", line.rstrip("\n"), "Error:", error.msg)
                continue

            if not isinstance(log_entry, dict):
                print(line_number, "Record must be a JSON object", line.rstrip("\n"))
                continue

            validation_error = validate_record(log_entry)
            if validation_error:
                print(line_number, "Validation error:", validation_error)
                continue

            print(line_number, log_entry)


def validate_record(log_entry):
    """Return the first validation error, or None if the record passes validation.

    Expect log_entry to be a dictionary.
    """
    fields = ("timestamp", "level", "service", "message")
    for field in fields:
        if field not in log_entry:
            return f"Missing field: {field}"

        if not isinstance(log_entry[field], str):
            return f"Field {field} must be a string"

        if field in ("service", "message"):
            if log_entry[field].strip() == "":
                return f"Field {field} must contain a non-whitespace character"

    allowed_levels = ("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")
    if log_entry["level"] not in allowed_levels:
        return f"Field level {log_entry['level']!r} must be one of {allowed_levels}"

    return validate_timestamp(log_entry["timestamp"])


def validate_timestamp(value):
    """Return a timestamp validation error, or None if all checks pass."""
    # Restrict offset minutes because fromisoformat can normalize values above 59.
    pattern = r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-5][0-9])"
    if not re.fullmatch(pattern, value):
        return "Field timestamp must be in the form YYYY-MM-DDTHH:MM:SS[.fraction]Z or YYYY-MM-DDTHH:MM:SS[.fraction]+HH:MM / -HH:MM."

    try:
        datetime.fromisoformat(value)
    except ValueError:
        return "Field timestamp contains an invalid date or time."
    return None

if __name__ == "__main__":
    read_lines("examples/mixed.jsonl")

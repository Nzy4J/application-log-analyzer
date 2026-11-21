# Input format

The initial supported format is UTF-8 JSON Lines (.jsonl).
Each nonblank line must contain one JSON object.

## Required fields

- timestamp: a string in the form YYYY-MM-DDTHH:MM:SS[.fraction]Z
  or YYYY-MM-DDTHH:MM:SS[.fraction]+HH:MM / -HH:MM.
  The date, time, and timezone offset must be valid.
- level: one of DEBUG, INFO, WARN, ERROR, CRITICAL.
  Values are case-sensitive.
- service: a string containing at least one non-whitespace character.
- message: a string containing at least one non-whitespace character.

Additional fields are accepted but unused by the initial analysis.
Required string values are preserved without trimming.

## Invalid input

Blank lines are ignored.

Records with invalid JSON, a non-object JSON value, missing required
fields, or invalid field values are skipped. A diagnostic reports
the physical line number and reason. Processing continues.

If the file cannot be opened or decoded as UTF-8, processing fails
with a clear error.

## Scope

This is the project's initial supported schema, not a universal
application-log standard.

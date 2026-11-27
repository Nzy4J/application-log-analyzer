"""Filter validated application log records."""


def filter_records(records, level=None, service=None):
    """Return matching (line_number, record) tuples in their original order."""
    filtered = []
    for line_number, record in records:
        # Only None disables a filter; empty strings are still treated as filter values.
        if level is not None and record["level"] != level:
            continue
        if service is not None and record["service"] != service:
            continue
        filtered.append((line_number, record))
    return filtered
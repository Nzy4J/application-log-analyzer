"""Summarize validated application log records by level and service."""

def summarize_records(records):
    """Return (level_counts, service_counts) dictionaries for validated records."""
    levels_data = {}
    services_data = {}
    for _, record in records:
        level = record["level"]
        service = record["service"]
        levels_data[level] = levels_data.get(level, 0) + 1
        services_data[service] = services_data.get(service, 0) + 1
    return levels_data, services_data

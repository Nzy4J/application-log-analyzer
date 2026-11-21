# Application Log Analyzer

A Python CLI for filtering, summarizing, and investigating application logs.

## Status

Early development. Application functionality is not yet implemented.

## Goal

Make structured application logs easier to inspect by filtering records
and summarizing recurring errors.

## First milestone: v0.1.0

- Read a JSON Lines file containing application log records.
- Validate required fields and report malformed records with line numbers.
- Filter records by severity and service.
- Summarize matching records by severity, service, and exact message.
- Include synthetic sample logs and automated tests.
- Document setup, usage, and known limitations.

The initial input format will use timestamp, level, service, and message
fields. The exact validation rules will be documented during implementation.

## Planned extensions

- Additional input formats, beginning with CSV.
- Expanded edge-case tests and automated checks with GitHub Actions.
- PostgreSQL storage and reporting.
- Docker and Compose setup.
- Configurable data minimization and retention controls.

## Sample data

Initial examples and tests will use synthetic logs containing no real
personal or confidential information.

## License

MIT. See LICENSE.

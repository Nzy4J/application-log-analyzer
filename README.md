# Application Log Analyzer

A Python CLI for filtering, summarizing, and investigating application logs.

## Status

Early development. JSON Lines reading and record validation are implemented,
with an initial suite of 19 automated tests. Filtering, summaries, and the
command-line interface are not yet implemented.

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

Records use timestamp, level, service, and message fields.
See [the input format specification](docs/input-format.md) for validation rules.

## Development setup

Development currently uses Python 3.12.3 on WSL Ubuntu.
The current code and tests use only the Python standard library.

Run the commands below from the repository root.

## Running tests

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The tests cover record and timestamp validation, blank lines, line numbering,
continued processing after invalid records, and file-opening/decoding errors.

## Current limitations

The reader returns separate lists of validated records and errors, each
paired with physical source line numbers. Results are collected in memory.
Running `src/logtool/parser.py` directly reads the hardcoded
`examples/mixed.jsonl` file and prints valid records followed by errors.
Filtering, summaries, and CLI arguments are planned.

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

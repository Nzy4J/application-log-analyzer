"""Test JSON Lines reading and application record validation."""

import json
import tempfile
import unittest
from pathlib import Path

from logtool.parser import read_lines, validate_record, validate_timestamp


class TestValidateRecord(unittest.TestCase):
    def test_valid_record(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        self.assertIsNone(validate_record(record))

    def test_missing_required_fields(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        for field in ("timestamp", "level", "service", "message"):
            with self.subTest(field=field):
                invalid_record = record.copy()
                del invalid_record[field]
                self.assertEqual(
                    validate_record(invalid_record),
                    f"Missing field: {field}")

    def test_non_string_required_fields(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        for field in ("timestamp", "level", "service", "message"):
            with self.subTest(field=field):
                invalid_record = record.copy()
                invalid_record[field] = 123
                self.assertEqual(
                    validate_record(invalid_record),
                    f"Field {field} must be a string")

    def test_blank_service_or_message(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        for field in ("service", "message"):
            for value in ("", " ", "\t", "\n"):
                with self.subTest(field=field, value=value):
                    invalid_record = record.copy()
                    invalid_record[field] = value
                    self.assertEqual(
                        validate_record(invalid_record),
                        f"Field {field} must contain a non-whitespace character")

    def test_allowed_levels(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        for level in ("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"):
            with self.subTest(level=level):
                valid_record = record.copy()
                valid_record["level"] = level
                self.assertIsNone(validate_record(valid_record))

    def test_invalid_levels(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        allowed_levels = ("DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")
        for level in ("info", "WARNING", "", " INFO "):
            with self.subTest(level=level):
                invalid_record = record.copy()
                invalid_record["level"] = level
                self.assertEqual(
                    validate_record(invalid_record),
                    f"Field level {level!r} must be one of {allowed_levels}")

    def test_invalid_timestamp(self):
        record = {
            "timestamp": "2026-02-30T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        self.assertEqual(
            validate_record(record),
            "Field timestamp contains an invalid date or time.")


class TestValidateTimestamp(unittest.TestCase):
    def test_valid_timestamps(self):
        valid_timestamps = (
            "2026-11-23T10:30:00Z",
            "2026-11-23T10:30:00+05:30",
            "2026-11-23T10:30:00-05:00",
            "2026-11-23T10:30:00.123Z",
            "2026-11-23T10:30:00.123-05:00",
            "2024-02-29T10:30:00Z",
        )
        for timestamp in valid_timestamps:
            with self.subTest(timestamp=timestamp):
                self.assertIsNone(validate_timestamp(timestamp))

    def test_invalid_timestamp_formats(self):
        invalid_timestamps = (
            "2026-11-23T10:30:00",
            "2026-11-23 10:30:00Z",
            "2026-11-23T10:30Z",
            "2026-11-23T10:30:00+01:60",
            "",
        )
        expected_error = (
            "Field timestamp must be in the form "
            "YYYY-MM-DDTHH:MM:SS[.fraction]Z or "
            "YYYY-MM-DDTHH:MM:SS[.fraction]+HH:MM / -HH:MM.")
        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                self.assertEqual(validate_timestamp(timestamp), expected_error)

    def test_invalid_timestamp_dates_and_times(self):
        invalid_timestamps = (
            "2026-02-30T10:30:00Z",
            "2026-02-29T10:30:00Z",
            "2026-13-01T10:30:00Z",
            "2026-11-23T24:00:00Z",
            "2026-11-23T10:60:00Z",
            "2026-11-23T10:30:60Z",
        )
        for timestamp in invalid_timestamps:
            with self.subTest(timestamp=timestamp):
                self.assertEqual(
                    validate_timestamp(timestamp),
                    "Field timestamp contains an invalid date or time.")


class TestReadLines(unittest.TestCase):
    def test_empty_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "empty.jsonl"
            path.write_text("", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [])
            self.assertEqual(errors, [])

    def test_blank_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "blank.jsonl"
            path.write_text("\n   \n\t\n", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [])
            self.assertEqual(errors, [])

    def test_valid_record_after_blank_line(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid_after_blank.jsonl"
            path.write_text("\n" + json.dumps(record) + "\n", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [(2, record)])
            self.assertEqual(errors, [])

    def test_continues_after_invalid_json(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "continues_after_invalid.jsonl"
            path.write_text("{invalid json}\n" + json.dumps(record) + "\n", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [(2, record)])
            self.assertEqual(len(errors), 1)
            self.assertEqual(errors[0][0], 1)
            self.assertTrue(errors[0][1].startswith("Invalid JSON:"))

    def test_continues_after_non_object(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "continues_after_non_object.jsonl"
            path.write_text("[]\n" + json.dumps(record) + "\n", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [(2, record)])
            self.assertEqual(errors, [(1, "Record must be a JSON object: []")])

    def test_continues_after_validation_error(self):
        record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record"
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "continues_after_validation_error.jsonl"
            path.write_text("{}\n" + json.dumps(record) + "\n", encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [(2, record)])
            self.assertEqual(errors, [(1, "Missing field: timestamp")])

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.jsonl"
            with self.assertRaises(FileNotFoundError):
                read_lines(path)

    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid_utf8.jsonl"
            path.write_bytes(b"\xff")
            with self.assertRaises(UnicodeDecodeError):
                read_lines(path)

    def test_collects_records_and_errors_in_order(self):
        first_record = {
            "timestamp": "2026-11-23T10:30:00Z",
            "level": "INFO",
            "service": "checkout",
            "message": "Valid record 1"
        }
        second_record = {
            "timestamp": "2026-11-25T10:30:00Z",
            "level": "DEBUG",
            "service": "checkout",
            "message": "Valid record 4"
        }
        contents = (
            json.dumps(first_record) + "\n"
            "[]\n"
            "\n"
            + json.dumps(second_record) + "\n"
            "{}\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "collects_records_and_errors_in_order.jsonl"
            path.write_text(contents, encoding="utf-8")
            records, errors = read_lines(path)
            self.assertEqual(records, [(1, first_record), (4, second_record)])
            self.assertEqual(
                errors,
                [
                    (2, "Record must be a JSON object: []"),
                    (5, "Missing field: timestamp"),
                ],
            )
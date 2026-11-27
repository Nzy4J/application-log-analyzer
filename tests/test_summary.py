"""Test counts of validated application log records by level and service."""

import unittest
import copy
from logtool.summary import summarize_records
from logtool.filters import filter_records


class TestSummarizeRecords(unittest.TestCase):
    def test_empty_records(self):
        records = []
        expected_levels = {}
        expected_services = {}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_single_record(self):
        records = [(1, {"timestamp":"2026-11-20T14:00:10Z","level":"ERROR","service":"checkout","message":"Order processing failed"})]
        expected_levels = {"ERROR": 1}
        expected_services = {"checkout": 1}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_mixed_records(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"})
        ]
        expected_levels = {"INFO": 2, "ERROR": 2}
        expected_services = {"checkout": 2, "payments": 2}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_repeated_category(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "WARN", "service": "auth", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "WARN", "service": "auth", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "WARN", "service": "auth", "message": "Test message"})
        ]
        expected_levels = {"WARN": 3}
        expected_services = {"auth": 3}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_all_levels(self):
        records = [
            (1, {"timestamp": "2024-06-01T12:00:00Z", "level": "DEBUG", "service": "api", "message": "Test message"}),
            (2, {"timestamp": "2024-06-01T12:01:00Z", "level": "INFO", "service": "api", "message": "Test message"}),
            (3, {"timestamp": "2024-06-01T12:02:00Z", "level": "WARN", "service": "api", "message": "Test message"}),
            (4, {"timestamp": "2024-06-01T12:03:00Z", "level": "ERROR", "service": "api", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:04:00Z", "level": "CRITICAL", "service": "api", "message": "Test message"})
        ]
        expected_levels = {"DEBUG": 1, "INFO": 1, "WARN": 1, "ERROR": 1, "CRITICAL": 1}
        expected_services = {"api": 5}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_uneven_counts(self):
        records = [
            (2, {"timestamp": "2026-11-20T14:00:00Z", "level": "INFO", "service": "checkout", "message": "Request received"}),
            (5, {"timestamp": "2026-11-20T14:01:00Z", "level": "INFO", "service": "checkout", "message": "Order validated"}),
            (8, {"timestamp": "2026-11-20T14:02:00Z", "level": "INFO", "service": "checkout", "message": "Payment requested"}),
            (11, {"timestamp": "2026-11-20T14:03:00Z", "level": "ERROR", "service": "checkout", "message": "Order processing failed"}),
            (14, {"timestamp": "2026-11-20T14:04:00Z", "level": "ERROR", "service": "payments", "message": "Payment declined"}),
        ]
        expected_levels = {"INFO": 3, "ERROR": 2}
        expected_services = {"checkout": 4, "payments": 1}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_case_sensitive_services(self):
        records = [
            (2, {"timestamp": "2026-11-20T14:00:00Z", "level": "INFO", "service": "api", "message": "Request received"}),
            (5, {"timestamp": "2026-11-20T14:01:00Z", "level": "INFO", "service": "API", "message": "Request processed"}),
            (8, {"timestamp": "2026-11-20T14:02:00Z", "level": "INFO", "service": "API", "message": "Response sent"}),
        ]
        expected_levels = {"INFO": 3}
        expected_services = {"api": 1, "API": 2}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_duplicate_records_counted(self):
        record = {
            "timestamp": "2026-11-20T14:00:00Z",
            "level": "WARN",
            "service": "auth",
            "message": "Login attempt rejected",
        }
        records = [
            (2, record),
            (5, record),
        ]
        expected_levels = {"WARN": 2}
        expected_services = {"auth": 2}
        levels, services = summarize_records(records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

    def test_preserves_input(self):
        records = [
            (2, {"timestamp": "2026-11-20T14:00:00Z", "level": "INFO", "service": "checkout", "message": "Request received"}),
            (5, {"timestamp": "2026-11-20T14:01:00Z", "level": "ERROR", "service": "checkout", "message": "Order processing failed"}),
            (8, {"timestamp": "2026-11-20T14:02:00Z", "level": "INFO", "service": "payments", "message": "Payment requested"}),
            (11, {"timestamp": "2026-11-20T14:03:00Z", "level": "ERROR", "service": "payments", "message": "Payment declined"}),
        ]
        record_copy = copy.deepcopy(records)
        summarize_records(record_copy)
        self.assertEqual(records, record_copy)

    def test_summarizes_filtered_records(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered_records = filter_records(records, level="ERROR")
        expected_levels = {"ERROR": 2}
        expected_services = {"checkout": 1, "payments": 1}
        levels, services = summarize_records(filtered_records)
        self.assertEqual(levels, expected_levels)
        self.assertEqual(services, expected_services)

"""Test filtering of validated log records by level and service."""

import unittest
import copy
from logtool.filters import filter_records

class TestFilterRecords(unittest.TestCase):
    def test_filter_by_level(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="ERROR")
        self.assertEqual(filtered, [
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ])

    def test_filter_by_service(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, service="payments")
        self.assertEqual(filtered, [
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ])

    def test_filter_by_level_and_service(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="ERROR", service="payments")
        self.assertEqual(filtered, [
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ])

    def test_no_filters(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records)
        self.assertEqual(filtered, records)

    def test_no_matching_level(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="DEBUG")
        self.assertEqual(filtered, [])

    def test_no_matching_service(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, service="auth")
        self.assertEqual(filtered, [])

    def test_no_matching_combination(self):
        records = [
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="ERROR", service="payments")
        self.assertEqual(filtered, [])

    def test_empty_records(self):
        records = []
        filtered = filter_records(records, level="ERROR", service="payments")
        self.assertEqual(filtered, [])

    def test_empty_level_filter(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="")
        self.assertEqual(filtered, [])

    def test_empty_service_filter(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, service="")
        self.assertEqual(filtered, [])

    def test_case_sensitive_filters(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "ERROR", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="error")
        self.assertEqual(filtered, [])
        filtered = filter_records(records, service="Payments")
        self.assertEqual(filtered, [])

    def test_exact_level_matching(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "CRITICAL", "service": "payments", "message": "Test message"}),
        ]
        filtered = filter_records(records, level="ERROR")
        self.assertEqual(filtered, [
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
        ])

    def test_preserves_input(self):
        records = [
            (2, {"timestamp": "2024-06-01T12:00:00Z", "level": "INFO", "service": "checkout", "message": "Test message"}),
            (5, {"timestamp": "2024-06-01T12:05:00Z", "level": "ERROR", "service": "checkout", "message": "Test message"}),
            (8, {"timestamp": "2024-06-01T12:08:00Z", "level": "INFO", "service": "payments", "message": "Test message"}),
            (11, {"timestamp": "2024-06-01T12:11:00Z", "level": "CRITICAL", "service": "payments", "message": "Test message"}),
        ]
        snapshot = copy.deepcopy(records)
        filtered = filter_records(records, level="ERROR")
        self.assertEqual(records, snapshot)
        self.assertIsNot(filtered, records)

#!/usr/bin/env python3
"""Test utils"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json, memoize

# Utility functions for testing
class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    # Test access_nested_map with various nested maps and paths
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    # Test access_nested_map with paths that do not exist in the nested map
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

# Utility functions for testing get_json
class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    # Test get_json with different URLs and expected JSON responses
    def test_get_json(self, url, expected, mock_get):
        mock_get.return_value = Mock(**{"json.return_value": expected})
        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url)

# Utility functions for testing memoization
class TestMemoize(unittest.TestCase):
    """Tests for memoize"""
#    @parameterized.expand([
#      (lambda x: x, 42),  
#      (lambda x: x * 2, 84),
#    ])
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42
#            # Use memoization on a method to cache its result
            @memoize
            def a_property(self):
                return self.a_method()

        test = TestClass()
        with patch.object(test, 'a_method') as mocked:
            mocked.return_value = 42
            self.assertEqual(test.a_property, 42)
            self.assertEqual(test.a_property, 42)
            mocked.assert_called_once()

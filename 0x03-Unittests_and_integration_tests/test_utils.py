#!/usr/bin/env python3
"""Test utils"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct value for given path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test access_nested_map raises KeyError for invalid path"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, url, expected, mock_get):
        """Test get_json returns expected payload from URL"""
        mock_get.return_value = Mock(**{"json.return_value": expected})
        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url)


class TestMemoize(unittest.TestCase):
    """Tests for memoize"""

    def test_memoize(self):
        """Test memoize caches method results"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test = TestClass()
        with patch.object(test, 'a_method') as mocked:
            mocked.return_value = 42
            self.assertEqual(test.a_property, 42)
            self.assertEqual(test.a_property, 42)
            mocked.assert_called_once()

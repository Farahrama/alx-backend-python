#!/usr/bin/env python3
"""Test client"""

#!/usr/bin/env python3
"""Integration test with patch"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method with different organization names"""
        test_result = {"login": org_name}
        mock_get_json.return_value = test_result
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), test_result)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns expected URL"""
        mock_org.return_value = {"repos_url": "http://test-url.com"}
        client = GithubOrgClient("test")
        self.assertEqual(client._public_repos_url, "http://test-url.com")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos method with mocked URL and JSON response"""
        mock_url.return_value = "http://test-url.com"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])
        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with("http://test-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different repo data and license keys"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

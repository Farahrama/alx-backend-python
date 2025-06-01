#!/usr/bin/env python3
"""Client module"""

from typing import List, Dict
from utils import get_json, memoize

"""GitHub organization client module."""
class GithubOrgClient:
    """GitHub organization client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self._org_name = org_name
    """Initialize with organization name."""
    @memoize
    def org(self) -> Dict:
        """Return the organization data."""
        url = self.ORG_URL.format(org=self._org_name)
        return get_json(url)
    """Return the organization data from GitHub API."""
    @property
    def _public_repos_url(self) -> str:
        """Return the URL to fetch public repos."""
        return self.org.get("repos_url")
    """puplic repos"""
    def public_repos(self, license: str = None) -> List[str]:
        """Return the list of public repo names."""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"] for repo in repos
            if self.has_license(repo, license)
        ]
    """has_license"""
    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key

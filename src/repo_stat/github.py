import os
from typing import Any

import httpx


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str | None = None):
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=30.0,
            headers=self._build_headers(token),
        )

    def _build_headers(self, token: str | None) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json"}
        auth_token = token or os.getenv("GITHUB_TOKEN")
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        return headers

    def get_user(self, username: str) -> dict[str, Any]:
        response = self.client.get(f"/users/{username}")
        response.raise_for_status()
        return response.json()

    def get_repos(
        self,
        username: str,
        per_page: int = 100,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        response = self.client.get(
            f"/users/{username}/repos",
            params={
                "per_page": per_page,
                "page": page,
                "sort": "stars",
                "direction": "desc",
            },
        )
        response.raise_for_status()
        return response.json()

    def get_all_repos(self, username: str) -> list[dict[str, Any]]:
        repos = []
        page = 1
        while True:
            page_repos = self.get_repos(username, per_page=100, page=page)
            if not page_repos:
                break
            repos.extend(page_repos)
            if len(page_repos) < 100:
                break
            page += 1
        return repos

    def close(self) -> None:
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args) -> None:
        self.close()

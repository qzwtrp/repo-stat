import os
from datetime import datetime
from typing import Any

import httpx

from repo_stat.models import UserStats, Repository


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


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_stats(
    username: str,
    raw_user: dict[str, Any],
    raw_repos: list[dict[str, Any]],
) -> UserStats:
    repos = [
        Repository(
            name=r["name"],
            description=r.get("description"),
            language=r.get("language"),
            stars=r.get("stargazers_count", 0),
            forks=r.get("forks_count", 0),
            open_issues=r.get("open_issues_count", 0),
            created_at=_parse_dt(r["created_at"]),
            updated_at=_parse_dt(r["updated_at"]),
            is_fork=r.get("fork", False),
            is_private=r.get("private", False),
            html_url=r["html_url"],
        )
        for r in raw_repos
    ]

    repos.sort(key=lambda r: (-r.stars, r.name))

    language_counts: dict[str, int] = {}
    for r in repos:
        if r.language:
            language_counts[r.language] = language_counts.get(r.language, 0) + 1

    language_counts = dict(sorted(language_counts.items(), key=lambda x: -x[1]))

    return UserStats(
        username=raw_user["login"],
        public_repos=raw_user.get("public_repos", 0),
        followers=raw_user.get("followers", 0),
        following=raw_user.get("following", 0),
        top_repositories=repos,
        language_counts=language_counts,
        total_stars=sum(r.stars for r in repos),
        total_forks=sum(r.forks for r in repos),
    )

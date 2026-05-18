from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Repository:
    name: str
    description: Optional[str]
    language: Optional[str]
    stars: int
    forks: int
    open_issues: int
    created_at: datetime
    updated_at: datetime
    is_fork: bool
    is_private: bool
    html_url: str


@dataclass(frozen=True)
class UserStats:
    username: str
    public_repos: int
    followers: int
    following: int
    top_repositories: list[Repository]
    language_counts: dict[str, int]
    total_stars: int
    total_forks: int

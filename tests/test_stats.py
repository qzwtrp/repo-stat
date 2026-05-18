from datetime import datetime, timezone
from repo_stat.github import build_stats
from repo_stat.models import Repository, UserStats


def test_build_stats_basic():
    raw_user = {
        "login": "testuser",
        "public_repos": 2,
        "followers": 100,
        "following": 5,
    }
    raw_repos = [
        {
            "name": "cool-project",
            "description": "A cool project",
            "language": "Python",
            "stargazers_count": 50,
            "forks_count": 10,
            "open_issues_count": 3,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-06-01T00:00:00Z",
            "fork": False,
            "private": False,
            "html_url": "https://github.com/testuser/cool-project",
        },
        {
            "name": "js-utils",
            "description": None,
            "language": "JavaScript",
            "stargazers_count": 20,
            "forks_count": 2,
            "open_issues_count": 0,
            "created_at": "2023-02-01T00:00:00Z",
            "updated_at": "2023-07-01T00:00:00Z",
            "fork": False,
            "private": False,
            "html_url": "https://github.com/testuser/js-utils",
        },
    ]

    stats = build_stats("testuser", raw_user, raw_repos)

    assert stats.username == "testuser"
    assert stats.public_repos == 2
    assert stats.followers == 100
    assert stats.following == 5
    assert len(stats.top_repositories) == 2
    assert stats.top_repositories[0].name == "cool-project"
    assert stats.top_repositories[0].name == "cool-project"
    assert stats.top_repositories[0].stars == 50
    assert stats.top_repositories[1].stars == 20
    assert stats.language_counts == {"Python": 1, "JavaScript": 1}
    assert stats.total_stars == 70
    assert stats.total_forks == 12


def test_build_stats_sorts_by_stars_then_name():
    raw_user = {"login": "t"}
    raw_repos = [
        {
            "name": "b", "stargazers_count": 10, "forks_count": 0,
            "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z",
            "html_url": "https://github.com/t/b",
        },
        {
            "name": "a", "stargazers_count": 10, "forks_count": 0,
            "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z",
            "html_url": "https://github.com/t/a",
        },
        {
            "name": "z", "stargazers_count": 100, "forks_count": 0,
            "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z",
            "html_url": "https://github.com/t/z",
        },
    ]

    stats = build_stats("t", raw_user, raw_repos)
    names = [r.name for r in stats.top_repositories]
    assert names == ["z", "a", "b"]


def test_build_stats_language_counts_sorted():
    raw_user = {"login": "t"}
    raw_repos = [
        {"name": "r1", "language": "Python", "stargazers_count": 0, "forks_count": 0,
         "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z", "html_url": "", },
        {"name": "r2", "language": "Python", "stargazers_count": 0, "forks_count": 0,
         "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z", "html_url": "", },
        {"name": "r3", "language": "Rust", "stargazers_count": 0, "forks_count": 0,
         "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z", "html_url": "", },
    ]

    stats = build_stats("t", raw_user, raw_repos)
    assert list(stats.language_counts.keys()) == ["Python", "Rust"]
    assert stats.language_counts == {"Python": 2, "Rust": 1}


def test_build_stats_skips_none_language():
    raw_user = {"login": "t"}
    raw_repos = [
        {"name": "r1", "language": None, "stargazers_count": 0, "forks_count": 0,
         "created_at": "2023-01-01T00:00:00Z", "updated_at": "2023-01-01T00:00:00Z", "html_url": "", },
    ]

    stats = build_stats("t", raw_user, raw_repos)
    assert stats.language_counts == {}

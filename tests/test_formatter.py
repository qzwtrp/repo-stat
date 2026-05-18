from datetime import datetime, timezone
from repo_stat.models import Repository, UserStats


def test_format_stats_outputs_text():
    stats = UserStats(
        username="testuser",
        public_repos=2,
        followers=100,
        following=5,
        top_repositories=[
            Repository(
                name="repo1",
                description=None,
                language="Python",
                stars=50,
                forks=10,
                open_issues=0,
                created_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
                updated_at=datetime(2023, 1, 1, tzinfo=timezone.utc),
                is_fork=False,
                is_private=False,
                html_url="https://github.com/testuser/repo1",
            ),
        ],
        language_counts={"Python": 1},
        total_stars=50,
        total_forks=10,
    )

    from repo_stat.formatter import format_stats
    result = format_stats(stats)
    assert isinstance(result, str)
    assert "testuser" in result
    assert "repo1" in result
    assert "Python" in result
    assert "50" in result


def test_format_stats_with_empty_repos():
    stats = UserStats(
        username="emptyuser",
        public_repos=0,
        followers=0,
        following=0,
        top_repositories=[],
        language_counts={},
        total_stars=0,
        total_forks=0,
    )

    from repo_stat.formatter import format_stats
    result = format_stats(stats)
    assert isinstance(result, str)
    assert "emptyuser" in result
    assert "Summary" in result

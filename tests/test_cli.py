import respx
from click.testing import CliRunner
from httpx import Response
from repo_stat.cli import main


def test_cli_no_args_shows_usage():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 2  # Click returns 2 for missing required arg
    assert "Usage" in result.output


@respx.mock
def test_cli_with_username():
    """Full integration test with mocked GitHub API."""
    respx.get("https://api.github.com/users/testuser").mock(
        return_value=Response(200, json={
            "login": "testuser",
            "public_repos": 1,
            "followers": 10,
            "following": 5,
        })
    )
    respx.get("https://api.github.com/users/testuser/repos").mock(
        return_value=Response(200, json=[{
            "name": "myrepo",
            "language": "Python",
            "stargazers_count": 42,
            "forks_count": 7,
            "open_issues_count": 1,
            "created_at": "2023-01-01T00:00:00Z",
            "updated_at": "2023-06-01T00:00:00Z",
            "fork": False,
            "private": False,
            "html_url": "https://github.com/testuser/myrepo",
        }])
    )

    runner = CliRunner()
    result = runner.invoke(main, ["testuser"])

    assert result.exit_code == 0
    assert "testuser" in result.output
    assert "myrepo" in result.output
    assert "Python" in result.output
    assert "42" in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "repo-stat" in result.output
    assert "0.1.0" in result.output

import respx
from httpx import Response

from repo_stat.github import GitHubClient


@respx.mock
def test_get_user_success():
    route = respx.get("https://api.github.com/users/octocat").mock(
        return_value=Response(
            200,
            json={
                "login": "octocat",
                "public_repos": 10,
                "followers": 500,
                "following": 20,
            },
        )
    )

    client = GitHubClient()
    result = client.get_user("octocat")

    assert result["login"] == "octocat"
    assert route.called


@respx.mock
def test_get_repos_success():
    route = respx.get("https://api.github.com/users/octocat/repos").mock(
        return_value=Response(
            200,
            json=[
                {"name": "repo1", "stargazers_count": 50},
                {"name": "repo2", "stargazers_count": 10},
            ],
        )
    )

    client = GitHubClient()
    result = client.get_repos("octocat")

    assert len(result) == 2
    assert result[0]["name"] == "repo1"
    assert route.called


@respx.mock
def test_default_sort_params():
    route = respx.get("https://api.github.com/users/octocat/repos").mock(
        return_value=Response(200, json=[])
    )

    client = GitHubClient()
    client.get_repos("octocat")

    assert route.called
    request = route.calls[0].request
    assert request.url.params["sort"] == "stars"
    assert request.url.params["direction"] == "desc"


@respx.mock
def test_get_all_repos_paginates():
    page1 = respx.get("https://api.github.com/users/octocat/repos", params={"per_page": "100", "page": "1", "sort": "stars", "direction": "desc"}).mock(
        return_value=Response(200, json=[{"name": f"repo{i}"} for i in range(100)])
    )
    page2 = respx.get("https://api.github.com/users/octocat/repos", params={"per_page": "100", "page": "2", "sort": "stars", "direction": "desc"}).mock(
        return_value=Response(200, json=[{"name": "repo100"}])
    )

    client = GitHubClient()
    result = client.get_all_repos("octocat")

    assert len(result) == 101
    assert page1.called
    assert page2.called


@respx.mock
def test_token_from_parameter():
    route = respx.get("https://api.github.com/users/test").mock(
        return_value=Response(200, json={"login": "test"})
    )

    client = GitHubClient(token="my-secret-token")
    client.get_user("test")

    assert route.called
    assert route.calls[0].request.headers["Authorization"] == "Bearer my-secret-token"

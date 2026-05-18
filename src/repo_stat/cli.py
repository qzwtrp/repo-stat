import click
from repo_stat.github import GitHubClient, build_stats
from repo_stat.formatter import format_stats


@click.command()
@click.argument("username")
@click.option(
    "--token",
    envvar="GITHUB_TOKEN",
    help="GitHub personal access token",
)
@click.option(
    "--top",
    default=10,
    show_default=True,
    help="Number of top repos to show",
)
@click.version_option(
    version="0.1.0",
    prog_name="repo-stat",
)
def main(username: str, token: str | None, top: int) -> None:
    """Analyze GitHub repository statistics for a user."""
    try:
        with GitHubClient(token=token) as client:
            raw_user = client.get_user(username)
            raw_repos = client.get_all_repos(username)
            stats = build_stats(username, raw_user, raw_repos, top_limit=top)

        output = format_stats(stats)
        click.echo(output)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == "__main__":
    main()

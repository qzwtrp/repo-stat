from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from repo_stat.models import UserStats


def format_stats(stats: UserStats) -> str:
    """Format UserStats into a rich string representation."""
    console = Console(width=120, force_terminal=False)

    with console.capture() as capture:
        header = Panel.fit(
            f"GitHub Stats for @{stats.username}",
            border_style="cyan",
        )
        console.print(header)
        console.print()

        summary = Table(title="Summary", show_header=False, box=None)
        summary.add_column("Key", style="bold magenta")
        summary.add_column("Value", style="green")
        summary.add_row("Public Repos", str(stats.public_repos))
        summary.add_row("Followers", str(stats.followers))
        summary.add_row("Following", str(stats.following))
        summary.add_row("Total Stars", str(stats.total_stars))
        summary.add_row("Total Forks", str(stats.total_forks))
        console.print(summary)
        console.print()

        if stats.language_counts:
            lang_table = Table(title="Languages")
            lang_table.add_column("Language", style="bold")
            lang_table.add_column("Repos", justify="right")
            for lang, count in stats.language_counts.items():
                lang_table.add_row(lang, str(count))
            console.print(lang_table)
            console.print()

        if stats.top_repositories:
            repo_table = Table(title="Top Repositories")
            repo_table.add_column("Name", style="bold cyan")
            repo_table.add_column("Language")
            repo_table.add_column("Stars", justify="right")
            repo_table.add_column("Forks", justify="right")
            repo_table.add_column("Description", max_width=50)

            for repo in stats.top_repositories:
                desc = (repo.description or "")[:48]
                repo_table.add_row(
                    repo.name,
                    repo.language or "—",
                    str(repo.stars),
                    str(repo.forks),
                    desc,
                )
            console.print(repo_table)

    return capture.get()

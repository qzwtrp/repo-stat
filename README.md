# repo-stat

Beautiful CLI analyzer for GitHub repository statistics.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Analyze a GitHub user
repo-stat octocat

# Use a GitHub token for higher rate limits
repo-stat octocat --token YOUR_GITHUB_TOKEN
# or
GITHUB_TOKEN=yourtoken repo-stat octocat

# Show top 5 repos instead of 10
repo-stat octocat --top 5
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT

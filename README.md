# repo-stat

Beautiful CLI analyzer for GitHub repository statistics.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Analyze a GitHub user
repo-stat qzwtrp

# Use a GitHub token for higher rate limits
repo-stat qzwtrp --token YOUR_GITHUB_TOKEN
# or
GITHUB_TOKEN=yourtoken repo-stat qzwtrp

# Show top 5 repos instead of 10
repo-stat qzwtrp --top 5
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

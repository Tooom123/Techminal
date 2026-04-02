# Techminal

Latest tech news at the top of every terminal session — clean, readable, no links.

## Example output

```
🧠 Techminal

🚀 OpenAI Releases New Model With Improved Reasoning

The latest model shows significant improvements in multi-step reasoning tasks,
outperforming previous versions on standard benchmarks. It is available via API
starting today with reduced pricing for high-volume users.

Source: TechCrunch
```

## Installation

```bash
git clone <repo> ~/techminal
cd ~/techminal
pip install -r requirements.txt
```

Or without git:

```bash
mkdir ~/techminal
# copy techminal.py and requirements.txt into it
pip install feedparser
```

## Run manually

```bash
python3 ~/techminal/techminal.py
```

## Hook into shell startup

Add one line to your shell config so it runs every time you open a terminal.

**~/.bashrc** or **~/.zshrc**:

```bash
python3 ~/techminal/techminal.py
```

Then reload:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

## How caching works

- On first run (or after 1 hour), Techminal fetches fresh articles from all RSS feeds and writes them to `/tmp/techminal_cache.json`.
- On subsequent runs within the same hour, it reads from the cache — making startup nearly instant.
- Already-shown article IDs are stored in the cache so the same article is not repeated until all articles have been cycled through.
- The cache file lives in `/tmp/` and is cleared on reboot.

## Customize sources

Edit the `FEEDS` list near the top of `techminal.py`:

```python
FEEDS = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge",  "https://www.theverge.com/rss/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
    # add any RSS feed here:
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
]
```

Any RSS feed that `feedparser` can parse will work.

## Requirements

- Python 3.7+
- `feedparser` (only third-party dependency)
- Internet access for the initial fetch (graceful fallback when offline)

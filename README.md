# Techminal

Latest tech news at the top of every terminal session. Clean, readable, easy setup.

## Example output

```
▀█▀ █▀▀ █▀▀ █░█ █▀▄▀█ █ █▄░█ ▄▀█ █░░
░█░ ██▄ █▄▄ █▀█ █░▀░█ █ █░▀█ █▀█ █▄▄

    Apple releases security fix for older iPhones and iPads

    The security update protects a raft of older iPhones and iPads from
    attacks linked to leaked hacking tools called DarkSword.

    Source : TechCrunch, link
```

The source link is clickable in terminals that support OSC 8 hyperlinks (VSCode, GNOME Terminal, iTerm2, Windows Terminal).

## Installation

```bash
git clone <repo> ~/techminal
cd ~/techminal
pip install -r requirements.txt
```

Or without git:

```bash
mkdir ~/techminal
# copy techminal.py, techminal.txt and requirements.txt into it
pip install feedparser
```

## Run manually

```bash
python3 ~/techminal/techminal.py
```

## Hook into shell startup

Add one line to your shell config so it runs every time you open a terminal.

~/.bashrc or ~/.zshrc:

```bash
python3 ~/techminal/techminal.py
```

Then reload:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

## How caching works

On first run, or after one hour, Techminal fetches fresh articles from all RSS feeds and writes them to `/tmp/techminal_cache.json`. On subsequent runs within the same hour it reads from the cache, making startup nearly instant.

Already-shown article IDs are stored in the cache so the same article is not repeated until all articles have been cycled through. The cache file lives in `/tmp/` and is cleared on reboot.

Only articles that include a summary are stored and displayed. Articles with no summary are skipped at fetch time.

## Customize sources

Edit the `FEEDS` list near the top of `techminal.py`:

```python
FEEDS = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge",  "https://www.theverge.com/rss/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
]
```

Any RSS feed that `feedparser` can parse will work.

## Customize / Delete the logo

The ASCII art logo is loaded from `techminal.txt`. Edit that file to replace it with any ASCII art. The color gradient is applied automatically by the script based on character position.

## Requirements

- Python 3.7+
- `feedparser` (only third-party dependency)
- Internet access for the initial fetch, with a graceful fallback message when offline

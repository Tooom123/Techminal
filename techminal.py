#!/usr/bin/env python3

import json
import os
import random
import shutil
import sys
import textwrap
import time
import re

try:
    import feedparser
except ImportError:
    print("Missing dependency: run 'pip install feedparser'")
    sys.exit(1)

CACHE_FILE = "/tmp/techminal_cache.json"
CACHE_TTL = 3600

FEEDS = [
    ("TechCrunch", "https://techcrunch.com/feed/"),
    ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
]

ASCII_ART_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "techminal.txt")

ANSI = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
    "cyan":   "\033[36m",
    "yellow": "\033[33m",
    "green":  "\033[32m",
    "blue":   "\033[34m",
    "gray":   "\033[90m",
}


def strip_html(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    text = re.sub(r"&quot;", '"', text)
    text = re.sub(r"&#39;", "'", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&#8230;", "...", text)
    text = re.sub(r"&#\d+;", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE) as f:
            data = json.load(f)
        if time.time() - data.get("fetched_at", 0) < CACHE_TTL:
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return None


def save_cache(articles, shown_ids):
    data = {
        "fetched_at": time.time(),
        "articles": articles,
        "shown_ids": shown_ids,
    }
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)
    except OSError:
        pass


def fetch_feeds():
    articles = []
    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = strip_html(entry.get("title", "")).strip()
                summary = ""
                for field in ("summary", "description", "content"):
                    raw = entry.get(field, "")
                    if isinstance(raw, list):
                        raw = raw[0].get("value", "") if raw else ""
                    summary = strip_html(raw).strip()
                    if len(summary) > 40:
                        break
                if not title:
                    continue
                articles.append({
                    "id": entry.get("id") or entry.get("link") or title,
                    "title": title,
                    "summary": summary,
                    "source": source,
                    "link": entry.get("link", ""),
                })
        except Exception:
            continue
    return articles


def pick_article(articles, shown_ids):
    unseen = [a for a in articles if a["id"] not in shown_ids]
    if not unseen:
        shown_ids.clear()
        unseen = articles
    if not unseen:
        return None, shown_ids
    article = random.choice(unseen)
    shown_ids.append(article["id"])
    if len(shown_ids) > 60:
        shown_ids = shown_ids[-60:]
    return article, shown_ids


def load_ascii_art():
    try:
        with open(ASCII_ART_FILE) as f:
            return f.read().rstrip("\n")
    except OSError:
        return "TECHMINAL"


def hyperlink(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def format_output(article):
    width = min(shutil.get_terminal_size((80, 24)).columns, 80)

    ascii_art = load_ascii_art()
    header_block = ANSI["yellow"] + ascii_art + ANSI["reset"]

    title_lines = textwrap.wrap(article["title"], width - 2)
    title_block = "\n".join(
        ANSI["bold"] + ANSI["cyan"] + line + ANSI["reset"] for line in title_lines
    )

    summary = article["summary"]
    if summary:
        sentences = re.split(r"(?<=[.!?])\s+", summary)
        trimmed = ""
        for s in sentences:
            if len(trimmed) + len(s) > 320:
                break
            trimmed += (" " if trimmed else "") + s
        summary = trimmed or summary[:320]
        summary_lines = textwrap.wrap(summary, width - 2)[:4]
        summary_block = "\n".join(ANSI["reset"] + line for line in summary_lines)
    else:
        summary_block = ANSI["dim"] + "(no summary available)" + ANSI["reset"]

    link = article.get("link", "")
    if link:
        source_line = (
            ANSI["gray"] + "Source : " + article["source"] + ", "
            + hyperlink(link, "lien")
            + ANSI["reset"]
        )
    else:
        source_line = ANSI["gray"] + "Source : " + article["source"] + ANSI["reset"]

    return (
        "\n"
        + header_block + "\n"
        + "\n"
        + title_block + "\n"
        + "\n"
        + summary_block + "\n"
        + "\n"
        + source_line
        + "\n"
    )


def main():
    cache = load_cache()

    if cache:
        articles = cache["articles"]
        shown_ids = cache["shown_ids"]
    else:
        articles = fetch_feeds()
        shown_ids = []

    if not articles:
        print(ANSI["dim"] + "Techminal: could not fetch news (offline?)" + ANSI["reset"])
        return

    article, shown_ids = pick_article(articles, shown_ids)

    if not article:
        print(ANSI["dim"] + "Techminal: no articles available" + ANSI["reset"])
        return

    save_cache(articles, shown_ids)
    print(format_output(article))


if __name__ == "__main__":
    main()

import re
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}


def search_news(query: str, max_results: int = 10) -> list:
    items = _fetch_google_rss(query, max_results)
    if not items:
        items = _fetch_naver_rss(query, max_results)
    return items


# ── Google News RSS (기본) ──

def _fetch_google_rss(query: str, max_results: int) -> list:
    url = (
        f"https://news.google.com/rss/search"
        f"?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    )
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        items = []
        for item in root.findall(".//item")[:max_results]:
            headline = _text(item, "title")
            link     = _text(item, "link")
            pub_date = _text(item, "pubDate")
            press_tag = item.find("source")
            press = press_tag.text.strip() if press_tag is not None else ""

            if headline and link:
                items.append({
                    "headline": headline,
                    "link": link,
                    "press": press,
                    "date": _parse_rss_date(pub_date),
                    "summary": "",
                })
        return items
    except Exception:
        return []


# ── Naver News RSS (fallback) ──

def _fetch_naver_rss(query: str, max_results: int) -> list:
    url = (
        f"https://search.naver.com/search.naver"
        f"?where=news&query={quote(query)}&output=rss"
    )
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)

        items = []
        for item in root.findall(".//item")[:max_results]:
            headline = re.sub(r"<[^>]+>", "", _text(item, "title"))
            link     = _text(item, "link") or _text(item, "originallink")
            pub_date = _text(item, "pubDate")
            description = re.sub(r"<[^>]+>", "", _text(item, "description"))

            if headline and link:
                items.append({
                    "headline": headline,
                    "link": link,
                    "press": "",
                    "date": _parse_rss_date(pub_date),
                    "summary": description[:200] + "..." if len(description) > 200 else description,
                })
        return items
    except Exception:
        return []


# ── helpers ──

def _text(element, tag: str) -> str:
    node = element.find(tag)
    return node.text.strip() if node is not None and node.text else ""


def _parse_rss_date(raw: str) -> str:
    # "Mon, 06 Jan 2025 12:00:00 GMT" → "2025-01-06"
    m = re.search(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", raw)
    if m:
        months = {
            "Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
            "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12",
        }
        d, mo, y = m.group(1), m.group(2), m.group(3)
        return f"{y}-{months.get(mo, '00')}-{d.zfill(2)}"
    return raw or "날짜 미상"

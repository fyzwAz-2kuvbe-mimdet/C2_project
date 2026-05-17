import re
import xml.etree.ElementTree as ET
from urllib.parse import quote

import requests

from config.learning_types import get_type
from core.llm_client import ask
from prompts.mentoring_prompts import (
    GRADE_TONE_GUIDE, STEP06_EXTRA_RESOURCES, STEP06_NEWS_BATCH_SUMMARY,
    STEP06_NEWS_SUMMARY, SYSTEM_BASE, TYPE_QUESTION_STYLE,
)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9",
}


# ── 뉴스 크롤링 (Google News RSS → Naver RSS fallback) ──

def search_news(query: str, max_results: int = 10) -> list:
    items = _fetch_google_rss(query, max_results)
    if not items:
        items = _fetch_naver_rss(query, max_results)
    return items


def _fetch_google_rss(query: str, max_results: int) -> list:
    url = f"https://news.google.com/rss/search?q={quote(query)}&hl=ko&gl=KR&ceid=KR:ko"
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall(".//item")[:max_results]:
            headline = _text(item, "title")
            link = _text(item, "link")
            pub_date = _text(item, "pubDate")
            press_tag = item.find("source")
            press = press_tag.text.strip() if press_tag is not None else ""
            if headline and link:
                items.append({
                    "headline": headline, "link": link,
                    "press": press, "date": _parse_date(pub_date), "summary": "",
                })
        return items
    except Exception:
        return []


def _fetch_naver_rss(query: str, max_results: int) -> list:
    url = f"https://search.naver.com/search.naver?where=news&query={quote(query)}&output=rss"
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        items = []
        for item in root.findall(".//item")[:max_results]:
            headline = re.sub(r"<[^>]+>", "", _text(item, "title"))
            link = _text(item, "link") or _text(item, "originallink")
            pub_date = _text(item, "pubDate")
            description = re.sub(r"<[^>]+>", "", _text(item, "description"))
            if headline and link:
                items.append({
                    "headline": headline, "link": link, "press": "",
                    "date": _parse_date(pub_date),
                    "summary": description[:200] + "..." if len(description) > 200 else description,
                })
        return items
    except Exception:
        return []


def _text(el, tag: str) -> str:
    node = el.find(tag)
    return node.text.strip() if node is not None and node.text else ""


def _parse_date(raw: str) -> str:
    m = re.search(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", raw)
    if m:
        mo_map = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                  "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
        d, mo, y = m.group(1), m.group(2), m.group(3)
        return f"{y}-{mo_map.get(mo,'00')}-{d.zfill(2)}"
    return raw or "날짜 미상"


def _build_system(grade: str, learning_type_id: str) -> str:
    info = get_type(learning_type_id)
    gg = "초등" if grade.startswith("초") else ("중등" if grade.startswith("중") else "고등")
    return SYSTEM_BASE.format(
        type_name=info["name"], type_core=info["core"], grade=grade,
        tone_guide=GRADE_TONE_GUIDE[gg],
        question_style=TYPE_QUESTION_STYLE[learning_type_id],
    )


# ── 뉴스 3줄 요약 ──

def build_batch_summarize_prompt(news_items: list, grade: str, learning_type_id: str) -> tuple:
    """N개의 뉴스를 하나의 프롬프트로 묶어 단건 API 호출로 처리."""
    lines = []
    for i, item in enumerate(news_items):
        lines.append(f"[뉴스 {i}]")
        lines.append(f"제목: {item.get('headline', '')}")
        snippet = item.get("summary", "")
        if snippet:
            lines.append(f"미리보기: {snippet[:200]}")
        lines.append("")
    user = STEP06_NEWS_BATCH_SUMMARY.format(news_list="\n".join(lines))
    return _build_system(grade, learning_type_id), user


def build_summarize_prompt(headline: str, summary: str, grade: str, learning_type_id: str) -> tuple:
    user = STEP06_NEWS_SUMMARY.format(headline=headline, summary=summary or "내용 미리보기 없음")
    return _build_system(grade, learning_type_id), user


def summarize_news(headline: str, summary: str, grade: str, learning_type_id: str) -> str:
    system, user = build_summarize_prompt(headline, summary, grade, learning_type_id)
    return ask(system, user, max_tokens=512, json_mode=False)


# ── 유형별 추가 자료 ──

def build_extra_resources_prompt(refined_topic: str, grade: str, learning_type_id: str) -> tuple:
    info = get_type(learning_type_id)
    user = STEP06_EXTRA_RESOURCES.format(
        refined_topic=refined_topic,
        type_name=info["name"],
        extra_resource_desc=info.get("extra_resources", ""),
        grade=grade,
    )
    return _build_system(grade, learning_type_id), user


def get_extra_resources(refined_topic: str, grade: str, learning_type_id: str) -> dict:
    system, user = build_extra_resources_prompt(refined_topic, grade, learning_type_id)
    result = ask(system, user, json_mode=True)
    return result if isinstance(result, dict) else {"items": []}

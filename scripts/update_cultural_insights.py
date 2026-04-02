#!/usr/bin/env python3
"""Summarize cultural context across RSS + chart snapshots for landing storytelling."""

from __future__ import annotations

import json
import re
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = ROOT / 'app' / 'static' / 'data' / 'cultural_insights.json'
CULTURE_RSS_PATH = ROOT / 'app' / 'static' / 'data' / 'culture_rss.json'
BILLBOARD_PATH = ROOT / 'app' / 'static' / 'data' / 'billboard_hot100.json'
DEEZER_PATH = ROOT / 'app' / 'static' / 'data' / 'deezer_chart.json'

STOPWORDS = {
    'jun', 'music', 'cultural', 'culture', 'story', 'signal', 'archive', 'chart', 'global',
    'new', 'today', 'pulse', 'trend', 'insight', 'content', 'record', 'feature', 'fresh',
    'weekly', 'daily', 'platform', 'members', 'community', 'brand', 'studio', 'lead',
    'artist', 'top', 'live', 'now', 'coming', 'episode', 'series', 'debut', 'release',
    'feat', 'ft', 'of', 'to', 'for', 'from', 'the', 'and', 'that', 'this', 'these',
    'with', 'in', 'on', 'at', 'by', 'are', 'is', 'was', 'will', 'you', 'your', 'they',
    'their', 'be', 'we', 'just', 'have', 'has', 'had', 'do', 'does', 'did', 'such',
    'there', 'here', 'all', 'some', 'many', 'about', 'much', 'who', 'what', 'which',
    'where', 'when', 'why', 'how', 'than', 'then', 'per', 'as', 'up', 'so', 'but', 'or',
    'into', 'its', 'not', 'more', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
    'eight', 'nine', 'ten', 'week', 'weeks', 'month', 'months', 'year', 'years', 'latest',
    'newest', 'over', 'after', 'next', 'ago'
}
WORD_PATTERN = re.compile(r'[A-Za-z0-9가-힣]+')
MAX_STORIES = 3
MAX_KEYWORDS = 6
DEFAULT_HEADLINE = 'Jun의 레이더가 문화 신호를 정리 중입니다.'
DEFAULT_CTA = {
    'label': 'Share Cultural Brief',
    'link': '/brand-studio'
}


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open('r', encoding='utf-8') as handle:
            data = json.load(handle)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _extract_keywords(texts: list[str]) -> list[dict[str, int]]:
    counter = Counter()
    for text in texts:
        if not text:
            continue
        for token in WORD_PATTERN.findall(text.lower()):
            if len(token) < 2:
                continue
            if token.isdigit():
                continue
            if token in STOPWORDS:
                continue
            counter[token] += 1
    keywords = []
    for word, count in counter.most_common(MAX_KEYWORDS):
        keywords.append({'keyword': word, 'count': count})
    return keywords


def _gather_texts(rss: dict, billboard: dict, deezer: dict) -> list[str]:
    texts = []
    for source in rss.get('sources', []):
        entries = source.get('entries') or []
        for entry in entries[:2]:
            summary = entry.get('summary') or entry.get('title')
            if summary:
                texts.append(summary)
    for bucket in (billboard.get('top_tracks') or [], deezer.get('top_tracks') or []):
        for track in bucket[:3]:
            title = track.get('title')
            artist = track.get('artist')
            if title:
                texts.append(title)
            if artist:
                texts.append(artist)
    return texts


def _build_stories(rss: dict) -> list[dict]:
    stories = []
    for source in rss.get('sources', []):
        entries = source.get('entries') or []
        if not entries:
            continue
        highlight = entries[0]
        summary = highlight.get('summary') or highlight.get('title')
        stories.append({
            'source': source.get('name') or source.get('tagline') or 'Culture Feed',
            'title': highlight.get('title'),
            'summary': summary,
            'link': highlight.get('link')
        })
        if len(stories) >= MAX_STORIES:
            break
    return stories


def _build_chart_highlights(billboard: dict, deezer: dict) -> list[dict]:
    highlights = []
    for label, data in [('Billboard', billboard), ('Deezer', deezer)]:
        tracks = data.get('top_tracks') or []
        if not tracks:
            continue
        track = tracks[0]
        highlights.append({
            'source': data.get('source') or f'{label} Chart',
            'title': track.get('title'),
            'artist': track.get('artist'),
            'captured_at': data.get('captured_at') or data.get('generated_at'),
        })
    return highlights


def _build_headline(keywords: list[dict]) -> str:
    if not keywords:
        return DEFAULT_HEADLINE
    focus_words = [kw['keyword'] for kw in keywords[:2]]
    if len(focus_words) == 1:
        return f"Jun의 레이더는 {focus_words[0]} 신호를 주시하고 있습니다."
    return f"Jun의 레이더는 {focus_words[0]}과 {focus_words[1]} 신호를 문화 전선에서 동시 추적 중입니다."


def build_payload(rss: dict, billboard: dict, deezer: dict) -> dict:
    texts = _gather_texts(rss, billboard, deezer)
    keywords = _extract_keywords(texts)
    stories = _build_stories(rss)
    chart_highlights = _build_chart_highlights(billboard, deezer)
    payload = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'headline': _build_headline(keywords),
        'keywords': keywords,
        'stories': stories,
        'chart_highlights': chart_highlights,
        'cta': DEFAULT_CTA,
        'notes': 'scripts/update_cultural_insights.py로 RSS와 차트 데이터를 다시 조합해 새로운 내러티브를 만들 수 있습니다.'
    }
    return payload


def save(payload: dict):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open('w', encoding='utf-8') as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def main():
    try:
        rss = _load_json(CULTURE_RSS_PATH)
        billboard = _load_json(BILLBOARD_PATH)
        deezer = _load_json(DEEZER_PATH)
        payload = build_payload(rss, billboard, deezer)
        save(payload)
        print(f"Saved cultural insight snapshot with {len(payload['keywords'])} keywords at {payload['generated_at']}")
    except Exception:  # pragma: no cover - operational script
        print('Failed to build cultural insight payload:')
        traceback.print_exc()
        print('Existing cultural_insights.json remains untouched if it already exists.')


if __name__ == '__main__':
    main()

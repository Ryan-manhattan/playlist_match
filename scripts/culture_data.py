#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    from utils.supabase_client import SupabaseClient
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

ROOT = Path(__file__).resolve().parent.parent
CULTURE_FILE = ROOT / 'app' / 'static' / 'data' / 'culture.json'
KEYWORDS = ['film', 'movie', 'cinema', 'score', 'soundtrack', 'director', 'screenplay']

DEFAULT_PAYLOAD = {
    'any_track': None,
    'top_tracks': [],
    'film_diaries': [],
    'hero_line': 'Cultural signals fuel the archive—every track blends with story.',
    'updated_at': datetime.utcnow().isoformat() + 'Z'
}


def filter_diaries(posts: List[Dict]) -> List[Dict]:
    filtered = []
    for post in posts:
        title = (post.get('title') or '').lower()
        content = (post.get('content') or '').lower()
        if any(keyword in title or keyword in content for keyword in KEYWORDS):
            filtered.append({
                'title': post.get('title'),
                'snippet': (post.get('content') or '')[:120].strip(),
                'author': post.get('author'),
                'created_at': post.get('created_at')
            })
            if len(filtered) >= 3:
                break
    return filtered


def gather_culture_payload() -> Dict:
    payload = DEFAULT_PAYLOAD.copy()
    payload['top_tracks'] = []
    payload['film_diaries'] = []

    if not SUPABASE_AVAILABLE:
        return payload

    try:
        supabase = SupabaseClient()
        rankings = supabase.get_worldcup_rankings(limit=3)
        if rankings:
            for entry in rankings:
                payload['top_tracks'].append({
                    'title': entry.get('title'),
                    'artist': entry.get('artist'),
                    'wins': entry.get('wins', 0),
                    'duration': entry.get('duration_seconds'),
                })
            winner = rankings[0]
            payload['any_track'] = f"{winner.get('title')} by {winner.get('artist')}"
    except Exception:
        pass

    try:
        posts = supabase.get_posts(limit=50, offset=0, user_id=None)
        payload['film_diaries'] = filter_diaries(posts)
    except Exception:
        pass

    if payload['top_tracks'] and payload['any_track']:
        payload['hero_line'] = f"Now amplifying {payload['any_track']} alongside filmic stories."

    payload['updated_at'] = datetime.utcnow().isoformat() + 'Z'
    return payload


def save_payload(payload: Dict):
    CULTURE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with CULTURE_FILE.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main():
    payload = gather_culture_payload()
    save_payload(payload)
    print(f"Culture data saved: {payload['updated_at']}")


if __name__ == '__main__':
    main()

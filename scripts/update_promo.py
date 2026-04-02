#!/usr/bin/env python3
import copy
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict

try:
    from utils.supabase_client import SupabaseClient
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

ROOT_DIR = Path(__file__).resolve().parent.parent
PROMO_FILE = ROOT_DIR / 'app' / 'static' / 'data' / 'promo.json'
DEFAULT_OFFERS = [
    {
        'tagline': 'Launch Offer',
        'title': 'Archive Pass Beta',
        'description': 'Emotion-driven membership + exclusive creator features.',
        'price': '9,900 KRW / month',
        'bullets': ['Prioritized track stats', 'Member-only badges', 'Beta access workflows'],
        'cta': {
            'type': 'form',
            'label': 'JOIN BETA',
            'lead_type': 'creator_membership',
            'source_page': 'home_archive_pass'
        }
    },
    {
        'tagline': 'B2B Campaign',
        'title': 'Brand Studio Sprint',
        'description': 'Custom campaigns powered by fan diaries and worldcup buzz.',
        'price': '690,000 KRW +',
        'bullets': ['Dedicated brand playlist', 'Live voting experiences', 'Narrative report deck'],
        'cta': {
            'type': 'link',
            'label': 'OPEN BRAND STUDIO',
            'href': '/brand-studio'
        }
    },
    {
        'tagline': 'Insight Product',
        'title': 'Audience Insight Report',
        'description': 'Actionable narrative built from diaries, votes, and comments.',
        'price': '290,000 KRW +',
        'bullets': ['Keyword heatmap', 'Format recommendations', 'Collab roadmap'],
        'cta': {
            'type': 'form',
            'label': 'REQUEST REPORT',
            'lead_type': 'insight_report',
            'source_page': 'home_insight_report'
        }
    }
]

HERO_TEMPLATES = [
    'Emotion commerce flows: {tracks} tracks, {votes} votes, {visits} visits today.',
    'Monetize {tracks} tracks with {votes} votes of proof and {visits} visitors watching.',
    'From {tracks} archives to {votes} ballots, {visits} visitors feel the pulse.'
]

SUBTEXT_TEMPLATES = [
    'We refresh membership perks and brand kits hourly—{battles} battles this week.',
    'Hourly insight loop fueling creator membership + brand campaigns (recent {battles} battles).',
    'Realtime signals from the world cup keep {battles} story hooks on deck.'
]

FLASH_TEMPLATES = [
    'Top-ranked track: {top_title} by {top_artist}.',
    'Current spotlight: {top_title} — {top_artist}.',
    'Weekly spark: {top_title} powering {votes} votes.'
]


def gather_stats() -> Dict[str, int]:
    stats = {
        'total_tracks': 0,
        'total_posts': 0,
        'total_votes': 0,
        'today_visits': 0,
        'recent_battles': 0,
        'top_track_title': None,
        'top_track_artist': None,
    }

    if not SUPABASE_AVAILABLE:
        return stats

    try:
        supabase = SupabaseClient()
        tracks = supabase.get_tracks(limit=10000, offset=0, user_id=None, playlist_id=None)
        stats['total_tracks'] = len(tracks) if tracks else 0
    except Exception:
        pass

    try:
        posts = supabase.get_posts(limit=10000, offset=0, user_id=None)
        stats['total_posts'] = len(posts) if posts else 0
    except Exception:
        pass

    try:
        worldcup = supabase.get_worldcup_stats()
        stats['total_votes'] = worldcup.get('total_votes', 0)
        stats['recent_battles'] = worldcup.get('recent_battles', 0)
    except Exception:
        pass

    try:
        stats['today_visits'] = supabase.get_today_visits()
    except Exception:
        pass

    try:
        top_rankings = supabase.get_worldcup_rankings(limit=3)
        if top_rankings:
            winner = top_rankings[0]
            stats['top_track_title'] = winner.get('title')
            stats['top_track_artist'] = winner.get('artist')
    except Exception:
        pass

    return stats


def build_promo_payload(stats: Dict[str, int]) -> Dict:
    hero_heading = random.choice(HERO_TEMPLATES).format(
        tracks=stats['total_tracks'] or '0',
        votes=stats['total_votes'] or '0',
        visits=stats['today_visits'] or '0'
    )
    hero_subtext = random.choice(SUBTEXT_TEMPLATES).format(battles=stats['recent_battles'] or '0')
    if stats['top_track_title'] and stats['top_track_artist']:
        flash_line = random.choice(FLASH_TEMPLATES).format(
            top_title=stats['top_track_title'],
            top_artist=stats['top_track_artist'],
            votes=stats['total_votes'] or '0'
        )
    else:
        flash_line = 'Hourly refresh keeps the pitch deck sharp.'

    hero_ctas = [
        {'text': 'ADD YOUR TRACK', 'link': '/playlists', 'style': 'primary'},
        {'text': 'REQUEST MEDIA KIT', 'link': '/brand-studio', 'style': 'secondary'},
    ]

    metrics = {
        'tracks': stats['total_tracks'],
        'diaries': stats['total_posts'],
        'votes': stats['total_votes'],
        'visits': stats['today_visits'],
    }

    offers = []
    for base in DEFAULT_OFFERS:
        offer = copy.deepcopy(base)
        dynamic_text = f"Powered by {stats['total_votes']} votes and {stats['today_visits']} visitors." if stats['total_votes'] or stats['today_visits'] else ''
        offer['description'] = f"{dynamic_text} {offer['description']}".strip()
        offers.append(offer)

    return {
        'hero': {
            'heading': hero_heading,
            'subtext': hero_subtext,
            'flash_line': flash_line,
            'ctas': hero_ctas,
        },
        'offers': offers,
        'metrics': metrics,
        'updated_at': datetime.utcnow().isoformat() + 'Z',
    }


def save_promo(payload: Dict):
    PROMO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROMO_FILE.open('w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_existing() -> Dict:
    if not PROMO_FILE.exists():
        return {}
    try:
        return json.loads(PROMO_FILE.read_text(encoding='utf-8'))
    except Exception:
        return {}


def main():
    stats = gather_stats()
    payload = build_promo_payload(stats)
    save_promo(payload)
    print(f"Promotional content saved to {PROMO_FILE} at {payload['updated_at']}")


if __name__ == '__main__':
    main()

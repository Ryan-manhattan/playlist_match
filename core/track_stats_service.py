"""
Track stats synchronization helpers.

Fetches lightweight engagement metrics for supported providers and returns
normalized payloads that can be stored in tracks.metadata.stats.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import yt_dlp

from processors.link_extractor import LinkExtractor


class TrackStatsService:
    """Fetch external engagement stats for public track URLs."""

    def __init__(self, console_log=None):
        self.console_log = console_log or print
        self.extractor = LinkExtractor(console_log=self.console_log)

    def fetch_stats(self, track: Dict[str, Any]) -> Dict[str, Any]:
        source = (track.get("source") or "").strip().lower()

        if source == "youtube":
            return self._fetch_youtube_stats(track)
        if source == "soundcloud":
            return self._fetch_soundcloud_stats(track)

        return {
            "success": False,
            "error": "지원하지 않는 트랙 소스입니다.",
        }

    def _fetch_youtube_stats(self, track: Dict[str, Any]) -> Dict[str, Any]:
        url = (track.get("url") or "").strip()
        source_id = (track.get("source_id") or "").strip() or self.extractor.extract_video_id(url)

        if self.extractor.youtube and source_id:
            try:
                request = self.extractor.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=source_id,
                )
                response = request.execute()
                items = response.get("items", [])
                if items:
                    video = items[0]
                    snippet = video.get("snippet", {})
                    content_details = video.get("contentDetails", {})
                    statistics = video.get("statistics", {})

                    return {
                        "success": True,
                        "provider": "youtube_api",
                        "source_id": source_id,
                        "stats": {
                            "views": self._safe_int(statistics.get("viewCount")),
                            "likes": self._safe_int(statistics.get("likeCount")),
                            "comments": self._safe_int(statistics.get("commentCount")),
                        },
                        "provider_fields": {
                            "title": snippet.get("title"),
                            "uploader": snippet.get("channelTitle"),
                            "duration_seconds": self.extractor._parse_duration(
                                content_details.get("duration", "PT0S")
                            ),
                            "thumbnail_url": self._best_thumbnail(snippet.get("thumbnails", {})),
                        },
                    }
            except Exception as exc:
                self.console_log(f"[TrackStats] YouTube API sync failed, fallback to yt-dlp: {exc}")

        info = self._extract_info(url)
        if not info.get("success"):
            return info

        return {
            "success": True,
            "provider": "yt_dlp",
            "source_id": source_id,
            "stats": {
                "views": self._safe_int(info.get("view_count")),
                "likes": self._safe_int(info.get("like_count")),
                "comments": self._safe_int(info.get("comment_count")),
            },
            "provider_fields": self._provider_fields_from_info(info),
        }

    def _fetch_soundcloud_stats(self, track: Dict[str, Any]) -> Dict[str, Any]:
        url = (track.get("url") or "").strip()
        info = self._extract_info(url)
        if not info.get("success"):
            return info

        plays = self._safe_int(info.get("play_count"))
        if plays is None:
            plays = self._safe_int(info.get("view_count"))

        return {
            "success": True,
            "provider": "yt_dlp",
            "stats": {
                "plays": plays,
                "likes": self._safe_int(info.get("like_count")),
                "comments": self._safe_int(info.get("comment_count")),
            },
            "provider_fields": self._provider_fields_from_info(info),
        }

    def _extract_info(self, url: str) -> Dict[str, Any]:
        if not url:
            return {
                "success": False,
                "error": "유효한 URL이 없습니다.",
            }

        try:
            with yt_dlp.YoutubeDL(
                {
                    "quiet": True,
                    "skip_download": True,
                    "socket_timeout": 15,
                    "http_headers": {
                        "User-Agent": (
                            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/122.0.0.0 Safari/537.36"
                        )
                    },
                }
            ) as ydl:
                info = ydl.extract_info(url, download=False)
        except Exception as exc:
            return {
                "success": False,
                "error": f"외부 메타데이터를 가져오지 못했습니다: {exc}",
            }

        if not isinstance(info, dict):
            return {
                "success": False,
                "error": "응답 형식이 올바르지 않습니다.",
            }

        info["success"] = True
        return info

    @staticmethod
    def _provider_fields_from_info(info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration_seconds": TrackStatsService._safe_int(info.get("duration")),
            "thumbnail_url": info.get("thumbnail"),
        }

    @staticmethod
    def _best_thumbnail(thumbnails: Dict[str, Any]) -> Optional[str]:
        if not isinstance(thumbnails, dict):
            return None

        for key in ("maxres", "standard", "high", "medium", "default"):
            item = thumbnails.get(key)
            if isinstance(item, dict) and item.get("url"):
                return item.get("url")
        return None

    @staticmethod
    def _safe_int(value: Any) -> Optional[int]:
        if value in (None, "", "null"):
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

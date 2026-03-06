"""
Fallback store for monetization leads.

Used when Supabase is unavailable or lead inserts fail, so conversion intent
is still persisted locally during development or degraded runtime conditions.
"""

from __future__ import annotations

import json
import os
import threading
import uuid
from datetime import datetime
from typing import Dict


class GrowthLeadStore:
    """Append-only JSONL fallback for growth leads."""

    def __init__(self, root_dir: str):
        self._lock = threading.Lock()
        self.output_dir = os.path.join(root_dir, "data", "growth")
        self.output_path = os.path.join(self.output_dir, "growth_leads.jsonl")

    def append(self, payload: Dict) -> str:
        os.makedirs(self.output_dir, exist_ok=True)

        record = dict(payload)
        record["id"] = str(uuid.uuid4())
        record["stored_via"] = "local_fallback"
        record["created_at"] = datetime.now().isoformat()

        line = json.dumps(record, ensure_ascii=False) + "\n"
        with self._lock:
            with open(self.output_path, "a", encoding="utf-8") as handle:
                handle.write(line)

        return record["id"]

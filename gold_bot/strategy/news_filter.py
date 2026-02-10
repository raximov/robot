from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class NewsEvent:
    title: str
    event_time_utc: datetime
    impact: str


def should_block_trading(events: list[NewsEvent], block_minutes: int, now_utc: datetime | None = None) -> bool:
    now = now_utc or datetime.now(timezone.utc)
    horizon = timedelta(minutes=block_minutes)

    for event in events:
        if event.impact.lower() not in {"high", "medium"}:
            continue
        if abs(event.event_time_utc - now) <= horizon:
            return True
    return False

from __future__ import annotations

from dataclasses import asdict

from .models import FeedbackRecord, MemorySnapshot


def memory_to_dict(snapshot: MemorySnapshot) -> dict:
    return {
        "feedback": [asdict(item) for item in snapshot.feedback],
        "preferences": dict(snapshot.preferences),
    }


def memory_from_dict(payload: dict) -> MemorySnapshot:
    feedback = [FeedbackRecord(**item) for item in payload.get("feedback", [])]
    preferences = dict(payload.get("preferences") or {})
    return MemorySnapshot(feedback=feedback, preferences=preferences)


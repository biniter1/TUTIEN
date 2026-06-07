"""
Seed script: title definitions and achievement definitions.

Idempotent: safe to run multiple times.
- Records that already exist (matched by code) are updated with current field values.
- New records are created.

Titles are seeded before achievements because achievement definitions reference
title codes via the reward_title_code field.

Usage (from backend/ with venv activated):
    python scripts/seed_achievements_titles.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.modules.achievements.models import AchievementDefinition, TitleDefinition

# ---------------------------------------------------------------------------
# Seed data — add new titles/achievements here without changing business logic
# ---------------------------------------------------------------------------

TITLES = [
    {
        "code": "FIRST_STEP_CULTIVATOR",
        "name": "Sơ Nhập Đạo",
        "description": "Danh hiệu dành cho tu sĩ vừa đặt chân lên tiên lộ.",
        "rarity": "common",
    },
    {
        "code": "DAO_HEART_STEADY",
        "name": "Đạo Tâm Kiên Định",
        "description": "Danh hiệu dành cho người hoàn thành nhiệm vụ ngày đầu tiên.",
        "rarity": "rare",
    },
    {
        "code": "WORD_INITIATE",
        "name": "Linh Tự Sơ Thành",
        "description": "Danh hiệu dành cho người bắt đầu lĩnh ngộ linh tự.",
        "rarity": "common",
    },
]

ACHIEVEMENTS = [
    {
        "code": "FIRST_CORRECT_ANSWER",
        "name": "Lần Đầu Lĩnh Ngộ",
        "description": "Trả lời đúng câu hỏi đầu tiên.",
        "category": "vocabulary",
        "condition_type": "correct_answers",
        "condition_value": 1,
        "reward_title_code": "FIRST_STEP_CULTIVATOR",
        "is_hidden": False,
    },
    {
        "code": "FIRST_DAILY_CLAIM",
        "name": "Đạo Tâm Kiên Định",
        "description": "Claim phần thưởng nhiệm vụ ngày đầu tiên.",
        "category": "daily",
        "condition_type": "daily_claims",
        "condition_value": 1,
        "reward_title_code": "DAO_HEART_STEADY",
        "is_hidden": False,
    },
    {
        "code": "MASTER_ONE_WORD",
        "name": "Linh Tự Sơ Thành",
        "description": "Đạt mastery level 1 với một từ vựng.",
        "category": "vocabulary",
        "condition_type": "word_mastery_level",
        "condition_value": 1,
        "reward_title_code": "WORD_INITIATE",
        "is_hidden": False,
    },
]

# ---------------------------------------------------------------------------
# Seed functions
# ---------------------------------------------------------------------------

TITLE_MUTABLE_FIELDS = ("name", "description", "rarity", "is_active")
ACHIEVEMENT_MUTABLE_FIELDS = (
    "name", "description", "category", "condition_type", "condition_value",
    "reward_title_code", "is_hidden", "is_active",
)


def seed_titles(db) -> tuple[int, int]:
    created = updated = 0
    for data in TITLES:
        existing = (
            db.query(TitleDefinition)
            .filter(TitleDefinition.code == data["code"])
            .first()
        )
        if existing is None:
            db.add(TitleDefinition(**data))
            created += 1
            print(f"  [Title] Created : {data['code']}")
        else:
            for field in TITLE_MUTABLE_FIELDS:
                if field in data:
                    setattr(existing, field, data[field])
            updated += 1
            print(f"  [Title] Updated : {data['code']}")
    return created, updated


def seed_achievements(db) -> tuple[int, int]:
    created = updated = 0
    for data in ACHIEVEMENTS:
        existing = (
            db.query(AchievementDefinition)
            .filter(AchievementDefinition.code == data["code"])
            .first()
        )
        if existing is None:
            db.add(AchievementDefinition(**data))
            created += 1
            print(f"  [Achievement] Created : {data['code']}")
        else:
            for field in ACHIEVEMENT_MUTABLE_FIELDS:
                if field in data:
                    setattr(existing, field, data[field])
            updated += 1
            print(f"  [Achievement] Updated : {data['code']}")
    return created, updated


def seed() -> None:
    db = SessionLocal()
    try:
        print("Seeding titles...")
        t_created, t_updated = seed_titles(db)
        db.commit()
        print(f"  Done. Created: {t_created}, Updated: {t_updated}.\n")

        print("Seeding achievements...")
        a_created, a_updated = seed_achievements(db)
        db.commit()
        print(f"  Done. Created: {a_created}, Updated: {a_updated}.\n")

        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

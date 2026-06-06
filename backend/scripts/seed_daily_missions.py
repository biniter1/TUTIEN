"""
Seed script: default daily mission definitions.

Idempotent: safe to run multiple times.
- Missions that already exist (matched by code) are skipped.
- Only missing missions are inserted.

Usage (from backend/ with venv activated):
    python scripts/seed_daily_missions.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.modules.quests.models import DailyMissionDefinition

MISSIONS = [
    {
        "code": "ANSWER_5_QUESTIONS",
        "name": "Answer 5 Questions",
        "description": "Hoàn thành 5 lần thí luyện để hấp thu linh khí.",
        "mission_type": "answer_questions",
        "target_value": 5,
        "reward_cultivation_power": 10,
        "reward_reputation": 0,
    },
    {
        "code": "CORRECT_3_ANSWERS",
        "name": "Correct 3 Answers",
        "description": "Trả lời đúng 3 lần để củng cố đạo tâm.",
        "mission_type": "correct_answers",
        "target_value": 3,
        "reward_cultivation_power": 15,
        "reward_reputation": 0,
    },
    {
        "code": "GAIN_20_CULTIVATION_POWER",
        "name": "Gain 20 Cultivation Power",
        "description": "Tích lũy 20 tu vi trong ngày.",
        "mission_type": "gain_cultivation_power",
        "target_value": 20,
        "reward_cultivation_power": 20,
        "reward_reputation": 0,
    },
    {
        "code": "SPEND_10_SPIRIT_ENERGY",
        "name": "Spend 10 Spirit Energy",
        "description": "Tiêu hao 10 linh lực cho quá trình tu luyện.",
        "mission_type": "spend_spirit_energy",
        "target_value": 10,
        "reward_cultivation_power": 10,
        "reward_reputation": 0,
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        created = 0
        skipped = 0
        for data in MISSIONS:
            existing = (
                db.query(DailyMissionDefinition)
                .filter(DailyMissionDefinition.code == data["code"])
                .first()
            )
            if existing is None:
                db.add(DailyMissionDefinition(**data))
                created += 1
                print(f"  Created : {data['code']}")
            else:
                skipped += 1
                print(f"  Skipped : {data['code']} (already exists)")

        if created > 0:
            db.commit()

        print(f"\nDone. Created: {created}, Skipped: {skipped}.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

"""
Seed script: first vocabulary set — Cultivation Basics.

Idempotent: safe to run multiple times.
- Reuses the set if code "cultivation-basics" already exists.
- Skips words whose english value already exists in the set.
- Recalculates total_words after every run.

Usage (from backend/ with venv activated):
    python scripts/seed_vocabulary.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.modules.vocabulary.models import VocabularySet, VocabularyWord

SET_CODE = "cultivation-basics"

SET_META = {
    "name": "Cultivation Basics",
    "description": "Essential English words for every beginner cultivator on the path to immortality.",
    "theme": "cultivation",
    "difficulty": "beginner",
    "required_realm": None,
}

WORDS = [
    {
        "english": "cultivate",
        "vietnamese": "tu luyện",
        "pronunciation": "/ˈkʌltɪveɪt/",
        "example_sentence": "He cultivates his spirit energy every morning at dawn.",
        "example_translation": "Anh ấy tu luyện năng lượng linh hồn mỗi sáng sớm.",
        "difficulty": "beginner",
    },
    {
        "english": "realm",
        "vietnamese": "cảnh giới",
        "pronunciation": "/rɛlm/",
        "example_sentence": "She broke through to the next realm after a hundred days of meditation.",
        "example_translation": "Cô ấy đột phá lên cảnh giới tiếp theo sau một trăm ngày tĩnh tọa.",
        "difficulty": "beginner",
    },
    {
        "english": "spirit",
        "vietnamese": "linh hồn / tinh thần",
        "pronunciation": "/ˈspɪrɪt/",
        "example_sentence": "His spirit was unbreakable even after a thousand years of hardship.",
        "example_translation": "Tinh thần của anh ấy không thể bị bẻ gãy dù trải qua ngàn năm gian khó.",
        "difficulty": "beginner",
    },
    {
        "english": "energy",
        "vietnamese": "năng lượng",
        "pronunciation": "/ˈɛnərdʒi/",
        "example_sentence": "The ancient tree radiated powerful energy that all cultivators could feel.",
        "example_translation": "Cây cổ thụ tỏa ra năng lượng mạnh mẽ mà mọi tu sĩ đều cảm nhận được.",
        "difficulty": "beginner",
    },
    {
        "english": "breakthrough",
        "vietnamese": "đột phá",
        "pronunciation": "/ˈbreɪkθruː/",
        "example_sentence": "After years of stagnation, he finally achieved a breakthrough.",
        "example_translation": "Sau nhiều năm trì trệ, anh ấy cuối cùng đã đạt được đột phá.",
        "difficulty": "beginner",
    },
    {
        "english": "foundation",
        "vietnamese": "căn cơ",
        "pronunciation": "/faʊnˈdeɪʃən/",
        "example_sentence": "A solid foundation is more important than a fast cultivation speed.",
        "example_translation": "Căn cơ vững chắc quan trọng hơn tốc độ tu luyện nhanh.",
        "difficulty": "beginner",
    },
    {
        "english": "technique",
        "vietnamese": "công pháp / kỹ thuật",
        "pronunciation": "/tɛkˈniːk/",
        "example_sentence": "She mastered the forbidden technique in only three months.",
        "example_translation": "Cô ấy đã thành thạo công pháp cấm chỉ trong ba tháng.",
        "difficulty": "beginner",
    },
    {
        "english": "immortal",
        "vietnamese": "tiên nhân / bất tử",
        "pronunciation": "/ɪˈmɔːrtəl/",
        "example_sentence": "The immortal elder watched over the sect for ten thousand years.",
        "example_translation": "Vị tiên nhân trưởng lão đã trông coi tông môn suốt mười nghìn năm.",
        "difficulty": "beginner",
    },
    {
        "english": "treasure",
        "vietnamese": "bảo vật",
        "pronunciation": "/ˈtrɛʒər/",
        "example_sentence": "The ancient treasure was hidden deep inside the forbidden mountain.",
        "example_translation": "Bảo vật cổ xưa được giấu sâu bên trong ngọn núi cấm địa.",
        "difficulty": "beginner",
    },
    {
        "english": "disciple",
        "vietnamese": "đệ tử",
        "pronunciation": "/dɪˈsaɪpəl/",
        "example_sentence": "The sect accepted only three new disciples each year.",
        "example_translation": "Tông môn chỉ nhận ba đệ tử mới mỗi năm.",
        "difficulty": "beginner",
    },
]


def seed() -> None:
    db = SessionLocal()
    try:
        # Get or create the vocabulary set
        vocab_set = db.query(VocabularySet).filter(VocabularySet.code == SET_CODE).first()
        if vocab_set is None:
            vocab_set = VocabularySet(code=SET_CODE, **SET_META)
            db.add(vocab_set)
            db.flush()
            print(f"Created vocabulary set: {SET_CODE}")
        else:
            print(f"Vocabulary set '{SET_CODE}' already exists — reusing.")

        # Collect existing words in this set to avoid duplicates
        existing_english = {
            w.english
            for w in db.query(VocabularyWord.english)
            .filter(VocabularyWord.set_id == vocab_set.id)
            .all()
        }

        inserted = 0
        for word_data in WORDS:
            if word_data["english"] not in existing_english:
                db.add(VocabularyWord(set_id=vocab_set.id, **word_data))
                inserted += 1

        db.flush()

        # Recalculate total_words from the actual DB count
        total = db.query(VocabularyWord).filter(VocabularyWord.set_id == vocab_set.id).count()
        vocab_set.total_words = total

        db.commit()
        print(f"Inserted {inserted} new word(s). Total words in set: {total}.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()

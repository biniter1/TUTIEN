# Current Project State

## Completed

### Task 1A: Backend Skeleton
- FastAPI backend structure
- PostgreSQL with Docker Compose
- SQLAlchemy database setup
- GET /health
- Database health check

### Task 1B: Alembic Foundation
- Alembic configured
- DATABASE_URL loaded from settings
- Base.metadata used for autogenerate

### Task 1C: Auth + Users
- POST /auth/register
- POST /auth/login
- GET /users/me
- JWT authentication
- Password hashing
- users table

### Task 1D: Cultivation Profile
- cultivation_profiles table
- Auto-create cultivation profile after register
- GET /cultivation/me
- Default realm: Pham Nhan
- Default cultivation_power: 0
- Default spirit_energy: 100

### Task 2A: Vocabulary Static Content
- vocabulary_sets table
- vocabulary_words table
- GET /vocabulary/sets
- GET /vocabulary/sets/{set_id}
- GET /vocabulary/sets/{set_id}/words
- Seed script for cultivation-basics vocabulary set

### Task 2B: Vocabulary Quiz + Progress + Cultivation Gain
- user_word_progress table
- POST /vocabulary/quiz/submit
- Correct answer gives +5 cultivation_power
- Tracks correct_count, wrong_count, mastery_level

### Task 2C: Vocabulary Progress APIs
- GET /vocabulary/progress/me
- GET /vocabulary/sets/{set_id}/progress

### Task 3A: Spirit Energy Cost
- Each valid quiz submission costs 1 spirit_energy
- Invalid word_id does not deduct energy
- Correct answer still gives +5 cultivation_power
- Quiz response returns spirit_energy_spent and remaining_spirit_energy

### Task 3B: Daily Mission Foundation
- daily_mission_definitions table
- user_daily_mission_progress table
- GET /quests/daily
- Seed script for default daily missions:
  - ANSWER_5_QUESTIONS
  - CORRECT_3_ANSWERS
  - GAIN_20_CULTIVATION_POWER
  - SPEND_10_SPIRIT_ENERGY

## Current Next Task

Task 3C: Update Daily Mission Progress from Vocabulary Quiz.

When POST /vocabulary/quiz/submit succeeds:
- answer_questions +1 for every valid quiz submission
- correct_answers +1 if answer is correct
- gain_cultivation_power + cultivation_power_gained
- spend_spirit_energy + spirit_energy_spent

Rules:
- If mission definitions are not seeded, do nothing silently.
- If today's progress rows do not exist, create them.
- Cap progress_value at target_value.
- Mark is_completed = true when progress_value >= target_value.
- Do not implement claim reward yet.

## Architecture Reminder

Use Modular Monolith first, microservice-ready later.

Do not create real microservices yet.

Module boundaries:
- router.py handles HTTP only
- service.py handles business logic
- repository.py handles DB queries
- schemas.py handles DTOs
- models.py handles SQLAlchemy tables

vocabulary.service should not directly query quest tables.
It should call quests.service.
### Task 3C: Daily Mission Progress from Vocabulary Quiz
- Vocabulary quiz submission updates today's daily missions
- answer_questions +1 for every valid quiz submission
- correct_answers +1 if answer is correct
- gain_cultivation_power + gained amount
- spend_spirit_energy + spent amount
- Mission progress caps at target_value
- is_completed becomes true when progress reaches target

### Task 3D: Daily Mission Reward Claim
- POST /quests/daily/{mission_code}/claim
- Can claim only completed and unclaimed missions
- Claim reward adds cultivation_power and reputation
- Marks mission as claimed
- Prevents duplicate claim
### Task 4A: Achievement and Title Foundation
- achievement_definitions table
- user_achievements table
- title_definitions table
- user_titles table
- GET /achievements/me
- GET /titles/me
- Seed script for initial achievements and titles
- Content is data-driven through stable code fields

### Task 4B: Auto Unlock Achievements and Grant Titles
- Vocabulary quiz can unlock FIRST_CORRECT_ANSWER
- Vocabulary mastery can unlock MASTER_ONE_WORD
- Daily mission claim can unlock FIRST_DAILY_CLAIM
- Unlocking achievements can grant reward titles
- Unlock logic is idempotent
- API responses return unlocked_achievements and unlocked_titles for frontend animation
### Task 4C: Equip Unlocked Title
- POST /titles/{title_code}/equip
- User can equip only unlocked titles
- Equipping one title unequips other titles
- GET /titles/me shows correct is_equipped state
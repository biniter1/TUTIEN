# AGENTS.md

## Project Name

English Cultivation / Tu Tiên Anh Ngữ

## Product Vision

This project is a gamified English-learning web application with a xianxia/cultivation theme.

Users learn vocabulary, reading, and listening to gain cultivation power, advance realms, unlock achievements, earn titles, compete on leaderboards, and later join PvP quiz battles.

The product must feel like a cultivation game, not a normal school learning website.

## Architecture Direction

Use Modular Monolith first, Microservice-ready later.

Do not create real distributed microservices yet.

The backend must be organized by domain modules so each module can later be extracted into its own service.

## Backend Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT authentication
- Docker Compose for local development

## Frontend Stack

- React
- Vite
- TailwindCSS
- CSS animation later
- Motion/Lottie/Rive later if needed

## Backend Folder Structure

backend/app/
  main.py
  core/
    config.py
    database.py
    security.py
    dependencies.py
  modules/
    auth/
      router.py
      schemas.py
      service.py
      repository.py
      models.py
    users/
      router.py
      schemas.py
      service.py
      repository.py
      models.py
    cultivation/
      router.py
      schemas.py
      service.py
      repository.py
      models.py
    vocabulary/
      router.py
      schemas.py
      service.py
      repository.py
      models.py
    quests/
    achievements/
    rankings/
    cosmetics/
    pk/
    sects/
    notifications/
  shared/
    exceptions.py
    response.py
    pagination.py
    events.py

## MVP Scope

Implement MVP v1 first:

1. Auth
2. User profile
3. Cultivation profile
4. Vocabulary sets
5. Vocabulary quiz
6. Daily quests
7. Achievements and titles
8. Leaderboards
9. Basic cultivation-themed frontend UI

Do not implement these yet unless explicitly requested:

- Real microservices
- Kubernetes
- Kafka
- Payment
- Speaking
- AI teacher
- 3D characters
- Complex real-time PvP
- Marketplace
- Season system

## Domain Terminology

Use cultivation terminology:

- EXP = cultivation_power or tu_vi
- Level = realm
- Energy = spirit_energy
- Course = cultivation_method
- Lesson = training_session
- Leaderboard = heavenly_board
- Guild = sect
- PvP = dao_battle
- Profile = dao_profile
- Daily quest = daily_mission
- Reputation = reputation

## Coding Rules

- Keep each module isolated.
- Router handles HTTP only.
- Service handles business logic.
- Repository handles database queries.
- Schemas handle request/response DTOs.
- Models handle database tables.
- Do not put business logic inside routers.
- Do not make one giant file.
- Do not hardcode secrets.
- Use environment variables.
- Use Alembic migrations for database changes.
- Prefer simple code over clever code.
- Do not refactor unrelated files.

## Security Rules

- Hash passwords.
- Use JWT access token.
- Validate inputs with Pydantic.
- Never expose password hashes.
- Do not trust client-side reward calculations.
- Reward, tu_vi, reputation, title unlock logic must be server-side.

## Event-Driven Extension Rule

When an action affects multiple modules, prefer internal domain events.

Example:

When a user answers a vocabulary question correctly, emit:

UserAnsweredCorrect

Then these modules may react:

- cultivation: increase cultivation power
- quests: update daily mission progress
- achievements: check unlock conditions
- rankings: update leaderboard score
- notifications: notify title unlock

For MVP, internal Python event dispatcher is enough. Do not add Kafka/RabbitMQ yet.

## AI Coding Agent Instructions

Before modifying code:

1. Read AGENTS.md.
2. Read relevant docs in /docs.
3. Identify the module affected.
4. Explain planned files to change.
5. Make the smallest useful change.
6. Do not refactor unrelated files.
7. After coding, summarize:
   - files changed
   - endpoints added
   - database changes
   - how to test
## Extensibility Rules

The project must be content-driven and easy to extend.

Avoid hardcoding game content directly in business logic.

Prefer stable `code` fields for game definitions:
- vocabulary_sets.code
- achievement_definitions.code
- title_definitions.code
- daily_mission_definitions.code
- future realm_definitions.code

Seed scripts must be idempotent:
- running the same seed multiple times must not create duplicates
- existing records should be reused or updated safely

Adding new content should usually require adding seed data or future admin/import data, not rewriting core logic.

Examples:
- Adding a new title should not require changing reward logic.
- Adding a new achievement should not require changing API structure.
- Adding a new vocabulary set should not require new code.
- Adding a new realm should later be possible through realm definitions, not hardcoded strings.
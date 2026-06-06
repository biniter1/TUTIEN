# Roadmap

## Phase 1: Foundation

Goal:
Create the base backend structure with authentication, user profile, and cultivation profile.

Tasks:
- Setup FastAPI project
- Setup PostgreSQL connection
- Setup SQLAlchemy
- Setup Alembic
- Setup Docker Compose
- Implement auth module
- Implement users module
- Implement cultivation module
- Auto-create cultivation profile after user registration

Definition of Done:
- User can register
- User can login
- User can call GET /users/me
- User can call GET /cultivation/me
- New user starts as Pham Nhan with 0 cultivation power and 100 spirit energy

## Phase 2: Vocabulary Core

Goal:
Allow users to learn vocabulary and gain cultivation power.

Tasks:
- Create vocabulary sets
- Create vocabulary words
- Seed first vocabulary set
- Create quiz endpoint
- Submit answer
- Track correct/wrong answers
- Increase cultivation power on correct answers

## Phase 3: Daily Loop

Goal:
Create daily retention loop.

Tasks:
- Daily mission system
- Streak system
- Spirit energy cost
- Claim daily reward

## Phase 4: Achievements and Titles

Goal:
Allow users to unlock and equip titles.

Tasks:
- Achievement definitions
- User achievement unlock
- Title definitions
- Equip title
- Show title on profile

## Phase 5: Leaderboards

Goal:
Allow competition.

Tasks:
- Top cultivation power
- Top vocabulary progress
- Top streak
- Top newbie
# Architecture

## Current Architecture

The project starts as a Modular Monolith.

There is one backend application, one database, and domain modules inside the codebase.

This allows fast development while keeping boundaries clean for future microservice extraction.

## Future Microservice Candidates

The following modules may become independent services later:

- auth-service
- user-service
- vocabulary-service
- cultivation-service
- quest-service
- achievement-service
- ranking-service
- pk-service
- notification-service

## Module Communication

For MVP, modules communicate through service calls and internal domain events.

Later, internal events can be replaced by a message broker.

## Request Flow Example

User submits vocabulary answer:

1. vocabulary.router receives request
2. vocabulary.service validates answer
3. vocabulary.repository stores answer progress
4. vocabulary.service emits UserAnsweredCorrect event
5. cultivation module increases cultivation power
6. quests module updates daily mission progress
7. achievements module checks unlock conditions
8. rankings module updates score
9. API returns result to frontend
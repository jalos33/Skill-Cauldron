# Backend Architect Skill

Guides developers on best practices for microservices architecture, API versioning strategies, and safe database schema migrations.

## Purpose

Helps developers design scalable, maintainable backend systems and plan safe changes. Whether you're extracting services from a monolith, versioning your APIs, or updating database schemas, this skill provides expert guidance following industry standards.

## Features

- **Microservice Boundary Analysis** - Analyzes current codebase to identify logical service boundaries using Domain-Driven Design principles
- **API Versioning Recommendations** - Suggests optimal versioning strategies (URI, header, query parameter) with implementation examples
- **Safe Database Migrations** - Generates zero-downtime migration plans with rollback support for production deployments
- **DDD & Clean Architecture** - Enforces domain-driven design patterns and clean architecture principles

## How to Use

1. Copy this skill folder to `~/.claude/skills/`
2. Invoke with natural language phrases:

| Phrase | What it does |
|--------|--------------|
| `"Design microservices for this app"` | Analyzes monolith and suggests service decomposition |
| `"Suggest API versioning strategy"` | Recommends URI, header, or query-based versioning |
| `"Plan database migration"` | Creates safe migration scripts with rollback plans |

## Example Usage

```
user: "Design microservices for this monolith e-commerce app"
skill: Backend Architect identifies bounded contexts (Order Service, Inventory Service, Payment Service) and provides a decomposition roadmap.
```

```
user: "Recommend API versioning for /users endpoint"
skill: Analyzes current usage and recommends URI-based versioning with code examples for implementation.
```

```
user: "Create safe migration script for adding user roles table"
skill: Generates zero-downtime migration plan with up/down SQL scripts and deployment steps.
```

## Dependencies

- **None required** - Reads code/files directly from repository

## License

MIT

## Author

Joe Quiñones / MdAlchemy.ai

---

Part of [Skill Cauldron](https://github.com/jalos33/Skill_cauldron-) – Collection of Claude Code Skills

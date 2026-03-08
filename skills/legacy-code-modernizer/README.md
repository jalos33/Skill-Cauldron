# Legacy Code Modernizer Skill

A Claude Code skill for suggesting incremental refactoring paths for old/monolithic codebases, breaking them into modern patterns without risky big-bang rewrites.

## Description

The Legacy Code Modernizer skill helps teams safely migrate legacy systems to modern architectures using proven patterns like Strangler Fig and Branch by Abstraction. Instead of attempting dangerous complete rewrites, it provides phased migration strategies that minimize risk while delivering continuous value.

## Purpose

Legacy codebases present unique challenges:
- Business-critical systems cannot afford extended downtime
- Complete rewrites often fail or exceed budgets dramatically
- Teams need to deliver features while maintaining old systems
- Technical debt accumulates and becomes harder to manage over time

This skill provides a systematic approach to modernization that:
- Reduces risk through incremental changes
- Maintains system availability throughout migration
- Builds team confidence with quick wins
- Enables continuous delivery during transformation

## Features

- **Codebase Analysis**: Scans project structure, dependencies, and code patterns to identify legacy issues
- **Boundary Identification**: Maps natural domain boundaries for extraction using DDD principles
- **Strangler Fig Planning**: Creates gradual replacement strategies while keeping systems running
- **Feature Toggle Integration**: Provides toggle infrastructure for safe incremental rollouts
- **Branch by Abstraction**: Enables swapping implementations without breaking callers
- **Phased Migration Plans**: Outputs detailed phase-by-phase migration with milestones
- **Risk Assessment**: Identifies high-risk areas (god classes, tight coupling, global state)
- **Rollback Procedures**: Includes revert strategies for each migration phase

## How to Use

### Activation Phrases

Use these phrases to invoke the Legacy Code Modernizer skill:
- "Refactor this legacy monolith"
- "Suggest incremental modernization path"
- "Break this old codebase into microservices safely"
- "Modernize legacy Java/.NET codebase"
- "Create Strangler Fig migration plan"

### Usage Examples

```bash
# Refactor a PHP monolith
Refactor this legacy PHP monolith into services

# Get modernization path for Ruby on Rails app
Suggest safe migration path for old Ruby on Rails app

# Create incremental architecture plan
Create incremental plan to move from monolith to clean architecture

# Modernize Java Spring codebase
Modernize this Java Spring legacy codebase
```

## Examples

### Example 1: PHP Monolith to Services

**Input:** Legacy PHP application with mixed concerns, tight coupling between layers.

**Output:** Phased migration plan including:
- Phase 0: Add automated tests, set up CI/CD
- Phase 1: Extract logging/config, add type hints
- Phase 2: Create API gateway, extract billing module first
- Phase 3: Migrate user management, order processing
- Phase 4: Decommission legacy PHP code after 90-day overlap

### Example 2: Java Spring Legacy Modernization

**Input:** Monolithic Spring Boot application with ~500k lines of code.

**Output:** Incremental plan covering:
- Module extraction using Spring Cloud modules
- Feature toggle setup with Spring Cloud Config
- API gateway implementation with Spring Cloud Gateway
- Database per service migration strategy
- Dual-write patterns for data consistency during transition

### Example 3: .NET Legacy System

**Input:** ASP.NET WebForms application with code-behind files.

**Output:** Modernization path including:
- Blazor/SPA frontend extraction first (lowest risk)
- API layer introduction alongside existing pages
- Feature flags to route users between old and new UI
- gradual database schema evolution
- Complete legacy removal after validation period

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/legacy-code-modernizer

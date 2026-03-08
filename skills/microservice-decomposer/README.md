# Microservice Decomposer Skill

A Claude Code skill for analyzing monolithic codebases and suggesting safe, incremental paths to break them into microservices with dependency mapping, bounded contexts, and migration steps.

## Description

The Microservice Decomposer skill provides a systematic approach to migrating from monolithic architectures to microservices. Instead of attempting risky "big bang" rewrites, it applies Domain-Driven Design (DDD) principles to identify natural service boundaries, maps dependencies between modules, and generates phased migration strategies using proven patterns like Strangler Fig and Branch by Abstraction. This reduces migration risk and allows teams to extract services incrementally while maintaining production systems.

## Purpose

Monolith-to-microservices migrations often fail when:
- Teams attempt big-bang rewrites that never complete
- Service boundaries are unclear, leading to distributed monoliths
- Dependencies between modules are not properly mapped before extraction
- No rollback strategy exists if migration encounters issues
- Testing strategies don't cover inter-service communication

This skill addresses these challenges by providing:
- Domain-Driven Design analysis to identify natural bounded contexts
- Dependency mapping (service calls, shared databases, shared libraries)
- Service boundary suggestions with priority scoring
- Phased migration plans using Strangler Fig pattern
- Risk assessment matrices with mitigation strategies
- Testing recommendations including contract tests and chaos engineering

## Features

- **Codebase Analysis**: Scans project structure, imports, database usage, and API endpoints to understand the monolith
- **DDD Bounded Contexts**: Applies Domain-Driven Design principles to discover natural service boundaries based on business capabilities
- **Dependency Mapping**: Identifies coupling patterns including direct method calls, shared database tables, shared libraries, and circular dependencies
- **Service Extraction Criteria**: Calculates priority scores for services based on business value, independence, and coupling penalty
- **Strangler Fig Implementation**: Generates code examples showing how to route traffic gradually from monolith to new services
- **Branch by Abstraction Pattern**: Provides abstraction layer patterns for safe gradual migration with feature toggles
- **Dependency Diagrams**: Outputs text-based or Mermaid diagram code visualizing current and target states
- **Phased Rollout Plans**: Creates detailed week-by-week migration plans with milestones, success criteria, and rollback triggers
- **Testing Recommendations**: Specifies unit tests, contract tests (Pact), integration tests (Testcontainers), and chaos engineering strategies
- **Risk Assessment Matrix**: Documents failure modes with probability, impact, mitigation, and rollback procedures

## How to Use

### Activation Phrases

Use these phrases to invoke the Microservice Decomposer skill:
- "Decompose this monolith into microservices"
- "Suggest microservice boundaries for this app"
- "Plan incremental migration from monolith"
- "Map dependencies and break this codebase"
- "Apply Strangler Fig pattern to this legacy system"

### Usage Examples

```bash
# Decompose an e-commerce application into services
Decompose this monolithic e-commerce app into services

# Get service boundary suggestions for Node.js applications
Suggest microservice boundaries for this Node.js monolith

# Create migration plan for Java Spring Boot applications
Create migration plan for breaking this Java Spring app

# Map dependencies and propose services for Python applications
Map dependencies and propose services for this Python monolith
```

## Examples

### Example 1: E-commerce Application Decomposition

**Input:** "Decompose this monolithic e-commerce app into services"

**Output:** Comprehensive decomposition plan showing:
- Five proposed microservices (User, Catalog, Order, Payment, Shipping) with bounded context mapping
- Dependency diagram identifying critical coupling points (orders table shared across modules)
- Priority scores for each service based on business value and independence
- 38-week phased migration plan with Infrastructure → Parallel Systems → Core Extraction → Data Consistency → Cutover phases
- Contract testing strategy using Pact to prevent API breakage during independent deployments

### Example 2: Node.js Monolith Analysis

**Input:** "Suggest microservice boundaries for this Node.js monolith"

**Output:** Service boundary analysis including:
- Project structure scan identifying controllers, models, routes, and services directories
- Bounded context mapping based on business capabilities (Customer, Catalog, Order domains)
- Database table usage matrix showing which modules share each table
- Recommended extraction order prioritizing read-heavy Catalog service first
- Strangler Fig middleware code example for gradual routing to new services

### Example 3: Java Spring Boot Migration

**Input:** "Create migration plan for breaking this Java Spring app"

**Output:** Detailed migration strategy covering:
- Service layer analysis identifying UserService, ProductService, OrderService, PaymentService
- Branch by Abstraction implementation with interface-based abstraction and feature toggles
- Kubernetes deployment templates for containerized services
- API Gateway routing configuration for traffic splitting
- Rollback script using kubectl commands to restore monolith handling all traffic

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/microservice-decomposer

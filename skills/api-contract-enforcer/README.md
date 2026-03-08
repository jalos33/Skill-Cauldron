# API Contract Enforcer Skill

A Claude Code skill for automatically validating OpenAPI specifications against code implementations and generating client SDKs from valid specs.

## Description

The API Contract Enforcer skill ensures consistency between your API documentation (OpenAPI/Swagger) and actual implementation. It detects contract drift, identifies mismatches between spec and code, and generates type-safe client libraries to prevent frontend-backend divergence.

## Purpose

API contracts often drift over time as developers:
- Add endpoints without updating the OpenAPI spec
- Change response schemas without modifying documentation
- Forget to document error responses or optional parameters
- Maintain separate manual client implementations that fall out of sync

This skill provides automated validation and code generation to:
- Detect specification-to-code mismatches before deployment
- Generate type-safe clients from a single source of truth
- Prevent contract drift through CI/CD integration
- Reduce maintenance burden with auto-generated SDKs

## Features

- **OpenAPI Spec Validation**: Parses and validates OpenAPI 3.0+ JSON/YAML specifications
- **Codebase Analysis**: Extracts routes, handlers, and schemas from Express, FastAPI, Spring Boot, and other frameworks
- **Contract Comparison**: Compares spec paths/methods against actual implementations
- **Schema Mismatch Detection**: Identifies type mismatches between expected and returned data
- **Status Code Validation**: Ensures all promised responses are implemented
- **Client SDK Generation**: Generates TypeScript (fetch/axios), Python, Java, Go clients using openapi-generator
- **Validation Reports**: Outputs detailed reports with errors, warnings, and fix suggestions
- **Cross-Language Support**: Supports Node.js/Express, Python/FastAPI, Java/Spring Boot

## How to Use

### Activation Phrases

Use these phrases to invoke the API Contract Enforcer skill:
- "Validate OpenAPI spec against this code"
- "Check API implementation matches spec"
- "Generate TypeScript client from OpenAPI"
- "Enforce contract on this REST API"
- "Audit OpenAPI compliance in this backend"

### Usage Examples

```bash
# Validate Express routes against OpenAPI spec
Validate openapi.yaml against my Express routes

# Generate Python client SDK
Generate Python client SDK from this spec

# Check endpoint coverage
Check if all endpoints in code match spec

# Find schema mismatches
Find mismatches in request/response schemas
```

## Examples

### Example 1: Validating Express Routes

**Input:** OpenAPI spec and Express.js application code.

**Output:** Validation report showing:
- All endpoints defined in spec have handlers
- Type mismatches (e.g., integer vs string IDs)
- Missing error response definitions
- Suggestions for fixing each issue

### Example 2: Generating TypeScript Client

**Input:** Valid OpenAPI 3.0 specification.

**Output:** Generated client code with:
```typescript
export class UsersApi {
  async getUser(id: string): Promise<User> { ... }
  async createUser(user: UserCreate): Promise<User> { ... }
}
```

### Example 3: Python SDK Generation

**Input:** OpenAPI spec for payment API.

**Output:** Python client with typed methods:
```python
class UsersApi:
    def get_user(self, id: str) -> User: ...
    def create_user(self, user: UserCreate) -> User: ...
```

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/api-contract-enforcer

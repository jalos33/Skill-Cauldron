# GraphQL Schema Builder Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/graphql-schema-builder)

A Claude Code skill that **generates GraphQL schemas (SDL)** from existing REST API endpoints and validates them for correctness and best practices. Automatically converts Express routes, Spring controllers, or other REST implementations into production-ready GraphQL schemas.

## Purpose

This skill bridges the gap between REST and GraphQL by:
- Scanning REST API code to infer proper GraphQL types
- Generating complete SDL (Schema Definition Language) files
- Validating schemas against GraphQL best practices
- Providing actionable improvement suggestions

Whether you're migrating from REST or building a new GraphQL API, this skill ensures your schema is well-structured and follows industry standards.

## Features

- **REST-to-GraphQL Conversion** - Automatically generates types from Express routes, Spring controllers, Django views, etc.
- **Type Inference** - Infers Query, Mutation, Input, Object, and Enum types from API patterns
- **Pagination Support** - Suggests cursor-based or offset-based pagination patterns
- **Validation Report** - Checks syntax, naming conventions, nullability, and descriptions
- **Improvement Suggestions** - Recommends interfaces, unions, deprecation strategies
- **Resolver Stubs** - Generates placeholder functions with proper signatures
- **Language Agnostic** - Works with any REST framework (Express, Spring, Django, FastAPI)

## Features Overview

| Feature | Description |
|---------|-------------|
| **REST Code Analysis** | Parses routes/controllers to extract endpoints and data shapes |
| **Type Inference Engine** | Maps HTTP methods to GraphQL Query/Mutation operations |
| **SDL Generation** | Outputs complete schema.graphql with proper syntax |
| **Pagination Patterns** | Suggests cursor-based (`first/after`) or offset (`limit/offset`) |
| **Validation Checks** | Syntax, naming (camelCase), nullability, descriptions |
| **Improvement Suggestions** | Interfaces, unions, deprecation notices, best practices |

## When to Use

Use this skill whenever you need to create or validate GraphQL schemas:

| Scenario | Command |
|----------|---------|
| Convert REST API to GraphQL | "Generate GraphQL schema from this REST API" |
| Analyze Express routes | "Build schema from Express routes" |
| Validate existing schema | "Validate and improve this GraphQL schema" |
| Spring controller conversion | "Convert REST endpoints to GraphQL for this Spring controller" |
| Add pagination support | "Add cursor-based pagination to this users query" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Generate GraphQL schema from this REST API"
   - "Convert REST endpoints to GraphQL schema"
   - "Build schema from Express routes"
   - "Validate and improve this GraphQL schema"
   - "Create GraphQL types from existing API code"

2. **Provide the REST API code**:
   ```
   Generate GraphQL schema from this Express users router:

   const express = require('express');
   const router = express.Router();
   const { createUser, getUser } = require('../services/userService');

   // GET /api/users - List all users
   router.get('/users', async (req, res) => {
     const users = await User.find().select('-password');
     res.json(users);
   });

   // POST /api/users - Create a new user
   router.post('/users', async (req, res) => {
     const { name, email } = req.body;
     const newUser = await createUser({ name, email });
     res.status(201).json(newUser);
   });

   // GET /api/users/:id - Get user by ID
   router.get('/users/:id', async (req, res) => {
     const user = await User.findById(req.params.id);
     if (!user) return res.status(404).json({ error: 'Not found' });
     res.json(user);
   });
   ```

3. **Receive generated schema and validation report**:
   - Complete `schema.graphql` file with all types
   - Validation report highlighting issues by severity
   - Improvement suggestions for optimization

### Example Workflow

```
User: Generate GraphQL schema from this Express users router

[REST API code provided above]

Skill Output:

# Generated GraphQL Schema

## schema.graphql

"""
User type representing a platform user account
"""
type User {
  id: ID!
  name: String!
  email: String!
  password: String # Consider removing from public response
  createdAt: DateTime!
}

input CreateUserInput {
  name: String!
  email: String!
}

type Query {
  """
  Get all users with pagination support
  """
  users(
    limit: Int = 10
    offset: Int = 0
  ): [User!]!

  """
  Get a specific user by ID
  """
  user(id: ID!): User
}

type Mutation {
  createUser(input: CreateUserInput!): UserPayload!
}

type UserPayload {
  success: Boolean!
  user: User
  errors: [String!]
}

## Validation Report

### Summary
- Types Generated: 6 (User, CreateUserInput, Query, Mutation, UserPayload)
- Fields Total: 10
- Issues Found: 2

### 🟠 High Priority
- Missing description on `CreateUserInput` type

### 🟡 Medium Priority
- Consider adding password validation rules to input type
- Suggest adding authentication middleware documentation

### 🟢 Suggestions
- Add pagination cursor support for large datasets (use `first`, `after`)
- Consider creating `Node` interface: `interface Node { id: ID! }`
- Add `@deprecated` directive if migrating from old API version

## Recommended Actions

1. **Add descriptions** to all types and fields before deployment
2. **Implement pagination** with cursor-based approach for scalability
3. **Consider password field** - should it be excluded from public responses?
4. **Add input validation** using GraphQL scalars or custom validators

---
*Generated by GraphQL Schema Builder Skill v1.0*
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/graphql-schema-builder/graphql-schema-builder.skill \
  -o ~/.claude/skills/graphql-schema-builder.skill && echo "✅ GraphQL Schema Builder installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/graphql-schema-builder.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Generate GraphQL schema from this Express users router" | Generated User type with fields, Query.users with pagination, Mutation.createUser with input type |
| **Test 2** | "Convert REST API endpoints to GraphQL for this Spring controller" | Proper mapping of @GetMapping/@PostMapping to Queries/Mutations, DTO-based types |
| **Test 3** | "Build schema and validate naming for this REST backend" | Complete validation report highlighting camelCase conventions, missing descriptions, nullability issues |

## Severity Badge Legend

| Badge | Level | Meaning | Action Required |
|-------|-------|---------|-----------------|
| 🔴 | CRITICAL | Syntax error or invalid schema structure | Fix before use |
| 🟠 | HIGH | Missing critical documentation or validation | Address before deployment |
| 🟡 | MEDIUM | Best practice violation or optimization opportunity | Improve for production |
| 🟢 | LOW | Minor suggestion or nice-to-have | Optional enhancement |

## Best Practices

- **Use camelCase for fields**: `userName`, not `user_name` (GraphQL convention)
- **Add descriptions to all types/fields**: Improves API documentation and tooling support
- **Prefer nullable fields unless required**: More flexible client behavior
- **Include pagination on list endpoints**: Use cursor-based (`first`, `after`) for scalability or offset-based (`limit`, `offset`) for simplicity
- **Validate with graphql-js**: Run syntax validation before deployment
- **Use proper nullability markers**: `!` for required, nullable without marker
- **Deprecate old fields gracefully**: Use `@deprecated(reason: "...")` directive
- **Document resolver patterns**: Note potential N+1 query issues in comments

## GraphQL Schema Patterns

### Recommended Pagination Styles

**Cursor-based (scalable for large datasets):**
```graphql
type Query {
  users(
    first: Int = 20
    after: String # Cursor from previous page
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Offset-based (simpler for smaller datasets):**
```graphql
type Query {
  users(
    limit: Int = 10
    offset: Int = 0
  ): [User!]!
}
```

### Input Validation Patterns

```graphql
input CreateUserInput {
  """
  User's display name (required, 2-50 characters)
  """
  name: String! @constraint(minLength: 2, maxLength: 50)

  """
  User's email address (required, valid format)
  """
  email: String! @constraint(format: EMAIL)

  """
  Password for new account (required, min 8 characters)
  """
  password: String! @constraint(minLength: 8)
}
```

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [Code Reviewer Skill](../code-reviewer/) - Automated code review with competing agents framework
- [CI/CD Pipeline Auditor](../ci-cd-pipeline-auditor/) - Security audit for GitHub Actions workflows
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)

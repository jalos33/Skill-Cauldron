---
name: graphql-schema-builder
description: Generates GraphQL schema (SDL) from existing REST API endpoints/code and validates it for correctness and best practices.
tags: [graphql, api, schema, codegen, validation]
author: Jose Quiñones
version: 1.0
license: MIT
---

# GraphQL Schema Builder

This skill generates **GraphQL schemas (SDL)** from existing REST API endpoints or code, then validates them for correctness and best practices. It scans Express routes, Spring controllers, or other REST implementations to infer proper GraphQL types and create production-ready schema files.

## Instructions

When activated, follow this step-by-step process:

### Step 1: Scan REST API Code
- **Identify route definitions**: Look for Express `router.get/post/put/delete`, Spring `@GetMapping/@PostMapping`, or similar patterns
- **Extract endpoint paths**: `/users`, `/users/:id`, `/posts`, etc.
- **Analyze request/response bodies**: Parse JSON payloads to infer input/output types
- **Identify authentication requirements**: Look for auth middleware, headers, tokens

### Step 2: Infer GraphQL Types
- **Query types**: Map GET endpoints to Query fields (e.g., `GET /users` → `users: [User!]!`)
- **Mutation types**: Map POST/PUT/DELETE to Mutation fields (e.g., `POST /users` → `createUser(input: CreateUserInput!): UserPayload!`)
- **Object types**: Create type definitions from response bodies (e.g., `{ id, name, email }` → `type User { ... }`)
- **Input types**: Create input types for mutation arguments (e.g., `CreateUserInput { name, email }`)
- **Enum types**: Identify fixed-value fields and create enums

### Step 3: Map Endpoints to Resolvers
- **Generate resolver stubs**: Create placeholder functions with proper signatures
- **Match HTTP methods**: GET→Query operations, POST/PUT/DELETE→Mutations
- **Handle path parameters**: Convert `:id` path params to required arguments
- **Document relationships**: Note foreign keys and nested data requirements

### Step 4: Generate SDL (Schema Definition Language)
- **Output schema.graphql format**: Use standard GraphQL SDL syntax
- **Add type definitions**: Include all inferred objects, inputs, enums
- **Include resolver stubs**: Comment markers showing where to implement logic
- **Generate complete file structure**: Organize types logically

### Step 5: Add Pagination and Filtering
- **Pagination arguments**: Add `limit`, `offset` or `first`, `after` (cursor-based)
- **Filtering support**: Suggest filter objects based on common query patterns
- **Sorting options**: Propose sort fields from API design
- **Default values**: Set reasonable defaults (e.g., limit: 10, offset: 0)

### Step 6: Validate Schema
- **Syntax validation**: Check SDL syntax correctness
- **Naming conventions**: Verify camelCase for fields, PascalCase for types
- **Nullability checks**: Ensure proper `!` usage for required vs nullable fields
- **Description requirements**: Suggest adding descriptions to all types/fields
- **Deprecated fields**: Identify legacy endpoints and suggest deprecation notices

### Step 7: Suggest Improvements
- **Naming suggestions**: Recommend clearer field/type names if needed
- **Descriptive additions**: Propose descriptions for better API documentation
- **Union types**: Suggest unions for polymorphic responses (e.g., `SearchResult = User | Post`)
- **Interface definitions**: Identify common patterns for interfaces (e.g., `Node { id, createdAt }`)
- **Pagination strategy**: Recommend cursor-based vs offset pagination

### Step 8: Output Results
- **schema.graphql file**: Complete SDL output ready to use
- **Validation report**: List of issues found with severity levels
- **Improvement suggestions**: Prioritized recommendations for optimization

## Activation Phrases / When to Use

Use this skill whenever you need to convert REST APIs to GraphQL or validate existing schemas:

- "Generate GraphQL schema from this REST API"
- "Convert REST endpoints to GraphQL schema"
- "Build schema from Express routes"
- "Validate and improve this GraphQL schema"
- "Create GraphQL types from existing API code"
- "Transform Spring controllers to GraphQL"
- "Add pagination to this GraphQL schema"

## Usage Examples

| User Input | Expected Skill Behavior |
|------------|------------------------|
| "Generate GraphQL schema from this Express users router" | Parse Express routes (GET /users, POST /users/:id), infer User type with fields {id, name, email}, generate Query.users and Mutation.createUser with proper input types. |
| "Convert REST API endpoints to GraphQL for this Spring controller" | Analyze Spring @RestController methods, map @GetMapping to Queries, @PostMapping to Mutations, create proper DTO-based input/output types. |
| "Build schema and validate naming for this REST backend" | Generate complete schema with validation report highlighting camelCase violations, missing descriptions, nullability issues, and deprecated endpoints. |
| "Suggest improvements for this partial GraphQL schema" | Review incomplete schema, suggest additional types needed, recommend pagination patterns, propose interfaces/unions for extensibility, identify circular dependencies. |

## How It Works

```
User provides REST API code or existing schema
          │
          ▼
┌───────────────────────┐
│  Step 1: SCAN        │ → Parse routes/controllers
│  (Extract Endpoints) │ → Infer request/response shapes
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 2: INFER       │ → Map to Query/Mutation types
│  (Generate Types)    │ → Create Input/Object/Enum types
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 3: MAP         │ → Generate resolver stubs
│  (Resolver Mapping)  │ → Document relationships
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 4: GENERATE    │ → Output schema.graphql SDL
│  (SDL Generation)    │ → Include pagination/filtering
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 5: VALIDATE    │ → Syntax checking
│  (Validation Report) │ → Naming conventions, nullability
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 6: SUGGEST     │ → Improvement recommendations
│  (Optimization)      │ → Interfaces, unions, pagination
└───────────────────────┘
          │
          ▼
    Output: schema.graphql + validation report
```

## Dependencies

- **No external dependencies required** - analyzes code/text directly using pattern matching
- Optional: `graphql-js` for runtime validation (if available in environment)
- Works with Express.js, Spring Boot, Django REST Framework, FastAPI, or any REST framework

## Best Practices / Notes

- **Use camelCase for fields**: `userName`, not `user_name` (GraphQL convention)
- **Add descriptions to all types/fields**: Improves API documentation and tooling
- **Prefer nullable fields unless required**: More flexible client behavior
- **Include pagination on list endpoints**: Use cursor-based (`first`, `after`) for scalability or offset-based (`limit`, `offset`) for simplicity
- **Validate with graphql-js**: Run syntax validation before deployment
- **Use proper nullability markers**: `!` for required, nullable without marker
- **Deprecate old fields gracefully**: Use `@deprecated(reason: "...")` directive
- **Consider DataLoader patterns**: Note N+1 query risks in resolver comments

## Output Format

The skill outputs two main artifacts:

### 1. schema.graphql File

```graphql
"""
User type representing a platform user account
"""
type User {
  id: ID!
  name: String!
  email: String!
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
```

### 2. Validation Report

```markdown
## Schema Validation Report

### Summary
- Types Generated: 5 (User, CreateUserInput, Query, Mutation, UserPayload)
- Fields Total: 12
- Issues Found: 3

### 🔴 Critical Issues
None

### 🟠 High Priority
- Missing description on `CreateUserInput` type

### 🟡 Medium Priority
- Consider adding `password` field validation in input type
- Suggest adding `updatedAt` timestamp to User type

### 🟢 Suggestions
- Add pagination cursor support for large datasets
- Consider creating `Node` interface for consistent ID handling
```

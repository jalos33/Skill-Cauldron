---
name: api-contract-enforcer
description: Automatically validates OpenAPI specs against code implementations and generates client SDK code from valid specs.
tags: [api, openapi, contract-testing, codegen, validation]
author: Joe Quiñones
version: 1.0
license: MIT
---

## Instructions

You are an API Contract Enforcer expert specializing in validating OpenAPI specifications against code implementations and generating client SDKs from valid specs. Follow these steps to ensure API contracts remain consistent across backend and frontend implementations.

### Step 1: Load and Parse OpenAPI Spec

Load the OpenAPI specification (JSON or YAML format):
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

Validate the spec has:
- `openapi` version 3.0+ (preferred over Swagger 2.0)
- All required paths defined with HTTP methods
- Proper schemas in components section
- Consistent response codes and content types

### Step 2: Analyze Codebase Routes and Handlers

Parse the codebase to identify actual implementations:

**Node.js/Express:**
```javascript
// Look for route definitions
app.get('/users/:id', getUserHandler);
app.post('/users', createUserHandler);
router.put('/items/:itemId', updateItemHandler);
```

Use AST parsing or regex patterns to extract:
- Route paths (including path parameters)
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Handler function names for deeper analysis
- Request validation schemas (Joi, Zod, express-validator)
- Response types and status codes returned

**Python/FastAPI:**
```python
# Look for route decorators
@app.get("/users/{user_id}")
async def get_user(user_id: int): ...

@app.post("/users")
async def create_user(user: UserCreate): ...
```

**Spring Boot (Java):**
```java
// Look for controller annotations
@GetMapping("/users/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) { ... }
```

### Step 3: Validate Request/Response Schemas Match

Compare OpenAPI spec against actual implementations:

**Path Matching:**
- `/users/{id}` in spec should match `app.get('/users/:id')` or `@GetMapping("/users/{id}")`
- Path parameter names must be consistent (or normalized)
- Query parameters, headers, and cookies must align

**Method Validation:**
- Each HTTP method in spec must have a handler in code
- No extra endpoints should exist without spec documentation
- Deprecated endpoints should be marked appropriately

**Schema Comparison:**
```javascript
// Spec expects:
{ "type": "object", "properties": { "name": {"type": "string"} } }

// Handler returns:
res.json({ name: req.body.name, id: user.id }); // Missing type validation!
```

Check for mismatches in:
- Data types (string vs number, boolean vs string)
- Required vs optional fields
- Enum values and constraints
- Array item types

### Step 4: Detect Common Issues

Identify these common problems:

**Missing Endpoints:**
- Spec defines `/admin/settings` but no handler exists
- Path defined without all HTTP methods (e.g., missing OPTIONS)

**Mismatched Types:**
- Spec says `type: integer`, code returns string "123"
- Response schema has `required: true`, handler may return null

**Status Code Gaps:**
- Spec promises 404, but only 500 returned on not found
- Missing error response definitions (400, 401, 403, 429)

**Parameter Issues:**
- Path parameter marked optional in spec but required by handler
- Query parameters missing validation or defaults
- Headers not documented but used in code

### Step 5: Generate Client SDK Code

Generate type-safe client libraries from valid OpenAPI specs:

**TypeScript/JavaScript (using openapi-generator):**
```bash
# Install generator CLI
npm install -g @openapitools/openapi-generator-cli

# Generate TypeScript fetch client
npx @openapitools/openapi-generator-cli generate \
  -i ./openapi.yaml \
  -g typescript-fetch \
  -o ./generated-client

# Or use axios instead of fetch
npx @openapitools/openapi-generator-cli generate \
  -i ./openapi.yaml \
  -g typescript-axios \
  -o ./generated-client
```

**Python SDK:**
```bash
npx @openapitools/openapi-generator-cli generate \
  -i ./openapi.yaml \
  -g python \
  -o ./generated-python-client
```

**Generated Code Structure:**
```typescript
// Generated TypeScript client example
export interface User {
  id: string;
  name: string;
  email: string;
}

export class UsersApi {
  constructor(private readonly basePath = '/api') {}

  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.basePath}/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  }

  async createUser(user: UserCreate): Promise<User> {
    const response = await fetch(`${this.basePath}/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(user)
    });
    return response.json();
  }
}
```

**Custom Template Options:**
- `typescript-fetch` - Modern fetch API client
- `typescript-axios` - Axios-based client with interceptors
- `python-requests` - Python requests library client
- `java-retrofit` - Java Retrofit/OkHttp client
- `go` - Go language client

### Step 6: Output Validation Report

Generate a comprehensive validation report:

```markdown
== API CONTRACT VALIDATION REPORT ==

Spec File: openapi.yaml
Codebase Analyzed: src/routes/, src/controllers/
Validation Time: 2026-03-07T14:30:00Z

=== SUMMARY ===

Overall Status: FAILED (3 errors, 5 warnings)

Passed Checks: 12/18
Missing Endpoints: 2
Type Mismatches: 3
Schema Gaps: 2

=== ERRORS ===

[ERROR] Missing Handler for /admin/settings GET
  - OpenAPI spec defines this endpoint
  - No matching route found in codebase
  - Location: Expected in src/routes/admin.ts

[ERROR] Type Mismatch on POST /users response
  - Spec expects: { "type": "object", "properties": { "id": {"type": "integer"} } }
  - Code returns: string id (e.g., "user_123")
  - Fix: Update spec schema to type: string for id field

[ERROR] Missing Status Code 404 on GET /users/{id}
  - Spec promises 404 response but handler always throws 500
  - Fix: Add conditional return with status 404 when user not found

=== WARNINGS ===

[WARNING] Query parameter 'limit' has no max constraint in spec
  - Code uses Math.min(limit, 100)
  - Suggestion: Add maximum: 100 to query parameter schema

[WARNING] Deprecated endpoint /v1/users still documented
  - Consider removing or marking as deprecated with replacement path

=== RECOMMENDATIONS ===

1. Fix type mismatch on user.id field (HIGH PRIORITY)
2. Add handler for /admin/settings endpoint
3. Implement proper 404 handling for GET /users/{id}
4. Add max constraint to query parameter schemas
5. Consider generating client SDK from updated spec

=== SUGGESTED FIXES ===

// Fix type mismatch in openapi.yaml
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string      # Changed from integer
```

### Step 7: Suggest Fixes and Remediation

Provide actionable suggestions for each issue:

**For Missing Endpoints:**
- "Add route handler in [file path]"
- "Consider if endpoint should exist (remove from spec)"
- "Mark as TODO with implementation deadline"

**For Type Mismatches:**
- "Update schema type to match actual return value"
- "Modify code to return expected type"
- "Document intentional deviation with @openapi-ignore comment"

**For Schema Gaps:**
- "Add missing required fields to request schema"
- "Define error response schemas for 4xx/5xx codes"
- "Include example values in schema documentation"

## Activation phrases / When to use

- "Validate OpenAPI spec against this code"
- "Check API implementation matches spec"
- "Generate TypeScript client from OpenAPI"
- "Enforce contract on this REST API"
- "Audit OpenAPI compliance in this backend"

## Usage Examples

```
Validate openapi.yaml against my Express routes
Generate Python client SDK from this spec
Check if all endpoints in code match spec
Find mismatches in request/response schemas
```

## How it works

1. **Loads OpenAPI spec** (JSON/YAML format, version 3.0+)
2. **Parses codebase** using AST or pattern matching to extract routes, handlers, and schemas
3. **Compares paths, methods, parameters, responses, status codes** between spec and implementation
4. **Generates client code** (TypeScript fetch/axios, Python requests, Java, Go) using openapi-generator templates
5. **Outputs validation report** with passing/failing checks, missing items, and suggestions
6. **Suggests fixes**: "Add missing param X", "Update response schema to match type Y"

## Dependencies

- Node.js or Python runtime (for code generation if using openapi-generator)
- Optional: `@openapitools/openapi-generator-cli` package for SDK generation
- Recommended: ESLint plugin for OpenAPI validation during development

## Best Practices / Notes

- **Prefer OpenAPI 3.0+ spec**: Better support for schemas, security, and documentation than Swagger 2.0
- **Run validation in CI/CD**: Prevent contract drift with automated checks on every PR
- **Use generated client in frontend**: Ensures frontend never drifts from backend API definition
- **Version your OpenAPI specs**: Track changes over time with version control
- **Document error responses**: Include 400, 401, 403, 404, 429, 500 in spec for complete coverage
- **Use component schemas**: Reuse common schemas to reduce duplication and improve consistency
- **Generate server stubs too**: Use openapi-generator to create skeleton controllers from spec

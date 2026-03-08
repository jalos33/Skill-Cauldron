---
name: tdd-workflow
description: Enforces a strict test-first (TDD) development cycle: write failing test before implementation, then make it pass, then refactor.
tags: [tdd, testing, workflow, red-green-refactor]
author: Jose Quiñones
version: 1.0
license: MIT
---

# TDD Workflow Assistant

This skill enforces a strict **test-driven development (TDD)** cycle following the **Red-Green-Refactor** methodology. It ensures tests are written before implementation code, preventing over-engineering and guaranteeing test coverage.

## Instructions

When activated, follow this exact sequence:

### Phase 1: Red (Write Failing Test First)
1. **Generate failing test cases BEFORE any implementation**
2. Tests should be minimal but comprehensive for the feature described
3. Include edge cases based on the user's description
4. Output ONLY test code - no implementation
5. Wait for user confirmation that tests fail before proceeding

### Phase 2: Green (Make Tests Pass)
6. **Refuse to write full implementation until tests are confirmed failing**
7. Once tests confirmed failing, provide MINIMAL implementation to pass all tests
8. No extra features or optimizations in this phase
9. Keep code simple and readable

### Phase 3: Refactor (Improve While Keeping Tests Green)
10. Suggest refactoring improvements while keeping all tests passing
11. Propose cleaner architecture, better naming, or performance optimizations
12. Never break existing tests during refactoring

**CRITICAL RULE:** Always output failing test code FIRST. Do not write implementation until user confirms tests exist and fail.

## Activation Phrases / When to Use

Use this skill whenever the user indicates they want TDD enforced:

- "Follow TDD for this feature"
- "Write test-first code for this function"
- "Enforce TDD workflow on this task"
- "Red-green-refactor this logic"
- "Help me write tests before code"
- "Test-driven development approach"
- "Start with red phase"

## Usage Examples

| User Input | Expected Skill Behavior |
|------------|------------------------|
| "Follow TDD to implement a function that calculates fibonacci" | Phase 1: Output failing test for fibonacci(0)=0, fibonacci(1)=1, fibonacci(5)=5. Wait. Phase 2: Provide minimal implementation. Phase 3: Suggest memoization or iterative approach. |
| "Use test-first approach for this React component" | Phase 1: Write Jest/React Testing Library tests for component rendering and interactions. Wait. Phase 2: Minimal JSX implementation. Phase 3: Suggest custom hooks, prop separation. |
| "Enforce TDD for adding user authentication endpoint" | Phase 1: Write integration tests for login, registration, token validation. Wait. Phase 2: Minimal Express route handlers. Phase 3: Suggest middleware pattern, security headers. |
| "Red-green-refactor this legacy function" | Analyze existing code, write failing regression tests first, then refactor with tests as safety net. |

## How It Works

```
User describes feature or code change
          │
          ▼
┌───────────────────────┐
│  Phase 1: RED        │ → Generate failing test cases
│  (Write Test First)  │ → Output ONLY test code
└───────────────────────┘
          │
          ▼
    User confirms tests exist/fail
          │
          ▼
┌───────────────────────┐
│  Phase 2: GREEN       │ → Minimal implementation to pass
│  (Make It Pass)       │ → No optimizations yet
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Phase 3: REFACTOR    │ → Improve code quality
│  (Improve Safely)     │ → Keep all tests passing
└───────────────────────┘
```

## Dependencies

- **No external dependencies required** - generates test and implementation as text
- Works with any language/framework (user specifies)
- Test framework assumed: Jest/Mocha for JS, pytest for Python, JUnit for Java, etc.

## Best Practices / Notes

- **Always write minimal test to fail first** - don't over-engineer tests upfront
- **Keep tests focused and fast** - one assertion per test where possible
- **Refactor only after green** - never refactor until all tests pass
- **Use clear, descriptive test names** - e.g., `should_return_zero_for_input_zero` not `test1`
- **Test edge cases explicitly** - zero, negative, null, empty strings, boundary values
- **Wait for confirmation between phases** - ensure user sees the red phase first

## Output Format

When activated, clearly label each phase:

```
=== PHASE 1: RED (Write Failing Test) ===

[Your failing test code here]

⚠️  These tests should FAIL. Please confirm they do before proceeding to implementation.

---

=== PHASE 2: GREEN (Make Tests Pass) ===

[Minimal implementation code here]

This implementation passes all tests with minimal changes.

---

=== PHASE 3: REFACTOR (Improve Safely) ===

[Suggested improvements here]

Consider these refactoring options while keeping tests green.
```

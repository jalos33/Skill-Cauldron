# TDD Workflow Assistant Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/tdd-workflow)

A Claude Code skill that enforces **test-driven development (TDD)** following the Red-Green-Refactor methodology. This skill ensures tests are written before implementation code, preventing over-engineering and guaranteeing test coverage for all features.

## Purpose

This skill guides developers through a strict TDD workflow:
1. **Red**: Write failing test cases first
2. **Green**: Implement minimal code to pass tests
3. **Refactor**: Improve code while keeping tests passing

By enforcing this cycle, the skill prevents writing implementation before understanding requirements and ensures every feature has corresponding tests.

## Features

- **Enforces strict TDD order** - refuses to write implementation until tests fail first
- **Clear phase separation** - labels each phase (Red/Green/Refactor) for clarity
- **Edge case coverage** - generates comprehensive test scenarios including edge cases
- **Minimal implementations** - provides lean code in Green phase, no premature optimization
- **Safe refactoring guidance** - suggests improvements while maintaining test safety net
- **Language agnostic** - works with any programming language or framework

## When to Use

Use this skill when you want to:

| Scenario | Command |
|----------|---------|
| Implement a new feature with TDD | "Follow TDD for this feature" |
| Write test-first code | "Write test-first code for this function" |
| Enforce testing discipline | "Enforce TDD workflow on this task" |
| Refactor legacy code safely | "Red-green-refactor this logic" |
| Learn TDD methodology | "Help me write tests before code" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Follow TDD for this feature"
   - "Write test-first code for this function"
   - "Enforce TDD workflow on this task"
   - "Red-green-refactor this logic"

2. **Describe your feature**:
   ```
   Follow TDD to implement a fibonacci function that handles edge cases.
   ```

3. **Review the Red phase output** (failing tests) and confirm they fail

4. **Request implementation** after confirming test failure:
   ```
   Tests confirmed failing, proceed with Green phase.
   ```

5. **Receive minimal implementation** that passes all tests

6. **Ask for refactoring suggestions**:
   ```
   Suggest refactor improvements.
   ```

### Example Workflow

```
User: Follow TDD to implement a fibonacci function

Skill (Phase 1 - RED):
=== PHASE 1: RED (Write Failing Test) ===

describe('fibonacci', () => {
  test('should return 0 for input 0', () => {
    expect(fibonacci(0)).toBe(0);
  });
  test('should return 1 for input 1', () => {
    expect(fibonacci(1)).toBe(1);
  });
  test('should return 5 for input 5', () => {
    expect(fibonacci(5)).toBe(5);
  });
});

⚠️ These tests should FAIL. Please confirm before proceeding.

User: Tests confirmed failing, proceed with Green phase.

Skill (Phase 2 - GREEN):
=== PHASE 2: GREEN (Make Tests Pass) ===

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

This implementation passes all tests with minimal changes.

User: Suggest refactor improvements.

Skill (Phase 3 - REFACTOR):
=== PHASE 3: REFACTOR (Improve Safely) ===

Consider these improvements:

1. **Add input validation**:
   if (!Number.isInteger(n) || n < 0) {
     throw new Error('Input must be a non-negative integer');
   }

2. **Use memoization for performance**:
   const cache = {};
   function fibonacci(n) {
     if (n in cache) return cache[n];
     if (n <= 1) return n;
     cache[n] = fibonacci(n - 1) + fibonacci(n - 2);
     return cache[n];
   }

3. **Iterative approach** (no stack overflow risk):
   function fibonacci(n) {
     if (n <= 1) return n;
     let prev = 0, curr = 1;
     for (let i = 2; i <= n; i++) {
       [prev, curr] = [curr, prev + curr];
     }
     return curr;
   }

All refactoring options keep tests green.
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/tdd-workflow/tdd-workflow.skill \
  -o ~/.claude/skills/tdd-workflow.skill && echo "✅ TDD Workflow Assistant installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/tdd-workflow.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Follow TDD to implement a fibonacci function" | Failing tests for fibonacci(0), fibonacci(1), fibonacci(5) first |
| **Test 2** | "Use test-first approach for this React component" | Jest/RTL tests for component rendering and interactions |
| **Test 3** | "Enforce TDD for adding user authentication endpoint" | Integration tests for login, registration, token validation |

## Best Practices

- **Write minimal tests first** - don't over-engineer test cases upfront
- **Keep tests focused** - one assertion per test where possible
- **Refactor only after green** - never refactor until all tests pass
- **Use descriptive names** - `should_return_zero_for_input_zero` not `test1`
- **Test edge cases explicitly** - zero, negative, null, empty strings

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [CI/CD Pipeline Auditor](../ci-cd-pipeline-auditor/) - Security audit for GitHub Actions workflows
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)

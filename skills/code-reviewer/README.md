# Code Reviewer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/code-reviewer)

A Claude Code skill that performs **automated code reviews** using a **competing agents framework**. Multiple specialized agents analyze code independently and their findings are aggregated into comprehensive, prioritized review reports.

## Purpose

This skill simulates a team of expert reviewers working in parallel:
- 🔒 **Security Agent** - OWASP Top 10 vulnerabilities, injection attacks, secrets exposure
- 🎨 **Style Agent** - Formatting, naming conventions, readability standards
- 🏗️ **Architecture Agent** - SOLID principles, coupling, scalability concerns
- 🐛 **Bug Hunter** - Edge cases, null checks, race conditions, memory leaks

By using competing agents, the skill reduces individual bias and catches issues that single-perspective reviews miss.

## Features

- **Competing Agents Framework** - Four specialized perspectives analyze independently
- **Severity-Based Prioritization** - Issues ranked CRITICAL/HIGH/MEDIUM/LOW with visual badges
- **Evidence-Cited Findings** - Every issue includes exact code excerpts and context
- **Actionable Fix Suggestions** - Each finding comes with corrected code snippets
- **Language Agnostic** - Works with any programming language or framework
- **Structured Markdown Reports** - Clear, readable output ready for PR comments

## Features Overview

| Feature | Description |
|---------|-------------|
| **Competing Agents** | Security, Style, Architecture, and Bug Hunter agents work independently |
| **Severity Badges** | 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW visual indicators |
| **Evidence Citations** | Exact code lines showing the problematic pattern |
| **Fix Suggestions** | Corrected code snippets for each issue |
| **Consensus Tracking** | Shows when multiple agents flag the same issue |
| **Overall Score** | Numerical rating (0-10) summarizing code quality |

## When to Use

Use this skill whenever you need comprehensive code review:

| Scenario | Command |
|----------|---------|
| Review a pull request | "Review this PR" |
| Analyze a code snippet | "Perform code review on this snippet" |
| Security-focused check | "Audit this code for security and style" |
| Full analysis with all perspectives | "Run competing agents on this pull request" |
| Bug detection focus | "Check for bugs and architectural issues" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Review this PR"
   - "Perform code review on this snippet"
   - "Audit this code for security and style"
   - "Run competing agents on this pull request"
   - "Check for bugs and architectural issues"

2. **Provide the code or PR diff** you want reviewed:
   ```
   Review this PR for security vulnerabilities and style issues.

   Here's the diff:
   @@ -1,5 +1,8 @@
   + function getUser(id) {
   +   return db.query(`SELECT * FROM users WHERE id = ${id}`);
   + }
   ```

3. **Receive structured review report** with:
   - Summary statistics and overall score
   - Issues grouped by category (Security, Style, Architecture, Bugs)
   - Severity badges for each finding
   - Evidence excerpts from the code
   - Fix suggestions with corrected snippets
   - Actionable recommendations prioritized by urgency

### Example Workflow

```
User: Review this PR for security vulnerabilities and style issues.

Here's the diff:
@@ -1,5 +1,8 @@
+ function getUser(id) {
+   return db.query(`SELECT * FROM users WHERE id = ${id}`);
+ }

Skill (Code Review Output):

# Code Review Report

## Summary
- Files Reviewed: 1 (src/api/users.js)
- Issues Found: 3 (Critical: 1, High: 1, Medium: 1)
- Overall Score: 5/10 ⚠️ Needs attention

---

## 🔴 Critical Issues

### SQL Injection Vulnerability
**Severity:** CRITICAL | **Agent:** Security Agent + Bug Hunter
**File:** `src/api/users.js` | **Line:** 2

**Evidence:**
```javascript
return db.query(`SELECT * FROM users WHERE id = ${id}`);
                                           ^^^^^^  <-- String interpolation in query
```

**Impact:** Attacker can execute arbitrary SQL queries, potentially exposing all user data or modifying/deleting records.

**Fix:** Use parameterized queries:
```javascript
function getUser(id) {
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
}
```

---

## 🎨 Style Issues

### Missing input validation
**Severity:** HIGH | **Agent:** Bug Hunter
**File:** `src/api/users.js` | **Line:** 1

**Evidence:**
```javascript
function getUser(id) { // No type or null check
```

**Impact:** Invalid inputs can cause database errors or unexpected behavior.

**Fix:** Add input validation:
```javascript
function getUser(id) {
  if (id === undefined || id === null) {
    throw new Error('User ID is required');
  }
  if (!Number.isInteger(id)) {
    throw new Error('User ID must be an integer');
  }
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
}
```

---

## 🏗️ Architectural Concerns

### Direct database access in API handler
**Severity:** MEDIUM | **Agent:** Architecture Agent
**File:** `src/api/users.js`

**Evidence:** Database query directly in route handler violates separation of concerns.

**Recommendation:** Introduce a repository layer for data access abstraction.

---

## Recommended Actions

1. **Immediate:** Fix SQL injection before merging (CRITICAL)
2. **Before Merge:** Add input validation (HIGH)
3. **Post-Merge:** Refactor to use repository pattern (MEDIUM)

**Overall Review Score: 5/10** ⚠️ Needs attention

---

*Generated by Code Reviewer Skill v1.0 (Competing Agents Framework)*
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/code-reviewer/code-reviewer.skill \
  -o ~/.claude/skills/code-reviewer.skill && echo "✅ Code Reviewer installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/code-reviewer.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Review this PR for security vulnerabilities and style issues" | Security-focused report with SQLi, XSS warnings; style violations noted |
| **Test 2** | "Perform code review on this React component" | Analysis of prop drilling, re-renders, error boundaries, accessibility |
| **Test 3** | "Audit this Node.js endpoint for bugs and performance" | Input validation checks, rate limiting, query optimization findings |

## Severity Badge Legend

| Badge | Level | Meaning | Action Required |
|-------|-------|---------|-----------------|
| 🔴 | CRITICAL | Immediate security risk or data loss | Fix before merge |
| 🟠 | HIGH | Significant bug or major violation | Fix before merge |
| 🟡 | MEDIUM | Affects maintainability or quality | Address soon |
| 🟢 | LOW | Minor suggestion or nitpick | Optional improvement |

## Best Practices

- **Competing agents reduce bias** - different perspectives catch more issues
- **Evidence-cited findings** - every issue shows exact code context
- **Prioritize security first** - critical vulnerabilities must be fixed before merge
- **Suggest tests for bugs** - prevent regression after fixes
- **Be constructive in feedback** - explain why something is a problem
- **Balance strictness with pragmatism** - not every style issue blocks PR

## Agent Descriptions

| Agent | Focus Area | What They Check |
|-------|------------|-----------------|
| 🔒 Security Agent | OWASP Top 10, injection attacks | SQLi, XSS, CSRF, hardcoded credentials, path traversal |
| 🎨 Style Agent | Formatting, naming conventions | Consistent indentation, camelCase/snake_case, line length |
| 🏗️ Architecture Agent | SOLID principles, coupling | Single Responsibility, dependency injection, module boundaries |
| 🐛 Bug Hunter | Edge cases, null checks | Null pointer exceptions, unhandled promises, resource leaks |

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [CI/CD Pipeline Auditor](../ci-cd-pipeline-auditor/) - Security audit for GitHub Actions workflows
- [TDD Workflow Assistant](../tdd-workflow/) - Enforces test-driven development cycle
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)

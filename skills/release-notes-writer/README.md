# Release Notes Writer Skill

Automatically generates customer-friendly release notes from git commits, PR descriptions, or issue tracker data.

## Description

The Release Notes Writer skill transforms technical changelog entries into clear, user-focused messaging that highlights value for end users. It categorizes changes by type (features, fixes, improvements), rewrites jargon-heavy commit messages into benefit-driven language, and structures output with professional formatting including emojis for scannability. Ideal for product managers, developers, and customer-facing teams preparing release communications.

## Purpose

Teams often struggle to communicate technical changes in ways that resonate with users. Release notes written by engineers tend to focus on implementation details rather than user benefits. This skill helps by:
- **Categorizing changes**: Automatically groups commits into features, fixes, improvements, and breaking changes
- **Rewriting for users**: Transforms "Implemented Redis caching" into "Faster page loads through smart caching"
- **Structured formatting**: Produces consistent markdown with emoji icons for quick scanning
- **Version recommendations**: Suggests appropriate semantic version bumps based on change types

Ideal for development teams, product managers, DevOps engineers, and customer support preparing release communications.

## Features

- **Multi-source parsing**: Accepts git logs, PR descriptions, issue tracker data, or manual input
- **Smart categorization**: Auto-classifies changes into 6 standard categories (features, fixes, improvements, security, breaking, deprecations)
- **User-friendly translation**: Converts technical jargon into benefit-focused language users understand
- **Visual formatting**: Adds emojis and markdown structure for scannable release notes
- **Version bump recommendations**: Suggests major/minor/patch based on change types following semver guidelines
- **Breaking changes highlighting**: Ensures migration guides and warnings are prominently featured
- **Known issues tracking**: Dedicated section for documenting limitations and workarounds

## How to Use

### Installation

```bash
curl -o skills/release-notes-writer/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/release-notes-writer/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Generate release notes for this version"
- "Write customer-friendly changelog from commits"
- "Create release notes from recent PRs"
- "Draft notes for v1.2.3 release"
- "Summarize changes for users since last release"

### Example Usage

**User**: Generate release notes for v1.2.3 from commits since v1.2.0

**Input**:
```
Recent git log (v1.2.0 to v1.2.3):

commit abc123: feat: add dashboard with real-time metrics
- New analytics dashboard showing live user activity
- Supports custom date ranges and export to CSV

commit def456: fix: resolve checkout payment timeout
- Fixes issue where payments fail after 5 minutes of inactivity
- Extended timeout to 30 minutes

commit ghi789: refactor: optimize database queries for reports
- Reduced query time by 60% through indexing improvements
```

**Skill Response**: Generates release notes with "What's New" section featuring the analytics dashboard, "Bug Fixes" highlighting resolved payment issues, and "Improvements" showcasing faster report generation. Suggests MINOR version bump due to new feature.

---

## Examples

### Example 1: Standard Feature Release

**Input**: "Generate release notes for v2.0.0 from commits since v1.9.0"

**Output Summary:**

```markdown
# 🚀 Release v2.0.0 - Analytics Dashboard (March 2026)

## ✨ What's New

### Real-Time Analytics Dashboard

✨ **Live Activity Monitoring**
- View user actions as they happen with sub-second updates
- Custom date ranges and export to CSV/Excel
- Perfect for operations teams monitoring system health

## 🐛 Bug Fixes

🐛 Fixed payment timeout issue during checkout
- Customers can now take up to 30 minutes without interruption

## ⚡ Improvements

⚡ **Faster Reports** - Report generation is now 60% faster

---
**Version:** 2.0.0 (Major) | **Full Changelog:** [View commits](link)
```

---

### Example 2: Security Patch Release

**Input**: "Draft release notes for security update addressing CVE-2024-5678"

**Output Summary:**

```markdown
# 🚀 Release v1.5.2 - Security Update (March 2026)

## 🔒 Security Updates

🔒 **Updated authentication library to address CVE-2024-5678**
- Fixes potential session hijacking vulnerability
- All users automatically protected on next login
- No action required for standard installations

## 🐛 Bug Fixes

🐛 Fixed edge case in email verification flow
- Resolved issue where some users didn't receive verification emails

---
**Version:** 1.5.2 (Patch) | **Security Advisory:** [Read details](link)
```

---

### Example 3: Major Version with Breaking Changes

**Input**: "Create release notes for v3.0.0 migration"

**Output Summary:**

```markdown
# 🚀 Release v3.0.0 - API Modernization (March 2026)

## ⚠️ Breaking Changes

⚠️ **API Endpoint Renamed**

The legacy `POST /v1/orders` endpoint has been replaced with `POST /v3/transactions`.

**Migration Required:**
1. Update integrations to use new endpoint path
2. Adjust payload format per [migration guide](link)
3. Complete migration before December 31, 2025

## ✨ What's New

✨ **Enhanced Transaction Tracking**
- Real-time status updates for all orders
- Integration with major shipping providers

---
**Version:** 3.0.0 (Major Breaking Change) | **Migration Guide:** [Start here](link)
```

---

## Output Format

The skill generates a structured markdown release note containing:

1. **Release Header**: Version number, release name, date, version type indicator
2. **What's New Section**: User-facing features with benefit descriptions and usage tips
3. **Bug Fixes Section**: Issues resolved from user perspective (what was broken, impact)
4. **Improvements Section**: Performance/UX enhancements with quantified metrics when available
5. **Security Updates Section**: Security patches with required actions clearly stated
6. **Breaking Changes Section**: Prominently featured migration instructions and timelines
7. **Known Issues Section**: Limitations and workarounds for this release
8. **Contributors & Links**: Credit to contributors, links to full changelog and documentation

## Best Practices

### When to Use This Skill

- Preparing GitHub/GitLab release drafts before tagging
- Weekly/monthly product update newsletters
- Internal stakeholder communications about changes
- Customer support knowledge base updates
- Marketing announcements highlighting new capabilities

### Target Output Guidelines

| Element | Recommendation | Why It Matters |
|--------|----------------|---------------|
| **Word Count** | Under 300 words per release | Keeps readers engaged |
| **Sentence Length** | Under 20 words average | Improves readability |
| **Emoji Usage** | Consistent category icons | Enables quick scanning |
| **Breaking Changes** | First section after What's New | Ensures visibility |
| **Links to Docs** | Include for new features | Reduces support burden |

### Writing Style Guidelines

**Use Active Voice:**
- ✅ "You can now export reports to CSV"
- ❌ "Added ability to export reports to CSV"

**Focus on Benefits:**
- ✅ "Faster page loads reduce customer drop-off by 30%"
- ❌ "Implemented Redis caching layer for static assets"

**Quantify Improvements:**
- ✅ "Reports load in under 2 seconds (was ~6s)"
- ❌ "Improved report performance significantly"

### Common Pitfalls to Avoid

1. **Listing commits verbatim**: Always rewrite technical descriptions into user language
2. **Hiding breaking changes**: Feature prominently with clear migration steps
3. **Forgetting known issues**: Document limitations to manage expectations
4. **Using inconsistent emojis**: Pick a style and stick to it across releases
5. **Overpromising**: Only claim improvements you can verify with data

### Version Bump Communication

Always indicate the version bump type clearly:
- Use `(Major)` for breaking changes requiring migration
- Use `(Minor)` for backward-compatible new features
- Use `(Patch)` for bug fixes and security updates only

## Dependencies

- **No external dependencies required** - Works with any text input format
- **Optional**: Git CLI for automated commit extraction
- **Optional**: GitHub/GitLab API integration for PR/issue linking
- **Optional**: Jira/Linear API for enterprise issue tracking integration

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Release notes best practices inspired by Keep a Changelog (keepachangelog.com), Semantic Versioning (semver.org), and GitHub's release documentation.*

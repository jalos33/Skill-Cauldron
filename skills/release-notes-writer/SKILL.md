---
name: release-notes-writer
description: Automatically generates customer-friendly release notes from git commits, PR descriptions, changelog entries, or issue trackers, focusing on user impact, new features, fixes, and improvements.
tags: [release-notes, changelog, communication, product, documentation]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Release Notes Writer Skill

Automatically generates customer-friendly release notes from git commits, PR descriptions, or issue tracker data, transforming technical changes into clear user-focused messaging.

## Instructions

Follow this step-by-step methodology to generate professional release notes:

### Step 1: Collect Change Data

Gather all change information from available sources:

**Data Sources:**
- Git commit history (`git log` since last tag)
- Pull request descriptions and titles
- Issue tracker updates (Jira, GitHub Issues, Linear)
- Manual changelog entries or contributor submissions
- Merge commit messages with conventional commits format

**Key Information to Extract:**
- Commit/PR title and description
- Type of change (feature, fix, refactor, chore, etc.)
- Associated issue/ticket numbers
- Labels/tags applied (bugfix, enhancement, security)
- Author/contributor information
- Links to related PRs or issues

### Step 2: Categorize Changes

Organize changes into standard release categories:

**Category Definitions:**

| Category | Description | Indicators | Emoji |
|----------|-------------|------------|-------|
| **New Features** | User-facing functionality additions | "feat:", "added", "new", "introduced" | ✨ |
| **Bug Fixes** | Resolved issues and error corrections | "fix:", "fixed", "resolved", "bug", "issue" | 🐛 |
| **Improvements** | Non-breaking enhancements to existing features | "improve:", "enhance", "optimize", "refactor" | ⚡ |
| **Security Updates** | Vulnerability fixes and security hardening | "security:", "vulnerability", "CVE-", "patch" | 🔒 |
| **Breaking Changes** | API changes, removed features, incompatible updates | "BREAKING:", "removed", "deprecated", "migration required" | ⚠️ |
| **Deprecations** | Features marked for future removal | "deprecate:", "will be removed in", "use X instead" | 📦 |

**Categorization Rules:**
- Default to most specific category when multiple apply
- Breaking changes always get their own prominent section
- Security patches should be highlighted even if minor
- Internal/refactor work typically excluded unless user-visible

### Step 3: Rewrite for User Impact

Transform technical language into customer-friendly messaging:

**Technical to User-Facing Translation:**

| Technical Term | User-Friendly Equivalent |
|----------------|--------------------------|
| "Implemented Redis caching layer" | "Faster page loads through smart caching" |
| "Refactored authentication module" | "Improved login security and reliability" |
| "Added OAuth 2.0 support" | "Sign in with Google, GitHub, or your SSO provider" |
| "Fixed null pointer exception in checkout" | "Fixed cart abandonment issue during checkout" |
| "Optimized database queries for reports" | "Reports now load 3x faster" |

**Writing Principles:**
- Use active voice: "You can now..." instead of "Added ability to..."
- Focus on benefits, not implementation details
- Quantify improvements where possible ("2x faster", "50% reduction")
- Avoid jargon unless it's product terminology users know
- Keep sentences short (under 20 words when possible)

### Step 4: Structure the Release Notes

Organize output into clear, scannable sections:

**Standard Template:**

```markdown
# [Release Title] - v[version] ([date])

## What's New

✨ [Feature name]
- Brief description of what it does and why it matters
- How users can access or use it
- Link to related documentation if applicable

## Fixes 🐛

🐛 [Issue summary]
- What was broken (from user perspective)
- Impact before fix
- Confirmation that it's resolved

## Improvements ⚡

⚡ [Improvement name]
- What improved and who benefits
- Quantified improvement if available
- Any new options or settings exposed

## Security Updates 🔒

🔒 [Security item]
- Brief description (avoid exposing vulnerability details)
- Action required from users if any

## Breaking Changes ⚠️

⚠️ **Migration Required**

Describe breaking changes prominently with:
- What changed and why
- Migration steps or upgrade instructions
- Timeline for support/deprecation
- Link to migration guide if available

## Known Issues

- Any known limitations or issues in this release
- Workarounds if available
- Expected resolution timeframe

---
**Contributors:** [List of contributors]
**Full Changelog:** [Link to full commit history]
```

### Step 5: Add Visual Elements

Enhance readability with emojis and formatting:

**Emoji Guide:**
| Element | Emoji | Usage |
|---------|-------|-------|
| New Feature | ✨ or 🎉 | Primary features, major additions |
| Bug Fix | 🐛 or 🔧 | Issue resolutions |
| Improvement | ⚡ or 🚀 | Performance, UX enhancements |
| Security | 🔒 or 🛡️ | Security patches |
| Breaking Change | ⚠️ or 💥 | Required actions, migrations |
| Deprecation | 📦 or 👋 | Removed features |
| Documentation | 📝 | Docs updates (minor releases) |

**Formatting Best Practices:**
- Bold key terms and version numbers
- Use bullet points for lists of items
- Include links to related resources
- Keep each item to 1-2 sentences maximum
- Use horizontal rules (`---`) between major sections

### Step 6: Suggest Version Bump

Determine appropriate semantic version based on changes:

**Version Bumping Rules:**

| Change Type | Version Impact | Example |
|-------------|----------------|---------|
| Only bug fixes, improvements | PATCH (1.0.1) | Fixes for existing features |
| New backward-compatible features | MINOR (1.1.0) | New endpoints, UI additions |
| Breaking API changes | MAJOR (2.0.0) | Removed endpoints, schema changes |
| Security patch without user impact | PATCH | CVE fixes, dependency updates |

**Decision Matrix:**
```
IF any breaking changes:
    bump = MAJOR
ELSE IF new features added:
    bump = MINOR
ELSE:
    bump = PATCH
```

### Step 7: Generate Final Output

Create the complete release notes file:

**Output Requirements:**
- File name: `release-notes.md` or follow project convention
- Ready for GitHub Release creation or email distribution
- Include version number and release date
- Link to full changelog or commit history
- Add contributor recognition section

**Quality Checklist:**
- [ ] All changes categorized correctly
- [ ] No technical jargon without explanation
- [ ] User benefits clearly stated
- [ ] Breaking changes prominently featured
- [ ] Version bump recommendation justified
- [ ] Links to documentation included where helpful
- [ ] Known issues documented if any

## Output Format Template

Your response should follow this structure:

```markdown
# 🚀 Release v[version] - [Release Name] ([date])

**Version:** [x.y.z] | **Type:** [Major/Minor/Patch] | **Status:** [Stable/Beta/RC]

---

## ✨ What's New

### [Feature Group or Major Feature Name]

✨ **[Feature Title]**
- Description focused on user benefit
- How to use or access the feature
- Link to docs: [link]

✨ **[Another Feature]**
- Brief description of second new capability

---

## 🐛 Bug Fixes

🐛 Fixed issue where [description from user perspective]
- Impact: [what problem this solved]

🐛 Resolved [another issue] affecting [user scenario]

---

## ⚡ Improvements

⚡ **Faster load times** - Reports now render in under 2 seconds (was ~6s)

⚡ **Better mobile experience** - Optimized for tablets and smaller screens

---

## 🔒 Security Updates

🔒 Updated dependencies to address [CVE or security concern]
- No action required for most users
- Details: [security advisory link if public]

---

## ⚠️ Breaking Changes

⚠️ **API Change: Endpoint renamed**

The `POST /v1/checkout` endpoint has been replaced with `POST /v2/payments`.

**Migration Steps:**
1. Update your integration to use the new endpoint
2. Adjust payload format per [migration guide](link)
3. Test in staging before production rollout

**Support ends:** December 31, 2025

---

## 📋 Known Issues

- Search function may return duplicates when using special characters (working on fix for v1.3.0)
- Export to CSV limited to 10,000 rows per request

---

**Contributors:** @user1, @user2, @user3
**Full Changelog:** [View commits](link) | **Docs:** [Release guide](link)
```

## Activation Phrases / When to Use

Use this skill when the user mentions:
- "Generate release notes for this version"
- "Write customer-friendly changelog from commits"
- "Create release notes from recent PRs"
- "Draft notes for v1.2.3 release"
- "Summarize changes for users since last release"

## Usage Examples

### Example 1: Standard Version Release

**Input**: "Generate release notes for v1.2.3 from commits since v1.2.0"

**Output**: Release notes with new dashboard features in "What's New", authentication fixes under "Bug Fixes", and performance improvements listed separately. Suggests PATCH version bump.

### Example 2: Security Patch Release

**Input**: "Draft release notes for security patch addressing CVE-2024-1234"

**Output**: Focused release notes highlighting the security update, any required actions from users, affected versions, and recommended upgrade path. Minimal other changes mentioned.

### Example 3: Major Version with Breaking Changes

**Input**: "Create release notes for v2.0.0 migration guide"

**Output**: Prominent breaking changes section with detailed migration steps, followed by new features that replace removed functionality, and deprecated APIs with sunset timeline.

## Best Practices / Notes

### When This Skill Adds Value
- Preparing GitHub/GitLab releases before tagging
- Weekly/monthly newsletter updates to users
- Internal stakeholder communications about product changes
- Customer support documentation for recent fixes
- Marketing materials highlighting new capabilities

### Release Note Writing Guidelines

**Do:**
- Write from user perspective ("You can now..." vs "Added...")
- Group related changes under subheadings
- Include links to relevant documentation
- Quantify improvements with metrics
- Acknowledge contributors by name/handle

**Don't:**
- Use technical jargon without explanation
- List commit messages verbatim
- Hide breaking changes in minor sections
- Forget to mention known issues or limitations
- Make claims you can't verify ("fastest ever" without basis)

### Version Bump Communication
Always clearly state the version bump type:
- **Major (x.0.0)**: Breaking changes, significant rework
- **Minor (0.x.0)**: New features, backward compatible
- **Patch (0.0.x)**: Bug fixes, security patches only

### Tone and Style
- Friendly but professional
- Confident without overpromising
- Transparent about limitations
- Action-oriented language
- Consistent emoji usage throughout release

## Dependencies

**Required:**
- None (works with text input or manual data)

**Optional Enhancements:**
- `git` CLI for extracting commit history
- GitHub API integration for PR/issue data
- Jira/Linear API for enterprise issue tracking
- Changelog parser for existing changelog files

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Release notes best practices inspired by Keep a Changelog (keepachangelog.com) and Semantic Versioning (semver.org).*

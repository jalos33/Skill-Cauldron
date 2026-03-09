# RFC Creator Skill

Generate standardized Request for Comment (RFC) documents to ensure stakeholder alignment on technical decisions, architecture changes, or feature proposals.

## Purpose

The RFC Creator skill helps teams document and communicate significant technical changes through a structured format that encourages thorough consideration of alternatives, risks, and implementation details before code is written.

## Features

- **Standardized RFC Template**: Ensures all critical sections are covered consistently
- **Mermaid Diagram Support**: Generates architecture, timeline, and sequence diagrams
- **Review Process Guidance**: Suggests appropriate reviewers and timelines
- **Flexible Status Tracking**: Supports Draft → Active → Approved → Live lifecycle
- **Rollback Planning**: Always includes contingency plans for risky changes

## How to Use

### Installation

```bash
curl -o ~/.claude/skills/rfc-creator.skill \
  https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/rfc-creator/SKILL.md
```

Or manually copy `SKILL.md` contents to your Claude skills directory.

### Activation Phrases

Use any of these phrases to activate the skill:
- "Create RFC for this architecture change"
- "Generate Request for Comment document"
- "Draft RFC for new feature proposal"
- "Standardize RFC for this technical decision"
- "Write RFC for database migration plan"

### Example Usage

After installation, simply ask Claude to create an RFC:

```
Create RFC for migrating from monolith to microservices
```

The skill will generate a complete RFC document with all standard sections.

## Examples

### Monolith to Microservices Migration

**Input:** "Create RFC for migrating from monolith to microservices"

**Output includes:**
- Problem statement about deployment bottlenecks and scaling limitations
- Phased migration strategy (strangler fig pattern)
- Service boundary definitions with ownership models
- Data consistency approach (eventual consistency, sagas)
- Risk mitigation for distributed system complexity
- Rollback plan to revert to monolith if needed

### GraphQL Addition to REST API

**Input:** "Draft RFC for adding GraphQL to existing REST API"

**Output includes:**
- Comparison table of REST vs GraphQL trade-offs
- Schema design with type definitions
- Backward compatibility strategy (dual-running period)
- Deprecation timeline for legacy endpoints
- Tooling and developer experience improvements

### New Authentication System

**Input:** "Generate RFC for new authentication system"

**Output includes:**
- OAuth 2.0 / OIDC implementation details
- Migration path for existing user sessions
- Security considerations (tokens, refresh rotation)
- SSO integration with enterprise identity providers
- Rate limiting and abuse prevention measures

## Output Format

The skill generates an `RFC.md` file with the following structure:

```markdown
# RFC Title

## Summary
Brief overview of the proposal.

## Status
Draft | Active | Approved | Rejected | Live

## Authors
- [Author Name](email)

## Stakeholders
- Team/Person: Role in this RFC

## Problem Statement
What problem are we solving? Why now?

## Proposed Solution
Detailed description of the approach.

## Alternatives Considered
Other options evaluated and why rejected.

## Risks and Mitigations
Potential issues and how to address them.

## Timeline
Key milestones and expected completion dates.

## Implementation Plan
Technical steps, dependencies, effort estimates.

## Testing Strategy
How we'll validate the change.

## Rollback Plan
Steps to revert if things go wrong.

## References
Related documents, RFCs, or research.
```

## Best Practices

### When to Write an RFC

Use this skill for:
- Major architecture changes
- New feature proposals with significant impact
- API design and interface changes
- Database schema migrations
- Security-related changes
- Process improvements affecting multiple teams

### RFC Quality Guidelines

1. **Keep it concise**: Aim for 1–3 pages; link to appendices for deep dives
2. **Be specific about metrics**: Define success criteria quantitatively
3. **Document alternatives**: Always show what you considered and rejected
4. **Include rollback plans**: Every risky change needs a revert strategy
5. **Update status as it progresses**: Keep the RFC current through lifecycle

## License

MIT License - see [SKILL.md](SKILL.md) for full license text.

## Repository

This skill is part of the Skill-Cauldron project: https://github.com/jalos33/Skill-Cauldron

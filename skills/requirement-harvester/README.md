# Requirement Harvester Skill

Extract clear, structured business rules and requirements from raw documents, emails, meeting notes, or user stories.

## Purpose

The Requirement Harvester skill transforms unstructured text inputs into well-organized requirement specifications. It helps product managers, analysts, and developers convert vague stakeholder communications into actionable, testable requirements with proper traceability to source materials.

## Features

- **Entity Extraction**: Identifies actors, actions, conditions, and outcomes from raw text
- **Given-When-Then Formatting**: Converts behavioral rules into testable specifications
- **Multi-Category Organization**: Groups rules by functional, non-functional, data, workflow, and security categories
- **Ambiguity Detection**: Flags vague terms, conflicts, missing details, and edge cases with clarifying questions
- **Traceability Matrix**: Links every requirement back to its source for verification

## How to Use

### Installation

```bash
curl -o ~/.claude/skills/requirement-harvester.skill \
  https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/requirement-harvester/SKILL.md
```

Or manually copy `SKILL.md` contents to your Claude skills directory.

### Activation Phrases

Use any of these phrases to activate the skill:
- "Harvest requirements from this document"
- "Extract business rules from these notes"
- "Turn user stories into structured requirements"
- "Analyze this email for decision logic"
- "Generate rule list from meeting transcript"

### Example Usage

After installation, provide your raw input:

```
Harvest requirements from this product brief PDF

[Attach or paste the document content]
```

The skill will generate a structured report with categorized rules, identified ambiguities, and clarification questions.

## Examples

### Product Brief Analysis

**Input:** "Harvest requirements from this product brief" (containing a 2-page product vision document)

**Output includes:**
- Executive summary of key features identified
- User roles extracted (customers, admins, support staff)
- Functional rules formatted as Given-When-Then scenarios
- Data requirements for customer profiles and order history
- Ambiguities flagged (e.g., "What defines a VIP customer?")
- 8-12 clarification questions for stakeholder review

### Stakeholder Email Thread Analysis

**Input:** "Extract business rules from these stakeholder emails" (thread with VP, engineering lead, design)

**Output includes:**
- Workflow requirements showing approval chains
- Security constraints from compliance discussions
- Data retention policies mentioned in passing
- Contradictions identified between different stakeholders' statements
- Prioritized questions by conflict severity

### Jira Ticket Consolidation

**Input:** "Turn these 15 Jira tickets into structured requirements" (epic with multiple related stories)

**Output includes:**
- Merged requirement set eliminating duplicate rules
- Cross-ticket dependencies mapped
- Conflicting acceptance criteria highlighted for resolution
- Traceability matrix linking consolidated rules to source ticket IDs
- Suggested backlog reorganization based on rule groupings

## Output Format

The skill generates a structured markdown report:

```markdown
# Requirement Harvesting Report

## Source Documents Analyzed
- [List of input documents]

## Executive Summary
[Key findings overview]

## Actors/Users Identified
| Role | Description | Key Actions |
|------|-------------|-------------|

## Business Rules by Category
### Functional Requirements
**R-001:** Given... When... Then...

### Non-Functional Requirements
[Performance targets, reliability SLAs]

### Data Requirements
[Data rules and constraints]

### Workflow Requirements
[Process flows and approvals]

### Security Requirements
[Access control rules]

## Ambiguities & Clarification Questions
| # | Rule Reference | Issue Type | Question | Priority |
|---|----------------|------------|----------|----------|

## Traceability Matrix
| Rule ID | Category | Description | Source Location | Priority |
|---------|----------|-------------|-----------------|----------|

## Recommended Next Steps
[Action items for requirements refinement]
```

## Best Practices

### When to Use This Skill

Use the Requirement Harvester when you have:
- Raw product briefs or vision documents needing structure
- Email threads with scattered requirement discussions
- Meeting notes that need formalization into requirements
- User stories requiring Gherkin-style conversion
- Jira tickets or backlog items needing consolidation
- Stakeholder interviews with unstructured feedback

### Requirement Quality Guidelines

1. **Always list ambiguities**: Never assume clarity; document what needs confirmation
2. **Use consistent formatting**: Stick to Given-When-Then for behavioral rules throughout
3. **Maintain traceability**: Every requirement should link back to source material
4. **Group by feature/module**: Organize logically for implementation teams

### Ambiguity Detection Patterns

| Pattern | Example | Question |
|---------|---------|----------|
| Vague timeline | "Process quickly" | What is acceptable response time? |
| Undefined actor | "The system validates" | Which role performs validation? |
| Missing edge case | "Upload a file" | How handle files >10MB? |
| Contradictory rules | Rule A vs Rule B | Can we reconcile these requirements? |

## License

MIT License - see [SKILL.md](SKILL.md) for full license text.

## Repository

This skill is part of the Skill-Cauldron project: https://github.com/jalos33/Skill-Cauldron

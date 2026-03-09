# Stakeholder Mapper Skill

Generates visual or structured stakeholder relationship maps, influence/power grids, RACI matrices, and engagement strategies from project datasets, documents, or user input.

## Purpose

The Stakeholder Mapper skill helps product managers, project managers, and team leads systematically identify, analyze, and plan engagement with all stakeholders involved in a project or initiative. It transforms scattered stakeholder information into structured maps and actionable communication plans.

## Features

- **Stakeholder Identification**: Extract individuals, roles, teams, and external parties from documents
- **Power/Interest Assessment**: Evaluate authority level, engagement commitment, and influence connections
- **Relationship Mapping**: Document how stakeholders connect (reports to, collaborates, approves, consulted)
- **Power/Interest Grid Generation**: Plot stakeholders on 2x2 matrix with tailored engagement strategies
- **RACI Matrix Creation**: Assign Responsible, Accountable, Consulted, Informed roles for deliverables
- **Engagement Strategy Development**: Tailored communication plans with channels and frequencies
- **Visual Output**: ASCII diagrams or Mermaid syntax for stakeholder relationship maps

## How to Use

### Installation

```bash
curl -o ~/.claude/skills/stakeholder-mapper.skill \
  https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/stakeholder-mapper/SKILL.md
```

Or manually copy `SKILL.md` contents to your Claude skills directory.

### Activation Phrases

Use any of these phrases to activate the skill:
- "Map stakeholders for this project"
- "Generate stakeholder influence grid"
- "Create RACI matrix for this feature"
- "Analyze stakeholder relationships from these notes"
- "Suggest stakeholder engagement plan"

### Example Usage

After installation, specify your project context:

```
Map stakeholders for new payment integration project

[Include details about project scope, teams involved, timeline]
```

The skill will generate a complete stakeholder analysis with power/interest grid, RACI matrix, and engagement strategies.

## Examples

### Payment Integration Project Stakeholder Map

**Input:** "Map stakeholders for new payment integration project"

**Output includes:**
- Stakeholder list: Finance team (budget owners), Legal (compliance review), External processors (Stripe/PayPal contacts), Engineering (integration work), Customer Support (post-launch inquiries)
- Power/Interest grid: CFO and Compliance Officer in "Keep Satisfied" quadrant; Engineering Lead in "Manage Closely"; Customer Support in "Monitor"
- RACI matrix for integration tasks: Development, Testing, Deployment with clear Responsible/Accountable assignments
- Engagement plan: Weekly finance reviews, bi-weekly legal check-ins, monthly engineering syncs

### Feature Launch Power/Interest Grid

**Input:** "Generate power/interest grid for this feature launch"

**Output includes:**
- Complete department assessment: Product, Engineering, Sales, Marketing, Customer Success, Legal
- 2x2 visualization placing each stakeholder group in appropriate quadrant
- Executive sponsor and VP of Product in "Manage Closely" (high power, variable interest)
- End-user representatives in "Monitor" (lower power but high interest as advocates)
- Tailored strategies: executive briefings for high-power groups, user community updates for monitors

### Backend Migration RACI Matrix

**Input:** "Create RACI matrix for backend migration"

**Output includes:**
- Detailed task breakdown: data mapping, API changes, legacy system decommissioning, testing, cutover
- Clear RACI assignments with single Accountable per task (Engineering Director as A for all tasks)
- Consultation paths: Legacy SMEs consulted on data mapping, Security team consulted on access controls
- Communication plan: Downtime notifications to impacted teams 48 hours before cutover
- Risk mitigation: Rollback procedures with clear decision authority

### Meeting Notes Stakeholder Analysis

**Input:** "Analyze stakeholder relationships from recent meeting notes"

**Output includes:**
- Extracted stakeholders from transcript with inferred power/interest based on发言 patterns and decision authority mentioned
- Relationship map showing collaboration chains between product, engineering, and design teams
- Identified influencers: Technical architect who can mobilize engineering support; Marketing lead who drives customer requirements
- Gaps identified: Legal not yet engaged despite compliance concerns raised; recommend scheduling discovery interview

## Output Format

The skill generates a structured markdown report:

```markdown
# Stakeholder Analysis Report: [Project Name]

## Executive Summary
[Brief overview of key stakeholders and engagement approach]

## Identified Stakeholders
| Name/Role | Organization | Power | Interest | Influence | Category |
|-----------|--------------|-------|----------|-----------|----------|
| ... | ... | High/Med/Low | High/Med/Low | High/Med/Low | Internal/External |

## Power/Interest Grid

```mermaid or ASCII diagram showing 2x2 placement of stakeholders```

### Quadrant Assignments

**Keep Satisfied (High Power, High Interest)**
- [Stakeholder names with engagement rationale]

**Manage Closely (High Power, Low Interest)**
- [Stakeholder names with engagement rationale]

**Monitor (Low Power, High Interest)**
- [Stakeholder names with engagement rationale]

**Keep Informed (Low Power, Low Interest)**
- [Stakeholder names with engagement rationale]

## Relationship Map

```mermaid flowchart showing stakeholder connections```

### Key Relationships Documented
- [List of critical dependencies and approval chains]

## RACI Matrix

| Task/Deliverable | Role 1 | Role 2 | Role 3 | Validation |
|------------------|--------|--------|--------|------------|
| ... | R/A/C/I | R/A/C/I | R/A/C/I | Pass/Fail checks |

## Communication Plan

| Stakeholder | Channel | Frequency | Content Focus | Owner |
|-------------|---------|-----------|---------------|-------|
| ... | Email/Meeting/Dashboard | Weekly/Monthly/Quarterly | Progress/Risks/Decisions | [Name] |

## Action Items

1. [Immediate stakeholder engagement activity] - Owner: [Who] - Due: [When]
2. [Follow-up analysis or interview] - Owner: [Who] - Due: [When]
3. [Schedule recurring communication cadence] - Owner: [Who] - Due: [When]

## Validation Checklist

- [ ] All key stakeholders identified (sponsor, customers, regulators if applicable)
- [ ] Power assessments validated with project sponsor
- [ ] Single Accountable assigned per RACI task
- [ ] Engagement frequencies appropriate for quadrant placement
- [ ] Communication channels match stakeholder preferences
```

## Best Practices

### When to Use This Skill

Use the Stakeholder Mapper when you need to:
- Launch a new initiative and identify all involved parties
- Navigate complex organizational politics on cross-functional projects
- Create clear accountability structures through RACI matrices
- Plan communication cadences for diverse stakeholder groups
- Identify potential blockers before they impact project timeline
- Onboard new team members to existing stakeholder landscapes

### Core Principles

1. **Categorize systematically**: Group by internal/external, power/interest to identify patterns early
2. **Validate with sponsor**: Power assessments are subjective; confirm accuracy before finalizing plans
3. **Update continuously**: Stakeholder dynamics shift during project lifecycle; schedule quarterly reviews
4. **Tailor engagement**: One-size-fits-all communication fails; match channels and frequency to preferences

### Power Assessment Tips

- Look for budget authority as primary power indicator
- Observe who gets consulted in decision meetings (reveals informal influence)
- Validate with multiple sources—perceptions of power can vary by department
- Consider both formal organizational authority and informal network power

### RACI Best Practices

- Enforce strict ONE Accountable per task rule to prevent decision paralysis
- Start with defining Accountable first, then assign Responsible
- Minimize Consulted roles (>3 indicates process bottleneck)
- Ensure Informed stakeholders actually want the updates they receive
- Validate RACI with all assigned parties before project kickoff

### Engagement Frequency Guidelines

| Quadrant | Touchpoint Frequency | Best Channels |
|----------|---------------------|---------------|
| Keep Satisfied | Weekly or milestone-based | Steering committee, 1:1s, decision reviews |
| Manage Closely | Monthly or as needed | Quarterly business reviews, escalation points |
| Monitor | Bi-weekly to monthly | Newsletters, user testing, feedback workshops |
| Keep Informed | Quarterly or major milestones | All-hands announcements, broad email updates |

### Common Pitfalls to Avoid

- **Missing key stakeholders**: Conduct discovery interviews early; review org charts and past project post-mortems
- **Misjudging power levels**: Validate with sponsor; observe who gets consulted in decision meetings
- **Too many Accountable roles**: Enforce strict ONE "A" per task rule in RACI validation
- **Generic engagement strategies**: Tailor communication channels and frequency to stakeholder preferences
- **Static stakeholder map**: Schedule quarterly reviews; update after major organizational changes

## License

MIT License - see [SKILL.md](SKILL.md) for full license text.

## Repository

This skill is part of the Skill-Cauldron project: https://github.com/jalos33/Skill-Cauldron

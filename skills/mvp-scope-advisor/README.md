# MVP Scope Advisor Skill

Analyze feature lists and product requirements to define a focused, functional Minimum Viable Product (MVP) scope using established prioritization frameworks.

## Description

The MVP Scope Advisor skill helps product managers trim "nice-to-have" features into a focused, functional MVP release by prioritizing based on user value, effort, risk, and business goals. It applies proven frameworks like MoSCoW, RICE, Value vs. Effort matrices, and Kano Model to systematically classify features and recommend what should (and shouldn't) be included in an MVP launch.

## Purpose

Product development often suffers from scope creep and feature bloat. This skill provides a structured approach to:
- Identify the truly essential features for launch
- Justify prioritization decisions with data-driven frameworks
- Create clear success metrics and failure signals
- Plan phased rollouts beyond the initial MVP
- Validate assumptions before investing in full development

Ideal for product managers, startup founders, and agile teams practicing lean startup methodologies.

## Features

- **Multi-framework analysis**: Applies MoSCoW, RICE, Value vs. Effort, and Kano models for cross-validated decisions
- **Feature classification**: Systematically categorizes features into Must-Have, Should-Have, Could-Have, Won't-Have
- **Constraint validation**: Ensures proposed scope fits within time, budget, and technical limitations
- **Success metrics definition**: Establishes quantitative and qualitative success criteria with failure signals
- **Phased roadmap creation**: Plans MVP v1.0 through v2.0+ with estimated timelines and dependencies
- **Risk assessment**: Identifies critical assumptions to validate and mitigation strategies

## How to Use

### Installation

```bash
curl -o skills/mvp-scope-advisor/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/mvp-scope-advisor/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Scope MVP for this feature set"
- "Trim this product backlog to MVP"
- "Prioritize features for minimum viable product"
- "Help define MVP scope from these ideas"
- "Create MVP plan with must-haves only"

### Example Usage

**User**: Scope MVP for a new task management app

**Skill Response**: Generates comprehensive MVP recommendation including:
- Must-have features (e.g., create/edit/delete tasks, user authentication)
- Excluded features for later (e.g., team collaboration, advanced filtering)
- RICE scores and prioritization matrix
- Success metrics and validation thresholds
- Phased roadmap from v1.0 through v2.0

## Examples

### 1. Task Management App MVP

**Input**: "Scope MVP for a new task management app with features: task creation, due dates, reminders, project organization, tags, team collaboration, file attachments, Gantt charts, time tracking, reporting dashboard"

**MVP Scope Result**:
- **Must-Have (3)**: Task creation/edit/delete, Due dates, User authentication
- **Should-Have (2)**: Reminders, Project organization
- **Could-Have (3)**: Tags, File attachments, Basic reporting
- **Won't-Have**: Team collaboration, Gantt charts, Time tracking

### 2. Fitness Tracking Mobile App MVP

**Input**: "Trim features for a fitness tracking mobile app MVP including workout logging, nutrition tracking, social feed, personal training videos, meal planning, progress photos, wearable integration, coaching chat"

**MVP Scope Result**:
- **Must-Have (3)**: Workout logging, Basic exercise library, User profiles
- **Should-Have (2)**: Progress photos, Basic stats dashboard
- **Could-Have (2)**: Social feed, Nutrition tracking
- **Won't-Have**: Personal training videos, Meal planning, Wearable integration, Coaching chat

### 3. E-commerce Checkout Redesign

**Input**: "Prioritize backlog for e-commerce checkout redesign with features: guest checkout, saved payment methods, address autocomplete, order tracking, gift cards, subscription orders, express shipping options, one-click reorder"

**MVP Scope Result**:
- **Must-Have (4)**: Guest checkout, Address autocomplete, Basic order confirmation, Mobile-responsive design
- **Should-Have (2)**: Saved payment methods, Order tracking page
- **Could-Have (2)**: Gift cards, Express shipping options
- **Won't-Have**: Subscription orders, One-click reorder

### 4. SaaS Analytics Dashboard MVP

**Input**: "Define MVP scope for SaaS analytics dashboard with features: custom reports, data export, real-time metrics, team workspaces, API access, scheduled emails, white-labeling, advanced filtering"

**MVP Scope Result**:
- **Must-Have (3)**: Real-time metrics display, Basic report viewer, User authentication
- **Should-Have (2)**: Advanced filtering, Data export to CSV
- **Could-Have (2)**: Custom reports, Scheduled emails
- **Won't-Have**: Team workspaces, API access, White-labeling

## Output Format

The skill generates a structured markdown report containing:

1. **Executive Summary**: Brief overview of MVP focus and key decisions
2. **Core Analysis**: User problem statement and business objectives
3. **Feature Classification**: MoSCoW counts, RICE scores, Value vs. Effort matrix visualization
4. **Recommended MVP Scope**: Detailed table of must-have features with justifications
5. **Excluded Features**: Should-Have and Could-Have items with deferral rationale
6. **Success Criteria & Metrics**: Quantitative targets and failure signals
7. **Risk Assessment**: Likelihood/impact matrix with mitigation strategies
8. **Phased Roadmap**: MVP v1.0 through v2.0+ timeline with goals and features

See the [SKILL.md](SKILL.md) for complete output format specification.

## Best Practices

### When to Use This Skill
- Early product discovery phase when scope is unclear
- Before sprint planning or roadmap creation
- When stakeholders request too many features for one release
- Need to justify feature prioritization decisions
- Validating lean startup hypotheses

### Core Principles
1. **Focus on the core user problem**: MVP should solve ONE primary pain point exceptionally well
2. **Validate must-haves with real users**: Confirm features address actual user needs through interviews
3. **Keep MVP scope to 3–5 key features**: True minimum viability means stripping away everything non-essential
4. **Include success metrics and failure signals**: Define what "success" looks like quantitatively AND when to pivot or kill the product
5. **Revisit scope after MVP validation**: Use data and feedback to inform v1.1 and beyond

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*This skill follows lean startup principles from "The Lean Startup" by Eric Ries, product management best practices from "Inspired" by Marty Cagan, and agile scope management concepts.*

# AI Prototyping Workflow Skill

Guides a 7-step AI-assisted prototyping process from user journey sketching to interactive mockups, wireframes, and high-fidelity prototypes.

## Purpose

The AI Prototyping Workflow skill helps product designers, UX researchers, and developers create structured, validated prototypes through an iterative process. It transforms vague feature ideas into concrete design plans with user journeys, wireframes, tool recommendations, and validation checklists.

## Features

- **7-Step Structured Process**: Complete workflow from needs gathering to visual polish
- **User Journey Mapping**: Text-based flow diagrams or Mermaid syntax for visualization
- **ASCII Wireframing**: Low-fidelity layouts for rapid iteration before high-fidelity work
- **Tool Recommendations**: Context-aware suggestions (Figma, Framer, React prototypes)
- **Validation Simulation**: Identify friction points and edge cases before development
- **Visual Design Guidance**: Typography, color palettes, animation timings

## How to Use

### Installation

```bash
curl -o ~/.claude/skills/ai-prototyping-workflow.skill \
  https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/ai-prototyping-workflow/SKILL.md
```

Or manually copy `SKILL.md` contents to your Claude skills directory.

### Activation Phrases

Use any of these phrases to activate the skill:
- "Create prototyping workflow for this feature"
- "Guide me through AI-assisted prototyping"
- "Build user journey and mockups for this app"
- "Prototype this UI flow step by step"
- "Generate wireframes and interactive design plan"

### Example Usage

After installation, specify your feature to prototype:

```
Prototype onboarding flow for new users

[Additional context about target audience or specific requirements]
```

The skill will generate a complete 7-step prototyping plan with deliverables at each stage.

## Examples

### Onboarding Flow Prototype

**Input:** "Prototype onboarding flow for new users"

**Output includes:**
- Step 1: User personas (new users, returning users), goals (quick value realization), constraints (mobile-first)
- Step 2: Multi-stage journey map with email verification, profile setup, first action completion
- Step 3: Screen inventory (welcome screen, email input, verification, dashboard preview)
- Step 4: ASCII wireframes for each onboarding step showing layout and key elements
- Step 5: Figma recommendation for collaborative prototyping with user testing mode
- Step 6: Validation checklist (can users complete in under 3 minutes?, clear error states?)
- Step 7: Visual polish guidance (progress indicators, micro-interactions, loading states)

### Dashboard Redesign Wireframes

**Input:** "Create AI-assisted wireframes for dashboard redesign"

**Output includes:**
- Step 1: User goals (quick data insights), pain points (too much information, slow load times)
- Step 2: Primary user journey (login -> view key metrics -> drill into details -> export)
- Step 3: Screen inventory with component library (stats cards, charts, filters, navigation)
- Step 4: Low-fidelity wireframe layouts showing layout options (grid vs list views)
- Step 5: Figma for design collaboration + React prototype for dev handoff
- Step 6: Edge cases addressed (empty states, loading skeletons, data refresh errors)
- Step 7: Typography scale recommendations, color contrast guidelines, animation timing

### Mobile Checkout Process

**Input:** "Guide prototyping for mobile checkout process"

**Output includes:**
- Step 1: Mobile user constraints (small screen, touch interactions), goals (quick purchase completion)
- Step 2: Touch-optimized journey (cart -> shipping info -> payment -> confirmation)
- Step 3: Screen inventory optimized for vertical scrolling and thumb zones
- Step 4: Mobile-specific wireframes with input field sizes, button placement considerations
- Step 5: Framer recommendation for high-fidelity mobile prototypes with animations
- Step 6: Validation against common abandonment points (payment errors, form validation)
- Step 7: Mobile polish guidance (haptic feedback timing, smooth transitions, loading indicators)

## Output Format

The skill generates a complete prototyping plan structured as follows:

```markdown
# Prototyping Plan: [Feature Name]

## Step 1: User Needs and Goals Summary
### Primary Personas
- [Persona name]: Key characteristics
### Core Needs
- [List of user needs]
### Business Objectives
- [Business goals]
### Success Metrics
- [KPIs to measure]

## Step 2: User Journey Map
```mermaid or text-based flow diagram```
### Decision Points
- [Branching paths identified]
### Edge Cases
- [Error states, cancellations]

## Step 3: Screen and Component Inventory
| Screen | Purpose | Key Components | Interactions |
|--------|---------|----------------|--------------|
| ... | ... | ... | ... |

### Reusable Components
- [List of shared components]

## Step 4: Low-Fidelity Wireframes
### Screen S1: [Name]
```ASCII or text description```

### Screen S2: [Name]
...

## Step 5: Tool Recommendations
### Recommended Tools
- [Tool name]: Best for [use case], Learning curve: [level], Export: [options]

### Setup Instructions
[Steps to get started with recommended tools]

## Step 6: Validation Report
### Friction Points Identified
- [Potential issues and solutions]

### Accessibility Considerations
- [A11y requirements and recommendations]

### Edge Case Handling
- [How edge cases should be handled]

## Step 7: Visual Polish Guidance
### Typography Recommendations
- Heading hierarchy, body text sizes

### Color Palette Suggestions
- Primary, secondary, accent colors

### Animation Guidelines
| Type | Duration | Easing |
|------|----------|--------|
| ... | ... | ... |
```

## Best Practices

### When to Use This Skill

Use the AI Prototyping Workflow when you need to:
- Transform vague feature ideas into concrete design plans
- Structure collaborative design discussions
- Create documentation for stakeholder reviews
- Plan UI/UX before committing to high-fidelity designs
- Identify edge cases and accessibility requirements early

### Core Principles

1. **Start with user needs, not UI**: Understand the problem before designing solutions
2. **Use low-fidelity first to iterate fast**: Paper/ASCII wireframes enable quick iteration without attachment to visual details
3. **Include edge cases in journey mapping**: Errors, cancellations, and timeouts are as important as happy paths
4. **Validate assumptions early**: Run usability tests on paper prototypes before investing in high-fidelity designs
5. **Keep prototypes lightweight until validated**: Don't spend weeks perfecting visuals before confirming the concept works

### Tool Selection Guide

| Project Type | Recommended Tools | Rationale |
|--------------|-------------------|-----------|
| Early concept exploration | Figma (free tier) or pen/paper | Fast iteration, easy sharing |
| User testing phase | Figma with prototyping mode | Clickable without dev work |
| Design handoff to team | Figma + component library | Single source of truth |
| Complex interactions | Framer or React prototypes | Animation and logic support |
| Production integration | React prototype first | Reuse components in codebase |

## License

MIT License - see [SKILL.md](SKILL.md) for full license text.

## Repository

This skill is part of the Skill-Cauldron project: https://github.com/jalos33/Skill-Cauldron

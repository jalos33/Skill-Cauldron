---
name: ai-prototyping-workflow
description: Guides a 7-step AI-assisted prototyping process from user journey sketching to interactive mockups, wireframes, and high-fidelity prototypes.
tags: [prototyping, ui-design, user-journey, mockups, product-design]
author: Jose Quiñones
version: 1.0
license: MIT
---

# AI Prototyping Workflow Skill

Guides a 7-step AI-assisted prototyping process from user journey sketching to interactive mockups, wireframes, and high-fidelity prototypes.

## Instructions

Follow this structured 7-step process to create comprehensive prototypes:

### Step 1: Gather User Needs and Goals
- Identify target users and their primary goals
- Clarify business objectives and success metrics
- Document constraints (technical, time, budget)
- Define user personas with key characteristics

**Output:** User requirements summary including:
- Primary user persona(s)
- Core user needs and pain points
- Business goals for the feature/product
- Success metrics (KPIs to measure)

### Step 2: Sketch User Journeys and Flows
- Map out the complete user journey from start to goal completion
- Identify entry points, decision nodes, and exit paths
- Document alternative paths and edge cases
- Visualize flows using text-based diagrams or Mermaid syntax

**Journey Mapping Template:**
```
Start -> [User Action] -> [System Response] -> Decision Point?
  |-> Yes: Continue flow
  |-> No: Handle edge case / error state
```

**Output:** User journey map with:
- Linear flow of user actions
- Decision points and branching paths
- Edge cases (errors, cancellations, timeouts)
- Entry/exit points identified

### Step 3: Define Key Screens and Components
- List all screens required for the complete journey
- Identify reusable components across screens
- Define component hierarchy and relationships
- Note interactive elements per screen (buttons, forms, inputs)

**Screen Inventory:**
| Screen ID | Purpose | Primary Users | Key Components | Interactions |
|-----------|---------|---------------|----------------|--------------|
| S1 | User authentication | New users | Email input, Password field, Login button | Click, Enter key |
| S2 | Dashboard overview | Returning users | Stats cards, Charts, Navigation menu | Hover, Click, Scroll |

**Output:** Screen inventory with:
- Complete list of required screens
- Component breakdown per screen
- Interactive element specifications
- Reusable component identification

### Step 4: Generate Low-Fidelity Wireframes
Create text-based wireframe descriptions for each key screen:

**ASCII Wireframe Format:**
```
+----------------------------------+
|          HEADER BAR              |
| [Logo]        [Navigation]       |
+----------------------------------+
|                                  |
|      PRIMARY CONTENT AREA        |
|                                  |
|  +------------------+            |
|  |                  |            |
|  |   Main Element   |            |
|  |                  |            |
|  +------------------+            |
|                                  |
+----------------------------------+
|          FOOTER BAR              |
+----------------------------------+
```

**Text Description Format:**
For complex layouts, use structured text:
- **Layout**: [Header] Full-width banner with logo left-aligned, navigation right-aligned
- **Main Content**: 3-column grid (sidebar 25%, content 60%, sidebar 15%)
- **Components**: Card component at top (image left, text right), followed by list

**Output:** Wireframe descriptions for each screen including:
- Layout structure and spacing
- Component placement and hierarchy
- Content areas and empty states
- Responsive behavior notes

### Step 5: Suggest Interactive Prototypes
Recommend appropriate tools based on project needs:

| Tool | Best For | Learning Curve | Export Options |
|------|----------|----------------|----------------|
| **Figma** | Collaborative design, handoff to dev | Low-Medium | PNG, SVG, CSS, React components |
| **Framer** | Interactive prototypes with animations | Medium | Web preview, code export |
| **React Prototype** | Production-ready interactive demos | High | Full source code |
| **Adobe XD** | Quick prototyping, voice design | Low | Plugins, sharing links |

**Tool Selection Criteria:**
- Need collaboration? -> Figma
- Complex interactions/animations? -> Framer or React
- Fast iteration needed? -> Figma or Adobe XD
- Production integration? -> React prototype

**Output:** Tool recommendation with:
- Recommended platform(s) based on requirements
- Setup instructions for chosen tool(s)
- Component library suggestions
- Collaboration workflow recommendations

### Step 6: Validate with User Feedback Simulation
Simulate potential user feedback and identify issues:

**Validation Checklist:**
- [ ] Is the primary goal achievable in under 3 clicks?
- [ ] Are error states clear and recoverable?
- [ ] Does the flow handle edge cases gracefully?
- [ ] Is accessibility considered (keyboard navigation, screen readers)?
- [ ] Do labels and instructions match user mental models?

**Potential Issues to Flag:**
- Confusing navigation patterns
- Unclear call-to-action hierarchy
- Missing empty states or error messages
- Inconsistent interaction patterns
- Accessibility gaps

**Output:** Validation report with:
- Identified potential friction points
- Suggested improvements for clarity
- Accessibility considerations
- Edge case handling recommendations

### Step 7: Iterate and Refine with Visual Polish
Provide guidance on visual enhancement and animations:

**Visual Polish Checklist:**
- Typography scale (heading hierarchy, body text sizes)
- Color palette (primary, secondary, accent colors)
- Spacing system (consistent margins, padding)
- Iconography style and sizing
- Loading states and transitions

**Animation Guidelines:**
| Animation Type | Purpose | Duration | Easing |
|----------------|---------|----------|--------|
| Page transition | Context preservation | 300-500ms | ease-in-out |
| Button hover | Feedback on interaction | 150-200ms | ease-out |
| Modal open | Focus indication | 250-350ms | cubic-bezier(0.4, 0, 0.2, 1) |
| Loading skeleton | Perceived performance | N/A (static) | N/A |

**Output:** Visual design guidance with:
- Typography recommendations
- Color palette suggestions
- Animation timing guidelines
- Progressive enhancement opportunities

## Activation phrases / When to use
Use this skill when you need to:
- Create prototyping workflow for this feature
- Guide me through AI-assisted prototyping
- Build user journey and mockups for this app
- Prototype this UI flow step by step
- Generate wireframes and interactive design plan

## Usage Examples

| Input | Expected Output |
|-------|-----------------|
| "Prototype onboarding flow for new users" | Complete 7-step workflow with user personas, multi-stage journey map, welcome screens wireframes, email verification flow, tool recommendations for Figma prototypes, accessibility validation checklist, and progressive enhancement suggestions |
| "Create AI-assisted wireframes for dashboard redesign" | Dashboard screen inventory, low-fidelity wireframe layouts (stats cards, charts, navigation), component hierarchy definitions, responsive behavior notes, recommended tools (Figma for collaboration), edge case handling (empty states, loading states), and visual polish guidance |
| "Guide prototyping for mobile checkout process" | Mobile-specific user journey (cart -> checkout -> payment -> confirmation), screen-by-screen wireframes with touch interactions, payment integration considerations, error handling flows, Framer recommendations for high-fidelity prototypes, validation against common checkout abandonment points |
| "Build interactive mockups for e-commerce product page" | Product detail page workflow, variant selection flow, add-to-cart animations, related products section layout, inventory status indicators, tool recommendations for code-based prototypes with React component libraries |

## How it works

```
┌─────────────────────────────────────────────────────────────────┐
│                  AI-ASSISTED PROTOTYPING WORKFLOW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STEP 1: GATHER NEEDS & GOALS                                   │
│  ┌───────────────┐                                              │
│  │ User Goals    │ -> Personas, Needs, Objectives              │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 2: SKETCH USER JOURNEYS                                   │
│  ┌───────────────┐                                              │
│  │ Journey Maps  │ -> Flow diagrams, Decision points          │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 3: DEFINE SCREENS & COMPONENTS                            │
│  ┌───────────────┐                                              │
│  │ Screen List   │ -> Inventory, Components, Interactions     │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 4: GENERATE WIREFRAMES                                    │
│  ┌───────────────┐                                              │
│  │ Wireframes    │ -> ASCII/text layouts, Component placement |
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 5: SUGGEST INTERACTIVE TOOLS                              │
│  ┌───────────────┐                                              │
│  │ Tool Recs     │ -> Figma/Framer/React, Setup guides         │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 6: VALIDATE FEEDBACK                                      │
│  ┌───────────────┐                                              │
│  │ Validation    │ -> Friction points, Edge cases, A11y       │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 7: ITERATE & REFINE                                       │
│  ┌───────────────┐                                              │
│  │ Visual Polish | -> Typography, Colors, Animations          │
│  └───────────────┘                                              │
│                                                                 │
│  OUTPUT: Complete prototyping plan with all deliverables       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Step-by-step process:**
1. **Gather user needs and goals**: Clarify personas, constraints, success metrics
2. **Sketch user journeys**: Map flows using text diagrams or Mermaid syntax
3. **Define screens and components**: Inventory all required screens with interactions
4. **Generate low-fidelity wireframes**: ASCII layouts or detailed text descriptions
5. **Suggest interactive prototypes**: Tool recommendations based on project needs
6. **Validate with user feedback simulation**: Identify friction points, edge cases, accessibility gaps
7. **Iterate and refine**: Visual polish guidance including typography, colors, animations

## Dependencies
- None required (text-based planning)
- Optional: Mermaid for diagrams, Figma/Framer API for export

## Best Practices / Notes

### Prototyping Principles
- **Start with user needs, not UI**: Understand the problem before designing solutions
- **Use low-fidelity first to iterate fast**: Paper/ASCII wireframes enable quick iteration without attachment to visual details
- **Include edge cases in journey mapping**: Errors, cancellations, and timeouts are as important as happy paths
- **Validate assumptions early**: Run usability tests on paper prototypes before investing in high-fidelity designs
- **Keep prototypes lightweight until validated**: Don't spend weeks perfecting visuals before confirming the concept works

### Wireframe Best Practices
- Use consistent component naming across all wireframes
- Document empty states and error conditions explicitly
- Note responsive behavior for each screen breakpoint
- Include loading states for data-dependent components

### Tool Selection Guidelines
| Project Type | Recommended Tools | Rationale |
|--------------|-------------------|-----------|
| Early concept exploration | Figma (free tier) or pen/paper | Fast iteration, easy sharing |
| User testing phase | Figma with prototyping mode | Clickable without dev work |
| Design handoff to team | Figma + component library | Single source of truth |
| Complex interactions | Framer or React prototypes | Animation and logic support |
| Production integration | React prototype first | Reuse components in codebase |

### Accessibility Considerations
- Ensure keyboard navigability for all interactive elements
- Provide sufficient color contrast (WCAG AA minimum)
- Include text alternatives for non-text content
- Test with screen reader simulation where possible

### Iteration Triggers
Know when to iterate based on:
- User testing reveals confusion at specific steps
- Stakeholder feedback indicates misaligned expectations
- Technical constraints require design adjustments
- Analytics show drop-off points in current flows
- Accessibility audit identifies barriers

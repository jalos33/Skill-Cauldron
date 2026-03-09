---
name: brainstormer
description: Uses iterative, structured questioning to turn vague ideas into fully formed concepts, features, designs, or solutions.
tags: [brainstorming, ideation, creativity, product-design, problem-solving]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Brainstormer Skill

Uses iterative, structured questioning to turn vague ideas into fully formed concepts, features, designs, or solutions.

## Instructions

Follow this structured brainstorming process to transform vague ideas into actionable concepts:

### Step 1: Clarify the Starting Point with Open-Ended Questions
Begin by gathering context through targeted questions:

**Core Clarification Questions:**
- What problem are we trying to solve? (Define the pain point)
- Who is this for? (Identify target users/customers)
- What are our goals and success criteria? (Define what "good" looks like)
- What constraints do we have? (Time, budget, technology, team capacity)

**Output:** Clarified problem statement with:
- Problem definition
- Target audience/personas
- Success metrics/objectives
- Known constraints

### Step 2: Apply Root Cause Analysis (5 Whys Technique)
Dig deeper to understand underlying causes before jumping to solutions:

**5 Whys Process:**
1. Ask "Why is this a problem?" -> Answer
2. Ask "Why does that happen?" -> Answer
3. Continue for 5 iterations or until root cause identified
4. Document each layer of the problem hierarchy

**Example:**
- Why are users dropping off during onboarding? -> Too many steps
- Why too many steps? -> We collect all data upfront
- Why collect all data? -> Fear of missing required fields later
- Why fear missing fields? -> Can't proceed without complete profile
- **Root cause**: System requires complete profile before any value is delivered

**Output:** Root cause analysis revealing underlying issues to address

### Step 3: Explore Multiple Perspectives (Six Thinking Hats)
Examine the idea from different angles to ensure comprehensive thinking:

| Hat | Color | Perspective | Questions to Ask |
|-----|-------|-------------|------------------|
| **Facts** | White | Objective data | What do we know? What information is missing? |
| **Emotions** | Red | Feelings/intuition | How does this make users feel? What's our gut reaction? |
| **Caution** | Black | Risks/concerns | What could go wrong? What are the risks? |
| **Benefits** | Yellow | Positives/benefits | What value does this create? Why will it succeed? |
| **Creativity** | Green | New ideas/alternatives | What else is possible? How can we improve this? |
| **Process** | Blue | Next steps/control | What should we do next? How do we proceed? |

**Output:** Multi-perspective analysis with insights from each "hat"

### Step 4: Generate Divergent Ideas (SCAMPER Technique)
Use SCAMPER to systematically explore variations and new possibilities:

| Letter | Action | Prompt Examples |
|--------|--------|-----------------|
| **S** | Substitute | What can we substitute? (materials, people, processes) |
| **C** | Combine | What can we combine? (features, functions, audiences) |
| **A** | Adapt | What else is similar? What can we adapt from other domains? |
| **M** | Modify/Magnify | What to modify? Magnify? (exaggerate, add features) |
| **P** | Put to another use | Can this be used differently? For other audiences? |
| **E** | Eliminate/Reduce | What can we eliminate? Reduce? Simplify? |
| **R** | Reverse/Rearrange | What if we reverse the order? Rearrange components? |

**Divergence Rules:**
- Aim for quantity first (target 10+ ideas minimum)
- Defer judgment during generation phase
- Build on others' ideas ("Yes, and...")
- Encourage wild/unconventional concepts
- No idea is too far-fetched at this stage

**Output:** List of 10+ diverse ideas exploring the solution space

### Step 5: Converge on Best Options
Evaluate and narrow down ideas using structured criteria:

**Idea Scoring Matrix:**
Score each idea (1-5) on these dimensions:

| Idea | Impact | Feasibility | Innovation | User Value | Total | Rank |
|------|--------|-------------|------------|------------|-------|------|
| Idea A | 4 | 3 | 5 | 4 | 16 | 2 |
| Idea B | 5 | 5 | 3 | 5 | 18 | 1 |

**Scoring Criteria:**
- **Impact**: How much will this solve the problem? (1=minor, 5=major)
- **Feasibility**: How easy is it to implement? (1=very hard, 5=easy)
- **Innovation**: How novel/distinctive is this approach? (1=commoditized, 5=groundbreaking)
- **User Value**: How much will users appreciate this? (1=minimal, 5=must-have)

**Output:** Ranked list of ideas with scoring rationale

### Step 6: Refine Selected Concepts with Pros/Cons Analysis
Deep-dive into top 2-3 concepts for final selection:

**Pros and Cons Template:**
```
Selected Concept: [Name]

PROS:
- [Benefit or advantage 1]
- [Benefit or advantage 2]
- [Benefit or advantage 3]

CONS:
- [Drawback or concern 1]
- [Drawback or concern 2]
- [Drawback or concern 3]

MITIGATIONS FOR CONS:
- For drawback 1: [How to address]
- For drawback 2: [How to address]
```

**Feasibility Assessment:**
- Technical feasibility (can we build it?)
- Resource requirements (team, budget, time)
- Dependencies and blockers
- Risk level (low/medium/high)

**Output:** Refined concept analysis with mitigation strategies

### Step 7: Define Next Steps and Action Plan
Translate selected concept into actionable items:

**Action Planning Template:**
```
Selected Concept: [Name]
Decision: [Proceed / Defer / Kill]

NEXT STEPS:
1. [Immediate action item] - Owner: [Who] - Due: [When]
2. [Follow-up action item] - Owner: [Who] - Due: [When]
3. [Next phase action item] - Owner: [Who] - Due: [When]

RESOURCES NEEDED:
- [People/Resources required]
- [Budget considerations]
- [Tools/Technology needed]

SUCCESS CRITERIA:
- How will we know this worked?
- What metrics will we track?
- When do we review progress?
```

**Output:** Concrete action plan with owners, timelines, and success criteria

## Activation phrases / When to use
Use this skill when you need to:
- Brainstorm ideas for this feature
- Help me think through this concept
- Turn this vague idea into a solid plan
- Run a brainstorming session on this problem
- Generate and refine ideas for this product

## Usage Examples

| Input | Expected Output |
|-------|-----------------|
| "Brainstorm ideas for a new mobile app onboarding experience" | Clarified problem (user drop-off, confusion), 5 Whys analysis of root causes, 12+ divergent ideas via SCAMPER, multi-perspective Six Hats analysis, scored concepts ranked by impact/feasibility, selected concept with mitigation strategies, action plan for prototype testing |
| "Help me think through a pricing model for a SaaS tool" | Problem definition (pricing confusion, conversion friction), customer segmentation analysis, 5 Whys on why current model fails, SCAMPER variations (freemium, tiered, usage-based, flat-rate), Six Hats analysis of each approach, scored pricing models with pros/cons, recommended model with implementation roadmap |
| "Turn 'better task management' into a concrete feature set" | Vague idea clarification (what's "better"? speed? clarity? collaboration?), user personas (individual users vs teams), 15+ feature ideas via SCAMPER, impact/feasibility matrix, top concepts refined with pros/cons, selected feature set prioritized by user value and implementation effort, phased rollout plan |
| "Run brainstorming on improving developer productivity" | Root cause analysis of productivity blockers, multi-perspective views (developers, managers, QA), 20+ improvement ideas across tools, processes, culture, scored concepts focusing on highest-impact changes, selected initiatives with success metrics and pilot program design |

## How it works

```
┌─────────────────────────────────────────────────────────────────┐
│                        BRAINSTORMING WORKFLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STEP 1: CLARIFY STARTING POINT                                 │
│  ┌───────────────┐                                              │
│  │ Open Questions│ -> Problem, Users, Goals, Constraints       │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 2: ROOT CAUSE ANALYSIS (5 Whys)                           │
│  ┌───────────────┐                                              │
│  │ Deep Dive     │ -> Root causes, Problem layers              │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 3: MULTI-PERSPECTIVE (Six Hats)                           │
│  ┌───────────────┐                                              │
│  │ Multiple Views│ -> Facts, Emotions, Risks, Benefits         │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 4: DIVERGENT IDEATION (SCAMPER)                           │
│  ┌───────────────┐                                              │
│  │ 10+ Ideas     │ -> Substitute, Combine, Adapt, Modify       │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 5: CONVERGENCE (Scoring)                                  │
│  ┌───────────────┐                                              │
│  │ Rank Ideas    │ -> Impact, Feasibility, Innovation scores   │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 6: REFINE SELECTED (Pros/Cons)                            │
│  ┌───────────────┐                                              │
│  │ Deep Analysis │ -> Top concepts, Mitigations                │
│  └───────────────┘                                              │
│           ▼                                                      │
│  STEP 7: ACTION PLAN                                            │
│  ┌───────────────┐                                              │
│  │ Next Steps    │ -> Owners, Timeline, Success metrics        │
│  └───────────────┘                                              │
│                                                                 │
│  OUTPUT: Structured brainstorm report with selected concept   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Step-by-step process:**
1. **Clarify starting point**: Ask open-ended questions about problem, users, goals, constraints
2. **Apply root cause analysis (5 Whys)**: Dig deeper to understand underlying issues
3. **Explore multiple perspectives (Six Thinking Hats)**: Analyze from facts, emotions, risks, benefits, creativity, process angles
4. **Generate divergent ideas (SCAMPER)**: Produce 10+ varied concepts using systematic modification techniques
5. **Converge on best options**: Score and rank ideas by impact, feasibility, innovation, user value
6. **Refine selected concepts**: Deep-dive analysis of top 2-3 with pros/cons and mitigation strategies
7. **Define next steps**: Concrete action plan with owners, timelines, success criteria

## Dependencies
- None required (text-based ideation)

## Best Practices / Notes

### Brainstorming Principles
- **Encourage quantity before quality in divergence phase**: Wild ideas often contain seeds of breakthrough solutions; filter later
- **Use diverse perspectives (user, technical, business)**: Six Hats ensures comprehensive analysis beyond initial assumptions
- **Always end with actionable next steps**: Ideas without execution plans remain theoretical; define clear owners and timelines
- **Iterate if user provides feedback**: Brainstorming is iterative; refine based on new information or stakeholder input

### Technique Selection Guide
| Situation | Recommended Techniques | Rationale |
|-----------|----------------------|-----------|
| Problem unclear | Start with 5 Whys | Uncovers root cause before solutions |
| Stuck in same ideas | SCAMPER forces variation | Systematic modification breaks patterns |
| Need buy-in from stakeholders | Six Hats ensures all views heard | Addresses concerns proactively |
| Many ideas, need to prioritize | Impact/Feasibility scoring | Data-driven selection criteria |
| Ready to decide on approach | Pros/Cons + Mitigations | Informed decision with risk management |

### Idea Scoring Tips
- Score collaboratively when possible (group calibration)
- Use relative scoring (compare ideas against each other)
- Weight scores if certain dimensions matter more (e.g., feasibility > innovation for MVP)
- Document rationale for scores to enable debate and refinement

### Common Pitfalls to Avoid
| Pitfall | Why It's Bad | How to Avoid |
|---------|--------------|--------------|
| Early judgment kills creativity | Team self-censors wild ideas | Explicitly defer judgment during divergence |
| Focusing on symptoms not root causes | Solves wrong problem | Always do 5 Whys before ideating |
| Too few ideas generated | Limited solution space | Set minimum idea target (10+) |
| No clear selection criteria | Decisions based on opinions | Use standardized scoring matrix |
| Ideas without owners | Nothing gets done | Every action item needs owner and deadline |

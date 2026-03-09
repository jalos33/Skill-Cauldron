---
name: mvp-scope-advisor
description: Helps product managers trim "nice-to-have" features into a focused, functional MVP release by prioritizing based on user value, effort, risk, and business goals.
tags: [mvp, product-management, scoping, prioritization, lean-startup]
author: Jose Quiñones
version: 1.0
license: MIT
---

# MVP Scope Advisor Skill

This skill helps product managers trim "nice-to-have" features into a focused, functional MVP (Minimum Viable Product) release by applying established prioritization frameworks and focusing on core user value.

## Instructions

Follow this systematic approach to scope an MVP from a feature list:

### Step 1: Extract Core Elements

Parse the input to identify:
- **Feature List**: All requested features, capabilities, and functionalities
- **User Stories**: Descriptions of how users will interact with each feature
- **Business Goals**: Strategic objectives (revenue, growth, validation, market entry)
- **Constraints**: Time limits, budget caps, technical limitations, resource availability
- **Target Users**: Primary user segments and their pain points
- **Success Metrics**: How MVP success will be measured

### Step 2: Apply Prioritization Frameworks

Apply multiple frameworks to cross-validate decisions:

**MoSCoW Method:**
- **MUST HAVE**: Critical for launch; product unusable without it
- **SHOULD HAVE**: Important but not vital; can wait until later
- **COULD HAVE**: Desirable but less impactful; nice-to-have
- **WON'T HAVE (for now)**: Explicitly excluded from current scope

**RICE Scoring:**
- **Reach**: How many users will this affect in a given period?
- **Impact**: How much will it improve the core metric? (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal)
- **Confidence**: How certain are you about your estimates? (100% = high confidence, 80% = medium, 50% = low)
- **Effort**: Person-weeks required to build and launch
- **RICE Score** = (Reach × Impact × Confidence) / Effort

**Value vs. Effort Matrix:**
- Plot each feature on a 2x2 matrix:
  - **Quick Wins** (High Value, Low Effort): Prioritize immediately
  - **Major Projects** (High Value, High Effort): Plan carefully
  - **Fill-ins** (Low Value, Low Effort): Do when time permits
  - **Time Wasters** (Low Value, High Effort): Eliminate

**Kano Model Analysis:**
- **Basic Needs**: Expected features; satisfaction baseline
- **Performance Features**: More = better; competitive differentiators
- **Delighters**: Unexpected features that create excitement
- MVP should focus on Basic + essential Performance features

### Step 3: Classify Each Feature

Assign each feature to a category with justification:

| Category | Criteria | Examples |
|----------|----------|----------|
| **Must-Have** | Core value proposition; product fails without it | User authentication, core task creation in task app |
| **Should-Have** | Important but not launch-critical | Advanced search, notifications |
| **Could-Have** | Nice-to-have with low impact | Dark mode, custom themes |
| **Won't-Have** | Out of scope for MVP; deferred to later | API access, team collaboration features |

### Step 4: Validate Against Constraints

Cross-check proposed MVP scope against:
- **Time**: Can this be built in the available timeframe?
- **Budget**: Does cost align with budget constraints?
- **Technical Feasibility**: Do we have the skills/architecture to build it?
- **Risk**: What could go wrong and how do we mitigate?

### Step 5: Generate MVP Scope Recommendation

Create a focused scope that:
- Addresses the core user problem directly
- Contains 3–5 key features maximum for true minimum viability
- Delivers measurable value to early adopters
- Enables learning and validation of business hypotheses

Include justification for each must-have feature explaining why it's essential.

### Step 6: Define Success Criteria

Establish clear metrics for MVP success/failure:
- **Quantitative Metrics**: User signups, activation rate, retention, revenue targets
- **Qualitative Feedback**: User interviews, satisfaction scores, NPS
- **Failure Signals**: When to pivot or kill the product (e.g., <10% activation after 500 signups)

### Step 7: Suggest Phased Rollout Plan

Create a roadmap beyond MVP:

**MVP v1.0**: Core features only for launch
**v1.1-v1.x**: Should-have features based on MVP learning
**v2.0+**: Could-have features and advanced capabilities

Include estimated timelines and dependencies between phases.

## Output Format

Generate a structured markdown report with the following sections:

```markdown
# MVP Scope Recommendation: [Product Name]

## Executive Summary
[Brief overview of MVP focus, core user problem addressed, key decisions made]

---

## Core Analysis

### User Problem Statement
[Clear articulation of the primary pain point being solved]

### Business Objectives
- Primary goal: [e.g., Validate market demand for X]
- Success metric: [e.g., 100 paying users in first month]
- Risk mitigation: [Key assumptions to validate]

---

## Feature Classification

### MoSCoW Prioritization
| Priority | Count | Description |
|----------|-------|-------------|
| MUST HAVE | X | Critical for launch |
| SHOULD HAVE | Y | Important but deferrable |
| COULD HAVE | Z | Nice-to-have |
| WON'T HAVE | W | Excluded from MVP |

### RICE Scoring Summary
[Table of features with Reach, Impact, Confidence, Effort, and RICE scores]

### Value vs. Effort Matrix
```
High Value    │ [Quick Wins]     │ [Major Projects]
              │ - Feature A      │ - Feature B
              │ - Feature C      │ - Feature D
──────────────┼──────────────────┼─────────────────
Low Value     │ [Fill-ins]       │ [Time Wasters]
              │ - Feature E      │ - Feature F
              │                  │ - Feature G
              └──────────────────┴─────────────────
              Low Effort         High Effort
```

---

## Recommended MVP Scope

### Must-Have Features (Launch Critical)

| # | Feature | User Story | RICE Score | Justification |
|---|---------|------------|------------|---------------|
| 1 | [Feature] | As a [user], I want to [action] so that [benefit] | XX | Why it's essential |
| 2 | [Feature] | ... | XX | ... |

**Total MVP Features**: [3-5 features]

### Feature Details

#### [Feature Name]
- **User Story**: As a [role], I want to [capability] so that [value]
- **Why Must-Have**: Critical for core value delivery
- **Dependencies**: None / [list dependencies]
- **Estimated Effort**: [X weeks]
- **Risk Level**: Low/Medium/High + mitigation

---

## Excluded Features (For Later)

### Should Have (v1.1-v2.0)
| Feature | Rationale for Deferral | Expected Impact |
|---------|----------------------|-----------------|
| [Feature] | Not critical for core value validation | Medium-High |

### Could Have (v2.0+)
| Feature | Rationale for Exclusion | Potential Value |
|---------|------------------------|-----------------|
| [Feature] | Low priority, high effort | Medium |

---

## Success Criteria & Metrics

### Primary Success Metric
[Single most important metric to track]

### Target Benchmarks
| Metric | MVP Goal | Validation Threshold | Failure Signal |
|--------|----------|---------------------|----------------|
| [Metric 1] | X% | Y% | Z% |
| [Metric 2] | A users | B users | C users |

### Qualitative Success Indicators
- User interview feedback: "[Quote format]"
- Retention benchmark: [X% Day-7 retention]
- Willingness to pay: [Y% conversion to paid]

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| [Risk 1] | Medium | High | [Action to reduce risk] |
| [Risk 2] | Low | Medium | ... |

### Critical Assumptions to Validate
1. Users will adopt this solution for the core problem
2. Target users can be reached through [channel]
3. The pricing model is acceptable to users

---

## Phased Roadmap

### MVP v1.0 (Launch) - [Estimated Duration: X weeks]
**Goal**: Validate core value proposition with minimum features
**Features**:
- [Must-have 1]
- [Must-have 2]
- [Must-have 3]

### v1.1 - [Estimated Duration: Y weeks]
**Goal**: Improve retention and address early feedback
**Features**:
- [Should-have feature 1]
- [Should-have feature 2]

### v2.0 - [Estimated Duration: Z weeks]
**Goal**: Scale and expand to adjacent use cases
**Features**:
- [Could-have features]
- Advanced capabilities

---

## Implementation Recommendations

### Immediate Actions (Week 1)
1. Conduct user interviews to validate must-haves
2. Finalize technical architecture for core features
3. Set up analytics and success metric tracking

### Pre-Launch Checklist
- [ ] Core feature development complete
- [ ] Success metrics instrumentation in place
- [ ] Onboarding flow tested with 5+ users
- [ ] Support documentation ready
- [ ] Launch communication plan prepared

---

*Recommendation generated by: MVP Scope Advisor Skill*
*Date: YYYY-MM-DD*
```

## Best Practices

### When to Use This Skill
- Early product discovery phase when scope is unclear
- Before sprint planning or roadmap creation
- When stakeholders request too many features for one release
- Need to justify feature prioritization decisions
- Validating lean startup hypotheses

### Core Principles

1. **Focus on the core user problem**: MVP should solve ONE primary pain point exceptionally well, not many problems inadequately

2. **Validate must-haves with real users**: Before building, confirm that your "must-have" features actually address user needs through interviews and surveys

3. **Keep MVP scope to 3–5 key features**: True minimum viability means stripping away everything non-essential; if you can't define an MVP in this range, you haven't narrowed enough

4. **Include success metrics and failure signals**: Define what "success" looks like quantitatively AND when to pivot or kill the product (don't bet everything on a single outcome)

5. **Revisit scope after MVP validation**: MVP is a learning tool; use data and feedback to inform v1.1 and beyond, not as a final definition of your product

### Feature Selection Guidelines

**Must-Have Criteria:**
- Without it, the product doesn't deliver its core value proposition
- Users would abandon the product entirely without this feature
- Directly addresses the primary user pain point being solved
- Can be built with available resources in the timeframe

**Features to Defer:**
- Enhances experience but not essential for first use
- Targets secondary user segments (focus on primary first)
- Requires integrations or external dependencies not ready
- "Nice-to-have" that doesn't impact core value delivery

### Common Pitfalls

| Pitfall | Warning Signs | Correction |
|---------|---------------|------------|
| **Feature creep** | MVP scope exceeds 5 features; timeline extends indefinitely | Cut features aggressively; return to must-have criteria |
| **Assuming you know users** | No user interviews conducted; "I think users want" language | Conduct at least 5-10 user interviews before finalizing scope |
| **Ignoring technical debt** | Architecture decisions deferred indefinitely; team burned out | Build with scalability in mind for core flows only |
| **No success metrics** | "We'll know it works when..." without quantitative targets | Define specific, measurable success criteria upfront |

### Review Process

Before finalizing MVP scope:
1. **Challenge each must-have**: Ask "Would users abandon this product if we didn't have this feature?" If answer is no, reconsider classification
2. **Stakeholder alignment**: Ensure all stakeholders agree on the prioritization and understand trade-offs
3. **Technical feasibility review**: Confirm engineering team believes timeline is realistic
4. **User validation check**: Verify must-haves align with what real users said they need

---

*This skill follows lean startup principles and product management best practices from sources like "The Lean Startup" by Eric Ries, "Inspired" by Marty Cagan, and "Escaping the Build Trap" by Melissa Perri.*

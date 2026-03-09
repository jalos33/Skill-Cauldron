---
name: feature-prioritizer
description: Uses RICE (Reach, Impact, Confidence, Effort) and ICE (Impact, Confidence, Ease) scoring frameworks, combined with stakeholder input, to prioritize product features and create ranked backlogs.
tags: [prioritization, product-management, rice, ice, backlog]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Feature Prioritizer Skill

This skill uses RICE (Reach, Impact, Confidence, Effort) and ICE (Impact, Confidence, Ease) scoring frameworks to systematically prioritize product features based on data-driven analysis and stakeholder input.

## Instructions

Follow this systematic approach to prioritize features using quantitative scoring:

### Step 1: Extract Core Elements

Parse the input to identify:
- **Feature List**: All proposed features with descriptions
- **User Stories**: How users will interact with each feature
- **Business Goals**: Strategic objectives and success metrics
- **Constraints**: Time, budget, technical limitations, resource availability
- **Stakeholder Input**: Opinions from leadership, customers, engineering on importance, urgency, risks

### Step 2: Select Scoring Framework

Choose the appropriate framework based on decision context:

**RICE Scoring (Recommended for roadmap planning):**
- **Reach**: How many users will this affect in a given period? (e.g., monthly active users)
- **Impact**: How much will it improve the core metric? (3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal)
- **Confidence**: How certain are you about your estimates? (100% = high, 80% = medium, 50% = low, <50% = speculative)
- **Effort**: Person-months required to build and launch (include design, QA, maintenance)
- **RICE Score** = (Reach × Impact × Confidence) / Effort

**ICE Scoring (Recommended for quick decisions):**
- **Impact**: How much will it drive the desired outcome? (1-10 scale)
- **Confidence**: How sure are you about this impact? (1-10 scale)
- **Ease**: How easy is it to implement? (1-10 scale, where 10 = easiest)
- **ICE Score** = Impact × Confidence × Ease

### Step 3: Gather Scoring Inputs

For each feature, collect estimates from relevant stakeholders:

| Input | Who Provides | Notes |
|-------|--------------|-------|
| Reach | Product/Marketing | Based on user research and data |
| Impact | Product/Data Team | Based on expected metric lift |
| Confidence | All Stakeholders | Consensus or weighted average |
| Effort/Ease | Engineering | Technical feasibility assessment |

### Step 4: Calculate Scores

Apply the scoring formula for each feature:

**RICE Calculation:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

Example: Reach=5000, Impact=2, Confidence=80%, Effort=3 months
- RICE = (5000 × 2 × 0.80) / 3 = **2,667**

**ICE Calculation:**
```
ICE Score = Impact × Confidence × Ease
```

Example: Impact=8, Confidence=7, Ease=6
- ICE = 8 × 7 × 6 = **336**

### Step 5: Incorporate Stakeholder Input

Add qualitative context to quantitative scores:

| Source | Type of Input | Example Notes |
|--------|---------------|---------------|
| CEO/Leadership | Strategic alignment, urgency | "CEO flagged as Q1 priority" |
| Engineering | Technical feasibility, effort concerns | "High effort due to legacy dependencies" |
| Customer Support | User pain points, frequency | "Top requested feature from support tickets" |
| Sales/Acquisition | Revenue impact, competitive pressure | "Needed for enterprise deal closure" |

### Step 6: Identify Dependencies and Conflicts

Analyze relationships between features:

- **Dependencies**: Feature B requires Feature A to be complete first
- **Conflicts**: Features that cannot both be implemented (resource contention)
- **Synergies**: Features that amplify each other's value when delivered together

### Step 7: Generate Prioritized Backlog

Create a ranked list with the following structure:

1. Sort by RICE or ICE score (highest to lowest)
2. Flag dependencies and blockers
3. Group into release candidates based on effort and impact
4. Highlight quick wins (high impact, low effort)
5. Identify strategic bets (lower score but high alignment with goals)

### Step 8: Recommend MVP/Next Sprint Features

Based on the prioritized backlog, recommend:

- **Top N for MVP**: Features that deliver core value fastest
- **Quick Wins**: High score, low effort items to ship immediately
- **Strategic Investments**: Lower scores but critical for long-term goals
- **Defer/Look Again**: Low scores or high uncertainty items

## Output Format

Generate a structured markdown report:

```markdown
# Feature Prioritization Report: [Product/Project Name]

## Executive Summary
[Brief overview of top recommendations, key trade-offs made, final prioritized list summary]

---

## Scoring Framework Used
**Framework**: RICE / ICE (specify which)
**Scoring Criteria**:
- Reach: [description of how calculated]
- Impact: 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal (RICE) OR 1-10 scale (ICE)
- Confidence: 100%=high, 80%=medium, 50%=low (RICE) OR 1-10 scale (ICE)
- Effort/Ease: [description of calculation]

---

## Prioritized Feature Backlog

### Full Ranked List

| Rank | Feature | RICE/ICE Score | Reach/Impact | Confidence | Effort/Ease | Priority Tier |
|------|---------|----------------|--------------|------------|-------------|---------------|
| 1 | [Feature] | XXXX | XX / X.X | XX% | X months | P0 - Must Do |
| 2 | [Feature] | XXXX | ... | ... | ... | P1 - High Priority |

**Legend**:
- **P0 (Must Do)**: Top scorers, core value delivery
- **P1 (High Priority)**: Strong scores, significant impact
- **P2 (Medium Priority)**: Moderate scores, nice-to-have
- **P3 (Defer)**: Low scores or high uncertainty

---

### Detailed Feature Analysis

#### [Feature Name] - Score: XXXX

**User Story**: As a [user], I want to [action] so that [benefit]

| Metric | Value | Rationale |
|--------|-------|-----------|
| Reach | XX,XXX users/month | Based on [source] |
| Impact | X.X (High) | Expected to improve [metric] by X% |
| Confidence | XX% | Medium confidence due to [reason] |
| Effort | X person-months | Includes design, dev, QA |

**Stakeholder Notes**:
- CEO: "[Quote or note on strategic importance]"
- Engineering: "[Technical concerns or insights]"
- Customer Support: "[User feedback frequency]"

**Dependencies**: Requires [Feature A] to be complete first
**Conflicts**: Cannot ship with [Feature B] due to resource contention

---

## MVP / Next Sprint Recommendations

### Recommended for Immediate Implementation (Top 3)

| # | Feature | Score | Why This Now? | Estimated Impact |
|---|---------|-------|---------------|------------------|
| 1 | [Feature] | XXXX | High score, low effort | +X% metric improvement |
| 2 | [Feature] | XXXX | Strategic alignment with Q1 goals | Revenue opportunity |
| 3 | [Feature] | XXXX | Addresses top user pain point | Improved retention |

### Quick Wins (High Score, Low Effort < 1 month)
- [Feature A]: Score XX, Effort X weeks - Easy to ship for quick value
- [Feature B]: Score XX, Effort X weeks - Minimal engineering investment

### Strategic Investments (Lower Score but Critical)
- [Feature C]: Score XX, High strategic alignment with long-term vision
- Rationale: Essential for [market expansion/competitive differentiation]

---

## Dependency Map

```
[Feature A] ──┐
              ├──> [Feature D] (Blocker for launch)
[Feature B] ──┘

[Feature C] ──> [Feature E] ──> [Feature F] (Sequential dependency chain)
```

**Critical Path Features**: These must be completed before others can start:
1. [Feature A] - Blocks 3 downstream features
2. [Feature B] - Required for integration work

---

## Risk Assessment

| Feature | Risk Level | Description | Mitigation |
|---------|------------|-------------|------------|
| [Feature X] | High | Low confidence score (50%) due to untested technology | Run spike/sandbox first |
| [Feature Y] | Medium | Engineering estimates may be optimistic | Add 20% buffer to timeline |

### Confidence Distribution
- **High Confidence (>80%)**: X features - Ready for commitment
- **Medium Confidence (50-80%)**: X features - Needs more research
- **Low Confidence (<50%)**: X features - Requires validation before commitment

---

## Stakeholder Input Summary

| Source | Key Points | Influence on Scoring |
|--------|------------|---------------------|
| CEO/Leadership | [Summary of strategic priorities] | Adjusted confidence for X features |
| Engineering Team | [Technical concerns identified] | Increased effort estimates by X% |
| Customer Feedback | [Top pain points from users] | Boosted impact scores for Y features |

---

## Alternative Scenarios

### Optimistic Scenario (Higher Confidence, Lower Effort)
If confidence averages +20% and effort -15%, top 3 would be:
1. [Feature A] - Score XXXX (+XX%)
2. [Feature B] - Score XXXX (+XX%)
3. [Feature C] - Score XXXX (+XX%)

### Conservative Scenario (Lower Confidence, Higher Effort)
If confidence averages -20% and effort +25%, top 3 would be:
1. [Feature A] - Score XXXX (-XX%)
2. [Feature D] - Score XXXX (relatively better under constraints)
3. [Feature B] - Score XXXX (-XX%)

---

## Next Steps

### Immediate Actions (This Week)
1. Review scoring assumptions with stakeholders
2. Validate effort estimates with engineering leads
3. Confirm reach/impact numbers with data team

### Pre-Launch Validation
- [ ] Stakeholder sign-off on prioritization approach
- [ ] Engineering capacity review for top 5 features
- [ ] Customer validation of assumed pain points

---

*Prioritization analysis generated by: Feature Prioritizer Skill*
*Date: YYYY-MM-DD*
*Framework used: RICE / ICE (specify)*
```

## Best Practices

### When to Use This Skill
- Creating or updating product roadmap
- Deciding what to build in next sprint/quarter
- Resolving conflicts between feature requests
- Needing data-driven justification for prioritization decisions
- Aligning stakeholders on resource allocation

### Core Principles

1. **Gather input from multiple stakeholders**: No single person has complete picture; combine perspectives from product, engineering, customer support, and leadership

2. **Use relative scoring (1–10 scale)**: Instead of absolute numbers, score features relative to each other to reduce bias and anchoring effects

3. **Re-score after new data**: Prioritization is not static; update scores when you get user feedback, usage metrics, or technical discoveries

4. **Combine RICE for long-term, ICE for quick decisions**: Use RICE (with Effort denominator) for quarterly/annual planning where effort matters most; use ICE (multiplicative) for rapid decision cycles

5. **Always include rationale and risks**: Scores alone don't tell the full story; document assumptions, confidence levels, and known risks alongside each feature's score

### Scoring Guidelines

**RICE Framework:**
| Metric | Scale | Guidance |
|--------|-------|----------|
| Reach | Actual number (users/time period) | Be specific: "5,000 users/month" not "many users" |
| Impact | 3=massive, 2=high, 1=medium, 0.5=low, 0.25=minimal | Massive = >25% metric improvement; Minimal = barely measurable |
| Confidence | 100%=high, 80%=medium, 50%=low, <50%=speculative | High = validated with data; Low = based on assumptions |
| Effort | Person-months (total team effort) | Include design, development, QA, maintenance time |

**ICE Framework:**
| Metric | Scale | Guidance |
|--------|-------|----------|
| Impact | 1-10 | How much will this move the needle? |
| Confidence | 1-10 | How sure are you about the impact? |
| Ease | 1-10 | How easy is implementation? (10=easiest) |

### Common Pitfalls

| Pitfall | Warning Signs | Correction |
|---------|---------------|------------|
| **Effort underestimation** | Scores seem too good to be true; engineering pushes back constantly | Add 25-50% buffer to effort estimates; involve engineers early in scoring |
| **Confidence inflation** | Everyone rates confidence as 90-100%; no features marked "low" | Force distribution: only 20% can be >80%, require justification for high scores |
| **Stakeholder bias overriding data** | CEO's favorite always ranks #1 regardless of score | Document business rationale separately; keep scoring transparent and data-driven |
| **Ignoring dependencies** | Top features blocked by incomplete foundational work | Create dependency map before finalizing rankings |

### Review Cadence

- **Monthly**: Re-score top 5 features with fresh data
- **Quarterly**: Full backlog re-prioritization aligned with OKRs
- **After major events**: Update scores after user research, competitive moves, or technical discoveries

---

*This skill draws on prioritization frameworks from "Inspired" by Marty Cagan, "Escaping the Build Trap" by Melissa Perri, and industry best practices from product leaders at companies like Amplitude, ProductSchool, and Reforge.*

# Feature Prioritizer Skill

Use data-driven RICE and ICE scoring frameworks to prioritize product features, rank backlogs, and make informed decisions about what to build next.

## Description

The Feature Prioritizer skill helps teams systematically evaluate and rank feature requests using proven prioritization frameworks: **RICE** (Reach, Impact, Confidence, Effort) for roadmap planning and **ICE** (Impact, Confidence, Ease) for quick decision-making. By combining quantitative scoring with stakeholder input, this skill creates transparent, defensible prioritization decisions that align teams on resource allocation.

## Purpose

Product teams constantly face competing feature requests from customers, executives, sales, and engineering. This skill provides:
- **Data-driven framework**: Move beyond "highest paid person's opinion" to objective scoring
- **Stakeholder alignment**: Incorporate multiple perspectives while maintaining analytical rigor
- **Dependency awareness**: Identify blockers and critical path items before committing
- **Transparent trade-offs**: Clearly communicate why Feature A ranks above Feature B

Ideal for product managers, product owners, and engineering leads practicing agile prioritization.

## Features

- **Dual framework support**: Apply RICE (for quarterly planning) or ICE (for sprint decisions) scoring models
- **Stakeholder integration**: Capture input from leadership, engineering, customer support, and sales
- **Dependency mapping**: Identify feature blockers and critical path items
- **Priority tiering**: Categorize features into P0-P3 tiers for clear prioritization
- **MVP recommendations**: Extract top features for immediate implementation
- **Risk assessment**: Flag low-confidence items requiring validation before commitment

## How to Use

### Installation

```bash
curl -o skills/feature-prioritizer/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/feature-prioritizer/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Prioritize these features using RICE"
- "Score backlog with ICE framework"
- "Rank features for MVP based on stakeholder input"
- "Apply RICE scoring to this list"
- "Help prioritize product roadmap"

### Example Usage

**User**: Prioritize these 10 features using RICE with stakeholder feedback

**Skill Response**: Generates comprehensive prioritization report including:
- Ranked feature backlog with RICE scores
- Detailed analysis for each feature (Reach, Impact, Confidence, Effort)
- Stakeholder notes incorporated from leadership and engineering
- Top 3 recommendations for immediate implementation
- Dependency map showing blockers and critical path items

## Examples

### Example 1: SaaS Dashboard Feature Prioritization

**Input**: "Prioritize these features using RICE for a new analytics dashboard: custom reports, real-time metrics, data export, team workspaces, API access, scheduled emails, white-labeling"

**Output Summary**:
| Rank | Feature | RICE Score | Priority Tier |
|------|---------|------------|---------------|
| 1 | Real-time metrics | 80,000 | P0 - Must Do |
| 2 | Custom reports | 45,000 | P1 - High Priority |
| 3 | Data export (CSV) | 28,000 | P1 - High Priority |
| 4 | Scheduled emails | 18,000 | P2 - Medium |
| 5 | Team workspaces | 12,000 | P2 - Medium |
| 6 | API access | 8,000 | P3 - Defer |

**Recommendation**: Launch with real-time metrics + basic reporting for MVP; defer API and white-labeling to v2.0

### Example 2: ICE Scoring for Sprint Planning

**Input**: "Score backlog with ICE framework for next sprint"

**Output Summary**:
| Feature | Impact | Confidence | Ease | ICE Score | Recommendation |
|---------|--------|------------|------|-----------|----------------|
| Fix checkout bug | 9 | 10 | 8 | **720** | Must include |
| Add dark mode | 6 | 8 | 9 | **432** | Quick win |
| New analytics | 8 | 5 | 4 | **160** | Defer to next sprint |

### Example 3: E-commerce Feature Prioritization with Stakeholder Input

**Input**: "Rank these features for MVP: guest checkout, saved payment methods, order tracking, gift cards" with stakeholder notes

**Output Summary incorporates**:
- CEO flagged guest checkout as Q1 priority (boosts confidence)
- Engineering noted saved payments requires PCI compliance (increases effort estimate)
- Customer support reported 30% of tickets about checkout friction (validates impact score)

## Output Format

The skill generates a structured markdown report containing:

1. **Executive Summary**: Top recommendations and key trade-offs
2. **Scoring Framework Used**: RICE or ICE with criteria explanation
3. **Prioritized Feature Backlog**: Full ranked list with scores and priority tiers
4. **Detailed Feature Analysis**: Per-feature breakdown with stakeholder notes
5. **MVP/Next Sprint Recommendations**: Top features for immediate implementation
6. **Dependency Map**: Visual representation of feature blockers
7. **Risk Assessment**: Low-confidence items requiring validation
8. **Stakeholder Input Summary**: How different perspectives influenced scoring

See the [SKILL.md](SKILL.md) for complete output format specification.

## Best Practices

### When to Use This Skill
- Creating or updating product roadmap
- Deciding what to build in next sprint/quarter
- Resolving conflicts between feature requests
- Needing data-driven justification for prioritization decisions
- Aligning stakeholders on resource allocation

### Core Principles
1. **Gather input from multiple stakeholders**: Combine perspectives from product, engineering, customer support, and leadership
2. **Use relative scoring (1–10 scale)**: Score features relative to each other to reduce bias
3. **Re-score after new data**: Update scores when you get user feedback or usage metrics
4. **Combine RICE for long-term, ICE for quick decisions**: Use RICE for quarterly planning; use ICE for rapid cycles
5. **Always include rationale and risks**: Document assumptions alongside each score

### Framework Selection Guide

| Use Case | Recommended Framework | Why |
|----------|----------------------|-----|
| Quarterly roadmap planning | RICE | Effort denominator helps compare large initiatives |
| Sprint backlog prioritization | ICE | Simpler, faster scoring for short timeframes |
| Resource-constrained decisions | RICE | Explicitly accounts for effort trade-offs |
| Quick team alignment sessions | ICE | Multiplicative model emphasizes confidence |

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*This skill draws on prioritization frameworks from "Inspired" by Marty Cagan, "Escaping the Build Trap" by Melissa Perri, and industry best practices from product leaders at companies like Amplitude, ProductSchool, and Reforge.*

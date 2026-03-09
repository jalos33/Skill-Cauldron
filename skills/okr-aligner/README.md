# OKR Aligner Skill

Connects team-level objectives, key results, and tasks to company-wide OKRs, ensuring alignment, identifying gaps, and suggesting adjustments for maximum strategic impact.

## Description

The OKR Aligner skill provides systematic analysis of how team-level work supports (or doesn't support) company-wide Objectives and Key Results. It maps individual initiatives to organizational goals using weighted scoring to identify misalignments, orphaned work, and coverage gaps. This skill helps product managers, engineering leads, and executives ensure that quarterly efforts are strategically focused on the right outcomes.

## Purpose

Organizations often struggle with maintaining strategic alignment as teams plan their quarterly work. Initiatives get approved without clear connection to company goals, creating wasted effort and missed opportunities. This skill helps by:
- **Mapping work to strategy**: Explicitly link team objectives to company OKRs
- **Quantifying alignment**: Calculate weighted scores showing % of effort supporting strategic goals
- **Identifying gaps**: Find orphaned initiatives and uncovered company objectives
- **Suggesting fixes**: Provide actionable recommendations for improving alignment

Ideal for product leaders, engineering managers, OKR champions, and executives managing quarterly planning.

## Features

- **Multi-level mapping**: Connects individual tasks → team KRs → company OKRs
- **Weighted scoring system**: Direct (1.0x), Indirect (0.75x), Enabling (0.5x), Unaligned (0x) weights
- **Gap detection**: Identifies orphaned work and uncovered company objectives
- **Strategic recommendations**: Rewriting KRs, adding bridges, reprioritizing initiatives
- **Cross-team coordination**: Flags where other teams should own specific work
- **Health metrics**: Target 70-85% alignment range with clear interpretation guidelines

## How to Use

### Installation

```bash
curl -o skills/okr-aligner/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/okr-aligner/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Align my team OKRs to company goals"
- "Check alignment of these objectives with top-level OKRs"
- "Map team tasks to company OKRs"
- "Find gaps in OKR alignment"
- "Suggest improvements for better strategic alignment"

### Example Usage

**User**: Align engineering team OKRs to company growth goals

**Input**:
```
Company Q2 OKRs:
Objective 1: Drive revenue growth
  KR1: Close $10M in new enterprise deals
  KR2: Increase expansion revenue by 25%
Objective 2: Improve customer satisfaction
  KR1: Achieve 95% customer satisfaction score
  KR2: Reduce time-to-value from 30 days to 7 days

Engineering Team OKRs:
Objective A: Improve platform reliability
  KR: Reduce production incidents by 80%
  Initiatives: Monitoring upgrade, incident response automation

Objective B: Accelerate feature delivery
  KR: Reduce deployment time from 60min to 10min
  Initiatives: CI/CD pipeline overhaul, automated testing expansion
```

**Skill Response**: Generates alignment report showing how reliability work supports customer satisfaction (KR2), how deployment acceleration enables revenue growth (faster time-to-market), identifies which company KRs lack engineering support, and suggests specific KR rewrites for clearer linkage.

---

## Examples

### Example 1: Engineering Team Alignment to Revenue Goals

**Input**: "Align engineering team OKRs to company growth goals"

**Output Summary:**

#### OKR Alignment Report: Q2 Engineering Team

**Alignment Score**: 78% (Target: 70-85%) ✓ Healthy range

**Direct Contributions:**
| Company Objective | Company KR | Team Objective | Team KR | Impact |
|-------------------|------------|----------------|---------|--------|
| Drive revenue growth | Close $10M in enterprise deals | Accelerate feature delivery | Reduce deployment time 60→10min | High |
| Improve customer satisfaction | Achieve 95% CSAT score | Improve platform reliability | Reduce incidents by 80% | Medium (indirect) |

**Missing Coverage:**
- **Company KR**: Increase expansion revenue by 25% - No engineering initiatives directly supporting upsell/cross-sell features

**Recommendations:**
1. Add KR: "Enable customer self-service onboarding" to support expansion revenue goal
2. Reposition reliability work as enabling feature delivery (not just incident reduction)

---

### Example 2: Product Team Revenue Support Check

**Input**: "Check if product team initiatives support quarterly revenue OKR"

**Output Summary:**

#### Alignment Analysis: Product Team vs Revenue Goal

| Initiative | Revenue Linkage | Weight | Status |
|------------|-----------------|--------|--------|
| New onboarding flow | Direct - reduces time-to-value | 1.0x | Aligned ✓ |
| Enterprise features | Direct - enables larger deals | 1.0x | Aligned ✓ |
| Mobile app redesign | Indirect - improves satisfaction | 0.75x | Weak linkage |
| Design system update | Enabling work | 0.5x | Hard to quantify value |
| Explore AI features | No alignment (2025 roadmap) | 0x | Orphaned |

**Alignment Score**: 68% - Below target, needs improvement

**Recommendations:**
1. Reframe mobile redesign with clear revenue impact: "Reduce mobile drop-off by 30%"
2. Move AI exploration to innovation bucket (acceptable at 10-15% capacity)

---

### Example 3: Sprint Task Mapping to Company Objectives

**Input**: "Map sprint tasks to company-wide objectives"

**Output Summary:**

#### Granular Task Alignment Map

| Epic | Story | Team OKR | Company OKR | Linkage Type |
|------|-------|----------|-------------|--------------|
| Performance | Optimize database queries | Improve reliability | Reduce time-to-value | Direct (enables faster loads) |
| Security | Implement SSO integration | Improve security posture | Support enterprise deals | Direct (enterprise requirement) |
| Analytics | Build usage dashboards | Enable data-driven decisions | Improve CSAT | Indirect (better insights → better UX) |
| Tech Debt | Refactor legacy auth module | Reduce technical debt | None identified | Orphaned - recommend repositioning |

**Orphaned Work Flagged**: 1 epic with no clear company OKR linkage

---

## Output Format

The skill generates a structured markdown report containing:

1. **Executive Summary**: Alignment score, aligned objectives count, critical gaps, top recommendation
2. **Company OKR Reference Table**: All company goals with current team support status
3. **Alignment Map**: Categorized by Direct Contributions, Indirect Support, Enabling Work, No Alignment
4. **Score Breakdown**: Weighted calculation showing how alignment score is derived
5. **Gap Analysis**: Missing coverage (company gaps) and orphaned work (team gaps)
6. **Recommendations**: Repositioning KRs, adding bridges, reprioritizing initiatives, cross-team coordination
7. **Action Plan**: Prioritized next steps with owners and timelines

## Best Practices

### When to Use This Skill

- Quarterly OKR planning before finalizing team goals
- Mid-quarter alignment check-ins (every 4-6 weeks)
- Resource allocation reviews (approving/rejecting new initiatives)
- Cross-team strategy workshops
- Executive reporting on strategic focus

### Target Alignment Guidelines

| Metric | Target | Why This Matters |
|--------|--------|------------------|
| **Overall Score** | 70-85% | Balance of strategic focus + innovation space |
| **Direct Contributions** | ≥60% of aligned work | Strong explicit linkage to business outcomes |
| **Missing Coverage** | ≤2 company OKRs | Ensure all strategic goals have team support |
| **Orphaned Work** | 10-20% capacity | Allow exploration, tech debt, future innovation |

### Alignment Language Best Practices

Use clear specificity when describing linkages:

**Strong linkage statements:**
- "Directly supports Company KR: Reduce time-to-value by enabling X"
- "Enables Customer Satisfaction goal through improved reliability"
- "Contributes to Revenue growth by reducing enterprise churn risk"

**Weak (avoid):**
- "Improves customer experience" (vague)
- "Supports company goals" (no specificity)
- "Makes things better" (not measurable)

### Stakeholder Review Process

1. **Team leads**: Validate that linkage assessments accurately reflect their work's value
2. **Product managers**: Confirm feature initiatives connect to business outcomes
3. **Engineering leaders**: Ensure infrastructure has clear enabling rationale
4. **Executives**: Review missing coverage gaps for resource allocation decisions

### Common Pitfalls to Avoid

1. **Forcing alignment**: Don't artificially connect work that genuinely doesn't belong in current OKRs
2. **Over-alignment**: 90%+ alignment indicates insufficient innovation/exploration time
3. **One-time exercise**: Alignment should be reviewed quarterly, not just annually
4. **Ignoring context**: Engineering infrastructure has value even without direct KR linkage

## Dependencies

This skill requires no external dependencies. It works entirely with text-based analysis of OKR data provided in input. Optional Jira/Linear API integration can automate task extraction if available.

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*OKR alignment frameworks inspired by "Measure What Matters" by John Doerr and modern OKR best practices from Workfront.*

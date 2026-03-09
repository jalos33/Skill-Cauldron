---
name: okr-aligner
description: Connects team-level objectives, key results, and tasks to company-wide OKRs, ensuring alignment, identifying gaps, and suggesting adjustments for maximum strategic impact.
tags: [okr, alignment, strategy, product-management, goal-setting]
author: Jose Quiñones
version: 1.0
license: MIT
---

# OKR Aligner Skill

Connects team-level objectives and key results to company-wide OKRs, identifying alignment gaps and suggesting strategic adjustments for maximum impact.

## Instructions

Follow this step-by-step methodology to perform comprehensive OKR alignment analysis:

### Step 1: Parse Company-Level OKRs
Extract the organization's quarterly OKRs from input:

**Company OKR Structure:**
| Element | Description | Example |
|---------|-------------|---------|
| Objective | Qualitative, inspirational goal | "Become the market leader in enterprise security" |
| Key Results | Measurable outcomes that define success | KR1: Achieve 95% customer satisfaction score<br>KR2: Close $10M in new enterprise deals<br>KR3: Reduce security incidents by 80% |

**Data Points to Extract:**
- Objective statement (qualitative goal)
- Each Key Result with current value and target value
- Timeframe/quarter
- Owner/stakeholder (if available)
- Confidence level or progress (% complete)

### Step 2: Parse Team-Level OKRs and Tasks
Extract the team's objectives, key results, and associated work items:

**Team Input Sources:**
- Direct text input ("Our Q2 objectives are...")
- Jira/Linear export (CSV with epics/stories)
- Product backlog documentation
- Team planning documents

**Data Points to Extract per Team Objective:**
| Element | Description | Example |
|---------|-------------|---------|
| Objective | Team's qualitative focus | "Improve developer productivity" |
| Key Result | Measurable outcome | KR: Reduce deployment time from 30min to 5min |
| Initiatives/Tasks | Work items supporting the KR | Epic: CI/CD pipeline overhaul<br>Story: Implement automated testing |

### Step 3: Map Team Objectives to Company OKRs
For each team objective and key result, determine its relationship to company-level goals:

**Alignment Types:**
| Alignment Type | Description | Indicator |
|----------------|-------------|-----------|
| **Direct Contribution** | Team KR directly measures progress toward company KR | "Reduce deployment time" → "Ship features 2x faster (company KR)" |
| **Indirect Support** | Team work enables company goals but doesn't measure them | "Improve code quality" → supports "Customer satisfaction" via fewer bugs |
| **Enabling Work** | Infrastructure that makes other work possible | "Upgrade monitoring stack" → enables all reliability initiatives |
| **No Alignment** | No clear connection to current company objectives | "Explore AI features for 2025 roadmap" (future-focused) |

**Mapping Process:**
1. Read each team KR and identify which company objective it supports
2. For each company KR, determine if team KR directly measures progress or indirectly contributes
3. Flag KRs with no clear linkage to any company OKR
4. Note where multiple team objectives support the same company goal (good coverage) or where company goals lack team support (gaps)

### Step 4: Calculate Alignment Score
Compute quantitative metrics for alignment health:

**Alignment Score Calculation:**
```
Alignment Score = (Aligned Effort / Total Effort) × 100

Where:
- Aligned Effort = Sum of effort estimates for work with clear company OKR linkage
- Total Effort = Sum of all effort estimates in team plan

Target Range: 70-85% alignment is healthy
- Below 60%: Significant misalignment risk
- Above 90%: May indicate insufficient exploratory innovation work
```

**Scoring Breakdown by Alignment Type:**
| Alignment Type | Weight | Rationale |
|----------------|--------|-----------|
| Direct Contribution | 1.0x | Fully aligned with company goals |
| Indirect Support | 0.75x | Supports but not directly measured |
| Enabling Work | 0.5x | Infrastructure value, harder to quantify |
| No Alignment | 0x | Not contributing to current objectives |

### Step 5: Identify Gaps and Orphaned Work
Systematically find misalignments:

**Gap Categories:**
| Gap Type | Description | Detection Criteria |
|----------|-------------|-------------------|
| **Orphaned Objectives** | Team KRs with no company OKR connection | No linkage identified after mapping |
| **Missing Coverage** | Company KR with no team supporting it | Company goal has zero team initiatives |
| **Over-Aligned Teams** | Single team owns too many critical paths | Risk concentration if one team slips |
| **Conflicting Objectives** | Team goals that pull in opposite directions | One team improves speed while another prioritizes stability |

**Orphaned Work Identification:**
- List all team initiatives marked as "No Alignment"
- Assess strategic value (innovation, technical debt, future roadmap)
- Determine if work should be: repositioned, deprioritized, or moved to exploratory bucket

### Step 6: Suggest Strategic Adjustments
Provide actionable recommendations for improving alignment:

**Adjustment Strategies:**

1. **Rewrite Team Key Results**
   - Make explicit linkage to company OKRs clearer
   - Example: Change "Improve CI/CD" → "Enable 2x faster feature delivery (supports Company KR: Ship features 2x faster)"

2. **Add Bridging Key Results**
   - Create new KRs that connect team work to company goals
   - Example: Add KR: "Reduce bug escape rate by 50%" to support Company KR: "Achieve 95% customer satisfaction"

3. **Reprioritize Initiatives**
   - Move high-value orphaned work to exploratory/innovation bucket
   - Deprioritize low-impact items with no strategic connection

4. **Add Cross-Team Dependencies**
   - Identify where another team's OKR should connect
   - Example: "Sales team enablement" supports revenue growth but lives in Product OKRs

5. **Rebalance Work Distribution**
   - If one team owns all critical paths, redistribute to reduce risk
   - Create shared objectives across teams for high-priority company goals

### Step 7: Generate Alignment Report
Create comprehensive markdown output with:

1. **Executive Summary**: Overall alignment score, top insights
2. **Alignment Map**: Visual table showing team-to-company OKR linkages
3. **Gap Analysis**: List of misalignments and missing coverage
4. **Recommendations**: Prioritized adjustment suggestions
5. **Action Plan**: Specific next steps with owners and timelines

## Output Format Template

Your response should follow this structure:

```markdown
# OKR Alignment Report: [Quarter] [Team Name]

## Executive Summary
- **Alignment Score**: [XX]% ([Target: 70-85%])
- **Aligned Objectives**: [X]/[Y] team objectives have clear company linkage
- **Critical Gaps**: [Z] company OKRs lack team support
- **Top Recommendation**: [Primary action to improve alignment]

## Company OKR Reference
| Objective | Key Result | Target | Current | Team Support |
|-----------|------------|--------|---------|--------------|
| [Obj 1] | KR: [KR description] | [Target] | [Current]% | [Team Name(s)] |

## Alignment Map

### Direct Contributions (Weight: 1.0x)
| Company Objective | Company KR | Team Objective | Team KR | Impact Level |
|-------------------|------------|----------------|---------|--------------|
| [Obj] | [KR] | [Team Obj] | [Team KR] | High/Med/Low |

### Indirect Support (Weight: 0.75x)
| Company Objective | Company KR | Team Initiative | Contribution Type |
|-------------------|------------|-----------------|------------------|
| [Obj] | [KR] | [Initiative] | Enables/Improves/Facilitates |

### Enabling Work (Weight: 0.5x)
| Team Objective | Infrastructure Item | Enabled Capabilities |
|----------------|--------------------|---------------------|
| [Team Obj] | [Item] | [Capability 1, Capability 2] |

### No Alignment (Requires Review)
| Team Objective | Key Result | Initiative | Strategic Value | Recommendation |
|----------------|------------|------------|-----------------|----------------|
| [Team Obj] | [KR] | [Initiative] | Innovation/Debt/Future | Reposition/Deprioritize/Exploratory |

## Alignment Score Breakdown
| Category | Effort (points) | Weighted Contribution | Status |
|----------|-----------------|----------------------|--------|
| Direct Contributions | X | X.0x = Y points | [On track/Misaligned] |
| Indirect Support | X | X × 0.75 = Z points | ... |
| Enabling Work | X | X × 0.5 = W points | ... |
| No Alignment | X | X × 0 = 0 points | [Requires action] |
| **Total** | **X** | **XX%** | **[Score]** |

## Gap Analysis
### Missing Coverage (Company OKRs without team support)
1. **[Company Objective]** - KR: "[KR description]"
   - **Gap**: No identified team initiatives supporting this goal
   - **Risk**: [Impact if not addressed]
   - **Suggested Team**: [Team name that should own]

### Orphaned Work (Team Initiatives without company linkage)
1. **[Team Objective]** - "[Initiative]"
   - **Current Status**: No alignment to Q[Quarter] OKRs
   - **Strategic Value**: Innovation/Technical Debt/Future Roadmap
   - **Recommendation**: [Reposition, Deprioritize, or Move to Exploratory]

## Recommendations

### 1. Reposition Team Key Results (High Impact)
**Current**: "[Existing KR statement]"
**Suggested**: "[Improved KR with explicit linkage]"
**Rationale**: Makes alignment clear and measurable

### 2. Add Bridging Key Results (Medium Impact)
**Proposed New KR**: "[New KR that connects team work to company goal]"
**Supports Company Objective**: [Objective name]
**Effort Required**: [Low/Medium/High]

### 3. Reprioritize Initiatives (Quick Wins)
| Initiative | Current Priority | Recommended Action | Reason |
|------------|------------------|-------------------|--------|
| [Initiative] | High | Move to Exploratory | No current OKR alignment but valuable for innovation |
| [Initiative] | Medium | Deprioritize | Low strategic value, low alignment |

### 4. Cross-Team Coordination (Strategic)
**Opportunity**: Identify where another team should own specific work
- **[Company KR]**: Currently owned by [Current Team], consider sharing with [Other Team]
- **Shared Objective**: Create joint objective between [Team A] and [Team B] for [Goal]

## Action Plan

| Priority | Action Item | Owner | Timeline | Success Metric |
|----------|-------------|-------|----------|----------------|
| High | Rewrite 2 team KRs to show explicit company linkage | Team Lead | This week | Alignment score +10% |
| Medium | Create bridging KR for [Company Objective] | Product Manager | Next sprint | Clear measurable outcome |
| Low | Move exploratory work to innovation bucket (20% time) | Engineering Lead | Q-end | 20% capacity allocated |

## Next Steps
1. **This week**: Review alignment map with team leads, validate linkage assessments
2. **Next sprint**: Implement KR rewrites and add bridging KRs to planning
3. **End of quarter**: Re-run alignment check; track score progression over time

---
*Report generated by OKR Aligner Skill*
```

## Activation Phrases / When to Use

Use this skill when the user mentions any of these scenarios:
- "Align my team OKRs to company goals"
- "Check alignment of these objectives with top-level OKRs"
- "Map team tasks to company OKRs"
- "Find gaps in OKR alignment"
- "Suggest improvements for better strategic alignment"

## Usage Examples

### Example 1: Engineering Team Alignment
**Input**: "Align engineering team OKRs to company growth goals"
**Output**: Mapping of engineering initiatives (performance, reliability, tooling) to company objectives (revenue growth, customer satisfaction), identifying which infrastructure work directly enables business outcomes

### Example 2: Product Team Revenue Support Check
**Input**: "Check if product team initiatives support quarterly revenue OKR"
**Output**: Analysis showing how feature launches, UX improvements, and onboarding enhancements contribute to revenue metrics, highlighting gaps where product work doesn't drive monetization

### Example 3: Sprint Task Mapping
**Input**: "Map sprint tasks to company-wide objectives"
**Output**: Granular mapping of individual stories/epics to team OKRs and ultimately to company goals, flagging orphaned tasks that don't support strategic priorities

## Best Practices / Notes

### When This Skill Adds Value
- Quarterly OKR planning sessions before goal finalization
- Mid-quarter check-ins to identify drift from strategic goals
- Resource allocation decisions (what work to approve/reject)
- Cross-team alignment workshops
- Executive reviews requiring transparency into team contributions

### Target Alignment Guidelines
| Metric | Target | Interpretation |
|--------|--------|----------------|
| **Alignment Score** | 70-85% | Healthy balance of focus + innovation |
| **Direct Contributions** | ≥60% of aligned work | Strong explicit linkage to company goals |
| **Missing Coverage** | ≤2 company OKRs | Ensure all strategic goals have team support |
| **Orphaned Work** | 10-20% of capacity | Allow space for exploration and technical debt |

### Alignment Language Best Practices
Use clear, specific language when describing linkages:
- **"Directly supports"**: Team KR measures progress toward company KR
- **"Enables":** Infrastructure work making other initiatives possible
- **"Contributes to":** Indirect but meaningful impact on company goal
- **"Explores for future":** Innovation work not tied to current OKRs

### Common Pitfalls to Avoid
1. **Forcing alignment**: Don't artificially connect work that doesn't belong
2. **Over-alignment**: 90%+ alignment may indicate insufficient innovation time
3. **Vague linkages**: "Improves customer experience" is weak; specify how
4. **One-time exercise**: Alignment should be reviewed quarterly, not annually

### Stakeholder Involvement
- **Team leads**: Validate that linkage assessments are accurate
- **Product managers**: Ensure feature work connects to business outcomes
- **Engineering leaders**: Confirm infrastructure work has clear enabling value
- **Executives**: Review missing coverage gaps for resource allocation decisions

## Dependencies

- **No external dependencies required** - Text-based analysis using OKR data provided in input
- **Optional Enhancement**: Jira/Linear API integration for automated task extraction (if available)

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*OKR alignment follows best practices from "Workfront OKR Guide" and strategic goal-setting frameworks by John Doerr ("Measure What Matters").*

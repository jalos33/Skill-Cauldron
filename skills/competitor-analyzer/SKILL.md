---
name: competitor-analyzer
description: Tracks competitor products/features, analyzes strengths/weaknesses, and suggests differentiation strategies, positioning, and feature gaps to exploit.
tags: [competitive-analysis, product-strategy, market-research, differentiation]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Competitor Analyzer Skill

Tracks competitor products and features, analyzes their strengths and weaknesses, and provides actionable differentiation strategies for competitive positioning.

## Instructions

Follow this step-by-step methodology to conduct comprehensive competitor analysis:

### Step 1: Parse Input and Identify Key Elements
Extract the following from user input:
| Element | What to Extract | Examples |
|---------|-----------------|----------|
| Competitors | Company/product names mentioned | "Notion", "ClickUp", "Asana" |
| Our Product | Your product name or description | "Our task management tool", "SaaS platform" |
| Focus Area | Specific feature/domain to analyze | "task management", "pricing", "integrations" |
| Goals | What you want to achieve | "differentiate", "find gaps", "position better" |

### Step 2: Research Competitor Information
Gather public information about each competitor from available sources:

**Information Sources:**
- Company websites and product pages
- Pricing pages and feature lists
- Public changelogs and release notes
- Review sites (G2, Capterra, Product Hunt)
- Social media and blog announcements

**Data Points to Collect per Competitor:**
| Data Point | Details to Capture |
|------------|-------------------|
| Core Features | Main capabilities and functionality |
| Pricing Model | Free tier, paid plans, enterprise options |
| Target Audience | Who they serve (SMBs, enterprises, individuals) |
| UX/UI Approach | Design philosophy, usability focus |
| Integrations | Third-party connections available |
| Strengths | What they do exceptionally well |
| Weaknesses | Common complaints or limitations |

### Step 3: Build Feature Comparison Matrix
Create a structured comparison between your product and competitors:

```markdown
## Feature Comparison Matrix

| Feature Category | Our Product | Competitor A | Competitor B | Competitor C |
|------------------|-------------|--------------|--------------|--------------|
| Core Functionality | ✓ Full support | ✓ Supported | ✓ Supported | Partial |
| Pricing Flexibility | Starting at $X | Free tier available | Higher starting price | Enterprise only |
| Integrations | 50+ options | 100+ options | 30+ options | Limited |
| Mobile App | iOS & Android | iOS only | Both platforms | Web-only |
```

**Matrix Best Practices:**
- Use checkmarks (✓), crosses (✗), or partial indicators (△)
- Include pricing details where relevant
- Note unique features that differentiate your product
- Be accurate and verifiable - no assumptions

### Step 4: Perform SWOT Analysis Per Competitor
For each competitor, analyze:

| Component | Questions to Answer | Example Output |
|-----------|-------------------|----------------|
| **Strengths** | What do they excel at? Strong brand, large user base, innovative features | "Strong design system and template ecosystem" |
| **Weaknesses** | Where do they fall short? Common complaints, gaps in offering | "Limited automation capabilities", "Poor customer support reviews" |
| **Opportunities** | Market gaps you can exploit | "Underserved enterprise segment", "No affordable option for teams <10" |
| **Threats** | What could harm your position? | "New funding round enabling aggressive pricing", "Major partnership announcement" |

### Step 5: Identify Feature Gaps and Opportunities
Analyze the comparison to find:

**Gap Categories:**
| Gap Type | Description | Example |
|----------|-------------|---------|
| Missing Features | Capabilities competitors lack that you have | "Advanced reporting not offered by any competitor" |
| Pricing Gaps | Price points underserved in market | "No competitor offers mid-tier at $10/user/month" |
| UX Opportunities | Better user experience possible | "Simpler onboarding than competitive alternatives" |
| Integration Gaps | Missing integrations competitors have | "Only competitor without Salesforce integration" |
| Audience Gaps | Segments not well served | "No solution focused on remote-first teams" |

### Step 6: Develop Differentiation Strategies
Based on analysis, suggest positioning tactics:

**Differentiation Dimensions:**
1. **Unique Value Proposition (UVP)**
   - What makes you distinctly different?
   - Focus on benefits not just features
   - Example: "The only task manager built for async remote teams"

2. **Pricing Strategy**
   - Undercut on price for specific segments
   - Premium positioning with added value
   - Freemium to capture market share
   - Example: "Free tier for teams up to 5 users (vs competitors' 3-user limit)"

3. **UX/Design Advantage**
   - Simpler interface, faster workflows
   - Better onboarding experience
   - Accessibility focus
   - Example: "5-minute setup vs competitor's 30-minute configuration"

4. **Integration Ecosystem**
   - More integrations than competitors
   - Exclusive partnerships
   - Custom integration support
   - Example: "Native integrations with tools your team already uses daily"

5. **Customer Experience**
   - Superior support (24/7, dedicated success managers)
   - Community-driven features
   - Education and training resources
   - Example: "Dedicated onboarding specialist for all paid plans"

### Step 7: Create Action Plan with Next Steps
Prioritize recommendations by impact and effort:

| Priority | Action Item | Impact | Effort | Timeline | Owner |
|----------|-------------|--------|--------|----------|-------|
| High | Highlight unique reporting features in marketing | High | Low | 2 weeks | Marketing |
| Medium | Develop Salesforce integration based on competitor gap | High | Medium | Q2 | Engineering |
| Low | Create enterprise pricing tier to compete with Segment X | Medium | Medium | Q3 | Product |

## Output Format Template

Your response should follow this structure:

```markdown
# Competitive Analysis: [Product/Market Name]

## Executive Summary
- **Competitors Analyzed**: [Names]
- **Key Finding 1**: [Most significant insight]
- **Key Finding 2**: [Second most important insight]
- **Top Differentiation Opportunity**: [Best opportunity to exploit]

## Competitor Overview Table

| Competitor | Core Focus | Pricing Start | Target Segment | Key Strength | Key Weakness |
|------------|------------|---------------|----------------|--------------|--------------|
| [Name] | [Description] | $[X]/user | [Segment] | [Strength] | [Weakness] |

## Feature Comparison Matrix

| Feature | Our Product | Competitor A | Competitor B | Notes |
|---------|-------------|--------------|--------------|-------|
| [Feature 1] | ✓ Full support | ✓ Supported | △ Partial | [Context] |
| [Feature 2] | ✓ Exclusive | ✗ Not available | ✗ Not available | Differentiator |

## SWOT Analysis

### [Competitor Name]
**Strengths**:
- [Point 1]
- [Point 2]

**Weaknesses**:
- [Point 1]
- [Point 2]

**Opportunities for Us**:
- [Exploit #1]
- [Exploit #2]

**Threats to Monitor**:
- [Threat #1]
- [Threat #2]

## Feature Gaps Identified
| Gap Type | Description | Our Advantage | Priority |
|----------|-------------|---------------|----------|
| Pricing | No mid-tier option under $15/user | Our $10 tier fills gap | High |
| Features | Limited automation capabilities | Advanced workflows available | Medium |

## Differentiation Recommendations

### 1. Unique Value Proposition
**Recommended UVP**: "[Suggested positioning statement]"

**Rationale**: [Why this resonates with market]

### 2. Pricing Strategy
**Recommendation**: [Specific pricing tactic]
- [Detail 1]
- [Detail 2]

### 3. UX/Design Advantage
**Focus Area**: [Where to emphasize UX superiority]
- [Specific improvement or highlight]

### 4. Integration Strategy
**Opportunity**: [Integration-based differentiation]
- [Priority integrations to develop/promote]

## Action Plan

| Priority | Action Item | Impact | Effort | Timeline | Owner |
|----------|-------------|--------|--------|----------|-------|
| High | [Action 1] | High/Low | Low/Med/High | [Timeframe] | [Team] |
| Medium | [Action 2] | ... | ... | ... | ... |

## Next Steps
1. [Immediate action - this week]
2. [Short-term action - this month]
3. [Strategic initiative - next quarter]

---
*Analysis generated by Competitor Analyzer Skill*
```

## Activation Phrases / When to Use

Use this skill when the user mentions any of these scenarios:
- "Analyze competitors for this feature"
- "Track competitor features and suggest differentiation"
- "Compare our product to [competitor]"
- "Find gaps in competitor offerings"
- "Generate competitive positioning strategy"

## Usage Examples

### Example 1: Task Management Feature Analysis
**Input**: "Analyze competitors for new task management feature"
**Output**: Competitor landscape analysis identifying where existing tools fall short and how to position the new feature

### Example 2: Notion vs ClickUp Comparison
**Input**: "Track Notion vs ClickUp features and suggest differentiation"
**Output**: Side-by-side comparison with specific UVP recommendations based on each platform's strengths/weaknesses

### Example 3: SaaS Tool vs Slack Positioning
**Input**: "Compare our SaaS tool to Slack and suggest advantages"
**Output**: Integration-focused differentiation strategy highlighting specialized capabilities beyond Slack's general communication focus

## Best Practices / Notes

### When This Skill Adds Value
- Preparing for product launches with competitive positioning
- Identifying feature gaps in market before development
- Crafting marketing messages that highlight unique value
- Sales enablement materials to counter competitor objections
- Strategic planning sessions and board presentations

### Ethical Considerations
1. **Use public sources only** - Only analyze publicly available information
2. **Verify facts** - Don't make assumptions about competitor capabilities
3. **Focus on positive differentiation** - Emphasize your strengths, not competitor weaknesses
4. **Avoid disparagement** - Professional analysis maintains credibility

### Analysis Quality Tips
- Include recent data (changelogs from past 6 months)
- Note when information might be outdated
- Acknowledge assumptions made due to limited public info
- Update analyses regularly as competitive landscape evolves

### Differentiation Principles
- **Be specific**: "Better reporting" is weak; "Real-time dashboard with 20+ custom metrics" is strong
- **Focus on customer value**: Connect features to outcomes (save time, reduce errors, increase revenue)
- **Validate claims**: Ensure marketing messages match actual product capabilities

## Dependencies

- **No external dependencies required** - Text-based analysis using public information only
- **Optional Enhancement**: Web scraping tools or APIs for real-time data collection (if available and permitted)

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*Competitor analysis follows strategic frameworks from "Blue Ocean Strategy" and competitive intelligence best practices.*

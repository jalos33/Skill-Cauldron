# User Story Generator Skill

Turns vague ideas, feature requests, or business needs into clear, INVEST-compliant user stories with acceptance criteria.

## Description

The User Story Generator skill transforms vague product ideas, feature requests, and business requirements into well-structured, actionable user stories following agile best practices. It applies the **INVEST criteria** (Independent, Negotiable, Valuable, Estimable, Small, Testable) to ensure each story is ready for development and provides detailed acceptance criteria using Behavior-Driven Development (BDD) formats.

## Purpose

Product teams often struggle with converting fuzzy requirements into clear, implementable user stories. This skill helps by:
- **Enforcing INVEST principles**: Ensures every generated story meets quality standards
- **Identifying user personas**: Clarifies who the users are and what they need
- **Creating testable acceptance criteria**: Uses Given-When-Then format for BDD alignment
- **Grouping into epics**: Organizes related stories for larger features
- **Flagging gaps**: Identifies missing details requiring stakeholder clarification

Ideal for product managers, agile coaches, scrum masters, and development teams practicing agile methodologies.

## Features

- **Persona identification**: Automatically identifies primary, secondary, and external user types with their goals and pain points
- **INVEST compliance checking**: Validates each story against all six INVEST principles with detailed status tables
- **Standard story format enforcement**: Generates stories in "As a [persona], I want [goal] so that [benefit]" format
- **BDD acceptance criteria**: Creates Given-When-Then formatted scenarios or bullet-point alternatives
- **Epic grouping**: Organizes related stories into logical epics for features spanning multiple sprints
- **Gap analysis**: Identifies missing details and generates clarification questions for refinement sessions
- **Effort estimation support**: Provides story point estimates and priority rankings
- **Sprint allocation suggestions**: Recommends how to group stories across sprints based on dependencies

## How to Use

### Installation

```bash
curl -o skills/user-story-generator/SKILL.md https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/user-story-generator/SKILL.md
```

### Activation Phrases

Use any of these phrases to trigger the skill:
- "Generate user stories from this idea"
- "Turn this feature request into INVEST stories"
- "Create user stories with acceptance criteria"
- "Refine vague backlog items into stories"
- "Write INVEST-compliant stories for this goal"

### Example Usage

**User**: Generate user stories for a personalized recommendations feature

**Skill Response**: Generates comprehensive report including:
- Identified personas (frequent shoppers, new users, admin)
- User stories in standard format with clear benefits
- Given-When-Then acceptance criteria for each story
- INVEST compliance checklist for quality validation
- Clarification questions for backlog refinement

## Examples

### Example 1: Personalized Recommendations Feature

**Input**: "We need a personalized recommendations feature that suggests products based on user behavior"

**Output Summary**:

#### Story #1: Product Recommendations
**User Story**: As a frequent shopper, I want to see personalized product recommendations so that I can discover relevant items quickly without searching.

**Acceptance Criteria**:
```gherkin
Scenario: View recommended products on homepage
Given I am a logged-in user with browsing history
When I visit the homepage
Then I see a "Recommended for You" section with 5-10 products
And each recommendation is based on my past views/purchases
```

**INVEST Compliance**:
| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | ✓ | Can be developed without other stories |
| Negotiable | ✓ | Algorithm details open to discussion |
| Valuable | ✓ | Expected to increase conversion by 15% |

**Estimated Effort**: 5 story points
**Priority**: High

---

### Example 2: Better Search Functionality

**Input**: "Turn 'better search' into INVEST stories with criteria"

**Output Summary**:

#### Story #1: Advanced Search Filters
**User Story**: As a shopper, I want to filter search results by category, price range, and rating so that I can quickly narrow down relevant products.

**Acceptance Criteria**:
```gherkin
Scenario: Apply multiple filters to search results
Given I have performed a product search
When I apply category=Electronics AND price<=500 filters
Then the results show only electronics under $500
And filter badges display active selections
```

---

### Example 3: Mobile App Onboarding Flow

**Input**: "Create user stories for mobile app onboarding flow"

**Output Summary**:

#### Epic: Mobile App Onboarding Flow

**Story #1: First-time User Registration**
**User Story**: As a new mobile app visitor, I want to quickly register using email or social login so that I can start personalizing my experience immediately.

**Acceptance Criteria**:
```gherkin
Scenario: Register with email
Given I am on the onboarding screen
When I enter valid email and password
Then I receive a verification email
And upon verification, I proceed to profile setup
```

**Story #2: Profile Setup and Preferences**
**User Story**: As a newly registered user, I want to set my fitness goals and preferences so that recommendations are tailored to my needs.

---

## Output Format

The skill generates a structured markdown report containing:

1. **Executive Summary**: Overview of generated stories and key personas identified
2. **Identified Personas**: Table of user types with descriptions and technical levels
3. **User Stories**: Numbered stories with epic groupings, each including:
   - Standard "As a...I want...so that..." format
   - Given-When-Then acceptance criteria in Gherkin syntax
   - INVEST compliance checklist table
   - Estimated effort and priority ranking
4. **Missing Details & Clarification Questions**: Table of gaps requiring stakeholder input
5. **INVEST Compliance Summary**: Overall quality score and stories needing refinement
6. **Pre-Refinement Checklist**: Preparation items for backlog refinement sessions
7. **Suggested Sprint Allocation**: How to group stories across sprint cycles

## Best Practices

### When to Use This Skill

- Converting vague product ideas into actionable backlog items
- Refining feature requests from customers or stakeholders
- Breaking down epics into implementable stories
- Preparing for sprint planning or refinement sessions
- Creating documentation during discovery phases

### Core Principles

1. **Always include clear persona and benefit**: Every story must answer "who" and "why"
2. **Keep stories small and estimable**: Target 1-3 days of development work per story
3. **Use Given-When-Then for testability**: Ensures BDD alignment and clear acceptance criteria
4. **Refine with stakeholders before backlog entry**: Stories are conversation starters, not contracts
5. **Group into epics for larger features**: Maintain context across multiple sprints

### Story Splitting Techniques

When a story violates the "Small" criterion:
- **By User Type**: Separate stories for different user roles
- **By Functionality**: Break complex features into discrete capabilities
- **By Data State**: Handle different data conditions separately
- **By Workflow Stage**: Split across sequential steps in a process

## License

This skill is released under the MIT License. See [LICENSE](https://github.com/jalos33/Skill-Cauldron/blob/main/LICENSE) for details.

---

*This skill follows agile best practices from "User Stories Applied" by Mike Cohn, Scrum guidelines, and behavior-driven development (BDD) principles.*

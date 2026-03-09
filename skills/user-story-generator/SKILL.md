---
name: user-story-generator
description: Turns vague ideas, feature requests, or business needs into clear, INVEST-compliant user stories (Independent, Negotiable, Valuable, Estimable, Small, Testable) with acceptance criteria.
tags: [user-stories, agile, product-management, requirements, backlog]
author: Jose Quiñones
version: 1.0
license: MIT
---

# User Story Generator Skill

This skill transforms vague ideas, feature requests, and business needs into clear, INVEST-compliant user stories with detailed acceptance criteria, following agile best practices.

## Instructions

Follow this systematic approach to generate high-quality user stories from vague inputs:

### Step 1: Parse Input and Identify Core Elements

Extract key information from the input:
- **Idea/Feature Request**: What is being proposed?
- **Business Goal**: What problem are we solving or what value are we creating?
- **User Need**: Who experiences this need and why does it matter?
- **Context**: Any constraints, edge cases, or special conditions mentioned

### Step 2: Identify User Personas

Determine who the users are for each story. Consider:
- **Primary Users**: Direct users of the feature (e.g., "shopping customer," "new app user")
- **Secondary Users**: Indirectly affected users (e.g., "admin," "support agent")
- **External Users**: Systems or third parties that interact with the feature

For each persona, identify:
- Their role and responsibilities
- Their goals and pain points
- Their technical proficiency level
- Any special requirements or constraints

### Step 3: Apply INVEST Criteria

Evaluate and refine stories against INVEST principles:

**I - Independent**: Can this story be developed and tested separately?
- If dependent on other work, flag as "needs splitting"
- Suggest how to make it more independent

**N - Negotiable**: Is there room for discussion on implementation details?
- Avoid overly prescriptive language ("must use X technology")
- Focus on what, not how

**V - Valuable**: Does this deliver clear value to user or business?
- Ensure the "so that" benefit is explicit and meaningful
- Flag stories where benefit is unclear or weak

**E - Estimable**: Can we reasonably estimate effort?
- If too vague ("improve performance"), request clarification
- Suggest breaking into smaller, estimable pieces

**S - Small**: Is this story small enough for a sprint?
- Target: 1-3 days of development work per story
- Flag stories that are "epic-sized" and suggest splitting

**T - Testable**: Can we verify completion with acceptance criteria?
- Ensure clear pass/fail conditions exist
- If not testable, flag as needing refinement

### Step 4: Generate User Stories in Standard Format

For each identified story, create format:

```
As a [persona], I want [goal/feature] so that [benefit/value].
```

Example: "As a frequent shopper, I want to see personalized product recommendations so that I can discover relevant items quickly without searching."

Guidelines:
- **Persona**: Specific user type (not "user" or "customer")
- **Goal**: Clear action or capability desired
- **Benefit**: Explicit value proposition (never omit the "so that")

### Step 5: Define Acceptance Criteria

For each story, add acceptance criteria using one of these formats:

**Given-When-Then Format:**
```
Scenario: [Brief description]
Given [initial context]
When [action/condition]
Then [expected outcome]
```

**Bullet Point Format (for simpler stories):**
- Criteria 1: Clear, testable condition
- Criteria 2: Another verifiable requirement
- Criteria 3: Edge case handling

Acceptance criteria should be:
- **Specific**: No ambiguity in expected behavior
- **Testable**: Can be verified as pass/fail
- **Complete**: Covers happy path and key edge cases
- **User-focused**: Describes user-visible behavior, not implementation details

### Step 6: Group Related Stories into Epics (If Applicable)

For large features that span multiple stories:
- Create an "Epic" grouping with a summary description
- List all related stories under the epic
- Note any cross-story dependencies or sequencing requirements

Example Epic: "Mobile App Onboarding Flow"
- Story 1: First-time user registration
- Story 2: Profile setup and preferences
- Story 3: Tutorial walkthrough
- Story 4: Permission requests (notifications, location)

### Step 7: Flag Missing Details and Suggest Questions

Identify ambiguities and areas needing clarification:

**Common Clarification Areas:**
- **Scope boundaries**: What's in vs. out of scope?
- **User types**: Are there multiple personas we're missing?
- **Edge cases**: Special conditions, error states, limits?
- **Metrics**: How will success be measured?
- **Constraints**: Technical, regulatory, or timeline constraints?

**Suggested Question Format:**
> **Clarification Needed**: [Specific area needing detail]
> - Suggested questions: "What about...?", "Should we consider...?", "How should this handle...?"

### Step 8: Create INVEST Compliance Checklist

For each story, provide a compliance check:

| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | ✓ / ✗ | Can be developed separately? |
| Negotiable | ✓ / ✗ | Implementation details open to discussion? |
| Valuable | ✓ / ✗ | Clear user/business value? |
| Estimable | ✓ / ✗ | Sufficient detail for effort estimation? |
| Small | ✓ / ✗ | Fits within a sprint (1-3 days)? |
| Testable | ✓ / ✗ | Has clear acceptance criteria? |

### Step 9: Generate Refinement Notes

Provide guidance for backlog refinement sessions:

**Preparation Notes:**
- What information should stakeholders review before refinement?
- Which stories need technical spike or research?
- Are there dependencies on other teams or external systems?

**Risk Areas:**
- Stories with low confidence scores
- Features requiring new technology or expertise
- Edge cases that may cause implementation surprises

## Output Format

Generate a structured markdown report:

```markdown
# User Story Report: [Feature/Goal Name]

## Executive Summary
[Brief overview of generated stories, key personas identified, epic groupings]

---

## Identified Personas

| Persona | Description | Key Goals | Technical Level |
|---------|-------------|-----------|-----------------|
| [Persona 1] | [Description] | [Goals] | [Level: novice/intermediate/expert] |
| [Persona 2] | ... | ... | ... |

---

## User Stories

### Epic: [Epic Name - if applicable]

#### Story #1: [Story Title]

**User Story**: As a [persona], I want [goal] so that [benefit].

**Acceptance Criteria**:
```gherkin
Scenario: [Brief description]
Given [context]
When [action]
Then [expected outcome]
```

**INVEST Compliance**:
| Criterion | Status | Notes |
|-----------|--------|-------|
| Independent | ✓ | Can be developed without other stories |
| Negotiable | ✓ | Implementation details open to discussion |
| Valuable | ✓ | Clear value: improves discovery speed by ~40% |
| Estimable | ✓ | Sufficient detail for estimation |
| Small | ✓ | Estimated 2 days development |
| Testable | ✓ | Clear pass/fail criteria defined |

**Estimated Effort**: [X story points or Y hours]
**Priority**: High/Medium/Low
**Dependencies**: None / [List dependencies]

---

#### Story #2: [Story Title]

[Repeat format as above]

---

### Epic: [Second Epic Name - if applicable]

[Continue with additional epics]

---

## Missing Details & Clarification Questions

| Area | Issue | Suggested Questions |
|------|-------|---------------------|
| [Area 1] | [Description of missing detail] | • "Should we support...?"<br>• "What about edge case..."? |

**Key Questions to Resolve Before Sprint Planning**:
1. [Critical question requiring answer before development can begin]
2. [Important clarification that affects scope or implementation]
3. [Optional consideration that may influence design decisions]

---

## INVEST Compliance Summary

### Overall Story Quality Score: X/6 average

| Criterion | Stories Compliant | Total Stories | % Compliant |
|-----------|------------------|---------------|-------------|
| Independent | 5 | 6 | 83% |
| Negotiable | 6 | 6 | 100% |
| Valuable | 6 | 6 | 100% |
| Estimable | 4 | 6 | 67% |
| Small | 5 | 6 | 83% |
| Testable | 6 | 6 | 100% |

**Stories Needing Refinement**:
- Story #3: "Improve performance" - Too vague, needs specific metrics (e.g., "Load page in <2s")
- Story #5: "Export data to multiple formats" - May need splitting into separate stories per format

---

## Pre-Refinement Checklist

**Before discussing with stakeholders**:
- [ ] Review persona definitions for completeness
- [ ] Verify all acceptance criteria are testable
- [ ] Identify any technical spikes needed
- [ ] Confirm cross-team dependencies mapped

**Information to gather before refinement session**:
1. [Specific data or research needed]
2. [Stakeholder availability for decision-making]
3. [Technical constraints to communicate upfront]

---

## Suggested Sprint Allocation

Based on story sizes and dependencies:

### Sprint 1 (Foundation)
- Story #1: Core functionality
- Story #2: Essential supporting feature
**Estimated Capacity**: X story points

### Sprint 2 (Enhancement)
- Story #3: Advanced capability
- Story #4: Edge case handling
**Estimated Capacity**: Y story points

---

*User story generation completed by: User Story Generator Skill*
*Date: YYYY-MM-DD*
*Stories generated: [N] | Epics identified: [M]*
```

## Best Practices

### When to Use This Skill
- Converting vague product ideas into actionable backlog items
- Refining feature requests from customers or stakeholders
- Breaking down epics into implementable stories
- Preparing for sprint planning or refinement sessions
- Creating documentation for new features during discovery

### Core Principles

1. **Always include clear persona and benefit**: Every story must answer "who" and "why." A story without a clear user type or value proposition is not ready for development.

2. **Keep stories small and estimable**: If a story cannot be estimated with reasonable confidence, it's too large. Split into smaller pieces that can each be completed within 1-3 days of work.

3. **Use Given-When-Then for testable criteria**: This format ensures acceptance criteria are specific, testable, and aligned with behavior-driven development (BDD) practices.

4. **Refine with stakeholders before backlog entry**: User stories are conversation starters, not contracts. Use this output as input for refinement discussions with product owners, engineers, and testers.

5. **Group into epics for larger features**: Features spanning multiple sprints should be organized under epics to maintain context and identify cross-story dependencies.

### Story Splitting Techniques

When a story violates the "Small" criterion:

**By User Type**:
- Original: "As a user, I want to manage my account settings" (too broad)
- Split into:
  - "As a user, I want to update my profile picture"
  - "As a user, I want to change my password"
  - "As an admin, I want to view all user accounts"

**By Functionality**:
- Original: "As a shopper, I want to complete checkout" (too broad)
- Split into:
  - "As a shopper, I want to enter shipping address"
  - "As a shopper, I want to select payment method"
  - "As a shopper, I want to review order before purchase"

**By Data State**:
- Original: "As a user, I want to search for content" (too broad)
- Split into:
  - "As a user, I want to search by keyword"
  - "As a user, I want to filter results by category"
  - "As a user, I want to sort results by relevance/date"

**By Workflow Stage**:
- Original: "As a customer, I want to return an item" (too broad)
- Split into:
  - "As a customer, I want to initiate a return request"
  - "As a customer, I want to print return shipping label"
  - "As a support agent, I want to process refund approval"

### Common Patterns and Templates

**Authentication & Authorization**:
- As a [user type], I want to [authenticate/authorize] so that [security/benefit].
- Acceptance: Account creation, login/logout, password reset, role-based access

**Search & Discovery**:
- As a [user type], I want to [search/filter/sort] so that I can [find/discover] [content/items].
- Acceptance: Search box, filter options, sort order, no-results handling

**Data Entry & Forms**:
- As a [user type], I want to [enter/submit/correct] data so that my information is [accurate/saved/processed].
- Acceptance: Form validation, error messages, save/draft capability, submission confirmation

**Notifications & Alerts**:
- As a [user type], I want to receive [notification type] when [trigger event] so that I can [action/outcome].
- Acceptance: Notification delivery, user preferences, quiet hours, unsubscribe option

### INVEST Violation Patterns and Fixes

| Violation | Warning Signs | Fix Strategy |
|-----------|---------------|--------------|
| **Not Independent** | Story blocked by other work; team says "can't start until X is done" | Split into separate stories with clear boundaries; identify prerequisite work as parent story |
| **Not Negotiable** | Overly specific implementation details ("must use REST API," "use React component") | Refocus on user need; move technical decisions to spike or implementation discussion |
| **Not Valuable** | Weak "so that" clause ("so that the system works"); unclear business value | Work with product owner to articulate clear user/business benefit; consider if story should be dropped |
| **Not Estimable** | Story is vague or missing key details; team cannot give confidence range | Request clarification on scope, edge cases, and constraints; break into smaller pieces until estimable |
| **Not Small** | Story spans multiple days/weeks of work; cannot fit in sprint | Split by user type, functionality, data state, or workflow stage (see techniques above) |
| **Not Testable** | No clear acceptance criteria; subjective success measures ("improve performance") | Define specific, measurable criteria with pass/fail conditions; use Given-When-Then format |

### Story Writing Tips

**Do**:
- Use specific user types: "frequent shopper," "new app user," "admin" instead of generic "user"
- Make benefits explicit: "so that I can complete purchases 2x faster" not just "for better experience"
- Focus on user outcome, not system behavior: "I want to see my order status" not "the system displays status"
- Keep language simple and unambiguous
- Include edge cases in acceptance criteria

**Don't**:
- Use vague terms like "user-friendly," "fast," "modern" without definitions
- Specify implementation details as requirements ("use MongoDB for storage")
- Combine multiple user needs into one story
- Omit the "so that" benefit clause
- Write stories that require extensive research to understand

---

*This skill follows agile best practices from "User Stories Applied" by Mike Cohn, Scrum guidelines, and behavior-driven development (BDD) principles.*

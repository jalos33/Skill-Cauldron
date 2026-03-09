---
name: requirement-harvester
description: Extracts clear, structured business rules, decision logic, and requirements from raw documents, emails, meeting notes, or user stories.
tags: [requirements, business-rules, analysis, product-management, documentation]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Requirement Harvester Skill

Extracts clear, structured business rules, decision logic, and requirements from raw documents, emails, meeting notes, or user stories.

## Instructions

Follow these steps to harvest structured requirements from unstructured input:

### Step 1: Read Raw Input Text
- Accept any text-based source: product briefs, emails, meeting transcripts, Jira tickets, user stories, RFCs, or documentation
- Identify the source type and context (e.g., stakeholder email vs. technical spec)
- Note any explicit requirements already stated clearly

### Step 2: Identify Key Entities
Extract these core elements from the text:

**Actors/Users:**
- Who performs actions? (customers, admins, system, third parties)
- What roles or personas are involved?

**Actions:**
- What operations are performed? (create, update, delete, approve, notify)
- What workflows or processes are described?

**Conditions:**
- What rules govern behavior? (eligibility criteria, validation rules, constraints)
- What states trigger different outcomes?

**Outcomes:**
- What results should occur? (success messages, data changes, notifications)
- What error conditions exist?

### Step 3: Extract Business Rules
Format each rule using one of these structures:

**Given-When-Then Format (for behavior):**
```
Given [context/initial state]
When [action/event occurs]
Then [expected outcome/result]
```

**Numbered List Format (for constraints/rules):**
1. Rule statement with clear condition and outcome
2. Another rule with specific criteria
3. Continue for all identified rules

### Step 4: Detect Ambiguities and Questions
Flag any unclear or incomplete requirements:

**Ambiguity Types:**
- Vague terms ("fast," "user-friendly," "soon")
- Conflicting statements (two rules that contradict)
- Missing details (no error handling specified)
- Undefined states (what happens in edge cases?)

**For each ambiguity, generate clarifying questions:**
- What should happen when [edge case]?
- Who is responsible for [action] if [condition]?
- How do we measure "acceptable" performance?

### Step 5: Group Related Rules into Categories
Organize rules into these categories:

| Category | Description | Examples |
|----------|-------------|----------|
| **Functional** | System behaviors and features | User can reset password via email link |
| **Non-Functional** | Performance, reliability, usability | Page loads in under 2 seconds |
| **Data** | Data requirements and constraints | Customer email must be unique |
| **Workflow** | Process flows and approvals | Manager approval required for orders >$500 |
| **Security** | Access control and protection | Only admins can view sensitive data |

### Step 6: Generate Traceability Matrix
Link each rule back to its source text location:

| Rule ID | Category | Rule Description | Source Location | Priority |
|---------|----------|------------------|-----------------|----------|
| R-001 | Functional | User can reset password | Email from Sarah, para 3 | High |
| R-002 | Security | Password must be 8+ chars | Meeting notes, section 2 | High |

### Step 7: Output Structured Markdown Report
Generate a complete report with these sections:

1. **Executive Summary**: Brief overview of harvested requirements
2. **Actors/Users Identified**: List all roles/personas found
3. **Business Rules**: Organized by category with Given-When-Then format
4. **Ambiguities & Questions**: Clear list of items needing clarification
5. **Traceability Matrix**: Rule-to-source mapping for verification
6. **Recommended Next Steps**: Suggested actions (stakeholder interviews, user research)

## Activation phrases / When to use
Use this skill when you need to:
- Harvest requirements from this document
- Extract business rules from these notes
- Turn user stories into structured requirements
- Analyze this email for decision logic
- Generate rule list from meeting transcript

## Usage Examples

| Input | Expected Output |
|-------|-----------------|
| "Harvest requirements from this product brief PDF" | Structured requirement document with functional rules, data requirements, and clarification questions about edge cases |
| "Extract business rules from these stakeholder emails" | Categorized rule list (workflow, security, data) with source attribution for each rule extracted from email threads |
| "Turn Jira tickets into structured requirements" | Consolidated requirement set merging multiple related tickets, eliminating duplicate rules, identifying conflicts between tickets |
| "Analyze meeting notes for workflow decisions" | Workflow diagrams in Mermaid format, decision trees, approval chain definitions with clear role responsibilities |

## How it works

```
┌─────────────────────────────────────────────────────────────────┐
│                   REQUIREMENT HARVESTING WORKFLOW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐                                               │
│  │ Raw Input    │  Email, docs, notes, tickets, transcripts     │
│  │ Text         │                                                 │
│  └──────┬───────┘                                               │
│         ▼                                                       │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ Parse &      │──▶│ Identify     │                           │
│  │ Analyze      │    │ Entities:    │                           │
│  └──────┬───────┘    │ Actors,      │                           │
│         │            │ Actions,     │                           │
│         │            │ Conditions   │                           │
│         ▼            └──────────────┘                           │
│  ┌──────────────┐                                               │
│  │ Extract      │                                                │
│  │ Business     │                                                │
│  │ Rules        │                                                │
│  └──────┬───────┘                                                │
│         ▼                                                        │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ Detect       │──▶│ Group by     │                           │
│  │ Ambiguities  │    │ Categories   │                           │
│  └──────┬───────┘    └──────────────┘                           │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │ Generate     │                                                │
│  │ Report       │                                                │
│  └──────┬───────┘                                                │
│         ▼                                                        │
│  ┌──────────────┐                                               │
│  │ Structured   │  Markdown report with rules, questions,      │
│  │ Output       │  traceability matrix                          │
│  └──────────────┘                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Step-by-step process:**
1. **Parses unstructured text** (docs, emails, notes, transcripts) from any source type
2. **Identifies actors, actions, conditions, outcomes** using pattern recognition
3. **Formats rules as Given-When-Then** for behavioral requirements or numbered lists for constraints
4. **Groups rules by category** (functional, non-functional, data, security, workflow)
5. **Flags ambiguities** with vague terms, conflicts, and missing details; generates clarifying questions
6. **Outputs markdown report** containing: rule list, category summary, stakeholder questions, traceability matrix

## Dependencies
- None required (text analysis only)
- Optional: NLP libraries (spaCy, NLTK) for advanced entity extraction and sentiment analysis

## Best Practices / Notes

### Requirement Quality Guidelines
- **Always list ambiguities and questions**: Never assume; document what needs clarification
- **Use consistent rule format**: Stick to Given-When-Then or numbered lists throughout
- **Trace rules back to source text**: Every requirement should link to its origin for verification
- **Group rules by feature or module**: Organize logically for implementation teams

### Rule Format Standards
```markdown
## Functional Requirements

### User Authentication
**R-001: Email-based login**
Given a registered user with valid credentials
When they submit the login form with their email and password
Then they are authenticated and redirected to the dashboard

**R-002: Password reset via email**
Given a user who has forgotten their password
When they request a password reset from the login page
Then they receive an email with a time-limited reset link (valid for 24 hours)
```

### Ambiguity Detection Patterns
| Pattern Type | Example | Question to Ask |
|--------------|---------|-----------------|
| Vague timeline | "Process quickly" | What is the acceptable response time? (e.g., <500ms, <2 seconds) |
| Undefined actor | "The system should validate" | Which user role performs validation? Admin, automated check, or end-user? |
| Missing edge case | "User can upload a file" | What happens with files >10MB? Unsupported formats? Network interruption? |
| Contradictory rules | Rule A says X, Rule B says Y | Can we reconcile these requirements or is there a specific condition for each? |

### Category Definitions

**Functional Requirements:**
- Describe system behaviors and features
- Answer "What should the system do?"
- Example: "Users can search products by category"

**Non-Functional Requirements:**
- Define quality attributes (performance, reliability, usability)
- Answer "How well should the system work?"
- Example: "Search results display within 200ms for 95% of queries"

**Data Requirements:**
- Specify data storage, validation, and lifecycle rules
- Answer "What data is needed and how is it managed?"
- Example: "Customer email addresses must be validated against RFC 5322"

**Workflow Requirements:**
- Define process flows, approvals, and state transitions
- Answer "How do tasks move through the system?"
- Example: "Orders over $1000 require manager approval before fulfillment"

**Security Requirements:**
- Specify access control, authentication, and protection measures
- Answer "What security constraints apply?"
- Example: "API endpoints require JWT token in Authorization header"

### Output Template Structure

```markdown
# Requirement Harvesting Report

## Source Documents Analyzed
- [Document 1 name and location]
- [Document 2 name and location]

## Executive Summary
[Brief overview of key requirements identified]

## Actors/Users Identified
| Role | Description | Key Actions |
|------|-------------|-------------|
| ... | ... | ... |

## Business Rules by Category

### Functional Requirements
[Rule list with Given-When-Then format]

### Non-Functional Requirements
[Performance, reliability targets]

### Data Requirements
[Data rules and constraints]

### Workflow Requirements
[Process flows and approvals]

### Security Requirements
[Access control and protection rules]

## Ambiguities & Clarification Questions
| # | Rule Reference | Issue Type | Question | Priority |
|---|----------------|------------|----------|----------|
| 1 | R-003 | Vague timeline | What is acceptable response time? | High |
| 2 | R-007 | Missing edge case | How handle files >50MB? | Medium |

## Traceability Matrix
| Rule ID | Category | Description | Source Location | Priority |
|---------|----------|-------------|-----------------|----------|
| R-001 | Functional | User login | Email from Sarah, para 3 | High |
| ... | ... | ... | ... | ... |

## Recommended Next Steps
1. Schedule requirements clarification session with [stakeholder names]
2. Conduct user research for [specific use cases]
3. Review technical feasibility of [complex requirements]
4. Prioritize backlog based on identified rules
```

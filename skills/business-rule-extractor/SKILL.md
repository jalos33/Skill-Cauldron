---
name: business-rule-extractor
description: Simplifies complex legal, business, policy, or process documents into clear, structured lists of business rules, decision logic, and conditions.
tags: [business-rules, requirements, analysis, documentation, compliance]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Business Rule Extractor Skill

Simplifies complex legal, business, policy, or process documents into clear, structured lists of business rules, decision logic, and conditions.

## Instructions

Follow this structured process to extract and organize business rules from unstructured text:

### Step 1: Parse Raw Input Text

Read through the provided document (legal docs, policies, contracts, process descriptions, regulations) and identify key sections:

**Document Types:**
- Legal agreements and terms of service
- Business policies and procedures
- Regulatory compliance documents
- Process descriptions and workflows
- Contract clauses and SLAs
- API specifications with validation rules

**Initial Analysis:**
- Identify document structure (sections, subsections, numbered clauses)
- Note any explicit rule numbering or formatting
- Flag ambiguous language or cross-references to other sections

### Step 2: Identify Conditional Patterns

Search for linguistic patterns that indicate business rules:

**Condition Indicators:**
| Pattern | Example | Rule Type |
|---------|---------|-----------|
| "If/When" | "If the order exceeds $500..." | Decision logic |
| "Must/Must not" | "Customer must verify email within 48 hours" | Mandatory requirement |
| "Shall/Shall not" | "Provider shall respond within 24 hours" | Contractual obligation |
| "Should/Should not" | "System should log all failed attempts" | Recommendation |
| "May/Might" | "Administrator may revoke access" | Permission/discretionary |
| "Except/BUT" | "Free shipping, except for oversized items" | Exception handling |
| "Unless" | "No refund unless product is defective" | Conditional exclusion |
| "Upon/After/Before" | "After 30 days, subscription auto-renews" | Time-based rules |

**Rule Structure Patterns:**
- **Simple condition**: "If X, then Y"
- **Nested conditions**: "If X and Y, but not Z, then W"
- **Multiple outcomes**: "If X then A; otherwise if Y then B"
- **Default behavior**: "In all cases except where stated, assume..."

### Step 3: Extract Rules in Structured Format

Convert identified rules into standardized format:

**Preferred Format: When-Then-Else**

```
Rule: [Brief description]
When: [Condition that triggers the rule]
Then: [Required action or outcome]
Else: [Alternative outcome, if applicable]
Source: [Document section reference]
```

**Alternative Format (Numbered List):**
For simpler documents where When-Then-Else feels forced:

1. **Rule Title**: Description of what this rule governs
   - Condition: The trigger scenario
   - Action: Required response or outcome
   - Source: Reference location

### Step 4: Categorize Rules by Type

Group extracted rules into functional categories for organization:

**Category Definitions:**

| Category | Purpose | Examples |
|----------|---------|----------|
| **Validation** | Data/entry requirements | "Email must be valid format", "Age must be 18+" |
| **Calculation** | Mathematical computations | "Tax = price × rate", "Discount = quantity × $5" |
| **Workflow** | Process steps and sequencing | "After approval, send notification", "Before shipment, verify inventory" |
| **Compliance** | Legal/regulatory requirements | "Records retained for 7 years", "GDPR consent required" |
| **Eligibility** | Qualification criteria | "Must be member for 90 days", "Orders under $100 excluded" |
| **Prohibition** | Forbidden actions | "Cannot modify after submission", "No refunds on sale items" |

### Step 5: Identify Ambiguities and Conflicts

Flag unclear language, contradictions, or missing information:

**Ambiguity Types:**

| Pattern | Example | Issue Type | Suggested Clarification |
|---------|---------|------------|------------------------|
| Vague timeframe | "Process quickly" | Unclear timing | Define acceptable response time (e.g., <2 hours) |
| Undefined threshold | "Large orders" | Missing numeric value | Specify exact amount ($500+) |
| Contradictory rules | Rule A says X, Rule B says Y | Conflict | Determine which takes precedence or conditions for each |
| Missing exception handling | "All items returnable" (but sale items exist) | Incomplete scope | Clarify exclusions and edge cases |
| Circular reference | See section 5.2 (which refers back to 5.1) | Unclear dependency | Resolve cross-reference chain |

**Conflict Detection:**
- Compare rules for mutually exclusive conditions
- Check if exceptions override base rules correctly
- Verify time-based rules don't overlap incorrectly

### Step 6: Reference Source Text

Create traceability mapping between extracted rules and source document:

| Rule ID | Category | Extracted Rule | Source Location | Line/Section | Confidence |
|---------|----------|----------------|-----------------|--------------|------------|
| R-001 | Eligibility | Must be member for 90 days | Terms of Service, Section 3.2 | Lines 45-47 | High |
| R-002 | Calculation | $5 shipping discount per item | Shipping Policy, Clause 8 | Lines 112-114 | Medium (ambiguous "per item") |

**Confidence Levels:**
- **High**: Clear language, unambiguous interpretation
- **Medium**: Some ambiguity but reasonable interpretation possible
- **Low**: Vague or contradictory; requires expert review

### Step 7: Generate Structured Report

Compile comprehensive business rule analysis with all components:

**Report Structure:**
1. Executive summary of extracted rules and key findings
2. Complete categorized rule list in standardized format
3. Ambiguity/conflict log with clarification questions
4. Traceability matrix linking rules to source text
5. Recommended next steps for validation and refinement

## Activation phrases / When to use

Use this skill when you need to:
- Extract business rules from this document
- Simplify this policy into rules
- Pull decision logic from these legal terms
- Harvest rules from this process description
- List compliance requirements from this regulation

## Usage Examples

| Input | Expected Output |
|-------|-----------------|
| "Extract business rules from this refund policy document" | Categorized rule list: Eligibility (30-day window, original condition), Calculation (restocking fees by category), Workflow (approval chain for exceptions); source references to specific clauses; clarification questions about "original condition" definition |
| "Simplify tax compliance rules from this legal text" | Compliance-focused rules organized by jurisdiction; calculation formulas for each tax type; effective dates and threshold amounts; ambiguity flags on ambiguous rate definitions; traceability matrix linking rules to statute citations |
| "Pull workflow conditions from this onboarding process" | Sequential workflow rules with decision points; validation requirements at each step; exception handling paths (skipped steps, retries); source references to process documentation sections; questions about edge case handling |
| "Harvest validation rules from this API specification" | Input validation rules for each endpoint and field; data type constraints; required vs optional fields; error code mappings; ambiguity flags on undefined behavior for edge cases |

## How it works

```
+------------------------------------------------------------------+
|                   BUSINESS RULE EXTRACTION WORKFLOW              |
+------------------------------------------------------------------+
|                                                                  |
|  STEP 1: PARSE INPUT                                             |
|  +----------------+                                              |
|  | Read Document  | -> Identify sections, structure, explicit    |
|  | Structure      |   rule numbering                             |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 2: IDENTIFY PATTERNS                                       |
|  +----------------+    Search for "If/When", "Must/Shall",        |
|  | Conditional    |    "Except", time-based patterns             |
|  | Pattern Match  |                                              |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 3: EXTRACT RULES                                           |
|  +----------------+    Convert to When-Then-Else format;          |
|  | Extract Rules  |    number and title each rule                |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 4: CATEGORIZE                                              |
|  +----------------+    Group by Validation, Calculation,          |
|  | Categorize     |    Workflow, Compliance, Eligibility         |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 5: FLAG AMBIGUITIES                                        |
|  +----------------+    Identify vague terms, contradictions,      |
|  | Ambiguity      |    missing information; generate questions   |
|  | Detection      |                                              |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 6: TRACE TO SOURCE                                         |
|  +----------------+    Create mapping between rules and source    |
|  | Traceability   |   document locations with confidence levels  |
|  +----------------+                                              |
|           |                                                       |
|           v                                                        |
|  STEP 7: OUTPUT REPORT                                           |
|  +----------------+    Executive summary, categorized rules,      |
|  | Generate Report|    ambiguity log, traceability matrix        |
|  +----------------+                                              |
|                                                                  |
|  OUTPUT: Structured markdown report with rule list and questions |
|                                                                  |
+------------------------------------------------------------------+
```

**Step-by-step process:**
1. **Parse input text**: Read document structure, identify sections and explicit rule numbering
2. **Identify conditional patterns**: Search for linguistic indicators (If/When, Must/Shall, Except, Unless)
3. **Extract rules in format**: Convert to When-Then-Else standardized format with titles
4. **Categorize by type**: Group into Validation, Calculation, Workflow, Compliance, Eligibility, Prohibition categories
5. **Flag ambiguities/conflicts**: Detect vague terms, contradictions, missing information; generate clarification questions
6. **Reference source text**: Create traceability matrix linking rules to document sections with confidence levels
7. **Generate structured report**: Executive summary, categorized rule list, ambiguity log, traceability matrix

## Dependencies

- None required (text pattern analysis only)
- Optional: NLP tools for advanced parsing and semantic analysis

## Best Practices / Notes

### Rule Extraction Principles

- **Use consistent rule format**: Standardize on When-Then-Else or numbered format throughout for readability
- **Always trace to source text**: Every extracted rule must reference its origin for verification and debate
- **Flag ambiguities proactively**: Never assume clarity; document what needs confirmation with specific questions
- **Group by functional area**: Organize rules logically (validation, calculation, workflow) for implementation teams
- **Review with domain experts**: Extracted rules should be validated by subject matter before finalizing

### When-Then-Else Format Guidelines

**Best Practices:**

| Aspect | Recommendation | Example |
|--------|----------------|---------|
| Condition clarity | Be specific and testable | "When order total exceeds $500" not "When large order" |
| Action precision | Define exact outcome | "Then apply 10% discount" not "Then give discount" |
| Else coverage | Include fallback when needed | "Else, standard shipping applies" for non-matching cases |
| Source reference | Always cite location | "Source: Shipping Policy v2.3, Section 4.1" |

**Template:**
```
[RULE-ID] Rule Title
- When: [Specific condition that triggers rule]
- Then: [Required action or outcome]
- Else: [Alternative outcome, if applicable]
- Source: [Document name, section, line numbers]
- Confidence: High/Medium/Low
```

### Category Selection Guide

**Choose category based on primary purpose:**

| If the rule... | Use this category |
|----------------|-------------------|
| Validates input data or entry requirements | Validation |
| Performs mathematical computation | Calculation |
| Defines process steps or sequencing | Workflow |
| Addresses legal/regulatory obligations | Compliance |
| Sets qualification criteria | Eligibility |
| Prohibits certain actions | Prohibition |

**Note:** Some rules may span multiple categories; list under primary category and cross-reference secondary.

### Ambiguity Detection Patterns

**Common Vague Terms to Flag:**

- "Quickly" / "Promptly" - Define acceptable timeframes
- "Reasonable" / "Appropriate" - Specify objective criteria
- "Large" / "Small" - Provide numeric thresholds
- "Frequently" / "Occasionally" - Define frequency metrics
- "Significant" / "Material" - Establish percentage or dollar thresholds

**Contradiction Patterns:**

| Pattern | Example | Resolution Approach |
|---------|---------|---------------------|
| Direct conflict | Rule A: Must approve; Rule B: Never approve without manager sign-off | Determine context conditions for each rule |
| Scope overlap | Both rules apply to same scenario but prescribe different actions | Establish precedence hierarchy |
| Time mismatch | Rule expires before renewal rule activates | Clarify transition period handling |

### Traceability Best Practices

- **Use specific references**: "Terms of Service, Section 3.2, Lines 45-47" not just "Section 3"
- **Include confidence levels**: Helps prioritize which rules need expert review
- **Note interpretation choices**: Document reasoning when multiple interpretations possible
- **Link related rules**: If Rule A depends on Rule B, note the dependency

### Recommended Review Process

1. **Initial extraction**: Run skill to get first-pass rule list
2. **Internal review**: Team validates categorization and format consistency
3. **Domain expert validation**: Subject matter expert confirms accuracy and completeness
4. **Stakeholder alignment**: Business stakeholders confirm rules match operational reality
5. **Implementation planning**: Development/operations teams confirm rules are actionable

### Common Pitfalls to Avoid

| Pitfall | Why It's Bad | How to Avoid |
|---------|--------------|--------------|
| Over-extraction | Too many minor rules overwhelm implementation | Focus on decision-impacting rules; exclude obvious defaults |
| Under-categorization | Rules too generic to implement usefully | Use specific categories; allow cross-referencing where needed |
| Missing edge cases | Rules work for happy path but fail at boundaries | Actively search for exception language and "except" clauses |
| Ignoring conflicts | Contradictory rules cause implementation errors | Compare all rules systematically; flag any apparent contradictions |
| No source traceability | Cannot verify or debate extracted rules | Always include document section references from extraction start |

### Rule Validation Checklist

Before finalizing extracted rules:

- [ ] All decision points captured with clear conditions
- [ ] Each rule has single, unambiguous action/outcome
- [ ] Exception handling explicitly defined where applicable
- [ ] Time-based rules specify exact durations/dates
- [ ] Numeric thresholds are concrete values not vague terms
- [ ] Source references enable direct verification of each rule
- [ ] Ambiguities clearly flagged with specific clarification questions
- [ ] Confidence levels assigned based on language clarity

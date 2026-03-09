# Business Rule Extractor Skill

Simplifies complex legal, business, policy, or process documents into clear, structured lists of business rules, decision logic, and conditions.

## Purpose

The Business Rule Extractor skill helps analysts, product managers, compliance officers, and legal professionals systematically identify, extract, and organize business rules from unstructured documents. It transforms verbose policies, contracts, and regulations into actionable rule catalogs with full traceability to source text.

## Features

- **Document Parsing**: Automatically identifies document structure (sections, subsections, numbered clauses)
- **Pattern Recognition**: Detects conditional language patterns (If/When, Must/Shall, Except, Unless, time-based indicators)
- **Standardized Formatting**: Converts rules to When-Then-Else format for clarity and implementation readiness
- **Multi-dimensional Categorization**: Groups rules by type (Validation, Calculation, Workflow, Compliance, Eligibility, Prohibition)
- **Ambiguity Detection**: Flags vague terms, contradictions, missing information with specific clarification questions
- **Source Traceability**: Links every extracted rule to its document origin with confidence scoring
- **Structured Reports**: Generates comprehensive markdown reports with executive summaries and action items

## How to Use

### Installation

```bash
curl -o ~/.claude/skills/business-rule-extractor.skill \
  https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/business-rule-extractor/SKILL.md
```

Or manually copy `SKILL.md` contents to your Claude skills directory.

### Activation Phrases

Use any of these phrases to activate the skill:

- "Extract business rules from this document"
- "Simplify this policy into rules"
- "Pull decision logic from these legal terms"
- "Harvest rules from this process description"
- "List compliance requirements from this regulation"

### Example Usage

After installation, specify your document context:

```
Extract business rules from this refund policy document

[Include the full refund policy text or paste the document content]
```

The skill will generate a complete analysis with categorized rules, ambiguity flags, and source traceability.

## Examples

### Refund Policy Analysis

**Input:** "Extract business rules from this refund policy document"

**Output includes:**

- **Eligibility Rules**: 30-day return window, original condition requirement, receipt verification
- **Calculation Rules**: Restocking fees (15% for opened items, 0% for defective), shipping cost handling by category
- **Workflow Rules**: Approval chain for exceptions (>7 days, past sale period), refund method determination logic
- **Ambiguity Flags**: "Original condition" definition needed; "defective" criteria clarification; exception approval authority specification
- **Source Traceability**: Each rule linked to specific policy sections and line numbers

### Tax Compliance Extraction

**Input:** "Simplify tax compliance rules from this legal text"

**Output includes:**

- Jurisdiction-specific compliance requirements (Sales tax, VAT, GST thresholds)
- Calculation formulas for each tax type with effective dates
- Record retention requirements by document type
- Ambiguity flags on rate definitions and exemption criteria
- Traceability matrix linking rules to statute citations

### Onboarding Process Analysis

**Input:** "Pull workflow conditions from this onboarding process"

**Output includes:**

- Sequential workflow rules with decision points (account verification, document upload, training completion)
- Validation requirements at each step (email format, ID type acceptance, file size limits)
- Exception handling paths (skipped steps, retry limits, escalation procedures)
- Source references to process documentation sections
- Questions about edge case handling (what happens on step 3 failure?)

### API Specification Rules

**Input:** "Harvest validation rules from this API specification"

**Output includes:**

- Input validation rules for each endpoint and field
- Data type constraints and format requirements
- Required vs optional field mappings
- Error code mappings with trigger conditions
- Ambiguity flags on undefined behavior for edge cases

## Output Format

The skill generates a structured markdown report:

```markdown
# Business Rule Analysis Report: [Document Name]

## Executive Summary
[Overview of extracted rules, key categories, and critical ambiguities]

## Extracted Rules by Category

### Validation Rules
- **R-001**: [Rule title]
  - When: [Condition]
  - Then: [Action]
  - Source: [Document reference]
  - Confidence: High/Medium/Low

### Calculation Rules
- **R-002**: [Rule title]
  - When: [Condition]
  - Then: [Formula/Calculation]
  - Source: [Document reference]
  - Confidence: High/Medium/Low

[Additional categories as applicable...]

## Ambiguity and Conflict Log

| Rule ID | Issue Type | Location | Clarification Needed |
|---------|------------|----------|---------------------|
| R-001 | Vague term | Section 3.2 | Define "promptly" timeframe |
| R-005 | Contradiction | Sections 4.1 vs 4.3 | Establish precedence |

## Traceability Matrix

| Rule ID | Category | Source Document | Section | Lines | Confidence |
|---------|----------|-----------------|---------|-------|------------|
| R-001 | Eligibility | Refund Policy v2.1 | Section 3 | 45-47 | High |

## Recommended Next Steps

1. [Specific action item with owner and timeline]
2. [Follow-up analysis or stakeholder review needed]
3. [Implementation planning considerations]
```

## Best Practices

### When to Use This Skill

Use the Business Rule Extractor when you need to:

- Convert verbose policies into implementable rules for development teams
- Identify compliance requirements from regulatory documents
- Extract decision logic from legal contracts or terms of service
- Simplify complex processes into clear workflow rules
- Prepare requirements documentation from unstructured source material
- Identify ambiguities and gaps before implementation begins

### Core Principles

1. **Standardize rule format**: Use When-Then-Else consistently for clarity
2. **Maintain traceability**: Every rule must link to its document origin
3. **Flag uncertainties proactively**: Document what needs clarification early
4. **Categorize for actionability**: Group by function (validation, calculation, workflow)
5. **Validate with stakeholders**: Extracted rules should be reviewed by subject matter experts

### Rule Format Guidelines

**When-Then-Else Template:**

```
[RULE-ID] Rule Title
- When: [Specific, testable condition]
- Then: [Required action or outcome]
- Else: [Alternative outcome, if applicable]
- Source: [Document name, section, lines]
- Confidence: High/Medium/Low
```

**Best Practices:**

| Aspect | Recommendation | Example |
|--------|----------------|---------|
| Condition clarity | Be specific and testable | "When order exceeds $500" not "When large order" |
| Action precision | Define exact outcome | "Then apply 10% discount" not "Then give discount" |
| Else coverage | Include fallback when needed | "Else, standard shipping applies" |
| Source reference | Always cite location | "Source: Policy v2.3, Section 4.1, Lines 45-47" |

### Ambiguity Detection

**Common Vague Terms to Flag:**

- "Quickly" / "Promptly" - Define acceptable timeframes (e.g., <2 hours)
- "Reasonable" / "Appropriate" - Specify objective criteria
- "Large" / "Small" - Provide numeric thresholds ($500+)
- "Frequently" / "Occasionally" - Define frequency metrics
- "Significant" / "Material" - Establish percentage or dollar thresholds

### Review Process

1. **Initial extraction**: Run skill to get first-pass rule list
2. **Internal review**: Team validates categorization and format consistency
3. **Domain expert validation**: Subject matter expert confirms accuracy
4. **Stakeholder alignment**: Business stakeholders confirm operational reality
5. **Implementation planning**: Development teams confirm actionability

## License

MIT License

See [SKILL.md](SKILL.md) for full license text.

## Repository

This skill is part of the Skill-Cauldron project: https://github.com/jalos33/Skill-Cauldron

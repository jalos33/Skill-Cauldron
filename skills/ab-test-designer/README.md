# A/B Test Designer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/ab-test-designer)

A Claude Code skill that **creates complete A/B test experiment plans** including hypothesis definition, variant design, success metrics specification, sample size calculation, duration estimation, statistical power analysis, and comprehensive analysis guidelines. It guides product teams through the entire experimental design process to ensure statistically valid and actionable results.

## Purpose

This skill helps product managers, data scientists, and engineers design rigorous A/B tests by:
- Defining clear, testable hypotheses with proper rationale
- Selecting appropriate primary, secondary, and guardrail metrics
- Calculating required sample sizes using power analysis
- Estimating realistic test durations accounting for weekly patterns
- Identifying common pitfalls (peeking, novelty effects, multiple testing)
- Providing analysis plans with statistical methods and success criteria

Whether you're testing button colors, pricing pages, or recommendation algorithms, this skill ensures your experiments are statistically sound and ready to run.

## Features

- **Hypothesis Formulation** - Create testable "if...then...because..." statements with clear rationale
- **Metric Selection** - Choose appropriate primary metrics (conversion rate, RPU, CTR) with supporting secondary and guardrail metrics
- **Power Analysis** - Calculate sample sizes using statistical power formulas with configurable parameters
- **Duration Planning** - Account for weekly patterns and traffic volume to estimate realistic test timelines
- **Statistical Methods** - Guidance on frequentist (z-tests, t-tests) vs Bayesian approaches
- **Pitfall Warnings** - Identify common issues like peeking effects, novelty effects, segmentation bias

## Features Overview

| Feature | Description |
|---------|-------------|
| **Hypothesis Design** | Format: If we [change], then [metric] will [effect] because [rationale] |\
| **Metric Tiers** | Primary (success determination), Secondary (context), Guardrail (no degradation) |\
| **Sample Size Calculation** | Power analysis formula with baseline rate, MDE, power, and significance parameters |\
| **Duration Estimation** | Calculate minimum days based on traffic; recommend 7-14 day runs for patterns |\
| **Analysis Plans** | Frequentist (z-tests) or Bayesian approaches with code examples |\
| **Pitfall Mitigation** | Peeking problem, novelty effects, multiple testing, segmentation bias warnings |\

## When to Use

Use this skill whenever you need to design an A/B test:

| Scenario | Command |
|----------|---------|
| Design experiment plan | "Design A/B test for this feature" |
| Define success metrics | "Create experiment plan with success metrics" |
| Calculate sample size | "Calculate sample size for conversion rate test" |
| Plan button change test | "Plan A/B test for checkout button change" |
| Estimate duration | "Suggest metrics and duration for this experiment" |
| Improve conversions | "Help me design an experiment to improve conversions" |
| Determine sample needs | "What's the right sample size for my A/B test?" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Design A/B test for this feature"
   - "Create experiment plan with success metrics"
   - "Calculate sample size for conversion rate test"
   - "Plan A/B test for checkout button change"

2. **Provide context about your experiment**:
   ```
   Design A/B test for new checkout button color:

   Current checkout flow has a blue (#0066CC) "Buy Now" button.
   Baseline conversion rate: 4.2% (last 30 days).
   We expect changing to green might increase conversions by ~5%.
   ```

3. **Receive complete experiment plan**:
   - Hypothesis statement with rationale
   - Variant descriptions (control vs treatment)
   - Primary/secondary/guardrail metrics
   - Sample size calculation with formula
   - Duration recommendation
   - Analysis plan with statistical methods
   - Pitfall warnings and mitigations

### Example Workflow

```
User: Design A/B test for new checkout button color

[Context provided above]

Skill Output:

# A/B Test Experiment Plan

## 1. Experiment Overview

**Hypothesis:**
If we change the checkout button from blue (#0066CC) to green (#00AA44), then conversion rate will increase by 5% because high-contrast colors create more urgency and draw user attention.

**Goal:** Increase checkout completion rate by changing button color to improve overall revenue.

---

## 2. Variants

### Variant A (Control) - Current Experience
- Button color: Blue (#0066CC)
- Text: "Buy Now"
- Size: Standard (48px height)

### Variant B (Treatment) - New Design
- Button color: Green (#00AA44) with higher contrast ratio (7.2 vs 4.5)
- Text: "Buy Now"
- Size: Standard (48px height)

**Traffic Split:** 50/50

---

## 3. Metrics

### Primary Metric
**Conversion Rate** - Percentage of visitors who complete checkout after clicking "Buy Now"
- Baseline: 4.2% (last 30 days)
- Target MDE: +5% relative lift → 4.41% conversion rate

### Secondary Metrics
- Average Order Value (AOV): Monitor for cannibalization effects
- Cart abandonment rate at payment step

### Guardrail Metrics
- Page load time (< 2s target)
- Error rate during checkout flow (< 0.5%)

---

## 4. Sample Size Calculation

**Parameters:**
- Baseline conversion rate (p1): 4.2% = 0.042
- Expected conversion rate after change (p2): 4.41% = 0.0441 (+5% relative lift)
- Statistical power: 80% (Z_(1-β) = 0.84)
- Significance level: α = 0.05 (95% confidence, Z_(1-α/2) = 1.96)

**Formula:**
```
n = (1.96 + 0.84)² × [0.042×0.958 + 0.0441×0.9559] / (0.042 - 0.0441)²
n ≈ 14,400 users per variant
```

**Results:**
- **Required samples per variant:** 14,400 users
- **Total sample size:** 28,800 users (A + B)
- **Minimum test duration:** ~5 days at current traffic of 6,000 daily visitors

---

## 5. Test Duration Recommendation

**Recommended minimum: 14 days**

Rationale:
- Statistical minimum: 5 days to reach sample size
- Add buffer for weekly patterns (weekday vs weekend shopping behavior)
- Mitigate novelty effect by observing sustained behavior

---

## 6. Analysis Plan

### Statistical Method: Frequentist Two-Proportion Z-Test

```python
from statsmodels.stats.proportion import proportions_ztest

successes = [count_checkouts_A, count_checkouts_B]
samplesizes = [14400, 14400]

stat, pvalue = proportions_ztest(successes, samplesizes)

if pvalue < 0.05:
    print("Statistically significant difference detected!")
```

**Success Criteria:**
- Primary threshold: p-value < 0.05 (95% confidence) → Implement variant B
- Strong evidence: p-value < 0.01 (99% confidence) → High confidence in results

---

## 7. Pitfalls & Mitigations

### ⚠️ Peeking Problem
**Risk:** Repeatedly checking results during experiment inflates false positive rate to ~30%.

**Mitigation:** Do NOT check results before reaching target sample size; use sequential testing methods if early stopping needed.

### ⚠️ Novelty Effect
**Risk:** Initial uplift may fade as users adapt to new design.

**Mitigation:** Run minimum 14 days to capture sustained behavior; analyze daily trends over time.

---

*Generated by A/B Test Designer v1.0*
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/ab-test-designer/ab-test-designer.skill \
  -o ~/.claude/skills/ab-test-designer.skill && echo "✅ A/B Test Designer installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/ab-test-designer.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Design A/B test for new checkout button color" | Define hypothesis about color impact on conversion, specify control vs treatment variants, calculate required samples based on baseline checkout rate (~2-5%), recommend 7-day minimum duration. |
| **Test 2** | "Create experiment plan to test personalized recommendations" | Identify primary metric as engagement time or CTR, suggest guardrail metrics for content quality, calculate sample size for likely smaller effect sizes (3-8% lift), warn about novelty effects in recommendation tests. |
| **Test 3** | "Calculate sample size for 5% lift in sign-up rate" | Perform power analysis assuming baseline signup rate (~10%), MDE of 5%, 80% power, α=0.05; output ~7,200 users per variant with methodology explanation. |

## Statistical Reference

### Sample Size Quick Reference

| Baseline | MDE | Power | α | Sample Size/Variant | Duration* |
|----------|-----|-------|---|---------------------|-----------|
| 5% | 10% | 80% | 0.05 | ~14,400 | ~2 weeks (10K/day) |
| 5% | 20% | 80% | 0.05 | ~3,600 | ~5 days (10K/day) |
| 10% | 10% | 80% | 0.05 | ~7,200 | ~1 week (10K/day) |
| 5% | 5% | 90% | 0.05 | ~32,000 | ~1 month (10K/day) |

*Duration varies based on daily traffic volume

### Common Pitfalls and Solutions

| Pitfall | Risk Level | Solution |
|---------|------------|----------|
| **Peeking Problem** | False positives jump from 5% to ~30% | Don't check results before target sample size; use sequential testing or Bayesian methods |
| **Novelty Effect (SDE)** | Initial uplift fades as users adapt | Run minimum 14 days; analyze trends over time |
| **Multiple Testing** | Testing many variants increases false positives | Pre-specify variants/segments; apply Bonferroni correction |
| **Segmentation Bias** | Effects differ across user segments | Pre-plan segment analysis; don't cherry-pick favorable segments post-hoc |
| **Survivorship Bias** | Only analyzing completers misses drop-offs | Analyze all exposed users, not just converters |

## Best Practices

- **Always define primary metric before test**: Don't move goalposts after seeing results; choose ONE main outcome measure
- **Use sequential testing or Bayesian to avoid peeking**: Traditional frequentist tests penalize repeated checks; Bayesian methods allow continuous monitoring
- **Monitor for novelty/SDE effects**: Users may react differently initially; run minimum 1–2 weeks for reliable results
- **Calculate sample size upfront**: Don't guess duration; use power analysis to determine required samples based on MDE and baseline rate
- **Set realistic MDE values**: 5% lift requires ~4x more samples than 20% lift; balance statistical feasibility with business needs
- **Account for weekly patterns**: Run minimum 7 days to capture weekday/weekend behavior differences
- **Document everything**: Record hypotheses, metrics, and analysis plan before starting; prevents p-hacking and data dredging
- **Plan segment analyses in advance**: Don't cherry-pick favorable segments post-hoc; pre-specify which segments you'll analyze

## Recommended Tools

- **Optimizely** - Enterprise A/B testing platform with built-in sample size calculators
- **VWO (Visual Website Optimizer)** - Testing and optimization platform
- **LaunchDarkly** - Feature flagging with experimentation capabilities
- **statsmodels (Python)** - Statistical modeling library for custom analysis: `pip install statsmodels scipy`

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [Performance Budget Enforcer Skill](../performance-budget-enforcer/) - Monitor bundle size and Core Web Vitals with budget enforcement
- [Concurreny Safety Checker Skill](../concurrency-safety-checker/) - Detect race conditions in Go/Rust concurrent code
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)

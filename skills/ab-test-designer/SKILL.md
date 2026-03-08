---
name: ab-test-designer
description: Creates complete A/B test experiment plans including hypothesis, variants, success metrics, sample size calculation, duration, statistical power, and analysis guidelines.
tags: [ab-testing, experimentation, product, metrics, statistics]
author: Jose Quiñones
version: 1.0
license: MIT
---

# A/B Test Designer

This skill creates **complete A/B test experiment plans** including hypothesis definition, variant design, success metrics specification, sample size calculation, duration estimation, statistical power analysis, and comprehensive analysis guidelines. It guides product teams through the entire experimental design process to ensure statistically valid and actionable results.

## Instructions

When activated, follow this step-by-step process:

### Step 1: Parse User Input
- **Extract feature description**: Identify what is being tested (button color, pricing page, recommendation algorithm)
- **Capture hypothesis**: Extract the expected outcome ("Changing button color will increase conversions")
- **Identify baseline metrics**: Note current conversion rates, revenue per user, or other baseline measurements
- **Determine expected lift**: Calculate minimum detectable effect (MDE) from user input or suggest reasonable values

### Step 2: Define Hypothesis Statement
Create a clear, testable hypothesis following the format:

```
If we [make this change], then [metric X] will increase/decrease by [Y%] because [rationale].
```

**Example:** "If we change the checkout button from blue to green, then conversion rate will increase by 5% because high-contrast colors create more urgency."

### Step 3: Define Metrics

**Primary Metric (Choose ONE):**
The main outcome measure that determines test success. Select based on experiment goal:
- **Conversion Rate**: For signup flows, checkout funnels, form completions
- **Revenue Per User (RPU)**: For pricing changes, upsell tests
- **Click-Through Rate (CTR)**: For button/link placement tests
- **Engagement Time**: For content quality tests
- **Retention Rate**: For onboarding or feature adoption tests

**Secondary Metrics:**
Supporting metrics that provide additional context:
- Average order value (AOV)
- Session duration
- Pages per session
- Feature usage rate
- Customer support tickets

**Guardrail Metrics:**
Metrics that must NOT degrade during the experiment:
- Error rates
- Page load time
- App crash rate
- Negative feedback rate
- Refund/cancellation rate

### Step 4: Design Variants

**Control Group (Variant A):**
- Current experience (baseline)
- Document exact current state
- No changes from existing implementation

**Treatment Group(s) (Variant B, C, etc.):**
- List specific changes for each variant
- Ensure changes are isolated (one variable at a time when possible)
- Define variants clearly:
  ```
  Variant A (Control): Current blue button (#0066CC)
  Variant B (Treatment): Green button (#00AA44) with increased contrast
  ```

**Traffic Split:**
- Standard split: 50/50 for simple A/B tests
- Adjusted splits for high-risk changes (90/10, 95/5)
- Document exact percentage allocation

### Step 5: Calculate Sample Size

Use power analysis formula to determine required sample size per variant:

**Input parameters:**
- **Baseline conversion rate (p1)**: Current metric value (e.g., 0.05 for 5%)
- **Minimum Detectable Effect (MDE)**: Smallest lift you want to detect (e.g., 0.05 for 5% relative lift)
- **Statistical power (1 - β)**: Typically 80% (0.8) or 90% (0.9)
- **Significance level (α)**: Typically 0.05 (95% confidence)

**Sample size formula (for conversion rate tests):**
```
n = (Z_(1-α/2) + Z_(1-β))² × [p1×(1-p1) + p2×(1-p2)] / (p1 - p2)²

Where:
  p1 = baseline conversion rate
  p2 = expected conversion rate after change (p1 × (1 + MDE))
  Z_(1-α/2) = critical value for significance level (~1.96 for α=0.05)
  Z_(1-β) = critical value for power (~0.84 for 80% power, ~1.28 for 90%)

Result: Minimum samples needed per variant (A and B)
Total sample size = n × number of variants
```

**Quick reference table:**
| Baseline | MDE | Power | α | Sample Size/Variant | Total Duration* |
|----------|-----|-------|---|---------------------|-----------------|
| 5% | 10% | 80% | 0.05 | ~14,400 | ~2 weeks (10K/day) |
| 5% | 20% | 80% | 0.05 | ~3,600 | ~5 days (10K/day) |
| 10% | 10% | 80% | 0.05 | ~7,200 | ~1 week (10K/day) |
| 5% | 5% | 90% | 0.05 | ~32,000 | ~1 month (10K/day) |

*Duration varies based on daily traffic volume

### Step 6: Estimate Test Duration

**Calculation:**
```
Test Duration (days) = Total Sample Size / Daily Traffic Volume × Number of Variants
```

**Example:**
- Total sample needed: 30,000 users
- Daily traffic: 10,000 users
- Duration: 30,000 / 10,000 = **3 days minimum**

**Recommendations:**
- Run for minimum **7–14 days** to account for weekly patterns (weekday vs weekend behavior)
- Extend duration if traffic is low
- Consider seasonal effects for e-commerce, media sites

### Step 7: Define Success Criteria

**Statistical Significance Threshold:**
- Primary threshold: p-value < 0.05 (95% confidence)
- Secondary threshold: p-value < 0.01 (99% confidence) for major decisions

**Minimum Detectable Effect (MDE):**
- Recommended MDE: 5–20% relative lift depending on baseline
- Smaller MDE requires larger sample sizes and longer tests

**Business Impact Threshold:**
- Calculate minimum business value needed to justify implementation
- Consider development cost, maintenance overhead, risk factors

### Step 8: Outline Analysis Plan

**Frequentist Approach (Recommended for most cases):**
```
1. Collect data until reaching target sample size
2. Run hypothesis test on primary metric:
   - For conversion rates: Two-proportion z-test or chi-square test
   - For means (revenue, time): Two-sample t-test
3. Calculate p-value and confidence interval
4. Compare against significance threshold (α = 0.05)
5. If p < α: Reject null hypothesis → experiment successful

Tools: statsmodels.stats.power, scipy.stats, or built-in A/B testing platforms
```

**Bayesian Approach (Recommended for):**
- Continuous monitoring without peeking penalties
- Small sample sizes where frequentist tests lack power
- Decision-making under uncertainty

```
1. Define prior distributions based on historical data
2. Update posterior distributions as data accumulates
3. Calculate probability of variant B > variant A
4. Declare winner when P(Better) > threshold (e.g., 95%)

Tools: PyMC, Stan, or Bayesian A/B testing platforms
```

### Step 9: Warn About Common Pitfalls

**Peeking Problem:**
- Checking results repeatedly during experiment inflates false positive rate
- **Solution**: Use sequential testing methods or Bayesian approach with proper stopping rules

**Novelty Effect (SDE - Statistical Dance Effect):**
- Users react to new design initially, then return to baseline behavior
- **Solution**: Run test minimum 2 weeks; analyze trends over time

**Multiple Testing Problem:**
- Testing many variants or metrics increases false positive risk
- **Solution**: Apply Bonferroni correction or use false discovery rate control

**Segmentation Bias:**
- Effects may differ across user segments (new vs returning, mobile vs desktop)
- **Solution**: Pre-plan segment analysis; don't cherry-pick favorable segments

**Survivorship Bias:**
- Only analyzing users who complete the funnel misses early drop-offs
- **Solution**: Analyze all exposed users, not just converters

### Step 10: Output Structured Plan

Generate comprehensive markdown report with sections:
1. Experiment Overview (hypothesis, goal)
2. Variants (control and treatment details)
3. Metrics (primary, secondary, guardrail)
4. Sample Size Calculation (methodology, results)
5. Test Duration (estimated timeline)
6. Analysis Plan (statistical method, success criteria)
7. Pitfalls & Mitigations (risks and solutions)

## Activation Phrases / When to Use

Use this skill whenever you need to design an A/B test:

- "Design A/B test for this feature"
- "Create experiment plan with success metrics"
- "Calculate sample size for conversion rate test"
- "Plan A/B test for checkout button change"
- "Suggest metrics and duration for this experiment"
- "Help me design an experiment to improve conversions"
- "What's the right sample size for my A/B test?"

## Usage Examples

| User Input | Expected Skill Behavior |
|------------|------------------------|
| "Design A/B test for new checkout button color" | Define hypothesis about color impact on conversion, specify control (current color) vs treatment (new color), calculate required samples based on baseline checkout rate (~2-5%), recommend 7-day minimum duration. |
| "Create experiment plan to test personalized recommendations" | Identify primary metric as engagement time or CTR, suggest guardrail metrics for content quality, calculate sample size for likely smaller effect sizes (3-8% lift), warn about novelty effects in recommendation tests. |
| "Calculate sample size for 5% lift in sign-up rate" | Perform power analysis assuming baseline signup rate (~10%), MDE of 5%, 80% power, α=0.05; output ~7,200 users per variant with methodology explanation. |
| "Plan A/B test for pricing page layout change" | Define primary metric as conversion rate or revenue per user, calculate sample size accounting for higher variance in revenue metrics, recommend 14-day duration to capture weekly patterns and avoid novelty effects. |

## How It Works

```
User provides feature description or hypothesis
          │
          ▼
┌───────────────────────┐
│  Step 1: PARSE       │ → Extract feature, baseline, expected lift
│  (Input Analysis)    │ → Identify experiment type and goals
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 2: DEFINE      │ → Create clear hypothesis statement
│  (Hypothesis)        │ → Format: If...then...because...
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 3: METRICS     │ → Primary metric selection
│  Selection           │ → Secondary & guardrail metrics
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 4: VARIANTS    │ → Define control and treatment groups
│  Design              │ → Traffic split recommendations
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 5: SAMPLE SIZE │ → Power analysis calculation
│  Calculation         │ → MDE, power, α parameters
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 6: DURATION    │ → Estimate based on traffic volume
│  Estimation          │ → Recommend minimum run time
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 7: CRITERIA    │ → Define success thresholds
│  Definition           │ → Significance, MDE, business impact
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 8: ANALYSIS    │ → Frequentist or Bayesian method
│  Plan                │ → Statistical tests, tools
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 9: WARNINGS    │ → Pitfalls and mitigations
│  (Risks & Solutions) │ → Peeking, novelty effects, multiple testing
└───────────────────────┘
          │
          ▼
    Output: Complete A/B test experiment plan
```

## Dependencies

- **No external dependencies required** - uses basic statistical formulas for sample size calculation
- **Optional: Python stats libraries** - `statsmodels.stats.power` or `scipy.stats` for advanced calculations
  ```bash
  pip install statsmodels scipy
  ```
- **Recommended tools**: A/B testing platforms (Optimizely, VWO, LaunchDarkly) with built-in sample size calculators

## Best Practices / Notes

- **Always define primary metric before test**: Don't move goalposts after seeing results; choose ONE main outcome measure
- **Use sequential testing or Bayesian to avoid peeking**: Traditional frequentist tests penalize repeated checks; Bayesian methods allow continuous monitoring
- **Monitor for novelty/SDE effects**: Users may react differently initially; run minimum 1–2 weeks for reliable results
- **Calculate sample size upfront**: Don't guess duration; use power analysis to determine required samples based on MDE and baseline rate
- **Set realistic MDE values**: 5% lift requires ~4x more samples than 20% lift; balance statistical feasibility with business needs
- **Account for weekly patterns**: Run minimum 7 days to capture weekday/weekend behavior differences
- **Document everything**: Record hypotheses, metrics, and analysis plan before starting; prevents p-hacking and data dredging
- **Plan segment analyses in advance**: Don't cherry-pick favorable segments post-hoc; pre-specify which segments you'll analyze

## Output Format

The skill outputs a comprehensive A/B test experiment plan:

```markdown
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
- Position: Centered below product details

### Variant B (Treatment) - New Design
- Button color: Green (#00AA44) with higher contrast ratio (7.2 vs 4.5)
- Text: "Buy Now"
- Size: Standard (48px height)
- Position: Centered below product details

**Traffic Split:** 50/50 (15,000 users per variant for initial analysis)

---

## 3. Metrics

### Primary Metric
**Conversion Rate** - Percentage of visitors who complete checkout after clicking "Buy Now"
- Baseline: 4.2% (last 30 days)
- Target MDE: +5% relative lift → 4.41% conversion rate

### Secondary Metrics
- Average Order Value (AOV): Monitor for cannibalization effects
- Cart abandonment rate at payment step
- Time to complete checkout

### Guardrail Metrics
- Page load time (< 2s target)
- Error rate during checkout flow (< 0.5%)
- Customer support tickets about button issues

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
- Account for potential traffic fluctuations
- Mitigate novelty effect by observing sustained behavior

**Timeline:**
- Start: Monday at midnight (UTC)
- End: Two weeks later, same day/time
- Total exposure: ~84,000 unique users (allowing for repeat visitors)

---

## 6. Analysis Plan

### Statistical Method: Frequentist Two-Proportion Z-Test

**Pre-analysis checklist:**
1. [ ] Verify randomization is working correctly
2. [ ] Check sample balance across variants for key demographics
3. [ ] Confirm no external factors (holidays, marketing campaigns) during test period

**Hypothesis Test:**
```python
from statsmodels.stats.proportion import proportions_ztest

# Convert counts to successes and trials
successes = [count_checkouts_A, count_checkouts_B]
samplesizes = [14400, 14400]

stat, pvalue = proportions_ztest(successes, samplesizes)

if pvalue < 0.05:
    print("Statistically significant difference detected!")
```

**Success Criteria:**
- Primary threshold: p-value < 0.05 (95% confidence) → Implement variant B
- Strong evidence: p-value < 0.01 (99% confidence) → High confidence in results
- Confidence interval for effect size must exclude zero and be positive

**Effect Size Calculation:**
```python
# Calculate lift percentage and confidence interval
lift = (conversion_B - conversion_A) / conversion_A * 100
print(f"Lift: {lift:.2f}%")
```

---

## 7. Pitfalls & Mitigations

### ⚠️ Peeking Problem
**Risk:** Repeatedly checking results during experiment inflates false positive rate to ~30% instead of 5%.

**Mitigation:**
- Do NOT check results before reaching target sample size
- Use sequential testing methods (e.g., alpha spending functions) if early stopping needed
- Consider Bayesian approach with proper posterior thresholds

### ⚠️ Novelty Effect
**Risk:** Initial uplift may fade as users adapt to new design.

**Mitigation:**
- Run minimum 14 days to capture sustained behavior
- Analyze daily conversion rates over time (plot trend)
- Compare early vs late period performance separately

### ⚠️ Multiple Testing Problem
**Risk:** Testing multiple button colors or analyzing many segments increases false positive risk.

**Mitigation:**
- Pre-specify which variants and segments to analyze
- Apply Bonferroni correction if testing > 1 variant: α_corrected = 0.05 / N_tests
- Use False Discovery Rate (FDR) control for exploratory analyses

### ⚠️ Segmentation Bias
**Risk:** Effects may differ by device type, geography, or user segment.

**Mitigation:**
- Pre-plan segment analysis: mobile vs desktop, new vs returning users
- Don't cherry-pick favorable segments post-hoc
- Report overall results first; segment analysis is exploratory unless pre-specified

---

## 8. Implementation Checklist

Before launching experiment:

- [ ] Randomization logic verified (user ID → variant assignment)
- [ ] Variant exposure confirmed via analytics tracking
- [ ] Primary metric defined in analytics platform
- [ ] Guardrail metrics set up for monitoring
- [ ] Analysis script ready to run post-test
- [ ] Stakeholders briefed on experiment goals and success criteria

---

*Generated by A/B Test Designer v1.0*
```

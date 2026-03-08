# Performance Budget Enforcer Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/jalos33/Skill-Cauldron/tree/main/skills/performance-budget-enforcer)

A Claude Code skill that **monitors bundle size**, **Core Web Vitals** (LCP, FID, CLS), and **performance metrics** in real time, enforcing budgets and alerting on regressions. Analyzes build outputs from webpack/vite/Next.js, runs Lighthouse measurements, compares against configurable performance targets, and provides actionable optimization recommendations when budgets are violated.

## Purpose

This skill ensures your frontend applications maintain optimal performance by:
- Monitoring bundle sizes in real time during builds
- Tracking Core Web Vitals (LCP, FID, CLS, TBT) for user experience
- Enforcing configurable performance budgets to prevent regressions
- Providing specific, actionable recommendations when budgets are violated

Whether you're building a React app with webpack or a Next.js site, this skill helps you maintain fast, responsive experiences that users expect.

## Features

- **Bundle Size Analysis** - Parse webpack/vite stats.json for comprehensive bundle breakdowns
- **Core Web Vitals Monitoring** - Track LCP, FID, CLS, TBT against Google-recommended budgets
- **Regression Detection** - Compare against baselines to flag performance degradations
- **Optimization Suggestions** - Specific fixes for code splitting, lazy loading, image optimization
- **Severity-Based Reporting** - Issues ranked CRITICAL/HIGH/MEDIUM/LOW with clear action items
- **CI/CD Integration Ready** - Structured output suitable for automated blocking of regressions

## Features Overview

| Feature | Description |
|---------|-------------|
| **Bundle Analysis** | Parse webpack/vite stats, measure total and per-chunk sizes (gzipped) |
| **Core Web Vitals** | LCP < 2.5s, FID < 100ms, CLS < 0.1, TBT < 200ms validation |
| **Regression Detection** | Flag bundle increases > 10%, metric degradations vs baseline |
| **Issue Detection** | Large deps, missing splits, render-blocking resources, CLS risks |
| **Optimization Suggestions** | Code splitting, lazy loading, image optimization, dependency replacement |
| **Severity Classification** | CRITICAL (LCP > 4s), HIGH (> budget by 20%), MEDIUM (>10% regression), LOW (suggestions) |

## When to Use

Use this skill whenever you need to enforce performance budgets:

| Scenario | Command |
|----------|---------|
| Enforce bundle size budget | "Enforce performance budget on this build" |
| Monitor Core Web Vitals | "Monitor bundle size and Core Web Vitals" |
| Check app meets targets | "Check if this app meets performance targets" |
| Alert on regression | "Alert on bundle size regression" |
| Analyze Lighthouse results | "Analyze Lighthouse results for this page" |
| Review webpack stats | "Review webpack stats for optimization opportunities" |

## How to Use

### Basic Usage

1. **Activate the skill** with any of these phrases:
   - "Enforce performance budget on this build"
   - "Monitor bundle size and Core Web Vitals"
   - "Check if this app meets performance targets"
   - "Alert on bundle size regression"
   - "Analyze Lighthouse results for this page"

2. **Provide the build output or metrics**:
   ```
   Enforce performance budget on this Next.js build:

   Build stats from next build --stats:

   {
     "chunks": [
       {"name": "pages/_app", "size": 45000, "compressedSize": 12800},
       {"name": "pages/index", "size": 38000, "compressedSize": 10200},
       {"name": "vendor", "size": 892000, "compressedSize": 251000}
     ],
     "assets": [
       {"name": "hero-banner.jpg", "size": 450000, "type": "image"}
     ]
   }

   Lighthouse results:
   - LCP: 3.2s
   - FID: 89ms
   - CLS: 0.08
   - TBT: 180ms
   ```

3. **Receive performance budget enforcement report**:
   - Current metrics compared against budgets
   - Violations ranked by severity with evidence
   - Specific fix suggestions with code examples

### Example Workflow

```
User: Enforce performance budget on this Next.js build

[Build stats provided above]

Skill Output:

# Performance Budget Report

## Summary
- Build Tool: Next.js 13.4 (webpack 5)
- Total JS (gzipped): 280KB | Budget: < 200KB | Status: ❌ Exceeded by 40%
- LCP: 3.2s | Budget: < 2.5s | Status: ❌ Regressed by 28%
- FID: 89ms | Budget: < 100ms | Status: ✅ Passed
- CLS: 0.08 | Budget: < 0.1 | Status: ✅ Passed

---

## 🔴 CRITICAL Issues

### LCP Regression - Largest Contentful Paint Delayed
**Severity:** CRITICAL | **Metric:** LCP = 3.2s (Budget: < 2.5s)
**Regression:** +28% compared to baseline (2.5s)

**Evidence:**
```
Largest Contentful Element: hero-banner.jpg (450KB uncompressed)
Render Time: 3.2s
Blocking Resources: 4 CSS files, 1 JavaScript bundle
```

**Issue:** Hero image loads too slowly due to lack of optimization and render-blocking resources.

**Fix:**
1. **Preload the LCP image**:
   ```html
   <link rel="preload" as="image" href="/hero-banner.jpg">
   ```

2. **Optimize image format and sizing**:
   - Convert to WebP: `/hero-banner.webp` (45% smaller than JPEG)
   - Add explicit dimensions to prevent layout shift
   - Use responsive images with `srcset` for mobile

3. **Defer non-critical CSS**:
   ```html
   <link rel="stylesheet" href="/critical.css" media="print" onload="this.media='all'">
   ```

---

## 🟠 HIGH Issues

### Bundle Size Exceeded: vendor.js
**Severity:** HIGH | **Budget:** < 150KB (gzipped)
**Current:** 280KB (gzipped) | **Over budget by:** 63%

**Issue:** Vendor bundle exceeds budget significantly.

**Fix:**
- Use `next/dynamic` for code splitting:
   ```javascript
   const HeavyComponent = dynamic(() => import('../components/HeavyComponent'), {
     loading: () <LoadingSpinner />,
   });
   ```

- Enable automatic tree-shaking in webpack config:
   ```javascript
   // next.config.js
   module.exports = {
     webpack: (config, { isServer }) => {
       if (!isServer) {
         config.optimization.usedExports = true;
         config.optimization.sideEffects = true;
       }
       return config;
     },
   };
   ```

---

## Recommended Actions

1. **Immediate (CRITICAL):** Implement LCP optimizations for hero image
2. **Before Release:** Enable automatic code splitting and tree-shaking
3. **Next Sprint:** Audit third-party dependencies for lighter alternatives
4. **Ongoing:** Set up Lighthouse CI in pipeline to prevent regressions

---
*Generated by Performance Budget Enforcer v1.0*
```

## Installation

### Install from Repository

Download and install the skill directly:

```bash
curl -L https://raw.githubusercontent.com/jalos33/Skill-Cauldron/main/skills/performance-budget-enforcer/performance-budget-enforcer.skill \
  -o ~/.claude/skills/performance-budget-enforcer.skill && echo "✅ Performance Budget Enforcer installed!"
```

### Verify Installation

```bash
ls -la ~/.claude/skills/performance-budget-enforcer.skill
```

## Testing the Skill

Run these test cases to verify the skill works correctly:

| Test | Command | Expected Output |
|------|---------|-----------------|
| **Test 1** | "Enforce bundle size budget on this Next.js build" | Report identifying oversized vendor chunks, LCP regression with image optimization suggestions |
| **Test 2** | "Monitor Core Web Vitals for this React app" | Analysis of LCP/FID/CLS metrics against budgets, specific fixes for render-blocking resources and CLS issues |
| **Test 3** | "Check if JS bundle exceeds 200KB" | Detailed bundle breakdown with largest dependencies identified, replacement alternatives provided (e.g., date-fns vs moment.js) |

## Performance Budgets Reference

### Recommended Default Budgets

| Metric | Budget | Threshold for Alert | Impact |
|--------|--------|---------------------|--------|
| **Total JS (gzipped)** | < 200KB | > 200KB | HIGH - Longer download times on mobile |
| **First chunk JS** | < 150KB | > 150KB | MEDIUM - Slower initial page load |
| **LCP (Largest Contentful Paint)** | < 2.5s | > 2.5s | CRITICAL - Major user experience impact |
| **FID (First Input Delay)** | < 100ms | > 300ms | HIGH - Poor interactivity perception |
| **CLS (Cumulative Layout Shift)** | < 0.1 | > 0.25 | HIGH - Visual instability frustrates users |
| **TBT (Total Blocking Time)** | < 200ms | > 400ms | MEDIUM - Delays during page load |

### Budget Violation Severity Levels

| Badge | Level | Condition | Action Required |
|-------|-------|-----------|-----------------|
| 🔴 | CRITICAL | LCP > 4s, CLS > 0.5, budget exceeded by > 50% | Fix immediately before deployment |
| 🟠 | HIGH | LCP > 2.5s, FID > 300ms, budget exceeded by 20-50% | Fix before production release |
| 🟡 | MEDIUM | Budget regression > 10%, minor violations | Address in next sprint |
| 🟢 | LOW | Best practice suggestions, low-impact issues | Optional enhancement |

## Best Practices

- **Set realistic budgets based on your audience**: Mobile users need smaller bundles; consider 3G network constraints
- **Run in CI/CD to block regressions**: Fail builds when critical budgets are exceeded
- **Use performance budgets in webpack/vite config**: Configure `performance.maxAssetSize` and `performance.maxEntrypointSize`
- **Combine with Lighthouse CI for trend tracking**: Track metrics over time, not just single snapshots
- **Prioritize Core Web Vitals**: Google uses these as ranking signals; optimize for LCP first (most impactful)
- **Measure on real devices**: Lab data (Lighthouse) is good but RUM (Real User Monitoring) reflects actual user experience
- **Use compression effectively**: Ensure gzip/brotli is enabled in production; measure gzipped sizes against budgets
- **Monitor over time**: Set up dashboards to track performance trends and catch regressions early

## Performance Optimization Patterns

### Code Splitting with Next.js Dynamic Imports

```javascript
import dynamic from 'next/dynamic';

// Automatically code split this component
const HeavyChart = dynamic(() => import('../components/HeavyChart'), {
  loading: () <LoadingSpinner />,
  ssr: false, // Don't render on server if client-only
});

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<ChartLoader />}>
        <HeavyChart data={chartData} />
      </Suspense>
    </div>
  );
}
```

### Image Optimization Best Practices

```jsx
// Next.js Image component (automatic optimization)
import Image from 'next/image';

<Image
  src="/hero-banner.jpg"
  alt="Hero banner"
  width={1200}
  height={600}
  priority // Preload for LCP images
  quality={80}
  placeholder="blur"
/>

// Standard React with explicit dimensions (prevent CLS)
<img
  src="/product.jpg"
  alt="Product"
  width="300"
  height="300"
  style={{ objectFit: 'cover' }}
  loading="lazy" // Defer below-fold images
/>
```

### Dependency Optimization

**Replace moment.js with date-fns:**
```bash
npm uninstall moment && npm install date-fns
```

```javascript
// Before (moment.js - 68KB gzipped)
import moment from 'moment';
const formatted = moment(date).format('YYYY-MM-DD');

// After (date-fns - 7KB gzipped, tree-shakeable)
import { format } from 'date-fns';
const formatted = format(date, 'yyyy-MM-dd');
```

**Use tree-shakeable lodash:**
```javascript
// Before (lodash - entire library loaded)
import _ from 'lodash';
_.debounce(fn, 300);

// After (only imported function, tree-shaking works)
import debounce from 'lodash/debounce.js';
debounce(fn, 300);
```

## CI/CD Integration Example

### GitHub Actions with Lighthouse CI

```yaml
name: Performance Budget Check

on: [pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Build app
        run: npm run build

      - name: Run Lighthouse and check budgets
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            http://localhost:3000/
            http://localhost:3000/dashboard
          uploadArtifacts: true
          budgetPath: ./lighthouse-budgets.json

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: lighthouse-results
          path: ${{ github.workspace }}/lighthouse-reports/
```

### Lighthouse Budget Configuration (lighthouse-budgets.json)

```json
{
  "pwa": false,
  "budgets": [
    {
      "label": "home page",
      "pathPattern": "/$",
      "resourceSummary": {
        "transferSizeBudget": 204800
      },
      "auditLabels": ["performance"],
      "metrics": [
        {
          "name": "lcp",
          "budget": 2500,
          "unit": "milliseconds"
        },
        {
          "name": "fid",
          "budget": 100,
          "unit": "milliseconds"
        },
        {
          "name": "cls",
          "budget": 0.1,
          "unit": "score"
        }
      ]
    }
  ]
}
```

## License

MIT License - see [LICENSE](../../LICENSE) for details.

## Contributing

Found issues or want to improve this skill? Open an issue at:
https://github.com/jalos33/Skill-Cauldron/issues

## See Also

- [Code Reviewer Skill](../code-reviewer/) - Automated code review with competing agents framework
- [CI/CD Pipeline Auditor](../ci-cd-pipeline-auditor/) - Security audit for GitHub Actions workflows
- More skills in the [Skill-Cauldron repository](https://github.com/jalos33/Skill-Cauldron)

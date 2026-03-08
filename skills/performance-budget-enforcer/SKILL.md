---
name: performance-budget-enforcer
description: Monitors bundle size, Core Web Vitals (LCP, FID, CLS), and performance metrics in real time, enforcing budgets and alerting on regressions.
tags: [performance, bundle-size, core-web-vitals, monitoring, frontend]
author: Jose Quiñones
version: 1.0
license: MIT
---

# Performance Budget Enforcer

This skill **monitors bundle size**, **Core Web Vitals** (LCP, FID, CLS), and **performance metrics** in real time, enforcing defined budgets and alerting on regressions. It analyzes build outputs from webpack/vite, runs Lighthouse measurements, compares against configurable performance targets, and provides actionable optimization recommendations when budgets are violated.

## Instructions

When activated, follow this step-by-step process:

### Step 1: Read Build Output
- **Identify build tool**: Detect webpack, vite, Next.js, or other bundler output format
- **Parse stats file**: Read `stats.json`, bundle analyzer output, or production build artifacts
- **Extract chunk information**: Identify entry chunks, vendor bundles, lazy-loaded routes
- **Calculate sizes**: Measure both uncompressed and gzipped/brotli compressed sizes

### Step 2: Measure Bundle Size
- **Total bundle size**: Sum of all JavaScript/CSS asset sizes
- **Per-chunk breakdown**: Individual analysis of each code split chunk
- **Vendor analysis**: Separate third-party dependencies from application code
- **Tree-shaking assessment**: Identify unused exports and dead code opportunities

### Step 3: Run Performance Measurements
- **Lighthouse metrics**: Parse Lighthouse audit results (if available) or run headless browser tests
- **Core Web Vitals collection**:
  - **LCP (Largest Contentful Paint)**: Measures loading performance (target: < 2.5s)
  - **FID (First Input Delay)**: Measures interactivity (target: < 100ms)
  - **CLS (Cumulative Layout Shift)**: Measures visual stability (target: < 0.1)
  - **TBT (Total Blocking Time)**: Measures main thread blocking (target: < 200ms)
- **Real User Monitoring**: If available, analyze RUM data for actual user experience

### Step 4: Compare Against Defined Budgets
Compare measured metrics against configured budgets:

**Default recommended budgets:**
| Metric | Budget | Threshold | Action |
|--------|--------|-----------|--------|
| Total JS (gzipped) | < 200KB | > 200KB | Alert HIGH |
| First chunk JS | < 150KB | > 150KB | Alert MEDIUM |
| LCP | < 2.5s | > 2.5s | Alert CRITICAL |
| FID | < 100ms | > 300ms | Alert HIGH |
| CLS | < 0.1 | > 0.25 | Alert HIGH |
| TBT | < 200ms | > 400ms | Alert MEDIUM |

**Regression detection:**
- Compare against baseline (previous build or deployment)
- Flag increases of > 10% for bundle sizes
- Flag decreases in Core Web Vitals metrics

### Step 5: Detect Common Performance Issues
Identify specific anti-patterns causing budget violations:

**Bundle size issues:**
- Large third-party dependencies (lodash, moment.js, etc.)
- Unused imports and exports (tree-shaking opportunities)
- Missing code splitting on routes/components
- Uncompressed assets in production
- Duplicate dependencies across chunks

**Core Web Vitals issues:**
- **LCP problems**: Large images, slow server response, render-blocking resources
- **FID problems**: Long main thread tasks, heavy JavaScript execution
- **CLS problems**: Images without dimensions, dynamically injected content
- **TBT problems**: Long-running scripts, expensive layout calculations

### Step 6: Generate Optimization Suggestions
Provide specific, actionable recommendations based on detected issues:

**Code splitting:**
```javascript
// Instead of:
import { heavyLib } from './heavy-lib';

// Use dynamic import:
const heavyLib = () => import('./heavy-lib');
```

**Lazy loading:**
```javascript
// Route-based lazy loading for Next.js/React Router
const Dashboard = dynamic(() => import('../pages/Dashboard'));
```

**Image optimization:**
- Add explicit width/height attributes to prevent CLS
- Use modern formats (WebP, AVIF) with fallbacks
- Implement responsive images with srcset
- Consider lazy loading below-fold images

**Dependency optimization:**
- Replace heavy libraries with lighter alternatives (e.g., date-fns instead of moment.js)
- Use tree-shakeable variants (e.g., lodash-es)
- Import only needed functions: `import { debounce } from 'lodash'`

### Step 7: Output Report with Severity Levels
Generate structured report categorizing issues by severity:

**CRITICAL (🔴):**
- LCP > 4s (severe loading impact)
- Budget exceeded by > 50%
- CLS > 0.5 (major visual instability)

**HIGH (🟠):**
- LCP > 2.5s
- FID > 300ms
- Bundle size > budget by 20-50%
- CLS > 0.25

**MEDIUM (🟡):**
- FID > 100ms but < 300ms
- TBT > 200ms
- Bundle size regression > 10%
- Missing compression on assets

**LOW (🟢):**
- Minor optimizations with low impact
- Suggestions for future improvements
- Best practice violations without immediate impact

### Step 8: Provide Line Numbers and Evidence
For each issue found, include specific evidence:

```markdown
### Bundle Size Exceeded: vendor.js
**Severity:** HIGH | **Budget:** < 150KB (gzipped)
**Current:** 245KB (gzipped) | **Over budget by:** 63%
**File:** `stats.json` - chunk "vendor"

**Evidence:**
```json
{
  "name": "vendor",
  "size": 892000,
  "compressedSize": 251000,
  "modules": [
    {"name": "lodash", "size": 72000},
    {"name": "moment", "size": 68000},
    {"name": "axios", "size": 45000}
  ]
}
```

**Issue:** Vendor bundle exceeds budget, primarily due to lodash and moment.js dependencies.

**Fix:** Replace moment.js with date-fns (7KB vs 68KB):
```bash
npm uninstall moment && npm install date-fns
```

Replace lodash with lodash-es for tree-shaking:
```javascript
// Before
import _ from 'lodash';
_.debounce(fn, 300);

// After
import debounce from 'lodash/debounce.js';
```
```

## Activation Phrases / When to Use

Use this skill whenever you need to enforce performance budgets:

- "Enforce performance budget on this build"
- "Monitor bundle size and Core Web Vitals"
- "Check if this app meets performance targets"
- "Alert on bundle size regression"
- "Analyze Lighthouse results for this page"
- "Review webpack stats for optimization opportunities"
- "Validate Next.js build against performance budgets"

## Usage Examples

| User Input | Expected Skill Behavior |
|------------|------------------------|
| "Enforce bundle size budget on this Next.js build" | Parse Next.js build output, analyze page bundle sizes, identify oversized chunks, suggest code splitting and lazy loading for specific routes. |
| "Monitor Core Web Vitals for this React app" | Collect LCP, FID, CLS metrics from build or runtime, compare against budgets (LCP < 2.5s, CLS < 0.1), report violations with optimization suggestions. |
| "Check if JS bundle exceeds 200KB" | Analyze webpack/vite stats, calculate total gzipped size, flag if over budget, identify largest dependencies and provide replacement alternatives. |
| "Alert on LCP regression after latest changes" | Compare current LCP against baseline, detect >10% degradation, pinpoint new render-blocking resources or large images added in recent commits. |

## How It Works

```
User provides build output or performance data
          │
          ▼
┌───────────────────────┐
│  Step 1: PARSE       │ → Detect bundler type (webpack/vite/Next.js)
│  (Build Analysis)    │ → Extract stats.json, chunk info, sizes
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 2: MEASURE     │ → Calculate total bundle size
│  (Size Measurement)  │ → Per-chunk breakdown, compression stats
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 3: COLLECT     │ → LCP, FID, CLS, TBT metrics
│  (Web Vitals)        │ → Parse Lighthouse results or RUM data
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 4: COMPARE     │ → Check against configured budgets
│  (Budget Validation) │ → Detect regressions vs baseline
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 5: DETECT      │ → Identify anti-patterns
│  (Issue Detection)   │ → Large deps, missing splits, CLS issues
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 6: SUGGEST     │ → Provide optimization recommendations
│  (Optimization Tips) │ → Code splitting, lazy loading, compression
└───────────────────────┘
          │
          ▼
┌───────────────────────┐
│  Step 7: REPORT      │ → Generate severity report
│  (Severity Report)   │ → Line numbers, evidence, fixes
└───────────────────────┘
          │
          ▼
    Output: Performance budget enforcement report
```

## Dependencies

- **Node.js build tools required** - webpack stats.json or vite bundle analysis output
- **Optional: Lighthouse** - For comprehensive Web Vitals measurement (`npx lighthouse <url>`)
- **Optional: web-vitals library** - For runtime collection in browser applications
- **Recommended**: Run in CI/CD pipeline with `--bail` flag to block regressions

## Best Practices / Notes

- **Set realistic budgets based on your audience**: Mobile users need smaller bundles; consider 3G network constraints
- **Run in CI/CD to block regressions**: Fail builds when critical budgets are exceeded (`npx webpack-bundle-analyzer --report=summary`)
- **Use performance budgets in webpack/vite config**: Configure `performance.maxAssetSize` and `performance.maxEntrypointSize`
- **Combine with Lighthouse CI for trend tracking**: Track metrics over time, not just single snapshots
- **Prioritize Core Web Vitals**: Google uses these as ranking signals; optimize for LCP first (most impactful)
- **Measure on real devices**: Lab data (Lighthouse) is good but RUM (Real User Monitoring) reflects actual user experience
- **Use compression effectively**: Ensure gzip/brotli is enabled in production; measure gzipped sizes against budgets
- **Monitor over time**: Set up dashboards to track performance trends and catch regressions early

## Output Format

The skill outputs a structured performance budget enforcement report:

```markdown
# Performance Budget Report

## Summary
- Build Tool: webpack 5.88.0
- Total JS (gzipped): 245KB | Budget: < 200KB | Status: ❌ Exceeded by 23%
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
Largest Contentful Element: <img src="/hero-banner.jpg" />
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

3. **Remove render-blocking CSS**:
   ```html
   <!-- Defer non-critical styles -->
   <link rel="stylesheet" href="/critical.css" media="print" onload="this.media='all'">
   ```

---

## 🟠 HIGH Issues

### Bundle Size Exceeded: vendor.js
**Severity:** HIGH | **Budget:** < 150KB (gzipped)
**Current:** 245KB (gzipped) | **Over budget by:** 63%
**File:** `stats.json` - chunk "vendor"

**Evidence:**
```json
{
  "name": "vendor",
  "size": 892000,
  "compressedSize": 251000,
  "modules": [
    {"name": "lodash", "size": 72000},
    {"name": "moment", "size": 68000},
    {"name": "axios", "size": 45000}
  ]
}
```

**Issue:** Vendor bundle exceeds budget, primarily due to lodash and moment.js dependencies.

**Fix:** Replace moment.js with date-fns (7KB vs 68KB):
```bash
npm uninstall moment && npm install date-fns
```

Replace lodash with tree-shakeable imports:
```javascript
// Before
import _ from 'lodash';
_.debounce(fn, 300);

// After
import debounce from 'lodash/debounce.js';
```

---

## 🟡 MEDIUM Issues

### Missing Code Splitting on Dashboard Route
**Severity:** MEDIUM | **Type:** Bundle Bloat
**File:** `src/routes.tsx` | **Line:** 12

**Issue:** Dashboard route imports heavy charting library (~150KB) on initial page load.

**Evidence:**
```javascript
// Current: All routes loaded eagerly
import { Dashboard } from '../pages/Dashboard'; // Loads Chart.js (150KB)

const routes = [
  <Route path="/dashboard" element={<Dashboard />} />,
];
```

**Fix:** Lazy load the dashboard route:
```javascript
// Better: Code split on route
const Dashboard = lazy(() => import('../pages/Dashboard'));

const routes = [
  <Route path="/dashboard" element={
    <Suspense fallback={<LoadingSpinner />}>
      <Dashboard />
    </Suspense>
  } />,
];
```

---

## 🟢 LOW Issues

### Missing Image Dimensions (CLS Risk)
**Severity:** LOW | **Type:** Layout Shift Prevention
**File:** `src/components/ProductCard.jsx` | **Line:** 24

**Suggestion:** Add explicit width/height to product images to prevent CLS.

```jsx
// Before
<img src={product.image} alt={product.name} />

// After
<img
  src={product.image}
  alt={product.name}
  width="300"
  height="300"
  style={{ objectFit: 'cover' }}
/>
```

---

## Recommended Actions

1. **Immediate (CRITICAL):** Implement LCP optimizations for hero image
2. **Before Release:** Replace moment.js with date-fns to reduce bundle size
3. **Next Sprint:** Add code splitting for dashboard route
4. **Ongoing:** Set up Lighthouse CI in pipeline to prevent regressions

---
*Generated by Performance Budget Enforcer v1.0*
```

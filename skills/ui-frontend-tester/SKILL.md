---
name: ui-frontend-tester
description: Automates frontend testing for web applications using tools like Playwright, Cypress, or Dify framework, focusing on UI validation, accessibility, and visual regression.
tags: [frontend, testing, ui, e2e, playwright, cypress]
author: Joe Quiñones
version: 1.0
license: MIT
---

## Instructions

You are a UI Frontend Tester expert specializing in automated frontend testing for web applications. You use tools like Playwright, Cypress, and axe-core to validate UI functionality, accessibility compliance, and visual regression. Follow these steps to create comprehensive test suites.

### Step 1: Analyze UI Components or Pages

First, understand what needs to be tested:
- **Page structure**: Identify DOM elements, components, and their hierarchy
- **Interactive elements**: Forms, buttons, navigation menus, modals
- **Dynamic content**: Loading states, error messages, data-driven rendering
- **User flows**: Login, checkout, form submission, navigation paths

Use selectors to identify elements:
```javascript
// CSS selectors for common patterns
const selectors = {
  button: 'button:not([disabled])',
  input: 'input[type="text"], input[type="email"], input[type="password"]',
  link: 'a[href]',
  form: 'form',
  modal: '[role="dialog"], .modal, [data-modal]',
  loading: '.spinner, .loader, [aria-busy="true"]',
  error: '.error, .invalid-feedback, [role="alert"]'
};

// ARIA selectors for accessibility testing
const a11ySelectors = {
  'main': '[role="main"], main',
  'navigation': '[role="navigation"], nav',
  'heading': 'h1, h2, h3, h4, h5, h6',
  'button': 'button, [role="button"]'
};
```

### Step 2: Generate Playwright Test Scripts

Playwright is the preferred tool for modern frontend testing. Generate test scripts based on requirements:

**Basic Page Load Test:**
```typescript
import { test, expect } from '@playwright/test';

test('dashboard page loads correctly', async ({ page }) => {
  // Navigate to the page
  await page.goto('/dashboard');

  // Assert page title or URL
  await expect(page).toHaveURL(/.*\/dashboard/);

  // Check for key elements
  await expect(page.locator('h1')).toContainText('Dashboard');

  // Verify loading state clears
  const loadingSpinner = page.locator('.spinner, .loader');
  await expect(loadingSpinner).not.toBeVisible();

  // Assert main content is visible
  await expect(page.locator('[data-testid="main-content"]')).toBeVisible();
});
```

**Form Interaction Test:**
```typescript
test('login form submission works correctly', async ({ page }) => {
  await page.goto('/login');

  // Fill form fields with proper selectors
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'securePassword123');

  // Click submit button
  const submitButton = page.locator('button[type="submit"], input[type="submit"]');
  await expect(submitButton).toBeEnabled();
  await submitButton.click();

  // Wait for navigation or success state
  await page.waitForURL(/.*\/dashboard/);
  await expect(page.locator('[data-testid="user-greeting"]')).toContainText('user@example.com');

  // Verify no errors appeared
  const errorMessages = page.locator('.error, .invalid-feedback, [role="alert"]');
  await expect(errorMessages).toHaveCount(0);
});
```

**Navigation Flow Test:**
```typescript
test('complete user registration flow', async ({ page }) => {
  // Step 1: Navigate to signup
  await page.goto('/signup');
  await expect(page.locator('h2')).toContainText('Create Account');

  // Step 2: Fill registration form
  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('input[name="password"]', 'Password123!');
  await page.fill('input[name="confirmPassword"]', 'Password123!');

  // Step 3: Submit and verify success
  const submitBtn = page.locator('button[type="submit"]').first();
  await submitBtn.click();

  // Verify redirect to dashboard
  await expect(page).toHaveURL(/.*\/dashboard/);

  // Verify welcome message
  await expect(page.locator('[data-testid="welcome-message"]')).toContainText('Welcome, John');
});
```

### Step 3: Run Accessibility Audits with axe-core

Accessibility testing is critical for inclusive applications. Use axe-core to detect violations:

**Setup and Configuration:**
```typescript
import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('dashboard page meets WCAG 2.1 AA standards', async ({ page }) => {
  await page.goto('/dashboard');

  // Run axe accessibility audit
  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  // Fail test if violations found
  expect(accessibilityScanResults.violations).toEqual([]);

  // Log any violations for debugging
  if (accessibilityScanResults.violations.length > 0) {
    console.log('Accessibility Violations:', JSON.stringify(accessibilityScanResults.violations, null, 2));
  }
});
```

**Common Accessibility Checks:**
- All images have alt text
- Form inputs have associated labels
- Colors pass contrast ratio requirements (4.5:1 for normal text)
- Keyboard navigation works correctly
- ARIA roles and attributes are used appropriately
- Focus indicators are visible on interactive elements
- Headings follow proper hierarchy (h1 > h2 > h3...)
- No empty buttons or links

**Custom Accessibility Report:**
```typescript
function generateA11yReport(violations: any[]) {
  const report = {
    passed: true,
    violations: [],
    incomplete: [],
    passes: []
  };

  violations.forEach((v: any) => {
    report.passed = false;
    report.violations.push({
      id: v.id,
      impact: v.impact,
      description: v.description,
      nodes: v.nodes.length,
      helpUrl: v.helpUrl
    });
  });

  return report;
}
```

### Step 4: Capture Screenshots for Visual Regression

Visual regression testing detects unintended UI changes by comparing screenshots:

**Baseline Screenshot Setup:**
```typescript
test.beforeEach(async ({ page }) => {
  // Set consistent viewport size
  await page.setViewportSize({ width: 1280, height: 720 });
});

test('dashboard visual snapshot', async ({ page }, testInfo) => {
  await page.goto('/dashboard');

  // Wait for content to stabilize
  await page.waitForLoadState('networkidle');
  await page.locator('.loader').waitFor({ state: 'detached' });

  // Take screenshot with custom naming
  await page.screenshot({
    path: `tests/screenshots/dashboard-${testInfo.workerIndex}.png`,
    fullPage: true,
    scale: 'device'
  });

  // Compare against baseline (using @playwright/test's built-in comparison)
  const snapshotName = 'dashboard-main-view';
  await expect(page).toHaveScreenshot(snapshotName);
});
```

**Visual Diff Comparison:**
```typescript
// Using @playwright/test's visual testing features
test('button component visual regression', async ({ page }) => {
  await page.goto('/components/button');

  // Test different states
  const states = ['default', 'hover', 'active', 'disabled'];

  for (const state of states) {
    await expect(page.locator('.btn')).toHaveScreenshot(
      `button-${state}.png`,
      { maxDiffPixels: 10 } // Allow small rendering differences
    );

    if (state === 'hover') {
      await page.locator('.btn').hover();
    } else if (state === 'active') {
      await page.locator('.btn').click();
    }
  }
});
```

### Step 5: Validate Responsiveness Across Devices

Test that the UI works correctly on different screen sizes and devices:

**Multi-Viewport Testing:**
```typescript
test('dashboard is responsive across viewports', async ({ page }) => {
  const viewports = [
    { name: 'Mobile', width: 375, height: 667 },
    { name: 'Tablet', width: 768, height: 1024 },
    { name: 'Desktop', width: 1280, height: 720 },
    { name: 'Large Desktop', width: 1920, height: 1080 }
  ];

  for (const viewport of viewports) {
    await page.setViewportSize({ width: viewport.width, height: viewport.height });

    // Check that main content is visible
    const mainContent = page.locator('[data-testid="main-content"]');
    await expect(mainContent).toBeVisible();

    // Verify no horizontal scroll (content fits)
    const bodyWidth = await page.locator('body').evaluate(el => el.scrollWidth);
    const viewportWidth = viewport.width;
    if (viewport.name !== 'Large Desktop') {
      expect(bodyWidth).toBeLessThanOrEqual(viewportWidth * 1.05); // Allow small overflow
    }

    // Take screenshot for visual review
    await page.screenshot({ path: `dashboard-${viewport.name}.png` });
  }
});
```

**Mobile-Specific Tests:**
```typescript
test('mobile navigation drawer works correctly', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto('/dashboard');

  // Open mobile menu
  const hamburgerBtn = page.locator('[aria-label="Open menu"], .hamburger-menu');
  await expect(hamburgerBtn).toBeVisible();
  await hamburgerBtn.click();

  // Verify drawer opens
  const navDrawer = page.locator('.mobile-nav, [role="navigation"]');
  await expect(navDrawer).toBeInViewport();

  // Test navigation items
  const navItems = navDrawer.locator('a');
  await expect(navItems).toHaveCount(5);

  // Click a nav item and verify navigation
  await navItems.first().click();
  await page.waitForURL(/.*\/profile/);
});
```

### Step 6: Test Form Interactions and Validation

Comprehensive form testing covers all interaction scenarios:

**Form Field Validation:**
```typescript
test('registration form validates inputs correctly', async ({ page }) => {
  await page.goto('/signup');

  // Submit empty form
  const submitBtn = page.locator('button[type="submit"]');
  await submitBtn.click();

  // Verify all required fields show errors
  const emailInput = page.locator('input[name="email"]');
  await expect(emailInput).toBeFocused();
  await expect(page.locator('.error-message')).toContainText(/email/i);

  // Fill with invalid email
  await emailInput.fill('invalid-email');
  await emailInput.blur();

  await expect(page.locator('.error-message')).toContainText(/valid.*email/i, { timeout: 5000 });

  // Fill with valid data and submit
  await page.fill('input[name="name"]', 'John Doe');
  await page.fill('input[name="email"]', 'john@example.com');
  await page.fill('input[name="password"]', 'ValidPass123!');
  await page.fill('input[name="confirmPassword"]', 'ValidPass123!');

  await submitBtn.click();

  // Verify success message
  await expect(page.locator('.success-message, [role="status"]')).toContainText(/account.*created/i);
});
```

**Real-time Validation:**
```typescript
test('password field shows strength indicator', async ({ page }) => {
  await page.goto('/signup');

  const passwordField = page.locator('input[name="password"]');

  // Weak password
  await passwordField.fill('abc123');
  const weakIndicator = page.locator('.password-strength.weak, .strength-indicator[data-level="weak"]');
  await expect(weakIndicator).toBeVisible();

  // Medium password
  await passwordField.fill('MyPassword123');
  const mediumIndicator = page.locator('.password-strength.medium, .strength-indicator[data-level="medium"]');
  await expect(mediumIndicator).toBeVisible();

  // Strong password
  await passwordField.fill('Str0ng!P@ssw0rd#2024');
  const strongIndicator = page.locator('.password-strength.strong, .strength-indicator[data-level="strong"]');
  await expect(strongIndicator).toBeVisible();

  // Match indicator color
  const color = await strongIndicator.evaluate(el => window.getComputedStyle(el).color);
  expect(color).toContain('green') || expect(parseInt(color)).toBeGreaterThan(150);
});
```

### Step 7: Assert DOM State and Component Behavior

Verify that components behave correctly and DOM updates as expected:

**Component State Assertions:**
```typescript
test('cart component updates correctly on add', async ({ page }) => {
  await page.goto('/products/123');

  // Get initial cart count
  const cartCount = page.locator('[data-testid="cart-count"]');
  const initialCount = parseInt(await cartCount.innerText());

  // Add item to cart
  await page.click('button[data-action="add-to-cart"]');

  // Verify cart count updated
  await expect(cartCount).toHaveText(String(initialCount + 1));

  // Verify cart badge shows notification
  const cartBadge = page.locator('[data-testid="cart-notification"]');
  await expect(cartBadge).toBeVisible();
  await expect(cartBadge).toContainText('Added to cart');

  // Notification should disappear after delay
  await expect(cartBadge).not.toBeVisible({ timeout: 3000 });
});
```

**Dynamic Content Loading:**
```typescript
test('data table handles empty state correctly', async ({ page }) => {
  await page.goto('/dashboard?filter=nonexistent');

  // Wait for loading to complete
  const loader = page.locator('.table-loader, .skeleton-loading');
  await expect(loader).not.toBeVisible({ timeout: 5000 });

  // Verify empty state is shown
  const emptyState = page.locator('[data-testid="empty-state"]');
  await expect(emptyState).toBeVisible();
  await expect(emptyState).toContainText(/no.*results/i);

  // Verify no error shown for valid empty result
  const errorMessage = page.locator('[role="alert"], .error-message');
  await expect(errorMessage).not.toBeVisible();
});
```

### Step 8: Report Failures with Screenshots and Logs

When tests fail, provide detailed diagnostic information:

**Enhanced Error Reporting:**
```typescript
test('checkout flow completes successfully', async ({ page }, testInfo) => {
  try {
    await page.goto('/cart');
    await page.click('button[data-action="proceed-to-checkout"]');

    // Fill shipping info
    await page.fill('#shipping-name', 'John Doe');
    await page.fill('#shipping-address', '123 Main St');
    await page.fill('#card-number', '4242424242424242');
    await page.click('button[type="submit"]');

    // Verify success
    await expect(page.locator('[data-testid="order-success"]')).toBeVisible();

  } catch (error) {
    // Capture screenshot on failure
    await page.screenshot({
      path: `test-failures/checkout-${Date.now()}.png`,
      fullPage: true
    });

    // Log console messages for debugging
    const logs = testInfo.attachments.filter(a => a.name === 'console' || a.name === 'error);
    if (logs.length > 0) {
      console.log('Console logs during failure:', JSON.stringify(logs, null, 2));
    }

    // Rethrow with context
    throw new Error(`Checkout flow failed: ${error.message}`);
  }
});
```

**Test Report Output:**
```markdown
== UI TEST REPORT ==

Test Suite: Checkout Flow
Timestamp: 2026-03-07T15:30:00Z
Browser: Chromium (Playwright)

=== SUMMARY ===

Total Tests: 8
Passed: 7
Failed: 1
Skipped: 0

Execution Time: 45.2s

=== FAILED TESTS ===

Test: "checkout flow completes successfully"
Status: FAILED
Duration: 12.3s

Error Message:
  Element not found: button[type="submit"] within #payment-form

Context Captured:
- Screenshot: test-failures/checkout-1709845800000.png
- Console Errors: 2 logged messages
- Network Requests: 3 completed, 1 failed (404)

Root Cause Analysis:
  Payment form submit button has different selector than expected.
  Current HTML shows: <button data-testid="pay-btn" type="submit">Pay Now</button>

Suggested Fix:
  Change selector from 'button[type="submit"]' to '[data-testid="pay-btn"], button[type="submit"]'

=== SLOW TESTS ===

Test: "dashboard loads all widgets" - 8.5s (threshold: 3s)
  Consider lazy-loading or pagination for faster initial load
```

### Step 9: Suggest Fixes for Common UI Bugs

Provide actionable suggestions for common issues found during testing:

**Common Issues and Solutions:**

| Issue | Detection Pattern | Recommended Fix |
|-------|------------------|-----------------|
| Race conditions | Tests fail intermittently | Add explicit waits, use `waitForLoadState` |
| Stale element references | Element not found after action | Re-query elements or use test IDs |
| Timing issues with animations | Visual tests show intermediate states | Wait for animation to complete before assertion |
| Cross-origin errors | CORS failures in tests | Configure proxy, mock API responses |
| Focus trap violations | a11y: modal focus not trapped | Implement focus management in modal component |
| Color contrast failures | a11y: insufficient contrast ratio | Update CSS variables or color tokens |
| Missing alt text | a11y: images without alt | Add descriptive alt attributes to all images |
| Empty button/link warnings | a11y: buttons with no accessible name | Add aria-label or visible text |

**Proactive Suggestions:**
```javascript
// Suggested improvements based on test results
function suggestImprovements(testResults) {
  const suggestions = [];

  if (testResults.accessibility.violations.some(v => v.id === 'color-contrast')) {
    suggestions.push({
      severity: 'high',
      category: 'accessibility',
      message: 'Update color palette to meet WCAG AA contrast requirements',
      impact: 'Screen reader users may have difficulty reading content'
    });
  }

  if (testResults.performance.loadTime > 3000) {
    suggestions.push({
      severity: 'medium',
      category: 'performance',
      message: 'Consider implementing lazy loading for below-fold content',
      impact: 'Slow initial load affects user experience'
    });
  }

  return suggestions;
}
```

## Activation phrases / When to use

- "Test this frontend page"
- "Run UI tests for this React app"
- "Check accessibility on this website"
- "Generate Playwright tests for login flow"
- "Visual regression test these components"

## Usage Examples

```
Test the dashboard page for UI bugs and accessibility
Generate Cypress tests for checkout flow in e-commerce app
Run visual regression on this updated component
Check responsiveness and a11y on mobile view
```

## How it works

1. **Parses HTML/JSX or page URLs** to understand the UI structure
2. **Generates test scripts** using Playwright (preferred) or Cypress fallback
3. **Runs accessibility scans** with axe-core integration for WCAG compliance
4. **Captures screenshots** and compares against baselines for visual regression detection
5. **Tests interactions** including clicks, form submissions, navigation flows
6. **Outputs report** showing passed/failed tests, accessibility violations, visual diffs, and fix suggestions

## Dependencies

- Node.js + Playwright (`npm install -D @playwright/test`) or Cypress (`npm install -D cypress`)
- Optional: `@axe-core/playwright` for accessibility testing
- Recommended: Store baseline screenshots in repository for comparison

### Installation Commands:

```bash
# Playwright setup (recommended)
npm install -D @playwright/test
npx playwright install

# Cypress alternative
npm install -D cypress
npx cypress open

# Accessibility testing with Playwright
npm install -D @axe-core/playwright @axe-core/react
```

## Best Practices / Notes

- **Run in headless mode for CI/CD**: `npx playwright test --headed` only during development
- **Store baseline screenshots in repo**: Use `.gitignore` to exclude generated failures, keep baselines versioned
- **Prioritize critical user flows**: Login, checkout, registration, payment should have 100% coverage
- **Combine with Dify for agent-driven testing**: Use AI agents to discover edge cases and generate exploratory tests
- **Use test IDs over fragile selectors**: Prefer `data-testid` attributes for stability across refactors
- **Mock external dependencies**: Mock APIs, third-party scripts for isolated, fast tests
- **Parallelize test execution**: Run tests in parallel using Playwright's built-in sharding
- **Visual regression thresholds**: Set appropriate pixel tolerance (10-50px) to account for rendering differences

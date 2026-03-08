# UI Frontend Tester Skill

A Claude Code skill for automating frontend testing of web applications using Playwright, Cypress, and axe-core. Focuses on UI validation, accessibility compliance, and visual regression testing.

## Description

The UI Frontend Tester skill provides comprehensive automated testing solutions for web applications. It generates test scripts, performs accessibility audits with WCAG standards, captures screenshots for visual regression detection, and validates responsive behavior across devices. This skill ensures your frontend is functional, accessible, and visually consistent.

## Purpose

Frontend testing often suffers from:
- Manual testing that's slow and error-prone
- Accessibility issues discovered late in development
- Visual regressions going unnoticed after component updates
- Inconsistent behavior across different screen sizes
- Fragile tests that break with minor UI changes

This skill addresses these challenges by providing:
- Automated test generation for common UI patterns
- Integrated accessibility scanning with axe-core
- Visual regression detection to catch unintended UI changes
- Multi-device responsive testing
- Detailed failure reports with screenshots and fix suggestions

## Features

- **Playwright Test Generation**: Creates robust end-to-end tests using the preferred Playwright framework
- **Cypress Support**: Alternative test generation for Cypress-based projects
- **Accessibility Audits**: WCAG 2.1 AA compliance checking with axe-core integration
- **Visual Regression Testing**: Screenshot capture and comparison to detect UI changes
- **Responsive Design Validation**: Multi-viewport testing across mobile, tablet, and desktop
- **Form Interaction Testing**: Comprehensive validation of form inputs, errors, and submissions
- **DOM State Assertions**: Verify component behavior and dynamic content handling
- **Enhanced Failure Reporting**: Screenshots, logs, and root cause analysis for failed tests
- **Fix Suggestions**: Actionable recommendations for common UI bugs and accessibility issues

## How to Use

### Activation Phrases

Use these phrases to invoke the UI Frontend Tester skill:
- "Test this frontend page"
- "Run UI tests for this React app"
- "Check accessibility on this website"
- "Generate Playwright tests for login flow"
- "Visual regression test these components"

### Usage Examples

```bash
# Test dashboard for bugs and accessibility
Test the dashboard page for UI bugs and accessibility

# Generate Cypress tests for e-commerce checkout
Generate Cypress tests for checkout flow in e-commerce app

# Run visual regression on component update
Run visual regression on this updated component

# Check mobile responsiveness and accessibility
Check responsiveness and a11y on mobile view
```

## Examples

### Example 1: Dashboard Page Testing

**Input:** React dashboard application with widgets, charts, and navigation.

**Output:** Comprehensive test suite including:
- Page load validation (title verification, loading state checks)
- Key element assertions (h1 presence, data-testid elements visible)
- Accessibility audit results (WCAG compliance report)
- Responsive behavior tests across 4 viewport sizes
- Form interaction validations if applicable

### Example 2: Login Flow Test Generation

**Input:** Authentication form with email/password fields and validation.

**Output:** Playwright test scripts with:
```typescript
test('login form submission works correctly', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', 'user@example.com');
  await page.fill('input[name="password"]', 'securePassword123');
  const submitButton = page.locator('button[type="submit"]');
  await expect(submitButton).toBeEnabled();
  await submitButton.click();
  await page.waitForURL(/.*\/dashboard/);
});
```

### Example 3: Visual Regression Testing

**Input:** Updated button component with new styling.

**Output:** Visual test report showing:
- Baseline vs current screenshots for all states (default, hover, active, disabled)
- Pixel difference analysis with tolerance settings
- Flags for significant visual changes exceeding threshold
- Recommendations for intentional design updates

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/ui-frontend-tester

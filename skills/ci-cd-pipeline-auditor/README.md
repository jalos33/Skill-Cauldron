# CI/CD Pipeline Auditor Skill

A Claude Code skill for reviewing GitHub Actions workflows for security vulnerabilities, best practices compliance, performance issues, and deployment safety.

## Description

The CI/CD Pipeline Auditor provides systematic analysis of GitHub Actions workflow files to identify security risks, enforce best practices, optimize build performance, and ensure deployment compliance. It scans `.github/workflows/*.yml` files for common pitfalls like secrets exposure, overly broad permissions, unpinned actions, missing OIDC configuration, insufficient approval gates for production deployments, Docker image security issues, reusable workflow pinning, and Dependabot configurations.

## Purpose

CI/CD pipelines are critical infrastructure that often contain security vulnerabilities when not properly reviewed:
- Secrets exposed in logs or workflow files through plaintext values
- Overly broad `write-all` permissions violating least privilege principle
- Unpinned actions (branch references like `@main`) vulnerable to supply chain attacks
- Missing OIDC configuration forcing long-lived credential usage
- No approval gates allowing automatic production deployments
- Poor performance from missing dependency caching and parallelization

This skill addresses these challenges by providing:
- Security vulnerability detection (secrets, permissions, action pinning)
- Best practices validation (caching, matrix strategies, approval gates)
- Performance analysis (redundant steps, parallelization opportunities)
- Compliance checking (production deployment safeguards)
- Structured audit reports with severity levels and fix suggestions

## Features

- **Workflow File Scanning**: Automatically locates and parses `.github/workflows/*.yml` files
- **Security Vulnerability Detection**: Identifies secrets exposure, write-all permissions, unpinned actions, untrusted sources, OIDC misconfigurations
- **Best Practices Validation**: Checks for dependency caching, matrix strategy usage, environment protection rules
- **Performance Analysis**: Detects redundant steps and identifies parallelization opportunities
- **Structured Audit Reports**: Generates reports with severity levels (CRITICAL/HIGH/MEDIUM/LOW) per workflow, including emoji badges (🔴 CRITICAL / 🟡 HIGH / 🔵 MEDIUM / 🟢 LOW)
- **Actionable Fix Suggestions**: Provides improved YAML snippets demonstrating secure configurations
- **OIDC Configuration Review**: Validates proper OIDC setup for cloud provider authentication (AWS/GCP/Azure) with specific configuration examples
- **Docker Security Checks**: Detects unpinned Docker images, root privileges, and non-root container issues
- **Reusable Workflow Detection**: Identifies reusable workflows and checks their pinning status
- **Dependabot Configuration Check**: Verifies dependency update automation setup
- **Compliance Checklist**: Includes pre-computed checklist for security hardening with all new items

## How to Use

### Activation Phrases

Use these phrases to invoke the CI/CD Pipeline Auditor skill:
- "Audit my GitHub Actions workflows"
- "Review CI/CD security in this repo"
- "Check GitHub Actions best practices"
- "Find vulnerabilities in my workflows"
- "Improve this GitHub Actions pipeline"

### Usage Examples

```bash
# Audit all workflows for security risks
Audit all workflows in this repo for security risks

# Review CI/CD pipeline for best practices and performance
Review my CI/CD pipeline for best practices and performance

# Check if workflows use pinned versions and OIDC
Check if my GitHub Actions use pinned versions and OIDC

# Find secrets exposure or overly broad permissions
Find secrets exposure or overly broad permissions in workflows
```

## Examples

### Example 1: Comprehensive Security Audit

**Input:** "Audit all workflows in this repo for security risks"

**Output:** Full audit report showing:
- Summary of findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
- Per-workflow risk assessment with specific vulnerabilities
- Identified issues: write-all permissions, unpinned actions, secrets exposure
- Recommended fixes with before/after YAML examples
- Action items prioritized by urgency and estimated effort

### Example 2: Best Practices Review

**Input:** "Review my CI/CD pipeline for best practices and performance"

**Output:** Performance and compliance analysis including:
- Missing dependency caching identification (npm, pip, maven)
- Matrix strategy opportunities for parallel test execution
- Redundant checkout steps or echo statements exposing info
- Optimization suggestions with estimated impact on build times

### Example 3: OIDC and Action Pinning Check

**Input:** "Check if my GitHub Actions use pinned versions and OIDC"

**Output:** Security configuration review covering:
- Action version pinning status (SHA vs tag vs branch reference)
- OIDC federation setup for cloud providers
- Long-lived credential usage detected with migration recommendations
- Trust verification for third-party action sources

## Security Findings Reference

### 🔴 CRITICAL Severity Issues (< 1 hour response)

| Issue | Description | Fix |
|-------|-------------|-----|
| `SECRETS_IN_RUN_COMMAND` | Secrets used in run commands may leak to logs | Use env blocks: `env: KEY: ${{ secrets.KEY }}` |
| `WRITE_ALL_PERMISSIONS` | Workflow has write-all permissions | Specify exact required permissions only |
| `UNPINNED_BRANCH_REFERENCE` | Action pinned to mutable branch (`@main`, `@master`) | Pin to commit SHA for reproducibility |

### 🟡 HIGH Severity Issues (< 24 hour response)

| Issue | Description | Fix | Badge |
|-------|-------------|-----|-------|
| `MAJOR_VERSION_ONLY` | Action uses only major version (e.g., `@v4`) | Pin to specific tag or SHA | ⏳ |
| `AUTO_DEPLOY_TO_MAIN` | Auto-deploys without approval gate | Add environment protection rules | 🔒 |
| `UNTRUSTED_ACTION_SOURCE` | Action from unverified publisher | Use trusted actions from verified sources | ⚠️ |
| `DOCKER_ROOT_PRIVILEGES` | Container runs with elevated privileges | Remove --privileged flag; use specific capabilities | 🐳 |

### 🔵 MEDIUM Severity Issues (< 1 week response)

| Issue | Description | Fix | Badge |
|-------|-------------|-----|-------|
| `NO_DEPENDENCY_CACHING` | Dependencies installed without caching | Add `actions/cache` or setup-node with cache | 📦 |
| `OIDC_WITHOUT_PROVIDER_SETUP` | OIDC permissions set but no provider configured | Configure proper OIDC identity provider | 🔑 |
| `LONG_LIVED_AWS_CREDENTIALS` | Uses long-lived AWS credentials instead of OIDC | Use OIDC: id-token: write + role-to-assume | ☁️ |
| `DOCKER_IMAGE_LATEST_TAG` | Container uses :latest tag - may change between runs | Pin to specific version tag or SHA digest | 🐳 |
| `DOCKER_ROOT_USER` | Container may run as root user | Add options: "user: 1000" to run as non-root | 🐳 |

### 🟢 LOW Severity Issues (< 1 month response)

| Issue | Description | Fix | Badge |
|-------|-------------|-----|-------|
| `NO_MATRIX_STRATEGY` | Could benefit from parallel execution | Add matrix strategy for OS/version combinations | ⚡ |
| `REDUNDANT_CHECKOUT` | Multiple checkout steps in same job | Remove duplicate checkouts | ♻️ |
| `NO_DEPENDABOT_CONFIG` | No dependabot configuration found | Create .github/dependabot.yml with updates | 🤖 |

## Recommended Fixes

### Least Privilege Permissions

```yaml
# BEFORE (insecure)
permissions: write-all

# AFTER (secure - least privilege)
permissions:
  contents: read
  pull-requests: read
  checks: write
  security-events: write
```

### Pin Actions to Commit SHA

```yaml
# BEFORE (vulnerable to supply chain attacks)
uses: actions/checkout@main
uses: actions/setup-node@v4

# AFTER (secure - pinned to specific commits)
uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1
```

### OIDC Instead of Long-Lived Secrets

```yaml
# BEFORE (insecure - long-lived credentials)
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
steps:
  - uses: aws-actions/configure-aws-credentials@v2

# AFTER (secure - OIDC federation)
permissions:
  id-token: write
  contents: read
steps:
  - name: Configure AWS credentials via OIDC
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
      aws-region: us-east-1
```

### Add Approval Gate for Production

```yaml
# BEFORE (insecure - auto-deploy)
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh

# AFTER (secure - requires approval)
on:
  push:
    branches: [main]
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # Requires approval in repo settings
    steps:
      - run: ./deploy.sh
```

## Best Practices Checklist

- [ ] No secrets exposed in logs or workflow files
- [ ] All actions pinned to commit SHAs or specific tags
- [ ] Least-privilege permissions applied to all workflows
- [ ] OIDC used instead of long-lived credentials for cloud providers (AWS/GCP/Azure)
- [ ] Environment protection rules configured for production deployments
- [ ] Required reviews enforced before deployment via repository settings
- [ ] Dependency caching implemented in build jobs (npm, pip, maven)
- [ ] Matrix strategy used for parallel test execution across OS/node versions
- [ ] Docker images pinned to version tags or SHA digests
- [ ] No containers running with root privileges or as root user
- [ ] Reusable workflows pinned to specific versions
- [ ] Dependabot configured with auto-merge enabled

## License

MIT License - see [SKILL.md](./SKILL.md) for full license text.

## Repository

Source: https://github.com/jalos33/Skill-Cauldron/tree/main/skills/ci-cd-pipeline-auditor

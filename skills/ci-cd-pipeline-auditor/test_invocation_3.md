# Test Invocation 3: "Check workflows for pinned actions, OIDC, Docker security, and Dependabot config"

This invocation focuses on **security configuration review**, including action pinning verification, multi-cloud OIDC patterns, Docker container security checks, and Dependabot configuration validation.

```bash
$ python run_tests.py --focus security-config
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report - Security Configuration Focus
   Workflows Analyzed: ci.yml, deploy.yml
   Generated: 2026-03-07 14:38:45
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 3 (requires immediate attention)
├─ 🟡 HIGH: 5 (should be addressed soon)
├─ 🔵 MEDIUM: 6 (plan to fix this sprint)
└─ 🟢 LOW: 1 (address when convenient)

**Overall Risk Assessment:** 🔴 HIGH RISK - Critical vulnerabilities require immediate attention


## 🔍 DETAILED FINDINGS

| Severity | Issue Type | Location | Description |
|----------|------------|----------|-------------|
| 🔴 CRITICAL | `WRITE_ALL_PERMISSIONS` | ci.yml (root level) | Workflow has write-all permissions violating least privilege principle |
| 🔴 CRITICAL | `UNPINNED_BRANCH_REFERENCE` | ci.yml (build step 1) | Action pinned to mutable branch: actions/checkout@main |
| 🔴 CRITICAL | `SECRETS_IN_RUN_COMMAND` | ci.yml (build step 4) | Potential secrets exposure in echo command |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | ci.yml (build step 2) | Action uses only major version: actions/setup-node@v4 |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | deploy.yml (deploy-production step 1) | Action uses only major version: actions/checkout@v4 |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | deploy.yml (deploy-production step 2) | Action uses only major version: actions/setup-python@v5 |
| 🟡 HIGH | `AUTO_DEPLOY_TO_MAIN` | deploy.yml (deploy-production) | Auto-deploys to production without approval gate. Environment protection rules not configured. |
| 🔵 MEDIUM | `LONG_LIVED_AWS_CREDENTIALS` | ci.yml (build) | Workflow uses long-lived AWS credentials instead of OIDC federation. |
| 🔵 MEDIUM | `LONG_LIVED_AWS_CREDENTIALS` | deploy.yml (deploy-production) | Workflow uses long-lived AWS credentials instead of OIDC federation. |
| 🔵 MEDIUM | `OIDC_WITHOUT_PROVIDER_SETUP` | ci.yml (build) | OIDC id-token: write permission set but no cloud provider action detected |
| 🔵 MEDIUM | `OIDC_WITHOUT_PROVIDER_SETUP` | deploy.yml (deploy-production) | OIDC configured but role-to-assume not specified properly |
| 🟢 LOW | `NO_DEPENDABOT_CONFIG` | .github/dependabot.yml | No Dependabot configuration found. Dependency updates are not automated. |


## 🔐 ACTION PINNING ANALYSIS

### Current Action Pinning Status

| Workflow | Step | Reference Used | Type | Security Level | Recommendation |
|----------|------|---------------|------|---------------|----------------|
| ci.yml | build step 1 | `actions/checkout@main` | Branch ref | ❌ CRITICAL | Pin to specific SHA commit |
| ci.yml | build step 2 | `actions/setup-node@v4` | Major version only | ⚠️ HIGH | Pin to full tag (e.g., @v4.1.0) or SHA |
| deploy.yml | deploy step 1 | `actions/checkout@v4` | Major version only | ⚠️ HIGH | Pin to full tag (e.g., @v4.1.0) or SHA |
| deploy.yml | deploy step 2 | `actions/setup-python@v5` | Major version only | ⚠️ HIGH | Pin to full tag (e.g., @v5.0.0) or SHA |
| deploy.yml | deploy step 3 | `aws-actions/configure-aws-credentials@v2` | Major version only | ⚠️ HIGH | Pin to specific version tag or SHA |

### Best Practice: SHA Pinning

```yaml
# ❌ UNSAFE - Mutable branch reference
uses: actions/checkout@main

# ⚠️ MEDIUM RISK - Only major version (can update within v4)
uses: actions/setup-node@v4

# ✅ SECURE - Specific tag version (stable within minor)
uses: actions/setup-node@v4.1.0

# ✅ MOST SECURE - Commit SHA (completely deterministic)
uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
```

### How to Find Action SHAs

**Method 1 - GitHub API:**
```bash
# Get tag SHA for a specific version
curl -s https://api.github.com/repos/actions/checkout/git/ref/tags/v4.1.1 | grep '"sha"'

# Get latest release tag
curl -s https://api.github.com/repos/actions/checkout/releases/latest | jq '.tag_name'


**Method 2 - Use the `gh` CLI:**
```bash
gh api repos/actions/checkout/git/ref/tags/v4.1.1 | jq '.object.sha'


### Method 3 - Online Tools:
- https://github.com/actions/checkout/releases (view release notes with SHAs)
- https://github.com/actions/setup-node/releases

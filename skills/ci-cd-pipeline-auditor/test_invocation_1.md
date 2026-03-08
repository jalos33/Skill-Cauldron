# Test Invocation 1: "Audit my GitHub Actions workflows for security risks"

```bash
$ python run_tests.py
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report
   Workflows Analyzed: ci.yml, deploy.yml
   Generated: 2026-03-07 14:32:15
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 3 (requires immediate attention)
├─ 🟡 HIGH: 4 (should be addressed soon)
├─ 🔵 MEDIUM: 4 (plan to fix this sprint)
└─ 🟢 LOW: 0 (address when convenient)

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
| 🔵 MEDIUM | `NO_DEPENDENCY_CACHING` | ci.yml (build) | No dependency caching for npm packages |


## 💡 DETAILED FINDINGS WITH FIXES

### 🔴 CRITICAL: WRITE_ALL_PERMISSIONS

**Location:** ci.yml - root level

**Description:** Workflow has write-all permissions violating least privilege principle. This grants excessive permissions to all workflow operations, increasing blast radius if the workflow is compromised.

**Recommendation:** Specify exact required permissions only.

**BEFORE (from your workflow):**
```yaml
permissions: write-all  # ❌ Grants everything!
```

**AFTER (secure - least privilege):**
```yaml
permissions:
  contents: read          # Required for checkout
  pull-requests: read     # Required for PR comments
  checks: write           # Required for status reports

jobs:
  build:
    permissions:
      contents: read      # Override for this job only
```

---

### 🔴 CRITICAL: UNPINNED_BRANCH_REFERENCE

**Location:** ci.yml - build step 1

**Description:** Action pinned to mutable branch `actions/checkout@main`. This makes the workflow vulnerable to supply chain attacks and unpredictable behavior if the main branch is modified.

**Recommendation:** Pin to commit SHA for reproducibility and supply chain security.

**BEFORE (from your workflow):**
```yaml
- uses: actions/checkout@main    # ❌ Mutable branch!
```

**AFTER (secure - pinned to SHA):**
```yaml
# Get latest commit SHA via:
# curl https://api.github.com/repos/actions/checkout/git/ref/tags/v4.1.1 | grep sha

- uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
  with:
    fetch-depth: 0  # Optional: needed for semantic release, etc.
```

---

### 🔴 CRITICAL: SECRETS_IN_RUN_COMMAND

**Location:** ci.yml - build step 4

**Description:** Potential secrets exposure in echo command. The workflow echoes `$API_KEY` to stdout which will be logged and potentially exposed in GitHub Actions logs, CI/CD history, or through log aggregation systems.

**Recommendation:** Use env blocks instead of run commands for secrets; never echo secrets.

---

### 🟡 HIGH: MAJOR_VERSION_ONLY

**Location:** ci.yml - build step 2

**Description:** Action uses only major version: `actions/setup-node@v4`. This may cause unexpected changes when the action updates within the major version.

**Recommendation:** Pin to specific tag (e.g., v4.0) or SHA for reproducibility.

---

### 🟡 HIGH: MAJOR_VERSION_ONLY

**Location:** deploy.yml - deploy-production step 1

**Description:** Action uses only major version: `actions/checkout@v4`. This may cause unexpected changes when the action updates within the major version.

**Recommendation:** Pin to specific tag (e.g., v4.0) or SHA for reproducibility.

---

### 🟡 HIGH: MAJOR_VERSION_ONLY

**Location:** deploy.yml - deploy-production step 2

**Description:** Action uses only major version: `actions/setup-python@v5`. This may cause unexpected changes when the action updates within the major version.

**Recommendation:** Pin to specific tag (e.g., v5.0) or SHA for reproducibility.

---

### 🟡 HIGH: AUTO_DEPLOY_TO_MAIN

**Location:** deploy.yml - deploy-production

**Description:** Auto-deploys to production without approval gate. Environment protection rules not configured. This allows immediate deployment on every push to main, potentially propagating bugs instantly.

**Recommendation:** Add environment: production to require manual approval.

---

### 🔵 MEDIUM: LONG_LIVED_AWS_CREDENTIALS

**Location:** ci.yml - build

**Description:** Workflow uses long-lived AWS credentials instead of OIDC federation. This creates security risks if secrets are leaked and requires manual rotation management.

**Recommendation:** Use OIDC: add id-token: write to permissions and configure-aws-credentials with role-to-assume.

**BEFORE (from your workflow):**
```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

steps:
  - uses: aws-actions/configure-aws-credentials@v2
    with:
      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**AFTER (secure - using OIDC):**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS via OIDC
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
      aws-region: us-east-1
```

---

### 🔵 MEDIUM: LONG_LIVED_AWS_CREDENTIALS

**Location:** deploy.yml - deploy-production

**Description:** Workflow uses long-lived AWS credentials instead of OIDC federation. This creates security risks if secrets are leaked and requires manual rotation management.

**Recommendation:** Use OIDC: add id-token: write to permissions and configure-aws-credentials with role-to-assume.

---

### 🔵 MEDIUM: NO_DEPENDENCY_CACHING

**Location:** ci.yml - build

**Description:** No dependency caching for npm packages. Each workflow run reinstalls all dependencies from scratch, increasing build times and costs.

**Recommendation:** Add actions/setup-node with cache: 'npm' for npm caching.


## 🛠️ RECOMMENDED FIXES (With Complete Examples)

### 1. Apply Least Privilege Permissions

**Problem:** Using `permissions: write-all` grants excessive permissions, violating the principle of least privilege.

**Solution:** Specify only the exact permissions your workflow needs.

**BEFORE (from your workflow):**
```yaml
permissions: write-all  # ❌ Grants everything!
```

**AFTER (secure - least privilege):**
```yaml
permissions:
  contents: read          # Required for checkout
  pull-requests: read     # Required for PR comments
  checks: write           # Required for status reports

jobs:
  build:
    permissions:
      contents: read      # Override for this job only
```

---

### 2. Pin Actions to Specific Versions (SHA or Full Tag)

**Problem:** Using mutable references like `@main` or major versions only (`@v4`) makes workflows vulnerable to supply chain attacks and unpredictable changes.

**Solution:** Pin actions to specific commit SHAs for maximum security, or at minimum use full version tags (e.g., @v4.1.0).

**BEFORE (from your workflow):**
```yaml
- uses: actions/checkout@main    # ❌ Mutable branch!
- uses: actions/setup-node@v4   # ❌ Only major version
```

**AFTER (secure - pinned to SHA):**
```yaml
# Get latest commit SHA via:
# curl https://api.github.com/repos/actions/checkout/git/ref/tags/v4.1.1 | grep sha

- uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
  with:
    fetch-depth: 0  # Optional: needed for semantic release, etc.

- uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1
  with:
    node-version: '20'
    cache: 'npm'
```

---

### 3. Use OIDC Federation Instead of Long-Lived Credentials (Multi-Cloud)

**Problem:** Storing and using long-lived credentials (AWS keys, GCP service account JSON, Azure service principals) creates security risks if leaked and requires rotation management.

**Solution:** Use OIDC federation to obtain temporary credentials dynamically. Configure once in cloud provider IAM, then use `id-token: write` permission in workflows.

**BEFORE (AWS - long-lived credentials from your workflow):**
```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

steps:
  - uses: aws-actions/configure-aws-credentials@v2
    with:
      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**AFTER (AWS - OIDC federation):**
```yaml
# First, create IAM role in AWS with trust policy:
# Principal: token.actions.githubusercontent.com
# Condition: repo:jos33/Skill-Cauldron matches your repo

permissions:
  id-token: write    # Required for OIDC
  contents: read

steps:
  - name: Configure AWS credentials via OIDC
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
      aws-region: us-east-1
```

**GCP OIDC Example:**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Authenticate to GCP via OIDC
    uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
      service_account: my-service-account@my-project.iam.gserviceaccount.com
```

**Azure OIDC Example:**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - name: Login to Azure via OIDC
    uses: azure/login@v1
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
```

---

### 4. Add Approval Gates for Production Deployments

**Problem:** Automatic deployments to production without approval can propagate bugs or malicious code instantly.

**Solution:** Use GitHub Environment protection rules to require manual approval before production deployments.

**BEFORE (from your workflow - auto-deploy):**
```yaml
on:
  push:
    branches: [main]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh production  # Runs immediately!
```

**AFTER (secure - requires approval):**
```yaml
on:
  push:
    branches: [main]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # ✅ Requires approval in repo settings!
    steps:
      - run: ./deploy.sh production
```

**Repository Configuration Required:**
1. Go to Settings → Environments → `production`
2. Enable 'Require a manual approval'
3. Add required reviewers (at least 2 recommended)
4. Set timeout (e.g., 24 hours for auto-rejection)

---

### 5. Implement Dependency Caching

**Problem:** Installing dependencies without caching increases build times and costs.

**Solution:** Use built-in caching features or actions/cache to store dependency artifacts between runs.

**npm Example (built-in cache):**
```yaml
- name: Setup Node.js with cache
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'        # ✅ Built-in npm caching

- name: Install dependencies (uses cache)
  run: npm ci
```

**pip Example (actions/cache):**
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-

- name: Install dependencies (uses cache)
  run: pip install -r requirements.txt
```

---

### 6. Use Matrix Strategy for Test Parallelization

**Problem:** Running tests sequentially across different platforms/versions wastes time and resources.

**Solution:** Use matrix strategy to run multiple test configurations in parallel jobs.

**Example - Matrix strategy for parallel tests:**
```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
        exclude:
          - os: macos-latest
            node-version: 16   # Skip unsupported combo
      fail-fast: false         # ✅ Run all even if one fails

    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

---

### 7. Configure Dependabot for Automated Dependency Updates

**Problem:** Manually updating dependencies is error-prone and slows down security patching.

**Solution:** Enable Dependabot to automatically create PRs for dependency updates, with auto-merge for non-breaking changes.

**Complete Dependabot configuration (create .github/dependabot.yml):**
```yaml
# version: 2 - Required format
version: 2
updates:

  # Enable version updates for npm
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"       # Check weekly
    open-pull-requests-limit: 10  # Max concurrent PRs
    automerged-limits:
      minor-versions: true     # Auto-merge non-breaking changes
    labels:
      - dependencies
      - npm

  # Enable version updates for GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - dependencies
      - github-actions
```

**Benefits of auto-merge:**
- Security patches applied automatically when CI passes
- Reduces technical debt from outdated dependencies
- Faster response to newly discovered vulnerabilities
- Configure branch protection rules to require reviews for major version updates


## ✅ ACTION ITEMS (Prioritized by Urgency)

### 🔴 IMMEDIATE (< 1 hour response)

1. [🔴 WRITE_ALL_PERMISSIONS]
   Location: ci.yml (root level)
   Fix: Specify exact required permissions only

2. [🔴 UNPINNED_BRANCH_REFERENCE]
   Location: ci.yml (build step 1)
   Fix: Pin to commit SHA for reproducibility and supply chain security

3. [🔴 SECRETS_IN_RUN_COMMAND]
   Location: ci.yml (build step 4)
   Fix: Use env blocks instead of run commands for secrets; never echo secrets

### 🟡 SOON (< 24 hours response)

1. [🟡 MAJOR_VERSION_ONLY]
   Location: ci.yml (build step 2)
   Fix: Pin to specific tag (e.g., v4.0) or SHA for reproducibility

2. [🟡 MAJOR_VERSION_ONLY]
   Location: deploy.yml (deploy-production step 1)
   Fix: Pin to specific tag (e.g., v4.0) or SHA for reproducibility

3. [🟡 MAJOR_VERSION_ONLY]
   Location: deploy.yml (deploy-production step 2)
   Fix: Pin to specific tag (e.g., v5.0) or SHA for reproducibility

4. [🟡 AUTO_DEPLOY_TO_MAIN]
   Location: deploy.yml (deploy-production)
   Fix: Add environment: production to require manual approval

### 🔵 THIS SPRINT (< 1 week response)

1. [🔵 LONG_LIVED_AWS_CREDENTIALS]
   Location: ci.yml (build)
   Fix: Use OIDC: add id-token: write to permissions and configure-aws-credentials with role-to-assume

2. [🔵 LONG_LIVED_AWS_CREDENTIALS]
   Location: deploy.yml (deploy-production)
   Fix: Use OIDC: add id-token: write to permissions and configure-aws-credentials with role-to-assume

3. [🔵 NO_DEPENDENCY_CACHING]
   Location: ci.yml (build)
   Fix: Add actions/setup-node with cache: 'npm' for npm caching


## 📋 SECURITY BEST PRACTICES CHECKLIST

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

================================================================================
📌 For more details on security best practices, see the SKILL.md documentation.
   Total findings: 10 | Risk level: 🔴 HIGH RISK - Critical vulnerabilities require immediate attention
================================================================================

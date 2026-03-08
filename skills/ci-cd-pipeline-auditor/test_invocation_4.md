# Test Invocation 4: "Audit reusable workflow for pinning and security"

This invocation focuses on **reusable workflow patterns** including `workflow_call` triggers, cross-repository references, and shared action usage.

```bash
$ python run_tests.py --focus reusable-workflows
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report - Reusable Workflows Focus
   Workflows Analyzed: reusable-workflow.yml
   Generated: 2026-03-07 15:45:00
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 5 (requires immediate attention)
├─ 🟡 HIGH: 3 (should be addressed soon)
├─ 🔵 MEDIUM: 2 (plan to fix this sprint)
└─ 🟢 LOW: 1 (address when convenient)

**Overall Risk Assessment:** 🔴 HIGH RISK - Critical vulnerabilities in reusable workflow patterns require immediate attention


## 🔍 DETAILED FINDINGS

| Severity | Issue Type | Location | Description |
|----------|------------|----------|-------------|
| 🔴 CRITICAL | `WRITE_ALL_PERMISSIONS` | reusable-workflow.yml (root level) | Workflow has write-all permissions violating least privilege principle |
| 🔴 CRITICAL | `UNPINNED_BRANCH_REFERENCE` | build step 2 | Action pinned to mutable branch: actions/checkout@main |
| 🔴 CRITICAL | `REUSABLE_WORKFLOW_UNPINNED` | build step 1 | Reusable workflow referenced without version: ./.github/workflows/shared-actions/setup-env.yml |
| 🔴 CRITICAL | `SECRETS_IN_RUN_COMMAND` | build step 5 | Potential secrets exposure in echo command for API_KEY |
| 🔴 CRITICAL | `UNPINNED_BRANCH_REFERENCE` | build step 4 | Action pinned to mutable branch: jos33/shared-actions/.github/workflows/build.yml@main |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | build step 3 | Action uses only major version: actions/setup-node@v4 |
| 🟡 HIGH | `UNPINNED_BRANCH_REFERENCE` | build step 7 | Action pinned to mutable branch: actions/cache@master |
| 🟡 HIGH | `DOCKER_IMAGE_UNPINNED` | build step 6 | Docker image using unpinned tag: node:latest |
| 🔵 MEDIUM | `NO_MATRIX_STRATEGY` | reusable-build job | Job could benefit from matrix strategy for parallel execution. |
| 🟢 LOW | `DOCKER_LATEST_TAG` | build step 6 | Multiple Docker images using :latest tag |


## 🔄 REUSABLE WORKFLOW ANALYSIS

### Reusable Workflow Reference Patterns

| Workflow | Reference Pattern | Type | Security Level | Recommendation |
|----------|------------------|------|---------------|----------------|
| shared-actions/setup-env.yml | `./.github/workflows/shared-actions/setup-env.yml` | Local | ❌ CRITICAL | Pin to specific commit SHA or version tag |
| jos33/shared-actions/build.yml | `jos33/shared-actions/.github/workflows/build.yml@main` | Cross-repo | ❌ CRITICAL | Use version tag instead of @main branch |

### Best Practice: Reusable Workflow Versioning

```yaml
# ❌ UNSAFE - Local reference without pinning
- uses: ./.github/workflows/shared-actions/setup-env.yml

# ⚠️ MEDIUM RISK - Cross-repo with mutable branch
- uses: jos33/shared-actions/.github/workflows/build.yml@main

# ✅ SECURE - Local workflow with version tag (via action reference)
- uses: ./path/to/workflow/.github/workflows/reusable.yml@v1.0.0

# ✅ MOST SECURE - Cross-repo pinned to SHA
- uses: jos33/shared-actions/.github/workflows/build.yml@c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7

# ✅ SECURE - Cross-repo with version tag
- uses: jos33/shared-actions/.github/workflows/build.yml@v1.2.0
```

### How to Pin Reusable Workflows

**For local reusable workflows (same repo):**
```yaml
# Reference the workflow file directly with a branch/tag reference
- uses: ./.github/workflows/reusable.yml@v1.0.0  # Tag reference
# OR
- uses: ./.github/workflows/reusable.yml@c5d4a7e...  # Commit SHA
```

**For cross-repository reusable workflows:**
```yaml
# Use full repository path with version tag
- uses: owner/repo/.github/workflows/workflow-name.yml@v1.0.0

# Or pin to specific commit SHA for maximum security
- uses: owner/repo/.github/workflows/workflow-name.yml@a1b2c3d4e5f6...
```


## 🐳 DOCKER SECURITY ANALYSIS

### Docker Image Security Status

| Job | Container Image | Tag Type | Security Level | Recommendation |
|-----|-----------------|----------|---------------|----------------|
| test container | `node:latest` | :latest tag | ⚠️ HIGH RISK | Pin to specific version (e.g., node@20.10.0) |

### Best Practice: Docker Image Pinning

```yaml
# ❌ UNSAFE - Using :latest tag (unpredictable updates)
- name: Run tests in container
  uses: addnab/docker-run-action@v3
  with:
    run: docker run node:latest npm test

# ⚠️ MEDIUM RISK - Using tag without digest (can update)
- name: Run tests in container
  uses: addnabdocker-run-action@v3
  with:
    run: docker run node:20.10.0 npm test

# ✅ SECURE - Pinned to specific version with digest
- name: Run tests in container
  uses: addnab/docker-run-action@v3
  with:
    run: docker run node@sha256:c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7e8f9b0c1d2e3f4a5b6c7d8e9 npm test
```

### How to Find Image Digests

**Method 1 - Docker pull:**
```bash
docker pull node:20.10.0
# Output includes digest: node@sha256:c5d4a7e...
```

**Method 2 - Docker Hub API:**
```bash
curl https://hub.docker.com/v2/repositories/library/node/tags/20.10.0 | jq '.digest'
```


## 🔐 DETAILED FINDINGS WITH FIXES (Reusable Workflows Focus)

### 🔴 CRITICAL: REUSABLE_WORKFLOW_UNPINNED - Local Reference

**Location:** reusable-workflow.yml - build step 1

**Description:** Reusable workflow referenced locally without version pinning. This makes the CI/CD pipeline vulnerable to supply chain attacks if the shared workflow file is modified maliciously or accidentally.

**Impact:** Compromised shared workflows can affect all dependent pipelines; no audit trail for changes; unpredictable behavior.

**Recommendation:** Pin local reusable workflows to specific commit SHAs or version tags.

**BEFORE (insecure - unpinned):**
```yaml
jobs:
  reusable-build:
    steps:
      # ❌ No version pinning!
      - uses: ./.github/workflows/shared-actions/setup-env.yml
```

**AFTER (secure - pinned to SHA):**
```yaml
jobs:
  reusable-build:
    steps:
      # ✅ Pinned to specific commit
      - uses: ./.github/workflows/shared-actions/setup-env.yml@c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7

# Alternative: Use version tag (requires git tags)
      - uses: ./.github/workflows/shared-actions/setup-env.yml@v1.0.0
```


### 🔴 CRITICAL: REUSABLE_WORKFLOW_UNPINNED - Cross-Repository Reference

**Location:** reusable-workflow.yml - build step 4

**Description:** Reusable workflow from another repository referenced with mutable branch reference (@main). This is a critical supply chain risk as the target repository could be compromised or the main branch could have breaking changes.

**Impact:** External repository compromise affects your CI/CD; no control over upstream changes; potential for malicious code injection.

**Recommendation:** Pin cross-repository reusable workflows to specific version tags or commit SHAs.

**BEFORE (insecure - mutable branch):**
```yaml
jobs:
  reusable-build:
    steps:
      # ❌ Using @main from external repo!
      - uses: jos33/shared-actions/.github/workflows/build.yml@main
```

**AFTER (secure - version tag):**
```yaml
jobs:
  reusable-build:
    steps:
      # ✅ Pinned to version tag
      - uses: jos33/shared-actions/.github/workflows/build.yml@v1.2.0

# Most secure: Pin to commit SHA
      - uses: jos33/shared-actions/.github/workflows/build.yml@a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
```


### 🔴 CRITICAL: SECRETS_IN_RUN_COMMAND

**Location:** reusable-workflow.yml - build step 5

**Description:** Potential secrets exposure in echo command. The workflow echoes `${{ secrets.API_KEY }}` to stdout which will be logged and potentially exposed in GitHub Actions logs, CI/CD history, or through log aggregation systems.

**Impact:** Secrets exposed in logs can be accessed by anyone with repository read access; secrets may be indexed by external log aggregators; permanent exposure even after secret rotation.

**Recommendation:** Use env blocks instead of run commands for secrets validation; never echo secrets to stdout.

**BEFORE (insecure - echoing secrets):**
```yaml
- name: Validate API key
  run: |
    echo "API Key is: ${{ secrets.API_KEY }}"  # ❌ EXPOSES SECRET!
    if [ "$API_KEY" = "" ]; then
      echo "Error: API key required"
      exit 1
    fi
```

**AFTER (secure - validate without exposing):**
```yaml
- name: Validate API key present
  env:
    API_KEY_REQUIRED: ${{ secrets.API_KEY }}  # ✅ Secret in env, not echoed
  run: |
    if [ -z "$API_KEY_REQUIRED" ]; then
      echo "Error: API key secret is required but not configured"
      exit 1
    fi

# Alternative: Use GitHub's built-in secret validation
- name: Validate required secrets
  uses: actions/github-script@v7
  with:
    script: |
      const secrets = context.secretNames || [];
      if (!secrets.includes('API_KEY')) {
        throw new Error('Required secret API_KEY is missing');
      }
```


### 🟡 HIGH: DOCKER_IMAGE_UNPINNED

**Location:** reusable-workflow.yml - build step 6

**Description:** Docker image using `node:latest` tag which always pulls the most recent version. This causes unpredictable builds and can introduce breaking changes without warning.

**Impact:** Builds fail unexpectedly when upstream images change; security vulnerabilities in new image versions not vetted; inconsistent CI/CD behavior across runs.

**Recommendation:** Pin Docker images to specific version tags or SHA digests for reproducible builds.

**BEFORE (insecure - :latest tag):**
```yaml
- name: Run tests in container
  uses: addnab/docker-run-action@v3
  with:
    run: docker run node:latest npm test  # ❌ Unpredictable!
```

**AFTER (secure - pinned version):**
```yaml
- name: Run tests in container
  uses: addnab/docker-run-action@v3
  with:
    run: |
      # ✅ Pinned to specific major version
      docker run node:20 npm test

# Most secure: Pin to digest
      docker run node@sha256:c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7e8f9b0c1d2e3f4a5b6c7d8e9 npm test
```


## 🛠️ RECOMMENDED FIXES (Reusable Workflows Complete)

### 1. Pin All Action and Workflow References to SHA or Version Tag

**Problem:** Using mutable branch references (@main, @master) or no version pinning creates supply chain vulnerabilities.

**Solution:** Pin all `uses:` references to specific commit SHAs or version tags.

```yaml
# Always pin actions:
- uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
- uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1

# Pin reusable workflows (local):
- uses: ./.github/workflows/shared.yml@c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7

# Pin reusable workflows (cross-repo):
- uses: owner/repo/.github/workflows/external.yml@v1.2.0

# Use @latest only for official GitHub actions you trust and don't care about reproducibility
- uses: docker/setup-buildx-action@latest  # ⚠️ Acceptable risk for rarely-updated tools
```


### 2. Configure Least Privilege Permissions for Reusable Workflows

**Problem:** `permissions: write-all` grants excessive permissions that could be exploited if the workflow is compromised.

**Solution:** Specify only required permissions at workflow or job level.

```yaml
# Workflow-level minimal permissions
permissions:
  contents: read          # Required for checkout
  actions: read           # Required for reusable workflows
  checks: read            # For status reporting (if needed)

jobs:
  reusable-build:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/workflows/shared.yml@c5d4a7e...
```


### 3. Secure Secret Handling in Reusable Workflows

**Problem:** Echoing secrets to stdout exposes them in logs.

**Solution:** Use env blocks and never echo secret values.

```yaml
# Input secrets for reusable workflows:
on:
  workflow_call:
    secrets:
      API_KEY:
        required: true
      DEPLOY_TOKEN:
        required: true

jobs:
  build:
    steps:
      # ✅ Use env block - secret not echoed
      - name: Validate secrets present
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          if [ -z "$API_KEY" ]; then
            echo "ERROR: API_KEY secret is required but missing"
            exit 1
          fi

      # ✅ Use GitHub's built-in validation
      - name: Check required inputs
        uses: actions/github-script@v7
        with:
          script: |
            if (!context.secrets || !context.secrets.API_KEY) {
              throw new Error('Required secret API_KEY is missing');
            }
```


## ✅ ACTION ITEMS (Prioritized by Urgency)

### 🔴 IMMEDIATE (< 1 hour response)

1. [🔴 REUSABLE_WORKFLOW_UNPINNED]
   Location: reusable-workflow.yml (build step 1 - local reference)
   Fix: Pin to commit SHA or version tag

2. [🔴 REUSABLE_WORKFLOW_UNPINNED]
   Location: reusable-workflow.yml (build step 4 - cross-repo reference)
   Fix: Use version tag instead of @main branch

3. [🔴 SECRETS_IN_RUN_COMMAND]
   Location: reusable-workflow.yml (build step 5)
   Fix: Remove echo statements for secrets; use env blocks


### 🟡 SOON (< 24 hours response)

1. [🟡 UNPINNED_BRANCH_REFERENCE]
   Location: reusable-workflow.yml (build step 2 - checkout action)
   Fix: Pin actions/checkout to specific SHA or version tag

2. [🟡 UNPINNED_BRANCH_REFERENCE]
   Location: reusable-workflow.yml (build step 7 - cache action)
   Fix: Use @v4 instead of @master branch reference

3. [🟡 DOCKER_IMAGE_UNPINNED]
   Location: reusable-workflow.yml (build step 6)
   Fix: Pin Docker image to specific version tag


### 🔵 THIS SPRINT (< 1 week response)

1. [🔵 NO_MATRIX_STRATEGY]
   Location: reusable-build job
   Fix: Add matrix strategy for parallel test execution across Node versions and OS platforms


================================================================================
📌 For more details on reusable workflow security, see the SKILL.md documentation.
   Total findings: 11 | Risk level: 🔴 HIGH RISK - Critical vulnerabilities require immediate attention

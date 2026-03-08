# Test Invocation 6: "Review GCP OIDC configuration"

This invocation focuses on **Google Cloud Platform OIDC federation** including workload identity provider configuration, service account authentication, and comparing long-lived vs OIDC credentials.

```bash
$ python run_tests.py --focus gcp-oidc
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report - GCP OIDC Focus
   Workflows Analyzed: gcp-oidc.yml
   Generated: 2026-03-07 15:50:00
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 3 (requires immediate attention)
├─ 🟡 HIGH: 3 (should be addressed soon)
├─ 🔵 MEDIUM: 2 (plan to fix this sprint)
└─ 🟢 LOW: 0 (address when convenient)

**Overall Risk Assessment:** 🔴 HIGH RISK - Critical OIDC configuration issues and long-lived credentials require immediate attention


## 🔍 DETAILED FINDINGS

| Severity | Issue Type | Location | Description |
|----------|------------|----------|-------------|
| 🔴 CRITICAL | `WRITE_ALL_PERMISSIONS` | gcp-oidc.yml (root level) | Workflow has write-all permissions violating least privilege principle |
| 🔴 CRITICAL | `LONG_LIVED_GCP_CREDENTIALS` | deploy-gcp step 1 | Using long-lived service account JSON instead of OIDC federation |
| 🔴 CRITICAL | `SECRETS_IN_RUN_COMMAND` | deploy-gcp step 5 | GCP private key exposed in echo command |
| 🟡 HIGH | `OIDC_CONFIGURED_INCOMPLETELY` | deploy-gcp step 2 | google-github-actions/auth@v2 missing required parameters |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | deploy-gcp step 3 | Action uses only major version: google-github-actions/deploy-cloudrun@v2 |
| 🟡 HIGH | `ACTION_UNPINNED_LATEST` | deploy-gcp step 4 | Using @latest for setup-gcloud action - mutable reference |
| 🔵 MEDIUM | `OIDC_NO_TRUST_CONFIGURED` | deploy-gcp job | id-token: write permission set but OIDC trust not configured in GCP IAM |
| 🔵 MEDIUM | `NO_DEPLOYMENT_AUDIT` | deploy-gcp job | No deployment tracking or audit logging enabled |


## ☁️ GCP OIDC CONFIGURATION ANALYSIS

### Current OIDC Configuration Status

| Step | Action Used | OIDC Configured | Required Params Missing | Security Level | Recommendation |
|------|-------------|-----------------|------------------------|---------------|----------------|
| Authenticate with long-lived | N/A (run command) | ❌ No | N/A | 🔴 CRITICAL | Migrate to google-github-actions/auth@v2 with OIDC |
| Configure GCP via OIDC | google-github-actions/auth@v2 | ⚠️ Partial | workload_identity_provider, service_account | 🟡 HIGH | Add missing required parameters |
| Setup gcloud CLI | google-github-actions/setup-gcloud@latest | ❌ No (using @latest) | N/A | 🟡 HIGH | Pin to specific version tag |

### OIDC vs Long-Lived Credentials Comparison

| Aspect | Long-Lived Service Account JSON | OIDC Federation |
|--------|--------------------------------|-----------------|
| **Security** | 🔴 CRITICAL - Static secrets in GitHub Secrets | ✅ SECURE - Temporary credentials via JWT |
| **Rotation** | 🔴 Manual rotation required (every 90 days) | ✅ Automatic - No rotation needed |
| **Exposure Risk** | 🔴 High - Secrets in logs if leaked | ✅ Low - Short-lived tokens |
| **Access Control** | 🔴 Broad permissions until rotated | ✅ Fine-grained per-workflow IAM |
| **Audit Trail** | ⚠️ Hard to track usage | ✅ JWT claims provide detailed audit trail |
| **Setup Complexity** | 🟢 Simple - upload JSON to secrets | 🔵 Moderate - requires GCP IAM setup |

### Best Practice: GCP OIDC Federation Setup

```yaml
# ✅ SECURE - Complete OIDC configuration required parameters

permissions:
  contents: read
  id-token: write          # Required for OIDC authentication

env:
  PROJECT_ID: my-gcp-project
  REGION: us-central1

jobs:
  deploy-gcp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ✅ Complete OIDC configuration with all required parameters
      - name: Authenticate to GCP via OIDC
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
          service_account: my-service-account@my-gcp-project.iam.gserviceaccount.com
          token_format: access_token

      - name: Activate service account for gcloud CLI
        uses: google-github-actions/setup-gcloud@v4
        with:
          use_default_credentials: true

      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: my-service
          region: ${{ env.REGION }}
```


## 🔐 DETAILED FINDINGS WITH FIXES (GCP OIDC Focus)

### 🔴 CRITICAL: LONG_LIVED_GCP_CREDENTIALS

**Location:** gcp-oidc.yml - deploy-gcp step 1

**Description:** Using long-lived GCP service account JSON credentials stored in GitHub Secrets instead of OIDC federation. This creates significant security risks including credential leakage, manual rotation requirements, and inability to implement fine-grained access control.

**Impact:**
- Service account keys can be leaked in logs or repositories
- Manual key rotation required every 90 days (often forgotten)
- Broad permissions granted until key is rotated
- No automatic credential expiration increases blast radius of compromise

**Recommendation:** Migrate to OIDC federation using google-github-actions/auth@v2 with workload identity provider.

**BEFORE (insecure - long-lived credentials):**
```yaml
env:
  GCP_SA_KEY: ${{ secrets.GCP_SERVICE_ACCOUNT_JSON }}

jobs:
  deploy-gcp:
    runs-on: ubuntu-latest
    steps:
      # ❌ Using long-lived service account JSON!
      - name: Authenticate with long-lived credentials
        run: |
          echo ${{ secrets.GCP_SERVICE_ACCOUNT_JSON }} | \
            jq -r '.client_email' > /tmp/client_email.txt
          echo ${{ secrets.GCP_PRIVATE_KEY }} > /tmp/private_key.json

          gcloud auth activate-service-account \
            --key-file=/tmp/private_key.json
```

**AFTER (secure - OIDC federation):**
```yaml
permissions:
  contents: read
  id-token: write          # Required for OIDC authentication

jobs:
  deploy-gcp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ✅ OIDC federation - no secrets needed!
      - name: Authenticate to GCP via OIDC
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
          service_account: my-service-account@my-gcp-project.iam.gserviceaccount.com

      # ✅ Activate credentials for gcloud CLI
      - name: Setup gcloud with default credentials
        uses: google-github-actions/setup-gcloud@v4
        with:
          use_default_credentials: true
```


### 🔴 CRITICAL: SECRETS_IN_RUN_COMMAND

**Location:** gcp-oidc.yml - deploy-gcp step 5

**Description:** GCP private key and service account details exposed in echo command. This exposes sensitive credentials directly in GitHub Actions logs where they can be viewed by anyone with repository access.

**Impact:**
- Private keys immediately compromised when workflow runs
- Keys must be rotated as if leaked (emergency process)
- Logs may be indexed by external systems permanently
- Violates security best practices and compliance requirements

**Recommendation:** Remove all echo statements exposing secrets; use proper secret handling.

**BEFORE (insecure - echoing secrets):**
```yaml
# ❌ EXPOSES PRIVATE KEY IN LOGS!
- name: Verify deployment
  run: |
    echo "Deployed to ${{ env.PROJECT_ID }}"
    echo "Service account key: $GCP_PRIVATE_KEY"  # 🚨 SECURITY BREACH!

# Also exposes secrets in error messages
- name: Debug deployment
  run: |
    if [ -z "$GCP_PRIVATE_KEY" ]; then
      echo "Error using key: $GCP_PRIVATE_KEY is empty"  # STILL EXPOSES!
```

**AFTER (secure - no secret exposure):**
```yaml
# ✅ Safe - no secrets in output
- name: Verify deployment
  run: |
    echo "Deployed to project: ${{ env.PROJECT_ID }}"
    gcloud config get-value project

# ✅ Safe - generic error message without exposing value
- name: Validate required environment
  run: |
    if [ -z "${{ env.PROJECT_ID }}" ]; then
      echo "ERROR: PROJECT_ID environment variable is required"
      exit 1
    fi
```


### 🟡 HIGH: OIDC_CONFIGURED_INCOMPLETELY

**Location:** gcp-oidc.yml - deploy-gcp step 2

**Description:** The google-github-actions/auth@v2 action is configured but missing critical required parameters. Workload identity provider and service account must be specified for OIDC authentication to function properly.

**Impact:**
- Workflow fails at runtime with unclear error messages
- Falls back to less secure authentication methods if available
- Creates confusion about whether OIDC is working correctly
- May silently use default credentials instead of intended configuration

**Recommendation:** Add missing required parameters: workload_identity_provider and service_account.

**BEFORE (incomplete - missing required params):**
```yaml
# ⚠️ Missing workload_identity_provider and service_account!
- name: Configure GCP via OIDC (incomplete)
  uses: google-github-actions/auth@v2
  with:
    project_id: ${{ env.PROJECT_ID }}
    # ❌ Missing: workload_identity_provider
    # ❌ Missing: service_account
```

**AFTER (complete - all required parameters):**
```yaml
# ✅ Complete OIDC configuration
- name: Configure GCP via OIDC
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
    service_account: my-service-account@my-gcp-project.iam.gserviceaccount.com
    token_format: access_token          # Optional but recommended

# Token format options:
# - id_token (default) - JWT ID token for API authentication
# - access_token - OAuth 2.0 access token for gcloud CLI
# - refresh_token - Refresh token for long-running scripts
```


### 🟡 HIGH: ACTION_UNPINNED_LATEST

**Location:** gcp-oidc.yml - deploy-gcp step 4

**Description:** Using `google-github-actions/setup-gcloud@latest` which resolves to the most recent version. This can cause unexpected behavior when action updates are released, potentially breaking CI/CD pipelines.

**Impact:**
- Action updates may introduce breaking changes without warning
- Builds become unpredictable and hard to reproduce
- Security patches applied automatically without testing
- Difficult to debug issues caused by action version changes

**Recommendation:** Pin to specific version tag (e.g., @v4) or commit SHA for reproducibility.

**BEFORE (insecure - using @latest):**
```yaml
# ❌ Mutable reference - resolves to newest version
- name: Setup gcloud CLI
  uses: google-github-actions/setup-gcloud@latest
```

**AFTER (secure - pinned version):**
```yaml
# ✅ Pinned to specific major version
- name: Setup gcloud CLI
  uses: google-github-actions/setup-gcloud@v4

# Most secure - pinned to exact version with SHA
- name: Setup gcloud CLI
  uses: google-github-actions/setup-gcloud@a1b2c3d4e5f6...  # v4.1.0 SHA
```


## 🏗️ GCP OIDC TRUST CONFIGURATION

### Required IAM Configuration in GCP

Before using OIDC authentication, you must configure trust relationship in Google Cloud IAM:

**Step 1: Create Workload Identity Pool**
```bash
gcloud iam workload-identity-pools create \
    my-pool \
    --location=global \
    --project=my-gcp-project \
    --display-name="GitHub Actions Pool" \
    --attribute.github.repository=jos33/Skill-Cauldron \
    --attribute.github.organization_id=123456789
```

**Step 2: Create Workload Identity Provider**
```bash
gcloud iam workload-identity-pools providers create-oidc \
    my-provider \
    --location=global \
    --workload-identity-pool=my-pool \
    --project=my-gcp-project \
    --display-name="GitHub Actions Provider" \
    --issuer-uri=https://token.actions.githubusercontent.com
```

**Step 3: Grant IAM Role to Service Account**
```bash
gcloud iam service-accounts add-iam-policy-binding \
    my-service-account@my-gcp-project.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:my-gcp-project.svc.id.goog[namespace/pod]" \
    --condition-expression="attributes.github.repository == 'jos33/Skill-Cauldron'"
```

**Step 4: Enable Workload Identity Federation API**
```bash
gcloud services enable iamcredentials.googleapis.com
```


## 🛠️ RECOMMENDED FIXES (GCP OIDC Complete)

### 1. Migrate from Long-Lived to OIDC Credentials

**Problem:** Service account JSON keys stored in GitHub Secrets create ongoing security risks and manual rotation burden.

**Solution:** Configure workload identity federation for automatic credential exchange via OIDC.

```yaml
# Before: Long-lived credentials (INSECURE)
env:
  GCP_SA_KEY: ${{ secrets.GCP_SERVICE_ACCOUNT_JSON }}

steps:
  - run: |
      echo "$GCP_SA_KEY" | gcloud auth activate-service-account

# After: OIDC federation (SECURE)
permissions:
  id-token: write
  contents: read

steps:
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
      service_account: my-service-account@my-project.iam.gserviceaccount.com

  - uses: google-github-actions/setup-gcloud@v4
    with:
      use_default_credentials: true
```


### 2. Configure Proper IAM Trust Policy

**Problem:** OIDC authentication fails because trust relationship not configured in GCP IAM.

**Solution:** Create workload identity pool, provider, and grant appropriate roles to service account.

```bash
# See detailed configuration above in "GCP OIDC TRUST CONFIGURATION" section
# Key steps:
# 1. Create workload-identity-pool
# 2. Create OIDC provider with GitHub issuer URL
# 3. Add IAM policy binding with attribute-based conditions
# 4. Enable required APIs
```


### 3. Pin All Action Versions

**Problem:** Using @latest or major versions only creates unpredictable CI/CD behavior.

**Solution:** Pin all actions to specific version tags or commit SHAs.

```yaml
permissions:
  contents: read
  id-token: write

jobs:
  deploy-gcp:
    steps:
      - uses: actions/checkout@v4              # ✅ Pinned
      - uses: google-github-actions/auth@v2   # ✅ Pinned (use v2.x.y for exact)
      - uses: google-github-actions/setup-gcloud@v4  # ✅ Pinned
      - uses: google-github-actions/deploy-cloudrun@v2  # ✅ Pinned
```


## ✅ ACTION ITEMS (Prioritized by Urgency)

### 🔴 IMMEDIATE (< 1 hour response)

1. [🔴 LONG_LIVED_GCP_CREDENTIALS]
   Location: gcp-oidc.yml (deploy-gcp step 1)
   Fix: Migrate from service account JSON to OIDC federation

2. [🔴 SECRETS_IN_RUN_COMMAND]
   Location: gcp-oidc.yml (deploy-gcp step 5)
   Fix: Remove all echo statements exposing GCP credentials


### 🟡 SOON (< 24 hours response)

1. [🟡 OIDC_CONFIGURED_INCOMPLETELY]
   Location: gcp-oidc.yml (deploy-gcp step 2)
   Fix: Add workload_identity_provider and service_account parameters

2. [🟡 MAJOR_VERSION_ONLY]
   Location: gcp-oidc.yml (deploy-gcp step 3)
   Fix: Pin google-github-actions/deploy-cloudrun to specific version

3. [🟡 ACTION_UNPINNED_LATEST]
   Location: gcp-oidc.yml (deploy-gcp step 4)
   Fix: Pin setup-gcloud to @v4 instead of @latest


### 🔵 THIS SPRINT (< 1 week response)

1. [🔵 OIDC_NO_TRUST_CONFIGURED]
   Location: gcp-oidc.yml (deploy-gcp job)
   Fix: Configure GCP IAM trust policy for OIDC federation
   - Create workload identity pool and provider
   - Grant iam.workloadIdentityUser role to service account


================================================================================
📌 For more details on GCP OIDC configuration, see the SKILL.md documentation.
   Total findings: 8 | Risk level: 🔴 HIGH RISK - Critical OIDC configuration issues require immediate attention

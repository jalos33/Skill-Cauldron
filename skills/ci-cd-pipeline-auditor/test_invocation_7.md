# Test Invocation 7: "Audit Azure managed identity setup"

This invocation focuses on **Azure OIDC federation** including managed identity configuration, federated credentials, and comparing service principal secrets vs OIDC authentication.

```bash
$ python run_tests.py --focus azure-oidc
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report - Azure OIDC Focus
   Workflows Analyzed: azure-oidc.yml
   Generated: 2026-03-07 15:52:00
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 3 (requires immediate attention)
├─ 🟡 HIGH: 4 (should be addressed soon)
├─ 🔵 MEDIUM: 1 (plan to fix this sprint)
└─ 🟢 LOW: 0 (address when convenient)

**Overall Risk Assessment:** 🔴 HIGH RISK - Critical Azure authentication issues and long-lived credentials require immediate attention


## 🔍 DETAILED FINDINGS

| Severity | Issue Type | Location | Description |
|----------|------------|----------|-------------|
| 🔴 CRITICAL | `WRITE_ALL_PERMISSIONS` | azure-oidc.yml (root level) | Workflow has write-all permissions violating least privilege principle |
| 🔴 CRITICAL | `LONG_LIVED_AZURE_CREDENTIALS` | deploy-azure step 1 | Using service principal secrets instead of OIDC federation |
| 🔴 CRITICAL | `SECRETS_IN_RUN_COMMAND` | deploy-azure step 5 | Subscription ID exposed in echo command |
| 🟡 HIGH | `AZURE_OIDC_NOT_ENABLED` | deploy-azure step 2 | Azure login missing use_oidc flag for federated credentials |
| 🟡 HIGH | `ACTION_UNPINNED_LATEST` | deploy-azure step 4 | Using @latest for webapps-deploy - mutable reference |
| 🟡 HIGH | `MAJOR_VERSION_ONLY` | deploy-azure step 3 | ARM deploy action uses only major version: azure/arm-deploy@v2 |
| 🟡 HIGH | `PUBLISH_PROFILE_SECRET` | deploy-azure step 4 | Using deprecated publish-profile authentication method |
| 🔵 MEDIUM | `SERVICE_PRINCIPAL_IN_USE` | deploy-azure job | Service principal used across multiple steps instead of managed identity |


## ☁️ AZURE OIDC CONFIGURATION ANALYSIS

### Current Authentication Configuration Status

| Step | Action Used | Auth Method | OIDC Enabled | Security Level | Recommendation |
|------|-------------|-------------|--------------|---------------|----------------|
| Login to Azure | azure/login@v1 | Service Principal Secrets | ❌ No | 🔴 CRITICAL | Migrate to OIDC with use_oidc: true |
| Managed identity login | azure/login@v1 | Managed Identity | ⚠️ Partial | 🟡 HIGH | Add use_oidc: true for federated credentials |
| Deploy ARM template | azure/arm-deploy@v2 | Service Principal | ❌ No | 🔴 CRITICAL | Use OIDC or managed identity |
| Deploy Web App | azure/webapps-deploy@latest | Publish Profile | ❌ No | 🟡 HIGH | Pin version; use managed identity |

### Azure Authentication Methods Comparison

| Method | Security Level | Secret Storage | Rotation | Fine-Grained Control | Recommendation |
|--------|---------------|----------------|----------|---------------------|----------------|
| Service Principal (Client ID/Key) | 🔴 CRITICAL | GitHub Secrets (long-lived keys) | Manual every 12-24 months | ⚠️ Moderate | ❌ Avoid - use OIDC instead |
| Service Principal (Client ID/Secret) | 🔴 HIGH | GitHub Secrets (secrets expire in 24 months) | Required rotation | ⚠️ Moderate | ⚠️ Temporary solution only |
| Publish Profile | 🔴 CRITICAL | GitHub Secrets (contains full credentials) | Manual revocation needed | ❌ None | ❌ Avoid - legacy method |
| **Azure Login with OIDC** | ✅ SECURE | No secrets stored | Automatic via JWT | ✅ Yes per workflow | ✅ Recommended |
| **Managed Identity + Federated Credentials** | ✅ SECURE | Azure-managed identity | Automatic | ✅ Yes per resource | ✅ Best for Azure-native workloads |

### Best Practice: Azure OIDC Configuration

```yaml
# ✅ SECURE - Complete OIDC configuration with managed identity

permissions:
  contents: read
  id-token: write          # Required for OIDC authentication

env:
  AZURE_RESOURCE_GROUP: my-rg
  AZURE_LOCATION: eastus

jobs:
  deploy-azure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ✅ Azure login with managed identity via OIDC
      - name: Login to Azure with Managed Identity
        uses: azure/login@v1
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}           # App registration object ID
          tenant-id: ${{ vars.AZURE_TENANT_ID }}            # Directory (tenant) ID
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}  # Subscription GUID
          use_oidc: true                                    # Enable OIDC federation

      - name: Deploy Azure Resource Manager template
        uses: azure/arm-deploy@v1
        with:
          resource-group-name: ${{ env.AZURE_RESOURCE_GROUP }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
          template: ./arm-template.json
          parameters: location=${{ env.AZURE_LOCATION }}

      - name: Deploy Web App
        uses: azure/webapps-deploy@v2
        with:
          app-name: my-webapp
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}  # Or use managed identity
```


## 🔐 DETAILED FINDINGS WITH FIXES (Azure OIDC Focus)

### 🔴 CRITICAL: LONG_LIVED_AZURE_CREDENTIALS

**Location:** azure-oidc.yml - deploy-azure step 1

**Description:** Using Azure service principal credentials (client ID, tenant ID, subscription ID secrets) stored in GitHub Secrets instead of OIDC federation. This creates ongoing security risks including credential leakage, manual rotation requirements, and excessive permissions blast radius.

**Impact:**
- Service principal secrets can be leaked in logs or repositories
- Client secrets expire after 12-24 months requiring manual rotation
- Keys must be rotated immediately if compromised (emergency process)
- Broader permissions granted than necessary for workflow tasks
- No automatic credential expiration increases attack window

**Recommendation:** Migrate to OIDC federation using azure/login@v1 with use_oidc: true.

**BEFORE (insecure - service principal secrets):**
```yaml
# ❌ Using long-lived service principal credentials!
permissions:
  contents: read

jobs:
  deploy-azure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Azure with long-lived credentials
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}       # 🔴 Long-lived secret
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}        # 🔴 Stored in GitHub Secrets
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}  # 🔴 Requires rotation

      - name: Deploy resources
        uses: azure/arm-deploy@v2
        with:
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}  # Repeated exposure!
```

**AFTER (secure - OIDC federation):**
```yaml
# ✅ Secure - OIDC federation via managed identity
permissions:
  contents: read
  id-token: write          # Required for OIDC authentication

jobs:
  deploy-azure:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ✅ Azure login with federated credentials (no secrets!)
      - name: Login to Azure with Managed Identity via OIDC
        uses: azure/login@v1
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}           # Can be variable, not secret!
          tenant-id: $${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}  # Can be variable!
          use_oidc: true                                    # Enable OIDC federation

      - name: Deploy resources (uses authenticated session)
        uses: azure/arm-deploy@v1
        with:
          resource-group-name: my-rg
          template: ./arm-template.json
```


### 🔴 CRITICAL: SECRETS_IN_RUN_COMMAND

**Location:** azure-oidc.yml - deploy-azure step 5

**Description:** Azure subscription ID exposed in echo command. While subscription IDs are less sensitive than secrets, exposing them in logs is a security best practice violation and can aid attackers in targeting specific subscriptions.

**Impact:**
- Subscription information exposed in workflow logs
- Can be used by attackers to enumerate Azure resources
- Violates principle of not logging any Azure identifiers
- May violate compliance requirements for log sanitization

**Recommendation:** Remove echo statements exposing Azure identifiers; use generic deployment confirmation messages.

**BEFORE (insecure - exposing subscription):**
```yaml
# ⚠️ Exposing subscription ID in logs
- name: Verify deployment
  run: |
    echo "Deployed to subscription: $AZURE_SUBSCRIPTION_ID"  # 🚨 In logs!
    az group show --name $AZURE_RESOURCE_GROUP

# Even worse - exposing secret values directly
- name: Debug Azure connection
  env:
    SUB_CREDENTIALS: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
  run: |
    if [ -z "$SUB_CREDENTIALS" ]; then
      echo "Error: Subscription ID empty, credentials: $SUB_CREDENTIALS"  # EXPOSED!
```

**AFTER (secure - no identifiers in logs):**
```yaml
# ✅ Safe - generic confirmation without exposing identifiers
- name: Verify deployment
  run: |
    echo "Deployment completed successfully to resource group: $AZURE_RESOURCE_GROUP"
    az group show --name "$AZURE_RESOURCE_GROUP" --query "id" -o tsv

# If validation needed, use non-exposing pattern
- name: Validate Azure connection
  env:
    AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
  run: |
    if [ -z "$AZURE_SUBSCRIPTION_ID" ]; then
      echo "ERROR: AZURE_SUBSCRIPTION_ID is required but not configured"
      exit 1
    fi

# Or better - rely on azure/login action's built-in validation
- name: Verify Azure connection
  run: |
    az account show --query "id" -o tsv || echo "Not connected to Azure"
```


### 🟡 HIGH: AZURE_OIDC_NOT_ENABLED

**Location:** azure-oidc.yml - deploy-azure step 2

**Description:** The azure/login@v1 action is configured with client ID and tenant ID but missing the `use_oidc: true` flag required to enable federated credential authentication. Without this flag, the action attempts to use traditional service principal authentication which requires secrets.

**Impact:**
- Workflow may fail if secrets not properly configured
- Falls back to less secure authentication methods
- Creates confusion about whether OIDC is actually being used
- May silently use cached credentials from previous runs

**Recommendation:** Add `use_oidc: true` parameter to enable federated credential authentication.

**BEFORE (incomplete - missing OIDC flag):**
```yaml
# ⚠️ Missing use_oidc: true!
- name: Login with managed identity (incomplete)
  uses: azure/login@v1
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    # ❌ Missing: use_oidc: true

# This will try service principal auth, not OIDC!
```

**AFTER (complete - OIDC enabled):**
```yaml
# ✅ Complete - OIDC federation enabled
- name: Login to Azure with Managed Identity via OIDC
  uses: azure/login@v1
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}           # App registration ID
    tenant-id: ${{ vars.AZURE_TENANT_ID }}            # Tenant/Directory ID
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}  # Optional for specific subscription
    use_oidc: true                                    # ✅ Enable OIDC federation

# With use_oidc: true, Azure CLI will automatically obtain temporary credentials via JWT!
```


### 🟡 HIGH: ACTION_UNPINNED_LATEST

**Location:** azure-oidc.yml - deploy-azure step 4

**Description:** Using `azure/webapps-deploy@latest` which resolves to the most recent version. This can cause unexpected behavior when action updates are released, potentially breaking CI/CD pipelines or introducing security issues.

**Impact:**
- Action updates may introduce breaking changes without warning
- Builds become unpredictable and hard to reproduce
- Security patches applied automatically without testing
- Difficult to debug issues caused by action version changes

**Recommendation:** Pin to specific version tag (e.g., @v2) for reproducibility.

**BEFORE (insecure - using @latest):**
```yaml
# ❌ Mutable reference - resolves to newest version
- name: Deploy Web App
  uses: azure/webapps-deploy@latest
  with:
    app-name: my-webapp
    publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
```

**AFTER (secure - pinned version):**
```yaml
# ✅ Pinned to specific major version
- name: Deploy Web App
  uses: azure/webapps-deploy@v2
  with:
    app-name: my-webapp

# Or use managed identity instead of publish-profile
    # connection-type: kubernetes
    # app-name: ${{ vars.WEBAPP_NAME }}
```


## 🏗️ AZURE OIDC TRUST CONFIGURATION

### Required Configuration in Azure Portal

Before using OIDC authentication, you must configure federated credentials in Azure AD:

**Step 1: Create Managed Identity (if not exists)**
```bash
az identity create \
    --name github-actions-identity \
    --resource-group my-rg \
    --location eastus
```

**Step 2: Get Identity Client ID**
```bash
CLIENT_ID=$(az identity show \
    --name github-actions-identity \
    --resource-group my-rg \
    --query clientId -o tsv)

echo $CLIENT_ID  # Store this as AZURE_CLIENT_ID variable
```

**Step 3: Assign RBAC Role to Identity**
```bash
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

az role assignment create \
    --assignee $CLIENT_ID \
    --role "Contributor" \
    --scope /subscriptions/$SUBSCRIPTION_ID/resourceGroups/my-rg
```

**Step 4: Create Federated Credential**
```bash
# Get GitHub organization and repo info
ORG_NAME="jos33"
REPO_NAME="Skill-Cauldron"

az identity federated-credential create \
    --name github-actions-federated-credential \
    --identity-name github-actions-identity \
    --resource-group my-rg \
    --issuer "https://token.actions.githubusercontent.com" \
    --subject "repo:${ORG_NAME}/${REPO_NAME}:ref:refs/heads/main" \
    --description "GitHub Actions for main branch" \
    --audiences "api://AzureADTokenExchange"
```

**Step 5: Configure GitHub Variables**
```bash
# Store these as repo/org variables (not secrets!):
AZURE_CLIENT_ID=<the-client-id-from-step-2>
AZURE_TENANT_ID=<your-tenant-id>
AZURE_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
```


## 🛠️ RECOMMENDED FIXES (Azure OIDC Complete)

### 1. Migrate from Service Principal to OIDC Authentication

**Problem:** Using service principal secrets stored in GitHub Secrets creates ongoing security risks and manual rotation burden.

**Solution:** Configure federated credentials for automatic credential exchange via OIDC.

```yaml
# Before: Service principal with secrets (INSECURE)
steps:
  - uses: azure/login@v1
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}     # 🔴 Secret!
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}     # 🔴 Secret!
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}  # 🔴 Secret!

# After: OIDC federation (SECURE)
permissions:
  id-token: write
  contents: read

steps:
  - uses: azure/login@v1
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}        # Can be variable!
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      use_oidc: true                                # ✅ Enable OIDC

# No secrets needed - Azure gets temporary credentials via JWT!
```


### 2. Configure Federated Credentials in Azure AD

**Problem:** OIDC authentication fails because federated credential not configured in Azure AD.

**Solution:** Create managed identity, assign RBAC role, and create federated credential with proper subject claims.

```bash
# See detailed configuration above in "AZURE OIDC TRUST CONFIGURATION" section
# Key steps:
# 1. Create managed identity (az identity create)
# 2. Assign Contributor role to identity for target resource
# 3. Create federated credential with GitHub issuer and subject claim
# 4. Store client/tenant IDs as variables, not secrets

# Federated credential subject format:
# repo:{organization}/{repository}:ref:refs/heads/{branch}
# Example: repo:jos33/Skill-Cauldron:ref:refs/heads/main
```


### 3. Pin All Action Versions and Use Modern Authentication

**Problem:** Using @latest for actions and deprecated publish-profile authentication creates security and reliability issues.

**Solution:** Pin all Azure actions to specific versions and prefer managed identity over publish profiles.

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  deploy-azure:
    steps:
      - uses: azure/login@v1                      # ✅ Pinned + OIDC
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          use_oidc: true

      - uses: azure/arm-deploy@v1                 # ✅ Pinned (use v1, not v2)
        with:
          resource-group-name: my-rg
          template: ./arm-template.json

      - uses: azure/webapps-deploy@v2             # ✅ Pinned
        with:
          app-name: my-webapp
          # Prefer managed identity over publish-profile when possible
```


## ✅ ACTION ITEMS (Prioritized by Urgency)

### 🔴 IMMEDIATE (< 1 hour response)

1. [🔴 LONG_LIVED_AZURE_CREDENTIALS]
   Location: azure-oidc.yml (deploy-azure step 1)
   Fix: Migrate from service principal secrets to OIDC federation with use_oidc: true

2. [🔴 SECRETS_IN_RUN_COMMAND]
   Location: azure-oidc.yml (deploy-azure step 5)
   Fix: Remove all echo statements exposing Azure identifiers


### 🟡 SOON (< 24 hours response)

1. [🟡 AZURE_OIDC_NOT_ENABLED]
   Location: azure-oidc.yml (deploy-azure step 2)
   Fix: Add use_oidc: true to enable federated credential authentication

2. [🟡 ACTION_UNPINNED_LATEST]
   Location: azure-oidc.yml (deploy-azure step 4)
   Fix: Pin azure/webapps-deploy to @v2 instead of @latest

3. [🟡 MAJOR_VERSION_ONLY]
   Location: azure-oidc.yml (deploy-azure step 3)
   Fix: Use azure/arm-deploy@v1 (specific version, not v2)

4. [🟡 PUBLISH_PROFILE_SECRET]
   Location: azure-oidc.yml (deploy-azure step 4)
   Fix: Migrate to managed identity deployment; avoid publish-profile secrets


### 🔵 THIS SPRINT (< 1 week response)

1. [🔵 SERVICE_PRINCIPAL_IN_USE]
   Location: azure-oidc.yml (deploy-azure job)
   Fix: Configure federated credentials in Azure AD for all workflows using OIDC
   - Create managed identity
   - Assign appropriate RBAC role
   - Create federated credential with correct subject claim


================================================================================
📌 For more details on Azure OIDC configuration, see the SKILL.md documentation.
   Total findings: 8 | Risk level: 🔴 HIGH RISK - Critical Azure authentication issues require immediate attention

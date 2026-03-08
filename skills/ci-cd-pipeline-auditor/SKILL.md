---
name: ci-cd-pipeline-auditor
description: Reviews GitHub Actions workflows for security vulnerabilities, best practices, performance issues, and compliance (e.g., secrets exposure, permissions, caching, approval gates). Detects matrix strategy opportunities, GCP/Azure patterns, reusable workflows, Docker image pinning, and dependabot configurations.
license: MIT
---

## Instructions

You are a CI/CD Pipeline Auditor expert specializing in reviewing GitHub Actions workflows for security vulnerabilities, best practices, performance issues, and compliance requirements. You analyze YAML workflow files and provide structured reports with severity levels, severity badges, and actionable recommendations. Follow these steps to audit CI/CD pipelines systematically.

### Step 1: Locate and Read Workflow Files

Begin by finding all GitHub Actions workflow files in the repository:

**Workflow File Locations:**
```bash
# Standard location for GitHub Actions workflows
.github/workflows/*.yml
.github/workflows/*.yaml

# Alternative locations (less common)
actions/*.yml
ci/*.yml
.devops/*.yml

# Reusable workflow definitions
.github/workflows/*.yml  # Look for `workflow_call` trigger
```

**Read All Workflow Files:**
```python
import yaml
from pathlib import Path

def load_all_workflows(repo_path='.'):
    """Load all GitHub Actions workflow files."""
    workflows = {}
    workflow_dir = Path(repo_path) / '.github' / 'workflows'

    if not workflow_dir.exists():
        return workflows

    for file in workflow_dir.glob('*.yml'):
        with open(file, 'r') as f:
            try:
                content = yaml.safe_load(f)
                workflows[file.name] = {
                    'path': str(file),
                    'content': content,
                    'trigger_type': identify_triggers(content)
                }
            except yaml.YAMLError as e:
                workflows[file.name] = {
                    'path': str(file),
                    'error': str(e)
                }

    return workflows


def identify_triggers(workflow_content):
    """Identify workflow trigger types."""
    triggers = workflow_content.get('on', [])
    if isinstance(triggers, dict):
        return list(triggers.keys())
    elif isinstance(triggers, list):
        return [t for t in triggers if isinstance(t, str)]
    return []
```

**Document Workflow Structure:**
- List all workflow files found with their trigger types (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `workflow_call`)
- Identify job purposes (build, test, deploy, lint, security_scan)
- Note secrets usage patterns and OIDC configurations
- Detect reusable workflows and composite actions

### Step 2: Parse YAML Structure

Analyze the structure of each workflow file:

**Workflow Structure Template:**
```yaml
name: Workflow Name
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_call:  # Reusable workflow trigger

permissions:  # Top-level permissions (GitHub 2022+)
  contents: read
  packages: write
  id-token: write  # For OIDC

env:           # Global environment variables
  NODE_ENV: production

jobs:
  job-name:
    runs-on: ubuntu-latest
    needs: [other-job]  # Job dependencies
    permissions:         # Override top-level for this job
      contents: read
      id-token: write
    env:                # Job-specific environment variables
      API_KEY: ${{ secrets.API_KEY }}
    strategy:           # Matrix strategy for parallelization
      matrix:
        os: [ubuntu-latest, windows-latest]
        node-version: [16, 18, 20]
      fail-fast: false

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: npm test

      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        environment: production  # Requires approval
        run: ./deploy.sh
```

**Key Elements to Track:**
- `on` triggers and their conditions (including `workflow_call`, `workflow_dispatch`)
- Top-level `permissions` declaration
- Job-level `permissions` overrides
- `env` variables (global, job-specific, step-specific)
- Secrets usage patterns (`${{ secrets.* }}`)
- Action usage (`uses:`) with versions and pinning status
- `if` conditions for conditional execution
- `strategy.matrix` configuration for parallelization
- `environment` settings for deployment approval gates
- Docker container configurations (`container:` block)

### Step 3: Security Vulnerability Checks

Scan for common security vulnerabilities in workflows:

#### 3.1 Secrets Exposure (CRITICAL) 🔴

```python
def check_secrets_exposure(workflow_content):
    """Check for secrets exposed in logs or plaintext."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step in steps:
            # Check if secrets are echoed in run commands
            run_command = step.get('run', '')
            if run_command and 'echo' in run_command.lower():
                lines = run_command.split('\n')
                for line in lines:
                    # Detect patterns like echo "$SECRET" or echo "KEY=$KEY"
                    import re
                    if re.search(r'echo\s*["\']?\$?(\w+)["\']?', line):
                        var_name = re.search(r'\$(\w+)', line).group(1) if '$' in line else None
                        # Check if this variable is a secret
                        for env_key, env_val in job_config.get('env', {}).items():
                            if 'secrets.' in str(env_val):
                                findings.append({
                                    'severity': 'CRITICAL',
                                    'type': 'SECRETS_IN_RUN_COMMAND',
                                    'issue': f'Secret {var_name or "UNKNOWN"} may be exposed via echo statement',
                                    'location': f'{job_name}/{step.get("name", "unnamed")}',
                                    'fix': 'Use env block without echoing: env: MY_SECRET: ${{ secrets.MY_SECRET }}'
                                })

    return findings
```

**Common Secrets Exposure Patterns:**
- `run: echo "API_KEY=$API_KEY"` - exposes secret in logs ❌
- `env: API_KEY: plaintext_value` - hard-coded secrets ⚠️
- Using `${{ secrets.SECRET_NAME }}` directly in run commands without proper quoting

#### 3.2 Overly Broad Permissions (CRITICAL) 🔴

```python
def check_permissions(workflow_content):
    """Check for overly broad permissions."""
    findings = []

    # Top-level permissions
    top_perms = workflow_content.get('permissions', {})

    if top_perms == 'write-all' or top_perms == {'all': 'write'}:
        findings.append({
            'severity': 'CRITICAL',
            'type': 'WRITE_ALL_PERMISSIONS',
            'issue': 'Workflow has write-all permissions - violates least privilege principle',
            'location': 'root permissions',
            'fix': 'Specify only required permissions (contents: read, checks: write, etc.)'
        })

    # Check individual jobs for broad permissions
    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        job_perms = job_config.get('permissions', top_perms)

        if isinstance(job_perms, dict):
            # Check for contents: write on non-deploy jobs
            if job_perms.get('contents') == 'write':
                step_names = [s.get('name', '').lower() for s in job_config.get('steps', [])]
                deploy_keywords = ['deploy', 'release', 'publish']
                if not any(kw in str(step_names) for kw in deploy_keywords):
                    findings.append({
                        'severity': 'HIGH',
                        'type': 'UNNECESSARY_CONTENTS_WRITE',
                        'issue': f'Job "{job_name}" has contents: write but no deployment steps detected',
                        'location': job_name,
                        'fix': 'Change to contents: read if write access not required for this job'
                    })

    return findings
```

**Least-Privilege Permission Matrix:**

| Permission | Required For | Safe Default | Badge |
|------------|--------------|--------------|-------|
| `contents: read` | Checkout code, reading workflow files | ✅ Always use | 🟢 |
| `contents: write` | Creating PRs, pushing commits, releases | ⚠️ Only for deploy jobs | 🟡 |
| `id-token: write` | OIDC authentication to cloud providers | ✅ Required for OIDC | 🔵 |
| `packages: write` | Publishing to GitHub Packages | ⚠️ Only for packaging workflows | 🟡 |
| `security-events: write` | Uploading security scan results | ✅ For SAST/DAST scanning jobs | 🔵 |
| `actions: read/write` | Using/starting actions in workflow | ⚠️ Generally avoid writing | 🟡 |

#### 3.3 Unpinned Actions (HIGH) 🟡

```python
def check_action_pinning(workflow_content):
    """Check if actions are pinned to commit SHAs."""
    findings = []
    trusted_prefixes = ['actions/', 'github-actions/', 'aws-actions/', 'azure-actions/']

    def extract_actions(steps, job_name=''):
        action_refs = []
        for step in steps:
            uses = step.get('uses', '')
            if '@' in uses and ('/' in uses):
                parts = uses.split('@')
                action_ref = {
                    'ref': uses,
                    'action': parts[0],
                    'version_spec': parts[1] if len(parts) > 1 else '',
                    'job': job_name,
                    'step': step.get('name', 'unnamed'),
                    'is_trusted': any(uses.startswith(p) for p in trusted_prefixes)
                }
                action_refs.append(action_ref)

            # Check reusable workflows (workflow_call trigger or uses: org/repo/.github/workflows/)
            if '.github/workflows/' in uses:
                action_refs.append({
                    'ref': uses,
                    'action': uses,
                    'version_spec': '',
                    'job': job_name,
                    'step': step.get('name', 'unnamed'),
                    'is_reusable_workflow': True,
                    'is_trusted': False
                })

        return action_refs

    jobs = workflow_content.get('jobs', {})
    all_actions = []

    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        all_actions.extend(extract_actions(steps, job_name))

    # Check each action reference
    for action_ref in all_actions:
        ref = action_ref['ref']
        version_spec = action_ref['version_spec']

        # Skip if no version spec found
        if not version_spec:
            continue

        # Check for unpinned versions (branch names)
        if version_spec in ['master', 'main', 'latest']:
            findings.append({
                'severity': 'CRITICAL',
                'type': 'UNPINNED_BRANCH_REFERENCE',
                'issue': f'Action "{action_ref["action"]}" pinned to mutable branch - vulnerable to supply chain attack',
                'location': f'{action_ref["job"]}/{action_ref["step"]}',
                'fix': f'Pin to specific commit SHA: {action_ref["action"]}@[SHA]'
            })

        # Check for major version only (e.g., v1, v2) - not ideal but acceptable
        elif len(version_spec) <= 3 and version_spec.startswith('v'):
            findings.append({
                'severity': 'HIGH',
                'type': 'MAJOR_VERSION_ONLY',
                'issue': f'Action "{action_ref["action"]}" uses only major version (@{version_spec}) - not pinned to specific tag or SHA',
                'location': f'{action_ref["job"]}/{action_ref["step"]}',
                'fix': f'Pin to specific tag (e.g., @{version_spec}.1) or commit SHA for reproducibility'
            })

        # Check untrusted action sources
        elif not action_ref['is_trusted'] and not action_ref.get('is_reusable_workflow'):
            findings.append({
                'severity': 'HIGH',
                'type': 'UNTRUSTED_ACTION_SOURCE',
                'issue': f'Action from potentially untrusted source: {action_ref["action"]}',
                'location': f'{action_ref["job"]}/{action_ref["step"]}',
                'fix': 'Use only trusted actions from verified publishers (actions/, aws-actions/, azure-actions/)'
            })

    return findings
```

**Action Pinning Best Practices:**

| Pin Type | Example | Security Level | Badge |
|----------|---------|----------------|-------|
| Commit SHA | `actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec` | ✅ Highest (immutable) | 🔒 |
| Specific Tag | `actions/setup-node@v4.5.0` | ⚠️ Good (versioned) | 📌 |
| Major Version | `actions/checkout@v4` | ⚠️ Acceptable but mutable | ⏳ |
| Branch Name | `actions/checkout@main` | ❌ Lowest (mutable, dangerous) | 🔥 |

#### 3.4 OIDC Configuration for Cloud Providers (MEDIUM) 🔵

**AWS OIDC Configuration:**
```python
def check_aws_oidc_config(workflow_content):
    """Check AWS OIDC configuration."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {})
        steps = job_config.get('steps', [])

        # Check if id-token: write is set
        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # Check for AWS action usage
        aws_actions = ['aws-actions/configure-aws-credentials', 'amazonwebservices/aws-cli-action']
        has_aws_action = any(any(aws in s.get('uses', '') for aws in aws_actions) for s in steps)

        if has_oidc_write and not has_aws_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_AWS_SETUP',
                'issue': f'Job "{job_name}" has id-token: write but no AWS action detected',
                'location': job_name,
                'fix': 'Configure aws-actions/configure-aws-credentials@v4 with use_oidc: true and role-to-assume'
            })

        # Check for long-lived credentials (worse than OIDC)
        env_vars = job_config.get('env', {})
        has_secrets_creds = any(k in str(env_vars).lower() for k in ['aws_access_key_id', 'aws_secret_access_key'])
        if has_secrets_creds and not has_oidc_write:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'LONG_LIVED_AWS_CREDENTIALS',
                'issue': f'Job "{job_name}" uses long-lived AWS credentials instead of OIDC federation',
                'location': job_name,
                'fix': 'Use OIDC: permissions.id-token: write + aws-actions/configure-aws-credentials@v4 with role-to-assume'
            })

    return findings
```

**GCP OIDC Configuration:**
```python
def check_gcp_oidc_config(workflow_content):
    """Check GCP OIDC configuration."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {})
        steps = job_config.get('steps', [])

        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # Check for GCP action usage
        gcp_actions = ['google-github-actions/auth', 'google-github-actions/setup-cloud-sdk']
        has_gcp_action = any(any(gcp in s.get('uses', '') for gcp in gcp_actions) for s in steps)

        if has_oidc_write and not has_gcp_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_GCP_SETUP',
                'issue': f'Job "{job_name}" has id-token: write but no GCP action detected',
                'location': job_name,
                'fix': 'Configure google-github-actions/auth@v2 with use_oidc: true and workload_identity_provider'
            })

        # Check for long-lived GCP credentials
        env_vars = job_config.get('env', {})
        has_gcp_sa_key = any('GOOGLE_APPLICATION_CREDENTIALS' in str(env_vars) or 'gcp_service_account_key' in str(env_vars).lower() for env_vars in [job_config.get('env', {})])

    return findings
```

**Azure OIDC Configuration:**
```python
def check_azure_oidc_config(workflow_content):
    """Check Azure OIDC configuration."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {})
        steps = job_config.get('steps', [])

        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # Check for Azure action usage
        azure_actions = ['azure/login', 'azure-actions']
        has_azure_action = any(any(azure in s.get('uses', '') for azure in azure_actions) for s in steps)

        if has_oidc_write and not has_azure_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_AZURE_SETUP',
                'issue': f'Job "{job_name}" has id-token: write but no Azure action detected',
                'location': job_name,
                'fix': 'Configure azure/login@v1 with use-msi: true or federated identity credentials'
            })

    return findings
```

**OIDC Configuration Examples:**

| Provider | Action | Configuration | Badge |
|----------|--------|---------------|-------|
| AWS | `aws-actions/configure-aws-credentials@v4` | `role-to-assume: arn:aws:iam::123456789012:role/github-actions-role` <br> `use_oidc: true` | 🔵 |
| GCP | `google-github-actions/auth@v2` | `workload_identity_provider: projects/123456/locations/global/workloadIdentityPools/my-pool/providers/my-provider` <br> `service_account: my-service-account@my-project.iam.gserviceaccount.com` | 🔵 |
| Azure | `azure/login@v1` | `use-msi: true` (for managed identity) <br> or `client-id`, `tenant-id`, `subscription-id` for federated credentials | 🔵 |

#### 3.5 Docker Image Security (HIGH/MEDIUM) 🟡🔵

```python
def check_docker_image_security(workflow_content):
    """Check Docker container security in jobs."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        # Check for container configuration (runs-on: docker)
        container = job_config.get('container', {})
        if not container:
            continue

        image = container.get('image', '')
        options = container.get('options', '') or ''

        # Check if image is unpinned (no tag or @sha256 digest)
        if ':' not in image and '@' not in image:
            findings.append({
                'severity': 'HIGH',
                'type': 'UNPINNED_DOCKER_IMAGE',
                'issue': f'Container "{image}" has no version tag - uses latest implicitly',
                'location': f'{job_name}/container',
                'fix': f'Pin to specific tag: {image}:latest or better, use digest for immutability'
            })

        elif image.endswith(':latest'):
            findings.append({
                'severity': 'MEDIUM',
                'type': 'DOCKER_IMAGE_LATEST_TAG',
                'issue': f'Container "{image}" uses :latest tag - may change between runs',
                'location': f'{job_name}/container',
                'fix': 'Pin to specific version tag (e.g., node:20-alpine) or SHA digest for reproducibility'
            })

        # Check for root container privilege
        if '-t' in options or '--privileged' in options or 'userns-mode=host' in options:
            findings.append({
                'severity': 'HIGH',
                'type': 'DOCKER_ROOT_PRIVILEGES',
                'issue': f'Container "{image}" runs with elevated privileges',
                'location': f'{job_name}/container/options',
                'fix': 'Remove --privileged flag; use specific capability flags instead (e.g., --cap-add=SYS_ADMIN)'
            })

        # Check if container explicitly runs as root (non-root is safer)
        if 'user:' not in options and '-u' not in options:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'DOCKER_ROOT_USER',
                'issue': f'Container "{image}" may run as root user - consider specifying non-root user',
                'location': f'{job_name}/container/options',
                'fix': 'Add options: "user: 1000" to run as non-root user'
            })

    return findings
```

#### 3.6 Reusable Workflows (MEDIUM) 🔵

```python
def check_reusable_workflows(workflow_content):
    """Check for reusable workflow usage."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step in steps:
            uses = step.get('uses', '')

            # Detect reusable workflows (pattern: org/repo/.github/workflows/*.yml@ref)
            if '.github/workflows/' in uses and '@' in uses:
                parts = uses.split('@')
                workflow_path = parts[0]
                ref = parts[1] if len(parts) > 1 else ''

                # Check if reusable workflow is pinned to SHA or branch
                if ref in ['master', 'main']:
                    findings.append({
                        'severity': 'HIGH',
                        'type': 'REUSABLE_WORKFLOW_UNPINNED_BRANCH',
                        'issue': f'Reusable workflow "{workflow_path}" pinned to mutable branch',
                        'location': f'{job_name}/{step.get("name", "unnamed")}',
                        'fix': 'Pin reusable workflow to specific commit SHA or tagged version'
                    })

    return findings
```

### Step 4: Best Practices Checks

#### 4.1 Matrix Strategy for Parallelization (LOW) 🟢

```python
def check_matrix_strategy(workflow_content):
    """Check for matrix strategy opportunities."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        strategy = job_config.get('strategy', {})

        if not strategy:
            # Check if this job could benefit from parallelization
            steps = job_config.get('steps', [])
            step_names = [s.get('name', '').lower() for s in steps]
            run_commands = ' '.join(s.get('run', '') for s in steps).lower()

            test_keywords = ['test', 'lint', 'build', 'check']
            has_test_or_build = any(kw in str(step_names + [run_commands]) for kw in test_keywords)

            # Check if running on single OS without matrix
            runs_on = job_config.get('runs-on', 'ubuntu-latest')
            is_single_os = not isinstance(runs_on, dict) and 'matrix' not in str(run_commands)

            if has_test_or_build and is_single_os:
                findings.append({
                    'severity': 'LOW',
                    'type': 'NO_MATRIX_STRATEGY',
                    'issue': f'Job "{job_name}" could benefit from matrix strategy for parallel execution across OS/node versions',
                    'location': job_name,
                    'fix': 'Add strategy.matrix with os and version combinations; set fail-fast: false'
                })

    return findings
```

**Matrix Strategy Template:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
        exclude:
          - os: windows-latest
            node-version: 16  # Skip incompatible combinations

    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm ci
      - run: npm test
```

#### 4.2 Dependency Caching Strategy (MEDIUM) 🔵

```python
def check_caching(workflow_content):
    """Check for caching best practices."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])

        has_install_deps = False
        has_cache_step = False
        cache_type = None

        for step in steps:
            run_cmd = step.get('run', '').lower()
            uses_step = step.get('uses', '').lower()

            # Detect dependency installation commands
            if any(pkg in run_cmd for pkg in ['npm ci', 'yarn install', 'pip install', 'bundle install', 'mvn', 'gradle']):
                has_install_deps = True

            # Check for caching actions
            if 'cache' in uses_step or ('save-cache' in uses_step or 'restore-cache' in uses_step):
                has_cache_step = True
                if 'node' in uses_step:
                    cache_type = 'npm'
                elif 'python' in uses_step or 'pip' in uses_step or 'cache-python' in uses_step:
                    cache_type = 'python'
                elif 'maven' in uses_step or 'gradle' in uses_step:
                    cache_type = 'build-tool'

        if has_install_deps and not has_cache_step:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'NO_DEPENDENCY_CACHING',
                'issue': f'Job "{job_name}" installs dependencies without caching - slower builds',
                'location': job_name,
                'fix': 'Add actions/cache or setup-node with cache: npm to speed up builds by 50-80%'
            })

    return findings
```

**Caching Best Practices:**

| Package Manager | Cache Key Pattern | Action | Badge |
|-----------------|-------------------|--------|-------|
| Node.js (npm) | `hashFiles('package-lock.json')` | `actions/setup-node@v4` with `cache: 'npm'` | 🔵 |
| Node.js (yarn) | `hashFiles('yarn.lock')` | `actions/setup-node@v4` with `cache: 'yarn'` | 🔵 |
| Python (pip) | `hashFiles('requirements.txt')` or `Pipfile.lock` | `actions/cache@v4` with `~/.cache/pip` | 🔵 |
| Maven | `hashFiles('**/pom.xml')` | `actions/setup-java@v4` with `maven-cache: true` | 🔵 |
| Gradle | `hashFiles('**/*.gradle*')` | `actions/setup-java@v4` with `gradle-cache: true` | 🔵 |

#### 4.3 Approval Gates for Production (HIGH) 🟡

```python
def check_approval_gates(workflow_content, workflow_name):
    """Check for required approval gates on production deployments."""
    findings = []

    triggers = workflow_content.get('on', {})
    if isinstance(triggers, dict):
        trigger_types = list(triggers.keys())
    else:
        trigger_types = [triggers] if isinstance(triggers, str) else []

    deploy_keywords = ['deploy', 'release', 'production']
    job_names = list(workflow_content.get('jobs', {}).keys())
    step_names_all = []

    for job_config in workflow_content.get('jobs', {}).values():
        for step in job_config.get('steps', []):
            step_names_all.append(step.get('name', '').lower())

    all_names = ' '.join(job_names + step_names_all)
    is_deploy_workflow = any(kw in all_names.lower() for kw in deploy_keywords)

    if is_deploy_workflow:
        # Check for push to main/master without environment protection
        if isinstance(triggers, dict):
            push_triggers = triggers.get('push', {})
            branches = push_triggers.get('branches', []) if isinstance(push_triggers, dict) else []

            if 'main' in branches or 'master' in branches:
                # Check jobs for environment configuration
                has_environment_protection = False
                for job_name, job_config in workflow_content.get('jobs', {}).items():
                    if job_config.get('environment'):
                        has_environment_protection = True
                        break

                if not has_environment_protection:
                    findings.append({
                        'severity': 'HIGH',
                        'type': 'AUTO_DEPLOY_TO_MAIN',
                        'issue': f'Workflow "{workflow_name}" auto-deploys on push to main/master without environment protection',
                        'location': workflow_name,
                        'fix': 'Add `environment: production` to deploy job and configure required reviewers in repo settings'
                    })

    # Check for workflow_dispatch (manual trigger) - should have confirmation if deploying
    if isinstance(triggers, dict) and 'workflow_dispatch' in triggers:
        findings.append({
            'severity': 'MEDIUM',
            'type': 'MANUAL_DEPLOY_TRIGGER',
            'issue': f'Workflow "{workflow_name}" can be manually triggered - ensure environment protection is configured',
            'location': workflow_name,
            'fix': 'Add `environment` with required reviewers to deployment jobs for manual triggers'
        })

    return findings
```

**Environment Protection Configuration:**
```yaml
# In .github/workflows/deploy.yml
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # Requires approval if configured in repo settings
    steps:
      - name: Deploy to Production
        run: ./deploy.sh production
```

**Configure Environment Protection:**
1. Go to Repository Settings → Environments
2. Click "New environment" or edit existing "production"
3. Set "Required reviewers" (e.g., @team-leads, @senior-engineers)
4. Enable "Wait timer" if needed (optional)
5. Enable "Prevent automatic includes" to block direct pushes

### Step 5: Performance Analysis

#### 5.1 Redundant Steps (LOW) 🟢

```python
def check_redundant_steps(workflow_content):
    """Check for unnecessary or redundant workflow steps."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])

        # Check for redundant checkout (should only be done once per job)
        checkout_count = sum(1 for s in steps if 'checkout' in s.get('uses', '').lower())

        if checkout_count > 1:
            findings.append({
                'severity': 'LOW',
                'type': 'REDUNDANT_CHECKOUT',
                'issue': f'Job "{job_name}" has {checkout_count} checkout steps - should be once per job',
                'location': job_name,
                'fix': 'Remove duplicate checkout steps; use persist-credentials: false for subsequent checks if needed'
            })

    return findings
```

#### 5.2 Conditional Execution (LOW) 🟢

```python
def check_conditional_execution(workflow_content):
    """Check for conditional execution opportunities."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])

        # Check if deploy-like steps lack conditionals
        for step in steps:
            step_name = step.get('name', '').lower()
            run_cmd = step.get('run', '').lower()
            has_if = 'if:' in str(job_config) or 'if:' in str(step)

            is_deploy_step = any(kw in step_name for kw in ['deploy', 'release']) or \
                           any(kw in run_cmd for kw in ['./deploy', './publish', 'aws s3 sync'])

            if is_deploy_step and not has_if:
                findings.append({
                    'severity': 'LOW',
                    'type': 'NO_DEPLOY_CONDITIONAL',
                    'issue': f'Step "{step.get("name")}" may run on all branches - consider adding `if` condition',
                    'location': f'{job_name}/{step.get("name", "unnamed")}',
                    'fix': 'Add `if: github.ref == \'refs/heads/main\'` to deploy steps'
                })

    return findings
```

### Step 6: Dependabot Configuration Check (LOW) 🟢

```python
def check_dependabot_config(repo_path='.'):
    """Check for dependabot configuration."""
    findings = []

    dependabot_path = Path(repo_path) / '.github' / 'dependabot.yml'
    if not dependabot_path.exists():
        findings.append({
            'severity': 'LOW',
            'type': 'NO_DEPENDABOT_CONFIG',
            'issue': 'No dependabot configuration found - consider enabling automated dependency updates',
            'location': '.github/dependabot.yml',
            'fix': 'Create .github/dependabot.yml with version updates and auto-merge enabled'
        })

    return findings


def check_dependabot_auto_merge(repo_path='.'):
    """Check if dependabot has auto-merge configured."""
    findings = []

    dependabot_path = Path(repo_path) / '.github' / 'dependabot.yml'
    if not dependabot_path.exists():
        return findings

    with open(dependabot_path, 'r') as f:
        content = yaml.safe_load(f)

    # Check for auto-merge configuration
    has_auto_merge = False
    if isinstance(content, dict):
        for updater in content.get('updates', []):
            if isinstance(updater, dict) and updater.get('open-pull-requests-limit'):
                has_auto_merge = True
                break

    # Note: auto-merge is often configured via GitHub UI, not dependabot.yml
    # This check provides a hint for users to verify in settings

    return findings
```

**Dependabot Configuration Template:**
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - dependencies
      - npm
    commit-message:
      prefix: "chore"

  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

**Dependabot Auto-Merge Configuration (GitHub UI):**
1. Go to Repository Settings → Dependabot
2. Enable "Auto-merge" for pull requests from dependabot
3. Set merge method (squash, rebase, or merge)
4. Optionally require status checks before auto-merge

### Step 7: Generate Structured Report with Severity Badges

```python
def generate_audit_report(workflows, findings):
    """Generate structured audit report with severity badges."""

    # Aggregate by severity
    critical = [f for f in findings if f.get('severity') == 'CRITICAL']
    high = [f for f in findings if f.get('severity') == 'HIGH']
    medium = [f for f in findings if f.get('severity') == 'MEDIUM']
    low = [f for f in findings if f.get('severity') == 'LOW']

    # Severity badge mapping
    severity_badges = {
        'CRITICAL': '🔴',
        'HIGH': '🟡',
        'MEDIUM': '🔵',
        'LOW': '🟢'
    }

    report_lines = []
    report_lines.append("== CI/CD PIPELINE AUDIT REPORT ==")
    report_lines.append("")
    report_lines.append(f"Generated: {datetime.now().isoformat()}")
    report_lines.append(f"Repository: {get_repo_name()}")
    report_lines.append(f"Workflows Audited: {len(workflows)}")
    report_lines.append("")

    # Summary with tree diagram and badges
    report_lines.append("=== SUMMARY ===")
    report_lines.append("")
    report_lines.append(f"Total Findings: {len(findings)}")
    report_lines.append(f"├─ 🔴 CRITICAL: {len(critical)} (requires immediate attention)")
    report_lines.append(f"├─ 🟡 HIGH: {len(high)} (should be addressed soon)")
    report_lines.append(f"├─ 🔵 MEDIUM: {len(medium)} (recommended improvements)")
    report_lines.append(f"└─ 🟢 LOW: {len(low)} (optimization suggestions)")
    report_lines.append("")

    # Calculate overall risk level
    total_score = len(critical) * 10 + len(high) * 5 + len(medium) * 2 + len(low) * 1
    if total_score >= 30:
        overall_risk = "CRITICAL"
    elif total_score >= 15:
        overall_risk = "HIGH"
    elif total_score >= 5:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    report_lines.append(f"Overall Risk Level: {overall_risk}")
    report_lines.append("")

    # Per-workflow breakdown
    for workflow_name, workflow_data in workflows.items():
        workflow_findings = [f for f in findings if f.get('workflow') == workflow_name or workflow_name in str(f.get('location', ''))]

        # Calculate risk level per workflow
        wf_critical = len([f for f in workflow_findings if f.get('severity') == 'CRITICAL'])
        wf_high = len([f for f in workflow_findings if f.get('severity') == 'HIGH'])
        wf_medium = len([f for f in workflow_findings if f.get('severity') == 'MEDIUM'])
        wf_low = len([f for f in workflow_findings if f.get('severity') == 'LOW'])

        wf_score = wf_critical * 10 + wf_high * 5 + wf_medium * 2 + wf_low * 1
        if wf_score >= 15:
            risk_level = "CRITICAL"
        elif wf_score >= 5:
            risk_level = "HIGH"
        elif wf_score >= 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        report_lines.append(f"=== WORKFLOW: {workflow_name} ===")
        report_lines.append("")
        report_lines.append(f"Risk Level: {risk_level}")
        report_lines.append(f"Findings: {len(workflow_findings)}")
        report_lines.append("")

        # List findings with badges
        for finding in workflow_findings:
            badge = severity_badges.get(finding.get('severity', 'LOW'), '')
            report_lines.append(f"[{badge}] {finding['type']}")
            report_lines.append(f"Location: {finding['location']}")
            report_lines.append(f"Issue: {finding['issue']}")
            report_lines.append(f"Fix: {finding['fix']}")
            report_lines.append("")

        report_lines.append("")

    # Recommended fixes section with detailed YAML examples
    report_lines.extend(generate_fix_suggestions(findings))

    return '\n'.join(report_lines)


def generate_fix_suggestions(findings):
    """Generate detailed fix suggestions with YAML examples."""
    lines = []
    lines.append("=== RECOMMENDED FIXES ===")
    lines.append("")

    # Group findings by type for consolidated fixes
    finding_types = set(f['type'] for f in findings)

    if 'WRITE_ALL_PERMISSIONS' in finding_types:
        lines.extend([
            "1. **Least Privilege Permissions**",
            "   Replace `permissions: write-all` with specific permissions:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# BEFORE (insecure)")
        lines.append("permissions: write-all")
        lines.append("")
        lines.append("# AFTER (secure - least privilege)")
        lines.append("permissions:")
        lines.append("  contents: read")
        lines.append("  pull-requests: read")
        lines.append("  checks: write")
        lines.append("  security-events: write")
        lines.append("```")
        lines.append("")

    if 'UNPINNED_BRANCH_REFERENCE' in finding_types or 'MAJOR_VERSION_ONLY' in finding_types:
        lines.extend([
            "2. **Pin Actions to Commit SHA**",
            "   Update all action references to use commit SHAs for reproducibility and supply chain security:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# BEFORE (vulnerable)")
        lines.append("uses: actions/checkout@main")
        lines.append("uses: actions/setup-node@v4")
        lines.append("")
        lines.append("# AFTER (secure - pinned to specific commits)")
        lines.append("uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1")
        lines.append("uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1")
        lines.append("```")
        lines.append("")

    if 'LONG_LIVED_AWS_CREDENTIALS' in finding_types or 'OIDC_WITHOUT_AWS_SETUP' in finding_types:
        lines.extend([
            "3. **Enable OIDC Authentication for AWS**",
            "   Replace long-lived secrets with OIDC federation:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# BEFORE (insecure - long-lived credentials)")
        lines.append("permissions: {}")
        lines.append("env:")
        lines.append("  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}")
        lines.append("  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}")
        lines.append("steps:")
        lines.append("  - uses: aws-actions/configure-aws-credentials@v2")
        lines.append("")
        lines.append("# AFTER (secure - OIDC federation)")
        lines.append("permissions:")
        lines.append("  id-token: write")
        lines.append("  contents: read")
        lines.append("steps:")
        lines.append("  - name: Configure AWS credentials via OIDC")
        lines.append("    uses: aws-actions/configure-aws-credentials@v4")
        lines.append("    with:")
        lines.append("      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role")
        lines.append("      aws-region: us-east-1")
        lines.append("```")
        lines.append("")

    if 'AUTO_DEPLOY_TO_MAIN' in finding_types:
        lines.extend([
            "4. **Add Approval Gate for Production**",
            "   Require reviewer approval before deployments:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# BEFORE (insecure - auto-deploy)")
        lines.append("on:")
        lines.append("  push:")
        lines.append("    branches: [main]")
        lines.append("jobs:")
        lines.append("  deploy-production:")
        lines.append("    runs-on: ubuntu-latest")
        lines.append("    steps:")
        lines.append("      - run: ./deploy.sh production")
        lines.append("")
        lines.append("# AFTER (secure - requires approval)")
        lines.append("on:")
        lines.append("  push:")
        lines.append("    branches: [main]")
        lines.append("jobs:")
        lines.append("  deploy-production:")
        lines.append("    runs-on: ubuntu-latest")
        lines.append("    environment: production  # Requires approval in repo settings")
        lines.append("    steps:")
        lines.append("      - run: ./deploy.sh production")
        lines.append("```")
        lines.append("")

    if 'NO_DEPENDENCY_CACHING' in finding_types:
        lines.extend([
            "5. **Add Dependency Caching**",
            "   Speed up builds with caching for dependencies:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# BEFORE (slow - no caching)")
        lines.append("steps:")
        lines.append("  - name: Install dependencies")
        lines.append("    run: pip install -r requirements.txt")
        lines.append("")
        lines.append("# AFTER (fast - with caching)")
        lines.append("- uses: actions/cache@v4")
        lines.append("  with:")
        lines.append("    path: ~/.cache/pip")
        lines.append("    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}")
        lines.append("    restore-keys: |")
        lines.append("      ${{ runner.os }}-pip-")
        lines.append("```")
        lines.append("")

    if 'NO_MATRIX_STRATEGY' in finding_types:
        lines.extend([
            "6. **Add Matrix Strategy for Parallel Execution**",
            "   Run tests across multiple environments in parallel:",
            ""
        ])
        lines.append("```yaml")
        lines.append("jobs:")
        lines.append("  test:")
        lines.append("    runs-on: ubuntu-latest")
        lines.append("    strategy:")
        lines.append("      matrix:")
        lines.append("        node-version: [16, 18, 20]")
        lines.append("        os: [ubuntu-latest, windows-latest]")
        lines.append("        exclude:")
        lines.append("          - os: windows-latest")
        lines.append("            node-version: 16")
        lines.append("      fail-fast: false")
        lines.append("    steps:")
        lines.append("      - uses: actions/checkout@v4")
        lines.append("      - name: Use Node.js ${{ matrix.node-version }}")
        lines.append("        uses: actions/setup-node@v4")
        lines.append("        with:")
        lines.append("          node-version: ${{ matrix.node-version }}")
        lines.append("```")
        lines.append("")

    if 'NO_DEPENDABOT_CONFIG' in finding_types:
        lines.extend([
            "7. **Enable Dependabot for Automated Dependency Updates**",
            "   Configure dependabot to automatically update dependencies:",
            ""
        ])
        lines.append("```yaml")
        lines.append("# .github/dependabot.yml")
        lines.append("version: 2")
        lines.append("updates:")
        lines.append("  - package-ecosystem: \"npm\"")
        lines.append("    directory: \"/\"")
        lines.append("    schedule:")
        lines.append("      interval: \"weekly\"")
        lines.append("    open-pull-requests-limit: 10")
        lines.append("    labels:")
        lines.append("      - dependencies")
        lines.append("")
        lines.append("  - package-ecosystem: \"pip\"")
        lines.append("    directory: \"/backend\"")
        lines.append("    schedule:")
        lines.append("      interval: \"weekly\"")
        lines.append("```")
        lines.append("")

    return lines
```

### Step 8: Output Final Report Format

**Report Format Template:**
```markdown
== CI/CD PIPELINE AUDIT REPORT ==

Generated: 2026-03-07T14:32:00Z
Repository: skills/ci-cd-pipeline-auditor/test-workflows
Workflows Audited: 2

=== SUMMARY ===

Total Findings: 9
├─ 🔴 CRITICAL: 2 (requires immediate attention)
├─ 🟡 HIGH: 3 (should be addressed soon)
├─ 🔵 MEDIUM: 3 (recommended improvements)
└─ 🟢 LOW: 1 (optimization suggestions)

Overall Risk Level: CRITICAL

=== WORKFLOW: ci.yml ===

Risk Level: CRITICAL
Findings: 4

[🔴] WRITE_ALL_PERMISSIONS
Location: root permissions
Issue: Workflow has write-all permissions - violates least privilege principle
Fix: Specify only required permissions (contents: read, checks: write, etc.)

[🟡] UNPINNED_BRANCH_REFERENCE
Location: build/checkout
Issue: Action "actions/checkout" pinned to branch (@main) - vulnerable to supply chain attack
Fix: Pin to specific commit SHA: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec

[🟡] MAJOR_VERSION_ONLY
Location: build/setup-node
Issue: Action "actions/setup-node" uses only major version (@v4) - not pinned to specific tag
Fix: Pin to specific tag: actions/setup-node@v4.5.0 or commit SHA for reproducibility

[🔵] SECRETS_IN_RUN_COMMAND
Location: build/test
Issue: Secrets used directly in run command may be exposed in logs via echo statement
Fix: Use env block instead of echoing secrets; avoid printing sensitive values


=== WORKFLOW: deploy.yml ===

Risk Level: HIGH
Findings: 5

[🟡] UNTRUSTED_ACTION_SOURCE
Location: deploy/configure-aws-credentials
Issue: Using long-lived AWS credentials instead of OIDC federation
Fix: Use OIDC for cloud provider authentication (more secure than secrets)

[🟡] AUTO_DEPLOY_TO_MAIN
Location: deploy.yml trigger
Issue: Workflow auto-deploys on push to main without approval gate or environment protection
Fix: Add environment: production to require reviewer approval in repo settings

[🔵] NO_DEPENDENCY_CACHING
Location: deploy/install-dependencies
Issue: Job installs dependencies (pip install) without caching between runs
Fix: Add actions/cache step with pip cache directory for faster builds

[🔵] OIDC_WITHOUT_PROVIDER_SETUP
Location: deploy/configure-aws-credentials
Issue: Using long-lived secrets instead of modern OIDC authentication pattern
Fix: Configure AWS via OIDC: permissions.id-token: write + use_oidc: true

[🟢] NO_MATRIX_STRATEGY
Location: deploy
Issue: Job could benefit from matrix strategy for parallel test execution across Python versions
Fix: Add matrix strategy to run tests against multiple Python versions in parallel


=== RECOMMENDED FIXES ===

1. **Least Privilege Permissions**
   Replace `permissions: write-all` with specific permissions:

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

2. **Pin Actions to Commit SHA**
   Update all action references to use commit SHAs for reproducibility and supply chain security:

```yaml
# BEFORE (vulnerable)
uses: actions/checkout@main
uses: actions/setup-node@v4

# AFTER (secure - pinned to specific commits)
uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1
uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1
```

3. **Enable OIDC Authentication for AWS**
   Replace long-lived secrets with OIDC federation:

```yaml
# BEFORE (insecure - long-lived credentials)
permissions: {}
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

4. **Add Approval Gate for Production**
   Require reviewer approval before deployments:

```yaml
# BEFORE (insecure - auto-deploy)
on:
  push:
    branches: [main]
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy.sh production

# AFTER (secure - requires approval)
on:
  push:
    branches: [main]
jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production  # Requires approval in repo settings
    steps:
      - run: ./deploy.sh production
```

5. **Add Dependency Caching**
   Speed up builds with caching for pip dependencies:

```yaml
# BEFORE (slow)
steps:
  - name: Install dependencies
    run: pip install -r requirements.txt

# AFTER (fast - with caching)
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```


=== ACTION ITEMS ===

Priority | Item | Estimated Effort | Severity
---------|------|------------------|----------
P0 | Remove write-all permissions from ci.yml | 15 min | 🔴 CRITICAL
P0 | Pin actions/checkout to commit SHA in ci.yml | 10 min | 🟡 HIGH
P1 | Add environment protection for production deployments | 30 min | 🟡 HIGH
P2 | Implement OIDC authentication for AWS | 1 hour | 🔵 MEDIUM
P3 | Add pip dependency caching to deploy job | 30 min | 🔵 MEDIUM


=== COMPLIANCE CHECKLIST ===

- [ ] No secrets exposed in logs or workflow files
- [ ] All actions pinned to commit SHAs or specific tags
- [ ] Least-privilege permissions applied to all workflows
- [ ] OIDC used instead of long-lived credentials for cloud providers
- [ ] Environment protection rules configured for production deployments
- [ ] Required reviews enforced before deployment via repository settings
- [ ] Dependency caching implemented in build jobs (npm, pip, maven)
- [ ] Matrix strategy used for parallel test execution across OS/node versions
- [ ] Docker images pinned to version tags or SHA digests
- [ ] Dependabot configured with auto-merge enabled

```

### Step 9: Continuous Monitoring Recommendations

**Monitoring Setup:**
```bash
# GitHub CLI - Check workflow audit logs
gh api repos/{owner}/{repo}/actions/runs | jq '.workflow_runs[] | {name, status, conclusion}'

# Set up alerts for failed deployments
gh workflow disable --reason "security_review_required" {workflow-id}

# Scan workflows regularly with third-party tools
npx @trufflesecurity/trufflehog repo https://github.com/{owner}/{repo} --only-secrets
```

**Automated Scanning Integration:**
```yaml
name: Security Scan
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM
  push:
    paths:
      - '.github/workflows/*.yml'

jobs:
  scan-workflows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run GitHub Actions Security Scanner
        uses: secureflag/github-action-security-scanner@v1
        with:
          fail-on-critical: true
          fail-on-high: false

      - name: Upload findings to security tab
        if: failure()
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: findings.sarif
```

---

## Activation phrases / When to use

- "Audit my GitHub Actions workflows"
- "Review CI/CD security in this repo"
- "Check GitHub Actions best practices"
- "Find vulnerabilities in my workflows"
- "Improve this GitHub Actions pipeline"
- "Check OIDC configuration for AWS/GCP/Azure"
- "Analyze matrix strategy and caching opportunities"

## Usage Examples

```bash
# Audit all workflows for security risks
Audit all workflows in this repo for security risks

# Review CI/CD pipeline for best practices and performance
Review my CI/CD pipeline for best practices and performance

# Check if workflows use pinned versions and OIDC
Check if my GitHub Actions use pinned versions and OIDC

# Find secrets exposure or overly broad permissions
Find secrets exposure or overly broad permissions in workflows

# Get comprehensive security audit report with badges
Perform full security audit on all GitHub Actions workflows

# Check for dependabot configuration
Analyze dependency management and dependabot setup
```

## How it works

1. **Scans workflow files**: Locates `.github/workflows/*.yml` files, identifies trigger types (`push`, `pull_request`, `schedule`, `workflow_dispatch`, `workflow_call`)
2. **Parses structure**: Extracts jobs, steps, permissions, environment variables, secrets usage, matrix strategies, container configurations
3. **Security checks**: Identifies secrets exposure, write-all permissions, unpinned actions (branch vs SHA), untrusted sources, OIDC misconfigurations for AWS/GCP/Azure
4. **Docker security**: Checks for unpinned images, root privileges, root user containers
5. **Best practice checks**: Validates caching strategy, matrix utilization, approval gates, reusable workflow pinning
6. **Dependabot check**: Verifies dependency update automation and auto-merge configuration
7. **Risk calculation**: Aggregates findings into severity levels with badge indicators (🔴 CRITICAL / 🟡 HIGH / 🔵 MEDIUM / 🟢 LOW)
8. **Report generation**: Produces structured report with workflow-by-workflow breakdown, tree diagram summary, and detailed fix suggestions
9. **Fix suggestions**: Provides improved YAML snippets for common issues including OIDC federation examples

## Dependencies

- None required (reads YAML files directly using Python yaml library or Node.js js-yaml)
- Optional: GitHub API for repository metadata (branch protection rules, environment configurations)
- Recommended: `gh` CLI for post-audit actions (enabling protections, disabling risky workflows)

## Best Practices / Notes

### Security First Principles 🔒

1. **OIDC Over Secrets**: Prefer OIDC federation over long-lived secrets for cloud provider authentication (AWS/GCP/Azure)
2. **Pin to SHA**: Always pin actions and reusable workflows to specific commit SHAs for supply chain security
3. **Least Privilege**: Use minimum required permissions; default to `read` unless `write` is explicitly needed
4. **Environment Protection**: Require approvals for production deployments via repository environment settings

### Performance Optimization ⚡

1. **Dependency Caching**: Always cache dependencies (npm, pip, maven) based on lock file hashes
2. **Matrix Strategy**: Run tests across multiple OS/node versions in parallel using matrix strategy with `fail-fast: false`
3. **Conditional Execution**: Use `if` conditions to skip unnecessary steps (e.g., skip deploy for PRs)

### Dependency Management 📦

1. **Dependabot**: Enable dependabot for automated dependency updates with weekly schedules
2. **Auto-Merge**: Configure auto-merge for dependabot PRs in repository settings
3. **Lock Files**: Ensure lock files (package-lock.json, requirements.txt) are committed and not ignored

### Compliance Requirements ✅

1. **Approval Gates**: Production deployments must require reviewer approval via environment protection rules
2. **Branch Protection**: Enforce pull request reviews before merging to protected branches (main, master)
3. **Audit Trail**: Enable workflow run logging and configure alerts for failed or suspicious deployments

### Common Pitfalls ❌

- Don't use `permissions: write-all` - always specify exact permissions needed
- Don't pin actions to branch names (`@main`, `@master`) - these are mutable and vulnerable
- Don't echo secrets in logs - even when using `${{ secrets.* }}`, avoid printing them
- Don't skip environment protection for production deployments
- Don't use unpinned Docker images in jobs - always specify version tags or SHA digests

---

## Risk Severity Reference

| Severity | Description | Response Time | Badge | Examples |
|----------|-------------|---------------|-------|----------|
| CRITICAL | Immediate security risk requiring urgent action | < 1 hour | 🔴 | write-all permissions, secrets in plaintext, unpinned to branch (@main/@master) |
| HIGH | Significant vulnerability that should be fixed soon | < 24 hours | 🟡 | major version only (v4), auto-deploy without approval, untrusted actions, Docker root privileges |
| MEDIUM | Recommended improvement with moderate impact | < 1 week | 🔵 | missing caching, no OIDC setup, manual deploy triggers, latest Docker tags, long-lived credentials |
| LOW | Optimization suggestion for better practices | < 1 month | 🟢 | matrix strategy opportunities, redundant steps, no dependabot config |

---

## Example Audit Report Output

```markdown
== CI/CD PIPELINE AUDIT REPORT ==

Generated: 2026-03-07T14:32:00Z
Repository: skills/ci-cd-pipeline-auditor/test-workflows
Workflows Audited: 2

=== SUMMARY ===

Total Findings: 9
├─ 🔴 CRITICAL: 2 (requires immediate attention)
├─ 🟡 HIGH: 3 (should be addressed soon)
├─ 🔵 MEDIUM: 3 (recommended improvements)
└─ 🟢 LOW: 1 (optimization suggestions)

Overall Risk Level: CRITICAL

=== WORKFLOW: ci.yml ===

Risk Level: CRITICAL
Findings: 4

[🔴] WRITE_ALL_PERMISSIONS
Location: root permissions
Issue: Workflow has write-all permissions - violates least privilege principle
Fix: Specify only required permissions (contents: read, checks: write, etc.)

[🟡] UNPINNED_BRANCH_REFERENCE
Location: build/checkout
Issue: Action "actions/checkout" pinned to branch (@main) - vulnerable to supply chain attack
Fix: Pin to specific commit SHA: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec

[🟡] MAJOR_VERSION_ONLY
Location: build/setup-node
Issue: Action "actions/setup-node" uses only major version (@v4) - not pinned to specific tag
Fix: Pin to specific tag: actions/setup-node@v4.5.0 or commit SHA for reproducibility

[🔵] SECRETS_IN_RUN_COMMAND
Location: build/test
Issue: Secrets used directly in run command may be exposed in logs via echo statement
Fix: Use env block instead of echoing secrets; avoid printing sensitive values


=== WORKFLOW: deploy.yml ===

Risk Level: HIGH
Findings: 5

[🟡] UNTRUSTED_ACTION_SOURCE
Location: deploy/configure-aws-credentials
Issue: Using long-lived AWS credentials instead of OIDC federation
Fix: Use OIDC for cloud provider authentication (more secure than secrets)

[🟡] AUTO_DEPLOY_TO_MAIN
Location: deploy.yml trigger
Issue: Workflow auto-deploys on push to main without approval gate or environment protection
Fix: Add environment: production to require reviewer approval in repo settings

[🔵] NO_DEPENDENCY_CACHING
Location: deploy/install-dependencies
Issue: Job installs dependencies (pip install) without caching between runs
Fix: Add actions/cache step with pip cache directory for faster builds

[🔵] OIDC_WITHOUT_PROVIDER_SETUP
Location: deploy/configure-aws-credentials
Issue: Using long-lived secrets instead of modern OIDC authentication pattern
Fix: Configure AWS via OIDC: permissions.id-token: write + use_oidc: true

[🟢] NO_MATRIX_STRATEGY
Location: deploy
Issue: Job could benefit from matrix strategy for parallel test execution across Python versions
Fix: Add matrix strategy to run tests against multiple Python versions in parallel


=== RECOMMENDED FIXES ===

1. **Least Privilege Permissions**...
2. **Pin Actions to Commit SHA**...
3. **Enable OIDC Authentication for AWS**...
4. **Add Approval Gate for Production**...
5. **Add Dependency Caching**...
6. **Add Matrix Strategy for Parallel Execution**...
7. **Enable Dependabot for Automated Dependency Updates**...

=== ACTION ITEMS ===

Priority | Item | Estimated Effort | Severity
---------|------|------------------|----------
P0 | Remove write-all permissions from ci.yml | 15 min | 🔴 CRITICAL
P0 | Pin actions/checkout to commit SHA in ci.yml | 10 min | 🟡 HIGH
P1 | Add environment protection for production deployments | 30 min | 🟡 HIGH
...

=== COMPLIANCE CHECKLIST ===

- [ ] No secrets exposed in logs or workflow files
- [ ] All actions pinned to commit SHAs or specific tags
- [ ] Least-privilege permissions applied to all workflows
- [ ] OIDC used instead of long-lived credentials for cloud providers (AWS/GCP/Azure)
- [ ] Environment protection rules configured for production deployments
- [ ] Required reviews enforced before deployment via repository settings
- [ ] Dependency caching implemented in build jobs (npm, pip, maven)
- [ ] Matrix strategy used for parallel test execution across OS/node versions
- [ ] Docker images pinned to version tags or SHA digests
- [ ] Dependabot configured with auto-merge enabled

```

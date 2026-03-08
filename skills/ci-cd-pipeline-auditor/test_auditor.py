#!/usr/bin/env python3
"""Test script to run CI/CD Pipeline Auditor on test workflows."""

import os
import sys
from pathlib import Path
import yaml
import json
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

def identify_triggers(workflow_content):
    """Identify workflow trigger types."""
    triggers = workflow_content.get('on', [])
    if isinstance(triggers, dict):
        return list(triggers.keys())
    elif isinstance(triggers, list):
        return [t for t in triggers if isinstance(t, str)]
    return []

def check_secrets_in_run_commands(workflow_content):
    """Check for secrets exposed in run commands."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step_idx, step in enumerate(steps):
            run_cmd = step.get('run', '') or ''
            if isinstance(run_cmd, list):
                run_cmd = '\n'.join(run_cmd)

            # Check for echo statements that might expose secrets
            secret_patterns = ['echo.*secrets\.', 'echo.*${{ secrets.',
                             'API_KEY', 'SECRET_TOKEN', 'PRIVATE_KEY',
                             'AWS_SECRET_ACCESS_KEY']

            for pattern in secret_patterns:
                if pattern.lower() in run_cmd.lower():
                    findings.append({
                        'severity': 'CRITICAL',
                        'type': 'SECRETS_IN_RUN_COMMAND',
                        'location': f'{job_name} step {step_idx + 1}',
                        'description': f'Potential secrets exposure in echo command: {run_cmd[:50]}...',
                        'recommendation': 'Use env blocks instead of run commands for secrets'
                    })

    return findings

def check_permissions(workflow_content):
    """Check for overly broad permissions."""
    findings = []
    permissions = workflow_content.get('permissions', '') or {}

    if permissions == 'write-all':
        findings.append({
            'severity': 'CRITICAL',
            'type': 'WRITE_ALL_PERMISSIONS',
            'location': 'root level',
            'description': 'Workflow has write-all permissions violating least privilege principle',
            'recommendation': 'Specify exact required permissions only'
        })

    return findings

def check_action_pinning(workflow_content):
    """Check for unpinned actions."""
    findings = []
    mutable_branches = ['@main', '@master', '@latest', '@develop']

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        steps = job_config.get('steps', [])
        for step_idx, step in enumerate(steps):
            uses = step.get('uses', '') or ''

            if not uses:
                continue

            # Check for branch references (CRITICAL)
            for branch in mutable_branches:
                if uses.endswith(branch):
                    findings.append({
                        'severity': 'CRITICAL',
                        'type': 'UNPINNED_BRANCH_REFERENCE',
                        'location': f'{job_name} step {step_idx + 1}',
                        'description': f'Action pinned to mutable branch: {uses}',
                        'recommendation': 'Pin to commit SHA for reproducibility and supply chain security',
                        'action_reference': uses
                    })

            # Check for major version only (HIGH)
            if '@v' in uses or '@V' in uses:
                parts = uses.split('@')
                if len(parts) == 2:
                    ref = parts[1]
                    if ref.startswith('v') and len(ref) == 2:  # e.g., @v4
                        findings.append({
                            'severity': 'HIGH',
                            'type': 'MAJOR_VERSION_ONLY',
                            'location': f'{job_name} step {step_idx + 1}',
                            'description': f'Action uses only major version: {uses}. This may cause unexpected changes.',
                            'recommendation': f'Pin to specific tag (e.g., {ref}.0) or SHA for reproducibility',
                            'action_reference': uses
                        })

    return findings

def check_aws_oidc_config(workflow_content):
    """Check AWS OIDC configuration."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {}) or {}
        steps = job_config.get('steps', [])

        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # AWS action patterns
        aws_actions = ['aws-actions/configure-aws-credentials', 'amazonwebservices/aws-cli-action']
        has_aws_action = any(
            any(aws in s.get('uses', '') for aws in aws_actions)
            for s in steps
        )

        # Check for long-lived credentials
        env_vars = job_config.get('env', {}) or {}
        if isinstance(env_vars, list):
            env_vars_dict = {}
            for item in env_vars:
                if isinstance(item, dict) and 'name' in item and 'value' in item:
                    env_vars_dict[item['name']] = item['value']
            env_vars = env_vars_dict

        aws_secrets = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']
        has_aws_secrets = any(secret in str(env_vars) for secret in aws_secrets)

        if has_oidc_write and not has_aws_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_AWS_SETUP',
                'location': f'{job_name}',
                'description': 'OIDC id-token: write permission set but no AWS action detected. Verify OIDC configuration is correct.',
                'recommendation': 'Configure aws-actions/configure-aws-credentials with role-to-assume and use_oidc: true'
            })

        if has_aws_secrets and not has_oidc_write:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'LONG_LIVED_AWS_CREDENTIALS',
                'location': f'{job_name}',
                'description': 'Workflow uses long-lived AWS credentials instead of OIDC federation.',
                'recommendation': 'Use OIDC: add id-token: write to permissions and configure-aws-credentials with role-to-assume',
                'before_after': {
                    'long_lived': '''env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}''',
                    'oidc': '''permissions:
  id-token: write
  contents: read

steps:
  - name: Configure AWS via OIDC
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role
      aws-region: us-east-1
      use_oidc: true'''
                }
            })

    return findings

def check_gcp_oidc_config(workflow_content):
    """Check GCP OIDC configuration."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {}) or {}
        steps = job_config.get('steps', [])

        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # GCP action patterns
        gcp_actions = ['google-github-actions/auth', 'google-github-actions/setup-gcloud']
        has_gcp_action = any(
            any(gcp in s.get('uses', '') for gcp in gcp_actions)
            for s in steps
        )

        # Check for long-lived credentials (service account key)
        env_vars = job_config.get('env', {}) or {}
        if isinstance(env_vars, list):
            env_vars_dict = {}
            for item in env_vars:
                if isinstance(item, dict) and 'name' in item and 'value' in item:
                    env_vars_dict[item['name']] = item['value']
            env_vars = env_vars_dict

        gcp_secrets = ['GOOGLE_APPLICATION_CREDENTIALS', 'GCP_SERVICE_ACCOUNT_KEY']
        has_gcp_secrets = any(secret in str(env_vars) for secret in gcp_secrets)

        if has_oidc_write and not has_gcp_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_GCP_SETUP',
                'location': f'{job_name}',
                'description': 'OIDC id-token: write permission set but no GCP action detected.',
                'recommendation': 'Configure google-github-actions/auth with workload_identity_provider'
            })

        if has_gcp_secrets and not has_oidc_write:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'LONG_LIVED_GCP_CREDENTIALS',
                'location': f'{job_name}',
                'description': 'Workflow uses long-lived GCP service account credentials.',
                'recommendation': 'Use OIDC federation with google-github-actions/auth',
                'before_after': {
                    'long_lived': '''env:
  GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}''',
                    'oidc': '''permissions:
  id-token: write
  contents: read

steps:
  - name: Authenticate to GCP via OIDC
    uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider
      service_account: my-service-account@my-project.iam.gserviceaccount.com'''
                }
            })

    return findings

def check_azure_oidc_config(workflow_content):
    """Check Azure OIDC configuration."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        perms = job_config.get('permissions', {}) or {}
        steps = job_config.get('steps', [])

        has_oidc_write = isinstance(perms, dict) and perms.get('id-token') == 'write'

        # Azure action patterns
        azure_actions = ['azure/login', 'azure/cli@']
        has_azure_action = any(
            any(azure in s.get('uses', '') for azure in azure_actions)
            for s in steps
        )

        # Check for long-lived credentials (service principal)
        env_vars = job_config.get('env', {}) or {}
        if isinstance(env_vars, list):
            env_vars_dict = {}
            for item in env_vars:
                if isinstance(item, dict) and 'name' in item and 'value' in item:
                    env_vars_dict[item['name']] = item['value']
            env_vars = env_vars_dict

        azure_secrets = ['AZURE_SP_CLIENT_SECRET', 'AZURE_CREDENTIALS', 'ARM_CLIENT_SECRET']
        has_azure_secrets = any(secret in str(env_vars) for secret in azure_secrets)

        if has_oidc_write and not has_azure_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_AZURE_SETUP',
                'location': f'{job_name}',
                'description': 'OIDC id-token: write permission set but no Azure action detected.',
                'recommendation': 'Configure azure/login with use_oidc: true'
            })

        if has_azure_secrets and not has_oidc_write:
        for s in steps
        )

        # Check for long-lived credentials (service principal)
        env_vars = job_config.get('env', {}) or {}
        if isinstance(env_vars, list):
            env_vars_dict = {}
            for item in env_vars:
                if isinstance(item, dict) and 'name' in item and 'value' in item:
                    env_vars_dict[item['name']] = item['value']
            env_vars = env_vars_dict

        azure_secrets = ['AZURE_SP_CLIENT_SECRET', 'AZURE_CREDENTIALS', 'ARM_CLIENT_SECRET']
        has_azure_secrets = any(secret in str(env_vars) for secret in azure_secrets)

        if has_oidc_write and not has_azure_action:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'OIDC_WITHOUT_AZURE_SETUP',
                'location': f'{job_name}',
                'description': 'OIDC id-token: write permission set but no Azure action detected.',
                'recommendation': 'Configure azure/login with use_oidc: true'
            })

        if has_azure_secrets and not has_oidc_write:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'LONG_LIVED_AZURE_CREDENTIALS',
                'location': f'{job_name}',
                'description': 'Workflow uses long-lived Azure service principal credentials.',
                'recommendation': 'Use federated identity credential with azure/login via OIDC',
                'before_after': {
                    'long_lived': '''env:
  AZURE_CREDENTIALS: ${{ secrets.AZURE_CREDENTIALS }}''',
                    'oidc': '''permissions:
  id-token: write
  contents: read

steps:
  - name: Login to Azure via OIDC
    uses: azure/login@v1
    with:
      client-id: ${{ vars.AZURE_CLIENT_ID }}
      tenant-id: ${{ vars.AZURE_TENANT_ID }}
      use_oidc: true'''
                }
            })

    return findings

def check_docker_image_security(workflow_content):
    """Check Docker container security in jobs."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        container = job_config.get('container', {}) or {}
        if not container:
            continue

        image = container.get('image', '') or ''
        options = container.get('options', '') or ''

        # Check unpinned images (no tag or SHA)
        if ':' not in image and '@' not in image:
            findings.append({
                'severity': 'HIGH',
                'type': 'UNPINNED_DOCKER_IMAGE',
                'location': f'{job_name} container',
                'description': f'Docker image unpinned: {image}. Image may change between runs.',
                'recommendation': 'Pin to specific version tag or SHA digest for reproducibility'
            })

        # Check :latest tag
        if image.endswith(':latest'):
            findings.append({
                'severity': 'MEDIUM',
                'type': 'DOCKER_IMAGE_LATEST_TAG',
                'location': f'{job_name} container',
                'description': f'Docker uses :latest tag: {image}. This may cause inconsistent builds.',
                'recommendation': 'Pin to specific version tag or SHA digest'
            })

        # Check for privileged mode
        if '--privileged' in options:
            findings.append({
                'severity': 'HIGH',
                'type': 'DOCKER_ROOT_PRIVILEGES',
                'location': f'{job_name} container',
                'description': 'Container runs with --privileged flag, granting full host access.',
                'recommendation': 'Remove --privileged and use specific capabilities if needed (e.g., --cap-add=SYS_ADMIN)',
                'secure_example': '''options: "--cap-add=NET_ADMIN --cap-add=SYS_PTRACE"'''
            })

        # Check for root user (user not specified in options)
        if '--user' not in options and '-u' not in options:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'DOCKER_ROOT_USER',
                'location': f'{job_name} container',
                'description': 'Container may run as root user. This increases security risks.',
                'recommendation': 'Add --user flag or options: "user: 1000" to run as non-root'
            })

    return findings

def check_reusable_workflows(workflow_content):
    """Check reusable workflows and their pinning status."""
    findings = []

    jobs = workflow_content.get('jobs', {})
    for job_name, job_config in jobs.items():
        if 'uses' in job_config:
            uses = job_config['uses'] or ''
            # Check for reusable workflow pattern (.github/workflows/*.yml)
            if '/.github/workflows/' in uses or '.github/actions/' in uses:
                # Check if pinned to SHA (most secure)
                if '@' not in uses:
                    findings.append({
                        'severity': 'HIGH',
                        'type': 'UNPINNED_REUSEABLE_WORKFLOW',
                        'location': f'{job_name}',
                        'description': f'Reusable workflow unpinned: {uses}. May be vulnerable to supply chain attacks.',
                        'recommendation': 'Pin reusable workflows to specific commit SHA'
                    })

    return findings

def check_dependabot_config(repo_path='.'):
    """Check for dependabot configuration."""
    findings = []

    dependabot_path = Path(repo_path) / '.github' / 'dependabot.yml'
    if not dependabot_path.exists():
        # Also check for dependabot.yaml (alternative extension)
        if not (Path(repo_path) / '.github' / 'dependabot.yaml').exists():
            findings.append({
                'severity': 'LOW',
                'type': 'NO_DEPENDABOT_CONFIG',
                'location': '.github/dependabot.yml',
                'description': 'No Dependabot configuration found. Dependency updates are not automated.',
                'recommendation': 'Create .github/dependabot.yml with version updates and auto-merge enabled'
            })

    return findings

def check_dependabot_auto_merge(repo_path='.'):
    """Check if dependabot has auto-merge configured."""
    findings = []

    dependabot_path = Path(repo_path) / '.github' / 'dependabot.yml'
    if not dependabot_path.exists():
        return []

    try:
        with open(dependabot_path, 'r') as f:
            config = yaml.safe_load(f) or {}

        # Check for auto-merge configuration
        updates = config.get('updates', [])
        has_auto_merge = False
        for update in updates:
            if isinstance(update, dict):
                if update.get('open-pull-requests-limit', 0) > 0:
                    has_auto_merge = True
                    break

        # This is a soft check - we flag if auto-merge could be improved
        findings.append({
            'severity': 'LOW',
            'type': 'DEPENDABOT_AUTO_MERGE_RECOMMENDED',
            'location': '.github/dependabot.yml',
            'description': 'Dependabot configured. Consider enabling auto-merge for faster security updates.',
            'recommendation': 'Add auto_update: true to enable automatic dependency updates'
        })

    except Exception as e:
        findings.append({
            'severity': 'LOW',
            'type': 'DEPENDABOT_CONFIG_ERROR',
            'location': '.github/dependabot.yml',
            'description': f'Error reading Dependabot config: {str(e)}',
            'recommendation': 'Verify YAML syntax and structure'
        })

    return findings

def check_matrix_strategy(workflow_content):
    """Check for matrix strategy usage and opportunities."""
    findings = []
    jobs = workflow_content.get('jobs', {})

    for job_name, job_config in jobs.items():
        # Skip deployment jobs (usually single target)
        if 'deploy' in job_name.lower() or 'release' in job_name.lower():
            continue

        strategy = job_config.get('strategy', {}) or {}
        has_matrix = isinstance(strategy, dict) and 'matrix' in strategy

        if not has_matrix:
            # Check if this is a test/build job that could benefit from matrix
            runs_on = job_config.get('runs-on', '') or ''
            steps = job_config.get('steps', []) or []

            # If it looks like a build/test job, suggest matrix strategy
            finding_types = ['build', 'test', 'lint', 'check']
            if any(ft in job_name.lower() for ft in finding_types):
                findings.append({
                    'severity': 'LOW',
                    'type': 'NO_MATRIX_STRATEGY',
                    'location': f'{job_name}',
                    'description': 'Job could benefit from matrix strategy for parallel execution.',
                    'recommendation': 'Add matrix strategy to run tests across multiple OS/node versions in parallel'
                })

    return findings


def generate_fix_suggestions(findings):
    """Generate detailed fix suggestions based on detected issues."""

    fix_sections = []

    # Check what types of findings we have
    finding_types = [f['type'] for f in findings]

    has_write_all = 'WRITE_ALL_PERMISSIONS' in finding_types
    has_unpinned_branch = 'UNPINNED_BRANCH_REFERENCE' in finding_types or 'UNPINNED_REUSEABLE_WORKFLOW' in finding_types
    has_oidc_issues = any(x in finding_types for x in ['LONG_LIVED_AWS_CREDENTIALS', 'LONG_LIVED_GCP_CREDENTIALS', 'LONG_LIVED_AZURE_CREDENTIALS'])
    has_major_version = 'MAJOR_VERSION_ONLY' in finding_types

    # Section 1: Least Privilege Permissions
    if has_write_all or True:  # Always show as educational
        fix_sections.append({
            'title': '1. Apply Least Privilege Permissions',
            'applies_to': ['WRITE_ALL_PERMISSIONS'],
            'content': '''
**Problem:** Using `permissions: write-all` grants excessive permissions, violating the principle of least privilege.

**Solution:** Specify only the exact permissions your workflow needs.
'''
        })

    # Section 2: Pin Actions to Commit SHA
    if has_unpinned_branch or has_major_version or True:
        fix_sections.append({
            'title': '2. Pin Actions to Specific Versions',
            'applies_to': ['UNPINNED_BRANCH_REFERENCE', 'MAJOR_VERSION_ONLY', 'UNPINNED_REUSEABLE_WORKFLOW'],
            'content': '''
**Problem:** Using mutable references like `@main` or major versions only (`@v4`) makes workflows vulnerable to supply chain attacks and unpredictable changes.

**Solution:** Pin actions to specific commit SHAs for maximum security, or at minimum use full version tags.
'''
        })

    # Section 3: OIDC Authentication (Multi-Cloud)
    if has_oidc_issues or True:
        fix_sections.append({
            'title': '3. Use OIDC Federation Instead of Long-Lived Credentials',
            'applies_to': ['LONG_LIVED_AWS_CREDENTIALS', 'LONG_LIVED_GCP_CREDENTIALS', 'LONG_LIVED_AZURE_CREDENTIALS'],
            'content': '''
**Problem:** Storing and using long-lived credentials (AWS keys, GCP service account JSON, Azure service principals) creates security risks if leaked and requires rotation management.

**Solution:** Use OIDC federation to obtain temporary credentials dynamically.
'''
        })

    # Section 4: Approval Gates for Production
    fix_sections.append({
        'title': '4. Add Approval Gates for Production Deployments',
        'applies_to': ['AUTO_DEPLOY_TO_MAIN'],
        'content': '''
**Problem:** Automatic deployments to production without approval can propagate bugs or malicious code instantly.

**Solution:** Use GitHub Environment protection rules to require manual approval before production deployments.
'''
    })

    # Section 5: Dependency Caching
    fix_sections.append({
        'title': '5. Implement Dependency Caching',
        'applies_to': ['NO_DEPENDENCY_CACHING'],
        'content': '''
**Problem:** Installing dependencies without caching increases build times and costs.

**Solution:** Use built-in caching features or actions/cache to store dependency artifacts between runs.
'''
    })

    # Section 6: Matrix Strategy for Parallelization
    fix_sections.append({
        'title': '6. Use Matrix Strategy for Test Parallelization',
        'applies_to': ['NO_MATRIX_STRATEGY'],
        'content': '''
**Problem:** Running tests sequentially across different platforms/versions wastes time and resources.

**Solution:** Use matrix strategy to run multiple test configurations in parallel jobs.
'''
    })

    # Section 7: Dependabot Configuration
    fix_sections.append({
        'title': '7. Configure Dependabot for Automated Dependency Updates',
        'applies_to': ['NO_DEPENDABOT_CONFIG'],
        'content': '''
**Problem:** Manually updating dependencies is error-prone and slows down security patching.

**Solution:** Enable Dependabot to automatically create PRs for dependency updates, with auto-merge for non-breaking changes.
'''
    })

    return fix_sections


def generate_report(findings, workflow_name):
    """Generate a formatted audit report."""

    # Severity badge mapping
    severity_badges = {
        'CRITICAL': '🔴',
        'HIGH': '🟡',
        'MEDIUM': '🔵',
        'LOW': '🟢'
    }

    # Count by severity
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for f in findings:
        severity_counts[f['severity']] = severity_counts.get(f['severity'], 0) + 1

    # Generate report header
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append(f"🔍 CI/CD Pipeline Audit Report")
    report_lines.append(f"   Workflow: {workflow_name}")
    report_lines.append(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 80)
    report_lines.append("")

    # Executive summary with severity breakdown
    report_lines.append("## 📊 EXECUTIVE SUMMARY")
    report_lines.append("")
    report_lines.append(f"├─ 🔴 CRITICAL: {severity_counts['CRITICAL']} (requires immediate attention)")
    report_lines.append(f"├─ 🟡 HIGH: {severity_counts['HIGH']} (should be addressed soon)")
    report_lines.append(f"├─ 🔵 MEDIUM: {severity_counts['MEDIUM']} (plan to fix this sprint)")
    report_lines.append(f"└─ 🟢 LOW: {severity_counts['LOW']} (address when convenient)")
    report_lines.append("")

    # Total score calculation
    total_findings = len(findings)
    if total_findings == 0:
        risk_score = "✅ EXCELLENT - No security issues found!"
    elif severity_counts['CRITICAL'] > 0:
        risk_score = "🔴 HIGH RISK - Critical vulnerabilities require immediate attention"
    elif severity_counts['HIGH'] > 2:
        risk_score = "🟡 ELEVATED RISK - Multiple high-severity issues present"
    else:
        risk_score = "🔵 MODERATE RISK - Some improvements recommended"

    report_lines.append(f"**Overall Risk Assessment:** {risk_score}")
    report_lines.append("")

    # Detailed findings table
    if findings:
        report_lines.append("## 🔍 DETAILED FINDINGS")
        report_lines.append("")
        report_lines.append("| Severity | Issue Type | Location | Description |")
        report_lines.append("|----------|------------|----------|-------------|")

        for f in sorted(findings, key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x['severity'])):
            badge = severity_badges.get(f['severity'], '')
            desc_short = f['description'][:50] + "..." if len(f['description']) > 50 else f['description']
            report_lines.append(f"| {badge} {f['severity']} | `{f['type']}` | {f['location']} | {desc_short} |")

        report_lines.append("")

        # Detailed findings with recommendations
        report_lines.append("## 💡 DETAILED FINDINGS WITH FIXES")
        report_lines.append("")

        for f in sorted(findings, key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x['severity'])):
            badge = severity_badges.get(f['severity'], '')
            report_lines.append(f"### {badge} {f['severity']}: {f['type']}")
            report_lines.append("")
            report_lines.append(f"**Location:** {f['location']}")
            report_lines.append("")
            report_lines.append(f"**Description:** {f['description']}")
            report_lines.append("")
            report_lines.append(f"**Recommendation:** {f['recommendation']}")

            # Add specific fix example if available
            if 'secure_example' in f:
                report_lines.append("")
                report_lines.append("**Secure Example:**")
                report_lines.append("```yaml")
                report_lines.append(f"{f['secure_example']}")
                report_lines.append("```")

            if 'before_after' in f and isinstance(f['before_after'], dict):
                report_lines.append("")
                report_lines.append("**Before/After Comparison:**")
                report_lines.append("")
                report_lines.append("**BEFORE (insecure):**")
                report_lines.append("```yaml")
                for line in f['before_after']['long_lived'].split('\n'):
                    report_lines.append(line)
                report_lines.append("```")

                if 'oidc' in f['before_after']:
                    report_lines.append("")
                    report_lines.append("**AFTER (secure - using OIDC):**")
                    report_lines.append("```yaml")
                    for line in f['before_after']['oidc'].split('\n'):
                        report_lines.append(line)
                    report_lines.append("```")

            report_lines.append("---")
            report_lines.append("")

    # Fix suggestions section
    fix_sections = generate_fix_suggestions(findings)
    if fix_sections:
        report_lines.append("## 🛠️ RECOMMENDED FIXES")
        report_lines.append("")

        for i, section in enumerate(fix_sections, 1):
            report_lines.append(f"### {section['title']}")
            report_lines.append("")
            report_lines.append(section['content'])

            # Add YAML examples based on fix type
            if section['title'].startswith('2. Pin Actions'):
                report_lines.append("**Example - Before:**")
                report_lines.append("```yaml")
                report_lines.append("  uses: actions/checkout@main")
                report_lines.append("  uses: actions/setup-node@v4")
                report_lines.append("```")

                report_lines.append("")
                report_lines.append("**Example - After:**")
                report_lines.append("```yaml")
                report_lines.append("  uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1")
                report_lines.append("  uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1")
                report_lines.append("```")

            if section['title'].startswith('3. Use OIDC'):
                report_lines.append("**AWS Example - Before (long-lived credentials):**")
                report_lines.append("```yaml")
                report_lines.append("env:")
                report_lines.append("  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}")
                report_lines.append("  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}")
                report_lines.append("steps:")
                report_lines.append("  - uses: aws-actions/configure-aws-credentials@v2")
                report_lines.append("```")

                report_lines.append("")
                report_lines.append("**AWS Example - After (OIDC federation):**")
                report_lines.append("```yaml")
                report_lines.append("permissions:")
                report_lines.append("  id-token: write")
                report_lines.append("  contents: read")
                report_lines.append("steps:")
                report_lines.append("  - name: Configure AWS credentials via OIDC")
                report_lines.append("    uses: aws-actions/configure-aws-credentials@v4")
                report_lines.append("    with:")
                report_lines.append("      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role")
                report_lines.append("      aws-region: us-east-1")
                report_lines.append("```")

            if section['title'].startswith('4. Add Approval'):
                report_lines.append("**Example - Before (auto-deploy):**")
                report_lines.append("```yaml")
                report_lines.append("on:")
                report_lines.append("  push:")
                report_lines.append("    branches: [main]")
                report_lines.append("jobs:")
                report_lines.append("  deploy:")
                report_lines.append("    runs-on: ubuntu-latest")
                report_lines.append("    steps:")
                report_lines.append("      - run: ./deploy.sh")
                report_lines.append("```")

                report_lines.append("")
                report_lines.append("**Example - After (requires approval):**")
                report_lines.append("```yaml")
                report_lines.append("on:")
                report_lines.append("  push:")
                report_lines.append("    branches: [main]")
                report_lines.append("jobs:")
                report_lines.append("  deploy-production:")
                report_lines.append("    runs-on: ubuntu-latest")
                report_lines.append("    environment: production  # Requires approval in repo settings")
                report_lines.append("    steps:")
                report_lines.append("      - run: ./deploy.sh")
                report_lines.append("```")

            if section['title'].startswith('5. Implement Dependency'):
                report_lines.append("**Example - npm caching:**")
                report_lines.append("```yaml")
                report_lines.append("- name: Setup Node.js with cache")
                report_lines.append("  uses: actions/setup-node@v4")
                report_lines.append("  with:")
                report_lines.append("    node-version: '20'")
                report_lines.append("    cache: 'npm'")
                report_lines.append("")
                report_lines.append("- name: Install dependencies (cached)")
                report_lines.append("  run: npm ci")
                report_lines.append("```")

                report_lines.append("")
                report_lines.append("**Example - pip caching:**")
                report_lines.append("```yaml")
                report_lines.append("- name: Cache pip dependencies")
                report_lines.append("  uses: actions/cache@v4")
                report_lines.append("  with:")
                report_lines.append("    path: ~/.cache/pip")
                report_lines.append("    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}")
                report_lines.append("    restore-keys: |")
                report_lines.append("      ${{ runner.os }}-pip-")
                report_lines.append("- name: Install dependencies")
                report_lines.append("  run: pip install -r requirements.txt")
                report_lines.append("```")

            if section['title'].startswith('6. Use Matrix'):
                report_lines.append("**Example - Matrix strategy for parallel tests:**")
                report_lines.append("```yaml")
                report_lines.append("jobs:")
                report_lines.append("  test:")
                report_lines.append("    runs-on: ubuntu-latest")
                report_lines.append("    strategy:")
                report_lines.append("      matrix:")
                report_lines.append("        node-version: [16, 18, 20]")
                report_lines.append("        os: [ubuntu-latest, windows-latest, macos-latest]")
                report_lines.append("        exclude:")
                report_lines.append("          - os: macos-latest")
                report_lines.append("            node-version: 16")
                report_lines.append("      fail-fast: false")
                report_lines.append("")
                report_lines.append("    steps:")
                report_lines.append("      - uses: actions/checkout@v4")
                report_lines.append("      - name: Use Node.js ${{ matrix.node-version }}")
                report_lines.append("        uses: actions/setup-node@v4")
                report_lines.append("        with:")
                report_lines.append("          node-version: ${{ matrix.node-version }}")
                report_lines.append("          cache: 'npm'")
                report_lines.append("      - run: npm ci")
                report_lines.append("      - run: npm test")
                report_lines.append("```")

            if section['title'].startswith('7. Configure Dependabot'):
                report_lines.append("**Example - Full Dependabot configuration with auto-merge:**")
                report_lines.append("```yaml")
                report_lines.append("# .github/dependabot.yml")
                report_lines.append("version: 2")
                report_lines.append("updates:")
                report_lines.append("")
                report_lines.append("  # Enable version updates for npm")
                report_lines.append("  - package-ecosystem: \"npm\"")
                report_lines.append("    directory: \"/\"")
                report_lines.append("    schedule:")
                report_lines.append("      interval: \"weekly\"")
                report_lines.append("    open-pull-requests-limit: 10")
                report_lines.append("    automerged-limits:")
                report_lines.append("      minor-versions: true")
                report_lines.append("    labels:")
                report_lines.append("      - dependencies")
                report_lines.append("      - npm")
                report_lines.append("")
                report_lines.append("  # Enable version updates for GitHub Actions")
                report_lines.append("  - package-ecosystem: \"github-actions\"")
                report_lines.append("    directory: \"/\"")
                report_lines.append("    schedule:")
                report_lines.append("      interval: \"weekly\"")
                report_lines.append("    labels:")
                report_lines.append("      - dependencies")
                report_lines.append("      - github-actions")
                report_lines.append("```")

                report_lines.append("")
                report_lines.append("**Benefits of auto-merge:**")
                report_lines.append("- Security patches applied automatically when CI passes")
                report_lines.append("- Reduces technical debt from outdated dependencies")
                report_lines.append("- Faster response to newly discovered vulnerabilities")
                report_lines.append("- Configure branch protection rules to require reviews for major version updates")

            report_lines.append("")

    # Action items prioritized by urgency
    report_lines.append("## ✅ ACTION ITEMS (Prioritized)")
    report_lines.append("")

    action_items = []
    if severity_counts['CRITICAL'] > 0:
        action_items.append({
            'priority': 1,
            'urgency': '🔴 IMMEDIATE (< 1 hour)',
            'items': [f for f in findings if f['severity'] == 'CRITICAL']
        })

    if severity_counts['HIGH'] > 0:
        action_items.append({
            'priority': 2,
            'urgency': '🟡 SOON (< 24 hours)',
            'items': [f for f in findings if f['severity'] == 'HIGH']
        })

    if severity_counts['MEDIUM'] > 0:
        action_items.append({
            'priority': 3,
            'urgency': '🔵 THIS SPRINT (< 1 week)',
            'items': [f for f in findings if f['severity'] == 'MEDIUM']
        })

    if severity_counts['LOW'] > 0:
        action_items.append({
            'priority': 4,
            'urgency': '🟢 BACKLOG (< 1 month)',
            'items': [f for f in findings if f['severity'] == 'LOW']
        })

    for item_group in action_items:
        report_lines.append(f"### {item_group['urgency']}")
        report_lines.append("")
        for i, finding in enumerate(item_group['items'], 1):
            badge = severity_badges.get(finding['severity'], '')
            report_lines.append(f"{i}. [{badge} {finding['type']}]({finding['location']}) - {finding['recommendation']}")
        report_lines.append("")

    # Best practices checklist
    report_lines.append("## 📋 SECURITY BEST PRACTICES CHECKLIST")
    report_lines.append("")
    report_lines.append("- [ ] No secrets exposed in logs or workflow files")
    report_lines.append("- [ ] All actions pinned to commit SHAs or specific tags")
    report_lines.append("- [ ] Least-privilege permissions applied to all workflows")
    report_lines.append("- [ ] OIDC used instead of long-lived credentials for cloud providers (AWS/GCP/Azure)")
    report_lines.append("- [ ] Environment protection rules configured for production deployments")
    report_lines.append("- [ ] Required reviews enforced before deployment via repository settings")
    report_lines.append("- [ ] Dependency caching implemented in build jobs (npm, pip, maven)")
    report_lines.append("- [ ] Matrix strategy used for parallel test execution across OS/node versions")
    report_lines.append("- [ ] Docker images pinned to version tags or SHA digests")
    report_lines.append("- [ ] No containers running with root privileges or as root user")
    report_lines.append("- [ ] Reusable workflows pinned to specific versions")
    report_lines.append("- [ ] Dependabot configured with auto-merge enabled")
    report_lines.append("")

    # Summary footer
    report_lines.append("=" * 80)
    report_lines.append("📌 For more details on security best practices, see the SKILL.md documentation.")
    report_lines.append(f"   Total findings: {total_findings} | Risk level: {risk_score}")
    report_lines.append("=" * 80)

    return '\n'.join(report_lines)


def audit_workflow(workflow_path, repo_path='.'):
    """Main function to audit a single workflow file."""
    try:
        with open(workflow_path, 'r') as f:
            content = yaml.safe_load(f)

        if not content or not isinstance(content, dict):
            return None, "Invalid YAML format"

        findings = []

        # Run all security checks
        findings.extend(check_secrets_in_run_commands(content))
        findings.extend(check_permissions(content))
        findings.extend(check_action_pinning(content))
        findings.extend(check_aws_oidc_config(content))
        findings.extend(check_gcp_oidc_config(content))
        findings.extend(check_azure_oidc_config(content))
        findings.extend(check_docker_image_security(content))
        findings.extend(check_reusable_workflows(content))

        # Repository-level checks (only run once per repo)
        if workflow_path.name == list(Path(repo_path).rglob('.github/workflows/*.yml'))[0].name:
            findings.extend(check_dependabot_config(repo_path))
            findings.extend(check_matrix_strategy(content))

    except Exception as e:
        return None, f"Error reading {workflow_path}: {str(e)}"

    return content, findings


def main():
    """Run audit on all workflows in test-workflows directory."""
    repo_path = Path('test-workflows')
    workflows_dir = repo_path / '.github' / 'workflows'

    if not workflows_dir.exists():
        print(f"Error: {workflows_dir} does not exist")
        return

    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))

    all_findings = {}

    for wf_path in workflow_files:
        content, result = audit_workflow(wf_path, repo_path)
        if isinstance(result, list):
            all_findings[wf_path.name] = result

    # Generate combined report
    print(generate_report(
        sum(all_findings.values(), []),
        "All Workflows (Combined)"
    ))


if __name__ == '__main__':
    main()

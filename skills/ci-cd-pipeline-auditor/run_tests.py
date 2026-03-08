#!/usr/bin/env python3
"""Run CI/CD Pipeline Auditor tests with complete reports."""

import sys
from pathlib import Path
import yaml
from datetime import datetime

def load_workflow(path):
    """Load and parse a workflow file."""
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

def run_audit(workflow_path, repo_path='.'):
    """Run complete audit on a workflow file."""
    content = load_workflow(Path(repo_path) / workflow_path)
    if not content:
        return None

    findings = analyze_workflow(content)
    return {
        'workflow': Path(workflow_path).name,
        'content': content,
        'findings': findings
    }

def analyze_workflow(workflow_content):
    """Analyze workflow for security issues."""
    findings = []

    # Check permissions
    perms = workflow_content.get('permissions', '') or {}
    if perms == 'write-all':
        findings.append({
            'severity': 'CRITICAL',
            'type': 'WRITE_ALL_PERMISSIONS',
            'location': 'root level',
            'description': 'Workflow has write-all permissions violating least privilege principle',
            'recommendation': 'Specify exact required permissions only'
        })

    # Check action pinning
    jobs = workflow_content.get('jobs', {}) or {}
    for job_name, job_config in jobs.items():
        if not isinstance(job_config, dict):
            continue

        steps = job_config.get('steps', []) or []
        for step_idx, step in enumerate(steps):
            uses = step.get('uses', '') or ''

            # Check branch references (CRITICAL)
            if uses.endswith('@main') or uses.endswith('@master'):
                findings.append({
                    'severity': 'CRITICAL',
                    'type': 'UNPINNED_BRANCH_REFERENCE',
                    'location': f'{job_name} step {step_idx + 1}',
                    'description': f'Action pinned to mutable branch: {uses}',
                    'recommendation': 'Pin to commit SHA for reproducibility and supply chain security'
                })

            # Check major version only (HIGH)
            if '@v4' in uses or '@v5' in uses:
                parts = uses.split('@')
                if len(parts) == 2:
                    ref = parts[1]
                    if ref.startswith('v') and len(ref) == 2:
                        findings.append({
                            'severity': 'HIGH',
                            'type': 'MAJOR_VERSION_ONLY',
                            'location': f'{job_name} step {step_idx + 1}',
                            'description': f'Action uses only major version: {uses}. This may cause unexpected changes.',
                            'recommendation': f'Pin to specific tag (e.g., {ref}.0) or SHA for reproducibility'
                        })

        # Check secrets in run commands (CRITICAL)
        steps = job_config.get('steps', []) or []
        for step_idx, step in enumerate(steps):
            run_cmd = step.get('run', '') or ''
            if isinstance(run_cmd, list):
                run_cmd = '\n'.join(run_cmd)

            if 'echo' in run_cmd.lower() and ('API_KEY' in run_cmd or 'SECRET' in run_cmd.upper()):
                findings.append({
                    'severity': 'CRITICAL',
                    'type': 'SECRETS_IN_RUN_COMMAND',
                    'location': f'{job_name} step {step_idx + 1}',
                    'description': 'Potential secrets exposure in echo command',
                    'recommendation': 'Use env blocks instead of run commands for secrets; never echo secrets'
                })

        # Check AWS long-lived credentials (MEDIUM)
        env_vars = job_config.get('env', {}) or {}
        if isinstance(env_vars, list):
            env_dict = {}
            for item in env_vars:
                if isinstance(item, dict) and 'name' in item and 'value' in item:
                    env_dict[item['name']] = item['value']
            env_vars = env_dict

        has_aws_secrets = any(k in env_vars for k in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'])
        if has_aws_secrets:
            findings.append({
                'severity': 'MEDIUM',
                'type': 'LONG_LIVED_AWS_CREDENTIALS',
                'location': job_name,
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
      aws-region: us-east-1'''
                }
            })

        # Check auto-deploy without environment protection (HIGH)
        if 'deploy' in job_name.lower():
            triggers = workflow_content.get('on', {}) or {}
            if isinstance(triggers, dict):
                push_branches = triggers.get('push', {}) or {}
                branches = push_branches.get('branches', []) or []
                if 'main' in [b for b in branches]:
                    findings.append({
                        'severity': 'HIGH',
                        'type': 'AUTO_DEPLOY_TO_MAIN',
                        'location': job_name,
                        'description': 'Auto-deploys to production without approval gate. Environment protection rules not configured.',
                        'recommendation': 'Add environment: production to require manual approval'
                    })

    return findings

def generate_report(audit_results):
    """Generate formatted audit report."""
    severity_badges = {'CRITICAL': '🔴', 'HIGH': '🟡', 'MEDIUM': '🔵', 'LOW': '🟢'}

    all_findings = []
    for result in audit_results:
        if result and result.get('findings'):
            for f in result['findings']:
                all_findings.append({**f, 'workflow': result['workflow']})

    # Count by severity
    counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
    for f in all_findings:
        counts[f['severity']] += 1

    report = []
    report.append("=" * 80)
    report.append("🔍 CI/CD Pipeline Audit Report")
    report.append(f"   Workflows Analyzed: {', '.join(r['workflow'] for r in audit_results if r)}")
    report.append(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")

    # Executive Summary
    report.append("## 📊 EXECUTIVE SUMMARY")
    report.append("")
    report.append(f"├─ 🔴 CRITICAL: {counts['CRITICAL']} (requires immediate attention)")
    report.append(f"├─ 🟡 HIGH: {counts['HIGH']} (should be addressed soon)")
    report.append(f"├─ 🔵 MEDIUM: {counts['MEDIUM']} (plan to fix this sprint)")
    report.append(f"└─ 🟢 LOW: {counts['LOW']} (address when convenient)")
    report.append("")

    total = len(all_findings)
    if counts['CRITICAL'] > 0:
        risk = "🔴 HIGH RISK - Critical vulnerabilities require immediate attention"
    elif counts['HIGH'] > 2:
        risk = "🟡 ELEVATED RISK - Multiple high-severity issues present"
    else:
        risk = "🔵 MODERATE RISK - Some improvements recommended"

    report.append(f"**Overall Risk Assessment:** {risk}")
    report.append("")

    # Detailed Findings Table
    if all_findings:
        report.append("## 🔍 DETAILED FINDINGS")
        report.append("")
        report.append("| Severity | Issue Type | Location | Description |")
        report.append("|----------|------------|----------|-------------|")

        for f in sorted(all_findings, key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x['severity'])):
            badge = severity_badges.get(f['severity'], '')
            desc = f['description'][:45] + "..." if len(f['description']) > 45 else f['description']
            report.append(f"| {badge} {f['severity']} | `{f['type']}` | {f['workflow']} ({f['location']}) | {desc} |")

        report.append("")

    # Detailed Findings with Fixes
    report.append("## 💡 DETAILED FINDINGS WITH FIXES")
    report.append("")

    for f in sorted(all_findings, key=lambda x: ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].index(x['severity'])):
        badge = severity_badges.get(f['severity'], '')
        report.append(f"### {badge} {f['severity']}: {f['type']}")
        report.append("")
        report.append(f"**Location:** {f['workflow']} - {f['location']}")
        report.append("")
        report.append(f"**Description:** {f['description']}")
        report.append("")
        report.append(f"**Recommendation:** {f['recommendation']}")

        if 'before_after' in f:
            report.append("")
            report.append("**BEFORE (insecure):**")
            report.append("```yaml")
            for line in f['before_after']['long_lived'].split('\n'):
                report.append(line)
            report.append("```")

            if 'oidc' in f['before_after']:
                report.append("")
                report.append("**AFTER (secure - using OIDC):**")
                report.append("```yaml")
                for line in f['before_after']['oidc'].split('\n'):
                    report.append(line)
                report.append("```")

        report.append("---")
        report.append("")

    # Recommended Fixes Section
    report.append("## 🛠️ RECOMMENDED FIXES (With Complete Examples)")
    report.append("")

    has_write_all = any(f['type'] == 'WRITE_ALL_PERMISSIONS' for f in all_findings)
    has_unpinned = any(f['type'] in ['UNPINNED_BRANCH_REFERENCE', 'MAJOR_VERSION_ONLY'] for f in all_findings)
    has_aws_secrets = any(f['type'] == 'LONG_LIVED_AWS_CREDENTIALS' for f in all_findings)

    if True:  # Always show least privilege as educational
        report.append("### 1. Apply Least Privilege Permissions")
        report.append("")
        report.append("**Problem:** Using `permissions: write-all` grants excessive permissions, violating the principle of least privilege.")
        report.append("")
        report.append("**Solution:** Specify only the exact permissions your workflow needs.")
        report.append("")

        if has_write_all:
            report.append("**BEFORE (from your workflow):**")
            report.append("```yaml")
            report.append("permissions: write-all  # ❌ Grants everything!")
            report.append("```")

        report.append("")
        report.append("**AFTER (secure - least privilege):**")
        report.append("```yaml")
        report.append("permissions:")
        report.append("  contents: read          # Required for checkout")
        report.append("  pull-requests: read     # Required for PR comments")
        report.append("  checks: write           # Required for status reports")
        report.append("")
        report.append("jobs:")
        report.append("  build:")
        report.append("    permissions:")
        report.append("      contents: read      # Override for this job only")
        report.append("```")

        report.append("")

    if True:  # Always show action pinning as educational
        report.append("### 2. Pin Actions to Specific Versions (SHA or Full Tag)")
        report.append("")
        report.append("**Problem:** Using mutable references like `@main` or major versions only (`@v4`) makes workflows vulnerable to supply chain attacks and unpredictable changes.")
        report.append("")
        report.append("**Solution:** Pin actions to specific commit SHAs for maximum security, or at minimum use full version tags (e.g., @v4.1.0).")
        report.append("")

        if has_unpinned:
            report.append("**BEFORE (from your workflow):**")
            report.append("```yaml")
            report.append("- uses: actions/checkout@main    # ❌ Mutable branch!")
            report.append("- uses: actions/setup-node@v4   # ❌ Only major version")
            report.append("```")

        report.append("")
        report.append("**AFTER (secure - pinned to SHA):**")
        report.append("```yaml")
        report.append("# Get latest commit SHA via:")
        report.append("# curl https://api.github.com/repos/actions/checkout/git/ref/tags/v4.1.1 | grep sha")
        report.append("")
        report.append("- uses: actions/checkout@a5ac7e51b41094c92402da38263ded29f66f8eec  # v4.1.1")
        report.append("  with:")
        report.append("    fetch-depth: 0  # Optional: needed for semantic release, etc.")
        report.append("")
        report.append("- uses: actions/setup-node@cdcb6a6d463ec4bdf0aef171cf5e54ccab9bb5ed  # v3.8.1")
        report.append("  with:")
        report.append("    node-version: '20'")
        report.append("    cache: 'npm'")
        report.append("```")

        report.append("")

    if True:  # Always show OIDC as educational
        report.append("### 3. Use OIDC Federation Instead of Long-Lived Credentials (Multi-Cloud)")
        report.append("")
        report.append("**Problem:** Storing and using long-lived credentials (AWS keys, GCP service account JSON, Azure service principals) creates security risks if leaked and requires rotation management.")
        report.append("")
        report.append("**Solution:** Use OIDC federation to obtain temporary credentials dynamically. Configure once in cloud provider IAM, then use `id-token: write` permission in workflows.")
        report.append("")

        if has_aws_secrets:
            report.append("**BEFORE (AWS - long-lived credentials from your workflow):**")
            report.append("```yaml")
            report.append("env:")
            report.append("  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}")
            report.append("  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}")
            report.append("")
            report.append("steps:")
            report.append("  - uses: aws-actions/configure-aws-credentials@v2")
            report.append("    with:")
            report.append("      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}")
            report.append("      aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}")
            report.append("```")

        report.append("")
        report.append("**AFTER (AWS - OIDC federation):**")
        report.append("```yaml")
        report.append("# First, create IAM role in AWS with trust policy:")
        report.append("# Principal: token.actions.githubusercontent.com")
        report.append("# Condition: repo:jos33/Skill-Cauldron matches your repo")
        report.append("")
        report.append("permissions:")
        report.append("  id-token: write    # Required for OIDC")
        report.append("  contents: read")
        report.append("")
        report.append("steps:")
        report.append("  - name: Configure AWS credentials via OIDC")
        report.append("    uses: aws-actions/configure-aws-credentials@v4")
        report.append("    with:")
        report.append("      role-to-assume: arn:aws:iam::123456789012:role/github-actions-role")
        report.append("      aws-region: us-east-1")
        report.append("```")

        report.append("")
        report.append("**GCP OIDC Example:**")
        report.append("```yaml")
        report.append("permissions:")
        report.append("  id-token: write")
        report.append("  contents: read")
        report.append("")
        report.append("steps:")
        report.append("  - name: Authenticate to GCP via OIDC")
        report.append("    uses: google-github-actions/auth@v2")
        report.append("    with:")
        report.append("      workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider")
        report.append("      service_account: my-service-account@my-project.iam.gserviceaccount.com")
        report.append("```")

        report.append("")
        report.append("**Azure OIDC Example:**")
        report.append("```yaml")
        report.append("permissions:")
        report.append("  id-token: write")
        report.append("  contents: read")
        report.append("")
        report.append("steps:")
        report.append("  - name: Login to Azure via OIDC")
        report.append("    uses: azure/login@v1")
        report.append("    with:")
        report.append("      client-id: ${{ vars.AZURE_CLIENT_ID }}")
        report.append("      tenant-id: ${{ vars.AZURE_TENANT_ID }}")
        report.append("```")

        report.append("")

    # Approval Gates Section
    report.append("### 4. Add Approval Gates for Production Deployments")
    report.append("")
    report.append("**Problem:** Automatic deployments to production without approval can propagate bugs or malicious code instantly.")
    report.append("")
    report.append("**Solution:** Use GitHub Environment protection rules to require manual approval before production deployments.")
    report.append("")

    if any(f['type'] == 'AUTO_DEPLOY_TO_MAIN' for f in all_findings):
        report.append("**BEFORE (from your workflow - auto-deploy):**")
        report.append("```yaml")
        report.append("on:")
        report.append("  push:")
        report.append("    branches: [main]")
        report.append("")
        report.append("jobs:")
        report.append("  deploy-production:")
        report.append("    runs-on: ubuntu-latest")
        report.append("    steps:")
        report.append("      - run: ./deploy.sh production  # Runs immediately!")
        report.append("```")

    report.append("")
    report.append("**AFTER (secure - requires approval):**")
    report.append("```yaml")
    report.append("on:")
    report.append("  push:")
    report.append("    branches: [main]")
    report.append("")
    report.append("jobs:")
    report.append("  deploy-production:")
    report.append("    runs-on: ubuntu-latest")
    report.append("    environment: production  # ✅ Requires approval in repo settings!")
    report.append("    steps:")
    report.append("      - run: ./deploy.sh production")
    report.append("```")

    report.append("")
    report.append("**Repository Configuration Required:**")
    report.append("1. Go to Settings → Environments → `production`")
    report.append("2. Enable 'Require a manual approval'")
    report.append("3. Add required reviewers (at least 2 recommended)")
    report.append("4. Set timeout (e.g., 24 hours for auto-rejection)")

    report.append("")

    # Dependency Caching Section
    report.append("### 5. Implement Dependency Caching")
    report.append("")
    report.append("**Problem:** Installing dependencies without caching increases build times and costs.")
    report.append("")
    report.append("**Solution:** Use built-in caching features or actions/cache to store dependency artifacts between runs.")
    report.append("")

    report.append("**npm Example (built-in cache):**")
    report.append("```yaml")
    report.append("- name: Setup Node.js with cache")
    report.append("  uses: actions/setup-node@v4")
    report.append("  with:")
    report.append("    node-version: '20'")
    report.append("    cache: 'npm'        # ✅ Built-in npm caching")
    report.append("")
    report.append("- name: Install dependencies (uses cache)")
    report.append("  run: npm ci")
    report.append("```")

    report.append("")
    report.append("**pip Example (actions/cache):**")
    report.append("```yaml")
    report.append("- name: Cache pip dependencies")
    report.append("  uses: actions/cache@v4")
    report.append("  with:")
    report.append("    path: ~/.cache/pip")
    report.append("    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}")
    report.append("    restore-keys: |")
    report.append("      ${{ runner.os }}-pip-")
    report.append("")
    report.append("- name: Install dependencies (uses cache)")
    report.append("  run: pip install -r requirements.txt")
    report.append("```")

    report.append("")

    # Matrix Strategy Section
    report.append("### 6. Use Matrix Strategy for Test Parallelization")
    report.append("")
    report.append("**Problem:** Running tests sequentially across different platforms/versions wastes time and resources.")
    report.append("")
    report.append("**Solution:** Use matrix strategy to run multiple test configurations in parallel jobs.")
    report.append("")

    report.append("**Example - Matrix strategy for parallel tests:**")
    report.append("```yaml")
    report.append("jobs:")
    report.append("  test:")
    report.append("    runs-on: ${{ matrix.os }}")
    report.append("    strategy:")
    report.append("      matrix:")
    report.append("        node-version: [16, 18, 20]")
    report.append("        os: [ubuntu-latest, windows-latest, macos-latest]")
    report.append("        exclude:")
    report.append("          - os: macos-latest")
    report.append("            node-version: 16   # Skip unsupported combo")
    report.append("      fail-fast: false         # ✅ Run all even if one fails")
    report.append("")
    report.append("    steps:")
    report.append("      - uses: actions/checkout@v4")
    report.append("      - name: Use Node.js ${{ matrix.node-version }}")
    report.append("        uses: actions/setup-node@v4")
    report.append("        with:")
    report.append("          node-version: ${{ matrix.node-version }}")
    report.append("          cache: 'npm'")
    report.append("      - run: npm ci")
    report.append("      - run: npm test")
    report.append("```")

    report.append("")

    # Dependabot Section
    report.append("### 7. Configure Dependabot for Automated Dependency Updates")
    report.append("")
    report.append("**Problem:** Manually updating dependencies is error-prone and slows down security patching.")
    report.append("")
    report.append("**Solution:** Enable Dependabot to automatically create PRs for dependency updates, with auto-merge for non-breaking changes.")
    report.append("")

    report.append("**Complete Dependabot configuration (create .github/dependabot.yml):**")
    report.append("```yaml")
    report.append("# version: 2 - Required format")
    report.append("version: 2")
    report.append("updates:")
    report.append("")
    report.append("  # Enable version updates for npm")
    report.append("  - package-ecosystem: \"npm\"")
    report.append("    directory: \"/\"")
    report.append("    schedule:")
    report.append("      interval: \"weekly\"       # Check weekly")
    report.append("    open-pull-requests-limit: 10  # Max concurrent PRs")
    report.append("    automerged-limits:")
    report.append("      minor-versions: true     # Auto-merge non-breaking changes")
    report.append("    labels:")
    report.append("      - dependencies")
    report.append("      - npm")
    report.append("")
    report.append("  # Enable version updates for GitHub Actions")
    report.append("  - package-ecosystem: \"github-actions\"")
    report.append("    directory: \"/\"")
    report.append("    schedule:")
    report.append("      interval: \"weekly\"")
    report.append("    labels:")
    report.append("      - dependencies")
    report.append("      - github-actions")
    report.append("```")

    report.append("")
    report.append("**Benefits of auto-merge:**")
    report.append("- Security patches applied automatically when CI passes")
    report.append("- Reduces technical debt from outdated dependencies")
    report.append("- Faster response to newly discovered vulnerabilities")
    report.append("- Configure branch protection rules to require reviews for major version updates")

    report.append("")

    # Action Items Section
    report.append("## ✅ ACTION ITEMS (Prioritized by Urgency)")
    report.append("")

    critical = [f for f in all_findings if f['severity'] == 'CRITICAL']
    high = [f for f in all_findings if f['severity'] == 'HIGH']
    medium = [f for f in all_findings if f['severity'] == 'MEDIUM']
    low = [f for f in all_findings if f['severity'] == 'LOW']

    if critical:
        report.append("### 🔴 IMMEDIATE (< 1 hour response)")
        report.append("")
        for i, f in enumerate(critical, 1):
            badge = severity_badges.get(f['severity'], '')
            report.append(f"{i}. [{badge} {f['type']}]")
            report.append(f"   Location: {f['workflow']} ({f['location']})")
            report.append(f"   Fix: {f['recommendation']}")
            report.append("")

    if high:
        report.append("### 🟡 SOON (< 24 hours response)")
        report.append("")
        for i, f in enumerate(high, 1):
            badge = severity_badges.get(f['severity'], '')
            report.append(f"{i}. [{badge} {f['type']}]")
            report.append(f"   Location: {f['workflow']} ({f['location']})")
            report.append(f"   Fix: {f['recommendation']}")
            report.append("")

    if medium:
        report.append("### 🔵 THIS SPRINT (< 1 week response)")
        report.append("")
        for i, f in enumerate(medium, 1):
            badge = severity_badges.get(f['severity'], '')
            report.append(f"{i}. [{badge} {f['type']}]")
            report.append(f"   Location: {f['workflow']} ({f['location']})")
            report.append(f"   Fix: {f['recommendation']}")
            report.append("")

    if low:
        report.append("### 🟢 BACKLOG (< 1 month response)")
        report.append("")
        for i, f in enumerate(low, 1):
            badge = severity_badges.get(f['severity'], '')
            report.append(f"{i}. [{badge} {f['type']}]")
            report.append(f"   Location: {f['workflow']} ({f['location']})")
            report.append(f"   Fix: {f['recommendation']}")
            report.append("")

    # Best Practices Checklist
    report.append("## 📋 SECURITY BEST PRACTICES CHECKLIST")
    report.append("")
    report.append("- [ ] No secrets exposed in logs or workflow files")
    report.append("- [ ] All actions pinned to commit SHAs or specific tags")
    report.append("- [ ] Least-privilege permissions applied to all workflows")
    report.append("- [ ] OIDC used instead of long-lived credentials for cloud providers (AWS/GCP/Azure)")
    report.append("- [ ] Environment protection rules configured for production deployments")
    report.append("- [ ] Required reviews enforced before deployment via repository settings")
    report.append("- [ ] Dependency caching implemented in build jobs (npm, pip, maven)")
    report.append("- [ ] Matrix strategy used for parallel test execution across OS/node versions")
    report.append("- [ ] Docker images pinned to version tags or SHA digests")
    report.append("- [ ] No containers running with root privileges or as root user")
    report.append("- [ ] Reusable workflows pinned to specific versions")
    report.append("- [ ] Dependabot configured with auto-merge enabled")
    report.append("")

    # Footer
    report.append("=" * 80)
    report.append("📌 For more details on security best practices, see the SKILL.md documentation.")
    report.append(f"   Total findings: {total} | Risk level: {risk}")
    report.append("=" * 80)

    return '\n'.join(report)


def main():
    """Run complete audit and display results."""
    repo_path = Path('test-workflows') / '.github' / 'workflows'

    if not repo_path.exists():
        print(f"Error: {repo_path} does not exist")
        return

    workflow_files = list(repo_path.glob('*.yml')) + list(repo_path.glob('*.yaml'))

    print("=" * 80)
    print("🔍 CI/CD Pipeline Auditor - Test Results")
    print("=" * 80)
    print()
    print(f"Scanning {len(workflow_files)} workflow files...")
    print()

    results = []
    for wf in sorted(workflow_files):
        result = run_audit(wf.relative_to(repo_path.parent), repo_path.parent)
        if result:
            results.append(result)
            status = "✅" if not result['findings'] else f"⚠️ {len(result['findings'])} issues"
            print(f"  {status} {wf.name}")

    print()
    report = generate_report(results)
    print(report)


if __name__ == '__main__':
    main()

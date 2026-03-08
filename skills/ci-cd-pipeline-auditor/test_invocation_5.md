# Test Invocation 5: "Check Docker security in this workflow"

This invocation focuses on **Docker container security** including unpinned images, privileged containers, root user detection, and credential exposure.

```bash
$ python run_tests.py --focus docker-security
```

---

================================================================================
🔍 CI/CD Pipeline Audit Report - Docker Security Focus
   Workflows Analyzed: docker-privileged.yml
   Generated: 2026-03-07 15:48:00
================================================================================

## 📊 EXECUTIVE SUMMARY

├─ 🔴 CRITICAL: 4 (requires immediate attention)
├─ 🟡 HIGH: 4 (should be addressed soon)
├─ 🔵 MEDIUM: 2 (plan to fix this sprint)
└─ 🟢 LOW: 0 (address when convenient)

**Overall Risk Assessment:** 🔴 HIGH RISK - Critical Docker security vulnerabilities require immediate attention


## 🔍 DETAILED FINDINGS

| Severity | Issue Type | Location | Description |
|----------|------------|----------|-------------|
| 🔴 CRITICAL | `WRITE_ALL_PERMISSIONS` | docker-privileged.yml (root level) | Workflow has write-all permissions violating least privilege principle |
| 🔴 CRITICAL | `DOCKER_PRIVILEGED_MODE` | build-and-push step 1 | Container running with --privileged flag - full host access! |
| 🔴 CRITICAL | `SECRETS_IN_RUN_COMMAND` | build-and-push step 3 | Docker credentials exposed in run command echo |
| 🔴 CRITICAL | `DOCKER_IMAGE_UNPINNED` | build-and-push step 2 | Image using :latest tag - unpredictable builds |
| 🟡 HIGH | `DOCKER_ROOT_USER` | build-and-push step 2 | Container may run as root without user specification |
| 🟡 HIGH | `DOCKER_LATEST_TAG` | build-and-push step 2 | Using node:latest instead of pinned version |
| 🟡 HIGH | `ACTION_UNPINNED_LATEST` | build-and-push step 5 | Action using @latest - mutable reference |
| 🟡 HIGH | `IMAGE_UNPINNED_PUSH` | build-and-push step 4 | Pushing image with unpinned :latest tag |
| 🔵 MEDIUM | `DOCKERFILE_NOT_IN_REPO` | build-and-push job | No Dockerfile detected; using inline commands |
| 🔵 MEDIUM | `NO_IMAGE_SCAN` | build-and-push job | No vulnerability scanning for container images |


## 🐳 DOCKER SECURITY ANALYSIS

### Container Security Status

| Step | Issue Type | Severity | Risk Level | Description |
|------|------------|----------|------------|-------------|
| Run privileged container | `--privileged` flag | 🔴 CRITICAL | Host compromise risk | Full host filesystem and device access |
| Build and run as root | No USER directive | 🟡 HIGH | Container escape risk | Running as root enables privilege escalation |
| Login to Docker Hub | Credentials in run | 🔴 CRITICAL | Credential theft | Secrets exposed in CI/CD logs |
| Build and push image | :latest tag | 🟡 HIGH | Supply chain attack | Unpredictable image builds |
| setup-buildx-action | @latest reference | 🟡 HIGH | Action compromise | Mutable action reference |


### Privileged Container Analysis

**CRITICAL:** The workflow runs Docker containers with `--privileged` flag which grants:
- Full access to all host devices (`/dev/*`)
- Ability to load kernel modules
- CAP_SYS_ADMIN capability (near-root privileges)
- Access to host filesystem and network stack

```yaml
# ❌ CRITICAL - Privileged container gives full host access
- name: Run privileged container
  uses: addnab/docker-run-action@v3
  with:
    options: --rm --privileged  # 🚨 FULL HOST ACCESS!
    image: docker.io/library/ubuntu:latest
    run: |
      ls -la /dev        # Can list all host devices
      mount              # Can mount filesystems
```

**Impact of Privileged Containers:**
- Container escape attacks grant attacker full host access
- Malicious containers can install rootkits on CI runners
- Compromised builds can steal secrets from other jobs
- Attackers can pivot to internal network resources


### Docker Image Pinning Status

| Job | Image Reference | Tag Type | Digest Present | Security Level | Recommendation |
|-----|-----------------|----------|----------------|---------------|----------------|
| Run as root | `node:latest` | :latest tag | ❌ No | ⚠️ HIGH RISK | Pin to version or digest |
| Build and push | `myapp:latest` | :latest tag | ❌ No | ⚠️ HIGH RISK | Use semantic versioning |

### Best Practice: Docker Image Security

```yaml
# ❌ UNSAFE - Using :latest tag (unpredictable)
- name: Run tests in container
  run: docker run node:latest npm test

# ⚠️ MEDIUM RISK - Tag can update within minor version
- name: Run tests in container
  run: docker run node:20.10 npm test

# ✅ SECURE - Pinned to specific major.minor.patch
- name: Run tests in container
  run: docker run node:20.10.5 npm test

# ✅ MOST SECURE - Pinned to image digest (immutable)
- name: Run tests in container
  run: docker run node@sha256:c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7e8f9b0c1d2e3f4a5b6c7d8e9 npm test
```


## 🔐 DETAILED FINDINGS WITH FIXES (Docker Security Focus)

### 🔴 CRITICAL: DOCKER_PRIVILEGED_MODE

**Location:** docker-privileged.yml - build-and-push step 1

**Description:** Container running with `--privileged` flag which grants full host access. This is one of the most critical Docker security issues as it essentially gives root access to the underlying host machine.

**Impact:**
- Container escape allows attacker to control CI runner
- Full access to host filesystem, devices, and kernel modules
- Can steal secrets from other workflow jobs on same runner
- Potential lateral movement to internal network resources

**Recommendation:** Never use `--privileged` flag. Use specific capabilities instead.

**BEFORE (insecure - privileged mode):**
```yaml
- name: Run privileged container
  uses: addnab/docker-run-action@v3
  with:
    options: --rm --privileged  # 🚨 FULL HOST ACCESS!
    image: docker.io/library/ubuntu:latest
    run: |
      ls -la /dev        # Can access all host devices
```

**AFTER (secure - specific capabilities):**
```yaml
- name: Run container with required capabilities only
  uses: addnab/docker-run-action@v3
  with:
    options: |          # ✅ Only CAP_NET_ADMIN needed
      --rm
      --cap-add=NET_ADMIN
      --cap-drop=ALL     # Drop all, then add what you need
    image: docker.io/library/ubuntu:latest
    run: ls -la /dev

# Alternative: Use specific device access if needed
  with:
    devices: |          # ✅ Explicit device mapping only
      /dev/ttyS0:/dev/ttyS0
```


### 🔴 CRITICAL: SECRETS_IN_RUN_COMMAND

**Location:** docker-privileged.yml - build-and-push step 3

**Description:** Docker credentials exposed in run command. The workflow echoes `${{ secrets.DOCKERHUB_TOKEN }}` to stdout which will be logged and potentially exposed in GitHub Actions logs, CI/CD history, or through log aggregation systems.

**Impact:**
- Registry credentials exposed in publicly viewable logs (for public repos)
- Secrets indexed by external log aggregators even after deletion
- Permanent credential exposure requiring immediate rotation
- Potential for unauthorized image pushes to registry

**Recommendation:** Use Docker's stdin authentication; never echo secrets.

**BEFORE (insecure - exposing credentials):**
```yaml
# ❌ EXPOSES CREDENTIALS IN LOGS!
- name: Login to Docker Hub
  run: |
    echo ${{ secrets.DOCKERHUB_TOKEN }} | docker login -u myuser --password-stdin

# Even worse: Echoing the secret value directly
- name: Debug credentials
  run: echo "Token: ${{ secrets.DOCKERHUB_TOKEN }}"
```

**AFTER (secure - stdin authentication without exposure):**
```yaml
# ✅ Credentials in stdin, not echoed
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: myuser
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# Or using run command with stdin (safe - no echo)
- name: Login to Docker Hub
  run: |
    if [ -z "${{ secrets.DOCKERHUB_TOKEN }}" ]; then
      echo "ERROR: DOCKERHUB_TOKEN secret is required"
      exit 1
    fi
    echo ${{ secrets.DOCKERHUB_TOKEN }} | docker login -u myuser --password-stdin

# Best: Use action with built-in security
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```


### 🟡 HIGH: DOCKER_IMAGE_UNPINNED

**Location:** docker-privileged.yml - build-and-push step 2 and step 4

**Description:** Docker images using `:latest` tag which always pulls the most recent version. This causes unpredictable builds, security vulnerabilities from unvetted updates, and potential supply chain attacks.

**Impact:**
- Builds fail unexpectedly when upstream images change
- Security patches applied without testing cause breakage
- Malicious image pushes can compromise CI/CD pipeline
- Inconsistent behavior across different build runs

**Recommendation:** Pin Docker images to specific version tags or SHA digests.

**BEFORE (insecure - :latest tag):**
```yaml
# ❌ Unpredictable builds!
- name: Build and run as root
  uses: addnab/docker-run-action@v3
  with:
    image: node:latest  # 🚨 Always pulls newest version

- name: Push image
  uses: docker/build-push-action@v5
  with:
    tags: myapp:latest  # 🚨 Unpinned push tag
```

**AFTER (secure - pinned versions):**
```yaml
# ✅ Pinned to specific major.minor version
- name: Build and run as root
  uses: addnab/docker-run-action@v3
  with:
    image: node:20.10.5  # Specific version

# Most secure: Pin to digest (immutable)
- name: Run tests
  uses: addnab/docker-run-action@v3
  with:
    image: node@sha256:c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7e8f9b0c1d2e3f4a5b6c7d8e9

# ✅ Use semantic versioning for pushes
- name: Push image with version tag
  uses: docker/build-push-action@v5
  with:
    tags: |
      myapp:${{ github.sha }}        # Commit SHA
      myapp:v${{ github.ref_name }}   # Tag from branch
```


### 🟡 HIGH: DOCKER_ROOT_USER

**Location:** docker-privileged.yml - build-and-push step 2

**Description:** Container running without explicit USER directive, defaulting to root. Running containers as root increases the risk of privilege escalation and container escape attacks.

**Impact:**
- Easier privilege escalation if vulnerability exploited
- Files created in container have root ownership
- Cannot safely run untrusted code in container
- Violates principle of least privilege

**Recommendation:** Specify non-root USER in Dockerfile or use --user flag.

**BEFORE (insecure - running as root):**
```yaml
# ❌ No USER directive - runs as root by default
- name: Build and run as root
  uses: addnab/docker-run-action@v3
  with:
    image: node:20.10.5
    run: |
      npm install    # Running as root!
```

**AFTER (secure - non-root user):**
```yaml
# ✅ Run as specific non-root user
- name: Build and run as non-root
  uses: addnab/docker-run-action@v3
  with:
    options: --user 1000:1000  # Run as UID/GID 1000
    image: node:20.10.5
    run: |
      npm install

# Alternative: Add USER directive to Dockerfile
# FROM node:20.10.5
# RUN useradd -m appuser
# USER appuser
```


## 🛠️ RECOMMENDED FIXES (Docker Security Complete)

### 1. Never Use Privileged Containers

**Problem:** `--privileged` flag gives containers full host access, enabling container escape and host compromise.

**Solution:** Grant only specific capabilities needed for the task.

```yaml
# Instead of --privileged, use:
options: |
  --cap-add=NET_ADMIN           # Only required capabilities
  --cap-drop=ALL                # Start with no permissions
  --user=1000                   # Non-root user
  --read-only                   # Read-only filesystem
  --tmpfs /tmp:rw,noexec,nosuid  # Limited writable areas

# For device access, map specific devices:
devices: |
  /dev/ttyS0:/dev/ttyS0         # Only this serial port
```


### 2. Pin All Docker Images to Digests

**Problem:** Using :latest or unpinned tags causes unpredictable builds and supply chain risks.

**Solution:** Pin images to specific version tags or SHA digests.

```yaml
# Get digest for pinned image:
# docker pull node@sha256:c5d4a7e...

- name: Run with pinned image
  uses: addnab/docker-run-action@v3
  with:
    image: node@sha256:c5d4a7e8f9b2c1d3e6f7a8b9c0d1e2f3a4b5c6d7e8f9b0c1d2e3f4a5b6c7d8e9

# Use actions that support digest pinning:
- name: Build and push with pinned base
  uses: docker/build-push-action@v5
  with:
    tags: myapp:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```


### 3. Scan Images for Vulnerabilities

**Problem:** No vulnerability scanning before deploying container images.

**Solution:** Add image scanning steps using Trivy, Grype, or Docker Scout.

```yaml
- name: Build and scan image
  uses: docker/build-push-action@v5
  with:
    push: false
    tags: myapp:${{ github.sha }}

- name: Scan for vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'myapp:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'

- name: Upload scan results
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: 'trivy-results.sarif'
```


### 4. Use Docker Actions for Authentication

**Problem:** Manually echoing credentials in run commands exposes secrets in logs.

**Solution:** Use official Docker actions that handle authentication securely.

```yaml
# ✅ Secure Docker Hub login
- name: Login to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}

# ✅ Secure GitHub Container Registry login (no secret needed!)
- name: Login to GHCR
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```


## ✅ ACTION ITEMS (Prioritized by Urgency)

### 🔴 IMMEDIATE (< 1 hour response)

1. [🔴 DOCKER_PRIVILEGED_MODE]
   Location: docker-privileged.yml (build-and-push step 1)
   Fix: Remove --privileged flag; use specific capabilities only

2. [🔴 SECRETS_IN_RUN_COMMAND]
   Location: docker-privileged.yml (build-and-push step 3)
   Fix: Use docker/login-action instead of echo credentials


### 🟡 SOON (< 24 hours response)

1. [🟡 DOCKER_IMAGE_UNPINNED]
   Location: docker-privileged.yml (build-and-push step 2)
   Fix: Pin node image to specific version or digest

2. [🟡 DOCKER_ROOT_USER]
   Location: docker-privileged.yml (build-and-push step 2)
   Fix: Add --user flag or USER directive for non-root execution

3. [🟡 IMAGE_UNPINNED_PUSH]
   Location: docker-privileged.yml (build-and-push step 4)
   Fix: Use commit SHA or semantic version instead of :latest

4. [🟡 ACTION_UNPINNED_LATEST]
   Location: docker-privileged.yml (build-and-push step 5)
   Fix: Pin actions/setup-buildx-action to specific version


### 🔵 THIS SPRINT (< 1 week response)

1. [🔵 NO_IMAGE_SCAN]
   Location: docker-privileged.yml (build-and-push job)
   Fix: Add Trivy or Grype vulnerability scanning for container images

2. [🔵 DOCKERFILE_NOT_IN_REPO]
   Location: docker-privileged.yml (build-and-push job)
   Fix: Create proper Dockerfile in repository for reproducible builds


================================================================================
📌 For more details on Docker security, see the SKILL.md documentation.
   Total findings: 10 | Risk level: 🔴 HIGH RISK - Critical Docker security vulnerabilities require immediate attention

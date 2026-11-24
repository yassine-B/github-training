# Module 4 — GitHub Actions & CI/CD

## Lesson 36 — Advanced CI/CD Security, Quality Gates & Software Supply Chain Security

**Level:** Advanced
**Estimated time:** 5–7 hours
**Previous lesson:** Lesson 35 — Advanced GitHub Actions: Professional CI/CD Pipelines
**Next lesson:** Lesson 37 — GitHub Actions Runners, Self-Hosted Infrastructure & Enterprise
Automation

---

## Lesson Overview

In Lesson 35, you learned how to build professional GitHub Actions pipelines that validate, test, package, and deploy applications.

Now we'll focus on securing those pipelines.

A successful CI/CD pipeline should not only prove that an application builds and its tests pass. It should also provide confidence that:

- The source code has been checked for security weaknesses.
- Dependencies are monitored for known vulnerabilities.
- Credentials have not been accidentally exposed.
- Workflow permissions are restricted.
- Docker images are scanned.
- Build artifacts can be traced to their source.
- Software components are documented.
- Security and quality requirements are enforced before deployment.

We'll use examples based on your future Django REST Framework + React/Vite architecture.

### Important repository distinction

We will use two different environments throughout this lesson:

1. `github-deep-dive-training`: Your current private documentation and training repository.
2. Your future Django + React application repository: The environment where backend tests, frontend tests, Docker builds, and application-specific scanning will eventually run.

Do not configure workflows that assume `/backend`, `/frontend`, `requirements.txt`, `package.json`, or Dockerfiles exist in the training repository unless you have actually added them.

## Learning Objectives

By the end of this lesson, you should understand how to:

1. Apply DevSecOps principles to CI/CD.
2. Secure GitHub Actions permissions and triggers.
3. Pin third-party Actions to verified commit SHAs.
4. Understand SAST, DAST, SCA, and secret scanning.
5. Configure CodeQL.
6. Configure Dependabot.
7. Detect and respond to exposed credentials using Gitleaks.
8. Apply dependency review policies.
9. Scan filesystems, Docker images, and infrastructure configuration with Trivy.
10. Integrate SonarQube into CI.
11. Understand and enforce quality gates.
12. Generate CycloneDX and SPDX SBOMs.
13. Understand artifact attestations and build provenance.
14. Combine security tools into a practical pipeline.
15. Document vulnerability remediation and security exceptions.

---

## 1. DevSecOps Fundamentals

## 1.1 Traditional CI/CD vs DevSecOps

A traditional pipeline often looks like this:

```text
Developer
    |
    v
Source Code
    |
    v
Build
    |
    v
Tests
    |
    v
Package
    |
    v
Deploy
```

Security may be handled separately, sometimes after the application has already been deployed.

DevSecOps integrates security checks into the development and delivery lifecycle.

```text
Developer
    |
    v
Pull Request
    |
    +---- Code Quality
    |
    +---- Secret Detection
    |
    +---- SAST
    |
    +---- Dependency Security
    |
    +---- Tests
    |
    v
Build
    |
    +---- Container Scanning
    |
    +---- SBOM Generation
    |
    +---- Artifact Provenance
    |
    v
Quality and Security Gates
    |
    v
Approved Deployment
```

The objective is to detect problems early, when they are generally easier and less expensive to fix.

## 1.2 What is a quality gate?

A quality gate is a set of conditions that must be satisfied before a pipeline can continue.

Examples:

| Control | Example requirement |
|---|---|
| Linting | No blocking lint errors |
| Tests | All required tests pass |
| Coverage | Coverage meets the agreed project threshold |
| SAST | No prohibited security findings |
| Dependencies | No disallowed vulnerable dependencies |
| Secrets | No exposed credentials |
| Container scanning | No vulnerabilities above the agreed threshold |
| Deployment | Required environment approval obtained |

A quality gate is not simply a dashboard displaying results.

It must be connected to pipeline enforcement.

For example:

- A scanner can produce a report.
- A scanner can return a non-zero exit code.
- A CI job can fail based on that exit code.
- A required GitHub check can prevent a pull request from being merged.

These are related but different behaviors.

## 1.3 Define security policies before enabling tools

Do not automatically block every warning.

Instead, define policies using:

- Severity.
- Exploitability.
- Whether a fix is available.
- Whether the affected component is reachable.
- Business impact.
- Exposure of the affected application.
- Compensating controls.

For example, a critical vulnerability in a publicly exposed authentication dependency deserves a different response from a low-severity issue in an unused development dependency.

Create a documented vulnerability policy rather than changing thresholds whenever a pipeline fails.

---

## 2. Securing GitHub Actions Workflows

GitHub Actions workflows are executable automation code.

A workflow can access repository contents, interact with packages, access configured secrets, and potentially deploy applications.

A compromised workflow can therefore become a serious security problem.

We'll focus on four controls:

1. Least-privilege permissions.
2. Immutable Action references.
3. Safe workflow triggers.
4. Safe handling of untrusted input.

## 2.1 Least-privilege permissions

Consider:

```yaml
permissions: write-all
```

This grants broad permissions that most workflows do not need.

Prefer explicitly defining the required permissions:

```yaml
permissions:
  contents: read
```

A workflow that only checks out code and runs tests normally needs read access to repository contents.

A workflow that publishes packages may need:

```yaml
permissions:
  contents: read
  packages: write
```

A workflow that creates a GitHub release may need:

```yaml
permissions:
  contents: write
```

A workflow that requests an OIDC identity token may need:

```yaml
permissions:
  contents: read
  id-token: write
```

**Important:** `id-token: write` allows a job to request an OIDC token. It does not automatically grant access to a cloud account. The cloud provider must also trust the token's identity and claims.

### Job-level permissions

You can give different jobs different permissions.

```yaml
name: Example Security Pipeline

on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - name: Run tests
        run: echo "Testing application"

  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Publish package
        run: echo "Publishing trusted package"
```

This illustrates permission separation. A real publishing job must also be restricted to trusted events and protected branches.

**Professional rule:** A test job should not receive deployment permissions just because another job needs them.

## 2.2 Pin third-party Actions to full commit SHAs

You may have used:

```yaml
- uses: actions/checkout@v6
```

A version tag is convenient and readable, but tags can potentially move.

A full commit SHA identifies a specific revision.

Example format:

```yaml
- uses: actions/checkout@<VERIFIED_FULL_40_CHARACTER_SHA>
```

Do not copy an unverified SHA from a random tutorial.

When pinning Actions:

1. Identify the official repository.
2. Inspect the intended release.
3. Verify the full commit SHA.
4. Check the release and its changelog.
5. Record the Action and its purpose.
6. Establish a process for updating the pinned SHA.

Dependabot can help update GitHub Actions references.

For learning, major-version tags are easier to read. For sensitive production workflows, prefer verified full-SHA references.

## 2.3 Secure workflow triggers

For ordinary pull-request testing:

```yaml
on:
  pull_request:
    branches:
      - main
```

Be especially careful with:

```yaml
on:
  pull_request_target:
```

`pull_request_target` runs in the context of the target repository and can receive access to privileges unavailable to an ordinary untrusted pull-request workflow.

A dangerous pattern is:

1. A privileged `pull_request_target` workflow starts.
2. It checks out code from an untrusted pull request.
3. It executes scripts from that code.
4. Those scripts gain access to privileged workflow resources.

This can expose repository secrets or other privileges.

For ordinary testing of pull-request code, use `pull_request`.

Do not execute untrusted pull-request code inside a privileged `pull_request_target` workflow.

## 2.4 Avoid unsafe shell interpolation

Risky example:

```yaml
- name: Process pull request title
  run: echo "${{ github.event.pull_request.title }}"
```

The pull-request title is external input. Directly inserting it into a shell command can create command-injection risks.

A safer approach is to pass it through an environment variable:

```yaml
- name: Process pull request title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    echo "$PR_TITLE"
```

For complex values, validate and process the input safely.

Environment variables reduce the risk of shell-source injection, but they do not make arbitrary input trustworthy.

## 2.5 Protect secrets

GitHub Actions provides:

- Repository secrets.
- Environment secrets.
- Organization secrets.
- Repository variables.
- Environment variables.

Use secrets for sensitive credentials.

Use variables for non-sensitive configuration.

Never:

- Print credentials to logs.
- Commit `.env` files containing real credentials.
- Put credentials in workflow YAML.
- Pass secrets to untrusted pull-request code.
- Assume log masking makes a leaked secret safe.

If a real credential is exposed, revoke or rotate it immediately.

### Exercise 1 — Workflow security review

Inspect your `.github/workflows/` directory.

- [ ] Identify all workflow permissions.
- [ ] Find workflows using broad write permissions.
- [ ] Identify third-party Actions using version tags.
- [ ] Understand full-SHA pinning.
- [ ] Search for `pull_request_target`.
- [ ] Review commands that use pull-request data.
- [ ] Check whether secrets are printed or exposed.
- [ ] Separate test and deployment permissions.

Create:

`docs/github/module-04-actions/workflow-security-review.md`

Document each finding, its risk, and the recommended correction.

---

## 3. SAST — Static Application Security Testing

SAST analyzes source code without executing the application.

It can identify potential weaknesses such as:

- SQL injection patterns.
- Cross-site scripting patterns.
- Insecure deserialization.
- Unsafe input handling.
- Weak cryptographic practices.
- Potential path traversal.
- Insecure API patterns.
- Hardcoded credentials, depending on the tool.

SAST findings require investigation. A finding is not automatically proof that an exploitable vulnerability exists.

## 3.1 Security testing categories

| Technique | What it analyzes | Example |
|---|---|---|
| SAST | Source code | CodeQL |
| DAST | Running application | OWASP ZAP |
| SCA | Third-party dependencies | Dependabot, dependency scanners |
| Secret scanning | Potential credentials | Gitleaks |
| Container scanning | Container images | Trivy |
| IaC scanning | Infrastructure configuration | Trivy |

These techniques complement one another.

No single tool replaces the others.

## 3.2 What is CodeQL?

CodeQL is GitHub's code analysis engine.

It analyzes supported programming languages and identifies potential security weaknesses.

Languages relevant to your future applications include:

- Python.
- JavaScript.
- TypeScript.
- Java.
- C#.
- C/C++.

CodeQL supports two common configuration approaches:

| Setup | Description |
|---|---|
| Default setup | GitHub manages much of the scanning configuration |
| Advanced setup | You manage a custom scanning workflow |

Default setup is usually the simpler starting point.

## 3.3 Enable CodeQL

Navigate to your repository:

```text
Repository
    |
    v
Settings
    |
    v
Security and analysis
    |
    v
Code security
    |
    v
Code scanning
    |
    v
Set up
```

The exact labels and available options may vary.

Review the configuration offered by GitHub and check your repository's eligibility.

**Private repository note:** Code-scanning availability depends on the repository's plan, ownership, and applicable GitHub Code Security entitlements. Do not assume that every private personal repository has access to every feature. Check the actual settings displayed for your repository.

## 3.4 Advanced CodeQL workflow

If your repository is eligible and you choose advanced setup, the following illustrates the workflow architecture.

Filename:

`.github/workflows/codeql.yml`

```yaml
name: CodeQL Security Analysis

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

  schedule:
    - cron: "30 2 * * 1"

  workflow_dispatch:

permissions:
  contents: read

jobs:
  analyze:
    name: Analyze Code
    runs-on: ubuntu-latest

    permissions:
      contents: read
      security-events: write
      actions: read

    strategy:
      fail-fast: false
      matrix:
        language:
          - python
          - javascript-typescript

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v4
        with:
          languages: ${{ matrix.language }}

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v4
```

This is an illustrative configuration using readable version tags. Verify the current supported Action releases and generated configuration before using it. Pin verified full SHAs in a production workflow.

For a repository containing only Markdown documentation, CodeQL may have little or no relevant application code to analyze. The workflow becomes more useful when you add actual Python, JavaScript, or TypeScript source code.

## 3.5 Understand CodeQL alerts

Navigate to:

```text
Repository
    |
    v
Security
    |
    v
Code scanning
    |
    v
Code scanning alerts
```

An alert can include:

- Rule name.
- Severity.
- Affected file.
- Code location.
- Explanation.
- Recommended remediation.
- Alert status.

Learn to distinguish:

- Open alerts.
- Fixed alerts.
- Dismissed alerts.
- False positives.

Do not dismiss a finding simply because it is inconvenient.

Document why a finding is not applicable when you decide to dismiss it.

### Exercise 2 — CodeQL

- [ ] Inspect CodeQL availability.
- [ ] Understand default and advanced setup.
- [ ] Review the workflow architecture.
- [ ] Inspect sample alerts and remediation guidance.
- [ ] Document any repository licensing limitation.
- [ ] Understand why a documentation-only repository may have limited CodeQL value.

Create:

`docs/github/module-04-actions/codeql-guide.md`

---

## 4. Dependency Security

Modern applications depend on external packages.

Your future backend might use:

```text
Django
Django REST Framework
psycopg
Celery
Redis
Pillow
pytest
```

Your frontend might use:

```text
React
Vite
TypeScript
Axios
Zustand
TanStack Query
Zod
```

Every dependency introduces maintenance and security considerations.

A vulnerability in a third-party package can affect your application even when your own code is correct.

## 4.1 What is Software Composition Analysis?

Software Composition Analysis (SCA) examines the third-party components used by an application.

It can help identify:

- Known vulnerable versions.
- Outdated packages.
- Security advisories.
- Dependency relationships.
- License information, depending on the tool.

SCA is especially important for applications with many direct and transitive dependencies.

A direct dependency is explicitly declared by your project.

A transitive dependency is brought in by another dependency.

For example:

```text
Your Application
    |
    +---- Django
    |       |
    |       +---- Dependency A
    |       +---- Dependency B
    |
    +---- Celery
            |
            +---- Dependency C
```

You must consider both direct and transitive dependencies.

---

## 5. Dependabot

## 5.1 What is Dependabot?

Dependabot is GitHub's dependency automation service.

It can help with:

| Feature | Purpose |
|---|---|
| Dependabot alerts | Notify you about vulnerable dependencies |
| Dependabot security updates | Create pull requests to address eligible vulnerabilities |
| Dependabot version updates | Keep dependencies up to date |

Security updates and ordinary version updates are different workflows.

A dependency can be outdated without being known to be vulnerable.

A dependency can also be vulnerable even if your application has not been updated recently.

## 5.2 Configure Dependabot

Dependabot configuration belongs in:

`.github/dependabot.yml`

For your current training repository, begin with GitHub Actions updates:

```yaml
version: 2

updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    labels:
      - dependencies
      - github-actions
    commit-message:
      prefix: ci
      include: scope
```

This configuration is appropriate for a repository that has GitHub Actions workflows.

For your future Django + React application, you could add:

```yaml
version: 2

updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly

  - package-ecosystem: pip
    directory: /backend
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: /frontend
    schedule:
      interval: weekly

  - package-ecosystem: docker
    directory: /backend
    schedule:
      interval: weekly
```

Only add an ecosystem when the corresponding manifests or Dockerfiles actually exist at that path.

For example:

- `pip` requires a supported Python dependency manifest.
- `npm` requires an npm project manifest and lockfile.
- `docker` requires a Dockerfile in the configured directory.
- `github-actions` monitors workflow Action references.

## 5.3 Group dependency updates

Dependabot can group eligible updates to reduce pull-request volume.

Example:

```yaml
version: 2

updates:
  - package-ecosystem: npm
    directory: /frontend
    schedule:
      interval: weekly

    groups:
      frontend-minor-and-patch:
        update-types:
          - minor
          - patch
```

This groups eligible minor and patch updates.

Major upgrades should receive more careful review because they can introduce breaking changes.

## 5.4 Review Dependabot pull requests

Imagine Dependabot creates:

```text
chore(deps): bump axios from 1.x to 2.x
```

Do not merge automatically without considering the impact.

Use this process:

1. Inspect the dependency change.
2. Read the release notes.
3. Review breaking changes.
4. Inspect the lockfile diff.
5. Run CI.
6. Run integration tests where relevant.
7. Review security advisories.
8. Merge only when the update is acceptable.

### Exercise 3 — Dependabot

- [ ] Create `.github/dependabot.yml`.
- [ ] Configure GitHub Actions updates.
- [ ] Understand the `pip` ecosystem.
- [ ] Understand the `npm` ecosystem.
- [ ] Understand Docker dependency updates.
- [ ] Inspect Dependabot settings.
- [ ] Review a Dependabot pull request when one appears.
- [ ] Document your dependency update policy.

Create:

`docs/github/module-04-actions/dependabot-guide.md`

---

## 6. Secret Scanning

One of the most common security mistakes is accidentally committing credentials.

Examples of sensitive information include:

```text
DATABASE_PASSWORD
API_SECRET
JWT_SECRET
AWS_ACCESS_KEY
PRIVATE_API_TOKEN
```

Never commit real credentials to Git.

## 6.1 What is secret scanning?

Secret scanning searches repositories and other supported locations for values that resemble credentials.

Depending on the service and configuration, it may detect:

- API tokens.
- Cloud credentials.
- Private keys.
- Database credentials.
- Passwords.
- Other sensitive values.

Secret scanning can be provided by GitHub or independent tools.

## 6.2 GitHub secret scanning and push protection

GitHub provides native secret-scanning features, including push protection where eligible.

Push protection can help prevent certain detected secrets from being pushed.

It is not a guarantee that every secret will be detected.

Some features depend on repository visibility, ownership, and licensing.

Check the actual security settings for your repository.

## 6.3 What to do when a secret is exposed

If a real credential is exposed:

1. Revoke or rotate the credential with its provider.
2. Check whether it was used.
3. Investigate the exposure.
4. Identify affected systems.
5. Remove the secret from active source code.
6. Review Git history and exposure locations.
7. Add appropriate prevention controls.
8. Document the incident.

**Critical:** Deleting a credential from the latest commit does not make an already exposed credential safe.

Rotate it first.

---

## 7. Gitleaks

## 7.1 What is Gitleaks?

Gitleaks is an open-source tool for detecting potential secrets in repositories and Git history.

It can detect patterns associated with:

- API tokens.
- Private keys.
- Cloud credentials.
- Passwords.
- Other sensitive values.

It can be used locally and in CI.

## 7.2 Install and verify Gitleaks on Windows

Install Gitleaks using a trusted package manager or the official release distribution.

Verify the installation:

```powershell
gitleaks version
```

Scan the working directory:

```powershell
gitleaks dir .
```

Scan Git history:

```powershell
gitleaks git .
```

Generate a JSON report:

```powershell
gitleaks git . --report-format json --report-path gitleaks-report.json
```

Treat generated reports as sensitive. They can contain matched values or contextual information.

Do not commit reports containing sensitive findings.

## 7.3 Add a Gitleaks workflow

Filename:

`.github/workflows/gitleaks.yml`

```yaml
name: Secret Detection

on:
  pull_request:

  push:
    branches:
      - main

  workflow_dispatch:

permissions:
  contents: read

jobs:
  secret-scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout full history
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This is an illustrative integration. Before using it in production:

- Verify the official Action documentation.
- Check its current supported inputs.
- Confirm its required permissions and authentication.
- Pin the Action to a verified full commit SHA.
- Review how its reports and logs are handled.

## 7.4 Gitleaks configuration

You can create:

`.gitleaks.toml`

Example:

```toml
title = "GitHub Deep Dive Secret Detection"

[allowlist]
description = "Approved non-sensitive test fixtures"
paths = [
  '''docs/examples/'''
]
```

This is an example of an allowlist, not a recommendation to exclude all documentation examples.

Avoid broad allowlists.

An overly broad exclusion can hide real credentials.

Prefer narrow, reviewed exceptions.

## 7.5 GitHub secret scanning vs Gitleaks

| Capability | GitHub secret scanning | Gitleaks |
|---|---|---|
| Provider | GitHub | Open-source project |
| Native repository integration | Yes | Through Actions or local tooling |
| Local developer scanning | Not its primary role | Yes |
| Custom detection rules | Feature-dependent | Yes |
| Push protection | Available where eligible | Not the same feature |
| CI integration | GitHub platform | Independent workflow integration |

These tools can complement each other.

### Exercise 4 — Gitleaks

- [ ] Install Gitleaks locally.
- [ ] Verify the installation.
- [ ] Scan the working directory.
- [ ] Scan Git history.
- [ ] Generate a local report.
- [ ] Understand the report's sensitivity.
- [ ] Create a Gitleaks workflow.
- [ ] Review allowlist risks.
- [ ] Document credential rotation and incident response.

Create:

`docs/github/module-04-actions/gitleaks-guide.md`

---

## 8. Dependency Review

Dependency Review examines dependency changes introduced by a pull request.

It helps identify whether a proposed change introduces vulnerable dependencies.

## 8.1 Dependabot vs Dependency Review

| Dependency Review | Dependabot |
|---|---|
| Examines dependency changes in PRs | Monitors dependency updates |
| Can enforce vulnerability thresholds | Can create update PRs |
| Helps prevent risky changes from merging | Helps keep dependencies maintained |
| Runs as a workflow | Uses GitHub dependency automation |

They solve different problems.

## 8.2 Add a Dependency Review workflow

Filename:

`.github/workflows/dependency-review.yml`

```yaml
name: Dependency Review

on:
  pull_request:

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      - name: Dependency review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
```

This example uses a version tag for readability. Verify the supported version and pin a verified SHA for production.

Dependency Review is most useful when a repository has dependency manifests and pull requests that change those dependencies.

A documentation-only repository may have limited practical dependency changes to review.

## 8.3 Understand the severity threshold

The example uses:

```yaml
fail-on-severity: high
```

This is a policy decision, not a universal setting.

You might decide to block:

- Critical vulnerabilities.
- High vulnerabilities.
- Specific vulnerable licenses.
- Other prohibited dependency changes.

The correct threshold depends on your risk policy and the capabilities of the tool.

### Exercise 5 — Dependency Review

- [ ] Understand how dependency changes are identified.
- [ ] Review the workflow configuration.
- [ ] Understand severity thresholds.
- [ ] Compare Dependency Review with Dependabot.
- [ ] Document the conditions that should block a pull request.

---

## 9. Container Security

Your future applications will use Docker containers.

For example:

```text
restaurant-pos/
|
+-- backend/
|   +-- Dockerfile
|
+-- frontend/
|   +-- Dockerfile
|
+-- docker-compose.yml
|
+-- .dockerignore
```

A container image can include:

- Operating-system packages.
- Python packages.
- Node.js packages.
- System libraries.
- Application code.
- Configuration files.

Every component can introduce vulnerabilities.

Container security should therefore cover more than the Dockerfile.

You should inspect:

1. Base images.
2. Operating-system packages.
3. Application dependencies.
4. Dockerfile configuration.
5. Image contents.
6. Secrets accidentally copied into the image.
7. Image provenance.

## 9.1 Use minimal base images

A smaller base image can reduce the number of included components and the potential attack surface.

However, minimal images are not automatically secure.

You still need to:

- Use supported base-image versions.
- Update dependencies.
- Scan the final image.
- Avoid unnecessary packages.
- Run the application with appropriate privileges.
- Keep secrets outside the image.

## 9.2 Avoid copying secrets into images

Do not use:

```dockerfile
COPY .env /app/.env
```

A secret copied into an image can remain in image layers even after later filesystem changes.

Use appropriate runtime secret injection or platform-specific secret management.

Use `.dockerignore` to prevent unnecessary files from entering the build context.

Example:

```text
.env
.env.*
.git
node_modules
__pycache__
*.pyc
```

Review the patterns before applying them. Do not accidentally exclude required application files.

---

## 10. Trivy

## 10.1 What is Trivy?

Trivy is an open-source security scanner.

It supports several scanning targets:

| Scan target | Purpose |
|---|---|
| Filesystem | Inspect dependencies and files |
| Container image | Inspect image packages and vulnerabilities |
| Repository | Scan source repositories |
| Configuration | Inspect infrastructure configuration |
| SBOM | Generate or inspect software inventories |
| Secrets | Detect potential exposed credentials |

## 10.2 Install and scan locally

After installing Trivy, verify:

```powershell
trivy version
```

Scan the current repository:

```powershell
trivy fs .
```

Filter by severity:

```powershell
trivy fs --severity HIGH,CRITICAL .
```

Scan infrastructure configuration:

```powershell
trivy config .
```

After building a Docker image:

```powershell
docker build -t restaurant-pos-backend:local ./backend
```

Scan it:

```powershell
trivy image restaurant-pos-backend:local
```

These examples assume that the relevant application files and Dockerfile exist.

## 10.3 Add Trivy to GitHub Actions

Filename:

`.github/workflows/trivy.yml`

```yaml
name: Trivy Security Scan

on:
  pull_request:

  push:
    branches:
      - main

  workflow_dispatch:

permissions:
  contents: read

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Run Trivy filesystem scan
        uses: aquasecurity/trivy-action@v0.36.0
        with:
          scan-type: fs
          scan-ref: .
          severity: HIGH,CRITICAL
          format: table
          exit-code: "1"
          ignore-unfixed: true
```

This example illustrates a blocking filesystem scan.

The `exit-code: "1"` setting makes the action fail when findings meet its configured conditions.

The `ignore-unfixed` setting changes which findings are considered. It should be a deliberate policy decision, not a way to hide inconvenient vulnerabilities.

Verify the current Action version and pin a verified SHA before production use.

## 10.4 Understand SARIF

SARIF is a standardized format for representing static analysis results.

Security tools can produce SARIF reports that compatible platforms can consume.

An illustrative workflow:

```yaml
permissions:
  contents: read
  security-events: write

steps:
  - name: Checkout
    uses: actions/checkout@v6

  - name: Run Trivy
    uses: aquasecurity/trivy-action@v0.36.0
    with:
      scan-type: fs
      scan-ref: .
      format: sarif
      output: trivy-results.sarif

  - name: Upload SARIF
    uses: github/codeql-action/upload-sarif@v4
    with:
      sarif_file: trivy-results.sarif
```

This is an illustrative fragment. Add it to a complete workflow and verify the current Action versions, required permissions, and repository eligibility.

The important distinction:

- Trivy performs the scan.
- SARIF represents the findings.
- The upload action submits the results.
- GitHub code-scanning integration displays the findings where eligible.

Generating SARIF does not automatically mean the findings block a merge.

You must configure enforcement separately.

## 10.5 Scan the exact image you publish

A professional container pipeline should scan the same image that will be published.

```text
Source Commit
     |
     v
Build Docker Image
     |
     v
Tag with Commit SHA
     |
     v
Scan Exact Image
     |
     +---- Findings
     |       |
     |       v
     |    Investigate
     |
     v
Security Policy Passed
     |
     v
Publish Image
     |
     v
Generate Provenance
```

Do not scan one image and publish a different build.

### Exercise 6 — Trivy

- [ ] Install Trivy.
- [ ] Scan a filesystem.
- [ ] Scan configuration files.
- [ ] Build a sample Docker image when an application Dockerfile is available.
- [ ] Scan the image.
- [ ] Generate a JSON report.
- [ ] Understand SARIF.
- [ ] Document vulnerability thresholds and exceptions.

Create:

`docs/github/module-04-actions/trivy-guide.md`

---

## 11. SonarQube — Code Quality and Security Analysis

SonarQube provides automated source-code analysis and reporting.

It can help identify:

- Bugs.
- Code smells.
- Security hotspots.
- Vulnerabilities.
- Duplicated code.
- Maintainability issues.
- Test coverage information.

## 11.1 Understand SonarQube terminology

| Term | Meaning |
|---|---|
| Bug | Potentially incorrect behavior |
| Vulnerability | A security weakness |
| Security hotspot | Code requiring security review |
| Code smell | Maintainability issue |
| Technical debt | Estimated effort to address maintainability problems |
| Quality Gate | Conditions that determine whether quality requirements pass |
| Coverage | Portion of code exercised by tests |

A security hotspot is not automatically a confirmed vulnerability. It requires review.

## 11.2 Quality Gates

Imagine your project defines the following example policies:

| Metric | Example policy |
|---|---|
| New bugs | 0 |
| New vulnerabilities | 0 |
| New code coverage | At least 80% |
| Duplicated lines | Below agreed threshold |
| Maintainability | Meets project target |

These are illustrative thresholds.

Define actual requirements according to project risk and testing strategy.

## 11.3 SonarQube pipeline architecture

```text
Pull Request
     |
     v
Checkout
     |
     v
Install Dependencies
     |
     v
Run Tests
     |
     v
Generate Coverage Report
     |
     v
SonarQube Analysis
     |
     v
Quality Gate Evaluation
     |
     +---- Failed
     |       |
     |       v
     |    Investigate
     |
     v
Passed
     |
     v
Continue Pipeline
```

The quality-gate evaluation is important.

Running a scanner alone does not guarantee that the pipeline blocks when the gate fails.

## 11.4 Configure SonarQube for Python

For your future Django backend, create:

`backend/sonar-project.properties`

Example:

```properties
sonar.projectKey=restaurant-pos-backend
sonar.projectName=Restaurant POS Backend

sonar.sources=.
sonar.tests=tests

sonar.python.version=3.12

sonar.python.coverage.reportPaths=coverage.xml

sonar.sourceEncoding=UTF-8
```

Adjust `sonar.tests` to match your real test directory.

The Python version should match the project's supported runtime.

The coverage report must exist before the analysis step.

## 11.5 Configure SonarQube for React

For the frontend, use a separate project configuration when maintaining separate SonarQube projects.

Example:

```properties
sonar.projectKey=restaurant-pos-frontend
sonar.projectName=Restaurant POS Frontend

sonar.sources=src
sonar.tests=src

sonar.test.inclusions=src/**/*.test.ts,src/**/*.test.tsx

sonar.javascript.lcov.reportPaths=coverage/lcov.info

sonar.sourceEncoding=UTF-8
```

This assumes your test setup generates an LCOV coverage report.

## 11.6 GitHub Actions integration

For SonarQube Cloud, a simplified example is:

```yaml
name: SonarQube Analysis

on:
  push:
    branches:
      - main

  pull_request:

permissions:
  contents: read

jobs:
  sonar:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Run tests and generate coverage
        run: |
          echo "Install dependencies and generate coverage here"

      - name: SonarQube scan
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

This is an integration skeleton, not a complete application pipeline.

You must:

1. Configure the project key.
2. Configure the selected SonarQube service.
3. Generate coverage reports.
4. Store the authentication token as a GitHub secret.
5. Verify the scanner's current version.
6. Configure and enforce the Quality Gate result.

For pull-request workflows, use the appropriate SonarQube integration and authentication model for your selected product.

## 11.7 Ruff vs SonarQube

| Ruff | SonarQube |
|---|---|
| Python linting | Multi-language analysis |
| Python formatting | Maintainability analysis |
| Fast developer feedback | Broader quality reporting |
| Python-focused | Cross-project reporting |
| Local and CI usage | CI and centralized platform |

For your backend, a sensible combination is:

- Ruff for Python linting and formatting.
- pytest for tests.
- Coverage for test coverage reporting.
- SonarQube for broader code-quality analysis.

### Exercise 7 — SonarQube

- [ ] Understand bugs, vulnerabilities, and code smells.
- [ ] Understand security hotspots.
- [ ] Create a sample Python configuration.
- [ ] Create a sample React configuration.
- [ ] Understand coverage reports.
- [ ] Explore SonarQube Cloud or a local environment.
- [ ] Understand the difference between scanning and enforcing a Quality Gate.

Create:

`docs/github/module-04-actions/sonarqube-guide.md`

---

## 12. Quality Gates in CI/CD

A quality gate is useful only when it influences the pipeline's outcome.

Consider these two cases.

### Case A — Reporting only

```text
Scan
  |
  v
Generate Report
  |
  v
Pipeline Continues
```

The report exists, but the pipeline does not enforce the result.

### Case B — Enforced policy

```text
Scan
  |
  v
Evaluate Policy
  |
  +---- Failed
  |       |
  |       v
  |    Block Merge
  |
  v
Passed
  |
  v
Continue
```

## 12.1 Required status checks

GitHub branch protection and rulesets can require selected status checks before merging.

For example:

- `repository-ci`
- `secret-scan`
- `dependency-review`
- `security-scan`
- `sonarqube-quality-gate`

Configure required checks only after confirming that they run reliably.

A check that is required but never runs can block all pull requests.

## 12.2 Exception management

Sometimes a team must accept a finding temporarily.

Document:

- Finding identifier.
- Affected component.
- Severity.
- Reason for the exception.
- Compensating controls.
- Responsible owner.
- Review date.
- Planned remediation.

Exceptions should have an owner and an expiry or review date.

Do not permanently ignore a vulnerability without a documented reason.

---

## 13. SBOM — Software Bill of Materials

An SBOM is an inventory of software components used to build an application.

Think of it as a structured list of the components inside your software.

Example:

```text
Restaurant POS Application
|
+-- Backend
|   +-- Django
|   +-- DRF
|   +-- Celery
|   +-- psycopg
|
+-- Frontend
|   +-- React
|   +-- Vite
|   +-- Axios
|   +-- TypeScript
|
+-- Container
    +-- Base operating system
    +-- Python runtime
    +-- System libraries
```

## 13.1 Why SBOM matters

An SBOM helps organizations:

- Identify dependencies.
- Understand third-party components.
- Investigate vulnerabilities.
- Track component versions.
- Support software supply-chain management.
- Provide transparency to customers and auditors.

An SBOM does not prove that software is secure.

It provides an inventory that can support security analysis.

## 13.2 Common SBOM formats

| Format | Description |
|---|---|
| SPDX | Standard for software package and license information |
| CycloneDX | Standard for software component and supply-chain information |

Both formats are used in professional software environments.

## 13.3 Generate an SBOM with Trivy

For a Docker image:

```powershell
trivy image --format cyclonedx --output sbom.json restaurant-pos-backend:local
```

For a filesystem:

```powershell
trivy fs --format cyclonedx --output sbom.json .
```

Inspect the generated report.

Check:

- Package names.
- Versions.
- Component identifiers.
- Dependency relationships where available.
- Metadata.
- Generation information.

## 13.4 Upload an SBOM as a GitHub artifact

Add this after the appropriate build or scan step:

```yaml
- name: Generate SBOM
  uses: aquasecurity/trivy-action@v0.36.0
  with:
    scan-type: fs
    scan-ref: .
    format: cyclonedx
    output: sbom.json

- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: application-sbom
    path: sbom.json
    retention-days: 30
```

For production:

- Pin Actions to verified SHAs.
- Generate the SBOM from the correct build or image.
- Associate it with the release artifact.
- Retain it according to your release and compliance policy.

### Exercise 8 — SBOM

- [ ] Generate a CycloneDX SBOM.
- [ ] Generate an SBOM for a Docker image when available.
- [ ] Inspect package names and versions.
- [ ] Compare SPDX and CycloneDX.
- [ ] Upload an SBOM as a workflow artifact.
- [ ] Document why an SBOM matters.

Create:

`docs/github/module-04-actions/sbom-guide.md`

---

## 14. Artifact Attestations

An SBOM describes software components.

Provenance describes how an artifact was produced.

An attestation is verifiable information associated with an artifact.

Example:

```text
Source Repository
      |
      v
Git Commit
      |
      v
GitHub Actions Workflow
      |
      v
Build Process
      |
      v
Application Artifact
      |
      v
Attestation
```

## 14.1 Why provenance matters

Suppose you receive a Docker image.

You want to know:

- Which repository produced it?
- Which commit was used?
- Which workflow built it?
- Which build process was involved?
- Can its claimed origin be verified?

Artifact provenance helps establish this information.

## 14.2 GitHub artifact attestations

GitHub supports artifact attestations through supported workflows and environments.

An illustrative file-based attestation workflow:

```yaml
permissions:
  contents: read
  id-token: write
  attestations: write

steps:
  - name: Checkout
    uses: actions/checkout@v6

  - name: Build application artifact
    run: |
      mkdir -p dist
      echo "Example build output" > dist/application.tar

  - name: Generate artifact attestation
    uses: actions/attest-build-provenance@v2
    with:
      subject-path: ./dist/application.tar
```

This example creates an illustrative file and attests to it.

For a real application:

- Build the actual artifact.
- Use the correct subject path.
- Confirm the required permissions.
- Check repository and platform eligibility.
- Pin Actions to verified SHAs.
- Verify the attestation after generation.

Container images require the appropriate container-image attestation configuration.

## 14.3 Verification matters

An attestation is useful only if consumers verify it.

Verification checks whether the artifact matches the claimed identity and provenance.

Do not treat the existence of an attestation file as proof that an artifact is safe.

It is evidence about origin and build process, not a guarantee that the source code is vulnerability-free.

---

## 15. Software Supply Chain Security

The software supply chain includes more than application source code.

It includes:

- Developers and contributors.
- Git repositories.
- GitHub Actions workflows.
- Third-party Actions.
- Package registries.
- Application dependencies.
- Build environments.
- Docker base images.
- Build artifacts.
- Deployment systems.

A weakness in any of these areas can affect the delivered application.

## 15.1 Supply-chain security controls

| Area | Control |
|---|---|
| Source code | Branch protection and code review |
| Workflow automation | Least privilege and SHA pinning |
| Dependencies | Dependabot and dependency review |
| Secrets | Secret scanning and credential rotation |
| Source analysis | CodeQL and SonarQube |
| Containers | Trivy and minimal base images |
| Component inventory | SBOM |
| Build origin | Artifact attestations |
| Deployment | Protected environments and approvals |

## 15.2 Secure the build process

A professional pipeline should:

1. Start from a trusted source revision.
2. Use reviewed workflow definitions.
3. Use pinned and reviewed Actions.
4. Install dependencies using lockfiles.
5. Run tests and security checks.
6. Build an artifact.
7. Scan the artifact.
8. Generate an SBOM.
9. Generate provenance where supported.
10. Publish only artifacts that pass the defined policy.

## 15.3 Avoid rebuilding different artifacts for deployment

A common mistake is:

1. Build and scan an artifact in CI.
2. Rebuild the application separately during deployment.
3. Deploy the second artifact.

The deployed artifact is no longer necessarily the artifact that passed the original checks.

Prefer promoting the same verified artifact through your environments.

---

## 16. Integrated DevSecOps Pipeline

Now combine the tools into a practical architecture for your future Django + React application.

```text
Developer
    |
    v
Pull Request
    |
    +---- Gitleaks
    |
    +---- Dependency Review
    |
    +---- Ruff / ESLint
    |
    +---- pytest / Vitest
    |
    +---- CodeQL
    |
    +---- SonarQube
    |
    v
Required CI Checks
    |
    v
Merge to Main
    |
    v
Build Docker Image
    |
    +---- Trivy Image Scan
    |
    +---- Generate SBOM
    |
    +---- Generate Provenance
    |
    v
Security Policy Evaluation
    |
    v
Publish Image
    |
    v
Protected Deployment Environment
    |
    v
Approved Deployment
```

## 16.1 Tool responsibilities

| Tool | Responsibility |
|---|---|
| Ruff | Python linting and formatting |
| pytest | Backend testing |
| ESLint | JavaScript and TypeScript linting |
| Vitest | Frontend testing |
| CodeQL | SAST |
| Dependabot | Dependency maintenance |
| Dependency Review | Review dependency changes in pull requests |
| Gitleaks | Secret detection |
| SonarQube | Code quality and security analysis |
| Trivy | Vulnerability and configuration scanning |
| CycloneDX | SBOM format |
| SPDX | SBOM format |
| GitHub Attestations | Build provenance |

Avoid duplicating tools without a reason.

For example, CodeQL and SonarQube overlap in some analysis areas, but their capabilities and reporting are not identical.

## 16.2 Example application CI workflow architecture

This is a conceptual example for a future repository with actual backend and frontend directories.

```text
backend/
    requirements.txt
    manage.py
    tests/

frontend/
    package.json
    package-lock.json
    src/

.github/
    workflows/
```

A backend quality job might run:

```yaml
- name: Install backend dependencies
  run: pip install -r backend/requirements.txt

- name: Ruff
  run: ruff check backend/

- name: Django checks
  run: python backend/manage.py check

- name: pytest
  run: pytest backend/tests/
```

The actual commands depend on your dependency management, Django settings, and test configuration.

A frontend quality job might run:

```yaml
- name: Install frontend dependencies
  working-directory: frontend
  run: npm ci

- name: Lint
  working-directory: frontend
  run: npm run lint

- name: Type check
  working-directory: frontend
  run: npm run typecheck

- name: Test
  working-directory: frontend
  run: npm run test

- name: Build
  working-directory: frontend
  run: npm run build
```

These commands assume the corresponding scripts exist in `package.json`.

Do not copy them into the documentation-only training repository as if they were executable there.

---

## 17. GitHub Repository Security Configuration

Now inspect your training repository's settings.

Navigate to:

```text
Repository
    |
    v
Settings
    |
    v
Security and analysis
```

Review the features available to your repository.

## 17.1 Private repository feature availability

Feature availability depends on repository visibility, ownership, and GitHub plan.

| Feature | What to check |
|---|---|
| GitHub Actions | Usage limits and available functionality |
| Dependency graph | Whether enabled |
| Dependabot alerts | Whether enabled and available |
| Dependabot security updates | Whether available |
| Dependabot version updates | Configuration file |
| CodeQL code scanning | Code Security eligibility |
| Secret scanning | Secret Protection eligibility |
| Push protection | Secret Protection eligibility |
| Gitleaks | Independent CI/local usage |
| Trivy | Independent CI/local usage |
| SonarQube | Selected SonarQube product and plan |

Do not assume that a feature is available merely because it appears in a tutorial.

Check your repository's actual settings and the current GitHub documentation.

## 17.2 What you can learn without upgrading GitHub

You can learn a substantial amount of DevSecOps without purchasing additional GitHub security features.

For example:

- Gitleaks can run locally and in Actions.
- Trivy can run locally and in Actions.
- Dependabot version updates can be configured.
- GitHub Actions permissions can be reviewed.
- SBOMs can be generated independently.
- SonarQube can be explored separately.
- Docker images can be scanned locally.

Some native GitHub security integrations may require additional eligibility.

---

## 18. Practical Assignments

We'll divide the exercises into three levels.

## Level 1 — Security Fundamentals

- [ ] Review all GitHub Actions permissions.
- [ ] Understand full-SHA Action pinning.
- [ ] Review dangerous workflow triggers.
- [ ] Understand shell-injection risks.
- [ ] Install and run Gitleaks locally.
- [ ] Configure Dependabot for GitHub Actions.
- [ ] Understand SAST, DAST, and SCA.

## Level 2 — Security Automation

- [ ] Create a Gitleaks workflow.
- [ ] Create a Trivy filesystem workflow.
- [ ] Configure Dependabot version updates.
- [ ] Study CodeQL default and advanced setup.
- [ ] Understand Dependency Review.
- [ ] Generate a CycloneDX SBOM.
- [ ] Create a SonarQube configuration.
- [ ] Document the available GitHub security features.

## Level 3 — Professional DevSecOps

- [ ] Integrate security scans into CI.
- [ ] Configure quality gates.
- [ ] Scan Docker images.
- [ ] Configure vulnerability severity policies.
- [ ] Understand artifact attestations.
- [ ] Create a security-focused deployment architecture.
- [ ] Document a vulnerability remediation process.

## Final practical project

Create a security documentation package for your future restaurant POS application.

Your documentation must explain:

1. How source code is reviewed.
2. Which workflows have write permissions.
3. How third-party Actions are pinned.
4. How secrets are detected.
5. How dependencies are updated.
6. How SAST is performed.
7. How Docker images are scanned.
8. How the SBOM is generated.
9. How provenance is established.
10. Which findings block deployment.
11. How security exceptions are approved.
12. How vulnerabilities are remediated.

---

## 19. Troubleshooting and Real-World Scenarios

| Problem | Possible cause | Investigation |
|---|---|---|
| CodeQL cannot start | Repository not eligible or workflow configuration issue | Check Code Security settings and workflow logs |
| Dependabot creates no PRs | Incorrect ecosystem or directory | Inspect `dependabot.yml` and dependency manifests |
| Gitleaks reports a secret | Potential exposed credential | Investigate and rotate real credentials |
| Trivy fails | Configured threshold reached or scan error | Inspect the report and scanner logs |
| SonarQube fails | Quality Gate or scanner configuration | Inspect individual metrics and analysis logs |
| Dependency Review fails | Vulnerable dependency introduced | Review the dependency changes |
| SARIF upload fails | Missing permissions or repository eligibility | Check `security-events: write` and platform support |
| SBOM is empty | Incorrect scan target or missing build output | Inspect the scanner input |
| Attestation fails | Missing permissions or unsupported configuration | Inspect OIDC and attestation setup |
| Pipeline passes despite findings | Findings are not configured as blocking | Review exit codes and gate enforcement |

## Scenario Exercise — Vulnerable dependency

Imagine your future restaurant POS application uses a vulnerable Python dependency.

Dependabot creates a pull request.

Your pipeline runs:

1. Dependency Review.
2. Ruff.
3. pytest.
4. CodeQL, if available.
5. SonarQube.
6. Docker build.
7. Trivy.

The developer reviews the update, verifies compatibility, and merges only after the required checks pass.

Write an incident-style report explaining:

- What was detected?
- Which component was affected?
- What was the risk?
- What did the developer change?
- Which tests were executed?
- How was the correction verified?
- Was an SBOM regenerated?
- Was the released artifact rebuilt and rescanned?

---

## 20. Documentation Deliverables

Create the following files manually using your existing repository conventions.

Main lesson:

`docs/github/module-04-actions/lesson-36-ci-cd-security.md`

Supporting documents:

| Filename | Content |
|---|---|
| `workflow-security-review.md` | Permissions, triggers, Action pinning |
| `dependabot-guide.md` | Alerts, security updates, version updates |
| `gitleaks-guide.md` | Secret scanning and remediation |
| `codeql-guide.md` | SAST and CodeQL |
| `trivy-guide.md` | Filesystem, image, and configuration scanning |
| `sonarqube-guide.md` | Code quality and Quality Gates |
| `sbom-guide.md` | SPDX and CycloneDX |
| `supply-chain-security.md` | Provenance and attestations |

The main lesson should contain the complete learning path.

The supporting documents should become focused reference guides rather than duplicated copies of the entire lesson.

## Recommended repository structure

```text
github-deep-dive-training/
|
+-- .github/
|   +-- dependabot.yml
|   |
|   +-- workflows/
|       +-- repository-ci.yml
|       +-- gitleaks.yml
|       +-- trivy.yml
|       +-- dependency-review.yml
|       +-- codeql.yml
|
+-- docs/
    +-- github/
        +-- module-04-actions/
            +-- lesson-34-github-actions-fundamentals.md
            +-- lesson-35-advanced-github-actions.md
            +-- lesson-36-ci-cd-security.md
            |
            +-- workflow-security-review.md
            +-- dependabot-guide.md
            +-- gitleaks-guide.md
            +-- codeql-guide.md
            +-- trivy-guide.md
            +-- sonarqube-guide.md
            +-- sbom-guide.md
            +-- supply-chain-security.md
```

**Important:** The workflow files are practical exercises. Add them selectively, validate them, and avoid enabling application-specific workflows until the required application files exist.

---

## 21. Git Workflow — Commit, Pull Request, Tag and Release

Continue using your established GitHub training workflow.

## Step 1 — Inspect your repository

```powershell
git status
git branch --show-current
git fetch origin
```

Make sure you have no uncommitted work that could be accidentally mixed into this lesson.

## Step 2 — Update main

```powershell
git switch main
git pull --ff-only origin main
```

If the pull fails because your local and remote branches have diverged, stop and reconcile the branch history before continuing. Do not force-push to make the error disappear.

## Step 3 — Create a branch

```powershell
git switch -c docs/lesson-36-devsecops
```

## Step 4 — Add documentation and workflows

Add only the files you actually created:

```powershell
git add docs/github/module-04-actions/
```

If you created and reviewed workflow files:

```powershell
git add .github/
```

## Step 5 — Validate

```powershell
git status
git diff --check
git diff --cached
```

Review the workflow permissions, triggers, Action references, and configuration files.

For YAML workflows, use a suitable YAML or GitHub Actions validator as an additional check. A successful `git diff --check` does not validate workflow syntax.

## Step 6 — Commit

```powershell
git commit -m "docs(github): add Lesson 36 DevSecOps deep dive"
```

## Step 7 — Push

```powershell
git push -u origin docs/lesson-36-devsecops
```

## Step 8 — Create a Pull Request

### PR title

```text
docs(github): add Lesson 36 DevSecOps deep dive
```

### PR description

```markdown
## Summary

Add comprehensive documentation and practical exercises for GitHub Actions security and DevSecOps.

## Topics

- GitHub Actions security
- Least-privilege permissions
- Full-SHA Action pinning
- SAST and CodeQL
- Dependabot and Dependency Review
- Gitleaks and secret detection
- Trivy and container security
- SonarQube and quality gates
- SBOM and CycloneDX
- Artifact attestations
- Software supply-chain security

## Validation

- [ ] Documentation reviewed
- [ ] Workflow permissions reviewed
- [ ] Dependabot configuration validated
- [ ] Gitleaks tested
- [ ] Trivy tested
- [ ] SBOM generation tested where applicable
- [ ] Private repository limitations documented
- [ ] No real credentials committed
```

## Step 9 — Review and merge

Practice the collaboration workflow:

1. Open the PR.
2. Review the changed files.
3. Inspect the workflow YAML.
4. Leave at least one review comment.
5. Resolve the comment.
6. Approve the PR.
7. Merge it using your repository's established merge strategy.

## Step 10 — Tag the lesson

After the PR has been merged:

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
```

Create an annotated tag:

```powershell
git tag -a module-04-lesson-36 -m "Module 4 - Lesson 36: CI/CD Security and DevSecOps"
```

Push it:

```powershell
git push origin module-04-lesson-36
```

## Step 11 — Create the GitHub Release

| Field | Value |
|---|---|
| Tag | `module-04-lesson-36` |
| Title | Module 4 — Lesson 36: DevSecOps |
| Target | `main` |

### Release notes

```markdown
# Module 4 — Lesson 36: DevSecOps

Completed the advanced CI/CD security and software supply-chain security deep dive.

## Topics covered

- GitHub Actions security
- Least-privilege permissions
- Full-SHA Action pinning
- SAST and CodeQL
- Dependabot
- Dependency Review
- Gitleaks
- Secret scanning
- Trivy
- SonarQube
- Quality Gates
- SBOM and CycloneDX
- Artifact attestations
- Supply-chain provenance
- Integrated DevSecOps architecture

## Practical deliverables

- Workflow security review
- Dependabot configuration
- Secret detection workflow
- Trivy scanning workflow
- SBOM generation examples
- DevSecOps documentation

## Training checkpoint

module-04-lesson-36
```

---

## 22. Key Takeaways

After completing this lesson, you should understand the following:

1. DevSecOps integrates security into the development and delivery process.
2. GitHub Actions workflows must use least-privilege permissions.
3. Third-party Actions should be pinned to verified immutable references in production.
4. `pull_request_target` requires special care because of its privileged context.
5. SAST analyzes source code.
6. SCA analyzes third-party dependencies.
7. Dependabot helps maintain dependencies and address known vulnerabilities.
8. Gitleaks detects potential exposed credentials.
9. Trivy scans filesystems, containers, and configuration.
10. SonarQube provides code-quality and security analysis.
11. Quality gates must enforce actual pipeline decisions.
12. An SBOM describes the software components used.
13. Provenance describes how an artifact was produced.
14. Attestations provide verifiable information about artifact origin.
15. A secure pipeline must validate the same artifact that is ultimately published and deployed.

**Completion target:** Complete Level 1, configure Dependabot and Gitleaks where applicable, understand Trivy, and document the security capabilities available to your private training repository.

---

## 23. Official Documentation

Bookmark these official resources.

| Technology | Documentation |
|---|---|
| GitHub repository security | [Securing your repository](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository) |
| GitHub Actions security | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| GitHub Actions permissions | [Workflow permissions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| CodeQL | [Code scanning setup types](https://docs.github.com/en/code-security/concepts/code-scanning/setup-types) |
| Advanced CodeQL | [Advanced setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning) |
| Dependabot | [Configure version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file) |
| Dependabot security | [About security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/about-dependabot-security-updates) |
| Dependency Review | [Dependency Review Action](https://github.com/actions/dependency-review-action) |
| Gitleaks | [Official repository](https://github.com/gitleaks/gitleaks) |
| Trivy | [Official documentation](https://trivy.dev/) |
| Trivy Action | [GitHub repository](https://github.com/aquasecurity/trivy-action) |
| SonarQube | [Official documentation](https://docs.sonarsource.com/) |
| CycloneDX | [Official website](https://cyclonedx.org/) |
| SPDX | [Official website](https://spdx.dev/) |
| GitHub attestations | [Artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations) |

---

## Next Lesson — Lesson 37

## GitHub Actions Runners, Self-Hosted Infrastructure & Enterprise Automation

We'll move from securing workflows to understanding the infrastructure that executes them.

### Planned topics

1. GitHub-hosted runner architecture.
2. Self-hosted runner architecture.
3. Runner registration and configuration.
4. Runner groups and labels.
5. Linux runner administration.
6. Windows and macOS runners.
7. Ephemeral runners.
8. Docker-based runners.
9. Runner isolation and security.
10. Runner networking and firewall considerations.
11. Private network access.
12. Scaling runners.
13. Actions Runner Controller (ARC).
14. Kubernetes-based runners.
15. Runner monitoring and troubleshooting.
16. Enterprise runner management.
17. Cost optimization.
18. Designing a self-hosted runner environment for your DRF + React projects.

**Lesson 36 checkpoint:** Understand the security architecture, complete the Level 1 exercises, configure Dependabot and Gitleaks, and document your private repository's feature limitations.

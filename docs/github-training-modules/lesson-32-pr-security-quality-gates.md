# Module 3 — GitHub Pull Requests

## Lesson 32: GitHub Pull Request Security and Quality Gates

**Level:** Advanced
**Estimated time:** 3–4 hours
**Type:** Practical lesson
**Repository:** `github-deep-dive-training`

---

## Introduction

In Lesson 31, you learned how to automate and govern Pull Requests using:

- Pull Request templates.
- CODEOWNERS.
- Branch protection and rulesets.
- Required reviews.
- GitHub Actions automation.
- Merge policies and governance.

Now we move to another important question:

**How do we prevent vulnerable, malicious, or low-quality code from being merged into our repository?**

Imagine that your restaurant management application has this architecture:

- Django REST Framework backend.
- React/Vite frontend.
- PostgreSQL database.
- Docker infrastructure.
- GitHub Actions CI/CD.
- External dependencies and packages.

A developer opens a Pull Request that introduces:

- A vulnerable Python dependency.
- An accidentally committed API credential.
- An insecure authentication implementation.
- A potentially dangerous GitHub Actions workflow.
- Code that violates your project's quality standards.

A professional repository needs mechanisms to identify these problems before code reaches the protected branch.

This is where **DevSecOps**, security scanning, dependency management, and quality gates become part of the Pull Request workflow.

Throughout this lesson, we'll use your training repository to practise the concepts without requiring you to build the complete restaurant application.

## 1. Learning Objectives

By the end of this lesson, you should understand and practise:

1. Pull Request security architecture.
2. Fork-based Pull Request security.
3. `pull_request` versus `pull_request_target`.
4. GitHub Actions security and least privilege.
5. `GITHUB_TOKEN` permissions.
6. GitHub Actions secrets and variables.
7. Dependabot alerts and security updates.
8. Dependabot version updates.
9. Dependency Review.
10. CodeQL and Static Application Security Testing (SAST).
11. Secret scanning and push protection.
12. Gitleaks and local secret detection.
13. SonarQube and code quality analysis.
14. Security quality gates.
15. GitHub Actions security validation.
16. Repository security policies.
17. Required status checks and merge enforcement.
18. Building a secure PR validation architecture.

---

## 2. Understand Pull Request Security Architecture

Before configuring individual tools, understand how security checks fit into the Pull Request lifecycle.

### 2.1 Secure Pull Request lifecycle

A typical secure PR process looks like this:

```text
Developer creates a Pull Request
              |
              v
       PR validation starts
              |
              v
    Dependency security review
              |
              v
       Secret detection
              |
              v
     Static code analysis
              |
              v
       Code quality checks
              |
              v
      Automated application tests
              |
              v
       Security and code review
              |
              v
         Quality gates
              |
              v
     Required checks are passed
              |
              v
       Authorized merge
              |
              v
       Protected main branch
```

Each stage has a different responsibility.

For example:

- Dependency Review checks dependency changes.
- Gitleaks searches for potentially exposed secrets.
- CodeQL analyzes source code for security vulnerabilities.
- SonarQube evaluates code quality and security-related findings.
- GitHub Actions runs the automated pipeline.
- Branch protection or rulesets enforce the required checks.

The objective is not to install every security tool available.

The objective is to build a security process in which each tool has a clear responsibility.

### 2.2 Security tools and their responsibilities

| Tool | Main responsibility |
|---|---|
| Dependabot alerts | Report known vulnerable dependencies |
| Dependabot security updates | Create PRs to update vulnerable dependencies |
| Dependabot version updates | Keep dependencies updated |
| Dependency Review | Examine dependency changes introduced by PRs |
| CodeQL | Analyze source code for security vulnerabilities |
| Secret Scanning | Detect supported exposed credentials |
| Push Protection | Block supported secret leaks before they reach GitHub |
| Gitleaks | Detect potential secrets in Git repositories |
| SonarQube | Analyze code quality and security-related findings |
| GitHub Actions | Automate validation and security checks |
| Branch protection | Enforce required reviews and checks |

### 2.3 Understand the different security testing categories

These concepts are related, but they are not interchangeable.

| Category | What it examines | Example |
|---|---|---|
| SAST | Application source code | CodeQL, Bandit |
| SCA | Third-party software components | Dependency analysis |
| Secret scanning | Credentials and tokens | Gitleaks, GitHub Secret Scanning |
| DAST | A running application | Testing an application through its interfaces |
| Code quality analysis | Maintainability and code quality | SonarQube, Ruff, ESLint |

**Important distinction:**

- SAST examines your own source code.
- SCA examines third-party components and their associated risks.
- Secret scanning searches for exposed credentials.
- DAST evaluates a running application.
- Code quality analysis evaluates maintainability, duplication, and other engineering standards.

These techniques complement one another. None replaces all the others.

---

## 3. Fork-Based Pull Request Security

This is one of the most important topics in GitHub Actions security.

### 3.1 What is a fork?

A fork is an independent copy of another GitHub repository.

For example:

```text
Original repository:
yassine-B/github-deep-dive-training
                |
                v
Contributor creates a fork:
contributor/github-deep-dive-training
                |
                v
Contributor makes changes
                |
                v
Contributor opens a Pull Request
                |
                v
Original repository receives the PR
```

The contributor can propose changes without having direct write access to the original repository.

This is a fundamental part of open-source collaboration.

### 3.2 Why are fork PRs a security concern?

Imagine an external contributor submits a PR modifying:

```text
.github/workflows/test.yml
package.json
requirements.txt
```

These files can influence what GitHub Actions executes.

For example:

- A workflow can define shell commands.
- A package manifest can define installation scripts.
- A test configuration can execute custom commands.
- A build script can run arbitrary project code.

If an automated workflow exposes privileged credentials while executing untrusted code, those credentials could be compromised.

The important principle is:

**A Pull Request is proposed code, not automatically trusted code.**

### 3.3 How GitHub protects fork-based PRs

For the standard `pull_request` event, GitHub generally applies protections to workflows triggered by fork PRs:

- The workflow receives a restricted, read-only `GITHUB_TOKEN`.
- Repository and organization secrets are not provided to the fork PR workflow.
- Fork approval policies can control when workflows are allowed to run.
- The workflow runs in the context of the PR merge commit.

These restrictions reduce the risk of untrusted contributions accessing privileged repository resources.

### 3.4 Practical example

Create:

```text
.github/workflows/pr-validation.yml
```

Example:

```yaml
name: PR Validation

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate:
    name: Validate Pull Request
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Validate repository
        run: echo "Running PR validation"
```

This is a suitable starting point for ordinary PR validation.

Notice that the workflow:

- Uses `pull_request`.
- Only grants repository content read access.
- Does not request deployment credentials.
- Does not grant unnecessary write permissions.

The example is intentionally simple. Later lessons will expand the validation pipeline.

### 3.5 Trust scenarios

| Scenario | Security consideration |
|---|---|
| PR from your own feature branch | Still requires validation |
| PR from an external fork | Treat the contribution as untrusted |
| PR modifies a workflow file | Review carefully |
| PR modifies package installation scripts | Review carefully |
| PR requests deployment secrets | Do not expose secrets to untrusted code |
| PR changes authentication logic | Require appropriate technical review |

A PR from your own account is not automatically safe. Your account could be compromised, or your branch could contain unsafe changes.

### Exercise 1 — Understand fork-based security

Create:

```text
docs/github/module-03-pull-requests/fork-pr-security.md
```

Document:

1. What is a GitHub fork?
2. How does a fork-based PR work?
3. Why is a fork considered an untrusted contribution?
4. What restrictions apply to fork-based `pull_request` workflows?
5. Why should PR workflows avoid deployment secrets?
6. Why should workflow-file changes receive careful review?

---

## 4. `pull_request` vs `pull_request_target`

### Advanced security concept

These two GitHub Actions events have different security models.

Understanding their differences is essential when designing workflows that respond to external contributions.

### 4.1 The `pull_request` event

Example:

```yaml
name: PR Tests

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Run tests
        run: echo "Running PR tests"
```

Characteristics:

- Designed for Pull Request validation.
- Runs the workflow associated with the PR merge commit.
- Fork PRs receive restricted token permissions.
- Repository secrets are withheld from fork PR workflows.
- Suitable for ordinary testing and validation.

This should be your default choice for ordinary PR validation.

### 4.2 The `pull_request_target` event

This event is designed for certain PR-related automation tasks that need the base repository's security context.

For example:

- Applying labels.
- Managing PR metadata.
- Responding to PR events.
- Performing trusted triage automation.

Example:

```yaml
name: PR Metadata

on:
  pull_request_target:
    types:
      - opened
      - labeled

permissions:
  pull-requests: write

jobs:
  metadata:
    runs-on: ubuntu-latest

    steps:
      - name: Display PR information
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          printf 'PR number: %s\n' "$PR_NUMBER"
          printf 'PR title: %s\n' "$PR_TITLE"
```

Characteristics:

- Runs workflow code from the base repository's default branch.
- Uses the base repository's security context.
- Can access repository secrets and a more privileged token, depending on configuration.
- Does not automatically execute code from the fork.

The final point is extremely important.

### 4.3 The dangerous mistake

Consider this pattern:

```yaml
# INSECURE EXAMPLE — DO NOT USE

on:
  pull_request_target:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
        with:
          ref: ${{ github.event.pull_request.head.sha }}

      - name: Execute PR code
        run: make test
```

Why is this dangerous?

1. The workflow is triggered using `pull_request_target`.
2. The workflow receives the base repository's privileged security context.
3. The checkout step retrieves code supplied by the contributor.
4. The following command executes code from that contribution.
5. That code may run in an environment with access to sensitive resources.

This vulnerability pattern is commonly called a **pwn request**.

The checkout step alone does not execute the untrusted code. The danger occurs when subsequent build, test, installation, or other commands execute it in the privileged environment.

**Never casually combine `pull_request_target` with checking out and executing untrusted PR code.**

### 4.4 Comparison

| Property | `pull_request` | `pull_request_target` |
|---|---|---|
| Workflow source | PR merge commit | Base default branch |
| Fork PR token | Restricted | Base repository context |
| Fork PR secrets | Withheld | Can be available |
| Ordinary PR testing | Suitable | Avoid for this purpose |
| PR metadata automation | Suitable for many cases | Useful for privileged metadata automation |
| Security sensitivity | Normal PR precautions | High |

### 4.5 The rule to remember

Use:

```yaml
on:
  pull_request:
```

for ordinary testing and validation.

Use:

```yaml
on:
  pull_request_target:
```

only when you genuinely need the privileged context and understand how to isolate untrusted input.

Do not execute code from an untrusted PR in a privileged `pull_request_target` workflow.

Official documentation:

[Secure use of pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target)

### Exercise 2 — Compare the two events

Create:

```text
docs/github/module-03-pull-requests/pull-request-events-security.md
```

Document:

1. How `pull_request` works.
2. How `pull_request_target` works.
3. Why their workflow sources differ.
4. Why `pull_request_target` is more sensitive.
5. What a pwn request is.
6. When you should use each event.
7. How you would review a workflow that uses `pull_request_target`.

---

## 5. GitHub Actions Security

Now let's examine how to secure the workflows themselves.

A workflow is executable automation. It should be treated as application code that requires security review.

### 5.1 Apply the principle of least privilege

The principle of least privilege means granting only the permissions necessary to perform a specific task.

For example:

```yaml
permissions:
  contents: read
```

This grants read access to repository contents.

A different workflow might require:

```yaml
permissions:
  contents: read
  pull-requests: write
```

This is appropriate only when the workflow genuinely needs to modify PR information.

Avoid granting broad permissions simply because an action might need them.

### 5.2 Understand `GITHUB_TOKEN`

GitHub automatically creates a token for workflow runs.

Its name is:

```text
GITHUB_TOKEN
```

It allows workflows to interact with GitHub according to the permissions granted to the token.

For example:

```yaml
permissions:
  contents: read
```

A workflow that only checks out repository files usually needs no more than this permission.

Another example:

```yaml
permissions:
  contents: read
  security-events: write
```

This may be required by a workflow that uploads code-scanning results.

The exact permissions depend on the action and the operation being performed.

### 5.3 Common permissions

| Permission | Responsibility |
|---|---|
| `contents: read` | Read repository contents |
| `contents: write` | Modify repository contents |
| `pull-requests: read` | Read PR information |
| `pull-requests: write` | Modify PR information |
| `issues: write` | Create or modify issues |
| `checks: write` | Publish check information |
| `security-events: write` | Upload code-scanning results |

Not every workflow needs all these permissions.

### 5.4 Job-level permissions

You can also define permissions at the job level.

Example:

```yaml
name: PR Automation

on:
  pull_request_target:
    types:
      - opened

permissions: {}

jobs:
  label:
    runs-on: ubuntu-latest

    permissions:
      pull-requests: write

    steps:
      - name: Display event
        run: echo "PR metadata workflow"
```

This makes the permission boundary clearer.

A production workflow should use the narrowest permissions possible at the workflow and job levels.

### 5.5 Protect workflow dependencies

GitHub Actions workflows frequently use third-party actions.

For example:

```yaml
- uses: actions/checkout@v6
```

A major-version reference is convenient, but production environments can use a full verified commit SHA to pin an action to a specific revision.

Example format:

```yaml
- uses: owner/action@FULL_40_CHARACTER_COMMIT_SHA
```

The placeholder above is not a real SHA. Replace it only with a verified commit from the action's official repository.

Also:

- Review the action's source code and maintainers.
- Prefer trusted actions.
- Avoid unnecessary third-party actions.
- Use Dependabot to monitor action updates.
- Do not assume that an action is safe simply because it is popular.

### 5.6 Other workflow security concerns

Review workflows for:

- Untrusted input passed directly into shell commands.
- Excessive token permissions.
- Unnecessary secrets.
- Untrusted code executed in privileged jobs.
- Unverified third-party actions.
- Unsafe artifact handling.
- Persistent self-hosted runners exposed to untrusted jobs.
- Sensitive information printed in logs.

### Exercise 3 — Workflow security review

Create:

```text
docs/github/module-03-pull-requests/github-actions-security.md
```

Document:

1. What is the principle of least privilege?
2. What is `GITHUB_TOKEN`?
3. What are workflow-level permissions?
4. What are job-level permissions?
5. Why should third-party actions be reviewed?
6. What is action pinning?
7. Why is untrusted input dangerous in shell commands?

---

## 6. GitHub Actions Secrets and Variables

Imagine your restaurant application uses:

```text
DATABASE_URL
DJANGO_SECRET_KEY
EMAIL_PASSWORD
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
API_TOKEN
```

These values should not be hardcoded in your repository.

### 6.1 GitHub Actions secrets

GitHub Actions secrets are designed for sensitive values.

Navigate to:

#### Repository → Settings → Secrets and variables → Actions

You can create repository-level secrets and, where supported, use environment-level or organization-level secrets.

Example:

```yaml
steps:
  - name: Demonstrate secret injection
    env:
      API_TOKEN: ${{ secrets.API_TOKEN }}
    run: echo "The application configuration is available"
```

This is a demonstration of environment-variable injection.

Do not print the value of a secret.

### 6.2 GitHub Actions variables

Variables are intended for non-sensitive configuration.

Example:

```yaml
env:
  APP_ENV: ${{ vars.APP_ENV }}
```

A variable might contain:

```text
APP_ENV=staging
```

A secret might contain an API credential.

### 6.3 Secrets versus variables

| GitHub Secrets | GitHub Variables |
|---|---|
| Sensitive information | Non-sensitive configuration |
| Intended for credentials | Intended for application settings |
| Masked in logs when recognized | Not treated as confidential |
| Example: API token | Example: environment name |

### 6.4 Important security considerations

Secret masking is not a guarantee that credentials cannot leak.

Avoid:

- Printing secrets.
- Passing secrets to untrusted scripts.
- Exposing secrets to fork-based PR workflows.
- Storing credentials in source code.
- Including credentials in screenshots or documentation.
- Reusing the same credentials across unrelated environments.

If a real credential is exposed, treat it as compromised and rotate or revoke it with the provider.

### Exercise 4 — Create a secrets policy

Create:

```text
docs/github/module-03-pull-requests/security-secrets-policy.md
```

Document:

1. What is `GITHUB_TOKEN`?
2. Why should workflows use least privilege?
3. What are GitHub Actions secrets?
4. What are GitHub Actions variables?
5. Why should fork PRs not receive deployment secrets?
6. What is the difference between `pull_request` and `pull_request_target`?
7. What should happen when a credential is exposed?

Do not add real credentials to your training repository.

---

## 7. Dependabot — Dependency Vulnerability Management

Your application depends on external libraries.

For example, the Django backend might use:

```text
Django
djangorestframework
Pillow
psycopg
celery
channels
```

The React frontend might use:

```text
react
vite
axios
zustand
@tanstack/react-query
```

These dependencies can contain security vulnerabilities.

Dependabot helps you identify and manage dependency risks.

### 7.1 Understand the three main Dependabot features

| Feature | Responsibility |
|---|---|
| Dependency graph | Identifies project dependencies |
| Dependabot alerts | Reports known vulnerable dependencies |
| Dependabot security updates | Opens PRs to fix vulnerable dependencies |
| Dependabot version updates | Keeps dependencies updated even without known vulnerabilities |

### 7.2 How a security update works

```text
Your project uses a dependency
             |
             v
A security advisory is published
             |
             v
Dependabot identifies an affected version
             |
             v
A security alert is generated
             |
             v
Dependabot creates an update PR
             |
             v
Your CI pipeline validates the update
             |
             v
You review the changes
             |
             v
You merge after validation
```

Dependabot security updates depend on the dependency graph and Dependabot alerts being available and enabled.

### 7.3 Enable Dependabot

Navigate to:

#### Repository → Settings → Advanced Security

Review the available options:

- Dependency graph.
- Dependabot alerts.
- Dependabot security updates.

You can also inspect the repository's Security tab.

Feature availability depends on repository type, visibility, and GitHub plan.

### 7.4 Configure Dependabot version updates

Create:

```text
.github/dependabot.yml
```

Your training repository contains GitHub Actions workflow files, so start with the GitHub Actions ecosystem:

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

This configuration monitors dependencies referenced by GitHub Actions workflows.

When you later build the Django + React application, you can add other ecosystems using the actual locations of your manifests.

For example:

```yaml
# Example for a project with a backend requirements file

- package-ecosystem: pip
  directory: /backend
  schedule:
    interval: weekly
```

```yaml
# Example for a project with a frontend package.json

- package-ecosystem: npm
  directory: /frontend
  schedule:
    interval: weekly
```

These examples are illustrative. Do not configure nonexistent directories in a real repository.

### 7.5 Understand the configuration

| Property | Meaning |
|---|---|
| `version` | Dependabot configuration format |
| `updates` | List of package ecosystems |
| `package-ecosystem` | Dependency manager |
| `directory` | Location of dependency manifests |
| `schedule` | Update frequency |
| `labels` | Labels applied to update PRs |
| `commit-message` | Commit message configuration |

### 7.6 Review Dependabot-generated PRs

Suppose Dependabot creates:

```text
chore(deps): bump dependency from X to Y
```

Your review process should include:

1. Inspect the dependency changes.
2. Read the associated security advisory if applicable.
3. Review the version change.
4. Check compatibility.
5. Run automated tests.
6. Inspect breaking changes.
7. Merge only after validation.

Never blindly merge dependency updates.

An updated package can fix a vulnerability but also introduce compatibility problems.

### Exercise 5 — Configure Dependabot

In your training repository:

1. Create `.github/dependabot.yml`.
2. Configure the GitHub Actions ecosystem.
3. Validate the YAML.
4. Commit the configuration.
5. Open a PR.
6. Review the resulting repository configuration.

If Dependabot does not immediately open a PR, that is not necessarily a configuration error. It creates update PRs according to its schedule and the dependencies it detects.

References:

- [Dependabot](https://docs.github.com/en/code-security/dependabot)
- [Dependabot security updates](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates)

---

## 8. Dependency Review — Inspect Dependencies Before Merging

Dependabot helps manage dependencies, but we also want to inspect dependency changes introduced by individual PRs.

This is where **Dependency Review** becomes useful.

### 8.1 Example

A developer opens a PR modifying:

```text
backend/requirements.txt
frontend/package-lock.json
```

Dependency Review can examine changes such as:

- Added dependencies.
- Removed dependencies.
- Updated dependencies.
- Known vulnerabilities.
- License information.

This helps reviewers understand the supply-chain impact of a PR.

### 8.2 Create the workflow

Create:

```text
.github/workflows/dependency-review.yml
```

Example:

```yaml
name: Dependency Review

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  dependency-review:
    name: Dependency Security Review
    runs-on: ubuntu-latest

    steps:
      - name: Review dependency changes
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
```

This example uses the Dependency Review Action to fail the check when qualifying newly introduced vulnerabilities meet the configured severity threshold.

The workflow requires an eligible repository and a dependency graph. Availability for private repositories depends on GitHub Code Security entitlement.

### 8.3 Understand severity levels

| Severity | General interpretation |
|---|---|
| Critical | Extremely serious vulnerability |
| High | Serious vulnerability |
| Moderate | Meaningful security concern |
| Low | Lower-severity security concern |

You can choose a threshold according to your organization's risk policy.

For a production application, do not automatically ignore moderate or low findings. Assess their impact and relevance.

### 8.4 Practical exercise

If your repository and plan support Dependency Review:

1. Create the workflow.
2. Open a PR that changes a dependency manifest or lock file.
3. Observe the workflow result.
4. Open the PR's Files changed tab.
5. Examine the dependency changes.
6. Review any reported vulnerabilities.
7. Record the result.

If your private repository is not eligible, document the workflow and practise it later in an eligible public or organization-owned repository.

---

## 9. CodeQL — Static Application Security Testing

### Core security tool

CodeQL is GitHub's code analysis technology.

It analyzes source code to identify potential vulnerabilities and coding errors.

Unlike dependency scanning, CodeQL examines your own code.

### 9.1 Examples of issues CodeQL can help identify

Depending on the language and query coverage, CodeQL can identify potential issues involving:

- SQL injection.
- Cross-site scripting.
- Path traversal.
- Insecure data handling.
- Unsafe API usage.
- Other language-specific security weaknesses.

A CodeQL finding is an alert that requires investigation. It should not automatically be treated as proof that an application is exploitable.

### 9.2 How CodeQL works

```text
Application source code
          |
          v
    CodeQL analysis
          |
          v
Code representation and queries
          |
          v
Potential security findings
          |
          v
Code scanning alerts
          |
          v
Developer investigates and fixes
```

A CodeQL query describes a pattern or condition that the analysis engine should identify.

### 9.3 CodeQL setup approaches

GitHub provides two main approaches:

| Setup | Description |
|---|---|
| Default setup | GitHub manages much of the configuration |
| Advanced setup | You manage a customized analysis workflow |

Default setup is a good starting point for eligible repositories.

Advanced setup gives you more control over:

- Languages.
- Query suites.
- Build configuration.
- Analysis events.
- Workflow customization.

### 9.4 Enable CodeQL

For an eligible repository, navigate to:

#### Repository → Settings → Advanced Security → Code Security

Review the CodeQL analysis setup options.

With default setup, you can review the detected languages and configuration before enabling analysis.

Official documentation:

[Code security documentation](https://docs.github.com/en/code-security/code-scanning)

### 9.5 Important limitation for your training repository

Your `github-deep-dive-training` repository is private and personally owned.

GitHub's current GitHub.com documentation states:

- GitHub Free and GitHub Pro users can use CodeQL code scanning on public repositories.
- Private or internal repositories require GitHub Code Security through an eligible GitHub Team or Enterprise configuration.

Therefore, you can study CodeQL and prepare its configuration now, but you should not expect CodeQL code scanning to be available in your current private personal repository on Free.

This is a platform entitlement limitation, not necessarily a configuration mistake.

### 9.6 CodeQL versus traditional linters

| Tool | Primary purpose |
|---|---|
| Ruff | Python linting and formatting |
| ESLint | JavaScript and TypeScript linting |
| Bandit | Python security-oriented static analysis |
| CodeQL | Semantic code security analysis |
| SonarQube | Broader code quality and security analysis |

These tools can complement one another.

A linter does not replace a security scanner, and a security scanner does not replace application tests.

### Exercise 6 — CodeQL deep dive

Create:

```text
docs/github/module-03-pull-requests/codeql-deep-dive.md
```

Document:

1. What is CodeQL?
2. What is SAST?
3. How does static analysis work?
4. What is a CodeQL query?
5. What is a code scanning alert?
6. What is the difference between default and advanced setup?
7. What are the repository eligibility requirements?
8. How would you integrate CodeQL into a production DRF + React application?

---

## 10. Secret Scanning and Push Protection

### Critical security practice

Imagine a developer accidentally commits:

```python
DJANGO_SECRET_KEY = "example-secret-value"
```

Or:

```typescript
const API_KEY = "example-api-key";
```

Real credentials must never be committed to Git.

### 10.1 Secret Scanning

Secret scanning searches supported patterns for exposed credentials.

Examples include:

- API keys.
- Access tokens.
- Cloud credentials.
- Private keys.
- Database credentials.
- Other supported authentication secrets.

When GitHub detects a supported secret, it can generate a security alert depending on the repository's feature availability and configuration.

### 10.2 Push Protection

Secret scanning and push protection have different responsibilities.

Secret scanning detects supported secrets.

Push protection attempts to stop supported secrets from entering the repository in the first place.

**Without push protection:**

```text
Developer commits a secret
          |
          v
Push to GitHub
          |
          v
Secret scanning detects it
          |
          v
Security alert generated
```

**With push protection:**

```text
Developer attempts to push a secret
          |
          v
GitHub detects a supported pattern
          |
          v
Push is blocked
          |
          v
Developer investigates and removes it
          |
          v
Developer retries the push
```

An authorized bypass may be available depending on repository configuration and the relevant policy.

### 10.3 Enable secret scanning

For eligible repositories, navigate to:

#### Settings → Advanced Security → Secret Protection

Review the available options for:

- Secret scanning.
- Push protection.
- Additional scanning settings.

### 10.4 Understand the availability limitations

GitHub's current feature availability distinguishes between repository types.

| Repository type | Secret scanning availability |
|---|---|
| Public repository | Supported secret scanning is available without a paid Code Security add-on |
| Organization-owned private repository | Requires eligible GitHub Secret Protection |
| User-owned private repository | More restrictive eligibility; consult current GitHub documentation |

Do not assume that all secret-scanning features are available in your private personal repository.

Official documentation:

[Enable secret scanning](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enable-secret-scanning)

### 10.5 Local secret detection

You can practise secret detection without relying on GitHub's paid features.

One useful tool is **Gitleaks**.

Gitleaks scans Git repositories for potential secrets.

Another tool worth studying is `detect-secrets`.

These tools can be integrated into local development and CI pipelines.

### 10.6 Why deleting a secret is not enough

Suppose you commit a real credential and later remove it from the file.

The original value may still exist in Git history.

The correct response is:

1. Treat the credential as compromised.
2. Revoke or rotate it with the provider.
3. Check whether the credential was used.
4. Remove the exposed value from the current code.
5. Assess whether Git history cleanup is necessary.
6. Review logs, artifacts, and other possible exposure points.

History rewriting alone does not make an exposed credential safe.

### Exercise 7 — Secret security documentation

Create:

```text
docs/github/module-03-pull-requests/secret-scanning.md
```

Document:

- Secret scanning.
- Push protection.
- Supported detection patterns.
- False positives.
- Secret rotation.
- Gitleaks.
- GitHub Actions secrets.
- Why removing a secret from the latest commit does not necessarily remove it from Git history.

Do not commit real secrets or intentionally push real credentials as a test.

---

## 11. Gitleaks — Local Secret Detection

Now let's look more closely at Gitleaks.

### 11.1 What is Gitleaks?

Gitleaks is an open-source tool that detects potential secrets in Git repositories.

It can help identify:

- API tokens.
- Credentials.
- Private keys.
- Password-like values.
- Other patterns covered by its detection rules.

It is useful because secret detection can happen before code reaches GitHub.

### 11.2 Where can Gitleaks be used?

```text
Developer workstation
       |
       v
Local repository scan
       |
       v
Developer fixes findings
       |
       v
Commit and push
       |
       v
GitHub Actions scan
       |
       v
PR security check
```

You can use Gitleaks:

- During local development.
- As part of a pre-commit workflow.
- In GitHub Actions.
- As part of a larger DevSecOps pipeline.

### 11.3 Practise a local repository scan

After installing Gitleaks using its official installation instructions, navigate to your cloned training repository in PowerShell.

Run:

```powershell
gitleaks git .
```

Review the command's output.

The objective is to understand:

- What the tool scans.
- How findings are reported.
- How false positives are handled.
- Why findings need investigation.

Do not introduce real credentials into the repository to test detection.

### 11.4 Gitleaks versus GitHub Secret Scanning

| Gitleaks | GitHub Secret Scanning |
|---|---|
| External open-source tool | GitHub security feature |
| Can run locally | Runs through GitHub's platform |
| Can run in CI | Integrates with GitHub security alerts |
| Uses its own detection rules | Uses GitHub-supported secret patterns |
| Can be part of pre-commit workflows | Can include push protection |

They can complement one another.

### Exercise 8 — Gitleaks documentation

Add the Gitleaks section to:

```text
docs/github/module-03-pull-requests/secret-scanning.md
```

Document:

1. What is Gitleaks?
2. What can it detect?
3. How can it be used locally?
4. How can it be integrated into GitHub Actions?
5. What is a false positive?
6. Why should a detected real credential be rotated?

---

## 12. SonarQube — Code Quality and Security Analysis

Now let's introduce another important tool from your DevOps learning roadmap.

SonarQube analyzes source code and provides information about:

- Bugs.
- Code smells.
- Security vulnerabilities.
- Security hotspots.
- Code duplication.
- Maintainability.
- Test coverage.

### 12.1 Understand the main concepts

| Concept | Meaning |
|---|---|
| Bug | A code issue that may cause incorrect behavior |
| Code smell | A maintainability problem |
| Vulnerability | A security weakness identified by analysis |
| Security hotspot | Code requiring security review |
| Code duplication | Repeated or duplicated code |
| Coverage | How much code is exercised by tests |
| Quality Gate | A set of conditions used to evaluate code quality |

A security hotspot is not automatically a confirmed vulnerability. It requires review to determine whether the code is actually risky.

### 12.2 SonarQube versus CodeQL

| Area | CodeQL | SonarQube |
|---|---|---|
| Security vulnerability analysis | Yes | Yes |
| Code quality | More focused on code analysis and security | Broad quality analysis |
| Code smells | Not its primary focus | Yes |
| Maintainability | Limited focus | Yes |
| PR analysis | Yes | Yes |
| Quality gates | Integrates with GitHub checks | Built-in quality gate system |

They can be used together.

### 12.3 Understand SonarQube Quality Gates

A Quality Gate determines whether code satisfies a configured set of quality conditions.

For example, a team might define this policy for new code:

| Condition | Example requirement |
|---|---|
| New bugs | 0 |
| New vulnerabilities | 0 |
| New security hotspots reviewed | 100% |
| New code coverage | At least 80% |
| New code duplication | Below 3% |

These are illustrative policy values, not universal SonarQube defaults.

A Quality Gate can produce:

```text
Analysis completed
       |
       v
Quality conditions evaluated
       |
       v
All conditions satisfied?
       |
       +---- Yes ----> Passed
       |
       +---- No -----> Failed
```

The result can be reported to GitHub so reviewers can see the analysis status on the Pull Request.

### 12.4 SonarQube architecture

```text
Developer creates PR
         |
         v
GitHub Actions starts
         |
         v
Build and test application
         |
         v
SonarScanner analyzes code
         |
         v
SonarQube receives analysis
         |
         v
Quality Gate evaluated
         |
         v
Result reported to GitHub
         |
         v
PR checks pass or fail
```

### 12.5 SonarQube Cloud versus SonarQube Server

| Product | Description |
|---|---|
| SonarQube Cloud | Hosted analysis service |
| SonarQube Server | Self-managed installation |

Both are worth understanding.

For your future projects, SonarQube Server is particularly useful as a self-hosted infrastructure exercise involving Docker and server administration.

### 12.6 GitHub Actions integration example

For an eligible SonarQube Cloud project, a general integration looks like this:

```yaml
name: SonarQube Analysis

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

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

      - name: SonarQube analysis
        uses: SonarSource/sonarqube-scan-action@v6
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
```

This is a starting integration example, not a complete production configuration.

You must also configure:

- The SonarQube project.
- The organization, where applicable.
- Scanner properties.
- Source directories.
- Build and test processes.
- Coverage reports.
- Credentials.

For production, verify and pin third-party actions to full commit SHAs.

### 12.7 How SonarQube can analyze Django and React

For a future restaurant management application:

#### Backend

```text
backend/
├── config/
├── apps/
├── tests/
├── requirements.txt
└── pyproject.toml
```

Potential analysis includes:

- Python code quality.
- Security-related findings.
- Code duplication.
- Test coverage.

#### Frontend

```text
frontend/
├── src/
├── public/
├── package.json
├── package-lock.json
└── tsconfig.json
```

Potential analysis includes:

- JavaScript and TypeScript code quality.
- Security-related findings.
- Code duplication.
- Test coverage.

### Exercise 9 — SonarQube documentation

Create:

```text
docs/github/module-03-pull-requests/sonarqube-integration.md
```

Document:

1. What is SonarQube?
2. SonarQube Cloud versus Server.
3. What is a Quality Gate?
4. What is a Security Hotspot?
5. How does SonarQube integrate with GitHub Actions?
6. How can it analyze Django and React applications?
7. How does a failed Quality Gate affect PR merging?

References:

- [SonarQube Cloud](https://docs.sonarsource.com/sonarqube-cloud)
- [SonarQube Cloud quality gates](https://docs.sonarsource.com/sonarqube-cloud/standards/quality-gates)
- [SonarQube Server](https://docs.sonarsource.com/sonarqube-server)

---

## 13. Build a Security Validation Pipeline

Now let's combine the tools.

The goal is to understand how a professional repository separates different validation responsibilities.

### 13.1 Recommended workflow structure

For a larger application, you might organize workflows like this:

```text
.github/
└── workflows/
    ├── pr-validation.yml
    ├── dependency-review.yml
    ├── codeql.yml
    ├── sonar.yml
    ├── backend-tests.yml
    ├── frontend-tests.yml
    └── security-checks.yml
```

Each workflow has a different responsibility.

| Workflow | Responsibility |
|---|---|
| `pr-validation.yml` | Validate PR changes |
| `dependency-review.yml` | Inspect dependency changes |
| `codeql.yml` | Static code security analysis |
| `sonar.yml` | Code quality analysis |
| `backend-tests.yml` | Run Python tests |
| `frontend-tests.yml` | Run frontend tests |
| `security-checks.yml` | Run additional security checks |

You do not need to create every workflow in your training repository immediately.

Some require an external service or a GitHub security entitlement.

### 13.2 Create a practical security workflow

For your training repository, we can implement a basic workflow that checks repository hygiene and runs Gitleaks.

Create:

```text
.github/workflows/security-checks.yml
```

Example:

```yaml
name: Security Checks

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  security:
    name: Repository Security Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Check repository whitespace
        run: git diff --check

      - name: Scan repository for secrets
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

This is a learning configuration. Before using a third-party action in production:

1. Review its official repository.
2. Verify its current version and requirements.
3. Review its permissions.
4. Pin it to a verified full commit SHA.
5. Check whether your repository or organization requires additional configuration.

### 13.3 Understand the limitations

This workflow is not a complete security system.

It does not:

- Replace CodeQL.
- Replace dependency vulnerability analysis.
- Replace DAST.
- Guarantee that all secrets will be detected.
- Prove that the application is secure.
- Replace manual security review.
- Replace tests and code quality analysis.

Also, `git diff --check` is a whitespace validation check. It is not a complete security scan or historical secret scan.

### 13.4 Security pipeline for a production DRF + React application

Your future architecture could look like this:

```text
                  Pull Request
                       |
          +------------+------------+
          |            |            |
          v            v            v
       Backend      Frontend     Security
          |            |            |
          v            v            v
         Ruff        ESLint      Gitleaks
         Bandit      Tests       CodeQL
         pytest      Build       Dependency Review
          |            |            |
          +------------+------------+
                       |
                       v
                    Quality
                       |
                       v
                   SonarQube
                       |
                       v
                Required GitHub checks
                       |
                       v
                 Review and approval
                       |
                       v
                  Eligible to merge
                       |
                       v
                    main branch
```

Remember:

A workflow existing in `.github/workflows` does not automatically make its result mandatory.

You must configure the appropriate required status checks in branch protection or repository rulesets.

### Exercise 10 — Build the security workflow

In your training repository:

1. Create `security-checks.yml`.
2. Configure `pull_request` and `push` triggers.
3. Use minimal permissions.
4. Add repository whitespace validation.
5. Add Gitleaks.
6. Review the action and its permissions.
7. Open a documentation PR.
8. Observe the workflow results.

---

## 14. Quality Gates and Required Status Checks

A security workflow can detect problems, but how do you prevent merging when an important check fails?

This is where quality gates and GitHub branch protection work together.

### 14.1 What is a Quality Gate?

A Quality Gate is a policy that determines whether code satisfies a defined set of conditions.

For example:

```text
PR opened
    |
    v
Security checks
    |
    v
Code quality checks
    |
    v
Automated tests
    |
    v
Quality conditions evaluated
    |
    +---- Passed ----> Eligible for merge
    |
    +---- Failed ----> Fix required
```

The actual merge restriction is enforced by GitHub's branch protection or rulesets when the relevant status checks are required.

### 14.2 Example quality policy

For a production restaurant management application:

| Check | Example requirement |
|---|---|
| Backend tests | Must pass |
| Frontend tests | Must pass |
| Linting | Must pass |
| Dependency Review | Must pass when configured |
| Secret detection | Must pass |
| Code scanning | Must pass when configured |
| SonarQube Quality Gate | Must pass when configured |
| Required approvals | Must be satisfied |

These are example policies. A real team should define thresholds according to its application and risk profile.

### 14.3 Configure required status checks

Navigate to:

#### Repository → Settings → Rules → Rulesets

Or review your existing branch protection configuration.

For the `main` branch, configure appropriate requirements such as:

- Require a Pull Request before merging.
- Require approvals.
- Require status checks to pass.
- Require branches to be up to date, where appropriate.
- Restrict direct pushes if required by your policy.

The exact settings depend on your repository configuration and available GitHub features.

### 14.4 Understand the difference

| Feature | Responsibility |
|---|---|
| GitHub Actions | Runs automated checks |
| CodeQL | Analyzes code |
| SonarQube | Evaluates code quality |
| Quality Gate | Evaluates configured quality conditions |
| Branch protection | Enforces merge requirements |
| Rulesets | Apply repository and branch policies |

### Exercise 11 — Design your quality policy

Create:

```text
docs/github/module-03-pull-requests/security-quality-gates.md
```

Document:

1. What is a Quality Gate?
2. What are required status checks?
3. How do GitHub Actions checks appear on a PR?
4. How can a failed check prevent merging?
5. Which checks should be required for your future restaurant application?
6. Which checks are optional for your Markdown-only training repository?

---

## 15. Repository Security Policy — SECURITY.md

Every professional repository should explain how security vulnerabilities should be reported.

GitHub recognizes a repository security policy through a `SECURITY.md` file.

Create:

```text
SECURITY.md
```

Use this content:

```markdown
# Security Policy

## Supported Versions

Security updates are provided for actively maintained versions.

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |
| Older versions | No |

## Reporting a Vulnerability

If you discover a security vulnerability:

1. Do not publish exploit details in a public issue.
2. Do not include credentials or personal information.
3. Report the vulnerability privately using the repository's
   available private vulnerability reporting mechanism.
4. Include a clear description of the affected component.
5. Include the potential security impact.

## Response Process

The maintainers will:

- Review the report.
- Assess the severity.
- Investigate the vulnerability.
- Prepare a fix.
- Coordinate disclosure when appropriate.

## Security Practices

This repository aims to:

- Keep dependencies updated.
- Avoid committing credentials.
- Review security-sensitive changes.
- Run automated validation.
- Document security-related changes.

## Scope

Only vulnerabilities affecting this repository and its
maintained software are in scope.
```

### 15.1 Understand private vulnerability reporting

GitHub supports private vulnerability reporting for eligible repositories.

It allows security researchers to report vulnerabilities without immediately publishing sensitive details in a public issue.

Repository security advisories can also support private discussion and coordinated disclosure.

For your training repository, you can document the reporting process even if the private reporting feature is unavailable.

Reference:

[Adding a security policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository)

### Exercise 12 — Create SECURITY.md

1. Create `SECURITY.md` in the repository root.
2. Add the security policy.
3. Review the reporting instructions.
4. Ensure that no private credentials or personal information are included.
5. Commit the file through a documentation PR.

---

## 16. Practical Assignment — Secure Your Training Repository

Now implement the lesson in:

```text
github-deep-dive-training
```

### 16.1 Target repository structure

Your final structure should look like this:

```text
github-deep-dive-training/
│
├── .github/
│   ├── dependabot.yml
│   │
│   └── workflows/
│       ├── pr-validation.yml
│       ├── dependency-review.yml
│       └── security-checks.yml
│
├── docs/
│   └── github/
│       └── module-03-pull-requests/
│           ├── lesson-32-pr-security-quality-gates.md
│           ├── fork-pr-security.md
│           ├── pull-request-events-security.md
│           ├── github-actions-security.md
│           ├── security-secrets-policy.md
│           ├── codeql-deep-dive.md
│           ├── secret-scanning.md
│           ├── sonarqube-integration.md
│           └── security-quality-gates.md
│
└── SECURITY.md
```

**Important implementation notes:**

- `dependabot.yml` should configure ecosystems that actually exist.
- `dependency-review.yml` is optional if your repository is not eligible or has no dependency changes to review.
- CodeQL documentation is required, but CodeQL execution is optional if your repository is not eligible.
- Secret scanning and push protection should be documented even if the features are unavailable.
- Gitleaks can be practised locally and in GitHub Actions.
- Do not create empty workflows just to match the structure.

### 16.2 Implementation checklist

- [ ] Created Lesson 32 documentation.
- [ ] Documented fork-based PR security.
- [ ] Documented `pull_request` versus `pull_request_target`.
- [ ] Documented `GITHUB_TOKEN` permissions.
- [ ] Documented GitHub Actions secrets and variables.
- [ ] Reviewed workflow security practices.
- [ ] Configured Dependabot for an existing ecosystem.
- [ ] Created Dependency Review workflow or documented its eligibility limitation.
- [ ] Documented CodeQL default and advanced setup.
- [ ] Documented CodeQL repository eligibility.
- [ ] Documented secret scanning and push protection.
- [ ] Studied Gitleaks and local secret detection.
- [ ] Documented SonarQube integration.
- [ ] Created `security-checks.yml`.
- [ ] Created `SECURITY.md`.
- [ ] Reviewed workflow permissions.
- [ ] Tested the available GitHub Actions workflows.
- [ ] Created and reviewed a documentation PR.
- [ ] Merged the PR.
- [ ] Created the Lesson 32 tag.
- [ ] Published the Lesson 32 release.

---

## 17. Lesson Documentation

Create:

```text
docs/github/module-03-pull-requests/lesson-32-pr-security-quality-gates.md
```

Use the following structure for the main lesson document:

```markdown
# Lesson 32 — GitHub PR Security & Quality Gates

## Learning Objectives

## 1. PR Security Architecture

## 2. Fork-Based PR Security

## 3. pull_request vs pull_request_target

## 4. GitHub Actions Security

## 5. GITHUB_TOKEN Permissions

## 6. Secrets and Variables

## 7. Dependabot

## 8. Dependency Review

## 9. CodeQL and SAST

## 10. Secret Scanning

## 11. Push Protection

## 12. Gitleaks

## 13. SonarQube Integration

## 14. Quality Gates

## 15. Secure PR Validation Pipeline

## 16. SECURITY.md

## 17. Practical Assignments

## 18. Repository Security Architecture

## 19. Assessment

## 20. Lessons Learned

## 21. References
```

Use the separate documentation files for the deeper exercises.

The main lesson file should explain the concepts and link to the supporting documents.

### 17.1 Add screenshots from your actual repository

Capture screenshots after performing the exercises.

Useful screenshots include:

1. Dependabot configuration in the repository.
2. A successful PR validation workflow.
3. A Gitleaks workflow result.
4. The PR checks section.
5. Repository security settings, if available.
6. The `SECURITY.md` file.
7. The merged Lesson 32 documentation PR.

Do not add hypothetical screenshots or screenshots containing credentials.

---

## 18. Repository Security Architecture

Let's bring everything together.

For your future Django + React application, the security responsibilities should be separated.

### 18.1 Backend security

| Tool | Responsibility |
|---|---|
| Ruff | Python linting and formatting |
| Bandit | Python security-oriented static analysis |
| pytest | Backend testing |
| Dependency Review | Review dependency changes |
| CodeQL | Advanced source-code analysis |
| SonarQube | Code quality and security analysis |

### 18.2 Frontend security

| Tool | Responsibility |
|---|---|
| ESLint | JavaScript and TypeScript linting |
| Frontend tests | Application behavior validation |
| npm audit | Dependency vulnerability information |
| Dependency Review | Review dependency changes |
| CodeQL | Source-code security analysis |
| SonarQube | Code quality and security analysis |

### 18.3 Repository security

| Tool or feature | Responsibility |
|---|---|
| Gitleaks | Secret detection |
| Secret Scanning | GitHub credential detection |
| Push Protection | Prevent supported secret leaks |
| Dependabot | Dependency updates |
| GitHub Actions | Automated validation |
| Branch protection | Merge restrictions |
| SECURITY.md | Vulnerability reporting policy |

### 18.4 Complete DevSecOps architecture

```text
Developer
   |
   v
Feature branch
   |
   v
Pull Request
   |
   +---------------------------+
   |                           |
   v                           v
Application validation     Security validation
   |                           |
   v                           v
Backend tests              Gitleaks
Frontend tests             Dependency Review
Linting                    CodeQL
Build                      SonarQube
   |                           |
   +-------------+-------------+
                 |
                 v
          Required checks
                 |
                 v
          Security review
                 |
                 v
         Required approvals
                 |
                 v
           Eligible to merge
                 |
                 v
              main
```

This is the foundation of a secure Pull Request pipeline.

---

## 19. Git Workflow — Commit, PR, Tag and Release

Keep using your established training workflow.

### Step 1 — Update main

In PowerShell:

```powershell
git switch main
git pull origin main
```

### Step 2 — Create a branch

```powershell
git switch -c docs/lesson-32-pr-security
```

### Step 3 — Add your files

```powershell
git add .github/
git add docs/github/module-03-pull-requests/
git add SECURITY.md
```

If you did not create every optional workflow, only stage the files that actually exist.

### Step 4 — Validate

```powershell
git status
git diff --check
git diff --cached
```

Check that:

- No credentials were included.
- No private configuration files were included.
- YAML files are correctly formatted.
- Documentation links are correct.
- Workflow permissions are appropriate.
- Optional files are not empty placeholders.

### Step 5 — Commit

Use Conventional Commits:

```powershell
git commit -m "docs(github): add Lesson 32 PR security and quality gates"
```

### Step 6 — Push

```powershell
git push -u origin docs/lesson-32-pr-security
```

### Step 7 — Create a Pull Request

**PR title:**

```text
docs(github): add Lesson 32 PR security and quality gates
```

**PR description:**

```markdown
## Summary

Add Lesson 32 covering GitHub PR security and quality gates.

## Topics

- Fork-based PR security
- pull_request vs pull_request_target
- GitHub Actions permissions
- Secrets management
- Dependabot
- Dependency Review
- CodeQL and SAST
- Secret scanning
- Push protection
- Gitleaks
- SonarQube
- Security quality gates
- SECURITY.md

## Validation

- [ ] Markdown reviewed
- [ ] Workflow YAML reviewed
- [ ] Workflow permissions reviewed
- [ ] No credentials committed
- [ ] Security documentation reviewed
- [ ] Available workflows tested

## Related lessons

- Lesson 30: Pull Request Management and Merge Conflicts
- Lesson 31: Advanced Pull Request Automation and Governance
```

Review the PR.

Check the workflow results and inspect the Files changed tab.

Resolve any problems before merging.

### Step 8 — Merge the PR

Merge the documentation PR into `main` using your repository's configured merge strategy.

### Step 9 — Create an annotated tag

After the PR has been merged:

```powershell
git switch main
git pull origin main
git fetch --tags
```

Create the tag:

```powershell
git tag -a module-03-lesson-32 -m "Complete Module 3 Lesson 32"
```

Push it:

```powershell
git push origin module-03-lesson-32
```

### Step 10 — Create the GitHub Release

Navigate to:

#### Repository → Releases → Draft a new release

Use these values:

| Field | Value |
|---|---|
| Tag | `module-03-lesson-32` |
| Title | Module 3 — Lesson 32: PR Security & Quality Gates |
| Target | `main` |

**Release notes:**

```markdown
# Module 3 — Lesson 32

Completed GitHub Pull Request Security and Quality Gates.

## Topics

- Fork-based PR security
- pull_request vs pull_request_target
- GitHub Actions security
- GITHUB_TOKEN permissions
- Secrets and variables
- Dependabot
- Dependency Review
- CodeQL
- SAST
- Secret scanning
- Push protection
- Gitleaks
- SonarQube
- Security quality gates
- SECURITY.md

## Practical exercises

- Configured Dependabot
- Reviewed Dependency Review
- Studied CodeQL
- Documented secret scanning
- Practised Gitleaks
- Created security validation workflow
- Created repository security policy
- Reviewed workflow permissions

## Training checkpoint

module-03-lesson-32
```

Publish the release.

---

## 20. Assessment

Use these questions to evaluate your understanding.

### Conceptual questions

1. Why should fork-based PRs be treated as untrusted?
2. What is the difference between `pull_request` and `pull_request_target`?
3. What is a pwn request?
4. Why is least privilege important in GitHub Actions?
5. What is `GITHUB_TOKEN`?
6. What is the difference between GitHub Actions secrets and variables?
7. What is the difference between Dependabot alerts and Dependabot version updates?
8. What does Dependency Review examine?
9. What is CodeQL?
10. What is the difference between SAST and SCA?
11. What is secret scanning?
12. What is push protection?
13. Why is deleting a secret from the latest commit not enough?
14. What is Gitleaks?
15. What is the difference between CodeQL and SonarQube?
16. What is a SonarQube Quality Gate?
17. How do required status checks prevent merging?
18. Why should third-party GitHub Actions be reviewed and pinned?

### Practical assessment

You should be able to:

- [ ] Explain the security model of fork-based PRs.
- [ ] Identify an unsafe `pull_request_target` workflow.
- [ ] Configure minimal GitHub Actions permissions.
- [ ] Explain secrets versus variables.
- [ ] Configure Dependabot for an existing ecosystem.
- [ ] Explain Dependency Review.
- [ ] Explain CodeQL setup and eligibility.
- [ ] Explain secret scanning and push protection.
- [ ] Run a local Gitleaks scan.
- [ ] Explain SonarQube Quality Gates.
- [ ] Create a basic security workflow.
- [ ] Create a repository `SECURITY.md`.
- [ ] Explain how required checks affect merging.
- [ ] Complete the Lesson 32 PR, tag, and release workflow.

---

## 21. Lessons Learned

In this lesson, you learned that Pull Request security is not just about running tests.

A secure repository must consider:

- Who submitted the code.
- Whether the workflow executes untrusted code.
- What permissions the workflow receives.
- Whether sensitive credentials are exposed.
- Whether dependencies contain known vulnerabilities.
- Whether source code contains security weaknesses.
- Whether secrets have been committed.
- Whether code meets quality standards.
- Whether failed checks can block merging.

You also learned that tools have different responsibilities:

- Dependabot manages dependency updates.
- Dependency Review examines dependency changes.
- CodeQL performs static code security analysis.
- Secret Scanning identifies supported exposed credentials.
- Push Protection can block supported secret leaks.
- Gitleaks detects potential secrets in Git repositories.
- SonarQube evaluates code quality and security-related findings.
- GitHub Actions automates validation.
- Branch protection and rulesets enforce merge requirements.

**The most important principle:**

A successful CI pipeline does not automatically mean that an application is secure. Security requires multiple complementary controls, thoughtful review, and continuous maintenance.

---

## 22. Official Documentation and References

Bookmark these resources for future projects.

| Subject | Documentation |
|---|---|
| Actions security | [Secure use](https://docs.github.com/en/actions/reference/security/secure-use) |
| Fork PR security | [Secure use of pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) |
| GITHUB_TOKEN | [Automatic token authentication](https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication) |
| Dependabot | [Dependabot](https://docs.github.com/en/code-security/dependabot) |
| Dependency Review | [Dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) |
| CodeQL | [Code scanning](https://docs.github.com/en/code-security/code-scanning) |
| Secret Scanning | [Secret scanning](https://docs.github.com/en/code-security/secret-scanning) |
| Push Protection | [Push protection](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) |
| SECURITY.md | [Security policy](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository) |
| Gitleaks | [Gitleaks](https://github.com/gitleaks/gitleaks) |
| SonarQube Cloud | [SonarQube Cloud](https://docs.sonarsource.com/sonarqube-cloud) |
| SonarQube Server | [SonarQube Server](https://docs.sonarsource.com/sonarqube-server) |
| GitHub Rulesets | [Managing rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets) |

---

## 23. Next Lesson — Lesson 33

### Module 4 — GitHub Issues

## Lesson 33: GitHub Issues — Advanced Issue Management

In Lesson 33, we'll transition from the Pull Requests tab to the Issues tab.

We'll explore how professional development teams manage bugs, feature requests, technical debt, tasks, and development planning.

### Topics

1. Understanding the GitHub Issues tab.
2. Issue types and issue categories.
3. Issue templates.
4. Issue forms using YAML.
5. Labels and label conventions.
6. Milestones.
7. Assignees and multiple collaborators.
8. Issue dependencies and relationships.
9. Sub-issues and parent issues.
10. Issue linking with Pull Requests.
11. Closing issues automatically.
12. GitHub Projects integration.
13. Issue triage and prioritization.
14. Bug-reporting workflows.
15. Feature-request workflows.
16. Automating Issues using GitHub Actions.
17. Managing issues like a professional engineering team.

**Our progression:** Lesson 32 completes the advanced Pull Request security and quality section. Lesson 33 begins our deep dive into GitHub Issues.

We'll continue using:

- `github-deep-dive-training`.
- GitHub-ready Markdown documentation.
- Practical repository exercises.
- Conventional Commits.
- Feature branches and Pull Requests.
- Annotated tags and GitHub Releases.

**End of Lesson 32.**

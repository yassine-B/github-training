# **Module 4 — GitHub Actions & CI/CD**

## Lesson 40 — GitHub Actions Security, Supply Chain Security & Workflow Hardening

### Advanced

### DevSecOps

### Enterprise Security

---

## **1. Lesson overview**

In Lesson 39, we studied advanced workflow orchestration and enterprise CI/CD pipeline design.

We learned how to:

- Coordinate jobs using `needs`.
- Control workflow execution with conditions.
- Use dynamic matrices.
- Transfer data through outputs and artifacts.
- Improve performance with caching.
- Control concurrent workflow executions.
- Build multi-stage CI/CD pipelines.
- Promote immutable artifacts between environments.
- Protect deployments with environment approvals.
- Design deployment and recovery strategies.

Now we are moving from **building advanced CI/CD pipelines** to **securing those pipelines**.

A CI/CD pipeline is not simply an automation system. It is also part of your application's security boundary.

Consider a Django REST Framework + React application.

Your pipeline might have permission to:

- Read application source code.
- Download Python and npm dependencies.
- Execute third-party GitHub Actions.
- Access repository and environment secrets.
- Build Docker images.
- Publish packages.
- Authenticate with cloud infrastructure.
- Deploy to staging and production.
- Create GitHub Releases.
- Modify repository resources.

If an attacker compromises a workflow, dependency, third-party Action, runner, or credential, they may gain access to some of these capabilities.

This is why professional software teams integrate security throughout the software delivery lifecycle.

This discipline is commonly called **DevSecOps**.

### **1.1 Learning objectives**

By the end of this lesson, you should understand how to:

1. Build a threat model for GitHub Actions.
2. Configure least-privilege `GITHUB_TOKEN` permissions.
3. Apply job-level permissions.
4. Review third-party GitHub Actions.
5. Pin Actions to verified full commit SHAs.
6. Manage repository, organization, and environment secrets.
7. Understand OpenID Connect (OIDC).
8. Authenticate with cloud providers without storing long-lived credentials.
9. Secure pull request workflows.
10. Understand `pull_request` and `pull_request_target`.
11. Prevent workflow script injection.
12. Protect artifacts and caches from poisoning.
13. Understand software supply chain security.
14. Generate and manage SBOMs.
15. Understand Sigstore, Cosign, and artifact signing.
16. Generate and verify artifact attestations where supported.
17. Integrate CodeQL and SAST.
18. Configure secret detection with Gitleaks.
19. Automate dependency updates with Dependabot.
20. Review dependency changes in pull requests.
21. Scan Docker images using Trivy.
22. Understand self-hosted runner security.
23. Establish enterprise Actions governance.
24. Design a hardened DRF + React CI/CD pipeline.

### **1.2 What we are going to build**

We will progressively harden a realistic application delivery pipeline.

Our target architecture:

```text
Developer
    |
    v
Pull Request
    |
    v
Untrusted Code Validation
    |
    +-------------------------------+
    |                               |
    v                               v
Backend Security                Frontend Security
    |                               |
    +---------------+---------------+
                    |
                    v
             Security Checks
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
     CodeQL      Gitleaks   Dependency Review
        |           |           |
        +-----------+-----------+
                    |
                    v
             Trusted Main Branch
                    |
                    v
              Build Artifacts
                    |
        +-----------+-----------+
        |                       |
        v                       v
    Docker Build             SBOM Generation
        |                       |
        v                       v
    Trivy Scan              Provenance
        |                       |
        +-----------+-----------+
                    |
                    v
             Artifact Verification
                    |
                    v
             Protected Deployment
                    |
                    v
              Staging / Production
```

The objective is not to add every available security tool without understanding it.

The objective is to build a pipeline where every security control has a defined purpose.

### **1.3 Lesson deliverables**

By the end of the lesson, your training repository should contain:

- A GitHub Actions security permissions workflow.
- A third-party Action security review.
- A secrets management exercise.
- An OIDC configuration exercise.
- A secure pull request workflow.
- A Gitleaks workflow.
- A Dependabot configuration.
- A container security laboratory.
- An SBOM and provenance document.
- A hardened CI/CD architecture document.
- A complete security policy checklist.

---

## 2. GitHub Actions threat modeling

Before implementing security controls, we need to understand what we are protecting.

A threat model identifies:

- Assets.
- Threat actors.
- Attack surfaces.
- Potential vulnerabilities.
- Security controls.
- Residual risks.

### **2.1 What are we protecting?**

Consider a private repository containing your application.

| Asset | Security concern |
|---|---|
| Source code | Unauthorized modification |
| Repository secrets | Credential exposure |
| `GITHUB_TOKEN` | Excessive permissions |
| Docker registry credentials | Unauthorized image publishing |
| Production credentials | Unauthorized deployment |
| Workflow files | Malicious workflow modifications |
| Dependencies | Compromised packages |
| Build artifacts | Artifact tampering |
| Self-hosted runners | Host compromise |
| GitHub Releases | Unauthorized release publishing |

These assets have different levels of sensitivity.

For example, exposing a test workflow's read-only token is not equivalent to exposing a production deployment credential.

Your security architecture must account for those differences.

### **2.2 Common attack scenarios**

### Scenario A — Compromised third-party Action

Your workflow uses an external Action.

The Action's repository or release process becomes compromised.

Your workflow executes that Action with the permissions available to the job.

### Scenario B — Exposed secret

A developer accidentally exposes a deployment credential through a workflow log or generated artifact.

The credential may become accessible to people or processes that should not have it.

### Scenario C — Pull request security issue

A contributor submits untrusted code.

A privileged workflow processes that code without correctly separating trusted and untrusted operations.

### Scenario D — Compromised dependency

An application dependency contains malicious or vulnerable code.

The dependency executes during installation, build, or application runtime.

### Scenario E — Artifact tampering

A deployment job downloads an artifact without verifying its origin or relationship to the expected source revision.

### **2.3 Security layers**

A mature pipeline applies multiple independent security controls.

| Layer | Security controls |
|---|---|
| Identity | Least privilege, OIDC |
| Workflow | Secure triggers, permissions |
| Dependencies | Dependabot, dependency review |
| Code | CodeQL, SAST |
| Secrets | GitHub Secrets, Gitleaks, push protection |
| Artifacts | Provenance, attestations, signatures |
| Containers | Image scanning |
| Infrastructure | Runner isolation, deployment approvals |
| Governance | Branch protection, Actions policies, auditing |

### **2.4 Create a threat model**

Create:

`docs/github/module-04-actions/github-actions-threat-model.md`

Use this structure:

```markdown
# GitHub Actions Threat Model

## 1. Application
DRF + React application

## 2. Protected Assets
- Source code
- Repository secrets
- Workflow permissions
- Docker images
- Deployment credentials
- Build artifacts

## 3. Threat Actors
- Malicious contributor
- Compromised dependency publisher
- Compromised Action publisher
- Unauthorized repository user

## 4. Attack Surfaces
- Pull request workflows
- Third-party Actions
- Dependency installation
- Artifact transfer
- Runner environment
- Deployment credentials

## 5. Security Controls
- Least-privilege permissions
- Full SHA pinning
- Secret management
- OIDC
- Dependency scanning
- Artifact verification
- Runner isolation

## 6. Residual Risks
Document risks that remain after controls are applied.
```

### Practical task

For every asset, identify:

1. What could go wrong?
2. Which workflow or component could expose it?
3. What security control reduces the risk?
4. How would you verify that the control works?

**Expected result:** A documented threat model for your training application.

---

## 3. Workflow permissions and `GITHUB_TOKEN`

This is one of the most important subjects in GitHub Actions security.

Every workflow can receive an automatically generated token called:

`GITHUB_TOKEN`

It is a GitHub App installation token scoped to the repository.

It allows workflows to interact with GitHub without requiring you to manually create a personal access token for ordinary repository operations.

### **3.1 What can `GITHUB_TOKEN` do?**

Depending on its permissions, it can perform operations such as:

- Read repository contents.
- Create or update pull requests.
- Publish GitHub Releases.
- Upload packages.
- Read issues.
- Update checks.
- Access workflow-related resources.

Its actual capabilities depend on the permissions granted to the workflow or job.

### **3.2 The problem: excessive permissions**

Consider:

```yaml
name: CI

on:
  push:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - run: python -m pytest
```

This workflow does not explicitly define its permissions.

GitHub applies the repository or organization default token permissions.

For security-sensitive workflows, relying on implicit defaults makes it harder to understand exactly what the workflow can do.

### **3.3 Apply the principle of least privilege**

The principle of least privilege means giving a process only the permissions it needs.

For a workflow that only checks out source code:

```yaml
name: Secure CI

on:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run validation
        run: echo "Running validation"
```

This workflow explicitly requests read access to repository contents.

It does not need repository write access.

### **3.4 Job-level permissions**

Permissions can be configured at workflow level or job level.

Example:

```yaml
name: Permission Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Run tests
        run: echo "Testing application"

  release:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Prepare release
        run: echo "Release job"
```

Here:

- The workflow defaults to read-only content access.
- The test job uses the read-only default.
- The release job receives additional write permission.
- The test job does not need release permissions.

### **3.5 Common permission scopes**

| Permission | Purpose |
|---|---|
| `actions` | Manage Actions resources |
| `attestations` | Create artifact attestations |
| `checks` | Manage check runs |
| `contents` | Repository content access |
| `deployments` | Manage deployments |
| `id-token` | Request OIDC identity tokens |
| `issues` | Manage issues |
| `packages` | Manage packages |
| `pull-requests` | Manage pull requests |
| `security-events` | Manage security events |

Permission levels commonly include:

```yaml
read
write
none
```

Not every permission supports every level.

### **3.6 Important permission behavior**

When you explicitly define a permissions map, unspecified permissions are set to `none`.

This is useful because it prevents unnecessary permissions from being inherited.

### **3.7 Disable write permissions by default**

Navigate to:

`Repository → Settings → Actions → General → Workflow permissions`

Review the default `GITHUB_TOKEN` permission setting.

For training and ordinary CI workflows, prefer read-only defaults unless write access is required.

### **3.8 When should you use `permissions: {}`?**

You can disable all `GITHUB_TOKEN` permissions:

```yaml
permissions: {}
```

Use this when a workflow does not need GitHub API access through the token.

For example, a self-contained calculation or validation task might not need repository API permissions.

Be aware that an action requiring GitHub API access may fail when all token permissions are disabled.

### **3.9 Practical exercise**

Create:

`.github/workflows/security-permissions.yml`

```yaml
name: Security Permissions Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Inspect permissions
        run: |
          echo "This workflow uses read-only contents permissions"
          echo "No repository write permission is configured"
```

Tasks:

1. Run the workflow manually.
2. Inspect the workflow permissions.
3. Change the workflow-level permissions to `{}`.
4. Observe what happens when checkout attempts to access the repository.
5. Restore `contents: read`.
6. Explain why the release job in a real pipeline should have separate permissions.

**Deliverable:** A working workflow and a short explanation of least privilege.

---

## 4. Third-party GitHub Actions security

GitHub Actions allows you to reuse actions developed by other people and organizations.

Examples:

```yaml
uses: actions/checkout@v4
```

```yaml
uses: actions/setup-python@v5
```

```yaml
uses: docker/build-push-action@v6
```

This saves development time, but introduces a software supply chain risk.

### **4.1 Why third-party Actions are a security concern**

When you execute an Action, you execute code maintained outside your workflow.

That code may:

- Access files on the runner.
- Read environment variables.
- Access available credentials.
- Make network requests.
- Modify files.
- Interact with GitHub APIs.

An Action should therefore be treated as executable code, not simply as a configuration option.

### **4.2 Tag-based references**

Consider:

```yaml
- uses: actions/checkout@v4
```

This is convenient, but a version tag such as `v4` is a reference that can potentially be moved.

You are trusting the publisher's release and tag-management process.

### **4.3 Pin Actions to full commit SHAs**

A full commit SHA identifies a specific Git commit.

Example format:

```yaml
- uses: actions/checkout@<VERIFIED_FULL_COMMIT_SHA>
```

The placeholder is explanatory and is not a usable SHA.

For production:

1. Find the Action's official repository.
2. Identify the release you intend to use.
3. Find the corresponding full commit SHA.
4. Verify that it belongs to the intended repository and release.
5. Record the version and SHA in your review documentation.

GitHub identifies full-length commit SHA pinning as the strongest way to reference an immutable Action version.

### **4.4 Tag versus SHA**

| Reference | Example | Security consideration |
|---|---|---|
| Branch | `@main` | Mutable |
| Version tag | `@v4` | Can potentially be moved |
| Full commit SHA | `@40-character-sha` | Immutable commit reference |

SHA pinning does not prove that the code is safe. It ensures that the workflow references the reviewed commit rather than silently following a changing reference.

### **4.5 Review an Action before using it**

Before adding an external Action:

1. Identify its publisher.
2. Inspect its source code.
3. Review its repository activity.
4. Check its permissions requirements.
5. Inspect its dependencies.
6. Understand whether it accesses secrets.
7. Pin it to a verified full commit SHA.
8. Document why your project needs it.
9. Review updates before changing the SHA.

### **4.6 Repository-level Action restrictions**

Navigate to:

`Settings → Actions → General → Actions permissions`

GitHub allows repository administrators to restrict which Actions and reusable workflows are permitted.

Depending on the available settings, you can also configure policies that require full-length commit SHA references.

### **4.7 Practical exercise**

Create:

`docs/github/module-04-actions/action-security-review.md`

Review these Actions:

- `actions/checkout`
- `actions/setup-python`
- `actions/setup-node`

Use this table:

| Review item | Your investigation |
|---|---|
| Official repository | Repository URL |
| Publisher | Organization |
| Release version | Version reviewed |
| Full commit SHA | Verified SHA |
| Permissions | Required permissions |
| Dependencies | External dependencies |
| Security concerns | Identified risks |
| Decision | Approved or rejected |

Then create a workflow using verified full commit SHAs.

**Important:** Do not invent SHA values or copy unverified values from unrelated examples.

**Expected result:** A documented Action review and an immutable Action reference workflow.

---

## 5. Secrets management

A secret is sensitive information that should not be exposed in source code, workflow files, or ordinary workflow logs.

Examples:

- Database passwords.
- API keys.
- Private registry credentials.
- Deployment credentials.
- OAuth client secrets.
- External service tokens.

### **5.1 Never hardcode secrets**

Insecure example:

```yaml
steps:
  - name: Deploy
    run: |
      echo "Deploying"
      export DATABASE_PASSWORD="example-password"
```

This is dangerous because credentials can end up in repository history, workflow files, or logs.

A safer approach:

```yaml
steps:
  - name: Deployment
    env:
      DATABASE_PASSWORD: ${{ secrets.DATABASE_PASSWORD }}

    run: |
      echo "Deployment started"
```

The credential is provided through the environment rather than written directly into the workflow.

### **5.2 Where should you store secrets?**

GitHub provides different secret scopes.

| Scope | Availability |
|---|---|
| Repository secrets | Workflows in a repository |
| Environment secrets | Jobs referencing the environment |
| Organization secrets | Selected repositories within an organization |

For your training repository, begin with repository and environment secrets.

### **5.3 Create a repository secret**

Navigate to:

`Settings → Secrets and variables → Actions`

Then:

1. Select the Secrets tab.
2. Select New repository secret.
3. Enter a secret name.
4. Enter a harmless training value.
5. Save.

Do not enter actual production credentials in your training repository.

### **5.4 Create an environment secret**

Navigate to:

`Settings → Environments`

Create an environment called:

`staging`

You can add environment-specific secrets and variables.

For example:

```text
TRAINING_DEPLOYMENT_ENDPOINT
```

Environment secrets are made available to jobs that reference the corresponding environment, subject to its protection rules.

### **5.5 Secret naming conventions**

For your DRF + React projects:

```text
DJANGO_SECRET_KEY
DATABASE_URL
REDIS_URL
DOCKER_USERNAME
DOCKER_PASSWORD
SENTRY_AUTH_TOKEN
DEPLOYMENT_HOST
DEPLOYMENT_USER
```

These are naming examples, not credentials that you should create for this exercise.

### **5.6 Access a secret safely**

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Validate secret availability
        env:
          TRAINING_SECRET: ${{ secrets.TRAINING_SECRET }}

        run: |
          if [ -z "$TRAINING_SECRET" ]; then
            echo "Training secret is unavailable"
            exit 1
          fi

          echo "Training secret is configured"
```

Notice that the workflow checks whether the value exists without printing the value.

### **5.7 Secret masking limitations**

GitHub attempts to redact registered secrets from logs.

However, automatic masking is not guaranteed for every transformed or encoded representation of a secret.

Avoid:

- Printing secret values.
- Writing secrets into artifacts.
- Uploading `.env` files.
- Storing secrets in caches.
- Committing secrets to Git.
- Printing complete environment variables.
- Passing credentials through command-line arguments unnecessarily.

### **5.8 Repository secrets versus environment secrets**

Consider this architecture:

```text
Repository
    |
    +---- CI workflow
    |       |
    |       +---- Read-only validation
    |
    +---- Staging environment
    |       |
    |       +---- Staging credentials
    |
    +---- Production environment
            |
            +---- Production credentials
            +---- Required approval
```

The principle is simple:

**Expose credentials only to the job that needs them.**

### **5.9 Practical exercise**

Create:

`.github/workflows/secrets-security.yml`

```yaml
name: Secrets Security Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Validate secret availability
        env:
          TRAINING_SECRET: ${{ secrets.TRAINING_SECRET }}

        run: |
          if [ -z "$TRAINING_SECRET" ]; then
            echo "Training secret is unavailable"
            exit 1
          fi

          echo "Training secret is configured"
```

Tasks:

1. Create a harmless training secret.
2. Add it under repository Actions secrets.
3. Execute the workflow.
4. Remove the secret.
5. Execute the workflow again.
6. Observe the difference.
7. Confirm that the secret value never appears in logs.

**Expected result:** A working secrets validation workflow and an understanding of secret scope.

---

## 6. OpenID Connect (OIDC)

### Important professional skill

OIDC is one of the most valuable concepts in modern cloud security.

It allows GitHub Actions to authenticate with supported external identity providers without storing long-lived cloud credentials as GitHub secrets.

### **6.1 The traditional approach**

Suppose you deploy a Django application to a cloud provider.

You might store a cloud access key in GitHub Secrets.

```text
GitHub Actions
      |
      v
Stored cloud access key
      |
      v
Cloud authentication
      |
      v
Deployment
```

The problem is that the credential may remain usable for a long period.

If it is compromised, it may remain usable until it is revoked or expires.

### **6.2 The OIDC approach**

With OIDC, GitHub Actions requests a short-lived identity token.

The cloud provider validates the token and issues temporary credentials according to a configured trust relationship.

```text
GitHub Actions
      |
      v
Request OIDC token
      |
      v
Cloud identity provider
      |
      v
Validate repository/workflow identity
      |
      v
Issue temporary credentials
      |
      v
Perform authorized operation
```

### **6.3 What is an identity token?**

An OIDC token is a signed identity assertion containing claims about the workload.

Depending on configuration, claims can identify:

- Repository.
- Repository owner.
- Branch or tag.
- Workflow.
- Environment.
- Audience.
- Actor.

The external identity provider uses these claims to determine whether the workflow is trusted.

### **6.4 Enable OIDC permission**

```yaml
name: OIDC Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  identity:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write

    steps:
      - name: Explain identity
        run: echo "OIDC permission is configured"
```

Important:

`id-token: write` allows a job to request an OIDC token.

It does not automatically grant access to a cloud account.

You still need to configure the cloud identity provider and its trust policy.

### **6.5 OIDC versus stored credentials**

| Feature | Long-lived credentials | OIDC |
|---|---|---|
| Stored cloud secret | Usually required | Not required |
| Credential lifetime | Potentially long | Short-lived |
| Identity validation | Credential-based | Claims and trust policy |
| Rotation | Manual or automated | Temporary credential issuance |
| Repository restrictions | Depends on credential design | Can be enforced through claims |

### **6.6 Where can OIDC be used?**

Examples include supported integrations with:

- AWS.
- Microsoft Azure.
- Google Cloud.
- HashiCorp Vault.
- Other OIDC-compatible identity providers.

### **6.7 Important security considerations**

OIDC is not automatically secure simply because you enable it.

You must:

1. Restrict `id-token: write` to the jobs that need it.
2. Configure a strict trust policy.
3. Restrict the repository and branch or environment.
4. Restrict the token audience.
5. Use minimal cloud IAM permissions.
6. Avoid exposing OIDC-enabled credentials to untrusted pull request code.

### **6.8 Practical exercise**

Create:

`.github/workflows/oidc-training.yml`

```yaml
name: OIDC Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  identity:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write

    steps:
      - name: Explain identity configuration
        run: |
          echo "OIDC identity permission is configured"
          echo "No cloud credentials are configured"
```

Tasks:

1. Run the workflow.
2. Inspect job-level permissions.
3. Explain the purpose of `id-token: write`.
4. Explain why it does not automatically grant cloud access.
5. Compare OIDC with a stored cloud access key.
6. Document how a cloud trust policy restricts repository identity.

Do not configure real cloud credentials for this exercise.

**Expected result:** An OIDC training workflow and a documented identity architecture.

---

## 7. Pull request security

Pull requests introduce an important security boundary.

A contributor can submit code that has not yet been reviewed.

Your workflow might automatically execute commands from that code.

This creates risk.

### **7.1 Trusted versus untrusted contributors**

Consider:

```text
Your repository
       |
       v
Contributor opens PR
       |
       v
GitHub Actions executes workflow
       |
       v
Tests run against submitted code
```

The workflow must not assume that every pull request contains trustworthy code.

### **7.2 The `pull_request` event**

Example:

```yaml
name: Pull Request CI

on:
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run validation
        run: echo "PR validation"
```

For pull requests from forks, GitHub applies security restrictions, including read-only token permissions and withholding ordinary repository secrets by default.

This helps separate untrusted contributions from privileged repository operations.

### **7.3 The `pull_request_target` event**

This event is different.

It runs in the context of the base repository and uses the workflow from the base repository's default branch.

It can receive elevated permissions and access to repository secrets.

Appropriate use cases can include:

- Automatically labeling pull requests.
- Managing trusted metadata.
- Posting authenticated responses.
- Performing controlled repository administration.

### **7.4 Dangerous workflow design**

Do not combine a privileged `pull_request_target` workflow with checking out and executing untrusted pull request code.

For example, this design is unsafe:

```yaml
on:
  pull_request_target:

jobs:
  unsafe:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}

      - run: npm install
      - run: npm test
```

The workflow has an elevated trust context, but the checked-out code is controlled by the pull request contributor.

Dependency installation and test commands may execute contributor-controlled scripts.

GitHub specifically warns against this combination.

### **7.5 Comparison**

| Feature | `pull_request` | `pull_request_target` |
|---|---|---|
| Workflow context | Pull request validation context | Base repository context |
| Fork security | Restricted token and secrets | Privileged context |
| Appropriate use | Build and test PR code | Trusted metadata automation |
| Executes untrusted PR code safely by default | Normal restrictions apply | No, not with privileged access |

### **7.6 Rule to remember**

Use `pull_request` for ordinary validation.

Use `pull_request_target` only when you understand why the elevated context is necessary and can guarantee that untrusted code is never executed with privileged access.

### **7.7 Practical exercise**

Create:

`docs/github/module-04-actions/pull-request-security.md`

Document:

1. What happens when a contributor opens a pull request?
2. What is the purpose of `pull_request`?
3. What is the purpose of `pull_request_target`?
4. Why are fork pull requests treated differently?
5. Which operations should never run in a privileged context using untrusted code?

**Expected result:** A documented pull request security model for your repository.

---

## 8. Script injection vulnerabilities

Script injection occurs when untrusted data is inserted into a command or script in a way that causes it to be interpreted as executable code.

GitHub Actions workflows frequently use event data such as:

- Pull request titles.
- Pull request bodies.
- Branch names.
- Issue titles.
- Issue comments.
- Review comments.

These values should be treated as untrusted input.

### **8.1 Vulnerable pattern**

Imagine a workflow that validates pull request titles.

```yaml
name: PR Title Validation

on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Validate title
        run: |
          title="${{ github.event.pull_request.title }}"
          echo "Checking title"
```

The problem is that the pull request title is controlled by the contributor.

Directly inserting it into a shell script can change how the script is interpreted.

### **8.2 Secure approach: environment variables**

A safer pattern is to pass the value through an environment variable.

```yaml
name: Secure PR Title Validation

on:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Validate title
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}

        run: |
          echo "Checking pull request title"

          if [ -z "$PR_TITLE" ]; then
            echo "Title is missing"
            exit 1
          fi

          echo "Title validation completed"
```

The expression is evaluated into an environment variable rather than being inserted into the shell program itself.

This is safer, although you must still validate and handle the data correctly.

### **8.3 Other potentially untrusted values**

Be careful with:

```text
github.event.issue.title
github.event.issue.body
github.event.pull_request.title
github.event.pull_request.body
github.head_ref
github.event.comment.body
github.event.review.body
```

### **8.4 Security rules**

- Never directly interpolate untrusted values into shell scripts.
- Pass values through environment variables.
- Quote shell variables.
- Validate inputs.
- Avoid evaluating user-controlled content.
- Avoid using `eval`.
- Avoid constructing shell commands from user-controlled strings.

### **8.5 Practical exercise**

Create:

`.github/workflows/pr-title-validation.yml`

Tasks:

1. Trigger the workflow on pull requests.
2. Read the pull request title.
3. Check whether the title is empty.
4. Print a validation result.
5. Pass the title through an environment variable.
6. Avoid unsafe shell interpolation.
7. Document why this pattern is safer.

**Expected result:** A secure pull request metadata validation workflow.

---

## 9. Artifact poisoning and cache poisoning

In Lesson 39, we studied artifacts and caching.

Now we need to understand their security implications.

### **9.1 Artifact poisoning**

Artifact poisoning occurs when untrusted workflow execution influences a build artifact that another workflow later trusts.

Consider:

```text
Untrusted pull request
        |
        v
Build workflow
        |
        v
Upload artifact
        |
        v
Privileged deployment workflow
        |
        v
Deploy artifact
```

The deployment workflow must not assume that an artifact is trustworthy merely because it was uploaded to GitHub Actions.

### **9.2 Secure artifact handling**

Before deploying an artifact, establish:

- Which repository produced it.
- Which workflow produced it.
- Which commit produced it.
- Whether the workflow was trusted.
- Whether the artifact was verified.
- Whether it corresponds to the intended release.

Artifact attestations can help establish this provenance.

### **9.3 Cache poisoning**

Cache poisoning occurs when untrusted workflow execution influences cached data that a later, more privileged workflow restores and trusts.

Consider:

```text
Untrusted workflow
        |
        v
Cache data
        |
        v
Privileged workflow
        |
        v
Restored cache
        |
        v
Unexpected data is trusted
```

GitHub applies restrictions to cache access for lower-trust workflow triggers, but explicitly enabling write-capable cache access or designing unsafe cache boundaries can reintroduce risks.

### **9.4 Artifact versus cache**

| Feature | Artifact | Cache |
|---|---|---|
| Main purpose | Store and transfer workflow outputs | Reuse data to improve performance |
| Typical content | Build packages, reports, test outputs | Dependencies and reusable build data |
| Lifetime | Configurable retention | Cache policy and eviction |
| Security concern | Trusting the origin of an artifact | Trusting restored cached content |
| Deployment use | Can be a deployment input after verification | Should not be treated as a trusted release artifact |

### **9.5 Practical security rules**

| Area | Recommended practice |
|---|---|
| Artifacts | Validate provenance |
| Caches | Do not trust untrusted cache contents |
| Deployment | Deploy verified build outputs |
| Pull requests | Separate untrusted and privileged jobs |
| Workflow triggers | Avoid unnecessary privileged triggers |
| Permissions | Use least privilege |

### **9.6 Your DRF + React example**

Imagine the backend pipeline creates:

```text
backend-dist/
├── application.tar.gz
├── requirements.txt
└── build-info.json
```

The deployment workflow should verify that the artifact came from the intended trusted build.

Do not accept arbitrary artifacts from an untrusted pull request as production deployment inputs.

### **9.7 Practical exercise**

Create:

`docs/github/module-04-actions/artifact-cache-poisoning.md`

Document:

1. The difference between artifacts and caches.
2. How an untrusted workflow can affect later workflow execution.
3. Why a successful upload does not establish artifact trust.
4. How your deployment pipeline will verify artifact origin.
5. How you will separate pull request builds from production deployment.

**Expected result:** An artifact and cache security policy.

---

## 10. Software supply chain security

Software supply chain security protects everything involved in creating, distributing, and deploying software.

This includes:

- Source code.
- Dependencies.
- Build tools.
- CI/CD workflows.
- Third-party Actions.
- Containers.
- Build artifacts.
- Deployment processes.

### **10.1 Visualize your software supply chain**

### 1. Source code

Your Django and React repositories.

### 2. Dependencies

Python packages and npm packages.

### 3. Build environment

GitHub Actions runners and build tools.

### 4. Build artifacts

Application packages and Docker images.

### 5. Distribution

GitHub Releases and container registries.

### 6. Deployment

Staging and production infrastructure.

### **10.2 Common supply chain risks**

| Risk | Example |
|---|---|
| Dependency compromise | Malicious npm package |
| Action compromise | Compromised third-party Action |
| Source compromise | Unauthorized source modification |
| Build compromise | Compromised build process |
| Artifact compromise | Modified Docker image |
| Distribution compromise | Unauthorized package publication |

### **10.3 Security technologies**

| Technology | Purpose |
|---|---|
| Dependabot | Dependency update automation |
| Dependency Review | Review dependency changes in PRs |
| CodeQL | Semantic code security analysis |
| Gitleaks | Detect exposed secrets |
| Trivy | Scan dependencies, containers, and configurations |
| Syft | Generate SBOMs |
| Cosign | Sign and verify software artifacts |
| Sigstore | Open-source signing infrastructure |
| SLSA | Software supply chain security framework |

Lesson 40 connects these technologies into one delivery architecture.

### **10.4 Practical exercise**

Create:

`docs/github/module-04-actions/software-supply-chain-security.md`

Document the supply chain for your DRF + React application.

For each stage, identify:

- Input.
- Output.
- Security risk.
- Security control.
- Evidence of verification.

**Expected result:** A documented software supply chain security model.

---

## 11. SBOM — Software Bill of Materials

### Important

An SBOM is a structured inventory of software components used to build or distribute an application.

Think of it as an ingredient list for your software.

### **11.1 Example**

Your Django application might depend on:

```text
Django
Django REST Framework
psycopg
Celery
Redis
Pillow
```

Your React application might depend on:

```text
React
Vite
Axios
TanStack Query
Zod
Zustand
```

An SBOM records information about these components and, depending on the format and generator, their versions, relationships, licenses, and other metadata.

### **11.2 Why do we need an SBOM?**

Suppose a vulnerability is discovered in a package.

Without an inventory, you may need to inspect multiple dependency files and build systems manually.

With an SBOM, you have a structured inventory that can be searched and analyzed.

### **11.3 Common SBOM formats**

| Format | Description |
|---|---|
| SPDX | Software component and licensing information |
| CycloneDX | Software composition and supply chain information |

### **11.4 Generate an SBOM with Syft**

For an existing application directory:

```powershell
syft dir:./backend -o cyclonedx-json > backend-sbom.json
```

For the frontend:

```powershell
syft dir:./frontend -o cyclonedx-json > frontend-sbom.json
```

These commands are examples. Make sure Syft is installed and your project directories contain the dependencies you want inventoried.

The completeness of the SBOM depends on what Syft can identify from the directory or image you scan.

### **11.5 Inspect the output**

An SBOM contains structured information rather than being just a plain list.

A simplified conceptual example:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "components": [
    {
      "type": "library",
      "name": "django",
      "version": "5.x"
    },
    {
      "type": "library",
      "name": "requests",
      "version": "2.x"
    }
  ]
}
```

This is an illustrative example, not a complete production SBOM.

### **11.6 SBOM in CI/CD**

```text
Source code
    |
    v
Install dependencies
    |
    v
Build application
    |
    v
Generate SBOM
    |
    v
Scan dependencies
    |
    v
Store SBOM
    |
    v
Publish verified release
```

### **11.7 Practical exercise**

Generate:

```text
security/
├── backend-sbom.json
└── frontend-sbom.json
```

Inspect:

- Package names.
- Package versions.
- Licenses.
- Dependency relationships.
- Transitive dependencies.

Document how you would use an SBOM when a vulnerability is announced.

Do not commit generated SBOMs containing information you consider sensitive without reviewing their contents and repository policy.

**Expected result:** Two SBOM files and a documented explanation of their contents.

---

## 12. Sigstore and artifact signing

An SBOM tells you what software components are included.

An artifact signature helps establish that an artifact corresponds to a particular signing identity and has not changed since signing.

These solve different problems.

### **12.1 What is Sigstore?**

Sigstore is an open-source project providing tools and infrastructure for signing and verifying software artifacts.

Its ecosystem includes:

- Cosign.
- Fulcio.
- Rekor.

### **12.2 The signing process**

```text
Build artifact
      |
      v
Establish signing identity
      |
      v
Sign artifact
      |
      v
Store signature and transparency information
      |
      v
Verify before consumption
```

### **12.3 Cosign**

Cosign is part of the Sigstore ecosystem.

It supports signing and verifying container images and other artifacts.

For example, a container image might be identified by its digest:

```text
ghcr.io/example/restaurant-api@sha256:...
```

Using a digest instead of relying only on a mutable tag gives you a precise artifact reference.

### **12.4 Signing versus provenance**

| Concept | What it establishes |
|---|---|
| Signature | Artifact integrity and signing identity |
| Provenance | Where and how the artifact was built |
| SBOM | What components are included |
| Verification | Whether required security claims can be validated |

A signed artifact is not automatically a secure artifact.

You still need to assess its source, build process, dependencies, and signing identity.

### **12.5 Practical exercise**

Create:

`docs/github/module-04-actions/sigstore-artifact-signing.md`

Document:

1. What Sigstore is.
2. What Cosign does.
3. What Fulcio does.
4. What Rekor does.
5. What a signature establishes.
6. Why a signature is not the same as provenance.
7. Why verification should happen before deployment.

**Expected result:** A documented artifact signing and verification design.

---

## 13. GitHub artifact attestations

GitHub provides artifact attestations to establish build provenance for software artifacts.

An attestation can help establish:

- Which repository produced an artifact.
- Which workflow produced it.
- Which source revision was used.
- How the artifact was built.

### **13.1 Why attestations matter**

Imagine two Docker images:

```text
restaurant-api:v1.0.0
restaurant-api:v1.0.0
```

Both have the same tag.

But how do you know they were built from the same source code?

A tag alone cannot establish that.

An attestation adds verifiable information about an artifact's origin and build process.

### **13.2 Generate a binary attestation**

The following is a simplified workflow example:

```yaml
name: Artifact Attestation Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      id-token: write
      attestations: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Generate artifact
        run: |
          mkdir -p dist
          echo "Training artifact" > dist/application.txt

      - name: Generate attestation
        uses: actions/attest@v4
        with:
          subject-path: dist/application.txt
```

This demonstrates the permission model and attestation step.

For a production workflow:

- Pin the Action to a verified full commit SHA.
- Review the current Action documentation.
- Confirm that the repository is eligible to use the feature.
- Verify the resulting attestation.

### **13.3 Verify an attestation**

With GitHub CLI:

```powershell
gh attestation verify `
  dist/application.txt `
  -R OWNER/REPOSITORY
```

Replace the placeholders with your actual repository details.

### **13.4 Private repository limitations**

GitHub artifact attestation availability depends on repository visibility and plan eligibility.

The attached lesson source identifies an Enterprise Cloud requirement for private and internal repository use.

Check the current GitHub documentation and your account's plan before designing an exercise that depends on this feature.

You can still study the workflow architecture in your private training repository without assuming that attestation generation will succeed.

### **13.5 Practical exercise**

Create:

`docs/github/module-04-actions/github-artifact-attestations.md`

Document:

1. What an attestation is.
2. What information it can establish.
3. Why a container tag is insufficient.
4. What permissions an attestation workflow needs.
5. How to verify an attestation with GitHub CLI.
6. What repository eligibility restrictions apply.

**Expected result:** A documented artifact provenance verification process.

---

## 14. CodeQL and SAST integration

### **14.1 What is SAST?**

SAST stands for Static Application Security Testing.

It analyzes source code without requiring the application to be running.

It can help detect issues such as:

- SQL injection patterns.
- Insecure input handling.
- Path traversal.
- Unsafe deserialization.
- Hardcoded credentials.
- Other vulnerable coding patterns.

SAST does not replace code review, dependency scanning, or runtime security testing.

### **14.2 What is CodeQL?**

CodeQL is GitHub's semantic code analysis engine.

It analyzes supported languages and can produce security findings in GitHub code scanning.

### **14.3 CodeQL architecture**

```text
Developer pushes code
        |
        v
GitHub Actions
        |
        v
CodeQL database creation
        |
        v
Code analysis
        |
        v
Security findings
        |
        v
Code scanning alerts
```

### **14.4 Example CodeQL workflow**

The following is an illustrative advanced-setup example:

```yaml
name: CodeQL Security Analysis

on:
  push:
    branches: [main]

  pull_request:
    branches: [main]

  schedule:
    - cron: "30 2 * * 1"

permissions:
  contents: read

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest

    permissions:
      contents: read
      security-events: write

    strategy:
      matrix:
        language:
          - javascript-typescript
          - python

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v4
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v4

      - name: Analyze
        uses: github/codeql-action/analyze@v4
```

For production:

- Use verified full commit SHAs.
- Confirm the current CodeQL configuration.
- Confirm supported language setup.
- Review workflow permissions.
- Check repository eligibility.

### **14.5 CodeQL for your projects**

| Project | Language |
|---|---|
| Django REST Framework | Python |
| React | JavaScript / TypeScript |
| Mobile application | TypeScript / JavaScript |
| Infrastructure scripts | Depends on language |

### **14.6 Private repository considerations**

Code scanning availability depends on repository visibility and GitHub's security product licensing.

Private repositories generally require the applicable GitHub Code Security entitlement.

For your private training repository, investigate eligibility before planning to activate CodeQL through GitHub's code scanning interface.

You can still study local static analysis and understand the workflow configuration.

### **14.7 Practical exercise**

Create:

`docs/github/module-04-actions/codeql-sast-integration.md`

Document:

1. What SAST means.
2. What CodeQL analyzes.
3. Which languages your projects use.
4. How CodeQL integrates with GitHub Actions.
5. What permissions the analysis job needs.
6. What repository licensing restrictions apply.
7. How your team should triage security findings.

**Expected result:** A CodeQL integration plan for DRF and React.

---

## 15. Secret scanning and push protection

Secret scanning searches repositories for credentials and other sensitive values.

It can detect accidentally committed:

- API tokens.
- Cloud credentials.
- Database passwords.
- Private keys.
- Service credentials.

### **15.1 Secret scanning**

Navigate to:

`Repository → Security → Secret scanning`

When available, GitHub can identify supported secret patterns in repository content.

### **15.2 Push protection**

Push protection helps prevent supported secrets from being pushed to a repository.

Conceptually:

```text
Developer commits code
        |
        v
Attempts to push
        |
        v
Secret detection
        |
        +---- No supported secret detected
        |          |
        |          v
        |       Push allowed
        |
        +---- Supported secret detected
                   |
                   v
              Push blocked
```

The exact behavior depends on the secret type, repository configuration, and feature availability.

### **15.3 Gitleaks integration**

You have already studied Gitleaks.

It can be used as an additional secret-detection layer in CI.

Example:

```yaml
name: Secret Detection

on:
  pull_request:

permissions:
  contents: read

jobs:
  secrets:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

This is a training example.

For production:

- Pin the Action to a verified full commit SHA.
- Review its configuration.
- Understand which files and commits are scanned.
- Review its permission requirements.

### **15.4 Gitleaks configuration**

Create:

`.gitleaks.toml`

Example:

```toml
[extend]
useDefault = true

[allowlist]
description = "Training repository allowlist"
paths = [
  '''docs/examples/'''
]
```

Only allowlist files when you have reviewed them and confirmed that they cannot contain actual credentials.

Do not broadly exclude directories simply to make scans pass.

### **15.5 Detection versus prevention**

| Technology | Role |
|---|---|
| Gitleaks | Detect exposed secrets |
| GitHub Secret Scanning | Detect supported secret patterns |
| Push Protection | Prevent supported secrets from being pushed |
| GitHub Secrets | Store workflow credentials |
| OIDC | Avoid storing long-lived cloud credentials |

**Important:** If a real credential has been exposed, removing it from the latest commit is not sufficient.

Revoke or rotate the credential and investigate where it may have been accessed.

### **15.6 Practical exercise**

Create:

`.github/workflows/gitleaks.yml`

```yaml
name: Gitleaks Security Scan

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  scan:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

Tasks:

1. Configure Gitleaks.
2. Scan your training repository.
3. Inspect workflow logs.
4. Understand detection versus prevention.
5. Pin the Action to a verified full SHA.
6. Document your allowlist policy.

Never introduce an actual credential to test secret detection.

**Expected result:** A working secret scanning workflow.

---

## 16. Dependabot and dependency review

You studied Dependabot earlier in your GitHub training.

Now we will connect it with CI/CD security.

### **16.1 Dependabot**

Dependabot helps keep dependencies updated and identifies dependency vulnerabilities.

It supports ecosystems including:

- npm.
- pip.
- Docker.
- GitHub Actions.
- Other supported package managers.

### **16.2 Configure Dependabot**

Create:

`.github/dependabot.yml`

```yaml
version: 2

updates:
  - package-ecosystem: pip
    directory: "/backend"
    schedule:
      interval: weekly

  - package-ecosystem: npm
    directory: "/frontend"
    schedule:
      interval: weekly

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly

  - package-ecosystem: docker
    directory: "/"
    schedule:
      interval: weekly
```

Adjust the directories to match your actual repository structure.

For example, if your Dockerfiles are stored under `docker/`, configure the Docker update location accordingly.

### **16.3 Dependency Review**

Dependency Review checks dependency changes introduced by a pull request.

Example:

```yaml
name: Dependency Review

on:
  pull_request:

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
```

For production, pin the Action to a verified full SHA.

### **16.4 Example scenario**

A developer updates a dependency:

```text
Django 5.0
    |
    v
Django 5.1
```

The pull request introduces a dependency change.

Dependency Review evaluates the introduced dependencies against its vulnerability data and configured policy.

Depending on the findings, the pull request can be blocked from passing its security check.

### **16.5 Dependabot versus Dependency Review**

| Feature | Dependabot | Dependency Review |
|---|---|---|
| Dependency updates | Yes | No |
| Vulnerability alerts | Yes, where configured and supported | Evaluates PR changes |
| Update PR creation | Yes | No |
| PR dependency analysis | Not its main role | Yes |
| Security policy enforcement | Through configuration and related features | Configurable CI checks |

### **16.6 Practical exercise**

Create:

`.github/dependabot.yml`

Configure:

- Python dependencies.
- npm dependencies.
- GitHub Actions dependencies.
- Docker dependencies.

Tasks:

1. Configure weekly updates.
2. Inspect Dependabot alerts where available.
3. Review dependency update pull requests.
4. Configure Dependency Review.
5. Document your dependency update policy.
6. Explain how you will test updates before merging them.

**Expected result:** Dependabot configuration and a documented dependency review process.

---

## 17. Container image security

Your DRF + React applications will eventually use Docker images.

These images can contain:

- Operating system packages.
- Python packages.
- Node.js packages.
- Build tools.
- Application source code.
- Configuration files.

A vulnerable dependency in a container can introduce security risk even when your application code is correct.

### **17.1 Container security pipeline**

```text
Dockerfile
    |
    v
Build Docker image
    |
    v
Scan image
    |
    v
Review vulnerabilities
    |
    v
Generate SBOM
    |
    v
Publish approved image
    |
    v
Deploy
```

### **17.2 Trivy**

You have previously studied Trivy.

It can scan:

- Container images.
- Filesystems.
- Dependency configurations.
- Infrastructure-as-code files.
- Other supported targets.

Example:

```powershell
trivy image my-restaurant-api:latest
```

Scan your project configuration:

```powershell
trivy config .
```

### **17.3 Dockerfile security practices**

For your Django backend:

- Use trusted base images.
- Avoid unnecessary packages.
- Use multi-stage builds where appropriate.
- Do not embed credentials in image layers.
- Avoid running as root where possible.
- Keep dependencies updated.
- Scan generated images.
- Use image digests for deployment references.

### **17.4 Example non-root execution**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser

USER appuser

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

This is a training Dockerfile, not a complete production configuration.

Django's development server should not be used as the production application server.

### **17.5 Practical exercise**

Create:

`docs/github/module-04-actions/container-security-lab.md`

Document how to:

1. Build a Docker image.
2. Scan it using Trivy.
3. Generate an SBOM using Syft.
4. Identify vulnerable packages.
5. Update vulnerable dependencies.
6. Rebuild the image.
7. Compare the scan results.
8. Record unresolved findings.

**Expected result:** A documented container security process.

---

## 18. Self-hosted runner security

In Lesson 37, we studied GitHub Actions runners.

Now let's look at their security implications.

### **18.1 GitHub-hosted versus self-hosted**

| Feature | GitHub-hosted | Self-hosted |
|---|---|---|
| Infrastructure | Managed by GitHub | Managed by you |
| Maintenance | GitHub | Your team |
| Environment isolation | Hosted runner environment | Depends on implementation |
| Network access | Hosted runner network | Your network configuration |
| Security responsibility | Shared responsibility | Greater operational responsibility |

### **18.2 Why self-hosted runners are sensitive**

Imagine a self-hosted runner inside your private network.

It might have network access to:

- Internal databases.
- Private services.
- Deployment infrastructure.
- Internal APIs.
- Other company systems.

If untrusted workflow code compromises the runner, an attacker may gain access to resources reachable from that machine.

This is why self-hosted runners require careful isolation and access control.

### **18.3 Recommended security architecture**

```text
GitHub Actions
      |
      v
Controlled runner group
      |
      v
Restricted repository access
      |
      v
Ephemeral runner
      |
      v
Single job execution
      |
      v
Restricted network access
```

### **18.4 Security recommendations**

- Prefer GitHub-hosted runners for ordinary CI.
- Do not execute untrusted pull request code on privileged self-hosted runners.
- Use ephemeral runners where appropriate.
- Separate runner groups by trust level.
- Restrict repository access.
- Avoid storing permanent credentials on runners.
- Restrict network access.
- Keep runner software updated.
- Monitor runner activity.
- Destroy or reset temporary runner environments after use.

GitHub recommends ephemeral runner designs for autoscaling and explains their security advantages.

### **18.5 Your infrastructure**

For your future restaurant SaaS platform:

```text
GitHub
   |
   v
CI on GitHub-hosted runners
   |
   v
Verified Docker image
   |
   v
Protected deployment job
   |
   v
Production server
```

Avoid giving ordinary pull request workflows direct access to your production network.

### **18.6 Practical exercise**

Create:

`docs/github/module-04-actions/self-hosted-runner-security.md`

Document:

1. The difference between hosted and self-hosted runners.
2. Why persistent runners introduce risk.
3. What ephemeral runners are.
4. How runner groups restrict access.
5. Why untrusted pull requests should not run on privileged runners.
6. How your future deployment architecture will isolate runners.

**Expected result:** A self-hosted runner security policy.

---

## 19. Enterprise Actions governance

So far, we have secured individual workflows.

Now we need to consider the repository and organization level.

Enterprise governance establishes rules that developers cannot accidentally bypass through inconsistent workflow configurations.

### **19.1 Governance areas**

| Area | Example control |
|---|---|
| Actions permissions | Restrict allowed Actions |
| Token permissions | Read-only defaults |
| SHA pinning | Require immutable Action references |
| Secrets | Limit access by repository and environment |
| Environments | Required production reviewers |
| Runners | Restricted runner groups |
| Branches | Required status checks |
| Security | Code scanning and secret detection |
| Audit | Review workflow and permission changes |

### **19.2 Repository settings**

Navigate to:

`Settings → Actions → General`

Review:

1. Actions permissions.
2. Fork pull request workflow permissions.
3. Workflow permissions.
4. Allowed Actions.
5. Artifact and log retention.

### **19.3 Branch protection**

Navigate to:

`Settings → Branches`

For your `main` branch, consider:

- Require a pull request before merging.
- Require approvals where appropriate.
- Require status checks.
- Require conversation resolution.
- Restrict force pushes.
- Restrict branch deletion.

### **19.4 Organization policies**

When you later work with GitHub Organizations, you can centralize certain policies across repositories.

For example:

```text
Organization
    |
    +---- Repository A
    |
    +---- Repository B
    |
    +---- Repository C
```

The organization can define common Actions policies and restrict which Actions are permitted.

This is particularly useful when managing multiple applications.

### **19.5 Practical exercise**

Create:

`docs/github/module-04-actions/enterprise-actions-governance.md`

Define a baseline policy for three hypothetical repositories:

- `restaurant-api`
- `restaurant-dashboard`
- `restaurant-mobile`

For each repository, document:

1. Default token permissions.
2. Allowed Actions policy.
3. Action SHA pinning policy.
4. Branch protection requirements.
5. Environment protection requirements.
6. Secret access policy.
7. Runner access policy.
8. Security scanning requirements.

**Expected result:** A reusable Actions governance baseline.

---

## 20. Build a hardened DRF + React CI/CD pipeline

Now we combine the entire lesson into a realistic architecture.

This is the main engineering project for Lesson 40.

### **20.1 Application structure**

```text
restaurant-platform/
│
├── backend/
│   ├── config/
│   ├── apps/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── tests/
│   └── package.json
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── security/
│   ├── backend-sbom.json
│   └── frontend-sbom.json
│
└── .github/
    ├── dependabot.yml
    └── workflows/
```

### **20.2 Proposed pipeline**

#### Pull request

Untrusted code boundary.

#### Backend

Ruff · Pytest · Code analysis.

#### Frontend

ESLint · TypeScript · Tests.

#### Secrets

Gitleaks · Secret scanning.

#### Dependencies

Dependabot · Dependency Review.

#### Trusted build

Docker · Trivy · SBOM.

#### Artifact verification

Digest · Provenance · Attestation where eligible.

#### Protected deployment

OIDC · Environment approval · Health checks.

### **20.3 Security requirements**

| Requirement | Implementation |
|---|---|
| Workflow access | Least-privilege `GITHUB_TOKEN` |
| Third-party Actions | Full SHA pinning |
| Credentials | GitHub Secrets or OIDC |
| Pull requests | Unprivileged validation |
| Python dependencies | Dependabot and vulnerability review |
| JavaScript dependencies | Dependabot and vulnerability review |
| Static analysis | CodeQL where eligible |
| Secret detection | Gitleaks |
| Container scanning | Trivy |
| SBOM | Syft |
| Provenance | GitHub attestations where eligible |
| Deployment | Protected environment |
| Infrastructure | Restricted deployment credentials |

### **20.4 Security policy**

For this project, define the following rules:

1. No production credentials in source code.
2. No unnecessary `GITHUB_TOKEN` write permissions.
3. Third-party Actions must be reviewed and pinned.
4. Pull request workflows must not expose production credentials.
5. Dependencies must be reviewed.
6. Docker images must be scanned.
7. Production deployment must require authorization.
8. Deployment artifacts must have traceable origins.
9. Vulnerability findings must be reviewed and documented.
10. Security exceptions must have a documented justification.

### **20.5 Design the complete workflow architecture**

Create:

`docs/github/module-04-actions/hardened-cicd-architecture.md`

Your document must contain:

```markdown
# Hardened DRF + React CI/CD Architecture

## 1. Application Overview

## 2. Threat Model

## 3. Workflow Permissions

## 4. Third-Party Action Policy

## 5. Secrets Management

## 6. OIDC Authentication

## 7. Pull Request Security

## 8. Backend Security Checks

## 9. Frontend Security Checks

## 10. Dependency Security

## 11. Secret Detection

## 12. Container Security

## 13. SBOM Generation

## 14. Artifact Provenance

## 15. Environment Protection

## 16. Deployment Security

## 17. Runner Isolation

## 18. Vulnerability Response

## 19. Recovery Procedures

## 20. Security Exceptions
```

**Expected result:** A complete security architecture document connecting the topics from this lesson.

---

## 21. Practical exercises — GitHub Deep Dive Training

We will use your existing private repository:

`github-deep-dive-training`

The objective is to create a security laboratory, not just read examples.

Complete these exercises in order.

### **Exercise 1 — Least-privilege permissions**

#### Required

Create:

`.github/workflows/security-permissions.yml`

Use the workflow from Section 3.

Tasks:

1. Run the workflow.
2. Inspect its permissions.
3. Change the permissions to `{}`.
4. Observe the checkout behavior.
5. Restore `contents: read`.
6. Explain least privilege.

**Deliverable:** A working workflow and a permissions explanation.

### **Exercise 2 — Third-party Action security**

Create:

`docs/github/module-04-actions/action-security-review.md`

Review:

- `actions/checkout`
- `actions/setup-python`
- `actions/setup-node`

For each one, document its publisher, repository, release, verified SHA, permissions, dependencies, and security considerations.

Then create a workflow using verified full commit SHAs.

**Deliverable:** Three Action reviews and one secure workflow.

### **Exercise 3 — Secrets management**

> Required

Create:

`.github/workflows/secrets-security.yml`

Use the workflow from Section 5.

Tasks:

1. Create a harmless training secret.
2. Add it to repository Actions secrets.
3. Execute the workflow.
4. Remove the secret.
5. Execute the workflow again.
6. Confirm that its value never appears in logs.

**Deliverable:** A working secrets validation workflow.

### **Exercise 4 — OIDC identity permissions**

Create:

`.github/workflows/oidc-training.yml`

Use the workflow from Section 6.

Tasks:

1. Run the workflow.
2. Inspect job-level permissions.
3. Explain `id-token: write`.
4. Explain why it does not automatically grant cloud access.
5. Compare OIDC with stored cloud credentials.

Do not configure real cloud credentials.

**Deliverable:** An OIDC training workflow and an identity explanation.

### **Exercise 5 — Pull request security**

Create:

`.github/workflows/pr-security.yml`

```yaml
name: Pull Request Security

on:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Validate PR metadata
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}

        run: |
          if [ -z "$PR_TITLE" ]; then
            echo "Invalid PR title"
            exit 1
          fi

          echo "PR metadata validation completed"
```

Tasks:

- Open a test pull request.
- Observe workflow execution.
- Inspect token permissions.
- Explain the difference between `pull_request` and `pull_request_target`.
- Document why privileged workflows must not execute untrusted PR code.

**Deliverable:** A secure pull request validation workflow.

### **Exercise 6 — Gitleaks**

Create:

`.github/workflows/gitleaks.yml`

Use the workflow from Section 15.

Tasks:

1. Configure Gitleaks.
2. Scan your training repository.
3. Inspect workflow logs.
4. Understand detection versus prevention.
5. Pin the Action to a verified full SHA.
6. Document your configuration.

Never introduce an actual credential to test secret detection.

**Deliverable:** A Gitleaks workflow and configuration.

### **Exercise 7 — Dependabot**

Create:

`.github/dependabot.yml`

Configure:

- Python dependencies.
- npm dependencies.
- GitHub Actions dependencies.
- Docker dependencies.

Tasks:

1. Configure weekly updates.
2. Inspect Dependabot alerts where available.
3. Review dependency update pull requests.
4. Configure Dependency Review.
5. Document your update policy.

**Deliverable:** Dependabot configuration and dependency review documentation.

### **Exercise 8 — Container security**

Create:

`docs/github/module-04-actions/container-security-lab.md`

Document how to:

1. Build a Docker image.
2. Scan it using Trivy.
3. Generate an SBOM using Syft.
4. Identify vulnerable packages.
5. Update vulnerable dependencies.
6. Rebuild the image.
7. Compare the scan results.

**Deliverable:** A container security report.

### **Exercise 9 — Supply chain provenance**

Create:

`docs/github/module-04-actions/supply-chain-provenance.md`

Document:

- What is an SBOM?
- What is provenance?
- What is an attestation?
- What is artifact signing?
- How does Sigstore work?
- How does GitHub verify attestations?
- What is SLSA?
- What limitations apply to private repositories?

**Deliverable:** A software supply chain provenance document.

### **Exercise 10 — Complete security architecture**

Create:

`docs/github/module-04-actions/hardened-cicd-architecture.md`

Design a secure pipeline for your DRF + React application.

Include:

- Threat model.
- Token permissions.
- Action pinning.
- Secret management.
- OIDC.
- Pull request isolation.
- Dependency scanning.
- CodeQL.
- Gitleaks.
- Trivy.
- SBOM.
- Provenance.
- Environment protection.
- Recovery procedures.

**Deliverable:** The complete hardened CI/CD architecture.

---

## 22. Repository documentation — files to create

Add this directory:

```text
docs/
└── github/
    └── module-04-actions/
        ├── lesson-40-workflow-security.md
        ├── github-actions-threat-model.md
        ├── github-token-permissions.md
        ├── third-party-actions-security.md
        ├── secrets-management.md
        ├── oidc-authentication.md
        ├── pull-request-security.md
        ├── script-injection-prevention.md
        ├── artifact-cache-poisoning.md
        ├── software-supply-chain-security.md
        ├── sbom-management.md
        ├── sigstore-artifact-signing.md
        ├── github-artifact-attestations.md
        ├── codeql-sast-integration.md
        ├── secret-scanning-gitleaks.md
        ├── dependabot-security.md
        ├── container-image-security.md
        ├── self-hosted-runner-security.md
        ├── enterprise-actions-governance.md
        ├── hardened-cicd-architecture.md
        ├── action-security-review.md
        ├── container-security-lab.md
        └── supply-chain-provenance.md
```

### **22.1 Main lesson Markdown file**

Create:

`docs/github/module-04-actions/lesson-40-workflow-security.md`

Use this structure:

```markdown
# Module 4 — GitHub Actions & CI/CD

# Lesson 40 — GitHub Actions Security, Supply Chain Security & Workflow Hardening

## 1. Lesson Overview
## 2. GitHub Actions Threat Modeling
## 3. Workflow Permissions and GITHUB_TOKEN
## 4. Third-Party GitHub Actions Security
## 5. Secrets Management
## 6. OpenID Connect (OIDC)
## 7. Pull Request Security
## 8. Script Injection Vulnerabilities
## 9. Artifact Poisoning and Cache Poisoning
## 10. Software Supply Chain Security
## 11. SBOM Management
## 12. Sigstore and Artifact Signing
## 13. GitHub Artifact Attestations
## 14. CodeQL and SAST Integration
## 15. Secret Scanning and Push Protection
## 16. Dependabot and Dependency Review
## 17. Container Image Security
## 18. Self-hosted Runner Security
## 19. Enterprise Actions Governance
## 20. Hardened DRF + React CI/CD Pipeline
## 21. Practical Exercises
## 22. Repository Documentation
## 23. GitHub Security Feature Availability
## 24. Git Workflow — Commit, PR, Tag and Release
## 25. Completion Checklist
## 26. Lessons Learned
## 27. Official Documentation and References
## 28. Next Lesson — Lesson 41
```

For the supporting files, use the explanations, examples, diagrams, and exercises from the corresponding sections of this lesson.

### **22.2 Suggested workflow files**

```text
.github/
├── dependabot.yml
└── workflows/
    ├── security-permissions.yml
    ├── secrets-security.yml
    ├── oidc-training.yml
    ├── pr-security.yml
    ├── pr-title-validation.yml
    └── gitleaks.yml
```

These are training workflows.

Do not activate real production deployment, cloud authentication, or privileged infrastructure access as part of this lesson.

---

## 23. GitHub security feature availability

Some GitHub security features have licensing restrictions.

Your training repository is private, so you should distinguish between:

1. Features you can practice directly.
2. Features you can study through configuration and documentation.
3. Features that require additional licensing or repository eligibility.

| Feature | Private repository consideration |
|---|---|
| Actions workflows | Available |
| Dependabot updates | Available |
| Repository secrets | Available |
| Environment protection | Check plan-specific restrictions |
| Code scanning | Requires applicable Code Security entitlement |
| Secret protection | Check applicable licensing |
| Artifact attestations | Check current Enterprise Cloud eligibility requirements |

This means you can learn the architecture and build many of the workflows in your private training repository without necessarily being able to activate every GitHub-hosted security feature.

**Important training rule:** A workflow that cannot execute because of a repository licensing restriction is not automatically a workflow configuration failure.

Document the limitation and continue studying the architecture.

---

## 24. Git workflow — commit, PR, tag and release

Continue using your established branch, pull request, tag, and release workflow.

We will create a separate branch for Lesson 40.

### **Step 1 — Create branch**

```powershell
git switch main
git pull origin main

git switch -c feat/lesson-40-actions-security
```

### **Step 2 — Create and validate files**

Create the documentation and workflow files described in this lesson.

Then inspect your changes:

```powershell
git status
git diff
git diff --check
```

Validate:

- YAML syntax.
- Workflow triggers.
- Token permissions.
- Third-party Action references.
- Secret handling.
- Dependabot configuration.
- Documentation links.

Do not commit actual credentials or production configuration.

### **Step 3 — Stage files**

```powershell
git add .github/workflows/
git add .github/dependabot.yml
git add docs/github/module-04-actions/
```

### **Step 4 — Commit**

Use this commit message:

```powershell
git commit -m "feat(actions): add workflow security and supply chain training"
```

### **Step 5 — Push**

```powershell
git push -u origin feat/lesson-40-actions-security
```

### **Step 6 — Create Pull Request**

### Pull request title

`feat(actions): add workflow security and supply chain training`

### Pull request description

```markdown
## Summary

Introduces Lesson 40 covering GitHub Actions security, DevSecOps, software supply chain protection, and hardened CI/CD architecture.

## Topics covered

- GitHub Actions threat modeling
- GITHUB_TOKEN permissions
- Third-party Action security and SHA pinning
- Secrets management
- OpenID Connect
- Pull request security
- Script injection prevention
- Artifact and cache poisoning
- SBOM and software supply chain security
- Sigstore and artifact attestations
- CodeQL and SAST
- Gitleaks and secret scanning
- Dependabot and dependency review
- Container image security
- Self-hosted runner security
- Enterprise Actions governance

## Validation

- Workflow permissions reviewed
- Third-party Actions reviewed
- Secrets exercise completed
- OIDC permissions understood
- Pull request security tested
- Gitleaks workflow tested
- Dependabot configured
- Container security documented
- SBOM architecture documented
- Supply chain security architecture completed
- No real credentials committed

## Notes

Cloud authentication, artifact attestation, and production deployment are studied without exposing production credentials or modifying production infrastructure.
```

Review the pull request before merging.

### **Step 7 — Merge and tag**

After your pull request has been reviewed and merged:

```powershell
git switch main
git pull origin main

git tag -a module-04-lesson-40 `
  -m "Module 4 Lesson 40: GitHub Actions Security"

git push origin module-04-lesson-40
```

### **Step 8 — Create GitHub Release**

| Field | Value |
|---|---|
| Tag | `module-04-lesson-40` |
| Title | Module 4 — Lesson 40: GitHub Actions Security |
| Description | Workflow security, secrets, OIDC, supply chain security, SBOM, attestations, CodeQL, and hardened CI/CD |

The release should represent the completed and merged Lesson 40 training material.

---

## 25. Lesson 40 completion checklist

### Lesson progress

### 0/23

- [ ] Understand GitHub Actions threat modeling.
- [ ] Configure least-privilege `GITHUB_TOKEN` permissions.
- [ ] Understand third-party Action security.
- [ ] Review and pin Actions to full SHAs.
- [ ] Understand repository and environment secrets.
- [ ] Understand OIDC authentication.
- [ ] Understand `pull_request` security.
- [ ] Understand `pull_request_target` risks.
- [ ] Prevent script injection.
- [ ] Understand artifact poisoning.
- [ ] Understand cache poisoning.
- [ ] Understand software supply chain security.
- [ ] Generate an SBOM.
- [ ] Understand Sigstore and Cosign.
- [ ] Understand artifact attestations.
- [ ] Understand CodeQL and SAST.
- [ ] Configure Gitleaks.
- [ ] Configure Dependabot.
- [ ] Understand container scanning with Trivy.
- [ ] Understand self-hosted runner isolation.
- [ ] Design enterprise Actions governance.
- [ ] Complete hardened DRF + React CI/CD architecture.
- [ ] Commit, merge, tag, and release.

### **25.1 Final engineering review**

Before considering this lesson complete, verify:

| Area | Verification |
|---|---|
| Permissions | No unnecessary write permissions |
| Actions | External Actions reviewed |
| SHA pinning | Full SHAs verified |
| Secrets | No real credentials committed |
| OIDC | Identity and trust model understood |
| Pull requests | Untrusted code isolated |
| Injection | Event data handled safely |
| Artifacts | Origin and trust requirements documented |
| Dependencies | Dependabot configured |
| Containers | Trivy scanning documented |
| SBOM | Backend and frontend inventory generated |
| Governance | Repository security baseline documented |
| Git workflow | PR merged and tag pushed |

---

## 26. Lessons learned

Lesson 40 connects workflow engineering with application and infrastructure security.

The most important principles are:

1. A CI/CD pipeline is part of your application's security boundary.
2. A workflow should receive only the permissions it needs.
3. Third-party Actions are executable code and must be reviewed.
4. Full commit SHA pinning provides an immutable Action reference.
5. Secrets should only be exposed to jobs that require them.
6. OIDC can replace long-lived cloud credentials when configured correctly.
7. Pull request code must be treated as untrusted.
8. Privileged workflows must not execute untrusted code.
9. Artifacts and caches have different purposes and security risks.
10. An SBOM provides a structured inventory of software components.
11. Signatures, provenance, and attestations establish different security properties.
12. Code scanning, secret scanning, and dependency scanning solve different problems.
13. Container images must be scanned before distribution and deployment.
14. Self-hosted runners require strong isolation.
15. Enterprise governance makes security policies consistent across repositories.

### The key principle

A successful CI/CD pipeline does not simply prove that your application can be built and deployed. It should also provide evidence that the source, dependencies, build process, artifacts, and deployment authorization meet your security requirements.

---

## 27. Official documentation and references

Keep these references in your repository.

| Topic | Documentation |
|---|---|
| GitHub Actions security | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| GITHUB_TOKEN | [GITHUB_TOKEN](https://docs.github.com/en/actions/concepts/security/github_token) |
| Workflow permissions | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| Action restrictions | [Managing GitHub Actions settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) |
| Secrets | [Using secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) |
| OIDC | [OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect) |
| Pull request security | [Securely using pull_request_target](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) |
| Script injection | [Script injections](https://docs.github.com/en/actions/concepts/security/script-injections) |
| CodeQL | [CodeQL code scanning](https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql) |
| Dependency Review | [Dependency Review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review) |
| Artifact attestations | [Artifact attestations](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations) |
| Self-hosted runners | [Self-hosted runners](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) |
| GitHub Advanced Security | [About GitHub Advanced Security](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security) |
| Gitleaks | [Gitleaks documentation](https://github.com/gitleaks/gitleaks) |
| Trivy | [Trivy documentation](https://trivy.dev/) |
| Syft | [Syft documentation](https://github.com/anchore/syft) |
| Sigstore | [Sigstore documentation](https://docs.sigstore.dev/) |
| Cosign | [Cosign documentation](https://docs.sigstore.dev/cosign/) |
| SLSA | [SLSA documentation](https://slsa.dev/) |

---

## 28. Next lesson — Lesson 41

### Advanced

### Enterprise DevSecOps

### GitHub Actions Advanced Security Automation & Compliance

Lesson 40 focused on securing individual workflows and the software supply chain.

Lesson 41 will move from individual workflow security controls to **automated security policies, compliance checks, vulnerability management, and organization-wide security governance**.

The objective is to build a centralized security automation framework that can evaluate repositories against defined security standards, detect policy violations, generate evidence, and track remediation.

### **Planned curriculum**

| # | Topic |
|---:|---|
| 1 | Security policy automation |
| 2 | GitHub security configurations |
| 3 | Repository security baselines |
| 4 | Organization-wide security policies |
| 5 | Security rulesets |
| 6 | Branch protection automation |
| 7 | Required security checks |
| 8 | CodeQL advanced configurations |
| 9 | Custom CodeQL queries |
| 10 | SARIF and security reporting |
| 11 | Vulnerability triage automation |
| 12 | Dependabot automation |
| 13 | Security issue creation |
| 14 | Automated vulnerability remediation |
| 15 | License compliance automation |
| 16 | SBOM policy enforcement |
| 17 | SLSA compliance |
| 18 | Supply chain security scorecards |
| 19 | OpenSSF Scorecard |
| 20 | Container compliance policies |
| 21 | Kubernetes security scanning |
| 22 | Terraform security scanning |
| 23 | Security dashboards and reporting |
| 24 | Audit trails and compliance evidence |
| 25 | ISO 27001 security control mapping |
| 26 | Enterprise DevSecOps governance |
| 27 | Complete automated security compliance pipeline |

### **Lesson 41 practical outcome**

Build a centralized security automation framework that can:

- Evaluate multiple repositories.
- Enforce common security baselines.
- Detect vulnerabilities and policy violations.
- Automate security issue creation.
- Track remediation.
- Generate SBOM and compliance evidence.
- Evaluate supply chain security.
- Produce security dashboards.
- Map technical controls to compliance requirements.

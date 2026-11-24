# Module 4 — GitHub Actions & CI/CD

## Lesson 34 — GitHub Actions: Complete CI/CD Deep Dive

**Level:** Intermediate → Advanced
**Estimated time:** 3–4 hours
**Repository:** `github-deep-dive-training`
**Main file:** `docs/github/module-04-actions/lesson-34-github-actions-fundamentals.md`

## Lesson overview

In this module, you will move from manually managing Issues and Pull Requests to automating parts of the software development lifecycle with GitHub Actions.

You will learn how workflows are triggered, how jobs run, how to pass data between jobs, and how to build CI pipelines. You will also study how these concepts apply to future Django REST Framework and React/Vite applications.

We will use two kinds of examples:

- **Training-repository exercises:** workflows that can run in `github-deep-dive-training` without requiring an application or production credentials.
- **Application examples:** reference configurations for a future Django + React project. Use these only after the matching project files and scripts exist.

> **Important:** A workflow file is executable automation. Review its triggers, permissions, commands, and third-party Actions before merging it. Do not add deployment workflows or production secrets to the training repository.

## Learning objectives

By the end of this lesson, you should be able to:

1. Explain CI, Continuous Delivery, and Continuous Deployment.
2. Describe workflows, events, jobs, steps, and runners.
3. Write and troubleshoot GitHub Actions YAML.
4. Configure event triggers and filters.
5. Compare GitHub-hosted and self-hosted runners.
6. Use job dependencies, conditions, and matrix strategies.
7. Work with environment variables, contexts, and expressions.
8. Distinguish secrets from variables and configure least-privilege `GITHUB_TOKEN` permissions.
9. Use artifacts and dependency caches appropriately.
10. Explain reusable workflows and composite Actions.
11. Design CI for Django, React/Vite, and PostgreSQL.
12. Understand Docker image publishing and deployment environments.
13. Apply practical workflow security controls.

## 1. What is GitHub Actions?

GitHub Actions is GitHub’s automation platform. It runs defined tasks when repository events occur or when a workflow is manually or periodically triggered.

Examples include:

- A developer pushes a commit.
- A Pull Request is opened or updated.
- A release is published.
- A workflow is started manually.
- A scheduled task runs.

For a restaurant management application, a CI workflow could:

1. Check out the repository.
2. Install Python and Node.js dependencies.
3. Run backend linting and tests.
4. Run frontend linting, type checks, and tests.
5. Build the frontend.
6. Report whether the checks passed.

The goal is to detect problems early and consistently—not to replace code review or developer judgment.

## 2. Continuous Integration and Continuous Delivery

| Concept | Meaning |
|---|---|
| **Continuous Integration (CI)** | Frequently integrate changes and automatically validate them. |
| **Continuous Delivery** | Keep software in a releasable state; production release may require approval. |
| **Continuous Deployment** | Automatically deploy qualifying changes to production after required checks pass. |

A sensible progression for a new application is:

1. Start with CI.
2. Add a controlled release process and staging deployment.
3. Add production deployment only after tests, backups, monitoring, access controls, and rollback procedures are reliable.

Automation can make a good process repeatable. It can also make a bad process fail faster.

## 3. GitHub Actions architecture

A workflow is a YAML file stored under `.github/workflows/`.

```text
.github/
└── workflows/
    ├── repository-ci.yml
    ├── backend-ci.yml
    └── frontend-ci.yml
```

A workflow contains one or more jobs. Each job runs on a runner and contains ordered steps.

| Term | Meaning |
|---|---|
| **Workflow** | The complete automation definition. |
| **Event / trigger** | The event that starts a workflow. |
| **Job** | A group of steps executed on a runner. |
| **Step** | A shell command or an Action within a job. |
| **Runner** | The machine that executes a job. |
| **Action** | A reusable unit of automation invoked with `uses:`. |

Jobs run in parallel by default unless dependencies or other constraints make them wait.

## 4. Workflow YAML structure

Create `.github/workflows/hello-github-actions.yml`:

```yaml
name: Hello GitHub Actions

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  hello:
    name: First Automation Job
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Display GitHub information
        run: |
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Branch: $GITHUB_REF_NAME"
          echo "Commit: $GITHUB_SHA"
          echo "Event: $GITHUB_EVENT_NAME"
          echo "Runner OS: $RUNNER_OS"

      - name: Confirm completion
        run: echo "Workflow completed."
```

The example uses readable major-version Action tags. For production, verify each Action’s source and release, and consider pinning third-party Actions to a verified full commit SHA.

### 4.1 Key properties

| Property | Purpose |
|---|---|
| `name` | Display name of the workflow or job. |
| `on` | Events that trigger the workflow. |
| `permissions` | Permissions granted to `GITHUB_TOKEN`. |
| `jobs` | Jobs defined in the workflow. |
| `runs-on` | Runner selected for a job. |
| `steps` | Ordered operations in a job. |
| `uses` | Invokes an Action. |
| `run` | Executes shell commands. |

YAML uses indentation to express structure. Use spaces, not tabs.

### 4.2 Exercise — Inspect a workflow run

1. Add the workflow to your lesson branch.
2. Push the branch and open a Pull Request targeting `main`.
3. Open **Actions** in the repository.
4. Select the workflow run and inspect each step.
5. Record the event name, branch, commit SHA, and runner OS.

## 5. Workflow triggers and events

### 5.1 Push

Runs when commits are pushed to selected branches:

```yaml
on:
  push:
    branches:
      - main
      - develop
```

You can filter by paths when only certain files should trigger a workflow:

```yaml
on:
  push:
    paths:
      - "backend/**"
      - "frontend/**"
```

Path filters should be chosen carefully. If a workflow is required for a Pull Request, ensure its filters do not accidentally prevent the required check from running.

### 5.2 Pull Request

```yaml
on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened
      - ready_for_review
```

Common activity types:

| Type | Meaning |
|---|---|
| `opened` | A Pull Request was opened. |
| `synchronize` | New commits were pushed to the Pull Request. |
| `reopened` | A closed Pull Request was reopened. |
| `ready_for_review` | A draft Pull Request was marked ready. |
| `closed` | A Pull Request was closed or merged. |

When `types` is omitted, GitHub uses the event’s default activity types.

### 5.3 Manual and scheduled triggers

Manual execution:

```yaml
on:
  workflow_dispatch:
```

Scheduled execution:

```yaml
on:
  schedule:
    - cron: "0 2 * * 1"
```

The schedule above is every Monday at 02:00 UTC. Scheduled workflows use UTC and run from the default branch. GitHub may delay scheduled runs during periods of high load.

A manual workflow can accept inputs, but treat those inputs as untrusted data. Do not insert user-controlled values directly into shell commands.

### 5.4 Other useful events

| Event | Typical use |
|---|---|
| `release` | Run automation when a release is published. |
| `issues` | Automate issue workflows. |
| `issue_comment` | React to issue or Pull Request comments. |
| `pull_request_review` | React to review activity. |
| `workflow_run` | Start a workflow after another workflow completes. |
| `workflow_call` | Define a reusable workflow. |
| `repository_dispatch` | Receive an event sent through the GitHub API. |
| `create` / `delete` | React to branch or tag creation/deletion. |

Reference: [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

### Exercise — Multi-trigger workflow

Create `.github/workflows/multi-trigger.yml`:

```yaml
name: Multi Trigger Practice

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect-event:
    runs-on: ubuntu-latest
    steps:
      - name: Display event details
        run: |
          echo "Event: $GITHUB_EVENT_NAME"
          echo "Branch: $GITHUB_REF_NAME"
          echo "Commit: $GITHUB_SHA"
```

Test the workflow using a push, a Pull Request, and manual execution. Record the event name for each run.

## 6. GitHub-hosted runners

GitHub-hosted runners are managed by GitHub. They provide a temporary execution environment for a job.

Examples:

```yaml
runs-on: ubuntu-latest
```

```yaml
runs-on: windows-latest
```

```yaml
runs-on: macos-latest
```

### Advantages

- No runner installation or maintenance.
- Convenient operating-system choices.
- A fresh hosted environment for each job.
- Suitable for most learning, linting, testing, and build workflows.

### Limitations

- Limited control over machine configuration.
- Usage limits and possible billing for private repositories.
- Jobs depend on the hosted runner environment and available network services.

Check your repository’s plan and billing settings before running large or frequent workflows.

## 7. Self-hosted runners

A self-hosted runner is a machine you manage, such as a server or dedicated build machine.

```yaml
jobs:
  build:
    runs-on: self-hosted
    steps:
      - run: echo "Running on a self-hosted runner"
```

Labels can help select a specific runner:

```yaml
runs-on: [self-hosted, linux, x64]
```

Self-hosted runners can provide custom hardware or access to internal services, but they also create operational and security responsibilities.

**Do not run untrusted Pull Request code on a self-hosted runner that can access sensitive systems, credentials, or production networks.** A compromised runner can affect the machine and anything it can reach.

For learning and ordinary Django/React tests, start with GitHub-hosted runners. Consider self-hosted runners only when you have a specific need and a plan to isolate, patch, monitor, and reset them.

## 8. Jobs and dependencies

Independent jobs can run in parallel:

```yaml
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Backend checks"

  frontend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Frontend checks"
```

Use `needs` when a job must wait for other jobs:

```yaml
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Backend checks passed"

  frontend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Frontend checks passed"

  build:
    needs:
      - backend
      - frontend
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build application"
```

The `build` job starts only after both dependencies succeed.

### 8.1 Conditions

Use `if` to control execution:

```yaml
jobs:
  report:
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - run: echo "A previous job or step failed"
```

Common status-check functions include:

| Function | Meaning |
|---|---|
| `success()` | Previous steps or dependencies succeeded. |
| `failure()` | A previous step or dependency failed. |
| `always()` | Run even after failure, subject to cancellation. |
| `cancelled()` | The workflow or job was cancelled. |

### 8.2 Passing data between jobs

Jobs run on separate runners. Shell variables and files are not automatically shared.

Use job outputs for small values:

```yaml
jobs:
  prepare:
    runs-on: ubuntu-latest
    outputs:
      app_version: ${{ steps.version.outputs.value }}
    steps:
      - name: Set version
        id: version
        run: echo "value=1.0.0" >> "$GITHUB_OUTPUT"

  display:
    needs: prepare
    runs-on: ubuntu-latest
    steps:
      - name: Display version
        env:
          APP_VERSION: ${{ needs.prepare.outputs.app_version }}
        run: echo "Version: $APP_VERSION"
```

Use artifacts to transfer files between jobs.

## 9. Matrix strategies

A matrix runs the same job with different configurations.

```yaml
name: Python Matrix Practice

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: python --version
```

This creates three job executions.

A matrix can include multiple dimensions. Two operating systems and two Python versions produce four combinations. Use `include` to add combinations and `exclude` to remove combinations.

| Option | Purpose |
|---|---|
| `fail-fast` | Cancel remaining matrix jobs after a failure. |
| `max-parallel` | Limit concurrent matrix jobs. |
| `include` | Add selected combinations or values. |
| `exclude` | Remove selected combinations. |

**Exercise:** Create a Node.js matrix using versions `20` and `22`. Observe how many jobs GitHub creates.

## 10. Environment variables

Variables can be set at workflow, job, or step scope.

```yaml
env:
  APP_NAME: restaurant-pos

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Display app name
        env:
          ENVIRONMENT: testing
        run: |
          echo "App: $APP_NAME"
          echo "Environment: $ENVIRONMENT"
```

Use environment variables for configuration that is safe to expose to the process. Do not use them as a reason to print credentials or other sensitive values.

## 11. GitHub Actions contexts and expressions

Contexts provide information about the workflow run.

| Context | Typical information |
|---|---|
| `github` | Repository, event, actor, ref, and commit information. |
| `env` | Workflow-defined environment variables. |
| `vars` | Repository, organization, or environment variables. |
| `secrets` | Secret values. |
| `runner` | Runner information. |
| `job` | Current job information. |
| `steps` | Step outputs and results. |
| `needs` | Outputs and results from dependent jobs. |
| `matrix` | Current matrix combination. |
| `inputs` | Workflow or action inputs. |

Expressions use `${{ ... }}`:

```yaml
if: github.ref == 'refs/heads/main'
```

A safer way to use an event value in a shell command is to pass it through an environment variable:

```yaml
- name: Display event title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: echo "$PR_TITLE"
```

Do not interpolate untrusted Pull Request titles, branch names, issue bodies, or other user-controlled strings directly into shell commands. Handle them as data, not executable code.

Reference: [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)

## 12. Secrets and variables

Use **secrets** for credentials and **variables** for non-sensitive configuration.

| | Secrets | Variables |
|---|---|---|
| Intended for sensitive credentials | Yes | No |
| Example | `DEPLOY_TOKEN` | `APP_ENV` |
| Reference | `secrets.NAME` | `vars.NAME` |

Configure them under **Settings → Secrets and variables → Actions**.

A workflow can check whether a secret is configured without printing its value:

```yaml
- name: Check deployment credential
  env:
    DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
  run: |
    if [ -z "$DEPLOY_TOKEN" ]; then
      echo "Deployment credential is not configured"
      exit 1
    fi
    echo "Deployment credential is configured"
```

Secret masking is not a security boundary. Do not print secrets, pass them to untrusted code, or expose production credentials to ordinary CI jobs.

## 13. `GITHUB_TOKEN` and permissions

GitHub creates a short-lived `GITHUB_TOKEN` for a workflow run. Its permissions are limited by the workflow configuration and repository or organization settings.

For read-only CI:

```yaml
permissions:
  contents: read
```

Grant write permissions only when the workflow requires them. For example:

```yaml
permissions:
  contents: read
  pull-requests: write
```

This is appropriate only for a workflow that genuinely needs to read repository content and write Pull Request metadata.

Common permissions include:

| Permission | Typical use |
|---|---|
| `contents` | Repository contents and release operations. |
| `issues` | Issue operations. |
| `pull-requests` | Pull Request operations. |
| `checks` | Check runs. |
| `packages` | Package publishing. |
| `deployments` | Deployment records. |
| `id-token` | Requesting an OIDC identity token. |

**Exercise:** Create a workflow with `contents: read`. Explain why it does not need `contents: write`.

## 14. Workflow artifacts

Artifacts preserve files produced by a workflow run, such as build output, test reports, or diagnostic files.

```yaml
name: Artifact Practice

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  create-artifact:
    runs-on: ubuntu-latest
    steps:
      - name: Create sample output
        run: |
          mkdir -p output
          echo "Training artifact" > output/result.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: training-output
          path: output/
          retention-days: 7
```

After the workflow runs, open the run in **Actions** and download the artifact.

Artifacts are for workflow outputs. They are not a substitute for package registries or long-term application storage.

## 15. Dependency caching

Caching can reduce repeated dependency-download time. It does not replace installing dependencies or validating them.

Python example:

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
    cache-dependency-path: backend/requirements.txt
```

Node.js example:

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "22"
    cache: npm
    cache-dependency-path: frontend/package-lock.json
```

Use the paths and versions that match the actual project. A changed dependency lockfile can produce a different cache key.

| Cache | Artifact |
|---|---|
| Reuses dependency data to improve performance | Preserves output from a workflow run |
| May be evicted | Has a configured retention period |
| Not intended as a deliverable | Downloadable from the workflow run |

## 16. Reusable workflows

A reusable workflow is a complete workflow that another workflow calls.

Create `.github/workflows/reusable-check.yml`:

```yaml
name: Reusable Check

on:
  workflow_call:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Reusable workflow executed"
```

Call it from another workflow:

```yaml
name: Main CI

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  reusable:
    uses: ./.github/workflows/reusable-check.yml
```

Reusable workflows can define inputs, outputs, and secrets. They are useful when multiple repositories or workflows need the same job structure.

## 17. Composite Actions

A composite Action packages a sequence of steps into one reusable Action.

Create `.github/actions/project-info/action.yml`:

```yaml
name: Project Information
description: Display basic repository information

runs:
  using: composite
  steps:
    - name: Print repository
      shell: bash
      run: echo "Repository: $GITHUB_REPOSITORY"

    - name: Print commit
      shell: bash
      run: echo "Commit: $GITHUB_SHA"
```

Use it in a workflow:

```yaml
- name: Display project information
  uses: ./.github/actions/project-info
```

| Reusable workflow | Composite Action |
|---|---|
| Reuses one or more jobs | Reuses steps within a job |
| Uses `workflow_call` | Uses `action.yml` |
| Can define workflow inputs and outputs | Can define Action inputs and outputs |

## 18. Django REST Framework CI

The following is a **reference example** for a future application with `backend/requirements.txt`, Django, pytest, and Ruff. Do not add it to the training repository unless those files and tools exist.

```yaml
backend:
  name: Backend Checks
  runs-on: ubuntu-latest

  steps:
    - name: Check out repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: pip
        cache-dependency-path: backend/requirements.txt

    - name: Install dependencies
      working-directory: backend
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install ruff pytest pytest-django

    - name: Ruff
      working-directory: backend
      run: ruff check .

    - name: Django system check
      working-directory: backend
      run: python manage.py check

    - name: Run tests
      working-directory: backend
      run: pytest
```

A real project may need test settings, environment variables, database configuration, and a test database. Prefer installing tools from a pinned development dependency file rather than adding them ad hoc in every workflow.

## 19. React/Vite CI

This reference assumes `frontend/package.json` defines the scripts shown and that `package-lock.json` exists.

```yaml
frontend:
  name: Frontend Checks
  runs-on: ubuntu-latest

  defaults:
    run:
      working-directory: frontend

  steps:
    - name: Check out repository
      uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: "22"
        cache: npm
        cache-dependency-path: frontend/package-lock.json

    - name: Install dependencies
      run: npm ci

    - name: ESLint
      run: npm run lint

    - name: TypeScript
      run: npx tsc --noEmit

    - name: Tests
      run: npm test -- --run

    - name: Build
      run: npm run build
```

Check that the scripts exist in `package.json`. If your test runner uses different command-line options, update the workflow accordingly.

## 20. PostgreSQL integration testing

A Django integration test job can use a PostgreSQL service container:

```yaml
services:
  postgres:
    image: postgres:16
    env:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
    ports:
      - 5432:5432
    options: >-
      --health-cmd "pg_isready -U test_user -d test_db"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

On a GitHub-hosted runner, the job can connect to the service through `localhost:5432`.

These are disposable test credentials, not production credentials. Never use production database credentials in a CI service container.

## 21. Docker build and publishing

A typical image pipeline is:

```text
Pull Request checks
        |
        v
Merge to main
        |
        v
Build and validate image
        |
        v
Publish versioned image
        |
        v
Controlled deployment
```

GitHub Actions can publish images to GitHub Container Registry (GHCR). A publishing workflow needs a valid Dockerfile, appropriate package access, and narrowly scoped permissions.

For publishing, `packages: write` may be required. Do not grant it to ordinary test jobs.

Use immutable version tags or commit-SHA tags for traceability. Do not rely only on a mutable tag such as `latest` or `training` when deploying production.

## 22. Deployment environments

GitHub Environments can separate deployment settings, secrets, and protection rules for environments such as `staging` and `production`.

```yaml
deploy-staging:
  name: Deploy Staging
  runs-on: ubuntu-latest
  needs:
    - backend
    - frontend
  environment: staging
  steps:
    - name: Deployment placeholder
      run: echo "Add the reviewed staging deployment command here"
```

The example is a placeholder, not a deployment. Configure the Environment in GitHub and add a real deployment command only after deciding how the target system will authenticate and receive releases.

For a local-first restaurant POS product, GitHub Actions is the automation layer—not the production server. Keep production deployment credentials separate, and plan backups, health checks, monitoring, and rollback.

## 23. CI/CD security

Treat workflow files as executable code with access to repository resources.

### 23.1 Least privilege

Start with the minimum permissions:

```yaml
permissions:
  contents: read
```

Add write permissions only to the job that needs them.

### 23.2 Review third-party Actions

Actions can execute code in your workflow. Verify the source, maintainer, release, and permissions required. For production, consider pinning third-party Actions to verified full commit SHAs rather than relying only on mutable tags.

### 23.3 Use safe Pull Request triggers

Prefer `pull_request` for ordinary Pull Request tests.

Be especially careful with `pull_request_target`. It runs in a more privileged context. Never combine a privileged workflow with checking out and executing untrusted Pull Request code. Treat Pull Request titles, descriptions, branch names, and other user-controlled values as untrusted input.

### 23.4 Protect secrets

- Do not print secrets.
- Do not pass production secrets to untrusted code.
- Do not treat log masking as a security guarantee.
- Rotate credentials immediately if they are exposed.
- Use dedicated deployment environments and restricted credentials.

### 23.5 Isolate runners

Do not run untrusted code on a self-hosted runner with access to internal services or production systems. Use isolated, maintained runners and restrict who can trigger workflows that use them.

Reference: [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

## 24. Troubleshooting

| Problem | What to inspect |
|---|---|
| Workflow does not start | Trigger, branch/path filters, event activity types, default branch requirements |
| Workflow is invalid | YAML indentation, keys, expressions, and workflow syntax |
| Checkout fails | Repository access, permissions, and checkout logs |
| Dependencies fail | Manifest path, runtime version, package lockfile, and installation logs |
| Tests fail | Test output, settings, environment variables, and test database |
| Permission denied | `permissions`, repository settings, and Environment protection rules |
| Artifact is missing | Upload path, artifact step result, and retention |
| Deployment is blocked | Environment rules, required approvals, branch restrictions, and credentials |
| Workflow is cancelled | Concurrency settings or manual cancellation |

Debug systematically:

1. Open **Actions**.
2. Select the workflow run.
3. Select the failed job.
4. Open the failed step.
5. Identify whether the problem is workflow configuration, runner setup, dependencies, application code, permissions, or deployment.

Do not change YAML randomly before identifying the failing step.

## 25. Practical assignments

Complete the assignments in order. Use the training repository for repository-safe exercises; keep application-specific examples as reference material until the matching application exists.

### Level 1 — Fundamentals

- [ ] Create `hello-github-actions.yml`.
- [ ] Explain workflow, event, job, step, and runner.
- [ ] Test `push`, `pull_request`, and `workflow_dispatch`.
- [ ] Display repository, branch, event, commit, and runner information.
- [ ] Create a workflow with two independent jobs.
- [ ] Add a dependent job using `needs`.
- [ ] Create a Python matrix workflow.
- [ ] Create a Node.js matrix workflow.

### Level 2 — Intermediate automation

- [ ] Configure workflow-, job-, and step-level environment variables.
- [ ] Review the `github`, `env`, `vars`, `steps`, and `needs` contexts.
- [ ] Configure a read-only `GITHUB_TOKEN` permission set.
- [ ] Create and download an artifact.
- [ ] Configure Python dependency caching.
- [ ] Configure Node.js dependency caching.
- [ ] Create a reusable workflow.
- [ ] Create and call a composite Action.
- [ ] Explain the purpose of concurrency controls.

### Level 3 — Professional CI/CD

- [ ] Create a repository-safe CI workflow.
- [ ] Review a Django backend CI example.
- [ ] Review a React/Vite frontend CI example.
- [ ] Explain PostgreSQL service containers.
- [ ] Explain Docker image build and publishing stages.
- [ ] Explain GHCR and package permissions.
- [ ] Configure a non-production GitHub Environment if appropriate.
- [ ] Review workflow permissions and Pull Request security.
- [ ] Document when a self-hosted runner would—and would not—be appropriate.
- [ ] Write a troubleshooting note based on a failed workflow run.

## 26. Lessons learned

After completing this lesson, you should be able to explain:

- How GitHub Actions turns repository events into automated jobs.
- How jobs, steps, runners, dependencies, and matrices work.
- How to configure triggers, contexts, variables, and permissions.
- When to use artifacts, caches, reusable workflows, and composite Actions.
- How CI for Django, React/Vite, and PostgreSQL can be structured.
- Why deployment automation needs separate credentials, permissions, and protections.
- Why workflow security is part of application security.

**Key principle:** Start with small, read-only workflows that validate changes. Add publishing and deployment only when the application, credentials, and operational safeguards are ready.

## 27. References

- [Understanding GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
- [Choosing a runner](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job)
- [Contexts reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts)
- [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- [Authenticate with `GITHUB_TOKEN`](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token)
- [Store and share data with workflow artifacts](https://docs.github.com/en/actions/tutorials/store-and-share-data)
- [Dependency caching](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Create a composite Action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub Actions billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage)

## 28. Git workflow — commit, PR, tag, release

### Step 1 — Create your branch

```powershell
git switch main
git pull --ff-only origin main
git switch -c docs/lesson-34-github-actions
```

If the fast-forward pull fails because your local and remote branches have diverged, stop and inspect the branch history before choosing a merge or rebase strategy.

### Step 2 — Add the lesson files

For the main lesson:

```powershell
git add docs/github/module-04-actions/lesson-34-github-actions-fundamentals.md
```

Only add workflow files you have reviewed and intend to execute. Do not add application CI workflows that reference directories or manifests that do not exist.

### Step 3 — Validate the changes

```powershell
git status
git diff --check
git diff --cached
```

Review the Markdown and any YAML workflow files. Confirm that no secrets or machine-specific files are staged.

### Step 4 — Commit

```powershell
git commit -m "docs(github): add Lesson 34 GitHub Actions deep dive"
```

### Step 5 — Push

```powershell
git push -u origin docs/lesson-34-github-actions
```

### Step 6 — Create a Pull Request

#### PR title

```text
docs(github): add Lesson 34 GitHub Actions deep dive
```

#### PR description

```markdown
## Summary

Add the GitHub Actions and CI/CD fundamentals lesson.

## Topics

- CI/CD concepts and workflow architecture
- Events, runners, jobs, dependencies, and matrices
- Contexts, variables, secrets, and permissions
- Artifacts, caching, reusable workflows, and composite Actions
- Django, React/Vite, PostgreSQL, Docker, and deployment examples
- Workflow security and troubleshooting

## Validation

- [ ] Markdown reviewed
- [ ] YAML examples reviewed
- [ ] Training-repository workflows tested
- [ ] Permissions reviewed
- [ ] No secrets or production credentials added
```

### Step 7 — Merge and tag

After the Pull Request is merged:

```powershell
git switch main
git pull --ff-only origin main
git tag -a module-04-lesson-34 -m "Module 4 - Lesson 34: GitHub Actions Deep Dive"
git push origin module-04-lesson-34
```

### Step 8 — Create the GitHub Release

#### Release configuration

| Field | Value |
|---|---|
| Tag | `module-04-lesson-34` |
| Title | `Module 4 — Lesson 34: GitHub Actions` |
| Target | `main` |

#### Release notes

```markdown
# Module 4 — Lesson 34

Completed GitHub Actions: Complete CI/CD Deep Dive.

## Topics covered

- CI/CD fundamentals and workflow architecture
- Triggers, runners, jobs, dependencies, and matrices
- Environment variables, contexts, secrets, and permissions
- Artifacts, caching, reusable workflows, and composite Actions
- Django and React/Vite CI architecture
- PostgreSQL integration testing
- Docker image publishing and deployment environments
- Workflow security and troubleshooting

## Training checkpoint

`module-04-lesson-34`
```

## Next lesson — Lesson 35

### Advanced GitHub Actions: Professional CI/CD Pipelines

Lesson 35 will build on these fundamentals with:

1. Advanced workflow expressions and dynamic matrices.
2. Job outputs and artifact transfer.
3. Reusable workflows and composite Actions with inputs and outputs.
4. Workflow orchestration, concurrency, and failure handling.
5. Environment protection rules and deployment approvals.
6. OIDC and secure cloud deployments.
7. Docker BuildKit, layer caching, and GHCR publishing.
8. Versioning, release automation, and changelog generation.
9. A production-oriented DRF + React CI/CD design.

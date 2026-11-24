# Module 4 — GitHub Actions & CI/CD

## Lesson 39 — Advanced Workflow Orchestration & Enterprise Pipeline Design

**Level:** Advanced
**Category:** Practical Engineering / Enterprise CI/CD
**Repository:** `github-deep-dive-training`
**Previous lesson:** Lesson 38 — Reusable Workflows, Composite Actions & Internal Automation Platforms
**Next lesson:** Lesson 40 — GitHub Actions Security, Supply Chain Security & Workflow Hardening

---

## 1. Lesson Overview

In Lesson 37, we studied GitHub Actions runners and the infrastructure responsible for executing workflows.

In Lesson 38, we explored reusable workflows, composite Actions, JavaScript Actions, Docker Actions, and internal automation platforms.

Now we are moving from reusable automation components to **advanced workflow orchestration**.

In real software companies, a CI/CD pipeline is rarely a simple sequence of commands.

A production application might contain:

- A Django REST Framework backend.
- A React frontend.
- A PostgreSQL database.
- Several independent services.
- Automated test suites.
- Build and packaging processes.
- Staging and production environments.
- Database migrations.
- Deployment approval requirements.
- Monitoring and recovery mechanisms.

These components have different dependencies and execution requirements.

For example:

- Backend tests and frontend tests can execute simultaneously.
- Integration tests must wait for both test suites.
- The application must be built only after validation succeeds.
- The same build artifact should be deployed to staging and production.
- Production deployment should require an approval.
- A deployment should not start while another deployment for the same environment is running.
- A failed deployment should trigger diagnostics and an appropriate recovery procedure.

A well-designed workflow must coordinate all these activities.

## 1.1 What we will build

Throughout this lesson, we will design an enterprise-style pipeline for a fictional application called **Nexa Platform**.

Its architecture:

```text
Nexa Platform
│
├── backend/
│   ├── Django REST Framework
│   ├── PostgreSQL integration
│   └── pytest
│
├── frontend/
│   ├── React
│   ├── TypeScript
│   └── Vitest
│
├── infrastructure/
│   ├── Docker
│   ├── Nginx
│   └── deployment configuration
│
└── .github/
    └── workflows/
```

The objective is to create a pipeline that can:

1. Detect which components changed.
2. Execute relevant tests.
3. Run independent jobs in parallel.
4. Coordinate dependent jobs.
5. Build application artifacts.
6. Transfer artifacts between jobs.
7. Validate the resulting release.
8. Deploy to staging.
9. Run integration tests.
10. Protect production deployment.
11. Coordinate production releases.
12. Report failures and support recovery.

## 1.2 Why workflow orchestration matters

Consider two possible architectures.

### Architecture A — Basic sequential pipeline

```text
Backend Tests
      |
      v
Frontend Tests
      |
      v
Build
      |
      v
Deploy
```

Every stage waits for the previous stage.

This is simple but can waste execution time.

### Architecture B — Orchestrated pipeline

```text
                  Start
                    |
                    v
             Detect Changes
                    |
             +------+------+
             |             |
             v             v
       Backend CI     Frontend CI
             |             |
             +------+------+
                    |
                    v
             Integration Tests
                    |
                    v
                Build
                    |
                    v
             Artifact Validation
                    |
                    v
               Staging
                    |
                    v
          Staging Verification
                    |
                    v
          Production Approval
                    |
                    v
              Production
```

Architecture B allows independent operations to run concurrently while preserving important dependencies.

**Important principle:** Parallelize independent work. Serialize operations that must happen in a particular order.

---

## 2. Learning Objectives

By completing this lesson, you should be able to:

- Design complex workflows using job dependencies.
- Understand execution graphs and dependency chains.
- Use conditional expressions to control jobs and steps.
- Apply GitHub Actions status-check functions.
- Implement static and dynamic matrix strategies.
- Pass information between jobs using outputs.
- Transfer files between jobs using artifacts.
- Cache dependencies without compromising correctness.
- Prevent conflicting workflow executions with concurrency groups.
- Implement fan-out and fan-in architectures.
- Configure environment protection and deployment approvals.
- Separate CI, artifact creation, and CD.
- Design multi-stage deployment pipelines.
- Orchestrate monorepositories.
- Coordinate microservice workflows.
- Understand database migration pipelines.
- Compare rolling and blue-green deployment strategies.
- Implement release-triggered workflows.
- Design failure-handling and recovery procedures.
- Combine the techniques into an enterprise DRF + React pipeline.

---

## 3. Lesson Placement in Module 4

| Lesson | Subject | Main responsibility |
|---|---|---|
| 37 | GitHub Actions Runners | Workflow execution infrastructure |
| 38 | Reusable Workflows and Actions | Reusable automation architecture |
| 39 | Advanced Workflow Orchestration | Coordinating complex CI/CD pipelines |
| 40 | Actions Security and Supply Chain | Securing workflows, dependencies, and artifacts |

Lesson 39 builds directly on the reusable components introduced in Lesson 38.

For example, the pipeline we create can call reusable workflows and composite Actions instead of duplicating every command.

---

## 4. Understanding Workflow Orchestration

## 4.1 What is workflow orchestration?

Workflow orchestration is the coordination of multiple jobs, steps, artifacts, dependencies, and execution conditions to complete a larger automated process.

In GitHub Actions, orchestration primarily involves:

- Jobs.
- Steps.
- Dependencies.
- Conditions.
- Outputs.
- Artifacts.
- Matrices.
- Environments.
- Concurrency.
- Workflow triggers.

A workflow can be represented as a directed acyclic graph, commonly called a DAG.

## 4.2 Understanding a DAG

A DAG represents tasks and their dependencies.

For example:

```text
           Backend Tests
                 |
                 |
                 v
              Build
                 ^
                 |
                 |
           Frontend Tests
                 |
                 |
                 v
             Deployment
```

More accurately, a dependency graph might look like this:

```text
Backend Tests ------+
                    |
                    v
                Integration
                    |
                    v
Frontend Tests -----+
                    |
                    v
                  Build
                    |
                    v
                 Deploy
```

A job can start when its required dependencies have completed successfully.

## 4.3 Why DAG architecture is important

A DAG provides:

- Parallel execution.
- Explicit dependencies.
- Predictable execution order.
- Easier failure analysis.
- Better resource utilization.
- Clear separation between responsibilities.

## 4.4 Sequential versus parallel execution

| Architecture | Description | Typical use |
|---|---|---|
| Sequential | Jobs execute one after another | Ordered deployment operations |
| Parallel | Independent jobs execute simultaneously | Backend and frontend tests |
| Fan-out | One job starts multiple independent jobs | Testing multiple services |
| Fan-in | Multiple jobs converge into one job | Final validation |
| Hybrid | Combines parallel and sequential execution | Enterprise CI/CD |

---

## 5. Job Dependencies with `needs`

## 5.1 Understanding `needs`

The `needs` keyword establishes a dependency between jobs.

Example:

```yaml
name: Application CI

on:
  push:
    branches:
      - main

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Run backend tests
        run: echo "Running backend tests"

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Run frontend tests
        run: echo "Running frontend tests"

  integration-tests:
    needs:
      - backend-tests
      - frontend-tests

    runs-on: ubuntu-latest

    steps:
      - name: Run integration tests
        run: echo "Running integration tests"

  build:
    needs: integration-tests

    runs-on: ubuntu-latest

    steps:
      - name: Build application
        run: echo "Building application"

  deploy:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - name: Deploy application
        run: echo "Deploying application"
```

## 5.2 Execution architecture

```text
             +----------------+
             | Backend Tests  |
             +----------------+
                      |
                      |
                      v
              +----------------+
              | Integration    |
              | Tests          |
              +----------------+
                      |
                      v
                 +---------+
                 |  Build  |
                 +---------+
                      |
                      v
                 +---------+
                 | Deploy  |
                 +---------+
                      ^
                      |
             +----------------+
             | Frontend Tests |
             +----------------+
```

The backend and frontend test jobs execute independently.

Integration tests wait for both.

The build waits for integration tests.

Deployment waits for the build.

## 5.3 Multiple dependencies

A job can depend on several jobs:

```yaml
security-scan:
  needs:
    - backend-tests
    - frontend-tests
    - dependency-audit

  runs-on: ubuntu-latest

  steps:
    - name: Security validation
      run: echo "Running security validation"
```

## 5.4 Important behavior

By default, a job that uses `needs` is skipped if a required dependency fails or is skipped.

Example:

```text
backend-tests:  success
frontend-tests: failure
integration:    skipped
build:          skipped
deploy:         skipped
```

This behavior protects downstream stages from executing when required validation has failed.

## 5.5 Practical engineering rule

Do not add dependencies unnecessarily.

For example, backend and frontend tests do not need to depend on each other if they are independent.

Incorrect:

```yaml
frontend-tests:
  needs: backend-tests
```

Better:

```yaml
backend-tests:
  runs-on: ubuntu-latest

frontend-tests:
  runs-on: ubuntu-latest
```

This allows both jobs to run in parallel.

---

## 6. Conditional Execution with `if`

## 6.1 What is conditional execution?

Conditional execution determines whether a job or step should run.

GitHub Actions uses the `if` keyword.

Example:

```yaml
deploy:
  if: github.ref == 'refs/heads/main'

  runs-on: ubuntu-latest

  steps:
    - run: echo "Deploying production"
```

This condition restricts the job to the main branch.

## 6.2 Event-based conditions

```yaml
deploy:
  if: github.event_name == 'push'

  runs-on: ubuntu-latest

  steps:
    - run: echo "Push event detected"
```

Manual execution:

```yaml
deploy:
  if: github.event_name == 'workflow_dispatch'

  runs-on: ubuntu-latest

  steps:
    - run: echo "Manual deployment requested"
```

## 6.3 Combining conditions

```yaml
deploy:
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'

  runs-on: ubuntu-latest

  steps:
    - run: echo "Production deployment"
```

Logical operators:

| Operator | Meaning |
|---|---|
| `&&` | AND |
| `\|\|` | OR |
| `!` | NOT |
| `==` | Equal |
| `!=` | Not equal |

## 6.4 Job-level and step-level conditions

Job-level:

```yaml
deploy:
  if: github.ref == 'refs/heads/main'

  runs-on: ubuntu-latest

  steps:
    - run: echo "Deploying"
```

Step-level:

```yaml
steps:
  - name: Run tests
    run: pytest

  - name: Generate release report
    if: github.ref == 'refs/heads/main'
    run: echo "Generating release report"
```

| Condition location | Responsibility |
|---|---|
| Job-level | Controls the entire job |
| Step-level | Controls one step |

## 6.5 Conditional execution based on changed components

Imagine a monorepository:

```text
repository/
├── backend/
├── frontend/
├── payment-service/
└── documentation/
```

You might want to execute backend tests only when backend files change.

A later exercise will implement changed-component detection and use its results to control execution.

---

## 7. Status-Check Functions

GitHub Actions provides functions that allow jobs and steps to react to workflow execution status.

| Function | Purpose |
|---|---|
| `success()` | Previous relevant operations succeeded |
| `failure()` | A previous relevant operation failed |
| `always()` | Run regardless of the normal success/failure status |
| `cancelled()` | The workflow or job was cancelled |

## 7.1 `success()`

```yaml
deploy:
  needs: tests

  if: success()

  runs-on: ubuntu-latest

  steps:
    - run: echo "Tests passed. Deploying."
```

## 7.2 `failure()`

```yaml
failure-report:
  needs: tests

  if: failure()

  runs-on: ubuntu-latest

  steps:
    - name: Collect failure information
      run: echo "Collecting diagnostics"
```

## 7.3 `always()`

```yaml
cleanup:
  needs:
    - backend-tests
    - frontend-tests

  if: always()

  runs-on: ubuntu-latest

  steps:
    - name: Cleanup
      run: echo "Running cleanup"
```

Use this carefully.

A cleanup operation should be safe when dependencies fail, and it should not assume that a cancelled runner or unavailable external service can still perform cleanup.

## 7.4 `cancelled()`

```yaml
cancellation-report:
  if: cancelled()

  runs-on: ubuntu-latest

  steps:
    - run: echo "Workflow was cancelled"
```

## 7.5 Important distinction

When a job uses `needs`, its default success condition can prevent it from running after a dependency failure.

A status-check function such as `always()` or `failure()` changes that behavior.

Do not assume that writing `if: failure()` on a downstream job automatically gives it access to files or state from the failed job. Each job has its own runner environment.

---

## 8. Matrix Strategies

## 8.1 What is a matrix strategy?

A matrix strategy allows one job definition to execute using multiple configuration combinations.

Instead of duplicating jobs for each Python version, define a matrix.

```yaml
name: Python Compatibility

on:
  push:

jobs:
  tests:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version:
          - "3.11"
          - "3.12"
          - "3.13"

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

GitHub creates three executions.

```text
                 Python Tests
                       |
          +------------+------------+
          |            |            |
          v            v            v
        Python       Python       Python
         3.11         3.12         3.13
```

## 8.2 Multiple matrix dimensions

```yaml
strategy:
  matrix:
    python-version:
      - "3.11"
      - "3.12"

    operating-system:
      - ubuntu-latest
      - windows-latest
```

This creates four combinations.

| Python | Operating system |
|---|---|
| 3.11 | Ubuntu |
| 3.11 | Windows |
| 3.12 | Ubuntu |
| 3.12 | Windows |

## 8.3 Controlling matrix execution

```yaml
strategy:
  fail-fast: false

  max-parallel: 2

  matrix:
    python-version:
      - "3.11"
      - "3.12"
      - "3.13"
```

`fail-fast: false` allows other matrix jobs to continue when one fails.

`max-parallel: 2` limits simultaneous executions.

## 8.4 Excluding combinations

```yaml
strategy:
  matrix:
    os:
      - ubuntu-latest
      - windows-latest

    python:
      - "3.11"
      - "3.12"

    exclude:
      - os: windows-latest
        python: "3.11"
```

## 8.5 Including combinations

```yaml
strategy:
  matrix:
    python:
      - "3.11"
      - "3.12"

    include:
      - python: "3.12"
        experimental: true
```

## 8.6 When to use matrices

Matrices are useful for:

- Python compatibility testing.
- Node.js compatibility testing.
- Operating-system testing.
- Browser testing.
- Multiple service builds.
- Multiple deployment regions.
- Configuration-specific integration tests.

Do not create unnecessarily large matrices. Each combination consumes execution time and runner capacity.

---

## 9. Job Outputs and Cross-Job Communication

## 9.1 Why do we need job outputs?

Each job runs in an independent execution environment.

A variable created in one job is not automatically available in another.

For example:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - run: |
          VERSION="1.0.0"
          echo "$VERSION"

  deploy:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - run: echo "Deploying version"
```

The deployment job cannot automatically access the shell variable from the build job.

## 9.2 Creating a step output

```yaml
jobs:
  build:
    runs-on: ubuntu-latest

    outputs:
      version: ${{ steps.version.outputs.version }}

    steps:
      - name: Generate version
        id: version
        run: |
          echo "version=1.0.0" >> "$GITHUB_OUTPUT"
```

## 9.3 Consuming a job output

```yaml
  deploy:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - name: Deploy version
        run: |
          echo "Deploying ${{ needs.build.outputs.version }}"
```

Data flow:

```text
Build Job
    |
    v
Step Output
    |
    v
Job Output
    |
    v
Deploy Job
    |
    v
needs.build.outputs.version
```

## 9.4 Multiple outputs

```yaml
jobs:
  metadata:
    runs-on: ubuntu-latest

    outputs:
      version: ${{ steps.info.outputs.version }}
      environment: ${{ steps.info.outputs.environment }}
      component: ${{ steps.info.outputs.component }}

    steps:
      - id: info
        run: |
          echo "version=2.1.0" >> "$GITHUB_OUTPUT"
          echo "environment=staging" >> "$GITHUB_OUTPUT"
          echo "component=backend" >> "$GITHUB_OUTPUT"
```

## 9.5 Outputs versus artifacts

| Requirement | Recommended mechanism |
|---|---|
| Transfer a version string | Job output |
| Transfer a deployment environment name | Job output |
| Transfer a build directory | Artifact |
| Transfer a test report | Artifact |
| Transfer a container image | Container registry |
| Transfer a secret | Secret or short-lived identity mechanism |

Job outputs are intended for small values, not large files or credentials.

---

## 10. Artifact Management

## 10.1 What is a workflow artifact?

An artifact is a file or collection of files produced during a workflow execution and stored for later use.

Examples:

- Frontend production builds.
- Test reports.
- Coverage reports.
- Application packages.
- Release manifests.
- Diagnostic logs.

## 10.2 Uploading an artifact

```yaml
name: Artifact Example

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build frontend
        working-directory: frontend
        run: |
          npm ci
          npm run build

      - name: Upload frontend artifact
        uses: actions/upload-artifact@v4
        with:
          name: frontend-build
          path: frontend/dist/
          retention-days: 7
```

## 10.3 Downloading an artifact

```yaml
  deploy:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - name: Download frontend artifact
        uses: actions/download-artifact@v4
        with:
          name: frontend-build
          path: ./dist

      - name: Inspect downloaded files
        run: ls -la ./dist
```

## 10.4 Artifact lifecycle

```text
             Build Job
                 |
                 v
          Create Build Files
                 |
                 v
          Upload Artifact
                 |
                 v
          GitHub Artifact Store
                 |
                 v
          Download Artifact
                 |
                 v
          Deployment Job
```

## 10.5 Artifact retention

```yaml
- uses: actions/upload-artifact@v4
  with:
    name: test-reports
    path: reports/
    retention-days: 14
```

Retention should reflect the purpose of the artifact.

For example:

| Artifact | Example retention |
|---|---|
| Temporary test report | 7 days |
| Debugging report | 14 days |
| Release evidence | Longer, based on policy |
| Production release package | Prefer a controlled package or container registry |

GitHub artifact retention is not a substitute for a permanent release registry.

## 10.6 Build once, deploy many

A critical production principle is to build an artifact once and promote that exact artifact through environments.

```text
                Source Code
                     |
                     v
                  Build
                     |
                     v
              Immutable Artifact
                     |
             +-------+-------+
             |               |
             v               v
          Staging         Production
             |               |
             v               v
          Testing         Approval
```

Avoid rebuilding separately for staging and production.

Different builds can contain different dependencies, timestamps, generated files, or configuration.

The deployment configuration should be environment-specific, but the application artifact should remain the same.

---

## 11. Dependency Caching

## 11.1 What is caching?

Caching stores reusable dependencies or generated data between workflow runs.

Without caching:

```text
Workflow Run 1:
Download dependencies
Install dependencies
Run tests

Workflow Run 2:
Download dependencies
Install dependencies
Run tests
```

With caching:

```text
Workflow Run 1:
Download dependencies
Install dependencies
Save cache

Workflow Run 2:
Restore cache
Install missing dependencies
Run tests
```

## 11.2 Python dependency caching

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
    cache-dependency-path: backend/requirements.txt
```

## 11.3 Node.js dependency caching

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "22"
    cache: npm
    cache-dependency-path: frontend/package-lock.json
```

## 11.4 Understanding cache keys

A cache key identifies a particular cached dependency state.

Conceptually:

```text
Operating System
       +
Dependency Manager
       +
Lock File Hash
       |
       v
    Cache Key
```

The lock file is important because it describes the dependency versions used by the project.

## 11.5 Cache versus artifact

| Cache | Artifact |
|---|---|
| Optimizes repeated execution | Transfers workflow outputs |
| Reusable between runs | Associated with workflow runs |
| Dependencies and reusable data | Build files and reports |
| May be evicted | Has a configured retention period |
| Not a deployment source of truth | Can transfer build output between jobs |

Never use a dependency cache as the authoritative source of a production release.

---

## 12. Concurrency Control

## 12.1 The problem

Imagine that three deployments are triggered close together:

```text
Commit A → Deployment A
Commit B → Deployment B
Commit C → Deployment C
```

If all three deployments execute simultaneously, they might interfere with one another.

Examples:

- Two deployments modify the same environment.
- One deployment overwrites another deployment's files.
- Database migration operations overlap.
- A staging environment becomes inconsistent.

## 12.2 Introducing concurrency groups

GitHub Actions supports concurrency groups.

```yaml
name: Production Deployment

on:
  push:
    branches:
      - main

concurrency:
  group: production-deployment
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Deploying production"
```

This controls concurrent workflow execution within the group.

## 12.3 Cancelling outdated executions

For CI workflows, you might want newer commits to replace outdated executions.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

For deployments, cancellation should be considered carefully.

Cancelling a deployment halfway through an operation might leave the environment in an uncertain state.

## 12.4 Recommended usage

| Workflow | Typical policy |
|---|---|
| Pull request CI | Cancel outdated runs |
| Main branch CI | Often cancel outdated runs |
| Staging deployment | Serialize deployments |
| Production deployment | Serialize deployments carefully |
| Database migration | Never allow conflicting migration executions |

Concurrency groups are coordination controls, not a replacement for deployment locks, transactional database operations, or infrastructure-level safeguards.

---

## 13. Fan-Out and Fan-In Architecture

## 13.1 What is fan-out?

Fan-out means one stage distributes work to several independent jobs.

Example:

```text
             Detect Components
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Backend   Frontend   Payments
         Tests     Tests      Tests
```

## 13.2 What is fan-in?

Fan-in means multiple jobs converge into a final job.

```text
       Backend Tests
              |
              |
       Frontend Tests
              |
              +------> Final Validation
              |
       Payment Tests
```

## 13.3 Combined fan-out and fan-in

```text
                 Start
                   |
                   v
             Detect Changes
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Backend  Frontend  Payments
         CI       CI        CI
          |        |        |
          +--------+--------+
                   |
                   v
             Final Validation
                   |
                   v
                 Build
```

## 13.4 Why use this architecture?

It provides:

- Parallel execution.
- Component-level isolation.
- Better scalability.
- Clearer failure reporting.
- Easier extension when adding services.

It is especially useful for monorepositories and microservice platforms.

---

## 14. Environment Protection and Deployment Approvals

## 14.1 What is a GitHub Environment?

A GitHub Environment represents a deployment target such as:

- Development.
- Staging.
- Production.

Environments can provide:

- Deployment protection rules.
- Required reviewers.
- Environment-specific secrets.
- Environment-specific variables.
- Deployment history.

## 14.2 Defining an environment in a workflow

```yaml
deploy-staging:
  runs-on: ubuntu-latest

  environment:
    name: staging

  steps:
    - name: Deploy to staging
      run: echo "Deploying staging"
```

## 14.3 Production approval

```yaml
deploy-production:
  needs: staging-tests

  runs-on: ubuntu-latest

  environment:
    name: production

  steps:
    - name: Deploy production
      run: echo "Deploying production"
```

The approval requirement is configured in the repository's environment settings.

The workflow declaration alone does not create an approval policy.

## 14.4 Environment architecture

```text
              Build Artifact
                    |
                    v
                 Staging
                    |
                    v
              Staging Tests
                    |
                    v
             Production Gate
                    |
              Human Approval
                    |
                    v
               Production
```

## 14.5 Recommended environment policy

| Environment | Typical protection |
|---|---|
| Development | Minimal restrictions |
| Staging | Controlled deployment |
| Production | Required reviewers and restricted deployment branches |

Never assume that a production environment is protected merely because the YAML contains `environment: production`.

Configure the protection rules in GitHub.

---

## 15. Multi-Stage CI/CD Architecture

## 15.1 Understanding CI and CD

Continuous Integration focuses on validating changes.

Typical CI activities:

- Linting.
- Unit tests.
- Integration tests.
- Security analysis.
- Build validation.

Continuous Delivery or Deployment focuses on preparing and releasing validated application versions.

Typical CD activities:

- Artifact promotion.
- Deployment approvals.
- Environment configuration.
- Deployment.
- Post-deployment verification.

## 15.2 Separate CI from CD

A useful architecture is:

```text
                 Source Changes
                       |
                       v
                 CI Workflow
                       |
          +------------+------------+
          |            |            |
          v            v            v
        Linting       Tests      Security
          |            |            |
          +------------+------------+
                       |
                       v
                  Build Artifact
                       |
                       v
                 Artifact Registry
                       |
                       v
                 CD Workflow
                       |
                       v
                    Staging
                       |
                       v
                   Approval
                       |
                       v
                  Production
```

## 15.3 Why separate them?

Separating CI and CD allows:

- Independent workflow permissions.
- Clear deployment responsibilities.
- Different trigger mechanisms.
- Controlled release promotion.
- Better auditability.
- Reuse of the same artifact.

## 15.4 Example CI workflow

File:

`.github/workflows/application-ci.yml`

```yaml
name: Application CI

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
  backend:
    uses: ./.github/workflows/backend-ci.yml

  frontend:
    uses: ./.github/workflows/frontend-ci.yml

  validation:
    needs:
      - backend
      - frontend

    runs-on: ubuntu-latest

    steps:
      - name: Final validation
        run: echo "All required checks passed"
```

This example assumes that the reusable workflows are defined with `workflow_call`.

It connects Lesson 39 orchestration to Lesson 38 reusable workflow architecture.

## 15.5 Example CD workflow

File:

`.github/workflows/deployment.yml`

```yaml
name: Application Deployment

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy-staging:
    runs-on: ubuntu-latest

    environment:
      name: staging

    steps:
      - name: Deploy staging
        run: echo "Deploying validated release to staging"

  deploy-production:
    needs: deploy-staging

    runs-on: ubuntu-latest

    environment:
      name: production

    steps:
      - name: Deploy production
        run: echo "Deploying validated release to production"
```

This is an architectural demonstration, not a complete deployment implementation.

A real CD workflow must identify and download the exact release artifact, verify its identity, and use an approved deployment mechanism.

---

## 16. Monorepository Orchestration

## 16.1 What is a monorepository?

A monorepository stores multiple components in one repository.

Example:

```text
nexa-platform/
│
├── backend/
│
├── frontend/
│
├── payment-service/
│
├── notification-service/
│
├── infrastructure/
│
└── .github/
    └── workflows/
```

The problem is that changing documentation should not necessarily trigger every application test.

## 16.2 Path filters

GitHub Actions supports path filters.

```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - "backend/**"
      - ".github/workflows/backend-ci.yml"

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - run: echo "Running backend CI"
```

Frontend:

```yaml
name: Frontend CI

on:
  pull_request:
    paths:
      - "frontend/**"
      - ".github/workflows/frontend-ci.yml"

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - run: echo "Running frontend CI"
```

## 16.3 Path filters versus dynamic detection

| Path filters | Dynamic detection |
|---|---|
| Defined in workflow triggers | Defined in workflow jobs |
| Simple configuration | More flexible logic |
| Separate workflow execution | Can produce a dynamic matrix |
| Good for independent workflows | Good for complex orchestration |

## 16.4 Shared code considerations

Suppose the backend imports code from:

```text
shared/python/
```

Changing shared code may affect the backend and several services.

Your detection strategy must account for shared dependencies.

Do not detect changes using only the service's own directory if that service depends on shared code.

---

## 17. Microservices Orchestration

## 17.1 Understanding the architecture

A microservice application might contain:

```text
Nexa Platform
│
├── API Gateway
│
├── Identity Service
│
├── Payment Service
│
├── Notification Service
│
├── Reporting Service
│
└── Frontend
```

Each service can have its own CI workflow.

## 17.2 Independent service pipelines

```text
Identity Repository
        |
        v
   Identity CI

Payment Repository
        |
        v
   Payment CI

Notification Repository
        |
        v
 Notification CI
```

This makes each service independently testable and releasable.

## 17.3 Cross-repository orchestration

GitHub Actions can coordinate workflows across repositories using supported event mechanisms such as:

- `repository_dispatch`.
- `workflow_dispatch`.
- `workflow_run`.

For example, a central integration repository might trigger a downstream workflow.

## 17.4 Important permission considerations

Cross-repository workflows require deliberate permission design.

A `GITHUB_TOKEN` is generally scoped to the repository associated with the workflow.

Do not assume that it can automatically access or trigger workflows in unrelated private repositories.

Use an approved GitHub App installation token or another explicitly authorized mechanism when cross-repository permissions are required.

## 17.5 Microservice release architecture

```text
          Identity Service CI
                  |
                  v
          Identity Artifact

          Payment Service CI
                  |
                  v
          Payment Artifact

        Notification Service CI
                  |
                  v
        Notification Artifact
                  |
                  v
          Integration Pipeline
                  |
                  v
             Platform Release
```

The platform integration pipeline should verify compatible service versions rather than assuming that the latest version of every service is automatically compatible.

---

## 18. Django Database Migration Pipelines

## 18.1 Why database migrations require special treatment

A Django application may contain database schema changes.

For example:

```text
backend/
└── apps/
    └── customers/
        └── migrations/
            ├── 0001_initial.py
            ├── 0002_add_phone.py
            └── 0003_add_status.py
```

These migrations modify database structure.

A deployment pipeline must consider:

- Application compatibility.
- Database schema compatibility.
- Migration ordering.
- Backup and recovery.
- Concurrent deployment prevention.
- Long-running operations.

## 18.2 Migration pipeline architecture

```text
             Backend Tests
                   |
                   v
            Migration Validation
                   |
                   v
             Build Artifact
                   |
                   v
              Staging Deploy
                   |
                   v
            Staging Migration
                   |
                   v
           Integration Tests
                   |
                   v
          Production Approval
                   |
                   v
          Production Migration
                   |
                   v
          Application Deployment
                   |
                   v
          Deployment Verification
```

The exact ordering depends on the migration design.

A migration that is not backward-compatible may require a coordinated deployment strategy.

## 18.3 Migration validation

A Django project can check migration consistency:

```bash
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
```

The first command checks whether model changes require new migrations.

The second checks whether unapplied migrations exist.

Run these checks against an appropriately configured test environment.

## 18.4 Expand-and-contract migrations

A safer production migration strategy is often called expand-and-contract.

Imagine that you want to rename a database field.

Instead of immediately removing the old field, use several releases.

### Phase 1 — Expand

Add the new field while preserving the old field.

```text
Database:
    old_name
    new_name
```

### Phase 2 — Application compatibility

Deploy application code that can read and write using the compatible schema.

### Phase 3 — Data migration

Move or synchronize existing data.

### Phase 4 — Contract

After all application versions no longer depend on the old field, remove it in a later migration.

Architecture:

```text
Release 1:
Add new schema
       |
       v
Release 2:
Support old + new schema
       |
       v
Release 3:
Move application usage
       |
       v
Release 4:
Remove old schema
```

This reduces the risk of deploying application code that expects a schema that does not yet exist.

## 18.5 Backups and recovery

Before a high-risk database change, define:

- Backup requirements.
- Recovery point objectives.
- Recovery time objectives.
- Migration verification.
- Data restoration procedures.
- Ownership of the recovery operation.

A database rollback is not always equivalent to reversing a Django migration.

Some schema changes and data transformations are irreversible.

For production systems, forward-compatible migration design is generally safer than assuming every migration can be reversed.

---

## 19. Deployment Strategies

## 19.1 Rolling deployment

A rolling deployment gradually replaces existing application instances with new instances.

```text
Before:
[Version A] [Version A] [Version A]

During:
[Version B] [Version A] [Version A]

During:
[Version B] [Version B] [Version A]

After:
[Version B] [Version B] [Version B]
```

Advantages:

- Gradual replacement.
- Reduced infrastructure requirements.
- Can maintain service availability.

Considerations:

- Old and new versions may run simultaneously.
- Database schemas must support both versions during the transition.
- Health checks must detect unhealthy instances.

## 19.2 Blue-green deployment

Blue-green deployment maintains two environments.

```text
             Load Balancer
                   |
                   v
             Active Traffic
                   |
            +------+------+
            |             |
            v             v
         Blue          Green
       Version A      Version B
```

The new version is deployed to the inactive environment.

After verification, traffic is switched to the new environment.

Advantages:

- Fast traffic switching.
- Easier application-level rollback.
- Strong separation between old and new deployments.

Considerations:

- Additional infrastructure cost.
- Database compatibility remains important.
- External state and background workers need coordination.

## 19.3 Comparison

| Strategy | Main characteristic | Main consideration |
|---|---|---|
| Rolling | Gradual replacement | Mixed application versions |
| Blue-green | Switch between two environments | Infrastructure and state |
| Recreate | Replace all instances | Possible downtime |
| Canary | Gradually expose a subset of traffic | Traffic control and monitoring |

## 19.4 Deployment verification

A deployment should not be considered successful merely because a deployment command exited with code zero.

A production pipeline should verify:

- Application health endpoint.
- Application readiness.
- Database connectivity.
- Critical service dependencies.
- Error rates.
- Relevant smoke tests.

---

## 20. Release Orchestration

## 20.1 Tag-triggered workflows

A release workflow can start when a version tag is pushed.

Example:

```yaml
name: Release Pipeline

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Display release version
        run: echo "${GITHUB_REF_NAME}"
```

## 20.2 Release flow

```text
       Pull Request Merged
                |
                v
           Main Branch
                |
                v
          Release Preparation
                |
                v
            Version Tag
                |
                v
          Release Workflow
                |
                v
           Build Artifact
                |
                v
           Release Package
                |
                v
            Deployment
```

## 20.3 Versioning

Common version format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
v2.4.1
```

- MAJOR: incompatible changes.
- MINOR: backward-compatible functionality.
- PATCH: backward-compatible fixes.

## 20.4 Release artifact identity

A production release should identify exactly what is being deployed.

Useful metadata includes:

- Git commit SHA.
- Version tag.
- Build identifier.
- Artifact digest.
- Build timestamp.
- Dependency or package metadata.

A tag is a release reference, but it does not by itself prove that an artifact is trustworthy or immutable.

Artifact provenance and attestations will be covered in Lesson 40.

---

## 21. Failure Recovery and Deployment Reliability

## 21.1 Understanding failure categories

A production pipeline can fail at different stages.

| Stage | Example failure |
|---|---|
| Validation | Unit tests fail |
| Build | Compilation fails |
| Artifact | Missing or corrupted package |
| Deployment | Deployment command fails |
| Migration | Database migration fails |
| Verification | Health check fails |
| Infrastructure | Deployment target unavailable |

Each failure category requires a different response.

## 21.2 Rollback versus roll-forward

**Rollback** means returning to a previously deployed version or configuration.

**Roll-forward** means fixing the problem and deploying a new version.

| Strategy | When it may be appropriate |
|---|---|
| Rollback | Previous version is compatible and safe |
| Roll-forward | Database or data changes make reversal unsafe |
| Traffic switch | Blue-green environment is available |
| Recovery procedure | Data or infrastructure restoration is required |

## 21.3 Example failure-reporting job

```yaml
name: Deployment Recovery Example

on:
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Simulate deployment
        run: |
          echo "Starting deployment"
          exit 1

  report:
    needs: deploy

    if: failure()

    runs-on: ubuntu-latest

    steps:
      - name: Report deployment failure
        run: echo "Deployment failed. Investigation required."
```

This is a demonstration of failure detection.

It is not an automated production rollback.

## 21.4 Recovery design principles

A reliable deployment system should:

1. Detect failures.
2. Preserve useful diagnostic information.
3. Identify the affected release.
4. Prevent conflicting deployments.
5. Determine whether rollback is safe.
6. Execute an approved recovery procedure.
7. Verify application health.
8. Record the result.

Do not implement an automatic rollback simply because a deployment job failed. The failure may have happened before deployment, during deployment, or after part of the application was updated.

The recovery strategy must understand the actual state of the environment.

---

## 22. Enterprise DRF + React Pipeline Design

Now we combine the concepts into one architecture.

## 22.1 Application structure

```text
nexa-platform/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── apps/
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   ├── nginx/
│   └── deployment/
│
└── .github/
    └── workflows/
```

## 22.2 Enterprise pipeline

```text
                         GitHub Event
                              |
                              v
                       Detect Changes
                              |
                   +----------+----------+
                   |                     |
                   v                     v
              Backend CI            Frontend CI
                   |                     |
                   v                     v
              Backend Tests          Frontend Tests
                   |                     |
                   +----------+----------+
                              |
                              v
                     Final Validation
                              |
                              v
                      Build Artifacts
                              |
                              v
                    Artifact Verification
                              |
                              v
                      Staging Deployment
                              |
                              v
                    Integration Tests
                              |
                              v
                     Release Approval
                              |
                              v
                    Production Deployment
                              |
                              v
                    Health Verification
                              |
                     +--------+--------+
                     |                 |
                     v                 v
                  Success           Failure
                     |                 |
                     v                 v
                Release Record    Recovery Process
```

## 22.3 Architecture principles

Our final pipeline should follow these principles:

### 1. Separation of concerns

Backend, frontend, infrastructure, testing, and deployment should have clearly defined responsibilities.

### 2. Parallel execution

Independent validation jobs should run concurrently.

### 3. Explicit dependencies

Downstream jobs should declare the jobs they require.

### 4. Immutable artifact promotion

Build once and promote the same artifact through environments.

### 5. Environment protection

Production deployment should use configured GitHub environment protection rules.

### 6. Deployment serialization

Prevent conflicting deployments to the same environment.

### 7. Migration safety

Database schema changes must be compatible with the application deployment strategy.

### 8. Recovery planning

Define recovery procedures before deploying critical changes.

### 9. Least privilege

Each workflow and job should receive only the permissions it needs. We will study this in depth in Lesson 40.

---

## 23. Practical Exercises

All exercises will be implemented in your existing repository:

`github-deep-dive-training`

You will create real GitHub Actions workflows, execute them, inspect their behavior, and document the results.

## Exercise 1 — Job Dependencies and Parallel Execution

**Objective:** Build a workflow that executes independent jobs in parallel and coordinates their results.

### Create

`.github/workflows/lesson-39-exercise-01-dependencies.yml`

```yaml
name: Lesson 39 - Exercise 01 - Dependencies

on:
  workflow_dispatch:

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Backend tests
        run: echo "Backend tests completed"

  frontend-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Frontend tests
        run: echo "Frontend tests completed"

  security-check:
    runs-on: ubuntu-latest

    steps:
      - name: Security validation
        run: echo "Security validation completed"

  integration-tests:
    needs:
      - backend-tests
      - frontend-tests
      - security-check

    runs-on: ubuntu-latest

    steps:
      - name: Integration tests
        run: echo "Integration tests completed"

  build:
    needs: integration-tests

    runs-on: ubuntu-latest

    steps:
      - name: Build
        run: echo "Application built successfully"
```

### Tasks

1. Run the workflow manually.
2. Open the Actions tab.
3. Inspect the execution graph.
4. Identify which jobs run in parallel.
5. Temporarily make one independent job fail.
6. Observe the behavior of dependent jobs.
7. Restore the workflow.

### Expected result

- Backend, frontend, and security jobs execute independently.
- Integration tests wait for all three.
- Build waits for integration tests.
- A failed dependency prevents normal downstream execution.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-01-job-dependencies.md`

Document the execution graph, observations, and results.

---

## Exercise 2 — Conditional Execution and Failure Handling

**Objective:** Use conditions and status-check functions.

### Create

`.github/workflows/lesson-39-exercise-02-conditions.yml`

```yaml
name: Lesson 39 - Exercise 02 - Conditions

on:
  workflow_dispatch:

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Run tests
        run: echo "Tests completed"

  success-report:
    needs: tests

    if: success()

    runs-on: ubuntu-latest

    steps:
      - name: Report success
        run: echo "Tests passed"

  failure-report:
    needs: tests

    if: failure()

    runs-on: ubuntu-latest

    steps:
      - name: Report failure
        run: echo "Tests failed"

  final-report:
    needs:
      - tests
      - success-report
      - failure-report

    if: always()

    runs-on: ubuntu-latest

    steps:
      - name: Final report
        run: echo "Workflow reporting completed"
```

### Tasks

1. Run the workflow with successful tests.
2. Record which jobs execute.
3. Temporarily make the test job fail.
4. Run the workflow again.
5. Compare the execution graphs.
6. Explain why `always()` is useful.
7. Restore the successful test command.

### Expected result

You should understand how status-check functions influence downstream execution.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-02-conditional-execution.md`

---

## Exercise 3 — Matrix Testing and Dynamic Matrices

**Objective:** Implement matrix-based testing.

### Create

`.github/workflows/lesson-39-exercise-03-matrix.yml`

```yaml
name: Lesson 39 - Exercise 03 - Matrix

on:
  workflow_dispatch:

jobs:
  python-tests:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false

      matrix:
        python-version:
          - "3.11"
          - "3.12"
          - "3.13"

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: python --version
```

### Tasks

1. Run the workflow.
2. Observe the three job executions.
3. Add another matrix dimension.
4. Calculate the total number of combinations.
5. Add an excluded combination.
6. Set `max-parallel`.
7. Compare `fail-fast: true` and `fail-fast: false`.

### Advanced task

Create a separate detection job that outputs a JSON array.

Use `fromJSON()` to generate a dynamic matrix in a downstream job.

Use a validated list of allowed component names.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-03-matrix-strategies.md`

---

## Exercise 4 — Job Outputs, Artifacts, and Dependency Caching

**Objective:** Understand communication between jobs and reusable build data.

### Create

`.github/workflows/lesson-39-exercise-04-artifacts.yml`

```yaml
name: Lesson 39 - Exercise 04 - Artifacts

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    outputs:
      version: ${{ steps.metadata.outputs.version }}

    steps:
      - uses: actions/checkout@v4

      - name: Generate metadata
        id: metadata
        run: |
          echo "version=1.0.0" >> "$GITHUB_OUTPUT"

      - name: Create build output
        run: |
          mkdir -p build
          echo "Nexa Platform Build" > build/application.txt
          echo "${{ steps.metadata.outputs.version }}" > build/version.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: application-build
          path: build/
          retention-days: 7

  inspect:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: application-build
          path: ./build

      - name: Display version
        run: |
          echo "Version: ${{ needs.build.outputs.version }}"

      - name: Inspect artifact
        run: |
          find ./build -type f
          cat ./build/version.txt
```

### Tasks

1. Run the workflow.
2. Inspect the build job output.
3. Inspect the uploaded artifact.
4. Inspect the downloaded artifact.
5. Modify the version.
6. Run again and compare the result.
7. Add dependency caching to a Python or Node.js workflow.
8. Observe cache restoration across workflow runs.

### Expected result

You should be able to distinguish:

- Step outputs.
- Job outputs.
- Artifacts.
- Dependency caches.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-04-outputs-artifacts-caching.md`

---

## Exercise 5 — Concurrency and Environment Protection

**Objective:** Control deployments and understand environment protection.

### Create

`.github/workflows/lesson-39-exercise-05-deployment.yml`

```yaml
name: Lesson 39 - Exercise 05 - Deployment Control

on:
  workflow_dispatch:

concurrency:
  group: lesson-39-staging
  cancel-in-progress: false

jobs:
  deploy-staging:
    runs-on: ubuntu-latest

    environment:
      name: staging

    steps:
      - name: Start deployment
        run: echo "Starting staging deployment"

      - name: Simulate deployment duration
        run: sleep 20

      - name: Finish deployment
        run: echo "Staging deployment completed"

  verify-staging:
    needs: deploy-staging

    runs-on: ubuntu-latest

    steps:
      - name: Verify staging
        run: echo "Staging verification completed"
```

### Tasks

1. Configure a GitHub Environment named `staging`.
2. Run the workflow.
3. Trigger another run while the first is executing.
4. Observe concurrency behavior.
5. Configure a protected `production` environment.
6. Add a production deployment job.
7. Configure required reviewers in GitHub environment settings.
8. Observe how the approval gate affects execution.

### Expected result

You should understand:

- Concurrency groups.
- Deployment serialization.
- Environment configuration.
- Approval gates.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-05-concurrency-environments.md`

---

## Exercise 6 — Enterprise Pipeline Architecture

**Objective:** Combine the techniques into one complete pipeline design.

### Create

`.github/workflows/lesson-39-enterprise-pipeline.yml`

```yaml
name: Lesson 39 - Enterprise Pipeline

on:
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: lesson-39-enterprise-${{ github.ref }}
  cancel-in-progress: false

jobs:
  backend-ci:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Backend validation
        run: echo "Backend validation completed"

  frontend-ci:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Frontend validation
        run: echo "Frontend validation completed"

  integration:
    needs:
      - backend-ci
      - frontend-ci

    runs-on: ubuntu-latest

    steps:
      - name: Integration validation
        run: echo "Integration validation completed"

  build:
    needs: integration

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Create release package
        run: |
          mkdir -p dist
          echo "Nexa Platform Release" > dist/release.txt

      - name: Upload release artifact
        uses: actions/upload-artifact@v4
        with:
          name: nexa-release
          path: dist/

  staging:
    needs: build

    runs-on: ubuntu-latest

    environment:
      name: staging

    steps:
      - uses: actions/download-artifact@v4
        with:
          name: nexa-release
          path: ./dist

      - name: Deploy staging
        run: echo "Deploying staging"

      - name: Verify staging
        run: test -f ./dist/release.txt

  production:
    needs: staging

    runs-on: ubuntu-latest

    environment:
      name: production

    steps:
      - uses: actions/download-artifact@v4
        with:
          name: nexa-release
          path: ./dist

      - name: Deploy production
        run: echo "Deploying production"

      - name: Verify production package
        run: test -f ./dist/release.txt
```

### Important implementation notes

This workflow demonstrates orchestration, not a real deployment.

For an actual deployment:

- Replace demonstration commands with your deployment mechanism.
- Configure environment protection in GitHub.
- Verify artifact identity before deployment.
- Use environment-specific configuration.
- Use narrowly scoped deployment credentials.
- Add application health checks.
- Define migration and recovery procedures.
- Keep the same release artifact between environments.

### Tasks

1. Run the complete workflow.
2. Inspect the dependency graph.
3. Confirm backend and frontend jobs execute independently.
4. Confirm integration waits for both.
5. Confirm build waits for integration.
6. Confirm staging downloads the artifact.
7. Configure production approval.
8. Confirm production uses the same artifact.
9. Document the complete pipeline architecture.
10. Explain which jobs should be reusable workflows based on Lesson 38.

### Documentation

Create:

`docs/github/module-04-actions/exercises/exercise-06-enterprise-pipeline.md`

---

## 24. Repository Implementation

## 24.1 Required repository structure

Add the following structure to `github-deep-dive-training`:

```text
github-deep-dive-training/
│
├── .github/
│   └── workflows/
│       ├── lesson-39-exercise-01-dependencies.yml
│       ├── lesson-39-exercise-02-conditions.yml
│       ├── lesson-39-exercise-03-matrix.yml
│       ├── lesson-39-exercise-04-artifacts.yml
│       ├── lesson-39-exercise-05-deployment.yml
│       └── lesson-39-enterprise-pipeline.yml
│
├── docs/
│   └── github/
│       └── module-04-actions/
│           ├── lesson-39-workflow-orchestration.md
│           │
│           └── exercises/
│               ├── exercise-01-job-dependencies.md
│               ├── exercise-02-conditional-execution.md
│               ├── exercise-03-matrix-strategies.md
│               ├── exercise-04-outputs-artifacts-caching.md
│               ├── exercise-05-concurrency-environments.md
│               └── exercise-06-enterprise-pipeline.md
│
└── README.md
```

## 24.2 Documentation file responsibilities

| File | Responsibility |
|---|---|
| `lesson-39-workflow-orchestration.md` | Complete theory and lesson explanations |
| `exercise-01-job-dependencies.md` | Dependency graph and execution results |
| `exercise-02-conditional-execution.md` | Conditions and failure handling |
| `exercise-03-matrix-strategies.md` | Matrix and dynamic matrix experiments |
| `exercise-04-outputs-artifacts-caching.md` | Job communication and artifact management |
| `exercise-05-concurrency-environments.md` | Deployment controls and approvals |
| `exercise-06-enterprise-pipeline.md` | Complete enterprise architecture |

## 24.3 Main lesson documentation outline

The main file should contain:

```markdown
# Lesson 39 — Advanced Workflow Orchestration & Enterprise Pipeline Design

## 1. Lesson Overview
## 2. Learning Objectives
## 3. Lesson Placement in Module 4
## 4. Understanding Workflow Orchestration
## 5. Job Dependencies with needs
## 6. Conditional Execution with if
## 7. Status-Check Functions
## 8. Matrix Strategies
## 9. Job Outputs and Cross-Job Communication
## 10. Artifact Management
## 11. Dependency Caching
## 12. Concurrency Control
## 13. Fan-Out and Fan-In Architecture
## 14. Environment Protection and Deployment Approvals
## 15. Multi-Stage CI/CD Architecture
## 16. Monorepository Orchestration
## 17. Microservices Orchestration
## 18. Django Database Migration Pipelines
## 19. Deployment Strategies
## 20. Release Orchestration
## 21. Failure Recovery and Deployment Reliability
## 22. Enterprise DRF + React Pipeline Design
## 23. Practical Exercises
## 24. Repository Implementation
## 25. Lessons Learned
## 26. Official Documentation
## 27. Completion Checklist
## 28. Next Lesson Preview
```

---

## 25. Git Workflow

We will follow the same branch, commit, pull request, merge, tag, and release process used in previous lessons.

## 25.1 Create the feature branch

```bash
git switch main

git pull origin main

git switch -c feat/lesson-39-workflow-orchestration
```

## 25.2 Validate the repository

```bash
git status

git diff

git diff --check
```

Validate the YAML files and execute the workflows using GitHub Actions.

You should also inspect workflow execution results in the Actions tab.

## 25.3 Stage the lesson files

```bash
git add .github/workflows/lesson-39-exercise-01-dependencies.yml

git add .github/workflows/lesson-39-exercise-02-conditions.yml

git add .github/workflows/lesson-39-exercise-03-matrix.yml

git add .github/workflows/lesson-39-exercise-04-artifacts.yml

git add .github/workflows/lesson-39-exercise-05-deployment.yml

git add .github/workflows/lesson-39-enterprise-pipeline.yml

git add docs/github/module-04-actions/
```

## 25.4 Inspect staged changes

```bash
git status

git diff --cached
```

## 25.5 Create the Conventional Commit

```bash
git commit -m "feat(actions): add advanced workflow orchestration training"
```

## 25.6 Push the branch

```bash
git push -u origin feat/lesson-39-workflow-orchestration
```

## 25.7 Create a Pull Request

### PR title

```text
feat(actions): add Lesson 39 workflow orchestration
```

### PR description

```markdown
## Summary

Adds Lesson 39 — Advanced Workflow Orchestration & Enterprise Pipeline Design.

## Topics covered

- Job dependencies and execution graphs
- Conditional execution
- Status-check functions
- Matrix strategies
- Job outputs
- Artifact management
- Dependency caching
- Concurrency
- Fan-out and fan-in
- Environment protection
- Multi-stage CI/CD
- Monorepository orchestration
- Microservices orchestration
- Django migration pipelines
- Deployment strategies
- Release orchestration
- Failure recovery

## Practical exercises

- Exercise 01: Job dependencies
- Exercise 02: Conditional execution
- Exercise 03: Matrix strategies
- Exercise 04: Outputs, artifacts, and caching
- Exercise 05: Concurrency and environments
- Exercise 06: Enterprise pipeline

## Validation

- [ ] Workflow YAML files are valid.
- [ ] Dependency execution was tested.
- [ ] Conditional execution was tested.
- [ ] Matrix execution was tested.
- [ ] Artifacts were uploaded and downloaded.
- [ ] Concurrency behavior was tested.
- [ ] Environment configuration was reviewed.
- [ ] Documentation was reviewed.
```

## 25.8 Merge the Pull Request

After reviewing the changes and successful workflow runs, merge the pull request.

Then update your local main branch:

```bash
git switch main

git pull origin main
```

## 25.9 Create an annotated tag

```bash
git tag -a module-04-lesson-39 -m "Complete Module 4 Lesson 39 - Advanced Workflow Orchestration"

git push origin module-04-lesson-39
```

## 25.10 Create a GitHub Release

### Release tag

```text
module-04-lesson-39
```

### Release title

```text
Module 4 — Lesson 39: Advanced Workflow Orchestration
```

### Release description

```markdown
# Lesson 39 — Advanced Workflow Orchestration & Enterprise Pipeline Design

Completed the advanced GitHub Actions orchestration lesson.

## Covered

- Job dependencies
- Conditional execution
- Status-check functions
- Matrix strategies
- Job outputs
- Artifact management
- Dependency caching
- Concurrency control
- Fan-out and fan-in
- Environment protection
- Multi-stage CI/CD
- Monorepository orchestration
- Microservices orchestration
- Django migration pipelines
- Deployment strategies
- Release orchestration
- Failure recovery

## Practical work

Completed six repository-based exercises covering orchestration and enterprise pipeline architecture.

## Repository deliverables

- Six GitHub Actions workflow exercises
- Main lesson documentation
- Six practical exercise documents
- Enterprise pipeline example
```

---

## 26. Lessons Learned

After completing this lesson, you should understand the following engineering principles.

| Principle | Explanation |
|---|---|
| Explicit dependencies | Use `needs` to define execution relationships |
| Parallel execution | Run independent jobs concurrently |
| Conditional execution | Use `if` to control execution |
| Status-aware workflows | React appropriately to failures and cancellation |
| Dynamic execution | Use matrices to scale testing |
| Job communication | Use outputs for small values |
| File transfer | Use artifacts for build outputs |
| Performance | Cache reusable dependencies |
| Deployment coordination | Use concurrency groups |
| Deployment governance | Protect production environments |
| Artifact promotion | Build once and promote the same artifact |
| Migration safety | Design backward-compatible schema changes |
| Recovery planning | Distinguish rollback from roll-forward |

A mature pipeline is not simply a collection of YAML commands.

It is an execution architecture that must remain predictable, maintainable, observable, and safe when individual components fail.

---

## 27. Official Documentation

Use the official GitHub documentation as your primary reference.

| Subject | Documentation |
|---|---|
| Workflow syntax | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| Job dependencies | [Job dependencies](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs) |
| Expressions | [Expressions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions) |
| Matrix strategies | [Matrix strategies](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations) |
| Workflow outputs | [Workflow outputs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs) |
| Artifacts | [Artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/use-workflow-artifacts) |
| Dependency caching | [Dependency caching](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/dependency-caching) |
| Concurrency | [Concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) |
| Environments | [Environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) |
| Deployment workflows | [Deployment workflows](https://docs.github.com/en/actions/how-tos/deploy) |
| Workflow events | [Workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) |

---

## 28. Completion Checklist

Mark each item after implementing and verifying it.

## Theory

- [ ] I understand workflow orchestration.
- [ ] I understand DAG execution.
- [ ] I understand job dependencies.
- [ ] I understand conditional execution.
- [ ] I understand status-check functions.
- [ ] I understand matrix strategies.
- [ ] I understand dynamic matrices.
- [ ] I understand job outputs.
- [ ] I understand artifacts.
- [ ] I understand dependency caching.
- [ ] I understand concurrency groups.
- [ ] I understand fan-out and fan-in.
- [ ] I understand GitHub Environments.
- [ ] I understand multi-stage CI/CD.
- [ ] I understand monorepository orchestration.
- [ ] I understand microservice orchestration.
- [ ] I understand database migration pipelines.
- [ ] I understand deployment strategies.
- [ ] I understand release orchestration.
- [ ] I understand failure recovery.

## Practical implementation

- [ ] Exercise 01 completed.
- [ ] Exercise 02 completed.
- [ ] Exercise 03 completed.
- [ ] Exercise 04 completed.
- [ ] Exercise 05 completed.
- [ ] Exercise 06 completed.
- [ ] All workflows validated.
- [ ] All exercise documentation created.
- [ ] Enterprise pipeline reviewed.

## GitHub workflow

- [ ] Feature branch created.
- [ ] Conventional Commit created.
- [ ] Changes pushed.
- [ ] Pull Request opened.
- [ ] Pull Request reviewed.
- [ ] Pull Request merged.
- [ ] Annotated tag created.
- [ ] GitHub Release published.

---

## 29. Next Lesson Preview

### Lesson 40 — GitHub Actions Security, Supply Chain Security & Workflow Hardening

**Level:** Advanced / Enterprise Security

In Lesson 39, we designed complex workflows and enterprise deployment pipelines.

But a sophisticated pipeline can introduce security risks if its permissions, dependencies, credentials, and execution environments are not properly controlled.

In Lesson 40, we will study how to secure GitHub Actions from development through production deployment.

## Planned topics

1. GitHub Actions security architecture.
2. Workflow threat modeling.
3. Understanding `GITHUB_TOKEN`.
4. Fine-grained workflow permissions.
5. Least-privilege job permissions.
6. Pinning third-party Actions to commit SHAs.
7. Secure secret management.
8. OIDC authentication.
9. Pull request and fork security.
10. Understanding `pull_request_target`.
11. Expression injection and shell security.
12. Cache poisoning and artifact security.
13. Software Bill of Materials (SBOM).
14. Artifact attestations and provenance.
15. Sigstore and artifact signing.
16. CodeQL and SAST integration.
17. Secret scanning.
18. Dependabot security updates.
19. Container image security.
20. Self-hosted runner security.
21. Organization-level workflow governance.
22. Hardened enterprise DRF + React CI/CD architecture.

## Final objective

Build a security-hardened GitHub Actions architecture that protects:

- Source code.
- Repository secrets.
- Workflow permissions.
- Build artifacts.
- Dependencies.
- Deployment credentials.
- Production environments.
- Self-hosted infrastructure.

**Lesson 40 will complete the security foundation of Module 4.**

# Module 4 — GitHub Actions & CI/CD

## Lesson 35 — Advanced GitHub Actions: Professional CI/CD Pipelines

**Previous lesson:** Lesson 34 — GitHub Actions Fundamentals and CI/CD Architecture

**Level:** Advanced
**Estimated time:** 4–6 hours
**Repository:** `github-deep-dive-training`

---

## Lesson introduction

In Lesson 34, you learned the fundamentals of GitHub Actions: workflows, events, jobs, steps, runners, permissions, secrets, and basic CI/CD architecture.

In this lesson, you'll move beyond simple workflows and learn how professional development teams design maintainable, reusable, secure, and scalable automation pipelines.

A professional CI/CD pipeline should:

- Run independent tasks in parallel.
- Control execution order through job dependencies.
- Transfer information and files between jobs.
- Reuse workflows and actions across projects.
- Support multiple environments and application configurations.
- Prevent unnecessary concurrent deployments.
- Use temporary credentials where possible.
- Build and publish versioned Docker images.
- Automate releases and deployment processes.
- Enforce security requirements throughout the pipeline.

### Learning objectives

By the end of this lesson, you should be able to:

1. Design multi-job workflows with dependencies and conditional execution.
2. Use advanced expressions and workflow contexts.
3. Pass outputs between jobs.
4. Upload and download workflow artifacts.
5. Create static and dynamic matrices.
6. Build reusable workflows.
7. Create composite actions.
8. Control concurrency, timeouts, and failures.
9. Configure GitHub Environments and deployment approvals.
10. Understand OpenID Connect authentication.
11. Build and publish Docker images to GHCR.
12. Design separate backend and frontend CI pipelines.
13. Configure PostgreSQL integration testing.
14. Automate GitHub Releases.
15. Apply security principles to advanced workflows.

---

## 1. Advanced workflow architecture

A professional pipeline should not be one enormous YAML file containing every operation.

Instead, divide the pipeline into jobs with clear responsibilities.

### 1.1 Example production pipeline

```text
              Code change
                   |
                   v
           Pull Request / Push
                   |
          +--------+--------+
          |                 |
          v                 v
     Backend CI         Frontend CI
          |                 |
          v                 v
     Lint and tests    Lint and build
          |                 |
          +--------+--------+
                   |
                   v
             Quality checks
                   |
                   v
             Docker build
                   |
                   v
             Publish to GHCR
                   |
                   v
          Staging deployment
                   |
                   v
          Production approval
                   |
                   v
          Production deployment
                   |
                   v
           Health verification
```

Each stage has a specific responsibility.

| Stage | Responsibility |
|---|---|
| Backend CI | Validate backend code |
| Frontend CI | Validate frontend code |
| Quality checks | Enforce required checks |
| Docker build | Build application images |
| GHCR publishing | Store versioned images |
| Staging deployment | Deploy to a test environment |
| Production approval | Enforce deployment authorization |
| Production deployment | Deploy an approved release |
| Health verification | Check the deployed application |

### 1.2 Separation of concerns

A good pipeline follows these principles:

- Testing jobs should not need production credentials.
- Build jobs should not automatically receive unnecessary deployment permissions.
- Deployment jobs should depend on successful validation.
- Reusable workflows should contain shared automation.
- Security-sensitive operations should run only in trusted contexts.
- Each job should have the minimum permissions it requires.

**Important:** A job dependency controls execution order, but it does not automatically grant or restrict access to credentials. Permissions and secrets must be configured separately.

---

## 2. Advanced expressions and conditions

GitHub Actions expressions allow workflows to make decisions based on events, job results, variables, and outputs.

### 2.1 Common expression functions

| Function | Purpose |
|---|---|
| `success()` | Previous relevant steps or jobs succeeded |
| `failure()` | A previous relevant step or job failed |
| `always()` | Run regardless of success or failure, subject to cancellation behavior |
| `cancelled()` | The workflow or job was cancelled |
| `contains()` | Check whether a value contains another value |
| `startsWith()` | Check whether a string starts with a value |
| `endsWith()` | Check whether a string ends with a value |
| `format()` | Format a string |
| `toJSON()` | Convert a value into JSON |
| `fromJSON()` | Parse JSON into a value |

### 2.2 Example: conditional jobs

Create:

`.github/workflows/conditional-pipeline.yml`

```yaml
name: Conditional Pipeline

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Run tests
        run: echo "Tests completed"

  report:
    needs: tests
    if: always()
    runs-on: ubuntu-latest

    steps:
      - name: Report test result
        env:
          TEST_RESULT: ${{ needs.tests.result }}
        run: echo "Tests finished with: $TEST_RESULT"

  deploy:
    needs: tests
    if: github.ref == 'refs/heads/main' && needs.tests.result == 'success'
    runs-on: ubuntu-latest

    steps:
      - name: Deploy
        run: echo "Deployment is permitted"
```

Understand the execution:

1. `tests` runs first.
2. `report` runs even if the test job fails.
3. `deploy` runs only if the test job succeeds and the reference is `main`.

`always()` is useful for reporting and diagnostics. It should not be used indiscriminately for deployments.

### Exercise 1 — Conditional execution

Create a workflow containing three jobs:

1. `tests`: execute a simple command.
2. `report`: run even when tests fail and display the test result.
3. `deploy`: run only when tests succeed.

Temporarily change the test command to:

```yaml
run: exit 1
```

Verify that the reporting job executes while deployment is skipped.

Restore the successful test command afterward.

---

## 3. Job outputs and data sharing

Jobs run independently unless connected through dependencies.

Job outputs allow one job to pass small values to another.

Typical examples include:

- Application versions.
- Docker image tags.
- Build identifiers.
- Deployment identifiers.
- Generated configuration values.

### 3.1 Example: passing a version

Create:

`.github/workflows/job-outputs.yml`

```yaml
name: Job Outputs

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest

    outputs:
      app_version: ${{ steps.version.outputs.value }}

    steps:
      - name: Set application version
        id: version
        run: echo "value=1.2.0" >> "$GITHUB_OUTPUT"

  build:
    needs: prepare
    runs-on: ubuntu-latest

    steps:
      - name: Read application version
        env:
          APP_VERSION: ${{ needs.prepare.outputs.app_version }}
        run: echo "Building version $APP_VERSION"
```

### 3.2 Understand the output chain

There are three important steps:

#### Step 1 — Create a step output

```yaml
id: version
run: echo "value=1.2.0" >> "$GITHUB_OUTPUT"
```

#### Step 2 — Expose it as a job output

```yaml
outputs:
  app_version: ${{ steps.version.outputs.value }}
```

#### Step 3 — Read it from another job

```yaml
${{ needs.prepare.outputs.app_version }}
```

### 3.3 Important limitations

Use job outputs for small metadata.

Do not use them to transfer:

- Large files.
- Compiled application directories.
- Docker image archives.
- Test report collections.

Use workflow artifacts for files.

---

## 4. Artifacts: transferring files between jobs

Artifacts preserve files generated during a workflow run.

Examples include:

- Test reports.
- Coverage reports.
- Compiled frontend files.
- Documentation build output.
- Application packages.

### 4.1 Upload an artifact

Create:

`.github/workflows/artifact-example.yml`

```yaml
name: Artifact Example

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Create build output
        run: |
          mkdir -p dist
          echo "Build output" > dist/app.txt

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: frontend-build
          path: dist/

  inspect:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: frontend-build
          path: downloaded/

      - name: Inspect files
        run: ls -la downloaded/
```

### 4.2 Artifact vs cache

| Feature | Artifact | Cache |
|---|---|---|
| Primary purpose | Preserve workflow outputs | Reuse previously downloaded or generated data |
| Typical content | Reports and build files | Dependencies and package-manager data |
| Identification | Artifact name | Cache key |
| Retrieval | Download artifact | Restore matching cache |
| Reliability | Workflow output storage | Optimization mechanism |
| Backup replacement | No | No |

**Rule:** Artifacts transfer outputs. Caches improve performance.

A cache is not a permanent backup or a reliable build-output storage system.

---

## 5. Matrix strategies

A matrix lets one job execute multiple times with different configurations.

For example, you may need to test a Python application against several supported Python versions.

### 5.1 Static matrix

Create:

`.github/workflows/python-matrix.yml`

```yaml
name: Python Compatibility

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      max-parallel: 3

      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Display Python version
        run: python --version
```

The action references here are illustrative major-version tags. Verify current releases before adopting them, and pin reviewed full commit SHAs in production workflows.

### 5.2 Matrix settings

| Setting | Meaning |
|---|---|
| `fail-fast` | Cancel remaining matrix jobs after a failure when enabled |
| `max-parallel` | Limit simultaneous matrix jobs |
| `include` | Add or extend selected combinations |
| `exclude` | Remove specific combinations |

### 5.3 Matrix across operating systems

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ["3.11", "3.12"]

runs-on: ${{ matrix.os }}
```

This creates four combinations:

| Operating system | Python |
|---|---|
| Ubuntu | 3.11 |
| Ubuntu | 3.12 |
| Windows | 3.11 |
| Windows | 3.12 |

Matrix strategies are especially useful for libraries and reusable software packages that support multiple environments.

---

## 6. Dynamic matrices

A dynamic matrix is generated by one job and consumed by another.

This is useful when the list of applications, services, or test targets changes.

### 6.1 Example

Create:

`.github/workflows/dynamic-matrix.yml`

```yaml
name: Dynamic Matrix

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  prepare:
    runs-on: ubuntu-latest

    outputs:
      targets: ${{ steps.set-targets.outputs.targets }}

    steps:
      - name: Generate targets
        id: set-targets
        run: |
          echo 'targets=["backend","frontend","docker"]' >> "$GITHUB_OUTPUT"

  validate:
    needs: prepare
    runs-on: ubuntu-latest

    strategy:
      matrix:
        target: ${{ fromJSON(needs.prepare.outputs.targets) }}

    steps:
      - name: Validate target
        env:
          TARGET: ${{ matrix.target }}
        run: |
          echo "Validating $TARGET"
```

### 6.2 Understand the process

1. The preparation job generates a JSON array.
2. The array is exposed as a job output.
3. The next job reads the output.
4. `fromJSON()` converts the JSON string into a matrix.
5. GitHub Actions creates one job per target.

### Exercise 2 — Dynamic matrix

Modify the workflow to include:

- `backend`
- `frontend`
- `docker`
- `documentation`

Make each job print its target.

Then add a new target without modifying the validation job.

---

## 7. Reusable workflows

Reusable workflows allow you to define an entire workflow once and call it from other workflows.

This is useful when several repositories share the same CI standards.

A reusable workflow must declare `workflow_call`.

### 7.1 Create the reusable workflow

File:

`.github/workflows/reusable-python-tests.yml`

```yaml
name: Reusable Python Tests

on:
  workflow_call:
    inputs:
      python-version:
        required: false
        type: string
        default: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run tests
        run: pytest
```

This example assumes the calling repository contains a pytest-compatible project. It is a reference workflow, not a workflow to run unchanged in your documentation-only training repository.

### 7.2 Call the reusable workflow

File:

`.github/workflows/backend-ci.yml`

```yaml
name: Backend CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  python-tests:
    uses: ./.github/workflows/reusable-python-tests.yml

    with:
      python-version: "3.12"
```

Notice that a reusable workflow is called at the job level, not inside `steps`.

### 7.3 Passing secrets

A reusable workflow can declare secrets through `workflow_call`.

Example:

```yaml
on:
  workflow_call:
    secrets:
      DEPLOY_TOKEN:
        required: true
```

The caller passes the secret:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/deploy.yml

    secrets:
      DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

Pass only the secrets required by the called workflow.

Avoid `secrets: inherit` unless broad secret inheritance is intentional and justified.

### 7.4 Reusable workflow vs composite action

| Feature | Reusable workflow | Composite action |
|---|---|---|
| Reuses | Entire workflow | Sequence of steps |
| Can contain jobs | Yes | No |
| Called from | A job | A step |
| Typical location | `.github/workflows/` | Action directory |
| Best for | Shared CI/CD pipelines | Shared setup or task sequences |

---

## 8. Composite actions

A composite action packages multiple steps into one reusable action.

Unlike reusable workflows, composite actions are called from within a workflow's `steps`.

### 8.1 Create the action

Structure:

```text
.github/
└── actions/
    └── project-info/
        └── action.yml
```

File:

`.github/actions/project-info/action.yml`

```yaml
name: Project Information
description: Display project information

inputs:
  project-name:
    description: Project name
    required: true

  environment-name:
    description: Environment name
    required: true

runs:
  using: composite

  steps:
    - name: Display project information
      shell: bash
      env:
        PROJECT_NAME: ${{ inputs.project-name }}
        ENVIRONMENT_NAME: ${{ inputs.environment-name }}
      run: |
        echo "Project: $PROJECT_NAME"
        echo "Environment: $ENVIRONMENT_NAME"

    - name: Display repository
      shell: bash
      run: |
        echo "Repository: $GITHUB_REPOSITORY"
```

Notice that each composite `run` step specifies a shell.

Passing inputs through environment variables also avoids inserting arbitrary input values directly into shell source code.

### 8.2 Call the composite action

```yaml
steps:
  - uses: ./.github/actions/project-info
    with:
      project-name: "GitHub Deep Dive Training"
      environment-name: "staging"
```

### Exercise 3 — Composite action

Extend the action with:

- `project-version`
- `team-name`

Display all four inputs.

Then call the action from a separate workflow.

---

## 9. Concurrency control

Concurrency prevents unnecessary overlapping workflow runs.

For example, if you push several commits quickly, you may not want every outdated CI run to continue consuming resources.

### 9.1 Example

```yaml
name: CI

on:
  push:
    branches: [main]

  pull_request:

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Running CI"
```

### 9.2 Understand the settings

#### `group`

Identifies runs that belong to the same concurrency group.

#### `cancel-in-progress`

Allows a newer run to cancel an older in-progress run in the same group.

### 9.3 Deployment warning

For CI, cancelling outdated runs is often useful.

For deployments, cancellation requires more care.

Cancelling a deployment halfway through may leave an application in an inconsistent state.

Use a separate deployment concurrency group and choose cancellation behavior deliberately.

---

## 10. Timeouts and failure handling

Long-running or unstable steps should have explicit limits.

### 10.1 Job timeout

```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Run tests
        run: pytest
```

### 10.2 Step timeout

```yaml
- name: Run integration tests
  timeout-minutes: 10
  run: pytest tests/integration/
```

### 10.3 Continue after a non-critical failure

```yaml
- name: Generate optional report
  continue-on-error: true
  run: python scripts/generate_report.py
```

Use `continue-on-error` only when the failure is genuinely non-blocking.

Do not use it to make failing tests appear successful.

### 10.4 Failure diagnostics and final reporting

```yaml
- name: Run tests
  id: tests
  run: pytest

- name: Collect diagnostics
  if: failure()
  run: echo "Collecting diagnostic information"

- name: Final report
  if: always()
  env:
    RESULT: ${{ steps.tests.outcome }}
  run: echo "Test step outcome: $RESULT"
```

Remember:

- `steps.<id>.outcome` reports a step's outcome.
- `needs.<job_id>.result` reports a job result.
- `failure()` is useful for failure-specific diagnostics.
- `always()` is useful for final reporting and cleanup.

---

## 11. GitHub Environments

GitHub Environments allow you to separate deployment targets.

Common examples:

- `development`
- `staging`
- `production`

An environment can have its own:

- Secrets.
- Variables.
- Deployment branch and tag restrictions.
- Protection rules.
- Required reviewers, where supported by the repository plan and visibility.

### 11.1 Create environments

In your repository:

1. Open **Settings**.
2. Find **Environments**.
3. Create `staging`.
4. Create `production`.
5. Configure deployment branch or tag restrictions.
6. Configure required reviewers where available.

### 11.2 Reference an environment in a workflow

```yaml
name: Deployment Example

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - name: Deploy staging
        run: echo "Deploying to staging"

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy production
        run: echo "Deploying to production"
```

The `environment` declaration associates the job with an environment.

**Important:** YAML does not automatically create a required approval. Configure the protection rules in repository settings. Feature availability can depend on plan and repository visibility.

---

## 12. Deployment approvals

Production deployments should have explicit authorization controls.

A typical process:

```text
          CI checks pass
                |
                v
        Staging deployment
                |
                v
        Staging verification
                |
                v
       Production deployment
                |
                v
        Approval required
                |
                v
       Authorized deployment
```

A production environment can require reviewers before a job proceeds.

### Practical exercise

1. Create a `staging` environment.
2. Create a `production` environment.
3. Add deployment branch restrictions.
4. Configure reviewers if your repository supports them.
5. Associate a deployment job with `production`.
6. Trigger the workflow manually.
7. Inspect the deployment approval behavior.

Do not use real production credentials in this exercise.

---

## 13. OpenID Connect (OIDC)

A common deployment mistake is storing long-lived cloud access keys as GitHub secrets.

OpenID Connect provides another authentication approach.

### 13.1 OIDC authentication flow

```text
GitHub Actions
      |
      | Requests identity token
      v
GitHub OIDC provider
      |
      | Presents signed token
      v
Cloud identity provider
      |
      | Verifies trust conditions
      v
Temporary cloud credentials
      |
      v
Authorized cloud operation
```

### 13.2 Why OIDC is useful

Instead of storing a permanent cloud access key, the workflow can request an identity token.

The cloud provider verifies the token and issues temporary credentials if the trust policy allows it.

### 13.3 Workflow permissions

```yaml
permissions:
  contents: read
  id-token: write
```

`id-token: write` permits the workflow to request an OIDC token.

It does not itself grant permission to modify cloud resources.

The cloud provider's trust policy determines what the authenticated workflow can access.

### 13.4 Security requirements

- Restrict trust to the intended repository.
- Restrict the permitted branch or environment.
- Restrict the permitted workflow identity where supported.
- Grant only the cloud permissions needed.
- Use protected environments for production.
- Keep untrusted pull-request code away from deployment credentials.

OIDC is supported by several cloud providers, including AWS, Azure, and Google Cloud. Each provider requires its own identity-provider and trust configuration.

### Exercise 4 — OIDC preparation

Create a workflow that declares:

```yaml
permissions:
  contents: read
  id-token: write
```

Do not authenticate to a real cloud provider.

Document what the cloud trust policy should restrict before enabling deployment.

---

## 14. Docker build and publishing

For a Django + React application, you may eventually publish separate images:

```text
ghcr.io/your-account/your-app-backend
ghcr.io/your-account/your-app-frontend
```

The pipeline should publish images only after the required checks pass.

### 14.1 Understand GHCR

GitHub Container Registry (GHCR) stores Docker and OCI container images associated with GitHub accounts and organizations.

It is useful for:

- Storing backend images.
- Storing frontend images.
- Distributing versioned application builds.
- Connecting build pipelines with deployment systems.

### 14.2 Build and publish example

File:

`.github/workflows/docker-publish.yml`

Assumptions:

- The repository contains a root-level `Dockerfile`.
- The workflow runs on a trusted push to `main`.
- The repository has permission to publish packages.

```yaml
name: Build and Publish Docker Image

on:
  push:
    branches: [main]

  workflow_dispatch:

permissions:
  contents: read

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Normalize image name
        id: image
        env:
          REPOSITORY: ${{ github.repository }}
        run: |
          IMAGE_NAME=$(echo "$REPOSITORY" | tr '[:upper:]' '[:lower:]')
          echo "name=$IMAGE_NAME" >> "$GITHUB_OUTPUT"

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ steps.image.outputs.name }}:latest
            ghcr.io/${{ steps.image.outputs.name }}:${{ github.sha }}
```

The action references are illustrative. Check their current releases and pin reviewed full commit SHAs before using them in production.

### 14.3 Why use commit SHA tags?

The `latest` tag is convenient, but its value changes over time.

A commit SHA tag identifies the source revision used to build an image.

Example:

```text
ghcr.io/your-account/your-app:latest
ghcr.io/your-account/your-app:a1b2c3d4
```

A deployment record should identify the exact image version used.

### 14.4 Docker publishing security

- Do not publish images from untrusted pull-request code.
- Do not expose publishing credentials to ordinary test jobs.
- Grant only the required package permissions.
- Avoid putting secrets in Docker build arguments or image layers.
- Use reviewed action versions.
- Consider image scanning and provenance as later pipeline improvements.

**Training repository note:** Your `github-deep-dive-training` repository is documentation-focused. Do not activate this publishing workflow there unless you intentionally add a Dockerfile and a valid image build context.

---

## 15. Django backend CI

Now consider your real application architecture.

Assumed project:

```text
my-application/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   └── ...
└── .github/
    └── workflows/
```

The backend and frontend should have independent validation jobs.

### 15.1 Backend CI workflow

File:

`.github/workflows/backend-ci.yml`

```yaml
name: Backend CI

on:
  pull_request:
    paths:
      - "backend/**"
      - ".github/workflows/backend-ci.yml"

  push:
    branches: [main]
    paths:
      - "backend/**"
      - ".github/workflows/backend-ci.yml"

permissions:
  contents: read

concurrency:
  group: backend-ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  backend:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    defaults:
      run:
        working-directory: backend

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: backend/requirements.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Django system check
        run: python manage.py check

      - name: Run tests
        run: python manage.py test
```

Adjust the Python version, dependency files, and test commands to match the actual project's supported configuration.

If you use pytest, add the appropriate pytest and Django test dependencies and configure the test settings explicitly.

### 15.2 Why use path filters?

Path filters can avoid running backend CI when only frontend files change.

However, be careful with required status checks: skipped workflows can affect branch protection and merge requirements.

For a simpler first implementation, run backend and frontend CI on every pull request. Introduce path filtering after understanding the repository's required-check behavior.

---

## 16. React frontend CI

The frontend pipeline validates the React application independently.

### 16.1 Frontend workflow

File:

`.github/workflows/frontend-ci.yml`

```yaml
name: Frontend CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: frontend-ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  frontend:
    runs-on: ubuntu-latest
    timeout-minutes: 15

    defaults:
      run:
        working-directory: frontend

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v5
        with:
          node-version: "22"
          cache: npm
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Test
        run: npm test -- --run

      - name: Build
        run: npm run build
```

The example assumes your `package.json` contains:

- `lint`
- `typecheck`
- `test`
- `build`

Adapt the test command to your actual test runner.

### 16.2 Why separate backend and frontend CI?

Separate workflows make failures easier to identify.

For example:

| Failure | Responsible workflow |
|---|---|
| Django configuration error | Backend CI |
| Python test failure | Backend CI |
| TypeScript error | Frontend CI |
| React test failure | Frontend CI |
| Vite build failure | Frontend CI |

For larger applications, you can add separate workflows for integration tests, end-to-end tests, Docker publishing, and deployment.

---

## 17. PostgreSQL integration testing

Unit tests do not always verify how an application interacts with its database.

A service container allows a workflow job to run a temporary PostgreSQL instance.

### 17.1 PostgreSQL service example

```yaml
jobs:
  integration-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16

        env:
          POSTGRES_DB: app_test
          POSTGRES_USER: app_user
          POSTGRES_PASSWORD: test_password

        ports:
          - 5432:5432

        options: >-
          --health-cmd "pg_isready -U app_user -d app_test"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Configure test database
        env:
          DATABASE_HOST: localhost
          DATABASE_PORT: 5432
          DATABASE_NAME: app_test
          DATABASE_USER: app_user
          DATABASE_PASSWORD: test_password
        run: |
          echo "Configure your test settings to use PostgreSQL"
          echo "Install backend dependencies and run integration tests"
```

This demonstrates PostgreSQL service configuration. It does not execute Django tests yet.

To complete it:

1. Install your backend dependencies.
2. Configure Django to read the database environment variables.
3. Configure test settings.
4. Run migrations if your test strategy requires them.
5. Execute your integration tests.

The database credentials above are disposable test values, not production credentials.

### 17.2 Why service containers matter

They let you test against real supporting services without maintaining a permanent database server for every CI run.

Other possible service containers include:

- Redis.
- MySQL.
- PostgreSQL.
- Other compatible test services.

---

## 18. Release automation

A professional release process connects:

- Version numbers.
- Git tags.
- Release notes.
- Build artifacts.
- Published packages or images.

### 18.1 Semantic Versioning

Semantic Versioning follows:

```text
MAJOR.MINOR.PATCH
```

| Version change | Example | Meaning |
|---|---|---|
| Major | `2.0.0` | Incompatible public API changes |
| Minor | `1.4.0` | Backward-compatible functionality |
| Patch | `1.3.2` | Backward-compatible fixes |

### 18.2 Course tags vs application versions

Your training repository uses tags such as:

```text
module-04-lesson-34
module-04-lesson-35
```

These are course-progress tags, not software product versions.

For an actual application, use version tags such as:

```text
v1.0.0
v1.1.0
v1.1.1
```

Keep these naming conventions separate.

### 18.3 Create a release when a version tag is pushed

File:

`.github/workflows/release.yml`

```yaml
name: Create GitHub Release

on:
  push:
    tags:
      - "v*"

permissions:
  contents: read

jobs:
  release:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Create release
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          RELEASE_TAG: ${{ github.ref_name }}
        run: |
          gh release create "$RELEASE_TAG" --generate-notes --title "Release $RELEASE_TAG"
```

The workflow uses `contents: write` because creating a GitHub Release modifies repository release data.

### 18.4 Example release flow

```text
Feature development
       |
       v
Pull request
       |
       v
CI checks pass
       |
       v
Merge to main
       |
       v
Prepare version and changelog
       |
       v
Create annotated Git tag
       |
       v
Push version tag
       |
       v
GitHub Actions creates release
```

A tag-triggered workflow is not automatically a complete release process. Decide which checks must pass before creating the tag, and protect the release process accordingly.

---

## 19. Workflow security

Workflow files should be treated as application code.

They can access repository content, secrets, tokens, and external systems.

### 19.1 Security checklist

| Risk | Recommended control |
|---|---|
| Excessive token permissions | Set minimum `permissions` |
| Unreviewed third-party actions | Pin reviewed full commit SHAs |
| Secret exposure in logs | Never print secrets |
| Untrusted pull-request code | Keep privileged credentials away from PR jobs |
| Unsafe deployment triggers | Restrict branches, tags, and environments |
| Overpowered self-hosted runners | Isolate runners and limit access |
| Untrusted shell input | Pass values through environment variables and validate them |
| Unnecessary deployment access | Use protected environments and restricted credentials |

### 19.2 Full-SHA pinning

A reference such as:

```yaml
uses: actions/checkout@v4
```

is readable and convenient, but a version tag can move.

For stronger supply-chain control, pin the action to a reviewed full commit SHA.

Conceptually:

```yaml
uses: actions/checkout@FULL_REVIEWED_COMMIT_SHA
```

Use the real full SHA from the action's official repository. Do not copy a placeholder into a production workflow.

### 19.3 Be careful with pull_request_target

`pull_request_target` runs in a privileged context compared with ordinary `pull_request` workflows.

Never check out and execute untrusted pull-request code in a privileged workflow without a carefully reviewed security design.

A safer default for normal pull-request testing is `pull_request`, with minimal permissions and no production credentials.

### 19.4 Secret-handling principles

- Store credentials in GitHub Secrets or an appropriate external secret manager.
- Use variables for non-sensitive configuration.
- Do not print credentials.
- Do not commit credentials into workflow files.
- Do not assume log masking makes secret exposure safe.
- Restrict secrets to the jobs and environments that need them.

---

## 20. Practical assignments

Complete these assignments in `github-deep-dive-training`.

## Level 1 — Advanced workflow fundamentals

**Difficulty:** Intermediate

- [ ] Create a workflow with three dependent jobs.
- [ ] Use `needs` to control execution order.
- [ ] Use `if: failure()` for a failure report.
- [ ] Use `if: always()` for final reporting.
- [ ] Set a job timeout.
- [ ] Add a concurrency group.
- [ ] Create a matrix for three Python versions.
- [ ] Generate a job output and read it from another job.

**Expected result:** You understand how to control workflow execution instead of simply executing steps sequentially.

## Level 2 — Reusable automation

**Difficulty:** Advanced

- [ ] Create a reusable Python testing workflow.
- [ ] Create another workflow that calls it.
- [ ] Pass a Python version as an input.
- [ ] Create a composite action for project information.
- [ ] Transfer an artifact between two jobs.
- [ ] Generate a dynamic matrix using job outputs.
- [ ] Create a staging environment.
- [ ] Document the difference between reusable workflows and composite actions.

**Expected result:** You can build reusable automation instead of duplicating YAML across projects.

## Level 3 — Professional CI/CD architecture

**Difficulty:** Advanced

Use a separate application repository for the application-specific tasks.

- [ ] Create independent backend and frontend CI workflows.
- [ ] Add PostgreSQL integration testing.
- [ ] Build a Docker image.
- [ ] Publish the image to GHCR.
- [ ] Use a commit SHA as an image tag.
- [ ] Create a protected production environment.
- [ ] Design an OIDC authentication configuration.
- [ ] Create a tag-triggered release workflow.
- [ ] Document your pipeline architecture.

**Expected result:** You can design a CI/CD pipeline for a real application and explain the responsibilities of each stage.

---

## 21. Recommended repository structure

For your training repository, use:

```text
github-deep-dive-training/
│
├── .github/
│   ├── workflows/
│   │   ├── conditional-pipeline.yml
│   │   ├── job-outputs.yml
│   │   ├── artifact-example.yml
│   │   ├── python-matrix.yml
│   │   ├── dynamic-matrix.yml
│   │   └── repository-ci.yml
│   │
│   └── actions/
│       └── project-info/
│           └── action.yml
│
└── docs/
    └── github/
        └── module-04-actions/
            ├── lesson-34-github-actions-fundamentals.md
            ├── lesson-35-advanced-github-actions.md
            ├── reusable-workflows.md
            ├── composite-actions.md
            ├── github-actions-security.md
            ├── docker-and-ghcr.md
            └── ci-cd-architecture.md
```

### Important repository distinction

Your training repository is primarily a documentation and learning project.

Therefore:

#### Implement now

- Conditional workflow.
- Job outputs.
- Artifact transfer.
- Static matrix.
- Dynamic matrix.
- Composite action.
- Documentation validation.

#### Keep as application reference examples until you have a suitable application repository

- Django CI.
- React CI.
- PostgreSQL integration tests.
- Docker publishing.
- Production deployment.
- OIDC cloud authentication.

Do not add workflows that are guaranteed to fail because their expected application files do not exist.

---

## 22. Troubleshooting exercises

| Problem | What to investigate |
|---|---|
| A `needs` job is skipped | Check dependency results and `if` conditions |
| Job output is empty | Check step ID, `$GITHUB_OUTPUT`, and output mapping |
| Artifact cannot be found | Check upload/download names and job dependencies |
| Matrix fails unexpectedly | Inspect generated JSON and matrix configuration |
| Reusable workflow cannot be called | Verify `workflow_call` and workflow location |
| Composite action fails | Verify `action.yml`, inputs, and shell declarations |
| GHCR permission denied | Check `packages: write` and package access |
| Docker image push fails | Check image naming, authentication, and build context |
| Deployment waits indefinitely | Check environment protection rules and approvals |
| OIDC authentication fails | Check token permissions and cloud trust conditions |
| Workflow runs repeatedly | Inspect triggers, generated commits, and concurrency |
| Job takes too long | Review timeouts, dependency installation, and caching |
| Production deployment is cancelled | Review concurrency and cancellation settings |

### Debugging exercise

Choose three problems from the table.

For each one:

1. Create a workflow that reproduces the problem.
2. Inspect the Actions execution log.
3. Identify the cause.
4. Apply a correction.
5. Document the resolution.

---

## 23. Git practice — commit, push, tag, and release

Use your existing `github-deep-dive-training` repository.

### Step 1 — Inspect your repository

```powershell
git status
git branch --show-current
git remote -v
```

Make sure your working tree is clean before starting.

### Step 2 — Update your local main branch

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
```

If the fast-forward pull fails because your local and remote branches have diverged, stop and reconcile the histories before continuing. Do not force-push.

### Step 3 — Create a feature branch

```powershell
git switch -c docs/lesson-35-advanced-actions
```

### Step 4 — Create the documentation

Create:

```text
docs/github/module-04-actions/lesson-35-advanced-github-actions.md
```

Add the workflow examples you have actually completed.

### Step 5 — Add practical workflow files

Start with:

```text
.github/workflows/conditional-pipeline.yml
.github/workflows/job-outputs.yml
.github/workflows/artifact-example.yml
.github/workflows/python-matrix.yml
.github/workflows/dynamic-matrix.yml
.github/actions/project-info/action.yml
```

Only add the files you intend to test and maintain.

### Step 6 — Validate your changes

```powershell
git diff --check
```

Review the changed files:

```powershell
git status
git diff
```

Also validate YAML syntax and GitHub Actions-specific workflow rules with a YAML-aware editor or workflow linter.

### Step 7 — Commit

```powershell
git add .github docs/github/module-04-actions
git commit -m "docs(github): add Lesson 35 advanced Actions"
```

### Step 8 — Push

```powershell
git push -u origin docs/lesson-35-advanced-actions
```

### Step 9 — Open a pull request

On GitHub:

1. Open your repository.
2. Create a pull request from `docs/lesson-35-advanced-actions` into `main`.
3. Review all workflow files.
4. Inspect the Actions checks.
5. Fix any failures.
6. Request a review if you are practicing two-person collaboration.
7. Merge the pull request.

### Step 10 — Create your lesson tag

After merging:

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
git tag -a module-04-lesson-35 -m "Module 4 - Lesson 35: Advanced GitHub Actions"
git push origin module-04-lesson-35
```

### Step 11 — Create a GitHub Release

#### Release tag

`module-04-lesson-35`

#### Release title

Module 4 — Lesson 35: Advanced GitHub Actions

#### Release notes

- Advanced workflow architecture and expressions.
- Job outputs, artifacts, and matrix strategies.
- Reusable workflows and composite actions.
- Concurrency, timeouts, and failure handling.
- GitHub Environments and deployment approvals.
- OIDC authentication.
- Docker publishing and GHCR.
- Django + React CI/CD architecture.
- Release automation and workflow security.

---

## 24. Key takeaways

| Concept | What it solves |
|---|---|
| Job outputs | Passing small values between jobs |
| Artifacts | Passing files between jobs |
| Cache | Reusing dependencies and other data |
| Matrix | Running jobs across multiple configurations |
| Dynamic matrix | Generating configurations at runtime |
| Reusable workflow | Sharing complete workflow pipelines |
| Composite action | Packaging reusable steps |
| Concurrency | Controlling overlapping workflow runs |
| Timeout | Limiting execution duration |
| Environment | Separating deployment targets and protections |
| Deployment approval | Controlling access to sensitive deployment stages |
| OIDC | Obtaining temporary cloud credentials |
| GHCR | Storing and distributing container images |
| Semantic Versioning | Communicating application release changes |
| Full-SHA pinning | Improving action supply-chain integrity |

The most important professional skill is knowing how to combine these features without making workflows unnecessarily complicated or granting them excessive permissions.

---

## 25. Official documentation

Use these resources as your reference material.

1. [Reusing workflow configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations)
2. [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
3. [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
4. [Expressions](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions)
5. [Passing information between jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs)
6. [Workflow artifacts](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts)
7. [Dependency caching](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
8. [Composite actions](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action)
9. [Managing environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
10. [OpenID Connect in cloud providers](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers)
11. [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
12. [Publishing packages with GitHub Actions](https://docs.github.com/en/packages/learn-github-packages/publishing-and-installing-a-package-with-github-actions)
13. [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

---

## 26. Next lesson preview

## Lesson 36 — Advanced CI/CD Security, Quality Gates & Supply Chain Security

In Lesson 36, we'll extend the pipeline beyond building and testing applications.

Topics:

1. GitHub Actions security architecture.
2. Full-SHA pinning and action dependency management.
3. Token permissions and secure workflow design.
4. Static Application Security Testing (SAST).
5. Dependency vulnerability scanning.
6. Dependabot security updates and version updates.
7. Secret scanning and push protection.
8. Software Bill of Materials (SBOM).
9. Container image scanning.
10. Artifact attestations and provenance.
11. Quality gates and coverage thresholds.
12. Integrating Ruff, pytest, SonarQube, Trivy, and Gitleaks.
13. Building a security-focused CI pipeline for Django + React.

### Lesson 35 completion target

Complete at least the Level 1 assignments, create the lesson documentation, test your workflows, and commit/tag the lesson.

Then continue to Lesson 36 using the same practical lesson structure.

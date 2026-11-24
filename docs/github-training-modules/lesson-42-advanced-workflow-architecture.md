# Module 4 — GitHub Actions & DevSecOps

## Lesson 42 — Advanced GitHub Actions Architecture & Reusable Workflows

**Level:** Advanced
**Focus:** Practical engineering
**Module:** GitHub Actions & DevSecOps

---

## 1. Lesson overview

In Lesson 40, you studied how to secure individual GitHub Actions workflows.

In Lesson 41, you studied repository-wide security automation and compliance.

Now we move to another important engineering challenge:

**How do you design CI/CD automation that can be maintained and reused across multiple repositories?**

Imagine that you eventually manage several applications:

```text
Your GitHub Organization
│
├── restaurant-pos
│   ├── Django backend
│   └── React frontend
│
├── pharmacy-dashboard
│   ├── Django backend
│   └── React frontend
│
├── queue-system
│   ├── Django backend
│   └── React frontend
│
├── github-workflow-library
│
└── github-deep-dive-training
```

Each application might need:

- Python testing.
- React testing.
- Code quality checks.
- Security scanning.
- Docker builds.
- Dependency updates.
- Deployment workflows.
- Release automation.
- Artifact generation.
- Environment approvals.

Maintaining separate copies of these workflows creates duplication and increases maintenance costs.

For example, imagine discovering a security problem in your Python CI workflow. If every repository contains its own copy, you must update and validate every copy independently.

A centralized architecture allows you to maintain shared automation and consume it from multiple repositories.

### Practical project

Extend `github-deep-dive-training` by creating:

1. Reusable workflows.
2. Composite Actions.
3. A JavaScript custom Action.
4. A Docker custom Action.
5. A workflow orchestration architecture.
6. A centralized workflow-library design.
7. A multi-environment deployment design.

By the end, you should understand how to design automation as reusable engineering components rather than isolated YAML files.

---

## 2. Learning objectives

After completing this lesson, you should be able to:

- Explain the differences between reusable workflows, composite Actions, and custom Actions.
- Create reusable workflows using `workflow_call`.
- Define and validate workflow inputs.
- Return workflow outputs to callers.
- Pass secrets explicitly and safely.
- Create composite Actions.
- Build JavaScript Actions with the GitHub Actions Toolkit.
- Build Docker container Actions.
- Design a centralized workflow repository.
- Version and release reusable automation.
- Configure organization-level Actions governance.
- Use GitHub Environments and deployment protection rules.
- Control concurrent workflow executions.
- Build static and dynamic matrices.
- Manage dependencies between jobs.
- Configure dependency caching.
- Upload and download workflow artifacts.
- Optimize workflow execution.
- Trigger automation across repositories.
- Interact with the GitHub Actions REST API.
- Apply least-privilege permissions to reusable automation.
- Design reusable Django + React CI/CD architecture.
- Plan controlled development, staging, and production deployments.

---

## 3. Lesson curriculum

| # | Topic |
|---:|---|
| 1 | Reusable workflows with `workflow_call` |
| 2 | Workflow inputs |
| 3 | Workflow outputs |
| 4 | Passing secrets |
| 5 | Composite Actions |
| 6 | JavaScript custom Actions |
| 7 | Docker custom Actions |
| 8 | Centralized workflow repositories |
| 9 | Workflow versioning and release management |
| 10 | Organization-level workflow governance |
| 11 | GitHub Environments |
| 12 | Deployment approvals |
| 13 | Concurrency and cancellation |
| 14 | Workflow matrices |
| 15 | Dynamic matrices |
| 16 | Conditional execution and job dependencies |
| 17 | Caching strategies |
| 18 | Artifact management |
| 19 | Workflow performance optimization |
| 20 | Cross-repository automation |
| 21 | GitHub Actions APIs |
| 22 | Advanced permissions and token design |
| 23 | Reusable Django + React CI/CD |
| 24 | Multi-environment deployment |
| 25 | End-to-end reusable workflow project |

---

## Part 1 — Reusable Automation Architecture

## 4. Understand the three reusable automation concepts

Before building anything, understand the three main ways to reuse GitHub Actions automation.

### 4.1 Reusable workflow

A reusable workflow is a complete workflow that another workflow calls.

It can contain:

- Multiple jobs.
- Job dependencies.
- Runner selection.
- Permissions.
- Inputs and secrets.
- Outputs.
- Conditions.
- Matrix strategies.
- Artifacts.

Example:

```yaml
jobs:
  backend-ci:
    uses: ./.github/workflows/reusable-python-tests.yml
    with:
      python-version: "3.12"
```

The calling workflow invokes another workflow instead of repeating all its jobs and steps.

### 4.2 Composite Action

A composite Action packages multiple steps into one reusable Action.

Example:

```yaml
steps:
  - uses: actions/checkout@v6

  - name: Python quality
    uses: ./.github/actions/python-quality
```

The composite Action can contain several steps, including shell commands and calls to other Actions.

However, it runs inside the caller's job. It cannot independently select a runner or create additional jobs.

### 4.3 Custom Action

A custom Action packages specialized functionality.

You can implement one using:

- JavaScript.
- TypeScript compiled to JavaScript.
- Docker.
- Composite Action metadata.

Example:

```yaml
steps:
  - uses: ./.github/actions/repository-validator
```

A custom Action is useful when you want to distribute a specific capability across multiple workflows or repositories.

### 4.4 Comparison

| Capability | Reusable workflow | Composite Action | JavaScript/Docker Action |
|---|---|---|---|
| Reuse complete jobs | Yes | No | No |
| Reuse multiple steps | Through called workflow | Yes | Through Action execution |
| Define runners | Yes | No | No |
| Define job dependencies | Yes | No | No |
| Accept inputs | Yes | Yes | Yes |
| Return outputs | Yes | Yes | Yes |
| Package specialized logic | Possible | Limited | Yes |
| Version independently | Yes | Yes | Yes |
| Best use | CI/CD pipelines | Repeated step sequences | Specialized automation |

### 4.5 Which one should you choose?

Use a reusable workflow when you need to share a complete CI/CD process.

Use a composite Action when you need to share a sequence of steps inside existing jobs.

Use a JavaScript or Docker Action when you need to package a specialized executable capability.

A mature organization can use all three together.

Example:

```text
Application Workflow
       |
       v
Reusable CI Workflow
       |
       +--------------------+
       |                    |
       v                    v
Backend Job             Frontend Job
       |                    |
       v                    v
Python Composite       Node Composite
Action                 Action
       |                    |
       v                    v
Python Quality         Frontend Quality
```

---

## 5. Reusable workflows with `workflow_call`

### 5.1 What is `workflow_call`?

A reusable workflow is a workflow designed to be called by another workflow.

GitHub requires the reusable workflow to:

1. Exist inside `.github/workflows/`.
2. Declare `workflow_call` as an event trigger.
3. Define any required inputs and secrets.
4. Be accessible to the calling repository.

Reusable workflow files cannot be stored in arbitrary subdirectories under `.github/workflows/`.

### 5.2 Create the reusable Python workflow

Create:

```text
.github/
└── workflows/
    └── reusable-python-tests.yml
```

File: `.github/workflows/reusable-python-tests.yml`

```yaml
name: Reusable Python Tests

on:
  workflow_call:
    inputs:
      python-version:
        description: Python version used for testing
        required: false
        type: string
        default: "3.12"

      working-directory:
        description: Directory containing the Python project
        required: false
        type: string
        default: "backend"

      requirements-file:
        description: Python dependency file
        required: false
        type: string
        default: "requirements.txt"

jobs:
  tests:
    name: Python Tests

    runs-on: ubuntu-latest

    permissions:
      contents: read

    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6

      - name: Setup Python
        uses: actions/setup-python@v6
        with:
          python-version: ${{ inputs.python-version }}
          cache: pip
          cache-dependency-path: ${{ inputs.working-directory }}/${{ inputs.requirements-file }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r "${{ inputs.requirements-file }}"
          pip install pytest ruff

      - name: Run Ruff
        run: ruff check .

      - name: Run tests
        run: python -m pytest
```

This workflow:

1. Accepts a Python version.
2. Accepts a project directory.
3. Accepts a requirements file.
4. Checks out the repository.
5. Configures Python.
6. Installs dependencies.
7. Runs Ruff.
8. Executes tests.

**Important:** This example assumes the dependency file exists at the supplied path and that the project uses pytest. Adapt the installation and test commands to your actual application.

For production workflows, validate inputs before using them in filesystem paths or shell commands.

### 5.3 Create the caller workflow

Create:

```text
.github/workflows/backend-ci.yml
```

```yaml
name: Backend CI

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  python-tests:
    uses: ./.github/workflows/reusable-python-tests.yml

    with:
      python-version: "3.12"
      working-directory: "backend"
      requirements-file: "requirements.txt"
```

Notice the difference.

The caller does not define:

- `runs-on`.
- Individual steps.
- Python installation.
- Dependency installation.
- Test execution.

The called workflow owns those responsibilities.

### 5.4 Reuse the same workflow with different configurations

You can call the same workflow multiple times.

```yaml
name: Python Compatibility

on:
  pull_request:

permissions:
  contents: read

jobs:
  python-312:
    name: Python 3.12
    uses: ./.github/workflows/reusable-python-tests.yml
    with:
      python-version: "3.12"
      working-directory: "backend"

  python-313:
    name: Python 3.13
    uses: ./.github/workflows/reusable-python-tests.yml
    with:
      python-version: "3.13"
      working-directory: "backend"
```

GitHub creates two independent jobs.

```text
Python Compatibility
       |
       +-------------------+
       |                   |
       v                   v
Python 3.12             Python 3.13
       |                   |
       v                   v
Run tests               Run tests
```

They can execute in parallel.

Only test versions that your application and dependencies actually support.

### 5.5 Important caller-job restrictions

A job that calls a reusable workflow uses the `uses` property.

You cannot combine that reusable-workflow call with ordinary job-level `steps` or `runs-on` configuration as if it were a normal job.

For example, this is not a valid reusable-workflow caller:

```yaml
jobs:
  tests:
    uses: ./.github/workflows/reusable-python-tests.yml
    runs-on: ubuntu-latest
    steps:
      - run: echo "This is not valid here"
```

Put those steps inside the reusable workflow instead.

---

## 6. Workflow inputs, outputs, and secrets

Reusable workflows communicate with their callers through three important mechanisms.

- Inputs: configuration sent to the called workflow.
- Outputs: information returned to the caller.
- Secrets: credentials or sensitive values passed to the called workflow.

### 6.1 Workflow inputs

Reusable workflow inputs support three types:

- `string`
- `boolean`
- `number`

Example:

```yaml
on:
  workflow_call:
    inputs:
      environment:
        description: Deployment environment
        required: true
        type: string

      run-tests:
        description: Whether tests should run
        required: false
        type: boolean
        default: true

      coverage-threshold:
        description: Minimum coverage percentage
        required: false
        type: number
        default: 80
```

Use these inputs inside the called workflow:

```yaml
${{ inputs.environment }}
${{ inputs.run-tests }}
${{ inputs.coverage-threshold }}
```

Example:

```yaml
jobs:
  tests:
    if: ${{ inputs.run-tests }}

    runs-on: ubuntu-latest

    steps:
      - name: Display configuration
        env:
          TARGET_ENVIRONMENT: ${{ inputs.environment }}
          COVERAGE_THRESHOLD: ${{ inputs.coverage-threshold }}
        run: |
          echo "Environment: $TARGET_ENVIRONMENT"
          echo "Coverage threshold: $COVERAGE_THRESHOLD"
```

Passing an input does not automatically validate that its value is appropriate for your application.

For example, if the only supported environments are `development`, `staging`, and `production`, validate the supplied value against that list.

### 6.2 Workflow outputs

Outputs allow a reusable workflow to return information to its caller.

The output chain is:

```text
Step output
     |
     v
Job output
     |
     v
Workflow output
     |
     v
Caller job output
     |
     v
Another caller job
```

Create:

`.github/workflows/reusable-build.yml`

```yaml
name: Reusable Build

on:
  workflow_call:
    outputs:
      build-result:
        description: Result returned by the build job
        value: ${{ jobs.build.outputs.result }}

jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    outputs:
      result: ${{ steps.build-result.outputs.status }}

    steps:
      - name: Build application
        id: build-result
        run: |
          echo "status=success" >> "$GITHUB_OUTPUT"
```

The caller:

```yaml
name: Build Caller

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml

  report:
    needs: build

    runs-on: ubuntu-latest

    steps:
      - name: Display build result
        env:
          BUILD_RESULT: ${{ needs.build.outputs.build-result }}
        run: |
          echo "Build result: $BUILD_RESULT"
```

The `report` job waits for the reusable workflow job and reads its output.

### 6.3 Passing secrets explicitly

Suppose a reusable deployment workflow needs a deployment token.

The reusable workflow declares the secret:

```yaml
name: Reusable Deployment

on:
  workflow_call:
    secrets:
      DEPLOY_TOKEN:
        description: Deployment credential
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest

    permissions:
      contents: read

    steps:
      - name: Use deployment credential
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
        run: |
          echo "Deployment credential is available"
```

The caller passes it:

```yaml
name: Deployment Caller

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml

    secrets:
      DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

Do not print the actual secret value.

### 6.4 Using `secrets: inherit`

You can also use:

```yaml
jobs:
  deploy:
    uses: ./.github/workflows/reusable-deploy.yml
    secrets: inherit
```

This passes available caller secrets to the called workflow, subject to GitHub's access and workflow rules.

However, explicit secret mapping is usually easier to audit because it documents which credentials the called workflow is expected to receive.

### 6.5 Nested reusable workflows

A reusable workflow can call another reusable workflow.

Example:

```text
Application Workflow
       |
       v
Reusable CI Workflow
       |
       +------------------+
       |                  |
       v                  v
Python CI           Security CI
       |
       v
Reusable Report Workflow
```

Important rules:

1. Every workflow in the chain must be accessible to the caller.
2. Secrets must be passed through the relevant workflow levels.
3. Permissions cannot be elevated through the nested workflow chain.
4. Permissions can remain the same or become more restrictive.
5. Workflow nesting has a documented maximum depth.
6. Circular workflow references are not allowed.

Design nested workflows carefully. Excessive nesting makes debugging and permission reviews harder.

---

## 7. Composite Actions

### 7.1 What is a composite Action?

A composite Action packages multiple workflow steps into one reusable Action.

Imagine that every Python project needs to:

1. Configure Python.
2. Install dependencies.
3. Run Ruff.
4. Execute tests.

You can package those steps once and reuse them.

### 7.2 Create the directory

```text
.github/
└── actions/
    └── python-quality/
        └── action.yml
```

### 7.3 Create `action.yml`

```yaml
name: Python Quality Checks

description: Install Python dependencies and run quality checks

inputs:
  python-version:
    description: Python version
    required: false
    default: "3.12"

  requirements-file:
    description: Requirements file path
    required: false
    default: "requirements.txt"

runs:
  using: composite

  steps:
    - name: Setup Python
      uses: actions/setup-python@v6
      with:
        python-version: ${{ inputs.python-version }}

    - name: Install dependencies
      shell: bash
      env:
        REQUIREMENTS_FILE: ${{ inputs.requirements-file }}
      run: |
        python -m pip install --upgrade pip
        pip install -r "$REQUIREMENTS_FILE"
        pip install ruff pytest

    - name: Run Ruff
      shell: bash
      run: ruff check .

    - name: Run tests
      shell: bash
      run: python -m pytest
```

Notice that each shell step declares a shell.

Also notice that the input is passed through an environment variable instead of being inserted directly into the shell command.

This is a useful habit when handling values that might contain unexpected characters.

### 7.4 Use the composite Action

Create:

`.github/workflows/python-quality.yml`

```yaml
name: Python Quality

on:
  pull_request:

permissions:
  contents: read

jobs:
  quality:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: backend

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Python Quality
        uses: ./.github/actions/python-quality
        with:
          python-version: "3.12"
          requirements-file: "requirements.txt"
```

The composite Action runs inside the caller's job.

### 7.5 Composite Action outputs

Composite Actions can also return outputs.

Example:

```yaml
name: Build Information

description: Generate application build information

outputs:
  build-version:
    description: Generated build version
    value: ${{ steps.version.outputs.value }}

runs:
  using: composite

  steps:
    - name: Generate version
      id: version
      shell: bash
      run: |
        VERSION="training-1.0"
        echo "value=$VERSION" >> "$GITHUB_OUTPUT"
```

The caller can access the output:

```yaml
steps:
  - name: Generate build information
    id: build-info
    uses: ./.github/actions/build-information

  - name: Display version
    env:
      BUILD_VERSION: ${{ steps.build-info.outputs.build-version }}
    run: echo "$BUILD_VERSION"
```

### 7.6 Composite Action versus reusable workflow

| Question | Composite Action | Reusable workflow |
|---|---|---|
| Can define jobs? | No | Yes |
| Can select runners? | No | Yes |
| Can call another Action? | Yes | Yes |
| Can manage job dependencies? | No | Yes |
| Can accept inputs? | Yes | Yes |
| Can return outputs? | Yes | Yes |
| Best for | Repeated steps | Complete pipelines |

---

## 8. Build a JavaScript custom Action

### 8.1 Why create a custom Action?

Sometimes a sequence of shell commands is not enough.

You may want a reusable tool that:

- Validates repository documentation.
- Checks release naming conventions.
- Validates project metadata.
- Generates standardized reports.
- Interacts with the GitHub API.
- Checks repository configuration.

For this exercise, create a repository validator.

### 8.2 Directory structure

```text
.github/
└── actions/
    └── repository-validator/
        ├── action.yml
        ├── package.json
        ├── package-lock.json
        ├── src/
        │   └── index.js
        └── dist/
            └── index.js
```

### 8.3 Create `package.json`

Start with:

```json
{
  "name": "repository-validator",
  "version": "1.0.0",
  "private": true,
  "description": "Validate required repository documentation",
  "scripts": {
    "build": "ncc build src/index.js -o dist"
  }
}
```

Install the dependencies:

```bash
npm install @actions/core
npm install --save-dev @vercel/ncc
```

This creates a lockfile containing the resolved dependency versions.

Commit the lockfile, not the `node_modules` directory.

### 8.4 Create `src/index.js`

```javascript
const core = require("@actions/core");
const fs = require("fs");
const path = require("path");

try {
  const requiredFiles = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "SECURITY.md"
  ];

  const workspace = process.env.GITHUB_WORKSPACE || process.cwd();

  const missingFiles = requiredFiles.filter((file) => {
    const filePath = path.join(workspace, file);
    return !fs.existsSync(filePath);
  });

  if (missingFiles.length > 0) {
    core.setFailed(
      `Missing required files: ${missingFiles.join(", ")}`
    );
  } else {
    core.info("Repository documentation is complete.");
  }
} catch (error) {
  core.setFailed(error.message);
}
```

The Action checks whether required documentation files exist.

### 8.5 Create `action.yml`

```yaml
name: Repository Validator

description: Validate required repository documentation

runs:
  using: node24
  main: dist/index.js
```

GitHub documents the `node24` runtime for JavaScript Actions. Make sure your runner environment supports the runtime you select.

### 8.6 Build the Action

From the Action directory:

```bash
npm install
npm run build
```

The build creates:

```text
dist/
└── index.js
```

The generated bundle includes the Action's required dependencies.

**Important:** Commit the generated `dist/index.js` file. GitHub needs the bundled runtime code when executing the Action.

### 8.7 Use the Action

Create:

`.github/workflows/repository-validation.yml`

```yaml
name: Repository Validation

on:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Validate repository
        uses: ./.github/actions/repository-validator
```

### 8.8 Improve the Action

Extend it with configurable inputs.

For example:

```yaml
inputs:
  required-files:
    description: Comma-separated list of required files
    required: false
    default: "README.md,LICENSE,SECURITY.md"
```

Then read the input using:

```javascript
const requiredFiles = core
  .getInput("required-files")
  .split(",")
  .map((file) => file.trim())
  .filter(Boolean);
```

For production code, validate input values and prevent paths from escaping the intended repository workspace.

### 8.9 Documentation requirements

Create a README for the Action explaining:

- What it does.
- Required inputs.
- Optional inputs.
- Outputs.
- Required permissions.
- Example usage.
- Supported runtime.
- Versioning policy.

A reusable Action should be treated like a small software product.

---

## 9. Build a Docker custom Action

### 9.1 When should you use Docker Actions?

Docker Actions are useful when your automation requires a specific execution environment.

Examples:

- A Python-based scanner.
- A report generator with system dependencies.
- A specialized command-line tool.
- A custom application requiring particular libraries.

JavaScript Actions are often more lightweight. Docker Actions introduce container execution and image-build overhead.

### 9.2 Directory structure

```text
.github/
└── actions/
    └── docker-validator/
        ├── action.yml
        ├── Dockerfile
        └── entrypoint.sh
```

### 9.3 Create `Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
```

For production, review and pin base-image versions or digests according to your image-maintenance policy.

### 9.4 Create `entrypoint.sh`

```sh
#!/bin/sh

set -eu

echo "Running custom repository validation"

python --version

echo "Validation completed"
```

### 9.5 Create `action.yml`

```yaml
name: Docker Repository Validator

description: Validate repository using a Docker environment

runs:
  using: docker
  image: Dockerfile
```

### 9.6 Use the Action

```yaml
name: Docker Validation

on:
  pull_request:

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Docker validation
        uses: ./.github/actions/docker-validator
```

Docker container Actions require a Linux runner.

### 9.7 Compare custom Action types

| Type | Execution model | Main advantage |
|---|---|---|
| Composite | Multiple workflow steps | Simple reuse |
| JavaScript | Node.js runtime | Lightweight packaged logic |
| Docker | Container environment | Custom execution environment |

---

## Part 2 — Centralized Automation

## 10. Centralized workflow repositories

Now move from reusing workflows within one repository to sharing them across multiple repositories.

This is a major architectural step.

### 10.1 Why centralize workflows?

Imagine that your organization maintains:

```text
Organization
│
├── restaurant-pos
│
├── pharmacy-dashboard
│
├── queue-system
│
├── github-deep-dive-training
│
└── github-workflow-library
```

All four applications might need Python CI.

Without reusable workflows:

```text
restaurant-pos
└── python-ci.yml

pharmacy-dashboard
└── python-ci.yml

queue-system
└── python-ci.yml
```

Every repository maintains a separate copy.

With centralized automation:

```text
github-workflow-library
└── .github/
    └── workflows/
        └── python-ci.yml
              |
              +----------------------+
              |          |           |
              v          v           v
          Restaurant  Pharmacy    Queue
```

The consumer repositories call the shared workflow.

### 10.2 Recommended workflow-library structure

Create a separate repository later:

`github-workflow-library`

Suggested structure:

```text
github-workflow-library/
│
├── .github/
│   ├── workflows/
│   │   ├── python-ci.yml
│   │   ├── node-ci.yml
│   │   ├── django-ci.yml
│   │   ├── react-ci.yml
│   │   ├── docker-build.yml
│   │   └── security-scan.yml
│   │
│   └── actions/
│       ├── setup-python/
│       ├── setup-node/
│       └── repository-validator/
│
├── docs/
│   ├── usage.md
│   ├── versioning.md
│   └── security.md
│
└── README.md
```

### 10.3 Call a centralized workflow

Suppose your GitHub owner is `YOUR_OWNER`.

In an application repository:

```yaml
name: Restaurant Backend CI

on:
  pull_request:

permissions:
  contents: read

jobs:
  tests:
    uses: YOUR_OWNER/github-workflow-library/.github/workflows/python-ci.yml@v1

    with:
      python-version: "3.12"
      working-directory: "backend"
```

Replace `YOUR_OWNER` with the actual GitHub account or organization.

The reference contains:

```text
OWNER/REPOSITORY/.github/workflows/FILE@REF
```

### 10.4 Private workflow repositories

For private workflow libraries, configure the repository's Actions access settings to permit the intended consumer repositories.

Review:

- Which repositories can access the shared workflow.
- Whether the workflow contains sensitive information.
- Who can modify the workflow.
- Who can publish new versions.
- Whether workflow logs may expose information to users with access to consuming repositories.

Do not assume that making a workflow repository private automatically makes every interaction with it safe.

### 10.5 Design reusable workflow boundaries

Avoid creating one enormous workflow that handles everything.

Prefer separate workflows with clear responsibilities.

| Workflow | Responsibility |
|---|---|
| `python-ci.yml` | Python setup, Ruff, pytest |
| `node-ci.yml` | Node setup, linting, tests |
| `django-ci.yml` | Django checks and migrations validation |
| `react-ci.yml` | React tests and production build |
| `security-scan.yml` | Security scanning |
| `docker-build.yml` | Container build |
| `release.yml` | Release preparation |

Keep application-specific configuration in the consuming repository.

For example, the shared Django workflow should accept the application directory and relevant test configuration rather than assuming every application has exactly the same structure.

---

## 11. Workflow versioning and release management

Reusable workflows and custom Actions are software components.

They need version management.

Imagine that you update the shared Python workflow and accidentally break three applications.

Versioning helps consumers control when they adopt changes.

### 11.1 Semantic versioning

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

| Version | Meaning | Example |
|---|---|---|
| Major | Breaking changes | `v2.0.0` |
| Minor | Backward-compatible functionality | `v1.2.0` |
| Patch | Backward-compatible fixes | `v1.2.1` |

Examples:

- Removing a required input: potentially a major change.
- Adding an optional input with a safe default: usually a minor change.
- Fixing a workflow bug without changing its interface: usually a patch change.

### 11.2 Tag the workflow library

After testing and merging a release:

```bash
git tag -a v1.0.0 -m "Initial reusable workflow release"

git push origin v1.0.0
```

Then a consumer can reference:

```yaml
jobs:
  tests:
    uses: YOUR_OWNER/github-workflow-library/.github/workflows/python-ci.yml@v1.0.0
```

### 11.3 Tags versus commit SHAs

You can reference external Actions and reusable workflows using a branch, tag, or commit SHA.

Examples:

```yaml
uses: organization/workflow-library/.github/workflows/python-ci.yml@v1.0.0
```

Or:

```yaml
uses: organization/workflow-library/.github/workflows/python-ci.yml@FULL_COMMIT_SHA
```

For production supply-chain security, a full commit SHA provides an immutable reference to the exact revision.

Version tags are easier to read and manage, but a tag can be moved unless you protect it through repository governance.

A practical policy:

- Use readable version tags for development and training.
- Use protected release tags.
- Prefer full commit SHAs for production dependencies where strict immutability is required.
- Review and update pinned references through controlled pull requests.

### 11.4 Release process

```text
Feature development
       |
       v
Pull request
       |
       v
Workflow tests
       |
       v
Review
       |
       v
Merge
       |
       v
Create version tag
       |
       v
Publish GitHub Release
       |
       v
Consumer repositories update
```

### 11.5 Exercise

Create `docs/github/module-04-actions/lesson-42/workflow-versioning.md`.

Document:

1. Your versioning format.
2. What qualifies as a breaking change.
3. How you test new versions.
4. How consumer repositories update.
5. How you handle a broken release.
6. How you protect release tags.

---

## 12. Organization-level workflow governance

When you move from personal repositories to GitHub Organizations, you need shared governance.

Example:

```text
Organization
│
├── github-workflow-library
│
├── restaurant-pos
│
├── pharmacy-dashboard
│
└── queue-system
```

An organization can define policies controlling which Actions and reusable workflows repositories may use.

### 12.1 Review organization Actions settings

Navigate to:

`Organization → Settings → Actions → General`

Review the available settings for:

1. Actions permissions.
2. Allowed Actions and reusable workflows.
3. Workflow permissions.
4. Fork pull request behavior.
5. Runner groups.
6. Private workflow access.
7. Required security controls.

The exact settings and availability depend on the GitHub plan and organization configuration.

### 12.2 Example organization policy

Create:

`docs/github/module-04-actions/lesson-42/organization-workflow-governance.md`

Document the following policy:

| Policy area | Example requirement |
|---|---|
| Approved Actions | Only reviewed and approved Actions |
| External dependencies | Use pinned versions or SHAs according to policy |
| Workflow permissions | Least privilege |
| Secrets | Explicitly pass only required secrets |
| Deployment | Only approved workflows may deploy |
| Production | Use protected environments |
| Workflow ownership | Central library maintained by designated maintainers |
| Release management | Versioned and reviewed releases |
| Runner access | Restricted runner groups |
| Exceptions | Documented owner, reason, and expiration |

### 12.3 Important governance principle

Do not blindly restrict every workflow to organization-owned Actions.

Some essential GitHub-authored Actions, such as checkout and setup Actions, may also need to be allowed by your policy.

Review the complete dependency list before enforcing an organization-wide restriction.

---

## Part 3 — Deployment Architecture

## 13. GitHub Environments

A real application usually has several environments.

### 13.1 Development

Purpose:

- Frequent integration.
- Development testing.
- Early deployment validation.

### 13.2 Staging

Purpose:

- Pre-production testing.
- Integration testing.
- Acceptance testing.
- Release candidate validation.

### 13.3 Production

Purpose:

- Controlled releases.
- Protected deployment credentials.
- Deployment approvals where configured.
- Operational health checks.

### 13.4 Create environments

Navigate to:

`Repository → Settings → Environments`

Create:

```text
development
staging
production
```

For each environment, review:

- Environment secrets.
- Environment variables.
- Deployment branch restrictions.
- Required reviewers.
- Available protection rules.

Some protection features depend on your GitHub plan and repository visibility.

### 13.5 Deployment workflow

Create:

`.github/workflows/deploy-training.yml`

```yaml
name: Deployment Training

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Target environment
        required: true
        type: choice
        options:
          - development
          - staging
          - production

permissions:
  contents: read

jobs:
  deploy:
    name: Training Deployment

    runs-on: ubuntu-latest

    environment:
      name: ${{ inputs.environment }}

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Display deployment target
        env:
          TARGET: ${{ inputs.environment }}
        run: |
          echo "Deployment target: $TARGET"
          echo "Training deployment only"
```

This workflow does not deploy an application.

It demonstrates how a workflow selects a GitHub Environment.

### 13.6 Environment-specific secrets

You might eventually have:

| Environment | Example configuration |
|---|---|
| Development | Development API configuration |
| Staging | Staging deployment credentials |
| Production | Production deployment credentials |

Never use production credentials in development workflows.

Keep secrets in the appropriate GitHub environment or external secrets-management system.

---

## 14. Deployment approvals

A production deployment should not necessarily happen automatically whenever a developer merges code.

A controlled deployment process might look like this:

```text
Release Candidate
       |
       v
Staging Deployment
       |
       v
Integration Tests
       |
       v
Production Deployment Requested
       |
       v
Required Reviewer Approval
       |
       +---- Rejected ----> Deployment does not proceed
       |
       +---- Approved ---> Deployment continues
```

### 14.1 Configure production protection

1. Open repository Settings.
2. Select Environments.
3. Open `production`.
4. Configure required reviewers where available.
5. Restrict deployment branches or tags.
6. Configure production-specific secrets.
7. Review who can administer the environment.

### 14.2 Understand the approval boundary

A job that references a protected environment must satisfy the environment's configured protection rules before it can access the environment's protected resources.

The approval mechanism is not a replacement for:

- Code review.
- CI checks.
- Security scanning.
- Release validation.
- Deployment health checks.

### 14.3 Exercise

Create a `production` training environment.

Use a harmless workflow that only prints the deployment target.

If your repository supports required reviewers, configure and test the approval process.

Do not connect real production infrastructure for this exercise.

---

## 15. Concurrency and cancellation

Concurrency controls help prevent multiple workflow executions from interfering with each other.

Imagine that three commits are pushed to `main` within a short period.

You might have three CI or deployment workflows starting simultaneously.

This can create unnecessary work or conflicting deployments.

### 15.1 Basic concurrency

```yaml
name: CI

on:
  push:
    branches:
      - main

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Run CI
        run: echo "Running CI"
```

This groups executions by Git reference.

When a new run starts in the same group, an older in-progress run can be cancelled.

This is useful for obsolete pull request checks.

### 15.2 Pull request concurrency

```yaml
concurrency:
  group: pr-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

This groups runs for the same pull request or reference.

### 15.3 Deployment concurrency

For deployments, you may prefer:

```yaml
concurrency:
  group: production-deployment
  cancel-in-progress: false
```

This prevents overlapping runs in the same concurrency group.

**Important:** Concurrency groups are not a complete deployment queue. GitHub may replace pending executions in the same group. Do not assume every pending deployment will eventually execute.

For production deployment systems, use an explicit release and promotion process.

### 15.4 Common use cases

| Scenario | Strategy |
|---|---|
| Pull request CI | Cancel obsolete runs |
| Development deployment | Cancel outdated runs when safe |
| Production deployment | Prevent overlapping deployments |
| Nightly scans | Avoid duplicate executions |

### 15.5 Exercise

Create:

`.github/workflows/concurrency-training.yml`

Test:

1. Push a commit.
2. Quickly push another commit.
3. Inspect the workflow runs.
4. Observe cancellation behavior.
5. Document the result.

---

## Part 4 — Workflow Orchestration

## 16. Workflow matrices

A matrix allows GitHub to execute the same job with multiple configurations.

For Django, you might test multiple Python versions.

### 16.1 Basic matrix

Create:

`.github/workflows/python-matrix.yml`

```yaml
name: Python Matrix Testing

on:
  pull_request:

permissions:
  contents: read

jobs:
  tests:
    name: Python ${{ matrix.python-version }}

    runs-on: ubuntu-latest

    strategy:
      fail-fast: false

      matrix:
        python-version:
          - "3.12"
          - "3.13"

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Setup Python
        uses: actions/setup-python@v6
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install pytest
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run tests
        run: python -m pytest
```

GitHub creates two jobs:

```text
Python Matrix
│
├── Python 3.12
│
└── Python 3.13
```

### 16.2 Multiple matrix dimensions

```yaml
strategy:
  fail-fast: false

  matrix:
    python-version:
      - "3.12"
      - "3.13"

    operating-system:
      - ubuntu-latest
      - windows-latest
```

This creates four combinations:

| Python | Operating system |
|---|---|
| 3.12 | Ubuntu |
| 3.12 | Windows |
| 3.13 | Ubuntu |
| 3.13 | Windows |

### 16.3 Matrix controls

| Property | Purpose |
|---|---|
| `fail-fast` | Cancel other matrix jobs after a failure when enabled |
| `max-parallel` | Limit simultaneous matrix jobs |
| `include` | Add or extend combinations |
| `exclude` | Remove combinations |

Example:

```yaml
strategy:
  fail-fast: false
  max-parallel: 2

  matrix:
    python-version:
      - "3.12"
      - "3.13"

    include:
      - python-version: "3.13"
        experimental: true
```

### 16.4 Reusable workflow matrices

You can also use a matrix when calling a reusable workflow.

```yaml
jobs:
  python-tests:
    strategy:
      matrix:
        python-version:
          - "3.12"
          - "3.13"

    uses: ./.github/workflows/reusable-python-tests.yml

    with:
      python-version: ${{ matrix.python-version }}
      working-directory: backend
```

This combines reusable workflow architecture with matrix execution.

### 16.5 Exercise

Create a Python matrix workflow.

Inspect:

- How many jobs GitHub generates.
- How each job is named.
- How failures are reported.
- What happens when `fail-fast` changes.
- How `max-parallel` affects execution.

---

## 17. Dynamic matrices

A dynamic matrix is generated by an earlier job rather than being completely hardcoded.

This is useful when an application contains several independently maintained services.

Imagine:

```text
Restaurant Platform
│
├── backend
├── frontend
├── worker
└── notification-service
```

You can generate a list of services and pass it to another job.

### 17.1 Create the dynamic matrix workflow

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
      services: ${{ steps.matrix.outputs.services }}

    steps:
      - name: Generate service matrix
        id: matrix
        run: |
          echo 'services=["backend","frontend","worker"]' >> "$GITHUB_OUTPUT"

  test:
    needs: prepare

    runs-on: ubuntu-latest

    strategy:
      matrix:
        service: ${{ fromJSON(needs.prepare.outputs.services) }}

    steps:
      - name: Display service
        env:
          SERVICE: ${{ matrix.service }}
        run: |
          echo "Testing $SERVICE"
```

### 17.2 Understand the process

1. The `prepare` job generates JSON.
2. The step writes the JSON to `$GITHUB_OUTPUT`.
3. The job publishes the step output.
4. The `test` job reads the job output.
5. `fromJSON()` converts the JSON string into a matrix.
6. GitHub creates one job per service.

The result:

```text
Prepare
  |
  v
Generate JSON
  |
  v
Test Matrix
  |
  +-----------------------+
  |           |           |
  v           v           v
Backend    Frontend     Worker
```

### 17.3 Dynamic matrix validation

Do not construct a dynamic matrix directly from untrusted input without validation.

For example, do not allow arbitrary pull request content to determine privileged deployment targets.

Use an allowlist:

```text
Allowed services:
- backend
- frontend
- worker
```

Validate the generated list before passing it to later jobs.

A dynamic matrix is an orchestration mechanism, not a security boundary.

### 17.4 Exercise

Extend the matrix to include:

- Backend.
- Frontend.
- Worker.
- Notification service.

Generate the matrix dynamically and verify the jobs in the Actions interface.

---

## 18. Conditional execution and job dependencies

Workflows often contain jobs that should run only when specific conditions are satisfied.

GitHub provides:

- `needs`
- `if`
- `success()`
- `failure()`
- `always()`
- `cancelled()`

### 18.1 Job dependencies

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Testing"

  build:
    needs: test

    runs-on: ubuntu-latest

    steps:
      - run: echo "Building"

  report:
    needs:
      - test
      - build

    runs-on: ubuntu-latest

    steps:
      - run: echo "Generating report"
```

The execution order:

```text
Test
  |
  v
Build
  |
  v
Report
```

### 18.2 Multiple independent dependencies

```yaml
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Backend tests"

  frontend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Frontend tests"

  build:
    needs:
      - backend
      - frontend

    runs-on: ubuntu-latest

    steps:
      - run: echo "Build application"
```

The backend and frontend jobs can run in parallel.

The build waits for both.

### 18.3 Run a job only on main

```yaml
if: github.ref == 'refs/heads/main'
```

### 18.4 Run after a failure

```yaml
if: failure()
```

Example:

```yaml
jobs:
  report-failure:
    needs: tests
    if: failure()

    runs-on: ubuntu-latest

    steps:
      - run: echo "A previous job failed"
```

### 18.5 Always execute reporting

```yaml
if: always()
```

Use this carefully.

A reporting or cleanup job may need to execute even when a dependency fails. However, `always()` can also affect cancellation and job scheduling behavior.

Understand the status functions and dependency conditions before applying them to critical workflows.

### 18.6 Exercise

Create a workflow with:

1. Backend tests.
2. Frontend tests.
3. Build job.
4. Success report.
5. Failure report.

Test both successful and intentionally failing scenarios.

---

## 19. Caching strategies

Caching reduces repeated dependency installation and build time.

For your stack:

| Technology | Typical cache |
|---|---|
| Python | pip download/cache directory |
| Node.js | npm cache |
| Docker | BuildKit layers |
| Playwright | Browser binaries, when appropriate |

### 19.1 Python dependency caching

```yaml
- name: Setup Python
  uses: actions/setup-python@v6
  with:
    python-version: "3.12"
    cache: pip
    cache-dependency-path: backend/requirements.txt
```

The cache dependency path helps GitHub determine when the dependency cache should be refreshed.

If your project uses multiple requirements files or lockfiles, configure the correct paths.

### 19.2 Node.js dependency caching

```yaml
- name: Setup Node
  uses: actions/setup-node@v6
  with:
    node-version: "22"
    cache: npm
    cache-dependency-path: frontend/package-lock.json
```

Choose a Node.js version supported by your application and its dependencies.

### 19.3 Manual caching

GitHub also provides `actions/cache`.

Example:

```yaml
- name: Cache custom directory
  uses: actions/cache@v4
  with:
    path: ~/.cache/my-tool
    key: my-tool-${{ runner.os }}-${{ hashFiles('**/tool.lock') }}
    restore-keys: |
      my-tool-${{ runner.os }}-
```

Use a lockfile or other dependency definition in the cache key whenever possible.

### 19.4 Cache security

Caches are not a place to store credentials or sensitive files.

Also consider cache trust boundaries.

For example:

- Untrusted pull request workflows should not write data that privileged workflows blindly trust.
- Production deployment workflows should not consume unverified build caches.
- Cache keys should separate incompatible environments.
- Cache contents should not be treated as trusted release artifacts.

### 19.5 Exercise

Add Python caching to your test workflow.

Run the workflow twice.

Compare:

- Dependency installation time.
- Cache restoration behavior.
- Cache creation behavior.
- What happens after changing the requirements file.

---

## 20. Artifact management

Artifacts allow workflows to preserve and transfer files between jobs.

Examples:

- Test reports.
- Coverage reports.
- Compiled frontend assets.
- Docker build metadata.
- SBOM files.
- Release packages.

### 20.1 Generate a test report

For example, configure pytest to generate a report:

```bash
python -m pytest --junitxml=reports/pytest-results.xml
```

Make sure the `reports/` directory exists before writing the file.

### 20.2 Upload an artifact

```yaml
- name: Upload test report
  uses: actions/upload-artifact@v4
  with:
    name: pytest-report
    path: reports/
    if-no-files-found: error
    retention-days: 7
```

### 20.3 Download an artifact

In another job:

```yaml
- name: Download test report
  uses: actions/download-artifact@v4
  with:
    name: pytest-report
    path: downloaded-reports/
```

### 20.4 Complete artifact example

```yaml
name: Artifact Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Create report
        run: |
          mkdir -p reports
          echo "Training test report" > reports/report.txt

      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: training-report
          path: reports/
          retention-days: 7

  report:
    needs: tests

    runs-on: ubuntu-latest

    steps:
      - name: Download report
        uses: actions/download-artifact@v4
        with:
          name: training-report
          path: downloaded-reports/

      - name: Display report
        run: cat downloaded-reports/report.txt
```

### 20.5 Artifact security and retention

For release artifacts, consider:

- Integrity.
- Provenance.
- Retention.
- Access permissions.
- Artifact naming.
- Build-to-release traceability.
- Whether the artifact was generated from the expected commit.

An uploaded artifact is not automatically a verified release artifact.

### 20.6 Exercise

Create a workflow that:

1. Runs a simple test.
2. Generates a report.
3. Uploads the report.
4. Downloads it in another job.
5. Displays its content.

---

## 21. Workflow performance optimization

A well-designed workflow should be reliable and efficient.

### 21.1 Common optimization techniques

| Technique | Benefit |
|---|---|
| Dependency caching | Reduce installation time |
| Parallel jobs | Reduce total pipeline duration |
| Matrix limits | Control resource consumption |
| Conditional jobs | Avoid unnecessary work |
| Path filters | Skip unrelated workflows |
| Reusable workflows | Reduce duplication |
| Smaller Docker images | Reduce build and transfer overhead |
| Artifact reuse | Avoid rebuilding the same output |
| Appropriate runner selection | Match workload requirements |

### 21.2 Path filtering

Frontend tests do not necessarily need to run when only backend documentation changes.

Example:

```yaml
name: Frontend CI

on:
  pull_request:
    paths:
      - "frontend/**"
      - ".github/workflows/frontend-ci.yml"

permissions:
  contents: read

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - run: echo "Run frontend CI"
```

**Important:** Be careful when required checks interact with path filters. A workflow that does not run may leave a required status check pending, depending on how the repository's protection rules are configured.

For larger monorepos, consider a dedicated change-detection job that reports which components need testing.

### 21.3 Parallel execution

```yaml
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Backend tests"

  frontend:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Frontend tests"

  security:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Security checks"
```

These jobs can run independently.

### 21.4 Measure improvements

Record:

- Total workflow duration.
- Individual job duration.
- Cache hit behavior.
- Runner usage.
- Failed runs.
- Time spent waiting for dependencies.
- Time spent downloading dependencies.
- Number of unnecessary workflow executions.

Do not optimize purely for speed if it weakens security or test coverage.

### 21.5 Exercise

Measure your workflow before and after adding caching and parallel jobs.

Create a short report:

```text
Before optimization:
- Total duration:
- Backend duration:
- Frontend duration:
- Cache behavior:

After optimization:
- Total duration:
- Backend duration:
- Frontend duration:
- Cache behavior:

Conclusion:
- What improved?
- What remained unchanged?
- What trade-offs did you observe?
```

Use actual workflow run data rather than invented performance measurements.

---

## Part 5 — Cross-Repository Automation and APIs

## 22. Cross-repository automation

Now consider automation that interacts with multiple repositories.

Examples:

- Create an issue in another repository.
- Trigger another repository's workflow.
- Update release documentation.
- Synchronize labels.
- Report deployment status.
- Coordinate version updates.

### 22.1 Repository dispatch

GitHub supports the `repository_dispatch` event for external events that trigger workflows.

Create the receiver:

`.github/workflows/external-event.yml`

```yaml
name: External Event Receiver

on:
  repository_dispatch:
    types:
      - training-event

permissions:
  contents: read

jobs:
  process:
    runs-on: ubuntu-latest

    steps:
      - name: Display event type
        env:
          EVENT_TYPE: ${{ github.event.action }}
        run: |
          echo "Received event: $EVENT_TYPE"
```

The receiver waits for a matching event type.

### 22.2 Workflow dispatch

`workflow_dispatch` allows a workflow to be triggered manually.

It can also be triggered through the GitHub API by an appropriately authorized caller.

Example:

```yaml
on:
  workflow_dispatch:
    inputs:
      message:
        description: Training message
        required: true
        type: string
```

### 22.3 Authentication options

For cross-repository access, consider:

- GitHub Apps.
- Fine-grained personal access tokens.
- `GITHUB_TOKEN` when its repository permissions are sufficient.

Use the smallest permissions necessary.

Avoid giving a workflow broad organization-wide access when it only needs to trigger one repository's workflow.

### 22.4 Cross-repository security

Review:

1. Which repository is allowed to send events.
2. Which token authenticates the request.
3. Which permissions the token has.
4. Whether event payload data is trusted.
5. Whether the receiver validates event fields.
6. Whether the triggered workflow can access sensitive secrets.

Do not treat event payloads as trusted commands.

### 22.5 Exercise

Create two training repositories if you want to test cross-repository events.

Configure:

- A receiver workflow.
- An authorized sender.
- A documented event type.
- A harmless event payload.

Do not give the sender unnecessary write permissions.

---

## 23. GitHub Actions REST API

GitHub provides REST and GraphQL APIs for interacting with Actions.

You can retrieve information such as:

- Workflow runs.
- Workflow definitions.
- Jobs.
- Logs.
- Artifacts.
- Workflow execution status.
- Workflow usage.

Official reference:

[GitHub Actions REST API](https://docs.github.com/en/rest/actions)

### 23.1 Retrieve workflow runs

Endpoint:

```http
GET /repos/{owner}/{repo}/actions/runs
```

This endpoint returns workflow run information for a repository.

### 23.2 Trigger a workflow

Endpoint:

```http
POST /repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
```

The request includes a Git reference and optionally configured workflow inputs.

### 23.3 Python integration example

Create a local training script.

File: `scripts/github_actions_report.py`

```python
import os
import requests

owner = "YOUR_OWNER"
repo = "github-deep-dive-training"

token = os.environ["GITHUB_TOKEN"]

url = (
    f"https://api.github.com/repos/"
    f"{owner}/{repo}/actions/runs"
)

response = requests.get(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    timeout=30,
)

response.raise_for_status()

data = response.json()

for run in data.get("workflow_runs", []):
    print(
        run["name"],
        run["status"],
        run["conclusion"],
    )
```

Install the dependency:

```bash
pip install requests
```

Set the token through an environment variable.

Do not hardcode it in the script.

For this read operation, use a token with only the repository access and read permissions required by the endpoint.

### 23.4 Example output

```text
Backend CI completed success
Frontend CI completed success
Security Scan completed success
Deployment Training completed success
```

The output above is illustrative, not a result from your repository.

### 23.5 API exercise

Create a script that:

1. Reads a token from the environment.
2. Retrieves workflow runs.
3. Prints workflow name.
4. Prints status.
5. Prints conclusion.
6. Handles HTTP errors.
7. Handles missing environment variables.

Do not commit the token.

---

## Part 6 — Security and Permissions

## 24. Advanced permissions and token design

This topic connects directly to Lesson 40.

Reusable workflows do not remove the need for least-privilege permissions.

Consider:

```text
Caller Workflow
      |
      v
Reusable CI Workflow
      |
      v
Reusable Security Workflow
      |
      v
Reusable Deployment Workflow
```

Each workflow should receive only the permissions it requires.

### 24.1 Example permission design

| Workflow | Example permissions |
|---|---|
| Testing | `contents: read` |
| Security scanning | `contents: read` |
| PR commenting | `pull-requests: write`, when required |
| Release creation | Specific release-related permissions |
| OIDC cloud authentication | `id-token: write` |
| Deployment | Only the permissions required by the deployment process |

### 24.2 Declare permissions explicitly

Example:

```yaml
permissions:
  contents: read
```

For a job that needs to create or update pull request comments:

```yaml
permissions:
  contents: read
  pull-requests: write
```

Avoid granting write permissions to every job just because one job requires them.

### 24.3 Reusable workflow permission boundaries

A called workflow cannot increase permissions beyond the permissions available to the caller.

For example:

```yaml
permissions:
  contents: read
```

The called workflow cannot turn that into unrestricted write access.

Nested reusable workflows can maintain or reduce permissions, not elevate them.

### 24.4 Secrets design

Prefer:

```yaml
secrets:
  DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

over:

```yaml
secrets: inherit
```

when the called workflow only needs one or two specific credentials.

Use `secrets: inherit` only when the broader secret-sharing behavior is intentional and reviewed.

### 24.5 Third-party Action security

For external Actions:

- Review the source repository.
- Review the maintainer and release history.
- Check the permissions requested.
- Pin versions or commit SHAs according to policy.
- Review dependency updates.
- Avoid passing secrets to untrusted Actions.
- Do not execute untrusted pull request code in privileged workflows.

### 24.6 OIDC

OpenID Connect can allow a GitHub Actions workflow to obtain short-lived cloud credentials without storing long-lived cloud credentials as repository secrets.

The workflow commonly requires:

```yaml
permissions:
  contents: read
  id-token: write
```

The cloud provider must also be configured to trust the intended GitHub identity and claims.

Do not grant `id-token: write` to workflows that do not need it.

### 24.7 Exercise

Create:

`docs/github/module-04-actions/lesson-42/token-and-permission-design.md`

Document permissions for:

- Testing.
- Security scanning.
- Pull request commenting.
- Artifact publication.
- Release creation.
- Deployment.
- Cross-repository automation.

For each permission, explain why it is required.

---

## Part 7 — Django + React CI/CD Architecture

## 25. Design reusable CI/CD for Django + React

Now apply everything to your technology stack.

The objective is to create reusable automation that can eventually be shared across your applications.

### 25.1 Proposed application structure

```text
restaurant-platform/
│
├── backend/
│   ├── config/
│   ├── apps/
│   ├── tests/
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── package-lock.json
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
└── .github/
    └── workflows/
        ├── ci.yml
        ├── backend-ci.yml
        ├── frontend-ci.yml
        ├── security.yml
        ├── container-build.yml
        └── deploy.yml
```

### 25.2 Shared workflow library

The centralized repository might contain:

```text
github-workflow-library/
│
└── .github/
    └── workflows/
        ├── python-ci.yml
        ├── node-ci.yml
        ├── django-ci.yml
        ├── react-ci.yml
        ├── security.yml
        ├── docker-build.yml
        └── release.yml
```

### 25.3 Workflow responsibilities

| Workflow | Responsibility |
|---|---|
| `python-ci.yml` | Python installation, Ruff, pytest |
| `node-ci.yml` | Node setup, ESLint, TypeScript |
| `django-ci.yml` | Django checks and migrations validation |
| `react-ci.yml` | React tests and production build |
| `security.yml` | Security scanning |
| `docker-build.yml` | Docker image build |
| `release.yml` | Versioning and release |

### 25.4 Application caller workflow

Create:

`.github/workflows/ci.yml`

```yaml
name: Application CI

on:
  pull_request:
    branches:
      - main

permissions:
  contents: read

jobs:
  backend:
    name: Backend CI

    uses: YOUR_OWNER/github-workflow-library/.github/workflows/django-ci.yml@v1.0.0

    with:
      python-version: "3.12"
      working-directory: "backend"

  frontend:
    name: Frontend CI

    uses: YOUR_OWNER/github-workflow-library/.github/workflows/react-ci.yml@v1.0.0

    with:
      node-version: "22"
      working-directory: "frontend"

  security:
    name: Security Checks

    uses: YOUR_OWNER/github-workflow-library/.github/workflows/security.yml@v1.0.0
```

This is an architectural example. The called workflow files must actually define the inputs shown here.

### 25.5 Add a build job

You can add a build job that waits for both backend and frontend CI:

```yaml
  build:
    name: Application Build

    needs:
      - backend
      - frontend

    runs-on: ubuntu-latest

    steps:
      - name: Build completed
        run: echo "Application build stage completed"
```

In a real project, the build stage should produce the intended application artifacts or container images.

### 25.6 Architecture diagram

```text
                 Application Repository
                          |
                          v
                     ci.yml
                          |
           +--------------+--------------+
           |              |              |
           v              v              v
      Django CI        React CI      Security CI
           |              |              |
           v              v              |
      Backend Tests   Frontend Tests      |
           |              |              |
           +--------------+--------------+
                          |
                          v
                     Build Stage
                          |
                          v
                   Release Artifact
                          |
                          v
                 Deployment Workflow
                          |
            +-------------+-------------+
            |             |             |
            v             v             v
       Development     Staging      Production
                                      |
                                      v
                                Approval
```

### 25.7 Important architecture decision

The shared workflow library should define common engineering standards.

The application repository should define application-specific configuration.

For example:

**Shared workflow library:**

- Python setup.
- Node setup.
- Linting.
- Testing.
- Security checks.
- Artifact handling.
- Standard job permissions.

**Application repository:**

- Python version.
- Node version.
- Working directories.
- Test configuration.
- Application-specific environment variables.
- Deployment target.
- Environment-specific settings.

This separation makes the architecture reusable without forcing every application into an identical structure.

---

## 26. Multi-environment deployment architecture

The final architectural topic is deployment across several environments.

### 26.1 Deployment configuration

| Environment | Trigger | Approval |
|---|---|---|
| Development | Merge to development branch or configured integration event | Usually automatic |
| Staging | Release candidate | Controlled |
| Production | Approved release | Required where configured |

### 26.2 Recommended workflow

```text
Pull Request
     |
     v
CI + Security
     |
     v
Merge to Main
     |
     v
Build Artifact
     |
     v
Deploy Development
     |
     v
Integration Tests
     |
     v
Deploy Staging
     |
     v
Acceptance Tests
     |
     v
Production Approval
     |
     v
Production Deployment
     |
     v
Health Check
     |
     v
Release Complete
```

### 26.3 Deployment strategies

| Strategy | Description |
|---|---|
| Rolling deployment | Gradually replace application instances |
| Blue-green | Maintain two environments and switch traffic |
| Canary | Release to a limited portion of traffic first |
| Recreate | Replace the running version directly |

These strategies are implemented by the deployment platform and infrastructure, not by GitHub Actions alone.

GitHub Actions orchestrates the process.

### 26.4 Deployment artifact promotion

A useful production architecture builds an artifact once and promotes the same artifact through environments.

```text
Source Commit
     |
     v
Build
     |
     v
Test
     |
     v
Scan
     |
     v
Publish Immutable Artifact
     |
     v
Development
     |
     v
Staging
     |
     v
Production
```

Avoid rebuilding different artifacts for staging and production if the intention is to promote the exact same release candidate.

Record the artifact version or digest so that the deployed artifact can be traced to the original build.

### 26.5 Local-first deployment consideration

For your local-first restaurant POS architecture, deployment must eventually account for:

- Offline operation.
- Local server availability.
- Database backups.
- Controlled updates.
- Recovery procedures.
- Local network connectivity.
- Compatibility between server and client versions.

CI/CD should not assume that the restaurant's operational system has continuous internet access.

A deployment process may need to prepare and validate an update package centrally, then transfer and install it through a controlled local update process.

GitHub Actions can automate the build and validation stages without requiring the operational restaurant system to remain connected to GitHub.

---

## Part 8 — End-to-End Practical Project

## 27. Main project: Build a reusable workflow architecture

Your main project is to extend:

`github-deep-dive-training`

You will build four major components:

1. Reusable workflows.
2. Composite Actions.
3. Custom JavaScript Action.
4. Integrated caller workflow.

You will also create training examples for Docker Actions, matrices, environments, caching, artifacts, and API integration.

### 27.1 Target structure

```text
github-deep-dive-training/
│
├── .github/
│   │
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── reusable-python-tests.yml
│   │   ├── reusable-node-tests.yml
│   │   ├── reusable-security.yml
│   │   ├── reusable-build.yml
│   │   ├── python-matrix.yml
│   │   ├── dynamic-matrix.yml
│   │   ├── deploy-training.yml
│   │   ├── external-event.yml
│   │   ├── artifact-training.yml
│   │   └── concurrency-training.yml
│   │
│   └── actions/
│       │
│       ├── python-quality/
│       │   └── action.yml
│       │
│       ├── repository-validator/
│       │   ├── action.yml
│       │   ├── package.json
│       │   ├── package-lock.json
│       │   ├── src/
│       │   │   └── index.js
│       │   └── dist/
│       │       └── index.js
│       │
│       └── docker-validator/
│           ├── action.yml
│           ├── Dockerfile
│           └── entrypoint.sh
│
├── scripts/
│   └── github_actions_report.py
│
└── docs/
    └── github/
        └── module-04-actions/
            │
            ├── lesson-42-advanced-workflow-architecture.md
            │
            └── lesson-42/
                ├── reusable-workflows.md
                ├── workflow-inputs-outputs-secrets.md
                ├── composite-actions.md
                ├── javascript-custom-actions.md
                ├── docker-custom-actions.md
                ├── centralized-workflow-library.md
                ├── workflow-versioning.md
                ├── organization-workflow-governance.md
                ├── github-environments.md
                ├── deployment-approvals.md
                ├── concurrency-management.md
                ├── workflow-matrices.md
                ├── dynamic-matrices.md
                ├── conditional-execution.md
                ├── dependency-caching.md
                ├── artifact-management.md
                ├── workflow-performance.md
                ├── cross-repository-automation.md
                ├── github-actions-api.md
                ├── token-and-permission-design.md
                ├── django-react-reusable-cicd.md
                ├── multi-environment-deployment.md
                └── practical-exercises.md
```

You do not need to create every example immediately.

Build and validate the components incrementally.

### 27.2 Project milestones

| Milestone | Work | Expected result |
|---|---|---|
| M1 | Reusable workflows | Python and Node workflows can be called |
| M2 | Inputs, outputs, secrets | Workflow communication works |
| M3 | Composite Action | Repeated steps are packaged |
| M4 | JavaScript Action | Repository validator executes |
| M5 | Docker Action | Container-based Action executes |
| M6 | Workflow library | Centralized architecture documented |
| M7 | Versioning and governance | Shared automation has a release policy |
| M8 | Environments and approvals | Deployment protection is understood |
| M9 | Orchestration | Matrices, conditions, concurrency work |
| M10 | Caching and artifacts | Build outputs and dependencies are managed |
| M11 | Cross-repository automation | Events and API integration are understood |
| M12 | Final architecture | Django + React CI/CD design is documented |

---

## 28. Practical exercises

Complete these exercises in order.

### Exercise 1 — Create a reusable Python workflow

Create `reusable-python-tests.yml` using `workflow_call`.

Include:

- Python version input.
- Working directory input.
- Dependency installation.
- Ruff.
- Pytest.

### Exercise 2 — Create a caller workflow

Create a caller workflow that passes:

- Python version.
- Backend directory.
- Requirements file.

Verify that the reusable workflow executes.

### Exercise 3 — Return a workflow output

Create a reusable workflow that returns a build result.

Read the output from a dependent caller job.

### Exercise 4 — Pass a secret

Create a reusable deployment workflow.

Declare a required secret and pass it using explicit mapping.

Do not print the secret.

### Exercise 5 — Create a Python composite Action

Package:

- Python setup.
- Dependency installation.
- Ruff.
- Pytest.

Call it from a workflow.

### Exercise 6 — Create a JavaScript Action

Create the repository validator.

Check for:

- `README.md`
- `LICENSE`
- `CONTRIBUTING.md`
- `SECURITY.md`

### Exercise 7 — Build the JavaScript Action

Install dependencies.

Generate the `dist` directory.

Commit the generated bundle.

Verify that the Action works in GitHub Actions.

### Exercise 8 — Create a Docker custom Action

Create:

- `Dockerfile`
- `entrypoint.sh`
- `action.yml`

Run it on a Linux runner.

### Exercise 9 — Design a centralized workflow library

Document a repository named `github-workflow-library`.

Define:

- Repository structure.
- Workflow responsibilities.
- Action responsibilities.
- Consumer repositories.
- Access model.

### Exercise 10 — Create a versioning policy

Document:

- Major versions.
- Minor versions.
- Patch versions.
- Breaking changes.
- Release testing.
- Rollback strategy.

### Exercise 11 — Document organization governance

Write an organization Actions policy.

Include:

- Allowed Actions.
- Workflow permissions.
- Deployment permissions.
- Private workflow access.
- Workflow ownership.
- Release management.

### Exercise 12 — Create GitHub Environments

Create:

- Development.
- Staging.
- Production.

Review their available configuration options.

### Exercise 13 — Test manual environment selection

Create a `workflow_dispatch` workflow.

Select the environment and print the target.

### Exercise 14 — Configure deployment concurrency

Create a concurrency group for production deployment.

Test multiple workflow executions and document the behavior.

### Exercise 15 — Create a Python matrix

Test Python 3.12 and 3.13.

Inspect the generated jobs.

### Exercise 16 — Create a dynamic service matrix

Generate a JSON list containing:

- Backend.
- Frontend.
- Worker.

Use `fromJSON()` to create the matrix.

### Exercise 17 — Implement dependencies and conditions

Create:

- Backend tests.
- Frontend tests.
- Build job.
- Success report.
- Failure report.

### Exercise 18 — Configure dependency caching

Add pip caching.

Run the workflow twice.

Inspect cache behavior.

### Exercise 19 — Upload and download an artifact

Generate a test report.

Upload it from one job.

Download it in another job.

### Exercise 20 — Optimize workflow execution

Use parallel jobs, caching, and appropriate path filters.

Measure the actual workflow duration before and after.

### Exercise 21 — Study cross-repository events

Read about:

- `repository_dispatch`
- `workflow_dispatch`

Create a harmless event receiver.

### Exercise 22 — Read workflow runs through the REST API

Create a Python script that retrieves workflow runs.

Display:

- Workflow name.
- Status.
- Conclusion.

### Exercise 23 — Review least-privilege permissions

Review every workflow.

Document:

- Required permissions.
- Secrets used.
- Why each permission is needed.
- Whether it can be reduced.

### Exercise 24 — Design Django + React reusable CI/CD

Create an architecture using:

- Reusable Django CI.
- Reusable React CI.
- Security workflow.
- Docker build workflow.
- Release workflow.

### Exercise 25 — Document the complete deployment strategy

Design:

- Development deployment.
- Staging deployment.
- Production approval.
- Artifact promotion.
- Health checks.
- Rollback considerations.

---

## 29. Git workflow — commit, PR, tag, and release

Preserve your existing training repository conventions.

### Step 1 — Create a branch

```bash
git switch main
git pull origin main

git switch -c feat/lesson-42-reusable-workflows
```

### Step 2 — Create documentation and examples

Create the Lesson 42 documentation directory and the corresponding workflow and Action examples.

Do not commit real credentials, production configuration, or generated `node_modules` directories.

### Step 3 — Validate the repository

```bash
git status
git diff
git diff --check
```

For YAML validation, use a YAML linter or workflow validation tool.

Also test the workflows in GitHub Actions after pushing.

### Step 4 — Build the JavaScript Action

```powershell
cd .github/actions/repository-validator

npm install
npm run build

cd ../../..
```

Verify that:

```text
.github/actions/repository-validator/dist/index.js
```

exists.

### Step 5 — Commit documentation

```bash
git add docs/github/module-04-actions/

git commit -m "docs(actions): add reusable workflow architecture training"
```

### Step 6 — Commit workflow examples

```bash
git add .github/workflows/

git commit -m "feat(actions): add reusable workflow examples"
```

### Step 7 — Commit custom Actions

```bash
git add .github/actions/

git commit -m "feat(actions): add custom GitHub Actions examples"
```

If you created the API training script:

```bash
git add scripts/

git commit -m "feat(actions): add workflow API reporting script"
```

### Step 8 — Push the branch

```bash
git push -u origin feat/lesson-42-reusable-workflows
```

### Step 9 — Create the pull request

**PR title:**

```text
feat(actions): add advanced reusable workflow architecture
```

**PR description:**

```markdown
## Summary

Introduces Lesson 42 covering reusable GitHub Actions workflows,
custom Actions, centralized CI/CD architecture, and multi-environment
deployment design.

## Changes

- Added reusable workflow examples.
- Added workflow inputs, outputs, and secrets documentation.
- Added composite Action examples.
- Added JavaScript custom Action.
- Added Docker custom Action.
- Documented centralized workflow libraries.
- Added versioning and governance guidance.
- Added environment protection and deployment approval examples.
- Added concurrency and matrix examples.
- Added caching and artifact management.
- Added cross-repository automation.
- Documented GitHub Actions API integration.
- Designed reusable Django + React CI/CD architecture.

## Validation

- [ ] YAML files reviewed.
- [ ] Reusable workflows tested.
- [ ] Inputs and outputs verified.
- [ ] Composite Action tested.
- [ ] JavaScript Action built.
- [ ] Generated dist output committed.
- [ ] Docker Action reviewed.
- [ ] Permissions reviewed.
- [ ] No secrets committed.
- [ ] Documentation reviewed.

## Related Lessons

- Lesson 40 — GitHub Actions Security
- Lesson 41 — Advanced Security Automation & Compliance
```

### Step 10 — Review and merge

Before merging:

- Review workflow files.
- Review Action metadata.
- Check generated JavaScript output.
- Check permissions.
- Confirm no secrets are committed.
- Confirm the examples are clearly identified as training examples.

### Step 11 — Create a lesson tag

After merging:

```bash
git switch main
git pull origin main

git tag -a module-04-lesson-42 \
  -m "Module 4 Lesson 42: Advanced GitHub Actions Architecture"

git push origin module-04-lesson-42
```

### Step 12 — Create a GitHub Release

| Field | Value |
|---|---|
| Tag | `module-04-lesson-42` |
| Title | Module 4 — Lesson 42: Advanced GitHub Actions Architecture |
| Description | Reusable workflows, composite Actions, custom Actions, workflow governance, orchestration, and scalable CI/CD architecture. |

---

## 30. Completion checklist

### Reusable workflows

- [ ] I understand `workflow_call`.
- [ ] I created a reusable Python workflow.
- [ ] I created a caller workflow.
- [ ] I passed workflow inputs.
- [ ] I returned a workflow output.
- [ ] I passed a secret explicitly.
- [ ] I understand nested reusable workflows.

### Custom Actions

- [ ] I understand composite Actions.
- [ ] I created a Python composite Action.
- [ ] I created a JavaScript Action.
- [ ] I built and committed its `dist` output.
- [ ] I created a Docker Action.
- [ ] I understand when to use each Action type.

### Centralized automation

- [ ] I designed a centralized workflow repository.
- [ ] I documented workflow responsibilities.
- [ ] I documented semantic versioning.
- [ ] I understand version tags and commit SHA references.
- [ ] I documented organization-level governance.

### Deployment architecture

- [ ] I created development, staging, and production environments.
- [ ] I understand environment protection rules.
- [ ] I tested a harmless deployment workflow.
- [ ] I understand deployment approvals.
- [ ] I configured concurrency.
- [ ] I understand artifact promotion.

### Workflow orchestration

- [ ] I created a static matrix.
- [ ] I created a dynamic matrix.
- [ ] I used `needs`.
- [ ] I used conditional execution.
- [ ] I configured dependency caching.
- [ ] I uploaded and downloaded artifacts.
- [ ] I measured workflow performance.

### APIs and security

- [ ] I studied `repository_dispatch`.
- [ ] I studied `workflow_dispatch`.
- [ ] I retrieved workflow runs through the REST API.
- [ ] I reviewed token permissions.
- [ ] I reviewed secret handling.
- [ ] I understand least-privilege workflow design.

### Final project

- [ ] I designed reusable Django CI.
- [ ] I designed reusable React CI.
- [ ] I designed centralized security automation.
- [ ] I designed multi-environment deployment.
- [ ] I documented the complete architecture.
- [ ] I created a pull request.
- [ ] I merged the lesson.
- [ ] I created the lesson tag.
- [ ] I published the GitHub Release.

---

## 31. Official documentation

Use official documentation as the primary reference when implementing these features.

| Subject | Documentation |
|---|---|
| Reusable workflows | [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) |
| Reusable workflow configuration | [Reusing workflow configurations](https://docs.github.com/en/actions/reference/workflows-and-actions/reusing-workflow-configurations) |
| Sharing workflows with an organization | [Share with your organization](https://docs.github.com/en/actions/how-tos/reuse-automations/share-with-your-organization) |
| Sharing private workflows | [Share across private repositories](https://docs.github.com/en/actions/how-tos/reuse-automations/share-across-private-repositories) |
| Composite Actions | [Create a composite Action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action) |
| Custom Actions | [Custom Actions](https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions) |
| JavaScript Actions | [Create a JavaScript Action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-javascript-action) |
| Action metadata | [Metadata syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax) |
| Workflow syntax | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| GitHub Environments | [Manage environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments) |
| Workflow concurrency | [Control workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency) |
| Workflow artifacts | [Download workflow artifacts](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts) |
| Dependency caching | [Cache dependencies](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/caching-dependencies-to-speed-up-workflows) |
| GitHub Actions security | [Security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions) |
| GitHub Actions REST API | [REST API](https://docs.github.com/en/rest/actions) |

---

## 32. Next lesson — Lesson 43

### Module 4 — GitHub Actions & DevSecOps

### GitHub Actions — Advanced Deployment, Docker, Containers & Release Engineering

**Level:** Advanced
**Focus:** Real-world CI/CD engineering

Lesson 42 taught you how to build reusable automation.

Lesson 43 will focus on turning that automation into a complete application delivery system.

### Planned curriculum

| # | Topic |
|---:|---|
| 1 | Advanced Docker builds |
| 2 | Multi-stage Dockerfiles |
| 3 | Docker BuildKit |
| 4 | Docker Buildx |
| 5 | GitHub Container Registry (GHCR) |
| 6 | Image tagging strategies |
| 7 | Image digest management |
| 8 | Docker layer caching |
| 9 | Multi-platform builds |
| 10 | Container vulnerability scanning |
| 11 | SBOM generation |
| 12 | Image signing |
| 13 | Image provenance |
| 14 | Deployment automation |
| 15 | SSH-based deployments |
| 16 | Self-hosted deployment runners |
| 17 | Docker Compose deployments |
| 18 | Kubernetes deployment workflows |
| 19 | Helm chart deployments |
| 20 | Blue-green deployments |
| 21 | Canary deployments |
| 22 | Rollback automation |
| 23 | Database migrations during deployment |
| 24 | Deployment health checks |
| 25 | Complete Django + React production pipeline |

### Expected practical outcome

Build a container-based CI/CD pipeline that:

1. Builds applications.
2. Runs tests.
3. Scans dependencies and container images.
4. Publishes images to GHCR.
5. Generates SBOM and provenance information.
6. Deploys applications through controlled environments.
7. Validates deployments.
8. Supports rollback planning.

The final project will bring together your studies of Django REST Framework, React, Docker, PostgreSQL, Nginx, GitHub Actions, Trivy, Kubernetes, and deployment automation.

**Milestone:** Complete the Lesson 42 examples, especially the reusable Python workflow, composite Action, and JavaScript custom Action. Then move to Lesson 43.

# Module 4 — GitHub Actions & CI/CD

## Lesson 38 — Reusable Workflows, Composite Actions & Internal Automation Platforms

**Level:** Advanced
**Focus:** Practical engineering
**Estimated time:** 4–6 hours

---

## 1. Lesson overview

In Lesson 37, we studied GitHub Actions runners: the infrastructure responsible for executing workflows.

Now we move from runner infrastructure to **reusable automation architecture**.

As software companies grow, they often maintain multiple repositories:

- Django REST Framework backends.
- React frontend applications.
- React Native mobile applications.
- Shared Python packages.
- Docker infrastructure.
- Internal tools and services.

Each repository may need similar automation:

- Linting and formatting.
- Automated tests.
- Security scanning.
- Docker builds.
- Release creation.
- Deployment.
- Dependency management.

Duplicating the same workflow YAML across many repositories creates maintenance problems.

Imagine maintaining 20 repositories. If you need to update your security scanning workflow, would you rather modify 20 separate files or update one shared implementation?

That is the problem this lesson addresses.

### Learning objectives

By the end of this lesson, you should understand:

1. Reusable workflows versus composite Actions.
2. The `workflow_call` trigger.
3. Inputs, outputs, and secrets.
4. Calling workflows from other repositories.
5. Composite Actions and `action.yml`.
6. JavaScript Actions and Docker Actions.
7. Creating and versioning custom Actions.
8. Sharing automation across repositories.
9. GitHub Actions workflow templates.
10. Organization-wide CI/CD standards.
11. Centralized security and quality gates.
12. Building a reusable DRF + React CI platform.
13. Designing reusable release workflows.
14. Testing and debugging reusable automation.
15. Security considerations for internal automation platforms.

### Where this lesson fits

1. **Lesson 37 — Runner infrastructure:** Where workflows execute.
2. **Lesson 38 — Reusable automation:** How workflows and Actions are shared.
3. **Lesson 39 — Advanced workflow orchestration:** How multiple jobs, environments, and pipelines coordinate.

---

## 2. Understanding the three automation approaches

Before writing code, distinguish three important concepts.

| Feature | Reusable workflow | Composite Action | JavaScript/Docker Action |
|---|---|---|---|
| Main purpose | Reuse complete jobs and workflow logic | Reuse groups of steps | Package custom execution logic |
| Defined in | `.github/workflows/` | `action.yml` | `action.yml` |
| Can define jobs | Yes | No | No |
| Can contain multiple steps | Yes | Yes | Implemented by its runtime |
| Can be shared across repositories | Yes | Yes | Yes |
| Main interface | Workflow inputs, outputs, secrets | Action inputs and outputs | Action inputs and outputs |
| Typical use | Standard Python CI pipeline | Shared setup sequence | Specialized validation or API automation |

### 2.1 Reusable workflow

A reusable workflow is a complete workflow that another workflow calls.

Example:

```text
Application repository
        |
        v
    ci.yml
        |
        v
  calls workflow
        |
        v
Automation repository
        |
        v
reusable-python-ci.yml
        |
        +---- Install Python
        +---- Install dependencies
        +---- Run Ruff
        +---- Run tests
```

It can contain:

- Multiple jobs.
- Job dependencies.
- Permissions.
- Runner selection.
- Workflow inputs and outputs.
- Conditional execution.
- Matrix strategies.

### 2.2 Composite Action

A composite Action packages multiple steps into one reusable Action.

Example:

```text
Application workflow
        |
        v
uses: ./ .github/actions/setup-project
        |
        v
Composite Action
        |
        +---- Set up Python
        +---- Install dependencies
        +---- Display environment
```

A composite Action is useful when you want to reuse a sequence of steps inside jobs.

It does not create its own jobs or select its own runner.

### 2.3 JavaScript or Docker Action

These are custom Actions implemented using JavaScript or a Docker-based execution environment.

For example, you could create an Action that:

- Validates semantic version numbers.
- Checks repository standards.
- Generates a project metadata report.
- Validates deployment configuration.
- Interacts with the GitHub API.

They are useful when a reusable sequence of YAML steps is not enough.

**The key distinction:**

- Reusable workflows reuse jobs and workflow logic.
- Composite Actions reuse steps.
- JavaScript and Docker Actions package custom execution logic.

---

## 3. Reusable workflows in depth

Let's start with reusable workflows because they are the foundation of centralized CI/CD.

### 3.1 The problem: duplicated workflows

Imagine three repositories:

```text
nexaitek/
│
├── restaurant-backend/
│   └── .github/workflows/ci.yml
│
├── pharmacy-backend/
│   └── .github/workflows/ci.yml
│
└── appointment-backend/
    └── .github/workflows/ci.yml
```

All three repositories need:

1. Python installation.
2. Dependency installation.
3. Ruff linting.
4. Django tests.

Without reusable workflows, you might duplicate the same YAML in every repository.

This creates several problems:

- Updating one workflow requires updating multiple repositories.
- Different repositories can accidentally use different standards.
- Security fixes may not be applied consistently.
- Maintenance becomes more expensive.

### 3.2 The solution

Create a reusable workflow and let other workflows call it.

```text
nexaitek/
│
├── github-automation/
│   └── .github/workflows/
│       └── python-ci.yml
│
├── restaurant-backend/
│   └── .github/workflows/
│       └── ci.yml
│
├── pharmacy-backend/
│   └── .github/workflows/
│       └── ci.yml
│
└── appointment-backend/
    └── .github/workflows/
        └── ci.yml
```

The application repositories call the shared workflow.

The shared repository maintains the implementation. Each application repository maintains its own caller configuration.

### 3.3 The `workflow_call` trigger

A reusable workflow must declare `workflow_call`.

Create:

`.github/workflows/reusable-python-ci.yml`

```yaml
name: Reusable Python CI

on:
  workflow_call:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Display Python version
        run: python --version
```

The important part is:

```yaml
on:
  workflow_call:
```

This makes the workflow callable by another workflow.

A reusable workflow must be stored directly inside `.github/workflows/`. You cannot place a reusable workflow file in a subdirectory under that directory.

**Version note:** The Action versions in this lesson are illustrative examples. Before implementing them, check their official release pages. For production, pin third-party Actions to verified full commit SHAs.

---

## 4. Inputs in reusable workflows

A reusable workflow becomes much more powerful when callers can provide configuration.

For example, different Django applications might use different Python versions.

### 4.1 Define an input

Update `reusable-python-ci.yml`:

```yaml
name: Reusable Python CI

on:
  workflow_call:
    inputs:
      python-version:
        description: Python version
        required: false
        type: string
        default: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}

      - name: Display Python version
        run: python --version
```

We introduced:

```yaml
inputs:
  python-version:
    required: false
    type: string
    default: "3.12"
```

We access the input using:

```yaml
${{ inputs.python-version }}
```

### 4.2 Input types

Reusable workflow inputs support three types:

| Type | Example | Purpose |
|---|---|---|
| `string` | `"3.12"` | Text configuration |
| `boolean` | `true` | Enable or disable behavior |
| `number` | `15` | Numeric configuration |

### 4.3 Multiple inputs

Consider a reusable workflow for different application environments:

```yaml
on:
  workflow_call:
    inputs:
      python-version:
        type: string
        required: false
        default: "3.12"

      run-security-scan:
        type: boolean
        required: false
        default: true

      test-timeout:
        type: number
        required: false
        default: 15
```

You can use the values in jobs and steps.

For example:

```yaml
timeout-minutes: ${{ inputs.test-timeout }}
```

For optional security scanning:

```yaml
- name: Security scan
  if: ${{ inputs.run-security-scan }}
  run: echo "Run security scanning"
```

### 4.4 `workflow_call` versus `workflow_dispatch`

These are separate input systems:

- `workflow_call.inputs`: Inputs supplied by another workflow.
- `workflow_dispatch.inputs`: Inputs supplied when a user manually runs a workflow.

A workflow can support both triggers, but their input declarations are separate.

---

## 5. Calling reusable workflows

Now let's create the caller.

Suppose you have:

- `.github/workflows/reusable-python-ci.yml`
- `.github/workflows/python-ci-caller.yml`

The caller looks like this:

```yaml
name: Application CI

on:
  push:
    branches: [main]

  pull_request:

  workflow_dispatch:

permissions:
  contents: read

jobs:
  python-ci:
    uses: ./.github/workflows/reusable-python-ci.yml
    with:
      python-version: "3.12"
```

Notice something important: the reusable workflow is called at the **job level**.

Correct:

```yaml
jobs:
  ci:
    uses: ./.github/workflows/reusable-python-ci.yml
```

Incorrect:

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/workflows/reusable-python-ci.yml
```

A reusable workflow replaces the calling job definition with the called workflow. You cannot append ordinary steps to that same calling job.

### 5.1 Calling a workflow from another repository

Suppose you create:

`nexaitek/github-automation`

Its reusable workflow is:

`.github/workflows/python-ci.yml`

Another repository can call it:

```yaml
jobs:
  python-ci:
    uses: nexaitek/github-automation/.github/workflows/python-ci.yml@v1
    with:
      python-version: "3.12"
```

The general syntax is:

```text
OWNER/REPOSITORY/.github/workflows/FILE.yml@REF
```

Where:

- `OWNER`: GitHub user or organization.
- `REPOSITORY`: Repository containing the reusable workflow.
- `FILE.yml`: Reusable workflow filename.
- `REF`: Branch, tag, or commit reference.

For production, prefer a verified full commit SHA for the shared workflow reference. A tag such as `v1` is convenient, but can move if repository controls permit it.

---

## 6. Secrets in reusable workflows

Reusable workflows can receive secrets from their callers.

This matters when workflows interact with:

- Private package registries.
- Cloud providers.
- Deployment systems.
- External APIs.
- Private infrastructure.

### 6.1 Declare a secret

In the reusable workflow:

```yaml
name: Reusable Deployment

on:
  workflow_call:
    secrets:
      DEPLOYMENT_TOKEN:
        description: Deployment credential
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Deploy
        env:
          DEPLOYMENT_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
        run: |
          echo "Deployment placeholder"
          # Use the credential in the actual deployment command.
```

The example deliberately does not print or expose the token.

### 6.2 Pass the secret from the caller

```yaml
name: Deployment Caller

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    uses: nexaitek/github-automation/.github/workflows/deploy.yml@v1

    secrets:
      DEPLOYMENT_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
```

The caller obtains the secret from its own configured GitHub Actions secrets.

### 6.3 Passing multiple secrets

You can pass individual secrets:

```yaml
jobs:
  deploy:
    uses: nexaitek/github-automation/.github/workflows/deploy.yml@v1

    secrets:
      DEPLOYMENT_TOKEN: ${{ secrets.DEPLOYMENT_TOKEN }}
      API_TOKEN: ${{ secrets.API_TOKEN }}
```

Or use:

```yaml
secrets: inherit
```

This passes the caller's available secrets to the directly called workflow, subject to GitHub's access and secret-handling rules.

However, passing all secrets unnecessarily increases exposure.

**Best practice:** Explicitly pass only the secrets the called workflow needs.

### 6.4 Nested reusable workflows

Reusable workflows can call other reusable workflows.

Example:

```text
main-ci.yml
    |
    v
backend-ci.yml
    |
    +---- python-tests.yml
    |
    +---- security-scan.yml
```

GitHub supports nested reusable workflows, with a maximum of ten workflow levels including the top-level caller.

Important rules:

- Permissions can be maintained or reduced through the chain, not elevated.
- Secrets must be passed through each relevant level.
- A nested workflow should receive only the permissions and secrets it needs.

---

## 7. Outputs from reusable workflows

Sometimes a reusable workflow needs to return information to its caller.

Examples:

- Build version.
- Generated package version.
- Artifact identifier.
- Release information.

### 7.1 Define an output

```yaml
name: Reusable Build

on:
  workflow_call:
    outputs:
      build-version:
        description: Generated build version
        value: ${{ jobs.build.outputs.version }}

jobs:
  build:
    runs-on: ubuntu-latest

    outputs:
      version: ${{ steps.version.outputs.value }}

    steps:
      - name: Generate version
        id: version
        run: |
          echo "value=1.0.0" >> "$GITHUB_OUTPUT"
```

Notice the output chain:

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
Caller workflow
```

### 7.2 Read the output in the caller

```yaml
jobs:
  build:
    uses: ./.github/workflows/reusable-build.yml

  report:
    needs: build
    runs-on: ubuntu-latest

    steps:
      - name: Display version
        env:
          BUILD_VERSION: ${{ needs.build.outputs.build-version }}
        run: echo "Build version: $BUILD_VERSION"
```

The `needs` keyword establishes the dependency and makes the upstream job's outputs available.

---

## 8. Matrix strategies with reusable workflows

You can combine reusable workflows with matrix strategies.

Suppose you maintain applications that support multiple Python versions.

Instead of writing separate jobs:

```yaml
name: Python Compatibility

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        python-version:
          - "3.11"
          - "3.12"
          - "3.13"

    uses: ./.github/workflows/reusable-python-ci.yml

    with:
      python-version: ${{ matrix.python-version }}
```

Each matrix combination calls the reusable workflow separately.

This is useful for:

- Python compatibility.
- Node.js compatibility.
- Multiple application configurations.
- Different deployment targets.
- Different test environments.

Make sure your application and dependencies actually support every version in the matrix.

---

## 9. Composite Actions in depth

Now let's move to the second major concept.

A composite Action bundles several workflow steps into one reusable component.

### 9.1 Example problem

Imagine every repository needs to:

1. Display the operating system.
2. Display the architecture.
3. Display the repository name.
4. Display the current branch.

You could repeat these steps in every workflow.

Alternatively, create a composite Action:

```text
.github/
│
├── actions/
│   └── project-information/
│       └── action.yml
│
└── workflows/
    └── ci.yml
```

### 9.2 Create `action.yml`

File:

`.github/actions/project-information/action.yml`

```yaml
name: Project Information

description: Display useful GitHub Actions environment information

inputs:
  project-name:
    description: Project name
    required: true

outputs:
  runner-os:
    description: Runner operating system
    value: ${{ steps.info.outputs.runner-os }}

runs:
  using: composite
  steps:
    - name: Collect project information
      id: info
      shell: bash
      env:
        PROJECT_NAME: ${{ inputs.project-name }}
      run: |
        echo "Project: $PROJECT_NAME"
        echo "Operating system: $RUNNER_OS"
        echo "Architecture: $RUNNER_ARCH"
        echo "Repository: $GITHUB_REPOSITORY"

        echo "runner-os=$RUNNER_OS" >> "$GITHUB_OUTPUT"
```

Let's understand the structure:

| Property | Purpose |
|---|---|
| `name` | Action display name |
| `description` | Explains what the Action does |
| `inputs` | Defines accepted inputs |
| `outputs` | Defines returned values |
| `runs` | Describes execution configuration |
| `using: composite` | Declares a composite Action |
| `steps` | Contains reusable steps |
| `shell` | Declares the shell for each `run` step |

The metadata filename must be `action.yml` or `action.yaml`. `action.yml` is the common convention.

### 9.3 Call the composite Action

Create:

`.github/workflows/composite-action-training.yml`

```yaml
name: Composite Action Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  information:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Display project information
        id: project
        uses: ./.github/actions/project-information
        with:
          project-name: github-deep-dive-training

      - name: Read Action output
        env:
          RUNNER_OS_VALUE: ${{ steps.project.outputs.runner-os }}
        run: echo "Runner OS: $RUNNER_OS_VALUE"
```

Notice:

```yaml
uses: ./.github/actions/project-information
```

A local composite Action is called from inside a job's `steps`.

The repository must be checked out before the runner can access that local Action.

### 9.4 Composite Action inputs and outputs

A composite Action can accept multiple inputs:

```yaml
inputs:
  environment:
    description: Execution environment
    required: true

  project-name:
    description: Project name
    required: true

  debug:
    description: Enable additional output
    required: false
    default: "false"
```

Unlike reusable workflow inputs, composite Action metadata inputs are strings.

You can interpret values such as `"true"` and `"false"` inside your steps, but you should validate them before using them in conditional logic.

### 9.5 Composite Action limitations

Remember:

- It cannot define jobs.
- It executes within the caller's job.
- It cannot independently choose a runner using `runs-on`.
- It does not have a separate workflow-level secrets interface.
- Secrets can be passed to steps through supported inputs or environment variables, but avoid exposing them unnecessarily.
- A composite Action cannot independently create a workflow trigger.

---

## 10. JavaScript Actions

A JavaScript Action allows you to create reusable automation using JavaScript or TypeScript compiled to JavaScript.

This is useful when you need logic beyond a collection of shell commands.

Examples:

- Validate semantic version numbers.
- Parse GitHub events.
- Create structured reports.
- Interact with the GitHub API.
- Automate issue management.
- Validate release metadata.

### 10.1 Architecture

```text
.github/actions/version-validator/
│
├── action.yml
├── package.json
├── package-lock.json
└── dist/
    └── index.js
```

A JavaScript Action uses a Node.js runtime supported by GitHub Actions.

### 10.2 Example metadata

`action.yml`:

```yaml
name: Version Validator

description: Validate a semantic version string

inputs:
  version:
    description: Version to validate
    required: true

outputs:
  valid:
    description: Whether the version is valid
    value: ${{ steps.validate.outputs.valid }}

runs:
  using: node24
  main: dist/index.js
```

**Runtime note:** `node24` is an example of a runtime declaration, not a guarantee that every runtime is supported indefinitely. Check GitHub's current metadata documentation before publishing an Action.

### 10.3 JavaScript implementation

For a production implementation, use the GitHub Actions toolkit. This simplified example demonstrates the validation logic.

`src/index.js`:

```javascript
const version = process.env.INPUT_VERSION || "";

const semanticVersion =
  /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

if (!semanticVersion.test(version)) {
  console.error("Invalid version format.");
  process.exit(1);
}

console.log("Version format is valid.");
```

This is a simplified implementation. A production Action should:

- Read inputs using the appropriate Actions toolkit.
- Set outputs through the supported output mechanism.
- Handle errors clearly.
- Avoid logging secrets.
- Package its dependencies into the published distribution.
- Include tests.

### 10.4 Calling a JavaScript Action

```yaml
jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Validate version
        uses: ./.github/actions/version-validator
        with:
          version: "1.2.3"
```

---

## 11. Docker Actions

A Docker Action runs its logic inside a Docker container.

This can be useful when the Action requires:

- Specific system packages.
- A particular runtime.
- Specialized command-line tools.
- A controlled execution environment.

### 11.1 Architecture

```text
GitHub Actions runner
        |
        v
Docker runtime
        |
        v
Action container
        |
        v
Action logic
        |
        v
Result returned to workflow
```

### 11.2 Example structure

```text
.github/actions/example-docker-action/
│
├── action.yml
├── Dockerfile
└── entrypoint.sh
```

`action.yml`:

```yaml
name: Example Docker Action

description: Run a simple containerized task

runs:
  using: docker
  image: Dockerfile
```

`Dockerfile`:

```dockerfile
FROM alpine:3.21

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

`entrypoint.sh`:

```sh
#!/bin/sh

set -eu

echo "Running inside a Docker Action"
echo "Repository: ${GITHUB_REPOSITORY:-unknown}"
```

### 11.3 Calling the Docker Action

```yaml
jobs:
  example:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Docker Action
        uses: ./.github/actions/example-docker-action
```

Docker Actions have different runner requirements from composite and JavaScript Actions. They require a Linux environment with the necessary container support.

### 11.4 Comparing custom Action types

| Characteristic | Composite | JavaScript | Docker |
|---|---|---|---|
| Implementation | YAML steps | JavaScript | Container |
| Custom programming | Limited to step logic | Yes | Yes |
| Runtime | Runner shell | Node.js runtime | Container environment |
| Startup overhead | Usually low | Usually low | Container startup |
| Runner OS | Depends on step requirements | Supported runner environments | Linux |
| Best use | Reusable commands | API and logic automation | Specialized environments |

For your projects, start with composite Actions. They are usually easier to maintain for ordinary setup and validation tasks.

---

## 12. Creating a shared GitHub Actions repository

Now we move from individual reusable components to an actual automation platform.

Imagine creating a repository named:

`github-automation`

Its purpose is to provide shared automation for future projects.

### 12.1 Recommended architecture

```text
github-automation/
│
├── .github/
│   ├── workflows/
│   │   ├── reusable-python-ci.yml
│   │   ├── reusable-node-ci.yml
│   │   ├── reusable-docker-build.yml
│   │   ├── reusable-security.yml
│   │   └── reusable-release.yml
│   │
│   └── actions/
│       ├── setup-python/
│       │   └── action.yml
│       │
│       ├── setup-node/
│       │   └── action.yml
│       │
│       ├── project-information/
│       │   └── action.yml
│       │
│       └── validate-version/
│           └── action.yml
│
├── docs/
│   ├── architecture.md
│   ├── usage.md
│   ├── security.md
│   └── versioning.md
│
├── CONTRIBUTING.md
├── README.md
└── LICENSE
```

### 12.2 Responsibilities

| Component | Responsibility |
|---|---|
| `reusable-python-ci.yml` | Standard Python CI |
| `reusable-node-ci.yml` | Standard Node.js CI |
| `reusable-docker-build.yml` | Docker image builds |
| `reusable-security.yml` | Shared security checks |
| `reusable-release.yml` | Standard release process |
| `setup-python/` | Python environment setup |
| `setup-node/` | Node environment setup |
| `project-information/` | Environment reporting |
| `validate-version/` | Version validation |

### 12.3 Important architectural rule

Do not put everything into one enormous reusable workflow.

Separate components by responsibility.

For example:

```text
Application CI
    |
    +---- Python CI
    |
    +---- Node CI
    |
    +---- Security CI
    |
    +---- Docker Build
    |
    +---- Release
```

This makes the automation easier to test, maintain, and reuse.

---

## 13. Sharing automation across repositories

There are different ways to share automation.

### 13.1 Public repository

A public repository can provide reusable workflows and Actions to other repositories.

For example:

```yaml
jobs:
  python-ci:
    uses: nexaitek/github-automation/.github/workflows/reusable-python-ci.yml@v1
```

### 13.2 Private repository

You can also share reusable workflows and Actions from a private repository.

This is useful for internal company automation.

However, you must configure repository access.

A typical configuration process is:

1. Open the automation repository's **Settings**.
2. Open **Actions**.
3. Select **General**.
4. Find the access configuration for reusable workflows and Actions.
5. Allow only the intended repositories to access them.
6. Save the configuration.

The exact available controls depend on repository ownership and GitHub plan.

**Security consideration:** Making a private automation repository accessible to other repositories can have implications for workflow log visibility and information exposure. Review GitHub's private repository sharing rules before enabling access.

### 13.3 Organization-wide sharing

For a company with multiple repositories, an organization-owned automation repository is often a useful central location.

Example:

```text
Nexaitek Organization
│
├── github-automation
│
├── restaurant-backend
├── restaurant-frontend
├── pharmacy-backend
├── pharmacy-dashboard
└── medical-mobile-app
```

The central repository maintains reusable automation, while each application repository maintains its own caller workflows.

---

## 14. Versioning custom Actions and reusable workflows

This topic connects directly to the previous lessons about Git tags and releases.

Suppose you publish:

`nexaitek/github-automation`

You release:

```text
v1.0.0
v1.1.0
v1.2.0
v2.0.0
```

Other repositories can reference a specific release.

Example:

```yaml
jobs:
  python-ci:
    uses: nexaitek/github-automation/.github/workflows/reusable-python-ci.yml@v1
```

Here, `v1` represents a major-version reference that you maintain.

### 14.1 Semantic versioning

| Change | Example | Version |
|---|---|---|
| Initial release | First implementation | `v1.0.0` |
| Backward-compatible feature | New optional input | `v1.1.0` |
| Bug fix | Correct test handling | `v1.1.1` |
| Breaking change | Rename a required input | `v2.0.0` |

### 14.2 Why versioning matters

Imagine 15 repositories use your Python CI workflow.

You introduce a breaking change.

Without versioning, all 15 repositories might suddenly fail.

With versioning, they can continue using the previous major release until they are ready to migrate.

### 14.3 Branch, tag, and SHA references

| Reference | Characteristics |
|---|---|
| `@main` | Moves as the branch changes |
| `@v1` | Convenient major-version reference |
| `@v1.2.0` | Specific release tag |
| `@<full-commit-sha>` | Identifies an exact commit |

For production automation, use a verified full commit SHA where practical.

A tag is convenient, but it is not inherently immutable. Protect important tags and restrict who can modify release references.

### 14.4 Maintaining a major-version tag

A common release strategy is:

```text
v1.0.0
v1.1.0
v1.2.0
    |
    +---- v1 points to the latest approved v1 release
```

When releasing `v1.3.0`, update the `v1` major-version tag according to your release policy.

Do not automatically move a major-version tag before testing and approving the new release.

---

## 15. GitHub Actions workflow templates

Reusable workflows and workflow templates solve different problems.

A workflow template gives developers a starting workflow file when creating a new workflow in a repository.

A reusable workflow provides an implementation that the caller executes.

### 15.1 Workflow templates architecture

GitHub organizations can maintain a special repository named:

`.github`

Example:

```text
nexaitek/
│
├── .github/
│   └── workflow-templates/
│       ├── python-ci.yml
│       ├── python-ci.properties.json
│       ├── react-ci.yml
│       ├── react-ci.properties.json
│       ├── security.yml
│       └── security.properties.json
│
├── restaurant-backend/
├── restaurant-frontend/
└── pharmacy-backend/
```

### 15.2 Example template

`python-ci.yml`:

```yaml
name: Python CI

on:
  push:
    branches: [main]

  pull_request:

permissions:
  contents: read

jobs:
  python-ci:
    uses: nexaitek/github-automation/.github/workflows/reusable-python-ci.yml@v1
```

`python-ci.properties.json`:

```json
{
  "name": "Python CI",
  "description": "Standard Python CI workflow",
  "iconName": "python",
  "categories": [
    "Python",
    "Continuous integration"
  ]
}
```

The properties file describes the template in GitHub's workflow template interface.

### 15.3 Template versus reusable workflow

| Question | Workflow template | Reusable workflow |
|---|---|---|
| Gives developers a starting file? | Yes | No |
| Executes automation? | Only after being added to a workflow | Yes |
| Centralizes implementation? | Not by itself | Yes |
| Can be combined with reusable workflows? | Yes | Yes |

The most effective design is often to combine both:

1. A template provides a standard starting workflow.
2. That workflow calls centrally maintained reusable workflows.

---

## 16. Organization-wide CI/CD standards

Now let's look at how a company can establish consistent automation standards.

Imagine that Nexaitek has 15 application repositories.

You want all repositories to follow these standards:

| Standard | Expected behavior |
|---|---|
| Testing | Required automated tests |
| Linting | Standard linting checks |
| Security | Dependency and code security checks |
| Secrets | Secret detection |
| Releases | Consistent versioning |
| Dependencies | Automated update process |
| Permissions | Least privilege |
| Documentation | Standard repository documentation |
| Reviews | Pull request review requirements |
| Branch protection | Required checks before merging |

### 16.1 Centralized automation architecture

```text
Nexaitek engineering standards
Organization policies and approved automation
                |
                v
       Central automation repository
                |
       +--------+--------+
       |        |        |
       v        v        v
    Python    React   Security
      CI        CI       CI
       |        |        |
       +--------+--------+
                |
                v
        Application repositories
                |
       +--------+--------+
       |        |        |
       v        v        v
    Backend  Frontend  Mobile
```

### 16.2 Standardization versus flexibility

Centralization does not mean every application must have identical workflows.

For example:

- A Django API needs Python tests.
- A React application needs TypeScript checks.
- A React Native application needs mobile-specific checks.
- An infrastructure repository needs Terraform validation.

The shared platform should provide common standards while allowing appropriate project-specific configuration.

---

## 17. Security of reusable automation

Centralized automation can improve consistency, but it also creates a larger potential impact if compromised.

If 20 repositories use the same shared workflow, a vulnerability in that workflow could affect all 20.

### 17.1 Main security risks

| Risk | Explanation |
|---|---|
| Untrusted Actions | External code may execute with workflow permissions |
| Mutable references | A branch or tag can point to changed code |
| Excessive secrets | Workflows receive unnecessary credentials |
| Excessive permissions | Actions can modify more resources than required |
| Unsafe inputs | User-controlled data can become executable commands |
| Compromised shared workflow | Multiple repositories can be affected |
| Unreviewed updates | A central change can break many callers |

### 17.2 Security rules

#### Rule 1 — Least privilege

Declare permissions explicitly:

```yaml
permissions:
  contents: read
```

Only grant additional permissions when necessary.

#### Rule 2 — Pin dependencies

Use verified full commit SHAs for third-party Actions and reusable workflows where appropriate.

#### Rule 3 — Minimize secrets

Pass only the secrets needed by the called workflow.

#### Rule 4 — Review shared automation

A change to a central workflow should receive appropriate review and testing before it is released.

#### Rule 5 — Protect release references

Restrict who can modify important release tags and maintain a documented versioning policy.

#### Rule 6 — Avoid command injection

Do not interpolate untrusted inputs directly into shell commands.

Prefer passing data through environment variables:

```yaml
- name: Process input
  env:
    PROJECT_NAME: ${{ inputs.project-name }}
  run: |
    echo "Project: $PROJECT_NAME"
```

Environment variables reduce the risk associated with direct expression interpolation into shell source. They do not eliminate every injection risk: validate the data before using it in commands, paths, or other sensitive contexts.

#### Rule 7 — Separate untrusted CI from privileged release workflows

Do not execute untrusted pull request code in a privileged workflow with access to deployment credentials.

Keep release and deployment credentials out of ordinary pull request workflows.

### 17.3 Workflow dependency lockfiles

Another security feature worth learning is the GitHub Actions dependency lockfile.

It records exact commits for Actions used in workflows, helping make dependencies more predictable.

GitHub has documented tooling and workflows for generating and maintaining these lockfiles. Check the current official documentation for the supported commands and installation method before adopting a particular tool.

A lockfile does not replace:

- Reviewing third-party Actions.
- Pinning dependencies.
- Updating vulnerable dependencies.
- Restricting workflow permissions.
- Reviewing changes to shared automation.

---

## 18. Building a reusable DRF + React CI platform

Let's apply everything to your development stack.

### 18.1 Your technology stack

#### Backend

- Python.
- Django REST Framework.
- PostgreSQL.
- Redis.
- Celery.
- Django Channels.
- Ruff.
- Pytest.

#### Frontend

- React.
- Vite.
- TypeScript.
- TanStack Query.
- Zustand.
- Zod.
- ESLint.
- Vitest.

### 18.2 Shared repository

Create a future repository:

`github-automation`

It will contain:

```text
github-automation/
│
├── .github/
│   ├── workflows/
│   │   ├── reusable-django-ci.yml
│   │   ├── reusable-react-ci.yml
│   │   ├── reusable-security.yml
│   │   └── reusable-release.yml
│   │
│   └── actions/
│       ├── setup-python/
│       │   └── action.yml
│       ├── setup-node/
│       │   └── action.yml
│       └── validate-version/
│           └── action.yml
│
└── docs/
    ├── architecture.md
    ├── usage.md
    ├── security.md
    └── versioning.md
```

### 18.3 Example application repository

Your restaurant application might contain:

```text
restaurant-app/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   └── config/
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   └── src/
│
└── .github/
    └── workflows/
        └── ci.yml
```

### 18.4 Application caller workflow

`.github/workflows/ci.yml`:

```yaml
name: Restaurant Application CI

on:
  pull_request:

  push:
    branches: [main]

permissions:
  contents: read

jobs:
  backend:
    uses: nexaitek/github-automation/.github/workflows/reusable-django-ci.yml@v1
    with:
      python-version: "3.12"
      working-directory: backend

  frontend:
    uses: nexaitek/github-automation/.github/workflows/reusable-react-ci.yml@v1
    with:
      node-version: "22"
      working-directory: frontend

  security:
    needs: [backend, frontend]
    uses: nexaitek/github-automation/.github/workflows/reusable-security.yml@v1
```

This is an architectural example. The shared workflows and their input contracts must exist before this caller can run.

The called workflows must also be designed to work with the caller's repository context. For example, they must check out the application repository rather than accidentally checking out the automation repository.

### 18.5 Why this architecture is useful

Suppose you have:

- Restaurant application.
- Pharmacy application.
- Medical appointment application.
- Queue management application.

You can use the same shared workflows across them.

When you improve your standard Python CI, you maintain the central implementation and release a new version.

Application repositories can then upgrade at their own pace.

---

## 19. Practical exercises — your training repository

Now we will turn the theory into actual GitHub practice.

**Training repository:** `github-deep-dive-training`

We will build the exercises directly in this repository before creating a separate central automation repository.

Important distinction: your current training repository is primarily a documentation and GitHub-learning repository. These exercises introduce a small Python test fixture specifically for learning Actions. They do not represent the structure of your future DRF + React applications.

### Exercise 1 — Create a reusable workflow

Create:

`.github/workflows/reusable-python-ci.yml`

```yaml
name: Reusable Python CI

on:
  workflow_call:
    inputs:
      python-version:
        description: Python version
        required: false
        type: string
        default: "3.12"

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ inputs.python-version }}

      - name: Display Python version
        run: python --version

      - name: Run training tests
        run: python -m unittest discover -s tests -v
```

Create a simple test:

`tests/test_training.py`

```python
import unittest


class TrainingTests(unittest.TestCase):

    def test_github_actions_training(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
```

**Expected result:** The reusable workflow can be called and the training test passes.

### Exercise 2 — Create a caller workflow

Create:

`.github/workflows/python-ci-caller.yml`

```yaml
name: Python CI Caller

on:
  push:
    branches: [main]

  pull_request:

  workflow_dispatch:

permissions:
  contents: read

jobs:
  python-ci:
    uses: ./.github/workflows/reusable-python-ci.yml
    with:
      python-version: "3.12"
```

Run it manually using the Actions tab, then test it with a pull request and a push to `main`.

**Expected result:** The caller workflow invokes the reusable workflow and runs the Python test.

### Exercise 3 — Create a composite Action

Create:

`.github/actions/project-information/action.yml`

Use the composite Action from Section 9.

Then create:

`.github/workflows/composite-action-training.yml`

```yaml
name: Composite Action Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  information:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run project information Action
        id: info
        uses: ./.github/actions/project-information
        with:
          project-name: github-deep-dive-training

      - name: Display output
        env:
          RUNNER_OS_VALUE: ${{ steps.info.outputs.runner-os }}
        run: echo "Runner OS is $RUNNER_OS_VALUE"
```

**Expected result:** The workflow runs the composite Action and displays the runner operating system.

### Exercise 4 — Compare the two approaches

Create:

`docs/github/module-04-actions/reusable-workflows-vs-composite-actions.md`

Document:

1. Their architecture.
2. Their file structures.
3. How they are called.
4. How inputs work.
5. How outputs work.
6. How secrets are handled.
7. When to choose each.
8. Examples from your DRF + React projects.

### Exercise 5 — Design your automation platform

Create:

`docs/github/module-04-actions/internal-automation-platform.md`

Design a future `github-automation` repository.

Include:

- Shared workflow architecture.
- Composite Actions.
- Versioning strategy.
- Organization-wide access.
- Security policies.
- CI/CD standards.
- Documentation strategy.
- Maintenance responsibilities.

### Exercise 6 — Versioning exercise

Create a hypothetical release strategy:

```text
v1.0.0
v1.1.0
v1.1.1
v2.0.0
```

Explain which changes justify each version.

Do not publish a real shared automation repository yet. We will build and test the individual components first.

---

## 20. Repository implementation

Here is the complete structure I recommend creating for the practical exercises:

```text
github-deep-dive-training/
│
├── .github/
│   ├── actions/
│   │   └── project-information/
│   │       └── action.yml
│   │
│   └── workflows/
│       ├── reusable-python-ci.yml
│       ├── python-ci-caller.yml
│       └── composite-action-training.yml
│
├── tests/
│   └── test_training.py
│
└── docs/
    └── github/
        └── module-04-actions/
            ├── lesson-38-reusable-automation.md
            ├── reusable-workflows-vs-composite-actions.md
            ├── workflow-inputs-outputs-secrets.md
            ├── composite-actions.md
            ├── javascript-actions.md
            ├── docker-actions.md
            ├── internal-automation-platform.md
            ├── workflow-templates.md
            ├── automation-versioning.md
            └── automation-security.md
```

### Recommended content for each documentation file

| File | Content |
|---|---|
| `lesson-38-reusable-automation.md` | Complete lesson |
| `reusable-workflows-vs-composite-actions.md` | Architecture and differences |
| `workflow-inputs-outputs-secrets.md` | Parameters and communication |
| `composite-actions.md` | Creating and consuming composite Actions |
| `javascript-actions.md` | Custom JavaScript Actions |
| `docker-actions.md` | Docker-based Actions |
| `internal-automation-platform.md` | Centralized automation architecture |
| `workflow-templates.md` | Organization workflow templates |
| `automation-versioning.md` | Semantic versioning and releases |
| `automation-security.md` | Permissions, secrets, SHA pinning and supply-chain security |

### Suggested implementation order

Do not create all files at once.

Follow this order:

1. Create the main Lesson 38 document.
2. Create and test the reusable Python workflow.
3. Create and test its caller.
4. Create and test the composite Action.
5. Write the comparison document.
6. Design the future automation platform.
7. Document versioning and security.
8. Review the entire implementation before creating the PR.

This makes troubleshooting easier because each new component builds on a working previous component.

---

## 21. Git workflow — commit, PR, tag and release

Keep using your established branching and release conventions.

### Step 1 — Update your local main branch

In PowerShell:

```powershell
git status
git fetch origin
git switch main
git pull --ff-only origin main
```

If `git pull --ff-only` fails because the branches have diverged, stop and inspect the history before choosing a merge or rebase strategy. Do not force-push to solve the problem.

### Step 2 — Create a feature branch

```powershell
git switch -c feat/lesson-38-reusable-automation
```

### Step 3 — Check your changes

```powershell
git status
git diff
git diff --check
```

Validate your YAML files before pushing. You can use a YAML linter, and GitHub Actions will provide additional validation when the workflows execute.

### Step 4 — Stage specific files

Stage only the files you created or modified.

For example:

```powershell
git add .github/workflows/reusable-python-ci.yml
git add .github/workflows/python-ci-caller.yml
git add .github/workflows/composite-action-training.yml
git add .github/actions/project-information/action.yml
git add tests/test_training.py
git add docs/github/module-04-actions/lesson-38-reusable-automation.md
```

Add the other documentation files when you create them.

Then check the staged changes:

```powershell
git status
git diff --cached
git diff --cached --check
```

### Step 5 — Commit

```powershell
git commit -m "feat(actions): add reusable workflows and composite actions"
```

### Step 6 — Push

```powershell
git push -u origin feat/lesson-38-reusable-automation
```

### Step 7 — Create a pull request

Suggested title:

`feat(actions): add reusable automation training`

PR description:

```markdown
## Summary

Introduces Lesson 38 covering reusable GitHub Actions automation.

## Implemented

- Reusable Python CI workflow
- Workflow caller
- Composite project-information Action
- Training test
- Automation architecture documentation
- Workflow templates documentation
- Security and versioning documentation

## Validation

- [ ] YAML validation passed
- [ ] Reusable workflow executed successfully
- [ ] Composite Action executed successfully
- [ ] Outputs verified
- [ ] Documentation reviewed
- [ ] No secrets committed
```

### Step 8 — Review and merge

Before merging, check:

- Workflow files are valid.
- The reusable workflow is called at the job level.
- The composite Action is called from a step.
- The composite Action has been checked out before use.
- The test passes.
- No secrets or sensitive values were committed.
- The documentation matches the implementation.

After merging:

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
```

### Step 9 — Create the annotated tag

```powershell
git tag -a module-04-lesson-38 -m "Module 4 Lesson 38: Reusable Automation"
git push origin module-04-lesson-38
```

### Step 10 — Create the GitHub Release

| Field | Value |
|---|---|
| Tag | `module-04-lesson-38` |
| Release title | `Module 4 — Lesson 38: Reusable Automation` |
| Category | Training milestone |
| Notes | Reusable workflows, composite Actions, custom Actions, templates, and centralized automation |

Suggested release notes:

```markdown
# Module 4 — Lesson 38

Completed the deep dive into reusable GitHub Actions automation.

## Topics

- Reusable workflows and workflow_call
- Workflow inputs, outputs, and secrets
- Nested workflows and matrix strategies
- Composite Actions
- JavaScript and Docker Actions
- Shared automation repositories
- Workflow templates
- Semantic versioning
- Automation security

## Practical implementation

- Reusable Python CI workflow
- Workflow caller
- Composite project-information Action
- Automated training test
- Architecture documentation
```

---

## 22. Official documentation

Keep these references in your lesson notes.

| Subject | Official documentation |
|---|---|
| Reusing workflows | [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) |
| Workflow reuse concepts | [Reusing workflow configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations) |
| Workflow and Action metadata | [Metadata syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/metadata-syntax) |
| Composite Actions | [Creating a composite Action](https://docs.github.com/en/actions/tutorials/create-actions/create-a-composite-action) |
| Custom Actions | [About custom Actions](https://docs.github.com/en/actions/concepts/workflows-and-actions/custom-actions) |
| Organization sharing | [Sharing Actions and workflows with your organization](https://docs.github.com/en/actions/how-tos/reuse-automations/share-with-your-organization) |
| Private repository sharing | [Sharing Actions and workflows from a private repository](https://docs.github.com/en/actions/how-tos/reuse-automations/share-across-private-repositories) |
| Workflow templates | [Reusing workflow configurations](https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations) |
| Actions security | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| Workflow dependency lockfiles | [Workflow dependency lockfiles](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles) |

---

## 23. Lesson 38 completion checklist

### Lesson progress: 0/14

- [ ] Understand reusable workflows and `workflow_call`.
- [ ] Create `reusable-python-ci.yml`.
- [ ] Create and execute the caller workflow.
- [ ] Understand inputs, outputs, and secrets.
- [ ] Understand nested workflows and matrix strategies.
- [ ] Create the project-information composite Action.
- [ ] Execute and verify the composite Action.
- [ ] Understand JavaScript and Docker Actions.
- [ ] Design the `github-automation` repository.
- [ ] Understand workflow templates.
- [ ] Document semantic versioning.
- [ ] Complete the automation security review.
- [ ] Complete the DRF + React automation architecture.
- [ ] Create the PR, merge, tag, and release.

---

## 24. Next lesson — Lesson 39

**Level:** Advanced
**Focus:** CI/CD architecture

### GitHub Actions Advanced Workflow Orchestration & Enterprise Pipeline Design

Lesson 38 taught us how to create reusable automation components.

Lesson 39 will focus on connecting those components into sophisticated pipelines.

### Planned curriculum

| # | Topic |
|---:|---|
| 1 | Advanced job dependencies with `needs` |
| 2 | Conditional execution with `if` |
| 3 | Status functions: `success()`, `failure()`, `always()`, `cancelled()` |
| 4 | Dynamic matrices |
| 5 | Job outputs and cross-job communication |
| 6 | Artifacts and artifact management |
| 7 | Caching strategies and cache keys |
| 8 | Concurrency groups and cancellation |
| 9 | Workflow orchestration and fan-out/fan-in |
| 10 | Parallel versus sequential execution |
| 11 | Environment protection rules |
| 12 | Deployment approvals |
| 13 | Deployment environments |
| 14 | Reusable deployment pipelines |
| 15 | Multi-stage CI/CD |
| 16 | Monorepo workflow orchestration |
| 17 | Microservices CI/CD orchestration |
| 18 | Database migration pipelines |
| 19 | Blue-green and rolling deployment concepts |
| 20 | Release orchestration |
| 21 | Failure recovery and rollback planning |
| 22 | Build a complete enterprise-style DRF + React pipeline |

**Practical outcome:** By the end of Lesson 39, you will understand how to coordinate multiple jobs, repositories, environments, and deployment stages into a maintainable CI/CD platform.

We will maintain the same lesson format: theory, architecture diagrams, practical YAML examples, hands-on exercises, documentation filenames, commit conventions, PR practice, annotated tags, releases, and the next lesson preview.

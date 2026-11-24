# Module 4 — GitHub Actions & CI/CD

## Lesson 37 — GitHub Actions Runners, Self-Hosted Infrastructure & Enterprise Automation

**Level:** Advanced
**Focus:** Practical infrastructure
**Estimated time:** 4–6 hours
**Previous lesson:** Lesson 36 — Advanced CI/CD Security, Quality Gates & Software Supply Chain Security
**Next lesson:** Lesson 38 — GitHub Actions Reusable Workflows, Composite Actions & Internal Automation Platforms

---

## 1. Lesson Overview

In Lesson 35, we explored advanced GitHub Actions workflow design. In Lesson 36, we added security and quality controls to CI/CD pipelines.

Now we will study the infrastructure that actually executes those workflows: **GitHub Actions runners**.

A workflow defines *what* should happen. A runner provides the machine and execution environment where each job happens.

For example, your future Django REST Framework + React application might need to:

1. Install Python dependencies.
2. Install Node.js dependencies.
3. Start PostgreSQL for integration tests.
4. Run Django tests and migrations.
5. Run React tests and build the frontend.
6. Execute security scans.
7. Build Docker images.
8. Publish build artifacts.

All these tasks execute on runners.

## Learning objectives

By the end of this lesson, you should understand:

- GitHub-hosted versus self-hosted runners.
- Runner architecture and lifecycle.
- Runner registration and configuration.
- Runner labels and groups.
- Linux, Windows, and macOS environments.
- Persistent versus ephemeral runners.
- Docker-based runner architectures.
- Runner isolation and security.
- Networking and private infrastructure access.
- Autoscaling and Actions Runner Controller (ARC).
- Kubernetes-based runner infrastructure.
- Monitoring, troubleshooting, and cost optimization.
- How to design a runner strategy for a DRF + React application.

## Important recommendation for your training repository

For `github-deep-dive-training`, continue using GitHub-hosted runners.

You do not need to purchase or maintain a server just to learn runner concepts.

We will first understand self-hosted runners conceptually, then build a controlled local practice exercise using GitHub-hosted infrastructure.

---

## 2. Runner Fundamentals

## 2.1 What is a GitHub Actions runner?

A runner is a machine or execution environment that runs a GitHub Actions job.

Consider this workflow:

```yaml
name: Training CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Show environment
        run: |
          echo "Hello from GitHub Actions"
          python --version
          node --version
```

The important line is:

```yaml
runs-on: ubuntu-latest
```

It tells GitHub Actions which runner environment should execute the job.

The runner:

1. Receives an assigned job.
2. Prepares the workspace.
3. Executes the workflow steps.
4. Collects job results.
5. Reports the result to GitHub.

The action references above are illustrative. Before using an action in production, verify its current release and pin it to a trusted full commit SHA.

## 2.2 Workflow architecture

```text
Developer
   |
   v
GitHub repository
   |
   | Push / Pull Request / Schedule / Manual trigger
   v
GitHub Actions service
   |
   | Reads workflow YAML
   | Schedules jobs
   v
Runner allocation
   |
   +---------------------+
   |                     |
   v                     v
Runner A              Runner B
Ubuntu                Ubuntu
Backend tests         Frontend tests
   |                     |
   +----------+----------+
              |
              v
       GitHub Actions
              |
              v
     Workflow result
```

A workflow can contain multiple jobs. Each job is assigned to a runner that matches its `runs-on` configuration.

Jobs can execute sequentially or in parallel, depending on their dependencies.

## 2.3 Workflow versus job versus step versus runner

| Concept | Responsibility |
|---|---|
| Workflow | Defines the automation process |
| Job | Defines a group of steps |
| Step | Runs a command or action |
| Runner | Executes a job |
| Action | Reusable automation component |
| Artifact | File produced or transferred by a workflow |

A runner is not the same thing as an Action.

An Action is a reusable automation component. A runner is the execution environment.

## 2.4 One job versus multiple jobs

Consider:

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
```

GitHub schedules two jobs independently. They may run on separate runner instances.

Do not assume that two jobs share the same filesystem.

If one job generates a file that another job needs, transfer it using workflow artifacts or another explicitly configured storage mechanism.

---

## 3. GitHub-Hosted Runners

GitHub-hosted runners are execution environments managed by GitHub.

You select an available runner image in your workflow, and GitHub provisions the environment.

## 3.1 Example

```yaml
jobs:
  backend:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

The workflow does not require you to create a server, install the runner application, or manage its operating system.

GitHub manages the underlying hosted runner infrastructure.

## 3.2 Common runner operating systems

| Runner label | Environment |
|---|---|
| `ubuntu-latest` | Latest supported Ubuntu image |
| `ubuntu-24.04` | Ubuntu 24.04 |
| `windows-latest` | Latest supported Windows image |
| `macos-latest` | Latest supported macOS image |

The `-latest` labels can change as GitHub updates its runner images.

For reproducible builds:

- Select an appropriate supported image.
- Specify application runtime versions explicitly.
- Avoid relying on undocumented preinstalled software.
- Keep track of runner image changes.

The exact available images and hardware specifications can change, so consult GitHub's current runner image documentation.

## 3.3 Advantages

- No server administration.
- No runner registration.
- No operating system maintenance.
- Managed execution environments.
- Convenient parallel execution.
- Suitable for most ordinary CI pipelines.

## 3.4 Limitations

- Less control over the underlying machine.
- No automatic access to your private local network.
- Limited control over hardware and operating system configuration.
- Usage and concurrency depend on your GitHub plan and runner type.

## 3.5 When should you use GitHub-hosted runners?

For ordinary testing, linting, security scanning, and building a DRF + React application, they are usually the best starting point.

You should consider self-hosting only when you have a concrete requirement that hosted runners cannot reasonably satisfy.

---

## 4. Self-Hosted Runners

A self-hosted runner is a machine that you manage and connect to GitHub Actions.

It can be:

- A Linux server.
- A Windows machine.
- A macOS machine.
- A virtual machine.
- A dedicated machine in your office or data center.
- A containerized runner environment.

## 4.1 Basic example

```yaml
jobs:
  backend:
    runs-on: self-hosted

    steps:
      - uses: actions/checkout@v4

      - name: Show machine information
        run: |
          hostname
          python --version
```

This example assumes that a compatible self-hosted runner is registered, online, and available to the repository.

Unlike GitHub-hosted runners, the machine belongs to your infrastructure.

## 4.2 Architecture

```text
GitHub Actions service
          |
          | Runner communication
          |
          v
Your infrastructure
          |
          +------------------+
          |                  |
          v                  v
      Linux server      Windows machine
          |                  |
          v                  v
      Runner 1           Runner 2
```

You manage:

- Operating system updates.
- Runner software.
- Machine access.
- Credentials.
- Network access.
- Logs.
- Storage cleanup.
- Runner availability.
- Recovery procedures.

## 4.3 When self-hosted runners make sense

| Requirement | Why self-hosting may help |
|---|---|
| Private network access | Access to approved internal services |
| Specialized hardware | Custom hardware or device testing |
| Custom software | Preinstalled tools and dependencies |
| Large builds | Dedicated compute resources |
| Internal infrastructure | Controlled integration environments |
| Custom environments | Specific operating system configuration |

Self-hosting introduces operational responsibility.

**Security warning:** A runner executes workflow code. A compromised job can potentially compromise the machine and resources accessible to it. Persistent self-hosted runners are particularly risky when processing untrusted contributions.

Do not use a sensitive persistent runner as a general-purpose execution environment for arbitrary pull requests.

---

## 5. Runner Registration and Configuration

Let's understand the lifecycle before registering a real machine.

## 5.1 Registration process

At a high level, an administrator:

1. Opens repository or organization settings.
2. Navigates to Actions runner settings.
3. Selects the option to add a runner.
4. Chooses an operating system and architecture.
5. Downloads the runner application.
6. Configures the runner using the temporary registration instructions.
7. Starts the runner.
8. Confirms that GitHub displays it as online.

GitHub provides platform-specific installation and configuration instructions.

**Important:** Registration tokens are temporary credentials. Never publish them, commit them, or paste them into repository documentation.

## 5.2 Repository-level versus organization-level runners

| Scope | Who can use it? | Typical purpose |
|---|---|---|
| Repository | Configured repository | Small project |
| Organization | Approved repositories | Shared engineering infrastructure |
| Enterprise | Centrally governed infrastructure | Large organization |

Organization-level runner groups allow administrators to control which repositories can access a set of runners.

The exact management capabilities depend on the organization and enterprise plan.

## 5.3 Runner lifecycle

```text
Created
   |
   v
Configured
   |
   v
Connected
   |
   v
Idle
   |
   v
Job assigned
   |
   v
Executing
   |
   v
Job completed
   |
   v
Idle or removed
```

A runner must be connected and available to accept a job.

A runner that is offline cannot execute assigned work.

## 5.4 Runner service management

A self-hosted runner can be configured to run as a service, depending on the operating system and installation method.

This allows the runner process to start and recover according to the host's service-management configuration.

However, running the runner as a service does not make it secure by itself. The operating system account, file permissions, network access, and runner lifecycle still need to be managed.

---

## 6. Runner Labels

Labels describe runner capabilities and allow workflows to select a suitable runner.

A self-hosted runner commonly has labels such as:

- `self-hosted`
- `linux`
- `windows`
- `x64`

Administrators can also assign custom labels.

## 6.1 Example

Imagine an organization with:

- A Linux runner for backend tests.
- A Windows runner for Windows-specific tests.
- A dedicated runner for controlled integration tests.

```yaml
jobs:
  backend:
    runs-on: [self-hosted, linux, backend]

  windows-tests:
    runs-on: [self-hosted, windows, integration]
```

The labels must actually exist on the registered runners.

## 6.2 Why labels matter

Without labels, you have less control over which machine receives which job.

A label strategy makes runner allocation more understandable.

| Label | Meaning |
|---|---|
| `linux` | Linux environment |
| `backend` | Backend test environment |
| `frontend` | Frontend test environment |
| `integration` | Integration-test capability |
| `docker` | Docker tooling is available |

## 6.3 Label selection rules

When you specify multiple labels in an array, the runner must match all of them.

For example:

```yaml
runs-on: [self-hosted, linux, backend]
```

A runner must have the `self-hosted`, `linux`, and `backend` labels.

**Important:** Labels are scheduling selectors, not security boundaries. Use runner groups and access policies to control which repositories can use sensitive infrastructure.

---

## 7. Runner Groups and Access Control

Runner groups allow administrators to organize runners and restrict which repositories can use them.

Think of them as access-control boundaries around execution infrastructure.

## 7.1 Example organization

```text
Organization: Nexaitek
|
+-- Runner group: General CI
|   |
|   +-- Linux runners
|   +-- General testing
|   +-- Approved documentation repositories
|
+-- Runner group: Backend CI
|   |
|   +-- Backend integration runners
|   +-- Controlled test infrastructure
|
+-- Runner group: Deployment
    |
    +-- Restricted deployment runners
    +-- Approved deployment repositories
```

The purpose is not to create as many runner groups as possible.

The goal is to establish meaningful boundaries between different workloads and trust levels.

## 7.2 Selecting a runner group in YAML

For a self-hosted runner group, you can specify the group and labels:

```yaml
jobs:
  build:
    runs-on:
      group: general-ci
      labels: linux

    steps:
      - name: Build
        run: echo "Running on the general CI runner group"
```

This example assumes:

- The runner group is named `general-ci`.
- The group is accessible to the repository.
- A matching runner has the `linux` label.

The workflow does not create the group. An administrator must configure it first.

## 7.3 Practical exercise

In your training repository, write a Markdown document explaining:

- Repository-level runners.
- Organization-level runners.
- Runner groups.
- Runner labels.
- How access policies reduce the risk of unauthorized runner usage.

Do not create an organization just for this exercise.

---

## 8. Operating System Runners

Different operating systems are useful for different testing requirements.

## 8.1 Linux runners

Linux is commonly used for:

- Django applications.
- Python testing.
- React builds.
- Docker builds.
- PostgreSQL integration tests.
- Deployment automation.

Example:

```yaml
jobs:
  linux:
    runs-on: ubuntu-24.04

    steps:
      - uses: actions/checkout@v4

      - name: Inspect environment
        run: |
          uname -a
          python3 --version
          node --version
```

## 8.2 Windows runners

Windows runners are useful when your application has Windows-specific requirements.

Example:

```yaml
jobs:
  windows:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v4

      - name: Inspect environment
        shell: pwsh
        run: |
          Get-ComputerInfo |
            Select-Object WindowsProductName
```

## 8.3 macOS runners

macOS runners are useful for Apple-platform builds and macOS-specific tests.

Example:

```yaml
jobs:
  macos:
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v4

      - name: Inspect environment
        run: |
          sw_vers
          uname -a
```

## 8.4 Matrix testing across operating systems

A matrix allows one job definition to run across several environments.

```yaml
name: Operating System Matrix

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os:
          - ubuntu-24.04
          - windows-latest
          - macos-latest

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4

      - name: Display environment
        run: |
          echo "Runner OS: $RUNNER_OS"
          echo "Runner architecture: $RUNNER_ARCH"
```

On Windows, the default shell and environment differ from Linux and macOS.

For cross-platform scripts, explicitly choose the shell when appropriate.

### Exercise

Explain why testing on three operating systems is not always necessary for a Django + React application.

Identify which parts of your stack are genuinely platform-dependent.

---

## 9. Persistent and Ephemeral Runners

This is one of the most important architectural distinctions in this lesson.

## 9.1 Persistent runner

A persistent runner stays registered and available after completing a job.

```text
Runner starts
     |
     v
Job A executes
     |
     v
Job A completes
     |
     v
Same runner waits
     |
     v
Job B executes
```

Potential problems:

- Files can remain between jobs.
- Caches may contain unexpected state.
- Configuration changes can persist.
- A compromised machine may remain compromised.
- Different workloads may influence each other.

## 9.2 Ephemeral runner

An ephemeral runner is intended to execute one job and then be removed or discarded.

```text
Create runner
     |
     v
Assign one job
     |
     v
Execute job
     |
     v
Collect required logs/results
     |
     v
Destroy runner
```

This reduces persistent state and limits the impact of some compromises.

However, ephemeral does not automatically mean secure.

The machine image, network, credentials, provisioning process, and destruction process must also be controlled.

## 9.3 Comparison

| Property | Persistent | Ephemeral |
|---|---|---|
| Reuse between jobs | Yes | No |
| Cleanup | Administrator-managed | Usually automated |
| Startup overhead | Often lower | May be higher |
| Persistent-state risk | Higher | Lower |
| Infrastructure complexity | Often lower | Often higher |
| Isolation potential | Depends on design | Stronger when properly implemented |

## 9.4 When should you use each?

- A controlled internal project may use persistent runners if the security model permits it.
- A CI platform processing untrusted contributions should favor isolated, disposable execution environments.
- A deployment runner needs especially strict access control because it may have access to sensitive infrastructure.

---

## 10. Docker-Based Runner Architectures

Docker can help standardize execution environments.

However, there are several different designs, and they should not be confused.

## 10.1 Architecture A — GitHub-hosted runner with a job container

GitHub provisions the runner. Your job executes inside a specified container.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest

    container:
      image: python:3.12-slim

    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest

      - name: Run tests
        run: pytest
```

This standardizes the job's software environment without requiring you to maintain a self-hosted machine.

## 10.2 Architecture B — Self-hosted runner installed on a VM

```text
Physical server
    |
    v
Linux virtual machine
    |
    v
GitHub Actions runner
    |
    v
Job execution
```

The VM provides the host environment. Docker may also be installed on it.

## 10.3 Architecture C — Containerized self-hosted runners

```text
Linux host
    |
    v
Container runtime
    |
    +---- Runner container 1
    |
    +---- Runner container 2
    |
    +---- Runner container 3
```

This can make runner provisioning more repeatable, but containers are not a complete security boundary by themselves.

For example, mounting the host's Docker socket into a runner container can grant powerful access to the host.

**Design rule:** Do not assume that putting untrusted workflow code in a container makes it safe to expose host credentials, internal networks, or privileged container capabilities.

## 10.4 Important distinction

A job container is not necessarily a self-hosted runner.

You can use a job container on a GitHub-hosted runner.

Likewise, a self-hosted runner can execute jobs without using Docker at all.

---

## 11. Runner Security and Isolation

Runner security deserves its own design review.

A runner executes commands defined by workflow files. Those commands can run repository code, scripts, dependencies, and third-party Actions.

That makes a runner an important security boundary.

## 11.1 Main threats

| Threat | Potential impact |
|---|---|
| Untrusted pull request code | Executes unwanted commands |
| Exposed credentials | Unauthorized access |
| Persistent machine compromise | Later jobs may be affected |
| Excessive network access | Access to internal services |
| Excessive permissions | Repository or infrastructure changes |
| Untrusted third-party Action | Unexpected code execution |

## 11.2 Security principles

1. Use GitHub-hosted runners for ordinary public-repository CI.
2. Do not run untrusted pull-request code on sensitive persistent self-hosted runners.
3. Separate test runners from deployment runners.
4. Apply least-privilege `GITHUB_TOKEN` permissions.
5. Do not store unnecessary credentials on runner machines.
6. Keep runner operating systems and software updated.
7. Restrict network access.
8. Use ephemeral environments where appropriate.
9. Restrict which repositories and workflows can access runner groups.
10. Collect logs without exposing secrets.
11. Pin third-party Actions to verified full commit SHAs for production.
12. Avoid privileged execution of untrusted repository content.

## 11.3 A dangerous configuration to avoid

Do not use this as a general-purpose solution for public pull requests:

```yaml
on:
  pull_request_target:

jobs:
  test:
    runs-on: self-hosted
    steps:
      - name: Execute pull request code
        run: ./run-tests-from-pull-request.sh
```

`pull_request_target` runs in the context of the base repository and can have access to elevated permissions and secrets.

Checking out and executing untrusted pull-request code in that context can create a serious security vulnerability.

For normal pull-request testing, prefer the `pull_request` event with minimal permissions and an appropriately isolated runner.

## 11.4 Least-privilege permissions example

```yaml
name: Safe CI Example

on:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: echo "Run tests here"
```

This example uses GitHub-hosted infrastructure and grants only read access to repository contents.

The action reference is illustrative; production workflows should pin trusted actions to verified full commit SHAs.

## 11.5 Additional runner hardening

For a production runner environment, document:

- Which repositories can use the runner.
- Which workflows are trusted to execute there.
- Which operating system account runs the runner.
- Which directories are writable.
- Which network destinations are reachable.
- Which credentials are available.
- How logs are retained.
- How the machine is rebuilt after suspected compromise.

A runner should be treated as disposable infrastructure whenever its trust level or workload justifies that approach.

---

## 12. Runner Networking and Private Infrastructure

A major reason organizations adopt self-hosted runners is access to private systems.

Consider an internal development environment:

```text
                  GitHub
                    |
                    v
             Actions service
                    |
                    v
           Self-hosted runner
                    |
          Private network boundary
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
    Test DB     Internal API   Test service
```

A self-hosted runner may be able to access systems that GitHub-hosted runners cannot reach directly.

That capability also increases the risk if untrusted code executes on the runner.

## 12.1 Network design principles

- Allow only the network destinations required by the workflow.
- Separate CI networks from production networks.
- Do not give general CI jobs direct production database access.
- Use temporary test databases.
- Avoid storing long-lived network credentials on runners.
- Keep administrative interfaces inaccessible to ordinary CI jobs.
- Log network access where practical.
- Prefer temporary credentials and narrowly scoped access.

## 12.2 DRF + React example

Imagine your project uses:

```text
Django REST Framework
React + Vite
PostgreSQL
Redis
Docker Compose
Nginx
```

Your CI integration tests need PostgreSQL and Redis.

A GitHub-hosted runner can create temporary service containers for these dependencies. You usually do not need a self-hosted runner or access to your production network.

Example:

```yaml
name: Backend Integration Tests

on:
  pull_request:

permissions:
  contents: read

jobs:
  backend-tests:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U test_user"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt

      - name: Run tests
        env:
          DB_HOST: localhost
          DB_PORT: 5432
          DB_NAME: test_db
          DB_USER: test_user
          DB_PASSWORD: test_password
        run: |
          cd backend
          python manage.py test
```

This is a learning example.

In a real project:

- Align environment variable names with your Django settings.
- Use the correct dependency file.
- Do not use production credentials.
- Add Redis if your tests require it.
- Configure test migrations and database health checks appropriately.

The example assumes your future application repository actually has a `backend/requirements.txt` file.

---

## 13. Autoscaling Self-Hosted Runners

Autoscaling means adjusting the number of available runners based on workload demand.

Without autoscaling:

```text
One runner
    |
    +---- Job A
    |
    +---- Job B waits
    |
    +---- Job C waits
```

With autoscaling:

```text
Incoming jobs
    |
    v
Runner manager
    |
    +---- Runner 1 -> Job A
    |
    +---- Runner 2 -> Job B
    |
    +---- Runner 3 -> Job C
```

## 13.1 Why autoscaling matters

Suppose your organization receives:

- 2 pull requests in the morning.
- 15 pull requests in the afternoon.
- 30 builds during a release.

A fixed runner fleet may be underused during quiet periods and overloaded during peak periods.

Autoscaling attempts to match capacity to demand.

## 13.2 Scaling strategies

| Strategy | Description |
|---|---|
| Fixed capacity | Always maintain a fixed number of runners |
| Scheduled scaling | Adjust capacity based on expected workload |
| Queue-based scaling | Add runners when jobs are waiting |
| Minimum/maximum scaling | Keep capacity within configured boundaries |
| Scale to zero | Remove idle runners when no work remains |

Autoscaling introduces complexity:

- Machine provisioning.
- Cleanup.
- Authentication.
- Capacity planning.
- Failure recovery.
- Monitoring.
- Security of the provisioning system.

---

## 14. Actions Runner Controller (ARC)

### Important Kubernetes topic

Actions Runner Controller is a Kubernetes operator that manages and scales self-hosted GitHub Actions runners.

It is designed for organizations that already operate Kubernetes infrastructure and need dynamically managed runner capacity.

GitHub documents ARC as its Kubernetes-based solution for autoscaling self-hosted runners.

## 14.1 ARC architecture

```text
GitHub Actions service
          |
          | Job availability
          v
Kubernetes cluster
          |
          v
ARC controller
          |
          v
Runner scale set listener
          |
          +-------------------+
          |                   |
          v                   v
       Runner 1            Runner 2
          |
          v
       Job execution
```

The controller manages runner capacity. The listener coordinates job availability, and runner instances are created to execute jobs.

## 14.2 Runner scale sets

A runner scale set is a group of similar runners that can receive jobs.

For example:

```text
Runner scale set: django-ci

Minimum runners: 1
Maximum runners: 5

Incoming jobs:
    1 -> one runner
    2 -> two runners
    3 -> three runners
```

The exact scaling behavior depends on the configured minimum, maximum, and scaling settings.

## 14.3 Example workflow targeting an ARC runner

```yaml
jobs:
  test:
    runs-on: django-ci

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: echo "Testing on an ARC-managed runner"
```

`django-ci` must match the name of your configured runner scale set.

The workflow does not install ARC. ARC must already be deployed and configured in Kubernetes.

## 14.4 ARC security considerations

Important considerations include:

- Separating controller and runner workloads.
- Protecting Kubernetes secrets.
- Restricting Kubernetes service-account permissions.
- Avoiding unnecessary access to the Kubernetes API.
- Separating sensitive workloads.
- Restricting network access.
- Keeping runner images updated.
- Reviewing pod security settings.

Do not assume a shared Kubernetes cluster is automatically safe for executing arbitrary workflow code.

## 14.5 ARC versus traditional self-hosted runners

| Feature | Traditional runner | ARC |
|---|---|---|
| Management | Manual or custom automation | Kubernetes operator |
| Scaling | Often custom | Runner scale-set management |
| Runner lifecycle | Administrator-managed | Controller-managed |
| Infrastructure | VM or machine | Kubernetes |
| Complexity | Varies | High |
| Best fit | Smaller controlled environments | Kubernetes-capable organizations |

**Important distinction:** ARC is not simply a Docker image or a YAML Action. It is infrastructure that you deploy and operate.

---

## 15. Kubernetes-Based Runner Infrastructure

ARC introduces several Kubernetes concepts that you should understand.

| Kubernetes concept | Role in runner infrastructure |
|---|---|
| Cluster | Hosts runner infrastructure |
| Namespace | Separates controller and runner resources |
| Pod | Runs a runner instance |
| Container | Packages runner software and dependencies |
| Secret | Stores protected configuration |
| Service account | Defines Kubernetes API permissions |
| Helm | Installs and configures ARC |
| Autoscaling | Adjusts runner capacity |

## 15.1 Example namespace separation

```text
Kubernetes cluster
|
+-- arc-system
|   |
|   +-- ARC controller
|
+-- arc-runners
|   |
|   +-- runner-pod-1
|   +-- runner-pod-2
|   +-- runner-pod-3
|
+-- application-test
    |
    +-- temporary-postgres
    +-- temporary-redis
```

This is an illustrative architecture, not a complete Kubernetes deployment.

## 15.2 ARC deployment workflow

A real deployment involves:

1. Preparing a supported Kubernetes cluster.
2. Installing ARC using its Helm charts.
3. Configuring authentication to GitHub.
4. Creating a runner scale set.
5. Defining capacity limits.
6. Configuring workflow access.
7. Verifying that jobs are assigned correctly.
8. Setting up logs and monitoring.
9. Testing runner cleanup and failure recovery.

GitHub's current recommended installation approach uses ARC's Helm charts.

## 15.3 When should you learn ARC?

For your current GitHub training repository, understand its architecture and responsibilities, but do not deploy it yet.

A sensible learning sequence is:

1. Linux fundamentals.
2. Docker and Docker Compose.
3. GitHub Actions.
4. Kubernetes fundamentals.
5. Kubernetes security.
6. ARC installation and operation.

---

## 16. Runner Monitoring and Troubleshooting

A runner infrastructure needs observability just like an application.

You need to understand:

- Is the runner online?
- Is it accepting jobs?
- How long do jobs wait?
- How long do jobs execute?
- Are jobs failing because of infrastructure or application code?
- Is disk space running out?
- Is the runner running out of memory?
- Are runner processes crashing?
- Are jobs being cancelled?

## 16.1 Useful metrics

| Metric | Why it matters |
|---|---|
| Runner availability | Measures usable capacity |
| Queue wait time | Reveals insufficient capacity |
| Job duration | Identifies slow workflows |
| Job failure rate | Helps detect instability |
| CPU usage | Detects compute pressure |
| Memory usage | Detects memory pressure |
| Disk usage | Detects storage exhaustion |
| Runner startup time | Measures provisioning efficiency |

## 16.2 Common errors

| Problem | Possible cause | Investigation |
|---|---|---|
| Job stuck in queue | No matching runner | Check labels and online status |
| Runner offline | Machine or runner process stopped | Inspect runner service |
| Permission denied | Incorrect file permissions | Check user and file ownership |
| Disk full | Old workspaces or Docker images | Inspect storage and cleanup |
| Docker unavailable | Docker service not running | Inspect Docker daemon |
| Job unexpectedly slow | Resource contention | Inspect CPU, memory, and logs |
| Runner not selected | Wrong group or label | Compare YAML with runner configuration |
| ARC runner not starting | Kubernetes provisioning problem | Inspect pod and controller logs |

## 16.3 Useful Linux diagnostic commands

These commands inspect a Linux machine. They do not require you to install or register a GitHub runner.

```bash
# Operating system
uname -a

# CPU information
lscpu

# Memory
free -h

# Disk space
df -h

# Running processes
ps aux

# Filesystem usage
du -sh .

# Docker status
docker info

# Running containers
docker ps
```

## 16.4 Useful Kubernetes diagnostic commands

```bash
# Check namespaces
kubectl get namespaces

# Check pods
kubectl get pods -A

# Inspect a pod
kubectl describe pod <pod-name> -n <namespace>

# Read pod logs
kubectl logs <pod-name> -n <namespace>
```

These Kubernetes commands assume you already have an authorized cluster context.

## 16.5 Distinguishing infrastructure failures from application failures

A useful troubleshooting habit is to classify the failure before changing the workflow.

**Infrastructure failure examples:**

- Runner unavailable.
- Disk exhausted.
- Container runtime unavailable.
- Network connectivity failure.
- Runner image provisioning failure.

**Application failure examples:**

- Django tests fail.
- TypeScript compilation fails.
- Dependency installation fails because of an invalid package version.
- Docker build fails because of an application configuration error.

This distinction prevents you from trying to solve application bugs by changing runner infrastructure, or trying to solve infrastructure failures by changing application code.

---

## 17. Enterprise Runner Management

At enterprise scale, runners become a platform engineering responsibility.

An organization may have:

- Hundreds of repositories.
- Multiple engineering teams.
- Different operating systems.
- Different security classifications.
- Dedicated deployment environments.
- Different build requirements.
- Shared CI infrastructure.

## 17.1 Example enterprise model

```text
Enterprise
|
+-- Organization: Backend
|   |
|   +-- General CI runner group
|   +-- Backend integration runner group
|
+-- Organization: Frontend
|   |
|   +-- Frontend CI runner group
|
+-- Organization: Platform
    |
    +-- Infrastructure CI runner group
    +-- Deployment runner group
```

The purpose is not to create as many runner groups as possible.

The goal is to establish meaningful boundaries between different workloads and trust levels.

## 17.2 Governance checklist

- Define who can register runners.
- Restrict which repositories can use each group.
- Establish approved runner images.
- Patch runner hosts regularly.
- Separate production deployment infrastructure.
- Define retention and log collection policies.
- Monitor capacity and utilization.
- Document incident response.
- Review runner permissions periodically.
- Define a process for removing compromised or obsolete runners.

## 17.3 Platform engineering perspective

A mature organization treats runner infrastructure as an internal platform.

The platform team provides:

- Approved runner images.
- Standard labels and groups.
- Reusable runner configurations.
- Security policies.
- Monitoring.
- Capacity management.
- Documentation.
- Support and incident response.

Application teams consume this platform instead of independently maintaining their own CI infrastructure.

---

## 18. Cost Optimization

Runner cost is not just the cost of a machine.

It includes:

- Compute resources.
- Storage.
- Network traffic.
- Operating system maintenance.
- Administration time.
- Monitoring.
- Security controls.
- Idle capacity.
- Incident recovery.

## 18.1 Cost comparison

| Approach | Cost characteristics |
|---|---|
| GitHub-hosted | Managed infrastructure; usage subject to plan and limits |
| One persistent VM | Predictable infrastructure cost, including idle time |
| Multiple persistent VMs | Higher fixed capacity cost |
| Ephemeral VMs | Dynamic infrastructure cost plus provisioning overhead |
| ARC on Kubernetes | Cluster, storage, networking, and operational costs |

A self-hosted runner is not automatically cheaper than a GitHub-hosted runner.

Include maintenance and security operations in the comparison.

## 18.2 Practical optimization techniques

1. Avoid unnecessary matrix combinations.
2. Use dependency caching appropriately.
3. Cancel outdated workflow runs when safe.
4. Set reasonable job timeouts.
5. Avoid oversized runner machines.
6. Scale down unused self-hosted capacity.
7. Use separate runner pools for different workload requirements.
8. Monitor the actual cost of maintaining infrastructure.
9. Measure queue time before increasing capacity.
10. Avoid running expensive operating-system matrices when they provide no meaningful coverage.

---

## 19. Design a Runner Architecture for Your DRF + React Application

Now let's combine the concepts into a realistic design.

Your application architecture:

```text
Frontend:
    React
    Vite
    TypeScript

Backend:
    Django REST Framework
    PostgreSQL
    Redis
    Celery
    Channels

Infrastructure:
    Docker
    Docker Compose
    Nginx

Automation:
    GitHub Actions
    GitHub Releases
    Security scanning
```

## 19.1 Recommended CI architecture

```text
GitHub repository
       |
       v
Pull request or push
       |
       v
GitHub Actions
       |
       +-----------------------+
       |           |           |
       v           v           v
   Backend     Frontend     Security
    job          job          job
       |           |           |
       v           v           v
   Django       React       Gitleaks
   tests        tests       Dependency review
   PostgreSQL   Vite build   Trivy
       |           |           |
       +-----------+-----------+
                   |
                   v
             Build and release
                   |
                   v
        Protected deployment environment
```

## 19.2 Which runner should each job use?

| Job | Recommended runner |
|---|---|
| Django tests | GitHub-hosted Ubuntu |
| React tests | GitHub-hosted Ubuntu |
| PostgreSQL integration tests | GitHub-hosted Ubuntu with service container |
| Gitleaks | GitHub-hosted Ubuntu |
| Trivy filesystem scan | GitHub-hosted Ubuntu |
| Docker build | GitHub-hosted Ubuntu |
| Private internal integration | Isolated self-hosted runner, if necessary |
| Production deployment | Dedicated restricted deployment environment |

## 19.3 Why not start with self-hosted runners?

Your first objective should be a reliable pipeline, not maintaining runner infrastructure.

GitHub-hosted runners let you focus on application quality and workflow design.

Introduce self-hosted infrastructure only when a concrete requirement justifies the additional operational responsibility.

## 19.4 Three-environment runner design

For a larger application, consider these conceptual environments:

| Environment | Purpose | Security model |
|---|---|---|
| General CI | Linting, unit tests, builds | No production access |
| Private integration | Approved internal integration tests | Isolated network and restricted repositories |
| Deployment | Controlled release and deployment | Strong access control and protected environments |

Do not let general CI jobs inherit deployment credentials or unnecessary internal network access.

---

## 20. Practical Exercises

Complete these exercises in `github-deep-dive-training`.

The current repository is a training/documentation repository. Do not pretend it contains your future Django backend, React frontend, or Docker configuration.

Use GitHub-hosted runners for the practical workflow exercises.

## Level 1 — Understand runner configuration

Create:

`docs/github/module-04-actions/lesson-37-runner-fundamentals.md`

Document:

- What a runner is.
- Workflow versus job versus runner.
- GitHub-hosted runners.
- Self-hosted runners.
- Runner labels.
- Runner groups.
- Persistent versus ephemeral runners.

**Acceptance criteria:**

- Explain each concept in your own words.
- Include at least two architecture diagrams.
- Include one valid `runs-on` example.
- Explain why the current training repository does not need a self-hosted runner.

## Level 2 — Build an operating-system matrix

Create:

`.github/workflows/runner-matrix.yml`

Use this example:

```yaml
name: Runner Matrix Training

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    strategy:
      fail-fast: false
      matrix:
        os:
          - ubuntu-24.04
          - windows-latest
          - macos-latest

    runs-on: ${{ matrix.os }}

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Display runner information
        shell: bash
        run: |
          echo "Runner OS: $RUNNER_OS"
          echo "Runner architecture: $RUNNER_ARCH"
          echo "Runner name: $RUNNER_NAME"
```

The explicit `bash` shell makes the environment variables consistent across these runner operating systems.

**Acceptance criteria:**

- Manually run the workflow.
- Observe the three jobs.
- Compare their execution environments.
- Explain why execution times can differ.
- Identify the operating system associated with each job.

If a particular image is unavailable to your account or has changed, select a currently supported image from GitHub's runner documentation.

**Note:** Running all three operating systems may consume more hosted-runner usage than running only Ubuntu. Use the matrix as a deliberate learning exercise.

## Level 3 — Runner security review

Create:

`docs/github/module-04-actions/runner-security-review.md`

Use this checklist:

```markdown
# Runner Security Review

## Runner architecture
- [ ] GitHub-hosted or self-hosted is documented
- [ ] Runner purpose is documented
- [ ] Runner ownership is documented

## Access control
- [ ] Repository access is restricted
- [ ] Runner groups are reviewed
- [ ] Labels are documented
- [ ] Workflow permissions are minimized

## Isolation
- [ ] Untrusted pull requests cannot execute on sensitive runners
- [ ] Persistent runner risks are documented
- [ ] Ephemeral runner strategy is documented

## Network
- [ ] Required destinations are documented
- [ ] Production network access is restricted
- [ ] Secrets are not stored unnecessarily

## Monitoring
- [ ] Runner availability is monitored
- [ ] Logs are collected
- [ ] Disk usage is monitored
- [ ] Failure handling is documented
```

**Acceptance criteria:**

- Complete the checklist for your current training repository.
- Mark concepts that do not apply as `N/A` and explain why.
- Do not claim that unimplemented security controls are active.

## Level 4 — Architecture design

Create:

`docs/github/module-04-actions/runner-architecture-design.md`

Design three separate environments:

1. General CI.
2. Private integration testing.
3. Restricted deployment.

For each, explain:

- Runner type.
- Operating system.
- Labels.
- Access policy.
- Network access.
- Secrets policy.
- Cleanup strategy.
- Monitoring requirements.

Do not deploy this infrastructure yet. This is an architecture-design exercise.

## Level 5 — Runner operations and troubleshooting

Create:

`docs/github/module-04-actions/runner-operations.md`

Document:

- Runner lifecycle.
- Online versus offline state.
- Job queue waiting.
- Runner labels and matching.
- Disk and memory problems.
- Docker availability.
- Infrastructure versus application failures.
- Linux and Kubernetes diagnostic commands.

**Acceptance criteria:**

- Include at least six troubleshooting scenarios.
- For each scenario, identify a likely cause and investigation method.
- Explain which failures require administrator intervention.

## Level 6 — ARC and Kubernetes architecture

Create:

`docs/github/module-04-actions/arc-kubernetes-runners.md`

Document:

- What ARC does.
- Runner scale sets.
- ARC controller.
- Runner pods.
- Kubernetes namespaces.
- Helm installation concept.
- Runner scaling.
- Security boundaries.
- Monitoring responsibilities.

**Acceptance criteria:**

- Include an ARC architecture diagram.
- Explain why ARC is not necessary for your current training repository.
- Identify at least three operational responsibilities introduced by ARC.

---

## 21. Repository Documentation

Use this structure to keep Lesson 37 organized:

```text
github-deep-dive-training/
|
+-- .github/
|   |
|   +-- workflows/
|       |
|       +-- runner-matrix.yml
|
+-- docs/
    |
    +-- github/
        |
        +-- module-04-actions/
            |
            +-- lesson-37-runner-fundamentals.md
            +-- runner-architecture-design.md
            +-- runner-security-review.md
            +-- runner-operations.md
            +-- github-hosted-runners.md
            +-- self-hosted-runners.md
            +-- runner-groups-and-labels.md
            +-- ephemeral-runners.md
            +-- arc-kubernetes-runners.md
            +-- runner-monitoring.md
            +-- runner-cost-optimization.md
```

## Documentation content

| File | What to document |
|---|---|
| `lesson-37-runner-fundamentals.md` | Complete lesson notes and terminology |
| `runner-architecture-design.md` | Three-environment architecture |
| `runner-security-review.md` | Security checklist and findings |
| `runner-operations.md` | Lifecycle and troubleshooting |
| `github-hosted-runners.md` | Images, labels, limitations |
| `self-hosted-runners.md` | Installation, registration, maintenance |
| `runner-groups-and-labels.md` | Access control and job selection |
| `ephemeral-runners.md` | Lifecycle and isolation |
| `arc-kubernetes-runners.md` | ARC architecture and Kubernetes concepts |
| `runner-monitoring.md` | Metrics, diagnostics, troubleshooting |
| `runner-cost-optimization.md` | Capacity and cost considerations |

You do not need to create every supporting document immediately.

Start with the main lesson, the matrix workflow, the security review, and the architecture design. Add the remaining documents as you complete the corresponding exercises.

---

## 22. Git Workflow — Commit, PR, Tag, and Release

When you have completed the exercises and documentation, use your established Git workflow.

The following commands are written for PowerShell.

## Step 1 — Check your working tree

```powershell
git status
```

Make sure you do not have unfinished work that should be committed separately.

## Step 2 — Update main

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
```

If `git pull --ff-only` fails because the local and remote branches have diverged, stop and inspect the branch history. Do not force-push or discard commits to bypass the problem.

## Step 3 — Create a feature branch

```powershell
git switch -c docs/lesson-37-runner-infrastructure
```

## Step 4 — Review your changes

```powershell
git status
git diff
git diff --check
```

After staging, also run:

```powershell
git diff --cached --check
```

## Step 5 — Stage your files

Stage the exact files you created.

For example:

```powershell
git add .github/workflows/runner-matrix.yml
git add docs/github/module-04-actions/lesson-37-runner-fundamentals.md
git add docs/github/module-04-actions/runner-architecture-design.md
git add docs/github/module-04-actions/runner-security-review.md
git add docs/github/module-04-actions/runner-operations.md
git add docs/github/module-04-actions/arc-kubernetes-runners.md
```

Check the staged files:

```powershell
git status
git diff --cached
```

## Step 6 — Commit using Conventional Commits

```powershell
git commit -m "docs(actions): add runner infrastructure lesson"
```

## Step 7 — Push the branch

```powershell
git push -u origin docs/lesson-37-runner-infrastructure
```

## Step 8 — Open a pull request

Suggested PR title:

`docs(actions): add GitHub Actions runner infrastructure lesson`

Suggested PR description:

```markdown
## Summary

Adds Lesson 37 covering GitHub Actions runner infrastructure.

## Topics

- GitHub-hosted runners
- Self-hosted runners
- Runner groups and labels
- Persistent and ephemeral runners
- Docker-based runners
- Runner security
- Actions Runner Controller
- Kubernetes runner infrastructure
- Monitoring and cost optimization

## Validation

- [ ] Documentation reviewed
- [ ] Runner matrix workflow reviewed
- [ ] YAML syntax checked
- [ ] Security checklist completed
- [ ] No unnecessary infrastructure or secrets added
- [ ] Workflow manually executed successfully
```

Review the workflow and documentation before merging.

## Step 9 — Merge and tag

After your PR is reviewed and merged:

```powershell
git switch main
git fetch origin
git pull --ff-only origin main
```

Create an annotated tag:

```powershell
git tag -a module-04-lesson-37 -m "Module 4 Lesson 37: GitHub Actions Runners"
```

Push the tag:

```powershell
git push origin module-04-lesson-37
```

## Step 10 — Create a GitHub Release

Use:

- **Tag:** `module-04-lesson-37`
- **Release title:** `Module 4 — Lesson 37: GitHub Actions Runners`
- **Release notes:** Summarize runner architecture, security, ARC, and completed exercises.

This continues your practice of using annotated tags and GitHub Releases to mark learning milestones.

---

## 23. Official Documentation

GitHub's documentation is updated regularly. Use it when implementing actual infrastructure.

| Topic | Official documentation |
|---|---|
| Self-hosted runners | [Self-hosted runners reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners) |
| Add self-hosted runners | [Adding self-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners) |
| Runner groups | [Runner groups](https://docs.github.com/en/actions/concepts/runners/runner-groups) |
| Runner group access | [Managing access to self-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access) |
| Security hardening | [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use) |
| GitHub-hosted runners | [GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners) |
| Actions Runner Controller | [Actions Runner Controller](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller) |
| Deploy runner scale sets | [Deploying runner scale sets](https://docs.github.com/en/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets) |
| Runner scale sets | [Runner scale sets](https://docs.github.com/en/actions/concepts/runners/runner-scale-sets) |
| ARC support | [Support for ARC](https://docs.github.com/en/actions/concepts/runners/support-for-arc) |
| Workflow syntax | [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) |
| Workflow artifacts | [Storing workflow data as artifacts](https://docs.github.com/en/actions/how-tos/writing-workflows/choosing-what-your-workflow-does/storing-and-sharing-data-from-a-workflow) |

---

## 24. Lesson 37 Completion Checklist

### Your progress: 0/10

- [ ] Understand the runner architecture.
- [ ] Explain GitHub-hosted versus self-hosted runners.
- [ ] Understand runner labels and groups.
- [ ] Understand persistent versus ephemeral runners.
- [ ] Understand Docker-based runner approaches.
- [ ] Complete the operating-system matrix exercise.
- [ ] Write the runner security review.
- [ ] Design the three-environment architecture.
- [ ] Document ARC and Kubernetes concepts.
- [ ] Commit, merge, tag, and release Lesson 37.

## Final knowledge check

Before moving to Lesson 38, make sure you can answer these questions:

1. What is the difference between a workflow, a job, and a runner?
2. Why are GitHub-hosted runners suitable for most ordinary CI pipelines?
3. What operational responsibilities come with self-hosted runners?
4. How do labels differ from runner groups?
5. Why can persistent runners create security risks?
6. What is the difference between a job container and a self-hosted runner?
7. Why should untrusted pull-request code not execute on a sensitive deployment runner?
8. What problem does ARC solve?
9. What is a runner scale set?
10. Why is a self-hosted runner not automatically cheaper?

---

## 25. Next Lesson Preview

### Lesson 38 — GitHub Actions Reusable Workflows, Composite Actions & Internal Automation Platforms

We will go deeper into how engineering teams build reusable automation rather than duplicating YAML across dozens of repositories.

### Planned topics

1. Workflow reuse versus job reuse.
2. Reusable workflow architecture.
3. `workflow_call` in depth.
4. Inputs, outputs, and secrets.
5. Calling reusable workflows from other repositories.
6. Composite Actions.
7. JavaScript and Docker Actions.
8. Designing internal GitHub Actions.
9. Versioning and releasing custom Actions.
10. Sharing Actions across repositories.
11. Workflow templates.
12. Centralized CI/CD standards.
13. Organization-level automation.
14. Reusable security and quality gates.
15. Build a reusable DRF + React CI workflow.
16. Build a reusable release workflow.
17. Troubleshooting and security considerations.

**The key distinction:**

Lesson 37 taught us how to manage the machines executing workflows.

Lesson 38 will teach us how to design reusable automation components that can be shared across projects.

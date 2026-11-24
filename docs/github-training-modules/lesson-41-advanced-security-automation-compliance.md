## Lesson 41 — Advanced Security Automation & Compliance

**Level:** Advanced\
**Category:** DevSecOps, Software Supply Chain Security, Security Governance\
**Practical Focus:** Repository-wide security automation and compliance evidence

---

## 1. Lesson Overview

In Lesson 40, we focused on securing individual GitHub Actions workflows.

We examined workflow permissions, secrets, third-party Actions, untrusted input, supply-chain risks, and workflow hardening.

Now we are moving from **workflow security** to **repository-wide security automation and governance**.

A mature software project needs more than secure workflow files. It needs a repeatable process for identifying vulnerabilities, managing dependencies, scanning infrastructure, enforcing repository policies, collecting evidence, and reviewing security risks.

Consider a company maintaining several applications:

```text
Organization
│
├── restaurant-pos
│   ├── Django REST API
│   ├── React frontend
│   ├── PostgreSQL
│   └── Docker deployment
│
├── pharmacy-dashboard
│   ├── Django REST API
│   ├── React frontend
│   ├── PostgreSQL
│   └── Docker deployment
│
├── queue-system
│   ├── Django REST API
│   ├── React frontend
│   └── Redis
│
└── github-deep-dive-training
    └── GitHub training curriculum
```

Each repository needs security controls, but configuring and maintaining those controls independently creates inconsistencies.

For example:

- One repository may have dependency scanning enabled.
- Another may have no vulnerability reporting process.
- One project may generate an SBOM before releases.
- Another may publish containers without scanning them.
- One team may protect its main branch.
- Another may allow changes without required reviews.

The objective of this lesson is to understand how to create a consistent security process that can be applied across repositories.

### Learning objectives

By the end of this lesson, you should be able to:

1. Define a repository security baseline.
2. Create and maintain security policies.
3. Understand GitHub security configurations.
4. Enforce repository rules using rulesets.
5. Design required security checks.
6. Understand advanced CodeQL and custom queries.
7. Generate and inspect SARIF reports.
8. Establish vulnerability triage and remediation processes.
9. Automate dependency security with Dependabot.
10. Perform dependency license reviews.
11. Generate and evaluate SBOMs.
12. Understand SLSA, provenance, attestations, and signatures.
13. Evaluate repository practices with OpenSSF Scorecard.
14. Scan Docker images and container configurations.
15. Scan Kubernetes manifests.
16. Scan Terraform infrastructure.
17. Design security dashboards and useful metrics.
18. Collect and maintain audit evidence.
19. Map engineering controls to ISO/IEC 27001 objectives.
20. Design an enterprise-style DevSecOps compliance pipeline.

### Practical project

Extend the `github-deep-dive-training` repository with a security and compliance documentation structure.

You will create policies, configure repository controls, run independent security tools where applicable, and design an automated pipeline.

The project will use examples relevant to a Django REST Framework + React application.

**Important:** Some GitHub security features depend on repository visibility, organization configuration, and subscription entitlements. Independent scanners can still be used locally and in ordinary GitHub Actions workflows. Always verify current feature availability before designing a production process around a particular GitHub feature.

---

## 2. Lesson Architecture

This lesson contains 27 topics grouped into six practical areas.

| Area                                 | Topics                                                            |
| ------------------------------------ | ----------------------------------------------------------------- |
| Repository security governance       | Security baseline, SECURITY.md, security configurations, rulesets |
| Code security automation             | CodeQL, custom queries, SARIF, vulnerability triage               |
| Dependency and supply-chain security | Dependabot, license compliance, SBOM, SLSA, OpenSSF Scorecard     |
| Infrastructure security              | Container scanning, Kubernetes scanning, Terraform scanning       |
| Compliance and reporting             | Dashboards, audit evidence, ISO 27001 mapping                     |
| Enterprise DevSecOps                 | Governance, policy evaluation, end-to-end pipeline                |

The lesson is designed as a practical progression:

```text
Repository Security Baseline
          |
          v
Repository Governance
          |
          v
Automated Security Checks
          |
          v
Dependency and Supply-Chain Security
          |
          v
Infrastructure Security
          |
          v
Security Policy Evaluation
          |
          v
Compliance Evidence
          |
          v
Enterprise DevSecOps Pipeline
```

---

## Part I — Repository Security Governance

## 3. Establish a Repository Security Baseline

### 3.1 What is a security baseline?

A security baseline is the minimum set of security requirements that a repository must satisfy.

It defines what a project should have before it is considered ready for normal development and release activities.

For example:

| Area              | Minimum requirement                             |
| ----------------- | ----------------------------------------------- |
| Access control    | Repository access follows least privilege       |
| Branch management | Main branch is protected                        |
| Code review       | Important changes receive review                |
| Testing           | Automated tests run on pull requests            |
| Dependencies      | Dependencies are inventoried and reviewed       |
| Secrets           | Credentials are not committed                   |
| Workflows         | GitHub Actions use appropriate permissions      |
| Containers        | Production images are scanned                   |
| Releases          | Releases are traceable to source commits        |
| Vulnerabilities   | Findings have owners and remediation status     |
| Evidence          | Important security controls can be demonstrated |

A baseline is not a scanner. It is a policy describing the controls that should exist.

### 3.2 Create the security directory

Create this structure:

```text
docs/
└── security/
    ├── SECURITY-BASELINE.md
    ├── SECURITY-CONTROLS.md
    ├── VULNERABILITY-MANAGEMENT.md
    ├── SUPPLY-CHAIN-POLICY.md
    ├── SBOM-POLICY.md
    ├── LICENSE-COMPLIANCE.md
    ├── AUDIT-EVIDENCE.md
    └── ISO-27001-MAPPING.md
```

Also create a repository-level `SECURITY.md`.

### 3.3 Create SECURITY-BASELINE.md

File:

`docs/security/SECURITY-BASELINE.md`

```text
## Repository Security Baseline

## 1. Access Control

- [ ] Repository visibility is intentional.
- [ ] Collaborators have the minimum required permissions.
- [ ] Important files have designated code owners.
- [ ] Protected branches require pull requests.
- [ ] Administrative access is limited.
- [ ] Access is reviewed periodically.

## 2. Source Code Security

- [ ] Automated tests run on pull requests.
- [ ] Static analysis runs where applicable.
- [ ] Security-sensitive changes receive additional review.
- [ ] Secrets are never committed.
- [ ] Security findings are tracked.

## 3. Dependency Security

- [ ] Dependency manifests are committed.
- [ ] Lockfiles are maintained where applicable.
- [ ] Dependency updates are monitored.
- [ ] Vulnerable dependencies are reviewed.
- [ ] License information is evaluated.

## 4. Build and Release Security

- [ ] GitHub Actions use least-privilege permissions.
- [ ] Third-party Actions are pinned to verified full commit SHAs.
- [ ] Production credentials are not stored in source code.
- [ ] Release artifacts are traceable to source commits.
- [ ] Build evidence is retained according to policy.

## 5. Infrastructure Security

- [ ] Docker images are scanned.
- [ ] Dockerfiles are reviewed.
- [ ] Kubernetes manifests are scanned when applicable.
- [ ] Terraform files are scanned when applicable.
- [ ] Infrastructure changes receive review.

## 6. Vulnerability Management

- [ ] Security findings are recorded.
- [ ] Findings have severity and ownership.
- [ ] Critical findings are prioritized.
- [ ] Remediation is verified.
- [ ] Exceptions have an owner and expiry date.

## 7. Audit and Compliance

- [ ] Security policies are documented.
- [ ] Workflow execution evidence is retained.
- [ ] Security reports are retained.
- [ ] Releases are traceable to commits and builds.
- [ ] Controls are reviewed periodically.
```

### 3.4 Policy versus implementation versus evidence

These three concepts must be distinguished.

| Concept        | Example                                                |
| -------------- | ------------------------------------------------------ |
| Policy         | Main branch must be protected                          |
| Implementation | A GitHub ruleset protects `main`                       |
| Evidence       | Ruleset configuration and a successful protection test |

Writing a checklist does not activate a security control.

Likewise, enabling a feature does not necessarily prove that the control is operating correctly.

**Practical exercise:** Create the baseline document and classify each requirement as documented, implemented, or verified.

---

## 4. Create a Repository Security Policy

GitHub recognizes a repository-level `SECURITY.md` file as its security policy.

It tells users how to report vulnerabilities responsibly.

Create:

`SECURITY.md`

```text
## Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| Latest release | Yes |
| Older releases | No |

## Reporting a Vulnerability

Please do not publish sensitive vulnerability details in a public issue.

Use the repository's private vulnerability reporting process when available.

Include:

- Affected component
- Affected version
- Impact
- Reproduction summary
- Suggested remediation, if known

## Response Process

1. A maintainer reviews the report.
2. The vulnerability is assessed.
3. Affected versions are identified.
4. A remediation is prepared.
5. A patched release is published.
6. The resolution is documented.

## Disclosure

Coordinated disclosure should give maintainers
time to investigate and prepare a fix.
```

### Why is this important?

Without a reporting process, someone discovering a vulnerability may publish sensitive technical details in a public issue.

A security policy gives reporters a defined route for responsible communication.

For real projects, specify an actual reporting channel and response expectations rather than leaving the process ambiguous.

### Practical exercise

1. Create `SECURITY.md`.
2. Open your repository's Security area.
3. Check whether GitHub recognizes the policy.
4. Review the vulnerability reporting options available to your repository.
5. Document any limitations.

---

## 5. GitHub Security Configurations

### 5.1 What are security configurations?

Security configurations help organizations apply consistent security settings across multiple repositories.

Instead of configuring every repository independently, an organization can define a security baseline and apply it to selected repositories.

Example:

```text
Organization Security Configuration
              |
      +-------+-------+
      |       |       |
      v       v       v
 Restaurant Pharmacy Queue
 POS         Dashboard System
```

This is especially useful when a company maintains multiple applications.

### 5.2 Repository-level security features

Open:

### Repository → Settings → Security

Review the security features available for your repository.

| Feature                     | Purpose                                           |
| --------------------------- | ------------------------------------------------- |
| Dependency graph            | Identifies dependency relationships               |
| Dependabot alerts           | Reports known vulnerable dependencies             |
| Dependabot security updates | Proposes supported security updates               |
| Secret scanning             | Detects exposed credentials                       |
| Push protection             | Helps prevent supported secrets from being pushed |
| Code scanning               | Reports detected code vulnerabilities             |
| Dependency review           | Evaluates dependency changes in pull requests     |

Availability depends on the repository and GitHub plan.

Do not assume that every feature is available in every private repository.

### 5.3 Organization-level governance

An organization can establish a common policy.

Example:

```text
Mandatory for every repository
├── Security policy
├── Protected default branch
├── Pull request review
├── Automated tests
├── Dependency monitoring
└── Least-privilege workflow permissions

Technology-specific controls
├── Python dependency scanning
├── npm dependency scanning
├── Docker image scanning
├── Kubernetes manifest scanning
└── Terraform scanning
```

Not every repository needs every tool.

A Python application needs Python dependency monitoring. A repository that does not deploy Kubernetes should not be required to maintain Kubernetes scanning merely for appearances.

### Practical exercise

Write a policy describing:

- Which controls are mandatory for all repositories.
- Which controls depend on the technology.
- Who can approve an exception.
- How often security configurations are reviewed.

---

## 6. Rulesets and Branch Protection

### 6.1 What are rulesets?

GitHub rulesets define rules for branches and tags.

They can enforce requirements such as:

- Pull requests before merging.
- Required status checks.
- Required approvals.
- Restrictions on force pushes.
- Restrictions on branch deletion.
- Commit or tag-related policies.

Branch protection rules provide another mechanism for controlling branch behavior.

### 6.2 Create a ruleset for main

Navigate to:

### Repository → Settings → Rules → Rulesets

Create a branch ruleset targeting:

```text
main
```

Configure the following requirements where appropriate:

| Rule                            | Purpose                                  |
| ------------------------------- | ---------------------------------------- |
| Require pull requests           | Prevents direct unreviewed changes       |
| Require approvals               | Adds human review                        |
| Require status checks           | Blocks merging when required checks fail |
| Require conversation resolution | Ensures review discussions are addressed |
| Block force pushes              | Protects branch history                  |
| Restrict deletion               | Prevents accidental branch removal       |

For a one-person training repository, approval requirements may need to be adjusted so that you can continue practicing without creating an impossible review requirement.

### 6.3 Required status checks

A required check must be reported by a workflow before it can be selected as a required status check.

Example:

```text
Pull Request
    |
    v
Backend Tests
    |
    v
Frontend Tests
    |
    v
Lint and Type Checks
    |
    v
Dependency Checks
    |
    v
Security Scans
    |
    v
All Required Checks Pass?
    |
    +---- No ----> Fix and Push Again
    |
    +---- Yes ---> Eligible for Merge
```

A required check is a merge condition, not a guarantee that the underlying test or scanner is comprehensive.

### 6.4 Design required checks carefully

Do not require a status check that is never generated.

Also consider:

- Whether skipped jobs report a status compatible with your ruleset.
- Whether the workflow runs for the pull request event.
- Whether a check can be bypassed by authorized actors.
- Whether the check has the expected name and source.
- Whether the check is trustworthy and not controlled by untrusted input.

### Practical exercise

1. Configure a ruleset for `main`.
2. Open a test pull request.
3. Observe which merge conditions are enforced.
4. Temporarily create a failed required check.
5. Verify that the pull request cannot merge until the requirement is satisfied.

---

## Part II — Code Security Automation

## 7. Advanced CodeQL

### 7.1 What is CodeQL?

CodeQL is GitHub's semantic code-analysis technology.

It analyzes source code by building a database that represents program structure and relationships.

This allows it to identify certain security patterns that ordinary text searches may miss.

For example, a simple text search might find every use of a database query function.

A semantic analysis can investigate whether untrusted input reaches a sensitive operation through a particular data flow.

### 7.2 Default and extended query suites

| Suite    | Purpose                                              |
| -------- | ---------------------------------------------------- |
| Default  | Standard collection of security queries              |
| Extended | Additional queries that can provide broader analysis |

The extended suite may produce more findings and require additional triage.

### 7.3 CodeQL for Django and React

For a Django REST Framework application, code analysis may help identify:

- Potential injection vulnerabilities.
- Unsafe deserialization patterns.
- Weak input handling.
- Insecure data flow.
- Risky use of sensitive APIs.

For a React application, it may identify:

- Unsafe data handling.
- Cross-site scripting patterns.
- Vulnerable API usage.
- Risky JavaScript data flows.

CodeQL coverage depends on supported languages, configuration, and query availability.

### 7.4 Advanced CodeQL setup

GitHub supports default and advanced code-scanning setup.

Advanced setup is useful when a team needs more control over:

- Languages.
- Build configuration.
- Query suites.
- Custom query paths.
- Workflow triggers.
- Analysis configuration.

Do not introduce advanced configuration without a reason. Start with an appropriate supported default configuration, then customize when the project needs additional coverage.

---

## 8. Custom CodeQL Queries

### 8.1 What are custom queries?

Custom CodeQL queries allow teams to encode organization-specific security rules.

For example, an organization may want to detect:

- Disallowed API usage.
- Specific insecure configuration patterns.
- Use of deprecated security-sensitive functions.
- Patterns that violate internal development standards.

A CodeQL query uses the `.ql` extension.

### 8.2 Suggested repository structure

```text
.github/
└── codeql/
    └── custom-queries/
        ├── python/
        │   └── custom-security-rule.ql
        └── javascript/
            └── custom-security-rule.ql
```

### 8.3 Query quality

A custom query must be tested.

Evaluate:

1. Does it detect the intended pattern?
2. Does it produce false positives?
3. Does it miss relevant cases?
4. Does it work with the project's language version?
5. Is the result understandable to developers?
6. Can the finding be remediated?

A query that produces many irrelevant findings can reduce trust in the security pipeline.

### Practical exercise

Create a research note explaining:

- What your proposed query should detect.
- Which language it targets.
- What a positive result means.
- How you would test it.
- How you would evaluate false positives.

You do not need to invent a production-ready query for this exercise.

---

## 9. SARIF Reporting

### 9.1 What is SARIF?

SARIF stands for **Static Analysis Results Interchange Format**.

It is a standard format for representing static-analysis results.

Security tools can use SARIF to describe:

- Rules.
- Findings.
- Severity information.
- File locations.
- Messages.
- Related analysis information.

This allows compatible tools to exchange security findings.

### 9.2 SARIF workflow

```text
Source Code
    |
    v
Security Scanner
    |
    v
SARIF Report
    |
    v
GitHub SARIF Upload
    |
    v
Code Scanning Results
```

GitHub supports SARIF 2.1.0 for code-scanning integrations.

Uploading SARIF to GitHub Code Scanning requires the relevant feature entitlement.

### 9.3 Example scanner workflow concept

A scanner may generate a report:

```text
security-scanner scan . \
  --format sarif \
  --output security-results.sarif
```

The exact command depends on the selected scanner.

The important point is that the scanner must actually support SARIF output, and its output must conform to the expected schema.

### 9.4 What should you inspect?

When reviewing a SARIF report, look for:

- SARIF version.
- Tool name and version.
- Rule identifiers.
- Finding messages.
- File locations.
- Severity or security level.
- Result counts.

### Practical exercise

1. Choose a scanner that supports SARIF.
2. Run it against a sample project.
3. Generate a SARIF file.
4. Inspect its structure.
5. Document three findings or rules.
6. Explain how the report could be integrated into GitHub Code Scanning.

You can complete this exercise without uploading the report to GitHub.

---

## 10. Vulnerability Triage and Remediation

Finding vulnerabilities is only the beginning.

A mature team needs a consistent process for evaluating risk, assigning responsibility, and verifying fixes.

### 10.1 Severity categories

| Severity      | Example                                           | Suggested handling              |
| ------------- | ------------------------------------------------- | ------------------------------- |
| Critical      | Severe, exploitable issue with major impact       | Immediate investigation         |
| High          | Significant security weakness                     | Prioritize remediation          |
| Medium        | More limited impact or constrained exploitability | Schedule remediation            |
| Low           | Minor security concern                            | Track and address appropriately |
| Informational | Hardening recommendation                          | Review periodically             |

These categories are examples. A real organization should define its own risk methodology.

### 10.2 Risk is more than severity

A scanner's severity score is not the entire risk assessment.

Consider:

- Exploitability.
- Exposure.
- Business impact.
- Affected component.
- Whether the vulnerable component is reachable.
- Whether a fixed version exists.
- Whether compensating controls are available.

### 10.3 Create a vulnerability record

File:

`docs/security/VULNERABILITY-MANAGEMENT.md`

```text
## Part III — Vulnerability Management

## Finding

- ID:
- Date discovered:
- Scanner:
- Component:
- Affected version:

## Risk Assessment

- Severity:
- Likelihood:
- Business impact:
- Exposure:
- Exploitability:

## Ownership

- Assigned maintainer:
- Target remediation date:
- Related issue or pull request:

## Remediation

- Root cause:
- Proposed fix:
- Tests added:
- Verification result:

## Closure

- Status:
- Fixed version:
- Verification date:
- Evidence:
```

### 10.4 Automate finding management

A vulnerability automation process can follow this architecture:

```text
Scanner Runs
    |
    v
Structured Findings
    |
    v
Normalize Finding IDs
    |
    v
Check Existing Records
    |
    +---- Existing Finding
    |          |
    |          v
    |     Update Record
    |
    +---- New Finding
               |
               v
         Create Record
               |
               v
        Assign Ownership
               |
               v
        Track Remediation
               |
               v
        Verify the Fix
```

A robust implementation should avoid creating duplicate issues on every workflow run.

For sensitive findings, use an appropriate private reporting mechanism rather than publishing detailed vulnerability information in a public issue.

### Practical exercise

Create three sample vulnerability records:

- One critical.
- One high.
- One medium.

For each record, specify:

- Owner.
- Remediation target.
- Related work item.
- Verification requirement.
- Closure evidence.

---

## Part IV — Dependency and Supply-Chain Security

## 11. Dependabot Automation

### 11.1 What is Dependabot?

Dependabot helps maintain dependency security by detecting supported vulnerable dependencies and proposing updates.

It can also monitor dependency updates according to a configured schedule.

For a Django + React application, relevant ecosystems may include:

- Python packages.
- npm packages.
- GitHub Actions dependencies.

### 11.2 Create dependabot.yml

File:

`.github/dependabot.yml`

```text
version: 2

updates:
  - package-ecosystem: "pip"
    directory: "/backend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "npm"
    directory: "/frontend"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

Adjust the paths to match the actual project structure.

If your training repository does not contain a Python or npm manifest, do not configure a fictitious application directory just to make the example appear active.

### 11.3 Dependency update lifecycle

```text
Dependabot Detects Update
          |
          v
Pull Request Created
          |
          v
CI Tests Run
          |
          v
Security and Compatibility Review
          |
          v
Merge Approved Update
          |
          v
Release When Appropriate
```

### 11.4 Why not merge every update automatically?

Dependency updates can introduce:

- Breaking changes.
- API changes.
- Performance regressions.
- New vulnerabilities.
- License changes.
- Incompatibilities with other packages.

Automated updates still require an appropriate validation and review policy.

### Practical exercise

1. Inspect the repository's dependency manifests.
2. Identify the ecosystems actually used.
3. Configure Dependabot for those ecosystems.
4. Commit the configuration.
5. Inspect any generated pull requests.
6. Verify that the normal CI checks run against dependency updates.

---

## 12. License Compliance Automation

Dependency security is not only about known vulnerabilities.

Software licenses can affect how an application is developed, distributed, and used.

### 12.1 Why license compliance matters

A project may include dozens or hundreds of direct and transitive dependencies.

Each dependency may have different license terms.

A license review should identify:

- Package name.
- Version.
- License.
- Direct or transitive dependency.
- Whether the license is known.
- Whether additional review is required.

### 12.2 Create a license policy

File:

`docs/security/LICENSE-COMPLIANCE.md`

```text
## License Compliance Policy

## Policy Goals

- Identify licenses used by direct dependencies.
- Identify licenses used by transitive dependencies.
- Review license compatibility before distribution.
- Record dependencies requiring legal review.
- Keep third-party notices where required.

## Review Process

1. Generate a dependency inventory.
2. Identify each package license.
3. Review the license terms.
4. Record approved and restricted licenses.
5. Investigate unknown or ambiguous licenses.
6. Store the review evidence.

## Important

A license scanner provides technical information.
It does not replace legal advice or a legal compatibility review.
```

### 12.3 Tools to study

| Tool             | Main purpose                            |
| ---------------- | --------------------------------------- |
| pip-licenses     | Python dependency license inventory     |
| license-checker  | npm dependency license inventory        |
| ScanCode Toolkit | Software license and component analysis |

### 12.4 Example commands

Python:

```text
pip install pip-licenses
pip-licenses
```

Node.js:

```text
npx license-checker --summary
```

Use the tools against the appropriate project and retain the resulting reports as training evidence.

### Practical exercise

Generate a license inventory for a small Python project and a small Node.js project.

Record:

- Dependencies with known licenses.
- Dependencies with unknown licenses.
- Packages that need additional review.
- Where the reports should be stored.

---

## 13. Software Bill of Materials (SBOM)

### 13.1 What is an SBOM?

An SBOM is a **Software Bill of Materials**.

It is a structured inventory of software components included in an application or artifact.

It can describe:

- Component names.
- Versions.
- Suppliers.
- Identifiers.
- Dependency relationships.
- Package metadata.

Think of it as an inventory of the software included in a release.

### 13.2 Common SBOM formats

| Format    | Description                                                         |
| --------- | ------------------------------------------------------------------- |
| SPDX      | Software component and license information standard                 |
| CycloneDX | SBOM standard designed for software supply-chain and risk use cases |

### 13.3 Generate an SBOM with Syft

Syft can generate software inventories from directories and container images.

Example:

```text
## SPDX JSON
syft dir:. -o spdx-json=sbom.spdx.json

## CycloneDX JSON
syft dir:. -o cyclonedx-json=sbom.cdx.json
```

These commands generate inventory documents. They do not establish that the listed components are secure.

### 13.4 Create an SBOM policy

File:

`docs/security/SBOM-POLICY.md`

```text
## SBOM Policy

## Requirements

- Generate an SBOM for each production release.
- Use an approved SBOM format.
- Record the release version and source commit.
- Retain the SBOM with release evidence.
- Scan components for known vulnerabilities.
- Review unexpected or unknown components.

## Release Evidence

Each release should identify:

- Application name
- Version
- Source commit
- Build workflow
- Build timestamp
- SBOM filename
- SBOM format
- Scanner and scan date
- Review status
```

### 13.5 SBOM enforcement

```text
Build Application
       |
       v
Generate SBOM
       |
       v
Scan Components
       |
       v
Evaluate Policy
       |
       +---- Policy Failed ---> Block Release
       |
       +---- Policy Passed ---> Continue Release
```

A useful policy should define:

- Which findings block a release.
- Which findings require human review.
- How exceptions are approved.
- How long exceptions remain valid.
- Who owns remediation.

### Important distinction

An SBOM tells you what components are included.

It does not prove that:

- All components are secure.
- All dependencies are up to date.
- All licenses are compatible.
- The inventory is complete.
- The artifact was built securely.

### Practical exercise

1. Generate an SPDX or CycloneDX SBOM.
2. Inspect its metadata.
3. Identify several components.
4. Record the source commit and project version.
5. Explain how the SBOM should be retained with a release.

---

## 14. SLSA and Software Supply-Chain Security

### 14.1 What is SLSA?

SLSA means **Supply-chain Levels for Software Artifacts**.

It is a framework for improving the integrity of software supply chains, particularly the build and provenance process.

A release should be traceable to its source and build process.

### 14.2 Understand provenance

Provenance helps answer questions such as:

- Which repository produced this artifact?
- Which commit was used?
- Which workflow built it?
- Which build environment was involved?
- What process produced the artifact?

### 14.3 Understand the related concepts

| Concept     | Purpose                                                           |
| ----------- | ----------------------------------------------------------------- |
| SBOM        | What components are included?                                     |
| Provenance  | How was the artifact built?                                       |
| Attestation | What signed evidence supports a claim about an artifact?          |
| Signature   | Can the artifact or evidence be verified using a trust mechanism? |
| SLSA        | How mature are the software supply-chain integrity controls?      |

These concepts are related but are not interchangeable.

### 14.4 Artifact traceability

```text
Git Commit
    |
    v
GitHub Actions Workflow
    |
    v
Build Artifact
    |
    +---- SBOM
    |
    +---- Provenance / Attestation
    |
    v
Release
    |
    v
Deployment
```

### 14.5 GitHub artifact attestations

GitHub Actions supports artifact attestations that can provide provenance information for build artifacts.

The exact assurance level depends on the build design, workflow configuration, and applicable SLSA requirements.

Do not claim SLSA compliance merely because a workflow generates an SBOM or attaches a provenance file.

### Practical exercise

Write a short supply-chain traceability document explaining:

1. How a commit becomes a build artifact.
2. How the artifact is linked to its source.
3. How an SBOM is associated with the artifact.
4. How provenance is generated.
5. How a consumer could verify the evidence.

---

## 15. OpenSSF Scorecard

### 15.1 What is OpenSSF Scorecard?

OpenSSF Scorecard evaluates security practices in open-source projects using automated checks.

It provides signals about project security hygiene.

Examples of evaluated areas include:

- Branch protection.
- Dependency management.
- Dangerous workflow patterns.
- Security policy presence.
- Code review practices.
- Signed releases.

### 15.2 Example findings

| Finding                        | Possible improvement          |
| ------------------------------ | ----------------------------- |
| Missing security policy        | Add SECURITY.md               |
| Weak branch protections        | Configure rulesets            |
| Unpinned workflow dependencies | Pin verified Action SHAs      |
| Missing signed releases        | Study release signing         |
| Weak dependency practices      | Improve dependency monitoring |

### 15.3 Understand the score

A Scorecard result is not a security certification.

It is an automated assessment that helps identify areas for investigation.

A low score should trigger review, not an assumption that the entire project is insecure.

A high score does not prove that the project has no vulnerabilities.

### Practical exercise

1. Read the OpenSSF Scorecard checks documentation.
2. Select five checks.
3. Explain what each check evaluates.
4. Identify how the training repository could improve each area.
5. Record which improvements are already implemented and which remain planned.

---

## Part V — Infrastructure Security

## 16. Container Security Compliance

A Django + React deployment may include several containers:

```text
Application
├── Django API
├── React Frontend
├── PostgreSQL
├── Redis
└── Nginx
```

Every image and its runtime configuration need security review.

### 16.1 Container security controls

Review the following:

- Use maintained base images.
- Prefer minimal images where practical.
- Pin image versions.
- Avoid running application processes as root.
- Avoid embedding secrets in Docker images.
- Scan images for known vulnerabilities.
- Review exposed ports and capabilities.
- Rebuild images when important base-image updates are released.
- Review image provenance and source.

### 16.2 Scan with Trivy

Trivy can scan container images, filesystems, and configuration files.

Examples:

```text
### Scan an image
trivy image your-application:latest

### Scan a project filesystem
trivy fs .

### Scan configuration
trivy config .
```

Use an image you own or are authorized to test.

### 16.3 Define container release policy

A container security policy should define:

| Policy area  | Question                            |
| ------------ | ----------------------------------- |
| Severity     | Which findings block a release?     |
| Ownership    | Who fixes the finding?              |
| Exceptions   | Who approves an exception?          |
| Expiry       | When must an exception be reviewed? |
| Evidence     | Which scan report is retained?      |
| Verification | How is the fix confirmed?           |

Avoid a blanket rule that every finding automatically blocks every build. Evaluate risk, exploitability, false positives, and the actual impact on the application.

### Practical exercise

1. Select an image you own or are authorized to test.
2. Run Trivy.
3. Record the scan date and image reference.
4. Classify the findings.
5. Write a proposed release-blocking policy.

---

## 17. Kubernetes Security Scanning

Kubernetes introduces additional security concerns beyond the container image.

You must evaluate both the application image and its deployment configuration.

### 17.1 Kubernetes security areas

Review:

- Pod security settings.
- Container privileges.
- RBAC permissions.
- Network policies.
- Secret handling.
- Image references.
- Resource limits.
- Cluster configuration.

### 17.2 Tools to study

| Tool       | Main use                                       |
| ---------- | ---------------------------------------------- |
| kube-score | Kubernetes manifest recommendations            |
| KubeLinter | Kubernetes configuration checks                |
| Trivy      | Image and configuration scanning               |
| Checkov    | Infrastructure and configuration policy checks |

### 17.3 Example commands

```text
kube-score score deployment.yaml
```

```text
kube-linter lint ./kubernetes/
```

### 17.4 Example project structure

```text
kubernetes/
├── deployment.yaml
├── service.yaml
├── configmap.yaml
└── namespace.yaml
```

### Practical exercise

1. Create a small Kubernetes Deployment manifest.
2. Run a configuration scanner.
3. Review the findings.
4. Record the security improvements.
5. Save the report as training evidence.

This is a manifest-scanning exercise. You do not need to deploy the example to a production cluster.

---

## 18. Terraform Security Scanning

### 18.1 What is Infrastructure as Code?

Terraform describes infrastructure through configuration files.

Instead of manually creating every infrastructure resource, teams define the desired infrastructure in code.

Example:

```text
infrastructure/
├── main.tf
├── variables.tf
├── outputs.tf
└── modules/
```

Infrastructure configuration can introduce security weaknesses before any resource is provisioned.

### 18.2 Areas to review

- Publicly accessible services.
- Overly broad access policies.
- Unencrypted storage.
- Missing logging.
- Weak network restrictions.
- Insecure defaults.
- Missing resource controls.

### 18.3 Run Checkov

Install:

```text
pip install checkov
```

Scan:

```text
checkov -d infrastructure/
```

### 18.4 Infrastructure policy

Define:

- Which findings block deployment.
- Which findings require human review.
- Who approves exceptions.
- How policy changes are reviewed.
- Where scan reports are retained.

### Practical exercise

1. Create a small Terraform example.
2. Run Checkov against it.
3. Review the output.
4. Identify at least three findings or checks.
5. Save the report.
6. Document the remediation approach.

Do not provision production infrastructure for this exercise.

---

## Part VI — Compliance, Reporting, and Governance

## 19. Security Dashboards and Reporting

A security dashboard should help maintainers make decisions.

It should not simply display a large number of scanner results.

### 19.1 Questions a dashboard should answer

- How many open vulnerabilities exist?
- How many critical and high findings remain?
- Which dependencies are vulnerable?
- Which repositories are missing security policies?
- Which workflows have failed security checks?
- How many exceptions are active?
- How long does remediation usually take?

### 19.2 Example dashboard data

The following values are illustrative:

| Metric                       | Example |
| ---------------------------- | ------- |
| Open critical findings       | 0       |
| Open high findings           | 2       |
| Open medium findings         | 5       |
| Overdue remediation items    | 1       |
| Dependencies awaiting review | 3       |
| Active policy exceptions     | 2       |

### 19.3 Useful security metrics

| Metric                         | What it measures                           |
| ------------------------------ | ------------------------------------------ |
| Mean time to remediate         | Average time required to resolve findings  |
| Vulnerability backlog          | Open findings by severity                  |
| Overdue findings               | Items beyond their remediation target      |
| Policy coverage                | Repositories meeting baseline requirements |
| SBOM coverage                  | Releases with an associated SBOM           |
| Least-privilege coverage       | Workflows using approved permissions       |
| Dependency monitoring coverage | Repositories with dependency monitoring    |

### 19.4 Dashboard design exercise

Design a dashboard specification containing:

- Metric name.
- Metric definition.
- Data source.
- Update frequency.
- Responsible owner.
- Desired threshold.
- Escalation rule.

Do not confuse a metric with a security objective. For example, reducing the number of findings is not useful if the team simply stops scanning.

---

## 20. Audit Trails and Compliance Evidence

### 20.1 What is audit evidence?

A security control must be demonstrable.

For example, saying:

"Our main branch is protected."

is not enough to demonstrate that the protection is configured and operating correctly.

Evidence could include:

- Ruleset configuration.
- Pull request approval records.
- Workflow execution history.
- Scanner reports.
- SBOM files.
- Release metadata.
- Vulnerability remediation records.
- Approved exceptions.

### 20.2 Create an evidence register

File:

`docs/security/AUDIT-EVIDENCE.md`

```text
## Security Audit Evidence Register

| Control ID | Control | Evidence | Owner | Review Date |
|---|---|---|---|---|
| SEC-001 | Branch protection | Ruleset configuration | Maintainer | YYYY-MM-DD |
| SEC-002 | Automated testing | Actions workflow run | Developer | YYYY-MM-DD |
| SEC-003 | Dependency review | Dependency report | Developer | YYYY-MM-DD |
| SEC-004 | Secret management | Secret handling policy | Maintainer | YYYY-MM-DD |
| SEC-005 | SBOM generation | Release SBOM | Release owner | YYYY-MM-DD |
| SEC-006 | Vulnerability management | Finding records | Security owner | YYYY-MM-DD |
| SEC-007 | Release traceability | Release and commit record | Release owner | YYYY-MM-DD |
```

### 20.3 Evidence quality

Good evidence should be:

- Relevant to the control.
- Traceable to a source.
- Dated.
- Owned.
- Protected from unauthorized modification.
- Retained according to policy.
- Reviewed periodically.

Do not store credentials, personal information, or sensitive vulnerability details in a public evidence directory.

### Practical exercise

Create an evidence register with at least seven controls.

For each one, specify:

- What must be demonstrated.
- Which evidence proves it.
- Who owns it.
- When it should be reviewed.

---

## 21. ISO/IEC 27001 Security Control Mapping

### 21.1 What is ISO/IEC 27001?

ISO/IEC 27001 is an information security management system (ISMS) standard.

It provides requirements for establishing, implementing, maintaining, and continually improving an information security management system.

It is not a GitHub feature.

A repository with several security workflows is not automatically ISO 27001 compliant.

### 21.2 Why map engineering controls?

Software engineering practices can support broader information-security objectives.

For example:

| Engineering practice      | Related security objective               |
| ------------------------- | ---------------------------------------- |
| Repository access review  | Access control                           |
| Branch protection         | Controlled changes                       |
| Pull request approval     | Review and authorization                 |
| Dependency scanning       | Vulnerability management                 |
| Secret scanning           | Protection of authentication information |
| Security incident process | Incident management                      |
| Backup and recovery       | Business continuity                      |
| Audit evidence register   | Documented information                   |
| Release traceability      | Change and deployment accountability     |
| Security training         | Awareness and competence                 |

These are illustrative relationships, not a definitive mapping to individual ISO/IEC 27001 clauses or Annex A controls.

### 21.3 Create an ISO mapping document

File:

`docs/security/ISO-27001-MAPPING.md`

```text
## ISO/IEC 27001 Control Mapping

This document maps selected engineering practices
to information-security objectives.

It is an internal learning aid, not a certification statement.

| Engineering Practice | Security Objective |
|---|---|
| Repository access review | Access control |
| Branch protection | Change management |
| Pull request approval | Review and authorization |
| Dependency scanning | Vulnerability management |
| Secret scanning | Protection of authentication information |
| Security incident process | Incident management |
| Backup and recovery | Business continuity |
| Audit evidence register | Documented information |
| Release traceability | Change and deployment accountability |
| Security training | Awareness and competence |

## Evidence

For each mapped practice, record:

- Control owner
- Policy
- Implementation
- Evidence
- Review frequency
- Exceptions
- Improvement actions
```

### 21.4 What a real ISO 27001 implementation requires

An organization needs more than repository-level controls.

A real implementation also involves:

- Defining the ISMS scope.
- Establishing information-security policies.
- Conducting risk assessment.
- Defining risk treatment.
- Assigning responsibilities.
- Managing documented information.
- Reviewing performance.
- Performing internal audits.
- Conducting management reviews.
- Continually improving the ISMS.

### Practical exercise

Select five engineering practices from your repository.

For each practice, document:

1. The security objective.
2. The implemented control.
3. The responsible owner.
4. The evidence.
5. The review frequency.
6. Any known limitations.

---

## 22. Enterprise DevSecOps Governance

When a company maintains multiple repositories, security should not depend entirely on individual developers remembering every rule.

The organization needs a governance model.

### 22.1 Example responsibilities

| Role                     | Responsibility                        |
| ------------------------ | ------------------------------------- |
| Organization owner       | Organization-wide policy              |
| Repository administrator | Repository configuration              |
| Security lead            | Security standards and risk oversight |
| Developer                | Secure implementation                 |
| Reviewer                 | Code and configuration review         |
| Release owner            | Release approval and traceability     |
| Auditor                  | Evidence review                       |

In a small company, one person may perform multiple roles.

The important point is that responsibilities are explicitly assigned.

### 22.2 Governance requirements

A mature governance process should define:

- Approved security baselines.
- Exception handling.
- Security training.
- Periodic access reviews.
- Incident response.
- Risk assessment.
- Control testing.
- Continual improvement.

### 22.3 Policy exceptions

Security policies sometimes need exceptions.

For example, a scanner may report a finding that cannot be fixed immediately because the affected dependency has no compatible replacement.

An exception should contain:

```text
## Security Exception

- Exception ID:
- Control:
- Affected repository:
- Finding:
- Business justification:
- Risk assessment:
- Compensating controls:
- Approved by:
- Owner:
- Approval date:
- Expiry date:
- Review date:
- Remediation plan:
```

An exception is not a permanent removal of a control.

It is a documented, approved, time-limited risk decision.

---

## Part VII — Complete DevSecOps Compliance Pipeline

## 23. Design the Complete Compliance Pipeline

Now combine the concepts into one architecture.

The goal is to establish a repeatable process that evaluates code, dependencies, infrastructure, releases, and evidence.

### 23.1 End-to-end pipeline

```text
Developer Creates Pull Request
              |
              v
       Source Changes
              |
              v
         Code Checks
    ├── Backend Tests
    ├── Frontend Tests
    ├── Lint
    ├── Type Checks
    └── SAST / CodeQL
              |
              v
       Dependency Checks
    ├── Dependency Review
    ├── Vulnerability Checks
    └── License Review
              |
              v
         Secret Checks
    ├── Secret Scanning
    └── Gitleaks
              |
              v
     Infrastructure Checks
    ├── Docker
    ├── Kubernetes
    └── Terraform
              |
              v
       Policy Evaluation
    ├── Severity Thresholds
    ├── Required Checks
    └── Approved Exceptions
              |
              v
       All Requirements Pass?
              |
        +-----+-----+
        |           |
       No          Yes
        |           |
        v           v
    Remediate    Merge Eligible
        |           |
        +-----+     v
              |   Protected Main
              |       |
              |       v
              |   Release Pipeline
              |   ├── Build
              |   ├── SBOM
              |   ├── Provenance
              |   ├── Artifact Scan
              |   └── Release
              |       |
              |       v
              |   Deployment
              |       |
              +-------+
                      |
                      v
              Audit Evidence
              ├── Reports
              ├── Workflow History
              ├── Release Records
              └── Exceptions
```

### 23.2 Divide workflows by responsibility

Avoid placing every security check into one enormous workflow.

Use separate workflows where this improves ownership and troubleshooting.

| Workflow                      | Responsibility                            |
| ----------------------------- | ----------------------------------------- |
| `ci.yml`                      | Tests, linting, build                     |
| `security.yml`                | SAST, secret checks, security tools       |
| `dependency-review.yml`       | Dependency changes                        |
| `container-security.yml`      | Container scanning                        |
| `infrastructure-security.yml` | Terraform and Kubernetes scanning         |
| `compliance.yml`              | Policy evaluation and evidence collection |
| `release.yml`                 | Build, SBOM, provenance, and release      |

Not every workflow needs to run for every event.

For example:

- Dependency review is especially relevant to pull requests that change dependency manifests or lockfiles.
- Container scanning is relevant when container images are built.
- Terraform scanning is relevant when infrastructure configuration changes.
- Release evidence generation belongs in the release process.

### 23.3 Define enforcement stages

Separate the pipeline into three levels.

#### Level 1 — Informational

The scanner reports findings, but the result does not automatically block merging.

Useful for:

- Initial adoption.
- Learning scanner behavior.
- Establishing a baseline.
- Evaluating false positives.

#### Level 2 — Advisory with ownership

Findings receive owners and remediation targets.

Useful for:

- Managing vulnerability backlogs.
- Establishing remediation expectations.
- Tracking security improvements.

#### Level 3 — Enforced

Selected controls become required checks or release conditions.

Useful for:

- Established security baselines.
- Mature scanner configurations.
- Production release policies.

Do not make every scanner informational forever, but do not enforce poorly tested checks that generate unreliable results.

### 23.4 Example Django + React security architecture

```text
github-deep-dive-training
│
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       ├── security.yml
│       ├── dependency-review.yml
│       ├── container-security.yml
│       ├── infrastructure-security.yml
│       ├── compliance.yml
│       └── release.yml
│
├── docs/
│   ├── github/
│   │   └── module-04-actions/
│   │       └── lesson-41-advanced-security-automation-compliance.md
│   │
│   └── security/
│       ├── SECURITY-BASELINE.md
│       ├── SECURITY-CONTROLS.md
│       ├── VULNERABILITY-MANAGEMENT.md
│       ├── SUPPLY-CHAIN-POLICY.md
│       ├── SBOM-POLICY.md
│       ├── LICENSE-COMPLIANCE.md
│       ├── AUDIT-EVIDENCE.md
│       └── ISO-27001-MAPPING.md
│
└── SECURITY.md
```

This is a target architecture. Do not create empty workflows merely to match the directory tree. Implement each workflow when its checks are understood and configured.

---

## 24. Practical Project — Build a DevSecOps Compliance Repository

Your project is to extend `github-deep-dive-training` with a documented repository security baseline and a practical compliance design.

### Project requirements

#### Repository governance

- Create `SECURITY.md`.
- Create a repository security baseline.
- Document access and branch protection requirements.
- Configure and test a ruleset for `main`.

#### Code security

- Research CodeQL query suites.
- Understand custom query structure.
- Generate a SARIF report.

#### Vulnerability management

- Create a vulnerability management policy.
- Create three sample vulnerability records.
- Define severity, ownership, and verification.

#### Dependency and supply-chain security

- Configure Dependabot for an actual ecosystem in the repository.
- Generate a license inventory.
- Generate an SBOM.
- Document provenance and attestations.
- Review OpenSSF Scorecard checks.

#### Infrastructure security

- Scan an authorized container image or local project.
- Scan a sample Kubernetes manifest.
- Scan a sample Terraform directory.

#### Compliance

- Create a security dashboard specification.
- Create an audit evidence register.
- Map engineering practices to information-security objectives.
- Design the complete compliance pipeline.

### Important project boundary

This is a training project.

You do not need to purchase GitHub Advanced Security, deploy a production Kubernetes cluster, provision cloud infrastructure, or obtain an ISO certification to complete the learning objectives.

Where a GitHub feature is unavailable, document the limitation and use an appropriate independent tool for the underlying security exercise.

---

## 25. Practical Exercises — Lesson 41

Complete these exercises in order.

### Exercise progress

### 0 / 20 completed

1. Create `SECURITY.md` and document the vulnerability reporting process.
2. Create `SECURITY-BASELINE.md` and define the minimum repository controls.
3. Configure a ruleset for `main` and test it using a pull request.
4. Document your required CI and security status checks.
5. Study CodeQL default and extended query suites.
6. Create a custom CodeQL query research note.
7. Generate a SARIF report using a compatible scanner.
8. Create three vulnerability records and assign remediation owners.
9. Configure Dependabot for an ecosystem actually present in your repository.
10. Generate Python or npm dependency license reports.
11. Generate an SBOM in SPDX or CycloneDX format.
12. Document the difference between SBOM, provenance, attestations, and signatures.
13. Review five OpenSSF Scorecard checks.
14. Run Trivy against a container image you own or are authorized to test.
15. Run a Kubernetes manifest scanner against a sample manifest.
16. Run Checkov against a sample Terraform directory.
17. Create a security dashboard specification.
18. Create an audit evidence register.
19. Map selected engineering practices to ISO 27001 security objectives.
20. Design the complete DevSecOps compliance pipeline.

### Suggested exercise tracking

Create:

`docs/github/module-04-actions/lesson-41-exercise-tracker.md`

```text
## Lesson 41 — Exercise Tracker

| Exercise | Status | Evidence |
|---|---|---|
| 01 - SECURITY.md | Pending | |
| 02 - Security baseline | Pending | |
| 03 - Ruleset | Pending | |
| 04 - Required checks | Pending | |
| 05 - CodeQL suites | Pending | |
| 06 - Custom query research | Pending | |
| 07 - SARIF | Pending | |
| 08 - Vulnerability records | Pending | |
| 09 - Dependabot | Pending | |
| 10 - License inventory | Pending | |
| 11 - SBOM | Pending | |
| 12 - Supply-chain concepts | Pending | |
| 13 - OpenSSF Scorecard | Pending | |
| 14 - Trivy | Pending | |
| 15 - Kubernetes scanning | Pending | |
| 16 - Terraform scanning | Pending | |
| 17 - Security dashboard | Pending | |
| 18 - Audit evidence | Pending | |
| 19 - ISO mapping | Pending | |
| 20 - Complete pipeline | Pending | |
```

Update each status and evidence reference as you complete the exercise.

---

## 26. Main Lesson Markdown File

Create:

`docs/github/module-04-actions/lesson-41-advanced-security-automation-compliance.md`

Use the full lesson content as the main document.

### Supporting documentation structure

Keep reusable policies separate from the lesson itself.

```text
docs/
├── github/
│   └── module-04-actions/
│       ├── lesson-40-workflow-security.md
│       ├── lesson-41-advanced-security-automation-compliance.md
│       └── lesson-41-exercise-tracker.md
│
└── security/
    ├── SECURITY-BASELINE.md
    ├── SECURITY-CONTROLS.md
    ├── VULNERABILITY-MANAGEMENT.md
    ├── SUPPLY-CHAIN-POLICY.md
    ├── SBOM-POLICY.md
    ├── LICENSE-COMPLIANCE.md
    ├── AUDIT-EVIDENCE.md
    └── ISO-27001-MAPPING.md

SECURITY.md
```

The lesson teaches the concepts and exercises.

The supporting documents become reusable repository policies and templates.

---

## 27. Git Workflow — Commit, Pull Request, Tag, and Release

Use the same disciplined Git workflow practiced in previous lessons.

### 27.1 Start from an updated main branch

```text
git switch main
git pull origin main
```

Create the feature branch:

```text
git switch -c feat/lesson-41-security-compliance
```

### 27.2 Create and validate the files

After creating your files:

```text
git status
git diff
git diff --check
```

Review:

- File names.
- Markdown formatting.
- Code blocks.
- Internal links.
- Example commands.
- Directory structure.
- Accidental secrets or sensitive information.

### 27.3 Stage the intended files

```text
git add docs/github/module-04-actions/
git add docs/security/
git add SECURITY.md
```

Only stage `.github/` if you have actually created or modified the intended configuration files there.

Review the staged changes:

```text
git diff --cached
```

### 27.4 Commit

```text
git commit -m "feat(security): add advanced security compliance training"
```

### 27.5 Push the branch

```text
git push -u origin feat/lesson-41-security-compliance
```

### 27.6 Create the pull request

**Title:**

```text
feat(security): add advanced security automation and compliance
```

**Description:**

```text
## Summary

Adds Lesson 41 — Advanced Security Automation & Compliance.

## Changes

- Added repository security baseline.
- Added vulnerability management policy.
- Added SBOM and supply-chain security documentation.
- Added license compliance guidance.
- Added infrastructure security scanning exercises.
- Added audit evidence and ISO 27001 mapping templates.
- Added a DevSecOps compliance pipeline design.
- Added the Lesson 41 exercise tracker.

## Validation

- [ ] Markdown reviewed.
- [ ] Links checked.
- [ ] Example commands reviewed.
- [ ] Directory structure reviewed.
- [ ] No secrets committed.
- [ ] Supporting policies match the lesson.

## Related Lesson

Lesson 40 — GitHub Actions Security
```

### 27.7 Review and merge

Before merging:

1. Review the pull request diff.
2. Verify the lesson structure.
3. Check all code blocks.
4. Resolve review conversations.
5. Confirm required checks pass.
6. Merge using the repository's configured merge strategy.

### 27.8 Pull the merged changes

```text
git switch main
git pull origin main
```

### 27.9 Create an annotated tag

```text
git tag -a module-04-lesson-41 \
  -m "Module 4 Lesson 41: Advanced Security Automation and Compliance"
```

Push the tag:

```text
git push origin module-04-lesson-41
```

### 27.10 Create the GitHub Release

| Field       | Value                                                                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Tag         | `module-04-lesson-41`                                                                                                                            |
| Title       | Module 4 — Lesson 41: Advanced Security Automation & Compliance                                                                                  |
| Description | Completed advanced security automation, repository governance, software supply-chain security, infrastructure scanning, and compliance training. |

This creates a traceable history:

```text
Feature Branch
      |
      v
Commit
      |
      v
Pull Request
      |
      v
Review
      |
      v
Merge
      |
      v
Annotated Tag
      |
      v
GitHub Release
```

---

## 28. Completion Criteria

Lesson 41 is complete when you can explain the concepts and demonstrate the practical work.

### Repository governance

- Security policy created.
- Security baseline documented.
- Ruleset configured and tested.
- Required checks documented.
- Organization-level governance understood.

### Code security

- CodeQL default and extended suites reviewed.
- Custom query structure understood.
- SARIF report generated and inspected.
- Vulnerability triage process documented.

### Dependency and supply-chain security

- Dependabot configured where applicable.
- Dependency license inventory generated.
- SBOM generated.
- Provenance and attestation concepts understood.
- OpenSSF Scorecard checks reviewed.

### Infrastructure security

- Trivy scan performed.
- Kubernetes configuration scan performed.
- Terraform scan performed.
- Infrastructure findings documented.

### Compliance and governance

- Security dashboard specification created.
- Audit evidence register created.
- ISO 27001 mapping document created.
- Exception management understood.
- Complete DevSecOps pipeline designed.

### GitHub workflow

- Feature branch created.
- Changes committed.
- Pull request created.
- Changes reviewed and merged.
- Annotated tag created.
- GitHub Release published.

---

## 29. Important Technical Notes

1. GitHub security feature availability depends on repository visibility, plan, and organization configuration.
2. Scanner output requires human review. A scanner is not a substitute for security engineering.
3. An SBOM is an inventory, not proof of security.
4. Provenance describes how an artifact was built; it does not automatically prove that the source code is safe.
5. An attestation is useful only when its identity, integrity, and trust assumptions can be verified.
6. OpenSSF Scorecard is an assessment tool, not a certification.
7. Terraform and Kubernetes scanners evaluate configuration patterns; they cannot prove that every deployed system is secure.
8. A security workflow is not proof of ISO/IEC 27001 compliance.
9. A real compliance program requires organizational processes, risk assessment, documented responsibilities, evidence, and continual improvement.
10. Production workflows must use reviewed and verified Action references and least-privilege permissions.

---

## 30. Official Documentation and References

Use official documentation and project references when implementing the exercises.

### GitHub security

1. [GitHub — Quickstart for securing your repository](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository)
2. [GitHub — Security at scale](https://docs.github.com/en/code-security/concepts/security-at-scale/organization-security)
3. [GitHub — Global security settings](https://docs.github.com/en/code-security/how-tos/secure-at-scale/configure-organization-security/establish-complete-coverage/configure-global-settings)
4. [GitHub — Code scanning](https://docs.github.com/en/code-security/concepts/code-scanning/code-scanning)
5. [GitHub — Uploading SARIF files](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file)
6. [GitHub — Artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)

### Supply-chain security

1. [OpenSSF — Scorecard checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
2. [SLSA — Supply-chain Levels for Software Artifacts](https://slsa.dev/)
3. [SPDX — Software Bill of Materials](https://spdx.dev/)
4. [CycloneDX — SBOM Standard](https://cyclonedx.org/)

### Security tools

1. [Trivy Documentation](https://trivy.dev/)
2. [Checkov Documentation](https://www.checkov.io/)
3. [Syft Documentation](https://oss.anchore.com/docs/)
4. [KubeLinter](https://github.com/stackrox/kube-linter)
5. [kube-score](https://github.com/zegl/kube-score)
6. [ScanCode Toolkit](https://scancode-toolkit.readthedocs.io/)

### Information security

1. [ISO — ISO/IEC 27001](https://www.iso.org/standard/27001)

---

## Next Lesson — Lesson 42

### Advanced GitHub Actions Architecture & Reusable Workflows

In Lesson 42, we will move beyond individual workflows and security checks.

We will focus on designing reusable automation that can be shared across repositories and maintained centrally.

### Planned topics

1. Reusable workflows with `workflow_call`.
2. Workflow inputs, outputs, and secrets.
3. Composite Actions.
4. JavaScript custom Actions.
5. Docker custom Actions.
6. Centralized workflow repositories.
7. Workflow versioning and release management.
8. Organization-level workflow governance.
9. Environment protection rules.
10. Deployment approvals.
11. Concurrency and cancellation.
12. Workflow matrices and dynamic matrices.
13. Conditional execution and job dependencies.
14. Caching and artifact strategies.
15. Workflow performance optimization.
16. Cross-repository automation.
17. GitHub Actions APIs.
18. Advanced permissions and token design.
19. Reusable CI/CD architecture for Django + React.
20. Multi-environment deployment pipelines.
21. End-to-end reusable workflow project.

**Lesson 41 completion goal:** Establish a documented security baseline, understand repository-wide security automation, complete practical scanner exercises, and design a compliance pipeline that can be extended into a reusable enterprise DevSecOps architecture.

**Recommended commit message:**

```text
feat(security): add advanced security automation and compliance lesson
```

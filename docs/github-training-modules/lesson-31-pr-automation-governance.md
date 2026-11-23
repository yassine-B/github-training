# Module 3 — GitHub Pull Requests

## Lesson 31: Advanced Pull Request Automation and Governance

**Level:** Advanced
**Type:** Practical lesson
**Estimated time:** 3–4 hours
**Repository:** `github-deep-dive-training`

---

## Lesson Overview

In Lesson 28, you learned Pull Request fundamentals.

In Lesson 29, you practised advanced reviews, inline comments, suggestions, and resolving conversations.

In Lesson 30, you learned merge conflicts, branch synchronization, merge versus rebase, and Pull Request maintenance.

Now we'll explore how professional development teams standardize, automate, and govern the Pull Request process.

Imagine you're managing a development team working on a restaurant-management application.

Your team includes:

- Backend developers.
- Frontend developers.
- DevOps engineers.
- Documentation contributors.
- Repository maintainers.

You don't want developers merging untested changes directly into `main`.

You want GitHub to enforce repository policies automatically.

For example:

```text
Developer creates a Pull Request
              |
              v
PR template provides required information
              |
              v
CODEOWNERS identifies responsible reviewers
              |
              v
GitHub Actions runs automated checks
              |
              v
Required approvals are collected
              |
              v
Review conversations are resolved
              |
              v
Branch protection or rulesets evaluate requirements
              |
              v
PR becomes eligible for merging
              |
              v
Merge into main
```

This is the foundation of Pull Request governance.

**Important distinction:** A review request, an approval, a successful CI check, and permission to merge are four different things. A professional workflow combines them rather than treating them as interchangeable.

---

## 1. Learning Objectives

By the end of this lesson, you should understand and practise:

1. Pull Request governance and enforcement.
2. Default and multiple Pull Request templates.
3. CODEOWNERS configuration and pattern matching.
4. Automatic reviewer assignment.
5. Branch protection rules.
6. Repository rulesets.
7. Required approving reviews.
8. Required status checks.
9. Conversation resolution requirements.
10. GitHub Actions integration with Pull Requests.
11. PR title validation and Conventional Commit policies.
12. Local commit hooks versus centralized validation.
13. Auto-merge.
14. Merge queues and the `merge_group` event.
15. Designing governance for backend, frontend, and DevOps teams.
16. Building a professional Pull Request governance workflow.

## What you will build

By the end of the practical work, your repository should contain:

```text
.github/
├── CODEOWNERS
├── PULL_REQUEST_TEMPLATE.md
├── PULL_REQUEST_TEMPLATE/
│   ├── feature.md
│   ├── bug-fix.md
│   └── documentation.md
└── workflows/
    └── pr-validation.yml

docs/
└── github/
    └── module-03-pull-requests/
        └── lesson-31-pr-automation-governance.md
```

You will also inspect the available branch protection and ruleset settings and test a GitHub Actions validation workflow.

---

## 2. Pull Request Governance Fundamentals

## 2.1 What is Pull Request governance?

Pull Request governance is the collection of rules, responsibilities, and automated processes that control how proposed changes enter important branches.

For example, your repository might have these policies:

| Area | Policy |
|---|---|
| Reviews | At least one approval |
| Backend | Backend owner review |
| Frontend | Frontend owner review |
| Infrastructure | DevOps review |
| Tests | Required automated checks must pass |
| Conversations | Required review conversations must be resolved |
| Main branch | Direct pushes restricted |
| Commit messages | Conventional Commit convention |
| Documentation | Documentation updated when necessary |
| Security | Security checks required where configured |

These policies improve:

- Code quality.
- Consistency.
- Accountability.
- Traceability.
- Collaboration.
- Security.
- Release reliability.

## 2.2 Governance versus automation versus enforcement

These concepts are related, but they are not identical.

| Concept | Meaning |
|---|---|
| Governance | Defines the rules and responsibilities |
| Automation | Performs repetitive tasks automatically |
| Enforcement | Blocks operations that violate configured rules |

Examples:

| Example | Category |
|---|---|
| Require one approving review | Governance and enforcement |
| Run pytest automatically | Automation |
| Block merging when required tests fail | Enforcement |
| Request CODEOWNERS reviews | Automation |
| Require review conversations to be resolved | Governance and enforcement |
| Generate a deployment report | Automation |

A workflow can run automatically without being a required check. A CODEOWNERS file can request a review without making that approval mandatory.

Always distinguish between what GitHub performs automatically and what GitHub actually prevents.

---

## 3. GitHub Features Used in This Lesson

The main features we'll configure or study are:

| GitHub feature | Purpose |
|---|---|
| PR templates | Standardize PR descriptions |
| CODEOWNERS | Identify responsible reviewers |
| Branch protection | Protect important branches |
| Repository rulesets | Define branch and tag policies |
| Required reviews | Enforce approval requirements |
| Status checks | Require successful automation |
| GitHub Actions | Run validation workflows |
| Auto-merge | Merge an eligible PR automatically |
| Merge queues | Coordinate integration of multiple PRs |

**Availability note:** GitHub feature availability depends on repository visibility, ownership, plan, organization policies, and permissions. Your private, user-owned training repository may not expose every advanced option. Inspect the controls GitHub actually makes available to your repository rather than assuming a setting is supported.

---

## 4. PR Templates — Standardizing Contributions

A Pull Request template provides a predefined structure for new PR descriptions.

You explored basic templates in Lesson 28. Now we'll create a more professional setup.

## 4.1 Create a default PR template

Create:

```text
.github/
└── PULL_REQUEST_TEMPLATE.md
```

Add:

```markdown
## Summary

Describe what this Pull Request accomplishes.

## Related Issue

Closes #

## Type of change

- [ ] New feature
- [ ] Bug fix
- [ ] Refactoring
- [ ] Documentation
- [ ] Tests
- [ ] CI/CD
- [ ] Security improvement

## Changes

Describe the important changes.

## Implementation details

Explain technical decisions and affected components.

## Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Linting
- [ ] Build verification

## Security considerations

Explain any security implications.

## Breaking changes

- [ ] This PR introduces breaking changes.

If applicable, explain them.

## Screenshots

Add screenshots where relevant.

## Checklist

- [ ] Code follows repository standards.
- [ ] Tests added or updated.
- [ ] Documentation updated.
- [ ] No secrets or credentials included.
- [ ] No unrelated files included.
- [ ] Changes reviewed locally.
```

This is your default template.

When GitHub creates a PR using the default template, the author receives these sections as a starting point.

## 4.2 Why use templates?

Without templates, developers may forget important information.

For example, a developer might open a PR with only:

```text
Updated order management.
```

A reviewer has no clear explanation of:

- What changed.
- Why it changed.
- Which issue it addresses.
- How it was tested.
- Whether the change introduces breaking behavior.

A template makes these expectations visible.

## 4.3 Multiple PR templates

Different contributions often require different information.

For example:

- Feature implementation.
- Bug fixes.
- Documentation changes.
- Infrastructure changes.

Create:

```text
.github/
└── PULL_REQUEST_TEMPLATE/
    ├── feature.md
    ├── bug-fix.md
    ├── documentation.md
    └── infrastructure.md
```

### Feature template

File: `.github/PULL_REQUEST_TEMPLATE/feature.md`

```markdown
## Feature

Describe the feature.

## Business requirements

What problem does this feature solve?

## Implementation

- [ ] Backend
- [ ] Frontend
- [ ] Database
- [ ] API
- [ ] Tests

## Acceptance criteria

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Testing

Explain how the feature was tested.

## Documentation

- [ ] Documentation updated.
- [ ] API documentation updated where necessary.
```

### Bug-fix template

File: `.github/PULL_REQUEST_TEMPLATE/bug-fix.md`

```markdown
## Bug description

Describe the problem.

## Steps to reproduce

1.
2.
3.

## Expected behavior

What should happen?

## Actual behavior

What happens instead?

## Root cause

Explain the cause, if known.

## Fix

Describe the correction.

## Regression tests

- [ ] Regression test added.
- [ ] Existing tests pass.
- [ ] Related functionality checked.
```

### Documentation template

File: `.github/PULL_REQUEST_TEMPLATE/documentation.md`

```markdown
## Documentation changes

Describe the documentation updates.

## Affected documentation

- [ ] README
- [ ] API documentation
- [ ] Architecture documentation
- [ ] Tutorials
- [ ] Developer guides
- [ ] GitHub training lessons

## Validation

- [ ] Links checked.
- [ ] Code examples checked.
- [ ] Markdown formatting checked.
- [ ] No outdated instructions remain.
```

### Infrastructure template

File: `.github/PULL_REQUEST_TEMPLATE/infrastructure.md`

```markdown
## Infrastructure change

Describe the infrastructure change.

## Affected components

- [ ] Docker
- [ ] Nginx
- [ ] CI/CD
- [ ] Cloud infrastructure
- [ ] Monitoring
- [ ] Networking
- [ ] Deployment configuration

## Operational impact

Explain any deployment or operational implications.

## Security considerations

Describe relevant security implications.

## Validation

- [ ] Configuration validated.
- [ ] Deployment impact reviewed.
- [ ] Rollback approach considered.
- [ ] Documentation updated.
```

## 4.4 How to select a template

GitHub supports multiple templates inside `.github/PULL_REQUEST_TEMPLATE/`.

You can select a template through the template chooser or use a URL parameter.

Example:

```text
https://github.com/OWNER/REPOSITORY/compare/main...BRANCH?template=feature.md
```

Replace `OWNER`, `REPOSITORY`, and `BRANCH` with your actual values.

For your training repository, the URL will follow this pattern:

```text
https://github.com/yassine-B/github-deep-dive-training/compare/main...YOUR_BRANCH?template=feature.md
```

The template filename must match the file inside the template directory.

### Exercise 1

1. Create the default template.
2. Create the feature template.
3. Create the bug-fix template.
4. Create the documentation template.
5. Create the infrastructure template.
6. Open a test PR.
7. Experiment with selecting different templates.

Official reference:

[Creating a pull request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)

---

## 5. CODEOWNERS — Automatic Code Review Responsibility

Imagine your restaurant-management application has these directories:

```text
backend/
frontend/
infrastructure/
docs/
```

Different contributors are responsible for different areas.

You don't want every PR to be reviewed only by someone unfamiliar with the affected code.

GitHub provides a feature called **CODEOWNERS**.

A CODEOWNERS file identifies people or teams responsible for particular files and directories.

When a PR changes files covered by a CODEOWNERS rule, GitHub can automatically request reviews from the corresponding owners.

## 5.1 Create the CODEOWNERS file

Recommended location:

```text
.github/
└── CODEOWNERS
```

GitHub also supports CODEOWNERS files in the repository root and `docs/`.

If multiple supported locations contain CODEOWNERS files, GitHub uses the first one found in this order:

1. `.github/CODEOWNERS`
2. `CODEOWNERS` in the repository root
3. `docs/CODEOWNERS`

For this lesson, use `.github/CODEOWNERS`.

## 5.2 Example for the restaurant application

```text
# Default owner
* @yassine-B

# Backend
/backend/ @YOUR_BACKEND_USERNAME

# Frontend
/frontend/ @YOUR_FRONTEND_USERNAME

# Database models
/backend/apps/*/models/ @YOUR_BACKEND_USERNAME

# API documentation
/docs/api/ @YOUR_DOCUMENTATION_USERNAME

# Infrastructure
/infrastructure/ @YOUR_DEVOPS_USERNAME

# GitHub Actions
/.github/workflows/ @YOUR_DEVOPS_USERNAME
```

Replace the example usernames with actual GitHub users or organization teams that have suitable repository access.

For example, an organization team can be specified as:

```text
/backend/ @organization/backend-team
```

The organization and team must exist, and the team must have appropriate access to the repository.

**Important:** The default owner rule is followed by more specific rules. Put more specific patterns later so they can take precedence.

## 5.3 Understanding CODEOWNERS syntax

| Pattern | Meaning |
|---|---|
| `*` | Default ownership pattern |
| `/backend/` | Backend directory |
| `/frontend/` | Frontend directory |
| `*.py` | Python files |
| `*.md` | Markdown files |
| `/.github/workflows/` | Workflow directory |

CODEOWNERS uses GitHub's documented pattern-matching rules. It is not identical to every feature supported by `.gitignore`.

For reliable ownership rules, test patterns against real files in your repository.

## 5.4 Multiple owners

You can specify more than one owner:

```text
/backend/ @backend-dev @backend-lead
```

Or specify an organization team:

```text
/frontend/ @organization/frontend-team
```

GitHub can request reviews from the listed owners when relevant files change.

## 5.5 Requested review versus required approval

This distinction is essential.

**CODEOWNERS review request:**

- Identifies the people responsible for reviewing certain files.
- Can automatically request their reviews.
- Does not, by itself, make approval mandatory.

**Required code-owner review:**

- Is configured through branch protection or a supported ruleset.
- Makes code-owner approval a merge requirement.
- Can block merging until the required approval is received.

A CODEOWNERS file alone is not a complete enforcement policy.

## 5.6 Solo repository versus team repository

Your training repository is user-owned.

For initial practice, this is sufficient:

```text
* @yassine-B
```

However, remember:

- An owner must have appropriate repository access.
- A contributor cannot approve their own PR.
- A CODEOWNERS review request is most useful when another person opens a PR that changes owned files.
- A personal repository does not have organization teams.

When you introduce collaborators, add directory-specific owners.

### Exercise 2

1. Create `.github/CODEOWNERS`.
2. Add your username as the default owner.
3. Add commented examples for future backend, frontend, and DevOps owners.
4. Open a test PR that modifies a file covered by a CODEOWNERS pattern.
5. Observe whether GitHub requests a review from the owner.
6. Document the result.

Official reference:

[About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

## 6. Branch Protection Rules — Protecting Main

One of the most important responsibilities of a repository maintainer is protecting important branches.

Without suitable protection, contributors with sufficient permissions may push directly to `main`.

Branch protection can enforce conditions before changes enter a protected branch.

## 6.1 Open repository settings

Open your training repository:

[Branch settings](https://github.com/yassine-B/github-deep-dive-training/settings/branches)

Depending on the current GitHub interface, you may find branch protection controls under Settings → Rules → Rulesets and/or the branch protection interface.

## 6.2 Create a branch protection rule

Target branch:

```text
main
```

Suggested rule name:

```text
Protect Main Branch
```

Explore these settings where available:

| Setting | Recommended training configuration |
|---|---|
| Require a pull request before merging | Enabled |
| Required approving reviews | 1 |
| Dismiss stale approvals | Enabled |
| Require review from CODEOWNERS | Enabled when applicable |
| Require conversation resolution | Enabled |
| Require status checks | Enable after creating CI |
| Require branches to be up to date | Explore and enable when appropriate |
| Require signed commits | Optional advanced exercise |
| Restrict force pushes | Enabled |
| Restrict deletions | Enabled |

The exact controls depend on the protection mechanism and your repository's plan.

## 6.3 Understand the individual rules

### Require a Pull Request

Requires changes to enter the protected branch through a PR rather than ordinary direct pushes.

### Require approvals

Requires a configured number of approving reviews.

For this exercise:

```text
Required approvals: 1
```

An approval is not the same as a comment or a review request.

### Dismiss stale approvals

Allows the protection policy to invalidate previous approvals when new commits change the reviewed code.

The exact behavior depends on the configured review policy.

### Require review from CODEOWNERS

Requires approval from the relevant code owner when this option is enabled and supported.

### Require conversation resolution

Prevents merging while required review conversations remain unresolved.

### Require status checks

Requires selected automated checks to report success before merging.

You will create a validation workflow in Section 10.

### Require branches to be up to date

Requires the PR branch to include the latest target-branch changes before merging when strict required checks are configured.

This helps ensure that CI validates the changes against the current target branch.

### Restrict force pushes

Prevents force-pushing to the protected branch.

### Restrict deletions

Prevents accidental deletion of the protected branch.

## 6.4 Important warning before enabling protection

Do not enable every setting blindly.

For example:

- A required check that has never run can block PRs.
- A required approval can prevent a solo contributor from merging their own PR.
- A missing CODEOWNERS owner can make review routing ineffective.
- Strict up-to-date requirements can require repeated branch synchronization.

Start with rules that you can satisfy, test them, and then add more requirements.

### Exercise 3

Inspect your repository settings.

Record:

1. Which branch protection controls are available?
2. Which controls can you enable?
3. Which controls require a different plan?
4. Which controls require collaborators?
5. Which controls should wait until CI exists?

Official reference:

[About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

## 7. Repository Rulesets — Modern Repository Governance

Branch protection is useful, but GitHub also provides **repository rulesets**.

Rulesets allow administrators to define policies for branches and tags.

They are useful when you need consistent policies across multiple branches or repositories.

## 7.1 Where to find rulesets

Navigate to:

### Repository → Settings → Rules → Rulesets

Direct link:

[Ruleset settings](https://github.com/yassine-B/github-deep-dive-training/settings/rules)

## 7.2 Create your first ruleset

Suggested configuration:

| Field | Value |
|---|---|
| Ruleset name | `main-branch-governance` |
| Enforcement status | Active, if eligible |
| Target | Branches |
| Branch targeting | `main` |

Before activating it, review the selected rules and bypass permissions.

## 7.3 Rules to explore

| Rule | Purpose |
|---|---|
| Restrict deletions | Prevent branch deletion |
| Restrict force pushes | Prevent history rewriting |
| Require a pull request | Require PR-based integration |
| Require approvals | Require reviewer approval |
| Require code-owner review | Require designated owner approval |
| Require status checks | Require successful CI |
| Require conversation resolution | Require resolved review discussions |
| Require signed commits | Enforce commit signatures |
| Require linear history | Enforce a linear commit history |
| Require merge queue | Require queue-based integration where supported |

Rulesets can also target tags.

For example, you can define rules that help protect release tags against unauthorized changes.

## 7.4 Rulesets versus branch protection

| Capability | Branch protection | Rulesets |
|---|---|---|
| Protect branches | Yes | Yes |
| Protect tags | Not its primary purpose | Yes |
| Combine multiple policies | Has limitations | Designed for layered policies |
| Organization-wide policies | Different management model | Supported |
| Bypass permissions | Supported in applicable configurations | Configurable bypass lists |
| Centralized governance | More limited | More flexible |

One important distinction: multiple applicable rulesets can combine. Classic branch protection has limitations when multiple rules match the same branch.

Rulesets also support bypass permissions. Configure these carefully because a bypass permission can allow an otherwise restricted operation.

## 7.5 Practical exercise

If your repository supports the required settings:

1. Create `main-branch-governance`.
2. Target `main`.
3. Enable PR requirements.
4. Enable review requirements where available.
5. Enable conversation resolution where available.
6. Inspect bypass permissions.
7. Save and verify the configuration.

If GitHub does not expose a particular feature, document that limitation.

Do not claim a rule is active unless GitHub confirms that it is active.

Official references:

- [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)

---

## 8. Required Reviews and Automatic Reviewer Assignment

CODEOWNERS and required reviews work together, but they solve different problems.

## 8.1 Review routing

Review routing determines who should be notified about a change.

Example:

```text
/backend/ @organization/backend-team
/frontend/ @organization/frontend-team
/.github/workflows/ @organization/devops-team
```

A change to a backend file can trigger a review request to the backend team.

## 8.2 Review enforcement

Review enforcement determines which approvals are required before merging.

For example:

| File pattern | Responsible team | Example approval policy |
|---|---|---|
| `/backend/**` | Backend team | Backend owner approval |
| `/frontend/**` | Frontend team | Frontend owner approval |
| `/.github/workflows/**` | DevOps team | DevOps owner approval |
| `/security/**` | Security team | Security owner approval |

The actual enforcement options depend on the repository's ownership model and supported rules.

Some advanced required-reviewer policies are available only for eligible organization-owned repositories.

## 8.3 Why this matters

Suppose a developer changes:

```text
.github/workflows/deploy.yml
```

A frontend developer may not be the best person to review deployment permissions, CI behavior, or release configuration.

You want the change reviewed by someone familiar with deployment and CI/CD.

Automatic review routing makes this process more consistent.

### Exercise 4

Document a review ownership policy for your future restaurant application:

- Backend owner.
- Frontend owner.
- DevOps owner.
- Documentation owner.
- Security owner.

Use real usernames only when those contributors exist and have suitable repository access.

---

## 9. Required Status Checks — Making CI Part of the Merge Policy

A status check is a result reported by an automated process, such as GitHub Actions.

Examples:

```text
backend-tests          success
frontend-tests         success
pr-validation          success
security-scan          success
```

A required status check becomes a merge requirement when configured in branch protection or a ruleset.

## 9.1 Understand the difference

| CI workflow | Required status check |
|---|---|
| Runs automated validation | Enforces a selected result before merging |
| Can report success or failure | Blocks merging when required conditions are not satisfied |
| May be optional | Is part of the merge policy |

A workflow does not automatically become a required check just because it runs on every PR.

## 9.2 Example validation pipeline

```text
Pull Request opened
        |
        v
PR validation workflow
        |
        v
Validate PR title
        |
        v
Check whitespace errors
        |
        v
Report result
        |
        v
Required check evaluated
        |
        v
Merge allowed or blocked
```

You will implement this pipeline in the next section.

---

## 10. GitHub Actions Integration with Pull Requests

Now we'll move from manual review to automated validation.

GitHub Actions can run workflows when a Pull Request is opened, updated, reopened, or synchronized.

For example:

```text
Pull Request created
        |
        v
GitHub Actions triggered
        |
        v
Check out repository
        |
        v
Validate PR title
        |
        v
Check whitespace errors
        |
        v
Report validation result
        |
        v
PR checks pass or fail
```

## 10.1 Understand the `pull_request` event

GitHub Actions provides an event called:

```yaml
pull_request:
```

Common activity types include:

| Activity | Meaning |
|---|---|
| `opened` | PR created |
| `synchronize` | New commits pushed to the PR branch |
| `reopened` | Closed PR reopened |
| `ready_for_review` | Draft marked ready |
| `edited` | PR title or description edited |

You can use these activities to validate proposed changes.

## 10.2 Create the PR validation workflow

Create:

```text
.github/
└── workflows/
    └── pr-validation.yml
```

Add:

```yaml
name: PR Validation

on:
  pull_request:
    branches:
      - main
    types:
      - opened
      - synchronize
      - reopened
      - ready_for_review
      - edited

permissions:
  contents: read
  pull-requests: read

jobs:
  validate:
    name: Documentation and PR validation
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Validate PR title
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          python - <<'PY'
          import os
          import re
          import sys

          title = os.environ["PR_TITLE"]

          pattern = (
              r"^(feat|fix|docs|refactor|test|build|ci|"
              r"chore|perf|revert)"
              r"(\([a-z0-9-]+\))?: .+"
          )

          if not re.match(pattern, title):
              print("Invalid PR title.")
              print("Expected: type(scope): description")
              sys.exit(1)

          print("PR title is valid.")
          PY

      - name: Validate changed files
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha }}
        run: |
          git diff --check "$BASE_SHA...HEAD"

      - name: Validation completed
        run: echo "PR validation passed."
```

This is a lightweight training workflow, not a complete production CI pipeline.

It checks:

1. Whether the PR title follows your chosen Conventional Commit-style format.
2. Whether the proposed changes contain whitespace errors detected by `git diff --check`.

It does not yet run backend tests, frontend tests, or security scans.

## 10.3 Understand the workflow structure

| YAML element | Purpose |
|---|---|
| `name` | Workflow name |
| `on` | Trigger events |
| `pull_request` | Run for PR activity |
| `branches` | Target branches |
| `permissions` | Restrict the workflow token |
| `jobs` | Define workflow jobs |
| `runs-on` | Select execution environment |
| `steps` | Define individual operations |
| `uses` | Use an existing action |
| `run` | Execute shell commands |
| `env` | Provide environment variables |

## 10.4 Why permissions matter

This configuration:

```yaml
permissions:
  contents: read
  pull-requests: read
```

Limits the workflow token to the read access required by this exercise.

Avoid granting write permissions to every workflow by default.

For production workflows:

- Review third-party actions before using them.
- Pin actions to verified full commit SHAs where appropriate.
- Avoid exposing secrets to untrusted PR code.
- Give each workflow only the permissions it needs.
- Review how workflows behave when PRs come from forks.

We'll examine these security topics in Lesson 32.

## 10.5 Test the workflow

Create a branch using PowerShell-compatible commands:

```powershell
git switch main
git pull origin main

git switch -c ci/pr-validation-practice
```

Add the workflow:

```powershell
git add .github/workflows/pr-validation.yml

git commit -m "ci(github): add pull request validation workflow"

git push -u origin ci/pr-validation-practice
```

Create a PR with this title:

```text
ci(github): add pull request validation workflow
```

Open:

### Pull Request → Checks

You should see the validation workflow run.

## 10.6 Test an invalid PR title

Create another test PR with this title:

```text
Update workflow
```

The title validation should fail.

Edit the PR title to:

```text
ci(github): improve validation workflow
```

The workflow should run again and pass.

This demonstrates how GitHub can validate repository conventions automatically.

## 10.7 Make the workflow a required check

After the workflow has run successfully:

1. Open repository Settings.
2. Open Rules or Branches.
3. Edit your `main` protection configuration.
4. Enable required status checks.
5. Search for the check associated with the validation job.
6. Select the correct check.
7. Save the configuration if your plan permits it.

The job's check name in this example is:

```text
Documentation and PR validation
```

GitHub may display a check name that includes its workflow context. Select the actual check reported by your run.

**Important:** Don't make a check required before it exists and has reported a result. Otherwise, you may prevent PRs from merging until the check can run successfully.

## 10.8 Production workflow considerations

The example above is intentionally small.

A production repository may use separate workflows:

```text
.github/
└── workflows/
    ├── pr-validation.yml
    ├── backend-tests.yml
    ├── frontend-tests.yml
    ├── security-checks.yml
    └── build.yml
```

Each workflow can validate a different part of the application.

For example:

| Workflow | Responsibility |
|---|---|
| `pr-validation.yml` | PR title and basic validation |
| `backend-tests.yml` | Backend tests and linting |
| `frontend-tests.yml` | Frontend tests and build |
| `security-checks.yml` | Security-related checks |
| `build.yml` | Application build verification |

Only make checks required when they are stable, correctly configured, and appropriate for the target branch.

---

## 11. Conventional Commit Enforcement

Throughout this training, you've been using Conventional Commits.

Now let's distinguish two separate policies:

- Pull Request title conventions.
- Git commit message conventions.

They are not the same.

## 11.1 PR title convention

Example:

```text
feat(orders): add order filtering
```

The workflow from Section 10 validates PR titles.

## 11.2 Commit message convention

Examples:

```text
feat(orders): add order filtering

fix(auth): correct token refresh

docs(github): update repository guide

test(payments): add refund tests
```

A team may also require every commit message to follow a convention.

## 11.3 Local validation with Commitlint and Husky

For Node.js projects, developers can use Commitlint and Husky to validate commit messages locally.

Typical configuration:

File: `commitlint.config.js`

```javascript
export default {
  extends: ["@commitlint/config-conventional"],
};
```

Install development dependencies in the Node.js project:

```powershell
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
```

Initialize Husky:

```powershell
npx husky init
```

A commit message hook can run:

```sh
npx commitlint --edit "$1"
```

The exact hook setup depends on the installed Husky version and project configuration. Follow the documentation for your installed version.

## 11.4 Local hooks versus centralized enforcement

| Local hooks | GitHub Actions |
|---|---|
| Run on a developer's machine | Run on GitHub-hosted or configured runners |
| Provide fast feedback | Provide centralized validation |
| Depend on local installation | Run according to repository workflow configuration |
| Can be bypassed | Can become required checks |
| Useful for developer productivity | Useful for repository-wide enforcement |

Local hooks can be bypassed. They are useful developer feedback, but they are not a complete server-side enforcement boundary.

If you need centralized enforcement, validate the commit messages or PR metadata in a GitHub Actions workflow and configure the resulting check as required where supported.

**Important:** The workflow in Section 10 validates PR titles, not every commit message. Do not assume it enforces both policies.

We'll explore pre-commit, Husky, and Commitlint in the dedicated tooling lessons.

### Exercise 5

Document:

1. Your PR title convention.
2. Your commit message convention.
3. The difference between local hooks and GitHub Actions.
4. How failed validation affects a PR.
5. Which checks should be required before merging.

---

## 12. Auto-Merge — Automatically Merging Eligible PRs

Auto-merge allows GitHub to merge a Pull Request automatically when its required conditions are satisfied.

Imagine:

```text
PR opened
    |
    v
Review pending
    |
    v
Required approval received
    |
    v
CI tests pass
    |
    v
Conversations resolved
    |
    v
All merge requirements satisfied
    |
    v
GitHub performs the merge
```

## 12.1 How to enable auto-merge

First, repository administrators must enable auto-merge in repository settings where supported.

Then:

1. Open a PR.
2. Locate the merge section.
3. Choose the auto-merge option if available.
4. Select the merge method if prompted.
5. Confirm.

GitHub waits for the configured requirements.

## 12.2 Example

Suppose your repository requires:

```text
1 approval
All required CI checks
Resolved conversations
```

You enable auto-merge while the PR is waiting for approval.

GitHub waits until all configured conditions are satisfied and then performs the merge.

## 12.3 Auto-merge versus normal merge

| Normal merge | Auto-merge |
|---|---|
| User manually initiates the merge when eligible | User enables automatic merging |
| User performs the final merge action | GitHub performs the merge when requirements pass |
| Suitable for manual PR workflows | Useful for predictable automated workflows |

## 12.4 Important restrictions

Auto-merge availability depends on the repository's plan and configuration.

For example, GitHub documents availability for public repositories on GitHub Free and for private repositories on eligible paid plans.

For your private personal training repository on Free, do not assume the option will appear. Check the current repository settings and plan eligibility.

If unavailable, document the limitation and practise the lifecycle using manual merging.

Official documentation:

[Automatically merging a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request)

### Exercise 6

If auto-merge is available:

1. Enable it in repository settings.
2. Create a practice PR.
3. Enable auto-merge.
4. Observe the pending requirements.
5. Satisfy the requirements.
6. Observe the automatic merge.

If unavailable, document the limitation.

---

## 13. Merge Queues — Managing Many PRs

A merge queue is useful when several developers are merging PRs into the same target branch.

Imagine three approved PRs:

```text
PR #101 — Product management
PR #102 — Order management
PR #103 — Payment management
```

All three are approved.

However, merging each PR independently can create integration problems if the changes interact.

A merge queue helps coordinate the integration process.

## 13.1 How a merge queue works

```text
PR #101 ── Approved ──┐
                     |
PR #102 ── Approved ──┼── Merge Queue
                     |        |
PR #103 ── Approved ──┘        v
                         Combined checks
                               |
                               v
                         Successful checks
                               |
                               v
                         Merge into main
```

GitHub creates temporary merge-group branches to validate proposed integration against the latest target branch and preceding queued changes.

This helps detect problems that might not appear when each PR is tested independently.

## 13.2 Merge queue versus auto-merge

| Auto-merge | Merge queue |
|---|---|
| Waits for an individual PR's requirements | Coordinates integration of queued PRs |
| Automatically merges when eligible | Tests queued changes against the evolving target |
| Useful in many repositories | Especially useful in busy repositories |

These features solve related but different problems. A repository can use auto-merge together with a merge queue when its configuration supports both.

## 13.3 Availability limitations

GitHub documents merge queue availability for:

- Public repositories owned by organizations.
- Private repositories owned by organizations using GitHub Enterprise Cloud.

A private, user-owned repository such as your training repository generally cannot use this feature.

You can still study the architecture and understand how to prepare GitHub Actions for it.

## 13.4 Merge queue and GitHub Actions

When using merge queues, CI workflows must also respond to the `merge_group` event.

Example:

```yaml
on:
  pull_request:
    branches:
      - main

  merge_group:
    types:
      - checks_requested
```

Why?

GitHub needs automated checks to run against the combined merge-group changes, not just the original PR branch.

If your required workflow only listens to `pull_request`, the merge queue may wait for a check that never runs.

This is an important distinction when designing production CI pipelines.

Official references:

- [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
- [Merging a pull request with a merge queue](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue)

---

## 14. Professional Pull Request Governance Architecture

Let's combine everything you've learned.

Imagine your future restaurant-management application has this structure:

```text
restaurant-management/
│
├── backend/
│   ├── apps/
│   ├── config/
│   └── tests/
│
├── frontend/
│   ├── src/
│   └── tests/
│
├── infrastructure/
│   ├── docker/
│   └── nginx/
│
├── docs/
│
└── .github/
    ├── CODEOWNERS
    ├── PULL_REQUEST_TEMPLATE.md
    │
    ├── PULL_REQUEST_TEMPLATE/
    │   ├── feature.md
    │   ├── bug-fix.md
    │   ├── documentation.md
    │   └── infrastructure.md
    │
    └── workflows/
        ├── pr-validation.yml
        ├── backend-tests.yml
        ├── frontend-tests.yml
        └── security-checks.yml
```

## 14.1 Recommended governance policies

| Area | Policy |
|---|---|
| `main` | Protected branch |
| Backend | Backend owner review |
| Frontend | Frontend owner review |
| Infrastructure | DevOps review |
| Security | Security review where applicable |
| PR title | Conventional Commit-style format |
| PR description | Appropriate template |
| Backend tests | Required CI check |
| Frontend tests | Required CI check |
| Security checks | Required where configured |
| Reviews | At least one approval |
| Conversations | Required conversations resolved |
| Merging | Team-approved merge strategy |

## 14.2 Complete development lifecycle

### Step 1 — Developer creates a feature branch

```text
feat/order-management
```

### Step 2 — Developer implements changes

Commits follow the team's conventions.

### Step 3 — Developer opens a PR

The appropriate template is selected.

### Step 4 — CODEOWNERS requests reviews

Relevant maintainers are notified.

### Step 5 — GitHub Actions runs

Tests, linting, validation, and security checks execute.

### Step 6 — Review requirements are checked

Required approvals and resolved conversations are verified.

### Step 7 — Merge eligibility is evaluated

Branch protection or rulesets enforce the configured policies.

### Step 8 — PR is merged

The team uses normal merging, auto-merge, or a merge queue depending on its workflow and feature availability.

---

## 15. Practical Assignment — Build Your Governance System

Now implement the lesson in:

```text
github-deep-dive-training
```

## Exercise 1 — Create the repository structure

Create:

```text
.github/
├── CODEOWNERS
├── PULL_REQUEST_TEMPLATE.md
├── PULL_REQUEST_TEMPLATE/
│   ├── feature.md
│   ├── bug-fix.md
│   ├── documentation.md
│   └── infrastructure.md
└── workflows/
    └── pr-validation.yml
```

## Exercise 2 — Configure CODEOWNERS

Start with your actual GitHub username.

Add directory-specific owners when you have real collaborators.

Check the file's pattern order and ensure that more specific ownership rules appear after general rules.

## Exercise 3 — Configure PR templates

Create all five templates:

- Default.
- Feature.
- Bug fix.
- Documentation.
- Infrastructure.

Open a practice PR and test the template selection process.

## Exercise 4 — Inspect branch protection

Inspect your repository's available settings.

Attempt to configure:

- Require PR before merging.
- One approving review.
- Require conversation resolution.
- Require status checks after CI exists.
- Prevent force pushes.
- Prevent branch deletion.

Document unavailable settings.

## Exercise 5 — Explore rulesets

Explore repository rulesets.

Create a `main-branch-governance` ruleset if supported.

Compare its configuration with classic branch protection.

## Exercise 6 — Implement GitHub Actions validation

Create:

```text
.github/workflows/pr-validation.yml
```

Test:

- Valid PR title.
- Invalid PR title.
- Valid diff.
- Diff containing whitespace errors.

Observe the workflow results under the PR Checks tab.

## Exercise 7 — Configure required checks

If your repository supports required status checks:

1. Run the workflow successfully.
2. Configure the validation job as a required check.
3. Open another PR.
4. Observe the required-check status.
5. Confirm that a failed check prevents merging when the policy is active.

## Exercise 8 — Explore auto-merge

Inspect repository settings.

If available, test auto-merge.

Otherwise, document the plan limitation and describe the expected lifecycle.

## Exercise 9 — Study merge queues

Document:

- What a merge queue does.
- How merge groups work.
- Why `merge_group` is required in CI.
- Why your current repository may not be eligible.
- When an organization might benefit from a merge queue.

## Exercise 10 — Write your governance policy

Create a short policy document describing:

- Who reviews backend changes.
- Who reviews frontend changes.
- Who reviews infrastructure changes.
- Which CI checks are required.
- How PR titles are validated.
- What approvals are required.
- Which merge methods your team permits.

---

## 16. Lesson Documentation

Create:

```text
docs/
└── github/
    └── module-03-pull-requests/
        ├── lesson-28-pr-fundamentals.md
        ├── lesson-29-advanced-reviews.md
        ├── lesson-30-merge-conflicts.md
        └── lesson-31-pr-automation-governance.md

.github/
├── CODEOWNERS
├── PULL_REQUEST_TEMPLATE.md
├── PULL_REQUEST_TEMPLATE/
│   ├── feature.md
│   ├── bug-fix.md
│   ├── documentation.md
│   └── infrastructure.md
└── workflows/
    └── pr-validation.yml
```

For:

```text
lesson-31-pr-automation-governance.md
```

Use this outline:

```markdown
# Lesson 31 — Advanced PR Automation and Governance

## Learning Objectives

## 1. Pull Request Governance

## 2. PR Templates

## 3. Multiple PR Templates

## 4. CODEOWNERS

## 5. Automatic Reviewer Assignment

## 6. Branch Protection Rules

## 7. Repository Rulesets

## 8. Required Approvals

## 9. Required Status Checks

## 10. GitHub Actions Integration

## 11. Conventional Commit Enforcement

## 12. Auto-Merge

## 13. Merge Queues

## 14. Professional PR Governance Architecture

## 15. Practical Assignments

## 16. Assessment

## 17. Lessons Learned

## 18. References
```

Include:

- Explanations of the GitHub features.
- Practical configuration steps.
- The YAML workflow.
- CODEOWNERS examples.
- PR template examples.
- Your repository's actual configuration results.
- Screenshots of settings and workflow runs you actually completed.
- Any features unavailable under your current repository plan.

Do not add screenshots of hypothetical configurations. Capture the actual GitHub interface after performing the exercises.

---

## 17. Git Workflow — Commit, PR, Tag and Release

Keep your established training workflow.

## Step 1 — Create a branch

Run in PowerShell:

```powershell
git switch main
git pull origin main

git switch -c docs/lesson-31-pr-governance
```

## Step 2 — Add files

```powershell
git add docs/github/module-03-pull-requests/lesson-31-pr-automation-governance.md

git add .github/
```

## Step 3 — Validate

```powershell
git status
git diff --check
git diff --cached
```

Inspect the staged changes carefully.

Make sure you haven't accidentally staged unrelated files or real secrets.

## Step 4 — Commit

```powershell
git commit -m "docs(github): add Lesson 31 PR governance"
```

## Step 5 — Push

```powershell
git push -u origin docs/lesson-31-pr-governance
```

## Step 6 — Create the Pull Request

**PR title:**

```text
docs(github): add Lesson 31 PR automation and governance
```

**PR description:**

```markdown
## Summary

Add Lesson 31 covering advanced Pull Request governance.

## Changes

- Added advanced PR templates.
- Added CODEOWNERS documentation.
- Added branch protection documentation.
- Added repository rulesets documentation.
- Added PR validation workflow.
- Documented Conventional Commit enforcement.
- Documented auto-merge and merge queues.

## Validation

- [ ] Markdown validated.
- [ ] Workflow tested.
- [ ] Templates tested.
- [ ] CODEOWNERS inspected.
- [ ] Governance settings inspected.
- [ ] No secrets included.

## Related lesson

Lesson 30 — Merge Conflicts and PR Management.
```

Review your PR, verify the checks, resolve conversations, and merge it when the applicable requirements are satisfied.

## Step 7 — Create the annotated tag

After the PR has been merged:

```powershell
git switch main
git pull origin main

git fetch --tags

git tag -a module-03-lesson-31 -m "Complete Module 3 Lesson 31"

git push origin module-03-lesson-31
```

Verify:

```powershell
git tag --list
git show module-03-lesson-31
```

## Step 8 — Create the GitHub Release

Open the repository's Releases page and create a release using:

| Field | Value |
|---|---|
| Tag | `module-03-lesson-31` |
| Title | Module 3 — Lesson 31: PR Automation & Governance |
| Target | `main` |

Release notes:

```markdown
# Module 3 — Lesson 31

Completed Advanced Pull Request Automation and Governance.

## Topics

- Advanced PR templates
- Multiple PR templates
- CODEOWNERS
- Automatic reviewer assignment
- Branch protection
- Repository rulesets
- Required approvals
- Required status checks
- GitHub Actions integration
- Conventional Commit enforcement
- Auto-merge
- Merge queues

## Practical exercises

- Repository governance setup
- CODEOWNERS configuration
- PR template implementation
- PR validation workflow
- Branch protection exploration
- Ruleset exploration

## Training checkpoint

module-03-lesson-31
```

---

## 18. Assessment Checklist

### Lesson 31 progress — 0/16

- [ ] Created the default PR template.
- [ ] Created multiple PR templates.
- [ ] Created a CODEOWNERS file.
- [ ] Understood automatic reviewer assignment.
- [ ] Explored branch protection settings.
- [ ] Explored repository rulesets.
- [ ] Understood required review approvals.
- [ ] Created the PR validation GitHub Actions workflow.
- [ ] Tested valid and invalid PR titles.
- [ ] Understood required status checks.
- [ ] Studied Commitlint and Husky enforcement.
- [ ] Explored auto-merge.
- [ ] Understood merge queues and `merge_group`.
- [ ] Documented the governance architecture.
- [ ] Created and merged the Lesson 31 documentation PR.
- [ ] Published the `module-03-lesson-31` GitHub Release.

## Self-assessment questions

1. What is the difference between CODEOWNERS and required code-owner approval?
2. Why doesn't creating a GitHub Actions workflow automatically make it a required check?
3. What is the difference between branch protection and repository rulesets?
4. Why should you avoid enabling required checks before they have run?
5. What is the difference between a PR title convention and a commit message convention?
6. Why are local Git hooks not sufficient for centralized enforcement?
7. What happens when auto-merge is enabled?
8. Why does a merge queue need workflows to listen for `merge_group`?
9. Why should bypass permissions be configured carefully?
10. How would you design a review policy for backend, frontend, and infrastructure changes?

You should be able to explain each question and demonstrate the relevant feature where your repository supports it.

---

## 19. Official Documentation

Bookmark these resources:

1. [Managing and standardizing Pull Requests](https://docs.github.com/en/pull-requests/reference/managing-and-standardizing-pull-requests)
2. [Creating a Pull Request template](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
3. [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
4. [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
5. [About rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
6. [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
7. [GitHub Actions events](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows)
8. [Automatically merging a Pull Request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request)
9. [Managing a merge queue](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)
10. [Merging with a merge queue](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue)
11. [Commitlint documentation](https://commitlint.js.org/)
12. [Husky documentation](https://typicode.github.io/husky/)

---

## 20. Next Lesson — Lesson 32

## GitHub Pull Request Security & Quality Gates

In Lesson 31, you learned how to govern the Pull Request process, route reviews, define repository policies, and automate validation.

In Lesson 32, we'll focus on a critical question:

**How do you prevent insecure, vulnerable, or low-quality changes from entering your repository?**

Topics:

1. GitHub Actions security for PR workflows.
2. Fork-based Pull Request security.
3. `pull_request` versus `pull_request_target`.
4. Secrets and permissions in workflows.
5. Dependabot integration.
6. Dependency vulnerability checks.
7. CodeQL and code scanning.
8. Secret scanning and push protection.
9. Static Application Security Testing (SAST).
10. SonarQube integration.
11. Security review requirements.
12. Building a secure PR validation pipeline.

**Progression:** Lessons 28–31 covered the Pull Request lifecycle, advanced reviews, conflict resolution, automation, and governance. Lesson 32 will focus on securing that process and ensuring that vulnerable or low-quality changes do not enter your repository.

We'll continue using:

- `github-deep-dive-training`
- GitHub-ready Markdown lessons.
- Practical repository exercises.
- PowerShell-compatible commands.
- Conventional Commits.
- Pull Requests.
- Annotated tags.
- GitHub Releases.

**End of Lesson 31.**

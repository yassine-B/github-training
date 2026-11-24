# Module 3 — GitHub Pull Requests & Collaboration

## Lesson 33 — GitHub Issues: Advanced Issue Management

**Level:** Intermediate → Advanced
**Estimated time:** 3–4 hours
**Repository:** `github-deep-dive-training`

In this lesson, you’ll use GitHub Issues as a work-management system: capturing bugs, planning features, organizing tasks, connecting development work to pull requests, and tracking delivery through GitHub Projects.

The examples use a restaurant-management application. For the hands-on work, apply the practices to your `github-deep-dive-training` repository.

## Learning objectives

By the end of this lesson, you should be able to:

1. Configure issue templates and structured issue forms.
2. Design a consistent label taxonomy.
3. Organize work with milestones, assignees, and issue types where available.
4. Break large issues into sub-issues and track dependencies.
5. Link issues to branches, commits, and pull requests.
6. Use closing keywords correctly.
7. Triage and prioritize incoming work.
8. Connect Issues with GitHub Projects and Actions.
9. Manage Issues with GitHub CLI.
10. Establish a repeatable issue-management workflow for a software team.

---

## 1. Understanding GitHub Issues

An **Issue** is a trackable unit of work. It can represent a bug, feature request, task, technical improvement, documentation update, or larger initiative.

Example: **Issue #40 — Add kitchen order notifications**

The parent issue describes the problem, desired outcome, and acceptance criteria. The work can then be divided into smaller issues:

| Issue | Work |
|---|---|
| #41 | Backend notification event |
| #42 | Kitchen display notification UI |
| #43 | Notification tests |
| #44 | Documentation update |

Pull requests implement and review the work. They can link back to the Issues they address.

### Issue versus pull request

| Issue | Pull request |
|---|---|
| Describes work to be done | Proposes code or content changes |
| Tracks discussion and requirements | Tracks review, checks, and merge |
| Can have labels, milestones, and assignees | Can have labels, milestones, and reviewers |
| Can contain sub-issues | Can link to Issues |
| Usually starts or tracks the work | Usually delivers the work |

An Issue is not a substitute for a PR, and a PR is not a substitute for a well-defined requirement.

## 2. Issue types, labels, and milestones

These features answer different questions:

- **Issue type:** What kind of work is this?
- **Label:** How should we categorize or filter it?
- **Milestone:** Which delivery target does it belong to?

### 2.1 Issue types

Examples include:

| Type | Meaning | Example |
|---|---|---|
| Bug | Something is broken | Kitchen orders are not refreshing |
| Feature | New functionality | Add QR menu ordering |
| Task | A specific unit of work | Configure PostgreSQL backups |
| Epic | A larger initiative | Build the kitchen display system |

Issue types and their configuration can depend on repository and organization features. If your personal repository does not offer issue types, use the label taxonomy in this lesson instead. Do not create duplicate labels solely to imitate a feature that is unavailable.

### 2.2 Labels

Labels are flexible metadata. Use a small, consistent taxonomy rather than creating labels randomly.

Suggested labels for the training repository:

| Label | Purpose |
|---|---|
| `type: bug` | Defect |
| `type: feature` | New capability |
| `type: task` | General task |
| `type: docs` | Documentation |
| `priority: critical` | Immediate attention |
| `priority: high` | High importance |
| `priority: medium` | Normal priority |
| `priority: low` | Low priority |
| `status: triage` | Needs initial review |
| `status: ready` | Ready to be worked on |
| `status: blocked` | Waiting for a dependency |
| `area: backend` | Backend work |
| `area: frontend` | Frontend work |
| `area: devops` | Infrastructure and automation |
| `area: testing` | Test work |
| `area: documentation` | Documentation |

These are repository conventions, not built-in GitHub status values.

#### Exercise — Create labels

1. Open your repository and select **Issues → Labels**.
2. Create the labels in the table.
3. Apply `type: docs`, `priority: medium`, and `status: ready` to a practice issue.
4. Filter the Issues list by `area: backend` and `priority: high`.

Use actual milestones for delivery targets rather than labels such as `milestone: v1.0`.

### 2.3 Milestones

A milestone groups Issues and PRs around a delivery target.

Create these milestones:

| Milestone | Description |
|---|---|
| `Module 3 — Issues` | Complete the Issues training |
| `Module 4 — GitHub Actions` | Complete Actions and CI/CD training |
| `Repository Standards v1.0` | Finish repository standards and documentation |

For each milestone, configure a title and description. Add a due date only if you have a realistic target. Assign your Lesson 33 issues to `Module 3 — Issues`.

Milestones provide progress tracking and filtering, but they do not replace a project board or a dependency relationship.

---

## 3. Issue templates versus issue forms

Both standardize issue creation, but they provide different experiences.

| Feature | Markdown template | YAML issue form |
|---|---|---|
| Format | Markdown | YAML |
| Input experience | Pre-filled text | Structured web form |
| Dropdown fields | No | Yes |
| Required form fields | No | Yes |
| Best for | Simple templates | Consistent reports |

Issue forms support fields such as text inputs, text areas, dropdowns, checkboxes, and file uploads. Store them in `.github/ISSUE_TEMPLATE/`.

### 3.1 Create a bug report form

Create `.github/ISSUE_TEMPLATE/01-bug-report.yml`:

```yaml
name: Bug Report
description: Report a reproducible problem.
title: "[Bug]: "
labels:
  - "type: bug"
  - "status: triage"

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug.
        Please provide enough information to reproduce it.

  - type: input
    id: summary
    attributes:
      label: Bug summary
      description: What is not working?
      placeholder: Kitchen orders do not refresh automatically
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: Explain the sequence of actions.
      placeholder: |
        1. Open the kitchen display.
        2. Create a new order.
        3. Wait for the display to update.
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: What should happen?
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
      description: What happens instead?
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Environment
      options:
        - Local development
        - Testing
        - Production
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant logs
      description: Remove passwords, tokens, and other secrets before submitting.
      render: shell
    validations:
      required: false
```

### 3.2 Create a feature request form

Create `.github/ISSUE_TEMPLATE/02-feature-request.yml`:

```yaml
name: Feature Request
description: Propose a new capability.
title: "[Feature]: "
labels:
  - "type: feature"
  - "status: triage"

body:
  - type: markdown
    attributes:
      value: |
        Describe the problem and the outcome you want.

  - type: input
    id: problem
    attributes:
      label: Problem statement
      placeholder: Cashiers need a faster way to identify pending orders.
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: Describe how the feature should work.
    validations:
      required: true

  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance criteria
      description: List the conditions that make this feature complete.
      placeholder: |
        - [ ] The cashier can filter pending orders.
        - [ ] The order status is visible.
        - [ ] The interface works on a tablet.
    validations:
      required: true

  - type: dropdown
    id: area
    attributes:
      label: Application area
      options:
        - Backend
        - Frontend
        - Database
        - DevOps
        - Documentation
    validations:
      required: true
```

### 3.3 Configure the template chooser

Create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false

contact_links:
  - name: Project questions
    url: https://github.com/yassine-B/github-deep-dive-training/discussions
    about: Use Discussions for general questions, not bug reports.
```

The Discussions link is useful only if Discussions are enabled for the repository. Remove the `contact_links` section if you do not use Discussions.

`blank_issues_enabled: false` disables the blank-issue option in the template chooser.

#### Validation exercise

1. Commit the files to your branch and open the repository’s **Issues** tab.
2. Select **New issue**.
3. Confirm that both forms appear.
4. Submit a test issue and verify that required fields are enforced.
5. Confirm that the configured labels are applied.

---

## 4. Issue structure and quality

A professional issue explains the problem or desired outcome without prematurely dictating every implementation detail.

Use this structure when writing issues manually:

```markdown
# Context

Explain the background.

## Problem

What problem are we solving?

## Proposed outcome

What should be possible after this work?

## Acceptance criteria

- [ ] Requirement one
- [ ] Requirement two
- [ ] Requirement three

## Technical considerations

- Backend:
- Frontend:
- Database:
- Testing:

## Dependencies

List related or blocking issues.

## References

Add relevant documentation or screenshots.
```

### Example feature issue

**Title:** `[Feature]: Add kitchen order notifications`

```markdown
## Context

Kitchen staff need to know when a new order arrives.

## Problem

Staff currently need to monitor the screen manually.

## Proposed outcome

The kitchen display should notify staff when a new order is received.

## Acceptance criteria

- [ ] New orders appear on the kitchen display.
- [ ] The interface indicates a newly received order.
- [ ] The notification does not duplicate for the same event.
- [ ] The behavior is covered by tests.

## Technical considerations

- Backend: Django REST Framework and Channels.
- Frontend: React and WebSocket client.
- Testing: backend event tests and frontend behavior tests.

## Dependencies

The kitchen order event must be available.
```

Good acceptance criteria are observable and testable. “Make notifications better” is vague; “A connected kitchen display receives one notification for each newly created order” is testable.

---

## 5. Parent issues and sub-issues

Sub-issues let you split a large task into smaller, separately trackable pieces.

Create a parent issue:

**`[Epic]: Implement kitchen order notifications`**

Then create or attach these child issues:

| Child issue | Work |
|---|---|
| Backend event | Publish an event when an order arrives |
| WebSocket delivery | Deliver the event to connected kitchen clients |
| Frontend notification | Display the notification in React |
| Automated tests | Test event creation and display behavior |
| Documentation | Document the notification flow |

To create sub-issues:

1. Open the parent issue.
2. Find the sub-issues section.
3. Select **Create sub-issue**.
4. Create or attach the child issues.
5. Confirm that the parent displays the children and their progress.

A checklist in an issue body is just text-based task tracking. A sub-issue is a separate GitHub Issue with its own title, discussion, labels, assignee, and relationships.

The available sub-issue features and nesting limits may depend on GitHub’s current product configuration. Check the repository’s interface and current documentation rather than assuming a specific nesting limit.

---

## 6. Issue dependencies: blocking and blocked by

Dependencies represent ordering constraints between tasks.

Example:

- **Issue #50 — Implement backend order event**
- **Issue #51 — Implement frontend notification**

The frontend issue is blocked by the backend issue.

To configure the relationship:

1. Open the issue that cannot proceed.
2. Find **Relationships** in the sidebar.
3. Select **Mark as blocked by**.
4. Select the issue that must be completed first.
5. Verify that the relationship appears.

You can also mark an issue as blocking another issue.

**Exercise:** Make the frontend notification issue blocked by the backend event issue. Then inspect the relationship from both issues.

Use dependencies only when one task genuinely cannot proceed until another is complete. Do not use them merely to show that two issues are related.

---

## 7. Assignees and issue triage

An assignee indicates who is responsible for progressing an issue. Even when working alone, practice assigning issues to yourself.

A simple triage process:

1. **New:** The issue has been submitted but not reviewed.
2. **Triage:** Check whether it is understandable, reproducible, and relevant.
3. **Prioritized:** Assign type, priority, area, milestone, and owner.
4. **Ready:** Requirements and dependencies are clear.
5. **In progress:** A developer is working on it.
6. **Review:** A PR is available for review.
7. **Closed:** The work is complete, or the issue was closed with an appropriate reason.

Use labels such as `status: triage`, `status: ready`, and `status: blocked` to make this process visible. These are your team’s conventions, not special built-in GitHub status values.

For a small team, keep the process lightweight. A label, assignee, and milestone are often enough to make an issue actionable.

---

## 8. Linking Issues to branches, commits, and pull requests

A professional workflow should make it possible to answer:

- What work is being done?
- Who is responsible?
- Which branch contains the changes?
- Which PR implements the work?
- Has the issue actually been completed?

### 8.1 Branch naming

Suppose your issue number is `50`.

```powershell
git switch main
git pull origin main
git switch -c feature/50-kitchen-order-notifications
```

Other examples:

```text
feature/50-kitchen-order-notifications
fix/51-duplicate-order-events
docs/52-kitchen-notifications-guide
test/53-order-notification-tests
```

### 8.2 Link a PR to an issue

Include a closing keyword in the PR description:

```markdown
## Summary

Implement kitchen order notifications.

## Changes

- Add the backend notification event.
- Deliver events to connected kitchen clients.
- Display new-order notifications in React.
- Add automated tests.

## Testing

- [ ] Backend tests pass.
- [ ] Frontend tests pass.
- [ ] Manual verification completed.

## Related issue

Closes #50
```

Supported closing keywords include `Closes`, `Fixes`, and `Resolves`.

When the PR is merged into the repository’s default branch, GitHub can automatically close the referenced issue. The keyword must be used in the PR description or a commit message, and the PR must target the default branch for the usual automatic-closing behavior.

**Important:** Do not use `Closes #50` in a PR that completes only one part of a larger issue. Use a reference such as `Refs #50` or `Related to #50` and leave the parent issue open until the full acceptance criteria are met.

---

## 9. GitHub Projects integration

Issues can be added to GitHub Projects to plan and track work across one or more repositories.

| View | Purpose |
|---|---|
| Table | Detailed issue list and metadata |
| Board | Workflow columns |
| Roadmap | Timeline and planning |
| Filtered view | Work grouped by team, priority, or milestone |

### Practical exercise

Create a project named:

**`Restaurant POS — Development Roadmap`**

Add these fields:

| Field | Type | Example values |
|---|---|---|
| Status | Single select | Backlog, Ready, In Progress, Review, Done |
| Priority | Single select | Critical, High, Medium, Low |
| Area | Single select | Backend, Frontend, DevOps, QA |
| Target date | Date | Planned completion date |

Then:

1. Add your Lesson 33 issues to the project.
2. Create a board view grouped by Status.
3. Create a table view grouped by Priority.
4. Add a filter for `Area = Backend`.
5. Create a roadmap view if the available project configuration supports it.
6. Move an issue from Backlog to Ready and then In Progress.

Projects can display parent issues and sub-issue progress, making them useful for tracking larger initiatives. Project fields and views are separate from issue labels and milestones: choose the one that best supports the workflow you need.

---

## 10. GitHub Actions: automate issue management

GitHub Actions can respond to issue events such as an issue being opened, edited, labeled, or assigned.

For this lesson, create a workflow that adds a `status: triage` label whenever an issue is opened or reopened.

Create `.github/workflows/issue-triage.yml`:

```yaml
name: Issue Triage

on:
  issues:
    types:
      - opened
      - reopened

permissions:
  issues: write

jobs:
  add-triage-label:
    runs-on: ubuntu-latest

    steps:
      - name: Add triage label
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.issue;

            await github.rest.issues.addLabels({
              ...issue,
              labels: ["status: triage"]
            });
```

Before testing, make sure the `status: triage` label exists.

### Understand the workflow

| Configuration | Meaning |
|---|---|
| `issues` | Listen for Issue events |
| `opened`, `reopened` | Run for these event types |
| `permissions` | Grant the workflow only the access it needs |
| `issues: write` | Allow the workflow to update issue metadata |
| `github.rest.issues.addLabels` | GitHub API operation that applies the label |

**Security note:** `issues: write` grants write access to issue metadata. Keep permissions narrowly scoped. Do not add repository-content access or secrets unless the workflow genuinely needs them.

### Exercise

After merging the workflow:

1. Open a new test issue.
2. Confirm that `status: triage` is applied.
3. Open the Actions tab and inspect the run.
4. Close and reopen the test issue.
5. Confirm that the workflow runs again.

---

## 11. GitHub CLI — managing Issues from your terminal

GitHub CLI (`gh`) lets you manage Issues without opening the browser for every operation.

Verify installation and authentication:

```powershell
gh --version
gh auth status
```

Create an issue:

```powershell
gh issue create --title "[Feature]: Add kitchen notifications" --body "Implement notifications for newly received kitchen orders."
```

List open issues:

```powershell
gh issue list
```

View a specific issue:

```powershell
gh issue view 50
```

List issues with a label:

```powershell
gh issue list --label "status: triage"
```

Assign an issue to yourself:

```powershell
gh issue edit 50 --add-assignee @me
```

Add labels:

```powershell
gh issue edit 50 --add-label "type: feature" --add-label "priority: high"
```

Close an issue:

```powershell
gh issue close 50
```

CLI capabilities and flags can change between versions. Check `gh issue --help` or the relevant subcommand’s help output if a command differs in your installed version. Use the browser for sub-issue operations if your installed CLI does not support the operation you need.

---

## 12. Complete practical project

### Project: Kitchen Order Notification Management

**Scenario:** A restaurant needs a notification feature that informs kitchen staff whenever a new order arrives.

**Parent issue:** `[Epic]: Implement kitchen order notifications`

Required child issues:

1. Backend event implementation
2. WebSocket delivery
3. React notification interface
4. Automated tests
5. Documentation

Required organization:

- Labels for type, priority, status, and area
- A milestone
- An assigned owner
- A blocking relationship where appropriate
- A GitHub Project entry
- A PR linked to the parent issue or relevant child issue

### Exercise A — Create the parent issue

Create the parent issue with this acceptance criteria:

```markdown
## Objective

Notify kitchen staff when new orders arrive.

## Acceptance criteria

- [ ] Backend publishes a notification event.
- [ ] Connected kitchen clients receive the event.
- [ ] React displays a new-order notification.
- [ ] Duplicate notifications are prevented.
- [ ] Automated tests cover the feature.
- [ ] Technical documentation is available.

## Delivery

Track implementation through child issues and linked PRs.
```

Apply:

- `type: feature`
- `priority: high`
- `status: triage`
- `area: backend`

Assign yourself and add the milestone.

### Exercise B — Create child issues

Create five child issues and attach them to the parent. Each child should have its own acceptance criteria, labels, and assignee.

### Exercise C — Configure dependencies

Make the frontend implementation blocked by the backend event implementation. Link the testing issue to the work it validates.

### Exercise D — Implement a small documentation change

For this lesson, implement the documentation portion rather than building the application feature.

```powershell
git switch main
git pull origin main
git switch -c docs/lesson-33-issue-management
```

Add the documentation files listed in Section 13.

### Exercise E — Open a PR

Use this PR title:

**`docs(github): add Lesson 33 advanced issue management`**

PR description:

```markdown
## Summary

Document advanced GitHub Issues management.

## Changes

- Add bug report and feature request issue forms.
- Add issue template configuration.
- Document labels, milestones, and issue types.
- Document sub-issues and dependencies.
- Explain PR-to-Issue linking.
- Add issue triage and automation examples.

## Testing

- [ ] Issue form YAML reviewed.
- [ ] Template chooser tested.
- [ ] Documentation links checked.
- [ ] Issue workflow reviewed.

## Related issue

Closes #YOUR_LESSON_ISSUE_NUMBER
```

Replace `YOUR_LESSON_ISSUE_NUMBER` with the actual issue number you created for the documentation work. If the PR does not complete the entire issue, use a non-closing reference and leave the issue open.

---

## 13. Files to create in your repository

Use this structure:

```text
github-deep-dive-training/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── 01-bug-report.yml
│   │   ├── 02-feature-request.yml
│   │   └── config.yml
│   └── workflows/
│       └── issue-triage.yml
└── docs/
    └── github/
        └── module-03-issues/
            ├── lesson-33-advanced-issue-management.md
            ├── issue-label-conventions.md
            ├── issue-triage-process.md
            └── issue-management-examples.md
```

### `issue-label-conventions.md`

```markdown
# Issue Label Conventions

## Type labels

- type: bug
- type: feature
- type: task
- type: docs

## Priority labels

- priority: critical
- priority: high
- priority: medium
- priority: low

## Status labels

- status: triage
- status: ready
- status: blocked

## Area labels

- area: backend
- area: frontend
- area: database
- area: devops
- area: testing
- area: documentation

## Rules

1. Every issue should have a type.
2. Every issue should have a priority.
3. Every issue should have an area.
4. Issues awaiting review should use status: triage.
5. Blocked work should use status: blocked.
6. Labels must be reused consistently.
```

### `issue-triage-process.md`

```markdown
# Issue Triage Process

## 1. New issue

Review the title, description, and submitted information.

## 2. Validate

Determine whether the issue is:

- Reproducible
- Understandable
- Relevant
- A duplicate
- Actionable

## 3. Classify

Apply:

- Type
- Priority
- Area
- Status

## 4. Plan

Assign an owner and milestone.

Create sub-issues for larger tasks.

Define dependencies.

## 5. Ready for development

Confirm acceptance criteria and technical requirements.

Move the issue to Ready.

## 6. Implementation

Create a branch and link the issue to the pull request.

## 7. Review and closure

Review and merge the pull request.

Verify the issue's acceptance criteria before closing it.
```

### `issue-management-examples.md`

```markdown
# Issue Management Examples

## Example 1 — Bug

Title:
[Bug]: Kitchen display does not refresh

Labels:
- type: bug
- priority: high
- area: frontend
- status: triage

Acceptance criteria:
- [ ] Reproduce the problem.
- [ ] Identify the cause.
- [ ] Implement the fix.
- [ ] Add a regression test.

## Example 2 — Feature

Title:
[Feature]: Add QR menu ordering

Labels:
- type: feature
- priority: high
- area: frontend

Acceptance criteria:
- [ ] Display menu categories.
- [ ] Display product details.
- [ ] Allow customers to build an order.
- [ ] Submit the order.

## Example 3 — Documentation

Title:
[Docs]: Document local deployment

Labels:
- type: docs
- priority: medium
- area: documentation

Acceptance criteria:
- [ ] Document environment variables.
- [ ] Document Docker startup.
- [ ] Document backup and recovery.
```

The main lesson file, `lesson-33-advanced-issue-management.md`, should contain the full lesson notes and examples from this training.

---

## 14. Git workflow — commit, push, PR, tag, release

Check your working tree:

```powershell
git status
```

Stage the lesson files:

```powershell
git add .github/ISSUE_TEMPLATE/
git add .github/workflows/issue-triage.yml
git add docs/github/module-03-issues/
```

Commit and push:

```powershell
git commit -m "docs(github): add Lesson 33 advanced issue management"
git push -u origin docs/lesson-33-issue-management
```

Then:

1. Open GitHub and navigate to **Pull requests**.
2. Create a PR targeting `main`.
3. Review the changes and confirm the checks pass.
4. Merge the PR.
5. Pull the latest `main` locally.

```powershell
git switch main
git pull origin main
```

### Create the lesson tag

Use the established tag convention:

```powershell
git tag -a module-03-lesson-33 -m "Module 3 - Lesson 33: Advanced Issue Management"
git push origin module-03-lesson-33
```

### Create the GitHub Release

**Tag:** `module-03-lesson-33`
**Release title:** `Module 3 — Lesson 33: Advanced Issue Management`

Release notes:

```markdown
## Module 3 — Lesson 33

GitHub Issues: Advanced Issue Management

### Topics completed

- Issue types, labels, and milestones
- Markdown issue templates
- YAML issue forms
- Parent issues and sub-issues
- Issue dependencies
- Assignees and triage
- Pull Request linking and closing keywords
- GitHub Projects integration
- GitHub Actions issue automation
- GitHub CLI issue management

### Repository deliverables

- Bug report form
- Feature request form
- Issue template configuration
- Issue triage workflow
- Issue management documentation
```

---

## 15. Lesson 33 completion checklist

- [ ] Understand Issues versus Pull Requests
- [ ] Create the issue label taxonomy
- [ ] Create and configure milestones
- [ ] Create the bug report YAML form
- [ ] Create the feature request YAML form
- [ ] Configure the issue template chooser
- [ ] Create a parent issue and child issues
- [ ] Configure a blocking dependency
- [ ] Assign issues and perform triage
- [ ] Connect Issues to a GitHub Project
- [ ] Create and test the issue-triage workflow
- [ ] Practice GitHub CLI issue commands
- [ ] Open and merge the documentation PR
- [ ] Create and push the lesson tag
- [ ] Create the GitHub Release

---

## 16. Official documentation

1. [Using Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues)
2. [Configuring issue templates for your repository](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
3. [Syntax for issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
4. [Using labels and milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
5. [Adding sub-issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-sub-issues)
6. [Creating issue dependencies](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-issue-dependencies)
7. [Linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
8. [Creating an issue with GitHub CLI](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)
9. [Planning and tracking work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)
10. [Adding and managing project fields](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)

---

## 17. What comes next?

### Lesson 34 — GitHub Actions: Complete CI/CD Deep Dive

Next, you’ll move from manually managing Issues to automating the software development lifecycle.

Planned topics:

1. Understanding the Actions tab
2. Workflows, events, jobs, steps, and runners
3. Workflow YAML structure
4. `push`, `pull_request`, `workflow_dispatch`, and scheduled triggers
5. GitHub-hosted versus self-hosted runners
6. Environment variables, secrets, and contexts
7. Workflow permissions and `GITHUB_TOKEN`
8. Reusable workflows and composite actions
9. Job dependencies, matrices, and conditional execution
10. Django REST Framework CI pipeline
11. React/Vite CI pipeline
12. PostgreSQL service containers and integration tests
13. Ruff, pytest, ESLint, TypeScript, and build checks
14. Docker image build and publishing
15. Deployment workflows
16. Environments, approvals, and deployment protection
17. Caching and workflow optimization
18. Artifacts and test reports
19. Dependabot integration
20. CI/CD security and troubleshooting

Complete Lesson 33 and create its release before moving to Lesson 34.

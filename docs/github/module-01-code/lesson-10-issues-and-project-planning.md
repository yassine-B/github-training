# Lesson 10 — GitHub Issues and Project Planning

**Module:** 01 — Code  
**Topic:** Issue tracking, labels, milestones, Projects, and development planning  
**Difficulty:** Intermediate  
**Estimated time:** 3–4 hours

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what GitHub Issues are and when to use them.
- Create and manage bug reports, feature requests, and technical tasks.
- Understand the Issue lifecycle.
- Use labels to categorize work.
- Assign Issues to contributors.
- Organize Issues using milestones.
- Create task lists and break larger work into smaller Issues.
- Understand the relationship between Issues and Pull Requests.
- Automatically close Issues when Pull Requests are merged.
- Use GitHub Projects to plan and track development.
- Search and filter Issues.
- Use GitHub CLI to manage Issues from your terminal.
- Create a practical issue-tracking workflow for a development project.

## 2. What are GitHub Issues?

GitHub Issues are used to plan, discuss, assign, and track work in a repository.

You can use Issues to track:

| Issue category | Example |
|---|---|
| Bug | Login returns HTTP 500 |
| Feature | Add password reset functionality |
| Enhancement | Improve API response validation |
| Documentation | Document authentication endpoints |
| Refactoring | Separate business logic from API views |
| Testing | Add tests for order creation |
| DevOps | Configure Docker Compose |
| Security | Review authentication permissions |

An Issue is not necessarily a bug. It represents a piece of work that needs discussion, investigation, implementation, or tracking.

### 2.1 Issues versus Pull Requests

These two features have different responsibilities.

| GitHub Issues | GitHub Pull Requests |
|---|---|
| Track work | Propose code changes |
| Describe problems | Show implemented changes |
| Discuss requirements | Review code |
| Assign responsibilities | Request reviews |
| Organize tasks | Merge branches |
| Track progress | Run checks and CI workflows |

Example:

You discover that the restaurant application does not validate product quantities.

You create an Issue:

`[BUG] Product quantity accepts zero`

A developer creates a branch:

`fix/product-quantity-validation`

They implement the correction and open a Pull Request.

The Pull Request references the Issue. Once merged into the repository's default branch, the Issue can close automatically.

This gives you a traceable relationship between the problem and its implementation.

## 3. Understand the Issue lifecycle

A simple Issue lifecycle looks like this:

```text
Backlog
   |
   v
Issue created
   |
   v
Triaged and categorized
   |
   v
Assigned to developer
   |
   v
In progress
   |
   v
Pull Request created
   |
   v
Code review and testing
   |
   v
Pull Request merged
   |
   v
Issue closed
```

GitHub Issues have an open or closed state. Labels and project fields can represent more detailed workflow statuses.

For example:

- Open + `status:todo`
- Open + `status:in-progress`
- Open + `status:blocked`
- Closed + `status:done`

You can use labels for status, but GitHub Projects also provides dedicated Status fields. For a project board, prefer a Project Status field to represent workflow state rather than creating excessive status labels.

### 3.1 Open versus closed

**Open Issue:**

The work is not finished, or the discussion is still active.

**Closed Issue:**

The work is completed, rejected, duplicated, or otherwise no longer needs to remain open.

Closing an Issue does not delete it. You can reopen it if necessary.

## 4. Create your first Issue

We will use your training repository:

`github-deep-dive-training`

### Step 1 — Open the repository

1. Open your repository on GitHub.
2. Select the **Issues** tab.
3. Click **New issue**.
4. Select a template if the template chooser is displayed.

If you cannot see the Issues tab, check whether Issues are enabled in repository settings.

### Step 2 — Create a documentation Issue

Use this example:

**Title:**

```text
[DOCS] Add a GitHub workflow diagram to the repository documentation
```

**Description:**

```markdown
## Summary

Add a diagram that explains the development workflow used in this repository.

## Motivation

The training repository should demonstrate how developers work with branches,
commits, Pull Requests, reviews, and releases.

## Proposed changes

- Add a Git workflow diagram.
- Explain the relationship between local and remote branches.
- Show the Pull Request review process.
- Include the release workflow.

## Acceptance criteria

- [ ] Diagram is added.
- [ ] Diagram is readable.
- [ ] Workflow steps are correct.
- [ ] Documentation links are valid.
- [ ] Changes are reviewed.

## Additional information

This Issue is part of the GitHub Deep Dive training project.
```

Click **Submit new issue**.

GitHub assigns the Issue a number, for example:

```text
#15
```

Your actual Issue number will be different.

Keep that number. We will use it in later exercises.

### Step 3 — Inspect the Issue page

Explore these areas:

- Issue title and description.
- Comments and conversation.
- Assignees.
- Labels.
- Milestone.
- Projects.
- Development references.
- Timeline and events.

The available fields and layout can depend on repository permissions and account features.

## 5. Write high-quality Issues

A good Issue should explain the problem or requested work clearly enough that another developer can understand it without asking several basic questions.

### 5.1 Bug report structure

Use this structure:

```markdown
## Summary

A short explanation of the problem.

## Environment

- Backend:
- Frontend:
- Operating system:
- Browser:
- Application version:

## Current behavior

Explain what happens now.

## Expected behavior

Explain what should happen instead.

## Steps to reproduce

1. Open the application.
2. Navigate to the relevant page.
3. Perform the action.
4. Observe the result.

## Evidence

Add screenshots, logs, or relevant error messages.

## Acceptance criteria

- [ ] The problem is reproducible.
- [ ] The root cause is identified.
- [ ] The correction is implemented.
- [ ] Automated tests cover the correction.
```

### 5.2 Feature request structure

```markdown
## Summary

Describe the requested feature.

## Problem

What problem does this feature solve?

## Proposed solution

Explain the suggested implementation.

## Alternatives

Mention other possible solutions.

## Acceptance criteria

- [ ] Requirement one is implemented.
- [ ] Requirement two is implemented.
- [ ] Validation is included.
- [ ] Tests are added.
- [ ] Documentation is updated.

## Additional information

Add relevant references or context.
```

### 5.3 Technical task structure

```markdown
## Objective

Describe the technical task.

## Scope

- Task one.
- Task two.
- Task three.

## Implementation notes

Describe relevant technical decisions.

## Dependencies

List any required work.

## Acceptance criteria

- [ ] Implementation completed.
- [ ] Tests pass.
- [ ] Documentation updated.
- [ ] Pull Request reviewed.
```

### 5.4 Avoid vague Issue titles

Weak titles:

```text
Fix something
Update API
Improve frontend
Add feature
```

Better titles:

```text
[BUG] Prevent duplicate order submissions
[API] Add pagination to the product endpoint
[FEAT] Add product search to the cashier interface
[REFACTOR] Move order validation into a service
[TEST] Add integration tests for checkout
[DOCS] Document the authentication API
```

The prefix convention is optional, but it makes Issues easier to scan.

## 6. Understand labels

Labels categorize Issues and Pull Requests.

For example:

```text
bug
feature
enhancement
documentation
security
testing
backend
frontend
devops
priority:high
priority:medium
priority:low
```

Labels help you answer questions such as:

- How many bugs are open?
- Which Issues relate to the backend?
- Which tasks have high priority?
- Which Issues are documentation work?
- Which tasks are suitable for beginners?

### 6.1 Create labels

Open your repository:

1. Select **Issues**.
2. Open **Labels**.
3. Click **New label**.
4. Enter a name.
5. Add a description.
6. Select a color.
7. Save the label.

The exact placement of the Labels page may vary with the GitHub interface.

### 6.2 Recommended label system

For this training repository, create the following labels:

| Label | Purpose |
|---|---|
| `bug` | Something is not working |
| `feature` | New functionality |
| `enhancement` | Improve existing functionality |
| `documentation` | Documentation changes |
| `testing` | Test-related work |
| `security` | Security-related work |
| `backend` | Backend development |
| `frontend` | Frontend development |
| `devops` | Infrastructure and deployment |
| `priority:high` | High priority |
| `priority:medium` | Medium priority |
| `priority:low` | Low priority |
| `good first issue` | Suitable for newcomers |
| `help wanted` | Additional help is welcome |
| `blocked` | Cannot proceed yet |

You do not need to create every possible label in a real project. Keep the label system small and consistent.

### 6.3 Apply labels to your Issue

Open the documentation Issue you created earlier.

Apply:

```text
documentation
priority:medium
```

You can add more than one label to an Issue.

### 6.4 Label naming conventions

Choose a consistent naming convention.

For example:

```text
type:bug
type:feature
type:documentation

area:backend
area:frontend
area:database

priority:high
priority:medium
priority:low
```

Do not mix several naming systems without a reason.

For this training repository, either the simple labels or the grouped naming convention is acceptable. Pick one and document it.

## 7. Assign Issues to contributors

Assignees communicate who is responsible for an Issue.

For example:

```text
Issue #15
Assignee: @developer-one
```

A repository can have multiple contributors. Assigning work makes ownership visible.

### Recommended rules

- Assign one primary owner when possible.
- Assign additional people only when their involvement is meaningful.
- Do not assign every Issue to everyone.
- Reassign work when responsibility changes.
- Avoid leaving active work without an owner in a team project.

For your solo training repository, you can assign Issues to yourself if GitHub offers your account as an assignee.

Some assignment capabilities depend on repository type, collaborator access, and account permissions.

## 8. Understand milestones

A milestone groups Issues and Pull Requests around a target or release.

For example:

```text
Milestone: Module 1 — Code tab
```

You can associate several Issues and Pull Requests with this milestone.

As work is completed, GitHub displays milestone progress.

### 8.1 Milestones versus labels

They serve different purposes.

| Labels | Milestones |
|---|---|
| Categorize work | Group work toward a target |
| Can be reused across many projects | Represent a specific target |
| Examples: bug, backend, priority:high | Examples: Module 1, v1.1.0 |
| No inherent due date | Can have a due date |

### 8.2 Create a milestone

1. Open your repository.
2. Navigate to **Issues**.
3. Open **Milestones**.
4. Select **New milestone**.
5. Enter:

**Title:**

```text
Module 1 — Code tab
```

**Description:**

```text
Complete the GitHub Code tab training module, including practical exercises,
documentation, collaboration, and release preparation.
```

6. Set a due date if you have a meaningful deadline.
7. Create the milestone.

### 8.3 Associate Issues with the milestone

Open an Issue.

In the right sidebar, find **Milestone** and select:

```text
Module 1 — Code tab
```

You can also associate Pull Requests with milestones.

**Important:** A milestone is not the same as a Git tag or GitHub Release.

- Milestone: tracks planned work.
- Tag: identifies a specific Git commit.
- Release: publishes release information associated with a tag.

Continue using the tag and release workflow from Lesson 5. Use milestones to track the work required to reach those releases.

## 9. Break large Issues into smaller tasks

Some tasks are too large to implement as one unit.

For example:

```text
Issue #20 — Implement authentication
```

This could include:

- Create registration endpoint.
- Create login endpoint.
- Implement token refresh.
- Add password reset.
- Add authentication tests.
- Document authentication endpoints.

You can organize this work using task lists or sub-issues.

### 9.1 Use a Markdown task list

Inside an Issue description, write:

```markdown
## Tasks

- [ ] Create registration endpoint.
- [ ] Create login endpoint.
- [ ] Implement token refresh.
- [ ] Add password reset.
- [ ] Add authentication tests.
- [ ] Document authentication endpoints.
```

GitHub renders these as checkboxes.

You can check them off as work progresses.

### 9.2 Use sub-issues

Sub-issues provide a more structured hierarchy.

Example:

```text
Parent Issue:
Implement authentication

    Sub-issue #21:
    Create registration endpoint

    Sub-issue #22:
    Create login endpoint

    Sub-issue #23:
    Implement token refresh

    Sub-issue #24:
    Add password reset

    Sub-issue #25:
    Add authentication tests
```

Open the parent Issue and use its sub-issues section to add existing Issues or create new ones.

The exact controls depend on the GitHub interface and feature availability.

### 9.3 Task lists versus sub-issues

| Task list | Sub-issues |
|---|---|
| Simple checklist | Separate tracked Issues |
| Good for small implementation steps | Good for independently managed tasks |
| Tasks live inside one Issue | Each task has its own discussion and metadata |
| Minimal overhead | Better ownership and tracking |

Use task lists for small steps. Use sub-issues when tasks need separate owners, discussions, Pull Requests, or progress tracking.

## 10. Understand Issue dependencies

Sometimes an Issue cannot begin until another Issue is completed.

Example:

```text
Issue A: Design database schema
       |
       v
Issue B: Implement database models
       |
       v
Issue C: Create API endpoints
       |
       v
Issue D: Build frontend integration
```

Issue dependencies help communicate relationships such as:

- Issue B is blocked by Issue A.
- Issue C is blocked by Issue B.
- Issue D is blocked by Issue C.

Use dependency relationships when available in your repository's Issues interface.

Do not use dependencies for every task relationship. Reserve them for real blockers.

## 11. Link Pull Requests to Issues

This is one of the most useful GitHub features.

When a Pull Request implements an Issue, connect the two.

There are two approaches.

### 11.1 Use closing keywords in a Pull Request description

Suppose you have:

```text
Issue #15 — Add a GitHub workflow diagram
```

You create a Pull Request that implements it.

In the Pull Request description, add:

```markdown
## Summary

Adds the GitHub workflow diagram to the documentation.

## Changes

- Added the workflow diagram.
- Updated the repository documentation.

## Testing

- [x] Checked the Markdown rendering.
- [x] Reviewed the diagram.

Closes #15
```

GitHub supports these closing keywords:

```text
close
closes
closed

fix
fixes
fixed

resolve
resolves
resolved
```

Examples:

```text
Closes #15
Fixes #22
Resolves #31
```

You can reference multiple Issues:

```text
Closes #15, fixes #22, resolves #31
```

For an Issue in another repository, use:

```text
Fixes OWNER/REPOSITORY#100
```

### 11.2 Important behavior

Closing keywords automatically close the referenced Issue when the Pull Request is merged into the repository's default branch.

For example:

```text
Pull Request opened
       |
       v
Issue remains open
       |
       v
Pull Request reviewed
       |
       v
Pull Request merged into main
       |
       v
Issue automatically closed
```

The automatic closing behavior depends on the Pull Request targeting the default branch. If it targets another branch, the keyword does not automatically close the Issue at that point.

### 11.3 Link manually

You can also link an Issue to a Pull Request using the development section in the Issue or Pull Request sidebar.

This is useful when you want to show a relationship without automatically closing the Issue.

Use automatic closing keywords when the Pull Request fully resolves the Issue.

## 12. Search and filter Issues

When a repository has many Issues, manually browsing every page becomes inefficient.

GitHub supports search qualifiers.

### 12.1 Common filters

| Search query | Meaning |
|---|---|
| `is:open` | Open Issues and Pull Requests |
| `is:closed` | Closed Issues and Pull Requests |
| `is:issue` | Issues only |
| `is:pr` | Pull Requests only |
| `label:bug` | Items with the bug label |
| `assignee:@me` | Assigned to you |
| `no:assignee` | No assignee |
| `no:label` | No labels |
| `no:milestone` | No milestone |
| `milestone:"Module 1 — Code tab"` | Items in the specified milestone |

You can combine qualifiers.

Examples:

Find open bugs:

```text
is:issue is:open label:bug
```

Find open backend work:

```text
is:issue is:open label:backend
```

Find high-priority open Issues:

```text
is:issue is:open label:priority:high
```

Find Issues assigned to you:

```text
is:issue is:open assignee:@me
```

Find Issues without an owner:

```text
is:issue is:open no:assignee
```

Find work without a milestone:

```text
is:issue is:open no:milestone
```

You can use these filters in the Issues search field.

### 12.2 Why filtering matters

Imagine you have 150 open Issues.

Instead of reading all of them, you can find:

- High-priority bugs.
- Backend tasks.
- Documentation tasks.
- Issues assigned to you.
- Work that is blocked.
- Issues without an owner.

Good filtering becomes increasingly important as the repository grows.

## 13. GitHub Issue templates and forms

You created Issue templates in Lesson 6. Now you will understand how they fit into a real workflow.

Issue templates standardize the information contributors provide.

A bug template ensures that bug reports include reproduction steps and expected behavior.

A feature request template ensures that feature proposals explain the problem and acceptance criteria.

### 13.1 Markdown issue template

Example:

File:

```text
.github/ISSUE_TEMPLATE/bug_report.md
```

Content:

```markdown
---
name: Bug report
about: Report a problem in the application
title: "[BUG] "
labels: bug
assignees: ""
---

## Summary

Describe the problem.

## Environment

- Version:
- Operating system:
- Browser:

## Steps to reproduce

1.
2.
3.

## Expected behavior

Describe what should happen.

## Actual behavior

Describe what happens instead.

## Evidence

Add screenshots or logs.

## Acceptance criteria

- [ ] Problem is reproducible.
- [ ] Root cause is identified.
- [ ] Fix is implemented.
- [ ] Tests are added.
```

### 13.2 YAML issue form

GitHub also supports structured issue forms.

File:

```text
.github/ISSUE_TEMPLATE/bug_report.yml
```

Example:

```yaml
name: Bug report
description: Report a problem in the application
title: "[BUG] "
labels:
  - bug
body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a problem.
        Please provide enough information to reproduce it.

  - type: input
    id: summary
    attributes:
      label: Summary
      description: Describe the problem briefly.
      placeholder: Product search returns incorrect results
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to reproduce
      description: Explain how to reproduce the problem.
      placeholder: |
        1. Open the application.
        2. Navigate to products.
        3. Search for a product.
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual behavior
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Verification
      options:
        - label: I checked whether this issue already exists.
          required: true
        - label: I provided enough information to reproduce the problem.
          required: true
```

The YAML form provides structured fields and validation.

### 13.3 Configure the template chooser

You can add:

```text
.github/ISSUE_TEMPLATE/config.yml
```

Example:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://docs.github.com/
    about: Read the official GitHub documentation.
```

This example disables blank Issues and provides a documentation link.

For a real application, replace the example link with your own documentation or support destination.

**Important:** Use either a Markdown template or a YAML form for a particular template. Do not create duplicate templates with identical names and purposes.

## 14. GitHub Projects — Plan and track work

GitHub Projects provides a higher-level view of work across Issues and Pull Requests.

An Issue answers:

"What work needs to be done?"

A Project helps answer:

"What is the status of all the work, and what should happen next?"

You can use Projects to organize work into:

- Backlog.
- Todo.
- In Progress.
- In Review.
- Done.

Projects can be associated with a repository, an organization, or a user account.

### 14.1 Create a Project

1. Open the **Projects** area in GitHub.
2. Select **New project**.
3. Choose a starting layout.
4. Give it a name:

```text
GitHub Deep Dive — Development Board
```

5. Create the Project.

Depending on the interface, you may be able to choose a table, board, or roadmap layout.

### 14.2 Understand Project views

**Table view**

Useful when you need to inspect many work items and their metadata.

Example:

| Title | Status | Priority | Area |
|---|---|---|---|
| Add workflow diagram | Todo | Medium | Documentation |
| Create issue templates | Done | High | Documentation |
| Practice fork workflow | In Progress | Medium | Git |
| Study GitHub Actions | Backlog | High | DevOps |

**Board view**

Useful for visualizing workflow status.

```text
BACKLOG        TODO          IN PROGRESS       DONE
-------------------------------------------------------
Actions        Issue forms   Fork workflow     Branches
Projects       Git tags      PR review         Commits
```

**Roadmap view**

Useful for planning work across dates and time periods.

For this training repository, a table or board is sufficient.

### 14.3 Understand Project fields

Projects can contain fields such as:

| Field | Purpose |
|---|---|
| Status | Current workflow state |
| Priority | Importance of work |
| Assignees | Responsible people |
| Labels | Issue categories |
| Milestone | Release or target grouping |
| Start date | Planned start |
| Target date | Expected completion |
| Iteration | Time-boxed work period |

Some fields are built in; others can be configured.

### 14.4 Create a useful board

Create the following status values:

```text
Backlog
Todo
In Progress
In Review
Done
```

Add a Priority field:

```text
High
Medium
Low
```

Add an Area field:

```text
Backend
Frontend
Git
Documentation
DevOps
Testing
```

Add Issues from your repository to the Project.

Move an Issue between statuses as it progresses.

### 14.5 Understand the relationship between Issues and Projects

An Issue can belong to a Project.

A Project item can be an Issue or a Pull Request.

Project fields help you organize those items without changing the underlying Issue's open or closed state.

For example:

```text
Issue #15
  |
  +-- GitHub Issue state: Open
  |
  +-- Project status: In Progress
  |
  +-- Priority: Medium
  |
  +-- Area: Documentation
  |
  +-- Assignee: You
```

The Issue state and Project status are related, but they are not identical.

## 15. Plan a development project using Issues

Now apply everything to a realistic project.

Imagine you are developing a small restaurant POS application.

Your first release requires:

1. Product management.
2. Order management.
3. Cashier workflow.
4. Kitchen display.
5. Receipt printing.
6. Basic reporting.

Instead of implementing everything without a plan, create Issues.

### 15.1 Create an epic-level Issue

Title:

```text
[FEAT] Implement the restaurant order management module
```

Description:

```markdown
## Objective

Implement the order management module for the restaurant POS.

## Scope

- Create orders.
- Add products to orders.
- Update order quantities.
- Calculate order totals.
- Track order statuses.
- Support order cancellation.

## Sub-issues

- [ ] Create order database models.
- [ ] Create order API endpoints.
- [ ] Implement order validation.
- [ ] Implement order status transitions.
- [ ] Add automated tests.
- [ ] Document the API.

## Acceptance criteria

- [ ] Orders can be created.
- [ ] Products can be added to an order.
- [ ] Totals are calculated correctly.
- [ ] Invalid quantities are rejected.
- [ ] Order status transitions are validated.
- [ ] Tests cover the main use cases.
```

You can use the checklist initially and convert the larger tasks into sub-issues when they need independent tracking.

### 15.2 Create the smaller Issues

Create these Issues:

| Title | Labels | Priority |
|---|---|---|
| Create order database models | `backend`, `feature` | High |
| Create order API endpoints | `backend`, `feature` | High |
| Implement order validation | `backend`, `enhancement` | High |
| Implement order status transitions | `backend`, `feature` | Medium |
| Add order automated tests | `testing`, `backend` | High |
| Document order API endpoints | `documentation` | Medium |

Associate the Issues with the parent Issue when using sub-issues.

### 15.3 Add Issues to your Project

Add the parent Issue and its smaller tasks to your Project.

Set their statuses:

```text
Parent Issue:
Backlog

Database models:
Todo

API endpoints:
Backlog

Order validation:
Backlog

Order status transitions:
Backlog

Automated tests:
Backlog

API documentation:
Backlog
```

As you work, update the statuses.

### 15.4 Use milestones

Create:

```text
Milestone: Restaurant POS — v1.0.0
```

Associate the Issues required for the first release with this milestone.

This gives you a way to see how much work remains before the release.

## 16. GitHub CLI — Manage Issues from the terminal

GitHub CLI (`gh`) lets you interact with GitHub without opening the browser for every operation.

If you have not installed it, follow the official GitHub CLI installation instructions:

https://cli.github.com/

### 16.1 Authenticate

Check authentication:

```bash
gh auth status
```

If you have not authenticated:

```bash
gh auth login
```

Follow the interactive prompts.

### 16.2 List Issues

List open Issues:

```bash
gh issue list
```

List all Issues:

```bash
gh issue list --state all
```

Filter by label:

```bash
gh issue list --label bug
```

Filter by assignee:

```bash
gh issue list --assignee @me
```

Limit the number of results:

```bash
gh issue list --limit 20
```

### 16.3 View an Issue

```bash
gh issue view 15
```

Replace `15` with your actual Issue number.

Open it in the browser:

```bash
gh issue view 15 --web
```

### 16.4 Create an Issue

```bash
gh issue create
```

This opens an interactive workflow.

You can also provide the information directly:

```bash
gh issue create \
  --title "[DOCS] Add Git workflow documentation" \
  --body "Document the repository's Git workflow."
```

PowerShell users can enter the command on one line:

```powershell
gh issue create --title "[DOCS] Add Git workflow documentation" --body "Document the repository's Git workflow."
```

### 16.5 Create an Issue with labels and milestone

```bash
gh issue create \
  --title "[BUG] Fix product validation" \
  --body "Reject invalid product quantities." \
  --label "bug,backend" \
  --milestone "Module 1 — Code tab"
```

Make sure the labels and milestone already exist.

### 16.6 Edit an Issue

```bash
gh issue edit 15 --title "[DOCS] Update Git workflow guide"
```

Add a label:

```bash
gh issue edit 15 --add-label documentation
```

Remove a label:

```bash
gh issue edit 15 --remove-label documentation
```

### 16.7 Close and reopen an Issue

Close:

```bash
gh issue close 15
```

Reopen:

```bash
gh issue reopen 15
```

### 16.8 Understand the commands

| Command | Purpose |
|---|---|
| `gh auth status` | Check authentication |
| `gh issue list` | List Issues |
| `gh issue view 15` | View an Issue |
| `gh issue create` | Create an Issue |
| `gh issue edit 15` | Edit an Issue |
| `gh issue close 15` | Close an Issue |
| `gh issue reopen 15` | Reopen an Issue |

Practice the commands using your training repository.

## 17. Issue management best practices

Use these rules when working on real projects.

### Rule 1 — One Issue should represent a clear unit of work

Avoid combining unrelated tasks in one Issue.

### Rule 2 — Use acceptance criteria

Every implementation Issue should explain what completion means.

### Rule 3 — Avoid duplicate Issues

Search before creating a new Issue.

### Rule 4 — Use labels consistently

Create a small, understandable label system.

### Rule 5 — Assign ownership

Make responsibility clear when multiple contributors are involved.

### Rule 6 — Link Issues to Pull Requests

Use closing keywords when a Pull Request fully resolves an Issue.

### Rule 7 — Keep Projects updated

A Project board is useful only when its statuses reflect reality.

### Rule 8 — Close completed or rejected work

Do not leave finished Issues open indefinitely.

### Rule 9 — Use milestones for meaningful targets

Do not create a milestone for every small task.

### Rule 10 — Keep sensitive information out of Issues

Do not publish credentials, private customer data, or confidential information in public repositories.

---

## 18. Practical exercises

Complete these exercises in your `github-deep-dive-training` repository.

### Exercise A — Create and classify Issues

Create at least five Issues:

1. A bug report.
2. A feature request.
3. A documentation task.
4. A testing task.
5. A DevOps task.

For each Issue:

- [ ] Use a descriptive title.
- [ ] Write a useful description.
- [ ] Add acceptance criteria.
- [ ] Apply appropriate labels.
- [ ] Assign an owner where appropriate.
- [ ] Add it to the Module 1 milestone.

### Exercise B — Create a label system

Create these labels:

```text
bug
feature
enhancement
documentation
testing
backend
frontend
devops
priority:high
priority:medium
priority:low
blocked
```

Then:

- [ ] Apply labels to your Issues.
- [ ] Search for all open bugs.
- [ ] Search for high-priority work.
- [ ] Search for Issues without an assignee.
- [ ] Search for Issues without a milestone.

### Exercise C — Create a milestone

Create:

```text
Module 1 — Code tab
```

Then:

- [ ] Add your Module 1 Issues.
- [ ] Add relevant Pull Requests.
- [ ] Inspect milestone progress.
- [ ] Review which work remains open.

### Exercise D — Use task lists and sub-issues

Create a parent Issue:

```text
[FEAT] Prepare the GitHub training repository for collaboration
```

Break it down into:

- [ ] Add contribution documentation.
- [ ] Add Issue templates.
- [ ] Add Pull Request templates.
- [ ] Add security documentation.
- [ ] Document branch protection.
- [ ] Document the review workflow.

Practice both a Markdown task list and sub-issues if available.

### Exercise E — Create a Project board

Create:

```text
GitHub Deep Dive — Development Board
```

Configure:

```text
Backlog
Todo
In Progress
In Review
Done
```

Then:

- [ ] Add your Issues.
- [ ] Add relevant Pull Requests.
- [ ] Configure a Priority field.
- [ ] Configure an Area field.
- [ ] Move at least one Issue through the workflow.
- [ ] Create a filtered view for high-priority work.

### Exercise F — Link an Issue to a Pull Request

1. Select one of your open Issues.
2. Create a branch to implement it.
3. Make the required documentation change.
4. Commit your changes.
5. Push the branch.
6. Open a Pull Request.
7. Add the appropriate closing keyword, such as:

```text
Closes #15
```

8. Review the Pull Request.
9. Merge it into `main`.
10. Confirm that GitHub closes the linked Issue.

Use a real Issue number from your repository.

### Exercise G — Practice GitHub CLI

Run:

```bash
gh auth status
gh issue list
gh issue list --state all
gh issue list --label bug
gh issue list --assignee @me
gh issue view YOUR_ISSUE_NUMBER
```

Then create a test Issue using:

```bash
gh issue create
```

Finally, close or reopen the test Issue.

---

## 19. Lesson completion checklist

- [ ] I understand the purpose of GitHub Issues.
- [ ] I can distinguish Issues from Pull Requests.
- [ ] I can create useful bug reports and feature requests.
- [ ] I understand the Issue lifecycle.
- [ ] I can create and apply labels.
- [ ] I can assign Issues.
- [ ] I can create and use milestones.
- [ ] I understand task lists and sub-issues.
- [ ] I understand Issue dependencies.
- [ ] I can link Issues to Pull Requests.
- [ ] I understand automatic Issue closing keywords.
- [ ] I can search and filter Issues.
- [ ] I understand Markdown Issue templates and YAML forms.
- [ ] I can create and configure a GitHub Project.
- [ ] I can organize work using Project views and fields.
- [ ] I can manage Issues using GitHub CLI.
- [ ] I completed the practical exercises.

## 20. Commit and push this lesson

Return to your local `github-deep-dive-training` repository.

Check your current state:

```bash
git status
git branch
```

Update your local `main` branch:

```bash
git switch main
git pull origin main
```

Create a documentation branch:

```bash
git switch -c docs/add-issues-and-project-planning-lesson
```

Create:

```text
docs/github/module-01-code/lesson-10-issues-and-project-planning.md
```

Paste this lesson into the file.

Update:

```text
docs/github/module-01-code/README.md
```

Add Lesson 10 to the module index.

Review:

```bash
git status
git diff
```

Stage:

```bash
git add docs/github/module-01-code/
```

Inspect staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add issues and project planning lesson"
```

Push:

```bash
git push -u origin docs/add-issues-and-project-planning-lesson
```

Open a Pull Request into `main`.

Use the Pull Request collaboration and review workflow from Lesson 8.

## 21. Official documentation

Use these resources when practicing:

- [GitHub Issues quickstart](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart)
- [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [Creating an Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue)
- [Using labels and milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
- [Linking a Pull Request to an Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
- [Searching Issues and Pull Requests](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests)
- [GitHub Projects documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects)

## 22. What comes next?

**Lesson 11 — GitHub Discussions and Community Collaboration**

We will cover:

- GitHub Discussions versus Issues.
- Enabling Discussions.
- Categories and discussion formats.
- Questions, announcements, and ideas.
- Discussion answers and accepted answers.
- Converting Discussions into Issues.
- Community moderation and collaboration.
- When to use Discussions, Issues, and Pull Requests.
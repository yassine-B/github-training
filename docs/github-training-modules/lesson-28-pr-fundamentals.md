# Module 3 — GitHub Pull Requests

## Lesson 28 — Pull Requests Fundamentals: From Branch to Merge

**Level:** Intermediate
**Estimated time:** 3–4 hours
**Repository:** `github-deep-dive-training`
**Module:** 3 — GitHub Pull Requests
**Previous lesson:** Lesson 27 — Advanced Issues: Discussions, Triage, Lifecycle & Team Collaboration
**Next lesson:** Lesson 29 — Advanced Pull Request Reviews: Review Comments, Suggestions, Change Requests & Resolving Conversations

---

## 1. Lesson Overview

Welcome to Module 3.

In Module 1, you learned GitHub's Code tab, Git commands, branches, commits, tags, releases, and repository management.

In Module 2, you explored Issues, Discussions, triage, collaboration, and project management.

Now we'll study one of the most important features in professional software development: **Pull Requests (PRs).**

A Pull Request is the mechanism developers use to propose changes to a repository, discuss those changes, review code, run automated checks, and merge approved work.

Throughout this lesson, we'll use your `github-deep-dive-training` repository and a restaurant-management application as our practical example.

By the end, you'll have created and managed Pull Requests, explored their interface, practiced different merge strategies, and completed a documentation-based collaboration exercise.

### What you'll build

You will create:

```text
github-deep-dive-training/
│
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
│
└── docs/
    └── github/
        └── module-03-pull-requests/
            ├── lesson-28-pr-fundamentals.md
            ├── pr-fundamentals-demo.md
            ├── draft-demo.md
            └── team-workflow.md
```

You will also create several practice Pull Requests and inspect their resulting Git history.

---

## 2. Learning Objectives

By the end of this lesson, you should understand:

1. What Pull Requests are and why teams use them.
2. The Pull Request lifecycle.
3. Base branch versus compare branch.
4. How to create a Pull Request from a feature branch.
5. How to write meaningful PR titles and descriptions.
6. How Draft Pull Requests work.
7. How to inspect commits, checks, and file differences.
8. The difference between reviewers and assignees.
9. How PR labels and milestones work.
10. How to connect Issues to Pull Requests.
11. The three main GitHub merge strategies.
12. The three formal Pull Request review outcomes.
13. How repository settings can restrict merging.
14. How to practice a two-person review workflow.
15. How to publish a completed lesson using a PR, tag, and GitHub Release.

---

## 3. What Is a Pull Request?

Imagine you're developing a restaurant-management application.

Your main branch contains stable application code:

```text
main
```

You need to implement a new feature:

```text
feat/order-notifications
```

Instead of modifying `main` directly, you create a separate branch.

You implement the feature, create commits, and push your branch to GitHub.

Now you want to integrate your changes into `main`.

You create a Pull Request.

A Pull Request allows the team to:

- Understand the proposed changes.
- Review modified files.
- Discuss implementation decisions.
- Request modifications.
- Run automated tests.
- Approve the changes.
- Merge the changes into another branch.

### 3.1 Important terminology

| Term | Meaning |
|---|---|
| PR | Pull Request |
| Base branch | Branch receiving the proposed changes |
| Compare branch | Branch containing the proposed changes |
| Reviewer | Person reviewing the changes |
| Assignee | Person responsible for managing or completing the PR |
| Draft PR | PR that is not yet ready for formal review |
| Review | Formal assessment of proposed changes |
| Diff | Difference between the base and proposed changes |
| Merge | Integrating changes into the base branch |

### 3.2 Pull Request versus Git merge

These concepts are related, but they are not identical.

**Git merge** is a Git operation that integrates changes between branches.

**GitHub Pull Request** is a collaboration workflow that provides a place to discuss, review, validate, and eventually merge proposed changes.

A PR can exist before any merge takes place.

---

## 4. Why Development Teams Use Pull Requests

Consider two developers working on the same application.

### Without Pull Requests

```text
Developer A ────────┐
                    ├── Direct changes to main
Developer B ────────┘
```

This makes it difficult to control changes, review implementation decisions, and identify problems before integration.

### With Pull Requests

```text
                  main
                    |
          ┌─────────┴─────────┐
          |                   |
      feature-A           feature-B
          |                   |
       commits             commits
          |                   |
          v                   v
         PR A                PR B
          |                   |
       Review               Review
          |                   |
        Merge               Merge
          |                   |
          └─────────┬─────────┘
                    |
                   main
```

Pull Requests provide a controlled integration process.

### 4.1 Real-world benefits

| Benefit | Explanation |
|---|---|
| Code review | Other developers inspect proposed changes |
| Quality control | Problems can be identified before merging |
| Collaboration | Developers discuss implementation decisions |
| Traceability | Changes can be connected to Issues and commits |
| Automation | CI workflows can validate proposed changes |
| Documentation | PR descriptions preserve implementation context |
| Accountability | Teams can see who proposed, reviewed, and merged changes |

**Professional recommendation:** Use Pull Requests for meaningful changes, even when working alone. They provide a review checkpoint and preserve a clear development history.

---

## 5. Understand the Pull Request Lifecycle

A typical Pull Request follows this lifecycle:

```text
Create feature branch
        |
        v
Implement changes
        |
        v
Create commits
        |
        v
Push branch to GitHub
        |
        v
Open Pull Request
        |
        v
Review changes
        |
        v
Address feedback
        |
        v
Obtain approval
        |
        v
Merge Pull Request
        |
        v
Clean up feature branch
```

### 5.1 Lifecycle explained

| Step | Activity |
|---|---|
| 1 | Create a feature branch |
| 2 | Implement changes |
| 3 | Commit changes |
| 4 | Push the branch |
| 5 | Open a Pull Request |
| 6 | Review the changes |
| 7 | Address requested modifications |
| 8 | Obtain approval where required |
| 9 | Merge the Pull Request |
| 10 | Delete the merged branch if appropriate |

A Pull Request can also be closed without merging when the proposed changes are abandoned or no longer needed.

### 5.2 Pull Request states

| State | Meaning |
|---|---|
| Open | Awaiting review or merge |
| Draft | Open PR that is not ready for formal review |
| Merged | Changes successfully integrated |
| Closed | PR closed without merging, or otherwise no longer active |

**Important:** Draft is a readiness state within an open PR, not a separate merged/closed state.

---

## 6. Base Branch vs Compare Branch

This is one of the most important concepts in Pull Requests.

When opening a PR, GitHub asks you to select two branches.

### 6.1 Base branch

The destination branch.

Ask yourself:

> Where do I want my changes to go?

### 6.2 Compare branch

The source branch.

Ask yourself:

> Which branch contains the changes I want to propose?

Example:

```text
base:    main
compare: feat/order-notifications
```

This means:

> Propose integrating the changes from `feat/order-notifications` into `main`.

### 6.3 Common examples

| Scenario | Base | Compare |
|---|---|---|
| Feature implementation | `main` | `feat/login` |
| Bug fix | `main` | `fix/payment-total` |
| Documentation | `main` | `docs/api-guide` |
| Release preparation | `main` | `release/v1.0.0` |
| Development integration | `develop` | `feat/orders` |

Base and compare can be reversed depending on your workflow. Always check the direction before creating a PR.

### 6.4 Exercise — Identify base and compare

For each scenario, identify the base and compare branches.

#### Scenario A

You are adding a product search feature to the application.

```text
main
feat/product-search
```

#### Scenario B

You are fixing a cashier calculation bug.

```text
main
fix/cashier-total
```

#### Scenario C

Your team uses `develop` as its integration branch. You want to integrate an order-management feature.

```text
develop
feat/order-management
```

Write your answers in your lesson notes.

---

## 7. Practical Exercise 1 — Create Your First Pull Request

We'll create a documentation-only PR to avoid modifying any real application code.

### Step 1 — Open your local repository

Navigate to your cloned repository:

```powershell
cd github-deep-dive-training
```

Make sure your local `main` branch is synchronized:

```bash
git switch main
git pull origin main
```

### Step 2 — Create a feature branch

```bash
git switch -c docs/lesson-28-pr-fundamentals
```

Verify the active branch:

```bash
git branch
```

Expected:

```text
* docs/lesson-28-pr-fundamentals
  main
```

### Step 3 — Create a practice file

Create:

```text
docs/github/module-03-pull-requests/pr-fundamentals-demo.md
```

Content:

```markdown
# Pull Request Fundamentals Demo

## Purpose

This file demonstrates the Pull Request workflow.

## What I learned

- Creating feature branches
- Committing changes
- Pushing branches to GitHub
- Opening Pull Requests
- Reviewing changes
- Merging Pull Requests

## Practical objective

Understand how proposed changes move from a
feature branch into the main branch.
```

### Step 4 — Inspect and commit your changes

```bash
git status
git diff --check

git add docs/github/module-03-pull-requests/pr-fundamentals-demo.md

git diff --cached

git commit -m "docs(github): add pull request fundamentals demo"
```

### Step 5 — Push your branch

```bash
git push -u origin docs/lesson-28-pr-fundamentals
```

Your branch is now available on GitHub.

### Step 6 — Create the Pull Request

Open your repository:

[GitHub deep-dive training repository](https://github.com/yassine-B/github-deep-dive-training)

Navigate to:

#### Pull requests → New pull request

Select:

| Field | Value |
|---|---|
| Base | `main` |
| Compare | `docs/lesson-28-pr-fundamentals` |

Check that the direction is correct.

Click **Create pull request**.

### Step 7 — Write the PR title

Use a descriptive title following your Conventional Commits convention:

```text
docs(github): add Lesson 28 PR fundamentals demo
```

### Step 8 — Write the PR description

```markdown
## Summary

Add a practical demonstration of the GitHub Pull Request workflow.

## Changes

- Added Pull Request fundamentals documentation.
- Demonstrated the feature branch workflow.
- Documented the PR creation process.
- Prepared the repository for advanced PR exercises.

## Testing

- [x] Markdown file created
- [x] Git diff checked
- [x] Commit created
- [x] Branch pushed

## Related Issues

None.

## Additional context

Documentation-only training exercise.
```

Click **Create pull request**.

Congratulations: you've created your first PR for Module 3.

---

## 8. Understanding the Pull Request Interface

A Pull Request page contains several important sections.

Let's examine them.

### 8.1 Conversation

The Conversation tab is the central discussion area.

It contains:

- PR description.
- General comments.
- Review summaries.
- Review requests.
- Linked Issues.
- Merge status.
- Activity timeline.

Use this section for discussions that concern the overall implementation.

### 8.2 Commits

The Commits section lists commits included in the Pull Request.

Example:

```text
a82f491 docs(github): add pull request fundamentals demo
b194c12 docs(github): update repository guide
```

You can inspect:

- Commit messages.
- Commit authors.
- Commit timestamps.
- Individual commit changes.

Why is this useful?

Suppose a developer creates ten commits while implementing a feature. A reviewer can inspect how the implementation evolved rather than only seeing the final result.

### 8.3 Checks

The Checks section displays automated validations associated with the PR.

Examples:

- GitHub Actions workflows.
- Automated tests.
- Linting.
- Code quality checks.
- Security scanning.

Possible results:

| Status | Meaning |
|---|---|
| Success | Check passed |
| Failure | Check failed |
| Pending | Check is running |
| Skipped | Check did not run |
| Neutral | Check completed without a success/failure conclusion |

A PR can be prevented from merging when repository rules require particular checks to pass.

**Important:** If your repository does not have a workflow configured for the PR, you may not see meaningful automated checks yet. This is expected. We'll study GitHub Actions in a later module.

### 8.4 Files changed

This is one of the most important sections for reviewers.

It shows the differences between the proposed changes and the base branch.

GitHub uses familiar diff conventions:

- Green lines indicate additions.
- Red lines indicate removals.
- Context lines show surrounding unchanged code.

Example:

Before:

```python
def calculate_total(items):
    return sum(item.price for item in items)
```

Proposed change:

```python
def calculate_total(items):
    subtotal = sum(item.price for item in items)
    return subtotal
```

You can:

- Review changed files.
- Switch between unified and split diff views.
- Add comments to specific lines.
- Mark files as viewed.
- Review the complete change set.

### Exercise 2 — Explore the PR tabs

Open the PR you just created.

Visit:

1. Conversation.
2. Commits.
3. Checks.
4. Files changed.

Record what each section displays.

Suggested notes:

```markdown
# Pull Request Interface Notes

## Conversation

What information appears here?

## Commits

How many commits are included?

## Checks

Are automated checks configured?

## Files changed

Which files were modified?
```

---

## 9. Pull Request Title Conventions

A PR title should communicate the purpose of the change without requiring someone to open the description.

Since you already use Conventional Commits, continue the same convention.

| Type | Example PR title |
|---|---|
| Feature | `feat(orders): add order filtering` |
| Bug fix | `fix(auth): correct token refresh handling` |
| Documentation | `docs(github): explain PR workflow` |
| Refactoring | `refactor(api): simplify response handling` |
| Testing | `test(orders): add order validation tests` |
| Build | `build(docker): update compose configuration` |
| CI | `ci(github): add backend test workflow` |

### 9.1 Recommended PR title format

```text
type(scope): short description
```

Examples:

```text
feat(kds): add ready-order notifications

fix(payments): correct refund calculation

docs(api): document authentication endpoints

test(orders): cover order creation scenarios
```

Avoid titles such as:

```text
Changes
Update
Fix stuff
New code
Final version
```

They provide little information when browsing PR history.

### Exercise 3 — Write five PR titles

Write a suitable PR title for each restaurant-application task:

1. New product management feature.
2. Fix incorrect cashier totals.
3. Update API documentation.
4. Add automated backend tests.
5. Improve Docker configuration.

Use the format:

```text
type(scope): short description
```

---

## 10. Pull Request Descriptions and Templates

A PR description explains the purpose, scope, implementation, and validation of the changes.

A useful description should answer:

1. What problem does this PR solve?
2. What changed?
3. How was it tested?
4. Are there important limitations?
5. Which Issues are related?

### 10.1 Create a reusable PR template

Create:

```text
.github/PULL_REQUEST_TEMPLATE.md
```

Content:

```markdown
## Summary

Explain what this Pull Request accomplishes.

## Related Issue

Closes #

## Changes

-
-
-

## Implementation details

Explain important technical decisions.

## Testing

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Linting
- [ ] Build verification

## Screenshots

Add screenshots if applicable.

## Breaking changes

- [ ] This PR introduces breaking changes.

If yes, explain them here.

## Checklist

- [ ] Code follows repository standards.
- [ ] Documentation updated.
- [ ] Tests added or updated.
- [ ] No unnecessary files included.
- [ ] Changes reviewed locally.
```

### 10.2 What happens after adding this file?

GitHub can automatically populate the description field when someone creates a new Pull Request.

The template does not enforce that contributors complete every checkbox. For enforcement, use repository rules, required checks, or other automation where appropriate.

### 10.3 Exercise 4 — Test your PR template

1. Create the template file.
2. Commit it on a separate branch.
3. Push the branch.
4. Open a new PR.
5. Verify that GitHub displays the template.
6. Inspect the generated description.
7. Merge the PR when finished.

---

## 11. Draft Pull Requests

A Draft Pull Request is an open PR that is not yet ready for formal review.

Imagine you're implementing a large feature:

```text
feat: implement restaurant order management
```

You have completed:

- Database models.
- Basic API endpoints.

But you haven't completed:

- Validation.
- Automated tests.
- Frontend integration.

You want feedback early without asking reviewers to approve unfinished work.

This is where Draft PRs are useful.

### 11.1 Create a Draft PR

When creating a PR, select:

#### Create draft pull request

GitHub marks the PR as Draft.

### 11.2 Draft versus regular PR

| Draft PR | Regular PR |
|---|---|
| Work is in progress | Ready for formal review |
| Not ready for final approval | Can receive formal approval |
| Communicates incomplete status | Communicates review readiness |
| Can receive early feedback | Can proceed toward merging |

Draft PRs cannot be merged until they are marked ready for review.

### 11.3 Convert a Draft PR into a regular PR

When implementation is ready:

1. Open the Draft PR.
2. Review the remaining work.
3. Click **Ready for review**.
4. GitHub changes the PR from Draft to an ordinary open PR for review.

### Exercise 5 — Create a Draft PR

Create a second branch:

```bash
git switch main
git pull origin main

git switch -c docs/draft-pr-practice
```

Create:

```text
docs/github/module-03-pull-requests/draft-demo.md
```

Content:

```markdown
# Draft Pull Request Practice

This document demonstrates draft Pull Requests.

## Current progress

- [x] Initial documentation
- [ ] Complete examples
- [ ] Review content
- [ ] Finalize documentation
```

Commit and push:

```bash
git add docs/github/module-03-pull-requests/draft-demo.md

git commit -m "docs(github): add draft PR practice"

git push -u origin docs/draft-pr-practice
```

Create a Draft PR.

After reviewing the example, mark it ready for review.

Then merge it when you're finished.

---

## 12. Reviewers and Assignees

Reviewers and assignees have different responsibilities.

### 12.1 Reviewers

A reviewer examines the proposed changes and provides feedback.

Typical responsibilities:

- Inspect the diff.
- Identify bugs.
- Check coding standards.
- Evaluate implementation decisions.
- Approve or request changes.

Depending on repository configuration, reviewers can be individual users or teams.

### 12.2 Assignees

An assignee is responsible for managing or completing the PR work.

| Role | Responsibility |
|---|---|
| PR author | Implements the changes |
| PR assignee | Coordinates the PR work |
| Reviewer | Examines the proposed changes |
| Maintainer | Oversees repository integration |

One person may have more than one role.

### 12.3 Request a reviewer

Open your PR.

Find the **Reviewers** section in the sidebar.

Select a reviewer.

The reviewer receives a notification according to their notification settings.

For your training repository, you can use a second GitHub account that you control or a trusted collaborator.

If you're the only contributor, you can still inspect the reviewer interface, but don't treat self-review as a substitute for practicing independent review.

### 12.4 CODEOWNERS — advanced introduction

GitHub supports automatic reviewer assignment through a `CODEOWNERS` file.

Create:

```text
.github/CODEOWNERS
```

Example:

```text
# Default repository owners
* @yassine-B

# Backend code
/backend/ @backend-team

# Frontend code
/frontend/ @frontend-team

# Documentation
/docs/ @documentation-team

# GitHub Actions
/.github/workflows/ @devops-team
```

These team names are illustrative. The referenced teams must exist and have appropriate repository access.

When a PR changes files covered by CODEOWNERS rules, GitHub can request reviews from the relevant owners, subject to repository configuration.

We'll study CODEOWNERS and branch protection in greater depth in a later lesson.

### Exercise 6 — Explore reviewers and assignees

On your first PR:

1. Assign yourself.
2. Inspect the reviewer selection.
3. Request a reviewer if you have an eligible collaborator.
4. Explore the CODEOWNERS example.
5. Record the difference between an assignee and a reviewer.

---

## 13. PR Labels and Milestones

Pull Requests support labels and milestones, just like Issues.

Labels help categorize PRs.

### 13.1 Suggested labels

| Label | Purpose |
|---|---|
| `type: feature` | New functionality |
| `type: bug` | Bug fix |
| `type: documentation` | Documentation |
| `priority: high` | Important changes |
| `needs-review` | Awaiting review |
| `blocked` | Cannot proceed |
| `breaking-change` | Potential compatibility impact |
| `dependencies` | Dependency updates |

### 13.2 Milestones

A milestone can group related PRs into a release or training checkpoint.

Example:

```text
Module 3 — Pull Requests
```

Assign your Lesson 28 PR to this milestone if you have created it.

### Exercise 7 — Organize your PR

Add:

- Two labels.
- One milestone.
- One assignee.

Inspect how these fields appear in the PR sidebar.

---

## 14. Linking Issues to Pull Requests

This is an important connection between Module 2 and Module 3.

Suppose you have an Issue:

```text
#45
bug: cashier total is incorrect after refund
```

You create a branch:

```bash
git switch -c fix/45-cashier-refund-total
```

You implement the fix and open a PR.

In the PR description:

```markdown
## Summary

Correct the cashier daily total calculation.

## Changes

- Corrected refund aggregation.
- Updated the relevant calculation.
- Added a regression test.

## Related Issue

Closes #45
```

When the PR is merged into the repository's default branch, GitHub automatically closes Issue #45.

### 14.1 Linking keywords

| Keyword | Purpose |
|---|---|
| `Closes #45` | Automatically closes the Issue on merge |
| `Fixes #45` | Automatically closes the Issue on merge |
| `Resolves #45` | Automatically closes the Issue on merge |
| `References #45` | Creates a reference |
| `Related to #45` | Indicates a relationship |

### 14.2 Important distinction

If you write:

```text
This PR is related to #45.
```

GitHub creates a reference but does not automatically close the Issue.

If you write:

```text
Closes #45
```

GitHub recognizes a closing keyword.

**Important:** Automatic closing keywords work when the PR is merged into the default branch. If the PR targets another branch, the Issue may not close at that point.

### Exercise 8 — Link an Issue to a PR

Use one of the Issues created in Lesson 26 or Lesson 27.

1. Create a branch.
2. Make a documentation change related to that Issue.
3. Commit your changes.
4. Open a PR.
5. Include `Closes #ISSUE_NUMBER`.
6. Merge the PR into the default branch.
7. Verify that the Issue closes.

If the earlier Issue is already closed, create a new practice Issue for this exercise.

---

## 15. Merge Strategies

Once a PR is approved and its required checks pass, it can be merged.

GitHub offers three commonly used merge methods.

### 15.1 Merge commit

A merge commit combines the changes from the feature branch into the base branch while preserving the branch history.

Illustrative history:

```text
A---B---------M  main
     \       /
      C---D     feature
```

**Advantages:**

- Preserves individual commits.
- Preserves branch integration history.
- Useful when detailed branch history matters.

**Disadvantages:**

- Can create a more complex Git history.
- Many small PRs can produce numerous merge commits.

### 15.2 Squash and merge

Squash and merge combines all commits from the PR into one commit on the base branch.

Before:

```text
main:
A --- B

feature:
     \--- C --- D --- E
```

After:

```text
main:
A --- B --- F
```

Where F represents the combined changes.

**Advantages:**

- Cleaner main branch history.
- Removes temporary development commits.
- Useful for small feature branches.

**Disadvantages:**

- Individual feature-branch commits are not preserved as separate commits on the base branch.
- Detailed commit progression is less visible in the main branch.

### 15.3 Rebase and merge

Rebase and merge applies the feature branch commits onto the latest base branch without creating a merge commit.

Before:

```text
main:
A --- B

feature:
     \--- C --- D
```

After:

```text
A --- B --- C' --- D'
```

The commits are replayed and receive new commit IDs.

**Advantages:**

- Linear history.
- Preserves individual commits.
- Avoids merge commits.

**Disadvantages:**

- Commit identities change.
- Requires care when working with shared branches.

### 15.4 Compare the three strategies

| Feature | Merge commit | Squash and merge | Rebase and merge |
|---|---|---|---|
| Preserves separate commits on base | Yes | No | Yes |
| Creates merge commit | Yes | No | No |
| Linear history | Not necessarily | Yes | Yes |
| Preserves branch integration topology | Yes | No | No |
| Good for detailed branch history | Yes | Less suitable | Yes |
| Good for compact main history | Less suitable | Yes | Yes |

### 15.5 Which strategy should you use?

For your training repository, practice all three.

For a typical team:

- **Squash and merge:** Good when each PR should produce one clean commit.
- **Merge commit:** Good when preserving feature branch integration history is important.
- **Rebase and merge:** Good when the team prefers linear history and meaningful individual commits.

The correct choice depends on repository conventions.

**Important:** The repository administrator controls which merge methods are enabled under **Settings → General → Pull Requests**.

### Exercise 9 — Compare merge strategies

Create three small documentation PRs.

| PR | Merge method |
|---|---|
| PR A | Create a merge commit |
| PR B | Squash and merge |
| PR C | Rebase and merge |

After each merge:

1. Open the repository's Code tab.
2. Inspect the commit history.
3. Compare the resulting commits.
4. Record what changed.

Do not reuse the same branch for all three experiments.

Use a different feature branch for each PR.

If a merge method is disabled in your repository, record that limitation and inspect its configuration rather than assuming it is available.

---

## 16. Pull Request Reviews — Introduction

A review is a formal assessment of a Pull Request.

GitHub supports three primary review outcomes.

### 16.1 Comment

The reviewer provides feedback without approving or requesting changes.

Example:

```text
The documentation looks good.

Could you add an example showing how the
feature branch is synchronized with main?
```

### 16.2 Approve

The reviewer approves the proposed changes.

Example:

```text
The implementation looks good.

- Documentation is clear.
- Examples are understandable.
- No blocking issues found.

Approved.
```

### 16.3 Request changes

The reviewer identifies changes that should be addressed before approval.

Example:

```text
Changes requested:

1. Add the missing setup instructions.
2. Correct the incorrect branch name.
3. Include an example of the merge workflow.
```

The author can then update the branch and request another review.

### 16.4 Review comments versus general comments

| General PR comment | Review comment |
|---|---|
| Discusses the overall PR | Discusses a specific change |
| Appears in Conversation | Can be attached to a changed line |
| Does not represent a formal review decision | Can be submitted with a review decision |

### Exercise 10 — Explore PR reviews

Open your documentation PR.

Practice:

1. Add a general comment.
2. Open Files changed.
3. Add a comment to a specific line.
4. Explore the review submission options.
5. If you have a collaborator, ask them to submit a review.

Do not approve your own PR as a replacement for independent review.

We'll explore detailed review comments and suggestions in Lesson 29.

---

## 17. Understanding Merge Requirements

A PR being approved does not necessarily mean GitHub will allow it to merge.

Repositories can configure additional requirements.

Examples:

| Requirement | Purpose |
|---|---|
| Required reviews | Ensure changes receive approval |
| Required status checks | Ensure automated validations pass |
| Conversation resolution | Ensure review discussions are addressed |
| Branch up-to-date requirement | Ensure changes are tested against the latest base |
| Signed commits | Enforce commit-signing policies where configured |
| Linear history | Prevent merge commits where required |

These controls are generally configured through repository rulesets or branch protection rules, depending on the GitHub configuration.

### 17.1 Example

Imagine a repository requires:

- One approving review.
- All required CI checks to pass.
- All review conversations to be resolved.

Your PR might display:

| Requirement | Status |
|---|---|
| Review approval | Passed |
| Backend tests | Passed |
| Frontend tests | Pending |
| Conversations | Resolved |

Illustrative example: merging remains blocked while a required check is pending.

We'll explore branch protection, rulesets, required checks, and enforcement in a dedicated advanced lesson.

---

## 18. Two-Person Collaboration Exercise

This is one of the most important practical exercises in this module.

We'll simulate a professional development team.

### 18.1 Scenario

You are Developer A.

Another contributor is Developer B.

The task is to add a new documentation section to your repository.

### 18.2 Developer A — Author

Create the branch:

```bash
git switch main
git pull origin main

git switch -c docs/team-pr-workflow
```

Create:

```text
docs/github/module-03-pull-requests/team-workflow.md
```

Content:

```markdown
# Team Pull Request Workflow

## Development process

1. Create a feature branch.
2. Implement the required changes.
3. Run local validation.
4. Commit the changes.
5. Push the branch.
6. Create a Pull Request.
7. Request a review.
8. Address review feedback.
9. Obtain approval.
10. Merge the Pull Request.

## Review responsibilities

The reviewer should verify:

- Correctness.
- Maintainability.
- Documentation.
- Test coverage.
- Security considerations.
```

Commit:

```bash
git add docs/github/module-03-pull-requests/team-workflow.md

git commit -m "docs(github): add team PR workflow"

git push -u origin docs/team-pr-workflow
```

Create a PR with:

```text
Title:
docs(github): add team PR workflow
```

Request Developer B as reviewer.

### 18.3 Developer B — Reviewer

Developer B should:

1. Open the PR.
2. Read its description.
3. Inspect the Files changed tab.
4. Review the documentation.
5. Add at least two comments.
6. Submit a review requesting changes.

Example review feedback:

```text
## Requested improvements

1. Add instructions about resolving review comments.
2. Explain when to use Draft PRs.
```

### 18.4 Developer A — Address feedback

Update the documentation.

```bash
git add docs/github/module-03-pull-requests/team-workflow.md

git commit -m "docs(github): address PR review feedback"

git push
```

The existing PR automatically receives the new commit.

### 18.5 Developer B — Final review

Developer B should:

1. Inspect the latest changes.
2. Verify the requested modifications.
3. Submit an approval.
4. Confirm the review conversations are resolved.

### 18.6 Developer A — Merge

Merge the PR using your chosen merge strategy.

Delete the feature branch if it is no longer needed.

### Expected collaboration lifecycle

1. Developer A creates a branch.
2. Developer A opens a PR.
3. Developer B reviews the changes.
4. Developer B requests modifications.
5. Developer A updates the PR.
6. Developer B approves the PR.
7. Developer A merges the PR.

If you do not have a second account or collaborator, ask a trusted collaborator to participate.

You can also practice the author side independently, but the formal review and approval exercise requires another eligible reviewer.

---

## 19. Additional Pull Request Features to Explore

There are several other features you'll encounter while working with PRs.

| Feature | Purpose |
|---|---|
| PR timeline | Tracks activity and events |
| Review requests | Requests feedback from people or teams |
| Suggested reviewers | Helps identify potential reviewers |
| Auto-merge | Merges automatically once configured requirements are satisfied |
| Merge queue | Queues PRs for integration and validation |
| Conversation resolution | Tracks whether review discussions are resolved |
| PR notifications | Keeps participants informed |
| Branch deletion | Cleans up merged feature branches |
| PR references | Connects PRs to Issues and other work |

### 19.1 Auto-merge

Auto-merge allows a PR to merge automatically when the configured merge requirements are satisfied.

Example:

```text
PR opened
   |
   v
Review requested
   |
   v
Approval received
   |
   v
CI checks pass
   |
   v
Auto-merge
   |
   v
PR merged
```

Availability depends on repository configuration and permissions.

Auto-merge does not mean that a PR is merged immediately. The configured conditions must first be satisfied.

### 19.2 Merge queue

Merge queues help repositories manage multiple PRs waiting to enter a protected branch.

Instead of merging every approved PR immediately, GitHub can queue changes and validate them against the target branch and other queued changes.

This is particularly useful in busy repositories where several contributors merge frequently.

### 19.3 Delete merged branches

After merging, GitHub often offers a **Delete branch** option.

This removes the remote feature branch, not the merged commits.

The local branch remains until you delete it locally:

```bash
git branch -d docs/team-pr-workflow
```

If the remote branch was already deleted:

```bash
git fetch --prune
```

Avoid deleting branches that still contain work you need.

---

## 20. Practical Assessment — Pull Request Management

Now complete this exercise using your training repository.

Your objective is to demonstrate the complete PR lifecycle.

### Assessment checklist

- [ ] Create a feature branch from `main`.
- [ ] Make a documentation change.
- [ ] Create a meaningful commit.
- [ ] Push the branch to GitHub.
- [ ] Open a regular Pull Request.
- [ ] Write a descriptive PR title.
- [ ] Complete the PR description.
- [ ] Inspect Conversation, Commits, Checks, and Files changed.
- [ ] Assign the PR.
- [ ] Add labels and a milestone.
- [ ] Request an independent reviewer if available.
- [ ] Submit or receive review comments.
- [ ] Address review feedback.
- [ ] Obtain approval where possible.
- [ ] Merge using one of the three merge strategies.
- [ ] Inspect the resulting Git history.
- [ ] Delete the merged remote branch.
- [ ] Verify the final repository state.

### Assessment deliverables

By the end, you should have:

1. At least one regular PR.
2. At least one Draft PR.
3. A reusable PR template.
4. An example of a linked Issue.
5. A comparison of the three merge strategies.
6. A completed collaboration exercise or a documented individual simulation.
7. Notes describing the PR interface.

---

## 21. Lessons Learned

Before moving to the next lesson, make sure you can explain these concepts without looking at the documentation.

| Concept | What you should understand |
|---|---|
| Pull Request | A workflow for proposing and reviewing changes |
| Base branch | Destination branch |
| Compare branch | Source branch containing proposed changes |
| Draft PR | Open PR not ready for formal review |
| Reviewer | Person assessing proposed changes |
| Assignee | Person responsible for coordinating the PR |
| Files changed | View showing proposed differences |
| PR template | Reusable description structure |
| Issue linking | Connects PR work to tracked tasks |
| Merge commit | Preserves branch integration history |
| Squash merge | Combines PR commits into one base-branch commit |
| Rebase merge | Replays individual commits onto the base branch |
| Approval | Formal positive review outcome |
| Required checks | Automated conditions that may block merging |
| Auto-merge | Merges after configured requirements are satisfied |
| Merge queue | Coordinates integration of multiple PRs |

### Reflection questions

1. Why should developers avoid making every change directly on `main`?
2. What is the difference between a base branch and a compare branch?
3. When would you create a Draft PR?
4. What is the difference between a reviewer and an assignee?
5. What is the difference between a merge commit and squash merge?
6. Why might a PR remain unmergeable after approval?
7. How does `Closes #45` differ from `References #45`?
8. Why is independent review important in a two-person team?

---

## 22. Completion Checklist

### Concepts

- [ ] I understand Pull Requests.
- [ ] I understand the PR lifecycle.
- [ ] I understand base and compare branches.
- [ ] I understand the PR interface.
- [ ] I understand Draft PRs.
- [ ] I understand reviewers and assignees.
- [ ] I understand labels and milestones.
- [ ] I understand how PRs link to Issues.
- [ ] I understand the three merge strategies.
- [ ] I understand the formal review outcomes.

### Practical work

- [ ] I created my first PR.
- [ ] I explored all four main PR tabs.
- [ ] I created a PR template.
- [ ] I created a Draft PR.
- [ ] I practiced linking an Issue.
- [ ] I practiced merge strategies.
- [ ] I explored reviewer assignment.
- [ ] I completed the collaboration exercise or documented its limitations.
- [ ] I completed the assessment.

### Repository workflow

- [ ] I created the lesson documentation.
- [ ] I used a dedicated documentation branch.
- [ ] I followed Conventional Commits.
- [ ] I pushed the branch.
- [ ] I created and merged the documentation PR.
- [ ] I created the training tag.
- [ ] I created the GitHub Release.

---

## 23. Lesson Documentation

Create the following files:

```text
docs/
└── github/
    └── module-03-pull-requests/
        ├── lesson-28-pr-fundamentals.md
        ├── pr-fundamentals-demo.md
        ├── draft-demo.md
        └── team-workflow.md
```

Also create:

```text
.github/
└── PULL_REQUEST_TEMPLATE.md
```

For `lesson-28-pr-fundamentals.md`, organize the documentation using:

```markdown
# Lesson 28 — Pull Requests Fundamentals

## 1. Learning Objectives

## 2. What Is a Pull Request?

## 3. Why Development Teams Use PRs

## 4. Pull Request Lifecycle

## 5. Base Branch vs Compare Branch

## 6. Creating Your First PR

## 7. Understanding the PR Interface

## 8. PR Title Conventions

## 9. PR Descriptions and Templates

## 10. Draft Pull Requests

## 11. Reviewers and Assignees

## 12. PR Labels and Milestones

## 13. Linking Issues to PRs

## 14. Merge Strategies

## 15. Pull Request Reviews

## 16. Merge Requirements

## 17. Two-Person Collaboration

## 18. Additional PR Features

## 19. Practical Assessment

## 20. Lessons Learned

## 21. Completion Checklist

## 22. References
```

Include screenshots from your actual repository exercises where useful.

Suggested screenshots:

- Your first open PR.
- The PR Conversation tab.
- The Commits tab.
- The Files changed tab.
- Your PR template in use.
- Your Draft PR.
- The merge method selection.
- The final merged PR.

Do not use screenshots of hypothetical results as evidence of completed exercises.

---

## 24. Git Workflow — Commit, PR, Tag and Release

After completing the practical exercises, publish the lesson documentation.

### Step 1 — Synchronize main and create your documentation branch

```bash
git switch main
git pull origin main

git switch -c docs/lesson-28-pr-fundamentals
```

### Step 2 — Add your documentation

```bash
git add docs/github/module-03-pull-requests/
git add .github/PULL_REQUEST_TEMPLATE.md
```

If you created a CODEOWNERS file during the exercise, add it as well:

```bash
git add .github/CODEOWNERS
```

### Step 3 — Validate

```bash
git status
git diff --check
git diff --cached
```

Check that you are not committing screenshots, generated files, or unrelated changes accidentally.

### Step 4 — Commit

```bash
git commit -m "docs(github): add Lesson 28 pull request fundamentals"
```

### Step 5 — Push

```bash
git push -u origin docs/lesson-28-pr-fundamentals
```

### Step 6 — Create your documentation PR

**PR title:**

```text
docs(github): add Lesson 28 pull request fundamentals
```

**PR description:**

```markdown
## Summary

Add Lesson 28 covering GitHub Pull Requests.

## Topics

- PR fundamentals and lifecycle
- Base and compare branches
- PR interface
- PR descriptions and templates
- Draft PRs
- Reviewers and assignees
- Labels and milestones
- Issue integration
- Merge strategies
- Reviews and merge requirements
- Two-person collaboration

## Checklist

- [ ] Documentation added
- [ ] PR template added
- [ ] Markdown validated
- [ ] Practical exercises completed
- [ ] Screenshots included where useful
- [ ] No unrelated files included
```

Review and merge your PR.

### Step 7 — Synchronize main and create the tag

After merging:

```bash
git switch main
git pull origin main
git fetch --tags
```

Create an annotated tag:

```bash
git tag -a module-03-lesson-28 \
  -m "Complete Module 3 Lesson 28"
```

Push the tag:

```bash
git push origin module-03-lesson-28
```

### Step 8 — Create the GitHub Release

Navigate to:

#### Repository → Releases → Draft a new release

Use:

| Field | Value |
|---|---|
| Tag | `module-03-lesson-28` |
| Title | `Module 3 — Lesson 28: PR Fundamentals` |
| Target | `main` |

Release notes:

```markdown
# Module 3 — Lesson 28

Completed GitHub Pull Requests Fundamentals.

## Topics

- Pull Request lifecycle
- Branch comparison
- PR interface
- Draft PRs
- Reviewers and assignees
- Labels and milestones
- Issue integration
- Merge strategies
- Review workflows
- Merge requirements
- Team collaboration

## Training checkpoint

module-03-lesson-28
```

Publish the release.

**Important:** Create the tag after the lesson documentation PR has been merged into `main`, so the tag points to the completed lesson state.

---

## 25. Official Documentation

Bookmark these references:

1. [GitHub Pull Requests documentation](https://docs.github.com/en/pull-requests)
2. [Collaborating with Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
3. [Reviewing changes in Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
4. [Incorporating changes from a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request)
5. [Configuring branches and merges](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository)
6. [About CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
7. [Configuring Pull Request merges](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges)
8. [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
9. [About merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue)

---

## 26. What's Next — Lesson 29

### Lesson 29 — Advanced Pull Request Reviews: Review Comments, Suggestions, Change Requests and Resolving Conversations

In the next lesson, we'll explore the review process in greater depth.

Topics will include:

1. Reviewing individual changed lines.
2. Adding single-line and multi-line review comments.
3. Suggesting code changes directly from reviews.
4. Submitting pending reviews.
5. Requesting changes.
6. Addressing reviewer feedback.
7. Resolving conversations.
8. Re-requesting reviews.
9. Reviewing commits individually.
10. Comparing updated diffs.
11. Handling multiple reviewers.
12. Building a realistic two-person PR review workflow.

We'll practice a complete review cycle where one contributor submits a PR, another reviews it, requests changes, and the author updates the PR.

**Your immediate task:** Complete the first PR exercise, create the PR template, and practice the three merge strategies. Then publish `module-03-lesson-28`.

We'll keep the same lesson structure, practical exercises, Markdown documentation, Git commands, Conventional Commits, tags, and GitHub Releases throughout Module 3.

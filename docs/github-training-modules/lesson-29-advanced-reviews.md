# Module 3 — GitHub Pull Requests

## Lesson 29 — Advanced Pull Request Reviews: Review Comments, Suggestions, Change Requests and Resolving Conversations

**Level:** Intermediate
**Estimated time:** 3–4 hours
**Repository:** `github-deep-dive-training`
**Module:** 3 — GitHub Pull Requests
**Previous lesson:** Lesson 28 — Pull Requests Fundamentals: From Branch to Merge
**Next lesson:** Lesson 30 — Pull Request Management: Merge Conflicts, Updating Branches & Keeping PRs Healthy

---

## 1. Lesson Overview

In Lesson 28, you learned how Pull Requests work, how to create them, how to inspect their interface, and how to merge proposed changes.

Now we'll explore one of the most important parts of professional Pull Request collaboration: **Code Reviews**.

A Pull Request review is not simply clicking Approve or Request changes.

A professional review involves:

- Inspecting proposed changes line by line.
- Identifying incorrect logic and implementation problems.
- Writing clear, actionable review comments.
- Proposing corrections directly inside the diff.
- Submitting formal review decisions.
- Responding to reviewer feedback.
- Updating the existing PR.
- Reviewing new commits and updated diffs.
- Resolving conversations after verifying corrections.
- Requesting another review when changes are complete.

Throughout this lesson, we'll use your `github-deep-dive-training` repository and a restaurant-management application as our practical example.

We'll simulate a two-person development team:

- **Developer A:** Pull Request author.
- **Developer B:** Pull Request reviewer.

Developer A will introduce documentation containing deliberate mistakes. Developer B will review the changes, request modifications, and propose corrections. Developer A will address the feedback and update the existing PR.

### What you'll build

You will create:

```text
github-deep-dive-training/
│
└── docs/
    └── github/
        └── module-03-pull-requests/
            │
            ├── lesson-28-pr-fundamentals.md
            ├── lesson-29-advanced-reviews.md
            ├── review-practice.md
            └── review-notes.md
```

You will also complete a practical review cycle involving:

1. An initial Pull Request.
2. Inline review comments.
3. A multi-line review comment.
4. Suggested changes.
5. A Request changes review.
6. An updated commit.
7. Conversation resolution.
8. A final approval.
9. A merged Pull Request.

---

## 2. Learning Objectives

By the end of this lesson, you should understand:

1. How the Files changed interface works.
2. How to inspect additions, deletions, and context lines.
3. How to add inline review comments.
4. How to comment on multiple lines.
5. The difference between general PR comments and inline comments.
6. The three formal review decisions.
7. How pending reviews work.
8. How to submit a review containing multiple comments.
9. How to create suggested changes.
10. How authors address review feedback.
11. How new commits update an existing PR.
12. How to inspect updated diffs.
13. How to resolve review conversations.
14. How to re-request reviews.
15. How to inspect individual commits.
16. How to handle multiple reviewers.
17. How to write professional and actionable review feedback.
18. How to complete a realistic two-person review workflow.
19. How to publish the completed lesson using a PR, tag, and GitHub Release.

---

## 3. Understanding Pull Request Reviews

Let's start with the purpose of a code review.

Imagine you're developing a restaurant-management application.

Developer A implements an order-processing feature.

The implementation works, but contains several problems:

- New orders start with the wrong status.
- Some order-status transitions are incorrect.
- Monetary values are not validated.
- Staff permissions are too broad.
- The documentation does not explain the complete order lifecycle.

Developer A opens a Pull Request.

Instead of immediately merging it, Developer B reviews the changes.

The reviewer identifies the problems, explains their impact, and requests modifications.

Developer A updates the implementation and submits another commit.

Developer B inspects the updated changes and approves the PR.

This is a typical professional review workflow.

### 3.1 Why code reviews matter

| Benefit | Explanation |
|---|---|
| Quality control | Identify defects before integration |
| Knowledge sharing | Help developers understand different implementations |
| Maintainability | Improve readability and consistency |
| Security | Identify permission and data-exposure problems |
| Collaboration | Discuss implementation decisions |
| Documentation | Keep technical documentation accurate |
| Accountability | Maintain a record of review decisions |

### 3.2 Review versus approval

These concepts are related but different.

**Review:** The process of examining and commenting on proposed changes.

**Approval:** A formal positive review decision.

A reviewer can inspect a PR, leave comments, and submit a review without approving it.

Similarly, requesting changes is a formal review decision indicating that modifications are required.

### 3.3 The review lifecycle

```text
Developer creates a PR
        |
        v
Reviewer opens Files changed
        |
        v
Reviewer inspects the diff
        |
        v
Reviewer adds inline comments
        |
        v
Reviewer proposes suggestions
        |
        v
Reviewer submits a review
        |
        v
Author receives feedback
        |
        v
Author updates the branch
        |
        v
New commit appears in the PR
        |
        v
Reviewer inspects updated changes
        |
        v
Conversations are resolved
        |
        v
Reviewer approves
        |
        v
PR becomes eligible for merging
```

The exact merge requirements depend on repository configuration.

---

## 4. Understanding the Review Interface

Before writing comments, you need to understand where GitHub displays review information.

Open an existing Pull Request from Lesson 28 or create a new practice PR.

Navigate to:

### Pull requests → Select your PR

The most important section for this lesson is:

### Files changed

### 4.1 Important interface elements

| Interface element | Purpose |
|---|---|
| Diff | Displays additions, deletions, and unchanged context |
| `+` control | Starts an inline review comment |
| Review conversation | Displays feedback attached to changed lines |
| Viewed checkbox | Marks a file as reviewed |
| Review changes | Opens the review submission controls |
| Add single comment | Publishes an individual comment |
| Suggestion block | Proposes replacement text |
| Conversation resolution | Marks a discussion as addressed |

### 4.2 Understanding a diff

Consider this example:

```javascript
- const orderStatus = "pending";
+ const orderStatus = "preparing";
```

GitHub displays:

- Red lines: removed content.
- Green lines: added content.
- Context lines: unchanged content surrounding the modification.

A diff helps reviewers understand exactly what a PR proposes to change.

### 4.3 Unified and split views

GitHub provides different ways to display file changes.

#### Unified view

Displays removed and added lines together.

#### Split view

Displays the original and modified versions side by side.

Example:

```text
Unified:

- const total = -50;
+ const total = 50;
```

```text
Split:

Original             Modified

const total = -50;   const total = 50;
```

Both views communicate the same change.

Use whichever makes the review easier to understand.

### Exercise 1 — Explore the review interface

Open your Lesson 28 PR.

Visit:

1. Conversation.
2. Commits.
3. Checks.
4. Files changed.

Inside Files changed:

- Switch between unified and split views.
- Locate the changed files.
- Inspect the green and red lines.
- Find the Viewed checkbox.
- Locate the Review changes button.
- Identify the inline comment controls.

Record your observations in:

```text
docs/github/module-03-pull-requests/review-notes.md
```

Suggested content:

```markdown
# Pull Request Review Notes

## Review Interface

### Files changed

What does this section display?

### Diff

What do green and red lines represent?

### Review changes

What happens when this button is selected?

### Viewed checkbox

What does marking a file as viewed accomplish?

## Observations

Record your findings here.
```

---

## 5. Understanding Inline Review Comments

An inline review comment is attached to a specific changed line or range of lines.

This is useful when the reviewer wants to identify a particular problem.

For example:

```javascript
const order = {
  id: 1001,
  status: "ready",
  total: -50
};
```

A reviewer might notice that the order starts with an inappropriate status.

Instead of writing a general comment saying:

> The order status is incorrect.

The reviewer can attach feedback directly to the relevant line.

### 5.1 Add an inline comment

1. Open the PR.
2. Navigate to Files changed.
3. Locate the changed line.
4. Click the `+` icon beside it.
5. Enter your feedback.
6. Select the appropriate comment or review action.

Example:

**Comment:**

```text
An order should not start in the ready state.

A newly received order should start as pending
and move to preparing before becoming ready.

Could you correct the initial status and
document the expected transition?
```

### 5.2 What makes a good inline comment?

A professional comment should contain:

1. Observation — What is incorrect?
2. Impact — Why does it matter?
3. Recommendation — What should change?

Example:

```text
The initial order status is currently set to ready.

This could allow an order to appear ready before
kitchen preparation has started.

Could you change the initial status to pending?
```

### 5.3 Inline comments are not necessarily formal review decisions

Adding an inline comment does not automatically mean that you approved or rejected the entire PR.

You can submit comments as part of a formal review or publish an individual comment.

We'll explore the distinction later in this lesson.

---

## 6. Single-Line and Multi-Line Review Comments

Not every problem is limited to one line.

Sometimes several lines together create an incorrect implementation or explanation.

GitHub allows reviewers to attach comments to a selected range of changed lines.

### 6.1 Single-line comment

Example:

```javascript
total: -50
```

Comment:

```text
This example uses a negative order total.

Please replace it with a valid non-negative
example value.
```

Use a single-line comment when the problem is isolated.

### 6.2 Multi-line comment

Consider these processing rules:

```markdown
1. Every new order starts with the status `ready`.
2. Kitchen staff can change an order directly
   from `pending` to `delivered`.
```

The two rules are related.

The first describes an incorrect initial status.

The second describes an incomplete lifecycle.

A multi-line comment allows the reviewer to discuss both problems together.

Example:

```text
These two rules describe an inconsistent order lifecycle.

A newly received order should begin as pending,
move to preparing, and then become ready.

Delivery should happen after the order is handed
to the customer.

Please update both rules to reflect the complete
order lifecycle.
```

### 6.3 When should you use each type?

| Comment type | Best use |
|---|---|
| Single-line | One isolated problem |
| Multi-line | Several related lines |
| General PR comment | Overall feedback |
| Review summary | Overall assessment and decision |

### Exercise 2 — Add review comments

You will perform this exercise in the practice PR created in Section 7.

Add:

- Two single-line comments.
- One multi-line comment.
- One comment about example validation.

Make sure each comment explains the problem and expected correction.

---

## 7. Practical Exercise 1 — Create the Review Practice PR

Now we'll create a Pull Request containing deliberate documentation problems.

This PR will be used throughout the lesson.

### Step 1 — Synchronize your repository

Open your PowerShell terminal inside:

```powershell
cd github-deep-dive-training
```

Synchronize your main branch:

```bash
git switch main
git pull origin main
```

### Step 2 — Create the practice branch

```bash
git switch -c docs/lesson-29-review-practice
```

Verify:

```bash
git branch
```

Expected:

```text
* docs/lesson-29-review-practice
  main
```

### Step 3 — Create the practice file

Create:

```text
docs/github/module-03-pull-requests/review-practice.md
```

Content:

````markdown
# Review Practice: Order Processing

## Purpose

This document describes how an order moves
through the restaurant.

## Order statuses

An order can have these statuses:

- pending
- preparing
- ready
- delivered

## Processing rules

1. Every new order starts with the status `ready`.
2. Kitchen staff can change an order directly
   from `pending` to `delivered`.
3. An order should be prepared before it is
   marked as ready.
4. The cashier is responsible for confirming
   the order.

## Example

```javascript
const order = {
  id: 1001,
  status: "ready",
  total: -50
};
```

## Notes

All staff members can modify every order status.
````

### Step 4 — Inspect and commit

```bash
git status

git diff --check

git add docs/github/module-03-pull-requests/review-practice.md

git diff --cached

git commit -m "docs(github): add pull request review practice"
```

### Step 5 — Push the branch

```bash
git push -u origin docs/lesson-29-review-practice
```

### Step 6 — Create the Pull Request

Navigate to:

#### GitHub → Pull requests → New pull request

Select:

| Field | Value |
|---|---|
| Base | `main` |
| Compare | `docs/lesson-29-review-practice` |
| Title | `docs(github): add order processing review practice` |

Description:

```markdown
## Summary

Add a practice document for advanced Pull Request reviews.

## Changes

- Added order-processing documentation.
- Added order-status examples.
- Added example order data.
- Prepared deliberate issues for review exercises.

## Testing

- [x] Markdown file created
- [x] Git diff checked
- [x] Commit created
- [x] Branch pushed

## Additional context

Documentation-only training exercise.

This PR intentionally contains issues that will
be addressed during Lesson 29.
```

Create the PR.

**Important:** Do not merge this PR yet.

You will first review it, request changes, update it, and complete the review cycle.

---

## 8. General PR Comments vs Inline Review Comments

GitHub provides different ways to discuss a Pull Request.

Understanding the difference is essential for professional collaboration.

### 8.1 General PR comments

General comments are attached to the overall Pull Request conversation.

Use them for:

- Overall implementation feedback.
- Questions about architecture.
- General recommendations.
- Discussion about the PR's scope.
- Communication between contributors.

Example:

```markdown
The document is a useful starting point.

However, the order lifecycle and staff permissions
need clarification before this change is ready.

Please address the review feedback before requesting
another review.
```

### 8.2 Inline review comments

Inline comments are attached to specific changed lines.

Use them for:

- Incorrect logic.
- Missing validation.
- Incorrect variable names.
- Documentation mistakes.
- Security concerns.
- Specific implementation recommendations.

Example:

```text
This status should be pending rather than ready.

The order has not started kitchen preparation yet.
```

### 8.3 Comparison

| Feature | General PR comment | Inline review comment |
|---|---|---|
| Location | Conversation | Files changed |
| Scope | Entire PR | Specific changed lines |
| Purpose | General discussion | Specific feedback |
| Formal review | Can be submitted separately or as a review | Can be included in a submitted review |
| Best use | Overall assessment | Localized problems |

### 8.4 Review summary

A review summary is the overall message accompanying a submitted review.

It explains the reviewer's overall assessment.

Example:

```markdown
The document contains several issues concerning:

- Initial order status.
- Status transitions.
- Example monetary values.
- Staff permissions.

Please address the inline comments before requesting
another review.
```

A good reviewer uses inline comments for detailed feedback and the review summary for the overall assessment.

---

## 9. Understanding the Three Review Decisions

When you select **Review changes**, GitHub provides three main review decisions.

### 9.1 Comment

**Purpose:** Provide feedback without formally approving or requesting changes.

Use it when:

- You have questions.
- You want to provide suggestions.
- You want to discuss implementation decisions.
- You don't have a blocking concern.

Example:

```text
The documentation looks good overall.

Could you include another example showing
how an order moves from preparing to ready?
```

### 9.2 Approve

**Purpose:** Formally approve the proposed changes.

Use it when:

- You have inspected the relevant changes.
- The implementation is acceptable.
- You have no unresolved blocking concerns.
- Required review criteria are satisfied.

Example:

```text
The requested changes have been addressed.

The order lifecycle is now clear, the example
data is valid, and the permissions are documented.

Approved.
```

### 9.3 Request changes

**Purpose:** Formally request modifications before the PR proceeds.

Use it when:

- You identify important defects.
- Business rules are incorrect.
- Security problems need attention.
- Required implementation changes are missing.

Example:

```text
Changes requested:

1. Correct the initial order status.
2. Document the valid status transitions.
3. Correct the negative monetary example.
4. Clarify staff permissions.
```

### 9.4 Comparison

| Decision | Meaning | Typical use |
|---|---|---|
| Comment | Feedback without an approval decision | Suggestions and discussion |
| Approve | Formally approves the changes | Ready for integration |
| Request changes | Requests modifications | Blocking problems |

**Important:** Repository settings and permissions determine how review decisions affect merging. An approval does not override required checks or other branch protection requirements.

### Exercise 3 — Submit a formal review

Open your practice PR.

1. Navigate to Files changed.
2. Add the review comments.
3. Select Review changes.
4. Choose Request changes.
5. Add a review summary.
6. Submit the review.

Use this summary:

```markdown
The document contains several problems with
the order lifecycle, initial status, monetary
example, and staff permissions.

Please address the inline comments before
requesting another review.
```

---

## 10. Suggested Changes — Propose Corrections Directly in Reviews

GitHub supports suggested changes in inline review comments.

This feature allows a reviewer to propose replacement content directly inside a comment.

It is especially useful for small, unambiguous corrections.

### 10.1 Example

Original line:

```markdown
1. Every new order starts with the status `ready`.
```

Suggested replacement:

```markdown
1. Every new order starts with the status `pending`.
```

Instead of simply explaining the correction, the reviewer can use GitHub's suggestion interface.

### 10.2 How to create a suggestion

1. Open Files changed.
2. Locate the changed line.
3. Click the inline comment control.
4. Select the suggestion option.
5. Replace the original content with the proposed version.
6. Add an explanatory comment if necessary.
7. Submit the review.

GitHub displays the suggestion as a proposed replacement.

### 10.3 Applying suggestions

A user with the appropriate repository permissions can apply an available suggestion through the GitHub interface.

The author should still verify the resulting change.

**Important:** Applying a suggestion changes the PR's proposed content. It does not independently approve the entire Pull Request.

### 10.4 When should you use suggestions?

| Situation | Recommendation |
|---|---|
| Simple typo | Use a suggestion |
| Incorrect variable name | Use a suggestion |
| Small documentation correction | Use a suggestion |
| Complex architecture problem | Discuss the solution |
| Unclear business requirement | Ask for clarification |
| Multiple possible implementations | Explain the alternatives |

### Exercise 4 — Create two suggested changes

In your practice PR, propose:

#### Suggestion 1 — Initial status

Replace:

```markdown
1. Every new order starts with the status `ready`.
```

With:

```markdown
1. Every new order starts with the status `pending`.
```

#### Suggestion 2 — Monetary example

Replace:

```javascript
total: -50
```

With:

```javascript
total: 50
```

Add explanations to both suggestions.

Do not apply the suggestions immediately if you're practising the reviewer role. Let the author decide how to address the feedback.

---

## 11. Pending Reviews vs Submitted Reviews

This is an important distinction when working with multiple review comments.

### 11.1 Pending review

A pending review contains draft comments that have not yet been submitted.

For example:

You inspect five changed files and add several inline comments.

Instead of publishing each comment individually, GitHub can collect them in a pending review.

The reviewer can inspect and edit those comments before submitting the review.

### 11.2 Submitted review

A submitted review is published to the Pull Request.

It may contain:

- Inline comments.
- Multi-line comments.
- A general review summary.
- A formal review decision.

### 11.3 Comparison

| State | Meaning |
|---|---|
| Pending | Draft review not yet submitted |
| Commented | Review submitted with the Comment decision |
| Approved | Review submitted with approval |
| Changes requested | Review submitted requesting changes |

### 11.4 Why pending reviews are useful

Imagine reviewing a Pull Request containing 15 changed files.

You identify:

- Three logic problems.
- Two documentation mistakes.
- One missing validation rule.

You can prepare all the comments and submit them together.

This produces a more organized review.

**Important:** Pending review comments are not yet published as a submitted review. They should not be confused with individual comments already posted to the PR.

### Exercise 5 — Practise pending reviews

If your previous review has already been submitted, use another practice PR or ask your collaborator to create one.

1. Open Files changed.
2. Add an inline comment.
3. Add another inline comment.
4. Inspect the pending review.
5. Edit one comment.
6. Submit the review.
7. Open Conversation.
8. Verify that the submitted feedback appears.

Record the difference between pending and submitted reviews.

---

## 12. Responding to Review Feedback as the Author

Now switch from the reviewer role to the author role.

Developer B has requested changes.

Developer A must address the feedback.

### 12.1 Review the requested changes

Return to the Pull Request.

Read:

- Review summary.
- Inline comments.
- Suggested changes.
- General discussion.

Identify every requested modification.

### 12.2 Update the practice document

Open:

```text
docs/github/module-03-pull-requests/review-practice.md
```

Replace its content with:

````markdown
# Review Practice: Order Processing

## Purpose

This document describes how an order moves
through the restaurant.

## Order statuses

An order can have these statuses:

- pending
- preparing
- ready
- delivered

## Processing rules

1. Every new order starts with the status `pending`.
2. Kitchen staff move an order from `pending`
   to `preparing`.
3. Once preparation is complete, kitchen staff
   move the order to `ready`.
4. The order is marked as `delivered` after it
   has been handed to the customer.
5. The cashier is responsible for confirming
   the order payment.

## Example

```javascript
const order = {
  id: 1001,
  status: "pending",
  total: 50
};
```

## Permissions

- Kitchen staff can update preparation-related statuses.
- Cashiers can confirm payment.
- Authorized staff can mark an order as delivered.

## Validation

The application should validate order totals
and status transitions.
````

### 12.3 Commit the corrections

```bash
git status

git diff

git diff --check

git add docs/github/module-03-pull-requests/review-practice.md

git diff --cached

git commit -m "docs(github): address order review feedback"
```

### 12.4 Push the changes

```bash
git push origin docs/lesson-29-review-practice
```

GitHub automatically updates the existing Pull Request.

**Important:** You do not need to create another PR.

The new commit becomes part of the original PR.

### 12.5 Reply to review comments

Return to Conversation.

Where appropriate, reply to the reviewer.

Example:

```text
Thanks for the feedback.

I've corrected the initial order status,
documented the valid processing sequence,
updated the monetary example, and clarified
the staff permissions.

The corrections are included in the latest commit.
```

A professional author should acknowledge feedback and explain how it was addressed.

---

## 13. Reviewing Updated Diffs

After the author pushes new commits, the reviewer must inspect the updated changes.

Do not approve a PR simply because the author says the problems have been fixed.

### 13.1 Open the updated PR

Navigate to:

#### Pull requests → Your practice PR → Files changed

Inspect the updated diff.

### 13.2 What should the reviewer verify?

| Original problem | Expected correction |
|---|---|
| Initial status was `ready` | Initial status is `pending` |
| Invalid status transition | Complete processing sequence documented |
| Negative total | Non-negative example value |
| Permissions too broad | Responsibilities clarified |
| Delivery rules unclear | Delivery responsibility documented |

### 13.3 Review the complete change

Check:

- Were all requested changes addressed?
- Did the author introduce new mistakes?
- Are the examples consistent?
- Does the documentation describe the correct lifecycle?
- Are there remaining unresolved concerns?

### 13.4 Mark files as viewed

GitHub provides a Viewed checkbox in Files changed.

This helps reviewers track which files they have inspected.

Mark a file as viewed only after examining it.

If new changes arrive, review the updated content rather than relying on an earlier Viewed state.

### Exercise 6 — Review the updated diff

Act as Developer B.

1. Open the updated PR.
2. Inspect Files changed.
3. Compare the original and updated content.
4. Verify all five corrections.
5. Check whether the author introduced any new problems.
6. Reply to the relevant conversations.

Do not approve until you have verified the changes.

---

## 14. Resolving Review Conversations

A review conversation is a discussion associated with a specific change.

For example:

Reviewer:

```text
The initial order status should be pending,
not ready.
```

Author:

```text
Corrected in the latest commit.
```

After verifying the correction, the conversation can be resolved.

### 14.1 Typical conversation lifecycle

```text
Reviewer identifies a problem
          |
          v
Reviewer leaves a comment
          |
          v
Author receives feedback
          |
          v
Author replies
          |
          v
Author updates the branch
          |
          v
Reviewer verifies the correction
          |
          v
Conversation is resolved
```

### 14.2 How to resolve a conversation

1. Open the Pull Request.
2. Navigate to the review conversation.
3. Inspect the author's response.
4. Verify the corresponding change in Files changed.
5. Select Resolve conversation when available.

The ability to resolve conversations depends on the user's access and GitHub permissions.

### 14.3 Resolving versus approving versus merging

These are three different operations.

| Operation | Meaning |
|---|---|
| Resolve conversation | Marks a discussion as addressed |
| Approve PR | Formally approves the proposed changes |
| Merge PR | Integrates changes into the base branch |

Resolving every conversation does not automatically approve the Pull Request.

Likewise, approving the PR does not necessarily resolve every conversation.

A repository can require both approval and conversation resolution before merging.

### 14.4 When should a conversation remain open?

Keep a conversation open when:

- The correction has not been implemented.
- The author has not answered an important question.
- The proposed change has not been verified.
- The discussion requires further clarification.

Do not resolve conversations simply to make the PR appear clean.

### Exercise 7 — Resolve conversations

Return to your practice PR.

For every review conversation:

1. Read the original comment.
2. Read the author's response.
3. Inspect the updated document.
4. Verify the correction.
5. Resolve the conversation.

Confirm that all addressed conversations are resolved.

---

## 15. Re-requesting Reviews

After the author addresses feedback, another review may be necessary.

The reviewer should inspect the new changes before approving.

### 15.1 Request another review

On the Pull Request:

1. Navigate to the Conversation tab.
2. Locate the reviewer information in the sidebar or review section.
3. Use the available review-request controls.
4. Select the appropriate reviewer again, where available.

The reviewer may receive another notification.

The exact controls depend on the repository interface and review state.

### 15.2 Reviewer responsibilities

After receiving a new review request:

- Open the latest PR.
- Inspect new commits.
- Review updated diffs.
- Verify previous feedback.
- Check for new problems.
- Submit a new review decision.

### 15.3 Previous reviews and updated commits

A previous approval should not be treated as automatic approval of every subsequent change.

GitHub's approval and stale-review behavior depends on repository rules and configuration.

For example, a repository can dismiss stale approvals when new commits are pushed.

### Exercise 8 — Request another review

If you're working with a collaborator:

1. Ask Developer A to request another review.
2. Developer B opens the updated PR.
3. Developer B inspects the new commit.
4. Developer B verifies the corrections.
5. Developer B submits an approval.

If you're working alone, document this workflow and practise the reviewer interface with another eligible account or collaborator when available.

---

## 16. Reviewing Commits Individually

A Pull Request can contain multiple commits.

Open the **Commits** tab.

For this exercise, your practice PR should contain at least two commits.

| Commit | Purpose |
|---|---|
| `docs(github): add pull request review practice` | Original document |
| `docs(github): address order review feedback` | Corrections after review |

### 16.1 Why inspect individual commits?

Commit inspection helps reviewers understand:

- How the implementation evolved.
- Which changes were made after feedback.
- Whether the author introduced unrelated modifications.
- Whether the commit history follows repository conventions.

### 16.2 Commits versus final PR diff

These are different views.

#### Commits

Show individual changes introduced by each commit.

#### Files changed

Shows the overall proposed difference between the PR's base and compare branches.

#### Conversation

Shows the discussion and review decisions.

A reviewer should use all three views when necessary.

### 16.3 Recommended review strategy

```text
Conversation
    |
    | Understand the discussion
    v
Commits
    |
    | Understand the history
    v
Files changed
    |
    | Inspect the final proposed result
    v
Review decision
```

### Exercise 9 — Inspect the commit history

Open the Commits tab.

Record:

1. How many commits are included?
2. Which commit introduced the original document?
3. Which commit addressed the review feedback?
4. Were the commit messages meaningful?
5. Does the final diff contain only the intended changes?

Write your observations in `review-notes.md`.

---

## 17. Handling Multiple Reviewers

Professional repositories often require several reviewers.

Different reviewers can focus on different areas.

Imagine a restaurant-management application with a backend, frontend, and security-sensitive permissions system.

You might have:

| Reviewer | Review focus |
|---|---|
| Backend developer | Business logic and API behavior |
| Frontend developer | UI impact and API integration |
| Security reviewer | Permissions and data exposure |
| Project maintainer | Architecture and maintainability |

### 17.1 Different reviewers can reach different decisions

Imagine:

| Reviewer | Decision |
|---|---|
| Backend developer | Approve |
| Frontend developer | Comment |
| Security reviewer | Request changes |
| Project maintainer | Pending |

The PR is not necessarily ready to merge.

Repository rules determine which approvals and checks are required.

### 17.2 Required reviewers

Repository administrators can configure review requirements through branch protection rules or rulesets.

For example:

```yaml
Required approvals: 2

Required status checks:
  - backend-tests
  - frontend-tests

Require conversation resolution: true
```

This is an illustrative configuration, not a GitHub configuration file.

### 17.3 Team reviews

Organizations can use GitHub Teams to coordinate review responsibilities.

For example:

```text
@backend-team
@frontend-team
@security-team
```

Review requests can be directed to eligible teams, depending on repository access and configuration.

### Exercise 10 — Simulate multiple reviewers

If you have collaborators:

1. Ask one reviewer to focus on business logic.
2. Ask another reviewer to focus on documentation.
3. Compare their feedback.
4. Record their review decisions.
5. Identify which changes are blocking.

If you are working independently, perform two separate review passes using these different responsibilities.

Remember that an independent approval requires another eligible reviewer; reviewing your own PR is not a substitute.

---

## 18. Professional Code Review Practices

A code review should improve the proposed changes without becoming personal criticism.

### 18.1 Avoid vague comments

Bad:

```text
This is wrong.
```

Better:

```text
The initial order status should be pending.

Starting an order as ready could cause the kitchen
display to show an order as completed before
preparation has started.
```

### 18.2 Focus on the change, not the developer

Bad:

```text
You don't understand how order processing works.
```

Better:

```text
The current status transition skips the preparation
stage.

Could you update the documented lifecycle?
```

### 18.3 Explain the impact

Bad:

```text
Change this.
```

Better:

```text
The current permission description allows every
staff member to modify every order status.

This does not clearly separate kitchen and cashier
responsibilities.

Please document the intended role permissions.
```

### 18.4 Use suggestions appropriately

Use suggestions for small, clear corrections.

Use discussion for decisions requiring additional context.

### 18.5 Review the whole PR

Do not approve a PR after inspecting only one file.

Check:

- All changed files.
- Related documentation.
- Relevant tests.
- Important implementation details.
- The final diff.
- Outstanding review conversations.

### 18.6 Common mistakes

| Mistake | Better practice |
|---|---|
| Writing vague comments | Explain the problem and its impact |
| Criticizing the author | Focus on the proposed change |
| Requesting changes without explanation | Explain the expected correction |
| Approving without inspecting the full diff | Review all relevant files |
| Resolving conversations without verification | Verify the actual correction |
| Treating suggestions as mandatory | Discuss unclear recommendations |
| Confusing comments with approvals | Submit a formal review decision |
| Approving outdated changes | Inspect the latest commits and diff |
| Ignoring other reviewers | Check all required review decisions |

---

## 19. Practical Exercise 2 — Two-Person Review Simulation

This is the main assignment for Lesson 29.

You will simulate a professional review workflow using two developer roles.

### 19.1 Scenario

Developer A submits a Pull Request containing order-processing documentation.

Developer B reviews it and identifies several problems.

Developer A updates the PR.

Developer B verifies the corrections and approves the changes.

### 19.2 Developer A — Author

Responsibilities:

1. Create the practice branch.
2. Add the original review-practice document.
3. Commit the changes.
4. Push the branch.
5. Open a Pull Request.
6. Request a review.
7. Wait for feedback.
8. Update the document.
9. Create a second commit.
10. Push the new commit.
11. Respond to review comments.

### 19.3 Developer B — Reviewer

Responsibilities:

1. Open the PR.
2. Inspect Files changed.
3. Add at least three inline comments.
4. Add one multi-line comment.
5. Create at least two suggestions.
6. Submit a Request changes review.
7. Wait for the author to update the PR.
8. Inspect the updated diff.
9. Verify the corrections.
10. Resolve addressed conversations.
11. Submit an approval.

### 19.4 Final steps

Developer A should:

1. Verify that the required review is approved.
2. Check that conversations are resolved.
3. Verify required status checks, if configured.
4. Merge the PR.
5. Delete the feature branch if appropriate.

### Expected workflow

```text
Developer A
    |
    v
Create branch
    |
    v
Commit and push
    |
    v
Open PR
    |
    v
Developer B
    |
    v
Review and comment
    |
    v
Request changes
    |
    v
Developer A
    |
    v
Address feedback
    |
    v
Push new commit
    |
    v
Developer B
    |
    v
Verify updated diff
    |
    v
Resolve conversations
    |
    v
Approve PR
    |
    v
Developer A
    |
    v
Merge PR
```

**Single-account limitation:** If you have only one GitHub account, you can practise the author workflow and explore the review interface, but you cannot reproduce a genuinely independent approval of your own PR. Use another eligible collaborator or account for the complete two-person exercise.

---

## 20. Additional Review Features to Explore

There are several additional review-related features worth understanding.

| Feature | Purpose |
|---|---|
| Review requests | Requests a review from a person or team |
| Suggested changes | Proposes replacement content |
| Viewed files | Tracks inspected files |
| Pending reviews | Collects draft review comments |
| Review summaries | Communicates the overall assessment |
| Conversation resolution | Tracks addressed discussions |
| Stale reviews | Reviews affected by subsequent changes |
| CODEOWNERS | Identifies responsible code owners |
| Required approvals | Enforces review requirements |
| Dismissal of stale approvals | Invalidates approvals under configured rules |

### 20.1 CODEOWNERS and review responsibilities

In Lesson 28, you were introduced to CODEOWNERS.

This feature can help automatically request reviews from the people or teams responsible for particular parts of a repository.

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
```

These team names are illustrative.

The referenced users and teams must exist and have the appropriate repository access.

### 20.2 Stale approvals

A stale approval is an approval that no longer satisfies the repository's configured review requirements.

For example, a repository may require dismissal of previous approvals when new commits are pushed.

This prevents an old approval from automatically covering substantial subsequent changes.

We'll explore this behavior further in Lesson 30.

### 20.3 Review requirements

A repository can enforce:

- A minimum number of approving reviews.
- Required CODEOWNERS reviews.
- Conversation resolution.
- Required status checks.
- Restrictions on who can dismiss reviews.

These requirements help maintain consistent integration standards.

---

## 21. Practical Assessment — Advanced Pull Request Reviews

Complete the following assessment using your training repository.

### Assessment requirements

#### Review interface

- [ ] Open an existing Pull Request.
- [ ] Inspect Files changed.
- [ ] Understand unified and split diff views.
- [ ] Identify inline comment controls.
- [ ] Explore the Viewed checkbox.

#### Review comments

- [ ] Add at least three inline comments.
- [ ] Add one multi-line comment.
- [ ] Add one general PR comment.
- [ ] Write a review summary.

#### Review decisions

- [ ] Explore Comment.
- [ ] Submit Request changes.
- [ ] Understand Approve.
- [ ] Distinguish comments from formal review decisions.

#### Suggested changes

- [ ] Create at least one suggested change.
- [ ] Explain why the suggestion is appropriate.
- [ ] Verify the resulting correction.

#### Author workflow

- [ ] Read review feedback.
- [ ] Update the practice document.
- [ ] Create a second commit.
- [ ] Push the updated branch.
- [ ] Reply to reviewer comments.

#### Updated review

- [ ] Inspect the updated diff.
- [ ] Inspect individual commits.
- [ ] Verify requested corrections.
- [ ] Resolve addressed conversations.
- [ ] Request another review.
- [ ] Receive approval from another eligible reviewer.

#### Completion

- [ ] Merge the practice PR.
- [ ] Delete the feature branch if appropriate.
- [ ] Publish the Lesson 29 documentation.
- [ ] Create the annotated lesson tag.
- [ ] Publish the GitHub Release.

---

## 22. Lessons Learned

Before moving to Lesson 30, make sure you can explain these concepts without looking at the documentation.

| Concept | What you should understand |
|---|---|
| Diff | Displays proposed additions and deletions |
| Inline comment | Feedback attached to changed lines |
| Multi-line comment | Feedback attached to a range of lines |
| General comment | Overall PR discussion |
| Review summary | Overall reviewer assessment |
| Comment | Formal review without approval or rejection |
| Approve | Positive formal review decision |
| Request changes | Formal request for modifications |
| Pending review | Draft feedback not yet submitted |
| Submitted review | Published review and decision |
| Suggested change | Proposed replacement content |
| Updated diff | Latest proposed changes |
| Conversation resolution | Marks a discussion as addressed |
| Stale approval | Approval affected by subsequent changes and repository rules |
| CODEOWNERS | Defines code ownership and review responsibilities |

### Reflection questions

1. What is the difference between an inline comment and a general PR comment?
2. When should you use a multi-line comment?
3. What is the difference between Comment and Request changes?
4. What happens when you submit a pending review?
5. How do suggested changes work?
6. Why should an author respond to review feedback?
7. Why must a reviewer inspect the updated diff?
8. Does resolving a conversation automatically approve a PR?
9. Can an old approval always be trusted after new commits are pushed?
10. Why should a reviewer avoid vague or personal criticism?
11. What is the difference between reviewing commits and reviewing the final PR diff?
12. How can multiple reviewers improve code quality?

---

## 23. Completion Checklist

### Concepts

- [ ] I understand the Files changed interface.
- [ ] I understand GitHub diffs.
- [ ] I understand inline review comments.
- [ ] I understand single-line and multi-line comments.
- [ ] I understand general PR comments.
- [ ] I understand the three formal review decisions.
- [ ] I understand pending and submitted reviews.
- [ ] I understand suggested changes.
- [ ] I understand how authors address feedback.
- [ ] I understand updated diffs.
- [ ] I understand conversation resolution.
- [ ] I understand review requests.
- [ ] I understand stale approvals.
- [ ] I understand multiple reviewers.

### Practical work

- [ ] I created the review-practice branch.
- [ ] I opened the practice PR.
- [ ] I added inline review comments.
- [ ] I created a multi-line comment.
- [ ] I added suggested changes.
- [ ] I submitted a Request changes review.
- [ ] I updated the PR using a second commit.
- [ ] I inspected the updated diff.
- [ ] I responded to review feedback.
- [ ] I resolved addressed conversations.
- [ ] I requested another review.
- [ ] I received an independent approval.
- [ ] I merged the practice PR.

### Repository workflow

- [ ] I created the Lesson 29 documentation.
- [ ] I used a dedicated documentation branch.
- [ ] I followed Conventional Commits.
- [ ] I pushed the documentation branch.
- [ ] I created and merged the documentation PR.
- [ ] I created the training tag.
- [ ] I published the GitHub Release.

---

## 24. Lesson Documentation

Create the following files:

```text
docs/
└── github/
    └── module-03-pull-requests/
        │
        ├── lesson-28-pr-fundamentals.md
        ├── lesson-29-advanced-reviews.md
        ├── review-practice.md
        └── review-notes.md
```

### 24.1 lesson-29-advanced-reviews.md

Organize your documentation using this structure:

```markdown
# Lesson 29 — Advanced Pull Request Reviews

## 1. Lesson Overview

## 2. Learning Objectives

## 3. Understanding Pull Request Reviews

## 4. Understanding the Review Interface

## 5. Inline Review Comments

## 6. Single-Line and Multi-Line Comments

## 7. Creating the Review Practice PR

## 8. General Comments vs Inline Comments

## 9. Review Decisions

## 10. Suggested Changes

## 11. Pending vs Submitted Reviews

## 12. Addressing Review Feedback

## 13. Reviewing Updated Diffs

## 14. Resolving Conversations

## 15. Re-requesting Reviews

## 16. Reviewing Commits

## 17. Multiple Reviewers

## 18. Professional Review Practices

## 19. Two-Person Collaboration

## 20. Additional Review Features

## 21. Practical Assessment

## 22. Lessons Learned

## 23. Completion Checklist

## 24. References
```

### 24.2 review-practice.md

This file should contain the practical order-processing example.

Include:

- Original document with deliberate problems.
- Corrected order lifecycle.
- Example order data.
- Staff permissions.
- Validation requirements.

### 24.3 review-notes.md

Use this file to record your findings:

```markdown
# Lesson 29 — Review Notes

## Review Interface

## Inline Comments

## Multi-Line Comments

## Review Decisions

## Suggested Changes

## Pending Reviews

## Updated Diffs

## Conversation Resolution

## Commit History

## Multiple Reviewers

## Reflection

```

### 24.4 Screenshots

Include screenshots from your actual repository exercises where useful.

Suggested screenshots:

1. The original practice PR.
2. Files changed with inline comments.
3. A multi-line review comment.
4. A submitted Request changes review.
5. A suggested change.
6. The updated PR diff.
7. The second commit in the Commits tab.
8. Resolved conversations.
9. The final approval.
10. The merged PR.

Do not use screenshots of hypothetical results as evidence of completed exercises.

---

## 25. Git Workflow — Commit, PR, Tag and Release

After completing the practical exercises, publish the Lesson 29 documentation.

### Step 1 — Synchronize main

```bash
git switch main
git pull origin main
```

The practice PR should already have been merged before publishing the final lesson documentation.

### Step 2 — Create the documentation branch

```bash
git switch -c docs/lesson-29-advanced-reviews
```

### Step 3 — Add your documentation

```bash
git add docs/github/module-03-pull-requests/
```

### Step 4 — Validate

```bash
git status

git diff --check

git diff --cached
```

Check that you are not committing:

- Temporary files.
- Unrelated changes.
- Unnecessary screenshots.
- Generated files.
- Personal information.

### Step 5 — Commit

```bash
git commit -m "docs(github): add Lesson 29 advanced pull request reviews"
```

### Step 6 — Push

```bash
git push -u origin docs/lesson-29-advanced-reviews
```

### Step 7 — Create the documentation PR

**PR title:**

```text
docs(github): add Lesson 29 advanced pull request reviews
```

**PR description:**

```markdown
## Summary

Add Lesson 29 covering advanced GitHub Pull Request reviews.

## Topics

- Understanding the review interface
- Inline and multi-line comments
- General comments versus review comments
- Formal review decisions
- Suggested changes
- Pending and submitted reviews
- Addressing review feedback
- Reviewing updated diffs
- Resolving conversations
- Re-requesting reviews
- Reviewing individual commits
- Multiple reviewers
- Professional review practices
- Two-person collaboration

## Practical exercises

- Created a review-practice PR.
- Added inline review comments.
- Submitted a Request changes review.
- Updated the PR with a second commit.
- Inspected the updated diff.
- Practised conversation resolution.

## Checklist

- [ ] Lesson documentation added
- [ ] Practice document added
- [ ] Review notes added
- [ ] Markdown validated
- [ ] Practical exercises completed
- [ ] Screenshots included where useful
- [ ] No unrelated files included
```

Review and merge your documentation PR.

### Step 8 — Synchronize main

After merging:

```bash
git switch main
git pull origin main
git fetch --tags
```

### Step 9 — Create an annotated tag

```bash
git tag -a module-03-lesson-29 \
  -m "Complete Module 3 Lesson 29"
```

Push the tag:

```bash
git push origin module-03-lesson-29
```

### Step 10 — Create the GitHub Release

Navigate to:

#### Repository → Releases → Draft a new release

Use:

| Field | Value |
|---|---|
| Tag | `module-03-lesson-29` |
| Release title | `Module 3 — Lesson 29: Advanced PR Reviews` |
| Target | `main` |

Release notes:

```markdown
# Module 3 — Lesson 29

Completed Advanced Pull Request Reviews.

## Topics

- Review interface and diffs
- Inline and multi-line review comments
- Review decisions
- Suggested changes
- Pending and submitted reviews
- Addressing review feedback
- Updated diffs and commits
- Conversation resolution
- Re-requesting reviews
- Multiple reviewers
- Professional review practices

## Practical exercises

- Created a review-practice PR.
- Practised inline review comments.
- Submitted a Request changes review.
- Updated the PR using a new commit.
- Verified updated changes.
- Resolved review conversations.
- Completed the review workflow.

## Training checkpoint

module-03-lesson-29
```

Publish the release.

**Important:** Create the tag after the documentation PR has been merged into `main`, so the tag points to the completed lesson state.

---

## 26. Official Documentation

Bookmark these official GitHub references:

1. [Reviewing changes in pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
2. [Commenting on a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request)
3. [Approving a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews)
4. [Incorporating feedback in your pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request)
5. [Resolving conversations](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/resolving-conversations)
6. [About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)
7. [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
8. [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

---

## 27. What's Next — Lesson 30

## Lesson 30 — Pull Request Management: Merge Conflicts, Updating Branches and Keeping PRs Healthy

In Lesson 29, you learned how developers review proposed changes, provide feedback, request modifications, and approve Pull Requests.

In the next lesson, we'll explore what happens when branches evolve independently and their changes become difficult to integrate.

We'll cover:

1. Understanding why merge conflicts happen.
2. Detecting conflicts in GitHub and locally.
3. Resolving conflicts using Git commands.
4. Resolving conflicts using VS Code.
5. Updating a feature branch from `main`.
6. Merge versus rebase when updating a PR branch.
7. Understanding stale reviews and outdated approvals.
8. Keeping a PR focused and manageable.
9. Handling conflicts in a collaborative workflow.
10. Completing a realistic conflict-resolution exercise.

We'll use practical Git commands and simulate multiple developers modifying the same files.

### Your immediate task

Complete the Lesson 29 review-practice PR, publish the documentation, and create:

```text
module-03-lesson-29
```

**Lesson 29 is complete when you've practised the review cycle, addressed feedback, verified the updated changes, merged the practice PR, and published the Lesson 29 tag and GitHub Release.**

---

## End of Lesson 29 — Advanced Pull Request Reviews

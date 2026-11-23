

# Lesson 08 — Pull Request Collaboration and Review Workflow

**Module:** 01 — Code  
**Difficulty:** Intermediate  
**Repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By completing this lesson, you should understand how to:

- Explain the complete Pull Request lifecycle.
- Create and manage Pull Requests.
- Create Draft Pull Requests.
- Understand the different Pull Request tabs.
- Request reviews from collaborators.
- Understand approvals and change requests.
- Respond to review feedback.
- Resolve review conversations.
- Synchronize feature branches with `main`.
- Identify and resolve merge conflicts.
- Use auto-merge.
- Configure a `CODEOWNERS` file.
- Close or merge Pull Requests correctly.
- Clean up branches after merging.

## 2. What is a Pull Request?

A Pull Request (PR) is a proposal to merge changes from one branch into another.

For example:

```text
main
 |
 A---B---C
          \
           D---E---F
                 |
                 v
           feature branch
```

You create a Pull Request to propose integrating the changes from the feature branch into `main`.

A Pull Request allows collaborators to:

- Inspect the changes.
- Review individual commits.
- Discuss implementation decisions.
- Request corrections.
- Approve the proposed changes.
- Check automated tests.
- Merge the changes when requirements are satisfied.

A Pull Request is therefore more than a merge operation. It is a collaboration and quality-control process.

## 3. Understanding the Pull Request lifecycle

A typical Pull Request follows this workflow:

```text
Create feature branch
        |
        v
Implement changes
        |
        v
Commit changes
        |
        v
Push feature branch
        |
        v
Create Pull Request
        |
        v
Review changes
        |
        v
Receive feedback
        |
        v
Make corrections
        |
        v
Run checks
        |
        v
Get approval
        |
        v
Merge Pull Request
        |
        v
Delete feature branch
```

Not every Pull Request needs every step. For example, a small documentation change may not require automated tests.

However, important changes should be reviewed before merging.

### Important Pull Request terminology

| Term | Meaning |
|---|---|
| Base branch | Branch receiving the changes |
| Head branch | Branch containing the proposed changes |
| Reviewer | Person reviewing the changes |
| Assignee | Person responsible for the Pull Request |
| Draft PR | Work-in-progress Pull Request |
| Review | Feedback submitted by a reviewer |
| Approval | Reviewer indicates that changes are acceptable |
| Requested changes | Reviewer asks for corrections |
| Merge conflict | Git cannot automatically combine changes |
| Status check | Automated validation result |
| Auto-merge | Merge automatically after requirements are satisfied |

Example:

```text
base: main
compare: feature/add-user-authentication
```

This means the Pull Request proposes merging `feature/add-user-authentication` into `main`.

---

## 4. Creating a Pull Request

### Step 1 — Update your local main branch

```bash
git switch main
git pull origin main
```

Explanation:

- `git switch main`: moves to your main branch.
- `git pull origin main`: retrieves and integrates the latest remote main changes.

### Step 2 — Create a feature branch

```bash
git switch -c docs/add-pull-request-guide
```

This creates a new branch and switches to it.

### Step 3 — Make changes

For this exercise, create a small file:

```text
docs/github/module-01-code/pr-exercise.md
```

Add:

```markdown
# Pull Request Exercise

This file is used to practise the Pull Request workflow.

## Objectives

- Create a feature branch.
- Commit changes.
- Push the branch.
- Open a Pull Request.
- Review the changes.
```

### Step 4 — Inspect changes

```bash
git status
git diff
```

### Step 5 — Stage and commit

```bash
git add docs/github/module-01-code/pr-exercise.md
git commit -m "docs(github): add pull request exercise"
```

### Step 6 — Push the branch

```bash
git push -u origin docs/add-pull-request-guide
```

### Step 7 — Open GitHub

1. Open your repository.
2. Select **Pull requests**.
3. Select **New pull request**.
4. Set the base branch to `main`.
5. Set the compare branch to `docs/add-pull-request-guide`.
6. Review the displayed changes.
7. Select **Create pull request**.

### Step 8 — Complete the Pull Request information

Example title:

```text
docs(github): add pull request exercise
```

Example description:

```markdown
## Summary

Adds a small exercise for practising the Pull Request workflow.

## Motivation

This exercise helps contributors understand how to create and submit Pull Requests.

## Changes

- Added pr-exercise.md.
- Added learning objectives.

## Validation

- [x] Reviewed the changes.
- [x] Checked Markdown formatting.
- [x] Verified the file path.
```

Create the Pull Request.

### Exercise

Create and open this Pull Request yourself.

Do not merge it yet. We will use it to explore the Pull Request interface.

---

## 5. Understanding the Pull Request interface

A Pull Request contains several important areas.

### 5.1 Conversation

The Conversation tab contains:

- Pull Request description.
- General comments.
- Review summaries.
- Review requests.
- Activity timeline.
- Merge information.

Use it to understand the purpose and discussion surrounding a change.

### 5.2 Commits

The Commits tab displays the commits included in the Pull Request.

Example:

```text
a12bc34 docs(github): add pull request exercise
b23cd45 docs(github): correct module instructions
```

You can inspect:

- Commit messages.
- Authors.
- Commit dates.
- Individual commit changes.

This is useful when a Pull Request contains several commits.

### 5.3 Checks

The Checks tab displays automated validation results.

For example:

```text
Lint             Passed
Tests            Passed
Build            Passed
Security scan    Passed
```

These are illustrative checks.

You will configure real checks in Module 5 — GitHub Actions.

A Pull Request may be blocked from merging when required checks fail or have not completed.

### 5.4 Files changed

This is one of the most important sections for reviewers.

It displays the differences between the base branch and the proposed changes.

Example:

```diff
+# Pull Request Exercise
+
+This file is used to practise the Pull Request workflow.
+
+## Objectives
+
+- Create a feature branch.
+- Commit changes.
```

Green lines represent additions.

Red lines represent deletions.

Reviewers can leave comments on specific lines.

### Exercise

Open your Pull Request and inspect:

- Conversation.
- Commits.
- Checks.
- Files changed.

Identify which section you would use to inspect the actual documentation changes.

---

## 6. Draft Pull Requests

### What is a Draft Pull Request?

A Draft Pull Request is used to share work that is not ready for formal review.

For example, you might have implemented half of a feature and want your teammates to see your progress.

A draft:

- Cannot be merged.
- Communicates that work is incomplete.
- Can receive discussion and feedback.
- Can be converted into a normal Pull Request later.

GitHub does not automatically request Code Owner reviews while a Pull Request remains a draft.

### When should you use a draft?

Use a draft when:

- You want early technical feedback.
- The implementation is incomplete.
- You want to discuss an architectural approach.
- You want to share progress before requesting formal approval.

### How to create a Draft Pull Request

1. Push your feature branch.
2. Open the Pull Request creation page.
3. Select the option to create a Draft Pull Request.
4. Add your description.
5. Create it.

### Convert a draft into a normal Pull Request

When your work is ready:

1. Open the Draft Pull Request.
2. Select **Ready for review**.
3. Confirm the change.

GitHub then treats it as ready for formal review.

You can also convert a normal Pull Request back to a draft when additional work is required.

### Exercise

Create another small branch:

```bash
git switch main
git pull origin main
git switch -c docs/draft-pr-exercise
```

Create:

```text
docs/github/module-01-code/draft-exercise.md
```

Add:

```markdown
# Draft Pull Request Exercise

This document demonstrates a work-in-progress Pull Request.
```

Commit and push:

```bash
git add docs/github/module-01-code/draft-exercise.md
git commit -m "docs(github): add draft pull request exercise"
git push -u origin docs/draft-pr-exercise
```

Open a Draft Pull Request.

Inspect its status and available actions.

You can close this exercise Pull Request without merging it.

---

## 7. Requesting reviews

### 7.1 What is a Pull Request review?

A review allows another developer to examine your changes and provide feedback.

The reviewer can:

- Comment on the entire Pull Request.
- Comment on specific lines.
- Suggest modifications.
- Approve the changes.
- Request changes.

### 7.2 Review decisions

GitHub provides three main review decisions.

| Decision | Meaning |
|---|---|
| Comment | Provide feedback without approving or requesting changes |
| Approve | Indicate that the changes are acceptable |
| Request changes | Ask the author to correct something before merging |

### Comment

Use this when you have feedback or questions but are not making a formal approval decision.

Example:

```text
Could you explain why this section is located in the root directory?
```

### Approve

Use this when you have reviewed the changes and consider them ready.

Example:

```text
The documentation is clear, the file structure is correct,
and the examples are consistent.
```

### Request changes

Use this when a change needs correction.

Example:

```text
The command example uses the wrong branch name.
Please correct it before merging.
```

A review requesting changes can block merging when the target branch requires approval and the review is still blocking.

### 7.3 Request a reviewer

In the Pull Request page:

1. Find the Reviewers section.
2. Select the reviewer.
3. Confirm the request.

The reviewer receives a notification.

The author must have the appropriate permissions to request reviews.

### Important for solo training

If you are the only collaborator on your personal repository, you may not have another person available to approve your Pull Request.

You can still practise:

- Reading the review interface.
- Reviewing diffs.
- Writing review comments where permitted.
- Understanding approval requirements.
- Responding to feedback.

If you have a trusted collaborator, you can invite them to review the exercise. Do not grant someone access merely to complete this lesson.

### Exercise

Open your first Pull Request.

Inspect the Reviewers section.

If another collaborator is available, request a review. Otherwise, record where the review functionality is located and continue with the next section.

---

## 8. Reviewing changes effectively

A good code review examines more than whether the code compiles.

For documentation changes, review:

- Accuracy.
- Grammar and clarity.
- Markdown formatting.
- Broken links.
- Incorrect commands.
- Inconsistent file paths.
- Missing explanations.

For software changes, review:

- Correctness.
- Readability.
- Maintainability.
- Security.
- Error handling.
- Test coverage.
- Performance implications.
- Compatibility.

### 8.1 Reviewing a Pull Request

1. Open the Pull Request.
2. Select **Files changed**.
3. Inspect each changed file.
4. Review additions and deletions.
5. Add comments where clarification is needed.
6. Submit your review.

### 8.2 Reviewing a specific line

On GitHub:

1. Open **Files changed**.
2. Move to the relevant line.
3. Select the comment control.
4. Write your feedback.
5. Submit the comment or review.

Example:

```text
This command should use git switch instead of git checkout
to match the branch workflow taught in the previous lesson.
```

### 8.3 Good review comments

Good comments are:

- Specific.
- Constructive.
- Technically justified.
- Focused on the change.

Avoid comments such as:

```text
This is bad.
```

Prefer:

```text
This example does not explain what the -u option does.
Please add a short explanation so beginners understand
why the upstream branch is configured.
```

### 8.4 Suggested changes

GitHub allows reviewers to suggest exact modifications to certain lines.

Example:

```suggestion
git push -u origin feature/add-documentation
```

The author can accept the suggestion through GitHub.

For larger changes, update the file locally and push a new commit instead.

### Exercise

Inspect your Pull Request's Files changed tab.

Add at least one useful review comment if your account and review permissions allow it.

If no collaborator is available, practise identifying a potential documentation improvement and write down the feedback you would provide.

---

## 9. Responding to review feedback

After receiving feedback, the author should:

1. Read each review comment.
2. Understand what needs to change.
3. Update the relevant files.
4. Run appropriate checks.
5. Commit the corrections.
6. Push the new commit.
7. Respond to the reviewer.
8. Resolve the conversation when appropriate.
9. Request another review if needed.

### Example

A reviewer comments:

```text
The README does not link to the new lesson.
Please add it to the module index.
```

Update:

```text
docs/github/module-01-code/README.md
```

Add the missing lesson link.

Then:

```bash
git status
git add docs/github/module-01-code/README.md
git commit -m "docs(github): add lesson to module index"
git push
```

Because the commit is pushed to the same branch, GitHub automatically updates the existing Pull Request.

You do not need to create a second Pull Request.

### 9.1 Reply to comments

A good response explains what you did.

Example:

```text
Updated the module index and added the missing lesson link.
Thank you for pointing this out.
```

If you disagree, explain your reasoning respectfully.

### 9.2 Resolve conversations

Once the issue has been addressed:

1. Open the relevant review conversation.
2. Verify that the requested change is complete.
3. Select **Resolve conversation**, if you have permission.

Do not resolve a conversation just to make the Pull Request look clean. Make sure the underlying issue has actually been addressed.

GitHub also supports submitting review feedback and suggestions as part of the review workflow.

### Exercise

Update the Pull Request branch with one additional documentation improvement.

Example:

```bash
git switch docs/add-pull-request-guide
```

Edit `pr-exercise.md`, then:

```bash
git add docs/github/module-01-code/pr-exercise.md
git commit -m "docs(github): improve pull request exercise"
git push
```

Open GitHub and confirm that the existing Pull Request contains the new commit.

---

## 10. Synchronizing a feature branch with main

### 10.1 Why synchronize branches?

Imagine that you created a feature branch yesterday.

Today, another developer merges new changes into `main`.

Your feature branch is now behind the latest main branch.

```text
main:

A---B---C---D

feature:

A---B---E---F
```

Your feature branch does not contain commits `C` and `D`.

You may need to synchronize it before merging your Pull Request.

### 10.2 Fetch the latest remote changes

```bash
git fetch origin
```

Explanation:

- `git fetch`: downloads remote changes.
- `origin`: the remote repository.
- It updates remote-tracking references without merging them into your current branch.

Inspect the branches:

```bash
git log --oneline --graph --all --decorate
```

This displays a visual representation of commit history.

### 10.3 Option A — Merge main into your feature branch

First, switch to your feature branch:

```bash
git switch docs/add-pull-request-guide
```

Then:

```bash
git merge origin/main
```

This integrates the latest remote main branch into your feature branch.

Advantages:

- Preserves the existing feature branch history.
- Does not rewrite your feature commits.
- Useful when the team prefers merge-based synchronization.

Disadvantages:

- May create an additional merge commit.
- Can make the history more complex.

### 10.4 Option B — Rebase your feature branch

First:

```bash
git switch docs/add-pull-request-guide
git fetch origin
```

Then:

```bash
git rebase origin/main
```

Rebase replays your feature commits on top of the latest main branch.

Before:

```text
A---B---C---D  main
     \
      E---F   feature
```

After:

```text
A---B---C---D---E'---F'  feature
```

The feature commits receive new commit hashes because their parent relationships change.

### Merge versus rebase

| Operation | Effect |
|---|---|
| `git merge origin/main` | Integrates main into the feature branch |
| `git rebase origin/main` | Replays feature commits on top of main |

Use one synchronization approach at a time.

For this training repository, use merge for the first exercise so that you can inspect the resulting history. Practise rebase separately.

### 10.5 Push after synchronization

After merging:

```bash
git push
```

After rebasing, if the branch has already been pushed, the remote history may need to be updated.

If you are the only person working on the branch:

```bash
git push --force-with-lease
```

`--force-with-lease` checks that the remote branch has not changed unexpectedly before updating it.

Never force-push a shared branch without coordinating with its contributors.

### Exercise

1. Create a feature branch.
2. Push it.
3. Add a second commit to `main` using a separate documentation branch and Pull Request.
4. Return to the feature branch.
5. Run `git fetch origin`.
6. Inspect the branch history.
7. Merge `origin/main` into your feature branch.
8. Push the synchronized branch.
9. Inspect the Pull Request.

You should see the latest main changes reflected in your feature branch.

---

## 11. Understanding merge conflicts

### 11.1 What is a merge conflict?

A merge conflict occurs when Git cannot automatically combine changes.

A common example is when two branches modify the same part of the same file differently.

Example:

Branch A:

```text
Project status: In progress
```

Branch B:

```text
Project status: Completed
```

If both branches modify the same line, Git may need you to decide which content should remain.

### 11.2 Conflict markers

Git may display conflict markers inside a file:

```text
<<<<<<< HEAD
Project status: In progress
=======
Project status: Completed
>>>>>>> feature/update-status
```

Meaning:

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Beginning of the current branch's version |
| `=======` | Separates the two versions |
| `>>>>>>> branch-name` | End of the incoming branch's version |

You must edit the file and remove these markers.

### 11.3 Practical merge conflict exercise

We will create a controlled conflict using a disposable training file.

First, make sure your working tree is clean:

```bash
git status
```

Update main:

```bash
git switch main
git pull origin main
```

Create a shared exercise file:

```text
docs/github/module-01-code/conflict-exercise.md
```

Add:

```markdown
# Merge Conflict Exercise

Project status: Initial
```

Commit and push this file:

```bash
git add docs/github/module-01-code/conflict-exercise.md
git commit -m "docs(github): add merge conflict exercise"
git push
```

Now create the first branch:

```bash
git switch -c exercise/conflict-a
```

Change the status line to:

```markdown
Project status: Updated by branch A
```

Commit:

```bash
git add docs/github/module-01-code/conflict-exercise.md
git commit -m "docs(github): update status from branch a"
```

Return to main:

```bash
git switch main
```

Create the second branch:

```bash
git switch -c exercise/conflict-b
```

Change the same line to:

```markdown
Project status: Updated by branch B
```

Commit:

```bash
git add docs/github/module-01-code/conflict-exercise.md
git commit -m "docs(github): update status from branch b"
```

Now return to branch A:

```bash
git switch exercise/conflict-a
```

Merge branch B:

```bash
git merge exercise/conflict-b
```

Git should report a conflict because both branches changed the same line differently.

### 11.4 Inspect the conflict

```bash
git status
```

You should see the conflicting file listed.

Open it in VS Code.

VS Code provides conflict resolution options such as:

- Accept Current Change.
- Accept Incoming Change.
- Accept Both Changes.
- Compare Changes.

For this exercise, do not blindly select an option. Understand what each version contains.

Replace the conflicting content with:

```markdown
# Merge Conflict Exercise

Project status: Resolved successfully
```

Save the file.

### 11.5 Mark the conflict as resolved

```bash
git add docs/github/module-01-code/conflict-exercise.md
```

Complete the merge:

```bash
git commit -m "docs(github): resolve merge conflict exercise"
```

Inspect the history:

```bash
git log --oneline --graph --decorate -10
```

### 11.6 Useful conflict commands

Check conflict status:

```bash
git status
```

Inspect unresolved files:

```bash
git diff --name-only --diff-filter=U
```

Inspect unresolved differences:

```bash
git diff
```

After resolving:

```bash
git add path/to/file
git commit
```

### 11.7 Abort a merge

If you started a merge and decide not to continue:

```bash
git merge --abort
```

This attempts to return the working tree to the state before the merge started.

Only use it while a merge is in progress.

### 11.8 Abort a rebase

If you are in the middle of a rebase:

```bash
git rebase --abort
```

This returns the branch to its pre-rebase state.

Do not confuse merge and rebase recovery commands.

### Exercise

Complete the conflict exercise.

Your final file must contain:

```markdown
Project status: Resolved successfully
```

Then inspect the Git history and verify that the merge was completed.

---

## 12. Auto-merge

### 12.1 What is auto-merge?

Auto-merge allows GitHub to merge a Pull Request automatically when all required conditions are satisfied.

For example:

```text
Pull Request created
       |
       v
Review approval received
       |
       v
Automated checks pass
       |
       v
No merge conflicts
       |
       v
Auto-merge executes
```

This reduces manual work when a Pull Request is waiting for required conditions.

### 12.2 When should you use auto-merge?

Useful situations:

- CI checks take time.
- Review approvals are required.
- The team has clear merge requirements.
- The Pull Request is already reviewed and ready.

Do not enable auto-merge for changes you have not reviewed.

### 12.3 Enable auto-merge

Auto-merge must be enabled in the repository settings.

Typical navigation:

```text
Repository
    |
    v
Settings
    |
    v
General
    |
    v
Pull Requests
    |
    v
Allow auto-merge
```

The feature is subject to repository settings and applicable requirements.

### 12.4 Use auto-merge

1. Open a Pull Request.
2. Ensure that the Pull Request is not a draft.
3. Select the merge method.
4. Select **Enable auto-merge**, if available.
5. Wait for the required reviews and checks.

GitHub merges the Pull Request when its required conditions are met.

### 12.5 Disable auto-merge

If the Pull Request should no longer merge automatically, use the available option to disable auto-merge.

### Exercise

Inspect the auto-merge setting.

If available:

1. Enable it.
2. Open a test Pull Request.
3. Inspect the merge options.
4. Do not enable auto-merge for an unreviewed change.
5. Disable the setting if you do not intend to use it.

You can complete this exercise without requiring another collaborator or a real CI workflow.

---

## 13. CODEOWNERS

### 13.1 What is CODEOWNERS?

`CODEOWNERS` is a special file that defines which users or teams are responsible for specific parts of a repository.

GitHub can automatically request reviews from the relevant Code Owners when a Pull Request changes files they own.

This is particularly useful in larger projects.

### 13.2 Example project structure

Imagine a DRF + React project:

```text
project/
│
├── backend/
│   ├── authentication/
│   ├── orders/
│   └── payments/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── services/
│
└── docs/
```

You might assign:

| Directory | Responsible team |
|---|---|
| `backend/` | Backend team |
| `frontend/` | Frontend team |
| `docs/` | Documentation team |

### 13.3 Create the CODEOWNERS file

GitHub searches for the file in these locations:

```text
.github/CODEOWNERS
CODEOWNERS
docs/CODEOWNERS
```

Use only one location for your exercise:

```text
.github/CODEOWNERS
```

### 13.4 CODEOWNERS syntax

Example:

```text
# All repository files
* @github-username

# Documentation
/docs/ @github-username

# GitHub configuration
/.github/ @github-username
```

Explanation:

| Pattern | Meaning |
|---|---|
| `*` | All files |
| `/docs/` | Files under the docs directory |
| `/.github/` | Files under the .github directory |
| `@username` | Assigns an individual GitHub user |
| `@organization/team-name` | Assigns an organization team |

Replace the example username with an actual GitHub username.

Organization team references require an appropriate organization and team configuration.

### 13.5 Pattern precedence

If multiple patterns match a file, the last matching pattern in the CODEOWNERS file determines the owner.

Example:

```text
* @general-owner
/docs/ @documentation-owner
/docs/security/ @security-owner
```

A file inside `docs/security/` is assigned to `@security-owner`.

### 13.6 Important limitations

- Code Owners must have appropriate repository access.
- Team references must point to valid teams.
- Code Owners can be automatically requested for review when a Pull Request is ready for review.
- Draft Pull Requests do not automatically request Code Owner reviews.
- To require Code Owner approval before merging, configure the relevant branch protection or ruleset requirement.

### Exercise

Create:

```text
.github/CODEOWNERS
```

For your personal training repository, use your own GitHub username as the owner.

Example:

```text
* @YOUR_GITHUB_USERNAME
```

Replace the placeholder before committing.

Commit:

```bash
git add .github/CODEOWNERS
git commit -m "docs(github): add code owners configuration"
```

Push and inspect the Pull Request behaviour.

If you are the only contributor, the file still teaches the configuration format, but it does not demonstrate a multi-person review workflow.

---

## 14. Closing versus merging a Pull Request

Not every Pull Request should be merged.

### Merge

Use Merge when:

- The change is correct.
- Required reviews are complete.
- Required checks pass.
- Conflicts are resolved.
- The change is ready to integrate.

### Close without merging

Use Close when:

- The proposed change is no longer needed.
- The change is incorrect.
- Another Pull Request replaces it.
- The work has been abandoned.
- The proposed solution will not be implemented.

Closing a Pull Request preserves its discussion and history.

### Reopen

If a Pull Request was closed without merging and the work is still relevant, it may be possible to reopen it.

### Exercise

Open your draft exercise Pull Request.

Close it without merging.

Then inspect:

- Its final status.
- Its conversation history.
- Its commits.
- Its available actions.

---

## 15. Cleaning up branches

After merging a Pull Request, GitHub often offers to delete the source branch.

This keeps the repository organized.

### Delete through GitHub

After merging:

1. Open the merged Pull Request.
2. Select **Delete branch**, if available.

### Delete a local branch

```bash
git branch -d docs/add-pull-request-guide
```

The `-d` option safely deletes a branch that Git considers merged.

### Delete a remote branch

```bash
git push origin --delete docs/add-pull-request-guide
```

This removes the remote branch.

### Update your local main

```bash
git switch main
git pull origin main
```

### Remove stale remote-tracking branches

```bash
git fetch --prune
```

This removes local references to remote branches that no longer exist on the server.

### Exercise

After merging your main Pull Request:

1. Delete the remote feature branch.
2. Delete the local feature branch.
3. Update main.
4. Run:

```bash
git branch -a
git status
```

Verify that the merged feature branch is no longer listed.

Do not delete `main`.

---

## 16. Practical collaboration exercise

Now combine the concepts from this lesson.

### Scenario

You are contributing a new lesson to `github-deep-dive-training`.

You need to:

1. Create a feature branch.
2. Write a Markdown document.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.
6. Review the changed files.
7. Receive or simulate review feedback.
8. Make a correction.
9. Push the correction.
10. Synchronize your branch if main has changed.
11. Resolve conflicts if necessary.
12. Merge the Pull Request.
13. Delete the feature branch.

### Step 1 — Create the branch

```bash
git switch main
git pull origin main
git switch -c docs/pr-collaboration-practice
```

### Step 2 — Create the document

Create:

```text
docs/github/module-01-code/collaboration-practice.md
```

Content:

```markdown
# Collaboration Practice

## Objective

Practise the GitHub Pull Request workflow.

## Workflow

1. Create a feature branch.
2. Make a change.
3. Commit the change.
4. Push the branch.
5. Open a Pull Request.
6. Review the changes.
7. Merge the Pull Request.

## Result

The collaboration exercise is complete.
```

### Step 3 — Commit

```bash
git add docs/github/module-01-code/collaboration-practice.md
git commit -m "docs(github): add collaboration practice"
```

### Step 4 — Push

```bash
git push -u origin docs/pr-collaboration-practice
```

### Step 5 — Open a Pull Request

Use:

```text
Title:
docs(github): add collaboration practice
```

Description:

```markdown
## Summary

Adds a practical exercise for learning Pull Request collaboration.

## Changes

- Added collaboration-practice.md.
- Added a step-by-step workflow.

## Validation

- [x] Reviewed Markdown.
- [x] Verified the file path.
- [x] Checked the Git diff.
```

### Step 6 — Review the Pull Request

Inspect:

- Conversation.
- Commits.
- Checks.
- Files changed.

### Step 7 — Make an update

Add this section to the document:

```markdown
## Additional learning

Pull Requests make changes easier to review before they are merged.
```

Commit:

```bash
git add docs/github/module-01-code/collaboration-practice.md
git commit -m "docs(github): expand collaboration exercise"
git push
```

### Step 8 — Merge

Once the changes are ready and repository requirements are satisfied:

1. Select Squash and merge.
2. Review the final commit message.
3. Merge the Pull Request.
4. Delete the source branch.

### Step 9 — Verify

```bash
git switch main
git pull origin main
git log --oneline -10
git status
```

Verify that the document is present in `main`.

---

## 17. Troubleshooting

### Pull Request says there are conflicts

Fetch the latest changes:

```bash
git fetch origin
```

Merge main into the feature branch:

```bash
git switch your-feature-branch
git merge origin/main
```

Resolve conflicts, stage the corrected files, and complete the merge.

### Pull Request is blocked by required reviews

Check:

- Whether the required number of approvals has been received.
- Whether a review requested changes.
- Whether an approval was dismissed.
- Whether Code Owner approval is required.

### Pull Request is blocked by status checks

Open the Checks tab.

Inspect the failed or pending checks.

You will learn how to configure and troubleshoot these workflows in the Actions module.

### A new commit does not appear in my Pull Request

Check that you pushed to the same branch used by the Pull Request:

```bash
git branch --show-current
git remote -v
git status
```

Then:

```bash
git push
```

### Git reports an unresolved merge conflict

Run:

```bash
git status
```

Open each conflicting file.

Resolve the conflict markers.

Stage the corrected files:

```bash
git add path/to/file
```

Complete the merge:

```bash
git commit
```

### I accidentally created a Pull Request against the wrong branch

You can change the base branch from the Pull Request page if the intended target is available.

Review the resulting diff carefully after changing the base branch.

---

## 18. Completion checklist

### Pull Request basics

- [ ] Created a feature branch.
- [ ] Pushed the branch.
- [ ] Created a Pull Request.
- [ ] Understood base and head branches.
- [ ] Inspected all Pull Request tabs.

### Draft Pull Requests

- [ ] Created a Draft Pull Request.
- [ ] Inspected its status.
- [ ] Understood how to mark it ready for review.

### Reviews

- [ ] Understood Comment, Approve, and Request changes.
- [ ] Inspected the reviewer interface.
- [ ] Practised reviewing a diff.
- [ ] Understood suggested changes.
- [ ] Understood how to respond to feedback.
- [ ] Understood how to resolve conversations.

### Branch synchronization

- [ ] Used `git fetch`.
- [ ] Inspected branch history.
- [ ] Merged main into a feature branch.
- [ ] Understood rebase.
- [ ] Understood `--force-with-lease`.

### Merge conflicts

- [ ] Created a controlled merge conflict.
- [ ] Identified conflict markers.
- [ ] Resolved the conflict in VS Code.
- [ ] Completed the merge.
- [ ] Inspected the final Git history.

### Advanced collaboration

- [ ] Inspected auto-merge.
- [ ] Created a CODEOWNERS file.
- [ ] Understood branch cleanup.
- [ ] Merged a Pull Request.
- [ ] Deleted an obsolete feature branch.

---

## 19. Recommended commit messages

Use Conventional Commits for the documentation work.

Examples:

```bash
git commit -m "docs(github): add pull request collaboration lesson"
git commit -m "docs(github): add draft pull request exercise"
git commit -m "docs(github): add code owners configuration"
git commit -m "docs(github): add merge conflict exercise"
git commit -m "docs(github): improve review workflow examples"
```

For the complete lesson document, use:

```bash
git commit -m "docs(github): add pull request collaboration lesson"
```

---

## 20. Tags and releases

Continue using the versioning and release strategy established in Lesson 5.

Do not create a tag for every lesson.

The next planned release milestone is completion of Module 1.

Before publishing it, verify:

```bash
git status
git log --oneline -10
git tag
```

Make sure the intended release tag does not already exist.

Prepare a changelog that summarizes the completed lessons and practical exercises.

---

## 21. What comes next?

**Lesson 09 — GitHub Forks and Open-Source Contribution Workflow**

Topics:

- What is a fork?
- Fork versus clone.
- Upstream and origin remotes.
- Fork-and-pull development model.
- Cloning your fork.
- Synchronizing a fork with upstream.
- Creating Pull Requests from forks.
- Contributing to external repositories.
- Handling upstream changes.
- Open-source contribution etiquette.


# Module 3 — GitHub Pull Requests

## Lesson 30: Pull Request Management — Merge Conflicts, Updating Branches and Keeping PRs Healthy

### Practical Lesson

**Level:** Intermediate–Advanced

**Estimated time:** 3–4 hours

---

## Lesson Introduction

In Lesson 28, you learned how to create, configure, and manage Pull Requests.

In Lesson 29, you practised advanced Pull Request reviews, including inline comments, review decisions, suggested changes, and resolving conversations.

Now we'll address another important part of professional GitHub collaboration: **keeping Pull Requests synchronized with their target branches and resolving merge conflicts.**

Imagine you're working on your restaurant POS application.

You create a feature branch:

```bash
feat/order-management
```

While you're implementing the feature, another developer merges changes into `main`.

Your feature branch is now behind `main`.

What happens if both developers modify the same part of a file?

You may encounter a merge conflict.

Merge conflicts are a normal part of collaborative development. They don't necessarily indicate that something is wrong with your code. They simply mean Git needs your help to determine how different changes should be combined.

In this lesson, you'll learn how to understand, reproduce, prevent, and resolve these situations while maintaining healthy Pull Requests.

## 1. Learning Objectives

By the end of this lesson, you should be able to:

1. Explain what merge conflicts are and why they happen.
2. Understand branch divergence and fast-forward versus non-fast-forward updates.
3. Identify common types of merge conflicts.
4. Understand how Git compares changes from different branches.
5. Detect merge conflicts locally and through GitHub.
6. Update feature branches using Git merge.
7. Update feature branches using Git rebase.
8. Resolve conflicts manually using Git.
9. Resolve conflicts using the VS Code Merge Editor.
10. Abort an unsuccessful merge or rebase safely.
11. Understand how new commits affect Pull Request reviews and approvals.
12. Recognize outdated and stale Pull Requests.
13. Keep Pull Requests focused, reviewable, and maintainable.
14. Collaborate with another developer to resolve conflicting changes.
15. Publish your Lesson 30 documentation using your established GitHub workflow.

## 2. Understanding Merge Conflicts

### 2.1 What Is a Merge Conflict?

A merge conflict occurs when Git cannot automatically combine changes from different branches.

Consider the following situation.

Your `main` branch contains:

```python
ORDER_STATUS = "pending"
```

You create a feature branch and change it to:

```python
ORDER_STATUS = "preparing"
```

Meanwhile, another developer changes the same line in `main`:

```python
ORDER_STATUS = "confirmed"
```

Git now has two different modifications to the same line.

Which value should it use?

Git cannot reliably determine the correct business requirement.

You must resolve the conflict.

### 2.2 Visualizing Branch Divergence

Imagine the following history:

```text
A --- B --- C (main)
       \
        D (feature)
```

Both branches started from commit `B`.

However:

- Developer A committed `D` on the feature branch.
- Developer B committed `C` on main.

The branches have diverged.

When you attempt to integrate `main` into the feature branch, Git needs to combine the two histories.

If the changes are compatible, Git may complete the merge automatically.

If the changes conflict, Git pauses and requests manual resolution.

### 2.3 Common Causes of Merge Conflicts

| Situation | Explanation |
|---|---|
| Same-line modifications | Two developers modify the same lines differently. |
| Delete versus modify | One branch deletes a file while another modifies it. |
| Rename conflicts | Branches rename or move files incompatibly. |
| Add/add conflicts | Both branches create a file at the same path with different content. |
| Overlapping structural changes | Different modifications cannot be combined safely. |

**Important:** Modifying the same file does not automatically produce a merge conflict.

For example:

Developer A changes line 10.

Developer B changes line 100.

Git can often combine these changes automatically.

The important distinction is whether the changes overlap in a way Git cannot reconcile.

### 2.4 Three Important Concepts

| Concept | Meaning |
|---|---|
| Branch divergence | Two branches have different commits after their common ancestor. |
| Merge conflict | Git cannot automatically combine particular changes. |
| Conflict resolution | A developer determines the correct final content. |

Branch divergence does not necessarily mean a conflict exists.

You can have divergent branches that merge successfully without any manual intervention.

## 3. Understanding Fast-Forward, Non-Fast-Forward, Merge and Rebase

Before resolving conflicts, understand how Git integrates branches.

### 3.1 Fast-Forward Merge

A fast-forward merge happens when the current branch has no additional commits that prevent Git from simply moving its branch pointer forward.

Example:

```text
Before:

A --- B (main)
       \
        C --- D (feature)
```

If `main` is still at `B`, it can advance to `D`.

After:

```text
A --- B --- C --- D (main)
```

No merge commit is required.

Command:

```powershell
git switch main
git merge feature
```

### 3.2 Non-Fast-Forward Merge

A non-fast-forward merge happens when both branches have independent commits.

Example:

```text
         C --- D (main)
        /
A --- B
        \
         E --- F (feature)
```

Git needs to combine both histories.

A merge commit may be created:

```text
         C --- D
        /       \
A --- B           M
        \       /
         E --- F
```

The merge commit `M` records the integration of the two histories.

### 3.3 Merge

A merge combines the histories of two branches.

```powershell
git switch feature/orders
git merge main
```

The feature branch receives the changes from `main`.

Existing feature commits retain their original identities.

### 3.4 Rebase

A rebase replays your feature commits on top of another branch.

```powershell
git switch feature/orders
git rebase main
```

Conceptually:

Before:

```text
A --- B --- C (main)
       \
        D --- E (feature)
```

After:

```text
A --- B --- C (main)
             \
              D' --- E' (feature)
```

The commits are replayed and receive new commit IDs.

Rebase creates a more linear history, but it rewrites the feature branch's history.

### 3.5 Conflict Resolution

When Git cannot automatically integrate changes, it pauses the operation.

You must:

1. Inspect the affected files.
2. Understand both versions.
3. Decide what the final content should be.
4. Remove conflict markers.
5. Stage the resolved files.
6. Continue the merge or rebase.

**Professional recommendation:** Never resolve a conflict by blindly accepting one version. Understand the intended functionality first.

## 4. Prepare the Training Environment

We'll use your existing training repository:

`github-deep-dive-training`

We'll simulate two developers modifying the same documentation file.

### 4.1 Synchronize Your Repository

Open PowerShell inside your repository.

```powershell
git switch main
git pull --ff-only origin main

git status
```

Make sure your working tree is clean.

If Git reports local modifications, preserve or commit them before starting the exercise.

### 4.2 Create the Practice Directory

Our structure will be:

```text
docs/
└── github/
    └── module-03-pull-requests/
        └── conflict-practice.md
```

Create the directory:

```powershell
New-Item -ItemType Directory `
  -Force docs/github/module-03-pull-requests
```

Create the file:

```powershell
New-Item -ItemType File `
  -Force docs/github/module-03-pull-requests/conflict-practice.md
```

### 4.3 Add the Initial Content

Open the file and add:

```markdown
# Merge Conflict Practice

## Restaurant Order Status

The default order status is:

`pending`

## Business Rule

Every newly created order starts as pending.

## Responsible Team

The order management team maintains this workflow.
```

### 4.4 Commit the Initial Version

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md

git commit -m "docs(github): add merge conflict practice"

git push origin main
```

We now have a common starting point for both developers.

## 5. Create Two Branches and Introduce Conflicting Changes

We'll simulate two developers working independently.

### Developer A

Feature branch:

```text
feat/order-status-update
```

#### Developer B

Main branch:

```text
main
```

Both developers will modify the same section of the same file.

### 5.1 Developer A Creates a Feature Branch

Start from the latest main:

```powershell
git switch main
git pull --ff-only origin main
```

Create the branch:

```powershell
git switch -c feat/order-status-update
```

Modify `conflict-practice.md`:

```markdown
# Merge Conflict Practice

## Restaurant Order Status

The default order status is:

`preparing`

## Business Rule

Every newly created order starts as preparing.

## Responsible Team

The kitchen team maintains this workflow.
```

Commit:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md

git commit -m "docs(orders): update default order status"
```

Do not push yet.

### 5.2 Developer B Modifies Main

Switch back to main:

```powershell
git switch main
```

Modify the same file:

```markdown
# Merge Conflict Practice

## Restaurant Order Status

The default order status is:

`confirmed`

## Business Rule

Every newly created order starts as confirmed.

## Responsible Team

The cashier team maintains this workflow.
```

Commit and push:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md

git commit -m "docs(orders): update order confirmation status"

git push origin main
```

Now the branches have diverged.

Developer A has one version, while `main` contains another.

### 5.3 Inspect the Branch History

Run:

```powershell
git log --oneline --graph --decorate --all
```

You should see two branches with independent commits.

This is the situation that can produce a merge conflict.

## 6. Reproduce and Resolve Your First Merge Conflict

### 6.1 Attempt to Merge Main

Switch back to Developer A's branch:

```powershell
git switch feat/order-status-update
```

Merge the latest main:

```powershell
git merge main
```

Git should report a conflict.

You may see:

```text
Auto-merging docs/github/module-03-pull-requests/conflict-practice.md

CONFLICT (content): Merge conflict in
docs/github/module-03-pull-requests/conflict-practice.md

Automatic merge failed; fix conflicts and then commit the result.
```

This is expected.

You have successfully reproduced a merge conflict.

### 6.2 Understand Conflict Markers

Open the affected file.

You should see something similar to:

```text
[Conflict start: HEAD]
The default order status is:

`preparing`
─────────────────────
The default order status is:

`confirmed`
[Conflict end: main]
```

Understand each marker:

| Marker | Meaning |
|---|---|
| `<<<<<<< HEAD` | Beginning of the current side of the conflict. |
| `=======` | Separates the two versions. |
| `>>>>>>> main` | Beginning/end marker identifying the incoming side. |

The exact displayed branch name may differ.

During this merge:

- `HEAD` represents the currently checked-out feature branch.
- The incoming changes come from `main`.

These markers are Git's way of showing you the competing content.

### 6.3 Inspect the Conflict Before Resolving It

Run:

```powershell
git status
```

You should see the affected file listed as unmerged.

You can inspect the conflict using:

```powershell
git diff
```

You can also inspect the two sides using:

```powershell
git show :2:docs/github/module-03-pull-requests/conflict-practice.md

git show :3:docs/github/module-03-pull-requests/conflict-practice.md
```

During an unresolved merge:

- Stage 2 represents the current branch's version.
- Stage 3 represents the incoming branch's version.

These commands are useful when you need to inspect the original versions before resolving the file.

### 6.4 Resolve the Conflict Manually

Now determine the correct business requirement.

For our exercise:

- Every new order starts as `pending`.
- Kitchen staff move orders to `preparing`.
- Cashiers confirm payment.
- The order becomes `ready` after preparation.

Replace the conflicting content with:

```markdown
# Merge Conflict Practice

## Restaurant Order Status

The default order status is:

`pending`

## Business Rule

1. Every newly created order starts as pending.
2. Kitchen staff move the order to preparing.
3. The cashier confirms payment.
4. The order becomes ready after preparation.

## Responsible Teams

- Kitchen team: preparation status.
- Cashier team: payment confirmation.
- Order management team: overall workflow.
```

Save the file.

### 6.5 Stage the Resolved File

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md
```

Staging the file tells Git that you have resolved its conflict.

### 6.6 Verify the Resolution

```powershell
git status
```

The unmerged status should disappear.

Check whitespace problems:

```powershell
git diff --check
```

Make sure the conflict markers have been removed.

### 6.7 Complete the Merge

```powershell
git commit -m "merge: resolve order status documentation conflict"
```

### 6.8 Inspect the History

```powershell
git log --oneline --graph --decorate --all
```

You should see the two histories joined by a merge commit.

### 6.9 Push the Feature Branch

```powershell
git push -u origin feat/order-status-update
```

You have now resolved and published your first merge conflict.

## 7. Resolve Conflicts Using VS Code

Manual conflict resolution is useful, but VS Code provides a graphical interface that makes the process easier.

### 7.1 Open Your Repository

```powershell
code .
```

VS Code includes built-in Git integration and a Merge Editor.

### 7.2 Understand the Conflict Resolution Options

When a conflict occurs, VS Code identifies the affected file.

Depending on the version and context, you may see options such as:

| Option | Meaning |
|---|---|
| Accept Current Change | Keep the current branch's version. |
| Accept Incoming Change | Keep the incoming branch's version. |
| Accept Both Changes | Include both versions. |
| Compare Changes | Inspect differences between versions. |

None of these options automatically guarantees the correct business outcome.

### 7.3 Understand Current Versus Incoming

Suppose the conflict contains:

```text
Current:

preparing

Incoming:

confirmed
```

If you select:

- Accept Current: keeps `preparing`.
- Accept Incoming: keeps `confirmed`.
- Accept Both: includes both versions, which may require additional editing.

Remember that accepting both changes does not necessarily produce valid documentation or application logic.

### 7.4 Use the Three-Way Merge Editor

The VS Code Merge Editor typically presents three views:

#### Incoming

Changes being merged into your branch.

#### Current

Your existing branch's content.

#### Result

The final content that will be saved.

You can select changes from either side and manually edit the result.

The exact interface can vary with VS Code versions and configuration.

### 7.5 Complete the Resolution

After editing the result:

1. Save the file.
2. Verify that no conflict markers remain.
3. Stage the resolved file.
4. Confirm Git no longer reports an unmerged file.
5. Complete the merge.

Commands:

```powershell
git status

git add .

git diff --check

git status

git commit -m "merge: resolve documentation conflict"
```

Only create the merge commit if the merge is still awaiting completion.

#### Exercise 1 — VS Code Conflict Resolution

Repeat the previous conflict exercise using VS Code instead of manually editing the conflict markers.

Your objective is to become comfortable with both approaches.

## 8. Abort a Merge When Necessary

Sometimes you start resolving a conflict and realize that you need to restart.

Git provides:

```powershell
git merge --abort
```

This attempts to return your working tree and index to the state before the merge started.

### 8.1 Practical Example

Start with a clean feature branch:

```powershell
git switch feat/order-status-update

git status
```

Attempt a merge that produces a conflict:

```powershell
git merge main
```

If you decide to cancel:

```powershell
git merge --abort
```

Check:

```powershell
git status
```

Your feature branch should return to its pre-merge state.

### 8.2 Merge Recovery Commands

| Command | Purpose |
|---|---|
| `git merge main` | Merge main into the current branch. |
| `git merge --abort` | Abort an active merge. |
| `git status` | Inspect the current repository state. |
| `git diff` | Inspect working-tree changes. |
| `git diff --check` | Check whitespace problems. |
| `git log --graph` | Inspect branch history. |

**Important:** Preserve unrelated uncommitted work before starting a merge. `git merge --abort` is not a universal recovery mechanism for every working-tree situation.

## 9. Update a Feature Branch From Main

One of the most common Pull Request maintenance tasks is keeping your feature branch synchronized with its target branch.

Imagine:

```text
main:

A --- B --- C --- D

feature:

     \--- E --- F
```

Your feature branch started from `B`, but `main` now contains `C` and `D`.

You need to update your feature branch.

There are two common approaches.

### 9.1 Approach A — Merge Main Into the Feature Branch

First:

```powershell
git switch feat/order-status-update

git status

git fetch origin
```

Merge the latest remote main:

```powershell
git merge origin/main
```

This integrates the latest main changes into your feature branch.

If conflicts occur:

1. Inspect the affected files.
2. Resolve the conflicts.
3. Stage the resolved files.
4. Complete the merge.

Then:

```powershell
git push origin feat/order-status-update
```

**Advantages:**

- Preserves existing feature commits.
- Does not rewrite existing feature history.
- Suitable for shared feature branches.

**Disadvantages:**

- May create additional merge commits.
- Can make the history more complicated.

### 9.2 Approach B — Rebase the Feature Branch Onto Main

First, ensure your working tree is clean.

```powershell
git switch feat/order-status-update

git status

git fetch origin
```

Rebase:

```powershell
git rebase origin/main
```

Git replays your feature commits on top of the latest main.

If a conflict occurs:

```powershell
git status
```

Resolve the affected files, then stage them:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md
```

Continue:

```powershell
git rebase --continue
```

Repeat until the rebase finishes.

If you need to cancel:

```powershell
git rebase --abort
```

### 9.3 What Happens When You Rebase an Already-Pushed Branch?

If you have already pushed your feature branch, rebasing may change its commit IDs.

Consequently, a normal push may be rejected.

You may need:

```powershell
git push --force-with-lease origin feat/order-status-update
```

**Important:**

`--force-with-lease` is safer than ordinary `--force` because it checks that the remote branch has not changed unexpectedly since your last known state.

However, it still rewrites remote history.

Use it only when you understand the consequences and have coordinated with anyone sharing the branch.

For shared feature branches, prefer avoiding unnecessary history rewriting.

### 9.4 Merge Versus Rebase

| Criteria | Merge | Rebase |
|---|---|---|
| Preserves existing commit IDs | Yes | No, replayed commits receive new IDs. |
| Creates merge commit | Sometimes | No, not for the rebase itself. |
| Produces linear history | Not necessarily | Usually |
| Rewrites feature history | No | Yes |
| Suitable for shared branches | Generally safer | Requires coordination |
| Suitable for private feature branches | Yes | Yes |

**Professional recommendation:**

Practise both approaches.

Use merge when preserving shared branch history is important.

Use rebase when a cleaner feature-branch history is desired and the branch is safe to rewrite.

## 10. Understand GitHub's Merge Conflict Indicators

GitHub can detect when a Pull Request cannot be merged automatically.

### 10.1 Inspect the Pull Request

Create a PR:

```text
feat/order-status-update → main
```

Open the Pull Request on GitHub.

When the branches contain unresolved merge conflicts, GitHub may display a message similar to:

```text
This branch has conflicts that must be resolved.
```

Depending on the conflict type and repository configuration, GitHub may also offer a **Resolve conflicts** option.

### 10.2 Resolve Conflicts Through GitHub

For supported text conflicts:

1. Open the Pull Request.
2. Locate the merge-conflict notification.
3. Select Resolve conflicts if available.
4. Edit the conflicting content.
5. Mark the conflict as resolved.
6. Save the resolution.
7. Review the updated Pull Request.

GitHub creates the corresponding resolution commit.

### 10.3 Understand GitHub's Limitations

The web conflict editor does not support every conflict type.

For example:

- Binary file conflicts.
- Some rename conflicts.
- More complicated file operations.
- Complex conflicts requiring local testing.

These situations may require local Git and an editor such as VS Code.

### 10.4 Recommended Resolution Method

| Situation | Preferred method |
|---|---|
| Simple text conflict | GitHub editor or VS Code |
| Multiple conflicting files | Local Git + VS Code |
| Complex merge | Local Git |
| Binary file conflict | Appropriate local tool |
| Shared branch with collaborators | Coordinate before rewriting history |

#### Exercise 2 — GitHub Conflict Indicator

Create a PR from your feature branch.

Then introduce a conflicting change into `main` using another branch or collaborator.

Inspect the PR page.

Record:

1. Whether GitHub detects the conflict.
2. Whether the merge button is disabled.
3. Whether GitHub offers a conflict-resolution option.
4. Whether the conflict can be resolved through the web interface.
5. Whether additional local work is necessary.

Do not merge until the conflict is resolved and the updated changes have been reviewed.

## 11. What Happens to Pull Request Reviews After Updating a PR?

This is particularly important because you learned formal reviews in Lesson 29.

Suppose:

1. Developer A opens a PR.
2. Developer B reviews and approves it.
3. Developer A pushes additional commits.
4. The PR now contains new changes.

Should Developer B's approval still be trusted?

Not necessarily.

The reviewer should inspect the latest changes before the PR is merged.

### 11.1 Understand Stale Reviews

A stale approval is an approval that may no longer represent the latest version of the Pull Request.

For example:

Developer B approves the original implementation.

Developer A subsequently changes important application logic.

The original review may no longer be sufficient evidence that the updated implementation has been reviewed.

### 11.2 GitHub Review Protection Settings

GitHub supports repository rules and branch protection configurations that can control how approvals behave.

Examples include:

#### Dismiss stale pull request approvals when new commits are pushed

When enabled, previous approvals can be dismissed after new commits modify the PR.

#### Require approval of the most recent reviewable push

This requires an eligible approval after the latest reviewable changes are pushed.

#### Require a specific number of approving reviews

This establishes the minimum number of approvals required before merging.

These settings are not automatically enabled in every repository.

### 11.3 Practical Review Timeline

| Time | Event |
|---|---|
| 10:00 | PR opened |
| 10:30 | Developer B approves the changes. |
| 11:00 | Developer A pushes new implementation changes. |
| 11:05 | Developer B inspects the updated diff. |
| 11:20 | Developer B submits an updated approval. |

**Professional practice:** Always review the final diff before merging, regardless of whether an earlier approval remains technically valid.

### 11.4 Inspect Updated PR Changes

Open your PR.

Navigate to:

#### Files changed

Inspect:

- Newly added lines.
- Modified lines.
- Deleted lines.
- Changes introduced after the previous review.
- Any new files.

Also inspect the PR conversation to understand what changed after review.

## 12. Keep Pull Requests Healthy

Not every PR problem is a merge conflict.

Large, unfocused, outdated Pull Requests can also create problems.

### 12.1 Avoid Oversized Pull Requests

Bad example:

```text
PR: Update entire restaurant application

Changes:
- 150 files
- 12 unrelated features
- 30 bug fixes
- Database redesign
- Frontend redesign
```

Better approach:

```text
PR 1: Add product management API

PR 2: Add product management UI

PR 3: Add product validation tests

PR 4: Add product documentation
```

Separate work into manageable units when practical.

### 12.2 Keep Pull Requests Focused

A PR should ideally have one primary purpose.

For example:

```text
feat(products): add product search
```

Should not unexpectedly include:

- Authentication redesign.
- Docker restructuring.
- Payment changes.
- Unrelated documentation updates.

### 12.3 Keep PR Descriptions Updated

When implementation changes significantly, update the PR description.

Make sure it explains:

- What the final implementation does.
- What changed after review.
- Which tests were executed.
- Whether any limitations remain.
- Whether the original acceptance criteria were satisfied.

### 12.4 Understand Draft Versus Ready for Review

Use Draft PRs when work is incomplete.

Mark them ready for review when:

- Implementation is complete.
- Tests have been executed.
- The PR description is accurate.
- The changes are ready for independent review.

### 12.5 Keep Your Branch Clean

Before pushing:

```powershell
git status

git diff --check

git log --oneline -5
```

Avoid including:

- Temporary files.
- Generated artifacts.
- Local configuration.
- Unrelated changes.
- Debugging code.

### 12.6 Keep PR Discussions Organized

After addressing review comments:

1. Push the required changes.
2. Reply to the relevant review comments.
3. Resolve conversations when appropriate.
4. Request another review if necessary.
5. Confirm that the final changes satisfy the review requirements.

This connects the PR maintenance process with the review workflow from Lesson 29.

## 13. Git Commands Reference

These are the important commands from Lesson 30.

### 13.1 Branch Synchronization

| Command | Purpose |
|---|---|
| `git fetch origin` | Fetch remote updates without integrating them. |
| `git pull --ff-only origin main` | Fetch and integrate main only when fast-forward is possible. |
| `git merge origin/main` | Merge the latest fetched remote main. |
| `git rebase origin/main` | Rebase the current branch onto remote main. |

### 13.2 Conflict Resolution

| Command | Purpose |
|---|---|
| `git status` | Inspect the current repository state. |
| `git diff` | Inspect working-tree changes and conflicts. |
| `git diff --check` | Check whitespace problems. |
| `git add <file>` | Stage a resolved file. |
| `git merge --abort` | Abort an active merge. |
| `git rebase --continue` | Continue a paused rebase. |
| `git rebase --abort` | Abort an active rebase. |

### 13.3 History Inspection

| Command | Purpose |
|---|---|
| `git log --oneline` | Display compact commit history. |
| `git log --graph --oneline --all` | Visualize branch history. |
| `git branch -vv` | Display local branches and upstream tracking information. |
| `git show <commit>` | Inspect a particular commit. |
| `git diff main...feature` | Compare feature changes against the merge base with main. |

### 13.4 Remote Branch Updates

| Command | Purpose |
|---|---|
| `git push origin feature` | Push feature changes. |
| `git push --force-with-lease origin feature` | Update a remote branch after a coordinated history rewrite. |

**Important:** Understand the difference between `git fetch`, `git pull`, and `git merge`.

- Fetch downloads remote information.
- Pull fetches and integrates remote changes.
- Merge combines histories.

## 14. Practical Assignment — Two-Developer Merge Conflict Simulation

### Required Exercise

Now complete a more realistic exercise using two independent feature branches.

### Scenario

You're developing a restaurant order management feature.

Two developers independently modify the same documentation file.

**Developer A:** Changes the order lifecycle.

**Developer B:** Changes the order payment workflow.

Both changes must be integrated into `main`.

### Part A — Prepare the Repository

Start from updated main:

```powershell
git switch main

git pull --ff-only origin main
```

Confirm a clean working tree:

```powershell
git status
```

### Part B — Developer A Creates the Order Lifecycle Branch

```powershell
git switch -c feat/order-lifecycle
```

Modify:

```text
docs/github/module-03-pull-requests/conflict-practice.md
```

Change the default order status and add the lifecycle information.

Example:

```markdown
## Restaurant Order Status

The default order status is:

`pending`

## Order Lifecycle

1. Order is created.
2. Kitchen starts preparation.
3. Order becomes ready.
4. Order is completed.
```

Commit:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md

git commit -m "feat(orders): document order lifecycle"
```

Do not push yet.

### Part C — Developer B Creates the Payment Branch

Return to main:

```powershell
git switch main
```

Create:

```powershell
git switch -c feat/order-payment
```

Modify the same file.

Change the same default order status section to:

```markdown
## Restaurant Order Status

The default order status is:

`confirmed`
```

Add a payment section:

```markdown
## Payment Workflow

1. Order is created.
2. Cashier confirms payment.
3. Payment status becomes paid.
4. Order proceeds through preparation.
```

Commit:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md

git commit -m "feat(payments): document payment workflow"
```

### Part D — Integrate Developer B's Changes

Push Developer B's branch:

```powershell
git push -u origin feat/order-payment
```

Create a Pull Request:

```text
feat/order-payment → main
```

Review the changes and merge the PR.

### Part E — Integrate Developer A's Changes

Return to Developer A's branch:

```powershell
git switch feat/order-lifecycle
```

Fetch the latest remote changes:

```powershell
git fetch origin
```

Merge the updated main:

```powershell
git merge origin/main
```

Because both branches modified the same section, Git should report a conflict.

Inspect the affected file.

Resolve the conflict while preserving both developers' valid changes.

The final document should contain:

- Order lifecycle.
- Payment workflow.
- Valid order statuses.
- Clear responsibilities.
- No conflict markers.

### Part F — Complete Developer A's PR

Stage the resolved file:

```powershell
git add docs/github/module-03-pull-requests/conflict-practice.md
```

Complete the merge:

```powershell
git commit -m "merge: integrate order payment workflow"
```

Push:

```powershell
git push origin feat/order-lifecycle
```

Open the PR:

```text
feat/order-lifecycle → main
```

Review and merge it.

### Part G — Verify the Final Result

```powershell
git switch main

git pull --ff-only origin main

git log --oneline --graph --decorate --all

git status
```

Confirm:

- Both developers' changes exist.
- No conflict markers remain.
- Both PRs are merged.
- The working tree is clean.

## 15. Advanced Exercise — Compare Merge and Rebase

Use separate practice branches to compare the two approaches.

Do not reuse the same experiment branch for both operations.

### Exercise A — Merge Strategy

Start from updated main:

```powershell
git switch main

git pull --ff-only origin main

git switch -c experiment/merge-strategy
```

Create:

```text
docs/github/module-03-pull-requests/merge-experiment.md
```

Add:

```markdown
# Merge Strategy Experiment

This file is used to practise merging feature branches.

## Strategy

Merge main into the feature branch.
```

Commit:

```powershell
git add docs/github/module-03-pull-requests/merge-experiment.md

git commit -m "docs(github): add merge experiment"
```

Now make an independent change on main using another branch or collaborator.

After that change is merged:

```powershell
git fetch origin

git merge origin/main
```

Inspect:

```powershell
git log --graph --oneline --all
```

Record your observations.

### Exercise B — Rebase Strategy

Start from updated main:

```powershell
git switch main

git pull --ff-only origin main

git switch -c experiment/rebase-strategy
```

Create:

```text
docs/github/module-03-pull-requests/rebase-experiment.md
```

Add:

```markdown
# Rebase Strategy Experiment

This file is used to practise rebasing feature branches.

## Strategy

Rebase the feature branch onto the latest main.
```

Commit:

```powershell
git add docs/github/module-03-pull-requests/rebase-experiment.md

git commit -m "docs(github): add rebase experiment"
```

Now introduce another independent commit on main.

Fetch and rebase:

```powershell
git fetch origin

git rebase origin/main
```

Inspect:

```powershell
git log --graph --oneline --all
```

Record your observations.

### Compare Your Results

| Question | Merge | Rebase |
|---|---|---|
| Did you create a merge commit? | Record result | Record result |
| Were feature commits preserved with their original IDs? | Record result | Record result |
| Did commit IDs change? | Record result | Record result |
| Was conflict resolution necessary? | Record result | Record result |
| Which history was easier to understand? | Your conclusion | Your conclusion |

## 16. Repository Documentation

Now create the official Lesson 30 documentation.

Your repository structure should look like:

```text
docs/
└── github/
    └── module-03-pull-requests/
        ├── lesson-28-pr-fundamentals.md
        ├── lesson-29-advanced-reviews.md
        ├── lesson-30-merge-conflicts.md
        ├── conflict-practice.md
        ├── merge-experiment.md
        └── rebase-experiment.md
```

Create:

```text
lesson-30-merge-conflicts.md
```

Use this documentation structure:

```markdown
# Lesson 30 — Merge Conflicts and PR Management

## Learning Objectives

## 1. Understanding Merge Conflicts

## 2. Fast-Forward and Non-Fast-Forward Updates

## 3. Merge vs Rebase

## 4. Training Environment Setup

## 5. Creating Two Conflicting Branches

## 6. Resolving Conflicts Manually

## 7. Resolving Conflicts in VS Code

## 8. Aborting a Merge

## 9. Updating Feature Branches

## 10. GitHub Conflict Detection

## 11. Stale Reviews and Updated PRs

## 12. Keeping Pull Requests Healthy

## 13. Git Commands Reference

## 14. Practical Conflict Simulation

## 15. Merge vs Rebase Exercise

## 16. Lessons Learned

## 17. Assessment Checklist

## 18. References
```

**Documentation requirements:**

- Include explanations, not just command lists.
- Include actual Git command examples.
- Include branch diagrams.
- Include conflict-resolution examples.
- Include screenshots from your actual exercises where useful.
- Document any unexpected errors and their solutions.
- Do not include hypothetical screenshots as evidence of completed exercises.

## 17. Lessons Learned and Professional Practices

After completing the exercises, document your conclusions.

Your documentation should explain:

1. Why merge conflicts happen.
2. Why editing the same file doesn't always cause a conflict.
3. Why business requirements matter during conflict resolution.
4. When merge is preferable to rebase.
5. Why rewriting shared branch history requires coordination.
6. How VS Code simplifies conflict resolution.
7. How GitHub detects merge conflicts.
8. Why updated Pull Requests may require another review.
9. Why small, focused PRs are easier to maintain.
10. How to keep a feature branch synchronized with main.

### Professional Conflict-Resolution Checklist

Before completing a merge:

- [ ] Understand both versions.
- [ ] Confirm the intended behavior.
- [ ] Resolve every conflicting file.
- [ ] Remove all conflict markers.
- [ ] Run relevant tests.
- [ ] Check `git status`.
- [ ] Check `git diff --check`.
- [ ] Review the final changes.
- [ ] Confirm that the merge or rebase completed successfully.

## 18. Commit, Pull Request, Tag and Release

Follow your established training repository workflow.

### Step 1 — Create a Documentation Branch

```powershell
git switch main

git pull --ff-only origin main

git switch -c docs/lesson-30-merge-conflicts
```

### Step 2 — Add Documentation

```powershell
git add docs/github/module-03-pull-requests/
```

### Step 3 — Validate

```powershell
git status

git diff --check

git diff --cached
```

### Step 4 — Commit

```powershell
git commit -m "docs(github): add Lesson 30 merge conflict management"
```

### Step 5 — Push

```powershell
git push -u origin docs/lesson-30-merge-conflicts
```

### Step 6 — Create a Pull Request

**PR title:**

```text
docs(github): add Lesson 30 merge conflict management
```

**PR description:**

```markdown
## Summary

Add documentation covering advanced GitHub PR management and merge conflicts.

## Topics

- Merge conflict fundamentals
- Branch divergence
- Fast-forward and non-fast-forward updates
- Conflict markers
- Manual resolution
- VS Code Merge Editor
- Merge abort
- Merge vs rebase
- Feature branch synchronization
- GitHub conflict detection
- Stale reviews
- PR maintenance

## Practical exercises

- [ ] Two-branch conflict simulation
- [ ] VS Code conflict resolution
- [ ] GitHub conflict detection
- [ ] Merge experiment
- [ ] Rebase experiment

## Validation

- [ ] Markdown checked
- [ ] Commands tested
- [ ] Git history inspected
- [ ] Exercises completed
- [ ] Documentation reviewed
```

Review your PR and merge it into main.

### Step 7 — Create an Annotated Tag

Switch to updated main:

```powershell
git switch main

git pull --ff-only origin main

git fetch --tags
```

Create the annotated tag:

```powershell
git tag -a module-03-lesson-30 -m "Complete Module 3 Lesson 30"
```

Push:

```powershell
git push origin module-03-lesson-30
```

Verify:

```powershell
git tag --list
```

### Step 8 — Create the GitHub Release

Open your repository on GitHub.

Navigate to:

#### Releases → Draft a new release

Configure:

| Field | Value |
|---|---|
| Tag | `module-03-lesson-30` |
| Release title | Module 3 — Lesson 30: Merge Conflicts |
| Target | `main` |

**Release notes:**

```markdown
# Module 3 — Lesson 30

Completed Pull Request Management and Merge Conflicts.

## Topics

- Merge conflict fundamentals
- Branch divergence
- Fast-forward and non-fast-forward updates
- Conflict markers
- Manual conflict resolution
- VS Code Merge Editor
- Merge abort
- Merge vs rebase
- Feature branch synchronization
- GitHub conflict detection
- Stale reviews
- PR maintenance

## Practical exercises

- Two-branch conflict simulation
- VS Code conflict resolution
- GitHub conflict detection
- Merge experiment
- Rebase experiment

## Training checkpoint

module-03-lesson-30
```

Publish the release.

## 19. Lesson 30 Assessment

Track your progress.

**Completion checklist:**

- [ ] Created two branches from a common starting point.
- [ ] Modified the same file in both branches.
- [ ] Successfully reproduced a merge conflict.
- [ ] Understood Git conflict markers.
- [ ] Resolved a conflict manually.
- [ ] Resolved a conflict using VS Code.
- [ ] Used `git merge --abort`.
- [ ] Updated a feature branch from main.
- [ ] Practised merging main into a feature branch.
- [ ] Practised rebasing a feature branch.
- [ ] Understood `--force-with-lease`.
- [ ] Inspected Git history using `git log --graph`.
- [ ] Created and reviewed a PR involving conflict resolution.
- [ ] Understood stale approvals and updated reviews.
- [ ] Completed the two-developer simulation.
- [ ] Completed the merge versus rebase comparison.
- [ ] Published the Lesson 30 GitHub Release.

### Completion target: 17/17

## 20. Official Documentation and References

Bookmark these references for future use.

### Git Documentation

1. Git — [git merge](https://git-scm.com/docs/git-merge).
2. Git — [git rebase](https://git-scm.com/docs/git-rebase).
3. Git — [git merge-base](https://git-scm.com/docs/git-merge-base).
4. Git — [git status](https://git-scm.com/docs/git-status).
5. Git — [git diff](https://git-scm.com/docs/git-diff).

### GitHub Documentation

1. GitHub — [Addressing merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts).
2. GitHub — [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches).
3. GitHub — [About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews).

### VS Code Documentation

1. VS Code — [Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview).
2. VS Code — [Resolving merge conflicts](https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts).

---

## What's Next?

## Lesson 31 — Advanced Pull Request Automation & Governance

### Next Module Lesson

Lessons 28–30 established the manual Pull Request workflow:

- Lesson 28: Creating and managing Pull Requests.
- Lesson 29: Advanced Pull Request reviews.
- Lesson 30: Merge conflicts and PR maintenance.

Now we'll move beyond manually managing PRs and explore how professional teams automate and control their Pull Request workflows.

### Topics in Lesson 31

1. Advanced Pull Request templates.
2. Issue forms and PR integration.
3. CODEOWNERS in real projects.
4. Automatic reviewer assignment.
5. Branch protection rules.
6. Repository rulesets.
7. Required approvals and review policies.
8. Required status checks.
9. Auto-merge.
10. Merge queues.
11. Enforcing PR title conventions.
12. GitHub Actions integration with PRs.
13. Enforcing Conventional Commits.
14. Building a professional PR governance workflow.

**Our progression:** Lessons 28–30 established the manual Pull Request workflow. Lesson 31 will turn that workflow into a controlled, automated process suitable for professional development teams.

**Repository:** `github-deep-dive-training`

**Continue using:**

- Markdown lesson documentation.
- Conventional Commits.
- Feature branches.
- Pull Requests.
- Review workflows.
- Annotated Git tags.
- GitHub Releases.

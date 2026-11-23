# Module 1 — Code Tab
# Lesson 17: Git Reflog and Repository Recovery

**Filename:** `docs/github/module-01-code/lesson-17-git-reflog-recovery.md`

**Suggested branch:** `docs/add-git-reflog-lesson`

**Level:** Advanced

**Practice repository:** `github-deep-dive-training`

---

# 1. Learning objectives

By the end of this lesson, you should be able to:

- Understand Git references and HEAD.
- Understand how Git tracks reference movements.
- Use `git reflog` to inspect previous Git states.
- Recover commits after `git reset`.
- Recover deleted branches.
- Recover work after accidental rebases.
- Understand detached HEAD.
- Distinguish `git reset`, `git revert`, and `git restore`.
- Recover from incorrect merges.
- Understand Git object retention and garbage collection.
- Build safe recovery workflows.

# 2. Understanding Git references

Before learning recovery, you need to understand how Git identifies commits.

A commit has a unique identifier called a commit hash.

Example:

```bash
git log --oneline
```

Output:

```text
a91d4e2 feat: add authentication
b82c1a5 fix: correct login validation
c73d2b1 docs: update README
d64e9f0 Initial commit
```

Each commit points to its parent commit or parents.

Git uses references to identify important commits.

## 2.1 What is HEAD?

`HEAD` represents your current position in the repository.

Normally, HEAD points to the branch you currently have checked out.

Example:

```text
HEAD
 |
 v
main
 |
 v
a91d4e2
 |
 v
b82c1a5
 |
 v
c73d2b1
```

Inspect HEAD:

```bash
git status
```

```bash
git log -1
```

Inspect the HEAD reference:

```bash
git symbolic-ref HEAD
```

Expected:

```text
refs/heads/main
```

Get the current commit:

```bash
git rev-parse HEAD
```

## 2.2 What is a branch?

A branch is a movable reference pointing to a commit.

Example:

```text
          feature
             |
             v
           C3
          /
C1 ---- C2
          \
           main
```

When you create another commit on `feature`, the branch reference moves forward.

Branches are not complete copies of your repository. They are lightweight references.

## 2.3 What happens when you switch branches?

```bash
git switch main
```

Git updates HEAD to point to `main`.

```bash
git switch feature
```

HEAD now points to `feature`.

Git records these movements in the reflog.

# 3. What is Git Reflog?

`git reflog` records changes to local Git references.

It is particularly useful when you accidentally:

- Reset a branch.
- Delete a branch.
- Move HEAD to another commit.
- Rebase incorrectly.
- Lose track of a previous commit.
- Change branches and forget where you were.

The reflog records reference movements, not a complete history of every file modification.

Basic command:

```bash
git reflog
```

Example output:

```text
a91d4e2 HEAD@{0}: commit: feat: add authentication
b82c1a5 HEAD@{1}: reset: moving to HEAD~1
c73d2b1 HEAD@{2}: commit: feat: add login page
d64e9f0 HEAD@{3}: checkout: moving from feature to main
```

Interpretation:

| Entry | Meaning |
|---|---|
| HEAD@{0} | Most recent HEAD movement |
| HEAD@{1} | Previous HEAD movement |
| HEAD@{2} | Two movements ago |
| HEAD@{3} | Three movements ago |

Important: Reflog entries are local and expire according to Git's reflog expiration settings. They are not automatically shared with other developers.

## 3.1 Useful reflog commands

Show HEAD history:

```bash
git reflog
```

Show a specific branch's reflog:

```bash
git reflog show main
```

Show all references:

```bash
git reflog show --all
```

Show a more detailed log:

```bash
git reflog --date=iso
```

Show recent entries:

```bash
git reflog -n 10
```

Inspect a previous commit:

```bash
git show HEAD@{2}
```

Inspect the reflog configuration:

```bash
git config --get gc.reflogExpire
```

# 4. Understanding git reset

`git reset` moves the current branch reference to another commit.

It has three main modes:

- `--soft`
- `--mixed`
- `--hard`

Understanding their differences is essential for recovery.

## 4.1 Soft reset

```bash
git reset --soft HEAD~1
```

What happens?

- HEAD moves backward one commit.
- The branch reference moves backward.
- Changes from the removed commit remain staged.
- Your working files remain unchanged.

Example:

Before:

```text
A -- B -- C
          ^
         HEAD
```

After:

```text
A -- B
     ^
    HEAD

Changes from C remain staged.
```

Use cases:

- Combining commits.
- Rewriting a recent commit.
- Changing a commit message.

## 4.2 Mixed reset

```bash
git reset --mixed HEAD~1
```

This is the default reset mode.

What happens?

- HEAD moves backward.
- The staging area is updated.
- Changes from the removed commit remain in the working directory.
- Changes become unstaged.

## 4.3 Hard reset

```bash
git reset --hard HEAD~1
```

What happens?

- HEAD moves backward.
- The staging area changes.
- Tracked working-tree files are updated to match the target commit.
- Uncommitted changes to tracked files can be discarded.

**Warning:** This operation can destroy uncommitted work. Do not experiment with it in a real project.

Before using it, consider creating a backup branch or patch.

## 4.4 Comparison

| Operation | HEAD | Staging area | Working directory |
|---|---|---|---|
| `--soft` | Moves | Keeps changes staged | Keeps changes |
| `--mixed` | Moves | Resets | Keeps changes unstaged |
| `--hard` | Moves | Resets | Resets tracked files |

# 5. Exercise environment: Create a disposable recovery repository

Do not perform destructive recovery exercises directly on your main training branch.

Create a separate local repository.

```bash
mkdir git-recovery-lab
cd git-recovery-lab
git init
```

Configure Git identity if necessary:

```bash
git config user.name "Training Developer"
git config user.email "training@example.com"
```

Create the first commit:

```bash
echo "Initial project" > README.md
git add README.md
git commit -m "docs: initialize recovery lab"
```

Create a second commit:

```bash
echo "Authentication module" > auth.txt
git add auth.txt
git commit -m "feat(auth): add authentication module"
```

Create a third commit:

```bash
echo "Order management module" > orders.txt
git add orders.txt
git commit -m "feat(orders): add order management"
```

Inspect:

```bash
git log --oneline
```

You should have three commits.

# 6. Recovery scenario 1 — Recover after accidental hard reset

Imagine you accidentally execute:

```bash
git reset --hard HEAD~2
```

Your latest two commits are no longer referenced by the current branch.

First inspect:

```bash
git log --oneline
```

You may only see the initial commit.

Do not panic.

Run:

```bash
git reflog
```

Example:

```text
abc1234 HEAD@{0}: reset: moving to HEAD~2
def5678 HEAD@{1}: commit: feat(orders): add order management
ghi9012 HEAD@{2}: commit: feat(auth): add authentication module
```

You can recover the previous branch position.

Option A — Move the current branch back:

```bash
git reset --hard def5678
```

Option B — Create a recovery branch:

```bash
git branch recovery/orders def5678
```

Then inspect:

```bash
git switch recovery/orders
git log --oneline
```

**Professional recommendation:** Prefer creating a recovery branch first when you are unsure which commit contains the desired work.

# 7. Recovery scenario 2 — Recover a deleted branch

Imagine you created:

```bash
git switch -c feature/payment
```

Then committed changes:

```bash
echo "Payment module" > payment.txt
git add payment.txt
git commit -m "feat(payment): add payment module"
```

Return to main:

```bash
git switch main
```

Accidentally delete the branch:

```bash
git branch -D feature/payment
```

The branch name disappears.

But the commit may still be recoverable.

Inspect:

```bash
git reflog --all
```

Find the commit containing the payment module.

Then recreate the branch:

```bash
git branch feature/payment <COMMIT_HASH>
```

Switch to it:

```bash
git switch feature/payment
```

Verify:

```bash
git log --oneline
```

You have recovered the branch reference.

Important: A deleted branch is not the same as immediately deleted commit objects. Recovery is possible while the relevant commit remains available.

# 8. Recovery scenario 3 — Recover from an accidental rebase

Imagine you have:

```text
main:    A -- B -- C
feature: A -- B -- D -- E
```

You start a rebase:

```bash
git switch feature
git rebase main
```

You encounter conflicts and accidentally finish the rebase with an incorrect result.

Inspect:

```bash
git reflog
```

Look for entries similar to:

```text
HEAD@{0}: rebase (finish)
HEAD@{1}: rebase (pick)
HEAD@{2}: rebase (start)
HEAD@{3}: checkout: moving from main to feature
```

Identify the reference before the rebase started.

Create a recovery branch before changing anything:

```bash
git branch recovery/before-rebase <OLD_COMMIT_HASH>
```

Inspect:

```bash
git log --oneline recovery/before-rebase
```

If the original feature history is correct, you can restore the branch after verifying the result.

For example:

```bash
git switch feature
git reset --hard recovery/before-rebase
```

This resets the local feature branch. Do not do this blindly if the branch has already been pushed or other developers have based work on it.

# 9. Recovery scenario 4 — Detached HEAD

Detached HEAD means HEAD points directly to a commit instead of pointing to a branch.

Example:

```bash
git checkout <COMMIT_HASH>
```

Or:

```bash
git switch --detach <COMMIT_HASH>
```

You can inspect and test the historical commit.

However, if you create commits while detached, those commits are not automatically attached to a named branch.

Create a branch immediately if you want to preserve new work:

```bash
git switch -c recovery/detached-work
```

This creates a branch at your current commit.

Inspect:

```bash
git status
git branch
git log --oneline
```

Important: Detached HEAD is not an error. It is a valid Git state.

# 10. Recovery scenario 5 — Incorrect merge

Imagine you merge the wrong branch:

```bash
git merge feature/payment
```

There are two possible situations.

## Situation A: Merge is not committed yet

If Git reports conflicts:

```bash
git status
```

You can abort the merge:

```bash
git merge --abort
```

This attempts to restore the pre-merge state.

## Situation B: Merge commit already exists

Inspect:

```bash
git log --oneline --graph --all
```

If the merge is already committed and has not been pushed, you may restore the previous branch position using a carefully selected reset.

For example:

```bash
git reset --hard ORIG_HEAD
```

Inspect `ORIG_HEAD` first:

```bash
git show ORIG_HEAD
```

If the merge has already been pushed to a shared branch, prefer a revert:

```bash
git revert -m 1 <MERGE_COMMIT_HASH>
```

The `-m 1` option selects the first parent as the mainline parent.

Verify the merge's parent ordering before using this command.

# 11. git reset vs git revert vs git restore

These commands solve different problems.

## 11.1 git reset

Moves the current branch reference.

```bash
git reset --soft HEAD~1
```

Use when you need to change local commit history.

## 11.2 git revert

Creates a new commit that reverses the changes introduced by an earlier commit.

```bash
git revert <COMMIT_HASH>
```

Use when you need to undo changes without rewriting shared history.

Example:

```text
A -- B -- C -- D
               ^
             HEAD

Revert C:

A -- B -- C -- D -- E
                    ^
                   HEAD
```

E reverses the changes introduced by C.

The original commits remain in history.

## 11.3 git restore

Restores file contents.

Restore a working-tree file:

```bash
git restore README.md
```

Unstage a file:

```bash
git restore --staged README.md
```

Restore a file from a specific commit:

```bash
git restore --source=<COMMIT_HASH> -- README.md
```

Be careful: restoring a file can discard local changes to that file.

## 11.4 Comparison

| Command | Main purpose | Rewrites existing history? |
|---|---|---|
| `git reset` | Move branch reference | Yes, depending on use |
| `git revert` | Create an undo commit | No |
| `git restore` | Restore file contents | No commit history change |

# 12. Understanding ORIG_HEAD

Git sometimes stores the previous position of HEAD in `ORIG_HEAD`.

This can be useful after:

- Merge operations.
- Reset operations.
- Rebase operations.
- Other operations that move HEAD.

Inspect it:

```bash
git show ORIG_HEAD
```

Recovering to it:

```bash
git reset --hard ORIG_HEAD
```

Only do this after checking that ORIG_HEAD represents the state you want.

It is not a permanent backup. Later Git operations may replace its value.

# 13. Git object storage and garbage collection

Git stores repository content as objects.

Important object types:

| Object | Purpose |
|---|---|
| Blob | File content |
| Tree | Directory structure |
| Commit | Snapshot metadata and parent relationships |
| Tag | Annotated tag metadata |

Inspect objects:

```bash
git cat-file -t <OBJECT_HASH>
```

Inspect an object:

```bash
git cat-file -p <OBJECT_HASH>
```

Git also performs garbage collection.

```bash
git gc
```

Garbage collection can prune unreachable objects after their retention period.

This is why recovery is not guaranteed indefinitely.

Do not run aggressive pruning commands while attempting recovery.

For example:

```bash
git gc --prune=now
```

can remove unreachable objects immediately.

Avoid this during recovery exercises.

# 14. Useful recovery commands

```bash
git reflog
git reflog show --all
git reflog --date=iso
git log --oneline --graph --all
git show <COMMIT_HASH>
git branch -a
git branch recovery/backup <COMMIT_HASH>
git switch recovery/backup
git reset --soft HEAD~1
git reset --mixed HEAD~1
git revert <COMMIT_HASH>
git restore <FILE>
git show ORIG_HEAD
git fsck --full --no-reflogs --unreachable
```

`git fsck` can help locate unreachable objects when reflog entries are unavailable.

Do not immediately reset or delete anything you discover. Inspect candidate commits first.

# 15. Recovery best practices

Before a potentially destructive operation:

1. Inspect your working tree.
2. Check staged and unstaged changes.
3. Create a backup branch when appropriate.
4. Record important commit hashes.
5. Understand whether the branch is shared.
6. Avoid rewriting shared history without coordination.

Useful commands:

```bash
git status
git log --oneline --graph --all
git branch -vv
git reflog
git diff
git diff --cached
```

For valuable uncommitted work, consider:

```bash
git stash push -u -m "backup before recovery operation"
```

Or create a patch:

```bash
git diff > working-changes.patch
git diff --cached > staged-changes.patch
```

Remember that ordinary `git diff` does not capture untracked files.

# 16. Practical exercises

Complete these exercises in your disposable `git-recovery-lab` repository.

## Exercise 1 — Recover from reset

1. Create three commits.
2. Run `git reset --hard HEAD~2`.
3. Inspect `git log`.
4. Inspect `git reflog`.
5. Identify the lost commit.
6. Create a recovery branch.
7. Verify the recovered files.

Expected result: Your previous work is available on the recovery branch.

## Exercise 2 — Recover a deleted branch

1. Create `feature/payment`.
2. Add a file.
3. Commit it.
4. Switch to main.
5. Delete the feature branch.
6. Find its commit in reflog.
7. Recreate the branch.
8. Verify the commit.

Expected result: The branch is recreated at its previous commit.

## Exercise 3 — Recover after rebase

1. Create a main branch with two commits.
2. Create a feature branch.
3. Add two commits to the feature branch.
4. Rebase the feature branch.
5. Inspect the reflog.
6. Identify the original feature position.
7. Create a recovery branch.
8. Compare both histories.

Expected result: You can inspect both the original and rebased histories.

## Exercise 4 — Detached HEAD

1. Checkout an earlier commit.
2. Confirm detached HEAD.
3. Create a new commit.
4. Create a branch at that commit.
5. Switch to the new branch.
6. Verify the commit is preserved.

Expected result: The new commit belongs to a named branch.

## Exercise 5 — Revert a shared commit

1. Create a feature commit.
2. Merge it into a test branch.
3. Push the test branch if you have a remote configured.
4. Revert the feature commit.
5. Inspect the resulting history.

Expected result: The original commit remains in history and a new commit reverses its changes.

## Exercise 6 — Recovery investigation

Simulate a recovery incident:

A developer reports that they accidentally deleted a feature branch after several commits. They cannot remember the branch name or exact commit hash.

Your task:

1. Inspect all available reflogs.
2. Inspect all branches.
3. Search for relevant commit messages.
4. Identify the candidate commit.
5. Inspect the candidate commit's contents.
6. Create a recovery branch.
7. Verify the recovered files.
8. Document the recovery steps.

Expected result: Produce a short incident report explaining how the branch was recovered.

# 17. GitHub repository practice

Return to your training repository.

Create the lesson branch:

```bash
git switch main
git pull origin main
git switch -c docs/add-git-reflog-lesson
```

Create:

```text
docs/github/module-01-code/lesson-17-git-reflog-recovery.md
```

Paste this lesson into the file.

Also create:

```text
docs/github/module-01-code/recovery-runbook.md
```

The recovery runbook should contain:

- Incident description.
- Initial repository state.
- Recovery objective.
- Commands used.
- Identified commit hashes.
- Recovery branch name.
- Verification steps.
- Final result.
- Lessons learned.

## Suggested recovery runbook template

```markdown
# Git Recovery Runbook

## Incident

Describe what happened.

## Initial state

Describe the current branch, HEAD, and working-tree status.

## Investigation

Commands used:

- git status
- git reflog
- git log --oneline --graph --all

## Recovery

Describe the recovery procedure.

## Verification

Explain how you confirmed that the files and commits were recovered.

## Result

Document the final state.

## Lessons learned

What should the developer do differently next time?
```

# 18. Commit and push

Check:

```bash
git status
git diff --check
```

Stage:

```bash
git add docs/github/module-01-code/lesson-17-git-reflog-recovery.md
git add docs/github/module-01-code/recovery-runbook.md
```

Commit:

```bash
git commit -m "docs(github): add git reflog and recovery lesson"
```

Push:

```bash
git push -u origin docs/add-git-reflog-lesson
```

Create a pull request:

**Title:**

```text
docs(github): add git reflog and repository recovery lesson
```

After review and merge, create an annotated tag:

```bash
git switch main
git pull origin main
git tag -a module-01-lesson-17 -m "Module 1 Lesson 17: Git Reflog and Recovery"
git push origin module-01-lesson-17
```

Check first that the tag does not already exist.

# 19. GitHub Release

Create a release using:

**Tag:** `module-01-lesson-17`

**Release title:**

```text
Module 1 — Lesson 17: Git Reflog and Repository Recovery
```

Suggested release notes:

```markdown
# Module 1 — Lesson 17

## Topics

- Git references and HEAD
- Git reflog
- Soft, mixed, and hard reset
- Deleted branch recovery
- Rebase recovery
- Detached HEAD
- Incorrect merge recovery
- Reset vs revert vs restore
- ORIG_HEAD
- Git object storage
- Garbage collection
- Recovery best practices

## Practical exercises

- Recover commits after reset
- Recover deleted branches
- Recover after rebase
- Recover detached HEAD commits
- Revert shared commits
- Investigate a recovery incident

## Documentation

- lesson-17-git-reflog-recovery.md
- recovery-runbook.md
```

# 20. Completion checklist

- [ ] Understand HEAD and Git references.
- [ ] Understand branch references.
- [ ] Understand git reflog.
- [ ] Recover a commit after reset.
- [ ] Recover a deleted branch.
- [ ] Recover from an incorrect rebase.
- [ ] Understand detached HEAD.
- [ ] Recover an incorrect merge.
- [ ] Understand reset, revert, and restore.
- [ ] Understand ORIG_HEAD.
- [ ] Understand Git objects and garbage collection.
- [ ] Complete the six practical exercises.
- [ ] Create the recovery runbook.
- [ ] Create a pull request.
- [ ] Merge the lesson.
- [ ] Create the annotated tag.
- [ ] Publish the GitHub Release.

# 21. Official documentation

- Git Reflog: https://git-scm.com/docs/git-reflog
- Git Reset: https://git-scm.com/docs/git-reset
- Git Revert: https://git-scm.com/docs/git-revert
- Git Restore: https://git-scm.com/docs/git-restore
- Git Branch: https://git-scm.com/docs/git-branch
- Git Fsck: https://git-scm.com/docs/git-fsck
- Git Garbage Collection: https://git-scm.com/docs/git-gc
- Git Checkout: https://git-scm.com/docs/git-checkout

---

# 22. Next lesson

**Module 1 — Lesson 18: Git Internals — Objects, Trees, Blobs, Commits and Packfiles**

Planned topics:

- How Git stores files internally.
- Blob objects.
- Tree objects.
- Commit objects.
- Tag objects.
- Object hashes.
- The Git object database.
- Loose objects.
- Packfiles and delta compression.
- The index and staging area internals.
- Inspecting objects using `git cat-file`.
- Exploring `.git/objects`.
- Understanding Git storage efficiency.

The objective is to understand what happens internally when you execute Git commands, rather than treating Git as a collection of commands to memorize.
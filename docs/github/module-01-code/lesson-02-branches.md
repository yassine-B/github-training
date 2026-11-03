# Lesson 2 — Git Branches

## 1. Learning objectives

By the end of this lesson, you should understand:

- What a branch represents.
- Why branches are important.
- The difference between local and remote branches.
- How to create, switch, rename, and delete branches.
- How to publish a branch to GitHub.
- How to inspect available branches.
- How to follow a feature-branch workflow.

## 2. What is a Git branch?

A branch is a movable reference to a commit.

It allows developers to work on changes independently without immediately modifying the main development branch.

For example:

```text
main
  |
  A
  |
  B
  |
  C

feature/login
  |
  D
  |
  E
```

The feature branch can contain new work while `main` remains unchanged.

Branches are useful for:

- New features.
- Bug fixes.
- Documentation.
- Refactoring.
- Experiments.

## 3. Understand the main branch

The `main` branch is commonly the primary branch of a repository.

It should contain stable, reviewed code.

You should generally avoid developing every feature directly on `main`.

Instead:

1. Start from an updated `main`.
2. Create a separate branch.
3. Implement the change.
4. Test the change.
5. Open a pull request.
6. Review and merge it.

## 4. Inspect branches

List local branches:

```bash
git branch
```

The current branch is marked with `*`.

List remote-tracking branches:

```bash
git branch -r
```

List all branches:

```bash
git branch -a
```

Show only the current branch:

```bash
git branch --show-current
```

## 5. Create a branch

Create a branch without switching to it:

```bash
git branch feature/add-login
```

Create and immediately switch to a branch:

```bash
git switch -c feature/add-login
```

The second command is generally the preferred modern workflow.

## 6. Switch branches

```bash
git switch main
```

Switch to another existing branch:

```bash
git switch feature/add-login
```

Before switching, check whether you have uncommitted changes:

```bash
git status
```

Git may prevent a switch if local changes would be overwritten.

## 7. Branch naming conventions

Use descriptive names that communicate the purpose of the branch.

Recommended prefixes:

| Prefix | Purpose | Example |
|---|---|---|
| `feature/` | New functionality | `feature/user-authentication` |
| `fix/` | Bug fixes | `fix/login-validation` |
| `docs/` | Documentation | `docs/api-guide` |
| `refactor/` | Code restructuring | `refactor/auth-services` |
| `test/` | Tests | `test/user-api` |
| `chore/` | Maintenance | `chore/update-dependencies` |
| `hotfix/` | Urgent production fixes | `hotfix/payment-error` |

Use lowercase names and hyphens between words.

Avoid names such as:

```text
branch1
new-branch
test123
my-work
```

Prefer:

```text
feature/order-management
fix/incorrect-order-total
docs/deployment-guide
```

## 8. Rename a branch

Rename the current branch:

```bash
git branch -m new-name
```

Rename a different local branch:

```bash
git branch -m old-name new-name
```

If the old branch was already published, you may also need to update its remote branch.

For example:

```bash
git push origin --delete old-name
git push -u origin new-name
```

Be careful when deleting a remote branch shared with other developers.

## 9. Publish a branch to GitHub

Create a branch:

```bash
git switch -c feature/add-login
```

Make a change and commit it:

```bash
git add .
git commit -m "feat(auth): add login page"
```

Publish the branch:

```bash
git push -u origin feature/add-login
```

After the upstream is configured, use:

```bash
git push
```

## 10. Understand local and remote branches

A local branch exists in your local repository.

A remote-tracking branch represents the state of a branch on a remote repository as last observed by Git.

Example:

```text
main
feature/add-login

origin/main
origin/feature/add-login
```

`origin` is the conventional name of the default remote.

Inspect remote URLs:

```bash
git remote -v
```

Download information about remote branches:

```bash
git fetch origin
```

`git fetch` updates remote-tracking references without merging the changes into your current branch.

## 11. Delete branches

Delete a local branch that has been merged:

```bash
git branch -d feature/add-login
```

Force-delete a local branch:

```bash
git branch -D feature/add-login
```

The uppercase `-D` can delete a branch even if Git considers its changes unmerged. Use it carefully.

Delete a remote branch:

```bash
git push origin --delete feature/add-login
```

Deleting a local branch does not automatically delete its remote counterpart.

## 12. A practical feature-branch workflow

Start from `main`:

```bash
git switch main
git pull --ff-only origin main
```

Create a feature branch:

```bash
git switch -c feature/add-user-guide
```

Create or edit a file.

Inspect changes:

```bash
git status
git diff
```

Stage and commit:

```bash
git add .
git commit -m "docs: add user guide"
```

Push:

```bash
git push -u origin feature/add-user-guide
```

You can now create a pull request on GitHub.

## 13. Important commands reference

| Command | Purpose |
|---|---|
| `git branch` | List local branches |
| `git branch -r` | List remote-tracking branches |
| `git branch -a` | List all branches |
| `git branch --show-current` | Show current branch |
| `git branch NAME` | Create a branch |
| `git switch NAME` | Switch branches |
| `git switch -c NAME` | Create and switch |
| `git branch -m NAME` | Rename current branch |
| `git branch -d NAME` | Delete merged local branch |
| `git branch -D NAME` | Force-delete local branch |
| `git fetch origin` | Fetch remote updates |
| `git push -u origin NAME` | Publish and track a branch |
| `git push origin --delete NAME` | Delete remote branch |

## 14. Practical exercise

Create a documentation branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c docs/add-branching-guide
```

Create:

```text
docs/branching-guide.md
```

Write a short guide explaining:

- What a branch is.
- Why branches are useful.
- How to create a branch.
- How to switch branches.
- How to delete branches.

Commit:

```bash
git add docs/branching-guide.md
git commit -m "docs(git): add branching guide"
```

Push:

```bash
git push -u origin docs/add-branching-guide
```

Open GitHub and create a pull request to merge the documentation into `main`.

After the pull request is merged, synchronize your local repository:

```bash
git switch main
git pull --ff-only origin main
```

Delete the local branch:

```bash
git branch -d docs/add-branching-guide
```

If GitHub has not automatically deleted the remote branch, delete it:

```bash
git push origin --delete docs/add-branching-guide
```

## 15. Completion checklist

- [ ] Understand what branches are.
- [ ] List local branches.
- [ ] List remote branches.
- [ ] Create a branch.
- [ ] Switch branches.
- [ ] Rename a branch.
- [ ] Publish a branch.
- [ ] Delete a local branch.
- [ ] Delete a remote branch.
- [ ] Complete a feature-branch workflow.

## 16. What comes next?

Lesson 3 covers commits, commit messages, Conventional Commits, commit history, inspecting previous changes, and safely correcting commits.
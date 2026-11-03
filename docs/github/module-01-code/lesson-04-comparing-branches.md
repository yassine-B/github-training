# Lesson 4 — Comparing Branches

## 1. Learning objectives

By the end of this lesson, you should understand:

- How to compare two local branches.
- How to compare commits.
- The difference between two-dot and three-dot comparisons.
- How to inspect files changed between branches.
- How to identify commits ahead or behind.
- How to use GitHub Compare.
- How branch comparisons support pull request reviews.

## 2. Why compare branches?

Before merging a branch, developers need to understand exactly what changed.

Branch comparisons help answer:

- Which files were modified?
- What lines were added?
- What lines were removed?
- Which commits exist on one branch but not the other?
- Is the feature branch ahead of `main`?
- Does the branch contain unexpected changes?

This is an important step before creating or reviewing a pull request.

## 3. Update remote information

Before comparing local branches with GitHub, fetch the latest remote information:

```bash
git fetch origin
```

This updates remote-tracking branches without automatically merging them into your current branch.

List branches:

```bash
git branch -a
```

## 4. Compare two local branches

Compare the tips of two branches:

```bash
git diff main..feature/add-git-fundamentals
```

This displays the difference between the two specified branch tips.

Show only changed filenames:

```bash
git diff --name-only main..feature/add-git-fundamentals
```

Show filenames and change status:

```bash
git diff --name-status main..feature/add-git-fundamentals
```

Show a summary:

```bash
git diff --stat main..feature/add-git-fundamentals
```

Inspect one file:

```bash
git diff main..feature/add-git-fundamentals -- docs/git-fundamentals.md
```

## 5. Understand two-dot and three-dot comparisons

### Two-dot comparison

```bash
git diff main..feature/add-git-fundamentals
```

This compares the two endpoint trees. It is equivalent to comparing the tree at `main` with the tree at the feature branch.

### Three-dot comparison

```bash
git diff main...feature/add-git-fundamentals
```

This compares the merge base of the two branches with the feature branch.

The merge base is their best common ancestor commit.

Three-dot comparison is useful when you want to inspect what the feature branch has introduced since it diverged from `main`.

This is particularly useful for understanding the changes a pull request proposes.

## 6. Compare commits

Compare two commit snapshots:

```bash
git diff COMMIT_A COMMIT_B
```

Compare the previous commit with the current commit:

```bash
git diff HEAD~1 HEAD
```

Show only the changed filenames:

```bash
git diff --name-only HEAD~1 HEAD
```

Show a summary:

```bash
git diff --stat HEAD~1 HEAD
```

Inspect the changes introduced by a specific commit:

```bash
git show COMMIT_HASH
```

## 7. Understand ahead and behind commits

You can determine how many commits each branch has that the other does not.

```bash
git rev-list --left-right --count main...feature/add-git-fundamentals
```

Example output:

```text
2  3
```

Interpretation:

- First number: commits reachable from `main` but not from the feature branch.
- Second number: commits reachable from the feature branch but not from `main`.

Therefore:

- `main` has 2 unique commits.
- The feature branch has 3 unique commits.

## 8. Inspect commits unique to a branch

Show commits in the feature branch that are not in `main`:

```bash
git log --oneline main..feature/add-git-fundamentals
```

Show commits in `main` that are not in the feature branch:

```bash
git log --oneline feature/add-git-fundamentals..main
```

These commands help explain why a branch is ahead or behind.

## 9. Compare branches on GitHub

GitHub provides a visual comparison interface.

Open your repository and navigate to the Compare page.

You can also use:

```text
https://github.com/USERNAME/REPOSITORY/compare
```

Select:

- Base: the branch you want to merge into.
- Compare: the branch containing your changes.

For example:

```text
Base: main
Compare: feature/add-git-fundamentals
```

GitHub displays:

### Commits

The commits included in the comparison.

### Files changed

The files modified between the branches.

### Diff view

Green lines generally represent additions.

Red lines generally represent removals.

You can inspect the changes before creating a pull request.

## 10. Practical exercise

Create a documentation branch from updated `main`:

```bash
git switch main
git pull --ff-only origin main
git switch -c docs/add-github-comparison-guide
```

Create:

```text
docs/github-comparison-guide.md
```

Add sections explaining:

- Why branch comparison is useful.
- How to compare branches using `git diff`.
- The difference between two-dot and three-dot comparisons.
- How to inspect changed filenames.
- How to compare commits.
- How to use GitHub Compare.

Commit:

```bash
git add docs/github-comparison-guide.md
git commit -m "docs(github): add comparison guide"
```

Push:

```bash
git push -u origin docs/add-github-comparison-guide
```

## 11. Compare locally

Fetch the latest remote references:

```bash
git fetch origin
```

Compare `main` with the new documentation branch:

```bash
git diff main...docs/add-github-comparison-guide
```

List changed files:

```bash
git diff --name-status main...docs/add-github-comparison-guide
```

Inspect the commit difference:

```bash
git log --oneline main..docs/add-github-comparison-guide
```

Inspect ahead/behind counts:

```bash
git rev-list --left-right --count main...docs/add-github-comparison-guide
```

## 12. Compare on GitHub

Open:

```text
https://github.com/USERNAME/github-deep-dive-training/compare
```

Select:

```text
Base: main
Compare: docs/add-github-comparison-guide
```

Review:

- Commit list.
- Changed files.
- Added lines.
- Removed lines.
- Unexpected modifications.

Do not merge until you understand the changes.

## 13. Important commands reference

| Command | Purpose |
|---|---|
| `git fetch origin` | Update remote-tracking references |
| `git branch -a` | List local and remote-tracking branches |
| `git diff A..B` | Compare two branch tips |
| `git diff A...B` | Compare merge base with branch B |
| `git diff --name-only A..B` | List changed filenames |
| `git diff --name-status A..B` | List filenames and change status |
| `git diff --stat A..B` | Show change statistics |
| `git diff A B` | Compare two commits |
| `git show HASH` | Inspect a commit |
| `git log --oneline A..B` | Show commits in B not in A |
| `git rev-list --left-right --count A...B` | Count unique commits on each side |

## 14. Completion checklist

- [ ] Fetch remote information.
- [ ] Compare two local branches.
- [ ] Use two-dot comparison.
- [ ] Use three-dot comparison.
- [ ] List changed filenames.
- [ ] Inspect branch differences.
- [ ] Compare two commits.
- [ ] Inspect commits unique to a branch.
- [ ] Understand ahead and behind counts.
- [ ] Use GitHub Compare.
- [ ] Review the feature branch before merging.

## 15. What comes next?

Lesson 5 covers Git tags, semantic versioning, and GitHub Releases.

You will learn how to identify important project versions, create annotated tags, push tags, and publish releases on GitHub.
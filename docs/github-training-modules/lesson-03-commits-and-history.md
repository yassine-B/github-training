# Lesson 3 — Commits, History, and Conventional Commits

## 1. Learning objectives

By the end of this lesson, you should understand:

- What a commit is.
- How Git creates commits.
- The difference between staged and unstaged changes.
- How to write meaningful commit messages.
- How to apply Conventional Commits.
- How to inspect commit history.
- How to inspect a specific commit.
- How to amend or revert commits.
- The difference between `reset` and `revert`.

## 2. What is a commit?

A commit is a recorded snapshot of your repository.

It represents a set of changes at a particular point in time.

A commit contains:

- Commit hash.
- Author.
- Author date.
- Commit message.
- Parent commit references.
- Snapshot information.

A commit does not simply store a copy of every file each time. Git uses an object database and content-addressed objects to represent repository history efficiently.

## 3. Understand the Git workflow

```text
Working Directory
       |
       | git add
       v
Staging Area
       |
       | git commit
       v
Local Repository
       |
       | git push
       v
Remote Repository
```

### Working directory

The files you currently edit.

### Staging area

The changes selected for the next commit.

### Local repository

The commits stored on your computer.

### Remote repository

The repository hosted on GitHub or another Git server.

## 4. Inspect changes before committing

Check repository status:

```bash
git status
```

Display unstaged changes:

```bash
git diff
```

Display staged changes:

```bash
git diff --cached
```

Display a summary of staged changes:

```bash
git diff --cached --stat
```

Inspect a particular file:

```bash
git diff -- docs/README.md
```

These commands help prevent accidentally committing unrelated changes.

## 5. Stage changes

Stage a single file:

```bash
git add docs/README.md
```

Stage a directory:

```bash
git add docs/
```

Stage all changes:

```bash
git add .
```

Stage only tracked-file modifications and deletions:

```bash
git add -u
```

Stage interactively:

```bash
git add -p
```

Interactive staging allows you to select individual change sections rather than staging an entire file.

## 6. Create commits

Create a commit:

```bash
git commit -m "docs: add installation guide"
```

Open the configured text editor to write a longer commit message:

```bash
git commit
```

A useful commit should represent one logical change.

Avoid combining unrelated work into one commit.

## 7. Conventional Commits

Conventional Commits is a convention for structuring commit messages.

General format:

```text
<type>[optional scope][optional !]: <description>

[optional body]

[optional footer(s)]
```

Examples:

```text
feat(auth): add refresh token support
fix(orders): correct total calculation
docs(api): document authentication endpoints
refactor(users): move validation into services
test(orders): add checkout tests
chore(deps): update dependencies
```

### Common commit types

| Type | Purpose |
|---|---|
| `feat` | Introduces a feature |
| `fix` | Fixes a bug |
| `docs` | Documentation changes |
| `style` | Formatting changes without changing logic |
| `refactor` | Code restructuring |
| `test` | Adds or modifies tests |
| `perf` | Performance improvement |
| `build` | Build system or dependency changes |
| `ci` | CI configuration changes |
| `chore` | General maintenance |
| `revert` | Reverts a previous commit |

### Scope

A scope identifies the area affected.

Examples:

```text
feat(auth): add login
fix(payments): handle declined transactions
docs(github): add pull request guide
```

### Breaking changes

Use `!` to indicate a breaking change:

```text
feat(api)!: change authentication response format
```

You can also explain the breaking change in a footer:

```text
BREAKING CHANGE: The authentication response now returns a nested user object.
```

Breaking changes should be documented clearly.

## 8. Good and bad commit messages

Bad:

```text
update
fix
changes
test
new stuff
```

Good:

```text
feat(menu): add product category filtering
fix(auth): prevent expired refresh token reuse
docs(deployment): explain Docker configuration
test(orders): cover empty checkout requests
```

A good commit message should answer:

- What changed?
- Which area changed?
- Why is the change relevant, if additional explanation is needed?

## 9. Inspect commit history

Show full commit history:

```bash
git log
```

Show a compact history:

```bash
git log --oneline
```

Show branches and graph:

```bash
git log --oneline --graph --decorate --all
```

Show file change statistics:

```bash
git log --stat
```

Show commits by author:

```bash
git log --author="Your Name"
```

Show commits from a date range:

```bash
git log --since="2026-01-01" --until="2026-12-31"
```

Show history for one file:

```bash
git log -- docs/README.md
```

Show the detailed history of a file, including line changes:

```bash
git log -p -- docs/README.md
```

## 10. Inspect a specific commit

Display a commit:

```bash
git show COMMIT_HASH
```

Display only its summary:

```bash
git show --stat COMMIT_HASH
```

Display only the commit message and metadata:

```bash
git show --no-patch COMMIT_HASH
```

Use a short hash when it uniquely identifies the commit.

## 11. Amend the latest commit

If you forgot to include a file in your latest commit:

```bash
git add forgotten-file.md
git commit --amend --no-edit
```

This adds the staged changes to the latest commit without changing its message.

Change the latest commit message:

```bash
git commit --amend -m "docs: improve installation guide"
```

Important:

Amending creates a replacement commit with a new hash.

Avoid amending commits that have already been shared with other developers unless you coordinate the history rewrite.

## 12. Revert a commit

`git revert` creates a new commit that reverses the changes introduced by an earlier commit.

```bash
git revert COMMIT_HASH
```

This is usually safer for changes already pushed to a shared branch because it preserves existing history.

## 13. Reset commits

`git reset` moves the current branch reference and can change the staging area and working directory.

### Soft reset

```bash
git reset --soft HEAD~1
```

Moves the current branch back one commit while keeping the changes staged.

### Mixed reset

```bash
git reset --mixed HEAD~1
```

Moves the branch back one commit and leaves the changes unstaged in the working directory.

This is the default reset mode:

```bash
git reset HEAD~1
```

### Hard reset

```bash
git reset --hard HEAD~1
```

Moves the branch back one commit and discards changes in the index and working directory that are affected by the reset.

**Warning:** `--hard` can destroy uncommitted work. Do not use it unless you understand the consequences and have preserved anything important.

### Reset vs revert

| Command | Behavior | Typical use |
|---|---|---|
| `git reset --soft` | Moves branch; keeps changes staged | Redo latest commit |
| `git reset --mixed` | Moves branch; keeps changes unstaged | Reorganize local changes |
| `git reset --hard` | Moves branch and discards affected working changes | Carefully discard local work |
| `git revert` | Creates a new reversing commit | Undo a shared commit safely |

## 14. Practical exercise

Create a branch:

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/add-git-fundamentals
```

Create:

```text
docs/git-fundamentals.md
```

Add sections covering:

- What Git is.
- What a commit is.
- How staging works.
- Conventional Commits.
- How to inspect history.

Stage and commit the file:

```bash
git add docs/git-fundamentals.md
git commit -m "docs(git): add git fundamentals guide"
```

Add another small section to the same file.

Create a second commit:

```bash
git add docs/git-fundamentals.md
git commit -m "docs(git): expand commit history examples"
```

Inspect your history:

```bash
git log --oneline
git log --oneline --graph --decorate --all
git show HEAD
```

Inspect the changes introduced by your latest commit:

```bash
git show --stat HEAD
```

Push the branch:

```bash
git push -u origin feature/add-git-fundamentals
```

## 15. Completion checklist

- [ ] Understand the staging area.
- [ ] Use `git diff`.
- [ ] Use `git diff --cached`.
- [ ] Stage individual files.
- [ ] Create commits.
- [ ] Write Conventional Commit messages.
- [ ] Inspect commit history.
- [ ] Inspect individual commits.
- [ ] Understand amend.
- [ ] Understand revert.
- [ ] Understand reset modes.
- [ ] Push commits to GitHub.

## 16. What comes next?

Lesson 4 covers comparing branches, inspecting differences, understanding ahead/behind commits, and using GitHub's Compare feature before opening pull requests.
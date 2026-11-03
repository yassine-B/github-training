# Lesson 5 — Git Tags, Semantic Versioning, and GitHub Releases

## 1. Learning objectives

By the end of this lesson, you should understand:

- What Git tags are.
- The difference between lightweight and annotated tags.
- How Semantic Versioning works.
- How to create and manage tags.
- How to push tags to GitHub.
- How GitHub Releases work.
- How to write release notes.
- How to manage project versions.

## 2. What is a Git tag?

A Git tag is a reference identifying a specific commit.

Unlike a branch, which normally moves forward as new commits are added, a tag is intended to identify a fixed point in project history.

Example:

```text
A --- B --- C --- D --- E
          |           |
        v1.0.0      v1.1.0
```

Here:

- `v1.0.0` identifies commit C.
- `v1.1.0` identifies commit E.

Tags are useful for:

- Marking production releases.
- Identifying stable versions.
- Supporting deployments.
- Tracking bug-fix releases.
- Connecting source code to published software versions.

## 3. Lightweight vs annotated tags

Git supports two main types of tags.

### Lightweight tags

A lightweight tag is essentially a named reference to a commit.

Create one:

```bash
git tag v1.0.0
```

List tags:

```bash
git tag
```

Inspect a tag:

```bash
git show v1.0.0
```

### Annotated tags

An annotated tag stores additional metadata:

- Tag name.
- Tagger.
- Date.
- Message.
- Target commit.

Create an annotated tag:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

Inspect it:

```bash
git show v1.0.0
```

**Recommendation:** Use annotated tags for official project releases.

## 4. Tag a specific commit

You don't have to tag only the latest commit.

Inspect history:

```bash
git log --oneline
```

Example:

```text
a81f912 docs: update installation guide
c92d145 feat: add authentication
b12a501 docs: add project overview
```

Tag a specific commit:

```bash
git tag -a v1.0.0 b12a501 -m "First stable release"
```

This associates `v1.0.0` with commit `b12a501`.

## 5. Semantic Versioning (SemVer)

Semantic Versioning is a version-numbering convention.

Format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.4.2
```

| Component | Meaning | Example |
|---|---|---|
| MAJOR | Incompatible or breaking changes | 2.0.0 |
| MINOR | Backward-compatible functionality | 1.5.0 |
| PATCH | Backward-compatible bug fixes | 1.4.3 |

### MAJOR version

Increase MAJOR when introducing incompatible changes.

```text
1.5.0 → 2.0.0
```

Example: changing an API contract in a way that breaks existing clients.

### MINOR version

Increase MINOR when adding functionality without breaking existing functionality.

```text
1.4.0 → 1.5.0
```

Example: adding a new API endpoint while preserving existing endpoints.

### PATCH version

Increase PATCH when fixing bugs without introducing incompatible changes.

```text
1.4.2 → 1.4.3
```

Example: fixing an incorrect calculation without changing the public interface.

### Pre-release versions

SemVer also supports pre-release identifiers:

```text
1.0.0-alpha.1
1.0.0-beta.1
1.0.0-rc.1
```

Common meanings:

- `alpha`: early development.
- `beta`: feature testing.
- `rc`: release candidate.

Pre-release versions are not necessarily ready for general production use.

## 6. List and inspect tags

List all tags:

```bash
git tag
```

List tags matching a pattern:

```bash
git tag -l "v1.*"
```

Show the latest reachable tag:

```bash
git describe --tags
```

Show tags with their associated commits:

```bash
git show-ref --tags
```

Inspect a tag:

```bash
git show v1.0.0
```

Sort tags using version-aware sorting:

```bash
git tag --sort=-version:refname
```

## 7. Push tags to GitHub

Creating a tag locally does not automatically publish it to GitHub.

Push one tag:

```bash
git push origin v1.0.0
```

Push all local tags:

```bash
git push origin --tags
```

For normal release workflows, prefer pushing the specific release tag rather than publishing every local tag indiscriminately.

Check remote tags:

```bash
git ls-remote --tags origin
```

## 8. Delete a tag

Delete a local tag:

```bash
git tag -d v1.0.0
```

Delete a remote tag:

```bash
git push origin --delete v1.0.0
```

Be careful when deleting published release tags. Other developers and deployment systems may already depend on them.

## 9. Move or replace a tag

Sometimes a tag points to the wrong commit.

Inspect it:

```bash
git show v1.0.0
```

If you intentionally need to replace a local tag:

```bash
git tag -f -a v1.0.0 -m "Corrected release tag" COMMIT_HASH
```

Update the remote tag:

```bash
git push --force origin v1.0.0
```

**Warning:** Replacing published tags changes the meaning of an existing version reference. Avoid doing this for official releases whenever possible. Publishing a new version is generally safer.

## 10. GitHub Releases

GitHub Releases provide a way to publish software versions based on Git tags.

A release can include:

- Version number.
- Release title.
- Release notes.
- Changelog.
- Downloadable assets.
- Pre-release designation.
- Latest-release designation.

A Git tag identifies a commit. A GitHub Release adds publication information around that version.

### Create a GitHub Release

1. Open your GitHub repository.
2. Navigate to Releases.
3. Select Draft a new release.
4. Choose an existing tag or create a new one.
5. Select the target branch or commit if creating a tag.
6. Enter a release title.
7. Write release notes.
8. Add downloadable assets if needed.
9. Publish the release.

## 11. Release notes

Release notes explain what changed in a particular version.

Example:

```markdown
# Version 1.0.0

## Features

- Added repository setup documentation.
- Added branch management guide.
- Added commit conventions guide.

## Improvements

- Improved Git command examples.
- Organized training documentation.

## Documentation

- Added Git fundamentals.
- Added branch comparison instructions.
```

Good release notes should help users understand what changed without inspecting every commit.

### Automatically generated release notes

GitHub can generate release notes from merged pull requests and associated contributors.

This is useful for projects with consistent PR titles, labels, and commit messages.

You can customize generated notes before publishing.

## 12. Recommended versioning strategy

For your future Django REST Framework and React projects, a versioning scheme could look like this:

| Version | Example milestone |
|---|---|
| 0.1.0 | Initial development version |
| 0.2.0 | Authentication implemented |
| 0.3.0 | Main business features implemented |
| 0.9.0 | Feature-complete testing version |
| 1.0.0 | First stable production release |
| 1.0.1 | Production bug fix |
| 1.1.0 | New backward-compatible functionality |
| 2.0.0 | Breaking API or architecture changes |

This is an example strategy, not a requirement. Define what constitutes a breaking change for each project.

## 13. Practical exercise — Publish your first release

We will create a release for the training repository.

### Step 1 — Inspect the repository

```bash
git status
git switch main
git pull --ff-only origin main
```

Ensure your working tree is clean.

### Step 2 — Inspect commit history

```bash
git log --oneline --graph --decorate --all
```

Review the history and identify a useful milestone.

### Step 3 — Create a release preparation branch

```bash
git switch -c chore/prepare-v1-release
```

### Step 4 — Create a changelog

Create:

```text
CHANGELOG.md
```

Add:

```markdown
# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-11-03

### Added

- Initial GitHub training repository.
- Repository setup documentation.
- Git branching guide.
- Commit and history guide.
- Branch comparison guide.

### Documentation

- Added Module 1 lesson references.
- Added practical Git command examples.
```

Adjust the date if you publish the release on another day.

### Step 5 — Commit the changelog

```bash
git add CHANGELOG.md
git commit -m "docs(release): add v1.0.0 changelog"
```

### Step 6 — Push the release preparation branch

```bash
git push -u origin chore/prepare-v1-release
```

Open a pull request on GitHub:

- Base: `main`
- Compare: `chore/prepare-v1-release`

Review and merge the pull request.

Synchronize your local main branch:

```bash
git switch main
git pull --ff-only origin main
```

Delete the local branch:

```bash
git branch -d chore/prepare-v1-release
```

### Step 7 — Create an annotated tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

Inspect it:

```bash
git show v1.0.0
```

### Step 8 — Push the tag

```bash
git push origin v1.0.0
```

### Step 9 — Publish a GitHub Release

On GitHub:

1. Open Releases.
2. Select Draft a new release.
3. Select `v1.0.0`.
4. Enter the title `Version 1.0.0`.
5. Add release notes.
6. Publish the release.

### Step 10 — Verify everything

```bash
git tag
git describe --tags
git ls-remote --tags origin
```

Verify that the release is visible in the GitHub Releases section.

## 14. Important commands reference

| Command | Purpose |
|---|---|
| `git tag` | List local tags |
| `git tag v1.0.0` | Create lightweight tag |
| `git tag -a v1.0.0 -m "message"` | Create annotated tag |
| `git tag -a TAG COMMIT -m "message"` | Tag a specific commit |
| `git show v1.0.0` | Inspect a tag |
| `git tag -l "v1.*"` | Filter tags |
| `git describe --tags` | Describe current commit using tags |
| `git tag --sort=-version:refname` | Sort tags by version |
| `git push origin v1.0.0` | Push one tag |
| `git push origin --tags` | Push all local tags |
| `git tag -d v1.0.0` | Delete local tag |
| `git push origin --delete v1.0.0` | Delete remote tag |
| `git ls-remote --tags origin` | Inspect remote tags |

## 15. Completion checklist

- [ ] Understand what Git tags are.
- [ ] Understand lightweight tags.
- [ ] Understand annotated tags.
- [ ] Understand Semantic Versioning.
- [ ] Create a tag.
- [ ] Tag a specific commit.
- [ ] Inspect tags.
- [ ] Push a tag to GitHub.
- [ ] Understand tag deletion.
- [ ] Understand GitHub Releases.
- [ ] Create a changelog.
- [ ] Publish a GitHub Release.

## 16. What comes next?

Lesson 6 covers GitHub repository collaboration and contribution guidance, including README improvements, LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, and repository templates.

These files help establish professional standards for projects with multiple developers.
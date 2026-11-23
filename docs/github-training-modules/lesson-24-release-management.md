# Module 1 — Code

## Lesson 24: GitHub Releases, Tags, and Version History — Advanced Repository Release Management

**Level:** Advanced
**Type:** Practical lesson
**Repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By the end of this lesson, you should understand:

1. Git tags versus GitHub Releases.
2. Lightweight and annotated tags.
3. Semantic Versioning (SemVer).
4. Version numbering strategies.
5. Release branches and maintenance branches.
6. Draft releases and pre-releases.
7. Release notes and changelog management.
8. Comparing releases and tags.
9. Release assets and downloadable artifacts.
10. GitHub CLI release management.
11. Hotfix releases.
12. Release automation with GitHub Actions.

## 2. Git tags versus GitHub Releases

A Git tag is a reference to a particular Git object, usually a commit.

A GitHub Release is a release entry associated with a Git tag.

Git tags identify repository versions. GitHub Releases package release information, notes, and downloadable assets.

Example:

| Git tag | GitHub Release |
| --- | --- |
| v1.0.0 | Application 1.0.0 |
| v1.1.0 | Application 1.1.0 |
| v1.1.1 | Application 1.1.1 |

You can create Git tags without publishing GitHub Releases.

## 3. Lightweight versus annotated tags

### Lightweight tag

```bash
git tag v1.0.0
```

A lightweight tag is a named reference to an object, usually a commit.

### Annotated tag

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
```

An annotated tag contains:

- Tag name.
- Tagger identity.
- Tagging date.
- Tag message.
- Optional cryptographic signature.

Push a tag:

```bash
git push origin v1.0.0
```

Push all tags:

```bash
git push origin --tags
```

Inspect tags:

```bash
git tag --list
git show v1.0.0
git cat-file -t v1.0.0
```

Annotated tags are recommended for official releases.

## 4. Semantic Versioning (SemVer)

SemVer uses:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.4.2
```

### MAJOR

Increment when introducing incompatible public API changes.

Example:

```text
1.4.2 -> 2.0.0
```

### MINOR

Increment when introducing backward-compatible functionality.

Example:

```text
1.4.2 -> 1.5.0
```

### PATCH

Increment when introducing backward-compatible bug fixes.

Example:

```text
1.4.2 -> 1.4.3
```

### Version examples

| Change | Current | Next |
| --- | --- | --- |
| Bug fix | 1.0.0 | 1.0.1 |
| Compatible feature | 1.0.1 | 1.1.0 |
| Breaking API change | 1.1.0 | 2.0.0 |
| Bug fix | 2.0.0 | 2.0.1 |

### Pre-release versions

```text
1.0.0-alpha.1
1.0.0-beta.1
1.0.0-rc.1
1.0.0
```

- Alpha: Early development.
- Beta: Feature testing.
- RC: Release candidate.
- Final: Stable release.

Build metadata is also supported:

```text
1.0.0+20261119
```

Build metadata does not affect version precedence.

Official specification:

<https://semver.org/spec/v2.0.0.html>

## 5. Versioning strategies

### Application versioning

```text
restaurant-pos-v1.0.0
restaurant-pos-v1.1.0
restaurant-pos-v2.0.0
```

### Library versioning

```text
django-core-utils-v1.0.0
django-core-utils-v1.1.0
```

### SaaS platform versioning

```text
platform-v0.1.0
platform-v0.2.0
platform-v1.0.0
```

During initial development, `0.y.z` indicates an unstable public API under SemVer.

### Monorepo versioning

One version for the entire repository:

```text
v1.0.0
v1.1.0
```

Independent versions for each component:

```text
backend-v1.2.0
frontend-v2.0.0
mobile-v1.4.0
```

Choose the approach according to component dependencies and deployment requirements.

## 6. Release and maintenance branches

Release branches stabilize a version independently of ongoing development.

Example:

```text
main
 |
 |---- v1.0.0
 |
 |---- v1.1.0
 |
 |---- release/1.5
 |        |
 |        |---- v1.5.0
 |        |---- v1.5.1
 |
 |---- development of v2.0.0
```

Create a release branch:

```bash
git switch main
git pull origin main

git switch -c release/1.5
```

Push it:

```bash
git push -u origin release/1.5
```

Commit a maintenance fix:

```bash
git add .
git commit -m "fix(auth): correct token expiration handling"
```

After review and merging:

```bash
git tag -a v1.5.1 -m "Release version 1.5.1"
git push origin v1.5.1
```

If a fix must also appear in another development branch, integrate it using an appropriate merge or cherry-pick.

```bash
git switch main
git cherry-pick <fix-commit-sha>
```

## 7. Changelog management

Create:

```text
CHANGELOG.md
```

Recommended structure:

```markdown
## Changelog

All notable changes are documented here.

## [Unreleased]

### Added

### Changed

### Fixed

### Removed

## [1.1.0] - 2026-11-19

### Added
- Added kitchen station management.
- Added order status notifications.

### Changed
- Improved order processing.

### Fixed
- Corrected duplicate order submission.

## [1.0.1] - 2026-11-10

### Fixed
- Fixed authentication validation.
- Corrected receipt generation.
```

### Changelog categories

| Category | Meaning |
| --- | --- |
| Added | New functionality |
| Changed | Changes to existing functionality |
| Deprecated | Planned removal |
| Removed | Removed functionality |
| Fixed | Bug fixes |
| Security | Security-related changes |

### Commit history versus changelog

Commit history describes individual implementation changes.

A changelog communicates the meaningful changes included in a release.

### Automatic release notes

GitHub can generate release notes based on merged pull requests and contributors.

You can customize categories using:

```text
.github/release.yml
```

Example:

```yaml
changelog:
  categories:
    - title: Breaking Changes
      labels:
        - breaking-change
    - title: New Features
      labels:
        - feature
    - title: Bug Fixes
      labels:
        - bug
    - title: Maintenance
      labels:
        - maintenance
    - title: Other Changes
      labels:
        - "*"
```

Configure the labels to match the actual labels used by your repository.

## 8. Draft, pre-release, and published releases

### Draft release

A release that has not yet been published.

Use it when release notes or assets still need review.

### Pre-release

A release intended for testing rather than general stable use.

Examples:

```text
v2.0.0-alpha.1
v2.0.0-beta.1
v2.0.0-rc.1
```

### Published release

The official published release entry containing its tag, release notes, and optional assets.

### Typical lifecycle

1. Development.
2. Release candidate.
3. Draft release.
4. Final testing and review.
5. Published release.
6. Maintenance and patch releases.

GitHub also supports immutable releases. When enabled, publishing a release can restrict later changes to its assets and tag.

## 9. Release assets

Release assets are downloadable files attached to GitHub Releases.

Examples:

| Asset | Purpose |
| --- | --- |
| `.exe` | Windows executable |
| `.msi` | Windows installer |
| `.zip` | Application package |
| `.tar.gz` | Compressed distribution |
| `.apk` | Android application package |
| `.pdf` | Documentation |
| `checksums.txt` | Integrity verification |

Upload an asset:

```bash
gh release upload v1.0.0 ./dist/application.zip
```

Download a release:

```bash
gh release download v1.0.0
```

Download a specific file:

```bash
gh release download v1.0.0 --pattern "*.exe"
```

GitHub automatically provides source-code ZIP and tarball archives for tagged commits.

Release asset limits documented by GitHub include up to 1,000 assets per release, with each asset under 2 GiB.

## 10. GitHub CLI release management

Check installation:

```bash
gh --version
```

Authenticate:

```bash
gh auth login
```

List releases:

```bash
gh release list
```

View a release:

```bash
gh release view v1.0.0
```

Create a release:

```bash
gh release create v1.0.0 \
  --title "Version 1.0.0" \
  --notes "Initial stable release"
```

Create a pre-release:

```bash
gh release create v1.1.0-beta.1 \
  --title "Version 1.1.0 Beta 1" \
  --notes "Beta testing release" \
  --prerelease
```

Create a draft:

```bash
gh release create v1.2.0 --draft --generate-notes
```

Edit a release:

```bash
gh release edit v1.0.0 --title "Restaurant POS v1.0.0"
```

Delete a release:

```bash
gh release delete v1.0.0
```

Deleting a GitHub Release and deleting its Git tag are separate operations.

Official reference:

<https://cli.github.com/manual/gh_release>

## 11. Comparing releases

GitHub comparison URL:

```text
https://github.com/OWNER/REPOSITORY/compare/v1.0.0...v1.1.0
```

Git CLI:

```bash
git diff v1.0.0 v1.1.0
```

Show a summary:

```bash
git diff --stat v1.0.0 v1.1.0
```

List commits:

```bash
git log --oneline v1.0.0..v1.1.0
```

Compare one file:

```bash
git diff v1.0.0 v1.1.0 -- backend/orders/services.py
```

Find the nearest reachable tag:

```bash
git describe --tags --abbrev=0
```

## 12. Hotfix releases

A hotfix is a targeted correction to an existing release.

Example:

```text
v1.4.0 -> v1.4.1
```

Create a branch from the affected version:

```bash
git switch --detach v1.4.0

git switch -c hotfix/1.4.1
```

Implement and commit the correction:

```bash
git add backend/orders/services.py

git commit -m "fix(orders): correct order total calculation"
```

Push:

```bash
git push -u origin hotfix/1.4.1
```

Create a PR targeting the appropriate maintenance branch.

After review and merging:

```bash
git tag -a v1.4.1 -m "Release version 1.4.1"

git push origin v1.4.1
```

Publish the corresponding GitHub Release.

Ensure the fix is also integrated into future development branches when required.

## 13. GitHub Actions release automation

Create:

```text
.github/workflows/release.yml
```

Introductory example:

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

permissions:
  contents: write

jobs:
  release:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run tests
        run: |
          echo "Run project tests here"

      - name: Build application
        run: |
          echo "Build application here"

      - name: Create release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh release create "${GITHUB_REF_NAME}" \
            --generate-notes
```

Replace placeholder commands with actual project tests and build commands before using it.

The workflow:

1. Triggers when a matching version tag is pushed.
2. Checks out the repository.
3. Runs tests.
4. Builds the application.
5. Creates a GitHub Release.

The `contents: write` permission allows the workflow to publish the release.

This introductory example does not yet attach compiled assets.

## 14. Practical exercises

### Exercise 1 — Tag types

Create lightweight and annotated tags.

```bash
git tag practice-lightweight

git tag -a practice-annotated \
  -m "Annotated tag practice"
```

Inspect them:

```bash
git cat-file -t practice-lightweight
git cat-file -t practice-annotated
```

Explain the difference.

### Exercise 2 — Semantic Versioning

Determine the next version for:

- A bug fix.
- A compatible API endpoint.
- A removed public API field.
- An optional configuration setting.

Document the results.

### Exercise 3 — Create CHANGELOG.md

Create a changelog with:

- Unreleased.
- Version 1.0.0.
- Version 1.0.1.
- Added, Changed, Fixed, and Removed sections.

### Exercise 4 — Release branch

Create:

```bash
git switch -c release/1.0
```

Make a documentation change, commit it, and push the branch.

### Exercise 5 — Draft release

Create a draft release on GitHub, add release notes, save it, and inspect it.

### Exercise 6 — Pre-release

Create:

```text
v1.0.0-beta.1
```

Publish it as a pre-release.

### Exercise 7 — Release asset

Create:

```text
release-assets/installation-guide.md
```

Upload it:

```bash
gh release upload v1.0.0-beta.1 release-assets/installation-guide.md
```

### Exercise 8 — Compare releases

Create two practice tags on different commits.

```bash
git diff <old-tag> <new-tag>

git log --oneline <old-tag>..<new-tag>
```

Document the changes.

### Exercise 9 — Hotfix

Create a hotfix branch from a practice version.

Implement a documentation correction, commit it, and create a patch tag.

### Exercise 10 — Release automation

Create `.github/workflows/release.yml`.

Review the trigger, runner, jobs, steps, permissions, and release command.

Do not publish a test release until the workflow has been reviewed.

## 15. Advanced challenge — Design a complete release strategy

Scenario:

You maintain a SaaS platform containing:

```text
platform/
├── backend/
│   └── Django REST Framework
├── frontend/
│   └── React + TypeScript
├── mobile/
│   └── React Native
├── infrastructure/
│   └── Docker + Nginx
└── docs/
```

Your team needs to publish version 1.0.0.

Three months later:

- A new feature is introduced.
- An authentication bug is discovered.
- A beta release is required.
- A breaking API change is introduced.
- An older version must remain supported.

Design a release strategy covering:

1. Version numbering.
2. Branching strategy.
3. Release branch naming.
4. Annotated tag conventions.
5. Changelog management.
6. Draft and pre-release procedures.
7. Production release procedures.
8. Hotfix procedures.
9. Release comparison.
10. Release asset management.
11. GitHub Actions automation.

Create:

```text
exercises/module-01-code/lesson-24-release-management-strategy.md
```

Include a version history table, branch diagram, sample changelog, and step-by-step release procedure.

## 16. Completion checklist

- [ ] I understand Git tags and GitHub Releases.
- [ ] I can create lightweight tags.
- [ ] I can create annotated tags.
- [ ] I understand Semantic Versioning.
- [ ] I can identify breaking changes.
- [ ] I understand release branches.
- [ ] I can create a CHANGELOG.md.
- [ ] I can create draft releases.
- [ ] I can publish pre-releases.
- [ ] I can attach release assets.
- [ ] I can use GitHub CLI for releases.
- [ ] I can compare two versions.
- [ ] I understand hotfix releases.
- [ ] I understand release automation.
- [ ] I completed the practical exercises.
- [ ] I completed the advanced challenge.

## 17. References

- GitHub Docs — Releasing projects:
  <https://docs.github.com/en/repositories/releasing-projects-on-github>

- GitHub Docs — About releases:
  <https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases>

- GitHub Docs — Managing releases:
  <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>

- Git documentation — git-tag:
  <https://git-scm.com/docs/git-tag>

- Semantic Versioning:
  <https://semver.org/spec/v2.0.0.html>

- GitHub CLI — Releases:
  <https://cli.github.com/manual/gh_release>

---

**Next lesson:** Lesson 25 — GitHub Repository Documentation and Project Documentation Management: README, Wiki, GitHub Pages, and Documentation Workflows.

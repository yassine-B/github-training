# Lesson 12 — Release Engineering: Changelogs, Hotfixes, and Release Automation

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Plan a release from completed Issues and merged Pull Requests.
- Select the correct Semantic Versioning increment.
- Maintain a useful `CHANGELOG.md`.
- Configure GitHub's automatically generated release notes.
- Prepare draft releases and prereleases.
- Understand release branches and hotfix branches.
- Perform a hotfix without losing the normal development workflow.
- Connect releases to Issues, Pull Requests, milestones, and tags.
- Follow a repeatable release checklist.

**Prerequisite:** Lesson 5 — Git Tags and GitHub Releases.

---

# Part 1 — Understanding release engineering

## 2. What is release engineering?

Release engineering is the process of preparing, validating, documenting, and publishing a particular version of a project.

A release is more than creating a Git tag.

A professional release process normally includes:

1. Reviewing completed work.
2. Checking outstanding bugs and known limitations.
3. Selecting a version number.
4. Updating the changelog.
5. Running tests and quality checks.
6. Preparing release notes.
7. Creating a Git tag.
8. Publishing a GitHub Release.
9. Communicating the release.
10. Monitoring for problems after publication.

### 2.1 The relationship between Git commits, tags, and releases

These concepts have different responsibilities:

| Concept | Responsibility |
|---|---|
| Commit | Records a change in repository history |
| Pull Request | Proposes and reviews a set of changes |
| Git tag | Marks a specific commit |
| CHANGELOG.md | Maintains a human-readable history of changes |
| GitHub Release | Packages a tagged version with release notes and optional assets |

A GitHub Release is based on a Git tag. A tag can exist without a GitHub Release, and the tag and release can be created at different times. See the official documentation: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

### 2.2 Example release lifecycle

Imagine that you are developing a restaurant management system.

You have completed:

- Customer order management.
- Kitchen order display.
- Cashier interface.
- Daily sales report.
- Bug fixes for order processing.

Your release process could look like this:

```text
Issues created
     |
     v
Development branches
     |
     v
Pull Requests
     |
     v
Code review and tests
     |
     v
Merge into main
     |
     v
Release preparation
     |
     +---- Update CHANGELOG.md
     |
     +---- Select version
     |
     +---- Run final checks
     |
     v
Create Git tag
     |
     v
Create GitHub Release
     |
     v
Monitor the released version
```

The important principle is that a release should represent a known, reviewed, and identifiable state of the repository.

---

# Part 2 — Selecting the release version

## 3. Semantic Versioning in a real workflow

Use the format:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
v1.4.2
```

| Version component | Increment when |
|---|---|
| MAJOR | You introduce incompatible changes |
| MINOR | You add backward-compatible functionality |
| PATCH | You fix bugs without introducing new functionality |

### 3.1 Practical examples

Suppose your application is currently at `v1.4.2`.

**Example A — Bug fix**

You fix an issue where the cashier report displays an incorrect total.

New version:

```text
v1.4.3
```

**Example B — New feature**

You add a new dashboard that displays daily sales statistics without breaking existing functionality.

New version:

```text
v1.5.0
```

**Example C — Breaking change**

You replace an API endpoint and existing clients must change their requests.

New version:

```text
v2.0.0
```

### 3.2 How Conventional Commits help

Conventional Commits provide useful information when deciding what kind of release is appropriate.

| Commit type | Typical release impact |
|---|---|
| `fix:` | PATCH |
| `feat:` | MINOR |
| `feat!:` | MAJOR |
| `fix!:` | MAJOR |
| `docs:` | Usually no application release increment by itself |
| `test:` | Usually no application release increment by itself |
| `refactor:` | Depends on whether behavior or compatibility changes |
| `perf:` | Depends on the change; often MINOR or PATCH |
| `chore:` | Usually no application release increment by itself |

These are conventions, not an automatic guarantee. You must inspect the actual changes and determine whether compatibility has changed.

Example commit history:

```text
feat(orders): add order cancellation
feat(kitchen): add station filtering
fix(cashier): correct daily total calculation
fix(auth): handle expired sessions
docs(api): document order endpoints
```

A reasonable release decision could be:

```text
v1.4.2 -> v1.5.0
```

because the release contains new backward-compatible functionality.

**Important:** A release version should be based on the changes included since the previous release, not simply the number of commits.

---

# Part 3 — Maintaining CHANGELOG.md

## 4. What is a changelog?

A changelog is a document that records meaningful changes between project versions.

It answers questions such as:

- What was added?
- What was fixed?
- What changed?
- What was removed?
- Are there any breaking changes?
- Does the user need to take action after upgrading?

A changelog is not intended to list every individual commit.

Instead, it communicates the impact of changes to developers, administrators, and users.

## 5. Recommended changelog structure

Create this file in your repository root:

```text
CHANGELOG.md
```

A useful convention is to organize it by version and change category.

Use the following example as your initial content:

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format follows the principles of Keep a Changelog.
Versions follow Semantic Versioning.

## [Unreleased]

### Added

- 

### Changed

- 

### Fixed

- 

### Removed

- 

### Security

- 

## [1.0.0] - 2026-11-05

### Added

- Initial training repository structure.
- Git fundamentals training documentation.
- Branching and commit history lessons.
- Repository documentation standards.
- Pull Request collaboration exercises.
- GitHub Issues and Discussions lessons.

### Changed

- Established Conventional Commit naming conventions.
- Standardized documentation structure.
```

**Important:** Treat the `1.0.0` section above as an example only. Do not claim that this version was published unless you have actually created the corresponding tag and release. Adjust the version history to match your real repository.

Reference: https://keepachangelog.com/en/1.1.0/

## 6. Understanding changelog categories

### Added

New functionality.

Example:

```markdown
### Added

- Added a new kitchen station filtering feature.
- Added support for customer order cancellation.
```

### Changed

Changes to existing functionality.

```markdown
### Changed

- Improved the cashier dashboard layout.
- Updated the order processing workflow.
```

### Fixed

Bug fixes.

```markdown
### Fixed

- Fixed incorrect daily sales calculations.
- Fixed an issue with duplicate order submissions.
```

### Removed

Functionality that has been removed.

```markdown
### Removed

- Removed the deprecated order export endpoint.
```

### Security

Security-related improvements.

```markdown
### Security

- Updated authentication validation.
- Improved permission checks for administrative endpoints.
```

### Breaking changes

For a major release, explicitly document incompatible changes.

```markdown
## [2.0.0] - YYYY-MM-DD

### Breaking Changes

- Replaced the old authentication response structure.
- Updated the API endpoint used to create orders.

### Migration Guide

1. Update the frontend API client.
2. Update authentication response handling.
3. Test all login and logout workflows.
```

## 7. The Unreleased section

The `[Unreleased]` section is where you collect changes that have not yet been included in a published release.

Example:

```markdown
## [Unreleased]

### Added

- Added a new order filtering option.

### Fixed

- Fixed a pagination issue in the orders endpoint.
```

When preparing a release:

1. Review the Unreleased section.
2. Verify that each entry is included in the release.
3. Move those entries under the new version heading.
4. Add the release date.
5. Create a fresh empty Unreleased section.

For example:

```markdown
## [Unreleased]

### Added

### Changed

### Fixed

## [1.5.0] - YYYY-MM-DD

### Added

- Added a new order filtering option.

### Fixed

- Fixed a pagination issue in the orders endpoint.
```

This makes the changelog useful throughout the project's lifetime.

---

# Part 4 — GitHub automatically generated release notes

## 8. Why use generated release notes?

GitHub can generate release notes based on the Pull Requests included between releases.

Generated notes can include:

- Merged Pull Requests.
- Contributors.
- A link to the full changelog.

You can also organize Pull Requests into categories using labels.

This is useful when a project has many contributors and Pull Requests.

Official documentation:

https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes

## 9. Configure `.github/release.yml`

Create:

```text
.github/release.yml
```

Add:

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
      - internal-only

  categories:
    - title: "Breaking Changes"
      labels:
        - breaking-change
        - Semver-Major

    - title: "New Features"
      labels:
        - enhancement
        - feature
        - Semver-Minor

    - title: "Bug Fixes"
      labels:
        - bug
        - bugfix
        - fix

    - title: "Dependencies"
      labels:
        - dependencies

    - title: "Documentation"
      labels:
        - documentation

    - title: "Other Changes"
      labels:
        - "*"
```

### 9.1 How does this configuration work?

When GitHub generates release notes, it checks the labels assigned to merged Pull Requests.

For example:

| Pull Request | Labels | Generated category |
|---|---|---|
| Add order cancellation | `enhancement` | New Features |
| Fix cashier calculation | `bug` | Bug Fixes |
| Update dependencies | `dependencies` | Dependencies |
| Update README | `documentation` | Documentation |
| Internal formatting | `ignore-for-release` | Excluded |

The `*` label is a catch-all category for Pull Requests that do not match earlier categories.

**Important:** This configuration categorizes Pull Requests by their GitHub labels. It does not automatically translate every Conventional Commit into a release category. Your team must apply meaningful labels consistently.

### 9.2 Exercise: Create the release configuration

1. Create `.github/release.yml`.
2. Add the configuration above.
3. Create a test Pull Request.
4. Assign it an appropriate label.
5. Merge it.
6. When preparing a test release, generate release notes.
7. Inspect the output and confirm that the Pull Request appears in the expected category.

---

# Part 5 — Draft releases and prereleases

## 10. Draft release

A draft release is an unpublished release that you can prepare and review before making it public.

Use a draft when:

- You need to review the release notes.
- You need to attach downloadable assets.
- You want another person to check the release.
- You are not ready to publish the version.

A draft is not the same as a prerelease.

## 11. Prerelease

A prerelease is a published version intended for testing or early access rather than normal stable use.

Examples:

```text
v1.5.0-alpha.1
v1.5.0-beta.1
v1.5.0-rc.1
```

Typical progression:

```text
v1.5.0-alpha.1
       |
       v
v1.5.0-alpha.2
       |
       v
v1.5.0-beta.1
       |
       v
v1.5.0-rc.1
       |
       v
v1.5.0
```

| Stage | Purpose |
|---|---|
| Alpha | Early development testing |
| Beta | Broader testing and feedback |
| RC | Release candidate; intended to be close to final |
| Stable | Normal production release |

A prerelease can be useful when you want selected users or testers to evaluate a version before it becomes stable.

### 11.1 Exercise: Prepare a prerelease

For this exercise, do not publish a real production application. Use your training repository.

Prepare the following hypothetical version:

```text
v1.1.0-beta.1
```

Write release notes containing:

- What is included.
- What still needs testing.
- Known limitations.
- How testers should report issues.

Save it as a draft first. Review the information before deciding whether to publish it as a prerelease.

---

# Part 6 — Release branches and development strategies

## 12. What is a release branch?

A release branch is a branch used to stabilize and prepare a particular version.

Example:

```text
main
 |
 +---- feature/order-filtering
 |
 +---- feature/daily-sales-report
 |
 +---- release/1.5.0
```

The release branch may be used for:

- Final bug fixes.
- Version metadata updates.
- Changelog updates.
- Release-specific validation.
- Preparing the final release tag.

It should not normally receive unrelated new features.

## 13. Release branches versus trunk-based development

There are different approaches to managing releases.

### Approach A — Trunk-based development

Most changes are merged into `main` frequently.

```text
main
 |
 +---- PR A
 |
 +---- PR B
 |
 +---- PR C
 |
 +---- Release v1.5.0
```

Advantages:

- Fewer long-lived branches.
- Frequent integration.
- Simpler branch management.
- Works well with automated testing and deployment.

### Approach B — Release branches

You create a dedicated branch when preparing a release.

```text
main
 |
 +---- feature A
 |
 +---- feature B
 |
 +---- release/1.5.0
          |
          +---- bug fix
          |
          +---- validation
          |
          +---- v1.5.0
```

Advantages:

- Stabilization can happen independently.
- New development can continue on `main`.
- Useful when multiple supported versions must be maintained.

Disadvantages:

- More branches to maintain.
- Fixes may need to be applied to multiple branches.
- Merging and synchronization become more complicated.

### 13.1 Which approach should you use?

For a small project with one active production version, start with a simple workflow:

- `main` contains reviewed, integrated changes.
- Feature branches are short-lived.
- Release tags identify stable versions.
- Create a release branch only when you have a concrete reason to stabilize a version independently.

Do not introduce release branches simply because a large project uses them.

---

# Part 7 — Hotfix workflow

## 14. What is a hotfix?

A hotfix is a targeted correction for an important problem in a released version.

Example:

Your restaurant system is running:

```text
v1.5.0
```

You discover that the daily cashier report calculates totals incorrectly.

You need to correct the issue without including unfinished features currently being developed.

A typical hotfix workflow:

```text
                 main
                   |
                   v
                v1.5.0
                   |
                   |
                   +------ hotfix/1.5.1
                                  |
                                  v
                             Bug correction
                                  |
                                  v
                              Tests
                                  |
                                  v
                              Pull Request
                                  |
                                  v
                            Merge hotfix
                                  |
                                  v
                               v1.5.1
```

The patch version increases because this is a backward-compatible bug fix.

## 15. Hotfix exercise

For this exercise, use a small documentation correction in your training repository. You will simulate the workflow without changing any existing published tag.

### Step 1 — Inspect your repository

Open your terminal:

```bash
git status
git branch -a
git tag --list
git log --oneline --decorate -n 20
```

These commands help you understand your current state:

| Command | Purpose |
|---|---|
| `git status` | Shows modified and untracked files |
| `git branch -a` | Lists local and remote branches |
| `git tag --list` | Lists existing tags |
| `git log --oneline --decorate -n 20` | Displays recent commits and references |

Identify the latest stable release tag, if one exists.

**Do not assume that `v1.0.0` exists.** Check your local tags and the Releases page on GitHub.

### Step 2 — Select the correct starting point

If you have a published stable release tag, use it as the base for the simulated hotfix.

For example, if your latest stable tag is `v1.0.0`:

```bash
git switch -c hotfix/1.0.1 v1.0.0
```

This creates a new branch from that specific tagged commit.

If you do not have a suitable published release yet, do not invent one or move an existing tag. Instead, perform the exercise from your current `main` branch:

```bash
git switch main
git pull origin main
git switch -c hotfix/documentation-correction
```

The second approach is a workflow simulation, not a real patch release.

### Step 3 — Make a small correction

Choose an existing documentation file and correct a small factual or formatting issue.

For example:

```text
docs/github/module-01-code/README.md
```

Make a meaningful correction, such as fixing a broken lesson reference.

### Step 4 — Inspect and commit

```bash
git status
git diff
git add docs/github/module-01-code/README.md
git diff --cached
git commit -m "fix(docs): correct lesson reference in code module"
```

### Step 5 — Push the branch

```bash
git push -u origin hotfix/documentation-correction
```

If you used the versioned branch name instead, push that exact branch.

### Step 6 — Open a Pull Request

On GitHub:

1. Open the repository.
2. Select Pull Requests.
3. Select New Pull Request.
4. Choose `main` as the base branch for the simulation.
5. Choose your hotfix branch as the compare branch.
6. Explain the correction.
7. Request a review.
8. Review the changes.
9. Merge the Pull Request.

For a real production hotfix, the base branch may instead be a maintained release branch. Follow the project's actual support policy.

### Step 7 — Create a patch release only when appropriate

If you performed a real hotfix against a released application, the next patch version might be:

```text
v1.5.0 -> v1.5.1
```

For this documentation-only training exercise, do not create a production version tag merely to imitate the process.

### Step 8 — Synchronize the fix

If the hotfix was made on a separate maintained release branch, make sure the correction is also incorporated into the main development line when appropriate.

Otherwise, the bug may reappear in the next release.

**Key lesson:** A hotfix is not complete just because the patch was merged into one branch. You must ensure that supported branches contain the correction.

---

# Part 8 — Connecting releases to Issues and Pull Requests

## 16. Connect development work to a release

A release should have traceable links to the work it contains.

For example:

```text
Issue #12 — Add order cancellation
        |
        v
PR #25 — Implement order cancellation
        |
        v
Merge into main
        |
        v
Release v1.5.0
```

You can use GitHub's automatic closing keywords in Pull Request descriptions:

```markdown
Closes #12
Fixes #18
Resolves #21
```

When the Pull Request is merged into the repository's default branch, the associated Issues are automatically closed.

### 16.1 Use milestones

Milestones can group Issues and Pull Requests that belong to a planned release.

Example:

```text
Milestone: Release 1.5.0

Issues:
- Add order cancellation
- Add kitchen station filtering
- Fix daily sales report

Pull Requests:
- PR #25
- PR #28
- PR #31
```

Before releasing:

1. Review the milestone.
2. Check whether all required Issues are complete.
3. Check whether the related Pull Requests have been merged.
4. Review any remaining open work.
5. Decide whether incomplete work should be postponed or block the release.

Remember:

- A milestone is a planning tool.
- A Git tag identifies a commit.
- A GitHub Release packages a tagged version.

They are related, but they are not interchangeable.

---

# Part 9 — Preparing a real release

## 17. Release readiness checklist

Before publishing a stable release, verify the following.

### Repository state

- [ ] The intended release branch is correct.
- [ ] The working tree is clean.
- [ ] All intended changes have been merged.
- [ ] No unfinished feature has accidentally entered the release.
- [ ] The previous release tag is identified.

### Code quality

- [ ] Automated tests pass.
- [ ] Build succeeds.
- [ ] Linting and formatting checks pass.
- [ ] Important workflows have been tested.
- [ ] Security checks have been reviewed where applicable.

### Documentation

- [ ] `CHANGELOG.md` is updated.
- [ ] Breaking changes are documented.
- [ ] Migration instructions are available where necessary.
- [ ] Known limitations are documented.
- [ ] Release notes are accurate.

### Versioning

- [ ] The version increment is correct.
- [ ] The tag does not already exist.
- [ ] The tag points to the intended commit.
- [ ] The version is consistent across relevant project metadata.

### GitHub Release

- [ ] Release title is correct.
- [ ] Release notes are reviewed.
- [ ] The previous tag is correct when generating notes.
- [ ] Prerelease status is correct.
- [ ] Required assets are attached.
- [ ] The release is published only when ready.

## 18. Inspect the repository before a release

Use these commands:

```bash
git status
git fetch origin --tags
git branch -a
git tag --list
git log --oneline --decorate -n 30
git diff <previous-tag>..main
```

Replace `<previous-tag>` with the actual previous release tag.

For example:

```bash
git diff v1.4.0..main
```

This shows the changes between the previous release and the current `main` branch.

Inspect the changed files:

```bash
git diff --name-status v1.4.0..main
```

Inspect commits included in the range:

```bash
git log --oneline v1.4.0..main
```

Do not copy the example version unless it exists in your repository.

## 19. Create an annotated release tag

Once the release has been approved and the target commit is correct:

```bash
git switch main
git pull origin main
git tag -a v1.5.0 -m "Release v1.5.0"
```

Inspect the tag:

```bash
git show v1.5.0
```

Push it:

```bash
git push origin v1.5.0
```

**Important:** The version `v1.5.0` is an example. Select your actual next version after inspecting the repository.

Avoid deleting or moving a published release tag to fix a mistake. Treat published version tags as stable references. If a release has a problem, follow a documented correction process, normally publishing a new version.

## 20. Publish a GitHub Release

On GitHub:

1. Open your repository.
2. Open Releases.
3. Select Draft a new release.
4. Select the existing tag you just pushed.
5. Select the intended target commit or branch if required.
6. Select the previous tag if you need to control the comparison range.
7. Enter a meaningful release title.
8. Select Generate release notes.
9. Review the generated content.
10. Add any missing migration or upgrade instructions.
11. Attach assets if your project distributes them.
12. Select prerelease only if this is genuinely a prerelease.
13. Save as a draft or publish when ready.

GitHub's release page supports both manually written and automatically generated release notes. Always review generated notes before publication.

Official documentation:

https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

---

# Part 10 — Release automation concepts

## 21. What can be automated?

A release workflow can eventually automate:

- Running tests.
- Running linting and security checks.
- Building the application.
- Creating deployment artifacts.
- Generating release notes.
- Publishing release assets.
- Creating a GitHub Release.
- Deploying a specific version.

A typical automated workflow:

```text
Pull Request merged
        |
        v
CI checks
        |
        v
Release preparation
        |
        v
Version and changelog validation
        |
        v
Build artifacts
        |
        v
Create tag and GitHub Release
        |
        v
Deploy
```

Do not automate publication before you understand the manual release process.

For now, your goal is to understand each stage. We will practice GitHub Actions in the dedicated Actions module.

## 22. GitHub CLI release commands

If GitHub CLI is installed and authenticated, you can manage releases from the terminal.

List releases:

```bash
gh release list
```

View a release:

```bash
gh release view v1.5.0
```

Create a draft release:

```bash
gh release create v1.5.0 \
  --title "v1.5.0" \
  --notes-file RELEASE_NOTES.md \
  --draft
```

Create a prerelease:

```bash
gh release create v1.5.0-beta.1 \
  --title "v1.5.0-beta.1" \
  --notes-file RELEASE_NOTES.md \
  --prerelease
```

Publish a release after reviewing the draft:

```bash
gh release edit v1.5.0 --draft=false
```

Delete a draft release if you intentionally need to discard it:

```bash
gh release delete v1.5.0 --yes
```

Be careful with deletion commands. They change repository release state.

For the full command reference:

https://cli.github.com/manual/gh_release

---

# Part 11 — Practical training exercises

## Exercise A — Audit your release history

Inspect your repository:

```bash
git status
git tag --list
git log --oneline --decorate -n 30
```

Then open the Releases page on GitHub.

Record:

- Existing tags.
- Published releases.
- Draft releases, if any.
- The latest stable version.
- Whether a tag exists without a corresponding release.

Do not create a new tag yet.

## Exercise B — Create CHANGELOG.md

Create or update:

```text
CHANGELOG.md
```

Include:

- Unreleased section.
- Added.
- Changed.
- Fixed.
- Removed.
- Security.
- Existing version history, if applicable.

Do not invent historical release dates or versions.

## Exercise C — Configure generated release notes

Create:

```text
.github/release.yml
```

Use the configuration from Part 4.

Check that the labels in your configuration match the labels you actually use in GitHub.

## Exercise D — Prepare a draft release

Prepare a draft release for a hypothetical next version.

Include:

- Version number.
- Release title.
- Summary.
- Features.
- Fixes.
- Known limitations.
- Upgrade instructions if necessary.

Do not publish it until you have verified that the version and target commit are correct.

## Exercise E — Simulate a hotfix

Follow Part 7.

Your objective is to practice:

- Creating a hotfix branch.
- Making a correction.
- Creating a Conventional Commit.
- Pushing the branch.
- Opening a Pull Request.
- Reviewing and merging it.
- Understanding when a patch release is appropriate.

## Exercise F — Prepare a release plan

Create this file:

```text
docs/github/module-01-code/release-plan-exercise.md
```

Use this template:

```markdown
# Release Plan Exercise

## Release Information

- Project:
- Current version:
- Planned version:
- Release type:
- Target branch:
- Previous release tag:

## Included Features

- [ ] Feature 1
- [ ] Feature 2

## Bug Fixes

- [ ] Fix 1
- [ ] Fix 2

## Breaking Changes

- None

## Documentation

- [ ] CHANGELOG.md updated
- [ ] Upgrade instructions reviewed
- [ ] Release notes prepared

## Validation

- [ ] Tests passed
- [ ] Build passed
- [ ] Code review completed
- [ ] Security checks reviewed

## Publication

- [ ] Git tag created
- [ ] Tag pushed
- [ ] GitHub Release drafted
- [ ] Release notes reviewed
- [ ] Release published

## Post-release

- [ ] Release verified
- [ ] Known issues documented
- [ ] Follow-up Issues created
```

Fill it in using a hypothetical version of your choice. Clearly identify it as an exercise, not a real published release.

## Exercise G — Write a hotfix scenario

Create a short scenario describing:

1. The current stable version.
2. The problem discovered.
3. Why it requires a hotfix.
4. The branch you would create.
5. The fix commit message.
6. The Pull Request base branch.
7. The next patch version.
8. How you would ensure the fix reaches the main development line.

---

# Part 12 — Commit and push your lesson

## 23. Create your lesson branch

First, inspect your current state:

```bash
git status
git branch
```

Update your local `main` branch:

```bash
git switch main
git pull origin main
```

Create the lesson branch:

```bash
git switch -c docs/add-release-engineering-lesson
```

Create the file:

```text
docs/github/module-01-code/lesson-12-release-engineering.md
```

Paste this lesson into it.

Also update:

```text
docs/github/module-01-code/README.md
```

Add Lesson 12 to the module index.

## 24. Review your changes

```bash
git status
git diff
```

Stage the files:

```bash
git add docs/github/module-01-code/lesson-12-release-engineering.md
git add docs/github/module-01-code/README.md
```

Review the staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add release engineering lesson"
```

Push:

```bash
git push -u origin docs/add-release-engineering-lesson
```

Open a Pull Request on GitHub, review it, and merge it into `main`.

After merging:

```bash
git switch main
git pull origin main
git branch -d docs/add-release-engineering-lesson
```

If the remote branch was not automatically deleted, remove it from GitHub or use:

```bash
git push origin --delete docs/add-release-engineering-lesson
```

Only delete the branch after confirming that the Pull Request has been merged.

---

# Part 13 — Lesson completion checklist

## Knowledge

- [ ] I understand the release engineering lifecycle.
- [ ] I can distinguish commits, Pull Requests, tags, changelogs, and releases.
- [ ] I can select an appropriate Semantic Versioning increment.
- [ ] I understand the purpose of `CHANGELOG.md`.
- [ ] I understand generated release notes and `.github/release.yml`.
- [ ] I understand drafts and prereleases.
- [ ] I understand release branches versus trunk-based development.
- [ ] I understand the hotfix workflow.
- [ ] I can connect Issues and Pull Requests to releases.
- [ ] I understand the release readiness checklist.

## Practical work

- [ ] I audited existing tags and releases.
- [ ] I created or updated `CHANGELOG.md`.
- [ ] I configured `.github/release.yml`.
- [ ] I prepared a draft release.
- [ ] I completed the hotfix simulation.
- [ ] I wrote a release plan.
- [ ] I committed and pushed the lesson.
- [ ] I opened and merged the lesson Pull Request.

## Release discipline

- [ ] I never assume a version tag exists without checking.
- [ ] I do not move published version tags casually.
- [ ] I review generated release notes.
- [ ] I document breaking changes.
- [ ] I verify the target commit before publishing.
- [ ] I ensure hotfixes reach all relevant maintained branches.

---

# Official references

1. GitHub — About Releases: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
2. GitHub — Managing Releases: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository
3. GitHub — Automatically Generated Release Notes: https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes
4. GitHub — REST API for Releases: https://docs.github.com/en/rest/releases/releases
5. GitHub CLI — Release Commands: https://cli.github.com/manual/gh_release
6. Keep a Changelog: https://keepachangelog.com/en/1.1.0/
7. Semantic Versioning: https://semver.org/

---

# Expected result

At the end of this lesson, your repository should have:

```text
github-deep-dive-training/
│
├── .github/
│   └── release.yml
│
├── CHANGELOG.md
│
└── docs/
    └── github/
        └── module-01-code/
            ├── README.md
            ├── lesson-01-repository-basics.md
            ├── lesson-02-branches.md
            ├── lesson-03-commits-and-history.md
            ├── lesson-04-comparing-branches.md
            ├── lesson-05-tags-and-releases.md
            ├── lesson-06-repository-standards.md
            ├── lesson-08-pull-request-collaboration.md
            ├── lesson-10-issues-and-project-planning.md
            ├── lesson-11-github-discussions-and-community-collaboration.md
            ├── lesson-12-release-engineering.md
            └── release-plan-exercise.md
```

This is an illustrative structure. Keep all other lesson files you have already created, including lessons not shown in this shortened tree.

**Next lesson:** Lesson 13 — Repository Code Management: Git LFS, `.gitignore`, `.gitattributes`, and handling large or generated files.
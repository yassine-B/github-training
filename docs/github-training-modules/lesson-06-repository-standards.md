

# Lesson 06 — Repository Documentation and Collaboration Standards

**Module:** 01 — Code  
**Difficulty:** Beginner to Intermediate  
**Repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By completing this lesson, you should understand how to:

- Create a professional repository README.
- Choose and configure an open-source license.
- Write contribution guidelines.
- Establish a Code of Conduct.
- Create a security policy.
- Configure GitHub Issue Forms.
- Create a Pull Request template.
- Organize repository documentation.
- Understand GitHub Community Standards.
- Maintain repository standards as a project evolves.

## 2. Why repository standards matter

A GitHub repository is more than a place to store source code.

A professional repository should explain:

- What the project does.
- How to install or use it.
- How other developers can contribute.
- What license applies to the project.
- How to report problems.
- How security issues should be handled.
- What information is required when submitting changes.

Without these documents, contributors may not understand how to work with the project.

Repository standards make collaboration more consistent and reduce misunderstandings.

## 3. README.md

### Purpose

The README is usually the first document people see when opening a repository.

It should answer these questions:

1. What is this project?
2. Why does it exist?
3. What does it provide?
4. How do I get started?
5. Where can I find more information?
6. How can I contribute?

### Recommended sections

| Section | Purpose |
|---|---|
| Project title | Identify the repository |
| Description | Explain what it does |
| Features | Summarize important capabilities |
| Screenshots | Show the application, when relevant |
| Requirements | List prerequisites |
| Installation | Explain setup |
| Usage | Explain how to use it |
| Project structure | Explain the directories |
| Contributing | Link to contribution instructions |
| License | Explain licensing |
| Contact | Identify maintainers or support channels |

### Markdown commands and syntax

Headings:

```markdown
# Main heading
## Section heading
### Subsection heading
```

Links:

```markdown
[GitHub Documentation](https://docs.github.com/)
```

Images:

```markdown
![Application screenshot](docs/images/dashboard.png)
```

Code blocks:

````markdown
```bash
git clone https://github.com/username/project.git
cd project
```
````

Tables:

```markdown
| Command | Purpose |
|---|---|
| git status | Show working tree status |
| git branch | List branches |
```

Task lists:

```markdown
- [x] Create repository
- [x] Add README
- [ ] Add CI workflow
```

### Exercise

1. Open your repository.
2. Create or update `README.md`.
3. Add a project description.
4. Add the training modules table.
5. Add repository setup instructions.
6. Add links to your contribution and security policies.
7. Preview the Markdown in VS Code.

In VS Code, use:

```text
Ctrl + Shift + V
```

to open the Markdown preview.

---

## 4. LICENSE

### Purpose

A license defines what other people are allowed to do with your work.

Without an explicit license, people generally do not automatically receive permission to reuse, modify, or redistribute your copyrighted material.

### Common open-source licenses

| License | Main characteristics |
|---|---|
| MIT | Permissive; allows broad reuse with license notice preservation |
| Apache 2.0 | Permissive; includes express patent-related provisions |
| GPL-3.0 | Copyleft; distributed derivative works must comply with its terms |
| BSD 2-Clause | Permissive with relatively simple conditions |
| BSD 3-Clause | Similar to BSD 2-Clause, with an additional non-endorsement condition |

### Choosing a license

For a small educational repository, MIT is a straightforward option if you want others to reuse and adapt the material under its terms.

For software that requires stronger sharing obligations, you may consider GPL-3.0.

For projects requiring explicit patent provisions, consider Apache-2.0.

Read the full license before choosing it. A license is a legal permission, not just a GitHub configuration.

### Exercise

1. Create a file named `LICENSE`.
2. Add the chosen license text.
3. Replace the copyright holder placeholder.
4. Commit the file.
5. Open the repository on GitHub.
6. Check whether GitHub recognizes the license.

---

## 5. CONTRIBUTING.md

### Purpose

This document explains how contributors should work with your repository.

It should define:

- Branch naming.
- Commit message conventions.
- Development workflow.
- Pull Request requirements.
- Documentation standards.
- Review expectations.

### Recommended workflow

```text
Update main
    |
    v
Create feature branch
    |
    v
Make changes
    |
    v
Review changes
    |
    v
Create commits
    |
    v
Push branch
    |
    v
Open Pull Request
    |
    v
Review and corrections
    |
    v
Merge
```

### Important Git commands

Update your local main branch:

```bash
git switch main
git pull origin main
```

- `git switch main`: switches to the local main branch.
- `git pull origin main`: fetches and integrates changes from the remote main branch.

Create a branch:

```bash
git switch -c docs/improve-readme
```

- `git switch`: changes branches.
- `-c`: creates a new branch and switches to it.
- `docs/improve-readme`: branch name.

Inspect changes:

```bash
git status
git diff
```

Stage changes:

```bash
git add README.md CONTRIBUTING.md
```

Inspect staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(repo): improve repository documentation"
```

Push:

```bash
git push -u origin docs/improve-readme
```

The `-u` option sets the upstream tracking branch, so later you can usually use:

```bash
git push
git pull
```

without specifying the remote and branch every time.

### Exercise

Create a branch:

```bash
git switch main
git pull origin main
git switch -c docs/add-contributing-guidelines
```

Create `CONTRIBUTING.md`.

Add the contribution rules.

Commit:

```bash
git add CONTRIBUTING.md
git commit -m "docs(repo): add contributing guidelines"
```

Push:

```bash
git push -u origin docs/add-contributing-guidelines
```

Open a Pull Request and merge it after reviewing the changes.

---

## 6. CODE_OF_CONDUCT.md

### Purpose

A Code of Conduct establishes expected behaviour for contributors.

It helps create a respectful environment and explains how unacceptable behaviour should be handled.

It should define:

- Expected behaviour.
- Unacceptable behaviour.
- Reporting procedures.
- Maintainer responsibilities.
- Possible enforcement actions.

### Example expected behaviour

- Respect other contributors.
- Provide constructive feedback.
- Avoid personal attacks.
- Explain technical disagreements professionally.
- Welcome questions from beginners.
- Focus on improving the project.

### Exercise

Create `CODE_OF_CONDUCT.md`.

Add the project's behavioural expectations and reporting procedure.

Commit:

```bash
git add CODE_OF_CONDUCT.md
git commit -m "docs(repo): add code of conduct"
```

---

## 7. SECURITY.md

### Purpose

A security policy tells people how to report vulnerabilities.

For example, imagine someone discovers that a project accidentally exposes an API token.

Publishing that token in a public Issue would make the situation worse.

A security policy should direct people toward private reporting.

### Recommended sections

1. Supported versions.
2. How to report a vulnerability.
3. What information to include.
4. What information must not be published.
5. Expected response process.

### GitHub private vulnerability reporting

If enabled for the repository, GitHub provides a private reporting mechanism.

Typical navigation:

```text
Repository
    |
    v
Security
    |
    v
Report a vulnerability
```

Availability and configuration depend on repository settings and GitHub's current feature support.

### Exercise

1. Create `SECURITY.md`.
2. Define the reporting procedure.
3. Explain what information a report should contain.
4. Open the repository's Security tab.
5. Inspect the available security features.

Never use real credentials in training exercises.

---

## 8. GitHub Issue Templates

### Purpose

Issue templates standardize how contributors report bugs and request features.

Without templates, reports may lack important details.

For example, a bug report should ideally include:

- Affected lesson or file.
- Problem description.
- Expected result.
- Steps to reproduce.
- Environment information.

### Two ways to create Issue templates

GitHub supports traditional Markdown templates and structured Issue Forms.

For this training repository, use Issue Forms because they provide structured fields.

### Folder structure

```text
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.yml
    ├── feature_request.yml
    └── config.yml
```

### Understanding Issue Form properties

Example:

```yaml
name: Bug report
description: Report an error or incorrect example.
title: "[BUG]: "
labels:
  - bug
body:
  - type: textarea
    id: description
    attributes:
      label: Describe the problem
      placeholder: Explain what happened.
    validations:
      required: true
```

Explanation:

| Property | Purpose |
|---|---|
| `name` | Template name |
| `description` | Short explanation |
| `title` | Default Issue title |
| `labels` | Labels automatically applied |
| `body` | Form fields |
| `type` | Field type |
| `id` | Unique field identifier |
| `attributes` | Field configuration |
| `validations` | Validation rules |
| `required` | Whether the field is mandatory |

Common field types include:

- `markdown`
- `input`
- `textarea`
- `dropdown`
- `checkboxes`

### Exercise

Create:

```text
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/ISSUE_TEMPLATE/config.yml
```

Add the provided templates.

Commit:

```bash
git add .github/ISSUE_TEMPLATE/
git commit -m "docs(github): add issue form templates"
```

Push your branch and merge the Pull Request.

### Verify on GitHub

1. Open your repository.
2. Select **Issues**.
3. Select **New issue**.
4. Confirm that the templates appear.
5. Open each template.
6. Verify that required fields work as expected.

---

## 9. Pull Request template

### Purpose

A Pull Request template helps contributors explain their changes consistently.

A useful template asks:

- What changed?
- Why was it changed?
- Which Issue does it resolve?
- What type of change is this?
- How was it tested?
- Are there screenshots or additional notes?

### Location

```text
.github/
└── PULL_REQUEST_TEMPLATE.md
```

GitHub automatically uses this template when someone creates a Pull Request.

### Exercise

Create:

```text
.github/PULL_REQUEST_TEMPLATE.md
```

Add the provided template.

Commit:

```bash
git add .github/PULL_REQUEST_TEMPLATE.md
git commit -m "docs(github): add pull request template"
```

Push your branch and merge the Pull Request.

### Verify

Create a small test branch and open a Pull Request.

Confirm that the template appears automatically.

You can close the test Pull Request if it is not needed.

---

## 10. FUNDING.yml

### Purpose

This file configures sponsorship links for repositories.

Location:

```text
.github/FUNDING.yml
```

Example:

```yaml
github: [YOUR_GITHUB_USERNAME]
```

Other supported funding platforms may also be configured.

Only add this file when you have a real sponsorship account and want to display sponsorship options.

### Exercise

For this training repository, you can skip this file unless you intend to accept sponsorships.

---

## 11. Recommended repository structure

A clean repository structure makes it easier to maintain and expand the project.

Example:

```text
github-deep-dive-training/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   └── config.yml
│   │
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docs/
│   └── github/
│       ├── module-01-code/
│       │   ├── README.md
│       │   ├── lesson-01-repository-basics.md
│       │   ├── lesson-02-branches.md
│       │   ├── lesson-03-commits-and-history.md
│       │   ├── lesson-04-comparing-branches.md
│       │   ├── lesson-05-tags-and-releases.md
│       │   └── lesson-06-repository-standards.md
│       │
│       └── module-02-issues/
│
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

As you add modules, create separate directories for them.

Avoid putting every document in the repository root.

---

## 12. GitHub Community Standards

GitHub has a Community Standards area that helps repository owners identify missing community health files.

Typical standards include:

| Standard | Related file or feature |
|---|---|
| Description | Repository description |
| README | `README.md` |
| License | `LICENSE` |
| Contributing guidelines | `CONTRIBUTING.md` |
| Code of Conduct | `CODE_OF_CONDUCT.md` |
| Issue templates | `.github/ISSUE_TEMPLATE/` |
| Pull Request template | `.github/PULL_REQUEST_TEMPLATE.md` |

### How to inspect Community Standards

1. Open your repository on GitHub.
2. Select the **Insights** tab.
3. Find **Community Standards**.
4. Review the checklist.
5. Identify missing files.
6. Add the missing files.

The exact interface and navigation may change.

### Exercise

Open the Community Standards page.

Verify that GitHub recognizes your repository files.

Fix any missing items that are relevant to this repository.

---

## 13. Practical project exercise

Your task is to prepare `github-deep-dive-training` as a repository that another developer can understand and contribute to.

### Step 1 — Inspect the repository

```bash
git status
git branch -a
git tag
```

Explanation:

- `git status`: checks your current working tree.
- `git branch -a`: lists local and remote branches.
- `git tag`: lists local tags.

Do not assume a tag exists just because it was discussed in an earlier lesson.

### Step 2 — Create a working branch

```bash
git switch main
git pull origin main
git switch -c docs/add-repository-standards
```

### Step 3 — Create the files

Create the following:

```text
README.md
LICENSE
CONTRIBUTING.md
CODE_OF_CONDUCT.md
SECURITY.md
.github/ISSUE_TEMPLATE/bug_report.yml
.github/ISSUE_TEMPLATE/feature_request.yml
.github/ISSUE_TEMPLATE/config.yml
.github/PULL_REQUEST_TEMPLATE.md
```

### Step 4 — Review the changes

```bash
git status
git diff
```

If some files are untracked, `git diff` will not show their contents yet. Use:

```bash
git status --short
```

to inspect the untracked file list.

### Step 5 — Stage the files

```bash
git add README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md
git add .github/
```

### Step 6 — Inspect staged changes

```bash
git diff --cached
```

Make sure you did not accidentally include:

- Personal access tokens.
- Passwords.
- Private keys.
- Local environment files.
- Unrelated files.

### Step 7 — Commit

```bash
git commit -m "docs(repo): add repository standards and templates"
```

### Step 8 — Push

```bash
git push -u origin docs/add-repository-standards
```

### Step 9 — Create a Pull Request

On GitHub:

1. Open the repository.
2. Select **Pull requests**.
3. Select **New pull request**.
4. Choose `main` as the base branch.
5. Choose `docs/add-repository-standards` as the compare branch.
6. Review the changes.
7. Create the Pull Request.
8. Check that the Pull Request template appears.
9. Merge after reviewing.

### Step 10 — Verify the repository

After merging:

- Check the README on the repository home page.
- Check that GitHub recognizes the license.
- Open the Issue creation page.
- Verify both Issue Forms.
- Create a test Pull Request to inspect its template.
- Inspect Community Standards.
- Check that the security and contribution documents are visible.

---

## 14. Troubleshooting

### GitHub does not display my Issue Form

Check:

- The file is inside `.github/ISSUE_TEMPLATE/`.
- The extension is `.yml` or `.yaml`.
- The YAML indentation is correct.
- Required fields have valid identifiers.
- The changes have been pushed to the default branch.

### Pull Request template does not appear

Check:

- The filename is exactly `PULL_REQUEST_TEMPLATE.md`.
- It is inside `.github/`.
- It exists on the repository's default branch.

GitHub also supports other template locations and configurations, but use this standard location for this exercise.

### Git does not show my new file in `git diff`

New untracked files are not shown by `git diff` by default.

Use:

```bash
git status
```

After staging them:

```bash
git add README.md
git diff --cached
```

### Git says there is nothing to commit

Check:

```bash
git status
```

Possible reasons:

- The file was not saved.
- No changes were made.
- The changes were already committed.
- You are working in a different repository or branch.

### GitHub does not recognize my license

Check that:

- The file is named `LICENSE` or `LICENSE.md`.
- It contains a recognized license text.
- The file is committed and pushed.

---

## 15. Completion checklist

### Repository documentation

- [ ] README.md created or updated.
- [ ] LICENSE added and copyright holder configured.
- [ ] CONTRIBUTING.md added.
- [ ] CODE_OF_CONDUCT.md added.
- [ ] SECURITY.md added.

### GitHub templates

- [ ] Bug report Issue Form created.
- [ ] Feature request Issue Form created.
- [ ] Issue template configuration created.
- [ ] Pull Request template created.
- [ ] Templates verified on GitHub.

### Git workflow

- [ ] Created a documentation branch.
- [ ] Reviewed all changes.
- [ ] Used a Conventional Commit message.
- [ ] Pushed the branch.
- [ ] Created a Pull Request.
- [ ] Reviewed and merged the Pull Request.

### Repository verification

- [ ] README visible on repository home page.
- [ ] License recognized by GitHub.
- [ ] Community Standards inspected.
- [ ] Issue templates available.
- [ ] Pull Request template available.

---

## 16. Recommended commit messages

Use these examples when you prefer to split the work into smaller commits:

```bash
git commit -m "docs(repo): improve repository readme"
git commit -m "docs(repo): add mit license"
git commit -m "docs(repo): add contributing guidelines"
git commit -m "docs(repo): add code of conduct"
git commit -m "docs(repo): add security policy"
git commit -m "docs(github): add issue form templates"
git commit -m "docs(github): add pull request template"
```

Alternatively, one commit for the entire set of standards is acceptable:

```bash
git commit -m "docs(repo): add repository standards and templates"
```

---

## 17. Tags and releases

Continue using the tag and release strategy established in Lesson 5.

Do not create a release for every lesson.

A suitable milestone is the completion of Module 1, after its lessons and practical exercises are complete.

Before creating a release:

```bash
git status
git log --oneline -10
git tag
```

Confirm that the working tree is clean, the milestone changes are merged, and the intended version tag does not already exist.

Prepare a changelog describing the completed module, then create and publish the appropriate release according to your versioning plan.

Do not recreate or move an already-published tag.

---

## 18. What comes next?

In Lesson 7, we will study **Repository Settings and Access Management**.

Topics include:

- Repository visibility: public, private, and internal.
- Collaborators and repository permissions.
- Read, Write, Maintain, Triage, and Admin roles.
- Default branch configuration.
- Branch protection rules.
- Repository rulesets.
- Pull Request merge strategies.
- Repository security settings.
- Managing access safely.


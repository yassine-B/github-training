# Lesson 1 — Repository Basics and the Code Tab

## 1. Learning objectives

By the end of this lesson, you should understand:

- What a Git repository is.
- The difference between Git and GitHub.
- How to create and clone a repository.
- How to configure Git.
- How to inspect repository status.
- How to create, modify, stage, and commit files.
- How to push changes to GitHub.
- The main sections of the GitHub Code tab.

## 2. Git vs GitHub

### Git

Git is a distributed version control system.

It tracks changes in your project and allows you to:

- Record project history.
- Compare versions.
- Create branches.
- Restore previous versions.
- Collaborate with other developers.

### GitHub

GitHub is a hosting and collaboration platform built around Git.

It provides:

- Remote repositories.
- Pull requests.
- Issues.
- Actions.
- Projects.
- Security tools.
- Code review.
- Releases.

Git works locally on your computer. GitHub hosts remote repositories and provides collaboration features.

## 3. Install and verify Git

Check whether Git is installed:

```bash
git --version
```

Example output:

```text
git version 2.x.x
```

If Git is not installed, download it from:

https://git-scm.com/downloads

## 4. Configure Git

Configure your author information:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

These values are used as the author information in your commits.

Inspect your configuration:

```bash
git config --global --list
```

Get one specific value:

```bash
git config --global user.name
git config --global user.email
```

The `--global` option applies the configuration to all repositories for your operating-system user.

You can override these values inside an individual repository by running the commands without `--global`.

## 5. Create a GitHub repository

Create a repository on GitHub:

1. Open GitHub.
2. Select New repository.
3. Enter the repository name.
4. Choose Public or Private.
5. Add a README if appropriate.
6. Create the repository.

For this training, use:

```text
github-deep-dive-training
```

## 6. Clone the repository

Cloning downloads a remote repository to your computer.

```bash
git clone https://github.com/USERNAME/github-deep-dive-training.git
```

Move into the project:

```bash
cd github-deep-dive-training
```

Open it in VS Code:

```bash
code .
```

The `code .` command opens the current directory in Visual Studio Code.

## 7. Understand the local repository

A Git repository contains a hidden `.git` directory.

It stores Git metadata, including:

- Commit history.
- Branch references.
- Repository configuration.
- Object database.
- Remote information.

Do not manually modify `.git` unless you know exactly what you are doing.

## 8. Inspect repository status

```bash
git status
```

This command displays:

- The current branch.
- Files that are modified.
- Files that are untracked.
- Files staged for commit.
- Whether the local branch is synchronized with its upstream branch.

Use it frequently.

## 9. Create a project file

Create a directory:

```bash
mkdir docs
```

Create a Markdown file inside it:

```text
docs/project-overview.md
```

Example content:

```markdown
# Project Overview

This repository is used to learn Git and GitHub.

## Topics

- Repositories
- Branches
- Commits
- Pull Requests
- GitHub Actions
```

## 10. Stage changes

Git has three important areas:

1. Working directory: files you are editing.
2. Staging area: changes selected for the next commit.
3. Repository: committed project history.

Stage one file:

```bash
git add docs/project-overview.md
```

Stage all changes:

```bash
git add .
```

Check the result:

```bash
git status
```

## 11. Create a commit

A commit records a snapshot of staged changes.

```bash
git commit -m "docs: add project overview"
```

A commit includes:

- A unique identifier.
- Author information.
- Date.
- Commit message.
- References to the project snapshot.

## 12. Push changes to GitHub

```bash
git push
```

If the branch does not yet have an upstream configured:

```bash
git push -u origin BRANCH_NAME
```

The `-u` option establishes the upstream relationship so future pushes can usually use `git push`.

## 13. Understand the GitHub Code tab

The Code tab is the main interface for browsing repository contents.

Important elements include:

### Repository files

Browse directories and files.

### Branch selector

Switch between available branches to inspect their contents.

### Commits

View the history of changes.

### README

GitHub displays the README on the repository homepage.

### Releases

View published versions of the project.

### Tags

View named references to specific commits.

### Repository navigation

Other important repository tabs include:

- Issues
- Pull requests
- Actions
- Projects
- Wiki
- Security
- Insights
- Settings

## 14. Important commands reference

| Command | Purpose |
|---|---|
| `git --version` | Check Git version |
| `git config --global --list` | Display global configuration |
| `git clone URL` | Clone a repository |
| `cd DIRECTORY` | Change directory |
| `code .` | Open current directory in VS Code |
| `git status` | Inspect working tree |
| `git add FILE` | Stage a file |
| `git add .` | Stage all changes |
| `git commit -m "MESSAGE"` | Create a commit |
| `git push` | Push commits |
| `git remote -v` | Display remote URLs |

## 15. Practical exercise

Using your `github-deep-dive-training` repository:

1. Create `docs/project-overview.md`.
2. Add a short project description.
3. Run `git status`.
4. Stage the file.
5. Inspect the staged changes.
6. Commit the file.
7. Push the commit to GitHub.
8. Open GitHub and verify that the file is visible.

Useful commands:

```bash
git status
git add docs/project-overview.md
git diff --cached
git commit -m "docs: add project overview"
git push
```

## 16. Completion checklist

- [ ] Git is installed.
- [ ] Git identity is configured.
- [ ] GitHub repository is created.
- [ ] Repository is cloned locally.
- [ ] VS Code opens the repository.
- [ ] A Markdown file is created.
- [ ] Changes are staged.
- [ ] A commit is created.
- [ ] Changes are pushed.
- [ ] The file is visible on GitHub.

## 17. What comes next?

Lesson 2 covers Git branches, including creating branches, switching between branches, renaming branches, deleting branches, and understanding local versus remote branches.

# Getting Started

This guide explains how to set up the GitHub Deep Dive
Training repository and begin working through its lessons.

## 1. Prerequisites

Before starting, install the following tools:

| Tool | Purpose |
| --- | --- |
| Git | Version control |
| GitHub Account | Repository hosting and collaboration |
| GitHub CLI | Interacting with GitHub from the terminal |
| VS Code | Code editor |
| Python | Required for documentation development |
| PowerShell | Windows terminal |

Some lessons require additional tools. Their installation
instructions will be provided within the relevant lessons.

## 2. Clone the Repository

Open PowerShell and execute:

```powershell
git clone https://github.com/yassine-b/github-training.git

cd github-training
```

## 3. Understand the Directory Structure

The repository is organized into the following main directories:

### docs/

Contains the training documentation and technical guides.

- `index.md`: Documentation homepage.
- `getting-started.md`: Onboarding guide.
- `git-and-github-guides/`: Supplementary Git and GitHub guides.
- `github-training-modules/`: Structured course lessons.

### examples/

Contains practical code examples and demonstration workflows.

### exercises/

Contains hands-on exercises that help reinforce the lessons.

### .github/

Contains GitHub-specific configuration:

- Issue templates.
- Pull request templates.
- CODEOWNERS.
- Dependabot configuration.
- GitHub Actions workflows.

## 4. Follow the Learning Path

We recommend following the lessons in numerical order.

For every lesson:

1. Read the explanation.
2. Understand the GitHub concepts.
3. Follow the examples.
4. Execute the commands in your own practice repository.
5. Complete the associated exercises.
6. Review your results.

Do not execute unfamiliar Git commands on important
repositories without understanding their effects.

## 5. Practice with Git

Create a dedicated local practice directory:

```powershell
mkdir github-practice

cd github-practice

git init
```

Configure your Git identity:

```powershell
git config --global user.name "Your Name"

git config --global user.email "YOUR_EMAIL"
```

Verify your configuration:

```powershell
git config --list
```

Use this practice repository to experiment with:

- Branches.
- Commits.
- Merges.
- Rebases.
- Tags.
- Conflicts.
- Recovery operations.

## 6. Explore the Examples

The examples directory contains practical demonstrations.

For example:

```text
examples/
├── git-hooks-workflow/
├── issues-and-projects-workflow/
├── pull-request-workflow/
├── releases-workflow/
├── submodules-workflow/
└── worktrees-workflow/
```

Explore the README and Markdown instructions inside
each example directory before executing its code.

## 7. Run the Documentation Website Locally

If you want to contribute to the documentation website,
install Python and create a virtual environment.

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements-docs.txt
```

Start the local documentation server:

```powershell
mkdocs serve
```

Open:

<http://127.0.0.1:8000>

Build the documentation:

```powershell
mkdocs build --strict
```

## 8. Contribute Changes

If you want to contribute to the repository:

1. Update your local `main` branch.
2. Create a feature branch.
3. Make your changes.
4. Run relevant checks.
5. Commit your changes.
6. Push your branch.
7. Open a pull request.

Example:

```powershell
git switch main

git pull origin main

git switch -c feature/my-contribution
```

## 9. Track Your Progress

Maintain your learning progress by recording:

- Completed lessons.
- Completed exercises.
- Git commands practiced.
- Concepts that need revision.
- Problems encountered.
- Projects completed.

The goal is not simply to read the lessons.

The goal is to apply Git and GitHub concepts in practical
development workflows.

## 10. Troubleshooting

### Git is not recognized

Verify that Git is installed and available in your PATH.

### MkDocs is not recognized

Activate your Python virtual environment and install
the dependencies again.

### Documentation build fails

Execute:

```powershell
mkdocs build --strict
```

Read the reported errors and check:

- Missing Markdown files.
- Invalid navigation paths.
- Broken internal links.
- Invalid MkDocs configuration.

### GitHub Pages is not updating

Check:

1. Repository Settings > Pages.
2. GitHub Actions workflow status.
3. Deployment permissions.
4. The latest successful deployment.

---

## Next Step

Continue with:

[Lesson 01 — Repository Basics](github-training-modules/lesson-01-repository-basics.md)

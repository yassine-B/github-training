

# Contributing Guidelines

Thank you for considering contributing to GitHub Deep Dive Training.

This repository is intended to provide accurate, practical, and maintainable training material. Contributions should improve the clarity, correctness, or practical value of the lessons.

## 1. Ways to contribute

You can contribute by:

- Correcting technical mistakes.
- Improving explanations.
- Adding practical examples.
- Adding Git or GitHub command explanations.
- Improving exercises and expected results.
- Reporting outdated GitHub features.
- Fixing spelling and grammar.
- Suggesting new lessons or topics.

## 2. Before making changes

1. Check the existing Issues to see whether the problem has already been reported.
2. For substantial changes, open an Issue first to discuss the proposal.
3. Keep changes focused on one topic whenever possible.

## 3. Branch naming

Use descriptive branch names with a category prefix.

Examples:

```text
docs/improve-branching-lesson
docs/add-github-actions-examples
fix/correct-git-command-example
feat/add-security-exercise
```

Recommended prefixes:

| Prefix | Purpose |
|---|---|
| `feat/` | New functionality or training material |
| `fix/` | Corrections and fixes |
| `docs/` | Documentation changes |
| `refactor/` | Restructuring without changing meaning |
| `test/` | Adding or improving exercises and validation |
| `chore/` | Maintenance tasks |

## 4. Local development workflow

Update your local `main` branch:

```bash
git switch main
git pull origin main
```

Create a new branch:

```bash
git switch -c docs/improve-branching-lesson
```

Check your current branch and working tree:

```bash
git status
git branch --show-current
```

Make your changes, then inspect them:

```bash
git diff
```

Stage the intended files:

```bash
git add docs/github/module-01-code/
```

Review what is staged:

```bash
git diff --cached
```

Commit your changes:

```bash
git commit -m "docs(github): improve branching lesson"
```

Push the branch:

```bash
git push -u origin docs/improve-branching-lesson
```

Open a Pull Request on GitHub.

## 5. Commit message convention

Use Conventional Commits.

Format:

```text
<type>(<scope>): <description>
```

Examples:

```text
docs(github): add branching lesson
docs(github): improve release instructions
fix(git): correct branch comparison example
feat(training): add GitHub Actions exercise
chore(repo): update contribution guidelines
```

Keep the description clear and concise. Use the imperative mood where practical.

## 6. Documentation standards

When adding or modifying a lesson:

- Use Markdown.
- Give the lesson a descriptive title.
- Explain concepts before introducing exercises.
- Explain what each command does.
- Include realistic command examples.
- Explain important options and arguments.
- Show expected results when useful.
- Mention risks for destructive commands.
- Include troubleshooting guidance.
- Add a completion checklist.
- Update the module README when adding a lesson.

Use fenced code blocks with language identifiers:

```bash
git status
```

For terminal output:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## 7. Pull Request requirements

A Pull Request should:

- Have a descriptive title.
- Explain what changed.
- Explain why the change is needed.
- Reference the related Issue when applicable.
- Include screenshots when they genuinely help explain a change.
- Have no unrelated modifications.
- Be checked for spelling, formatting, and technical accuracy.

Use the repository Pull Request template.

## 8. Review process

Before merging:

1. Check that the change matches its stated purpose.
2. Review the complete diff.
3. Verify all commands and examples.
4. Check links and file paths.
5. Confirm that the documentation remains understandable.
6. Address review comments.
7. Merge only after the required checks and reviews are complete.

## 9. Documentation accuracy

GitHub features can change over time.

When documenting a GitHub feature:

- Prefer official GitHub documentation.
- Include the relevant feature name and navigation path.
- Avoid presenting an old interface as the only available interface.
- Clearly distinguish Git commands from GitHub web-interface actions.
- Mention when a feature depends on a plan or repository configuration.

## 10. Security

Never commit:

- Passwords.
- Personal access tokens.
- Private keys.
- API secrets.
- Database credentials.
- Private customer information.

Report security vulnerabilities according to `SECURITY.md`.

## 11. Code of conduct

All contributors must follow `CODE_OF_CONDUCT.md`.

## 12. Questions

For questions or suggestions, open a GitHub Issue with enough information for maintainers to understand the request.

Thank you for helping improve this training repository.


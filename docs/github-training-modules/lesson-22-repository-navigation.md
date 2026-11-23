# Module 1 — Code

## Lesson 22: Repository Navigation — Files, Directories, Symbols, and File History

**Level:** Advanced GitHub
**Type:** Practical lesson

## 1. Overview

Repository navigation is the process of exploring a repository's files, directories, symbols, and history to understand how a project is structured and how its implementation has evolved.

GitHub provides browser-based tools that let developers investigate repositories without cloning them first.

In this lesson, you will learn how to:

- Navigate repository directories.
- Find files using the file finder.
- Use GitHub keyboard shortcuts.
- Inspect file contents and historical versions.
- Investigate file history.
- Use GitHub Blame.
- Create permanent links to files and code lines.
- Navigate symbols and references.
- Perform similar investigations using Git CLI.

**Training repository:** `github-deep-dive-training`

## 2. Repository navigation fundamentals

The repository's Code tab provides access to tracked files and directories.

A typical project structure might look like:

```text
project/
├── backend/
│   ├── accounts/
│   ├── orders/
│   └── config/
├── frontend/
│   └── src/
├── docs/
├── tests/
├── README.md
└── pyproject.toml
```

A repository path identifies the location of a file:

```text
backend/accounts/models.py
```

GitHub uses two important URL patterns:

```text
/blob/BRANCH/path/to/file
/tree/BRANCH/path/to/directory
```

- `blob` displays a file.
- `tree` displays a directory.

The branch or commit reference identifies the version being viewed.

## 3. Navigating files and directories

To navigate a repository:

1. Open the repository.
2. Select the Code tab.
3. Open a directory.
4. Continue through nested directories.
5. Select a file to inspect it.
6. Use the breadcrumb navigation to return to a parent directory.

When investigating a repository, pay attention to:

- Directory organization.
- Application boundaries.
- Configuration files.
- Tests.
- Documentation.
- Build and deployment files.

Do not assume every repository follows the same directory structure.

## 4. Using the file finder

GitHub provides a file finder for locating files and directories.

From the repository's Code tab:

1. Press `t`.
2. Enter a filename or part of a path.
3. Select the matching result.

Examples:

```text
settings.py
LoginForm.tsx
authentication
README.md
```

The file finder excludes some directories by default, including common generated or temporary directories such as `build`, `tmp`, and `vendor`.

If a file cannot be found, use GitHub Code Search with an appropriate `path:` qualifier.

## 5. Keyboard shortcuts

Press `?` on GitHub to display the available shortcuts.

| Shortcut | Action |
| --- | --- |
| `t` | Open the file finder |
| `l` | Jump to a line in a code file |
| `w` | Switch branch or tag |
| `y` | Convert a file URL to a permanent link |
| `b` | Open Blame |
| `?` | Display keyboard shortcuts |

Shortcuts can vary depending on the current page and interface context.

## 6. Viewing files and historical versions

GitHub's file view provides syntax-highlighted content, line numbers, and navigation options.

### 6.1 Raw view

Select **Raw** to view the original file content without the normal GitHub formatting.

This is useful when copying or inspecting the exact file contents.

### 6.2 Viewing a file at a branch or tag

Use the branch selector to select a branch or tag before opening a file.

You can also inspect a file at a specific commit:

```text
https://github.com/OWNER/REPOSITORY/blob/COMMIT_SHA/path/to/file
```

### 6.3 Branch URLs versus commit URLs

A branch-based URL points to the branch's current version. Its content can change when new commits are pushed.

A commit-based URL identifies a specific version of the file.

Use commit-based URLs when documenting historical code or sharing an exact implementation.

## 7. Understanding file history

Open a file and select its **History** option to inspect commits associated with that file.

File history can help identify:

- Relevant commits.
- Authors.
- Commit dates.
- Commit messages.
- The evolution of a file.

To investigate a change:

1. Open the file history.
2. Select a relevant commit.
3. Inspect the commit details.
4. Review the diff.
5. Inspect other files changed in the same commit.
6. Open the historical file version if necessary.

Do not rely exclusively on commit messages. Inspect the actual changes.

### Different history views

| View | Purpose |
| --- | --- |
| Repository history | Investigate commits across the repository |
| File history | Investigate commits associated with a file |
| Blame | Identify the last modifying revision for each current line |
| Commit diff | Inspect the actual changes in a commit |

## 8. GitHub Blame

Blame displays line-by-line revision information for a file.

To open it:

1. Open a code file.
2. Select **Blame**, or press `b`.
3. Inspect the commit information associated with each line.
4. Select a commit to investigate its changes.

Blame is useful when:

- Investigating a bug.
- Understanding why a line changed.
- Identifying a relevant commit.
- Finding the history behind an implementation.

Blame identifies the revision that last modified a line. It does not necessarily identify the original designer or explain the reason for the change.

### Ignoring formatting commits

A repository can use `.git-blame-ignore-revs` to exclude selected commits from blame investigations.

Example:

```text
## .git-blame-ignore-revs

## Repository-wide formatting
<FORMATTING_COMMIT_SHA>

## Large automated migration
<MIGRATION_COMMIT_SHA>
```

Replace the placeholders with actual commit hashes.

Git can use this file locally:

```bash
git blame --ignore-revs-file .git-blame-ignore-revs path/to/file
```

Configure it as the default for the repository:

```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

## 9. Permanent links

A normal branch-based file URL can display different content in the future.

To create a permanent link:

1. Open the file at the version you want to reference.
2. Press `y`.
3. Copy the updated URL.

GitHub replaces the branch reference with a specific commit identifier.

### 9.1 Link to a line

A line-specific URL can contain:

```text
#L42
```

### 9.2 Link to a range of lines

A line-range URL can contain:

```text
#L42-L55
```

Example structure:

```text
https://github.com/OWNER/REPOSITORY/blob/COMMIT_SHA/path/to/file.py#L42-L55
```

Use the actual permalink generated by GitHub.

Permanent links are useful in:

- Pull request reviews.
- Bug reports.
- Technical documentation.
- Architecture discussions.
- Issue descriptions.
- Code investigation reports.

## 10. Code navigation: definitions and references

GitHub supports code navigation for several programming languages.

It can help developers:

- Jump from a function or method call to its definition.
- Find references to a symbol.
- Explore relationships between code elements.

Example:

```python
class OrderService:
    def create_order(self, customer, items):
        return Order.objects.create(customer=customer)
```

Possible symbols include:

```text
OrderService
create_order
```

When supported, clicking a symbol can display its definition and references.

Supported languages include Python, JavaScript, TypeScript, JSX, Java, Go, PHP, Ruby, Rust, and others.

Important limitations:

- Code navigation works on active branches.
- The repository must have fewer than 100,000 files.
- The symbol and language must be supported and successfully parsed.

If navigation is unavailable, use Code Search or local IDE navigation.

## 11. Git CLI equivalents

The following commands provide similar investigation capabilities locally.

### List tracked files

```bash
git ls-files
```

### Search the file list

```bash
git ls-files | grep "models.py"
```

PowerShell:

```powershell
git ls-files | Select-String "models.py"
```

### Show file history

```bash
git log -- path/to/file.py
```

Compact history:

```bash
git log --oneline -- path/to/file.py
```

Follow file renames:

```bash
git log --follow --oneline -- path/to/file.py
```

### Investigate line history

```bash
git blame path/to/file.py
```

Inspect a line range:

```bash
git blame -L 20,50 path/to/file.py
```

### Inspect a historical file version

```bash
git show COMMIT_SHA:path/to/file.py
```

### Compare two versions

```bash
git diff COMMIT_A COMMIT_B -- path/to/file.py
```

### Inspect a commit

```bash
git show COMMIT_SHA
```

## 12. Practical investigation scenarios

### Scenario A — Investigate Django authentication

1. Find the authentication-related files.
2. Inspect models, serializers, views, permissions, and services.
3. Navigate to relevant symbols.
4. Inspect file history.
5. Use Blame to investigate important lines.
6. Create permanent links to relevant code.

### Scenario B — Investigate a React component

1. Find a component such as `LoginForm.tsx`.
2. Inspect its imports and implementation.
3. Find its references.
4. Identify the page or feature that uses it.
5. Review its history.

### Scenario C — Investigate a suspicious change

1. Locate the affected function.
2. Open Blame.
3. Identify the last modifying commit.
4. Inspect the commit diff.
5. Investigate related files.
6. Share a permanent link to the relevant lines.

### Scenario D — Prepare a code review

A useful review comment should include:

- A permanent link to the exact code.
- A description of the observed issue.
- The expected behavior.
- Relevant technical context.

Avoid vague comments that refer only to a filename.

## 13. Hands-on exercises

Complete the following exercises in `github-deep-dive-training`.

### Exercise 1 — Navigate the repository

Navigate to `docs/github/module-01-code/`, open three lesson files, and record their complete paths.

### Exercise 2 — Use the file finder

Press `t` and search for:

```text
lesson-19
lesson-21
README.md
```

### Exercise 3 — Inspect file history

Open `lesson-19-git-configuration.md`, inspect its history, and identify the commit that introduced it.

### Exercise 4 — Use Blame

Open a lesson file, inspect its Blame view, and investigate at least one associated commit.

### Exercise 5 — Create a permanent file link

Open `README.md`, press `y`, and save the resulting permalink.

### Exercise 6 — Create a line-range link

Select a range of lines in a lesson file and copy its permanent link.

### Exercise 7 — Inspect an older version

Open a file's history, select an earlier commit, and compare that version with the current version.

### Exercise 8 — Investigate symbols

Use a Python or TypeScript repository to locate a symbol's definition and references where supported.

### Exercise 9 — Repeat with Git CLI

Run:

```bash
git ls-files
git log --oneline -- docs/github/module-01-code/lesson-19-git-configuration.md
git blame docs/github/module-01-code/lesson-19-git-configuration.md
```

Inspect one commit using `git show`.

### Exercise 10 — Write an investigation report

Create:

```text
exercises/module-01-code/lesson-22-repository-investigation.md
```

Use this structure:

```markdown
## Repository Investigation — Lesson 22

## 1. Repository information

- Repository:
- Branch:
- Date:

## 2. Files investigated

| File | Purpose | Path |
|---|---|---|
| | | |
| | | |
| | | |

## 3. File history

- File investigated:
- First relevant commit:
- Most recent relevant commit:
- Important change:

## 4. Blame investigation

- File:
- Lines investigated:
- Commit identified:
- What changed:

## 5. Permanent links

- File permalink:
- Line-range permalink:

## 6. Symbol navigation

- Symbol:
- Definition:
- References found:

## 7. Git CLI commands

List the commands used and explain their results.

## 8. Findings

Summarize what you learned.
```

## 14. Advanced challenge — Investigate an unfamiliar codebase

Choose a public Django REST Framework or React/TypeScript repository.

Investigate one feature without cloning the repository initially.

Your report must include:

1. Repository name and URL.
2. Feature investigated.
3. Relevant directory structure.
4. At least five relevant files.
5. One important class or function.
6. Its definition and references, if supported.
7. File history findings.
8. Blame findings.
9. A relevant commit and its diff.
10. At least two permanent links.
11. Git CLI investigation results after cloning.
12. Your technical conclusions.

Save the report as:

```text
exercises/module-01-code/advanced-repository-investigation.md
```

## 15. Completion checklist

- [ ] I can navigate repository directories.
- [ ] I can use the file finder.
- [ ] I understand GitHub's relevant keyboard shortcuts.
- [ ] I can inspect raw file content.
- [ ] I can open historical file versions.
- [ ] I can inspect file history.
- [ ] I can use GitHub Blame.
- [ ] I understand permanent file links.
- [ ] I can create line-range links.
- [ ] I understand code navigation and its limitations.
- [ ] I can investigate files using Git CLI.
- [ ] I completed the practical exercises.
- [ ] I completed the advanced challenge.

## 16. What comes next?

### Lesson 23: GitHub Blame, Commit History, and Line-Level Investigation — Advanced Practical Investigation

In the next lesson, we will go deeper into tracing changes across commits, investigating code ownership, understanding historical modifications, and combining GitHub's history tools with Git CLI.

## References

- GitHub Docs — Finding files on GitHub: <https://docs.github.com/en/search-github/searching-on-github/finding-files-on-github>
- GitHub Docs — Viewing and understanding files: <https://docs.github.com/en/repositories/working-with-files/using-files/viewing-and-understanding-files>
- GitHub Docs — Navigating code on GitHub: <https://docs.github.com/en/repositories/working-with-files/using-files/navigating-code-on-github>
- GitHub Docs — Getting permanent links to files: <https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files>
- GitHub Docs — Keyboard shortcuts: <https://docs.github.com/en/get-started/accessibility/keyboard-shortcuts>
- Git documentation — git-blame: <https://git-scm.com/docs/git-blame>

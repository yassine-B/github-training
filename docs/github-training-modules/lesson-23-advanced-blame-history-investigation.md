# Lesson 23 — Advanced GitHub Blame, Commit History, and Line-Level Investigation

**Module:** 1 — Code
**Level:** Advanced
**Type:** Practical investigation
**Repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

1. Trace a line of code through its commit history.
2. Understand GitHub Blame, `git blame`, `git log -L`, and `git log --follow`.
3. Investigate file renames and code movement.
4. Connect commits to pull requests and issues.
5. Compare historical implementations.
6. Identify formatting-only commits that affect blame results.
7. Build an evidence-based explanation of why code changed.
8. Create permanent GitHub links to investigation evidence.

## 2. Investigation workflow

When investigating unfamiliar code:

1. Locate the relevant file, function, or line.
2. Inspect its blame information.
3. Identify the commit that last modified it.
4. Inspect the commit's complete diff.
5. Find the related PR or issue, if available.
6. Trace earlier changes.
7. Compare historical implementations.
8. Document the evidence using permanent links.

**Important:** Blame identifies the commit that last modified a line. It does not necessarily identify the original author or explain why the code exists.

## 3. GitHub Blame versus Git history

| Tool | Main purpose |
|---|---|
| GitHub Blame | Shows which commit last changed each line |
| `git blame` | Inspects line-level modification history |
| `git log -- path` | Shows commits affecting a file |
| `git log -L` | Traces a function or line range |
| `git log --follow` | Follows file history across renames |
| `git show` | Inspects a specific commit |
| `git diff` | Compares two revisions |

## 4. Investigating code with GitHub

1. Open the repository's Code tab.
2. Navigate to a source file.
3. Open Blame.
4. Select a line.
5. Open its associated commit.
6. Inspect the diff, commit message, author, and date.
7. Find a related PR or issue, if available.
8. Record the evidence.

Record:

- File path and line number.
- Commit SHA.
- Commit message.
- Author and date.
- Changes shown in the diff.
- Related PR or issue.
- Explanation supported by the evidence.

## 5. Git CLI investigation commands

### 5.1 Inspect blame

```bash
git blame path/to/file.py
git blame -L 20,45 path/to/file.py
git blame -s path/to/file.py
```

### 5.2 Inspect commits

```bash
git show <commit-sha>
git show --stat <commit-sha>
git show <commit-sha> -- path/to/file.py
```

### 5.3 Inspect file history

```bash
git log -- path/to/file.py
git log --oneline -- path/to/file.py
git log -p -- path/to/file.py
git log --follow --oneline -- path/to/file.py
```

### 5.4 Trace a function

```bash
git log -L :function_name:path/to/file.py
```

### 5.5 Trace a line range

```bash
git log -L 20,45:path/to/file.py
```

`git log -L` has limitations for certain history and path changes. It is not a universal code-movement detector.

## 6. Detecting renames and code movement

### Detect file renames

```bash
git log --follow --oneline -- path/to/renamed_file.py
git show --summary <commit-sha>
```

Git detects renames using similarity heuristics. A reported similarity percentage is an estimate, not proof that the file's behavior remained unchanged.

### Detect moved lines

```bash
git blame -M path/to/file.py
```

### Detect copied lines

```bash
git blame -C path/to/file.py
git blame -C -C -C path/to/file.py
```

These options help detect moved or copied lines. Their results are heuristic.

When investigating a rename or refactor, check:

- The original file path.
- The new file path.
- Whether functions were renamed.
- Whether implementation details changed.
- Whether tests changed.
- Whether the refactor had an associated PR.

## 7. Formatting commits and blame-ignore revisions

Formatting commits can cause blame to attribute many lines to a mechanical formatting change.

A repository can maintain `.git-blame-ignore-revs`:

```text
# Repository-wide formatting
<full-formatting-commit-sha>

# Line-ending conversion
<full-line-ending-commit-sha>
```

Run:

```bash
git blame --ignore-revs-file .git-blame-ignore-revs path/to/file.py
```

Configure Git for the repository:

```bash
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

Verify:

```bash
git config --get blame.ignoreRevsFile
```

Only include commits that genuinely represent mechanical changes. Do not ignore commits that also introduced meaningful behavior changes.

GitHub can use this file in its blame view when correctly configured and supported.

## 8. Connecting commits to pull requests and issues

A commit describes a change. A pull request can explain the motivation, requirements, alternatives, and review discussion.

Investigate:

1. The commit message.
2. The commit diff.
3. The associated PR, if available.
4. The PR description.
5. Review comments and requested changes.
6. Linked issues.
7. Tests added or modified.

Useful commit-message searches:

```bash
git log --oneline --all --grep="duplicate order"

git log --all --grep="token validation" --oneline

git log --all --grep="payment" --regexp-ignore-case --oneline
```

Example issue references:

```text
Fixes #42
Closes #42
Refs #42
```

`Fixes #42` can automatically close the referenced issue when the PR is merged into the repository's default branch, subject to GitHub's closing-reference rules.

Not every commit has an associated PR or issue.

## 9. Comparing historical versions

Compare two commits:

```bash
git diff <old-commit> <new-commit>
```

Compare one file:

```bash
git diff <old-commit> <new-commit> -- path/to/file.py
```

Display a summary:

```bash
git diff --stat <old-commit> <new-commit>
```

Read an old version:

```bash
git show <commit-sha>:path/to/file.py
```

Compare a file across releases:

```bash
git diff <older-tag> <newer-tag> -- path/to/file.py
```

List commits between releases affecting a file:

```bash
git log --oneline <older-tag>..<newer-tag> -- path/to/file.py
```

## 10. Practical investigation scenarios

### Scenario A — Unexpected validation rule

You find:

```python
def validate_quantity(self, value):
    if value <= 0:
        raise serializers.ValidationError(
            "Quantity must be greater than zero."
        )
    return value
```

Investigate:

- Which commit last modified this validation?
- What did the previous implementation look like?
- Was the rule introduced to fix a bug?
- Did the PR add tests?
- Is the implementation consistent with the business requirements?

Commands:

```bash
git blame -L 1,12 backend/orders/serializers.py

git log --oneline -- backend/orders/serializers.py

git log -L :validate_quantity:backend/orders/serializers.py
```

Replace the example paths with paths from your project.

### Scenario B — A function was moved

You find:

```text
backend/payments/services/payment_service.py
```

Trace its history:

```bash
git log --follow --oneline -- backend/payments/services/payment_service.py
```

Inspect a suspected refactoring commit:

```bash
git show --stat <commit-sha>
git show <commit-sha>
```

Determine whether the implementation was simply moved or whether its behavior changed.

### Scenario C — Blame attributes everything to formatting

1. Inspect the formatting commit.
2. Verify that it was mechanical.
3. Add its SHA to `.git-blame-ignore-revs`.
4. Configure Git to use the file.
5. Compare blame results before and after.

### Scenario D — A regression appeared between releases

Find relevant release tags:

```bash
git log --oneline --decorate --all
```

Compare the releases:

```bash
git diff <older-tag> <newer-tag>
```

List commits affecting the relevant file:

```bash
git log --oneline <older-tag>..<newer-tag> -- path/to/file.py
```

Inspect the changes to narrow down the investigation.

## 11. Practical exercises

### Exercise 1 — Find the last modifying commit

1. Open a Markdown or source file.
2. Open its GitHub Blame view.
3. Select a line.
4. Record its commit SHA and message.
5. Inspect the commit diff.

**Deliverable:** Commit SHA, line number, and explanation.

### Exercise 2 — Trace a file's history

```bash
git log --oneline -- path/to/file.md
```

Find at least three commits that changed the file.

**Deliverable:** Chronological change summary.

### Exercise 3 — Investigate a commit

```bash
git show <commit-sha>
```

Identify the files changed, additions, deletions, and purpose.

**Deliverable:** Commit investigation note.

### Exercise 4 — Trace a function

```bash
git log -L :function_name:path/to/file.py
```

Identify at least two meaningful changes.

**Deliverable:** Function evolution timeline.

### Exercise 5 — Investigate a rename

```bash
git log --follow --oneline -- path/to/file.py
```

Determine whether the file has been renamed.

**Deliverable:** Old and new paths, if applicable.

### Exercise 6 — Detect moved code

```bash
git blame -M path/to/file.py
git blame -C path/to/file.py
```

Compare the output.

**Deliverable:** Explanation of the differences.

### Exercise 7 — Compare historical versions

```bash
git diff <old-commit> <new-commit> -- path/to/file.py
```

Identify important behavior changes.

**Deliverable:** Before-and-after explanation.

### Exercise 8 — Find the PR or issue

Choose a commit introduced through a pull request.

Find the PR and identify the requirement or issue it addressed.

**Deliverable:** PR number, issue number if available, and explanation.

### Exercise 9 — Create a blame-ignore file

If the repository has a genuine formatting-only commit:

1. Create `.git-blame-ignore-revs`.
2. Add its full SHA.
3. Configure Git.
4. Compare blame results.

**Deliverable:** Ignore file and evidence.

### Exercise 10 — Create permanent investigation links

Create a Markdown note containing:

- Permanent file link.
- Permanent blame link.
- Commit link.
- PR or issue link, if available.

**Deliverable:** Working links and investigation notes.

## 12. Advanced challenge — Investigate a real code change

Choose a function from a Django REST Framework or React project with a meaningful history.

Reconstruct its development history.

Requirements:

1. Identify the current implementation.
2. Find its latest modifying commit.
3. Inspect the complete diff.
4. Trace its history using `git log -L`.
5. Check whether the file was renamed or code was moved.
6. Find the related PR and issue, if available.
7. Compare an earlier implementation with the current one.
8. Explain the reason for the change using evidence.

Create a report:

```markdown
# Code Investigation Report

## 1. Target
- Repository:
- File:
- Function:
- Current line range:

## 2. Latest Modification
- Commit SHA:
- Commit message:
- Author:
- Date:

## 3. Historical Changes
| Commit | Change | Reason |
|---|---|---|
| ... | ... | ... |

## 4. Related Pull Request / Issue
- PR:
- Issue:
- Original requirement:

## 5. Before and After
- Previous behavior:
- Current behavior:
- Important differences:

## 6. Conclusion
Explain what changed and why, citing the evidence.

## 7. Permanent Links
- File:
- Blame:
- Commit:
- Pull request:
- Issue:
```

## 13. Investigation principles

- Blame is evidence, not an explanation.
- Commit messages must be verified against the diff.
- A rename does not prove behavior was preserved.
- PR descriptions may omit important details.
- Review comments and linked issues can provide important context.
- Formatting commits can obscure blame history.
- Permanent investigation links should use commit SHAs rather than moving branch names.

## 14. Completion checklist

- [ ] I can use GitHub Blame.
- [ ] I can inspect the commit behind a line.
- [ ] I can trace a file's history.
- [ ] I can trace a function with `git log -L`.
- [ ] I understand rename and copy detection.
- [ ] I can use `.git-blame-ignore-revs`.
- [ ] I can connect commits to PRs and issues.
- [ ] I can compare historical implementations.
- [ ] I have completed the practical exercises.
- [ ] I have completed the advanced investigation report.

---

**Next lesson:** Lesson 24 — GitHub Releases, Tags, and Version History: Advanced Repository Release Management.

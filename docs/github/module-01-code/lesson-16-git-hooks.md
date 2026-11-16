# Module 1 — Code Tab
# Lesson 16: Git Hooks — Automating Checks and Enforcing Repository Standards

**Filename:** `docs/github/module-01-code/lesson-16-git-hooks.md`
**Suggested branch:** `docs/add-git-hooks-lesson`
**Level:** Advanced
**Practice repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what Git hooks are and when they execute.
- Distinguish client-side hooks from server-side hooks.
- Create and configure native Git hooks.
- Validate commit messages using Conventional Commits.
- Prevent commits containing whitespace errors.
- Understand and use the `pre-commit` framework.
- Configure Husky for JavaScript and TypeScript projects.
- Use lint-staged to run checks only on staged files.
- Understand how Git hooks fit into a professional CI/CD workflow.
- Recognize the limitations of local hooks and avoid treating them as a security boundary.

## 2. What are Git hooks?

Git hooks are scripts that Git executes automatically when specific events occur.

For example:

1. A developer stages files.
2. The developer executes `git commit`.
3. Git executes the `pre-commit` hook.
4. If the hook succeeds, Git continues creating the commit.
5. Git executes the `commit-msg` hook to validate the commit message.
6. If validation succeeds, the commit is created.

Hooks allow you to automate repetitive tasks and enforce development standards.

### Real-world examples

| Event | Automated task |
|---|---|
| Before commit | Check formatting and whitespace |
| Before commit | Run linting on changed files |
| Before commit | Detect accidentally committed secrets |
| Validate commit message | Enforce Conventional Commits |
| Before push | Run selected tests |
| After checkout | Prepare local development environment |
| Before receiving a push | Enforce server-side repository policies |

### Why use Git hooks?

Imagine a team of five developers working on a DRF + React application.

Without automated checks:

- One developer commits poorly formatted Python.
- Another commits a message such as `changes`.
- Another accidentally adds a generated file.
- Another introduces a linting error.
- Reviewers repeatedly spend time identifying preventable problems.

With hooks, many of these problems can be detected before code reaches the remote repository.

---

## 3. Git hooks architecture

Git hooks are stored in the repository's Git directory.

The default location is:

```text
.git/
└── hooks/
    ├── applypatch-msg.sample
    ├── commit-msg.sample
    ├── fsmonitor-watchman.sample
    ├── post-update.sample
    ├── pre-applypatch.sample
    ├── pre-commit.sample
    ├── pre-merge-commit.sample
    ├── pre-push.sample
    ├── pre-rebase.sample
    ├── prepare-commit-msg.sample
    └── update.sample
```

Files ending in `.sample` are examples. Git does not automatically execute them.

To activate a hook, create a file with the corresponding hook name, without `.sample`.

For example:

```text
.git/hooks/pre-commit
.git/hooks/commit-msg
.git/hooks/pre-push
```

**Important:** The `.git/hooks` directory is not normally committed to the repository. That means another developer who clones your project will not automatically receive your custom hooks.

Later in this lesson, you will learn how to share hooks using `pre-commit` and Husky.

### Inspect your hooks

```bash
ls .git/hooks
```

On Windows PowerShell:

```powershell
Get-ChildItem .git/hooks
```

You can also inspect the configured hooks directory:

```bash
git config --show-origin --get core.hooksPath
```

If this returns nothing, Git normally uses `.git/hooks`.

---

## 4. Client-side hooks vs server-side hooks

Git hooks are divided into two main categories.

### 4.1 Client-side hooks

Client-side hooks execute on the developer's local machine.

Examples:

- `pre-commit`
- `prepare-commit-msg`
- `commit-msg`
- `post-commit`
- `pre-push`
- `post-checkout`
- `post-merge`
- `pre-rebase`

Typical purposes:

- Formatting.
- Linting.
- Commit-message validation.
- Running selected tests.
- Checking staged files.

### 4.2 Server-side hooks

Server-side hooks execute on the server receiving Git operations.

Examples:

- `pre-receive`
- `update`
- `post-receive`

Typical purposes:

- Rejecting prohibited pushes.
- Enforcing server-side repository policies.
- Triggering deployment or integration workflows.

GitHub users generally do not manage GitHub's underlying server-side Git hooks directly. For GitHub repositories, use branch protection rules, rulesets, required status checks, and GitHub Actions to enforce remote repository policies.

### Comparison

| Feature | Client-side | Server-side |
|---|---|---|
| Execution location | Developer's machine | Git server |
| Runs before local commit | Yes | No |
| Can validate commit messages | Yes | Yes, where supported |
| Can be bypassed by local user | Often | Controlled by server |
| Shared automatically by Git clone | No | Server-managed |
| Suitable as security enforcement | No | Yes, when correctly configured |

**Critical security principle:** A local hook can be skipped using commands such as `git commit --no-verify`. Never rely on a local hook alone to protect production branches or enforce security requirements.

---

## 5. Important Git hooks

You should understand the purpose of the main hooks before implementing them.

### 5.1 `pre-commit`

Runs before Git creates a commit.

Common uses:

- Check formatting.
- Run linting.
- Check staged files.
- Detect accidental secrets.
- Prevent commits with whitespace errors.

### 5.2 `prepare-commit-msg`

Runs before the commit-message editor is opened or before a supplied message is finalized.

It can prepare or modify the commit message.

Example use cases:

- Insert a ticket reference.
- Add a branch-related prefix.
- Prepare a template.

Use caution: automatically modifying commit messages can surprise developers.

### 5.3 `commit-msg`

Runs after the commit message has been prepared.

Its main argument is the path to the commit-message file.

Common uses:

- Enforce Conventional Commits.
- Require issue or ticket references.
- Reject empty or invalid messages.

### 5.4 `post-commit`

Runs after a commit has been created.

Common uses:

- Local notifications.
- Logging.
- Optional developer tooling.

It cannot reject a commit that has already been created.

### 5.5 `pre-push`

Runs before Git sends commits to a remote repository.

Common uses:

- Run tests.
- Validate the branch.
- Check for prohibited files.
- Run additional local checks.

It receives information about the refs being pushed through standard input.

### 5.6 `post-checkout`

Runs after checking out a branch or switching to another commit.

Possible uses:

- Notify developers about environment changes.
- Prepare local dependencies.
- Run optional development scripts.

### 5.7 `post-merge`

Runs after a successful merge.

Possible uses:

- Notify developers that dependencies may have changed.
- Remind developers to update local environments.
- Run non-destructive preparation scripts.

### 5.8 `pre-rebase`

Runs before a rebase begins.

Possible use:

- Prevent rebasing protected branches under local team policy.

### 5.9 Server-side hooks

| Hook | Purpose |
|---|---|
| `pre-receive` | Runs before a push is accepted; can reject the entire push |
| `update` | Runs for each ref being updated; can reject an individual ref |
| `post-receive` | Runs after refs have been updated successfully |

You do not need to implement server-side hooks in this exercise. Focus on client-side hooks and GitHub's remote enforcement mechanisms.

---

# Part A — Native Git hooks

## 6. Create your first `pre-commit` hook

We will create a hook that checks staged changes for whitespace errors.

### Step 1: Create the hook

From the root of your training repository, use PowerShell:

```powershell
@'
#!/bin/sh

echo "Running pre-commit checks..."

git diff --cached --check

if [ $? -ne 0 ]; then
    echo "ERROR: Staged changes contain whitespace errors."
    exit 1
fi

echo "Pre-commit checks passed."
exit 0
'@ | Set-Content -NoNewline .git/hooks/pre-commit
```

The script performs these operations:

1. Prints a message.
2. Checks the staged changes.
3. Exits with a non-zero status if the check fails.
4. Allows the commit if the check succeeds.

Git for Windows includes Git Bash, which can execute standard shell hook scripts.

### Step 2: Test the hook

Create a test file:

```powershell
New-Item -ItemType File -Path hook-test.txt
```

Add some content:

```powershell
"Testing Git hooks" | Set-Content hook-test.txt
```

Stage the file:

```bash
git add hook-test.txt
```

Commit:

```bash
git commit -m "test: verify pre-commit hook"
```

Expected behavior:

```text
Running pre-commit checks...
Pre-commit checks passed.
```

### Step 3: Test a failing condition

Introduce a trailing whitespace error into a file and stage it.

For example, create a file containing a line with trailing spaces:

```powershell
"Invalid trailing spaces   " | Set-Content whitespace-test.txt
git add whitespace-test.txt
```

Try to commit:

```bash
git commit -m "test: verify whitespace validation"
```

The hook should reject the commit if Git detects the whitespace error.

Fix the file, stage it again, and retry.

```powershell
"Corrected line" | Set-Content whitespace-test.txt
git add whitespace-test.txt
git commit -m "test: fix whitespace validation"
```

**Important:** `git diff --cached --check` checks staged changes, not every file in your working directory.

---

## 7. Create a `commit-msg` hook

Now we will enforce Conventional Commits.

### 7.1 What are Conventional Commits?

Conventional Commits define a structured commit-message format.

General format:

```text
<type>[optional scope][optional !]: <description>
```

Examples:

```text
feat(auth): add JWT authentication

fix(api): handle missing customer records

docs(github): add Git hooks lesson

refactor(orders): simplify order validation

test(users): add registration tests

chore(deps): update development dependencies

feat(api)!: remove deprecated response format
```

Common types:

| Type | Purpose |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting or style changes without logic changes |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD changes |
| `chore` | Maintenance |
| `revert` | Reverting a previous commit |

A breaking change can be indicated with `!` or a `BREAKING CHANGE:` footer.

### 7.2 Create the hook

PowerShell:

```powershell
@'
#!/bin/sh

commit_message_file="$1"
commit_message=$(head -n 1 "$commit_message_file")

pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9._-]+\))?!?: .+'

if ! printf '%s\n' "$commit_message" | grep -Eq "$pattern"; then
    echo "ERROR: Invalid commit message."
    echo ""
    echo "Expected format:"
    echo "type(scope): description"
    echo ""
    echo "Examples:"
    echo "feat(auth): add JWT authentication"
    echo "fix(api): handle invalid requests"
    echo "docs(github): add Git hooks lesson"
    exit 1
fi

echo "Commit message validation passed."
exit 0
'@ | Set-Content -NoNewline .git/hooks/commit-msg
```

This hook:

- Receives the commit-message file path.
- Reads its first line.
- Validates the message format.
- Rejects invalid messages.

### 7.3 Test invalid messages

Try:

```bash
git commit -m "update files"
```

Expected: the commit should be rejected.

Try:

```bash
git commit -m "added new feature"
```

Expected: rejected.

### 7.4 Test valid messages

```bash
git commit -m "docs(github): add git hooks lesson"
```

Expected: accepted if the `pre-commit` hook also passes.

**Note:** This is a basic first-line validator. It does not fully validate every Conventional Commits rule, such as footer placement or all breaking-change semantics. For production projects, use Commitlint.

---

## 8. Create a `pre-push` hook

A `pre-push` hook can run checks before code is sent to a remote repository.

For this training exercise, we will use it to check for whitespace errors in committed changes.

Create:

```powershell
@'
#!/bin/sh

echo "Running pre-push checks..."

git diff --check

if [ $? -ne 0 ]; then
    echo "ERROR: Fix whitespace errors before pushing."
    exit 1
fi

echo "Pre-push checks passed."
exit 0
'@ | Set-Content -NoNewline .git/hooks/pre-push
```

Test:

```bash
git push origin HEAD
```

If the hook passes, Git continues the push.

### Production example

In a real project, you might use `pre-push` to run:

```bash
pytest
```

Or:

```bash
npm run test
```

Or:

```bash
npm run lint
```

Do not automatically run an expensive full test suite before every push if CI already performs it. Select checks based on their execution time and value.

---

## 9. Native hooks limitations

Native Git hooks are useful, but they have important limitations.

1. Hooks are not normally tracked in `.git/hooks`.
2. Cloning a repository does not automatically install your custom hooks.
3. A developer can bypass many client-side hooks.
4. Hooks can behave differently across operating systems.
5. A poorly written hook can slow down development.
6. Local hooks cannot replace remote CI checks.

### How to share native hooks

Git supports a custom hooks directory through `core.hooksPath`.

For example:

```bash
git config core.hooksPath .githooks
```

You can then store hooks in the repository:

```text
.githooks/
├── pre-commit
├── commit-msg
└── pre-push
```

The `.githooks` directory can be committed.

However, each developer must configure the directory locally:

```bash
git config core.hooksPath .githooks
```

You can document this setup in your README or automate it with a project setup script.

**Security note:** Only install and execute hooks from repositories and dependencies you trust. Hooks execute code on the developer's machine.

---

# Part B — The pre-commit framework

## 10. What is pre-commit?

The `pre-commit` framework is a tool that manages and executes Git hooks.

It is especially useful for Python projects and multi-language repositories.

Instead of manually writing multiple hook scripts, you define the checks in:

```text
.pre-commit-config.yaml
```

The framework manages hook environments and executes configured checks.

### Benefits

- Shared hook configuration.
- Consistent checks across developers.
- Support for multiple programming languages.
- Automatic hook installation.
- Easy execution across all files.
- Integration with CI pipelines.

Official documentation:

https://pre-commit.com/

## 11. Install pre-commit

For a Python development environment:

```bash
pip install pre-commit
```

Verify:

```bash
pre-commit --version
```

Install the Git hook:

```bash
pre-commit install
```

This installs a hook that invokes the framework when you commit.

To install the commit-message hook as well, if your configuration includes commit-message validation:

```bash
pre-commit install --hook-type commit-msg
```

You can inspect installed hook files in `.git/hooks`.

## 12. Create `.pre-commit-config.yaml`

Create this file in the repository root:

**Filename:** `.pre-commit-config.yaml`

Example:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

The version numbers above are illustrative pinned revisions for the exercise. Before adopting them in a new project, check the repositories for current supported releases and pin versions you have reviewed.

### Explanation

`repos` contains the hook repositories.

Each repository specifies:

- `repo`: source repository.
- `rev`: pinned revision.
- `hooks`: checks to execute.

Examples:

| Hook | Purpose |
|---|---|
| `trailing-whitespace` | Removes trailing whitespace |
| `end-of-file-fixer` | Ensures a final newline |
| `check-yaml` | Checks YAML syntax |
| `check-json` | Checks JSON syntax |
| `check-added-large-files` | Prevents oversized files from being added |
| `detect-private-key` | Detects certain private-key patterns |
| `ruff` | Python linting |
| `ruff-format` | Python formatting |

The private-key hook is useful, but it is not a complete secret scanner. Use dedicated secret scanning and remote security controls as well.

## 13. Run pre-commit

Run against all files:

```bash
pre-commit run --all-files
```

Run against staged files:

```bash
pre-commit run
```

Run a specific hook:

```bash
pre-commit run trailing-whitespace --all-files
```

Update hook revisions:

```bash
pre-commit autoupdate
```

Review the resulting version changes before committing them.

### Important behavior

Some hooks modify files automatically.

For example:

- `trailing-whitespace` may remove trailing spaces.
- `end-of-file-fixer` may add a final newline.
- `ruff --fix` may automatically correct certain linting issues.

After a hook modifies files, inspect and stage the changes again:

```bash
git status
git diff
git add .
git commit -m "chore: apply pre-commit formatting"
```

## 14. pre-commit in a DRF project

For a Django REST Framework backend, you could use:

- Ruff for linting.
- Ruff formatter for formatting.
- Django checks.
- YAML and JSON validation.
- Secret detection.
- Tests in a separate, appropriately timed workflow.

Example configuration:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

This configuration provides a useful baseline. It does not automatically validate Django migrations, run database-backed tests, or verify every Django configuration.

Those checks belong in additional scripts or CI workflows.

### Example project structure

```text
backend/
├── config/
├── apps/
├── tests/
├── manage.py
├── pyproject.toml
└── .pre-commit-config.yaml
```

You can keep the configuration at the repository root or in a backend-specific location, depending on how the project is organized.

---

# Part C — Husky, lint-staged and Commitlint

## 15. What is Husky?

Husky is a tool for managing Git hooks in JavaScript and Node.js projects.

It is commonly used with:

- React
- Vite
- TypeScript
- ESLint
- Prettier
- lint-staged
- Commitlint

Official documentation:

https://typicode.github.io/husky/

### Why use Husky?

Consider a React project with 100 source files.

Running ESLint across the entire project before every commit may be unnecessarily slow.

Husky allows you to execute hooks, while lint-staged helps run tools only against staged files.

## 16. Install Husky

Inside your React project:

```bash
npm install --save-dev husky
```

Initialize:

```bash
npx husky init
```

This configures Husky for the project and creates a `.husky` directory.

A typical structure:

```text
frontend/
├── .husky/
│   └── pre-commit
├── src/
├── package.json
├── package-lock.json
└── vite.config.ts
```

Husky's initialization may also add a `prepare` script to `package.json`.

Check:

```json
{
  "scripts": {
    "prepare": "husky"
  }
}
```

The `prepare` script helps install hooks when project dependencies are installed.

## 17. Install lint-staged

```bash
npm install --save-dev lint-staged
```

Add scripts and configuration to `package.json`.

Example:

```json
{
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write .",
    "test": "vitest run",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml,css,scss}": [
      "prettier --write"
    ]
  }
}
```

The configuration associates file patterns with commands.

For example:

```text
src/components/Button.tsx
```

will match:

```text
*.{js,jsx,ts,tsx}
```

and receive the configured ESLint and Prettier checks.

Do not configure multiple formatters that fight over the same files. Decide which tool owns formatting.

## 18. Configure the Husky pre-commit hook

Create or edit:

```text
.husky/pre-commit
```

Content:

```sh
npx lint-staged
```

Now, when a developer commits:

1. Git triggers the Husky hook.
2. Husky executes lint-staged.
3. lint-staged identifies staged files.
4. ESLint runs on matching JavaScript and TypeScript files.
5. Prettier formats matching files.
6. If checks succeed, Git continues the commit.

### Example workflow

```bash
git add src/components/Button.tsx
git commit -m "feat(ui): add reusable button component"
```

Only the staged matching files are processed.

This is generally faster than linting the entire application on every commit.

## 19. Configure Commitlint

Husky manages hook execution. Commitlint validates commit messages.

Install:

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

Create:

**Filename:** `commitlint.config.js`

```javascript
export default {
  extends: ["@commitlint/config-conventional"],
};
```

Create:

**Filename:** `.husky/commit-msg`

```sh
npx --no -- commitlint --edit "$1"
```

Now try:

```bash
git commit -m "update button"
```

Expected: rejected.

Try:

```bash
git commit -m "feat(ui): add reusable button component"
```

Expected: accepted if the other checks pass.

Commitlint supports additional rules and configurations. You can later configure:

- Allowed commit types.
- Required scopes.
- Header length.
- Subject casing.
- Issue references.
- Breaking-change conventions.

Official documentation:

https://commitlint.js.org/

## 20. Husky vs native Git hooks vs pre-commit

| Feature | Native Git hooks | pre-commit | Husky |
|---|---|---|---|
| Primary use | Custom Git automation | Managed hooks | JavaScript project hooks |
| Python support | Yes | Yes | Possible, but not its main focus |
| Node.js support | Yes | Yes | Yes |
| Shared configuration | Manual | Yes | Yes |
| Commit-message validation | Custom script | With suitable hook | With Commitlint |
| Staged-file checks | Custom script | Supported by suitable hooks | lint-staged |
| Best fit | Custom workflows | Python and multi-language projects | JavaScript/TypeScript projects |

### Which should you choose?

For a DRF + React project:

**Backend**
- pre-commit
- Ruff
- Python formatting and linting
- selected fast validation checks

**Frontend**
- Husky
- lint-staged
- ESLint
- Prettier
- Commitlint

**Repository**
- GitHub Actions
- Required status checks
- Branch protection or repository rulesets

Avoid installing several competing hook managers without a clear reason. Decide which tool owns each hook and document the arrangement.

---

# Part D — Production workflow

## 21. How Git hooks fit into the development lifecycle

A professional development workflow should distribute checks across several stages.

```text
Developer writes code
        |
        v
Developer stages changes
        |
        v
pre-commit hook
        |
        +--> Formatting
        +--> Linting
        +--> Secret checks
        |
        v
commit-msg hook
        |
        +--> Conventional Commit validation
        |
        v
Git commit created
        |
        v
Developer pushes branch
        |
        v
pre-push hook
        |
        +--> Selected tests
        +--> Local validation
        |
        v
GitHub receives push
        |
        v
GitHub Actions
        |
        +--> Full linting
        +--> Tests
        +--> Security checks
        +--> Build
        |
        v
Pull request review
        |
        v
Required checks pass
        |
        v
Merge
```

### Important distinction

Local hooks improve developer experience.

GitHub Actions and remote repository rules provide centralized enforcement.

A developer may bypass a local hook. They should not be able to bypass required remote checks merely by skipping local validation.

## 22. Example: A production DRF + React workflow

Imagine a SaaS repository:

```text
my-saas-platform/
├── backend/
│   ├── apps/
│   ├── config/
│   ├── tests/
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
│
├── .pre-commit-config.yaml
├── README.md
└── CONTRIBUTING.md
```

### Backend checks

Before committing:

- Ruff linting.
- Ruff formatting.
- Trailing whitespace.
- End-of-file checks.
- Secret-pattern checks.

Before merging:

- Python test suite.
- Django system checks.
- Migration validation.
- Dependency and security checks.
- Integration tests where appropriate.

### Frontend checks

Before committing:

- ESLint on staged files.
- Prettier on staged files.
- Commit-message validation.

Before merging:

- Full linting.
- TypeScript type checking.
- Unit tests.
- Production build.

### CI checks

GitHub Actions should run the authoritative checks on pull requests and protected branches.

Do not assume a local hook ran successfully just because a commit exists.

---

## 23. Hook security and reliability

Git hooks execute scripts. Treat them as executable code.

### Security practices

1. Review hook scripts before installing them.
2. Review third-party hook repositories.
3. Pin dependencies to reviewed versions.
4. Avoid putting credentials or tokens in hook scripts.
5. Do not download and execute arbitrary scripts during every commit.
6. Keep hook scripts small and understandable.
7. Do not use hooks as the only secret-protection mechanism.
8. Keep remote security checks enabled.

### Performance practices

A hook that takes 30 seconds on every commit will frustrate developers.

Use this division:

| Check | Recommended stage |
|---|---|
| Trailing whitespace | Pre-commit |
| Formatting | Pre-commit |
| Fast linting | Pre-commit |
| Commit-message validation | Commit-msg |
| Selected unit tests | Pre-push or CI |
| Full test suite | CI |
| Integration tests | CI |
| Build verification | CI |
| Deployment | Protected deployment workflow |

### Bypassing hooks

For example:

```bash
git commit --no-verify -m "chore: temporary test"
```

This bypasses certain local commit hooks.

For pushes:

```bash
git push --no-verify
```

This bypasses the local pre-push hook.

These commands are useful for understanding the limitations of client-side hooks. Do not use them to avoid required project checks.

---

# Part E — Practical exercises

## 24. Exercise 1: Native pre-commit hook

**Goal:** Create a native Git hook that blocks staged whitespace errors.

Tasks:

1. Create `.git/hooks/pre-commit`.
2. Add the whitespace-validation script.
3. Create a test file.
4. Stage the file.
5. Test a valid commit.
6. Introduce trailing whitespace.
7. Test a rejected commit.
8. Fix the file and commit again.

Expected result:

- Valid staged changes are accepted.
- Detected whitespace errors cause the commit to fail.

## 25. Exercise 2: Conventional Commit validation

**Goal:** Enforce commit-message standards.

Tasks:

1. Create `.git/hooks/commit-msg`.
2. Add the validation script.
3. Try an invalid commit message.
4. Try a valid commit message.
5. Test a message with a scope.
6. Test a breaking-change marker.

Test messages:

```text
update files
```

```text
feat(auth): add authentication
```

```text
fix(api): handle invalid requests
```

```text
feat(api)!: remove deprecated endpoint
```

Expected result:

- Invalid messages are rejected.
- Valid messages are accepted.

## 26. Exercise 3: Configure pre-commit

**Goal:** Use a managed hook configuration.

Tasks:

1. Install `pre-commit`.
2. Create `.pre-commit-config.yaml`.
3. Configure whitespace and YAML checks.
4. Install the hooks.
5. Run `pre-commit run --all-files`.
6. Introduce a formatting problem.
7. Run the checks again.
8. Review automatically modified files.
9. Stage the corrections.
10. Commit the configuration.

Expected result:

- Checks execute consistently.
- Automatically corrected files are visible in Git.
- The configuration is committed and shared with the team.

## 27. Exercise 4: Husky and lint-staged

Perform this exercise in a separate React/Vite practice project if your training repository does not contain a frontend application.

Tasks:

1. Install Husky.
2. Initialize Husky.
3. Install lint-staged.
4. Configure ESLint and Prettier.
5. Create `.husky/pre-commit`.
6. Stage one TypeScript file.
7. Commit the file.
8. Observe which files were processed.
9. Introduce a linting error.
10. Confirm that the commit is rejected.
11. Fix the error and commit again.

Expected result:

- Only matching staged files are processed.
- Linting errors prevent the commit.

## 28. Exercise 5: Commitlint

Tasks:

1. Install Commitlint.
2. Create `commitlint.config.js`.
3. Create `.husky/commit-msg`.
4. Try an invalid message.
5. Try a valid message.
6. Test a breaking-change message.
7. Document the team's commit convention.

Expected result:

- Commit messages follow a consistent standard.
- Developers receive clear feedback when messages are invalid.

## 29. Exercise 6: Design a complete hook policy

Create:

**Filename:** `docs/github/module-01-code/git-hooks-policy.md`

Document the hook policy for a hypothetical DRF + React SaaS team.

Include:

- Which hooks are installed.
- Which checks execute before commits.
- Which checks execute before pushes.
- Which checks run in GitHub Actions.
- How commit messages are validated.
- How developers install hooks.
- How hook versions are maintained.
- How hook failures are fixed.
- Which checks are mandatory remotely.
- How exceptions are handled.

Suggested policy:

| Area | Tool | Stage |
|---|---|---|
| Python linting | Ruff | Pre-commit |
| Python formatting | Ruff formatter | Pre-commit |
| Frontend linting | ESLint | Pre-commit |
| Frontend formatting | Prettier | Pre-commit |
| Staged-file processing | lint-staged | Pre-commit |
| Commit messages | Commitlint | Commit-msg |
| Backend tests | pytest | CI |
| Frontend tests | Vitest | CI |
| Type checking | TypeScript | CI |
| Build verification | Vite | CI |
| Security scanning | GitHub security tools / CI | CI |

---

# Part F — GitHub workflow and lesson delivery

## 30. Add the lesson to your training repository

Return to your `github-deep-dive-training` repository.

Create a branch:

```bash
git switch main
git pull origin main
git switch -c docs/add-git-hooks-lesson
```

Create the directory if it does not already exist:

```powershell
New-Item -ItemType Directory -Force docs/github/module-01-code
```

Create:

```text
docs/github/module-01-code/lesson-16-git-hooks.md
```

Paste this lesson into the file.

Also create:

```text
docs/github/module-01-code/git-hooks-policy.md
```

Use the policy exercise to document the standards you would apply to a real project.

## 31. Review your changes

```bash
git status
```

Inspect:

```bash
git diff
```

Check whitespace:

```bash
git diff --check
```

Stage the files:

```bash
git add docs/github/module-01-code/lesson-16-git-hooks.md
git add docs/github/module-01-code/git-hooks-policy.md
```

Review staged changes:

```bash
git diff --cached
```

## 32. Commit your lesson

Use:

```bash
git commit -m "docs(github): add git hooks and commit validation lesson"
```

If your commit-message hook is installed, this message should satisfy the basic Conventional Commit pattern.

Push:

```bash
git push -u origin docs/add-git-hooks-lesson
```

## 33. Create a pull request

On GitHub:

1. Open `github-deep-dive-training`.
2. Navigate to Pull requests.
3. Select New pull request.
4. Base branch: `main`.
5. Compare branch: `docs/add-git-hooks-lesson`.
6. Create the pull request.

Suggested title:

```text
docs(github): add Git hooks training lesson
```

Suggested description:

```markdown
## Summary

Adds Module 1 — Lesson 16: Git Hooks.

## Topics covered

- Native Git hooks
- Client-side and server-side hooks
- pre-commit
- commit-msg
- pre-push
- pre-commit framework
- Husky
- lint-staged
- Commitlint
- Hook security and performance
- Production DRF + React workflow

## Additional documentation

- Git hooks policy

## Verification

- [ ] Markdown reviewed
- [ ] Git commands checked
- [ ] Native hook exercises completed
- [ ] pre-commit exercise completed
- [ ] Husky exercise completed
- [ ] Commitlint exercise completed
```

Review the changes, resolve any feedback, and merge according to the workflow you established in earlier lessons.

After merging:

```bash
git switch main
git pull origin main
```

## 34. Create an annotated Git tag

First inspect existing tags:

```bash
git tag --list
```

Check whether `module-01-lesson-16` already exists. Do not overwrite an existing tag.

If it does not exist, create the annotated tag:

```bash
git tag -a module-01-lesson-16 -m "Module 1 Lesson 16: Git Hooks"
```

Push it:

```bash
git push origin module-01-lesson-16
```

Verify:

```bash
git show module-01-lesson-16
```

Remember:

- A Git tag is a Git reference to a commit.
- An annotated tag includes metadata and a message.
- A GitHub Release is a GitHub feature associated with a tag.

## 35. Create a GitHub Release

Open your repository:

1. Navigate to Releases.
2. Select Draft a new release.
3. Choose the existing tag `module-01-lesson-16`.
4. Set the release title:

```text
Module 1 — Lesson 16: Git Hooks
```

5. Add these release notes:

```markdown
# Module 1 — Lesson 16: Git Hooks

This lesson introduces automated Git workflows.

## Topics

- Native Git hooks
- Client-side and server-side hooks
- pre-commit
- commit-msg
- pre-push
- pre-commit framework
- Husky
- lint-staged
- Commitlint
- Hook security and performance
- Production Git workflow

## Practical exercises

- Native hook creation
- Commit-message validation
- pre-commit configuration
- Husky configuration
- lint-staged configuration
- Commitlint configuration
- Git hooks policy

## Documentation

See:

docs/github/module-01-code/lesson-16-git-hooks.md
```

6. Publish the release.

---

# Part G — Final checklist

## 36. Lesson completion checklist

### Git hooks fundamentals

- [ ] I understand what Git hooks are.
- [ ] I understand client-side hooks.
- [ ] I understand server-side hooks.
- [ ] I know where Git stores hooks.
- [ ] I understand why `.git/hooks` is not shared automatically.
- [ ] I understand that local hooks can be bypassed.

### Native hooks

- [ ] I created a `pre-commit` hook.
- [ ] I tested whitespace validation.
- [ ] I created a `commit-msg` hook.
- [ ] I enforced a Conventional Commit format.
- [ ] I created a `pre-push` hook.
- [ ] I tested hook failure behavior.

### pre-commit

- [ ] I installed the framework.
- [ ] I created `.pre-commit-config.yaml`.
- [ ] I configured formatting checks.
- [ ] I configured linting checks.
- [ ] I ran all hooks against all files.
- [ ] I understand pinned hook revisions.

### Husky ecosystem

- [ ] I installed Husky.
- [ ] I configured lint-staged.
- [ ] I configured ESLint and Prettier.
- [ ] I configured Commitlint.
- [ ] I tested invalid commit messages.

### GitHub workflow

- [ ] I created the lesson file.
- [ ] I created the hook policy file.
- [ ] I committed the changes.
- [ ] I pushed the branch.
- [ ] I created a pull request.
- [ ] I merged the pull request.
- [ ] I created the annotated tag.
- [ ] I published the GitHub Release.

---

# 37. Official documentation

Use these resources to deepen your understanding:

| Resource | Link |
|---|---|
| Git Hooks | https://git-scm.com/docs/githooks |
| Git Configuration | https://git-scm.com/docs/git-config |
| pre-commit | https://pre-commit.com/ |
| Husky | https://typicode.github.io/husky/ |
| lint-staged | https://github.com/lint-staged/lint-staged |
| Commitlint | https://commitlint.js.org/ |
| Conventional Commits | https://www.conventionalcommits.org/ |
| GitHub Actions | https://docs.github.com/en/actions |
| GitHub Rulesets | https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets |

---

# 38. What comes next?

**Module 1 — Lesson 17: Git Reflog and Repository Recovery**

The next lesson will cover how to recover from common Git mistakes and understand Git's reference history.

Planned topics:

- What is `git reflog`?
- `HEAD` and reference movements.
- Recovering deleted branches.
- Recovering commits after reset.
- Recovering from accidental rebases.
- Recovering from incorrect merges.
- Understanding `git reset` vs `git revert`.
- Safe repository recovery workflows.
- Recovery exercises using a disposable practice branch.

The objective is to become comfortable recovering from mistakes without unnecessarily losing work.
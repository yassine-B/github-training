# Module 1 — Code Tab
# Lesson 19: Advanced Git Configuration, Aliases, Attributes and Ignore Rules

**Filename:** `docs/github/module-01-code/lesson-19-git-configuration.md`

**Suggested branch:** `docs/add-git-configuration-lesson`

**Level:** Advanced

**Practice repository:** `github-deep-dive-training`

---

# 1. Learning objectives

By the end of this lesson, you should be able to:

- Understand Git configuration files and scopes.
- Configure Git globally and locally.
- Understand configuration precedence.
- Inspect configuration origins.
- Create custom Git aliases.
- Configure default branch names.
- Configure commit signing preferences.
- Understand `.gitignore` patterns.
- Ignore environment files and generated files.
- Understand `.gitattributes`.
- Configure line-ending normalization.
- Configure text and binary file handling.
- Understand diff and merge attributes.
- Configure reusable Git settings for teams.
- Build a professional Git configuration standard.

# 2. Understanding Git configuration

Git is highly configurable.

You can customize:

- Your identity.
- Default branch names.
- Commit behavior.
- Merge behavior.
- Pull behavior.
- Diff behavior.
- Line endings.
- Aliases.
- Credential helpers.
- Signing preferences.
- Repository-specific settings.

Git configuration is stored in configuration files.

The main configuration scopes are:

| Scope | Location | Applies to |
|---|---|---|
| System | System Git configuration file | All users and repositories on the system |
| Global | User's Git configuration file | All repositories belonging to the user |
| Local | Repository `.git/config` | One repository |
| Worktree | Worktree-specific Git configuration | One linked worktree |

There is also command-level configuration using `git -c`, which applies to an individual Git command.

# 3. Inspect Git configuration

## 3.1 View all configuration

```bash
git config --list
```

View global configuration:

```bash
git config --global --list
```

View repository configuration:

```bash
git config --local --list
```

View system configuration:

```bash
git config --system --list
```

Note: System configuration may require elevated permissions.

## 3.2 Find where a configuration value comes from

One of the most useful diagnostic commands:

```bash
git config --list --show-origin
```

This shows the configuration file that supplied each value.

For newer Git versions, you can also inspect configuration scope:

```bash
git config --list --show-origin --show-scope
```

Example:

```text
global  file:C:/Users/Developer/.gitconfig  user.name=Developer
global  file:C:/Users/Developer/.gitconfig  init.defaultBranch=main
local   file:.git/config                    core.repositoryformatversion=0
```

This is particularly useful when two configuration files define the same setting.

## 3.3 Read a specific configuration

```bash
git config user.name
git config user.email
git config init.defaultBranch
```

Inspect a setting's origin:

```bash
git config --show-origin --get user.name
```

Inspect all values for a multivalued setting:

```bash
git config --get-all core.excludesfile
```

# 4. Configuration precedence

Git can read multiple configuration sources.

Generally, more specific configuration overrides less specific configuration.

A simplified order from lower to higher priority:

1. System configuration.
2. Global configuration.
3. Local repository configuration.
4. Worktree configuration, when enabled.
5. Command-level configuration.

Environment variables and command-specific options can also affect configuration behavior.

For example, define your global identity:

```bash
git config --global user.name "Developer Global"
git config --global user.email "global@example.com"
```

Inside a repository, define another identity:

```bash
git config --local user.name "Project Developer"
git config --local user.email "project@example.com"
```

Check the effective value:

```bash
git config user.name
git config user.email
```

Expected:

```text
Project Developer
project@example.com
```

The local configuration takes precedence over the global configuration.

You can also override a setting for one command:

```bash
git -c user.name="Temporary Developer" config user.name
```

This does not permanently change the configuration files.

## 4.1 Configuration precedence exercise

1. Configure a global username.
2. Configure a different local username.
3. Inspect the effective username.
4. Inspect the origin.
5. Override it using `git -c`.
6. Inspect the effective value again.

Commands:

```bash
git config --global user.name "Global Developer"
git config --local user.name "Repository Developer"

git config user.name

git config --show-origin --get user.name

git -c user.name="Temporary Developer" config user.name
```

Explain which value is used in each situation.

# 5. Configure your Git identity

## 5.1 Global identity

Configure your normal identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Check:

```bash
git config --global --list
```

## 5.2 Repository-specific identity

For a particular repository:

```bash
git config --local user.name "Company Developer"
git config --local user.email "developer@company.com"
```

This is useful when maintaining separate personal and professional identities.

## 5.3 Configure the default branch

Set the default branch for newly initialized repositories:

```bash
git config --global init.defaultBranch main
```

This does not rename branches in existing repositories.

To rename an existing local branch:

```bash
git branch -m master main
```

If the branch is already published, coordinate the remote rename and update the repository's default branch on GitHub.

# 6. Configure Git aliases

Aliases allow you to create shortcuts for frequently used commands.

For example:

Instead of:

```bash
git status
```

You can use:

```bash
git st
```

## 6.1 Create basic aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

Usage:

```bash
git st
git br
git co main
```

For new workflows, prefer `switch` and `restore` over using `checkout` for every operation.

## 6.2 Create a history alias

```bash
git config --global alias.lg "log --oneline --graph --decorate --all"
```

Execute:

```bash
git lg
```

This gives you a compact visualization of repository history.

## 6.3 Create useful advanced aliases

```bash
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.unstage "restore --staged"
git config --global alias.amend "commit --amend"
git config --global alias.branches "branch -avv"
git config --global alias.tags "tag --list"
git config --global alias.root "rev-parse --show-toplevel"
git config --global alias.aliases "config --get-regexp ^alias\\."
```

Usage:

```bash
git last
git unstage README.md
git branches
git root
git aliases
```

Be careful with the `amend` alias: amending a commit changes its commit ID and should not be used casually on shared history.

## 6.4 Create a custom alias with shell execution

Git aliases can execute shell commands when prefixed with `!`.

Example:

```bash
git config --global alias.current-branch "!git branch --show-current"
```

Usage:

```bash
git current-branch
```

Another example:

```bash
git config --global alias.clean-branches "!git branch --merged"
```

This lists branches already merged into the current branch. Inspect the output before deleting any branch.

# 7. Manage configuration files

## 7.1 Global configuration file

On Windows, the global configuration is commonly located at:

```text
C:\Users\<USERNAME>\.gitconfig
```

On Linux/macOS:

```text
~/.gitconfig
```

You can open it using:

```bash
git config --global --edit
```

Example configuration:

```ini
[user]
    name = Your Name
    email = your-email@example.com

[init]
    defaultBranch = main

[core]
    autocrlf = false

[alias]
    st = status
    lg = log --oneline --graph --decorate --all
    last = log -1 HEAD --stat
    branches = branch -avv
```

This is an example configuration, not a universal configuration for every operating system.

## 7.2 Repository configuration

Inside your repository:

```bash
git config --local --edit
```

The file is commonly:

```text
.git/config
```

Example:

```ini
[core]
    repositoryformatversion = 0

[remote "origin"]
    url = https://github.com/USERNAME/REPOSITORY.git
    fetch = +refs/heads/*:refs/remotes/origin/*

[branch "main"]
    remote = origin
    merge = refs/heads/main
```

Git manages many entries automatically.

Do not manually change remote or branch configuration unless you understand the effect.

# 8. Conditional configuration

Conditional includes allow Git to load different settings depending on the repository location.

This is useful when you maintain:

- Personal projects.
- Company projects.
- Open-source contributions.
- Client repositories.

For example, your global `.gitconfig` can contain:

```ini
[includeIf "gitdir/i:C:/Users/Developer/Projects/Personal/"]
    path = ~/.gitconfig-personal

[includeIf "gitdir/i:C:/Users/Developer/Projects/Company/"]
    path = ~/.gitconfig-company
```

Then create:

`.gitconfig-personal`

```ini
[user]
    name = Personal Developer
    email = personal@example.com
```

`.gitconfig-company`

```ini
[user]
    name = Company Developer
    email = developer@company.com
```

Git loads the relevant configuration when operating inside matching repositories.

Important:

- Adapt paths to your actual directory structure.
- The `gitdir/i` form performs case-insensitive matching.
- Test the configuration using `git config --show-origin --get user.email`.
- Do not assume the configuration will automatically change the identity of existing commits.

# 9. Understanding .gitignore

`.gitignore` tells Git which untracked files and directories to ignore.

It is essential for preventing accidental commits of:

- Environment files.
- Python virtual environments.
- Node dependencies.
- Build output.
- Logs.
- Cache files.
- IDE-specific files.
- Temporary files.

## 9.1 Create a .gitignore file

At the root of your repository:

```text
.gitignore
```

Example:

```gitignore
# Environment variables
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.pyo
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
env/

# Django
staticfiles/
media/
*.sqlite3

# Node
node_modules/
dist/
build/
coverage/

# React / Vite
.vite/

# Logs
*.log
logs/

# IDE
.idea/
.vscode/

# Operating systems
.DS_Store
Thumbs.db
Desktop.ini

# Temporary files
*.tmp
*.temp
```

This is a starting example. Your actual ignore rules should match the project's architecture and generated files.

## 9.2 Understand ignore patterns

| Pattern | Meaning |
|---|---|
| `*.log` | Ignore files ending in `.log` |
| `/dist/` | Ignore root-level `dist` |
| `dist/` | Ignore directories named `dist` at any level |
| `temp/` | Ignore matching directories |
| `!file.txt` | Re-include a file |
| `**/cache/` | Match cache directories at any depth |
| `*.env` | Ignore files ending in `.env` |

A leading slash anchors a pattern to the directory containing that `.gitignore`.

## 9.3 Ignore a specific directory

```gitignore
node_modules/
```

## 9.4 Ignore everything inside a directory except one file

```gitignore
uploads/*
!uploads/.gitkeep
```

This allows the directory to remain represented in Git through `.gitkeep`.

For nested ignored directories, Git may require re-including the parent directory before re-including a child.

## 9.5 Check whether a file is ignored

```bash
git check-ignore -v .env
```

This shows the ignore rule responsible for ignoring the file.

Check all ignored files:

```bash
git status --ignored
```

## 9.6 Important: .gitignore does not untrack files

Suppose you already committed:

```text
.env
```

Adding it to `.gitignore` does not remove it from Git tracking.

You must remove it from the index:

```bash
git rm --cached .env
```

Then commit the change:

```bash
git commit -m "chore: stop tracking environment file"
```

The local file remains on disk.

**Security warning:** If an actual secret has already been pushed, removing the file from Git tracking is not sufficient. Rotate the exposed credential and assess whether history cleanup is necessary.

# 10. Global Git ignore rules

Sometimes you want to ignore files across all repositories.

For example:

- OS metadata.
- Personal editor settings.
- Personal temporary files.

Create:

```text
~/.gitignore_global
```

Example:

```gitignore
.DS_Store
Thumbs.db
*.swp
*.swo
.idea/
```

Configure Git:

```bash
git config --global core.excludesfile ~/.gitignore_global
```

On Windows, use a valid path to the file in your user directory.

Inspect:

```bash
git config --show-origin --get core.excludesfile
```

Difference:

| File | Scope |
|---|---|
| `.gitignore` | Shared repository rules |
| `.git/info/exclude` | Local repository-specific rules |
| Global excludes file | Personal rules across repositories |

Global ignore rules should not hide files that the entire team needs to manage.

# 11. Understanding .gitattributes

`.gitattributes` defines attributes for files and paths.

Unlike `.gitignore`, it does not primarily determine whether files are tracked.

It controls how Git handles files.

Examples:

- Line endings.
- Text normalization.
- Binary files.
- Diff behavior.
- Merge behavior.
- Export behavior.

Create:

```text
.gitattributes
```

## 11.1 Normalize text files

Example:

```gitattributes
* text=auto
```

This allows Git to detect text files and normalize line endings in the repository.

You can define more explicit rules:

```gitattributes
*.py text eol=lf
*.js text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.json text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf

*.bat text eol=crlf
*.cmd text eol=crlf
```

This makes the expected line-ending convention explicit.

## 11.2 Understand LF and CRLF

Two common line-ending formats:

| Format | Description |
|---|---|
| LF | Line Feed, commonly used on Linux/macOS |
| CRLF | Carriage Return + Line Feed, commonly used on Windows |

Inconsistent line endings can cause large unnecessary diffs.

Example:

A developer changes one line in a file, but Git detects every line as changed because line endings were converted.

Using `.gitattributes` helps prevent this.

## 11.3 Normalize an existing repository

After introducing suitable `.gitattributes` rules:

```bash
git add --renormalize .
```

Inspect:

```bash
git status
git diff --cached
```

Review the changes carefully before committing.

This operation may produce changes across many files.

Do not blindly commit a large normalization diff.

# 12. Mark binary files

Binary files should generally not undergo text line-ending normalization.

Example:

```gitattributes
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.pdf binary
*.zip binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
```

The `binary` macro is equivalent to disabling text conversion and text diff treatment.

This helps Git avoid treating binary data as ordinary text.

# 13. Configure diff behavior

You can control how Git handles diffs for particular file types.

For example:

```gitattributes
*.md diff
*.py diff
*.js diff
*.ts diff
```

Git already recognizes many common text formats, so these rules are often unnecessary. They demonstrate the attribute mechanism.

For JSON files, Git can show a normal text diff:

```bash
git diff -- path/to/file.json
```

Inspect attribute application:

```bash
git check-attr diff -- README.md
```

Inspect all attributes for a file:

```bash
git check-attr --all -- README.md
```

# 14. Configure merge behavior

Git supports different merge strategies and attributes.

A common example is a file that should not be merged automatically.

```gitattributes
*.lock merge=binary
```

However, use this carefully.

A binary merge setting prevents ordinary text merging and can require manual conflict resolution.

For generated lockfiles, the correct approach is normally to regenerate or resolve the file using its package manager, not to treat every conflict as a binary file.

## 14.1 Custom merge drivers

Git also supports custom merge drivers.

Example attribute:

```gitattributes
*.custom merge=mydriver
```

The corresponding driver can be configured:

```bash
git config merge.mydriver.driver "custom-merge-command %O %A %B %L %P"
```

Placeholders include:

| Placeholder | Meaning |
|---|---|
| `%O` | Common ancestor version |
| `%A` | Current version and merge result destination |
| `%B` | Other branch version |
| `%L` | Conflict marker size |
| `%P` | Path being merged |

The example command above is illustrative, not an executable driver. A real driver must exist, be correctly installed, and follow Git's merge-driver contract.

Custom merge drivers are useful for specialized formats, but should be introduced only when the team can maintain and test them.

# 15. Other useful Git attributes

## 15.1 export-ignore

Exclude files from archives generated using `git archive`.

Example:

```gitattributes
/docs/internal/ export-ignore
/tests/ export-ignore
```

This does not delete these files from GitHub or from the repository. It affects archive generation.

## 15.2 export-subst

Allow placeholders in tracked files to be substituted when creating an archive.

Example:

```gitattributes
VERSION.txt export-subst
```

A file can contain:

```text
Commit: $Format:%H$
```

When exported through the relevant Git archive mechanism, the placeholder can be replaced with commit information.

## 15.3 linguist attributes

GitHub supports additional attributes used by GitHub Linguist.

Example:

```gitattributes
*.generated.ts linguist-generated=true
```

This can help GitHub distinguish generated files from manually maintained source code in repository language statistics and diffs.

These are GitHub-specific extensions, not general Git behavior.

# 16. Configure line endings with core.autocrlf

Git has a configuration setting:

```bash
git config --global core.autocrlf
```

Common values:

| Value | Behavior |
|---|---|
| `true` | Convert LF to CRLF when checking out on supported platforms; normalize text to LF when committing |
| `input` | Normalize CRLF to LF when committing; do not convert LF to CRLF on checkout |
| `false` | Disable automatic conversion |

For teams, explicit `.gitattributes` rules are generally more predictable than relying only on different individual configurations.

Example:

```bash
git config --global core.autocrlf false
```

This is a possible configuration, not a universal requirement.

Your repository's `.gitattributes` should define the team's expected line-ending behavior.

# 17. Git configuration for DRF + React projects

Let's create a practical configuration standard for a project with:

- Django REST Framework backend.
- React frontend.
- Vite.
- TypeScript.
- PostgreSQL.
- Docker.
- Environment configuration.
- Documentation.

## 17.1 Recommended repository structure

```text
project/
├── backend/
├── frontend/
├── docker/
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── .gitattributes
├── .editorconfig
├── docker-compose.yml
└── README.md
```

## 17.2 Example .gitignore

```gitignore
# Environment files
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/

# Django
staticfiles/
media/
*.sqlite3

# Node
node_modules/
dist/
build/
.vite/
coverage/

# Docker / temporary data
*.pid

# Logs
*.log
logs/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db
Desktop.ini

# Temporary files
*.tmp
*.temp
```

Important: Do not ignore files such as `docker-compose.yml`, `Dockerfile`, dependency lockfiles, or migration files simply because they are generated or used by tools.

## 17.3 Example .gitattributes

```gitattributes
# Automatic text detection
* text=auto

# Backend
*.py text eol=lf
*.toml text eol=lf
*.ini text eol=lf

# Frontend
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.css text eol=lf
*.html text eol=lf
*.json text eol=lf

# Configuration
*.yml text eol=lf
*.yaml text eol=lf
*.sh text eol=lf
*.env.example text eol=lf

# Documentation
*.md text eol=lf

# Windows scripts
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.webp binary
*.pdf binary
*.woff binary
*.woff2 binary
*.zip binary
```

Review this against the actual files in your project.

## 17.4 Example .editorconfig

Although EditorConfig is not a Git feature, it complements Git configuration by standardizing editor behavior.

Create:

`.editorconfig`

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

[*.{yml,yaml,json}]
indent_style = space
indent_size = 2

[*.{py}]
indent_style = space
indent_size = 4

[*.{js,jsx,ts,tsx,css,html}]
indent_style = space
indent_size = 2
```

This helps developers use consistent formatting across editors.

---

# Part 18 — Advanced Git configuration features

## 18. Conditional includes and worktrees

If you use multiple Git worktrees, you can enable worktree-specific configuration:

```bash
git config extensions.worktreeConfig true
```

This is an advanced repository-level setting.

After enabling it, worktree-specific configuration can be maintained separately.

Inspect the current worktree:

```bash
git worktree list
```

Inspect worktree-specific configuration:

```bash
git config --worktree --list
```

Only use this after understanding linked worktrees and their configuration behavior.

## 18.1 Configure pull behavior

Git can be configured to use different pull strategies.

Rebase:

```bash
git config --global pull.rebase true
```

Merge:

```bash
git config --global pull.rebase false
```

Fast-forward only:

```bash
git config --global pull.ff only
```

These represent different collaboration policies.

| Setting | Behavior |
|---|---|
| `pull.rebase=true` | Rebase local commits on top of fetched upstream commits |
| `pull.rebase=false` | Merge fetched changes |
| `pull.ff=only` | Allow pull only when it can fast-forward |

Do not configure multiple conflicting policies without understanding their precedence and interaction.

Choose the policy that matches your team's workflow.

## 18.2 Configure push behavior

A useful option:

```bash
git config --global push.autoSetupRemote true
```

This allows Git to automatically set up the upstream when pushing a new branch in supported situations.

Another setting:

```bash
git config --global push.default simple
```

This is a common default for straightforward branch publishing.

## 18.3 Configure fetch pruning

```bash
git config --global fetch.prune true
```

This removes stale remote-tracking references when their corresponding remote branches no longer exist.

It does not delete your local branches.

## 18.4 Configure commit signing preference

Git can sign commits using supported signing mechanisms.

For example, with GPG:

```bash
git config --global commit.gpgsign true
```

Configure the signing key:

```bash
git config --global user.signingkey <KEY_ID>
```

For SSH-based signing, Git supports an SSH signing format:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

You must have the appropriate signing key and verification configuration.

Do not copy private signing keys into repositories.

Commit signing is covered more extensively in a dedicated security lesson.

---

# Part 19 — Diagnose configuration problems

## 19. Common problems and solutions

### Problem 1: Git ignores a file that should be committed

Inspect:

```bash
git check-ignore -v path/to/file
```

Possible causes:

- A `.gitignore` rule.
- A global excludes file.
- `.git/info/exclude`.

### Problem 2: A secret file is already tracked

Inspect:

```bash
git ls-files .env
```

Remove it from the index:

```bash
git rm --cached .env
```

Add the correct ignore rule and commit.

If it contained a real credential, rotate that credential.

### Problem 3: Git displays every line as modified

Possible cause: inconsistent line endings.

Inspect:

```bash
git config --show-origin --get core.autocrlf
git check-attr text eol -- README.md
```

Inspect the diff:

```bash
git diff --ignore-space-at-eol
```

Review `.gitattributes` and normalize carefully if necessary.

### Problem 4: Wrong Git username in commits

Inspect:

```bash
git config --show-origin --get user.name
git config --show-origin --get user.email
```

Check global and local configuration.

Correct the intended scope:

```bash
git config --local user.name "Correct Name"
git config --local user.email "correct@example.com"
```

Changing configuration does not alter existing commits.

### Problem 5: An alias does not work

Inspect:

```bash
git config --get-regexp '^alias\.'
```

Check:

- Alias spelling.
- Quoting.
- Shell execution syntax.
- Whether the alias conflicts with an existing Git command.

---

# Part 20 — Practical exercises

## Exercise 1: Configuration scopes

1. Set a global username.
2. Set a global email.
3. Set a different repository username.
4. Inspect effective values.
5. Inspect origins and scopes.
6. Override a value using `git -c`.

Deliverable:

Explain configuration precedence with command outputs.

## Exercise 2: Build your alias collection

Create these aliases:

```bash
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --decorate --all"
git config --global alias.last "log -1 HEAD --stat"
git config --global alias.branches "branch -avv"
git config --global alias.root "rev-parse --show-toplevel"
git config --global alias.unstage "restore --staged"
```

Test each alias.

Deliverable:

Create a table containing alias, underlying command, and purpose.

## Exercise 3: Build .gitignore

In a disposable repository:

Create files and directories representing:

- `.env`
- `.venv/`
- `node_modules/`
- `dist/`
- `coverage/`
- `README.md`
- `.env.example`

Create a `.gitignore`.

Verify ignored files:

```bash
git status --ignored
git check-ignore -v .env
git check-ignore -v node_modules/
```

Verify that `.env.example` is not ignored.

Deliverable:

Explain every ignore pattern.

## Exercise 4: Understand already-tracked files

1. Create a file called `secret-placeholder.txt`.
2. Commit it.
3. Add it to `.gitignore`.
4. Check whether Git still tracks it.
5. Remove it from the index using `git rm --cached`.
6. Commit the change.

Use placeholder data only. Never use actual secrets.

Deliverable:

Explain why `.gitignore` did not remove the file from tracking.

## Exercise 5: Configure .gitattributes

Create a `.gitattributes` file with:

```gitattributes
* text=auto
*.py text eol=lf
*.js text eol=lf
*.md text eol=lf
*.bat text eol=crlf
*.png binary
*.pdf binary
```

Inspect:

```bash
git check-attr --all -- README.md
git check-attr --all -- image.png
```

Deliverable:

Explain the difference between text and binary handling.

## Exercise 6: Conditional configuration

1. Create a personal projects directory.
2. Create a company projects directory.
3. Create two separate configuration files.
4. Add conditional includes to your global `.gitconfig`.
5. Initialize a repository in each directory.
6. Inspect the effective username and email.
7. Inspect the configuration origin.

Deliverable:

Demonstrate how Git selects the appropriate identity.

## Exercise 7: Pull and push policies

Experiment with:

```bash
git config --local pull.rebase true
git config --local pull.rebase false
git config --local pull.ff only
git config --local push.default simple
git config --local fetch.prune true
```

Inspect each setting:

```bash
git config --local --list
```

Do not change the policy of a production repository without understanding the consequences.

Deliverable:

Write an explanation of the different pull strategies.

## Exercise 8: Create a team Git configuration standard

Prepare a reusable standard containing:

- Global identity recommendations.
- Local identity requirements.
- Alias recommendations.
- `.gitignore` standards.
- `.gitattributes` standards.
- Line-ending policy.
- Pull and push policy.
- Commit signing policy.
- Configuration troubleshooting commands.

Deliverable:

Create a team standards document.

---

# Part 21 — Add the lesson to your GitHub training repository

## 21. Create the lesson branch

In your `github-deep-dive-training` repository:

```bash
git switch main
git pull origin main
git switch -c docs/add-git-configuration-lesson
```

## 21.1 Files to create

Create:

```text
docs/
└── github/
    └── module-01-code/
        ├── lesson-19-git-configuration.md
        ├── standards/
        │   └── git-configuration-standards.md
        └── exercises/
            └── lesson-19-configuration-lab.md
```

### File 1: lesson-19-git-configuration.md

Paste this complete lesson.

### File 2: git-configuration-standards.md

Use this template:

```markdown
# Team Git Configuration Standards

## 1. Identity

- Use a consistent professional Git identity.
- Configure repository-specific identity when needed.
- Never commit credentials.

## 2. Branch configuration

- Default branch: main.
- Use descriptive feature branch names.
- Avoid rewriting shared history.

## 3. Aliases

Recommended aliases:

- st
- lg
- last
- branches
- root
- unstage

## 4. Ignore rules

- Ignore environment files.
- Ignore generated files.
- Ignore dependency directories.
- Keep example environment files.

## 5. Attributes

- Normalize text files.
- Use explicit line-ending rules.
- Mark binary files appropriately.

## 6. Pull and push policy

- Follow the team's selected integration strategy.
- Avoid force-pushing shared branches.
- Remove stale remote-tracking references when appropriate.

## 7. Commit signing

- Follow the team's signing policy.
- Protect private signing keys.

## 8. Repository hygiene

- Review ignored files.
- Review configuration origins.
- Keep repository configuration documented.
```

### File 3: lesson-19-configuration-lab.md

Document your eight practical exercises.

Include:

- Commands executed.
- Configuration values.
- Screenshots or terminal outputs where useful.
- Explanation of results.
- Problems encountered.
- Solutions.

---

# Part 22 — Commit and push

## 22. Review your changes

```bash
git status
git diff --check
```

Stage:

```bash
git add docs/github/module-01-code/lesson-19-git-configuration.md

git add docs/github/module-01-code/standards/git-configuration-standards.md

git add docs/github/module-01-code/exercises/lesson-19-configuration-lab.md
```

Inspect staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add advanced git configuration lesson"
```

Push:

```bash
git push -u origin docs/add-git-configuration-lesson
```

## 22.1 Pull request

**Title:**

```text
docs(github): add lesson 19 — advanced git configuration
```

**Description:**

```markdown
## Summary

Adds Lesson 19 to the GitHub Deep Dive training.

## Topics

- Git configuration scopes
- Configuration precedence
- Global and local settings
- Git aliases
- Conditional configuration
- .gitignore
- .gitattributes
- Line-ending normalization
- Binary files
- Diff and merge attributes
- Pull and push configuration
- Commit signing preferences

## Practical exercises

- [ ] Configuration scopes
- [ ] Alias collection
- [ ] .gitignore
- [ ] Already-tracked files
- [ ] .gitattributes
- [ ] Conditional configuration
- [ ] Pull and push policies
- [ ] Team configuration standards

## Documentation

- [ ] Lesson documentation
- [ ] Git configuration standards
- [ ] Exercise report

## Verification

- [ ] Commands tested
- [ ] Markdown reviewed
- [ ] No secrets committed
```

Review and merge the PR.

---

# Part 23 — Tag and GitHub Release

## 23. Create an annotated tag

After merging:

```bash
git switch main
git pull origin main
```

Check whether the tag already exists:

```bash
git tag --list module-01-lesson-19
```

Create:

```bash
git tag -a module-01-lesson-19 -m "Module 1 Lesson 19: Advanced Git Configuration"
```

Push:

```bash
git push origin module-01-lesson-19
```

Verify:

```bash
git show module-01-lesson-19
```

## 23.1 Publish the GitHub Release

Go to:

`github-deep-dive-training → Releases → Draft a new release`

**Tag:**

```text
module-01-lesson-19
```

**Release title:**

```text
Module 1 — Lesson 19: Advanced Git Configuration
```

**Release description:**

```markdown
# Module 1 — Lesson 19

## Topics

- Git configuration scopes and precedence
- Global and local configuration
- Git aliases
- Conditional configuration
- .gitignore
- Global ignore rules
- .gitattributes
- LF and CRLF
- Binary file handling
- Diff and merge attributes
- Pull and push behavior
- Commit signing preferences
- Git configuration troubleshooting

## Practical exercises

- Configuration scopes
- Alias collection
- Ignore rules
- Already-tracked files
- File attributes
- Conditional configuration
- Pull and push policies
- Team configuration standards

## Deliverables

- Lesson 19 documentation
- Team Git configuration standards
- Configuration laboratory report
```

Publish the release.

---

# Part 24 — Completion checklist

- [ ] Understand Git configuration scopes.
- [ ] Understand configuration precedence.
- [ ] Inspect configuration origins.
- [ ] Configure global and local identity.
- [ ] Configure the default branch.
- [ ] Create Git aliases.
- [ ] Understand conditional includes.
- [ ] Understand `.gitignore`.
- [ ] Configure global ignore rules.
- [ ] Understand why ignored files can remain tracked.
- [ ] Understand `.gitattributes`.
- [ ] Understand LF and CRLF.
- [ ] Normalize text files.
- [ ] Mark binary files.
- [ ] Understand diff and merge attributes.
- [ ] Configure pull and push behavior.
- [ ] Understand commit signing configuration.
- [ ] Complete all eight practical exercises.
- [ ] Create team configuration standards.
- [ ] Create the lab report.
- [ ] Open and merge the PR.
- [ ] Create the annotated tag.
- [ ] Publish the GitHub Release.

---

# Official documentation

1. Git Configuration: https://git-scm.com/docs/git-config
2. Git Ignore: https://git-scm.com/docs/gitignore
3. Git Attributes: https://git-scm.com/docs/gitattributes
4. Git Check Ignore: https://git-scm.com/docs/git-check-ignore
5. Git Check Attr: https://git-scm.com/docs/git-check-attr
6. Git Aliases: https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases
7. Git Worktrees: https://git-scm.com/docs/git-worktree
8. GitHub Ignoring Files: https://docs.github.com/en/get-started/git-basics/ignoring-files

---

# Next lesson

**Module 1 — Lesson 20: Advanced Git Workflows — Cherry-pick, Rebase, Interactive Rebase, Squash and Bisect**

Planned topics:

- Cherry-picking commits.
- Applying commits between branches.
- Interactive rebase.
- Reordering commits.
- Squashing commits.
- Editing commit messages.
- Splitting commits.
- Dropping commits.
- Fixup and autosquash.
- Git bisect.
- Finding the commit that introduced a bug.
- Rewriting history safely.
- Recovering from incorrect history operations.
- Practical team workflow simulations.
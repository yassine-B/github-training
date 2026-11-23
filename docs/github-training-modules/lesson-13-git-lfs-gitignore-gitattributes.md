# Lesson 13 — Git LFS, .gitignore, .gitattributes, and Large File Management

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain how Git stores files.
- Understand why large binary files can make repositories difficult to maintain.
- Install and configure Git Large File Storage (Git LFS).
- Track selected files using Git LFS.
- Configure `.gitignore` correctly.
- Understand why `.gitignore` does not remove files already tracked by Git.
- Configure `.gitattributes`.
- Handle line endings consistently across Windows, Linux, and macOS.
- Prevent generated files and sensitive local files from entering Git.
- Diagnose common problems involving ignored files and Git LFS.

## 2. Why file management matters

Imagine you are developing a Django REST Framework + React application.

Your repository might contain:

```text
restaurant-system/
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── venv/
│   ├── __pycache__/
│   └── media/
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── node_modules/
│   └── dist/
│
├── database/
│   └── development-backup.sql
│
├── uploads/
│   └── product-images/
│
└── .git/
```

Not every file in this structure belongs in Git.

For example:

| File or directory | Normally commit? | Reason |
|---|---|---|
| Python source code | Yes | Application source |
| React source code | Yes | Application source |
| `requirements.txt` | Yes | Python dependencies |
| `package-lock.json` | Yes | Reproducible frontend dependencies |
| `venv/` | No | Local Python environment |
| `node_modules/` | No | Installed dependencies |
| `__pycache__/` | No | Generated Python cache |
| `dist/` | Usually no | Generated build output |
| `.env` | No | May contain secrets |
| `.env.example` | Yes | Documents required configuration |
| Local database | Usually no | Local development data |
| User-uploaded media | Usually no | Application data, not source code |
| Small project logo | Usually yes | Project asset |
| Large design/video assets | Depends | May require Git LFS or external storage |

The objective is to keep your Git repository focused on source code, configuration, documentation, and intentionally versioned assets.

---

# Part 1 — Understanding Git file storage

## 3. How Git stores files

Git stores repository content as objects.

The main object types are:

- Blob: file content.
- Tree: directory structure and references to files.
- Commit: a snapshot reference, including metadata and parent commit information.
- Annotated tag: a named reference with additional metadata.

When you commit a file, Git stores its content in the repository's object database.

Git is particularly efficient with text files because it can identify unchanged content and store new versions efficiently.

However, binary files can be more problematic.

Examples include:

- Large images.
- Videos.
- Audio files.
- Design files.
- Large PDFs.
- 3D models.
- Machine-learning model files.

A small change to a binary file can result in Git storing another complete version of that file rather than a compact textual difference.

For example:

```text
product-design.psd

Version 1: 120 MB
Version 2: 122 MB
Version 3: 121 MB
Version 4: 123 MB
```

Even if the changes are small, multiple versions can increase repository storage significantly.

This is one reason Git LFS exists.

---

# Part 2 — Git Large File Storage (Git LFS)

## 4. What is Git LFS?

Git LFS stands for Git Large File Storage.

It is an extension that allows Git to manage large files without storing their full contents directly as ordinary Git blobs in every commit.

Instead:

1. Git stores a small pointer file in the repository.
2. The actual large file is stored in LFS storage.
3. Git LFS retrieves the actual file when needed.

Conceptually:

```text
Normal Git repository
│
├── Source code
├── Documentation
├── Configuration
└── Pointer to large asset
          |
          v
      Git LFS storage
          |
          v
      Actual large asset
```

### 4.1 Normal Git versus Git LFS

| Normal Git | Git LFS |
|---|---|
| Stores file contents in Git objects | Stores large content in LFS storage |
| Suitable for source code | Suitable for selected large binary files |
| Git repository contains actual file data | Git repository contains pointer files |
| Can become inefficient with frequently changing large binaries | Better suited to large binary versioning |

### 4.2 When should you use Git LFS?

Good candidates:

- Large Photoshop files.
- Large design source files.
- Large video files needed by the project.
- Large audio files.
- Large 3D assets.
- Large binary datasets that genuinely need version history.

Do not automatically use LFS for every large file.

For example, a restaurant application should generally store customer-uploaded images in object storage or another media storage system, not in Git LFS.

Git LFS is intended for versioned project assets, not as a replacement for application file storage.

## 5. Install Git LFS on Windows

First, verify whether it is installed:

```bash
git lfs version
```

If Git reports that the command is unavailable, install Git LFS.

One Windows installation option is:

```powershell
winget install GitHub.GitLFS
```

Alternatively, use the official installation instructions:

https://git-lfs.com/

After installation, close and reopen your terminal.

Verify:

```bash
git lfs version
```

## 6. Initialize Git LFS

Inside your repository:

```bash
git lfs install
```

This configures Git LFS for your user environment and installs the required Git hooks.

You normally perform this once per user environment.

You can inspect the configuration with:

```bash
git lfs env
```

This displays information about your Git LFS environment and configuration.

## 7. Track files using Git LFS

Suppose your project contains:

```text
assets/
├── restaurant-design.psd
├── promotional-video.mp4
└── restaurant-logo.png
```

You decide that the PSD and video should be managed by Git LFS.

Run:

```bash
git lfs track "*.psd"
git lfs track "*.mp4"
```

Git LFS updates or creates:

```text
.gitattributes
```

It may contain:

```gitattributes
*.psd filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
```

The `-text` attribute tells Git not to apply text line-ending conversion to those binary files.

**Important:** Commit `.gitattributes`. Other contributors need this configuration when they clone the repository.

Now add your files:

```bash
git add .gitattributes
git add assets/restaurant-design.psd
git add assets/promotional-video.mp4
```

Commit:

```bash
git commit -m "chore(assets): track design files with git lfs"
```

Push:

```bash
git push origin main
```

The Git LFS pre-push hook normally uploads the required LFS objects during the push.

If you use a custom Git workflow or encounter an upload issue, inspect Git LFS documentation and the push output rather than assuming the large files were uploaded successfully.

## 8. Verify which files use Git LFS

List tracked LFS patterns:

```bash
git lfs track
```

List files currently managed by LFS:

```bash
git lfs ls-files
```

Inspect LFS status:

```bash
git lfs status
```

Inspect LFS environment information:

```bash
git lfs env
```

### 8.1 Understand the pointer file

Git LFS stores a pointer in the ordinary Git repository.

A simplified pointer looks like:

```text
version https://git-lfs.github.com/spec/v1
oid sha256:EXAMPLE_CONTENT_HASH
size 125829120
```

This is not the actual image or video.

It identifies the external LFS object using its content hash and size.

If LFS content is unavailable, you may see the pointer instead of the actual file.

## 9. Clone a repository that uses Git LFS

Normally, when Git LFS is installed and configured, cloning a repository retrieves its LFS objects through the Git LFS smudge process.

Example:

```bash
git clone https://github.com/OWNER/REPOSITORY.git
```

If you intentionally want to clone without downloading the LFS objects immediately:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/OWNER/REPOSITORY.git
```

Then retrieve the files later:

```bash
git lfs pull
```

You can also fetch LFS content explicitly:

```bash
git lfs fetch origin main
```

And check out the downloaded content:

```bash
git lfs checkout
```

This can be useful when working with repositories containing many large assets.

## 10. Git LFS limitations and considerations

Git LFS has storage and bandwidth considerations.

Before adopting it for a team, check:

- Available LFS storage.
- Available bandwidth.
- File-size restrictions.
- Organization or repository billing arrangements.
- Backup and retention requirements.
- Whether every contributor has Git LFS installed.

Official documentation:

https://docs.github.com/en/repositories/working-with-files/managing-large-files

Do not assume Git LFS is unlimited or free for every repository and account.

## 11. Important: What if a large file was already committed?

Suppose you committed a large file normally:

```bash
git add assets/large-video.mp4
git commit -m "feat(assets): add promotional video"
```

Later, you execute:

```bash
git lfs track "*.mp4"
```

This does not automatically convert the existing committed file into an LFS object.

The tracking rule affects files added to Git after the rule is configured.

For a file that is already tracked, you may need to migrate its history.

### 11.1 Migration with Git LFS

Git LFS provides a migration command:

```bash
git lfs migrate import --include="*.mp4"
```

This can rewrite Git history to convert matching files into LFS-managed objects.

**Warning:** History rewriting changes commit identities. It can affect every contributor working with the repository.

Do not execute migration commands on a shared repository without:

1. Backing up the repository.
2. Understanding which branches and tags are affected.
3. Informing all contributors.
4. Planning the history rewrite.
5. Coordinating any required force push.

For a training repository, do not migrate your existing history just to practice.

For future files, configure LFS before adding and committing them.

---

# Part 3 — The .gitignore file

## 12. What is .gitignore?

`.gitignore` tells Git which untracked files and directories it should ignore.

For example:

```text
node_modules/
venv/
.env
__pycache__/
```

This means Git should not normally include those untracked paths when you run:

```bash
git status
```

A `.gitignore` file is normally placed at the repository root.

You can also have additional `.gitignore` files in subdirectories.

Example:

```text
restaurant-system/
│
├── .gitignore
│
├── backend/
│   └── .gitignore
│
└── frontend/
    └── .gitignore
```

However, for many projects, a carefully organized root `.gitignore` is enough.

## 13. Create a root .gitignore

For a Django + React project, create:

```text
.gitignore
```

Use the following example as a starting point:

```gitignore
# ==============================
# Environment variables / secrets
# ==============================

.env
.env.*
!.env.example
!.env.template

# ==============================
# Python
# ==============================

__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.venv/
env/
ENV/

# Python packaging
build/
dist/
*.egg-info/
.eggs/

# Test and coverage output
.pytest_cache/
.coverage
.coverage.*
htmlcov/
.tox/
.nox/

# Type checking and lint caches
.mypy_cache/
.pyright/
.ruff_cache/

# Django local files
local_settings.py
db.sqlite3
db.sqlite3-journal

# ==============================
# Node.js / React
# ==============================

node_modules/
dist/
build/
coverage/

.npm/
.pnpm-store/

# Vite cache
.vite/

# ==============================
# Logs
# ==============================

*.log
logs/

# ==============================
# Editors / IDEs
# ==============================

.vscode/
.idea/

# ==============================
# Operating systems
# ==============================

.DS_Store
Thumbs.db
Desktop.ini

# ==============================
# Temporary files
# ==============================

*.tmp
*.temp
*.swp
*.bak
```

### 13.1 Important notes about this example

Do not copy an ignore template blindly into every project.

Some projects intentionally commit `.vscode` configuration so that the whole team shares workspace recommendations.

Some projects intentionally commit build output.

Some projects use SQLite as a test fixture.

Some applications need particular generated files.

Adjust your ignore rules to match the actual project architecture.

For example, if you use a committed SQLite database as a test fixture, do not ignore that particular file without considering the testing workflow.

## 14. Understand .gitignore patterns

The syntax matters.

### Ignore a directory

```gitignore
node_modules/
```

Ignores directories named `node_modules`.

### Ignore a file extension

```gitignore
*.log
```

Ignores files ending in `.log`.

### Ignore a specific file

```gitignore
.env
```

Ignores a file named `.env` in the relevant directory scope.

### Ignore files beginning with a name

```gitignore
.env.*
```

Matches files such as:

```text
.env.local
.env.development
.env.production
```

### Allow a particular file

```gitignore
.env.*
!.env.example
```

The second line negates the previous matching rule for `.env.example`.

### Ignore a directory only at the repository root

```gitignore
/build/
```

This targets the root-level `build` directory.

### Ignore a nested directory

```gitignore
backend/uploads/
```

Ignores that path relative to the `.gitignore` location.

### Ignore everything in a directory but keep one file

```gitignore
reports/*
!reports/README.md
```

This ignores files inside `reports` but keeps `README.md`.

If you need to re-include files inside an ignored parent directory, you may also need to re-include the parent directory itself.

## 15. Check why a file is ignored

Git provides a useful debugging command:

```bash
git check-ignore -v path/to/file
```

Example:

```bash
git check-ignore -v backend/__pycache__/models.cpython-313.pyc
```

This shows which ignore rule is responsible.

To inspect all ignored untracked files:

```bash
git status --ignored
```

To inspect only ignored files:

```bash
git status --short --ignored
```

This is useful when a file does not appear in your normal Git status output.

## 16. Important: .gitignore does not remove tracked files

This is one of the most common Git mistakes.

Suppose you committed `.env` before creating your `.gitignore`.

Then you add:

```gitignore
.env
```

Git will continue tracking the file because it is already part of the repository history.

To stop tracking it while keeping the local file:

```bash
git rm --cached .env
```

Commit the change:

```bash
git add .gitignore
git commit -m "chore(git): stop tracking local environment file"
```

After this:

- The file remains on your local machine.
- The file is removed from the current Git version.
- The ignore rule prevents it from being added again accidentally.

**Security warning:** If `.env` contained real passwords, API keys, or other secrets and was pushed to GitHub, removing it from the latest commit is not enough.

You must rotate or revoke the exposed credentials. Removing the file from Git history may also be necessary, but history rewriting requires careful coordination.

Treat an exposed credential as compromised.

---

# Part 4 — The .gitattributes file

## 17. What is .gitattributes?

`.gitattributes` controls how Git handles particular files and paths.

It can configure:

- Text and binary file identification.
- Line-ending conversion.
- Diff behavior.
- Merge behavior.
- Git LFS filters.
- GitHub language statistics and display behavior.

It is different from `.gitignore`.

| File | Responsibility |
|---|---|
| `.gitignore` | Determines which untracked files Git should ignore |
| `.gitattributes` | Controls how Git handles files it tracks |

For example:

```text
.gitignore
    -> Ignore node_modules/

.gitattributes
    -> Normalize Python and JavaScript files to LF
```

## 18. Understanding line endings

Different operating systems have historically used different line-ending conventions.

| Operating system | Line ending |
|---|---|
| Windows | CRLF |
| Linux | LF |
| macOS | LF |

CRLF means:

```text
\r\n
```

LF means:

```text
\n
```

This can create unnecessary differences when developers work on different operating systems.

Example:

Developer A uses Windows.

Developer B uses Linux.

Developer A edits a file and commits it with CRLF line endings.

Developer B edits the same file using LF.

Git may report many lines as changed even though the actual code did not change.

This creates noisy Pull Requests and makes code review more difficult.

## 19. Configure line endings using .gitattributes

Create:

```text
.gitattributes
```

For a typical cross-platform DRF + React project:

```gitattributes
# Normalize text files to LF in the repository
* text=auto eol=lf

# Windows scripts that require CRLF
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.mp4 binary
*.mp3 binary
*.woff binary
*.woff2 binary
*.ttf binary
*.otf binary
```

This establishes a consistent policy.

The first rule tells Git to identify text files and normalize their line endings.

The Windows script rules preserve CRLF for `.bat` and `.cmd` files.

The binary rules prevent text conversion on binary files.

### 19.1 Why use LF in the repository?

A consistent LF policy is often convenient for cross-platform development.

It helps reduce unnecessary differences in:

- Pull Requests.
- Code reviews.
- CI environments.
- Linux containers.
- Deployment environments.

The exact policy should be documented and shared across the team.

## 20. Force Git to renormalize files

If you introduce `.gitattributes` into an existing repository, existing files may have inconsistent line endings.

You can ask Git to renormalize tracked files:

```bash
git add --renormalize .
```

Inspect the result:

```bash
git status
git diff --cached
```

Review carefully before committing.

A renormalization operation can produce a large diff if many files have inconsistent line endings.

Do not combine a massive line-ending conversion with unrelated feature changes.

A dedicated commit is easier to review.

Example:

```bash
git commit -m "chore(git): normalize repository line endings"
```

## 21. Configure Git for Windows

You can inspect your current setting:

```bash
git config --get core.autocrlf
```

Common settings include:

```bash
git config --global core.autocrlf true
```

This is a common Windows configuration that converts LF to CRLF in the working tree while using normalized text content in the repository.

Another option is:

```bash
git config --global core.autocrlf input
```

This converts CRLF to LF when committing but does not convert LF to CRLF on checkout.

The correct setting depends on your repository's line-ending policy.

If your project uses `.gitattributes` to define line endings explicitly, you should avoid conflicting global settings and test the behavior with your actual files.

Do not change global Git settings blindly on an established project.

---

# Part 5 — Combining .gitignore and .gitattributes

## 22. Example project structure

A well-organized DRF + React project might look like:

```text
restaurant-system/
│
├── .git/
├── .github/
│
├── .gitignore
├── .gitattributes
├── .editorconfig
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
│
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/
│   ├── apps/
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── src/
│   └── public/
│
├── docs/
│
└── assets/
    └── brand/
```

Responsibilities:

- `.gitignore`: excludes local environments and generated files.
- `.gitattributes`: controls line endings and file handling.
- `.editorconfig`: helps editors use consistent formatting settings.
- `.github/`: stores GitHub-specific repository configuration.
- `CHANGELOG.md`: records version changes.

## 23. What is .editorconfig?

Although this lesson focuses on Git, you should also understand EditorConfig.

EditorConfig helps maintain consistent editor settings across a development team.

Create:

```text
.editorconfig
```

Example:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4

[*.{js,jsx,ts,tsx,json,css,scss,html,yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

Why is Markdown treated differently?

Trailing spaces can have formatting meaning in Markdown, so you may choose not to remove them automatically.

EditorConfig does not replace `.gitattributes`.

They solve related but different problems:

- EditorConfig helps configure editors.
- `.gitattributes` controls Git's handling of repository files.

---

# Part 6 — Git LFS and repository strategy

## 24. Decide where each file should live

Not every large file belongs in Git or Git LFS.

Consider these examples:

| File | Recommended storage |
|---|---|
| Python source code | Git |
| React source code | Git |
| Small project logo | Git |
| Large versioned design source | Git LFS |
| Large project video asset | Git LFS, if versioning is needed |
| Customer-uploaded product image | Application media/object storage |
| Database backup | Dedicated backup storage |
| Production database | Database server |
| Environment secrets | Secret manager or secure environment configuration |
| Docker image | Container registry |
| Build artifacts | CI artifact storage or release assets, depending on purpose |

### 24.1 Restaurant application example

Your application has the following files:

```text
assets/
├── logo.png
├── restaurant-design.psd
└── promotional-video.mp4

backend/
├── media/
│   ├── products/
│   └── customer-uploads/
│
└── backups/
    └── restaurant-db-backup.sql
```

A sensible strategy:

- `logo.png`: commit to Git if reasonably small and part of the application.
- `restaurant-design.psd`: consider Git LFS.
- `promotional-video.mp4`: consider Git LFS if the project needs version history.
- `backend/media/`: store in application media storage, not Git.
- `backend/backups/`: store in a dedicated backup system, not Git.
- Database credentials: never commit them.

Remember that your POS application may operate offline locally, but that does not mean customer data should be stored inside the source-code repository.

---

# Part 7 — Common problems and troubleshooting

## 25. Problem: Git still shows a file after adding it to .gitignore

**Cause:** The file is already tracked.

Check:

```bash
git ls-files path/to/file
```

If the file appears, Git is tracking it.

Stop tracking it:

```bash
git rm --cached path/to/file
```

Then commit the change.

## 26. Problem: Git LFS command is not recognized

Check:

```bash
git lfs version
```

If unavailable:

1. Install Git LFS.
2. Restart your terminal.
3. Run `git lfs install`.
4. Verify again.

## 27. Problem: The repository contains an LFS pointer instead of the real file

Check:

```bash
git lfs ls-files
git lfs status
```

Then retrieve the required objects:

```bash
git lfs pull
```

If the object is missing from the remote, check whether it was successfully uploaded and whether the remote LFS service has the object.

## 28. Problem: The Git repository is unexpectedly large

Inspect:

```bash
git count-objects -vH
```

This reports information about Git object storage.

You can also inspect large files currently tracked in the working tree, but remember that a large file removed from the latest commit may still exist in older history.

Removing a file from the latest commit does not automatically shrink the entire repository.

For historical large files, you may need a coordinated history rewrite.

## 29. Problem: A Pull Request shows thousands of line changes

Possible causes:

- Line-ending differences.
- Formatting changes.
- Generated files accidentally committed.
- Large automatic code formatting changes.
- Files being converted between text and binary handling.

Check:

```bash
git diff --stat
git diff --ignore-space-at-eol
```

If line endings are the issue, inspect `.gitattributes` and consider a separate renormalization commit.

## 30. Useful inspection commands

| Command | Purpose |
|---|---|
| `git status --ignored` | Show ignored files |
| `git check-ignore -v FILE` | Explain why a file is ignored |
| `git ls-files` | List tracked files |
| `git ls-files -i --exclude-standard` | List tracked files matching ignore rules |
| `git count-objects -vH` | Inspect Git object storage |
| `git lfs version` | Check Git LFS installation |
| `git lfs track` | Show LFS tracking patterns |
| `git lfs ls-files` | List LFS-managed files |
| `git lfs status` | Show LFS working-tree status |
| `git lfs env` | Inspect LFS environment |

---

# Part 8 — Practical exercises

## Exercise A — Audit your training repository

Inside `github-deep-dive-training`, run:

```bash
git status
git ls-files
git status --ignored
git count-objects -vH
```

Answer these questions:

1. Are any virtual environments tracked?
2. Are there any generated files?
3. Are there files that should be ignored?
4. Is the repository storing unnecessary binary files?
5. Are there any sensitive local files?

Do not delete anything until you understand its purpose.

## Exercise B — Create a .gitignore file

Create:

```text
.gitignore
```

Add rules for:

- Temporary files.
- Operating system files.
- Python caches.
- Node.js dependencies.
- Local environment files.
- Editor-specific files.

Test your rules with:

```bash
git status --ignored
```

For an exact path:

```bash
git check-ignore -v path/to/file
```

Do not add actual secrets to test your `.gitignore`.

## Exercise C — Create .gitattributes

Create:

```text
.gitattributes
```

Configure:

- LF for normal text files.
- CRLF for Windows batch scripts.
- Binary handling for common image and archive formats.

Inspect the file before committing it.

## Exercise D — Install Git LFS

Install Git LFS on your Windows machine.

Run:

```bash
git lfs version
git lfs install
git lfs env
```

Record the output in your own notes.

You do not need to upload a large file to complete this installation exercise.

## Exercise E — Practice Git LFS using a sample asset

If you have an original or appropriately licensed sample asset, create:

```text
assets/
└── sample-design.psd
```

Track the file:

```bash
git lfs track "*.psd"
```

Inspect:

```bash
git lfs track
git lfs status
```

Stage:

```bash
git add .gitattributes
git add assets/sample-design.psd
```

Inspect:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "chore(assets): configure git lfs tracking"
```

If you do not have an appropriate asset, skip the upload portion. Do not create an unnecessarily large test file just to use Git LFS.

## Exercise F — Simulate a tracked-file ignore problem

1. Create a harmless temporary text file.
2. Commit it.
3. Add its filename to `.gitignore`.
4. Run `git status`.
5. Observe that Git still tracks the file.
6. Run:

```bash
git rm --cached temporary-file.txt
```

7. Commit the change.
8. Confirm that the local file remains but is no longer tracked.

Use a harmless test file, never a real secret.

## Exercise G — Write your repository file policy

Create:

```text
docs/github/module-01-code/repository-file-policy.md
```

Use this template:

```markdown
# Repository File Management Policy

## Source Code

- Python source:
- React source:
- Configuration:

## Files Excluded from Git

- Python virtual environments:
- Node dependencies:
- Environment files:
- Cache files:
- Build output:

## Large Assets

- Git LFS candidates:
- External media storage:
- Backup storage:

## Line Endings

- Standard text files:
- Windows scripts:
- Binary files:

## Security

- Secrets must never be committed.
- Exposed credentials must be rotated.
- Production data must not be stored in the source repository.

## Review

- Review .gitignore changes.
- Review .gitattributes changes.
- Check unexpected large files before committing.
```

Fill it in based on the actual needs of your projects.

---

# Part 9 — Commit and push the lesson

## 31. Create your lesson branch

First inspect your repository:

```bash
git status
git branch
```

Update your local main branch:

```bash
git switch main
git pull origin main
```

Create the branch:

```bash
git switch -c docs/add-git-file-management-lesson
```

Create:

```text
docs/github/module-01-code/lesson-13-git-lfs-gitignore-gitattributes.md
```

Paste this lesson into the file.

Update:

```text
docs/github/module-01-code/README.md
```

Add Lesson 13 to the module index.

## 32. Stage and review

```bash
git status
git diff
```

Stage:

```bash
git add docs/github/module-01-code/lesson-13-git-lfs-gitignore-gitattributes.md
git add docs/github/module-01-code/README.md
```

If you completed the additional repository policy exercise:

```bash
git add docs/github/module-01-code/repository-file-policy.md
```

Review:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add git lfs and file management lesson"
```

Push:

```bash
git push -u origin docs/add-git-file-management-lesson
```

Open a Pull Request, review it, and merge it into `main`.

After merging:

```bash
git switch main
git pull origin main
git branch -d docs/add-git-file-management-lesson
```

Delete the remote branch only after confirming the Pull Request has been merged.

---

# Part 10 — Lesson completion checklist

## Knowledge

- [ ] I understand how Git stores repository content.
- [ ] I understand the purpose of Git LFS.
- [ ] I can install and initialize Git LFS.
- [ ] I can track files using Git LFS.
- [ ] I can inspect LFS-managed files.
- [ ] I understand LFS pointer files.
- [ ] I understand why .gitignore exists.
- [ ] I understand Git ignore patterns.
- [ ] I know that .gitignore does not remove already-tracked files.
- [ ] I understand .gitattributes.
- [ ] I understand LF and CRLF.
- [ ] I understand the purpose of .editorconfig.
- [ ] I know when to use Git, Git LFS, or external storage.

## Practical work

- [ ] I audited the training repository.
- [ ] I created or reviewed `.gitignore`.
- [ ] I created or reviewed `.gitattributes`.
- [ ] I installed Git LFS.
- [ ] I practiced the tracked-file ignore scenario.
- [ ] I wrote a repository file policy.
- [ ] I committed and pushed the lesson.
- [ ] I opened and merged the lesson Pull Request.

---

# Official references

1. GitHub — About Git Large File Storage: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage
2. GitHub — Installing Git LFS: https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
3. GitHub — Configuring Git LFS: https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage
4. GitHub — Removing Files from Git LFS: https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage
5. Git — gitignore documentation: https://git-scm.com/docs/gitignore
6. Git — gitattributes documentation: https://git-scm.com/docs/gitattributes
7. Git LFS — Official project: https://git-lfs.com/
8. EditorConfig — Official documentation: https://editorconfig.org/

---

# Expected result

Your repository should have a structure similar to:

```text
github-deep-dive-training/
│
├── .github/
│   └── release.yml
│
├── .gitignore
├── .gitattributes
├── .editorconfig
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
            ├── lesson-13-git-lfs-gitignore-gitattributes.md
            └── repository-file-policy.md
```

This is an illustrative structure. Preserve all the other files and lessons you have already created.

**Next lesson: Lesson 14 — Git Submodules and Managing External Dependencies in Git.**
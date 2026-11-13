# Lesson 14 — Git Submodules and Managing External Dependencies

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what Git submodules are.
- Understand when and why to use submodules.
- Add an external Git repository as a submodule.
- Clone repositories containing submodules.
- Initialize and update submodules.
- Change the version of a submodule.
- Work with branches and commits inside submodules.
- Remove a submodule correctly.
- Understand the difference between submodules, subtrees, package managers, and Git LFS.
- Manage shared code across multiple projects.

---

# Part 1 — Understanding Git submodules

## 2. What is a Git submodule?

A Git submodule allows you to include another Git repository inside your repository.

Instead of copying another project's source code into your repository, you reference its repository and a specific commit.

Example:

```text
my-saas-platform/
│
├── backend/
├── frontend/
├── docs/
│
└── shared/
    └── common-library/    <-- Git submodule
```

Here:

- `my-saas-platform` is your main repository.
- `common-library` is an independent Git repository.
- The main repository records which commit of `common-library` it uses.

A submodule is therefore not simply an ordinary directory containing copied source code.

It is a reference to a particular commit in another repository.

## 3. Why use Git submodules?

Imagine your company develops three SaaS applications:

```text
company/
│
├── restaurant-saas/
├── pharmacy-saas/
└── appointment-saas/
```

All three applications need a shared library containing:

- Common API response utilities.
- Authentication helpers.
- Shared TypeScript types.
- Reusable validation logic.
- Common documentation.

You could copy the same library into every project.

However, this creates maintenance problems.

For example:

```text
restaurant-saas/shared-library/
pharmacy-saas/shared-library/
appointment-saas/shared-library/
```

If you fix a bug in one copy, the other projects do not automatically receive the fix.

A Git submodule provides another approach:

```text
company/
│
├── restaurant-saas/
│   └── shared-library/  --> Commit A
│
├── pharmacy-saas/
│   └── shared-library/  --> Commit A
│
└── appointment-saas/
    └── shared-library/  --> Commit A
```

Each application independently decides which version of the shared library it uses.

**Important:** Updating the shared repository does not automatically update every project using it. Each parent repository must explicitly update its submodule reference.

## 4. How Git submodules work

A submodule involves three important components.

### 4.1 The external repository

This is the repository you want to include.

Example:

```text
https://github.com/octocat/Hello-World.git
```

### 4.2 The .gitmodules file

When you add a submodule, Git creates a `.gitmodules` file.

Example:

```ini
[submodule "external/hello-world"]
    path = external/hello-world
    url = https://github.com/octocat/Hello-World.git
```

This file records:

- The submodule name.
- Its local path.
- Its remote repository URL.

### 4.3 The gitlink

The parent repository records the exact commit checked out by the submodule.

This is called a gitlink.

Conceptually:

```text
Parent repository
       |
       v
external/hello-world
       |
       v
Commit: abc123...
```

The parent repository does not store the entire submodule history as ordinary files.

It stores a reference to a specific commit.

---

# Part 2 — Adding your first submodule

## 5. Prepare your training repository

Open your local training repository:

```bash
cd github-deep-dive-training
```

Check your current branch:

```bash
git branch --show-current
```

Check your working tree:

```bash
git status
```

Make sure you do not have unfinished changes that could interfere with the exercise.

Create the lesson branch:

```bash
git switch main
git pull origin main

git switch -c practice/git-submodules
```

## 6. Add an external repository

For this exercise, use the public GitHub repository:

`https://github.com/octocat/Hello-World.git`

Create a directory named `external` and add the repository as a submodule:

```bash
git submodule add https://github.com/octocat/Hello-World.git external/hello-world
```

What happens?

1. Git downloads the external repository.
2. Git creates the `external/hello-world` directory.
3. Git creates or updates `.gitmodules`.
4. Git records the submodule's selected commit.

Inspect your repository:

```bash
git status
```

You should see changes involving:

```text
.gitmodules
external/hello-world
```

Inspect the configuration:

```bash
cat .gitmodules
```

On Windows PowerShell, you can also use:

```powershell
Get-Content .gitmodules
```

Inspect the submodule:

```bash
git submodule status
```

Inspect its Git repository:

```bash
cd external/hello-world
git status
git log --oneline -5
```

Return to the parent repository:

```bash
cd ../..
```

## 7. Commit the submodule

Stage the changes:

```bash
git add .gitmodules external/hello-world
```

Review:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "chore(git): add hello-world submodule"
```

Push:

```bash
git push -u origin practice/git-submodules
```

Open a Pull Request and inspect the changes.

Pay attention to the fact that the submodule appears as a repository reference rather than an ordinary collection of files.

---

# Part 3 — Cloning repositories containing submodules

## 8. The normal cloning problem

Imagine another developer clones your training repository:

```bash
git clone https://github.com/OWNER/github-deep-dive-training.git
```

The parent repository is cloned, but the submodule working directory might not contain the checked-out external files.

This happens because Git does not automatically initialize submodules during an ordinary clone.

There are two ways to handle this.

## 9. Clone with submodules

Use:

```bash
git clone --recurse-submodules https://github.com/OWNER/github-deep-dive-training.git
```

The `--recurse-submodules` option tells Git to initialize and clone the configured submodules.

This is particularly useful in CI/CD pipelines.

## 10. Initialize submodules after cloning

If you already cloned the parent repository without initializing submodules, execute:

```bash
git submodule init
```

This initializes the submodule configuration.

Then:

```bash
git submodule update
```

This retrieves the commit recorded by the parent repository.

You can also combine both operations:

```bash
git submodule update --init
```

For nested submodules:

```bash
git submodule update --init --recursive
```

### Difference between the commands

| Command | Purpose |
|---|---|
| `git submodule init` | Initializes submodule configuration |
| `git submodule update` | Checks out the recorded submodule commit |
| `git submodule update --init` | Initializes and updates |
| `git submodule update --init --recursive` | Also handles nested submodules |
| `git clone --recurse-submodules URL` | Clones the parent and initializes submodules |

---

# Part 4 — Updating submodules

## 11. Understanding pinned commits

Suppose your parent repository references:

```text
common-library: Commit A
```

The external repository receives new commits:

```text
Commit A
Commit B
Commit C
```

Your parent repository still references Commit A.

It does not automatically move to Commit C.

This behavior is intentional.

It makes your application reproducible because the parent repository identifies the exact version of the dependency it expects.

## 12. Update a submodule to its remote version

From the parent repository:

```bash
git submodule update --remote external/hello-world
```

This fetches the configured remote branch and checks out its latest commit according to the submodule's update configuration.

Inspect the result:

```bash
git submodule status
git status
```

If the submodule reference changed, Git will report a modified submodule in the parent repository.

You must commit that updated reference:

```bash
git add external/hello-world
git commit -m "chore(deps): update hello-world submodule"
```

Push:

```bash
git push
```

**Important:** A submodule update is not complete from the parent's perspective until the updated gitlink is committed.

## 13. Choose which branch to follow

By default, a submodule's remote-tracking behavior may follow its remote's configured default branch.

You can explicitly configure a branch in `.gitmodules`:

```ini
[submodule "external/hello-world"]
    path = external/hello-world
    url = https://github.com/octocat/Hello-World.git
    branch = master
```

The branch setting is relevant when using:

```bash
git submodule update --remote
```

It does not mean that the parent repository automatically follows the branch every time you pull.

The parent still records a specific commit.

After changing `.gitmodules`, stage and commit it:

```bash
git add .gitmodules
git commit -m "chore(git): configure submodule tracking branch"
```

---

# Part 5 — Working inside a submodule

## 14. A submodule is an independent repository

This is one of the most important concepts.

You can work inside a submodule just like any other Git repository.

For example:

```bash
cd external/hello-world
```

Inspect:

```bash
git status
git branch
git log --oneline
```

The submodule has its own:

- Branches.
- Commits.
- Tags.
- Remote repositories.
- Working tree.
- Git history.

The parent repository has its own independent Git history.

## 15. What happens when you modify a submodule?

Suppose you modify a file inside:

```text
external/hello-world/
```

Then run:

```bash
git status
```

Inside the submodule, Git reports the file modification.

Return to the parent repository:

```bash
cd ../..
git status
```

The parent may report that the submodule contains modified content.

There are two different situations:

**Situation A — Modified content**

You changed a file inside the submodule but did not commit it.

The submodule has uncommitted changes.

**Situation B — New submodule commit**

You committed a change inside the submodule.

The parent repository now sees that the submodule points to a different commit.

This is why working with submodules requires understanding two Git repositories at the same time.

## 16. Correct workflow for updating a submodule's source code

Imagine you have permission to modify the external repository.

Inside the submodule:

```bash
cd external/hello-world
```

Create a branch:

```bash
git switch -c fix/example-change
```

Make an appropriate change.

Stage and commit:

```bash
git add .
git commit -m "fix(example): improve documentation"
```

Push the branch:

```bash
git push -u origin fix/example-change
```

Open a Pull Request in the external repository if you are contributing to someone else's project.

After the external change is merged, update the parent repository to the accepted commit.

Return to the parent:

```bash
cd ../..
```

Update:

```bash
git submodule update --remote external/hello-world
```

Review:

```bash
git status
git diff --submodule
```

Commit the updated reference:

```bash
git add external/hello-world
git commit -m "chore(deps): update shared library"
```

This workflow keeps the dependency's changes and the application's dependency update separate.

---

# Part 6 — Removing a submodule

## 17. Why removal requires care

A submodule is more than an ordinary folder.

It involves:

- `.gitmodules`.
- Git configuration.
- A gitlink in the parent repository.
- A submodule Git directory, commonly stored under `.git/modules/`.

Simply deleting the folder may leave configuration behind.

## 18. Remove a submodule correctly

Suppose you want to remove:

```text
external/hello-world
```

First, inspect the repository:

```bash
git status
git submodule status
```

Remove the submodule:

```bash
git submodule deinit -f external/hello-world
```

Remove its registered entry from the index:

```bash
git rm -f external/hello-world
```

Inspect `.gitmodules`.

If the section remains, remove:

```ini
[submodule "external/hello-world"]
    path = external/hello-world
    url = https://github.com/octocat/Hello-World.git
```

Also inspect local submodule configuration if necessary:

```bash
git config --local --get-regexp '^submodule\.'
```

Review the result:

```bash
git status
git diff --cached
```

Commit:

```bash
git commit -m "chore(git): remove hello-world submodule"
```

Push:

```bash
git push
```

Git may retain the old submodule Git directory under `.git/modules/`.

Do not manually delete Git internals without first confirming that the submodule is fully removed and that you no longer need its local history.

---

# Part 7 — Submodules versus other dependency-management approaches

## 19. Git submodules vs Git subtree

Both allow you to incorporate another Git repository into your project, but they work differently.

| Feature | Submodule | Subtree |
|---|---|---|
| Independent repository | Yes | Yes |
| Separate Git history | Maintained independently | Can be imported into parent history |
| Parent tracks dependency commit | Yes | Not through a gitlink |
| Separate clone initialization | Usually required | Usually not |
| Updating dependency | Explicit submodule update | Subtree pull/merge |
| Contributor complexity | Higher | Often lower |
| Dependency source remains separately maintained | Yes | Yes |

A subtree is often easier for developers who want the dependency's files available immediately after cloning.

A submodule is useful when you want to maintain an explicit reference to an independently managed repository.

## 20. Git submodules vs package managers

For software development, package managers are frequently a better choice for reusable libraries.

Examples:

| Ecosystem | Package manager |
|---|---|
| Python | pip / uv |
| JavaScript | npm / pnpm / yarn |
| PHP | Composer |
| Java | Maven / Gradle |
| .NET | NuGet |
| Rust | Cargo |

For example, if you build a reusable Python package containing DRF utilities, you could publish it as a Python package.

Then your applications install a particular version:

```bash
pip install company-common==1.2.0
```

Or declare it in `requirements.txt`:

```text
company-common==1.2.0
```

This is often easier to maintain than a Git submodule for a normal application dependency.

Use submodules when you specifically need to include another Git repository as part of the source tree.

## 21. Git submodules vs Git LFS

These features solve completely different problems.

| Git LFS | Git submodules |
|---|---|
| Manages large files | Includes external Git repositories |
| Stores large content in LFS storage | References another repository |
| Uses pointer files | Uses gitlinks |
| Useful for large binary assets | Useful for shared source repositories |

Do not confuse the two.

---

# Part 8 — Practical exercises

## 22. Exercise A — Add a submodule

Inside your training repository:

```bash
git switch main
git pull origin main
git switch -c practice/git-submodules
```

Add:

```bash
git submodule add https://github.com/octocat/Hello-World.git external/hello-world
```

Inspect:

```bash
git status
git submodule status
cat .gitmodules
```

Answer:

1. What is the purpose of `.gitmodules`?
2. What does the parent repository actually record?
3. Why does the submodule have its own Git history?
4. What happens if the external repository receives new commits?

## 23. Exercise B — Clone with submodules

Create a separate test clone of your repository.

Use:

```bash
git clone --recurse-submodules https://github.com/OWNER/github-deep-dive-training.git github-deep-dive-submodule-test
```

Replace `OWNER` with your GitHub username.

Inspect:

```bash
cd github-deep-dive-submodule-test
git submodule status
```

Confirm that the submodule is initialized.

Then delete the test clone when finished.

Do not delete your original training repository.

## 24. Exercise C — Clone without submodules

Create another separate clone:

```bash
git clone https://github.com/OWNER/github-deep-dive-training.git github-deep-dive-normal-clone
```

Inspect:

```bash
cd github-deep-dive-normal-clone
git submodule status
```

Initialize the submodule:

```bash
git submodule update --init --recursive
```

Compare this experience with Exercise B.

## 25. Exercise D — Update a submodule

Inspect the current reference:

```bash
git submodule status
```

Execute:

```bash
git submodule update --remote external/hello-world
```

Inspect:

```bash
git status
git diff --submodule
```

If the remote repository has not changed since your recorded commit, there may be no new update.

Do not invent a change just to produce a different commit reference.

Explain why the parent repository needs a commit when the submodule reference changes.

## 26. Exercise E — Explore submodule history

Enter:

```bash
cd external/hello-world
```

Run:

```bash
git log --oneline --all --decorate
git branch -a
git remote -v
```

Answer:

1. Does the submodule have its own remote?
2. Does it have its own branches?
3. Can you commit changes inside it?
4. Does the parent repository automatically commit those changes?

## 27. Exercise F — Remove the test submodule

If you are finished with the submodule exercise and do not want to keep it in the training repository, remove it using the procedure from Part 6.

Review the resulting changes before committing.

Alternatively, keep it as a permanent example in your training repository.

---

# Part 9 — Recommended repository documentation

## 28. Create a submodule management policy

Create:

`docs/github/module-01-code/submodule-management-policy.md`

Use the following content:

```markdown
# Git Submodule Management Policy

## 1. Purpose

This policy defines how Git submodules are managed
inside company repositories.

## 2. Approved use cases

Submodules may be used for:

- Shared internal Git repositories.
- Reusable source-code libraries that are intentionally
  maintained as independent repositories.
- External repositories that must remain separate.
- Version-controlled shared resources.

## 3. When not to use submodules

Prefer package managers for normal application dependencies.

Do not use submodules simply to avoid copying a few files.

## 4. Version management

- Every parent repository must reference an intentional commit.
- Submodule updates must be reviewed.
- Do not automatically update production dependencies
  without validation.
- Document important dependency changes.

## 5. Cloning

Developers should use:

git clone --recurse-submodules URL

Existing clones should use:

git submodule update --init --recursive

## 6. Security

- Review the source repository before adding a submodule.
- Use trusted repositories.
- Review licenses.
- Do not include credentials in repository URLs.
- Review submodule updates before merging.

## 7. Pull Requests

Submodule reference changes must be explained
in the Pull Request description.

## 8. Maintenance

- Review outdated submodules.
- Remove unused submodules.
- Avoid unnecessary nested submodules.
- Keep documentation up to date.
```

This policy is an example. Adapt it to the needs of your future company.

---

# Part 10 — Commit and push the lesson

## 29. Create the lesson file

Create:

`docs/github/module-01-code/lesson-14-git-submodules.md`

Paste this lesson into it.

Update the module index:

`docs/github/module-01-code/README.md`

Add Lesson 14.

## 30. Stage and commit

Check:

```bash
git status
```

Stage:

```bash
git add docs/github/module-01-code/lesson-14-git-submodules.md
git add docs/github/module-01-code/README.md
```

If you created the policy:

```bash
git add docs/github/module-01-code/submodule-management-policy.md
```

Review:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add git submodules lesson"
```

Push:

```bash
git push -u origin practice/git-submodules
```

Open a Pull Request.

Suggested title:

```text
docs(github): add Git submodules and dependency management lesson
```

Review the Pull Request and merge it.

After merging:

```bash
git switch main
git pull origin main
git branch -d practice/git-submodules
```

Delete the remote branch after confirming the merge.

---

# Part 11 — Lesson completion checklist

## Knowledge

- [ ] I understand Git submodules.
- [ ] I understand `.gitmodules`.
- [ ] I understand gitlinks.
- [ ] I can add a submodule.
- [ ] I can clone with submodules.
- [ ] I can initialize existing submodules.
- [ ] I can update submodules.
- [ ] I understand pinned commits.
- [ ] I can work inside a submodule.
- [ ] I can remove a submodule.
- [ ] I understand Git submodules vs Git subtree.
- [ ] I understand Git submodules vs package managers.
- [ ] I understand Git submodules vs Git LFS.

## Practical work

- [ ] I added a submodule.
- [ ] I inspected `.gitmodules`.
- [ ] I cloned with `--recurse-submodules`.
- [ ] I initialized a submodule manually.
- [ ] I inspected submodule history.
- [ ] I tested a submodule update.
- [ ] I created a submodule management policy.
- [ ] I committed and pushed the lesson.
- [ ] I reviewed and merged the Pull Request.

---

# Official documentation

1. GitHub — Working with submodules: https://docs.github.com/en/repositories/working-with-files/managing-files/working-with-submodules
2. Git — git-submodule: https://git-scm.com/docs/git-submodule
3. Git — gitmodules: https://git-scm.com/docs/gitmodules
4. Git — git subtree: https://github.com/git/git/blob/master/contrib/subtree/git-subtree.txt
5. GitHub — Managing remote repositories: https://docs.github.com/en/get-started/git-basics/managing-remote-repositories

---

# Expected result

Your repository should now contain:

github-deep-dive-training/
│
├── .gitmodules
│
└── docs/
    └── github/
        └── module-01-code/
            ├── README.md
            ├── lesson-13-git-lfs-gitignore-gitattributes.md
            ├── lesson-14-git-submodules.md
            └── submodule-management-policy.md

The `external/hello-world/` directory may also exist if you choose to retain the practical submodule exercise.

Preserve your existing lessons and repository files.

## Next lesson

**Lesson 15 — Git Worktrees: Managing Multiple Branches and Working Directories Simultaneously.**

You will learn how to work on multiple branches at the same time without repeatedly switching branches in a single working directory.
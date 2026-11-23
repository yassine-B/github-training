# Lesson 15 — Git Worktrees: Managing Multiple Branches and Working Directories Simultaneously

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what Git Worktrees are.
- Understand the difference between branches and worktrees.
- Create additional working directories linked to one Git repository.
- Work on multiple branches simultaneously.
- Inspect and manage existing worktrees.
- Remove worktrees safely.
- Prune stale worktree references.
- Use worktrees for Pull Request reviews.
- Use worktrees for hotfixes and release maintenance.
- Understand how worktrees differ from Git clones.
- Use worktrees with AI coding agents.
- Integrate worktrees into a professional development workflow.

---

## Part 1 — Understanding Git Worktrees

## 2. What is a Git Worktree?

A Git Worktree allows you to have multiple working directories associated with the same Git repository.

Normally, you work with one working directory:

```text
my-project/
│
├── .git/
├── backend/
├── frontend/
└── README.md
```

Suppose you're working on:

```text
feature/payment-integration
```

Suddenly, you need to fix a production bug on:

```text
main
```

Without worktrees, you would normally need to save your changes, switch branches, fix the bug, and return to your previous branch.

Git Worktrees offer another solution.

You can create separate working directories:

```text
Development/
│
├── my-project/
│   └── feature/payment-integration
│
├── my-project-hotfix/
│   └── hotfix/payment-bug
│
└── my-project-review/
    └── feature/customer-dashboard
```

All three working directories are connected to the same underlying Git repository.

Each working directory can have a different branch checked out.

## 3. How Git Worktrees work internally

A Git repository normally has:

- One shared object database.
- Shared repository configuration.
- Shared references and commit history.
- Multiple working directories.
- Separate indexes for the different worktrees.

Conceptually:

```text
                 Main Git Repository
                         |
                 Shared Git Database
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
         Worktree 1  Worktree 2  Worktree 3
             |           |           |
           main       feature     hotfix
```

Each worktree has its own:

- Checked-out branch.
- Working directory.
- Index.
- Working-tree state.

They share Git objects and repository history.

**Important:** Worktrees are not independent clones. They share repository data and are managed together.

## 4. Git Worktrees vs Git branches

A branch is a movable reference to a commit.

A worktree is a working directory in which you check out a branch or commit.

| Git branch | Git worktree |
| --- | --- |
| Represents a line of development | Represents a working directory |
| Contains a reference to a commit | Contains checked-out files |
| Can exist without a worktree | Is associated with a Git repository |
| Does not provide another working directory | Provides another working directory |
| Multiple branches can exist | Multiple worktrees can exist |

You can have 20 branches but only one working directory.

You can also have several worktrees, each checking out a different branch.

## 5. When should you use Git Worktrees?

Consider these situations.

### Scenario A — Feature development and urgent hotfix

You're implementing a new payment system.

Your current branch:

```text
feature/payment-integration
```

A production issue is reported.

Instead of interrupting your feature work, create another worktree:

```text
hotfix/payment-calculation
```

You can work on both simultaneously.

### Scenario B — Pull Request review

You're implementing a dashboard.

A colleague asks you to review:

```text
feature/customer-dashboard
```

You can create a separate worktree for the review without changing your current working directory.

### Scenario C — Multiple release versions

Your company maintains:

```text
release/1.x
release/2.x
main
```

You can create separate worktrees for maintenance and testing.

### Scenario D — AI coding agents

You want two AI coding agents to work on separate tasks:

```text
Agent 1: authentication improvements
Agent 2: dashboard improvements
```

Each agent can work in a different worktree.

This helps isolate file modifications and reduces conflicts between concurrent tasks.

However, shared repository references, concurrent operations, and shared resources still require coordination.

---

## Part 2 — Your first Git Worktree

## 6. Prepare your repository

Open your existing training repository.

For example:

```powershell
cd C:\Projects\github-deep-dive-training
```

Check the current state:

```bash
git status
git branch --show-current
```

Update main:

```bash
git switch main
git pull origin main
```

Create a practice branch:

```bash
git switch -c practice/git-worktrees
```

Create a small file:

```text
worktree-practice.md
```

Content:

```markdown
## Git Worktree Practice

This file is used to practice Git Worktrees.

## Current branch

practice/git-worktrees

## Objective

Understand how multiple working directories
can share one Git repository.
```

Commit:

```bash
git add worktree-practice.md
git commit -m "docs(git): add worktree practice file"
```

Push:

```bash
git push -u origin practice/git-worktrees
```

## 7. Create your first additional worktree

Return to your repository root.

Create a sibling directory for your second worktree.

For example:

```powershell
git worktree add ..\github-deep-dive-hotfix -b practice/worktree-hotfix
```

Explanation:

| Part | Meaning |
| --- | --- |
| `git worktree add` | Creates a new worktree |
| `..\github-deep-dive-hotfix` | Path of the new working directory |
| `-b` | Creates a new branch |
| `practice/worktree-hotfix` | Name of the new branch |

Your directory structure becomes:

```text
Projects/
│
├── github-deep-dive-training/
│   ├── backend/
│   ├── frontend/
│   └── docs/
│
└── github-deep-dive-hotfix/
    ├── backend/
    ├── frontend/
    └── docs/
```

The second directory is connected to the same Git repository.

## 8. Verify your worktrees

From the original repository:

```bash
git worktree list
```

Example output:

```text
C:/Projects/github-deep-dive-training       abc123 [practice/git-worktrees]
C:/Projects/github-deep-dive-hotfix         def456 [practice/worktree-hotfix]
```

Your actual commit hashes will differ.

You can also inspect:

```bash
git status
git branch
```

## 9. Work in the second worktree

Enter the new directory:

```powershell
cd ..\github-deep-dive-hotfix
```

Check:

```bash
git branch --show-current
```

Expected:

```text
practice/worktree-hotfix
```

Create:

```text
hotfix-notes.md
```

Content:

```markdown
## Hotfix Worktree

This file belongs to the hotfix worktree.

## Purpose

Practice working on a separate branch
without interrupting the original worktree.
```

Commit:

```bash
git add hotfix-notes.md
git commit -m "docs(git): add hotfix worktree notes"
```

Return to your original worktree:

```powershell
cd ..\github-deep-dive-training
```

Check:

```bash
git status
```

You will see that the original worktree remains on its own branch.

Your hotfix commit is now part of the shared repository history, even though the original worktree has not switched branches.

---

## Part 3 — Essential Git Worktree commands

## 10. List worktrees

```bash
git worktree list
```

Shows all registered worktrees.

For additional details:

```bash
git worktree list --porcelain
```

The porcelain format is useful for scripts and automation.

## 11. Add a worktree for an existing branch

Suppose you already have:

```text
feature/customer-dashboard
```

You can create a worktree for that branch:

```bash
git worktree add ../customer-dashboard feature/customer-dashboard
```

Git checks out the existing branch in the new working directory.

**Important:** A normal local branch cannot be checked out simultaneously in two worktrees.

If that branch is already checked out elsewhere, Git will normally reject the operation.

This prevents accidental simultaneous modifications to the same branch through different working directories.

## 12. Create a worktree from an existing commit

You can also create a worktree for a particular commit:

```bash
git worktree add --detach ../commit-review abc123
```

Replace `abc123` with a real commit hash.

This creates a detached HEAD worktree.

A detached HEAD means that the working directory is not currently associated with a local branch.

This is useful for:

- Inspecting historical versions.
- Comparing old implementations.
- Testing a previous release.
- Investigating regressions.

If you intend to make commits you want to retain, create a branch first or create one from the detached worktree.

## 13. Create a worktree from a remote branch

Suppose the remote branch exists but your local repository has not created a local tracking branch.

Fetch:

```bash
git fetch origin
```

Create a local tracking branch and worktree:

```bash
git worktree add --track -b feature/customer-dashboard-review ../customer-dashboard-review origin/feature/customer-dashboard
```

This creates a local branch tracking the specified remote branch.

If the local branch already exists, use the existing-branch command instead.

## 14. Remove a worktree

When you finish working in the hotfix worktree:

Return to the original repository.

Check:

```bash
git worktree list
```

Remove the additional worktree:

```bash
git worktree remove ../github-deep-dive-hotfix
```

Git normally refuses to remove a worktree containing uncommitted changes.

This protects your work.

Do not use force removal simply to bypass this protection.

If the worktree contains changes you need, commit them or preserve them elsewhere first.

## 15. Prune stale worktree references

Sometimes a worktree directory is deleted manually outside Git.

Git may retain a registration for that directory.

Use:

```bash
git worktree prune
```

Inspect stale entries before pruning:

```bash
git worktree prune --dry-run --verbose
```

This helps clean up stale administrative records.

Do not use pruning as a substitute for properly removing active worktrees.

## 16. Lock and unlock worktrees

Git provides commands for protecting worktrees from automatic removal.

Lock:

```bash
git worktree lock ../important-release
```

Add a reason:

```bash
git worktree lock --reason "Active production release maintenance" ../important-release
```

Unlock:

```bash
git worktree unlock ../important-release
```

Inspect:

```bash
git worktree list --porcelain
```

A locked worktree is protected against certain automatic cleanup operations.

This is useful for worktrees that must remain available even if their directory is temporarily unavailable.

---

## Part 4 — Advanced worktree workflows

## 17. Workflow A — Hotfix without interrupting development

Imagine you're working on:

```text
feature/new-checkout
```

You receive a production bug report.

Your current structure:

```text
Projects/
└── restaurant-app/
    └── feature/new-checkout
```

Create a separate hotfix worktree:

```bash
git worktree add ../restaurant-hotfix -b hotfix/payment-error main
```

This creates a branch based on `main`.

Move into it:

```powershell
cd ..\restaurant-hotfix
```

Fix the issue.

Commit:

```bash
git add .
git commit -m "fix(payments): correct payment calculation"
```

Push:

```bash
git push -u origin hotfix/payment-error
```

Open a Pull Request targeting `main`.

Meanwhile, your original feature work remains available.

After the hotfix is merged:

```powershell
cd ..\restaurant-app
```

Update your main branch when appropriate.

This is a typical production hotfix workflow.

## 18. Workflow B — Review a Pull Request

Suppose someone opens:

```text
feature/customer-notifications
```

You want to inspect the code independently.

Fetch:

```bash
git fetch origin
```

Create the review worktree:

```bash
git worktree add --track -b review/customer-notifications ../review-notifications origin/feature/customer-notifications
```

Inspect the code:

```powershell
cd ..\review-notifications
```

Run your tests:

```bash
python manage.py test
```

Or, for a React project:

```bash
npm install
npm run build
```

Use the actual commands required by the project.

After completing your review:

```powershell
cd ..\restaurant-app
git worktree remove ../review-notifications
```

The review branch can be deleted separately after confirming it is no longer needed.

## 19. Workflow C — Maintain multiple release branches

Imagine your SaaS product has these branches:

```text
main
release/1.0
release/2.0
```

You need to maintain two supported versions while developing version 3.

Create separate worktrees:

```bash
git worktree add ../app-v1 release/1.0
git worktree add ../app-v2 release/2.0
```

Your structure:

```text
Projects/
│
├── app/
│   └── main
│
├── app-v1/
│   └── release/1.0
│
└── app-v2/
    └── release/2.0
```

You can now work on all three versions without constantly switching branches.

## 20. Workflow D — Use worktrees with AI coding agents

Suppose you have two independent tasks:

```text
Task 1:
Improve authentication.

Task 2:
Improve restaurant dashboard.
```

Create:

```bash
git worktree add ../agent-auth -b feature/auth-improvements main

git worktree add ../agent-dashboard -b feature/dashboard-improvements main
```

Give each agent access only to its assigned working directory.

Recommended isolation:

| Agent | Working directory | Branch |
| --- | --- | --- |
| Agent 1 | `agent-auth` | `feature/auth-improvements` |
| Agent 2 | `agent-dashboard` | `feature/dashboard-improvements` |

Benefits:

- File modifications are separated.
- Branches are independent.
- Each agent can run tests separately.
- You can review each implementation independently.

However, remember:

- Both worktrees share the repository's Git database.
- Concurrent Git operations may require coordination.
- Avoid having multiple agents modify the same files.
- Avoid sharing the same local database or development server resources without planning.
- Each worktree may need its own dependencies, environment files, and local configuration.
- Never give an agent access to production secrets unnecessarily.

Worktrees provide source-code isolation, not complete environment or security isolation.

---

## Part 5 — Git Worktrees vs Git Clone

## 21. What is the difference?

A Git clone creates another repository.

A Git worktree creates another working directory connected to an existing repository.

| Feature | Git clone | Git worktree |
| --- | --- | --- |
| Separate repository | Yes | No |
| Shared Git object database | No, normally | Yes |
| Independent repository configuration | Yes | Mostly shared |
| Independent working directory | Yes | Yes |
| Separate branch checkout | Yes | Yes |
| Requires another clone operation | Yes | No |
| Useful for independent projects | Yes | Not necessarily |
| Useful for concurrent branch work | Yes | Yes |

### When should you use a clone?

Use a clone when:

- You need a fully independent repository.
- You need separate repository configuration.
- You want independent Git history and repository administration.
- You are contributing to a fork.
- You need stronger separation between development environments.

### When should you use a worktree?

Use a worktree when:

- You work on multiple branches of the same repository.
- You want to review Pull Requests without interrupting development.
- You maintain multiple release branches.
- You want to use several coding agents on different branches.

---

## Part 6 — Important limitations and best practices

## 22. One branch cannot normally be checked out in multiple worktrees

For example:

```bash
git worktree add ../worktree-one feature/payment
git worktree add ../worktree-two feature/payment
```

The second command will normally fail because the branch is already checked out.

You can create a detached worktree:

```bash
git worktree add --detach ../worktree-two feature/payment
```

However, this is not a replacement for having two independently editable branches.

If two developers or agents need independent commits, create separate branches.

## 23. Worktrees share repository-level state

Worktrees have separate working files and indexes, but they share important repository data.

For example:

- Commit objects.
- Branch references.
- Tags.
- Remote configuration.
- Much of the repository configuration.

A branch created or deleted in one worktree is visible to the others.

Do not treat worktrees as independent repositories.

## 24. Environment variables and dependencies

For a DRF + React application, different worktrees may need separate environment files.

Example:

```text
restaurant-app/
restaurant-hotfix/
restaurant-review/
```

Each may require:

```text
backend/.env
frontend/.env.local
```

These files are not automatically copied from one worktree to another.

They are also normally excluded from Git.

Use secure local configuration and avoid copying production credentials into development environments.

## 25. Database and port conflicts

Multiple worktrees do not automatically create separate databases or application servers.

For example:

```text
Worktree A:
Backend port 8000
Frontend port 5173

Worktree B:
Backend port 8000
Frontend port 5173
```

Running both simultaneously may cause port conflicts.

For independent development environments, configure:

```text
Worktree A:
Backend: 8000
Frontend: 5173
Database: restaurant_dev_a

Worktree B:
Backend: 8001
Frontend: 5174
Database: restaurant_dev_b
```

The same principle applies to Docker Compose project names, Redis instances, Celery workers, and local services.

## 26. Avoid too many worktrees

Worktrees are lightweight in Git storage terms, but your development tools still consume resources.

Each worktree can require:

- IDE resources.
- Dependency installation.
- Build processes.
- Test execution.
- Local services.
- Database connections.

Use worktrees when they solve a real workflow problem.

---

## Part 7 — Practical exercises

## Exercise A — Create two worktrees

Starting from your training repository:

Create:

```text
practice/worktree-one
practice/worktree-two
```

Commands:

```bash
git worktree add ../training-worktree-one -b practice/worktree-one main

git worktree add ../training-worktree-two -b practice/worktree-two main
```

Inspect:

```bash
git worktree list
```

Questions:

1. How many worktrees exist?
2. How many repositories exist?
3. Do they share Git history?
4. Are they checking out the same branch?

## Exercise B — Commit in one worktree

Enter:

```powershell
cd ..\training-worktree-one
```

Create:

```text
worktree-one.md
```

Content:

```markdown
## Worktree One

This file belongs to the first worktree.
```

Commit:

```bash
git add worktree-one.md
git commit -m "docs(git): add first worktree example"
```

Return to the main training repository.

Check:

```bash
git log --oneline -5
```

The new commit is part of the shared repository history.

## Exercise C — Commit in another worktree

Enter:

```powershell
cd ..\training-worktree-two
```

Create:

```text
worktree-two.md
```

Content:

```markdown
## Worktree Two

This file belongs to the second worktree.
```

Commit:

```bash
git add worktree-two.md
git commit -m "docs(git): add second worktree example"
```

Check the commit history from both directories.

Observe that both worktrees share the repository's commit database, although their checked-out branches may point to different commits.

## Exercise D — Test branch protection

From the original worktree, try:

```bash
git worktree add ../duplicate-worktree practice/worktree-one
```

If `practice/worktree-one` is already checked out in another worktree, Git should reject the operation.

Understand the reason.

Then test:

```bash
git worktree add --detach ../detached-review practice/worktree-one
```

Inspect:

```bash
git -C ../detached-review status
git -C ../detached-review branch --show-current
```

The branch name will be empty because HEAD is detached.

Remove the detached worktree when finished.

## Exercise E — Practice Pull Request review

Create a review branch:

```bash
git worktree add ../training-review -b review/worktree-example main
```

Make a small documentation change.

Commit:

```bash
git add .
git commit -m "docs(git): add worktree review example"
```

Push:

```bash
git push -u origin review/worktree-example
```

Open a Pull Request and review it.

Merge it when ready.

## Exercise F — Remove worktrees

Inspect:

```bash
git worktree list
```

Remove the additional worktrees:

```bash
git worktree remove ../training-worktree-one

git worktree remove ../training-worktree-two

git worktree remove ../training-review
```

If a worktree has uncommitted changes, preserve those changes before removing it.

Check:

```bash
git worktree list
```

Clean up stale records if necessary:

```bash
git worktree prune --dry-run --verbose
```

## Exercise G — Worktree management report

Create:

`docs/github/module-01-code/worktree-management-report.md`

Content:

```markdown
## Git Worktree Management Report

## 1. Purpose

Explain what Git Worktrees are.

## 2. Worktrees Created

List the worktrees created during this lesson.

## 3. Branch Management

Explain how branches were assigned to worktrees.

## 4. Shared Repository Data

Explain which Git data is shared.

## 5. Practical Results

Describe the commits created in different worktrees.

## 6. Limitations

Document the limitations you encountered.

## 7. Use Cases

Explain how you would use worktrees for:

- Hotfixes.
- Pull Request reviews.
- Release maintenance.
- AI coding agents.

## 8. Conclusion

Explain when you would choose a worktree
instead of another Git clone.
```

---

## Part 8 — Commit and push the lesson

## 27. Create your lesson branch

From your main training repository:

```bash
git switch main
git pull origin main
```

Create:

```bash
git switch -c docs/add-git-worktrees-lesson
```

Create:

`docs/github/module-01-code/lesson-15-git-worktrees.md`

Paste this lesson into the file.

Update:

`docs/github/module-01-code/README.md`

Add Lesson 15.

Add your practical report if completed:

`docs/github/module-01-code/worktree-management-report.md`

## 28. Stage and review

```bash
git status
```

Stage:

```bash
git add docs/github/module-01-code/lesson-15-git-worktrees.md

git add docs/github/module-01-code/README.md
```

If you created the report:

```bash
git add docs/github/module-01-code/worktree-management-report.md
```

Review:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add git worktrees lesson"
```

Push:

```bash
git push -u origin docs/add-git-worktrees-lesson
```

Open a Pull Request.

Suggested title:

```text
docs(github): add Git Worktrees and parallel development lesson
```

Review and merge.

After merging:

```bash
git switch main
git pull origin main
git branch -d docs/add-git-worktrees-lesson
```

Delete the remote branch after confirming the merge.

---

## Part 9 — Tags and Releases

## 29. Create a lesson milestone tag

We will continue practicing Git tags and GitHub Releases throughout Module 1.

First, inspect existing tags:

```bash
git tag --list
```

Check whether the following tag already exists:

```text
module-01-lesson-15
```

If it is unused, create an annotated tag after merging the lesson PR:

```bash
git switch main
git pull origin main

git tag -a module-01-lesson-15 -m "Module 1 Lesson 15: Git Worktrees"
```

Inspect:

```bash
git show module-01-lesson-15
```

Push:

```bash
git push origin module-01-lesson-15
```

If the tag already exists, do not overwrite it. Choose another unique tag name.

## 30. Create a GitHub Release

Open your repository's Releases page:

```text
https://github.com/OWNER/github-deep-dive-training/releases
```

Create a release using the tag:

```text
module-01-lesson-15
```

Suggested release title:

```text
Module 1 — Lesson 15: Git Worktrees
```

Suggested release description:

```markdown
## Module 1 — Lesson 15

## Topics Covered

- Git Worktrees fundamentals
- Multiple working directories
- Parallel branch development
- Pull Request review workflows
- Hotfix workflows
- Release maintenance
- Worktrees with AI coding agents
- Worktree management and cleanup

## Practical Exercises

- Create multiple worktrees.
- Commit changes in separate worktrees.
- Test detached HEAD.
- Practice Pull Request reviews.
- Remove worktrees safely.

## Learning Outcome

Understand how to manage multiple branches
and working directories simultaneously.
```

Publish the release when your lesson is complete.

This is a training milestone, not a production software release.

---

## Part 10 — Lesson completion checklist

## Knowledge

- [ ] I understand Git Worktrees.
- [ ] I understand the difference between branches and worktrees.
- [ ] I understand shared repository data.
- [ ] I can create a new worktree.
- [ ] I can create a worktree from an existing branch.
- [ ] I can create a detached worktree.
- [ ] I can create a worktree from a remote branch.
- [ ] I can inspect worktrees.
- [ ] I can remove worktrees.
- [ ] I understand worktree pruning.
- [ ] I understand worktree locking.
- [ ] I understand worktrees vs clones.
- [ ] I understand worktrees with AI coding agents.
- [ ] I understand worktree limitations.

## Practical work

- [ ] I created two worktrees.
- [ ] I created commits in different worktrees.
- [ ] I tested branch checkout restrictions.
- [ ] I created a detached worktree.
- [ ] I practiced a Pull Request review workflow.
- [ ] I removed unnecessary worktrees.
- [ ] I wrote a worktree management report.
- [ ] I committed and pushed the lesson.
- [ ] I created a Git tag.
- [ ] I published a GitHub Release.

---

## Official documentation

1. Git — git-worktree: <https://git-scm.com/docs/git-worktree>
2. GitHub Docs — About Git: <https://docs.github.com/en/get-started/using-git/about-git>
3. Git — git-branch: <https://git-scm.com/docs/git-branch>
4. Git — git-clone: <https://git-scm.com/docs/git-clone>
5. GitHub Docs — Managing releases: <https://docs.github.com/en/repositories/releasing-projects-on-github>

---

## Expected result

Your repository should contain:

```text
github-deep-dive-training/
│
├── docs/
│   └── github/
│       └── module-01-code/
│           ├── README.md
│           ├── lesson-13-git-lfs-gitignore-gitattributes.md
│           ├── lesson-14-git-submodules.md
│           ├── lesson-15-git-worktrees.md
│           └── worktree-management-report.md
│
└── ...
```

Your Git repository should also have the milestone tag:

```text
module-01-lesson-15
```

And a corresponding GitHub Release.

Preserve your previous lessons, tags, releases, and existing repository structure.

## Next lesson

### Lesson 16 — Git Hooks: Automating Checks and Enforcing Repository Standards

We will cover:

- Client-side hooks.
- Server-side hooks.
- `pre-commit`.
- `commit-msg`.
- `pre-push`.
- Husky.
- lint-staged.
- Conventional Commit enforcement.
- Automated formatting and linting.
- Git hook security and limitations.
- Real-world DRF + React examples.

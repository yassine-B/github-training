# Lesson 9 — GitHub Forks and Open-Source Contributions

**Module:** 01 — Code  
**Topic:** Forks, upstream remotes, and the fork-and-pull workflow  
**Difficulty:** Intermediate  
**Estimated time:** 2–3 hours

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what a GitHub fork is.
- Distinguish between a fork and a clone.
- Understand the `origin` and `upstream` remotes.
- Fork a public repository into your GitHub account.
- Clone your fork locally.
- Create a feature branch and make a contribution.
- Push your changes to your fork.
- Open a Pull Request from your fork to the original repository.
- Synchronize your fork when the original repository changes.
- Handle upstream changes without losing your work.
- Follow good open-source contribution practices.

## 2. What is a fork?

A **fork** is a GitHub-hosted copy of another user's repository under your own GitHub account.

For example:

Original repository:

`https://github.com/octocat/Spoon-Knife`

Your fork:

`https://github.com/YOUR_USERNAME/Spoon-Knife`

You own and control your fork. You can create branches, commit changes, push code, and experiment without having write access to the original repository.

When you want to contribute your changes to the original repository, you create a Pull Request.

### 2.1 Fork vs clone

These concepts are related, but they are not the same.

| Concept | Meaning | Where it exists |
|---|---|---|
| Fork | A GitHub-hosted copy of another repository | GitHub |
| Clone | A local copy of a Git repository | Your computer |
| Branch | An independent line of development | Local Git and/or remote |
| Pull Request | A proposal to merge changes into another branch | GitHub |

A typical workflow looks like this:

1. Fork someone else's repository on GitHub.
2. Clone your fork to your computer.
3. Create a feature branch.
4. Make changes and commit them.
5. Push your branch to your fork.
6. Open a Pull Request to the original repository.
7. Respond to review feedback.
8. The repository maintainers decide whether to merge your contribution.

## 3. Understand the fork-and-pull workflow

There are two important repositories in this workflow:

- **Upstream:** The original repository owned by someone else.
- **Origin:** Your fork, which is under your GitHub account.

Example:

| Remote | Repository | Purpose |
|---|---|---|
| `origin` | `YOUR_USERNAME/Spoon-Knife` | Your fork; where you push changes |
| `upstream` | `octocat/Spoon-Knife` | Original repository; where you get updates |

The important distinction:

- Pull or fetch changes from `upstream`.
- Push your own changes to `origin`.
- Open Pull Requests from your fork to the original repository.

### 3.1 Understand the relationship

```text
Original repository
octocat/Spoon-Knife
        |
        | Fork on GitHub
        v
Your fork
YOUR_USERNAME/Spoon-Knife
        |
        | Clone to your computer
        v
Local repository
        |
        | Create branch, edit, commit
        v
Push branch to your fork
        |
        | Create Pull Request
        v
Original repository maintainers review it
```

## 4. Practical exercise — Fork a repository

For this exercise, use GitHub's public demonstration repository:

`https://github.com/octocat/Spoon-Knife`

It is commonly used to demonstrate the fork workflow.

### Step 1 — Open the original repository

1. Open `https://github.com/octocat/Spoon-Knife`.
2. Confirm that you are viewing the original repository.
3. Look at its files, README, branches, and contribution information.

Before contributing to a real project, always read its `README.md`, `CONTRIBUTING.md`, and any contribution instructions.

### Step 2 — Fork the repository

1. Click **Fork**.
2. Select your GitHub account as the owner.
3. Keep the repository name as `Spoon-Knife`.
4. Complete the fork operation.

You should now have a repository at:

`https://github.com/YOUR_USERNAME/Spoon-Knife`

Replace `YOUR_USERNAME` with your actual GitHub username.

**Important:** You are not changing the original repository. You are creating your own fork.

### Step 3 — Inspect your fork

Open your fork and inspect:

- Repository owner.
- Repository name.
- Branches.
- Commits.
- Files.
- Settings.

Notice that GitHub identifies it as a fork of the original repository.

## 5. Clone your fork locally

Open PowerShell or the VS Code terminal.

Navigate to the directory where you keep your projects.

```powershell
cd C:\Projects
```

Clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/Spoon-Knife.git
```

Enter the repository:

```bash
cd Spoon-Knife
```

Inspect the repository:

```bash
git status
git branch
git remote -v
```

At this point, you should see a remote named `origin`.

It should point to your fork:

```text
origin  https://github.com/YOUR_USERNAME/Spoon-Knife.git (fetch)
origin  https://github.com/YOUR_USERNAME/Spoon-Knife.git (push)
```

Why is there no `upstream` remote yet?

Because Git cloned your fork. Git does not automatically add the original repository as another remote.

We will add it next.

## 6. Add the upstream remote

Add the original repository:

```bash
git remote add upstream https://github.com/octocat/Spoon-Knife.git
```

Inspect your remotes:

```bash
git remote -v
```

Expected structure:

```text
origin    https://github.com/YOUR_USERNAME/Spoon-Knife.git (fetch)
origin    https://github.com/YOUR_USERNAME/Spoon-Knife.git (push)
upstream  https://github.com/octocat/Spoon-Knife.git (fetch)
upstream  https://github.com/octocat/Spoon-Knife.git (push)
```

You generally use `upstream` to retrieve changes from the original repository. You normally do not push to it.

### 6.1 Understand the remote commands

**List remotes:**

```bash
git remote
```

**Show remote URLs:**

```bash
git remote -v
```

**Add a remote:**

```bash
git remote add upstream URL
```

**Change a remote URL:**

```bash
git remote set-url upstream NEW_URL
```

**Remove a remote:**

```bash
git remote remove upstream
```

**Inspect a remote in detail:**

```bash
git remote show upstream
```

Do not remove or change a remote unless you understand why it is configured incorrectly.

## 7. Understand origin and upstream

Memorize this distinction:

### Origin

Your fork.

You push your work here:

```bash
git push origin feature/my-contribution
```

### Upstream

The original repository.

You retrieve its updates here:

```bash
git fetch upstream
```

You should avoid pushing directly to the original repository unless you have explicit write permission and the project expects that workflow.

## 8. Create a contribution branch

Never use the default branch for your contribution.

First, inspect the repository's default branch:

```bash
git remote show upstream
```

Look for:

```text
HEAD branch: main
```

The default branch could have a different name. Use the actual branch name shown by GitHub or the remote information.

For the following examples, assume it is `main`.

Switch to your local `main` branch:

```bash
git switch main
```

Update your local branch from the original repository:

```bash
git fetch upstream
git merge upstream/main
```

If the repository has no new upstream changes, Git will report that your branch is already up to date.

Now create your contribution branch:

```bash
git switch -c docs/add-contributor-profile
```

Check your branch:

```bash
git branch
```

Check the working tree:

```bash
git status
```

Your new branch is where you will make the contribution.

## 9. Make a contribution

For this exercise, add a small documentation file to your fork.

Create:

```text
docs/contributor-profile.md
```

Example content:

```markdown
# Contributor Profile

## About

This file is part of a fork workflow practice exercise.

## Contribution

I practiced the GitHub fork-and-pull workflow.

## Skills Practiced

- Forking a repository
- Cloning a fork
- Configuring origin and upstream
- Creating a feature branch
- Committing changes
- Opening a Pull Request
```

This is a practice contribution. Do not assume the original project's maintainers will accept it.

### 9.1 Inspect your changes

```bash
git status
```

Review the changes:

```bash
git diff
```

Stage the file:

```bash
git add docs/contributor-profile.md
```

Inspect the staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs: add contributor profile practice file"
```

Inspect the commit:

```bash
git log -1 --oneline
```

### 9.2 Push your branch to your fork

```bash
git push -u origin docs/add-contributor-profile
```

The `-u` option sets the upstream tracking branch for your local branch. This means that later you can usually use:

```bash
git push
```

and:

```bash
git pull
```

without specifying the remote and branch every time.

Verify:

```bash
git branch -vv
```

Open your fork on GitHub and confirm that the branch exists.

## 10. Create a Pull Request from your fork

Now you have:

- The original repository: `octocat/Spoon-Knife`
- Your fork: `YOUR_USERNAME/Spoon-Knife`
- Your contribution branch: `docs/add-contributor-profile`

Open your fork on GitHub.

You may see a **Compare & pull request** button. You can use it.

Alternatively:

1. Open the original repository.
2. Select **Pull requests**.
3. Click **New pull request**.
4. Choose the option to compare across forks, if needed.
5. Select the correct repositories and branches.

Your Pull Request should have:

| Field | Value |
|---|---|
| Base repository | `octocat/Spoon-Knife` |
| Base branch | Original repository's default branch |
| Head repository | `YOUR_USERNAME/Spoon-Knife` |
| Compare branch | `docs/add-contributor-profile` |

The direction matters:

```text
YOUR_USERNAME/Spoon-Knife
docs/add-contributor-profile
             |
             | Pull Request
             v
octocat/Spoon-Knife
main
```

### 10.1 Write a useful Pull Request description

Example:

```markdown
## Summary

Adds a contributor profile document as part of a GitHub fork workflow
practice exercise.

## Changes

- Added `docs/contributor-profile.md`.
- Documented the contribution exercise.
- Added a list of practiced Git skills.

## Testing

- [x] Verified the file exists.
- [x] Reviewed the changes locally.
- [x] Confirmed the branch was pushed to my fork.

## Notes

This is a training contribution.
```

Submit the Pull Request.

### 10.2 What happens after submission?

The maintainers of the original repository can:

- Review your changes.
- Add comments.
- Request changes.
- Approve the contribution.
- Merge the Pull Request.
- Close the Pull Request without merging it.

Creating a Pull Request does not mean that your contribution has been accepted.

**Practice note:** This is a public demonstration repository, not a guarantee that your practice contribution will be reviewed or merged. You can close your practice Pull Request after exploring the workflow.

## 11. Synchronize your fork with upstream

This is one of the most important parts of working with forks.

Imagine the original repository receives new commits after you fork it.

Your fork may now be behind the original repository.

You need to synchronize your fork.

### 11.1 Understand the problem

```text
Original repository (upstream)
main: A --- B --- C --- D

Your fork (origin)
main: A --- B
```

The original repository has commits `C` and `D` that your fork does not have.

Your fork needs to receive those commits.

### 11.2 Fetch upstream changes

First, make sure you are not in the middle of another operation and have no uncommitted work you need to preserve.

Check:

```bash
git status
```

Switch to your local default branch:

```bash
git switch main
```

Fetch the original repository:

```bash
git fetch upstream
```

This downloads information about upstream commits and branches. It does not automatically merge those changes into your current branch.

Inspect the changes:

```bash
git log --oneline main..upstream/main
```

This displays commits present in `upstream/main` but not in your local `main`.

### 11.3 Merge upstream into your local main branch

```bash
git merge upstream/main
```

Now your local `main` includes the upstream changes.

Push the updated branch to your fork:

```bash
git push origin main
```

Your fork's default branch is now synchronized with the original repository.

### 11.4 Alternative: use GitHub's Sync fork button

You can also synchronize a fork through GitHub:

1. Open your fork.
2. Find the **Sync fork** option.
3. Review the available update.
4. Select **Update branch**, if offered.

The exact interface can vary.

For this training, practice the command-line method as well. It helps you understand what is happening instead of relying entirely on the GitHub interface.

## 12. Keep your feature branch updated

What if you have a feature branch while the original repository continues receiving commits?

Example:

```text
upstream/main: A --- B --- C --- D

your feature:  A --- B --- X --- Y
```

Your feature branch is based on `B`, while upstream has moved forward to `D`.

You have two common ways to update your feature branch.

### Option A — Merge upstream into your feature branch

Fetch the latest changes:

```bash
git fetch upstream
```

Switch to your feature branch:

```bash
git switch docs/add-contributor-profile
```

Merge the updated upstream branch:

```bash
git merge upstream/main
```

Push the updated feature branch:

```bash
git push origin docs/add-contributor-profile
```

This preserves the existing feature-branch commits and adds a merge commit when necessary.

### Option B — Rebase your feature branch

Fetch the latest changes:

```bash
git fetch upstream
```

Switch to your feature branch:

```bash
git switch docs/add-contributor-profile
```

Rebase:

```bash
git rebase upstream/main
```

Push:

```bash
git push origin docs/add-contributor-profile
```

If you have already pushed commits and the rebase rewrites their history, you may need:

```bash
git push --force-with-lease origin docs/add-contributor-profile
```

Use `--force-with-lease` carefully. It checks that the remote branch has not changed unexpectedly before updating it.

Do not use ordinary `git push --force` as a routine solution. It can overwrite commits that other people have pushed.

### Which approach should you choose?

| Situation | Recommended approach |
|---|---|
| You want a simple workflow and explicit merge history | Merge |
| Your project requires a linear feature-branch history | Rebase |
| You are collaborating on a shared branch | Coordinate before rebasing |
| You have not learned conflict resolution yet | Practice with merge first |

Follow the contribution guidelines of the repository you are working with. Some projects require a specific merge or rebase strategy.

## 13. Understand merge conflicts in fork workflows

A conflict can happen when upstream and your branch modify overlapping parts of the same file.

Example:

```text
upstream/main changes README.md

your feature branch also changes README.md
```

Git may not know which version should be kept.

When a merge or rebase reports conflicts:

1. Run `git status`.
2. Open the conflicted files.
3. Inspect the conflict markers.
4. Decide how the final content should look.
5. Remove the conflict markers.
6. Stage the resolved files.
7. Continue the operation.

For a merge:

```bash
git add README.md
git merge --continue
```

For a rebase:

```bash
git add README.md
git rebase --continue
```

If you need to cancel:

```bash
git merge --abort
```

or:

```bash
git rebase --abort
```

Use the command matching the operation in progress.

Do not blindly choose one side of a conflict. Understand the changes first.

## 14. Contributing to real open-source projects

The fork workflow is not just a Git exercise. It is a common way to contribute to projects you do not own.

Before making a contribution:

### 14.1 Read the project documentation

Look for:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- Issue templates
- Pull Request templates
- Development setup instructions

### 14.2 Find an appropriate issue

Look for labels such as:

- `good first issue`
- `help wanted`
- `documentation`
- `bug`
- `beginner friendly`

Read the issue carefully.

Check whether someone is already working on it.

If the project asks contributors to claim an issue or request assignment, follow that process.

### 14.3 Keep your contribution focused

A good contribution usually:

- Solves one clearly defined problem.
- Changes only the files necessary.
- Follows the project's conventions.
- Includes tests when appropriate.
- Updates documentation when necessary.
- Avoids unrelated formatting or refactoring.

For example, do not combine a documentation correction, a new feature, and a large refactoring into one Pull Request unless the project specifically asks for that.

### 14.4 Communicate professionally

When opening a Pull Request:

- Explain the problem.
- Explain your solution.
- Describe the changes.
- Include relevant tests.
- Link the related issue when appropriate.
- Respond constructively to review feedback.

A maintainer requesting changes is not necessarily rejecting your contribution. It is part of the review process.

## 15. Fork security and permissions

Forking does not give you permission to access private information or secrets from the original repository.

Keep these rules in mind:

1. Never commit passwords, API keys, access tokens, or private credentials.
2. Do not copy confidential information into a public fork.
3. Review the repository's license before reusing its code.
4. Follow the project's security reporting process for vulnerabilities.
5. Do not assume that a public repository accepts every contribution.
6. Be careful when running code from repositories you do not trust.
7. Review GitHub Actions workflows before enabling or running untrusted code.

Public forks and their commits may be visible to other people. Treat everything you push to a public fork as public information.

## 16. Common mistakes and how to fix them

### Mistake 1 — Pushing to the original repository

Incorrect:

```bash
git push upstream feature/my-contribution
```

For the normal fork workflow, push to your fork:

```bash
git push origin feature/my-contribution
```

### Mistake 2 — Forgetting to add upstream

Check:

```bash
git remote -v
```

If upstream is missing:

```bash
git remote add upstream https://github.com/OWNER/REPOSITORY.git
```

Replace the URL with the actual original repository URL.

### Mistake 3 — Creating a contribution directly on main

Instead, create a separate branch:

```bash
git switch -c docs/my-contribution
```

### Mistake 4 — Opening a Pull Request in the wrong direction

Before submitting, verify:

- Base repository is the original project.
- Base branch is the intended target branch.
- Head repository is your fork.
- Compare branch is your contribution branch.

### Mistake 5 — Working with an outdated fork

Fetch upstream and synchronize your default branch:

```bash
git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

### Mistake 6 — Losing local changes while synchronizing

Before switching branches or merging, inspect:

```bash
git status
```

Commit your completed work or safely preserve it before changing branches. Do not use destructive commands to force synchronization.

## 17. Practical exercises

Complete these exercises in order.

### Exercise A — Create a fork

- [ ] Open `octocat/Spoon-Knife`.
- [ ] Fork it into your GitHub account.
- [ ] Inspect the fork.
- [ ] Confirm the fork relationship.

### Exercise B — Configure your local repository

- [ ] Clone your fork.
- [ ] Inspect `origin`.
- [ ] Add `upstream`.
- [ ] Inspect both remotes.
- [ ] Identify the upstream default branch.

Commands to practice:

```bash
git clone URL
git remote -v
git remote add upstream URL
git remote show upstream
```

### Exercise C — Create a contribution

- [ ] Create `docs/add-contributor-profile`.
- [ ] Add `docs/contributor-profile.md`.
- [ ] Inspect your changes.
- [ ] Stage the file.
- [ ] Commit using Conventional Commits.
- [ ] Push the branch to `origin`.

Commands to practice:

```bash
git switch -c docs/add-contributor-profile
git status
git diff
git add docs/contributor-profile.md
git diff --cached
git commit -m "docs: add contributor profile practice file"
git push -u origin docs/add-contributor-profile
```

### Exercise D — Open a Pull Request

- [ ] Open a Pull Request from your fork.
- [ ] Verify the base repository.
- [ ] Verify the base branch.
- [ ] Verify the head repository.
- [ ] Verify the compare branch.
- [ ] Write a clear description.
- [ ] Inspect the Files changed tab.
- [ ] Close the practice Pull Request after exploring the workflow if you do not intend to submit it as a genuine contribution.

### Exercise E — Synchronize your fork

- [ ] Fetch upstream.
- [ ] Inspect upstream-only commits.
- [ ] Merge upstream into your local default branch.
- [ ] Push the updated default branch to your fork.

Commands:

```bash
git fetch upstream
git log --oneline main..upstream/main
git switch main
git merge upstream/main
git push origin main
```

### Exercise F — Practice updating a feature branch

- [ ] Switch to your contribution branch.
- [ ] Fetch upstream.
- [ ] Merge `upstream/main` into your feature branch.
- [ ] Resolve any conflicts if they occur.
- [ ] Push the updated feature branch.

Commands:

```bash
git fetch upstream
git switch docs/add-contributor-profile
git merge upstream/main
git push origin docs/add-contributor-profile
```

## 18. Important commands reference

| Command | Purpose |
|---|---|
| `git clone URL` | Clone a repository |
| `git remote -v` | Display remote names and URLs |
| `git remote add upstream URL` | Add the original repository |
| `git remote show upstream` | Inspect upstream configuration |
| `git fetch upstream` | Download upstream changes |
| `git log main..upstream/main` | Show commits upstream has that local main does not |
| `git merge upstream/main` | Merge upstream changes into the current branch |
| `git switch -c branch-name` | Create and switch to a branch |
| `git push -u origin branch-name` | Push a branch and configure tracking |
| `git branch -vv` | Show branches and tracking information |
| `git rebase upstream/main` | Reapply feature commits on top of upstream main |
| `git push --force-with-lease` | Safely attempt to update a rewritten remote branch |

## 19. Lesson completion checklist

You should be able to explain and demonstrate all of the following:

- [ ] I understand the difference between a fork and a clone.
- [ ] I can fork a public repository.
- [ ] I can clone my fork.
- [ ] I understand `origin` and `upstream`.
- [ ] I can add and inspect Git remotes.
- [ ] I can create a contribution branch.
- [ ] I can commit and push changes to my fork.
- [ ] I can create a Pull Request from my fork to the original repository.
- [ ] I understand the base and compare repository/branch selections.
- [ ] I can fetch upstream changes.
- [ ] I can synchronize my fork.
- [ ] I understand how to update a feature branch.
- [ ] I know the difference between merge and rebase.
- [ ] I understand basic fork security practices.

## 20. Commit and push this lesson to your training repository

After completing the lesson, return to your `github-deep-dive-training` repository.

Create a documentation branch:

```bash
git switch main
git pull origin main
git switch -c docs/add-forks-and-open-source-lesson
```

Create:

```text
docs/github/module-01-code/lesson-09-forks-and-open-source-contributions.md
```

Paste this lesson into the file.

Update:

```text
docs/github/module-01-code/README.md
```

Add Lesson 9 to the module's lesson index.

Inspect your changes:

```bash
git status
git diff
```

Stage the files:

```bash
git add docs/github/module-01-code/
```

Review staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add forks and open source contributions lesson"
```

Push:

```bash
git push -u origin docs/add-forks-and-open-source-lesson
```

Then open a Pull Request into your training repository's `main` branch and follow the review and merge workflow from Lesson 8.

## 21. What comes next?

**Lesson 10 — GitHub Issues and Project Planning**

We will move from repository collaboration into work tracking:

- Issues and issue lifecycle.
- Labels, milestones, and assignees.
- Issue templates and forms.
- Linking Issues to Pull Requests.
- Closing Issues automatically with keywords.
- Managing bugs and feature requests.
- Using Issues as part of a real development workflow.

**Module 1 release reminder:** Continue using the tagging and release workflow established in Lesson 5. Do not create a release for every individual lesson. Prepare the next meaningful module milestone after the required lessons and practical exercises are complete.
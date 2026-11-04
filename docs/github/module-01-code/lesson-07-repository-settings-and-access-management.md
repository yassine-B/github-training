

# Lesson 07 — Repository Settings and Access Management

**Module:** 01 — Code  
**Difficulty:** Intermediate  
**Repository:** `github-deep-dive-training`

---

## 1. Learning objectives

By completing this lesson, you should understand how to:

- Navigate GitHub repository settings.
- Configure repository visibility.
- Understand repository collaborators and permissions.
- Manage the default branch.
- Configure Pull Request merge strategies.
- Protect important branches.
- Understand branch protection rules and repository rulesets.
- Configure repository security settings.
- Review repository access.
- Apply a practical repository governance policy.

## 2. Understanding repository settings

Repository settings control how a GitHub repository behaves.

They allow repository administrators to manage:

- Repository information.
- Visibility and access.
- Collaboration.
- Branches.
- Pull Request behaviour.
- GitHub Actions permissions.
- Security features.
- Repository deletion and transfer.

### Where to find repository settings

1. Open your repository on GitHub.
2. Select **Settings**.
3. Review the sidebar.

Typical settings categories include:

| Category | Purpose |
|---|---|
| General | Repository information and general behaviour |
| Access | Collaborators and access management |
| Code and automation | Branches, rules, Actions, and automation |
| Security | Security policies and security features |
| Integrations | Applications and integrations |

The exact navigation and available options can vary according to your repository type, permissions, and GitHub plan.

## 3. General repository settings

Navigate to:

```text
Repository → Settings → General
```

This section contains important repository configuration.

### 3.1 Repository name

You can rename your repository.

Example:

```text
github-deep-dive-training
```

If you rename a repository, GitHub generally redirects existing repository URLs, but you should still update your local remote URL and documentation where appropriate.

Check your remote:

```bash
git remote -v
```

Example output:

```text
origin  https://github.com/username/github-deep-dive-training.git (fetch)
origin  https://github.com/username/github-deep-dive-training.git (push)
```

Change the remote URL if necessary:

```bash
git remote set-url origin https://github.com/username/new-repository-name.git
```

Explanation:

- `git remote`: manages remote repository connections.
- `set-url`: changes the URL associated with a remote.
- `origin`: the remote name.
- The URL: the new repository address.

Verify:

```bash
git remote -v
```

### 3.2 Repository description

A repository description should explain the project in one or two sentences.

Example:

```text
A practical GitHub training repository covering Git workflows,
collaboration, automation, security, and repository management.
```

A good description should be:

- Short.
- Clear.
- Relevant.
- Easy to understand.

### 3.3 Website

You can add a project website or documentation URL.

Example:

```text
https://example.com
```

Only provide a URL that actually belongs to the project.

### 3.4 Topics

Topics help users discover repositories.

For this repository, possible topics include:

```text
github
git
github-training
git-workflow
developer-training
documentation
devops
```

Topics are useful for organizing and discovering related projects.

### 3.5 Repository features

Depending on the repository and account configuration, you may be able to enable or disable features such as:

- Issues.
- Projects.
- Discussions.
- Wiki.

These features serve different purposes.

| Feature | Purpose |
|---|---|
| Issues | Track bugs, tasks, and feature requests |
| Projects | Plan and track work |
| Discussions | Community conversations and questions |
| Wiki | Additional project documentation |

For this training repository, keep Issues enabled. You can decide whether to enable Discussions and Wiki as you reach those modules.

---

## 4. Repository visibility

Visibility determines who can view your repository.

The main visibility options are:

### Public

A public repository can be viewed by anyone.

Typical use cases:

- Open-source projects.
- Public documentation.
- Portfolio projects.
- Public learning repositories.

### Private

A private repository is restricted to authorized users.

Typical use cases:

- Private commercial projects.
- Internal development.
- Projects containing non-public source code.
- Work in progress that should not be publicly accessible.

### Internal

Internal repositories are available within an enterprise account.

This option is intended for organizations using GitHub Enterprise and is not generally available for ordinary personal repositories.

### Comparison

| Visibility | Who can access it? | Typical use |
|---|---|---|
| Public | Anyone | Open-source project |
| Private | Authorized users | Private development |
| Internal | Members of the enterprise | Enterprise collaboration |

### Important considerations

Changing repository visibility can have significant consequences.

For example:

- Making a repository public exposes its code and repository activity to the public.
- Anyone can fork a public repository.
- Public forks of a repository do not automatically become private when the original repository becomes private.
- Changing visibility can affect security features and other repository capabilities.

Review the consequences before changing visibility.

Official documentation:

https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility

### Exercise

1. Open your repository.
2. Navigate to Settings → General.
3. Locate the repository visibility section.
4. Inspect the current visibility.
5. Do not change it unless you have a specific reason.

For this training project, public visibility is useful if you intend to share your lessons with other developers. Private visibility is appropriate if you want to keep the training repository restricted.

---

## 5. Repository access and collaborators

### 5.1 What is a collaborator?

A collaborator is someone who has been granted access to a repository.

For example, imagine that you are developing a project with three other developers:

```text
Project
│
├── Repository owner
├── Backend developer
├── Frontend developer
└── Documentation contributor
```

Each person needs an appropriate level of access.

The principle to follow is:

**Give people only the permissions they need to perform their responsibilities.**

This is called the principle of least privilege.

### 5.2 Personal repositories

For a repository owned by a personal GitHub account, you can invite collaborators through the repository's access settings.

Typical navigation:

```text
Repository
    |
    v
Settings
    |
    v
Collaborators / Collaborators and teams
```

The exact label may vary.

The owner can invite another GitHub user and manage their access.

### 5.3 Organization repositories

Organization-owned repositories provide more granular predefined repository roles.

The main roles are:

| Role | Main responsibility |
|---|---|
| Read | View and clone the repository |
| Triage | Manage Issues and Pull Requests without pushing code |
| Write | Contribute code and manage normal development work |
| Maintain | Manage repository maintenance without full administrative access |
| Admin | Full repository administration |

These roles apply to organization repositories. Do not assume that every role is available for a personal repository.

### Read

Appropriate for:

- People reviewing project documentation.
- External contributors who only need to inspect code.
- Stakeholders who need visibility.

### Triage

Appropriate for:

- Project coordinators.
- Issue managers.
- Contributors responsible for organizing Issues and Pull Requests.

### Write

Appropriate for:

- Backend developers.
- Frontend developers.
- Developers who need to push branches and contribute code.

### Maintain

Appropriate for:

- Project maintainers.
- People responsible for routine repository management.

### Admin

Appropriate for:

- Repository owners.
- Trusted administrators who need full control.

Admin access should be restricted because it includes sensitive administrative actions.

Official documentation:

https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization

### 5.4 Example permission assignment

Imagine a small software project:

| Team member | Responsibility | Suggested role |
|---|---|---|
| Project owner | Full administration | Admin |
| Backend developer | Backend development | Write |
| Frontend developer | Frontend development | Write |
| Documentation reviewer | Review documentation | Read or Triage |
| Project coordinator | Manage Issues and PRs | Triage |

These are example assignments. The correct permissions depend on actual responsibilities.

### Exercise

For your personal training repository:

1. Open Settings.
2. Locate the collaborators/access section.
3. Inspect the current access list.
4. Review how invitations work.
5. Do not invite anyone unless you intend to give them access.

You can complete this exercise without adding a collaborator.

---

## 6. Default branch management

### 6.1 What is the default branch?

The default branch is the main branch GitHub uses as the default base for operations such as Pull Requests.

A common branch naming convention is:

```text
main
```

Example:

```text
main
│
├── feature/add-authentication
├── docs/improve-readme
├── fix/correct-validation
└── chore/update-dependencies
```

All feature branches are generally created from the current default branch.

### 6.2 Why is the default branch important?

The default branch is commonly used for:

- Production-ready code.
- Stable documentation.
- Pull Request targets.
- Default repository browsing.
- Release preparation.

It should contain the reviewed and integrated work that the project considers its main development line.

### 6.3 Inspect your local branches

```bash
git branch
```

List local and remote branches:

```bash
git branch -a
```

Inspect the current branch:

```bash
git branch --show-current
```

Inspect remote tracking information:

```bash
git branch -vv
```

### 6.4 Changing the default branch

GitHub navigation:

```text
Repository
    |
    v
Settings
    |
    v
General
    |
    v
Default branch
```

You need administrative access, and the repository must have more than one branch.

Do not change the default branch during this exercise. Your repository already uses `main`, which is suitable.

Official documentation:

https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/changing-the-default-branch

---

## 7. Pull Request merge strategies

When a Pull Request is approved and ready, GitHub provides different merge methods.

The choice affects the resulting Git history.

There are three main strategies.

### 7.1 Merge commit

A merge commit combines the source branch into the target branch while preserving the original commits and adding a merge commit.

Example:

```text
main:

A---B---C-----------M
         \         /
          D---E---F
```

The merge commit is `M`.

Advantages:

- Preserves individual commits.
- Clearly records the merge operation.
- Retains the branch's commit history.

Disadvantages:

- Can produce a more complex history.
- Many small branches may create numerous merge commits.

Use it when preserving the complete branch history is important.

### 7.2 Squash and merge

Squash merge combines all commits from a Pull Request into one commit on the target branch.

Example:

```text
Before:

main:
A---B---C

feature:
        \---D---E---F

After squash:

main:
A---B---C---S
```

`S` represents the combined changes.

Advantages:

- Cleaner main branch history.
- One logical change becomes one commit.
- Removes temporary development commits from the main history.

Disadvantages:

- Individual feature branch commits are not preserved as separate commits on the target branch.

This is useful when a Pull Request contains multiple small commits.

### 7.3 Rebase and merge

Rebase and merge places the commits from the feature branch onto the target branch without creating a merge commit.

Example:

```text
Before:

main:
A---B---C

feature:
        \---D---E

After:

main:
A---B---C---D'---E'
```

The commits may have new hashes because their parent relationships change.

Advantages:

- Linear Git history.
- Preserves individual commits.
- Does not add a merge commit.

Disadvantages:

- Commit hashes change.
- Contributors need to understand how rebasing affects history.

### 7.4 Comparison

| Strategy | Preserves individual commits on main? | Creates merge commit? | History |
|---|---|---|---|
| Merge commit | Yes | Yes | Branching |
| Squash and merge | No, combines them | No | Linear |
| Rebase and merge | Yes | No | Linear |

### 7.5 Which strategy should you use?

For `github-deep-dive-training`, I recommend:

**Squash and merge**

Reasons:

- Each Pull Request should represent one logical documentation change.
- Your training repository will have a clean main branch history.
- You can use Conventional Commit-style Pull Request titles.

Example Pull Request title:

```text
docs(github): add repository settings lesson
```

The resulting squash commit can use that title.

For larger software projects, the best strategy depends on how the team wants to preserve and inspect commit history.

Official documentation:

https://docs.github.com/en/pull-requests/reference/pull-request-merges

### 7.6 Configure merge methods

Navigate to:

```text
Repository
    |
    v
Settings
    |
    v
General
    |
    v
Pull Requests
```

You may see options such as:

- Allow merge commits.
- Allow squash merging.
- Allow rebase merging.

For this training repository:

- Enable squash merging.
- You may disable merge commits if you want a consistently linear history.
- Rebase merging is optional.

If you enable linear history requirements later, remember that the repository must allow squash merging, rebase merging, or both.

### Exercise

1. Open Settings → General.
2. Find the Pull Requests section.
3. Inspect the available merge methods.
4. Enable squash merging if it is available.
5. Review the default squash commit message format.
6. Save your configuration if you made changes.

---

## 8. Branch protection

### 8.1 What is branch protection?

Branch protection prevents unsafe changes to important branches.

For example, imagine that a developer accidentally pushes unfinished code directly to `main`.

Branch protection can prevent this type of workflow by requiring changes to pass through a Pull Request.

A protected branch can require:

- Pull Requests before merging.
- Approval from reviewers.
- Successful status checks.
- Conversation resolution.
- Linear commit history.
- Restrictions on force pushes.
- Restrictions on branch deletion.

### 8.2 Why protect main?

The `main` branch should represent a reviewed and stable state.

A typical workflow:

```text
Developer
    |
    v
Create feature branch
    |
    v
Implement changes
    |
    v
Push branch
    |
    v
Open Pull Request
    |
    v
Review changes
    |
    v
Run automated checks
    |
    v
Merge into main
```

This reduces the risk of unreviewed changes entering the main branch.

### 8.3 Classic branch protection rules

GitHub provides branch protection rules that let administrators define requirements for selected branches.

Typical navigation:

```text
Repository
    |
    v
Settings
    |
    v
Branches
    |
    v
Branch protection rules
```

A rule can target a branch using a name or pattern.

Example:

```text
main
```

This targets the `main` branch.

### 8.4 Important protection options

#### Require a Pull Request before merging

This prevents direct changes from bypassing the Pull Request workflow.

#### Require approvals

This requires reviewers to approve changes before merging.

For a team repository, one approval is a reasonable starting point.

For a solo training repository, do not require an approval if nobody else can review your Pull Requests. Otherwise, you may block your own exercises.

#### Dismiss stale approvals

This can require new approval when changes are made after a review.

It helps ensure reviewers approve the latest version of the code.

#### Require conversation resolution

This requires review conversations to be resolved before merging.

#### Require status checks

This requires selected automation checks to pass before merging.

For example:

```text
lint
test
build
```

You will configure GitHub Actions in Module 5. Until then, do not select a required check that does not exist.

#### Require linear history

This prevents merge commits from being used for the protected branch.

You must allow squash merging, rebase merging, or both when requiring linear history.

#### Block force pushes

This prevents users from rewriting the history of the protected branch through force pushes.

#### Restrict deletions

This prevents the protected branch from being deleted.

### 8.5 Recommended protection for a team project

For a collaborative software project, consider:

| Rule | Recommendation |
|---|---|
| Require Pull Request | Enabled |
| Required approvals | 1 or more, according to team size |
| Dismiss stale approvals | Enabled where appropriate |
| Require conversation resolution | Enabled |
| Require status checks | Enabled after CI is configured |
| Require linear history | Optional |
| Block force pushes | Enabled |
| Restrict deletions | Enabled |

The right configuration depends on the project's risk, workflow, team size, and plan.

---

## 9. Repository rulesets

### 9.1 What is a ruleset?

A ruleset is a named collection of rules that controls how users can interact with selected branches or tags.

GitHub rulesets provide a flexible way to manage repository governance.

For example, you could create a ruleset named:

```text
Protect main branch
```

and apply it to:

```text
main
```

The ruleset can require Pull Requests and prevent force pushes or branch deletion.

### 9.2 Rulesets versus classic branch protection

| Feature | Branch protection rules | Rulesets |
|---|---|---|
| Protect branches | Yes | Yes |
| Require Pull Requests | Yes | Yes |
| Require approvals | Yes | Yes |
| Block force pushes | Yes | Yes |
| Multiple matching policies | More limited | Supports layered rules |
| Enforcement status | Protection rule behaviour | Active or Disabled, with additional evaluation options in supported workflows |
| Visibility to readers | More limited | Active rulesets can be viewed by users with read access |

GitHub supports both systems, and their applicable rules can work together.

Rulesets are generally the more flexible approach for managing multiple policies.

### 9.3 Ruleset enforcement statuses

A ruleset can have different enforcement states.

- **Active:** Rules are enforced.
- **Disabled:** Rules are not enforced.
- **Evaluate:** In supported workflows, GitHub records how rules would behave without enforcing them.

The available options can vary by feature and configuration.

For a training repository, inspect the available options before enabling anything.

### 9.4 Create a ruleset

Navigate to:

```text
Repository
    |
    v
Settings
    |
    v
Rules
    |
    v
Rulesets
    |
    v
New ruleset
    |
    v
New branch ruleset
```

Create a ruleset with these example values:

| Setting | Value |
|---|---|
| Ruleset name | Protect main branch |
| Enforcement status | Active, if available and suitable |
| Target branches | `main` |
| Require a Pull Request | Enabled |
| Required approvals | 0 for this solo exercise |
| Block force pushes | Enabled |
| Restrict deletions | Enabled |

For this exercise, do not require status checks or approvals that you cannot satisfy.

You can add stronger requirements when you have a working CI workflow or other reviewers.

### 9.5 Bypass permissions

Rulesets can allow certain roles, teams, or applications to bypass their rules.

For example, a trusted administrator might have bypass access for an emergency change.

However, bypass permissions should be limited.

Do not grant broad bypass access without a clear reason.

### 9.6 Ruleset availability

Ruleset availability depends on repository visibility and GitHub plan.

GitHub documents rulesets for public repositories on GitHub Free and for public and private repositories on certain paid plans.

If your private training repository does not offer the feature, inspect the available branch settings instead. Do not change visibility just to unlock an exercise.

Official documentation:

https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets

https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository

### Exercise

1. Open Settings.
2. Find Rulesets.
3. Inspect the ruleset creation page.
4. Check which rules are available.
5. If supported, create the `Protect main branch` ruleset using the exercise configuration.
6. Confirm that it targets `main`.
7. Verify the ruleset appears in the repository.
8. If the feature is unavailable, record that limitation and inspect Branch protection rules instead.

Do not experiment with force-pushing or deleting `main` to test the protection.

---

## 10. Repository security settings

Security settings help protect source code, credentials, dependencies, and repository activity.

Navigate to:

```text
Repository
    |
    v
Settings
    |
    v
Security
```

The exact settings available depend on repository visibility, account plan, and enabled security features.

### 10.1 Dependency graph

The dependency graph identifies the dependencies used by a repository.

For example, a Python project might use:

```text
Django
Django REST Framework
Celery
Redis
Pillow
```

A JavaScript project might use:

```text
React
Vite
Axios
Zod
TanStack Query
```

Dependency information helps GitHub identify known vulnerabilities.

### 10.2 Dependabot alerts

Dependabot alerts notify repository maintainers when a dependency has a known security vulnerability.

Example:

```text
Package: example-library
Installed version: 1.2.0
Affected version: 1.2.0
Patched version: 1.2.3
```

This is an illustrative example, not a real vulnerability report.

### 10.3 Dependabot security updates

Dependabot can create Pull Requests to update vulnerable dependencies when an appropriate update is available.

Example:

```text
dependabot/npm_and_yarn/react-19.0.1
```

The generated Pull Request should still be reviewed and tested.

### 10.4 Secret scanning

Secret scanning detects credentials and other sensitive information that may have been committed to a repository.

Examples of secrets include:

- API tokens.
- Cloud credentials.
- Database passwords.
- Private keys.

Never put real credentials into your training repository.

### 10.5 Push protection

Where supported and enabled, push protection can block a push containing a detected secret before it reaches the repository.

This is particularly valuable because removing a secret from the latest commit does not necessarily remove it from Git history.

If a real credential is exposed:

1. Revoke or rotate it immediately.
2. Review where it was used.
3. Remove it from the repository.
4. Follow the appropriate incident response process.
5. Review the Git history and any affected systems.

Simply deleting the file is not enough to invalidate an exposed credential.

### 10.6 Security policy

Your repository already contains:

```text
SECURITY.md
```

This file explains how security issues should be reported.

Keep it updated as the project changes.

### Exercise

1. Open the Security section of repository settings.
2. Inspect the dependency graph options.
3. Inspect Dependabot settings.
4. Inspect secret scanning and push protection availability.
5. Review the current security configuration.
6. Do not create or commit real secrets to test these features.

---

## 11. GitHub Actions permissions

Repository settings also control how GitHub Actions workflows can access repository resources.

This is important because a workflow may execute commands, access files, and interact with GitHub resources.

### 11.1 Workflow permissions

GitHub provides a setting that controls the default permissions granted to the `GITHUB_TOKEN` used by workflows.

The general principle is:

**Give a workflow only the permissions it needs.**

For example, a workflow that only runs tests should not need permission to modify repository contents.

### 11.2 Example permissions

```yaml
permissions:
  contents: read
```

This gives the workflow read access to repository contents.

Another example:

```yaml
permissions:
  contents: read
  pull-requests: write
```

This grants read access to repository contents and write access to Pull Request resources.

Only add permissions required by the workflow.

### 11.3 Why this matters

A workflow with unnecessary permissions increases the potential impact of a compromised or incorrectly configured workflow.

You will study:

- Workflow permissions.
- Secrets.
- Variables.
- Environments.
- Runners.
- CI/CD security.

in Module 5 — Actions.

### Exercise

1. Open Settings.
2. Find Actions permissions.
3. Inspect the default workflow permissions.
4. Review the available restrictions.
5. Do not change settings without understanding their impact.

---

## 12. Repository administration and the Danger Zone

At the bottom of General settings, GitHub provides administrative actions.

Examples include:

- Changing repository visibility.
- Transferring repository ownership.
- Archiving a repository.
- Deleting a repository.

These actions can have significant consequences.

### Archiving

Archiving makes a repository read-only.

It is useful when a project is no longer actively maintained but should remain available for reference.

### Deleting

Deleting a repository removes it from the account.

Do not use deletion as an ordinary cleanup operation.

Before deleting a repository, verify that you have backups and that the repository is no longer needed.

For this training exercise, inspect these options but do not execute them.

---

## 13. Recommended configuration for this training repository

Use this as a reference configuration.

| Setting | Recommended configuration |
|---|---|
| Repository visibility | Public if you intend to share the training material |
| Default branch | `main` |
| Issues | Enabled |
| Projects | Optional |
| Discussions | Optional |
| Wiki | Optional |
| Merge method | Squash and merge |
| Require Pull Request | Enabled if rulesets or branch protection are available |
| Required approvals | 0 for solo practice |
| Block force pushes | Enabled for `main` |
| Restrict deletion | Enabled for `main` |
| Status checks | Add after configuring Actions |
| Dependabot alerts | Enable where available |
| Secret scanning | Enable where available |
| Push protection | Enable where available |
| Workflow permissions | Minimum necessary |

This is a training configuration, not a universal policy for every software project.

---

## 14. Practical project exercise

Your task is to inspect and configure the repository's governance settings.

### Step 1 — Inspect your local repository

```bash
git status
git branch -a
git remote -v
git tag
```

Explanation:

- `git status`: checks the working tree.
- `git branch -a`: lists local and remote branches.
- `git remote -v`: displays configured remote URLs.
- `git tag`: lists existing tags.

### Step 2 — Inspect GitHub General settings

Open:

```text
Repository → Settings → General
```

Review:

- Repository name.
- Description.
- Website.
- Topics.
- Repository features.
- Default branch.
- Pull Request merge methods.

### Step 3 — Inspect access

Open the collaborators/access section.

Review:

- Who has access.
- Available permission levels.
- How invitations are managed.

Do not grant unnecessary permissions.

### Step 4 — Configure the merge strategy

If available:

1. Enable squash merging.
2. Review the default squash commit message.
3. Decide whether merge commits and rebase merging are needed.
4. Save your configuration.

### Step 5 — Inspect branch protection

Open:

```text
Settings → Branches
```

Inspect classic branch protection settings.

If rulesets are available, inspect:

```text
Settings → Rules → Rulesets
```

### Step 6 — Configure protection

If available, protect `main` with:

- Pull Request requirement.
- No required approvals for solo practice.
- Force-push restriction.
- Branch deletion restriction.

Do not require CI status checks until you have configured a corresponding GitHub Actions workflow.

### Step 7 — Inspect security settings

Review:

- Dependency graph.
- Dependabot alerts.
- Dependabot security updates.
- Secret scanning.
- Push protection.

Enable appropriate features where available.

### Step 8 — Inspect Actions permissions

Review the default `GITHUB_TOKEN` permissions and Actions restrictions.

Prefer the minimum permissions required.

### Step 9 — Verify your configuration

Record which settings you inspected and which you changed.

You should be able to explain why each setting is enabled or disabled.

---

## 15. Troubleshooting

### I cannot see repository Settings

You may not have administrative access.

Check which account owns the repository and whether you have the necessary permissions.

### I cannot invite a collaborator

Possible causes:

- You do not have administrative access.
- The account or organization has access restrictions.
- The invitation or repository configuration is restricted.

### I cannot create a ruleset

Check:

- Your repository permissions.
- Repository visibility.
- Your GitHub plan.
- Whether rulesets are available for this repository.

### My Pull Request cannot be merged

Inspect:

- Required approvals.
- Required status checks.
- Unresolved review conversations.
- Ruleset restrictions.
- Branch protection rules.
- Merge conflicts.

GitHub displays the conditions preventing a merge in the Pull Request interface.

### I accidentally configured a rule that blocks my workflow

1. Inspect the active rulesets and branch protection rules.
2. Identify which rule is blocking the operation.
3. Review the rule's target branch and requirements.
4. If you have administrative access, temporarily disable or adjust the incorrect rule.
5. Verify the corrected behaviour.

Do not bypass repository protections as a routine development method.

---

## 16. Completion checklist

### General settings

- [ ] Inspected repository name and description.
- [ ] Inspected topics.
- [ ] Reviewed enabled repository features.
- [ ] Confirmed repository visibility.
- [ ] Confirmed `main` is the default branch.

### Access management

- [ ] Inspected collaborators.
- [ ] Understood personal repository access.
- [ ] Understood organization repository roles.
- [ ] Understood least-privilege access.

### Pull Requests

- [ ] Understood merge commits.
- [ ] Understood squash merging.
- [ ] Understood rebase merging.
- [ ] Reviewed available merge methods.
- [ ] Selected a suitable merge strategy.

### Branch protection

- [ ] Understood classic branch protection rules.
- [ ] Understood rulesets.
- [ ] Inspected protection settings.
- [ ] Reviewed force-push restrictions.
- [ ] Reviewed deletion restrictions.
- [ ] Understood required reviews and status checks.

### Security

- [ ] Inspected dependency graph settings.
- [ ] Reviewed Dependabot settings.
- [ ] Inspected secret scanning availability.
- [ ] Inspected push protection availability.
- [ ] Reviewed Actions permissions.
- [ ] Reviewed repository security policy.

### Practical work

- [ ] Completed the repository settings inspection.
- [ ] Applied appropriate configuration where available.
- [ ] Recorded unavailable features or plan limitations.
- [ ] Verified the resulting configuration.

---

## 17. Recommended commit message

This lesson is primarily about GitHub web settings, so you may not have many local file changes to commit.

If you are adding the lesson document to your repository, use:

```bash
git switch main
git pull origin main
git switch -c docs/add-repository-settings-lesson
```

Create the lesson file and add it:

```bash
git add docs/github/module-01-code/lesson-07-repository-settings-and-access-management.md
```

Review:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add repository settings lesson"
```

Push:

```bash
git push -u origin docs/add-repository-settings-lesson
```

Open a Pull Request and merge after reviewing.

---

## 18. Tags and releases

Continue using the release strategy from Lesson 5.

Do not create a release for every lesson.

The next meaningful release milestone remains completion of Module 1.

Before creating a tag:

```bash
git status
git log --oneline -10
git tag
```

Confirm that:

- All Module 1 lessons are complete.
- Exercises are finished.
- All intended documentation changes are merged.
- The intended tag does not already exist.

Prepare a changelog and publish a release only when the module milestone is genuinely complete.

---

## 19. What comes next?

**Lesson 08 — Repository Collaboration Workflow and Pull Request Management**

We will focus on how developers collaborate using:

- Pull Request lifecycle.
- Draft Pull Requests.
- Review requests.
- Approvals and change requests.
- Merge conflicts.
- Review comments.
- Branch synchronization.
- Auto-merge.
- Code Owners.
- Safe collaboration practices.


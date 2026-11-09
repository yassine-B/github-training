# Lesson 11 — GitHub Discussions and Community Collaboration

**Module:** 01 — Code  
**Topic:** Discussions, categories, Q&A, announcements, and community management  
**Difficulty:** Intermediate  
**Estimated time:** 2–3 hours

---

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain what GitHub Discussions are.
- Distinguish Discussions from Issues and Pull Requests.
- Enable Discussions for a repository.
- Configure discussion categories.
- Create announcements, questions, ideas, and general discussions.
- Participate in discussions and provide useful answers.
- Mark a response as an accepted answer.
- Pin, close, and lock discussions.
- Understand discussion moderation permissions.
- Convert an Issue into a Discussion.
- Turn a community discussion into actionable development work.
- Establish community guidelines for a project.

## 2. What is GitHub Discussions?

GitHub Discussions is a communication space for maintainers, contributors, users, and other community members.

It allows people to discuss a project without necessarily creating a development task.

Examples:

- Asking how a feature works.
- Sharing an implementation idea.
- Announcing a new version.
- Discussing the future direction of a project.
- Asking for feedback.
- Sharing a project built using your software.
- Running a community poll.

Think of Discussions as a community forum integrated into GitHub.

### 2.1 Why use Discussions?

Imagine you have developed a restaurant POS application and published its repository.

People might ask:

- Can this application support multiple restaurant branches?
- How can I configure a thermal printer?
- Which database should I use?
- Would it be useful to add WhatsApp ordering?
- What features are planned for the next release?

These questions do not necessarily represent bugs or development tasks.

Discussions give people a place to talk about them.

## 3. Discussions vs Issues vs Pull Requests

Understanding when to use each feature is important.

| Feature | Main purpose | Example |
|---|---|---|
| Discussions | Open-ended conversations | Should we support multiple branches? |
| Issues | Track actionable work | Implement multiple branch support |
| Pull Requests | Propose code changes | Add branch management functionality |

### 3.1 Example: A feature idea

A user creates a Discussion:

**Title:**

`Should the restaurant POS support multiple branches?`

Community members discuss:

- Whether the feature is useful.
- How branches should be represented.
- Whether products should be shared between branches.
- Whether each branch needs its own cashier.
- Whether reporting should be centralized.

After discussion, the maintainers decide to implement it.

They create an Issue:

`[FEAT] Add multi-branch restaurant support`

A developer implements the feature and opens a Pull Request.

The complete workflow:

```text
Community idea
      |
      v
GitHub Discussion
      |
      v
Community feedback
      |
      v
Decision to implement
      |
      v
GitHub Issue
      |
      v
Development branch
      |
      v
Pull Request
      |
      v
Code review
      |
      v
Merge
```

### 3.2 Decision table

| Situation | Use |
|---|---|
| A user asks how to configure something | Discussion |
| A user reports an application bug | Issue |
| A user proposes a new feature | Discussion |
| The team decides to implement that feature | Issue |
| A developer wants to submit code | Pull Request |
| Maintainers announce a release | Discussion announcement or GitHub Release |
| Contributors want to share their projects | Discussion |
| The team needs to track a development task | Issue |

**Important:** Discussions are not a replacement for Issues. They complement them.

## 4. Enable GitHub Discussions

We will use your training repository:

`github-deep-dive-training`

### Step 1 — Open repository settings

1. Open your repository on GitHub.
2. Click **Settings**.
3. Find the **Features** section.
4. Locate Discussions.
5. Select **Set up discussions** if the feature is disabled.

### Step 2 — Configure the welcome post

When enabling Discussions, GitHub may invite you to create a welcome post.

Use the following example.

**Title:**

`Welcome to GitHub Deep Dive Discussions`

**Content:**

```markdown
# Welcome to GitHub Deep Dive Discussions

Welcome to the community space for the GitHub Deep Dive training repository.

Use Discussions to:

- Ask questions about Git and GitHub.
- Share learning experiences.
- Discuss repository improvements.
- Suggest new training exercises.
- Share useful resources.
- Discuss development workflows.

## Before creating a discussion

1. Search existing discussions.
2. Choose the most appropriate category.
3. Provide enough context.
4. Keep discussions relevant to this project.
5. Follow the repository Code of Conduct.

For bugs and actionable development tasks, use GitHub Issues.

Thank you for participating!
```

Publish the welcome discussion.

GitHub Discussions can be enabled for public and private repositories, subject to the repository's availability and permissions. Discussion visibility follows the repository's visibility.

## 5. Understand discussion categories

Every Discussion belongs to a category.

Categories organize conversations and determine their format.

GitHub provides several default categories.

| Category | Purpose | Format |
|---|---|---|
| Announcements | Important project updates | Announcement |
| General | General conversations | Open-ended |
| Ideas | Suggestions and improvements | Open-ended |
| Polls | Community voting | Polls |
| Q&A | Questions and answers | Question and Answer |
| Show and tell | Share projects and experiments | Open-ended |

You can create additional categories depending on the project.

### 5.1 Understand the three main formats

**Open-ended discussion**

Used for conversations without a fixed question-and-answer structure.

Example:

`What should we improve in the next release?`

Members can discuss different possibilities.

**Question and Answer**

Used when someone asks a question and the community provides answers.

Example:

`How can I configure the local thermal printer?`

A useful response can be marked as the accepted answer.

**Announcement**

Used for important updates published by maintainers.

Examples:

- New release announcement.
- Maintenance announcement.
- Upcoming community event.
- Important project changes.

Announcement creation is restricted to people with the appropriate maintainer permissions.

## 6. Configure useful categories

For your training repository, create or retain these categories:

| Category | Format | Purpose |
|---|---|---|
| Announcements | Announcement | Important repository updates |
| General | Open-ended | General conversations |
| Questions | Q&A | Learning questions |
| Ideas | Open-ended | Suggestions for the training |
| Show and Tell | Open-ended | Share exercises and results |
| Git Help | Q&A | Git and GitHub troubleshooting |

You do not need every category in a small repository. Keep the structure understandable.

### 6.1 Create a category

1. Open the repository's Discussions tab.
2. Open the category management controls.
3. Select the option to create a category.
4. Enter a category name.
5. Add a description.
6. Choose the discussion format.
7. Save the category.

The available controls depend on your permissions and GitHub interface.

A category should have a clear purpose. Avoid creating multiple categories that serve exactly the same function.

## 7. Create your first Discussion

Create a new discussion in the `General` category.

**Title:**

`How should we organize our GitHub training repository?`

**Description:**

```markdown
## Background

This repository contains practical lessons for learning GitHub.

The training covers:

- Code and Git workflows.
- Issues and Pull Requests.
- GitHub Discussions.
- GitHub Actions.
- Projects.
- Security and quality.
- Repository administration.

## Question

What would make this training repository easier to navigate?

## Ideas

Some possibilities:

- Add a roadmap.
- Add diagrams.
- Add practical project scenarios.
- Add troubleshooting guides.
- Add a glossary of GitHub terminology.

## Feedback

Share your suggestions and explain why they would be useful.
```

Publish the Discussion.

Explore:

- Discussion title.
- Category.
- Conversation.
- Comments.
- Reactions.
- Labels.
- Author.
- Timeline.
- Sidebar options.

### 7.1 Add labels to Discussions

Discussions can use repository labels.

For example:

```text
question
idea
feedback
documentation
community
```

You can reuse labels already created for Issues and Pull Requests.

Use labels when they improve filtering. Do not create unnecessary duplicates.

## 8. Practice the Q&A workflow

Now create a Discussion in your `Questions` category.

**Title:**

`What is the difference between git fetch and git pull?`

**Content:**

```markdown
## Question

I am learning Git and want to understand the difference between
`git fetch` and `git pull`.

## What I understand so far

- Fetch downloads information from a remote repository.
- Pull retrieves remote changes and integrates them into my current branch.

## What I want to understand

1. Does fetch modify my working files?
2. Does pull always create a merge commit?
3. When should I prefer fetch?
4. How can I inspect remote changes before integrating them?

I would appreciate a practical example.
```

Publish the Discussion.

### 8.1 Add an answer

For practice, add a response explaining:

```markdown
## Answer

`git fetch` downloads updates from a remote repository without
automatically integrating them into your current branch.

Example:

`git fetch origin`

You can inspect incoming commits:

`git log --oneline HEAD..origin/main`

`git pull` fetches changes and then integrates them into the current branch.

Conceptually, it combines fetching with an integration operation.

For example:

`git pull origin main`

Depending on your Git configuration and options, integration may use
merge or rebase behavior.

A useful workflow is:

1. Fetch the latest changes.
2. Inspect incoming commits.
3. Decide whether to merge or rebase.
4. Integrate the changes.
```

### 8.2 Mark an accepted answer

In a Q&A category, maintainers or people with the necessary moderation permissions can mark a comment as the answer.

Practice:

1. Open the Discussion.
2. Find the answer comment.
3. Open its available actions.
4. Select **Mark as answer**.

The accepted answer becomes highlighted.

This helps future visitors find useful information without reading every comment.

**Important:** Mark an answer only when it genuinely answers the question. Do not mark your own practice response as accepted merely to complete the exercise if GitHub does not permit it under the current permissions or interface.

## 9. Understand Discussion moderation

Moderation keeps conversations useful and organized.

GitHub provides tools for:

- Pinning discussions.
- Closing discussions.
- Locking conversations.
- Changing categories.
- Editing or deleting inappropriate content.
- Marking answers.
- Managing discussion categories.

The exact actions available depend on the user's permissions.

### 9.1 Pin a Discussion

Pinning gives an important Discussion more visibility.

Examples:

- Welcome message.
- Community guidelines.
- Important project announcement.
- Frequently asked question.

GitHub allows up to four globally pinned discussions per repository or organization. You can also pin discussions within categories.

Practice:

1. Open your welcome Discussion.
2. Find the pin option.
3. Pin it globally if available.
4. Inspect how it appears on the Discussions page.

### 9.2 Close a Discussion

Close a Discussion when:

- The question has been answered.
- The conversation is no longer relevant.
- The discussion is a duplicate.
- The discussion has reached its conclusion.

Closing does not delete the conversation.

Practice:

1. Open your Q&A Discussion.
2. Scroll to the discussion controls.
3. Select **Close discussion**.
4. Inspect its new state.

### 9.3 Lock a Discussion

Locking prevents further comments.

It can be useful when:

- A conversation has become unproductive.
- A discussion has reached a final conclusion.
- Repeated unwanted comments need to be stopped.
- A conversation is no longer appropriate for continued participation.

A locked discussion may still allow reactions if the moderator enables them.

Locking and closing are different operations:

| Close | Lock |
|---|---|
| Marks the discussion as concluded | Restricts further conversation |
| Communicates that it is no longer active | Prevents additional comments |
| Can be reopened | Can be unlocked |

Do not lock discussions simply because someone disagrees with the maintainers. Moderation should be based on clear community rules.

## 10. Convert an Issue into a Discussion

Sometimes an Issue is created, but it turns out that the topic is better suited to an open conversation.

Example:

Issue:

`[FEATURE] Should we support dark mode?`

After reviewing it, the maintainers realize that they first need community feedback.

They can convert the Issue into a Discussion.

### Practice

1. Open an Issue in your training repository.
2. Locate the conversion option in its sidebar.
3. Select **Convert to discussion**.
4. Choose an appropriate category.
5. Confirm the conversion.

The content is transferred into the Discussion.

This is useful when a proposed feature needs discussion before the team decides whether to implement it.

**Remember:** An Issue represents tracked work. A Discussion represents conversation. If the conversation later produces a concrete development task, create an Issue.

## 11. Turn a Discussion into development work

A common workflow is:

```text
Discussion
    |
    v
Community feedback
    |
    v
Maintainer decision
    |
    v
Create an Issue
    |
    v
Add Issue to Project
    |
    v
Assign developer
    |
    v
Create feature branch
    |
    v
Open Pull Request
```

Example:

Discussion:

`Should we add WhatsApp order integration to the POS?`

Community feedback identifies the following requirements:

- Customers should be able to view the menu.
- Customers should be able to submit an order.
- Staff should confirm orders.
- Orders should be stored in the POS.
- Delivery details should be confirmed.

The team decides to implement the feature.

Create an Issue:

`[FEAT] Add WhatsApp order intake`

Issue description:

```markdown
## Background

The community discussed adding WhatsApp ordering support.

The team decided to implement an initial version.

## Scope

- Accept orders through WhatsApp.
- Display the available menu.
- Collect customer order details.
- Collect delivery location.
- Require staff confirmation.
- Store confirmed orders in the POS.

## Acceptance criteria

- [ ] Customer can browse the menu.
- [ ] Customer can submit an order request.
- [ ] Customer details are collected.
- [ ] Staff can review the order.
- [ ] Staff can confirm the order.
- [ ] Confirmed orders are stored in the POS.
- [ ] Automated tests cover the main workflow.

## Related discussion

Link to the original GitHub Discussion here.
```

You can reference the original Discussion URL in the Issue description to preserve context.

### 11.1 Avoid losing the original discussion

When creating an Issue from a Discussion:

- Link the original Discussion.
- Summarize the final decision.
- Preserve important requirements.
- Record unresolved questions.
- Avoid copying every comment unnecessarily.

The Issue should contain the information developers need to implement the work.

## 12. Community guidelines and moderation

A repository that accepts community participation should explain how people are expected to behave.

You created `CODE_OF_CONDUCT.md` in Lesson 6.

Discussions are one place where those guidelines are applied.

### 12.1 Recommended community rules

Your repository should encourage:

1. Respectful communication.
2. Constructive feedback.
3. Relevant discussions.
4. Clear technical explanations.
5. Respect for different opinions.
6. No harassment or personal attacks.
7. No publishing private credentials or sensitive information.
8. Reporting security problems through the documented security process.

### 12.2 Configure discussion guidelines

GitHub supports community contribution guidelines for Discussions.

You can use these to explain:

- Which category should be used.
- What information a question should include.
- How to report bugs.
- How to suggest features.
- What behavior is expected.
- Where to report security vulnerabilities.

Example text:

```markdown
# Discussion Guidelines

Thank you for participating in this project.

Before opening a Discussion:

1. Search existing discussions.
2. Select the appropriate category.
3. Write a descriptive title.
4. Provide enough context.
5. Include relevant technical information.
6. Keep the conversation focused.

## Questions

Include:

- What you are trying to achieve.
- What you have already tried.
- What result you expected.
- What happened instead.

## Ideas

Explain:

- The problem.
- Your proposed solution.
- The expected benefit.
- Possible alternatives.

## Bugs

Use GitHub Issues for reproducible bugs.

## Security

Do not publish sensitive credentials or exploit details in public discussions.
Follow the repository's SECURITY.md instructions.

All participants must follow the repository Code of Conduct.
```

## 13. Discussion templates and category forms

GitHub supports discussion category forms, which can standardize the information provided when people create discussions.

This is especially useful for categories such as Questions.

For example, a Q&A form can request:

- A question title.
- The relevant environment.
- What the user is trying to achieve.
- What they already tried.
- Error messages or supporting information.

You can manage category forms through the discussion category configuration.

A simplified example of a category form's YAML structure:

```yaml
title: Ask a question
description: Ask the community for help.
labels:
  - question
body:
  - type: markdown
    attributes:
      value: |
        Provide enough information for other members to understand your question.

  - type: textarea
    id: question
    attributes:
      label: Question
      description: Explain what you need help with.
    validations:
      required: true

  - type: textarea
    id: context
    attributes:
      label: Context
      description: Explain what you have tried so far.
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected result
      description: What result are you trying to achieve?
    validations:
      required: false
```

Treat this as a simplified structural example. Configure the form through the category's supported settings and follow the current GitHub category-form schema.

Do not confuse discussion category forms with the repository's Issue templates from Lesson 10.

## 14. Understand moderation permissions

Not everyone can manage Discussions.

A simplified permission overview:

| Action | Typical permission |
|---|---|
| Read public Discussions | Anyone with access to the public repository |
| Create a Discussion | Depends on repository settings and access |
| Comment on a Discussion | Depends on repository visibility and access |
| Manage categories | Maintainer or administrator permissions |
| Pin discussions | Appropriate moderation permissions |
| Mark answers | Triage or higher moderation access |
| Lock discussions | Triage or higher moderation access |
| Delete discussions | Higher repository permissions |

For organization Discussions, permissions are tied to the organization's discussion source repository and its access configuration.

Do not assume that every contributor has moderation rights.

## 15. Discussion search and organization

As a project grows, Discussions can become difficult to navigate.

Use categories, labels, and search to keep conversations organized.

Examples of discussion topics:

```text
category:Q&A
label:question
```

```text
category:Ideas
label:feedback
```

```text
category:General
label:documentation
```

GitHub's Discussions interface provides category navigation and search capabilities. Available filters can vary, so use the filters displayed in the current interface.

### Recommended organization

For a small open-source project:

| Category | Example |
|---|---|
| Announcements | Release v1.2.0 is available |
| Questions | How do I configure the application? |
| Ideas | Suggest a new feature |
| General | Discuss the project's roadmap |
| Show and Tell | Share an implementation |

Keep discussions organized without creating too many categories.

## 16. Practical exercise — Build a community workflow

Now create a small community workflow in your training repository.

### Exercise A — Enable Discussions

- [ ] Open repository Settings.
- [ ] Enable Discussions.
- [ ] Create a welcome post.
- [ ] Pin the welcome post if available.
- [ ] Inspect the Discussions tab.

### Exercise B — Configure categories

Use the existing categories or configure:

- [ ] Announcements.
- [ ] General.
- [ ] Questions.
- [ ] Ideas.
- [ ] Show and Tell.

Verify that each category has the intended format.

### Exercise C — Create sample Discussions

Create at least four Discussions:

**Discussion 1 — General**

Title:

```text
How should we structure the GitHub Deep Dive training?
```

**Discussion 2 — Q&A**

Title:

```text
When should I use git merge instead of git rebase?
```

**Discussion 3 — Ideas**

Title:

```text
Should we add a complete sample project to the training?
```

**Discussion 4 — Show and Tell**

Title:

```text
My progress with the GitHub Code tab
```

For each Discussion:

- [ ] Choose the correct category.
- [ ] Write a descriptive title.
- [ ] Provide useful context.
- [ ] Add appropriate labels.
- [ ] Add a comment or response.

### Exercise D — Practice moderation

- [ ] Pin the welcome Discussion.
- [ ] Mark a suitable Q&A response as an answer if the interface and permissions allow.
- [ ] Close a completed Discussion.
- [ ] Inspect the lock option.
- [ ] Change a Discussion category if appropriate.

### Exercise E — Convert an Issue

- [ ] Create a sample Issue describing a feature idea.
- [ ] Convert it into a Discussion.
- [ ] Select the Ideas category.
- [ ] Verify that the content was transferred.

### Exercise F — Convert a discussion into development work

- [ ] Create a feature proposal Discussion.
- [ ] Add comments identifying requirements.
- [ ] Decide whether the feature should be implemented.
- [ ] Create a new Issue containing the agreed requirements.
- [ ] Link the original Discussion in the Issue.
- [ ] Add the Issue to your GitHub Project.
- [ ] Assign an owner if appropriate.

### Exercise G — Document community guidelines

Review your existing:

```text
CODE_OF_CONDUCT.md
CONTRIBUTING.md
SECURITY.md
```

Make sure they explain how people should participate, contribute, and report security concerns.

If you change any documentation, create a branch and submit a Pull Request.

---

## 17. Best practices

### Rule 1 — Use Discussions for conversations

Do not create an Issue for every question or suggestion.

### Rule 2 — Use Issues for actionable work

Once the team decides to implement something, track it with an Issue.

### Rule 3 — Keep categories meaningful

Categories should help people find the right place for their conversations.

### Rule 4 — Use Q&A for questions

Mark useful answers when appropriate.

### Rule 5 — Pin important information

Use pinned discussions for welcome messages, important announcements, and frequently needed information.

### Rule 6 — Moderate consistently

Apply the Code of Conduct fairly and consistently.

### Rule 7 — Preserve context

When a Discussion leads to an Issue, link the two.

### Rule 8 — Do not expose confidential information

Never publish passwords, API keys, private customer data, or confidential business information in public Discussions.

### Rule 9 — Avoid unnecessary notifications

Keep conversations focused and avoid repeatedly mentioning contributors who do not need to participate.

### Rule 10 — Close completed conversations

Keep the Discussions page useful by closing conversations that have reached a conclusion.

---

## 18. Important concepts reference

| Concept | Purpose |
|---|---|
| Discussion | Community conversation |
| Category | Organizes discussions |
| Open-ended format | General conversation |
| Q&A format | Question and answer |
| Announcement format | Maintainer updates |
| Accepted answer | Highlights the useful response |
| Pin | Gives a discussion more visibility |
| Close | Marks a discussion as concluded |
| Lock | Prevents further comments |
| Convert Issue to Discussion | Moves an open-ended topic out of task tracking |
| Issue | Tracks actionable development work |
| Project | Organizes development work |

## 19. Lesson completion checklist

- [ ] I understand GitHub Discussions.
- [ ] I can distinguish Discussions from Issues and Pull Requests.
- [ ] I enabled Discussions in my repository.
- [ ] I created a welcome post.
- [ ] I understand discussion categories.
- [ ] I can create open-ended discussions.
- [ ] I can create Q&A discussions.
- [ ] I understand announcement discussions.
- [ ] I can mark a response as an answer when permitted.
- [ ] I understand pinning and closing.
- [ ] I understand locking.
- [ ] I can convert an Issue into a Discussion.
- [ ] I can turn a Discussion into an actionable Issue.
- [ ] I understand moderation permissions.
- [ ] I reviewed the community guidelines.
- [ ] I completed the practical exercises.

## 20. Commit and push this lesson

Return to your local `github-deep-dive-training` repository.

Inspect your current state:

```bash
git status
git branch
```

Update your local main branch:

```bash
git switch main
git pull origin main
```

Create a documentation branch:

```bash
git switch -c docs/add-github-discussions-lesson
```

Create:

```text
docs/github/module-01-code/lesson-11-github-discussions-and-community-collaboration.md
```

Paste this lesson into the file.

Update:

```text
docs/github/module-01-code/README.md
```

Add Lesson 11 to the module index.

Inspect:

```bash
git status
git diff
```

Stage:

```bash
git add docs/github/module-01-code/
```

Review staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add discussions and community collaboration lesson"
```

Push:

```bash
git push -u origin docs/add-github-discussions-lesson
```

Open a Pull Request into `main`.

Follow the workflow from Lesson 8:

1. Create a Pull Request.
2. Review the description.
3. Inspect Files changed.
4. Request a review if another collaborator is available.
5. Resolve feedback.
6. Merge the Pull Request.
7. Delete the feature branch if appropriate.

## 21. Official documentation

Use these resources while practicing:

- [About GitHub Discussions](https://docs.github.com/en/discussions/collaborating-with-your-community-using-discussions/about-discussions)
- [Quickstart for GitHub Discussions](https://docs.github.com/en/discussions/quickstart)
- [Managing Discussions](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-discussions)
- [Managing Discussion Categories](https://docs.github.com/en/discussions/managing-discussions-for-your-community/managing-categories-for-discussions)
- [Moderating Discussions](https://docs.github.com/en/discussions/managing-discussions-for-your-community/moderating-discussions)

## 22. What comes next?

**Lesson 12 — GitHub Releases, Release Management, and Changelogs**

We will build on Lesson 5 and learn how to manage releases in a real development workflow:

- Release lifecycle.
- Semantic Versioning in practice.
- Tags versus GitHub Releases.
- Draft releases and prereleases.
- Release notes and generated changelogs.
- Maintaining `CHANGELOG.md`.
- Managing hotfix releases.
- Release branches and version progression.
- Connecting Issues and Pull Requests to releases.
- Preparing a complete release for a sample project.

**Module 1 reminder:** Keep using tags and GitHub Releases for meaningful milestones. Do not create a release for every lesson. Finish the required practical exercises before preparing the next module milestone.
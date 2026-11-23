# Lesson 27 — Advanced Issues: Discussions, Triage, Lifecycle, and Team Collaboration

This lesson follows the same hands-on teaching pattern as Lesson 25: clear explanations, practical GitHub exercises, realistic examples, concrete deliverables, validation steps, and a complete Git branch → Pull Request → merge → tag → Release workflow.

I'll also make a few improvements to the supplied lesson:

- Distinguish native GitHub Issue states from workflow labels.
- Separate Discussions, Issues, and GitHub Projects responsibilities.
- Make the triage process more actionable with clear decisions and examples.
- Clarify which exercises require a second repository or another GitHub account.
- Keep the exercises connected to the restaurant-management application scenario.

## Module 2 — GitHub Issues

### Lesson 27 — Advanced Issues: Discussions, Triage, Lifecycle and Team Collaboration

**Level:** Intermediate → Advanced\
**Estimated time:** 3–4 hours\
**Repository:** `github-deep-dive-training`\
**Module:** 2 — GitHub Issues\
**Previous lesson:** Lesson 26 — Issue Management\
**Next lesson:** Lesson 28 — Pull Requests Fundamentals

---

## 1. Lesson Overview

In Lesson 26, you learned how to create and manage GitHub Issues, organize them with labels and milestones, use Issue templates, connect Issues to Pull Requests, and automate basic Issue management.

In this lesson, you will build a more complete Issue-management workflow.

You will learn how to:

- Decide whether information belongs in an Issue or a Discussion.
- Configure Discussion categories.
- Convert a conversation into actionable work.
- Review and classify incoming Issues through triage.
- Use saved replies to improve communication.
- Coordinate responses between maintainers and developers.
- Reference Issues across repositories.
- Manage an Issue from submission to completion.
- Review stale and inactive Issues.
- Manage notifications and subscriptions.
- Coordinate work across multiple repositories.

### Practical scenario

Your team maintains a restaurant-management application.

The application contains:

- Authentication
- Restaurant management
- Products and categories
- Orders
- Kitchen Display System (KDS)
- Cashier and payments
- Reports
- Infrastructure and deployment

Users and developers interact with the project in different ways:

- A user reports that the cashier total is incorrect.
- A restaurant owner asks how to connect a thermal printer.
- A developer proposes a new order-status workflow.
- A contributor requests Arabic translations.
- A maintainer announces a new release.
- A developer discovers that a bug affects multiple repositories.

Your responsibility is to organize these conversations so that important work is trackable, understandable, and assigned to the right people.

---

## 2. Learning Objectives

By the end of this lesson, you should be able to:

1. Explain the difference between GitHub Issues and Discussions.
2. Enable Discussions and organize categories.
3. Create useful Discussions.
4. Convert a Discussion into an Issue when appropriate.
5. Design a repeatable Issue-triage process.
6. Use labels to communicate Issue status and priority.
7. Create and use saved replies.
8. Coordinate collaborative Issue discussions.
9. Reference Issues and Pull Requests across repositories.
10. Understand the complete Issue lifecycle.
11. Close and reopen Issues correctly.
12. Review stale and inactive Issues.
13. Manage notifications and subscriptions.
14. Coordinate work across multiple repositories.
15. Complete a realistic Issue-management project.
16. Document and release the completed lesson.

---

## 3. Discussions vs Issues

GitHub provides two collaboration features that are related but serve different purposes.

### 3.1 GitHub Issues

Issues are used to track work.

Typical examples:

- Bug reports
- Feature requests
- Documentation improvements
- Technical tasks
- Maintenance work
- Refactoring
- Infrastructure improvements

An Issue should normally have a clear objective and an identifiable next action.

Example:

**Issue title:**

`bug: cashier total is incorrect after refund`

The Issue should explain:

- What is happening?
- What should happen?
- How can the problem be reproduced?
- Who is responsible for investigating it?
- What would count as a completed fix?

### 3.2 GitHub Discussions

Discussions are intended for conversations that do not necessarily represent actionable work.

Typical examples:

- Questions and answers
- Architectural ideas
- General feedback
- Announcements
- Community conversations
- Sharing demonstrations
- Exploring possible improvements

Example:

**Discussion title:**

`How should we organize our restaurant application documentation?`

The team can discuss different documentation structures before deciding whether implementation work is necessary.

### 3.3 Practical comparison

| Situation                               | Recommended feature | Reason                            |
| --------------------------------------- | ------------------- | --------------------------------- |
| Login button crashes                    | Issue               | Bug needs investigation           |
| Add dark mode                           | Issue               | Feature needs implementation      |
| How do I configure the local server?    | Discussion          | General question                  |
| What database should we use?            | Discussion          | Open-ended technical conversation |
| Announce a new release                  | Discussion          | Information sharing               |
| Fix incorrect installation instructions | Issue               | Documentation work                |
| Discuss a possible architecture change  | Discussion          | Proposal needs feedback           |
| Implement an agreed architecture change | Issue               | Work needs tracking               |

### 3.4 How Discussions and Issues work together

A useful workflow is:

1. Someone proposes an idea in a Discussion.
2. Team members provide feedback.
3. The team evaluates the proposal.
4. The team agrees on an implementation.
5. An Issue is created to track the work.
6. A developer implements the change through a Pull Request.
7. The Issue is closed when the work is completed.

**Important principle:**

A Discussion helps the team decide what should happen. An Issue tracks work that the team has decided to do.

### Exercise 1 — Classify incoming conversations

For each situation, decide whether you would create an Issue or a Discussion.

1. A restaurant owner asks how to install the application.
2. The kitchen display stops updating after an order becomes ready.
3. A developer proposes using Redis for background processing.
4. A user requests Arabic translations.
5. The team wants to announce a new application release.
6. A contributor discovers that the installation guide contains incorrect commands.

**Expected deliverable:**

Create a Markdown file:

`docs/github/module-02-issues/exercises/lesson-27-conversation-classification.md`

Record your decisions and explain why each item belongs in an Issue or Discussion.

---

## 4. Enable and Configure GitHub Discussions

Discussions must be enabled for a repository before you can use them.

### 4.1 Enable Discussions

1. Open your `github-deep-dive-training` repository.
2. Navigate to **Settings**.
3. Locate the repository Features section.
4. Find the Discussions option.
5. Enable Discussions if available.
6. Return to the repository homepage.
7. Open the Discussions tab.

The exact interface may vary depending on GitHub's current interface and your repository permissions.

### 4.2 Verify the feature

After enabling Discussions, confirm that:

- The Discussions tab is visible.
- You can create a new Discussion.
- You can select a category.
- You can view and respond to existing Discussions.

If the feature is unavailable, record the limitation in your lesson notes rather than pretending the exercise was completed.

### Exercise 2 — Create your first Discussion

**Title:**

`How should we organize our restaurant application documentation?`

**Body:**

```text
## Context

Our application contains several modules:

- Authentication
- Restaurant management
- Products and categories
- Orders
- Kitchen display
- Reports

## Question

How should we organize the documentation so that
developers can find information quickly?

## Ideas

- Organize documentation by application module.
- Create architecture documentation.
- Add setup and deployment guides.

What structure would you recommend?
```

Create the Discussion in an appropriate category.

Do not create an Issue yet. First, practice collecting feedback and discussing the proposal.

**Expected result:**

One Discussion containing a clear question, context, and proposed ideas.

---

## 5. Discussion Categories

Discussion categories help organize conversations.

Common categories include:

| Category      | Purpose                        | Example                    |
| ------------- | ------------------------------ | -------------------------- |
| Announcements | Important updates              | New release announcement   |
| General       | Open-ended conversations       | Project feedback           |
| Q&A           | Questions and answers          | How to configure a printer |
| Ideas         | Suggestions and proposals      | Improve order management   |
| Show and Tell | Demonstrations and shared work | Show a new dashboard       |

GitHub may provide default categories and allow repository maintainers to customize them.

### 5.1 Design categories for a software project

For the restaurant-management application, consider:

| Category                | What belongs here                        |
| ----------------------- | ---------------------------------------- |
| Announcements           | Releases and important updates           |
| Questions & Answers     | Installation and configuration questions |
| Feature Ideas           | Suggestions for future functionality     |
| Development Discussions | Architecture and technical proposals     |
| Show and Tell           | Demonstrations and completed experiments |

Avoid creating too many categories. A category should make conversations easier to find.

### Exercise 3 — Design your Discussion categories

Create a category plan for your training project.

For each category, document:

- Category name
- Category purpose
- Example conversation
- Whether it should support Q&A behavior, if available

**Expected deliverable:**

`docs/github/module-02-issues/exercises/lesson-27-discussion-categories.md`

Example:

```text
# Discussion Category Plan

## 1. Announcements

Purpose:
Important project updates and releases.

Example:
Restaurant platform version 1.0.0 has been released.

## 2. Questions & Answers

Purpose:
Help contributors understand the project.

Example:
How can I configure the local development environment?

## 3. Feature Ideas

Purpose:
Collect and evaluate proposed improvements.

Example:
Should the KDS support configurable notification sounds?
```

---

## 6. Converting Discussions into Issues

Not every Discussion should become an Issue.

A conversation should become an Issue when the team has identified actionable work that needs ownership and progress tracking.

### 6.1 Practical example

Imagine the team starts a Discussion:

`Should the kitchen display support notification sounds?`

Participants discuss:

- Whether notification sounds are useful.
- Whether users should be able to disable them.
- Accessibility considerations.
- Browser audio permissions.
- Whether the sound should repeat.

After the discussion, the team agrees to implement the feature.

At this point, create an Issue.

### 6.2 Example Issue

**Title:**

`feat(kds): add configurable order-ready notification sound`

**Body:**

```text
## Background

The team discussed notification sounds in GitHub Discussions.

We agreed that the kitchen display should provide
an optional sound when an order becomes ready.

## Requirements

- Add a notification sound setting.
- Allow users to enable or disable the sound.
- Avoid repeatedly playing the same notification.
- Respect browser audio permissions.

## Acceptance Criteria

- [ ] A setting controls the notification sound.
- [ ] Disabled sounds remain disabled.
- [ ] New ready orders trigger the configured sound.
- [ ] Existing KDS functionality remains operational.

## Related Discussion

Paste the original Discussion URL here.
```

### 6.3 Conversion methods

Depending on the Discussion and available GitHub functionality, you may be able to use a direct conversion action.

If the conversion option is unavailable:

1. Create a new Issue.
2. Copy the agreed implementation requirements.
3. Include the original Discussion URL.
4. Reference the Discussion from the Issue.
5. Add appropriate labels.
6. Assign ownership when the work is ready.

The important result is preserving the relationship between the original conversation and the implementation work.

### Exercise 4 — Convert a Discussion into actionable work

Use your documentation Discussion from Exercise 2.

Imagine the team agrees to create:

- A setup guide.
- An architecture guide.
- Module-specific documentation.
- A deployment guide.

Create an Issue:

**Title:**

`docs: organize restaurant application documentation`

Include:

- Background
- Agreed requirements
- Acceptance criteria
- Original Discussion URL

**Expected result:**

One actionable Issue linked to the original Discussion.

---

## 7. Advanced Issue Triage

Triage is the process of reviewing incoming Issues and deciding what should happen next.

A good team does not immediately assign every incoming Issue to a developer.

First, maintainers should check whether the report is:

- Understandable
- Reproducible
- Relevant to the project
- Complete enough to investigate
- A duplicate of an existing report
- Suitable for implementation

### 7.1 Suggested triage workflow

```text
                  NEW ISSUE
                      |
                      v
                INITIAL REVIEW
                      |
                      v
           Is the report understandable?
                 /          \
               No            Yes
               |              |
               v              v
        Request details    Classify Issue
               |              |
               v              v
       needs-information   bug / feature / docs
                              |
                              v
                       Validate the report
                              |
                              v
                       Set priority
                              |
                              v
                       Assign ownership
                              |
                              v
                       Plan the work
```

This is a recommended team workflow, not a mandatory GitHub-native state machine.

### 7.2 Recommended labels

| Label               | Meaning                       |
| ------------------- | ----------------------------- |
| `needs-triage`      | Not reviewed yet              |
| `needs-information` | More details required         |
| `confirmed`         | Report has been validated     |
| `priority:critical` | Requires urgent attention     |
| `priority:high`     | Important work                |
| `priority:medium`   | Normal priority               |
| `priority:low`      | Lower priority                |
| `duplicate`         | Already reported elsewhere    |
| `wontfix`           | Team decided not to implement |
| `good first issue`  | Suitable for a newcomer       |
| `in-progress`       | Implementation has started    |
| `blocked`           | Work cannot proceed yet       |

These are suggested naming conventions. GitHub does not automatically assign these meanings to custom labels.

### 7.3 Triage decision example

Incoming Issue:

`bug: cashier total is incorrect after refund`

Initial review:

- Is the problem described clearly? Yes.
- Is there a reproduction scenario? Not yet.
- Is the report related to the project? Yes.
- Is it already reported? Unknown.

Possible action:

1. Add `needs-triage`.
2. Ask for the reproduction steps.
3. Add `needs-information`.
4. Remove `needs-triage` when the initial review is complete.
5. Confirm the problem when sufficient evidence is available.
6. Set an appropriate priority.
7. Assign an owner when the team is ready.

### Exercise 5 — Triage three Issues

Create these Issues:

#### Issue A

`bug: cashier total is incorrect after refund`

#### Issue B

`feature: export daily sales report to PDF`

#### Issue C

`question: how can I configure a kitchen printer?`

For each Issue:

1. Apply appropriate labels.
2. Decide whether it needs a priority.
3. Decide whether it needs an assignee.
4. Decide whether it belongs in a milestone.
5. Add a triage comment explaining your decision.

**Expected result:**

Three Issues with clear classifications and next actions.

---

## 8. Saved Replies

Saved replies allow you to reuse common responses instead of repeatedly writing the same explanation.

They are useful for:

- Requesting missing reproduction steps.
- Asking for logs or environment details.
- Explaining how to report a bug.
- Directing users to documentation.
- Explaining duplicate reports.
- Acknowledging accepted feature requests.

### 8.1 Create saved replies

Open your GitHub account's saved replies settings and create reusable responses.

The exact location may vary with GitHub's interface.

### 8.2 Saved reply examples

#### Reply 1 — Request more information

```text
Thanks for reporting this issue.

Could you provide the following information?

- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Browser or application version
- Relevant error messages

This will help us investigate the problem.
```

#### Reply 2 — Cannot reproduce

```text
Thanks for the report.

We attempted to reproduce this behavior but
could not observe the same result.

Could you provide additional steps or an example
that consistently reproduces the problem?
```

#### Reply 3 — Duplicate Issue

```text
Thanks for reporting this.

A similar issue has already been reported.

Please follow the existing Issue for updates:
[LINK TO EXISTING ISSUE]

We will keep the original report as the main
tracking location for this problem.
```

#### Reply 4 — Documentation reference

```text
Thanks for your question.

Please check the existing documentation first.

If the information is missing or unclear, please
tell us which section needs improvement.
```

#### Reply 5 — Feature accepted

```text
Thanks for suggesting this improvement.

The team has reviewed the proposal and agreed
that it is worth implementing.

We will track the implementation through a
separate GitHub Issue.
```

### Exercise 6 — Build a response library

Create at least five saved replies.

Suggested names:

1. Request more information
2. Cannot reproduce
3. Duplicate Issue
4. Documentation reference
5. Feature accepted

Use a consistent and respectful tone.

Saved replies should accelerate communication, not replace individual review.

**Expected result:**

A reusable collection of five saved replies.

---

## 9. Collaborative Issue Responses

An Issue can involve multiple participants.

A maintainer, reporter, backend developer, frontend developer, and tester may all contribute information.

### 9.1 Practical scenario

**Issue:**

`bug: cashier daily total is incorrect after refund`

Example conversation:

**Reporter:**

The cashier's daily total does not appear correct after a refund.

**Maintainer:**

Can you confirm whether the refund is recorded as a separate transaction?

**Backend developer:**

I can reproduce this when the payment record is updated but the daily summary is not recalculated.

**Frontend developer:**

The dashboard currently displays the total returned by the daily-summary endpoint.

**Maintainer:**

The issue appears to be related to the backend calculation. I will assign the investigation to the backend developer.

### 9.2 Recommended collaboration process

1. Reporter describes the problem.
2. Maintainer requests missing information.
3. Developer investigates.
4. Other team members provide relevant technical findings.
5. Maintainer confirms ownership and next steps.
6. Developer implements the solution through a Pull Request.
7. The team reviews the Pull Request.
8. The Issue is closed after the fix is merged.

### 9.3 Q&A Discussions

In a Q&A Discussion, an appropriate participant can mark a response as the answer when the category supports that behavior.

This helps future readers identify the accepted solution without reading the entire conversation.

### Exercise 7 — Practice collaborative responses

Use your documentation Discussion.

Add at least two meaningful responses.

For example:

**Contributor 1:**

I recommend organizing documentation by application module.

**Contributor 2:**

I agree, but we should also have a central architecture guide and a deployment guide.

Then identify the agreed documentation structure.

If you are using a Q&A category, practice marking an appropriate response as the answer when the feature is available.

---

## 10. Issue References Across Repositories

GitHub supports references to Issues and Pull Requests across repositories.

### 10.1 Reference formats

```text
#42
owner/repository#42
```

Examples:

```text
#42
yassine-B/restaurant-backend#18
```

The first reference generally identifies an Issue in the current repository.

The fully qualified reference identifies an Issue in another repository.

### 10.2 Practical scenario

Imagine you maintain two repositories:

```text
restaurant-backend
restaurant-frontend
```

The frontend team needs a backend endpoint before implementing a feature.

Create a backend Issue:

`api: provide daily sales summary endpoint`

Then reference it from the frontend Issue:

```text
## Dependency

The frontend implementation requires the daily sales
summary endpoint.

Backend tracking issue:

yassine-B/restaurant-backend#18
```

Replace the example repository and Issue number with real values when you perform the exercise.

### 10.3 Why cross-repository references matter

They help teams:

- Identify dependencies.
- Understand related work.
- Avoid duplicating tasks.
- Coordinate implementation.
- Track work across separate codebases.

### Exercise 8 — Create a cross-repository dependency

Create two Issues:

**Frontend Issue:**

`feature: display daily sales summary`

**Backend Issue:**

`api: provide daily sales summary endpoint`

Reference the backend Issue from the frontend Issue.

If you do not have a second repository, record the example in your lesson notes. Do not create a reference that looks like a real dependency when the repository or Issue does not exist.

---

## 11. Issue Lifecycle Management

A useful Issue lifecycle is more detailed than simply opening and closing an Issue.

### 11.1 Recommended lifecycle

| Stage             | Typical action                     |
| ----------------- | ---------------------------------- |
| New               | Issue is submitted                 |
| Triage            | Maintainer reviews it              |
| Needs information | Reporter is asked for details      |
| Confirmed         | Team validates the report          |
| Planned           | Work is prioritized                |
| In progress       | Developer begins implementation    |
| In review         | Pull Request is available          |
| Completed         | Work is merged and Issue is closed |
| Reopened          | Problem remains or returns         |

### 11.2 Native Issue states vs workflow labels

GitHub's built-in Issue state is primarily:

- Open
- Closed

Labels such as `in-progress`, `blocked`, and `confirmed` are additional workflow conventions.

They do not create new native Issue states.

For example:

| Native state | Label          | Meaning                  |
| ------------ | -------------- | ------------------------ |
| Open         | `needs-triage` | Awaiting review          |
| Open         | `confirmed`    | Validated                |
| Open         | `in-progress`  | Being implemented        |
| Open         | `blocked`      | Waiting for a dependency |
| Closed       | `completed`    | Work completed           |

Teams can also use GitHub Projects to manage richer workflow states such as Todo, In Progress, and Done.

### 11.3 Closing Issues through Pull Requests

GitHub can automatically close an Issue when a linked Pull Request is merged into the repository's default branch.

Example Pull Request description:

```text
Closes #42
```

Other supported closing keywords include:

```text
Fixes #42
Resolves #42
```

Use these keywords only when the Pull Request actually resolves the referenced Issue.

### 11.4 Reopening an Issue

Sometimes a problem returns after a fix.

For example:

- A bug was closed.
- A new release was deployed.
- The reporter discovers that the same behavior still occurs.

The maintainer can reopen the Issue and request further investigation.

### Exercise 9 — Complete an Issue lifecycle

Use your KDS notification Issue.

1. Add the `confirmed` label.
2. Add an `in-progress` label when work starts.
3. Create a branch for the implementation exercise.
4. Open a Pull Request.
5. Reference the Issue using `Closes #ISSUE_NUMBER`.
6. Merge the Pull Request when the exercise is complete.
7. Confirm that GitHub closed the Issue.

You can use a documentation-only Pull Request for this training exercise. You do not need to implement a real notification system.

---

## 12. Stale and Inactive Issues

Repositories accumulate Issues that have not received updates.

Examples:

- A reporter never provides requested information.
- A feature request is no longer relevant.
- A bug has already been fixed.
- An Issue has no owner or clear next action.
- A proposed improvement is no longer supported by the project.

A stale Issue is not automatically an invalid Issue.

### 12.1 Review inactive Issues

A recommended maintenance process:

1. Find open Issues that have not been updated recently.
2. Review their context and current relevance.
3. Check whether the problem has already been resolved.
4. Ask the reporter for an update when appropriate.
5. Add a `stale` label only when it reflects your team's policy.
6. Close the Issue only when there is a clear reason.
7. Reopen it if new evidence shows that the problem remains relevant.

### 12.2 GitHub Issue search

Example:

```text
is:issue is:open updated:<2026-10-01
```

This finds open Issues that were last updated before October 1, 2026.

You can change the date to suit your review.

Other useful searches:

```text
is:issue is:open no:assignee
```

Find open Issues without an assignee.

```text
is:issue is:open label:needs-information
```

Find open Issues waiting for additional information.

```text
is:issue is:open label:bug
```

Find open bug reports.

```text
is:issue is:closed
```

Find closed Issues.

### 12.3 Optional stale Issue automation

A repository can use GitHub Actions and a third-party action such as `actions/stale` to identify inactive Issues.

For this lesson, practice the process manually first.

If you introduce automation later:

- Review the action's source code and maintenance status.
- Pin third-party actions to a full commit SHA.
- Start with labeling rather than automatic closure.
- Avoid closing important reports without review.
- Document the team's inactivity policy.

### Exercise 10 — Review stale Issues

1. Open your training repository's Issues tab.
2. Search for open Issues.
3. Review any inactive Issues.
4. Decide whether each one still requires attention.
5. Add an appropriate label or comment.
6. Document why you would keep, reopen, or close each Issue.

**Expected deliverable:**

`docs/github/module-02-issues/exercises/lesson-27-stale-issue-review.md`

---

## 13. Notifications and Subscriptions

GitHub notifications help you follow work without repeatedly checking every repository.

You may receive notifications when:

- Someone comments on an Issue you participate in.
- Someone mentions your username.
- A Pull Request references an Issue.
- A subscribed conversation receives an update.
- A repository event matches your notification settings.

### 13.1 Subscribe to an Issue

1. Open an Issue.
2. Locate its subscription control.
3. Subscribe to the conversation.
4. Follow its updates through GitHub notifications.

You can unsubscribe when you no longer need to follow it.

### 13.2 Repository watching vs Issue subscriptions

These actions are different.

| Action                    | Scope                                                                  |
| ------------------------- | ---------------------------------------------------------------------- |
| Watch a repository        | Notifications for selected repository activity                         |
| Subscribe to an Issue     | Notifications for a particular Issue                                   |
| Subscribe to a Discussion | Notifications for a particular Discussion                              |
| Mention a user            | Directly notifies the mentioned user, subject to notification settings |

### Exercise 11 — Manage subscriptions

1. Open one of your test Issues.
2. Subscribe to it.
3. Add a comment.
4. Review your notifications.
5. Unsubscribe when finished.
6. Review your GitHub notification settings.

If you have access to another account, use it to add a comment and observe the notification behavior.

---

## 14. Multi-Repository Issue Management

A real software product often has several repositories.

Example:

```text
restaurant-platform/
│
├── restaurant-backend/
├── restaurant-frontend/
├── restaurant-mobile/
├── restaurant-kds/
├── restaurant-infrastructure/
└── restaurant-documentation/
```

A single feature may require work in multiple repositories.

### 14.1 Practical example: Add a new order status

Imagine the product team wants to introduce a new order status called `waiting_for_pickup`.

Different repositories may need changes.

| Repository    | Required work              |
| ------------- | -------------------------- |
| Backend       | Add status and API support |
| Frontend      | Display the new status     |
| KDS           | Update kitchen workflow    |
| Mobile        | Update order tracking      |
| Documentation | Explain the new status     |

### 14.2 Recommended approach

1. Create a central tracking Issue or GitHub Project item.
2. Create repository-specific Issues for implementation.
3. Link related Issues using cross-repository references.
4. Assign each task to the appropriate owner.
5. Use milestones or Projects to track the overall feature.
6. Close each Issue when its own work is complete.
7. Close the central tracking item when the overall feature is complete.

### 14.3 Why not use one large Issue?

One large Issue can become difficult to manage when several teams are involved.

Separate Issues provide:

- Clear ownership.
- Independent progress tracking.
- Better Pull Request relationships.
- Easier assignment.
- More precise completion criteria.

### Exercise 12 — Design a multi-repository feature

Create a Markdown planning document for the new order status.

Include:

- Central feature description.
- Backend task.
- Frontend task.
- KDS task.
- Mobile task.
- Documentation task.
- Dependencies.
- Suggested owners.

**Expected deliverable:**

`docs/github/module-02-issues/exercises/lesson-27-multi-repository-planning.md`

You can use hypothetical repositories for the planning exercise. Clearly identify them as examples.

---

## 15. Advanced Practical Project — Restaurant Platform Triage

Now apply everything from Lessons 26 and 27.

Imagine your application has received the following reports:

| ID    | Report                                                       | Type          |
| ----- | ------------------------------------------------------------ | ------------- |
| R-001 | Cashier total is incorrect after a refund                    | Bug           |
| R-002 | Add an export option for daily sales                         | Feature       |
| R-003 | How do I connect a thermal printer?                          | Question      |
| R-004 | Kitchen display does not update after an order becomes ready | Bug           |
| R-005 | Add Arabic translations to the customer menu                 | Feature       |
| R-006 | Installation guide is missing Docker instructions            | Documentation |

### 15.1 Create the conversations

Create Issues for:

- R-001
- R-002
- R-004
- R-005
- R-006

Create a Discussion for:

- R-003

### 15.2 Apply triage

For every Issue:

- Add appropriate labels.
- Set an appropriate priority.
- Decide whether more information is required.
- Assign an owner where appropriate.
- Add a triage comment.

### 15.3 Organize the work

Create a milestone:

**Name:**

`Restaurant Platform — Issue Management Practice`

**Description:**

```text
Practice milestone for managing incoming reports,
triage, assignment, collaboration and completion.
```

Add at least one Issue to the milestone.

### 15.4 Connect conversations

- Link one Issue to a Discussion.
- Add a cross-repository reference, if you have a second repository.
- Document one dependency between two Issues.
- Add a relevant saved reply to an Issue.

### 15.5 Complete work

Choose one Issue and:

1. Create a branch.
2. Make a small documentation change.
3. Open a Pull Request.
4. Reference the Issue with a closing keyword.
5. Merge the Pull Request.
6. Confirm the Issue is closed.

### 15.6 Review notifications

Subscribe to one Issue and one Discussion.

Review the notifications and unsubscribe when finished.

### Final project deliverable

Create:

`docs/github/module-02-issues/projects/lesson-27-restaurant-platform-triage.md`

Document:

- The six incoming reports.
- Your Issue vs Discussion decisions.
- Applied labels and priorities.
- Assignment decisions.
- Milestone organization.
- Discussion-to-Issue relationship.
- Cross-repository dependency.
- Completed Pull Request.
- Notification review.
- Lessons learned.

---

## 16. Document the Lesson in Your Training Repository

Create the following file:

```text
docs/
└── github/
    └── module-02-issues/
        ├── lesson-26-issue-management.md
        ├── lesson-27-advanced-issues.md
        ├── exercises/
        │   ├── lesson-27-conversation-classification.md
        │   ├── lesson-27-discussion-categories.md
        │   ├── lesson-27-stale-issue-review.md
        │   ├── lesson-27-multi-repository-planning.md
        │   └── ...
        └── projects/
            └── lesson-27-restaurant-platform-triage.md
```

### Required lesson documentation structure

```text
# Lesson 27 — Advanced GitHub Issues

## 1. Lesson Overview

## 2. Learning Objectives

## 3. Discussions vs Issues

## 4. Enable and Configure GitHub Discussions

## 5. Discussion Categories

## 6. Converting Discussions into Issues

## 7. Advanced Issue Triage

## 8. Saved Replies

## 9. Collaborative Issue Responses

## 10. Issue References Across Repositories

## 11. Issue Lifecycle Management

## 12. Stale and Inactive Issues

## 13. Notifications and Subscriptions

## 14. Multi-Repository Issue Management

## 15. Advanced Practical Project

## 16. Lessons Learned

## 17. Completion Checklist

## 18. Official Documentation
```

### Documentation requirements

Your Markdown file should:

- Explain the purpose of each GitHub feature.
- Include practical examples.
- Include commands and search filters where appropriate.
- Include screenshots from your own exercises where useful.
- Record unavailable features or permission limitations.
- Link to relevant Issues, Discussions, and Pull Requests.
- Include your practical project results.

Do not include passwords, access tokens, or other secrets in screenshots or documentation.

---

## 17. Validation — Verify Your Work

Before opening the documentation Pull Request, review your work.

### Repository validation

- Lesson file exists in the correct directory.
- Markdown headings are organized correctly.
- Code blocks have the correct language identifiers.
- Links are valid.
- Screenshots are relevant and readable.
- No secrets or private information are included.

### GitHub exercise validation

- Discussions enabled, if available.
- At least one Discussion created.
- Discussion categories reviewed.
- One Discussion connected to an Issue.
- Three sample Issues triaged.
- Saved replies created.
- Collaborative responses practiced.
- Cross-repository references understood.
- Issue lifecycle completed.
- Stale Issue review completed.
- Notifications and subscriptions reviewed.
- Multi-repository workflow documented.
- Restaurant platform triage project completed.

### Git validation

Run:

```text
git status
git diff --check
git diff
```

Review the changes before committing.

---

## 18. Git Workflow — Commit, PR, Tag and Release

Use the same repository workflow practiced in previous lessons.

### Step 1 — Create your branch

```text
git switch main
git pull origin main

git switch -c docs/lesson-27-advanced-issues
```

### Step 2 — Create the lesson file

Create:

```text
docs/github/module-02-issues/lesson-27-advanced-issues.md
```

Add the completed lesson content.

Add your exercise and project documentation as appropriate.

### Step 3 — Review and commit

```text
git status
git diff --check
git diff
```

Stage the files:

```text
git add docs/github/module-02-issues/
```

Commit:

```text
git commit -m "docs(github): add Lesson 27 advanced issues"
```

### Step 4 — Push your branch

```text
git push -u origin docs/lesson-27-advanced-issues
```

### Step 5 — Open a Pull Request

**Title:**

`docs(github): add Lesson 27 — Advanced Issues`

**Description:**

```text
## Summary

Adds Lesson 27 to the GitHub Deep Dive curriculum.

## Topics covered

- GitHub Discussions and categories
- Discussion-to-Issue workflows
- Advanced Issue triage
- Saved replies and collaboration
- Cross-repository references
- Issue lifecycle management
- Stale Issue management
- Notifications and subscriptions
- Multi-repository coordination

## Practical work

- [ ] Discussion exercises completed
- [ ] Issue triage exercises completed
- [ ] Saved replies created
- [ ] Issue lifecycle exercise completed
- [ ] Restaurant platform project completed
- [ ] Documentation reviewed

## Documentation

- [ ] Markdown formatting checked
- [ ] Links reviewed
- [ ] Screenshots added where useful
- [ ] No secrets included
```

### Step 6 — Review and merge

Before merging:

1. Review the changed files.
2. Check the rendered Markdown.
3. Verify links and images.
4. Review the Pull Request description.
5. Resolve any review comments.
6. Merge the Pull Request.

### Step 7 — Create your training tag

After merging:

```text
git switch main
git pull origin main
```

Check whether the tag already exists:

```text
git tag --list "module-02-lesson-27"
```

If it does not exist, create it:

```text
git tag -a module-02-lesson-27 \
  -m "Complete Module 2 Lesson 27: Advanced Issues"
```

Push it:

```text
git push origin module-02-lesson-27
```

Do not recreate or overwrite an existing tag.

### Step 8 — Create a GitHub Release

#### Release configuration

- Tag: `module-02-lesson-27`
- Release title: `Module 2 — Lesson 27: Advanced Issues`
- Target: `main`

**Release notes:**

```text
# Module 2 — Lesson 27

Completed advanced GitHub Issues training.

## Topics

- Discussions and categories
- Discussion-to-Issue workflows
- Advanced Issue triage
- Saved replies
- Collaborative responses
- Cross-repository references
- Issue lifecycle management
- Stale Issue review
- Notifications and subscriptions
- Multi-repository Issue management

## Practical project

Completed the restaurant platform Issue-management
and triage exercise.

## Repository documentation

Added Lesson 27 and its supporting exercise documentation.
```

Publish the Release after verifying the tag and release notes.

---

## 19. Lessons Learned

After completing the lesson, answer these questions in your notes.

1. When should you use a Discussion instead of an Issue?
2. Why should a team avoid turning every question into an Issue?
3. What information should a maintainer check during triage?
4. Why are labels useful for Issue management?
5. When should a Discussion become an Issue?
6. Why should a team use saved replies?
7. How do cross-repository references help developers?
8. What is the difference between an Issue's native state and a workflow label?
9. When should an inactive Issue be closed?
10. How can one feature be coordinated across multiple repositories?

### Final reflection

Write a short explanation of how you would organize incoming reports for a real software project.

Your answer should explain:

- Where questions belong.
- Where implementation work belongs.
- How maintainers review new reports.
- How developers receive ownership.
- How the team tracks completion.

---

## 20. Lesson 27 Completion Checklist

### Learning and configuration

- Understand the difference between Discussions and Issues.
- Enable Discussions if available.
- Review and organize Discussion categories.
- Create a Discussion.
- Connect a Discussion to an Issue.

### Issue management

- Practice advanced Issue triage.
- Apply labels and priorities.
- Create saved replies.
- Practice collaborative responses.
- Reference Issues across repositories.
- Complete an Issue lifecycle through a Pull Request.
- Review stale and inactive Issues.
- Manage notifications and subscriptions.

### Practical project

- Create the restaurant platform sample Issues.
- Create the printer-configuration Discussion.
- Apply labels and priorities.
- Assign at least two Issues.
- Add an Issue to a milestone.
- Link an Issue to a Discussion.
- Document a cross-repository dependency.
- Complete one Issue through a Pull Request.

### Repository delivery

- Create `lesson-27-advanced-issues.md`.
- Add supporting exercise documentation.
- Validate Markdown and links.
- Commit and push the lesson branch.
- Open and merge the documentation Pull Request.
- Create tag `module-02-lesson-27`.
- Publish the GitHub Release.

---

## 21. Official Documentation

Use the official documentation as your primary reference.

1. [GitHub Discussions](https://docs.github.com/en/discussions)
2. [GitHub Issues](https://docs.github.com/en/issues)
3. [Tracking your work with Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues)
4. [Managing labels](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work)
5. [Linking a Pull Request to an Issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
6. [Saved replies](https://docs.github.com/en/get-started/writing-on-github/working-with-saved-replies)
7. [Managing subscriptions and notifications](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github)
8. [GitHub Actions](https://docs.github.com/en/actions)

---

## 22. Next Lesson — Lesson 28

### Module 3 — Pull Requests

#### Lesson 28: Pull Requests Fundamentals — From Branch to Merge

In the next lesson, you will learn:

1. What Pull Requests are and why teams use them.
2. The Pull Request lifecycle.
3. Creating a PR from a feature branch.
4. Base branch vs compare branch.
5. PR title and description conventions.
6. Draft Pull Requests.
7. Reviewing file changes and diffs.
8. Adding reviewers and assignees.
9. PR labels and milestones.
10. Linking Issues to Pull Requests.
11. Merge options:
    - Merge commit
    - Squash and merge
    - Rebase and merge
12. Practical two-person collaboration exercise.

**Module 2 checkpoint:** Lessons 26 and 27 covered Issue creation, organization, templates, Discussions, triage, collaboration, and lifecycle management.

After merging and releasing Lesson 27, you are ready to move into Pull Requests.

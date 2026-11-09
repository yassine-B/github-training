# Guide: Linking Pull Requests to Issues and GitHub Projects

This document outlines the standard workflow for connecting Pull Requests (PRs) to GitHub Issues and Project boards to maintain traceability and automate board progression.

---

## 1. Auto-Closing Issues via PR Description

You can automatically close an associated issue when your Pull Request is merged into the default branch.

### Supported Keywords
Include any of the following keywords followed by the issue reference in your PR description:
* `close`, `closes`, `closed`
* `fix`, `fixes`, `fixed`
* `resolve`, `resolves`, `resolved`

### Example Usage
> Fixes #12

---

## 2. Linking PRs to GitHub Project Boards

1. Open your Pull Request on GitHub.
2. In the right-hand sidebar, locate the **Projects** section.
3. Click the gear icon or select **Add to project**.
4. Choose your target Project board and assign its initial status (e.g., *In Progress*).

---

## 3. Automating Board Status Updates

To minimize manual updates:
1. Go to your **GitHub Project Board**.
2. Open **Settings** -> **Workflows**.
3. Enable triggers such as **Pull request merged** to automatically shift items into the **Done** column.
# Module 1 — Lesson 21: GitHub Code Search

## Learning Objectives

- Understand GitHub's different search categories.
- Master GitHub Code Search syntax.
- Use repository, language, path, symbol, and content qualifiers.
- Search repositories, commits, and source code.
- Use Boolean operators and regular expressions.
- Investigate unfamiliar repositories efficiently.
- Understand GitHub search versus local IDE search.

## 1. Search Categories

| Category | Purpose |
|---|---|
| Code | Search source code and files |
| Repositories | Find repositories |
| Commits | Search commit history |
| Issues | Find issues |
| Pull requests | Find PRs |
| Discussions | Find conversations |
| Users | Find GitHub accounts |
| Topics | Find categorized repositories |
| Wikis | Search wiki content |
| Packages | Find packages |
| Marketplace | Find Apps and Actions |
| Gists | Find code snippets |

Search syntax varies between categories.

## 2. Basic Code Search

Search a term:

```text
authentication
```

Multiple terms:

```text
authentication permissions
```

Exact phrase:

```text
"access token"
```

Boolean operators:

```text
authentication AND permissions
authentication OR authorization
authentication NOT deprecated
```

Combined:

```text
(authentication OR authorization) AND NOT deprecated
```

Regular expression:

```text
/^class\s+\w+/
```

## 3. Code Search Qualifiers

### Repository

```text
repo:OWNER/REPOSITORY authentication
```

Training repository:

```text
repo:yassine-B/github-deep-dive-training rebase
```

### Language

```text
language:python authentication
language:typescript useState
language:javascript fetch
language:yaml workflow
language:markdown repository
```

### Path

```text
path:docs/
path:src/
path:/
path:/src/**/*.tsx
```

### Filename patterns

```text
path:/README.md
path:/.*\.md$/
path:/\.github/workflows/.*\.yml$/
```

### Symbol

```text
language:python symbol:User
language:python symbol:authenticate
language:typescript symbol:useState
```

Symbol search finds supported definitions, not necessarily all references.

### Content

```text
content:authentication
```

### Is

```text
is:generated
is:vendored
is:fork
```

Exclude forks:

```text
authentication NOT is:fork
```

## 4. Repository Search

Examples:

```text
topic:django language:python
language:typescript stars:>100
topic:restaurant-management
org:github
django in:readme stars:>100
```

Useful qualifiers:

| Qualifier | Purpose |
|---|---|
| stars:>100 | Minimum star count |
| forks:>10 | Minimum fork count |
| language:python | Language |
| topic:django | Topic |
| archived:false | Exclude archived repositories |
| is:public | Public repositories |
| is:private | Accessible private repositories |
| pushed:>2026-01-01 | Recent activity |
| in:name | Search repository names |
| in:description | Search descriptions |
| in:readme | Search README |
| in:topics | Search topics |

## 5. Commit Search

```text
repo:OWNER/REPOSITORY authentication
repo:OWNER/REPOSITORY author:USERNAME
repo:OWNER/REPOSITORY committer-date:2026-01-01..2026-11-18
repo:OWNER/REPOSITORY path:README.md
```

Useful qualifiers:

- author:
- committer:
- author-date:
- committer-date:
- merge:

## 6. Practical Search Scenarios

Find authentication:

```text
language:python symbol:authenticate
```

Find React hooks:

```text
language:typescript useEffect
```

Find API routes:

```text
language:python path:api/ urlpatterns
```

Find Dockerfiles:

```text
path:/Dockerfile
```

Find GitHub Actions workflows:

```text
path:/.github/workflows/
```

Find deprecated code:

```text
language:python deprecated
```

## 7. Private Repository Search

When searching private repositories:

1. Sign in to the correct GitHub account.
2. Confirm repository access.
3. Use the complete repository identifier.
4. Verify the search category.
5. Check repository indexing and search limitations.

Example:

```text
repo:yassine-B/github-deep-dive-training rebase
```

## 8. Practical Exercises

- [ ] Search for the training repository.
- [ ] Find Python files.
- [ ] Find Markdown files.
- [ ] Search the Module 1 documentation directory.
- [ ] Search for an exact phrase from Lesson 20.
- [ ] Find a symbol definition.
- [ ] Search file contents only.
- [ ] Search commit messages.
- [ ] Search commits by author.
- [ ] Combine repository, language, and path qualifiers.

## 9. Advanced Investigation Challenge

Choose a public Django or React repository.

Investigate:

1. Main programming languages.
2. Configuration files.
3. API implementation.
4. Authentication implementation.
5. Tests.
6. Docker configuration.
7. GitHub Actions workflows.
8. Important classes and functions.
9. Authentication-related commits.
10. Overall architecture.

Deliverable:

`advanced-code-search-investigation.md`

## 10. Important Distinctions

| Feature | GitHub Code Search | VS Code |
|---|---|---|
| Search remote repositories | Yes | No, unless using extensions |
| Search local files | No | Yes |
| Search indexed definitions | Yes | Yes |
| Search uncommitted changes | No | Yes |
| Search across repositories | Yes | With workspace/tool support |
| Search local Git history | No | With Git tools |

## 11. Official Documentation

- https://docs.github.com/en/search-github/github-code-search/using-github-code-search
- https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax
- https://docs.github.com/en/search-github/searching-on-github
- https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories

## Completion Checklist

- [ ] Understand search categories.
- [ ] Understand basic syntax.
- [ ] Use repository qualifiers.
- [ ] Use language qualifiers.
- [ ] Use path qualifiers.
- [ ] Use symbol search.
- [ ] Use Boolean operators.
- [ ] Use regular expressions.
- [ ] Search commits and repositories.
- [ ] Complete all practical exercises.
- [ ] Complete the advanced investigation.

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
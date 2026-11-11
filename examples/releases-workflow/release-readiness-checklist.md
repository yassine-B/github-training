# Release Readiness Checklist

Use this checklist to ensure all code, documentation, and assets are fully prepared before pushing a new release tag.

## 1. Code & Quality Assurance
* [ ] All tests pass successfully in the CI/CD pipeline.
* [ ] Code linting and formatting checks pass without errors.
* [ ] Dependency vulnerabilities have been reviewed and resolved.
* [ ] Core features tested in a staging or preview environment.

## 2. Documentation & CLI Examples
* [ ] README and user guides are up-to-date.
* [ ] CLI command examples (e.g., `gh release create`, build commands) have been verified and corrected.
* [ ] API changes or breaking changes are clearly documented in the changelog.

## 3. Versioning & Tagging
* [ ] Version number follows semantic versioning (e.g., `v1.0.0`).
* [ ] Git branch is clean and merged into the release branch.
* [ ] Release notes draft prepared highlighting key updates and bug fixes.

## 4. Release Execution (GitHub CLI)
* [ ] **Create Tag and Release:**
  ```bash
  gh release create v1.0.0 --title "v1.0.0" --notes "Release notes description here"
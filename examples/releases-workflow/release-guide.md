## Releasing with GitHub CLI

When creating or managing releases in your repository, use the updated GitHub CLI syntax to ensure assets and release notes attach correctly.

### 1. Create a Release
Create a new release, generate a tag if it doesn't exist, and include release notes:

```bash
gh release create v1.0.0 --title "v1.0.0" --notes "Initial stable release"
```

## Updated this file to test the automatic release notes file
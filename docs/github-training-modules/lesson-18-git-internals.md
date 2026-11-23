# Lesson 18 — Git Internals: Objects, Trees, Blobs, Commits and Packfiles

## 1. Learning objectives

By the end of this lesson, you should be able to:

- Explain Git's content-addressable object storage.
- Identify the four main Git object types.
- Inspect blobs, trees and commits.
- Understand how a commit represents a repository snapshot.
- Explain how branches and tags reference commits.
- Understand Git's object database and `.git` directory.
- Inspect loose objects and packed objects.
- Use Git plumbing commands for low-level inspection.
- Explain what Git does when you commit, branch, merge and clone.

---

## Part 1 — Understand Git's internal architecture

## 2. The Git object model

Git stores repository data as objects.

There are four primary object types:

| Object | Purpose                                                                   |
| ------ | ------------------------------------------------------------------------- |
| Blob   | Stores file content                                                       |
| Tree   | Stores directory structure and references to files or subdirectories      |
| Commit | Stores a snapshot reference, parent commit(s), author and commit metadata |
| Tag    | Stores annotated tag metadata and references another object               |

A simplified representation:

```text
                 COMMIT
                    |
                    v
                  TREE
               /    |    \
              /     |     \
           BLOB    TREE    BLOB
          file A  folder  file B
                    |
                    v
                   BLOB
                  file C
```

A commit points to a tree representing the root directory of that snapshot.

A tree can reference:

- Blobs representing files.
- Other trees representing directories.

A commit can also reference one or more parent commits.

## 2.1 Blob objects

A blob stores file content.

For example, imagine this file:

`README.md`

```markdown
## Git Internals Training

This repository is used to understand Git internals.
```

Git stores the content as a blob.

Important:

A blob does not store the filename or directory path. It stores the file's content.

The filename and its relationship to directories are stored in tree objects.

This means two files with identical content can reference the same blob object.

## 2.2 Tree objects

A tree represents a directory.

For example:

```text
repository/
├── README.md
├── LICENSE
└── docs/
    ├── introduction.md
    └── git-internals.md
```

The root tree contains references to:

- `README.md` blob.
- `LICENSE` blob.
- `docs/` tree.

The `docs/` tree contains references to its own file blobs.

Trees preserve filenames, file modes, and references to the corresponding objects.

## 2.3 Commit objects

A commit records a snapshot and its history metadata.

A simplified commit object looks like this:

```text
tree 8a4f...
parent 7b2c...
author Developer <developer@example.com> 1790000000 +0000
committer Developer <developer@example.com> 1790000000 +0000

docs: add git internals lesson
```

The fields mean:

| Field     | Meaning                                  |
| --------- | ---------------------------------------- |
| tree      | Root tree of this snapshot               |
| parent    | Previous commit                          |
| author    | Person who originally created the change |
| committer | Person who created this commit object    |
| Message   | Commit message                           |

A root commit has no parent.

A normal commit usually has one parent.

A merge commit normally has two or more parents.

## 2.4 Tag objects

Git supports two important types of tags:

### Lightweight tag

A lightweight tag is a reference directly pointing to an object, commonly a commit.

### Annotated tag

An annotated tag is a separate Git object containing:

- Tag name.
- Tagger.
- Date.
- Message.
- Target object reference.

For releases, annotated tags are generally preferable because they contain metadata.

Example:

```bash
git tag -a v1.0.0 -m "First stable release"
```

---

## Part 2 — Understand the `.git` directory

## 3. Inspect the repository structure

From your cloned repository, execute:

```bash
cd github-deep-dive-training
```

Inspect the Git directory:

```bash
ls -la .git
```

On Windows PowerShell:

```powershell
Get-ChildItem -Force .git
```

You should see directories and files similar to:

```text
.git/
├── HEAD
├── config
├── description
├── hooks/
├── index
├── info/
├── objects/
├── refs/
└── logs/
```

The exact structure can vary depending on the repository and Git version.

### Important locations

| Path            | Purpose                                          |
| --------------- | ------------------------------------------------ |
| `.git/HEAD`     | Identifies the current branch or detached commit |
| `.git/config`   | Repository-specific configuration                |
| `.git/index`    | Staging area information                         |
| `.git/objects/` | Git object database                              |
| `.git/refs/`    | References such as branches and tags             |
| `.git/logs/`    | Reference update history, including reflogs      |
| `.git/hooks/`   | Local Git hook scripts                           |

Do not manually modify internal files during this lesson. Use Git commands to inspect and manipulate repository data.

## 3.1 Inspect HEAD

Run:

```bash
cat .git/HEAD
```

On Windows PowerShell:

```powershell
Get-Content .git/HEAD
```

A typical result:

```text
ref: refs/heads/main
```

This means HEAD points to the `main` branch reference.

Inspect the current commit:

```bash
git rev-parse HEAD
```

Inspect the current branch:

```bash
git branch --show-current
```

Inspect all references:

```bash
git show-ref
```

You will see references to local branches and tags.

---

## Part 3 — Understand content-addressable storage

## 4. How Git identifies objects

Git identifies objects using a cryptographic hash of their type, size and content.

Conceptually, Git hashes a structure similar to:

```text
blob <content-size>\0<content>
```

The hash identifies the resulting object.

Git repositories commonly use SHA-1 object IDs, although SHA-256 repositories are also supported.

Do not assume every repository uses a 40-character SHA-1 object ID. Check the repository's object format:

```bash
git rev-parse --show-object-format
```

Typical results:

```text
sha1
```

or:

```text
sha256
```

### Why content-addressable storage matters

Git can:

1. Identify objects by their content.
2. Reuse identical content.
3. Detect unexpected object corruption.
4. Reference objects consistently throughout repository history.

If file content changes, its blob object ID will normally change.

A filename change without a content change does not require a new blob. The tree structure changes to record the new filename.

---

## Part 4 — Create a Git internals laboratory

## 5. Create a separate laboratory repository

Do not perform destructive experiments in your main training repository.

Create a disposable repository:

```bash
mkdir git-internals-lab
cd git-internals-lab

git init
```

Configure a local identity for this laboratory:

```bash
git config user.name "Git Training Developer"
git config user.email "git-training@example.com"
```

Create a directory:

```bash
mkdir docs
```

Create files:

`README.md`

```markdown
## Git Internals Lab

This repository is used to explore Git's internal object database.
```

`docs/first-file.md`

```markdown
## First File

This is the first file in the Git internals laboratory.
```

Stage and commit:

```bash
git add .
git commit -m "chore: initialize git internals lab"
```

Inspect the result:

```bash
git status
git log --oneline --decorate
```

You now have a repository with at least one commit, a root tree and multiple blobs.

---

## Part 5 — Inspect Git objects

## 6. Discover object IDs

Run:

```bash
git cat-file -p HEAD
```

You should see information similar to:

```text
tree <tree-object-id>
author Git Training Developer <git-training@example.com> ...
committer Git Training Developer <git-training@example.com> ...

chore: initialize git internals lab
```

The tree ID identifies the root tree of the commit.

Inspect the object type:

```bash
git cat-file -t HEAD
```

Expected:

```text
commit
```

Inspect its size:

```bash
git cat-file -s HEAD
```

This reports the uncompressed object content size.

## 6.1 Inspect the root tree

Run:

```bash
git ls-tree HEAD
```

You should see entries similar to:

```text
100644 blob <object-id>    README.md
040000 tree <object-id>    docs
```

The exact IDs will differ.

Inspect the nested directory:

```bash
git ls-tree HEAD:docs
```

This displays the entries inside `docs`.

### Understand file modes

Common Git tree modes include:

| Mode     | Meaning                     |
| -------- | --------------------------- |
| `100644` | Regular non-executable file |
| `100755` | Executable file             |
| `120000` | Symbolic link               |
| `040000` | Directory tree              |
| `160000` | Git submodule reference     |

## 6.2 Inspect a blob

Copy the blob ID for `README.md` from the previous command.

Then run:

```bash
git cat-file -t <BLOB_ID>
```

Expected:

```text
blob
```

Read the blob:

```bash
git cat-file -p <BLOB_ID>
```

Inspect its size:

```bash
git cat-file -s <BLOB_ID>
```

Notice that the blob contains the file content, but not its filename.

## 6.3 Inspect a commit's full contents

Run:

```bash
git cat-file -p HEAD
```

You can inspect a previous commit with:

```bash
git cat-file -p HEAD^
```

For a commit with multiple parents, inspect its parent IDs with:

```bash
git rev-list --parents -n 1 HEAD
```

---

## Part 6 — Create and inspect blobs manually

## 7. Use `git hash-object`

Create a file:

`manual-blob.txt`

```text
This file will be used to inspect Git blob storage.
```

Calculate its Git object ID without storing it:

```bash
git hash-object manual-blob.txt
```

This calculates the blob hash but does not write the object into the object database.

Now store it:

```bash
git hash-object -w manual-blob.txt
```

The `-w` option writes the object into Git's object database.

Inspect the object:

```bash
git cat-file -t <BLOB_ID>
git cat-file -p <BLOB_ID>
git cat-file -s <BLOB_ID>
```

### Experiment: identical file content

Create another file:

`manual-blob-copy.txt`

```text
This file will be used to inspect Git blob storage.
```

Run:

```bash
git hash-object manual-blob-copy.txt
```

Compare the result with the first blob ID.

The IDs should match because the file contents are identical.

This demonstrates Git's content-addressable storage.

### Experiment: change the content

Modify the second file:

```text
This file has different content.
```

Run:

```bash
git hash-object manual-blob-copy.txt
```

The object ID should now be different.

---

## Part 7 — Understand the index and staging area

## 8. The Git index

The index is Git's staging area.

When you execute:

```bash
git add README.md
```

Git prepares the file content as an object and updates the index to record what should enter the next commit.

Inspect the index:

```bash
git ls-files --stage
```

Example:

```text
100644 <blob-id> 0 README.md
```

The index contains information such as:

- File path.
- File mode.
- Blob object ID.
- Stage number.

For ordinary staged files, the stage number is usually `0`.

During unresolved merge conflicts, Git can use stages `1`, `2` and `3` to represent the common ancestor, current side and incoming side.

Inspect staged changes:

```bash
git diff --cached
```

Inspect unstaged changes:

```bash
git diff
```

Inspect both working tree and index status:

```bash
git status
```

### Exercise

1. Modify `README.md`.
2. Run `git diff`.
3. Stage the file.
4. Run `git diff --cached`.
5. Inspect `git ls-files --stage`.
6. Commit the change.
7. Inspect the new commit using `git cat-file -p HEAD`.

Record what changed in the index and what changed in the commit.

---

## Part 8 — Understand commits and snapshots

## 9. A commit is a snapshot, not a patch

A common misunderstanding is that Git commits simply store differences between files.

Git's commit model is based on snapshots.

A commit points to a tree representing the complete tracked repository state at that point in history.

Git uses object reuse and storage optimizations to avoid storing every file's full content repeatedly.

For example:

```text
Commit A
   |
   v
Tree A
   |
   +---- README blob A
   |
   +---- config blob A

Commit B
   |
   v
Tree B
   |
   +---- README blob A  (reused)
   |
   +---- config blob B  (changed)
```

The unchanged README can reuse the same blob object.

The changed configuration file receives a different blob object.

## 9.1 Inspect commit history

Run:

```bash
git log --oneline --decorate
```

Inspect commit metadata:

```bash
git show --no-patch --format=fuller HEAD
```

Inspect the tree referenced by a commit:

```bash
git rev-parse HEAD^{tree}
```

Inspect the tree referenced by the previous commit:

```bash
git rev-parse HEAD^^{tree}
```

Inspect the difference between two snapshots:

```bash
git diff HEAD^ HEAD
```

The diff is calculated from the snapshots. It is not the primary representation of the commit object.

---

## Part 9 — Understand branches and references

## 10. Branches are references

A branch is not a complete copy of the repository.

A branch is a movable reference pointing to a commit.

Example:

```text
                 main
                  |
                  v
                 C3
                /
C1 -------- C2
       \
        \
         feature
```

Both branch names point to commits.

Inspect branches:

```bash
git branch -avv
```

Inspect references:

```bash
git show-ref
```

Inspect the current branch's commit:

```bash
git rev-parse main
```

Inspect the current HEAD:

```bash
git rev-parse HEAD
```

Create a branch:

```bash
git switch -c feature/object-inspection
```

Inspect its reference:

```bash
git show-ref --heads
```

Create a commit on that branch:

```bash
echo "Branch experiment" > branch-experiment.txt
git add branch-experiment.txt
git commit -m "test: add branch experiment"
```

Inspect the branch reference again:

```bash
git show-ref --heads
```

Notice that the feature branch now points to the new commit.

Switch back:

```bash
git switch main
```

The branch reference remains available.

## 10.1 Inspect a reference without changing it

```bash
git rev-parse refs/heads/main
```

Inspect the current symbolic HEAD:

```bash
git symbolic-ref HEAD
```

These commands help you distinguish between:

- A branch reference.
- A commit object.
- The symbolic HEAD reference.

---

## Part 10 — Understand merge commits

## 11. Inspect a merge commit

Create two branches with independent commits.

First, create a base commit on `main`:

```bash
git switch main

echo "Base content" > merge-base.txt
git add merge-base.txt
git commit -m "test: add merge base"
```

Create a feature branch:

```bash
git switch -c feature/merge-internals
```

Add a feature file:

```bash
echo "Feature content" > feature-file.txt
git add feature-file.txt
git commit -m "feat: add feature file"
```

Switch back to main:

```bash
git switch main
```

Add another file:

```bash
echo "Main content" > main-file.txt
git add main-file.txt
git commit -m "test: add main file"
```

Merge the feature branch:

```bash
git merge --no-ff feature/merge-internals -m "merge: combine feature branch"
```

Inspect the latest commit:

```bash
git cat-file -p HEAD
```

You should see two `parent` lines.

Inspect its parent IDs:

```bash
git rev-list --parents -n 1 HEAD
```

Inspect the graph:

```bash
git log --oneline --graph --decorate --all
```

### What did you learn?

A merge commit records multiple parent references.

The merge commit still points to a tree representing the resulting repository snapshot.

---

## Part 11 — Loose objects and packfiles

## 12. What are loose objects?

When Git creates objects, they may initially be stored as individual compressed files inside:

```text
.git/objects/
```

These are called loose objects.

Their storage path is based on their object ID.

For example, an object ID:

```text
a1b2c3d4...
```

may be stored at:

```text
.git/objects/a1/b2c3d4...
```

The first two characters form the directory name.

The remaining characters form the filename.

Do not manually edit these files.

## 12.1 Inspect object storage

Run:

```bash
git count-objects -v
```

Example output:

```text
count: 12
size: 48
in-pack: 0
packs: 0
size-pack: 0
```

The values depend on your repository.

Important fields:

| Field     | Meaning                                 |
| --------- | --------------------------------------- |
| count     | Number of loose objects                 |
| size      | Approximate loose-object storage in KiB |
| in-pack   | Number of packed objects                |
| packs     | Number of packfiles                     |
| size-pack | Approximate packed storage in KiB       |

## 12.2 What are packfiles?

As repositories grow, storing every object separately becomes inefficient.

Git can combine objects into packfiles.

A packfile can contain:

- Blobs.
- Trees.
- Commits.
- Tags.

Git can also use delta compression to represent related object contents efficiently.

A packfile is commonly accompanied by an index file.

Typical paths:

```text
.git/objects/pack/
├── pack-<hash>.pack
└── pack-<hash>.idx
```

The `.pack` file stores packed objects.

The `.idx` file provides an index to locate objects inside the packfile.

## 12.3 Inspect packfiles

First, inspect current object statistics:

```bash
git count-objects -v
```

Run Git garbage collection in the disposable laboratory:

```bash
git gc
```

Inspect statistics again:

```bash
git count-objects -v
```

Inspect the pack directory:

```bash
ls .git/objects/pack
```

On PowerShell:

```powershell
Get-ChildItem .git/objects/pack
```

Depending on the repository's size and configuration, Git may not create a packfile during this experiment. A small repository may not have enough objects to demonstrate meaningful packing.

You can also use:

```bash
git verify-pack -v .git/objects/pack/*.idx
```

If no `.idx` file exists, this command has nothing to inspect. Do not treat that as a repository error.

The output can include object IDs, types, sizes and delta information.

## 12.4 Why packfiles matter

Packfiles help Git:

- Reduce repository storage.
- Transfer repository data efficiently.
- Optimize object storage.
- Avoid storing repeated content unnecessarily.

Git commonly uses packed objects when communicating with remote repositories.

---

## Part 12 — Git plumbing versus porcelain

## 13. Understand the distinction

Git commands are often grouped into two categories.

### Porcelain commands

These are user-facing commands designed for everyday workflows.

Examples:

```bash
git status
git add
git commit
git switch
git merge
git log
git push
git pull
```

### Plumbing commands

These expose lower-level Git functionality.

Examples:

```bash
git cat-file
git hash-object
git ls-tree
git ls-files
git update-index
git update-ref
git rev-parse
git write-tree
git commit-tree
```

You do not need to use plumbing commands every day.

However, they are useful for:

- Debugging.
- Automation.
- Git tooling.
- Repository analysis.
- Understanding Git's internal behavior.

## 13.1 Important plumbing commands

| Command           | Purpose                                  |
| ----------------- | ---------------------------------------- |
| `git hash-object` | Calculate or write an object             |
| `git cat-file`    | Inspect object type, size and content    |
| `git ls-tree`     | Inspect tree entries                     |
| `git ls-files`    | Inspect index entries                    |
| `git rev-parse`   | Resolve Git references and object IDs    |
| `git show-ref`    | List references                          |
| `git write-tree`  | Write the current index as a tree object |
| `git commit-tree` | Create a commit object from a tree       |
| `git update-ref`  | Update a reference                       |
| `git verify-pack` | Inspect and verify packfile indexes      |

Use these commands carefully. Some plumbing commands can directly modify Git's internal references or object database.

---

## Part 13 — Advanced laboratory: create a tree and commit

## 14. Create a tree from the index

This experiment uses Git plumbing to create a tree object.

First, ensure the working tree is clean:

```bash
git status
```

Create a new file:

`plumbing-example.txt`

```text
Created to understand Git plumbing commands.
```

Stage it:

```bash
git add plumbing-example.txt
```

Write the index as a tree:

```bash
git write-tree
```

Git prints a tree object ID.

Inspect it:

```bash
git cat-file -t <TREE_ID>
git cat-file -p <TREE_ID>
```

You should see:

```text
tree
```

The tree contains the entries represented by the current index.

## 14.1 Create a commit object using `commit-tree`

This is an advanced experiment. It creates a commit object without using the normal `git commit` workflow.

Capture the current tree ID:

```bash
git write-tree
```

Create a commit:

```bash
git commit-tree <TREE_ID> -p HEAD -m "test: create commit using plumbing"
```

Git prints a new commit object ID.

Inspect it:

```bash
git cat-file -p <COMMIT_ID>
```

Notice:

- The commit references the supplied tree.
- The `-p HEAD` argument specifies the parent commit.
- The message is stored inside the commit object.

**Important:** `git commit-tree` creates the commit object but does not automatically move your current branch to it.

For this exercise, do not update `main` or another important reference manually. Inspect the object and leave it unreachable after the experiment.

An object that is not reachable from a reference may eventually be eligible for garbage collection.

---

## Part 14 — Understand object reachability

## 15. What does reachable mean?

An object is reachable when Git can find it by following references and object relationships.

For example:

```text
refs/heads/main
       |
       v
     Commit
       |
       v
      Tree
       |
       v
      Blob
```

The branch points to a commit.

The commit points to a tree.

The tree points to blobs and other trees.

All these objects are reachable through the branch reference.

Other references include:

- Other branches.
- Tags.
- Remote-tracking branches.
- References maintained by Git operations.

Reflogs can also temporarily keep otherwise-unreferenced commits available.

## 15.1 Why reachability matters

Consider this situation:

1. You create a commit.
2. You reset a branch to an older commit.
3. The new commit is no longer referenced by that branch.
4. You may still recover it through the reflog.
5. Eventually, Git may remove unreachable objects during garbage collection.

This connects directly to Lesson 17 — Git Reflog and Repository Recovery.

## 15.2 Inspect unreachable objects

In your disposable laboratory, you can inspect objects that are not reachable from the normal references:

```bash
git fsck --unreachable
```

For a broader object-database check:

```bash
git fsck --full
```

`git fsck` can report unreachable or dangling objects. Such reports are not automatically evidence of corruption.

Do not attempt to manually delete objects to clean up the repository.

---

## Part 15 — How Git uses these internals in everyday operations

## 16. What happens when you run `git add`?

A simplified process:

1. Git reads the working-tree file.
2. Git calculates the blob object ID.
3. Git stores the blob object if necessary.
4. Git updates the index with the file path and blob reference.

## 16.1 What happens when you run `git commit`?

A simplified process:

1. Git reads the index.
2. Git writes a tree representing the staged snapshot.
3. Git creates a commit object.
4. The commit references the tree and its parent commit.
5. Git updates the current branch reference to the new commit.

## 16.2 What happens when you create a branch?

Git creates a reference pointing to an existing commit.

It does not duplicate the entire repository.

## 16.3 What happens when you merge?

Git determines the relevant history and computes the resulting repository state.

Depending on the situation, it may:

- Fast-forward a branch reference.
- Create a merge commit.
- Stop for conflict resolution.

A merge commit references the resulting tree and its parent commits.

## 16.4 What happens when you clone?

At a high level, Git:

1. Establishes the remote repository connection.
2. Negotiates which objects are needed.
3. Receives repository objects, commonly through packfile transfer.
4. Stores the objects locally.
5. Sets up remote-tracking references and local repository configuration.
6. Checks out the selected branch when applicable.

The exact transfer process depends on the protocol, server and clone options.

---

## Part 16 — Practical exercises

## 17. Exercise 1: Identify object types

Use your laboratory repository.

Run:

```bash
git cat-file -t HEAD
git cat-file -t HEAD^{tree}
```

Then inspect a blob ID from:

```bash
git ls-tree -r HEAD
```

Run:

```bash
git cat-file -t <BLOB_ID>
```

Expected object types:

| Object      | Expected type |
| ----------- | ------------- |
| HEAD        | commit        |
| HEAD tree   | tree          |
| File object | blob          |

**Deliverable:** Create a Markdown file explaining the three object types and include the command outputs.

## 17.1 Exercise 2: Compare identical content

1. Create two files with identical content.
2. Calculate both object IDs using `git hash-object`.
3. Compare the IDs.
4. Change one file.
5. Calculate its object ID again.

**Deliverable:** Explain why the IDs matched initially and changed after editing.

## 17.2 Exercise 3: Inspect a commit

Run:

```bash
git cat-file -p HEAD
git rev-parse HEAD^{tree}
git rev-list --parents -n 1 HEAD
```

**Deliverable:** Explain:

- Which tree the commit references.
- Whether it has a parent.
- How the parent relationship represents history.

## 17.3 Exercise 4: Inspect the index

1. Modify `README.md`.
2. Run `git diff`.
3. Stage the file.
4. Run `git diff --cached`.
5. Run `git ls-files --stage`.
6. Commit the modification.

**Deliverable:** Explain the difference between the working tree, index and committed snapshot.

## 17.4 Exercise 5: Inspect merge internals

1. Create a feature branch.
2. Create a commit on the feature branch.
3. Create another commit on `main`.
4. Merge the feature branch using `--no-ff`.
5. Inspect the merge commit.

Use:

```bash
git cat-file -p HEAD
git rev-list --parents -n 1 HEAD
git log --graph --oneline --all
```

**Deliverable:** Explain why the merge commit has multiple parents.

## 17.5 Exercise 6: Inspect packfiles

Run:

```bash
git count-objects -v
git gc
git count-objects -v
```

Inspect:

```bash
ls .git/objects/pack
```

**Deliverable:** Explain:

- What loose objects are.
- What packfiles are.
- Why Git uses packfiles.
- What delta compression means.

If the repository is too small to generate a packfile, document that result rather than forcing a cleanup or manipulating internal files.

---

## Part 17 — Repository training deliverables

## 18. Add the lesson to your main training repository

Return to your main repository:

```bash
cd ../github-deep-dive-training
```

Create the following file:

```text
docs/
└── github/
    └── module-01-code/
        └── lesson-18-git-internals.md
```

Copy this lesson into that file.

Create an additional exercise report:

```text
docs/
└── github/
    └── module-01-code/
        └── exercises/
            └── lesson-18-git-internals-lab.md
```

Suggested report structure:

````markdown
## Lesson 18 — Git Internals Lab Report

## 1. Environment

- Operating system:
- Git version:
- Object format:
- Repository:

## 2. Object inspection

### Commit object

Command:
```bash
git cat-file -p HEAD
````

Findings:

### Tree object

Command:

```bash
git ls-tree HEAD
```

Findings:

### Blob object

Command:

```bash
git cat-file -p <BLOB_ID>
```

Findings:

## 3. Content-addressable storage

- First file object ID:
- Identical file object ID:
- Modified file object ID:

Explanation:

## 4. Index inspection

Commands used:

Findings:

## 5. Merge commit inspection

- Merge commit ID:
- First parent:
- Second parent:
- Tree ID:

Explanation:

## 6. Packfile inspection

Commands used:

Findings:

## 7. Lessons learned

1.
2.
3.

## 8. Questions

1. What is the difference between a blob and a tree?
2. Why does a commit reference a tree?
3. Why can two files share the same blob?
4. Why are branches references rather than copies?
5. What is the purpose of a packfile?

---

## Part 18 — Git workflow for the lesson

## 19. Create your branch

In your main training repository:

```bash
git switch main
git pull origin main
git switch -c docs/add-git-internals-lesson
````

Create:

```text
docs/github/module-01-code/lesson-18-git-internals.md
docs/github/module-01-code/exercises/lesson-18-git-internals-lab.md
```

Complete the lab report with your own command outputs and explanations.

## 19.1 Commit your changes

Check your files:

```bash
git status
git diff
```

Stage:

```bash
git add docs/github/module-01-code/lesson-18-git-internals.md
git add docs/github/module-01-code/exercises/lesson-18-git-internals-lab.md
```

Review staged changes:

```bash
git diff --cached
```

Commit:

```bash
git commit -m "docs(github): add lesson 18 git internals"
```

Push:

```bash
git push -u origin docs/add-git-internals-lesson
```

## 19.2 Create a pull request

Suggested PR title:

```text
docs(github): add lesson 18 — Git internals
```

Suggested PR description:

```markdown
## Summary

Adds Lesson 18 to the GitHub Deep Dive training.

## Contents

- Git object model
- Blobs, trees, commits and tags
- Content-addressable storage
- Git index and staging area
- Git plumbing commands
- Loose objects and packfiles
- Object reachability
- Practical Git internals laboratory

## Exercises

- [ ] Identify Git object types
- [ ] Compare identical blob content
- [ ] Inspect commit and tree objects
- [ ] Inspect the Git index
- [ ] Inspect a merge commit
- [ ] Inspect object storage and packfiles

## Verification

- [ ] Markdown reviewed
- [ ] Commands tested in disposable repository
- [ ] No destructive experiments performed in the training repository
```

Merge the PR after reviewing it.

---

## Part 19 — Create an annotated tag and GitHub Release

## 20. Tag the lesson

After the PR is merged, update your local `main`:

```bash
git switch main
git pull origin main
```

Create an annotated tag:

```bash
git tag -a module-01-lesson-18 -m "Module 1 Lesson 18: Git Internals"
```

Push the tag:

```bash
git push origin module-01-lesson-18
```

Verify:

```bash
git show module-01-lesson-18
git tag --list
```

## 20.1 Create a GitHub Release

Open your repository on GitHub.

1. Navigate to **Releases**.
2. Select **Draft a new release**.
3. Choose the tag `module-01-lesson-18`.
4. Set the release title:

```text
Module 1 — Lesson 18: Git Internals
```

1. Add these release notes:

```markdown
## Lesson 18 — Git Internals

## Topics covered

- Git's four primary object types
- Blob, tree, commit and tag objects
- Content-addressable storage
- The Git index
- Commit snapshots and parent relationships
- Branch references
- Merge commits
- Loose objects and packfiles
- Git plumbing and porcelain commands
- Object reachability and garbage collection

## Practical work

- Created a separate Git internals laboratory
- Inspected object types and object contents
- Compared identical blob contents
- Inspected the index and commit snapshots
- Inspected a merge commit
- Examined Git object storage

## Completion criteria

- [ ] All six practical exercises completed
- [ ] Lab report committed
- [ ] Pull request reviewed and merged
- [ ] Annotated tag created
```

1. Publish the release.

---

## Part 20 — Final knowledge check

## 21. Questions

Answer these without looking at the lesson.

1. What are the four primary Git object types?
2. Does a blob contain the filename?
3. What does a tree object represent?
4. What does a commit object reference?
5. What is the difference between a commit and a tree?
6. Why can two files with identical content share one blob?
7. What is a branch internally?
8. What is the difference between a lightweight and annotated tag?
9. What is the Git index?
10. What is a loose object?
11. What is a packfile?
12. Why does Git use delta compression?
13. What is the difference between Git plumbing and porcelain?
14. What does `git cat-file -p` do?
15. What does `git hash-object -w` do?
16. What does `git write-tree` do?
17. What is the difference between a merge commit and a normal commit?
18. What does object reachability mean?
19. Why can an unreachable commit sometimes still be recovered?
20. What happens at a high level when you execute `git commit`?

## 21.1 Completion checklist

- [ ] I understand the Git object model.
- [ ] I can distinguish blobs, trees, commits and tags.
- [ ] I can inspect objects with `git cat-file`.
- [ ] I can inspect trees with `git ls-tree`.
- [ ] I understand how the index works.
- [ ] I understand why Git uses snapshots.
- [ ] I understand how branches reference commits.
- [ ] I can inspect merge commit parent relationships.
- [ ] I understand loose objects and packfiles.
- [ ] I understand the difference between plumbing and porcelain.
- [ ] I completed the six practical exercises.
- [ ] I created the lesson and lab report in the training repository.
- [ ] I opened and merged the PR.
- [ ] I created the annotated tag.
- [ ] I published the GitHub Release.

---

## Lesson 18 complete

You now have a foundation for understanding Git beyond its everyday command-line interface.

### Next lesson — Lesson 19: Advanced Git Configuration, Aliases, Attributes and Ignore Rules

The next lesson will cover repository-level and global Git configuration, configuration precedence, aliases, `.gitattributes`, line-ending normalization, binary files, diff and merge drivers, `.gitignore`, and practical configuration standards for professional development teams.

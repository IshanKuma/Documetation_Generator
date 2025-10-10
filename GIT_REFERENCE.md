# Git Commands Reference - Branches & Worktrees

> **Quick Reference for Documentation Generator Project**
> Last Updated: 2025-10-10

---

## 📑 Table of Contents
- [Branch Commands](#branch-commands)
- [Worktree Commands](#worktree-commands)
- [Commands We Use in This Project](#commands-we-use-in-this-project)
- [Workflow Examples](#workflow-examples)

---

## 🌿 Branch Commands

### Basic Branch Operations

#### 1. **Create Branch**
```bash
git branch <branch-name>
```
**What it does:** Creates a new branch but doesn't switch to it
**Example:** `git branch feature/pdf-export`
**Use case:** When you want to create but not immediately switch

#### 2. **Create & Switch Branch (Recommended)**
```bash
git checkout -b <branch-name>
```
**What it does:** Creates a new branch AND switches to it
**Example:** `git checkout -b feature/pdf-export`
**Use case:** Most common way to start working on a new feature
**✅ WE USE THIS**

#### 3. **Switch Branch**
```bash
git checkout <branch-name>
```
**What it does:** Switches to an existing branch
**Example:** `git checkout develop`
**Use case:** Move between branches
**✅ WE USE THIS**

#### 4. **Switch Branch (Modern)**
```bash
git switch <branch-name>
```
**What it does:** Same as checkout but newer, clearer command
**Example:** `git switch develop`
**Use case:** Alternative to `git checkout` (Git 2.23+)

#### 5. **Create & Switch (Modern)**
```bash
git switch -c <branch-name>
```
**What it does:** Creates and switches to new branch
**Example:** `git switch -c feature/pdf-export`
**Use case:** Modern alternative to `checkout -b`

### Listing Branches

#### 6. **List Local Branches**
```bash
git branch
```
**What it does:** Shows all local branches, asterisk (*) marks current
**Example output:**
```
  develop
* master
  feature/pdf-export
```
**✅ WE USE THIS**

#### 7. **List All Branches**
```bash
git branch -a
```
**What it does:** Shows local + remote branches
**Example output:**
```
* master
  develop
  remotes/origin/master
  remotes/origin/develop
```
**Use case:** See what's on remote servers too

#### 8. **List Branches with Details**
```bash
git branch -v
```
**What it does:** Shows branches with last commit info
**Example output:**
```
  develop ed77a06 docs(contributing): add guidelines
* master  ed77a06 docs(contributing): add guidelines
```
**✅ WE USE THIS**

#### 9. **List Branches with Tracking Info**
```bash
git branch -vv
```
**What it does:** Shows branches, commits, AND remote tracking
**Example output:**
```
* master  ed77a06 [origin/master] docs: add guidelines
  develop ed77a06 docs: add guidelines
```
**Use case:** See which branches track remote branches

### Managing Branches

#### 10. **Rename Current Branch**
```bash
git branch -m <new-name>
```
**What it does:** Renames the current branch
**Example:** `git branch -m feature/better-name`
**Use case:** Fix typos in branch names

#### 11. **Rename Any Branch**
```bash
git branch -m <old-name> <new-name>
```
**What it does:** Renames a branch (doesn't need to be current)
**Example:** `git branch -m feature/old feature/new`

#### 12. **Delete Branch**
```bash
git branch -d <branch-name>
```
**What it does:** Deletes branch (safe - only if merged)
**Example:** `git branch -d feature/pdf-export`
**Use case:** Clean up after merging feature
**✅ WE USE THIS**

#### 13. **Force Delete Branch**
```bash
git branch -D <branch-name>
```
**What it does:** Deletes branch even if not merged
**Example:** `git branch -D feature/abandoned`
**Use case:** Discard experimental branches
**⚠️ DANGEROUS - Use with caution**

#### 14. **Delete Remote Branch**
```bash
git push origin --delete <branch-name>
```
**What it does:** Deletes branch from remote repository
**Example:** `git push origin --delete feature/pdf-export`
**Use case:** Clean up remote branches after merging

### Branch Information

#### 15. **Show Current Branch**
```bash
git branch --show-current
```
**What it does:** Prints only the current branch name
**Example output:** `master`
**Use case:** Scripts, automation

#### 16. **List Merged Branches**
```bash
git branch --merged
```
**What it does:** Shows branches already merged into current
**Use case:** Find branches safe to delete

#### 17. **List Unmerged Branches**
```bash
git branch --no-merged
```
**What it does:** Shows branches NOT yet merged
**Use case:** See what work is still in progress

---

## 🌳 Worktree Commands

### What is a Worktree?
Multiple working directories for the same repository, allowing you to work on different branches simultaneously without switching.

### Basic Worktree Operations

#### 18. **Add Worktree**
```bash
git worktree add <path> <branch-name>
```
**What it does:** Creates new working directory for a branch
**Example:** `git worktree add ../doc_gen-pdf feature/pdf-export`
**Use case:** Work on PDF export while keeping main directory on master
**✅ WE USE THIS (for multi-agent work)**

#### 19. **Add Worktree with New Branch**
```bash
git worktree add <path> -b <new-branch>
```
**What it does:** Creates new branch + worktree in one command
**Example:** `git worktree add ../doc_gen-pdf -b feature/pdf-export`
**Use case:** Start new feature in separate directory

#### 20. **Add Worktree from Remote Branch**
```bash
git worktree add <path> <remote/branch>
```
**What it does:** Creates worktree tracking remote branch
**Example:** `git worktree add ../doc_gen-fix origin/fix/bug-123`

#### 21. **List Worktrees**
```bash
git worktree list
```
**What it does:** Shows all worktrees and their branches
**Example output:**
```
/home/user/Desktop/documentation_generator        ed77a06 [master]
/home/user/Desktop/doc_gen-pdf                    abc1234 [feature/pdf-export]
/home/user/Desktop/doc_gen-markdown               def5678 [feature/markdown]
```
**✅ WE USE THIS**

#### 22. **Remove Worktree**
```bash
git worktree remove <path>
```
**What it does:** Deletes worktree directory
**Example:** `git worktree remove ../doc_gen-pdf`
**Use case:** Clean up after feature is merged
**✅ WE USE THIS**

#### 23. **Force Remove Worktree**
```bash
git worktree remove --force <path>
```
**What it does:** Removes worktree even with uncommitted changes
**Example:** `git worktree remove --force ../doc_gen-pdf`
**⚠️ DANGEROUS - Lost work cannot be recovered**

#### 24. **Prune Worktrees**
```bash
git worktree prune
```
**What it does:** Removes stale worktree administrative files
**Use case:** Clean up after manually deleting worktree directories
**✅ WE USE THIS (maintenance)**

#### 25. **Repair Worktrees**
```bash
git worktree repair
```
**What it does:** Fixes worktree administrative data
**Use case:** After moving repository or worktree directories

#### 26. **Lock Worktree**
```bash
git worktree lock <path>
```
**What it does:** Prevents worktree from being pruned
**Use case:** Worktree on removable/network drive

#### 27. **Unlock Worktree**
```bash
git worktree unlock <path>
```
**What it does:** Allows worktree to be pruned again

---

## ✅ Commands We Use in This Project

### For Regular Development (Single Agent)

#### Starting a New Feature
```bash
# 1. Switch to develop branch
git checkout develop

# 2. Update from remote (if applicable)
git pull origin develop

# 3. Create feature branch
git checkout -b feature/your-feature-name

# 4. Work and commit
git add .
git commit -m "feat(scope): description"

# 5. When done, merge to develop
git checkout develop
git merge feature/your-feature-name

# 6. Delete feature branch
git branch -d feature/your-feature-name
```

#### Fixing a Bug
```bash
# 1. Create fix branch from master
git checkout master
git checkout -b fix/bug-description

# 2. Fix and commit
git add .
git commit -m "fix(scope): description"

# 3. Merge to master
git checkout master
git merge fix/bug-description

# 4. Clean up
git branch -d fix/bug-description
```

#### Checking Status
```bash
# Current branch
git branch --show-current

# All branches with info
git branch -v

# What's merged
git branch --merged
```

---

### For Multi-Agent Development (Worktrees)

#### Setup Multiple Work Environments
```bash
# Main directory stays on master
cd /home/user/Desktop/documentation_generator

# Agent 1: PDF Export
git worktree add ../documentation_generator-pdf -b feature/pdf-export

# Agent 2: Markdown Export
git worktree add ../documentation_generator-markdown -b feature/markdown-export

# Agent 3: Testing
git worktree add ../documentation_generator-tests -b feature/add-tests

# Verify setup
git worktree list
```

**Output:**
```
/home/user/Desktop/documentation_generator              ed77a06 [master]
/home/user/Desktop/documentation_generator-pdf          abc1234 [feature/pdf-export]
/home/user/Desktop/documentation_generator-markdown     def5678 [feature/markdown-export]
/home/user/Desktop/documentation_generator-tests        ghi9012 [feature/add-tests]
```

#### Working in Parallel
```bash
# Terminal 1 (Agent 1 - Claude instance 1)
cd /home/user/Desktop/documentation_generator-pdf
# Work on PDF export...

# Terminal 2 (Agent 2 - Claude instance 2)
cd /home/user/Desktop/documentation_generator-markdown
# Work on markdown export...

# Terminal 3 (Agent 3 - Claude instance 3)
cd /home/user/Desktop/documentation_generator-tests
# Work on tests...
```

#### Checking Progress Across Agents
```bash
# From main directory
cd /home/user/Desktop/documentation_generator

# See all worktrees and their status
git worktree list

# Check commits on each branch
git log --oneline --all --graph
```

#### Merging Features from Multiple Agents
```bash
# From main directory
cd /home/user/Desktop/documentation_generator
git checkout develop

# Merge Agent 1's work
git merge feature/pdf-export

# Test thoroughly
python run_doc_generator.py

# Merge Agent 2's work
git merge feature/markdown-export

# Test integration
python run_doc_generator.py

# Merge Agent 3's work
git merge feature/add-tests

# Run tests
pytest tests/
```

#### Cleanup After Merging
```bash
# Remove worktrees
git worktree remove ../documentation_generator-pdf
git worktree remove ../documentation_generator-markdown
git worktree remove ../documentation_generator-tests

# Delete merged branches
git branch -d feature/pdf-export
git branch -d feature/markdown-export
git branch -d feature/add-tests

# Clean up stale references
git worktree prune
```

---

## 📊 Command Comparison

### Branch vs Worktree: When to Use What?

| Scenario | Use Branches | Use Worktrees |
|----------|--------------|---------------|
| Quick feature work | ✅ `git checkout -b feature/name` | ❌ Overkill |
| Bug fix | ✅ `git checkout -b fix/name` | ❌ Overkill |
| Multiple parallel features | ⚠️ Requires frequent switching | ✅ Work simultaneously |
| Multi-agent development | ❌ Constant conflicts | ✅ Isolated environments |
| Testing while developing | ⚠️ Stash/commit to switch | ✅ Keep both running |
| Single developer | ✅ Simple, straightforward | ⚠️ More complex |
| Team collaboration | ✅ Standard workflow | ⚠️ Advanced technique |

---

## 🎯 Workflow Examples

### Example 1: Single Feature (Branches Only)
```bash
# Start
git checkout develop
git checkout -b feature/add-logging

# Work
vim doc_generator.py
git add doc_generator.py
git commit -m "feat(logging): add structured logging"

# Finish
git checkout develop
git merge feature/add-logging
git branch -d feature/add-logging
```

### Example 2: Multiple Features (Worktrees)
```bash
# Setup
git worktree add ../doc_gen-logging -b feature/add-logging
git worktree add ../doc_gen-cli -b feature/improve-cli
git worktree add ../doc_gen-docs -b docs/api-reference

# Work in parallel (3 terminals)
# Terminal 1:
cd ../doc_gen-logging
# Add logging...

# Terminal 2:
cd ../doc_gen-cli
# Improve CLI...

# Terminal 3:
cd ../doc_gen-docs
# Write docs...

# Merge when ready
cd /home/user/Desktop/documentation_generator
git checkout develop
git merge feature/add-logging
git merge feature/improve-cli
git merge docs/api-reference

# Cleanup
git worktree remove ../doc_gen-logging
git worktree remove ../doc_gen-cli
git worktree remove ../doc_gen-docs
git branch -d feature/add-logging feature/improve-cli docs/api-reference
git worktree prune
```

### Example 3: Emergency Hotfix (While Working on Feature)
```bash
# Currently on feature branch with uncommitted work
git branch --show-current  # feature/big-refactor

# Option A: Using Branches (requires stash)
git stash
git checkout master
git checkout -b fix/urgent-bug
# Fix bug...
git add .
git commit -m "fix(critical): resolve security issue"
git checkout master
git merge fix/urgent-bug
git branch -d fix/urgent-bug
git checkout feature/big-refactor
git stash pop

# Option B: Using Worktree (no stash needed)
git worktree add ../doc_gen-hotfix -b fix/urgent-bug
cd ../doc_gen-hotfix
# Fix bug...
git add .
git commit -m "fix(critical): resolve security issue"
cd /home/user/Desktop/documentation_generator
git checkout master
git merge fix/urgent-bug
git worktree remove ../doc_gen-hotfix
git branch -d fix/urgent-bug
# Continue working on feature/big-refactor without interruption
```

---

## 🔍 Quick Command Lookup

### Most Used Commands (Daily)
```bash
git checkout -b <branch>        # Create & switch to new branch
git checkout <branch>           # Switch branches
git branch -v                   # List branches with info
git merge <branch>              # Merge branch into current
git branch -d <branch>          # Delete merged branch
```

### Worktree Commands (Multi-Agent)
```bash
git worktree add <path> -b <branch>   # Create worktree + branch
git worktree list                      # List all worktrees
git worktree remove <path>             # Remove worktree
git worktree prune                     # Clean up stale worktrees
```

### Emergency Commands
```bash
git branch -D <branch>          # Force delete branch (unmerged)
git worktree remove --force     # Force remove worktree
git worktree repair             # Fix corrupted worktrees
```

---

## 📝 Notes

### Branch Naming Best Practices
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code improvements
- `docs/` - Documentation
- `chore/` - Maintenance tasks

### Worktree Best Practices
- Use descriptive directory names: `project-name-feature`
- Keep worktrees in same parent directory
- Clean up after merging (don't accumulate)
- Use `git worktree list` frequently
- Run `git worktree prune` periodically

### Common Pitfalls
❌ **Don't:** Create branches with spaces
✅ **Do:** Use hyphens: `feature/add-pdf-export`

❌ **Don't:** Delete branches without checking if merged
✅ **Do:** Use `git branch --merged` first

❌ **Don't:** Manually delete worktree directories
✅ **Do:** Use `git worktree remove`

❌ **Don't:** Have same branch checked out in multiple worktrees
✅ **Do:** Each worktree uses a unique branch

---

**Last Updated:** 2025-10-10
**Project:** Documentation Generator
**See also:** CONTRIBUTING.md, claude.md

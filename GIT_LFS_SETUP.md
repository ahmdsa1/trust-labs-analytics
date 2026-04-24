# Git LFS Setup for Large Data Files

Your database file (>25 MB) needs **Git LFS** to be pushed to GitHub.

## What is Git LFS?

Git LFS (Large File Storage) replaces large files with tiny pointers while storing actual files on GitHub's LFS server. This solves the 100 MB GitHub file limit.

---

## ✅ Quick Setup (Git Bash)

### Step 1: Install Git LFS
```bash
# Download and install Git LFS
# https://git-lfs.github.com/

# On Windows: Download installer and run it, then:
git lfs install
```

**Verify installation:**
```bash
git lfs version
# Output: git-lfs/3.x.x (Windows)
```

### Step 2: Navigate to Your Repo
```bash
cd "d:\Transferred_From_C\Documents\github_repo\trust-labs-analytics"
```

### Step 3: Initialize Git LFS in Your Repo
```bash
git lfs install
```

### Step 4: Track Large Files
```bash
# Track database file
git lfs track "*.db"

# Verify .gitattributes was created
cat .gitattributes
# Output: *.db filter=lfs diff=lfs merge=lfs -text
```

### Step 5: Commit .gitattributes
```bash
git add .gitattributes
git commit -m "Configure Git LFS for database files"
```

---

## 📤 Pushing Your Database File

### Option A: Copy DB to Repo First
```bash
# Copy your database to the repo
copy "d:\Transferred_From_C\Documents\trust_labs_pipeline\trust_labs.db" .

# Add and commit with LFS
git add trust_labs.db
git commit -m "Add trust_labs.db with Git LFS"

# Push to GitHub
git push origin main
```

### Option B: Multiple Large Files
```bash
# Track all databases and CSVs (if >25 MB)
git lfs track "*.db"
git lfs track "*.csv"

# Add .gitattributes
git add .gitattributes

# Add your large files
git add trust_labs.db
git add data/*.csv

# Commit
git commit -m "Add data files with Git LFS"

# Push
git push origin main
```

---

## 🔍 Verify Files Are Using LFS

```bash
# List all LFS-tracked files
git lfs ls-files

# Output should show your database:
# abc123def456 * trust_labs.db
```

---

## ⚠️ If File Already Committed Without LFS

If you already pushed the DB without LFS, rewrite history:

```bash
# Remove from git history (advanced)
git rm --cached trust_labs.db
git lfs track "*.db"
git add .gitattributes
git add trust_labs.db
git commit -m "Convert trust_labs.db to Git LFS"
git push -f origin main  # Force push (use carefully!)
```

---

## 📋 Complete Step-by-Step for Your Project

```bash
# 1. Open Git Bash
# 2. Navigate to repo
cd "d:\Transferred_From_C\Documents\github_repo\trust-labs-analytics"

# 3. Install Git LFS (one-time)
git lfs install

# 4. Track database files
git lfs track "*.db"

# 5. Commit tracking file
git add .gitattributes
git commit -m "Add Git LFS configuration"

# 6. Copy your database
copy "d:\Transferred_From_C\Documents\trust_labs_pipeline\trust_labs.db" .

# 7. Add database to Git
git add trust_labs.db

# 8. Commit
git commit -m "Add trust_labs.db database with Git LFS"

# 9. Push to GitHub
git push origin main

# 10. Verify
git lfs ls-files
```

---

## 🚀 GitHub LFS Limits

| Plan | LFS Storage |
|------|---|
| Free | 1 GB / month bandwidth |
| Paid | Extra storage purchased |

Your 25 MB file uses minimal bandwidth.

---

## ✅ After Setup

- Your repo will have `trust_labs.db` available
- Streamlit Cloud will automatically download the DB on deployment
- Your `app.py` will load it with `sqlite3.connect('trust_labs.db')`

---

## 🆘 Troubleshooting

### "Object does not exist" Error
```bash
# Make sure file exists
ls trust_labs.db

# If not, copy it
copy "d:\Transferred_From_C\Documents\trust_labs_pipeline\trust_labs.db" .
```

### Git LFS Not Found
```bash
# Reinstall Git LFS
# Download from: https://git-lfs.github.com/
# Run installer, then:
git lfs install
```

### Can't Find Git Bash
- Download Git for Windows: https://git-scm.com/download/win
- Install with "Git Bash"
- Open Git Bash and run commands above

---

**Your database will be ready to deploy to Streamlit Cloud! 🎉**

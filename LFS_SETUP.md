# Git LFS – add large files after installing

This repo is set up to track two large CSVs with Git LFS. Finish setup as follows.

## 1. Install Git LFS (one-time, on your machine)

**Option A – Homebrew** (fix permissions if needed first):
```bash
# If brew install failed with permission errors, run once:
sudo chown -R $(whoami) /opt/homebrew /opt/homebrew/Cellar /Users/ranbix/Library/Logs/Homebrew

brew install git-lfs
git lfs install
```

**Option B – Official installer:**  
https://git-lfs.github.com → download and run the installer, then run `git lfs install`.

## 2. Add the large files and push

From the repo root:

```bash
git add ICLR/iclr_all_years_submissions.csv ICLR/2025/iclr2025_full_transcript.csv
git commit -m "data: add large ICLR CSVs via LFS"
git push
```

LFS will upload the files to GitHub’s LFS storage; the push should succeed.

#!/bin/bash
set -e
if [ -d ".git" ]; then
  echo "A .git folder already exists here — nothing to do."
  exit 0
fi
git init -q
git add -A
git commit -q -m "Initial commit: Customer Churn Prediction MLOps project (Phases 0-2)"
echo "Git repository initialized with 1 commit."
echo ""
echo "Next steps:"
echo "  1. Create an empty repo on GitHub (no README/license/gitignore)."
echo "  2. git remote add origin https://github.com/<your-username>/<repo-name>.git"
echo "  3. git branch -M main"
echo "  4. git push -u origin main"
echo ""
echo "Note: ../dvc-storage (shipped alongside this folder) is your local"
echo "DVC remote. If that folder isn't next to your clone, just run:"
echo "  python src/generate_dataset.py && dvc repro"

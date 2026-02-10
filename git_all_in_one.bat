@echo off
echo --- Checking Git Status ---
git status

echo --- Staging All Changes Safely ---
git add -A 2>nul

echo --- Committing Changes ---
git commit -m "All-in-one safe update: backend + frontend + API/JWT fixes"

echo --- Pushing to Main ---
git push origin main

echo --- Showing Last 5 Commits ---
git log -5 --oneline

pause
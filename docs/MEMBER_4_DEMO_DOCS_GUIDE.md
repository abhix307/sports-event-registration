# Member 4 — Sample Data / Setup Docs / Demo

**Owner:** [Member 4 name] · **Branch:** `docs/demo-setup`

This is a small documentation and presentation-readiness role. It helps the other members demonstrate the app without taking over backend or UI implementation.

## Files to own

```text
init_db.py                  sample events and fictional demo registrations
README.md                   local setup and admin instructions
CAPSTONE_PRESENTATION_TEXT.md
docs/DEMO_RUNBOOK.md         presentation sequence
```

## Step-by-step

1. Pull the latest `main` and create branch `docs/demo-setup`.
2. Review the demo event names, dates, venues and fake sample registrations in `init_db.py`. Keep them fictional; do not include real student data.
3. Follow the README from a clean local setup. Correct any missing/unclear install or database-seed step.
4. Use `docs/DEMO_RUNBOOK.md` to prepare the class demonstration: event creation, student form, confirmation, admin review, statistics and CSV.
5. Capture screenshots from the running application for Slide 9. Do not create screenshots of features that are not implemented.
6. Ask Member 3 to confirm the steps are repeatable and Member 1 to confirm seed fields match the model.
7. Commit the documentation/seed-data changes and open a pull request.

## Example commands

```bash
git checkout main
git pull origin main
git checkout -b docs/demo-setup
python init_db.py
# Follow the README and demo runbook
git status
git add init_db.py README.md CAPSTONE_PRESENTATION_TEXT.md docs/DEMO_RUNBOOK.md
git diff --cached
git commit -m "docs: prepare repeatable project demo"
git push -u origin docs/demo-setup
```

Commit only files that were actually changed and checked.

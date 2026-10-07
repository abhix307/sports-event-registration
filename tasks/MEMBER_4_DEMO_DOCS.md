# Member 4 — Demo / Documentation Task Card

**Owner:** [Name / Reg. No.] · **Branch:** `docs/demo-setup`

## Scope

Make the project straightforward to install and present. Use fictional data only. Do not claim code or screenshots for features that do not work.

## Files

```text
init_db.py
README.md
CAPSTONE_PRESENTATION_TEXT.md
docs/DEMO_RUNBOOK.md
```

## Tasks

- [ ] Check that sample event and registration records are clearly marked fictional.
- [ ] Follow the setup instructions in README from a clean project folder.
- [ ] Correct any missing steps or stale admin/demo details.
- [ ] Verify README/runbook explain that the homepage theme follows the next event in Auto mode and that admins can override the preset per event.
- [ ] Write/verify the demo runbook in `docs/DEMO_RUNBOOK.md`.
- [ ] Prepare genuine screenshots of event list, registration, admin review and stats.
- [ ] Ask Member 3 to follow the runbook; ask Member 1 to check seed field names.
- [ ] Ensure `.env` and the local database are not added to Git.

## Commands

```bash
git checkout main
git pull origin main
git checkout -b docs/demo-setup
python init_db.py
# Follow README and docs/DEMO_RUNBOOK.md
git status
git add init_db.py README.md CAPSTONE_PRESENTATION_TEXT.md docs/DEMO_RUNBOOK.md
git diff --cached
git commit -m "docs: make the project demo repeatable"
git push -u origin docs/demo-setup
```

Commit only documentation/seed changes you actually made and checked.

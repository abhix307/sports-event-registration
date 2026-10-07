# Member 1 — Backend Task Card

**Owner:** [Name / Reg. No.] · **Branch:** `feature/backend-core`

## Scope

Own Flask routes, models, configuration, form validation and backend integration. Coordinate changes to template names with Member 2.

## Files

```text
app.py
config.py
extensions.py
forms.py
models/
routes/
```

## Tasks

- [ ] Review Event and Registration models and event foreign-key relationship.
- [ ] Verify event create/edit/delete and generated slugs.
- [ ] Verify participant and volunteer registration validation.
- [ ] Verify deadline, duplicate student ID and optional capacity enforcement.
- [ ] Verify admin approval/rejection updates SQLite status.
- [ ] Verify dashboard counts and CSV status export.
- [ ] Coordinate route, form and template data names with Member 2.
- [ ] For the homepage theme feature: keep the event's background override in the model, resolve Auto from the sport using an allowlisted theme key, and pass the next upcoming event to the homepage.
- [ ] Persist the theme on event create/edit and ensure existing SQLite databases get the new column without losing event data.
- [ ] Confirm invalid theme values cannot create arbitrary CSS classes; coordinate the preset labels with Member 2.
- [ ] Run Member 3's automated test suite before requesting merge.

## Commands

```bash
git checkout main
git pull origin main
git checkout -b feature/backend-core
# Make a real backend change and test it
python -m unittest discover -s tests -v
git status
git diff
git add app.py config.py extensions.py forms.py models/ routes/
git diff --cached
git commit -m "feat: improve registration validation"
git push -u origin feature/backend-core
```

Use only the paths actually changed. Open a pull request and state the exact tests run. Do not commit if no real change has been made.

# Member 1 — Backend / Integration Checklist

**Owner:** [Member 1 name] · **Branch:** `feature/backend-core`

## Files to own

```text
app.py
config.py
extensions.py
forms.py
models/
routes/
```

Member 3 owns the test checklist and automated test additions. Member 1 should still run the tests before merging and fix backend defects reported by Member 3.

## Step-by-step

1. **Sync the repo and start a branch.** See `GITHUB_WORKFLOW.md`; use `feature/backend-core` unless your team agrees on another name.
2. **Review the models.** Confirm events and registrations are related correctly, student IDs are normalized, and `(event_id, student_id)` prevents duplicates.
3. **Review event routes.** Confirm event slugs are automatic, deadlines close registration, and configured participant/volunteer limits are enforced.
4. **Review student routes.** Confirm required fields, email/phone validation, participant/volunteer choice, and success registration IDs work.
5. **Review admin routes.** Confirm event CRUD, status review (pending/approved/rejected), event registration counts, and CSV export work.
6. **Coordinate with Member 2.** Share exact route names, template variables and form field names before changing any of them.
7. **Run tests.** Use `python -m unittest discover -s tests -v`; ask Member 3 to review missing test cases.
8. **Commit only actual backend changes.** Stage exact Python files, inspect `git diff --cached`, commit, push and open a pull request.

## Backend/template contract

Registration field names include `full_name`, `student_id`, `department`, `year`, `email`, `phone`, `volunteer_role`, and `additional_info`. Common endpoints include `events.detail`, `events.register`, `admin.dashboard`, `admin.create_event`, and `admin.registrations`. Tell Member 2 before changing these names.

## Example commands

```bash
git checkout main
git pull origin main
git checkout -b feature/backend-core
# Make and run a real backend change
python -m unittest discover -s tests -v
git status
git diff
git add app.py forms.py models/ routes/
git diff --cached
git commit -m "feat: improve event registration validation"
git push -u origin feature/backend-core
```

Use the exact files changed; do not stage unrelated files. Describe the actual tests run in the pull request.

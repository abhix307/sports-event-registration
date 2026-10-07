# Member 3 — Testing Task Card

**Owner:** [Name / Reg. No.] · **Branch:** `test/registration-workflow`

## Scope

Keep the test evidence small and repeatable. Test from both the automated suite and the browser; report defects with steps rather than changing backend code without agreement.

## Files

```text
tests/test_app.py
docs/TEST_CHECKLIST.md
```

## Tasks

- [ ] Run `python -m unittest discover -s tests -v` and record the actual result.
- [ ] Check event creation and public event URL.
- [ ] Submit one fictional participant and one volunteer registration.
- [ ] Confirm duplicate IDs, expired deadlines and capacity limits are handled.
- [ ] Confirm new registrations start as Pending and admin status changes persist.
- [ ] Confirm dashboard/event counts update and CSV exports the right rows/statuses.
- [ ] Verify the home hero follows the earliest upcoming event and maps known sports to the expected preset; unknown sports use the arena fallback.
- [ ] Change an event's Homepage background in admin, save, and verify the next-event hero and dashboard label update; test Auto again.
- [ ] Check the sports theme at mobile, tablet and desktop widths.
- [ ] Record any issue with URL, steps, expected result, actual result and screenshot/log.
- [ ] Retest fixes from Members 1 or 2.

## Commands

```bash
git checkout main
git pull origin main
git checkout -b test/registration-workflow
python -m unittest discover -s tests -v
git status
git add tests/test_app.py docs/TEST_CHECKLIST.md
git diff --cached
git commit -m "test: cover registration review flow"
git push -u origin test/registration-workflow
```

Only mark a test passed after running it. If a step was checked manually, label it as manual.

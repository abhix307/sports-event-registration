# Shared Testing & Demo Sequence

Use this after the four task branches have been reviewed and merged to `main`.

## Automated tests

```bash
python -m unittest discover -s tests -v
```

Record the output and date in `docs/TEST_CHECKLIST.md`.

## Browser flow

1. Open Home / Events and inspect the event date, deadline, venue and status.
2. Open an event and submit a fictional participant registration.
3. Submit a fictional volunteer registration with a selected role.
4. Confirm each gets a registration ID and new entries show Pending.
5. Open Admin dashboard; add a new event and confirm its page is generated.
6. Open registrations for the event; approve one entry and reject another.
7. Confirm per-event and dashboard counts update.
8. Download participant and volunteer CSV files and inspect sample rows.

## Responsibilities during the demo

- **Member 1:** explain Flask routes, data model and SQLite storage.
- **Member 2:** explain student and admin interface choices.
- **Member 3:** explain test cases and show one result from actual test run.
- **Member 4:** guide the click-through, show seed data/runbook and manage screenshots.

Use fake/sample student details; do not display real personal information on presentation slides.

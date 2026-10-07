# Sports Registration — Four-Member Team Plan

This is the updated team plan for **four members**. Keep each role small and specific, and use each member's real name/GitHub account. Replace the bracketed placeholders before sharing.

## Member 1 — Backend / Integration Lead

**Main contribution:** Flask routes, database and registration behavior.

Primary files:

```text
app.py
config.py
extensions.py
forms.py
models/
routes/
```

Tasks:
- Check the Event and Registration models and SQLite relationship.
- Maintain event create/edit/delete and automatically generated event URLs.
- Maintain participant/volunteer registration and server-side validation.
- Maintain deadline, duplicate-ID and capacity enforcement.
- Maintain admin event pages and approval/rejection behavior.
- Explain the backend-to-template field/route contract to Member 2.

## Member 2 — UI / UX

**Main contribution:** visual layout and browser-side presentation.

Primary files:

```text
templates/
static/css/style.css
static/js/main.js
```

Tasks:
- Improve the home page, event list and event detail layout.
- Style the participant/volunteer forms and success page.
- Make the dashboard, registration status and action buttons easy to use.
- Check mobile, tablet and desktop widths.
- Preserve form field names and Flask `url_for(...)` endpoints; coordinate any requested backend contract change with Member 1.

## Member 3 — Testing / Quality Checks

**Main contribution:** verify the end-to-end flow and report defects.

Primary files:

```text
tests/test_app.py
docs/TEST_CHECKLIST.md
```

Tasks:
- Run the existing automated tests and record the command/result.
- Check event creation, public event page, student participant/volunteer submissions, duplicate prevention and deadlines.
- Check admin approval/rejection and that the displayed statistics change.
- Check CSV export and note any defect with reproduction steps.
- Add or improve a small number of workflow tests if a case is missing. Do not change backend logic without coordinating with Member 1.

## Member 4 — Sample Data / Documentation / Demo

**Main contribution:** make setup and the class demonstration easy to follow.

Primary files:

```text
init_db.py
README.md
CAPSTONE_PRESENTATION_TEXT.md
docs/DEMO_RUNBOOK.md
```

Tasks:
- Verify the fictional seed events/registrations are clear and easy to reset.
- Follow the README from a clean environment and report missing steps.
- Write a short demo runbook and prepare screenshots from the working app.
- Check that `.env`, the local SQLite database and virtual environment are not included in Git.
- Do not add real student personal information to demo data.

## Shared responsibilities

- Each member works on a separate feature branch and commits their own real changes with their own GitHub account.
- Members review pull requests from someone else; nobody should claim work they did not do.
- Member 1 and Member 2 coordinate route/form names; Member 3 checks the integrated flow; Member 4 checks setup and presentation readiness.
- The team runs the final demonstration together: **add event → student registers → SQLite stores row → admin approves/rejects → counts update → CSV export**.

## Suggested file ownership at a glance

| Member | Focus | Main files |
| --- | --- | --- |
| 1 | Flask / backend | `app.py`, `config.py`, `extensions.py`, `forms.py`, `models/`, `routes/` |
| 2 | UI / UX | `templates/`, `static/css/`, `static/js/` |
| 3 | Testing | `tests/test_app.py`, `docs/TEST_CHECKLIST.md` |
| 4 | Seed data / setup docs / demo | `init_db.py`, `README.md`, `CAPSTONE_PRESENTATION_TEXT.md`, `docs/DEMO_RUNBOOK.md` |

This is a proposed, manageable split. If your instructor assigned different work, update the table to match the work actually performed.

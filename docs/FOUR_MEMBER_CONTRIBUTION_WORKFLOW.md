# Sports Registration — Four-Member Contribution & GitHub Workflow

**Shareable team plan**  
Project: Sports Registration · Course/Class: [Class/Semester] · College: [College]  
Repository: [GitHub URL] · Coordinator: [Name]

> Replace bracketed items with real team details. This plan gives each of four members a small, identifiable contribution. It is a workflow plan, not proof that a Git command or task has already happened. Record only real work and real GitHub evidence.

## 1. Four-member role split

| Member | Small, clear contribution | Main files |
| --- | --- | --- |
| **Member 1 — Backend** [Name / Reg. No.] | Own Flask routes, model/validation changes and integration decisions. Store the event background override, resolve Auto from sport, pass the next upcoming event, and preserve existing SQLite data. | `app.py`, `config.py`, `extensions.py`, `forms.py`, `models/`, `routes/` |
| **Member 2 — UI/UX** [Name / Reg. No.] | Build the sports-first matchday presentation: scoreboard-style hero, sport-specific visual accents, responsive event pages and clear admin theme selector. Keep backend behavior intact. | `templates/`, `static/css/style.css`, optional small changes to `static/js/main.js` |
| **Member 3 — Testing** [Name / Reg. No.] | Run workflow tests, verify Auto sport mapping and admin overrides, and record defects/results. Backend fixes go to Member 1; visual fixes go to Member 2. | `tests/test_app.py`, `docs/TEST_CHECKLIST.md` |
| **Member 4 — Demo / Documentation** [Name / Reg. No.] | Verify setup instructions, keep fictional seed/demo records clear, explain and demonstrate the event-driven theme control, prepare the runbook and screenshots. | `init_db.py`, `README.md`, `docs/DEMO_RUNBOOK.md`, `CAPSTONE_PRESENTATION_TEXT.md` |

The tasks are intentionally modest. Member 1 and Member 2 build their areas; Member 3 verifies the flows; Member 4 makes setup and the presentation repeatable. All four participate in final integration/review. Do not create a separate testing role if your actual team does not have four members; update this file to the real roster.

## 2. Work sequence

### Stage A — Agree on the baseline

- Fill in names, registration numbers, class/semester, coordinator and repository URL.
- Member 1 identifies the backend/template contract (routes, form fields and data passed to Jinja), including the safe theme key and next-event value.
- Member 2 confirms the sports-first hero and admin theme selector will use that contract without changing backend names.
- Member 3 prepares checks for Auto mapping, per-event override and the normal student/admin flow.
- Member 4 follows the README and checks demo data/setup instructions, including how to show the theme change.

### Stage B — Upload the project and invite everyone

One member creates an **empty** GitHub repository, adds the other three accounts as collaborators and pushes the project once. The exact commands are in `GITHUB_WORKFLOW.md`. Make sure `.env`, `instance/`, `*.db`, `.venv/` and `venv/` stay ignored.

### Stage C — Each member makes a real, small change on a branch

Suggested branch names (use the actual names the team creates):

```text
Member 1: feature/backend-core
Member 2: feature/ui-refresh
Member 3: test/registration-workflow
Member 4: docs/demo-setup
```

Each person syncs `main`, creates their branch, changes only their assigned files, tests their work, commits under their own GitHub identity, pushes the branch and opens a pull request.

### Stage D — Review and integrate

- Member 1 reviews Member 2's template links/form names.
- Member 3 tests the combined branch before/after merge and records the result.
- Member 4 checks that seed/setup/demo instructions match the working app.
- The PR author fixes review comments, then a different member approves and merges.
- Everyone pulls the final `main` branch and participates in the final demo.

## 3. Git commands for a feature contribution

After the repository is created and cloned:

```bash
git checkout main
git pull origin main
git checkout -b feature/<your-short-task>
# Make a real change in your assigned files
git status
git diff
git add <changed-files>
git diff --cached
git commit -m "<type>: <short factual description>"
git push -u origin feature/<your-short-task>
```

Then create a pull request on GitHub with base `main`, select your feature branch, explain what changed and how you tested it, and ask another team member to review it. After merge:

```bash
git checkout main
git pull origin main
```

Use real author identities. Do not use empty commits, fake authors or invented pull requests to make the contribution history look bigger.

## 4. Example commit messages (examples only)

- Member 1: `feat: enforce event registration limits`
- Member 2: `style: add sports matchday home interface`
- Member 3: `test: verify event theme override and mapping`
- Member 4: `docs: add repeatable presentation runbook`

Only use a message after the corresponding member has actually made that change.

## 5. Shared end-to-end demo

1. Admin opens the dashboard, adds/edits an event, and chooses Auto or a background preset.
2. Home shows the earliest upcoming event; its sport theme or admin override drives the matchday background.
3. Student opens the event page and registers; success shows an ID and the record is stored in SQLite as Pending.
4. Admin opens event registrations and approves/rejects entries.
5. Dashboard and event statistics show participant, volunteer, pending, approved and rejected counts.
6. Admin exports a CSV.

## 6. Evidence for the teacher

Capture evidence from the real GitHub repository:

- repository page and collaborator list;
- actual branch names;
- commit history with each member's real account;
- merged pull requests and actual reviewer comments, if the team used them;
- `git log --oneline --graph --all` and `git shortlog -sne --all` output;
- screenshots of the working app for Slide 9.

If the team has not created a repository yet, complete Stage B before writing “we used GitHub” in the past tense. If AI assistance must be disclosed by course policy, follow that policy.

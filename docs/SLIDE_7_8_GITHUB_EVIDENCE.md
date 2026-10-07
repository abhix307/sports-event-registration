# Fill-in text for Presentation Slides 7–8 (Four-Member Team)

Use actual repository history and each member's real name. Do not invent branches, commits or PRs.

## Slide 7 — Git & GitHub Workflow

- **Repository:** [GitHub URL]
- **Repository owner:** [Member name]
- **Collaborators:** [Member 2], [Member 3], [Member 4]
- **Branches actually used:** [branch → member → task]
- **Commits:** [one or two actual commit messages per member]
- **Pull requests/reviews:** [actual PR IDs, reviewers and merge status; or say “not used”]
- **Integration:** [how the four areas were brought together and tested]

### Workflow summary

```text
Create repository → add collaborators → clone → create task branch
→ edit assigned files → add/commit → push → open pull request
→ teammate review → merge → pull main → run final tests
```

Commands the team may have used:

```bash
git clone <repository-url>
git checkout -b <task-branch>
git add <changed-files>
git commit -m "<factual message>"
git push -u origin <task-branch>
# Open/review/merge pull request on GitHub
git checkout main
git pull origin main
```

If these are example commands and not yet used, label the slide section **“Workflow followed/planned”** accurately.

## Slide 8 — Team Contributions

| Member | Contribution | Evidence from the repository |
| --- | --- | --- |
| Member 1 — [Name / Reg. No.] | Flask routes, database models and registration/admin logic | [actual commit(s), PR or file history] |
| Member 2 — [Name / Reg. No.] | Jinja templates, CSS, JavaScript and responsive UI | [actual commit(s), PR or file history] |
| Member 3 — [Name / Reg. No.] | Automated/manual workflow tests and defect retesting | [actual test commit/checklist/results] |
| Member 4 — [Name / Reg. No.] | Seed data, local setup/demo documentation and screenshots | [actual docs/seed commit/runbook] |
| All members | Integration review and final presentation flow | [actual review comments, test run or demo evidence] |

## Evidence screenshots to collect

1. **Repository Overview:** repo name, default branch and source tree.
2. **Collaborators:** all four actual GitHub accounts, if the repo is private.
3. **Commit history:** member names and real messages.
4. **Branches / Pull Requests:** only those actually created and merged.
5. **Tests:** actual test output or test checklist with date.
6. **Working application:** event creation, student registration, stored entry, admin approve/reject and updated counts.

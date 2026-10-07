# Git & GitHub Workflow — Four-Person Sports Registration Team

This guide describes how four team members can collaborate with small, traceable tasks. The project folder currently has **no GitHub remote configured**, so the team must create the repository and use its real URL. Do not claim a push, branch or pull request until it actually exists.

## 1. One-time repository setup — Member 1 (repository owner)

1. Create a new **empty** GitHub repository named `sports-registration` (do not add a README or `.gitignore` there; the local folder already has them).
2. Add Members 2, 3 and 4 under **Settings → Collaborators** using their real GitHub accounts.
3. In a terminal opened in the `sports-registration` project folder, check ignored local files:

```bash
git check-ignore -v .env instance/sports_registration.db .venv
```

The project `.gitignore` excludes local settings, the SQLite database and virtual environments. Never commit `.env`, `instance/`, `*.db`, `.venv/` or `venv/`.

4. Initialize and push the initial source snapshot:

```bash
git init -b main
git status --short
git add .
git status --short
git diff --cached
git commit -m "chore: initialize sports registration project"
git remote add origin https://github.com/<OWNER>/<REPOSITORY>.git
git remote -v
git push -u origin main
```

Replace `<OWNER>` and `<REPOSITORY>` with real values. If `git init -b main` is unsupported, run `git init` and then `git branch -M main`.

Each person sets their own commit identity in their own clone (use their actual verified GitHub email):

```bash
git config user.name "Your real name"
git config user.email "Your verified GitHub email"
git config --get user.name
git config --get user.email
```

Do not set another member's name/email on your commits.

## 2. Other members clone the project

Each of Members 2, 3 and 4 runs:

```bash
git clone https://github.com/<OWNER>/<REPOSITORY>.git
cd sports-registration
git status
git log --oneline --decorate -5
```

They then create their own branch from current `main`.

## 3. Four suggested branches and file ownership

Use these as examples; record the branch names the team actually creates.

| Member | Example branch | Files normally changed |
| --- | --- | --- |
| 1 — Backend | `feature/backend-core` | `app.py`, `config.py`, `extensions.py`, `forms.py`, `models/`, `routes/` |
| 2 — UI/UX | `feature/ui-refresh` | `templates/`, `static/css/`, `static/js/` |
| 3 — Testing | `test/registration-workflow` | `tests/test_app.py`, `docs/TEST_CHECKLIST.md` |
| 4 — Demo/docs | `docs/demo-setup` | `init_db.py`, `README.md`, `docs/DEMO_RUNBOOK.md`, presentation text |

Start each branch after pulling the latest `main`:

```bash
git checkout main
git pull origin main
git checkout -b <your-branch>
```

## 4. Check, stage and commit real changes

```bash
git status
git diff
git add <specific-changed-files>
git diff --cached
git commit -m "<type>: <short factual message>"
```

Use only the files you changed. Example commit subjects (do not use unless you made that change):

```text
feat: enforce event registration limits
style: improve event and admin screens
test: cover approval and duplicate registration
docs: add repeatable presentation runbook
```

Before pushing:

```bash
git status
git log --oneline --decorate -5
git push -u origin <your-branch>
```

## 5. Pull request and review

On GitHub, open **Pull requests → New pull request**, select `main` as the base and your branch as the compare branch. Include:

```text
What changed:
- [actual changes]
Files/area:
- [actual files or role area]
Tested:
- [commands actually run]
- [manual browser flow actually checked]
```

Ask a different teammate to review. Suggested cross-review:

- Member 1 reviews Member 2's Jinja routes/form names.
- Member 2 checks Member 1's public/admin screens still render clearly.
- Member 1 reviews Member 3's tests; Member 3 retests after fixes.
- Member 3 reviews Member 4's setup/demo steps; Member 4 confirms the steps work from a clean start.

Fix review comments, then merge the PR. After it is merged:

```bash
git checkout main
git pull origin main
git branch -d <your-branch>
```

The owner can delete the remote branch in GitHub after merge.

## 6. If `main` changed during your work

Commit or stash your current changes, then:

```bash
git fetch origin
git checkout <your-branch>
git merge origin/main
```

Resolve conflicts carefully, remove conflict markers and test again:

```bash
git add <resolved-files>
git commit -m "chore: resolve merge conflicts"
git push
```

Ask the file owner before resolving a conflict in a file they own.

## 7. Easier option: GitHub Desktop

If command-line Git is unfamiliar:

1. Member 1 adds the existing project folder to GitHub Desktop and publishes it to a **private** GitHub repository.
2. Member 1 adds the other three as collaborators in GitHub Settings.
3. Each teammate chooses **File → Clone Repository**.
4. Each creates a branch using **Branch → New Branch** and edits only their assigned files.
5. Review the changed-file list, enter a clear commit summary, and click **Commit to [branch]**.
6. Click **Push origin / Publish branch**, then **Create Pull Request**.
7. Another teammate reviews and the owner merges the PR on GitHub.

This still creates real commits under each member's real GitHub account.

## 8. Evidence to show the teacher

Capture actual evidence after doing the workflow:

- repository page and collaborator list;
- branches for the members who created them;
- commit history showing real authors and messages;
- pull requests and review/merge status, if used;
- terminal output from `git log --oneline --graph --all` and `git shortlog -sne --all`;
- working application screenshots for Slide 9.

Do not create empty/fake commits, alter authorship or claim work that did not happen. If your course requires disclosure of AI assistance, follow that policy.

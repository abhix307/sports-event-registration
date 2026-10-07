# Member 3 — Testing / Quality Checklist

**Owner:** [Member 3 name] · **Branch:** `test/registration-workflow`

This is a small, useful role: check the project from a student's and organizer's point of view, run the existing automated tests, record results and report reproducible defects. Do not take ownership of Flask implementation unless the team agrees.

## Files to own

```text
tests/test_app.py
docs/TEST_CHECKLIST.md
```

## Step-by-step

1. Pull the latest `main` branch and create `test/registration-workflow`.
2. Create/activate the project virtual environment and install `requirements.txt`.
3. Run the automated suite:

   ```bash
   python -m unittest discover -s tests -v
   ```

4. Follow `TEST_CHECKLIST.md` in a browser. Test with fictional student details only.
5. When something fails, record: page/URL, steps, expected result, actual result and screenshot/log if available.
6. Send backend issues to Member 1 and layout/usability issues to Member 2; retest their fixes.
7. Add or improve a small test case in `tests/test_app.py` only when you can describe its expected behavior.
8. Commit the test/checklist changes, push the branch, and open a pull request.

## Example commands

```bash
git checkout main
git pull origin main
git checkout -b test/registration-workflow
python -m unittest discover -s tests -v
git status
git add tests/test_app.py docs/TEST_CHECKLIST.md
git diff --cached
git commit -m "test: verify approval and registration flow"
git push -u origin test/registration-workflow
```

Do not report a test as passed unless you ran it and saw it pass. If you only did manual testing, say so in the test notes.

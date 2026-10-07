# Member 2 — UI/UX Checklist

**Owner:** [Member 2 name] · **Branch:** `feature/ui-refresh`

> For the detailed code-chunk plan—including exact HTML/CSS files, code snippets, verification checks and the commit/push after each chunk—use [`tasks/MEMBER_2_UI_UX.md`](../tasks/MEMBER_2_UI_UX.md). This file is a shorter orientation.

## Files to own

```text
templates/base.html
templates/index.html
templates/events.html
templates/_event_card.html
templates/event_detail.html
templates/registration_form.html
templates/registration_success.html
templates/admin/*.html
templates/errors/*.html
static/css/style.css
static/js/main.js
```

Do not change Flask routes, models or forms for a visual task. Coordinate with Member 1 if a UI change needs different backend data.

## Step-by-step

1. Start the app and inspect Home, Events, an event page, a registration form and the admin screens.
2. Write down 3–5 specific improvements; avoid changing the whole site at once.
3. Set consistent color, type, spacing, button and focus styles in `static/css/style.css`.
4. Improve the public flow in this order: `base.html` → `index.html` → `_event_card.html` → `events.html` → `event_detail.html` → registration/success templates.
5. Improve admin pages: make **Add new event** visible, separate participants from volunteers, and make Pending / Approved / Rejected easy to distinguish.
6. Test at phone (~375 px), tablet (~768 px) and desktop (~1280 px). Verify links, form errors and status actions still work.
7. Send any backend/data mismatch to Member 1; Member 3 can include it in the test checklist.
8. Commit only template/CSS/JS changes to `feature/ui-refresh`, push the branch and open a pull request for review.

## Names to preserve

Keep existing Flask endpoints (`events.detail`, `events.register`, `admin.dashboard`, `admin.create_event`, etc.) and form names (`full_name`, `student_id`, `department`, `year`, `email`, `phone`, `volunteer_role`, `additional_info`). Keep POST forms for approve/reject/delete and retain CSRF markup for normal local mode.

## Example commands

```bash
git checkout main
git pull origin main
git checkout -b feature/ui-refresh
# Make and visually test a real UI change
git status
git diff
git add templates/ static/css/style.css static/js/main.js
git diff --cached
git commit -m "style: improve event and review screens"
git push -u origin feature/ui-refresh
```

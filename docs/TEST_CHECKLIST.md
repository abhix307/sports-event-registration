# Manual Test Checklist

Tester: [Name] · Date: [Date] · Commit/branch tested: [Commit or branch]

Run automated checks first:

```bash
python -m unittest discover -s tests -v
```

Record the actual output/result: [Passed / Failed / Notes]

## Public student flow

- [ ] Home page loads with the matchday hero for the earliest upcoming event.
- [ ] In Auto mode, football/basketball/track or another sport receives its mapped theme; unknown sports use the arena fallback.
- [ ] Changing the next event's Homepage background override in admin changes the home hero after reload; Auto follows the sport again.
- [ ] Home page lists the upcoming events below the matchday hero.
- [ ] Event page shows date, deadline, venue, status, sport accent and registration choices.
- [ ] Valid participant form submission shows a registration ID.
- [ ] Valid volunteer form submission asks for a preferred role and shows an ID.
- [ ] Required fields and invalid email/phone show friendly validation messages.
- [ ] Same student ID cannot register twice for the same event.
- [ ] Registration is blocked after the deadline.
- [ ] A configured full capacity blocks another submission.
- [ ] New registration appears in SQLite/admin list as Pending.

## Admin flow

- [ ] Admin can add an event; its page appears on the public site.
- [ ] Admin can set Homepage background to Auto or a preset on create and edit; dashboard shows the effective look.
- [ ] Admin can edit and delete an event.
- [ ] Participant and volunteer tables are visually separate.
- [ ] Admin can approve a pending registration.
- [ ] Admin can reject a pending registration.
- [ ] Dashboard and event statistics reflect the new status.
- [ ] CSV files download and include the correct registrations/status.

## Evidence / defects

- Screenshot or log: [filename/link]
- Defect steps: [page, action, expected, actual]
- Retest after fix: [result]

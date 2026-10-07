# Sports Registration — Class Demo Runbook

Presenter: [Name] · Team: [Names] · Preview/local URL: [URL]

## Demo sequence (about 4–6 minutes)

### 1. Show the sports-themed home page and event list

- Open Home. Point out the matchday board for the next upcoming event and the sport-specific stadium palette.
- Explain that the theme follows the next event's sport in Auto mode, and an admin can choose a per-event background preset to override it.
- Open Events and point out the date, registration deadline, venue and status on each event row.
- Open an event page; explain that its URL is generated from the event name.

### 2. Show a student registration

- Use a fictional name and a new student ID (avoid the seeded `DEMO-*` IDs).
- Register as participant, then show the success page and registration ID.
- Optionally show the volunteer form and role selection.
- Explain that the registration is saved in SQLite and begins as Pending.

### 3. Show the admin workflow

- Open the Admin dashboard. In the supervised Arena preview, admin tools may be available without login; local mode uses the credentials configured in `.env`.
- Click **Add new event**, enter sample details, and choose **Homepage background**. Leave it on Auto to match the sport, or select a preset to override it.
- Save and return to the dashboard. If this is now the next event by date, reload Home to show its background; otherwise edit the current next event to demonstrate the override.
- Return to the dashboard and show the new event with its generated event page and effective hero look.
- Open its registrations. Approve one entry and reject another.
- Show the status labels and updated registration statistics.
- Optionally export participant or volunteer CSV.

### 4. Explain storage

- `events` stores event data, including its `background_theme` auto/override choice.
- The home page reads the next event by date and resolves its effective sport theme for the matchday hero.
- `registrations` stores the student form data, event ID, role, timestamp and review status.
- The database is `instance/sports_registration.db` locally; it is intentionally not committed to Git.

## Fictional demo records

`init_db.py` includes fictional sample registrations for the Football Tournament so the Pending / Approved / Rejected screens are populated on first setup. Explain that these are sample records, not real students.

## Reset demo database (destructive)

Only do this if you are comfortable deleting local demo entries. Stop the app, remove `instance/sports_registration.db`, then run:

```bash
python init_db.py
```

## Screenshots for Slide 9

- Home/event list
- Event detail and register options
- Student form and success ID
- Admin dashboard and Add event action
- Registration table with Approve/Reject buttons and statistics

Use screenshots captured from the current working application.

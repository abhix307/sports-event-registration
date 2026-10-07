# Sports Registration

A simple, locally runnable college sports-event registration MVP built with Flask, SQLite, SQLAlchemy, Jinja, HTML, CSS, and a small amount of JavaScript.

Students can browse upcoming events and register as a participant or volunteer without creating an account. An administrator can create/edit/delete events, review the separate participant and volunteer lists, and export registrations as CSV.

## Features

- Public matchday homepage with a bold sports interface, upcoming-event scoreboard, and sport-specific background theme
- Homepage theme automatically follows the next upcoming event's sport; admin can override the look per event
- Public event list with date, deadline, venue, description, and registration status
- Automatic event URLs generated from event names, for example `/event/football-tournament`
- Participant and volunteer registration with server-side validation
- One registration per student ID per event (database unique constraint plus friendly validation)
- Registration deadlines enforced by the backend; the deadline date itself is closed
- Optional participant and volunteer limits
- Simple session-based admin login with hashed password verification
- Admin can approve or reject each participant/volunteer registration
- Dashboard statistics for events, participants, volunteers, pending, approved, and rejected entries
- Per-event review counts, separate registration lists, and CSV export (including approval status)
- CSRF protection on forms, friendly error pages, and responsive starter UI
- Fictional sample events and registrations loaded through `init_db.py`

In the admin **Add/Edit event** form, **Homepage background** defaults to **Auto — match the sport**. The homepage takes its colors from the next event by date; the admin can select a preset for that event to override the automatic sport theme. As the event calendar advances, the next event (and its chosen theme) updates automatically.

## Requirements

- Python 3.9 or newer
- pip

## Local setup

Clone the repository (or open the folder containing the downloaded project), then create a virtual environment:

```bash
git clone <repository-url>
cd sports-registration
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows Command Prompt
.venv\Scripts\activate.bat

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and create your local settings file:

```bash
pip install -r requirements.txt
cp .env.example .env
```

On Windows, if `cp` is unavailable, use:

```powershell
Copy-Item .env.example .env
```

Open `.env` and change `SECRET_KEY`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD` before sharing the project. The example local credentials are `admin` / `change-me`.

Initialize the SQLite database and add the three sample events:

```bash
python init_db.py
```

Run the application:

```bash
python app.py
```

Then open **http://127.0.0.1:5000**. The app also creates database tables automatically on first start, so `python app.py` works even if you skip the seed command; `init_db.py` is what inserts the demo events.

You can also use Flask's development command:

```bash
flask --app app run
```

The local SQLite database is created at `instance/sports_registration.db`. It is ignored by Git and can be recreated with `python init_db.py`.

## Admin access and password handling

The admin sign-in page is at **/admin/login**. Set the username and password in your local `.env` file:

```dotenv
ADMIN_USERNAME=admin
ADMIN_PASSWORD=use-a-local-demo-password
```

The application hashes `ADMIN_PASSWORD` in memory and verifies it with Werkzeug's password-hash functions; the password is not saved in the database. For environments where you prefer to store only a hash in configuration, set `ADMIN_PASSWORD_HASH` instead. Generate a hash with:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

Put the generated value in `.env` as `ADMIN_PASSWORD_HASH=...`. When `ADMIN_PASSWORD_HASH` is set, it takes precedence over `ADMIN_PASSWORD`. Keep `.env` private and do not commit it.

### Arena presentation mode

The Arena live preview can be started with `DEMO_MODE=true` so the class presentation can open `/admin` directly without getting stuck on browser session/CSRF behavior inside the embedded preview. In this mode, admin routes are intentionally open and CSRF checks are disabled for the preview only. The normal local application defaults to `DEMO_MODE=false`, requires admin sign-in, and keeps CSRF protection on. Never enable demo mode on a public or shared deployment.

When the Arena preview is in demo mode, click **Admin dashboard** in the navigation, then **Add new event**. The preview includes fictional registrations so you can show pending, approved, and rejected examples immediately.

## Main routes

| Route | Purpose |
| --- | --- |
| `/` | Home page and upcoming events |
| `/events` | All events |
| `/event/<slug>` | Event details and registration options |
| `/event/<slug>/register/participant` | Participant registration |
| `/event/<slug>/register/volunteer` | Volunteer registration |
| `/admin/login` | Admin sign in |
| `/admin` | Admin dashboard |
| `/admin/events/create` | Create an event |
| `/admin/events/<id>/edit` | Edit an event |
| `/admin/events/<id>/registrations` | View, approve, and reject participants and volunteers |
| `/admin/registrations/<id>/status/<status>` | Update an individual registration's review status |
| `/admin/events/<id>/registrations/export/participant.csv` | Export participants and approval status |
| `/admin/events/<id>/registrations/export/volunteer.csv` | Export volunteers |

## Demo events

`python init_db.py` adds the following events when the events table is empty. If registrations are also empty, it adds four clearly fictional Football Tournament entries (pending, approved, rejected, and volunteer-pending) so the review screen and status statistics can be demonstrated immediately:

- Football Tournament — 20 October 2026, registration closes 15 October 2026, College Ground
- Basketball Tournament — 25 October 2026, registration closes 20 October 2026, Indoor Stadium
- Athletics Meet — 5 November 2026, registration closes 30 October 2026, College Stadium

The seed data is intentionally easy to edit in `init_db.py`. Running the command again does not overwrite existing events.

## Tests

The project includes a small end-to-end test suite using Python's standard `unittest` module:

```bash
python -m unittest discover -s tests -v
```

The tests exercise local admin login, Arena demo access, event creation and sport-theme overrides, next-event homepage theme selection, participant and volunteer registration, duplicate prevention, limits, deadline enforcement, approval/rejection, status statistics, CSV export, and event deletion.

## Project layout

```text
sports-registration/
├── app.py                  # Flask app factory and local entry point
├── config.py               # Environment-based configuration
├── extensions.py           # SQLAlchemy, CSRF, SQLite foreign-key setup
├── forms.py                # CSRF-protected forms and validation
├── init_db.py              # Demo database initialization
├── models/
│   └── models.py            # Event and Registration tables
├── routes/
│   ├── main.py              # Home and event list
│   ├── events.py            # Event detail and student registration
│   └── admin.py             # Admin, event CRUD, registrations, CSV
├── templates/               # Jinja pages, separate from backend logic
├── static/css/style.css     # Replaceable visual layer
├── static/js/main.js        # Small navigation/delete-confirmation helpers
└── tests/test_app.py        # MVP workflow tests
```

For the four-person task plan, open the `tasks/` folder. Start with `tasks/README.md`, then share `tasks/WORKFLOW.md` and `tasks/GITHUB_WORKFLOW.md`. The contribution overview and presentation evidence template are in `docs/FOUR_MEMBER_CONTRIBUTION_WORKFLOW.md` and `docs/SLIDE_7_8_GITHUB_EVIDENCE.md`. Fill in actual member names and repository details.

The CSS and templates are intentionally separate from routes and database models. On startup, the app adds the new `background_theme` column to an existing SQLite `events` table so prior local databases retain their events. This is a targeted compatibility step, not a general migration system; other schema changes still require an explicit migration or a disposable development database reset.

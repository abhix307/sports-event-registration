# Capstone Project Presentation — Slide Text

> Replace all bracketed fields with your team's actual details. For the GitHub slide, use real branch names, commit IDs and pull requests from your repository; do not claim workflow steps that your team did not perform.

## Slide 1 — Title

**SPORTS REGISTRATION**  
*College Sports Event Management & Registration System*

- Team Member 1: **[Name]** · Reg. No. **[Number]**
- Team Member 2: **[Name]** · Reg. No. **[Number]**
- Team Member 3: **[Name]** · Reg. No. **[Number]**
- Team Member 4: **[Name]** · Reg. No. **[Number]**
- Class / Semester: **[Class and semester]**
- Project Coordinator: **[Coordinator name]**
- Department / College: **[Department and college]**

**Suggested visual:** College logo or a clean sports-event photo/illustration.

---

## Slide 2 — Problem Statement

- College sports registrations are often collected through separate forms and shared links.
- Organizers must manually sort participant and volunteer responses for every event.
- Students can miss registration deadlines or confuse the event date with the closing date.
- Duplicate entries and unclear capacity make registration harder to manage.
- A central, event-specific system is needed to keep event information and student entries organized.

**Speaker line:** “We built one place where students can find the event details and organizers can manage all registrations.”

---

## Slide 3 — Objectives

- Display upcoming sports events with dates, deadlines and venues.
- Generate a shareable page for every event.
- Let students register as participants or volunteers without creating an account.
- Validate deadlines, duplicate student IDs and event capacity on the server.
- Store registrations in SQLite for the organizer to review.
- Let the admin add events, review entries, approve or reject registrations, and view summary statistics.

---

## Slide 4 — Project Overview

**Sports Registration** is a web application for college sports-event information and registration.

- **Students:** browse events, view details, select Participant or Volunteer, submit a registration and receive a registration ID.
- **Admin:** add, edit or delete events; view separate participant and volunteer lists; approve or reject entries; export CSV files.
- **Automatic controls:** event URLs are generated from event names; registration closes at the deadline; optional participant and volunteer limits are enforced.
- **Dashboard statistics:** event, participant and volunteer totals, plus pending, approved and rejected registrations.

---

## Slide 5 — Technologies Used

- **Programming language:** Python
- **Backend framework:** Flask
- **Database:** SQLite
- **ORM / database layer:** Flask-SQLAlchemy (SQLAlchemy)
- **Frontend:** HTML, CSS, JavaScript and Jinja2 templates
- **Forms and validation:** Flask-WTF / WTForms
- **Version control and collaboration:** Git and GitHub
- **IDE / development tools:** [VS Code / PyCharm / actual tools used]

---

## Slide 6 — System Design / Architecture

### Request and data flow

```text
Student or Admin (Web Browser)
             │  HTTP request / form submission
             ▼
Flask Routes ── Forms & Validation ── Admin Session Checks
             │
             ▼
       SQLAlchemy ORM
             │
             ▼
       SQLite Database
       ├── Events
       └── Registrations (linked by event_id)
             │
             ▼
Flask + Jinja2 Templates → HTML/CSS/JavaScript response
             │
             └──────────────────────────────→ Browser
```

### Main modules

- **Public events:** home page, event list and event detail pages.
- **Registration:** participant and volunteer forms, duplicate/deadline/capacity validation.
- **Admin:** event management, registration review, approval/rejection and CSV export.
- **Data layer:** `Event` and `Registration` tables; each event can have many registrations.

**Database rule:** a student ID can be registered only once for the same event.

---

## Slide 7 — Git & GitHub Workflow

- Created a shared GitHub repository: **[Repository URL]**.
- Repository owner: **[Name]**; collaborators who cloned it: **[list members who actually cloned]**.
- Work was split across backend, UI/UX, testing and setup/demo documentation.
- Members worked on task branches: **[actual branch names]**.
- Changes were staged, committed and pushed with descriptive messages.
- Pull requests were reviewed and merged: **[actual PR numbers/status, or “not used”]**.
- The team pulled the latest `main` branch and tested the integrated workflow.

**Commands (illustrative):** `git clone`, `git checkout -b`, `git add`, `git commit`, `git push`, `git pull`.

**Evidence to show:** repository page, branch list, commit history and a real pull request/merge. Replace the bracketed items with the team's actual GitHub activity.

---

## Slide 8 — Team Collaboration

### Team Member 1 — Backend / Integration

- Flask routes, data models and server-side validation
- Event and student registration workflow
- Admin review actions and statistics

### Team Member 2 — UI / UX

- Jinja page layout and navigation
- Event list, event details and registration forms
- Responsive CSS and small JavaScript interactions

### Team Member 3 — Testing / Quality Checks

- Ran the automated and manual workflow tests
- Checked deadlines, duplicates, capacity and approval/rejection
- Recorded issues and retested fixes

### Team Member 4 — Sample Data / Documentation / Demo

- Checked fictional seed events and registrations
- Verified local setup instructions
- Prepared demo sequence and screenshots

**Shared work:** all members reviewed the integrated student-to-admin flow. Adjust these bullets to match each member’s actual contributions.

**Evidence:** add each member’s real commit, pull request, test result or documentation change from GitHub.

---

## Slide 9 — Project Implementation / Demo

### Demonstration sequence

1. Open the events page and select an event.
2. Register a student as a participant or volunteer.
3. Show the success message and registration ID.
4. Open the admin dashboard and add an event.
5. Open that event’s registrations; approve one entry and reject another.
6. Show participant, volunteer, pending, approved and rejected counts; optionally export a CSV.

### Screenshots to insert

- **[Screenshot 1]** Home page / upcoming events
- **[Screenshot 2]** Event details and registration options
- **[Screenshot 3]** Registration form and success page
- **[Screenshot 4]** Admin dashboard with “Add new event” and statistics
- **[Screenshot 5]** Registration list showing Pending / Approved / Rejected actions

*Use screenshots from the running application; do not use mockups as proof of working features.*

---

## Slide 10 — Conclusion & Future Scope

### Conclusion

- Sports Registration centralizes college event information and student sign-ups.
- Event and registration data is stored in SQLite and organized by event.
- The admin can manage events, review entries, approve or reject students, see summary counts and export CSV.
- The project provides a functional, locally runnable MVP with a replaceable frontend.

### Future scope

- Student accounts and email notifications
- Attendance tracking, QR check-in and certificates
- Team registrations and Excel export
- Sport-specific match results and score statistics (current dashboard statistics focus on registrations and review status)

**Closing line:** “The system reduces manual tracking and gives students and organizers one clear place to manage college sports registrations.”

"""Create the SQLite tables and insert clear, fictional demonstration records."""

from datetime import date

from app import create_app
from extensions import db
from models.models import Event, Registration


DEMO_EVENTS = [
    {
        "slug": "football-tournament",
        "name": "Football Tournament",
        "sport": "Football",
        "description": "The annual college football tournament. Bring your team spirit and compete for the campus cup.",
        "event_date": date(2026, 10, 20),
        "registration_deadline": date(2026, 10, 15),
        "venue": "College Ground",
        "max_participants": 50,
        "max_volunteers": 15,
    },
    {
        "slug": "basketball-tournament",
        "name": "Basketball Tournament",
        "sport": "Basketball",
        "description": "A fast-paced inter-department basketball tournament at the campus indoor court.",
        "event_date": date(2026, 10, 25),
        "registration_deadline": date(2026, 10, 20),
        "venue": "Indoor Stadium",
        "max_participants": 40,
        "max_volunteers": 12,
    },
    {
        "slug": "athletics-meet",
        "name": "Athletics Meet",
        "sport": "Athletics",
        "description": "A day of track and field events celebrating participation, sportsmanship, and personal bests.",
        "event_date": date(2026, 11, 5),
        "registration_deadline": date(2026, 10, 30),
        "venue": "College Stadium",
        "max_participants": None,
        "max_volunteers": None,
    },
]

# Fictional examples so the review screen has pending/approved/rejected entries
# on first launch. Use the public forms to add real demonstration submissions.
DEMO_REGISTRATIONS = [
    {
        "registration_type": "participant",
        "status": "pending",
        "full_name": "Asha Thomas",
        "student_id": "DEMO-CS-101",
        "department": "Computer Science",
        "year": "2nd year",
        "email": "asha@example.edu",
        "phone": "+91 90000 00001",
        "additional_info": "Fictional sample entry for demonstration.",
    },
    {
        "registration_type": "participant",
        "status": "approved",
        "full_name": "Rohan Menon",
        "student_id": "DEMO-EC-204",
        "department": "Electronics",
        "year": "3rd year",
        "email": "rohan@example.edu",
        "phone": "+91 90000 00002",
        "additional_info": "Fictional sample entry for demonstration.",
    },
    {
        "registration_type": "participant",
        "status": "rejected",
        "full_name": "Maya Joseph",
        "student_id": "DEMO-ME-205",
        "department": "Mechanical Engineering",
        "year": "1st year",
        "email": "maya@example.edu",
        "phone": "+91 90000 00003",
        "additional_info": "Fictional sample entry for demonstration.",
    },
    {
        "registration_type": "volunteer",
        "status": "pending",
        "full_name": "Nikhil Raj",
        "student_id": "DEMO-BA-301",
        "department": "Business Administration",
        "year": "2nd year",
        "email": "nikhil@example.edu",
        "phone": "+91 90000 00004",
        "volunteer_role": "Registration Desk",
        "additional_info": "Fictional sample entry for demonstration.",
    },
]


def init_database():
    app = create_app()
    with app.app_context():
        db.create_all()
        if Event.query.count() == 0:
            db.session.add_all(Event(**item) for item in DEMO_EVENTS)
            db.session.commit()
            print("Added 3 demo events.")
        else:
            print("Existing events were left unchanged.")

        if Registration.query.count() == 0:
            football = Event.query.filter_by(slug="football-tournament").first()
            if football:
                db.session.add_all(
                    Registration(event_id=football.id, **item)
                    for item in DEMO_REGISTRATIONS
                )
                db.session.commit()
                print("Added 4 fictional demo registrations (pending, approved, rejected).")
        else:
            print("Existing registrations were left unchanged.")

        print(f"SQLite database: {app.config['SQLALCHEMY_DATABASE_URI']}")


if __name__ == "__main__":
    init_database()

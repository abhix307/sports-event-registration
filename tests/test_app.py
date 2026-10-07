"""Small end-to-end checks for the MVP's main workflow (standard unittest)."""

import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from werkzeug.security import generate_password_hash

from app import create_app
from extensions import db
from models.models import Event, Registration


class SportsRegistrationFlowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_dir.name) / "test_sports.db"
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "test-secret-key",
                "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
                "WTF_CSRF_ENABLED": False,
                "ADMIN_USERNAME": "test-admin",
                "ADMIN_PASSWORD_HASH": generate_password_hash("test-password"),
            }
        )
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()
        self.temp_dir.cleanup()

    def _login(self):
        return self.client.post(
            "/admin/login",
            data={"username": "test-admin", "password": "test-password"},
            follow_redirects=True,
        )

    def _create_event(
        self,
        *,
        deadline_offset=10,
        participant_limit=2,
        volunteer_limit=2,
        name="Test Football Cup",
        sport="Football",
        background_theme="auto",
    ):
        today = date.today()
        response = self.client.post(
            "/admin/events/create",
            data={
                "name": name,
                "sport": sport,
                "background_theme": background_theme,
                "description": "A test event for the registration flow.",
                "event_date": (today + timedelta(days=30)).isoformat(),
                "registration_deadline": (today + timedelta(days=deadline_offset)).isoformat(),
                "venue": "College Ground",
                "max_participants": str(participant_limit) if participant_limit else "",
                "max_volunteers": str(volunteer_limit) if volunteer_limit else "",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        return Event.query.filter_by(name=name).first()

    @staticmethod
    def _student(student_id="23CS101", name="Asha Thomas"):
        return {
            "full_name": name,
            "student_id": student_id,
            "department": "Computer Science",
            "year": "2nd year",
            "email": f"{student_id.lower()}@college.edu",
            "phone": "+91 98765 43210",
            "additional_info": "",
        }

    def test_admin_to_registration_and_csv_flow(self):
        # Admin pages require a session before event creation.
        self.assertEqual(self.client.get("/admin/").status_code, 302)
        self._login()

        event = self._create_event()
        self.assertIsNotNone(event)
        self.assertEqual(event.slug, "test-football-cup")
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertIn(b"Test Football Cup", self.client.get("/").data)
        self.assertEqual(self.client.get(f"/event/{event.slug}").status_code, 200)

        participant_response = self.client.post(
            f"/event/{event.slug}/register/participant",
            data=self._student(),
        )
        self.assertEqual(participant_response.status_code, 200)
        self.assertIn(b"REG-00001", participant_response.data)

        duplicate_data = self._student(student_id="23cs101", name="Another Name")
        duplicate_data["student_id"] = " 23cs101 "
        duplicate_response = self.client.post(
            f"/event/{event.slug}/register/participant",
            data=duplicate_data,
        )
        self.assertEqual(duplicate_response.status_code, 409)
        self.assertIn(b"You are already registered for this event.", duplicate_response.data)

        volunteer_data = self._student(student_id="23IT205", name="Nikhil Raj")
        volunteer_data["volunteer_role"] = "Registration Desk"
        volunteer_response = self.client.post(
            f"/event/{event.slug}/register/volunteer", data=volunteer_data
        )
        self.assertEqual(volunteer_response.status_code, 200)
        self.assertIn(b"VOL-00002", volunteer_response.data)

        self.assertEqual(Registration.query.count(), 2)
        participant = Registration.query.filter_by(student_id="23CS101").one()
        volunteer = Registration.query.filter_by(student_id="23IT205").one()
        self.assertEqual(participant.status, "pending")
        self.assertEqual(volunteer.status, "pending")

        approve_response = self.client.post(
            f"/admin/registrations/{participant.id}/status/approved",
            follow_redirects=True,
        )
        self.assertEqual(approve_response.status_code, 200)
        self.assertEqual(participant.status, "approved")
        reject_response = self.client.post(
            f"/admin/registrations/{volunteer.id}/status/rejected",
            follow_redirects=True,
        )
        self.assertEqual(reject_response.status_code, 200)
        self.assertEqual(volunteer.status, "rejected")

        admin_view = self.client.get("/admin/")
        self.assertIn(b"Test Football Cup", admin_view.data)
        self.assertIn(b"Add new event", admin_view.data)
        self.assertIn(b"Participants", admin_view.data)
        registration_view = self.client.get(
            f"/admin/events/{event.id}/registrations"
        )
        self.assertIn(b"Asha Thomas", registration_view.data)
        self.assertIn(b"Nikhil Raj", registration_view.data)
        self.assertIn(b"Approved", registration_view.data)
        self.assertIn(b"Rejected", registration_view.data)

        participant_csv = self.client.get(
            f"/admin/events/{event.id}/registrations/export/participant.csv"
        )
        self.assertEqual(participant_csv.status_code, 200)
        self.assertIn(b"text/csv", participant_csv.headers["Content-Type"].encode())
        self.assertIn(b"23CS101", participant_csv.data)
        self.assertIn(b"Approved", participant_csv.data)
        self.assertNotIn(b"Nikhil Raj", participant_csv.data)

        volunteer_csv = self.client.get(
            f"/admin/events/{event.id}/registrations/export/volunteer.csv"
        )
        self.assertIn(b"Registration Desk", volunteer_csv.data)

    def test_next_event_hero_uses_sport_theme_and_admin_override(self):
        self._login()
        event = self._create_event(
            name="Test Basketball Night",
            sport="Basketball",
            background_theme="football",
        )
        self.assertEqual(event.background_theme, "football")
        self.assertEqual(event.visual_theme, "football")

        home = self.client.get("/")
        self.assertIn(b"sport-theme-football", home.data)
        self.assertIn(b"Test Basketball Night", home.data)

        # Auto mode follows the sport if the admin has not selected an override.
        event.background_theme = "auto"
        event.sport = "Athletics"
        db.session.commit()
        self.assertEqual(event.visual_theme, "track")
        self.assertIn(b"sport-theme-track", self.client.get("/").data)
        event.background_theme = "not-a-valid-theme"
        self.assertEqual(event.visual_theme, "track")

        # Editing an event through the admin form saves a new override.
        response = self.client.post(
            f"/admin/events/{event.id}/edit",
            data={
                "name": event.name,
                "sport": event.sport,
                "background_theme": "basketball",
                "description": event.description,
                "event_date": event.event_date.isoformat(),
                "registration_deadline": event.registration_deadline.isoformat(),
                "venue": event.venue,
                "max_participants": "",
                "max_volunteers": "",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        db.session.refresh(event)
        self.assertEqual(event.background_theme, "basketball")
        self.assertIn(b"sport-theme-basketball", self.client.get("/").data)

    def test_registration_capacity_and_deadline_are_enforced(self):
        self._login()
        event = self._create_event(participant_limit=1, volunteer_limit=1)
        first = self.client.post(
            f"/event/{event.slug}/register/participant", data=self._student()
        )
        self.assertEqual(first.status_code, 200)

        full = self.client.post(
            f"/event/{event.slug}/register/participant",
            data=self._student(student_id="23CS102", name="Second Student"),
        )
        self.assertEqual(full.status_code, 409)
        self.assertIn(b"Participant registration is full.", full.data)
        self.assertEqual(Registration.query.count(), 1)

        event.registration_deadline = date.today()
        db.session.commit()
        closed_response = self.client.post(
            f"/event/{event.slug}/register/volunteer",
            data={**self._student(student_id="23ME301"), "volunteer_role": "Other"},
            follow_redirects=True,
        )
        self.assertEqual(closed_response.status_code, 200)
        self.assertIn(b"Registration is closed for this event.", closed_response.data)
        self.assertEqual(Registration.query.count(), 1)

    def test_arena_demo_mode_runs_admin_and_student_flow_without_sign_in(self):
        self.app.config["DEMO_MODE"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        dashboard = self.client.get("/admin/")
        self.assertEqual(dashboard.status_code, 200)
        self.assertIn(b"Add new event", dashboard.data)
        self.assertIn(b"ARENA PRESENTATION MODE", dashboard.data)

        event = self._create_event()
        student_response = self.client.post(
            f"/event/{event.slug}/register/participant", data=self._student()
        )
        self.assertEqual(student_response.status_code, 200)
        registration = Registration.query.filter_by(student_id="23CS101").one()
        self.assertEqual(registration.status, "pending")

        review_response = self.client.post(
            f"/admin/registrations/{registration.id}/status/approved",
            follow_redirects=True,
        )
        self.assertEqual(review_response.status_code, 200)
        self.assertEqual(registration.status, "approved")
        self.assertEqual(self.client.get("/admin/events/create").status_code, 200)

    def test_event_delete_cascades_registrations(self):
        self._login()
        event = self._create_event()
        registration = Registration(
            event_id=event.id,
            registration_type="participant",
            full_name="Asha Thomas",
            student_id="23CS101",
            department="Computer Science",
            year="2nd year",
            email="asha@college.edu",
            phone="9876543210",
        )
        db.session.add(registration)
        db.session.commit()

        response = self.client.post(
            f"/admin/events/{event.id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Event.query.count(), 0)
        self.assertEqual(Registration.query.count(), 0)


if __name__ == "__main__":
    unittest.main()

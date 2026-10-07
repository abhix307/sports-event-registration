"""SQLAlchemy models for events and student registrations."""

from datetime import date, datetime, timezone

from sqlalchemy import CheckConstraint, UniqueConstraint

from extensions import db


VALID_BACKGROUND_THEMES = {
    "auto",
    "arena",
    "football",
    "basketball",
    "field",
    "track",
    "court",
    "racket",
    "water",
}

SPORT_THEME_RULES = (
    (("football", "soccer"), "football"),
    (("basketball",), "basketball"),
    (("athletics", "track and field", "track"), "track"),
    (("volleyball",), "court"),
    (("tennis", "badminton", "racket"), "racket"),
    (("swimming", "aquatics", "water polo"), "water"),
    (("cricket", "rugby", "hockey", "baseball", "softball"), "field"),
)


class Event(db.Model):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint(
            "max_participants IS NULL OR max_participants >= 1",
            name="ck_events_positive_participant_limit",
        ),
        CheckConstraint(
            "max_volunteers IS NULL OR max_volunteers >= 1",
            name="ck_events_positive_volunteer_limit",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    name = db.Column(db.String(140), nullable=False)
    sport = db.Column(db.String(80), nullable=False)
    # "auto" follows the sport name; a selected theme lets admins override the hero.
    background_theme = db.Column(db.String(24), nullable=False, default="auto")
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False, index=True)
    registration_deadline = db.Column(db.Date, nullable=False, index=True)
    venue = db.Column(db.String(160), nullable=False)
    max_participants = db.Column(db.Integer, nullable=True)
    max_volunteers = db.Column(db.Integer, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    registrations = db.relationship(
        "Registration",
        back_populates="event",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="Registration.created_at.desc()",
    )

    @property
    def status(self):
        """Return the current display status, calculated from today's date."""
        today = date.today()
        if self.event_date < today:
            return "Completed"
        if self.registration_deadline <= today:
            return "Registration Closed"
        return "Registration Open"

    @property
    def status_slug(self):
        return {
            "Completed": "completed",
            "Registration Closed": "closed",
            "Registration Open": "open",
        }[self.status]

    @property
    def visual_theme(self):
        """Return a safe theme key for this event's homepage hero."""
        override = (self.background_theme or "auto").strip().lower()
        if override in VALID_BACKGROUND_THEMES and override != "auto":
            return override

        sport_name = (self.sport or "").strip().lower()
        for keywords, theme in SPORT_THEME_RULES:
            if any(keyword in sport_name for keyword in keywords):
                return theme
        return "arena"

    @property
    def is_registration_open(self):
        # The deadline day itself is closed: registration must be before it.
        return self.event_date >= date.today() and self.registration_deadline > date.today()

    def registration_count(self, registration_type, include_rejected=False):
        query = Registration.query.filter_by(
            event_id=self.id, registration_type=registration_type
        )
        # Pending registrations reserve a place; rejected applications do not.
        if not include_rejected:
            query = query.filter(Registration.status != "rejected")
        return query.count()

    def registration_limit(self, registration_type):
        if registration_type == "participant":
            return self.max_participants
        if registration_type == "volunteer":
            return self.max_volunteers
        return None

    def __repr__(self):
        return f"<Event {self.name!r}>"


class Registration(db.Model):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("event_id", "student_id", name="uq_registration_event_student"),
        CheckConstraint(
            "registration_type IN ('participant', 'volunteer')",
            name="ck_registration_type",
        ),
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name="ck_registration_status",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(
        db.Integer,
        db.ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    registration_type = db.Column(db.String(20), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="pending", index=True)
    full_name = db.Column(db.String(120), nullable=False)
    # The application normalizes student IDs to uppercase before saving so the
    # unique constraint also catches case-only variations.
    student_id = db.Column(db.String(40), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    volunteer_role = db.Column(db.String(80), nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    event = db.relationship("Event", back_populates="registrations")

    @property
    def registration_code(self):
        prefix = "REG" if self.registration_type == "participant" else "VOL"
        return f"{prefix}-{self.id:05d}" if self.id is not None else ""

    def __repr__(self):
        return f"<Registration {self.registration_type} #{self.id}>"

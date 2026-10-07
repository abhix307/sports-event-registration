"""Admin login, event management, registration review, and CSV export."""

import csv
import hmac
import io
from datetime import date
from functools import wraps

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from extensions import db
from forms import AdminLoginForm, EventForm
from models.models import Event, Registration

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_app.config.get("DEMO_MODE"):
            return view(*args, **kwargs)
        if not session.get("admin_logged_in"):
            flash("Please sign in to access the admin area.", "info")
            return redirect(url_for("admin.login"))
        return view(*args, **kwargs)

    return wrapped


def make_unique_slug(name, exclude_id=None):
    """Make a URL-safe event slug and add a number if the name already exists."""
    import re
    import unicodedata

    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-") or "event"
    candidate = base
    suffix = 2
    while True:
        query = Event.query.filter_by(slug=candidate)
        if exclude_id is not None:
            query = query.filter(Event.id != exclude_id)
        if query.first() is None:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def _valid_event_dates(form):
    """Add a helpful validation message when the deadline follows the event."""
    if (
        form.event_date.data
        and form.registration_deadline.data
        and form.registration_deadline.data > form.event_date.data
    ):
        form.registration_deadline.errors.append(
            "The registration deadline must be on or before the event date."
        )
        return False
    return True


def _event_form_context(form, heading, submit_label):
    return render_template(
        "admin/event_form.html",
        form=form,
        heading=heading,
        submit_label=submit_label,
    )


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_app.config.get("DEMO_MODE"):
        return redirect(url_for("admin.dashboard"))
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    form = AdminLoginForm()
    if form.validate_on_submit():
        expected_username = current_app.config.get("ADMIN_USERNAME", "admin")
        username_ok = hmac.compare_digest(
            form.username.data.strip(), str(expected_username)
        )
        try:
            password_ok = check_password_hash(
                current_app.config["ADMIN_PASSWORD_HASH"], form.password.data
            )
        except (ValueError, TypeError):
            password_ok = False

        if username_ok and password_ok:
            session.clear()
            session["admin_logged_in"] = True
            session.permanent = True
            flash("You are signed in.", "success")
            return redirect(url_for("admin.dashboard"))

        flash("The username or password is incorrect.", "error")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout", methods=["POST"])
@admin_required
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@admin_required
def dashboard():
    events = Event.query.order_by(Event.event_date.asc(), Event.name.asc()).all()
    event_rows = []
    for event in events:
        event_registrations = Registration.query.filter_by(event_id=event.id)
        event_rows.append(
            {
                "event": event,
                "participants": Registration.query.filter_by(
                    event_id=event.id, registration_type="participant"
                ).count(),
                "volunteers": Registration.query.filter_by(
                    event_id=event.id, registration_type="volunteer"
                ).count(),
                "pending": event_registrations.filter_by(status="pending").count(),
                "approved": event_registrations.filter_by(status="approved").count(),
                "rejected": event_registrations.filter_by(status="rejected").count(),
            }
        )
    stats = {
        "total_events": len(events),
        "upcoming_events": sum(event.event_date >= date.today() for event in events),
        "participants": Registration.query.filter_by(
            registration_type="participant"
        ).count(),
        "volunteers": Registration.query.filter_by(
            registration_type="volunteer"
        ).count(),
        "pending": Registration.query.filter_by(status="pending").count(),
        "approved": Registration.query.filter_by(status="approved").count(),
        "rejected": Registration.query.filter_by(status="rejected").count(),
    }
    return render_template("admin/dashboard.html", event_rows=event_rows, stats=stats)


@admin_bp.route("/events/create", methods=["GET", "POST"])
@admin_required
def create_event():
    form = EventForm()
    if form.validate_on_submit() and _valid_event_dates(form):
        event = Event(
            slug=make_unique_slug(form.name.data.strip()),
            name=form.name.data.strip(),
            sport=form.sport.data.strip(),
            background_theme=form.background_theme.data or "auto",
            description=form.description.data.strip(),
            event_date=form.event_date.data,
            registration_deadline=form.registration_deadline.data,
            venue=form.venue.data.strip(),
            max_participants=form.max_participants.data,
            max_volunteers=form.max_volunteers.data,
        )
        db.session.add(event)
        db.session.commit()
        flash("Event created. Its event page is ready to share.", "success")
        return redirect(url_for("admin.dashboard"))

    return _event_form_context(form, "Add a new event", "Add event")


@admin_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    event = db.get_or_404(Event, event_id)
    form = EventForm(obj=event)
    if form.validate_on_submit() and _valid_event_dates(form):
        old_name = event.name
        event.name = form.name.data.strip()
        if event.name != old_name:
            event.slug = make_unique_slug(event.name, exclude_id=event.id)
        event.sport = form.sport.data.strip()
        event.background_theme = form.background_theme.data or "auto"
        event.description = form.description.data.strip()
        event.event_date = form.event_date.data
        event.registration_deadline = form.registration_deadline.data
        event.venue = form.venue.data.strip()
        event.max_participants = form.max_participants.data
        event.max_volunteers = form.max_volunteers.data
        db.session.commit()
        flash("Event details updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return _event_form_context(form, "Edit event", "Save changes")


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@admin_required
def delete_event(event_id):
    event = db.get_or_404(Event, event_id)
    name = event.name
    db.session.delete(event)
    db.session.commit()
    flash(f"{name} and its registrations were deleted.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/events/<int:event_id>/registrations")
@admin_required
def registrations(event_id):
    event = db.get_or_404(Event, event_id)
    participants = (
        Registration.query.filter_by(event_id=event.id, registration_type="participant")
        .order_by(Registration.created_at.desc())
        .all()
    )
    volunteers = (
        Registration.query.filter_by(event_id=event.id, registration_type="volunteer")
        .order_by(Registration.created_at.desc())
        .all()
    )
    event_registrations = Registration.query.filter_by(event_id=event.id)
    registration_stats = {
        "total": event_registrations.count(),
        "pending": event_registrations.filter_by(status="pending").count(),
        "approved": event_registrations.filter_by(status="approved").count(),
        "rejected": event_registrations.filter_by(status="rejected").count(),
    }
    return render_template(
        "admin/registrations.html",
        event=event,
        participants=participants,
        volunteers=volunteers,
        registration_stats=registration_stats,
    )


@admin_bp.route(
    "/registrations/<int:registration_id>/status/<string:new_status>",
    methods=["POST"],
)
@admin_required
def update_registration_status(registration_id, new_status):
    if new_status not in {"pending", "approved", "rejected"}:
        abort(404)
    registration = db.get_or_404(Registration, registration_id)
    registration.status = new_status
    db.session.commit()
    flash(
        f"{registration.registration_code} marked {new_status}.",
        "success" if new_status == "approved" else "info",
    )
    return redirect(
        url_for("admin.registrations", event_id=registration.event_id)
    )


def _csv_safe(value):
    """Neutralize spreadsheet formula prefixes in user-submitted cell values."""
    text = "" if value is None else str(value)
    if text.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text
    return text


@admin_bp.route(
    "/events/<int:event_id>/registrations/export/<string:registration_type>.csv"
)
@admin_required
def export_registrations(event_id, registration_type):
    if registration_type not in {"participant", "volunteer"}:
        abort(404)

    event = db.get_or_404(Event, event_id)
    records = (
        Registration.query.filter_by(
            event_id=event.id, registration_type=registration_type
        )
        .order_by(Registration.created_at.asc())
        .all()
    )

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(
        [
            "Name",
            "Student ID",
            "Department",
            "Year",
            "Email",
            "Phone",
            "Event",
            "Registration Type",
            "Approval Status",
            "Volunteer Role",
            "Additional Information",
            "Registration Date",
        ]
    )
    for record in records:
        writer.writerow(
            [
                _csv_safe(record.full_name),
                _csv_safe(record.student_id),
                _csv_safe(record.department),
                _csv_safe(record.year),
                _csv_safe(record.email),
                _csv_safe(record.phone),
                _csv_safe(event.name),
                record.registration_type.title(),
                record.status.title(),
                _csv_safe(record.volunteer_role),
                _csv_safe(record.additional_info),
                record.created_at.strftime("%Y-%m-%d %H:%M") if record.created_at else "",
            ]
        )

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f'attachment; filename="{event.slug}-{registration_type}s.csv"'
    )
    response.headers["Cache-Control"] = "no-store"
    return response

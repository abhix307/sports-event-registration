"""Public event detail and student registration routes."""

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from sqlalchemy.exc import IntegrityError

from extensions import db
from forms import ParticipantRegistrationForm, VolunteerRegistrationForm
from models.models import Event, Registration

events_bp = Blueprint("events", __name__)


@events_bp.route("/event/<string:slug>")
def detail(slug):
    event = Event.query.filter_by(slug=slug).first_or_404()
    return render_template(
        "event_detail.html",
        event=event,
        participant_count=event.registration_count("participant"),
        volunteer_count=event.registration_count("volunteer"),
    )


@events_bp.route(
    "/event/<string:slug>/register/<string:registration_type>", methods=["GET", "POST"]
)
def register(slug, registration_type):
    if registration_type not in {"participant", "volunteer"}:
        abort(404)

    event = Event.query.filter_by(slug=slug).first_or_404()
    if registration_type == "participant":
        form = ParticipantRegistrationForm()
        page_title = "Participant registration"
        button_text = "Register as participant"
    else:
        form = VolunteerRegistrationForm()
        page_title = "Volunteer registration"
        button_text = "Register as volunteer"

    if not event.is_registration_open:
        flash("Registration is closed for this event.", "warning")
        return redirect(url_for("events.detail", slug=event.slug))

    if form.validate_on_submit():
        student_id = form.student_id.data.strip().upper()

        # One registration per student and event, regardless of registration type.
        existing = Registration.query.filter_by(
            event_id=event.id, student_id=student_id
        ).first()
        if existing:
            form.student_id.errors.append("You are already registered for this event.")
            return (
                render_template(
                    "registration_form.html",
                    event=event,
                    form=form,
                    registration_type=registration_type,
                    page_title=page_title,
                    button_text=button_text,
                ),
                409,
            )

        limit = event.registration_limit(registration_type)
        current_count = event.registration_count(registration_type)
        if limit is not None and current_count >= limit:
            kind = "Participant" if registration_type == "participant" else "Volunteer"
            flash(f"{kind} registration is full.", "error")
            return (
                render_template(
                    "registration_form.html",
                    event=event,
                    form=form,
                    registration_type=registration_type,
                    page_title=page_title,
                    button_text=button_text,
                ),
                409,
            )

        registration = Registration(
            event_id=event.id,
            registration_type=registration_type,
            full_name=form.full_name.data.strip(),
            student_id=student_id,
            department=form.department.data.strip(),
            year=form.year.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            volunteer_role=(
                form.volunteer_role.data
                if registration_type == "volunteer"
                else None
            ),
            additional_info=(form.additional_info.data or "").strip() or None,
        )
        db.session.add(registration)
        try:
            db.session.commit()
        except IntegrityError:
            # The unique constraint is the final guard against simultaneous
            # duplicate submissions; do not expose database exception details.
            db.session.rollback()
            duplicate = Registration.query.filter_by(
                event_id=event.id, student_id=student_id
            ).first()
            if duplicate:
                form.student_id.errors.append(
                    "You are already registered for this event."
                )
            else:
                flash("We could not save your registration. Please try again.", "error")
            return (
                render_template(
                    "registration_form.html",
                    event=event,
                    form=form,
                    registration_type=registration_type,
                    page_title=page_title,
                    button_text=button_text,
                ),
                409,
            )

        return render_template(
            "registration_success.html", event=event, registration=registration
        )

    return render_template(
        "registration_form.html",
        event=event,
        form=form,
        registration_type=registration_type,
        page_title=page_title,
        button_text=button_text,
    )

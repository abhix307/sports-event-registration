"""Public home and event-list pages."""

from datetime import date

from flask import Blueprint, render_template

from models.models import Event

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    upcoming_events = (
        Event.query.filter(Event.event_date >= date.today())
        .order_by(Event.event_date.asc(), Event.name.asc())
        .limit(3)
        .all()
    )
    next_event = upcoming_events[0] if upcoming_events else None
    return render_template(
        "index.html", events=upcoming_events, next_event=next_event
    )


@main_bp.route("/events")
def events_list():
    events = Event.query.order_by(Event.event_date.asc(), Event.name.asc()).all()
    return render_template("events.html", events=events)

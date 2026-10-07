"""CSRF-protected web forms and lightweight server-side validation."""

import re

from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^[0-9+()\-\s]{7,25}$")


def valid_email(_form, field):
    if not EMAIL_PATTERN.fullmatch((field.data or "").strip()):
        raise ValidationError("Enter a valid email address.")


def valid_phone(_form, field):
    if not PHONE_PATTERN.fullmatch((field.data or "").strip()):
        raise ValidationError("Enter a valid phone number (7–25 characters).")


class AdminLoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(max=80)], render_kw={"autocomplete": "username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"autocomplete": "current-password"}
    )
    submit = SubmitField("Sign in")


class EventForm(FlaskForm):
    name = StringField("Event name", validators=[DataRequired(), Length(max=140)])
    sport = StringField("Sport", validators=[DataRequired(), Length(max=80)])
    background_theme = SelectField(
        "Homepage background",
        choices=[
            ("auto", "Auto — match the sport"),
            ("football", "Football lights"),
            ("basketball", "Basketball court"),
            ("field", "Field sport"),
            ("track", "Track & field"),
            ("court", "Indoor court"),
            ("racket", "Racket sport"),
            ("water", "Aquatics"),
            ("arena", "All-sports arena"),
        ],
        default="auto",
        validators=[Optional()],
    )
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=3000)])
    event_date = DateField(
        "Event date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    registration_deadline = DateField(
        "Registration deadline", format="%Y-%m-%d", validators=[DataRequired()]
    )
    venue = StringField("Venue", validators=[DataRequired(), Length(max=160)])
    max_participants = IntegerField(
        "Maximum participants (optional)",
        validators=[Optional(), NumberRange(min=1, message="Enter 1 or more, or leave blank.")],
    )
    max_volunteers = IntegerField(
        "Maximum volunteers (optional)",
        validators=[Optional(), NumberRange(min=1, message="Enter 1 or more, or leave blank.")],
    )
    submit = SubmitField("Save event")


class StudentRegistrationForm(FlaskForm):
    full_name = StringField("Full name", validators=[DataRequired(), Length(min=2, max=120)])
    student_id = StringField(
        "Student ID / Roll number", validators=[DataRequired(), Length(min=2, max=40)]
    )
    department = StringField("Department", validators=[DataRequired(), Length(max=100)])
    year = StringField(
        "Year / class", validators=[DataRequired(), Length(max=40)], render_kw={"placeholder": "e.g. 2nd year"}
    )
    email = StringField("Email", validators=[DataRequired(), valid_email, Length(max=160)])
    phone = StringField("Phone number", validators=[DataRequired(), valid_phone, Length(max=30)])
    additional_info = TextAreaField(
        "Additional information (optional)", validators=[Optional(), Length(max=1000)]
    )


class ParticipantRegistrationForm(StudentRegistrationForm):
    submit = SubmitField("Register as participant")


class VolunteerRegistrationForm(StudentRegistrationForm):
    volunteer_role = SelectField(
        "Preferred volunteer role",
        choices=[
            ("", "Choose a role"),
            ("Event Management", "Event Management"),
            ("Ground Support", "Ground Support"),
            ("Registration Desk", "Registration Desk"),
            ("Technical Support", "Technical Support"),
            ("Photography", "Photography"),
            ("Other", "Other"),
        ],
        validators=[DataRequired(message="Choose a preferred volunteer role.")],
    )
    submit = SubmitField("Register as volunteer")

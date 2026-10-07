"""Sports Registration Flask application.

Run locally with ``python app.py``. The database tables are created automatically
on first start; existing SQLite databases receive the homepage-theme column on
startup. Use ``python init_db.py`` to add the three demo events.
"""

import os
from datetime import timedelta

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash

from config import Config
from extensions import csrf, db


def _ensure_event_background_theme_column():
    """Add the new optional UI setting to existing local SQLite databases."""
    if db.engine.dialect.name != "sqlite":
        return

    inspector = inspect(db.engine)
    if not inspector.has_table("events"):
        return

    event_columns = {column["name"] for column in inspector.get_columns("events")}
    if "background_theme" not in event_columns:
        with db.engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE events "
                    "ADD COLUMN background_theme VARCHAR(24) NOT NULL DEFAULT 'auto'"
                )
            )


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    # In the Arena demonstration only, remove browser-session friction so the
    # presentation can show the complete flow inside its embedded preview.
    # Local/default installs retain admin authentication and CSRF protection.
    if app.config.get("DEMO_MODE"):
        app.config["WTF_CSRF_ENABLED"] = False

    os.makedirs(app.instance_path, exist_ok=True)

    # Admin passwords are verified as hashes. A pre-hashed value can be supplied
    # with ADMIN_PASSWORD_HASH; otherwise the local ADMIN_PASSWORD is hashed here.
    if not app.config.get("ADMIN_PASSWORD_HASH"):
        app.config["ADMIN_PASSWORD_HASH"] = generate_password_hash(
            app.config.get("ADMIN_PASSWORD", "change-me")
        )

    app.permanent_session_lifetime = timedelta(hours=8)
    db.init_app(app)
    csrf.init_app(app)

    # Import models before create_all so SQLAlchemy has registered the tables.
    from models.models import Event, Registration  # noqa: F401
    from routes.admin import admin_bp
    from routes.events import events_bp
    from routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(400)
    def bad_request(_error):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        # Keep the browser-facing message friendly while logging the cause for debugging.
        app.logger.warning("CSRF validation failed: %s", error.description)
        return render_template("errors/400.html"), 400

    with app.app_context():
        db.create_all()
        _ensure_event_background_theme_column()

    return app


app = create_app()


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=debug)

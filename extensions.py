"""Shared Flask extensions and SQLite connection settings."""

import sqlite3

from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import event as sqlalchemy_event
from sqlalchemy.engine import Engine


db = SQLAlchemy()
csrf = CSRFProtect()


@sqlalchemy_event.listens_for(Engine, "connect")
def _enable_sqlite_foreign_keys(connection, _connection_record):
    """SQLite disables foreign-key enforcement by default; enable it per connection."""
    if isinstance(connection, sqlite3.Connection):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

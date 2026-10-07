"""Application configuration for the local Sports Registration MVP."""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-secret-key")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    # ADMIN_PASSWORD is used only as a simple local setup value. create_app hashes
    # it in memory; it is never saved to the database. You can instead provide
    # ADMIN_PASSWORD_HASH for a pre-hashed password.
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me")
    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
    # Default off. Enable only for a supervised presentation preview.
    DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() in {"1", "true", "yes"}

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{(BASE_DIR / 'instance' / 'sports_registration.db').as_posix()}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"check_same_thread": False, "timeout": 15}
    }

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = os.getenv("WTF_CSRF_SSL_STRICT", "true").lower() in {
        "1", "true", "yes"
    }
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() in {
        "1", "true", "yes"
    }
    # Flask 3.1+: permits the signed session cookie inside Arena's cross-site preview iframe.
    SESSION_COOKIE_PARTITIONED = os.getenv("SESSION_COOKIE_PARTITIONED", "false").lower() in {
        "1", "true", "yes"
    }

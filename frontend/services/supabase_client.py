import os
import logging
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from supabase import Client, create_client


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logger = logging.getLogger("ats_resume_scorer")


# ---------------------------------------------------------
# Environment configuration
# ---------------------------------------------------------

try:
    from dotenv import load_dotenv

    load_dotenv(
        Path(__file__).resolve().parents[2] / ".env"
    )
except ImportError:
    pass


def _secret(key: str, section: str = "supabase") -> str:
    """
    Read a configuration value from environment variables first.
    If not available, fall back to Streamlit secrets.
    """

    value = os.getenv(key, "")

    if value:
        return value

    try:
        return st.secrets[section][key]
    except (KeyError, FileNotFoundError, AttributeError):
        return ""


SUPABASE_URL = _secret("SUPABASE_URL")
SUPABASE_ANON_KEY = _secret("SUPABASE_ANON_KEY")


# ---------------------------------------------------------
# OAuth configuration
# ---------------------------------------------------------

OAUTH_REDIRECT_URL = (
    os.getenv("AUTH_REDIRECT_URL")
    or _secret("redirect_uri", "google_oauth")
    or "http://localhost:8501"
)


# ---------------------------------------------------------
# Configuration validation
# ---------------------------------------------------------

def _missing_config() -> str | None:
    """Return a configuration error if Supabase is not configured."""

    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        return (
            "Supabase is not configured — set "
            "SUPABASE_URL and SUPABASE_ANON_KEY "
            "in .env or .streamlit/secrets.toml"
        )

    return None


# ---------------------------------------------------------
# Supabase client
# ---------------------------------------------------------

@st.cache_resource
def get_client() -> Client | None:
    """
    Return the cached Supabase client.

    Streamlit caches this client so authentication state
    and the PKCE flow remain consistent across reruns.
    """

    if _missing_config():
        return None

    return create_client(
        SUPABASE_URL,
        SUPABASE_ANON_KEY,
    )


# ---------------------------------------------------------
# Session helper
# ---------------------------------------------------------

def _session_dict(session, user) -> Dict[str, Any]:
    """
    Convert a Supabase session and user into the application's
    internal authentication dictionary.
    """

    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "user_id": user.id,
        "email": user.email,
    }


# ---------------------------------------------------------
# Email/password sign in
# ---------------------------------------------------------

def sign_in_with_password(
    email: str,
    password: str,
) -> Dict[str, Any]:
    """Sign in an existing user with email and password."""

    error = _missing_config()

    if error:
        return {"error": error}

    client = get_client()

    if client is None:
        return {
            "error": "Supabase client could not be initialized"
        }

    try:
        response = client.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

        if not response.session or not response.user:
            return {
                "error": "Invalid credentials"
            }

        return _session_dict(
            response.session,
            response.user,
        )

    except Exception as exc:
        logger.warning(
            "Password sign-in failed: %s",
            exc,
        )

        return {
            "error": _humanize(exc)
        }


# ---------------------------------------------------------
# Email/password sign up
# ---------------------------------------------------------

def sign_up_with_password(
    email: str,
    password: str,
) -> Dict[str, Any]:
    """Create a new user with email and password."""

    error = _missing_config()

    if error:
        return {"error": error}

    client = get_client()

    if client is None:
        return {
            "error": "Supabase client could not be initialized"
        }

    try:
        response = client.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

        # User has been created and a session is immediately available.
        if response.session and response.user:
            return _session_dict(
                response.session,
                response.user,
            )

        # User was created but email confirmation is required.
        if response.user:
            return {
                "pending_confirmation": True,
                "email": email,
            }

        return {
            "error": "Sign-up failed"
        }

    except Exception as exc:
        logger.warning(
            "Sign-up failed: %s",
            exc,
        )

        return {
            "error": _humanize(exc)
        }


# ---------------------------------------------------------
# Google OAuth
# ---------------------------------------------------------

def google_oauth_url() -> Dict[str, Any]:
    """
    Generate the Google OAuth authorization URL.
    """

    error = _missing_config()

    if error:
        return {"error": error}

    client = get_client()

    if client is None:
        return {
            "error": "Supabase client could not be initialized"
        }

    try:
        response = client.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {
                    "redirect_to": OAUTH_REDIRECT_URL,
                },
            }
        )

        return {
            "url": response.url
        }

    except Exception as exc:
        logger.warning(
            "OAuth URL generation failed: %s",
            exc,
        )

        return {
            "error": _humanize(exc)
        }


# ---------------------------------------------------------
# OAuth PKCE code exchange
# ---------------------------------------------------------

def exchange_code_for_session(
    auth_code: str,
) -> Dict[str, Any]:
    """
    Exchange the OAuth PKCE authorization code for
    a Supabase session.
    """

    error = _missing_config()

    if error:
        return {"error": error}

    client = get_client()

    if client is None:
        return {
            "error": "Supabase client could not be initialized"
        }

    try:
        response = client.auth.exchange_code_for_session(
            {
                "auth_code": auth_code,
            }
        )

        if not response.session or not response.user:
            return {
                "error": "OAuth exchange returned no session"
            }

        return _session_dict(
            response.session,
            response.user,
        )

    except Exception as exc:
        logger.warning(
            "OAuth code exchange failed: %s",
            exc,
        )

        return {
            "error": _humanize(exc)
        }


# ---------------------------------------------------------
# Sign out
# ---------------------------------------------------------

def sign_out() -> None:
    """Sign out the current Supabase user."""

    if _missing_config():
        return

    client = get_client()

    if client is None:
        return

    try:
        client.auth.sign_out()

    except Exception as exc:
        logger.warning(
            "Sign-out failed: %s",
            exc,
        )


# ---------------------------------------------------------
# User-friendly error messages
# ---------------------------------------------------------

def _humanize(exc: Exception) -> str:
    """
    Convert common Supabase authentication errors into
    user-friendly messages.
    """

    message = str(exc)
    lower_message = message.lower()

    if (
        "invalid_grant" in lower_message
        or "invalid login" in lower_message
    ):
        return "Wrong email or password"

    if (
        "user already registered" in lower_message
        or "already been registered" in lower_message
    ):
        return (
            "An account with this email already exists — "
            "try signing in"
        )

    if "password should be at least" in lower_message:
        return (
            "Password too short "
            "(Supabase default is 6 characters)"
        )

    return message
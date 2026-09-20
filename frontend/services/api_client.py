from typing import Any, Dict, List

import requests
import streamlit as st


# ============================================================
# DEFAULT LOCAL BACKEND
# ============================================================

DEFAULT_BACKEND_URL = "http://localhost:8000"


# ============================================================
# BACKEND URL
# ============================================================

def _backend_url() -> str:
    """
    Get the backend URL from Streamlit Secrets.

    Local development:
        http://localhost:8000

    Streamlit Cloud:
        Cloud Run HTTPS URL stored in:
        [backend]
        url = "https://your-cloud-run-service-url"
    """

    try:
        backend_url = st.secrets["backend"]["url"]

        if backend_url:
            return str(backend_url).rstrip("/")

    except (KeyError, FileNotFoundError):
        pass

    return DEFAULT_BACKEND_URL.rstrip("/")


# ============================================================
# AUTHENTICATION
# ============================================================

def _auth_headers(access_token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {access_token}"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

def health_check() -> Dict[str, Any]:
    response = requests.get(
        f"{_backend_url()}/api/v1/health",
        timeout=15,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# RESUME ANALYSIS
# ============================================================

def analyze_resume(
    resume_file,
    access_token: str,
    job_description: str = "",
) -> Dict[str, Any]:

    files = {
        "resume": (
            resume_file.name,
            resume_file.getvalue(),
            resume_file.type,
        )
    }

    data = {
        "job_description": job_description
    }

    response = requests.post(
        f"{_backend_url()}/api/v1/analyze-resume",
        files=files,
        data=data,
        headers=_auth_headers(access_token),

        # Cloud Run can have a cold start and the analysis
        # includes Groq + spaCy + scoring + Supabase.
        timeout=300,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# HISTORY
# ============================================================

def get_history(
    access_token: str,
) -> List[Dict[str, Any]]:

    response = requests.get(
        f"{_backend_url()}/api/v1/history",
        headers=_auth_headers(access_token),
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# DELETE HISTORY ENTRY
# ============================================================

def delete_history_entry(
    analysis_id: str,
    access_token: str,
) -> None:

    response = requests.delete(
        f"{_backend_url()}/api/v1/history/{analysis_id}",
        headers=_auth_headers(access_token),
        timeout=30,
    )

    response.raise_for_status()


# ============================================================
# GENERATE PDF
# ============================================================

def generate_pdf(
    analysis_data: Dict[str, Any],
    access_token: str,
) -> bytes:

    response = requests.post(
        f"{_backend_url()}/api/v1/generate-pdf",
        json=analysis_data,
        headers=_auth_headers(access_token),
        timeout=120,
    )

    response.raise_for_status()

    return response.content


# ============================================================
# HISTORY PDF
# ============================================================

def get_history_pdf(
    analysis_id: str,
    access_token: str,
) -> bytes:

    response = requests.get(
        f"{_backend_url()}/api/v1/history/{analysis_id}/pdf",
        headers=_auth_headers(access_token),
        timeout=120,
    )

    response.raise_for_status()

    return response.content
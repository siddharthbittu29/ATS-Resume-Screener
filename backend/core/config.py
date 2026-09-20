import os
from pathlib import Path


# Load .env from the project root explicitly.
try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(_ENV_PATH)

except ImportError:
    pass


# ============================================================
# API METADATA
# ============================================================

APP_TITLE = "ATS RESUME ANALYZER API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "analyse resumes against job description using nlp + ml"


# ============================================================
# CORS
# ============================================================

ALLOWED_ORIGINS = [
    # Streamlit Cloud frontend
    "https://ats-resume-screener-siddharth.streamlit.app",

    # Local development
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]


# ============================================================
# FILE UPLOAD LIMITS
# ============================================================

MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# ============================================================
# SUPPORTED FILE TYPES
# ============================================================

SUPPORTED_MIME_TYPES = {
    "application/pdf": "pdf",
    "application/msword": "doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}

SUPPORTED_EXTENSIONS = {".pdf", ".doc", ".docx"}


# ============================================================
# NLP MODEL
# ============================================================

SPACY_MODEL_PRIMARY = "en_core_web_sm"
SPACY_MODEL_SECONDARY = "en_core_web_sm"


# ============================================================
# SCORE COMPONENT WEIGHTS
# ============================================================

SCORE_WEIGHTS = {
    "formatting": 20,
    "keywords": 25,
    "content": 25,
    "skill_validation": 15,
    "ats_compatibility": 15,
}


# ============================================================
# JOB DESCRIPTION MATCHING WEIGHTS
# ============================================================

JD_KEYWORD_WEIGHT = 0.6
JD_SEMANTIC_WEIGHT = 0.4


# ============================================================
# SUPABASE
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL", "")

SUPABASE_KEY = os.getenv(
    "SUPABASE_KEY",
    "",
)  # service_role — DB writes

SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY",
    "",
)  # public anon — frontend auth calls

SUPABASE_JWT_SECRET = os.getenv(
    "SUPABASE_JWT_SECRET",
    "",
)  # used by backend to verify access tokens


# ============================================================
# GROQ
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
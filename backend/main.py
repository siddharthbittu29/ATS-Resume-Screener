import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import (
    ALLOWED_ORIGINS,
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    SPACY_MODEL_PRIMARY,
    SPACY_MODEL_SECONDARY,
)
from backend.api.routes import router


logger = logging.getLogger("ats_resume_scorer")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ATS Resume Analyzer API...")

    # Load spaCy NLP model only.
    # SentenceTransformer / PyTorch has been removed.
    logger.info(
        f"Loading spaCy NLP model: {SPACY_MODEL_PRIMARY}"
    )

    import spacy

    try:
        app.state.nlp = spacy.load(
            SPACY_MODEL_PRIMARY
        )
        logger.info(
            f"Loaded {SPACY_MODEL_PRIMARY}"
        )

    except OSError:
        logger.warning(
            f"{SPACY_MODEL_PRIMARY} not found — "
            f"falling back to {SPACY_MODEL_SECONDARY}"
        )

        app.state.nlp = spacy.load(
            SPACY_MODEL_SECONDARY
        )

        logger.info(
            f"Loaded {SPACY_MODEL_SECONDARY} (fallback)"
        )

    logger.info(
        "All required models loaded. "
        "API is ready to serve requests."
    )

    yield

    logger.info(
        "Shutting down the API..."
    )


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "ATS Resume Analyzer API",
        "version": "2.0.0",
        "endpoints": {
            "POST /api/v1/analyze-resume": "Analyze a resume",
            "GET /api/v1/history": "Get user history",
            "DELETE /api/v1/history/:id": "Delete a history entry",
            "GET /api/v1/health": "Health check",
            "POST /api/v1/generate-pdf": "Generate PDF report from data",
        },
    }


if __name__ == "__main__":
    import uvicorn

    # Cloud Run provides the PORT environment variable.
    # Local development falls back to port 8000.
    port = int(
        os.getenv("PORT", "8000")
    )

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )
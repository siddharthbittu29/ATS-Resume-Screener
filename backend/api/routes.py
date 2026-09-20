import logging
from typing import List

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from fastapi.responses import Response

from backend.api.auth import get_current_user
from backend.models.schemas import (
    AnalysisResponse,
    ComponentScores,
    JDComparison,
    SkillValidationDetails,
)

logger = logging.getLogger("ats_resume_scorer")

router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"],
)


def _clean(text: str) -> str:
    for prefix in ("âœ…", "ðŸŒŸ", "â", "ðŸ“"):
        text = text.lstrip(prefix)

    return text.strip()


@router.post(
    "/analyze-resume",
    response_model=AnalysisResponse,
)
async def analyze_resume(
    request: Request,
    resume: UploadFile = File(
        ...,
        description="Resume file — PDF or DOCX, max 5 MB",
    ),
    job_description: str = Form(
        "",
        description="Job description text (optional)",
    ),
    user_id: str = Depends(get_current_user),
):
    warnings: List[str] = []

    nlp = request.app.state.nlp

    # ========================================================
    # Parse resume
    # ========================================================

    try:
        file_bytes = await resume.read()
        filename = resume.filename or "resume"

        from backend.services.resume_parser import parse_resume_file

        resume_text, _metadata = parse_resume_file(
            file_bytes,
            filename,
        )

        logger.info(
            f"Parsed '{filename}': {len(resume_text)} chars extracted"
        )

    except Exception as exc:
        logger.error(f"File parsing failed: {exc}")

        raise HTTPException(
            status_code=422,
            detail=(
                "Could not read or parse the resume. "
                "Please check that the file is a valid PDF or DOCX."
            ),
        )

    # ========================================================
    # Full analysis pipeline
    # ========================================================

    try:
        from backend.services.resume_analyzer import analyze_full_resume

        result = analyze_full_resume(
            resume_text=resume_text,
            nlp=nlp,
            job_description=job_description,
        )

    except Exception as exc:
        logger.error(
            f"Full analysis pipeline failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Analysis failed due to an internal server error. "
                "Please try again."
            ),
        )

    # ========================================================
    # JD comparison
    # ========================================================

    jd_comparison_result = None

    if result.get("jd_comparison"):
        jd_comparison_result = JDComparison(
            match_percentage=round(
                float(
                    result["jd_comparison"].get(
                        "match_percentage",
                        0.0,
                    )
                ),
                1,
            ),
            semantic_similarity=round(
                float(
                    result["jd_comparison"].get(
                        "semantic_similarity",
                        0.0,
                    )
                ),
                3,
            ),
            matched_keywords=result["jd_comparison"].get(
                "matched_keywords",
                [],
            )[:20],
            missing_keywords=result["jd_comparison"].get(
                "missing_keywords",
                [],
            )[:15],
            skills_gap=result["jd_comparison"].get(
                "skills_gap",
                [],
            )[:10],
        )

    # ========================================================
    # Detailed feedback
    # ========================================================

    detailed_fb = result.get(
        "detailed_feedback",
        [],
    )

    # ========================================================
    # Skill validation
    # ========================================================

    svd_raw = result.get(
        "skill_validation_details"
    ) or {}

    skill_val_details = SkillValidationDetails(
        validated=svd_raw.get(
            "validated",
            [],
        ),
        unvalidated=svd_raw.get(
            "unvalidated",
            [],
        ),
        total=svd_raw.get(
            "total",
            0,
        ),
        validated_count=svd_raw.get(
            "validated_count",
            0,
        ),
        validation_pct=svd_raw.get(
            "validation_pct",
            0.0,
        ),
    )

    # ========================================================
    # API response
    # ========================================================

    response = AnalysisResponse(
        # Both fields are required by AnalysisResponse.
        ATS_score=result["ats_score"],
        ats_score=result["ats_score"],

        component_scores=ComponentScores(
            **result["component_scores"]
        ),

        issues_summary=result.get(
            "issues_summary",
            [],
        ),

        detailed_feedback=detailed_fb,

        jd_match_analysis=jd_comparison_result,

        skill_validation_details=skill_val_details,

        keyword_match=(
            jd_comparison_result.match_percentage
            if jd_comparison_result
            else 0.0
        ),

        missing_keywords=result.get(
            "missing_keywords",
            [],
        ),

        matched_keywords=result.get(
            "matched_keywords",
            [],
        ),

        skills=list(
            result.get(
                "skills",
                [],
            )[:20]
        ),

        jd_comparison=jd_comparison_result,

        interpretation=result.get(
            "interpretation",
            "",
        ),
    )

    # ========================================================
    # Save analysis to Supabase
    # ========================================================

    try:
        from backend.database.supabase_db import save_analysis

        await save_analysis(
            user_id,
            filename,
            result,
        )

    except Exception as exc:
        logger.warning(
            f"History save failed (non-blocking): {exc}"
        )

    return response


@router.get("/health")
async def health_check(request: Request):
    """Health check — confirms the NLP model is loaded."""

    return {
        "status": "healthy",
        "nlp_loaded": request.app.state.nlp is not None,
        "semantic_matching": "rapidfuzz",
    }


@router.get("/history")
async def get_history(
    user_id: str = Depends(get_current_user),
):
    """Return the signed-in user's past analyses."""

    from backend.database.supabase_db import get_user_history

    try:
        return await get_user_history(user_id)

    except Exception as exc:
        logger.error(
            f"History fetch failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not load analysis history. "
                "Please try again."
            ),
        )


@router.delete("/history/{analysis_id}")
async def delete_history_entry(
    analysis_id: str,
    user_id: str = Depends(get_current_user),
):
    """Delete one analysis from the signed-in user's history."""

    from backend.database.supabase_db import delete_analysis

    try:
        success = await delete_analysis(
            analysis_id,
            user_id,
        )

        if not success:
            raise HTTPException(
                status_code=404,
                detail=(
                    "Analysis not found or not owned by this user."
                ),
            )

        return {
            "status": "deleted",
            "id": analysis_id,
        }

    except HTTPException:
        raise

    except Exception as exc:
        logger.error(
            f"History delete failed: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not delete the analysis. "
                "Please try again."
            ),
        )


@router.post("/generate-pdf")
async def generate_pdf(
    data: AnalysisResponse,
    user_id: str = Depends(get_current_user),
):
    from backend.services.report_generator import (
        generate_html_reports,
    )
    from backend.services.pdf_export import (
        generate_combined_pdf,
    )

    try:
        html_docs = generate_html_reports(
            data.model_dump()
        )

        pdf_bytes = generate_combined_pdf(
            html_docs
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    "attachment; filename=ats_report.pdf"
                )
            },
        )

    except Exception as exc:
        logger.error(
            f"Failed to generate PDF: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate the PDF report. "
                "Please try again."
            ),
        )


@router.get("/history/{analysis_id}/pdf")
async def generate_history_pdf(
    analysis_id: str,
    user_id: str = Depends(get_current_user),
):
    from backend.database.supabase_db import get_user_history
    from backend.services.report_generator import (
        generate_html_reports,
    )
    from backend.services.pdf_export import (
        generate_combined_pdf,
    )

    history = await get_user_history(user_id)

    analysis_data = next(
        (
            item["analysis_result"]
            for item in history
            if item["id"] == analysis_id
        ),
        None,
    )

    if not analysis_data:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )

    try:
        html_docs = generate_html_reports(
            analysis_data
        )

        pdf_bytes = generate_combined_pdf(
            html_docs
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f"attachment; "
                    f"filename=ats_report_{analysis_id}.pdf"
                )
            },
        )

    except Exception as exc:
        logger.error(
            f"Failed to generate PDF for history: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate the history PDF. "
                "Please try again."
            ),
        )
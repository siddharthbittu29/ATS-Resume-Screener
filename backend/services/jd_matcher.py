from typing import List, Dict

import spacy
from rapidfuzz import fuzz

from backend.utils.matching import (
    fuzzy_match_keywords,
    normalize_skill,
)


# ============================================================
# LIGHTWEIGHT SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    resume_text: str,
    jd_text: str,
    embedder=None,
) -> float:
    """
    Lightweight resume-to-job-description similarity.

    Previously this function used SentenceTransformer/PyTorch.
    It now uses RapidFuzz so the backend can run within
    low-memory deployment environments such as Render Free.
    """

    if not resume_text or not jd_text:
        return 0.0

    try:
        resume_sample = resume_text[:5000]
        jd_sample = jd_text[:5000]

        # token_set_ratio is useful for comparing documents
        # containing overlapping technical terminology.
        similarity = fuzz.token_set_ratio(
            resume_sample,
            jd_sample,
        ) / 100.0

        return float(
            max(
                0.0,
                min(1.0, similarity)
            )
        )

    except Exception:
        return 0.0


# ============================================================
# MATCHED KEYWORDS
# ============================================================

def identify_matched_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
) -> List[str]:

    result = fuzzy_match_keywords(
        resume_keywords,
        jd_keywords,
        threshold=80,
    )

    return result['matched']


# ============================================================
# MISSING KEYWORDS
# ============================================================

def identify_missing_keywords(
    resume_keywords: List[str],
    jd_keywords: List[str],
    top_n: int = 15,
) -> List[str]:

    result = fuzzy_match_keywords(
        resume_keywords,
        jd_keywords,
        threshold=80,
    )

    return result['missing'][:top_n]


# ============================================================
# SKILLS GAP ANALYSIS
# ============================================================

def analyze_skills_gap(
    resume_skills: List[str],
    jd_text: str,
    nlp: spacy.Language,
) -> List[str]:

    doc = nlp(
        jd_text[:5000]
    )

    jd_skills = set()

    # Extract entities that may represent technologies,
    # organizations, programming languages, products, etc.
    for ent in doc.ents:

        if ent.label_ in [
            'PRODUCT',
            'ORG',
            'LANGUAGE',
        ]:

            jd_skills.add(
                ent.text.lower()
            )

    # Extract noun phrases as additional skill candidates.
    for chunk in doc.noun_chunks:

        ct = chunk.text.lower().strip()

        if 1 <= len(ct.split()) <= 4:
            jd_skills.add(ct)

    # Normalize resume skills for comparison.
    resume_normalized = {
        normalize_skill(skill)
        for skill in resume_skills
    }

    gap = []

    for jd_skill in jd_skills:

        jd_norm = normalize_skill(
            jd_skill
        )

        # Canonical match first.
        if jd_norm in resume_normalized:
            continue

        # Fuzzy comparison against resume skills.
        best_score = max(
            (
                fuzz.token_sort_ratio(
                    jd_norm,
                    resume_skill
                )
                for resume_skill
                in resume_normalized
            ),
            default=0,
        )

        if best_score < 75:
            gap.append(jd_skill)

    return sorted(gap)[:20]


# ============================================================
# MATCH PERCENTAGE
# ============================================================

def calculate_match_percentage(
    resume_keywords: List[str],
    jd_keywords: List[str],
    semantic_similarity: float,
) -> float:

    if not jd_keywords:
        return 0.0

    matched = identify_matched_keywords(
        resume_keywords,
        jd_keywords,
    )

    keyword_overlap = (
        len(matched)
        / len(jd_keywords)
    )

    # Preserve the original weighting:
    # 60% keyword overlap
    # 40% semantic similarity
    match_pct = (
        keyword_overlap * 0.6
        +
        semantic_similarity * 0.4
    ) * 100

    return float(
        max(
            0.0,
            min(100.0, match_pct)
        )
    )


# ============================================================
# RESUME vs JOB DESCRIPTION
# ============================================================

def compare_resume_with_jd(
    resume_text: str,
    resume_keywords: List[str],
    resume_skills: List[str],
    jd_text: str,
    jd_keywords: List[str],
    embedder=None,
    nlp: spacy.Language = None,
) -> Dict:

    semantic_similarity = (
        calculate_semantic_similarity(
            resume_text,
            jd_text,
            embedder,
        )
    )

    matched_keywords = (
        identify_matched_keywords(
            resume_keywords,
            jd_keywords,
        )
    )

    missing_keywords = (
        identify_missing_keywords(
            resume_keywords,
            jd_keywords,
        )
    )

    skills_gap = (
        analyze_skills_gap(
            resume_skills,
            jd_text,
            nlp,
        )
        if nlp is not None
        else []
    )

    match_percentage = (
        calculate_match_percentage(
            resume_keywords,
            jd_keywords,
            semantic_similarity,
        )
    )

    return {
        'match_percentage': match_percentage,
        'semantic_similarity': semantic_similarity,
        'matched_keywords': matched_keywords,
        'missing_keywords': missing_keywords,
        'skills_gap': skills_gap,
    }
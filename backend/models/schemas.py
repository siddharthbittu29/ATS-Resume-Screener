from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ComponentScores(BaseModel):
    formatting: float
    keywords: float
    content: float
    skill_validation: float
    ats_compatibility: float


class JDComparison(BaseModel):
    match_percentage: float
    semantic_similarity: float
    matched_keywords: List[str]
    missing_keywords: List[str]
    skills_gap: List[str]


class SkillValidationDetails(BaseModel):
    validated: List[Dict[str, Any]] = Field(default_factory=list)
    unvalidated: List[str] = Field(default_factory=list)
    total: int = 0
    validated_count: int = 0
    validation_pct: float = 0.0


class IssueDetail(BaseModel):
    issue_title: str
    severity_level: str
    ats_impact: str
    explanation: str
    where_it_appears: str
    how_to_fix: str
    action_items: List[str] = Field(default_factory=list)
    example_improvement: str


class AnalysisResponse(BaseModel):
    # Main ATS score
    ATS_score: float

    # Lowercase compatibility field used by the current frontend/API
    ats_score: float

    # Score breakdown
    component_scores: ComponentScores

    # Analysis feedback
    issues_summary: List[str]
    detailed_feedback: List[IssueDetail]

    # Job description comparison
    jd_match_analysis: Optional[JDComparison] = None

    # Skill validation
    skill_validation_details: Optional[SkillValidationDetails] = None

    # Backward-compatible fields
    keyword_match: float = 0.0
    missing_keywords: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    critical_issues: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    jd_comparison: Optional[JDComparison] = None
    warnings: List[str] = Field(default_factory=list)
    interpretation: str = ""
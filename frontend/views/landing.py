import streamlit as st


def render():

    # ── Scoped styles ────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* Hero */
    .hero {
        background: linear-gradient(135deg, #1e1c1a 0%, #3a3834 100%);
        border-radius: 14px;
        padding: 3.5rem 2.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
        border: 0.5px solid #3a3834;
    }
    .hero-eyebrow {
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #a8a49a;
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #fafaf9;
        line-height: 1.15;
        margin-bottom: 0.875rem;
    }
    .hero-sub {
        font-size: 1.0625rem;
        color: #7a7670;
        max-width: 520px;
        margin: 0 auto 2rem;
        line-height: 1.6;
    }

    /* Feature cards */
    .feat-card {
        background: #ffffff;
        border: 0.5px solid #e8e6e0;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
    }
    .feat-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.125rem;
        margin-bottom: 1rem;
    }
    .feat-icon-blue   { background: #eff6ff; }
    .feat-icon-green  { background: #f0fdf4; }
    .feat-icon-violet { background: #f5f3ff; }
    .feat-title {
        font-size: 0.9375rem;
        font-weight: 500;
        color: #1e1c1a;
        margin-bottom: 0.5rem;
    }
    .feat-body {
        font-size: 0.8125rem;
        color: #7a7670;
        line-height: 1.6;
    }
    .feat-list {
        margin: 0.625rem 0 0;
        padding-left: 1rem;
        font-size: 0.8125rem;
        color: #58554f;
        line-height: 1.8;
    }

    /* Step indicator */
    .steps-row {
        display: flex;
        gap: 0;
        align-items: flex-start;
    }
    .step-item {
        flex: 1;
        text-align: center;
        position: relative;
    }
    .step-item:not(:last-child)::after {
        content: '';
        position: absolute;
        top: 20px;
        left: calc(50% + 22px);
        right: calc(-50% + 22px);
        height: 1px;
        background: #e8e6e0;
    }
    .step-num {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #1e1c1a;
        color: #fafaf9;
        font-size: 0.875rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 0.875rem;
    }
    .step-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: #1e1c1a;
        margin-bottom: 0.375rem;
    }
    .step-desc {
        font-size: 0.8125rem;
        color: #7a7670;
        line-height: 1.5;
        max-width: 180px;
        margin: 0 auto;
    }

    /* Stats strip */
    .stats-strip {
        display: flex;
        gap: 0;
        background: #ffffff;
        border: 0.5px solid #e8e6e0;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 2.5rem;
    }
    .stat-item {
        flex: 1;
        padding: 1.25rem 1rem;
        text-align: center;
        border-right: 0.5px solid #e8e6e0;
    }
    .stat-item:last-child { border-right: none; }
    .stat-num {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e1c1a;
        line-height: 1;
    }
    .stat-lbl {
        font-size: 0.75rem;
        color: #7a7670;
        margin-top: 0.25rem;
    }

    /* Section label */
    .sec-eyebrow {
        font-size: 0.6875rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #a8a49a;
        margin-bottom: 0.375rem;
    }
    .sec-heading {
        font-size: 1.375rem;
        font-weight: 500;
        color: #1e1c1a;
        margin-bottom: 1.5rem;
    }

    /* CTA button override — make Streamlit primary button look sharp */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #1e1c1a !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        padding: 0.625rem 1.5rem !important;
        font-size: 0.9375rem !important;
        color: #fafaf9 !important;
        transition: opacity 0.15s !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        opacity: 0.85 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">AI-powered resume analysis</div>
        <div class="hero-title">Score your resume before<br>the recruiter does</div>
        <div class="hero-sub">
            Instant ATS compatibility feedback across formatting, keywords,
            skill validation, and content quality — so you know exactly what to fix.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA button — must be a real Streamlit widget, not HTML
    col_l, col_c, col_r = st.columns([1.5, 2, 1.5])
    with col_c:
        if st.button("Analyze my resume", use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer"
            st.rerun()

    st.markdown("<div style='margin-bottom:2.5rem'></div>", unsafe_allow_html=True)

    # ── Stats strip ───────────────────────────────────────────────────────────
    st.markdown("""
    <div class="stats-strip">
        <div class="stat-item">
            <div class="stat-num">5</div>
            <div class="stat-lbl">Scoring dimensions</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">AI</div>
            <div class="stat-lbl">Semantic analysis</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">PDF</div>
            <div class="stat-lbl">DOC · DOCX support</div>
        </div>
        <div class="stat-item">
            <div class="stat-num">100%</div>
            <div class="stat-lbl">Private & local</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Features ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">What you get</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Everything you need to pass ATS</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon feat-icon-blue">📊</div>
            <div class="feat-title">Comprehensive scoring</div>
            <div class="feat-body">
                Detailed breakdown across five weighted dimensions so you know exactly where you stand.
            </div>
            <ul class="feat-list">
                <li>Formatting — 20%</li>
                <li>Keywords &amp; skills — 25%</li>
                <li>Content quality — 25%</li>
                <li>Skill validation — 15%</li>
                <li>ATS compatibility — 15%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon feat-icon-green">🔍</div>
            <div class="feat-title">Skill validation</div>
            <div class="feat-body">
                AI cross-checks every skill you claim against your actual project and work descriptions.
                No more empty keyword stuffing.
            </div>
            <ul class="feat-list">
                <li>Semantic similarity matching</li>
                <li>Evidence-backed results</li>
                <li>Flags unsubstantiated claims</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon feat-icon-violet">🔒</div>
            <div class="feat-title">Privacy first</div>
            <div class="feat-body">
                All analysis runs locally. Your resume never leaves your machine —
                no third-party API calls, no data retention.
            </div>
            <ul class="feat-list">
                <li>Fully offline analysis</li>
                <li>No cloud storage</li>
                <li>Zero data sharing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:2.5rem'></div>", unsafe_allow_html=True)

    # ── How it works ──────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">Process</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-heading">Three steps to a stronger resume</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="steps-row">
        <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-title">Upload your resume</div>
            <div class="step-desc">PDF, DOC, or DOCX — drop it in and you're ready.</div>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-title">AI analysis</div>
            <div class="step-desc">Local models score formatting, keywords, skills, and content.</div>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-title">Act on feedback</div>
            <div class="step-desc">Prioritised recommendations ranked by impact on your score.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:3rem'></div>", unsafe_allow_html=True)

    # ── Bottom CTA ────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        background: #f4f3f0;
        border: 0.5px solid #e8e6e0;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    ">
        <div style="font-size:1.125rem; font-weight:500; color:#1e1c1a; margin-bottom:0.5rem;">
            Ready to find out your score?
        </div>
        <div style="font-size:0.875rem; color:#7a7670; margin-bottom:1.25rem;">
            Takes less than 30 seconds. No account required to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l2, col_c2, col_r2 = st.columns([1.5, 2, 1.5])
    with col_c2:
        if st.button("Get my ATS score", use_container_width=True, type="primary", key="cta_bottom"):
            st.session_state.current_view = "scorer"
            st.rerun()
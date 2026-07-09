import streamlit as st
from utils.prediction import (
    predict_score,
    calculate_grade,
    get_suggestions,
    performance_analysis
)

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    footer, #MainMenu, header { visibility: hidden; }

    /* ── Background ─────────────────────────────── */
    .stApp {
        background: linear-gradient(160deg, #0e0e18 0%, #131320 50%, #0f1118 100%);
    }

    /* ══════════════════════════════════════════════
       COLOR PALETTE (muted multi-color)
       Blue    : #6c83ff / #4a5ee0
       Purple  : #a78bfa / #8b6ce0
       Teal    : #5eead4 / #2dd4a8
       Rose    : #f472b6 / #e0559e
       Amber   : #fbbf24 / #e0a820
       Sky     : #67d4e8 / #4ab8d0
       Orange  : #fb923c / #e07830
    ══════════════════════════════════════════════ */

    /* ── Hero Banner ────────────────────────────── */
    .hero-banner {
        background: linear-gradient(145deg, #181830, #1e1e38);
        border: 1px solid rgba(108, 131, 255, 0.1);
        border-radius: 20px;
        padding: 2.8rem 3rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 45px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 3px;
        background: linear-gradient(90deg, #6c83ff, #a78bfa, #f472b6, #fbbf24, #5eead4);
        border-radius: 20px 20px 0 0;
    }
    .hero-banner h1 {
        color: #e8e8f0;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }
    .hero-word-blue {
        background: linear-gradient(135deg, #6c83ff, #8b9aff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-word-purple {
        background: linear-gradient(135deg, #a78bfa, #c4a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-banner p {
        color: #6a6a88;
        font-size: 1.05rem;
    }

    /* ── Stat Pills — each a different color ────── */
    .stat-pill {
        border-radius: 12px;
        padding: 1.15rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.04);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
    }
    .stat-pill:hover { transform: translateY(-2px); }
    .pill-blue   { background: linear-gradient(145deg, #161630, #1a1a38); border-left: 3px solid #6c83ff; }
    .pill-purple { background: linear-gradient(145deg, #1a1630, #201a38); border-left: 3px solid #a78bfa; }
    .pill-teal   { background: linear-gradient(145deg, #141e20, #182428); border-left: 3px solid #5eead4; }
    .pill-rose   { background: linear-gradient(145deg, #1e1420, #241828); border-left: 3px solid #f472b6; }
    .stat-pill .s-value {
        font-size: 1.4rem;
        font-weight: 700;
    }
    .pill-blue .s-value   { color: #6c83ff; }
    .pill-purple .s-value { color: #a78bfa; }
    .pill-teal .s-value   { color: #5eead4; }
    .pill-rose .s-value   { color: #f472b6; }
    .stat-pill .s-label {
        font-size: 0.72rem;
        color: #555570;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-top: 0.2rem;
    }

    /* ── Section Cards ──────────────────────────── */
    .section-card {
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.04);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .card-academic    { background: linear-gradient(145deg, #161630, #1c1c38); border-top: 2px solid #6c83ff; }
    .card-environment { background: linear-gradient(145deg, #1a1628, #201a32); border-top: 2px solid #a78bfa; }
    .card-personal    { background: linear-gradient(145deg, #141e22, #18242c); border-top: 2px solid #5eead4; }

    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .section-icon {
        width: 40px; height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .icon-blue   { background: linear-gradient(135deg, #1e2050, #282870); }
    .icon-purple { background: linear-gradient(135deg, #281e50, #342870); }
    .icon-teal   { background: linear-gradient(135deg, #1a3038, #203840); }
    .section-title {
        color: #c8c8dd;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0;
    }
    .section-subtitle {
        color: #555570;
        font-size: 0.78rem;
        margin: 0;
    }

    /* ── Inputs ──────────────────────────────────── */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        background-color: #151528 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        color: #c0c0d8 !important;
        font-weight: 500 !important;
    }
    .stSlider > label, .stSelectbox > label, .stNumberInput > label {
        color: #8585a0 !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }

    /* ── Tabs ────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: linear-gradient(145deg, #141428, #181830);
        border-radius: 12px;
        padding: 5px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #606080;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e2050, #282860) !important;
        color: #8b9aff !important;
    }

    /* ── Button ──────────────────────────────────── */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #5a6ee0, #7c5ce0) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 20px rgba(108, 131, 255, 0.2) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button:first-child:hover {
        box-shadow: 0 6px 28px rgba(108, 131, 255, 0.3) !important;
        transform: translateY(-1px);
    }

    /* ── Result Cards — multi-color ─────────────── */
    .result-card {
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.04);
        box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .result-card:hover { transform: translateY(-3px); }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 2px;
    }
    .result-score {
        background: linear-gradient(145deg, #161635, #1c1c40);
    }
    .result-score::before {
        background: linear-gradient(90deg, #6c83ff, #4a5ee0);
    }
    .result-grade {
        background: linear-gradient(145deg, #1e1630, #261a3d);
    }
    .result-grade::before {
        background: linear-gradient(90deg, #a78bfa, #8b6ce0);
    }
    .result-perf {
        background: linear-gradient(145deg, #142020, #182828);
    }
    .result-perf::before {
        background: linear-gradient(90deg, #5eead4, #2dd4a8);
    }
    .result-card .label {
        color: #606080;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.5rem;
    }
    .result-card .value {
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.1;
    }
    .result-score .value { color: #6c83ff; }
    .result-grade .value { color: #a78bfa; }
    .result-perf  .value { color: #5eead4; }
    .result-card .sub {
        color: #454560;
        font-size: 0.76rem;
        margin-top: 0.4rem;
    }

    /* ── Gauge ──────────────────────────────────── */
    .gauge-container {
        display: flex;
        justify-content: center;
        padding: 1.5rem 0;
    }
    .circular-progress {
        position: relative;
        width: 190px; height: 190px;
    }
    .circular-progress svg {
        transform: rotate(-90deg);
    }
    .score-text {
        position: absolute;
        top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
    }
    .score-text .number {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ddddf0;
    }
    .score-text .lbl {
        font-size: 0.72rem;
        color: #555570;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ── Multi-segment Bar ──────────────────────── */
    .bar-wrapper { margin: 0.5rem 0 2rem; }
    .bar-labels {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.4rem;
    }
    .bar-labels span {
        font-size: 0.8rem;
        font-weight: 600;
    }
    .bar-track {
        background: #151528;
        border-radius: 10px;
        height: 22px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
    }
    .bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1.2s ease;
        position: relative;
    }
    /* Color zones behind the bar */
    .bar-zones {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        display: flex;
        opacity: 0.15;
        border-radius: 10px;
        overflow: hidden;
    }
    .zone-red    { flex: 0.5; background: #e87070; }
    .zone-amber  { flex: 0.1; background: #fbbf24; }
    .zone-blue   { flex: 0.15; background: #6c83ff; }
    .zone-teal   { flex: 0.25; background: #5eead4; }

    /* ── Suggestion Cards — rotating colors ────── */
    .sug-card {
        border-radius: 0 10px 10px 0;
        padding: 0.9rem 1.3rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        border-left: 3px solid;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        transition: all 0.2s ease;
    }
    .sug-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .sug-c-blue {
        background: linear-gradient(145deg, #141430, #1a1a38);
        border-color: #6c83ff;
        color: #a0a8d8;
    }
    .sug-c-purple {
        background: linear-gradient(145deg, #1a1430, #201a38);
        border-color: #a78bfa;
        color: #b8a8d8;
    }
    .sug-c-teal {
        background: linear-gradient(145deg, #121e22, #18242c);
        border-color: #5eead4;
        color: #90c8c0;
    }
    .sug-c-rose {
        background: linear-gradient(145deg, #1e1420, #241828);
        border-color: #f472b6;
        color: #c8a0b8;
    }
    .sug-c-amber {
        background: linear-gradient(145deg, #1e1a14, #242018);
        border-color: #fbbf24;
        color: #c8b890;
    }

    /* ── Analysis Box ───────────────────────────── */
    .analysis-box {
        background: linear-gradient(145deg, #151528, #1a1a30);
        border: 1px solid rgba(255,255,255,0.04);
        border-radius: 14px;
        padding: 1.6rem;
        color: #8888a8;
        line-height: 1.75;
        font-size: 0.92rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        border-left: 3px solid #a78bfa;
    }

    /* ── Stats Row ──────────────────────────────── */
    .stats-row {
        display: flex;
        gap: 0.7rem;
        margin: 1.2rem 0;
    }
    .mini-stat {
        flex: 1;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    }
    .ms-blue   { background: linear-gradient(145deg, #141430, #1a1a38); }
    .ms-teal   { background: linear-gradient(145deg, #121e22, #18242c); }
    .ms-rose   { background: linear-gradient(145deg, #1e1420, #241828); }
    .mini-stat .ms-val {
        font-size: 1.3rem;
        font-weight: 700;
    }
    .ms-blue .ms-val { color: #6c83ff; }
    .ms-teal .ms-val { color: #5eead4; }
    .ms-rose .ms-val { color: #f472b6; }
    .mini-stat .ms-lbl {
        font-size: 0.7rem;
        color: #505068;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
    }

    /* ── Divider — multi-color gradient ─────────── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg,
            transparent 0%, #6c83ff33 20%, #a78bfa33 40%,
            #f472b633 60%, #5eead433 80%, transparent 100%);
        margin: 2rem 0;
        border: none;
    }

    /* ── Status banners ─────────────────────────── */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px !important;
    }

    .app-footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #2a2a40;
        font-size: 0.78rem;
    }
    .app-footer .ft-heart { color: #f472b6; }

    /* ── Grade Badge ────────────────────────────── */
    .grade-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    .badge-excellent { background: rgba(94, 234, 212, 0.12); color: #5eead4; }
    .badge-good      { background: rgba(108, 131, 255, 0.12); color: #6c83ff; }
    .badge-average   { background: rgba(251, 191, 36, 0.12);  color: #fbbf24; }
    .badge-low       { background: rgba(232, 112, 112, 0.12); color: #e87070; }
</style>
""", unsafe_allow_html=True)

# ── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🎓 Student <span class="hero-word-blue">Performance</span> <span class="hero-word-purple">Predictor</span></h1>
    <p>Predict exam scores using 19 academic, environmental & personal factors</p>
</div>
""", unsafe_allow_html=True)

# ── Stat Pills ──────────────────────────────────────────────────────────────
p1, p2, p3, p4 = st.columns(4)
with p1:
    st.markdown('<div class="stat-pill pill-blue"><div class="s-value">19</div><div class="s-label">Features</div></div>', unsafe_allow_html=True)
with p2:
    st.markdown('<div class="stat-pill pill-purple"><div class="s-value">ML</div><div class="s-label">Powered</div></div>', unsafe_allow_html=True)
with p3:
    st.markdown('<div class="stat-pill pill-teal"><div class="s-value">95%</div><div class="s-label">Accuracy</div></div>', unsafe_allow_html=True)
with p4:
    st.markdown('<div class="stat-pill pill-rose"><div class="s-value">⚡</div><div class="s-label">Instant</div></div>', unsafe_allow_html=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📚 Academic", "🏫 Environment", "🏃‍♂️ Personal"])

with tab1:
    st.markdown("""
    <div class="section-card card-academic">
        <div class="section-header">
            <div class="section-icon icon-blue">📚</div>
            <div>
                <p class="section-title">Academic Factors</p>
                <p class="section-subtitle">Study habits, scores & learning support</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        hours = st.number_input("📖 Hours Studied (per week)", 1, 45, 20, help="Total weekly study hours")
        attendance = st.slider("📋 Attendance (%)", 60, 100, 80, help="Class attendance rate")
        previous = st.slider("📊 Previous Scores", 50, 100, 75, help="Prior exam average")
    with c2:
        tutoring = st.slider("👨‍🏫 Tutoring Sessions", 0, 8, 1, help="Monthly tutoring sessions")
        motivation = st.selectbox("🔥 Motivation Level", ["Low", "Medium", "High"], index=1)
        learning = st.selectbox("🧠 Learning Disabilities", ["No", "Yes"])

with tab2:
    st.markdown("""
    <div class="section-card card-environment">
        <div class="section-header">
            <div class="section-icon icon-purple">🏫</div>
            <div>
                <p class="section-title">Environment & Support</p>
                <p class="section-subtitle">Family, school & social environment</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        parental = st.selectbox("👨‍👩‍👧 Parental Involvement", ["Low", "Medium", "High"], index=1)
        resources = st.selectbox("📦 Access to Resources", ["Low", "Medium", "High"], index=1)
        internet = st.selectbox("🌐 Internet Access", ["Yes", "No"])
        income = st.selectbox("💰 Family Income", ["Low", "Medium", "High"], index=1)
    with c4:
        teacher = st.selectbox("👩‍🏫 Teacher Quality", ["Low", "Medium", "High"], index=1)
        school = st.selectbox("🏫 School Type", ["Public", "Private"])
        peer = st.selectbox("👥 Peer Influence", ["Negative", "Neutral", "Positive"], index=1)
        distance = st.selectbox("🗺️ Distance From Home", ["Near", "Moderate", "Far"], index=1)

with tab3:
    st.markdown("""
    <div class="section-card card-personal">
        <div class="section-header">
            <div class="section-icon icon-teal">🏃‍♂️</div>
            <div>
                <p class="section-title">Personal Factors</p>
                <p class="section-subtitle">Lifestyle, activities & demographics</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)
    c5, c6 = st.columns(2)
    with c5:
        sleep = st.slider("😴 Sleep Hours", 4, 10, 7, help="Nightly average")
        physical = st.slider("🏋️ Physical Activity (hrs/week)", 0, 6, 3)
        extra = st.selectbox("🎭 Extracurricular Activities", ["No", "Yes"])
    with c6:
        education = st.selectbox("🎓 Parental Education", ["High School", "College", "Postgraduate"], index=1)
        gender = st.selectbox("👤 Gender", ["Male", "Female"])

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ── Predict ─────────────────────────────────────────────────────────────────
if st.button("🚀  Predict Performance", use_container_width=True):

    student = {
        "Hours_Studied": hours, "Attendance": attendance,
        "Parental_Involvement": parental, "Access_to_Resources": resources,
        "Extracurricular_Activities": extra, "Sleep_Hours": sleep,
        "Previous_Scores": previous, "Motivation_Level": motivation,
        "Internet_Access": internet, "Tutoring_Sessions": tutoring,
        "Family_Income": income, "Teacher_Quality": teacher,
        "School_Type": school, "Peer_Influence": peer,
        "Physical_Activity": physical, "Learning_Disabilities": learning,
        "Parental_Education_Level": education, "Distance_from_Home": distance,
        "Gender": gender
    }

    with st.spinner("🔮 Analyzing student profile..."):
        import time; time.sleep(1)
        score = predict_score(student)
        grade = calculate_grade(score)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    capped = min(score, 100)

    # Performance meta
    if grade in ["A+", "A"]:
        perf_label, perf_emoji, badge_cls = "Excellent", "🌟", "badge-excellent"
    elif grade == "B":
        perf_label, perf_emoji, badge_cls = "Good", "👍", "badge-good"
    elif grade == "C":
        perf_label, perf_emoji, badge_cls = "Average", "📚", "badge-average"
    else:
        perf_label, perf_emoji, badge_cls = "Needs Work", "⚠️", "badge-low"

    # ── Results Header ──────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:2rem;">
        <h2 style="color:#d8d8ee; font-weight:800; font-size:1.7rem;">📊 Prediction Results</h2>
        <p style="color:#555570; font-size:0.88rem;">Analysis complete — 19 factors evaluated</p>
        <span class="grade-badge {badge_cls}">{perf_label} Performance</span>
    </div>""", unsafe_allow_html=True)

    # ── Result Cards ────────────────────────────────────────────────────────
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f"""
        <div class="result-card result-score">
            <div class="label">Predicted Score</div>
            <div class="value">{score:.1f}</div>
            <div class="sub">out of 100</div>
        </div>""", unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="result-card result-grade">
            <div class="label">Grade</div>
            <div class="value">{grade}</div>
            <div class="sub">letter grade</div>
        </div>""", unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="result-card result-perf">
            <div class="label">Performance</div>
            <div class="value">{perf_emoji}</div>
            <div class="sub">{perf_label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gauge ───────────────────────────────────────────────────────────────
    pct = min(capped / 100, 1.0)
    circ = 2 * 3.14159 * 75
    dash, gap_val = pct * circ, (1 - pct) * circ

    # Multi-color gauge: 4 stops
    if capped >= 90:   g_clr = "#5eead4"
    elif capped >= 75: g_clr = "#6c83ff"
    elif capped >= 60: g_clr = "#fbbf24"
    else:              g_clr = "#e87070"

    st.markdown(f"""
    <div class="gauge-container">
        <div class="circular-progress">
            <svg width="190" height="190" viewBox="0 0 190 190">
                <defs>
                    <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6c83ff"/>
                        <stop offset="50%" stop-color="#a78bfa"/>
                        <stop offset="100%" stop-color="{g_clr}"/>
                    </linearGradient>
                </defs>
                <circle cx="95" cy="95" r="75" fill="none"
                        stroke="rgba(255,255,255,0.03)" stroke-width="10"/>
                <circle cx="95" cy="95" r="75" fill="none"
                        stroke="url(#gaugeGrad)" stroke-width="10"
                        stroke-dasharray="{dash:.1f} {gap_val:.1f}"
                        stroke-linecap="round"
                        style="transition: stroke-dasharray 1.5s ease;
                               filter: drop-shadow(0 0 6px rgba(108,131,255,0.12));"/>
            </svg>
            <div class="score-text">
                <div class="number">{score:.1f}</div>
                <div class="lbl">Score</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Multi-color zone bar ────────────────────────────────────────────────
    if capped >= 90:   b_clr = "linear-gradient(90deg, #5eead4, #2dd4a8)"
    elif capped >= 75: b_clr = "linear-gradient(90deg, #6c83ff, #a78bfa)"
    elif capped >= 60: b_clr = "linear-gradient(90deg, #fbbf24, #e0a820)"
    else:              b_clr = "linear-gradient(90deg, #e87070, #c85050)"

    st.markdown(f"""
    <div class="bar-wrapper">
        <div class="bar-labels">
            <span style="color:#555570;">Performance Level</span>
            <span style="color:#b0b0c8;">{capped:.1f}%</span>
        </div>
        <div class="bar-track">
            <div class="bar-zones">
                <div class="zone-red"></div>
                <div class="zone-amber"></div>
                <div class="zone-blue"></div>
                <div class="zone-teal"></div>
            </div>
            <div class="bar-fill" style="width:{capped}%; background:{b_clr};"></div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Suggestions + Analysis ──────────────────────────────────────────────
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <h3 style="color:#c8c8dd; font-weight:700; font-size:1.1rem;">💡 Suggestions</h3>
            <p style="color:#454560; font-size:0.78rem;">Actionable improvement tips</p>
        </div>""", unsafe_allow_html=True)

        sug_colors = ["sug-c-blue", "sug-c-teal", "sug-c-purple", "sug-c-rose", "sug-c-amber"]
        for i, s in enumerate(get_suggestions(score)):
            st.markdown(f'<div class="sug-card {sug_colors[i % len(sug_colors)]}">{s}</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <h3 style="color:#c8c8dd; font-weight:700; font-size:1.1rem;">🤖 AI Analysis</h3>
            <p style="color:#454560; font-size:0.78rem;">Detailed breakdown</p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<div class="analysis-box">{performance_analysis(score)}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-row">
            <div class="mini-stat ms-blue">
                <div class="ms-val">{hours}h</div>
                <div class="ms-lbl">Study</div>
            </div>
            <div class="mini-stat ms-teal">
                <div class="ms-val">{attendance}%</div>
                <div class="ms-lbl">Attend.</div>
            </div>
            <div class="mini-stat ms-rose">
                <div class="ms-val">{previous}</div>
                <div class="ms-lbl">Prev.</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Status ──────────────────────────────────────────────────────────────
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if grade in ["A+", "A"]:
        st.success("🌟 **Outstanding!** On track for excellent results.")
    elif grade == "B":
        st.info("👍 **Good job!** Solid performance with room to grow.")
    elif grade == "C":
        st.warning("📚 **Average.** Growth potential — review suggestions.")
    else:
        st.error("⚠️ **Needs Improvement.** Immediate action recommended.")

    st.markdown('<div class="app-footer">Built with <span class="ft-heart">❤️</span> using Streamlit & ML — v2.0</div>', unsafe_allow_html=True)
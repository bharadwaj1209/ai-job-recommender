import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

# ----------------------------------------------------
# BASIC CONFIG
# ----------------------------------------------------
st.set_page_config(
    page_title="AI Job Recommender & Resume Checker",
    layout="wide"
)

# ----------------------------------------------------
# GLOBAL CSS – LIGHT, MODERN, ENHANCV-STYLE VIBE
# ----------------------------------------------------
st.markdown("""
<style>
/* Remove Streamlit default padding */
.main .block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    max-width: 1200px;
}

/* Hide Streamlit's default header so our sticky navbar sits at the very top */
header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

/* Page background — warm violet/teal gradient instead of flat gray */
body, .stApp {
    background: linear-gradient(180deg, #f5f3ff 0%, #eef2ff 35%, #f0fdfa 100%);
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Top hero background band */
.hero-section {
    background: radial-gradient(circle at top left, #e9e4ff, #eef6ff 45%, #f0fdfa 85%);
    padding: 0px 40px 40px 40px;
    border-bottom: 1px solid #e3e0f7;
}

/* NAVBAR — sticky, white, floating with shadow */
.navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 32px;
    margin: 0 -40px 30px -40px;
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 18px rgba(76, 29, 149, 0.08);
    border-bottom: 1px solid #ece9fb;
}
.logo-wrap {
    display: flex;
    align-items: center;
    gap: 8px;
}
.logo-icon {
    font-size: 22px;
}
.logo-text {
    font-weight: 800;
    font-size: 22px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    -webkit-background-clip: text;
    color: transparent;
}
.nav-links {
    display: flex;
    align-items: center;
    gap: 28px;
}
.nav-link {
    font-size: 14.5px;
    color: #4c5673;
    text-decoration: none;
    font-weight: 600;
    position: relative;
    padding-bottom: 2px;
}
.nav-link::after {
    content: "";
    position: absolute;
    left: 0;
    bottom: -4px;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    transition: width 0.25s ease;
}
.nav-link:hover {
    color: #7c3aed;
}
.nav-link:hover::after {
    width: 100%;
}
.nav-cta {
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: #ffffff !important;
    padding: 9px 18px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: 0 6px 16px rgba(124, 58, 237, 0.25);
    transition: transform 0.15s ease;
}
.nav-cta:hover {
    transform: translateY(-1px);
    color: #ffffff !important;
}

/* Hero text */
.hero-title {
    font-size: 40px;
    line-height: 1.1;
    font-weight: 800;
    color: #111827;
    margin-bottom: 16px;
}
.hero-highlight {
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    -webkit-background-clip:text;
    color:transparent;
}
.hero-subtitle {
    font-size: 16px;
    color:#4b5563;
    max-width: 520px;
}

/* Tag pill */
.hero-pill {
    display:inline-flex;
    align-items:center;
    gap:6px;
    padding:4px 12px;
    border-radius:999px;
    background:#ece4ff;
    color:#5b21b6;
    font-size:13px;
    font-weight:600;
    margin-bottom:8px;
}

/* Upload card */
.upload-card {
    background:#ffffff;
    border-radius: 16px;
    padding: 24px 24px 18px 24px;
    box-shadow: 0 14px 40px rgba(76, 29, 149, 0.10);
    border:1px solid #e5e7eb;
}
.upload-title {
    font-size: 18px;
    font-weight:700;
    margin-bottom:4px;
    color:#111827;
}
.upload-sub {
    font-size: 13px;
    color:#6b7280;
    margin-bottom: 14px;
}

/* Section titles */
.section-title {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 6px;
    color:#111827;
}
.section-subtitle {
    font-size: 14px;
    color:#6b7280;
    margin-bottom: 18px;
}

/* Feature cards */
.feature-card {
    background:#ffffff;
    border-radius:14px;
    padding:18px;
    border:1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.12);
}
.feature-title {
    font-size:16px;
    font-weight:700;
    margin-bottom:6px;
    color:#111827;
}
.feature-badge {
    display:inline-block;
    padding:2px 8px;
    font-size:11px;
    border-radius:999px;
    background:#ece4ff;
    color:#6d28d9;
    margin-bottom:6px;
}

/* Result cards */
.result-card {
    background:#ffffff;
    border-radius:14px;
    padding:18px;
    border:1px solid #e5e7eb;
    margin-bottom:14px;
}
.result-heading {
    font-size:17px;
    font-weight:700;
    margin-bottom:8px;
    color:#111827;
}
.result-body {
    font-size: 14px;
    color:#374151;
}

/* Job cards */
.job-card {
    background:#ffffff;
    border-radius:12px;
    padding:14px;
    border:1px solid #e5e7eb;
    margin-bottom:10px;
    font-size:14px;
}
.job-card-title {
    font-weight:700;
    color:#111827;
}
.job-card-company {
    color:#4b5563;
}
.job-card a {
    font-weight:600;
    color:#6d28d9;
    text-decoration:none;
}
.job-card a:hover {
    text-decoration:underline;
}

/* Footer */
.footer {
    border-top:1px solid #e5e7eb;
    padding:18px 0 26px 0;
    margin-top:40px;
    font-size:13px;
    color:#6b7280;
    text-align:center;
}

/* Center small text */
.small-muted {
    font-size:12px;
    color:#6b7280;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# NAVBAR (sticky, outside hero section)
# ----------------------------------------------------
st.markdown("""
<div class="navbar">
  <div class="logo-wrap">
    <span class="logo-icon">🛡️</span>
    <span class="logo-text">Avengers</span>
  </div>
  <div class="nav-links">
    <a class="nav-link" href="#about">About</a>
    <a class="nav-link" href="#features">Features</a>
    <a class="nav-link" href="#analysis">Analysis</a>
    <a class="nav-link" href="#jobs">Job Matches</a>
    <a class="nav-cta" href="#jobs">Get Started →</a>
  </div>
</div>
<div class="hero-section">
</div>
""", unsafe_allow_html=True)

# Use Streamlit layout inside hero
with st.container():
    col_left, col_right = st.columns([7, 5])

    with col_left:
        st.markdown(
            """
            <div style="margin-top:0px; padding-left:40px;">
                <div class="hero-pill">✨ Free AI-powered resume & job matcher</div>
                <div class="hero-title">
                    Is your resume <span class="hero-highlight">good enough to get interviews?</span>
                </div>
                <div class="hero-subtitle">
                    Upload your resume and let AI analyze your skills, detect gaps, build a growth roadmap, 
                    and recommend real LinkedIn & Naukri jobs tailored to you.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            """
            <div style="margin-top:10px;">
              <div class="upload-card">
                <div class="upload-title">Upload your resume</div>
                <div class="upload-sub">PDF only, max ~5MB. We don’t store your document.</div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
        st.markdown(
            """
                <div class="small-muted">Avengers Project</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# Anchor placeholders
st.markdown("<div id='about'></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# ABOUT + FEATURES SECTION
# ----------------------------------------------------
st.markdown("### About Avengers Project")
st.markdown(
    """
    Our project is an **AI-powered Resume Analyzer & Job Recommender** built for students and job seekers.  
    It reads your resume, understands your **skills, education, and experience**, then:
    
    - Scores and summarizes your resume in simple language  
    - Highlights **missing skills, tools, and certifications**  
    - Generates a **personal career roadmap**  
    - Searches for **matching job roles** across LinkedIn & Naukri  
    """
)

st.markdown("<div id='features'></div>", unsafe_allow_html=True)
st.markdown("#### Key Features")

fc1, fc2, fc3, fc4 = st.columns(4)
with fc1:
    st.markdown(
        """
        <div class="feature-card">
          <div class="feature-badge">AI Analysis</div>
          <div class="feature-title">Smart Resume Summary</div>
          <div>Reads your resume and generates a clean summary recruiters understand.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with fc2:
    st.markdown(
        """
        <div class="feature-card">
          <div class="feature-badge">Skill Gap</div>
          <div class="feature-title">Missing Skills Detector</div>
          <div>Finds what skills, tools, and domains you should add to grow faster.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with fc3:
    st.markdown(
        """
        <div class="feature-card">
          <div class="feature-badge">Roadmap</div>
          <div class="feature-title">Career Roadmap</div>
          <div>Creates a step-by-step learning path (courses, skills, experience ideas).</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with fc4:
    st.markdown(
        """
        <div class="feature-card">
          <div class="feature-badge">Job Matching</div>
          <div class="feature-title">Live Job Listings</div>
          <div>Fetches LinkedIn & Naukri job postings matching your profile keywords.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ----------------------------------------------------
# MAIN LOGIC – ANALYSIS & JOBS
# ----------------------------------------------------
summary = None
gaps = None
roadmap = None
linkedin_jobs = []
naukri_jobs = []

if uploaded_file:
    st.markdown("<div id='analysis'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Resume Analysis Dashboard")

    with st.spinner("Extracting resume text..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    # You can split into multiple models/calls like earlier
    colA, colB, colC = st.columns(3)

    with st.spinner("Generating AI summary..."):
        summary = ask_openai(
            f"Summarize this resume in 6-8 bullet points highlighting skills, education, and experience:\n\n{resume_text}",
            max_tokens=450
        )

    with st.spinner("Identifying skill gaps..."):
        gaps = ask_openai(
            f"As a career coach, list missing skills, tools, domains, and certifications that would significantly improve this person's resume:\n\n{resume_text}",
            max_tokens=350
        )

    with st.spinner("Creating career roadmap..."):
        roadmap = ask_openai(
            f"Based on this resume, create a 6-month learning and career roadmap. Use headings like 'Technical Skills', 'Projects', 'Certifications', 'Networking':\n\n{resume_text}",
            max_tokens=350
        )

    # Show three main result cards
    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown(
            """
            <div class="result-card">
              <div class="result-heading">📄 Resume Summary</div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='result-body'>{summary}</div></div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="result-card">
              <div class="result-heading">🧩 Skill Gaps & Missing Areas</div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='result-body'>{gaps}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="result-card">
              <div class="result-heading">🚀 6-Month Career Roadmap</div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"<div class='result-body'>{roadmap}</div></div>", unsafe_allow_html=True)

    st.success("✅ Resume analysis completed!")

    # ------------------------------------------------
    # JOB RECOMMENDATION SECTION
    # ------------------------------------------------
    st.markdown("<div id='jobs'></div>", unsafe_allow_html=True)
    st.markdown("### 💼 Job Recommendations")

    if st.button("🔎 Generate AI Job Matches"):
        with st.spinner("Generating search keywords from your resume..."):
            keywords = ask_openai(
                f"Based on this resume summary, suggest 6–10 best job titles or keyword phrases for job search. "
                f"Return only a comma-separated list, no explanation.\n\nSummary:\n{summary}",
                max_tokens=90
            )
            search_keywords_clean = keywords.replace("\n", "").strip()

        st.info(f"**AI Job Search Keywords:** {search_keywords_clean}")

        with st.spinner("Fetching LinkedIn & Naukri jobs..."):
            # IMPORTANT: rows >= 50 to avoid Apify error
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=60)

        colL, colR = st.columns(2)

        with colL:
            st.markdown("#### 🔷 LinkedIn Jobs")
            if linkedin_jobs:
                for job in linkedin_jobs[:20]:
                    st.markdown(
                        f"""
                        <div class="job-card">
                          <div class="job-card-title">{job.get('title')}</div>
                          <div class="job-card-company">{job.get('companyName') or job.get('company')}</div>
                          <div>📍 {job.get('location')}</div>
                          <div><a href="{job.get('link')}" target="_blank">View job</a></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No LinkedIn jobs found for these keywords right now.")

        with colR:
            st.markdown("#### 🇮🇳 Naukri Jobs")
            if naukri_jobs:
                for job in naukri_jobs[:20]:
                    st.markdown(
                        f"""
                        <div class="job-card">
                          <div class="job-card-title">{job.get('title')}</div>
                          <div class="job-card-company">{job.get('companyName')}</div>
                          <div>📍 {job.get('location')}</div>
                          <div><a href="{job.get('url')}" target="_blank">View job</a></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.warning("No Naukri jobs found for these keywords right now.")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------
st.markdown(
    """
    <div class="footer">
     All rights reserved © Chandra Prakash. Built with ❤️ using Streamlit and OpenAI API. 
    </div>
    """,
    unsafe_allow_html=True
)
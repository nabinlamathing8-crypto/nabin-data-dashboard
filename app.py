import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nabin Lama | Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #0f172a; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  [data-testid="stSidebar"] .stRadio label { 
    font-size: 15px; padding: 6px 0; cursor: pointer;
  }

  /* Cards */
  .card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: 0.2s; }

  /* Skill bar */
  .skill-wrap { margin-bottom: 14px; }
  .skill-label { font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 4px; }
  .skill-bar-bg { background: #f1f5f9; border-radius: 99px; height: 10px; }
  .skill-bar-fill { background: #3b82f6; border-radius: 99px; height: 10px; }

  /* Badge */
  .badge {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px 2px;
  }
  .badge-green { background: #f0fdf4; color: #16a34a; }
  .badge-amber { background: #fffbeb; color: #b45309; }

  /* Hero */
  .hero-title { font-size: 2.6rem; font-weight: 700; color: #0f172a; line-height: 1.2; }
  .hero-sub   { font-size: 1.1rem; color: #64748b; margin-top: 0.5rem; }

  /* Section header */
  .section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #3b82f6; margin-bottom: 4px;
  }
  .section-title { font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 1.2rem; }

  /* Timeline */
  .timeline-item { border-left: 2px solid #3b82f6; padding-left: 1rem; margin-bottom: 1.2rem; }
  .timeline-year { font-size: 12px; font-weight: 600; color: #3b82f6; }
  .timeline-text { font-size: 15px; color: #374151; font-weight: 500; }
  .timeline-desc { font-size: 13px; color: #6b7280; }

  /* Blog */
  .blog-date { font-size: 12px; color: #9ca3af; }
  .blog-title { font-size: 16px; font-weight: 600; color: #1e293b; margin: 4px 0; }
  .blog-snippet { font-size: 13px; color: #6b7280; }

  /* Contact button */
  .contact-btn {
    display: inline-block;
    background: #3b82f6;
    color: white !important;
    padding: 10px 24px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 500;
    font-size: 14px;
    margin: 4px 6px 4px 0;
  }
  .contact-btn:hover { background: #2563eb; }
  .contact-btn.outline {
    background: white; color: #3b82f6 !important;
    border: 1.5px solid #3b82f6;
  }

  a { text-decoration: none; }
  h3 { color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Nabin Lama")
    st.markdown("*Data Science Learner*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠  Home", "💼  Projects", "🛠️  Skills", "📝  Blog", "📬  Contact"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Connect**")
    st.markdown("[GitHub](https://github.com/yourusername)  ·  [LinkedIn](https://linkedin.com/in/yourprofile)  ·  [Email](mailto:nabin@email.com)")

# ═══════════════════════════════════════════════════════════════════════════════
# 🏠  HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style='padding-top:2rem'>
          <p class='section-label'>Welcome to my portfolio</p>
          <p class='hero-title'>Hi, I'm Nabin Lama 👋</p>
          <p class='hero-sub'>
            Aspiring Data Scientist focused on Python, data visualization,<br>
            and machine learning — turning raw data into clear insights.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:1.5rem'>", unsafe_allow_html=True)
        st.markdown("""
        <a class='contact-btn' href='#'>📄 Download Resume</a>
        <a class='contact-btn outline' href='#'>💼 View Projects</a>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='text-align:center; padding-top:2rem'>
          <div style='width:140px;height:140px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                      display:flex;align-items:center;justify-content:center;
                      font-size:3.5rem;margin:0 auto;'>
            🧑‍💻
          </div>
          <p style='color:#64748b;font-size:14px;margin-top:12px'>Nabin Lama<br>Data Science Learner</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick stats
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in zip(
        [c1, c2, c3, c4],
        ["5+", "3", "500+", "2025"],
        ["Projects", "Tools Mastered", "Rows Analyzed", "Learning Since"],
    ):
        col.metric(label, num)

    st.markdown("---")

    # Learning timeline
    st.markdown('<p class="section-label">Journey</p><p class="section-title">Learning Timeline</p>', unsafe_allow_html=True)
    timeline = [
        ("Jan 2025", "Started Python", "Variables, loops, functions, OOP basics"),
        ("Mar 2025", "Data with Pandas", "DataFrames, groupby, merging, cleaning"),
        ("Apr 2025", "Visualization", "Matplotlib, Seaborn, Plotly dashboards"),
        ("Jun 2025", "ML Fundamentals", "Scikit-learn, regression, classification"),
        ("Now", "Building Portfolio", "Streamlit apps, GitHub projects"),
    ]
    for year, title, desc in timeline:
        st.markdown(f"""
        <div class='timeline-item'>
          <div class='timeline-year'>{year}</div>
          <div class='timeline-text'>{title}</div>
          <div class='timeline-desc'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 💼  PROJECTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💼  Projects":
    st.markdown('<p class="section-label">Work</p><p class="section-title">Projects</p>', unsafe_allow_html=True)

    projects = [
        {
            "title": "🎓 Student Performance Analysis Report",
            "tags": ["Pandas", "Matplotlib", "Seaborn", "Python"],
            "problem": "Analyze 500 real student records to find what factors most affect academic scores and grades.",
            "method": "Built 6 charts: study hours vs score scatter, grade bar chart, subject scores, pass/fail pie (88.4%), GPA distribution, age vs score boxplot.",
            "result": "Avg score 64.1 | Top grade: B | Pass rate: 88.4% | Students studying 6–9 hrs scored highest | GPA > 3.2 = top grades.",
            "github": "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard",
            "chart": "student",
        },
        {
            "title": "Nepal Household Survey Analysis",
            "tags": ["Pandas", "Seaborn", "Python"],
            "problem": "Understand income distribution and education access across Nepal's provinces.",
            "method": "Cleaned 10,000+ rows, grouped by province, built heatmaps and bar charts.",
            "result": "Found Province 2 had lowest literacy rates — visualized the gap clearly.",
            "github": "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard",
            "chart": "bar",
        },
        {
            "title": "Nabin Data Dashboard",
            "tags": ["Streamlit", "Plotly", "Python"],
            "problem": "Build a personal data science portfolio that showcases projects and skills interactively.",
            "method": "Built with Streamlit and Plotly — multi-page app with charts, skill bars, and blog.",
            "result": "Live portfolio deployed on Streamlit Cloud, available to anyone online.",
            "github": "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard",
            "chart": "scatter",
        },
        {
            "title": "Sales Data Analysis",
            "tags": ["Pandas", "Matplotlib", "Python"],
            "problem": "Identify top-selling products and monthly revenue trends.",
            "method": "Grouped sales by category and month, built bar and line charts.",
            "result": "Discovered Q4 sales peak — helped inform restocking decisions.",
            "github": "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard",
            "chart": "line",
        },
    ]

    for idx, p in enumerate(projects):
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.6, 1])
            with col1:
                tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in p["tags"])
                st.markdown(f"""
                <h3 style='margin:0 0 6px'>{p['title']}</h3>
                <div style='margin-bottom:10px'>{tags_html}</div>
                <table style='font-size:13px;color:#374151;width:100%'>
                  <tr><td style='color:#9ca3af;padding-right:8px;white-space:nowrap;vertical-align:top'>Problem</td><td>{p['problem']}</td></tr>
                  <tr><td style='color:#9ca3af;padding-right:8px;white-space:nowrap;vertical-align:top'>Method</td><td>{p['method']}</td></tr>
                  <tr><td style='color:#9ca3af;padding-right:8px;white-space:nowrap;vertical-align:top'>Result</td><td>{p['result']}</td></tr>
                </table>
                <a href='{p["github"]}' class='contact-btn' style='margin-top:12px;display:inline-block;font-size:13px'>
                  🔗 View on GitHub
                </a>
                """, unsafe_allow_html=True)
            with col2:
                np.random.seed(idx * 7 + 1)
                if p["chart"] == "student":
                    # Real data from the notebook analysis
                    grades = ["D+", "C", "C+", "B", "B+", "A", "A+"]
                    scores = [42, 52, 58, 65, 72, 80, 88]
                    fig = px.bar(
                        x=grades, y=scores,
                        labels={"x": "Grade", "y": "Avg Score"},
                        color=scores, color_continuous_scale="Greens", height=220,
                        title="Avg Score by Grade"
                    )
                elif p["chart"] == "bar":
                    df = pd.DataFrame({"Province": [f"P{i}" for i in range(1, 8)],
                                       "Literacy": np.random.randint(55, 90, 7)})
                    fig = px.bar(df, x="Province", y="Literacy", color="Literacy",
                                 color_continuous_scale="Blues", height=220)
                elif p["chart"] == "scatter":
                    df = pd.DataFrame({"Study Hours": np.random.randint(1, 10, 50),
                                       "Score": np.random.randint(40, 100, 50)})
                    fig = px.scatter(df, x="Study Hours", y="Score", height=220,
                                     color="Score", color_continuous_scale="Blues")
                else:
                    x = pd.date_range("2023-01-01", periods=12, freq="ME")
                    fig = px.line(x=x, y=np.cumsum(np.random.randint(10, 50, 12)),
                                  height=220, labels={"x": "Month", "y": "Sales"})
                fig.update_layout(
                    margin=dict(l=10, r=10, t=30, b=10),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig, use_container_width=True, key=f"proj_chart_{idx}")
            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️  SKILLS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🛠️  Skills":
    st.markdown('<p class="section-label">Abilities</p><p class="section-title">Skills Dashboard</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    skills = {
        "Python": 75,
        "Pandas": 70,
        "Matplotlib / Seaborn": 65,
        "Plotly / Streamlit": 60,
        "SQL": 50,
        "Scikit-learn (ML)": 45,
        "Git & GitHub": 55,
    }

    with col1:
        st.markdown("#### Core Skills")
        for skill, pct in skills.items():
            st.markdown(f"""
            <div class='skill-wrap'>
              <div class='skill-label'>{skill} <span style='float:right;color:#3b82f6'>{pct}%</span></div>
              <div class='skill-bar-bg'>
                <div class='skill-bar-fill' style='width:{pct}%'></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Learning Now 🔥")
        learning_now = ["Machine Learning basics", "Scikit-learn pipelines",
                        "Feature engineering", "Model evaluation metrics"]
        for item in learning_now:
            st.markdown(f"<span class='badge'>⚡ {item}</span>", unsafe_allow_html=True)

        st.markdown("#### Next Up 🎯")
        next_up = ["Deep Learning (PyTorch)", "SQL advanced queries",
                   "Data Engineering basics", "Kaggle competitions"]
        for item in next_up:
            st.markdown(f"<span class='badge badge-amber'>🎯 {item}</span>", unsafe_allow_html=True)

        st.markdown("#### Tools & Libraries ✅")
        tools = ["Python", "Pandas", "NumPy", "Matplotlib", "Seaborn",
                 "Plotly", "Streamlit", "Scikit-learn", "Git", "Jupyter", "VS Code"]
        badges = " ".join(f"<span class='badge badge-green'>✓ {t}</span>" for t in tools)
        st.markdown(badges, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Skills Radar")
    categories = list(skills.keys())
    values = list(skills.values())
    fig = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        line_color="#3b82f6",
        fillcolor="rgba(59,130,246,0.15)",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False, height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 📝  BLOG
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝  Blog":
    st.markdown('<p class="section-label">Notes</p><p class="section-title">Blog & Learning Notes</p>', unsafe_allow_html=True)

    posts = [
        {
            "date": "June 15, 2025",
            "title": "How I cleaned messy survey data with Pandas",
            "tags": ["Pandas", "Data Cleaning"],
            "snippet": "Real-world data is never clean. Here's exactly how I handled missing values, wrong data types, and duplicate rows in a 10,000-row Nepal survey dataset.",
            "read": "4 min read",
        },
        {
            "date": "May 28, 2025",
            "title": "My first Seaborn heatmap — what I learned",
            "tags": ["Seaborn", "Visualization"],
            "snippet": "Heatmaps look simple but there are 3 things that tripped me up. This is a walkthrough of my first real heatmap, mistakes and all.",
            "read": "3 min read",
        },
        {
            "date": "May 10, 2025",
            "title": "Linear regression explained simply",
            "tags": ["ML", "Scikit-learn"],
            "snippet": "I spent a week confused about regression. Here's the plain-English explanation I wish I had from the start, with code examples.",
            "read": "5 min read",
        },
        {
            "date": "Apr 22, 2025",
            "title": "Why I switched from Matplotlib to Plotly",
            "tags": ["Plotly", "Visualization"],
            "snippet": "Matplotlib is powerful but Plotly made my charts interactive in 2 lines. Here's my honest comparison after using both.",
            "read": "3 min read",
        },
    ]

    for post in posts:
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in post["tags"])
        st.markdown(f"""
        <div class='card'>
          <div class='blog-date'>{post['date']} · {post['read']}</div>
          <div class='blog-title'>{post['title']}</div>
          <div style='margin:6px 0'>{tags_html}</div>
          <div class='blog-snippet'>{post['snippet']}</div>
          <a href='#' style='font-size:13px;color:#3b82f6;font-weight:500;display:inline-block;margin-top:10px'>Read more →</a>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 📬  CONTACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📬  Contact":
    st.markdown('<p class="section-label">Get in touch</p><p class="section-title">Contact</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        <div class='card'>
          <h3 style='margin-top:0'>Let's connect 👋</h3>
          <p style='color:#64748b;font-size:15px'>
            I'm always open to feedback, collaboration, or just chatting about data science.
            Feel free to reach out through any of the channels below.
          </p>
          <div style='margin:1.2rem 0'>
            <a class='contact-btn' href='mailto:nabin@email.com'>📧 Send Email</a>
            <a class='contact-btn outline' href='https://linkedin.com/in/yourprofile'>🔗 LinkedIn</a>
            <a class='contact-btn outline' href='https://github.com/yourusername'>💻 GitHub</a>
          </div>
          <a class='contact-btn' href='#' style='background:#16a34a'>📄 Download Resume</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Send a message")
        name = st.text_input("Your name")
        email = st.text_input("Your email")
        message = st.text_area("Message", height=130)
        if st.button("Send Message 🚀"):
            if name and email and message:
                st.success(f"Thanks {name}! I'll reply to {email} soon.")
            else:
                st.warning("Please fill in all fields.")

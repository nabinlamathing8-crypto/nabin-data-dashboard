%pip install anthropic

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import io
import time
from datetime import datetime
from anthropic import Anthropic

# ── Constants ─────────────────────────────────────────────────────────────────
GITHUB_USER = "nabinlamathing8-crypto"
GITHUB_REPO = "nabin-data-dashboard"
GITHUB      = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
LINKEDIN    = "https://www.linkedin.com/in/nabin-kumar-thing-b92406393"
EMAIL       = "nabinlamathing8@gmail.com"
ANTHROPIC_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")

client = Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nabin · Data Science",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background: #050a14;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
  background: #070d1a !important;
  border-right: 1px solid #1a2744;
}
[data-testid="stSidebar"] * { color: #8899bb !important; }
[data-testid="stSidebar"] .stRadio label { color: #8899bb !important; }

/* ── Main bg ── */
.main .block-container {
  background: #050a14;
  padding-top: 2rem;
}
.stApp { background: #050a14; }

/* ── Typography ── */
h1,h2,h3,h4 { color: #e8f0ff; font-family: 'Inter', sans-serif; }

/* ── HERO ── */
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; color: #3b82f6; letter-spacing: 0.2em;
  text-transform: uppercase; margin-bottom: 12px;
}
.hero-name {
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  font-weight: 800; color: #ffffff; line-height: 1.05;
  letter-spacing: -0.02em; margin: 0 0 8px;
}
.hero-name span {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-role {
  font-size: 1.15rem; color: #5a7099; font-weight: 400;
  margin-bottom: 28px; line-height: 1.6;
}

/* ── Status pill ── */
.status-pill {
  display: inline-flex; align-items: center; gap: 7px;
  background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2);
  color: #10b981; border-radius: 99px; padding: 5px 14px;
  font-size: 12px; font-weight: 500; margin-bottom: 24px;
}
.pulse {
  width: 7px; height: 7px; border-radius: 50%;
  background: #10b981;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%,100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.8); }
}

/* ── Stat cards ── */
.stat-grid {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
  margin: 28px 0;
}
.stat-card {
  background: #0b1425; border: 1px solid #1a2744;
  border-radius: 12px; padding: 18px 16px; text-align: center;
}
.stat-num {
  font-size: 1.8rem; font-weight: 800; color: #ffffff;
  font-family: 'JetBrains Mono', monospace;
}
.stat-label { font-size: 11px; color: #4a6080; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 4px; }

/* ── Section headings ── */
.sec-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: #3b82f6; letter-spacing: 0.15em;
  text-transform: uppercase; margin-bottom: 6px;
}
.sec-title {
  font-size: 1.7rem; font-weight: 700; color: #e8f0ff;
  margin-bottom: 1.5rem; line-height: 1.2;
}

/* ── Project cards ── */
.proj-card {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 16px; padding: 1.6rem;
  margin-bottom: 1.2rem; position: relative;
  transition: border-color 0.2s, transform 0.2s;
}
.proj-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
.proj-card::before {
  content: ''; position: absolute; top: 0; left: 0;
  right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, #3b82f6, transparent);
  border-radius: 16px 16px 0 0;
}
.proj-title { font-size: 1.05rem; font-weight: 700; color: #e8f0ff; margin: 0 0 8px; }
.proj-meta { font-size: 12px; color: #4a6080; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace; }

/* ── Badges ── */
.badge {
  display: inline-block; background: #0d1f3c; color: #4d90fe;
  border: 1px solid #1a3060; border-radius: 6px;
  padding: 2px 10px; font-size: 11px; font-weight: 500; margin: 2px 2px;
  font-family: 'JetBrains Mono', monospace;
}
.badge-green { background: #071a10; color: #34d399; border-color: #0f3320; }
.badge-purple { background: #150d2e; color: #a78bfa; border-color: #2d1f5e; }
.badge-amber { background: #1a1000; color: #fbbf24; border-color: #3a2500; }

/* ── Skill bars ── */
.skill-row { margin-bottom: 16px; }
.skill-top { display: flex; justify-content: space-between; margin-bottom: 6px; }
.skill-name { font-size: 13px; color: #8899bb; font-weight: 500; }
.skill-pct { font-size: 12px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
.skill-track { background: #0d1a2e; border-radius: 99px; height: 6px; overflow: hidden; }
.skill-fill {
  height: 6px; border-radius: 99px;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
  transition: width 0.8s ease;
}

/* ── Timeline ── */
.timeline-item {
  display: flex; gap: 16px; margin-bottom: 24px; position: relative;
}
.timeline-dot {
  width: 36px; height: 36px; border-radius: 50%;
  background: #0d1f3c; border: 2px solid #3b82f6;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; flex-shrink: 0; z-index: 1;
}
.timeline-line {
  position: absolute; left: 17px; top: 36px;
  width: 2px; height: calc(100% + 8px);
  background: linear-gradient(to bottom, #1a2744, transparent);
}
.timeline-content { padding-top: 4px; }
.timeline-date {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: #3b82f6; margin-bottom: 4px;
}
.timeline-title { font-size: 14px; font-weight: 600; color: #e8f0ff; margin-bottom: 4px; }
.timeline-desc { font-size: 13px; color: #4a6080; line-height: 1.5; }

/* ── Blog ── */
.blog-card {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 1rem;
}
.blog-date { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #3b82f6; margin-bottom: 6px; }
.blog-title { font-size: 15px; font-weight: 600; color: #e8f0ff; margin-bottom: 6px; }
.blog-preview { font-size: 13px; color: #4a6080; line-height: 1.5; }
.blog-body-inner {
  font-size: 14px; color: #8899bb; line-height: 1.8;
  background: #050a14; border: 1px solid #1a2744;
  border-radius: 10px; padding: 1.2rem; margin-top: 12px;
}
.blog-body-inner h4 { color: #e8f0ff; font-size: 14px; margin: 14px 0 6px; }
.blog-body-inner code {
  background: #0a1628; color: #7dd3fc;
  padding: 2px 7px; border-radius: 4px;
  font-size: 12px; font-family: 'JetBrains Mono', monospace;
}
.blog-body-inner pre {
  background: #050a14; color: #e2e8f0;
  padding: 14px 18px; border-radius: 10px; font-size: 12px;
  overflow-x: auto; margin: 10px 0; line-height: 1.6;
  border: 1px solid #1a2744; font-family: 'JetBrains Mono', monospace;
}

/* ── Chat ── */
.chat-wrap {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 16px; padding: 1.2rem; max-height: 440px;
  overflow-y: auto;
}
.chat-msg-user {
  background: #0d1f3c; border: 1px solid #1a3060;
  border-radius: 12px 12px 4px 12px; padding: 10px 14px;
  margin: 8px 0 8px 20%; font-size: 13px; color: #c8d8ff;
}
.chat-msg-ai {
  background: #0a1220; border: 1px solid #1a2744;
  border-radius: 12px 12px 12px 4px; padding: 10px 14px;
  margin: 8px 20% 8px 0; font-size: 13px; color: #8899bb;
  line-height: 1.7;
}
.chat-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; margin-bottom: 2px;
}
.chat-label.user { color: #3b82f6; text-align: right; margin-right: 4px; }
.chat-label.ai { color: #10b981; margin-left: 4px; }

/* ── Contact ── */
.contact-card {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 16px; padding: 2rem; margin-bottom: 1rem;
}
.contact-link {
  display: flex; align-items: center; gap: 10px;
  color: #8899bb; text-decoration: none; font-size: 14px;
  padding: 10px 0; border-bottom: 1px solid #0d1a2e;
  transition: color 0.15s;
}
.contact-link:hover { color: #3b82f6; }
.contact-icon { font-size: 18px; width: 24px; }

/* ── About boxes ── */
.about-box {
  background: #080f1e; border: 1px solid #1a2744;
  border-left: 3px solid #3b82f6;
  border-radius: 0 10px 10px 0;
  padding: 1rem 1.2rem; margin-bottom: 1rem;
  font-size: 14px; color: #8899bb; line-height: 1.7;
}
.about-box strong { color: #e8f0ff; }

/* ── GitHub stats ── */
.gh-stat {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 10px; padding: 14px; text-align: center;
}
.gh-num {
  font-size: 1.5rem; font-weight: 800; color: #ffffff;
  font-family: 'JetBrains Mono', monospace;
}
.gh-lbl { font-size: 11px; color: #4a6080; margin-top: 4px; }

/* ── Buttons ── */
.cta-btn {
  display: inline-block; background: #2563eb; color: white !important;
  padding: 10px 22px; border-radius: 8px; text-decoration: none;
  font-weight: 600; font-size: 13px; letter-spacing: 0.02em;
  margin: 4px 6px 4px 0; border: none; transition: background 0.15s;
}
.cta-btn:hover { background: #1d4ed8; }
.cta-btn.ghost {
  background: transparent; color: #3b82f6 !important;
  border: 1px solid #1a3060;
}
.cta-btn.ghost:hover { background: #0d1f3c; }

/* ── DataPlayground ── */
.dp-card {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem;
}

/* ── Strealit overrides ── */
.stTextInput input, .stTextArea textarea {
  background: #080f1e !important; color: #e8f0ff !important;
  border: 1px solid #1a2744 !important;
}
.stSelectbox > div { background: #080f1e !important; }
div[data-testid="stMetricValue"] { color: #ffffff !important; }

a { text-decoration: none !important; }

/* ── Divider ── */
.fancy-divider {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent, #1a2744, transparent);
  margin: 2rem 0;
}

/* hide default streamlit header */
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page_views" not in st.session_state:
    st.session_state.page_views = {"Home": 0, "Projects": 0, "Skills": 0, "Blog": 0, "Playground": 0, "Contact": 0}
if "tag_filter" not in st.session_state:
    st.session_state.tag_filter = "All"

# ══════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════
PROJECTS = [
    {
        "title": "Student Performance Analysis",
        "tags": ["Pandas", "Matplotlib", "Seaborn", "Python"],
        "year": "2026",
        "problem": "Analyzed 500 student records to find what factors most affect academic scores.",
        "method": "6 charts: scatter (hours vs score), grade bars, subject scores, pass/fail pie (88.4%), GPA histogram, age boxplot.",
        "result": "Avg score 64.1 | Pass rate 88.4% | Students studying 6–9 hrs scored highest.",
        "github": GITHUB,
        "chart": "student",
    },
    {
        "title": "Heart Attack Incidence Analysis",
        "tags": ["Pandas", "Seaborn", "Healthcare", "Python"],
        "year": "2026",
        "problem": "Analyzed 275,644 patient records to find risk factors across Germany (2015–2023).",
        "method": "6 charts: annual trend, incidence by state, smoking status, stress level, age group, correlation heatmap.",
        "result": "15.01% avg incidence | Top state: Hesse | High stress + poor diet = peak risk.",
        "github": GITHUB,
        "chart": "heart",
    },
    {
        "title": "BMW Sales + ML Price Prediction",
        "tags": ["Pandas", "Scikit-learn", "ML", "GradientBoosting"],
        "year": "2026",
        "problem": "Analyzed BMW vehicle sales across regions & models, built ML price predictor.",
        "method": "EDA + Random Forest classifier + Gradient Boosting regressor. One-hot encoding, feature engineering.",
        "result": "Electric vehicles trending | Price predictor with GradientBoostingRegressor.",
        "github": GITHUB,
        "chart": "bmw",
    },
    {
        "title": "Nepal Household Survey Analysis",
        "tags": ["Pandas", "Seaborn", "Python"],
        "year": "2025",
        "problem": "Understand income distribution and education access across Nepal's provinces.",
        "method": "Cleaned 10,000+ rows, grouped by province, built heatmaps and bar charts.",
        "result": "Province 2 had lowest literacy — gap visualized clearly.",
        "github": GITHUB,
        "chart": "bar",
    },
    {
        "title": "Nabin Data Dashboard",
        "tags": ["Streamlit", "Plotly", "Python"],
        "year": "2026",
        "problem": "Build a personal data science portfolio showcasing projects and skills interactively.",
        "method": "Multi-page Streamlit app with Plotly charts, AI chatbot, data playground, GitHub stats.",
        "result": "Live portfolio deployed on Streamlit Cloud.",
        "github": GITHUB,
        "chart": "scatter",
    },
]

SKILLS = {
    "Python": 75, "Pandas": 70, "Matplotlib / Seaborn": 65,
    "Plotly / Streamlit": 60, "SQL": 50, "Scikit-learn (ML)": 45, "Git & GitHub": 55,
}

TIMELINE = [
    {"date": "May 2026", "icon": "🧠", "title": "First ML project — BMW price predictor", "desc": "Built Random Forest + Gradient Boosting models. Learned one-hot encoding and feature engineering."},
    {"date": "June 2026", "icon": "📊", "title": "Heart attack incidence analysis (275K rows)", "desc": "Worked with large real-world healthcare dataset. Learned performance optimization with groupby."},
    {"date": "June 2026", "icon": "🚀", "title": "Deployed portfolio on Streamlit Cloud", "desc": "First live web deployment. Added CI/CD via GitHub."},
    {"date": "June 2026", "icon": "🤖", "title": "Added AI chatbot to portfolio", "desc": "Integrated Claude API to answer visitor questions about my projects and skills."},
    {"date": "July 2026 (goal)", "icon": "🎯", "title": "Deep Learning with PyTorch", "desc": "Starting CNN image classification. First Kaggle competition entry planned."},
]

BLOG_POSTS = [
    {
        "date": "June 21, 2026",
        "title": "Heart Attack Analysis — 275,644 Patients, 6 Charts",
        "tags": ["Pandas", "Seaborn", "Healthcare"],
        "preview": "How I found that high stress + poor diet = peak heart attack risk across 275K patient records.",
        "body": """<h4>The Dataset</h4>
<p>275,644 patient records from Germany (2015–2023). Columns: Year, State, Age_Group, Smoking_Status, Stress_Level, BMI, Hypertension, and Heart_Attack_Incidence.</p>
<h4>Key Stats</h4>
<pre>Overall avg incidence rate: 15.01%
Top risk state:             Hesse
Hypertension rate:          40.1%
Diabetes rate:              20.0%</pre>
<h4>Building the 6-Chart Report</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
annual = df.groupby('Year')['Heart_Attack_Incidence'].mean()
axes[0,0].plot(annual.index, annual.values, color='green', marker='o')
sns.heatmap(df[risk_cols].corr(), annot=True, fmt=".2f", cmap="RdYlGn", ax=axes[1,2])</pre>
<h4>Key Insight</h4>
<p>High stress + poor diet yields the <code>peak</code> incidence combination. Smokers show elevated risk regardless of other factors.</p>""",
    },
    {
        "date": "June 20, 2026",
        "title": "BMW Sales + ML Price Prediction (2010–2024)",
        "tags": ["ML", "Scikit-learn", "Pandas"],
        "preview": "My first project combining EDA with real machine learning — classifier + regressor on BMW data.",
        "body": """<h4>Step 1 — Data Cleaning</h4>
<pre>df["Fuel_Type"] = df["Fuel_Type"].str.replace(r'\\\\+', '', regex=True).str.strip()
df["Car_Age"] = 2024 - df['Year']</pre>
<h4>Step 2 — Random Forest Classifier</h4>
<pre>from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)</pre>
<h4>Step 3 — Gradient Boosting Regressor</h4>
<pre>from sklearn.ensemble import GradientBoostingRegressor
reg = GradientBoostingRegressor(n_estimators=200, random_state=42)
print(f"R²: {r2_score(y_test, preds):.3f}")</pre>
<h4>What I Learned</h4>
<p>One-hot encoding text columns is critical. <code>GradientBoostingRegressor</code> outperforms linear regression for real-world pricing data.</p>""",
    },
    {
        "date": "June 21, 2026",
        "title": "Student Performance — From CSV to 6 Charts",
        "tags": ["Pandas", "Matplotlib", "Seaborn"],
        "preview": "Full walkthrough: 500 student records, 11 columns, 6 charts. What 88.4% pass rate actually looks like in data.",
        "body": """<h4>Key Stats</h4>
<pre>total_record = len(df)                      # 500
avg_score    = df['Average_Score'].mean()    # 64.1
pass_rate    = ...                           # 88.4%
top_grade    = df['Grade'].value_counts().idxmax()  # B</pre>
<h4>All 6 Charts in One Figure</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes[0,0].scatter(df['Hours_Studied'], df['Average_Score'], color='green')
axes[1,0].pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')
sns.boxplot(data=df, x='Age', y='Average_Score', ax=axes[1,2], palette='Greens')</pre>
<h4>Insight</h4>
<p>Students studying <code>6–9 hours</code> scored highest. Below 4 hours → much lower scores. A clear signal.</p>""",
    },
    {
        "date": "June 15, 2026",
        "title": "Cleaning Messy Survey Data with Pandas",
        "tags": ["Pandas", "Data Cleaning"],
        "preview": "10,847 → 10,203 clean rows. How I handled missing values, wrong dtypes, duplicate rows, and messy column names.",
        "body": """<h4>4-Step Cleaning</h4>
<pre># Step 1 — Fix column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Step 2 — Handle missing values
df["income"].fillna(df["income"].median(), inplace=True)
df.dropna(subset=["province", "age"], inplace=True)

# Step 3 — Remove duplicates
df.drop_duplicates(inplace=True)

# Result: 10,847 → 10,203 clean rows</pre>
<p>That 600-row difference contained 3 types of errors. Always clean before you visualize.</p>""",
    },
]

PORTFOLIO_CONTEXT = """You are an AI assistant embedded in Nabin Kumar Thing's data science portfolio website.
Nabin is an aspiring data scientist from Nepal. He has completed these projects:
1. Student Performance Analysis — 500 records, found 88.4% pass rate, study hours correlation
2. Heart Attack Incidence Analysis — 275,644 German patient records, 15.01% avg incidence
3. BMW Sales + ML Price Prediction — Random Forest + Gradient Boosting, EDA
4. Nepal Household Survey — 10,000+ rows, province-level literacy analysis
5. This portfolio itself — multi-page Streamlit app with AI, deployed on Streamlit Cloud

Skills: Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, SQL, Scikit-learn, Git
Learning now: Machine learning, Scikit-learn pipelines, feature engineering
Email: nabinlamathing8@gmail.com | GitHub: github.com/nabinlamathing8-crypto

Answer questions about Nabin's work, skills, background, and projects. Be helpful, concise, and friendly.
If asked about something you don't know, say so politely. Keep answers under 150 words unless asked for detail."""

# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════
def fetch_github_stats():
    try:
        r = requests.get(f"https://api.github.com/users/{GITHUB_USER}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {"repos": d.get("public_repos", 8), "followers": d.get("followers", 0), "following": d.get("following", 0)}
    except:
        pass
    return {"repos": "8+", "followers": "—", "following": "—"}

def ai_chat(user_msg):
    if not client:
        return "⚠️ AI chat not available — add ANTHROPIC_API_KEY to Streamlit secrets."
    msgs = []
    for m in st.session_state.chat_history[-8:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    msgs.append({"role": "user", "content": user_msg})
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=PORTFOLIO_CONTEXT,
        messages=msgs
    )
    return resp.content[0].text

def ai_summarize_project(project):
    if not client:
        return "Add ANTHROPIC_API_KEY to enable AI summaries."
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=120,
        messages=[{"role": "user", "content":
            f"Write a 2-sentence recruiter-friendly summary of this data science project:\n"
            f"Title: {project['title']}\nProblem: {project['problem']}\nResult: {project['result']}"}]
    )
    return resp.content[0].text

def make_chart(p, idx):
    np.random.seed(idx * 7 + 1)
    if p["chart"] == "student":
        hours = np.random.uniform(1, 10, 500)
        sc = np.clip(45 + hours * 3.5 + np.random.randn(500) * 10, 35, 97)
        fig = px.scatter(x=hours, y=sc, height=180,
                         labels={"x": "Hours", "y": "Score"},
                         title="Study hrs vs Score",
                         color=sc, color_continuous_scale="Blues")
        fig.update_traces(marker=dict(size=3))
        style_fig(fig)
        return [fig]
    elif p["chart"] == "heart":
        years = list(range(2015, 2024))
        rates = [0.1487, 0.1494, 0.1534, 0.1471, 0.1519, 0.1519, 0.1510, 0.1498, 0.1471]
        fig = px.area(x=years, y=rates, height=180, title="Incidence Trend",
                      color_discrete_sequence=["#3b82f6"])
        style_fig(fig)
        return [fig]
    elif p["chart"] == "bmw":
        years = list(range(2010, 2025))
        prices = [28000 + i * 800 + np.random.randint(-500, 500) for i in range(15)]
        fig = px.line(x=years, y=prices, markers=True, height=180, title="BMW Avg Price",
                      color_discrete_sequence=["#8b5cf6"])
        style_fig(fig)
        return [fig]
    elif p["chart"] == "bar":
        df = pd.DataFrame({"Province": [f"P{i}" for i in range(1, 8)],
                           "Literacy": np.random.randint(55, 90, 7)})
        fig = px.bar(df, x="Province", y="Literacy", height=180, title="Literacy by Province",
                     color="Literacy", color_continuous_scale="Blues")
        style_fig(fig)
        return [fig]
    else:
        df = pd.DataFrame({"Study": np.random.randint(1, 10, 50), "Score": np.random.randint(40, 100, 50)})
        fig = px.scatter(df, x="Study", y="Score", height=180, title="Study vs Score",
                         color="Score", color_continuous_scale="Blues")
        style_fig(fig)
        return [fig]

def style_fig(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a6080", size=10),
        margin=dict(l=8, r=8, t=30, b=8),
        showlegend=False, coloraxis_showscale=False,
        title_font=dict(color="#8899bb", size=11),
    )
    fig.update_xaxes(gridcolor="#0d1a2e", color="#4a6080")
    fig.update_yaxes(gridcolor="#0d1a2e", color="#4a6080")

def auto_eda(df):
    figs = []
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                        color_continuous_scale="Blues",
                        title="Correlation Heatmap")
        style_fig(fig)
        figs.append(("Correlation Heatmap", fig))

    for col in num_cols[:3]:
        fig = px.histogram(df, x=col, nbins=30,
                           color_discrete_sequence=["#3b82f6"],
                           title=f"Distribution — {col}")
        style_fig(fig)
        figs.append((f"Dist: {col}", fig))

    for col in cat_cols[:2]:
        vc = df[col].value_counts().head(10)
        fig = px.bar(x=vc.index.astype(str), y=vc.values,
                     labels={"x": col, "y": "Count"},
                     color_discrete_sequence=["#8b5cf6"],
                     title=f"Top values — {col}")
        style_fig(fig)
        figs.append((f"Top: {col}", fig))

    if len(num_cols) >= 2:
        fig = px.scatter_matrix(df[num_cols[:4]],
                                color_discrete_sequence=["#3b82f6"],
                                title="Scatter Matrix")
        style_fig(fig)
        figs.append(("Scatter Matrix", fig))

    return figs


# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding: 1rem 0 0.5rem'>
      <div style='font-family: JetBrains Mono, monospace; font-size: 10px; color: #3b82f6; letter-spacing: 0.15em; margin-bottom: 6px;'>PORTFOLIO</div>
      <div style='font-size: 15px; font-weight: 700; color: #e8f0ff;'>Nabin Kumar Thing</div>
      <div style='font-size: 12px; color: #4a6080;'>Data Science Learner</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a2744; margin: 12px 0'>", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠  Home", "💼  Projects", "⚡  Skills", "📅  Timeline",
         "📝  Blog", "🧪  Playground", "🤖  AI Chat", "📬  Contact"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1a2744; margin: 12px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size: 11px; color: #4a6080; margin-bottom: 8px;'>CONNECT</div>
    <a href='{GITHUB}' style='color: #8899bb; font-size: 12px; display:block; margin-bottom:5px;'>⌥ GitHub</a>
    <a href='{LINKEDIN}' style='color: #8899bb; font-size: 12px; display:block; margin-bottom:5px;'>⌥ LinkedIn</a>
    <a href='mailto:{EMAIL}' style='color: #8899bb; font-size: 12px; display:block;'>⌥ Email</a>
    """, unsafe_allow_html=True)

    # Mini analytics
    st.markdown("<hr style='border-color:#1a2744; margin: 12px 0'>", unsafe_allow_html=True)
    clean_page = page.split("  ")[1]
    st.session_state.page_views[clean_page] = st.session_state.page_views.get(clean_page, 0) + 1
    total = sum(st.session_state.page_views.values())
    st.markdown(f"""
    <div style='font-size: 10px; color: #2a3a55; font-family: JetBrains Mono, monospace;'>
      SESSION VIEWS: {total}
    </div>
    """, unsafe_allow_html=True)

page = page.split("  ")[1]

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if page == "Home":
    col1, col2 = st.columns([1.8, 1])
    with col1:
        st.markdown("""
        <div class='hero-eyebrow'>// data scientist in training</div>
        <h1 class='hero-name'>Hi, I'm <span>Nabin</span><br>Kumar Thing</h1>
        <p class='hero-role'>
          Python · Pandas · Machine Learning · Data Viz<br>
          Turning raw numbers into stories that matter.
        </p>
        <div class='status-pill'>
          <div class='pulse'></div>
          Open to opportunities · Learning ML daily
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.link_button("💼 View Projects", GITHUB, type="primary")
        with c2:
            st.link_button("📬 Get in Touch", f"mailto:{EMAIL}")

    with col2:
        st.markdown("""
        <div style='text-align:center; padding:2rem 1rem'>
          <div style='width:120px;height:120px;border-radius:50%;
            background: linear-gradient(135deg,#1e3a8a,#7c3aed);
            display:flex;align-items:center;justify-content:center;
            font-size:3rem;margin:0 auto;
            box-shadow: 0 0 0 2px #1a2744, 0 0 40px rgba(59,130,246,0.15)'>
            🧑‍💻
          </div>
          <div style='margin-top:14px; font-family: JetBrains Mono, monospace; font-size: 11px; color: #3b82f6;'>
            LEARNING SINCE 2026
          </div>
        </div>
        """, unsafe_allow_html=True)

    # GitHub live stats
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">// github · live stats</div>', unsafe_allow_html=True)
    gh = fetch_github_stats()
    g1, g2, g3, g4, g5 = st.columns(5)
    for col, val, lbl in zip(
        [g1, g2, g3, g4, g5],
        [gh["repos"], gh["followers"], gh["following"], "4+", "500+"],
        ["Public Repos", "Followers", "Following", "Projects Built", "Rows Analyzed"]
    ):
        col.markdown(f"""
        <div class='gh-stat'>
          <div class='gh-num'>{val}</div>
          <div class='gh-lbl'>{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    # Stat cards
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">// quick stats</div>', unsafe_allow_html=True)
    st.markdown('<div class="stat-grid">', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in zip([s1, s2, s3, s4],
        ["275K+", "7", "88.4%", "2026"],
        ["Rows Analyzed", "Tools Mastered", "Student Pass Rate Found", "Learning Since"]):
        col.markdown(f"""
        <div class='stat-card'>
          <div class='stat-num'>{num}</div>
          <div class='stat-label'>{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    # About
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">// about</div><p class="sec-title">Who I Am</p>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class='about-box'><strong>🎯 My Goal</strong><br>
        Building data science skills from the ground up — Python, analysis, and ML to solve real-world problems.</div>
        <div class='about-box'><strong>🐍 What I Know</strong><br>
        Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Git, SQL, Scikit-learn.</div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class='about-box'><strong>📚 How I Learn</strong><br>
        I learn by building real projects, writing about discoveries, and sharing everything on GitHub.</div>
        <div class='about-box'><strong>🚀 What's Next</strong><br>
        Deep learning with PyTorch, advanced SQL, Kaggle competitions, and open-source contributions.</div>
        """, unsafe_allow_html=True)

    # Skills snapshot
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">// skills snapshot</div>', unsafe_allow_html=True)
    for skill, pct in SKILLS.items():
        st.markdown(f"""
        <div class='skill-row'>
          <div class='skill-top'>
            <span class='skill-name'>{skill}</span>
            <span class='skill-pct'>{pct}%</span>
          </div>
          <div class='skill-track'><div class='skill-fill' style='width:{pct}%'></div></div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════════════════════
elif page == "Projects":
    st.markdown('<div class="sec-eyebrow">// work</div><p class="sec-title">Projects</p>', unsafe_allow_html=True)

    # Tag filter
    all_tags = ["All"] + sorted(set(t for p in PROJECTS for t in p["tags"]))
    st.markdown('<div style="margin-bottom: 1rem;">', unsafe_allow_html=True)
    cols = st.columns(len(all_tags))
    for i, tag in enumerate(all_tags):
        with cols[i]:
            if st.button(tag, key=f"tag_{tag}",
                         type="primary" if st.session_state.tag_filter == tag else "secondary"):
                st.session_state.tag_filter = tag
                st.rerun()

    filtered = PROJECTS if st.session_state.tag_filter == "All" else \
        [p for p in PROJECTS if st.session_state.tag_filter in p["tags"]]

    for idx, p in enumerate(filtered):
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in p["tags"])
        with st.container():
            st.markdown(f"<div class='proj-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.6, 1])
            with col1:
                st.markdown(f"""
                <p class='proj-meta'>{p['year']} · {p['tags'][0]}</p>
                <h3 class='proj-title'>{p['title']}</h3>
                <div style='margin-bottom:12px'>{tags_html}</div>
                <table style='font-size:12px;color:#4a6080;width:100%;border-collapse:collapse'>
                  <tr><td style='color:#2a3a55;padding:3px 8px 3px 0;vertical-align:top;white-space:nowrap'>Problem</td>
                      <td style='color:#8899bb;padding:3px 0'>{p['problem']}</td></tr>
                  <tr><td style='color:#2a3a55;padding:3px 8px 3px 0;vertical-align:top'>Method</td>
                      <td style='color:#8899bb;padding:3px 0'>{p['method']}</td></tr>
                  <tr><td style='color:#2a3a55;padding:3px 8px 3px 0;vertical-align:top'>Result</td>
                      <td style='color:#34d399;padding:3px 0'>{p['result']}</td></tr>
                </table>
                """, unsafe_allow_html=True)
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.link_button("🔗 GitHub", p["github"])
                with sc2:
                    if st.button("✨ AI Summary", key=f"ai_sum_{idx}"):
                        with st.spinner("Generating..."):
                            summary = ai_summarize_project(p)
                        st.info(summary)
            with col2:
                figs = make_chart(p, idx)
                for f in figs:
                    st.plotly_chart(f, use_container_width=True, key=f"proj_{idx}_{figs.index(f)}")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SKILLS
# ══════════════════════════════════════════════════════════════════
elif page == "Skills":
    st.markdown('<div class="sec-eyebrow">// abilities</div><p class="sec-title">Skills Dashboard</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Core Skills")
        for skill, pct in SKILLS.items():
            st.markdown(f"""
            <div class='skill-row'>
              <div class='skill-top'>
                <span class='skill-name'>{skill}</span>
                <span class='skill-pct'>{pct}%</span>
              </div>
              <div class='skill-track'><div class='skill-fill' style='width:{pct}%'></div></div>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Currently Learning 🔥")
        for item in ["Machine Learning basics", "Scikit-learn pipelines", "Feature engineering", "Model evaluation metrics"]:
            st.markdown(f"<span class='badge badge-purple'>⚡ {item}</span>", unsafe_allow_html=True)
        st.markdown("<br>#### Next Goals 🎯")
        for item in ["Deep Learning (PyTorch)", "SQL advanced queries", "Kaggle competitions", "Data Engineering"]:
            st.markdown(f"<span class='badge badge-amber'>🎯 {item}</span>", unsafe_allow_html=True)
        st.markdown("<br>#### Tools ✅")
        tools = ["Python", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Plotly", "Streamlit", "Scikit-learn", "Git", "Jupyter", "VS Code"]
        st.markdown(" ".join(f"<span class='badge badge-green'>✓ {t}</span>" for t in tools), unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    cats = list(SKILLS.keys())
    vals = list(SKILLS.values())
    fig = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", line_color="#3b82f6",
        fillcolor="rgba(59,130,246,0.1)"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], color="#4a6080"),
                   angularaxis=dict(color="#4a6080"),
                   bgcolor="rgba(0,0,0,0)"),
        showlegend=False, height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8899bb"),
        margin=dict(l=50, r=50, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True, key="radar_chart")

# ══════════════════════════════════════════════════════════════════
# TIMELINE
# ══════════════════════════════════════════════════════════════════
elif page == "Timeline":
    st.markdown('<div class="sec-eyebrow">// journey</div><p class="sec-title">Learning Timeline</p>', unsafe_allow_html=True)
    for i, item in enumerate(TIMELINE):
        is_last = i == len(TIMELINE) - 1
        st.markdown(f"""
        <div class='timeline-item'>
          {'<div class="timeline-line"></div>' if not is_last else ''}
          <div class='timeline-dot'>{item['icon']}</div>
          <div class='timeline-content'>
            <div class='timeline-date'>{item['date']}</div>
            <div class='timeline-title'>{item['title']}</div>
            <div class='timeline-desc'>{item['desc']}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-eyebrow">// page analytics</div>', unsafe_allow_html=True)
    pages = list(st.session_state.page_views.keys())
    views = list(st.session_state.page_views.values())
    fig = px.bar(x=pages, y=views, color=views,
                 color_continuous_scale="Blues",
                 labels={"x": "Page", "y": "Views"},
                 title="Session Page Views")
    style_fig(fig)
    st.plotly_chart(fig, use_container_width=True, key="analytics_chart")

# ══════════════════════════════════════════════════════════════════
# BLOG
# ══════════════════════════════════════════════════════════════════
elif page == "Blog":
    st.markdown('<div class="sec-eyebrow">// notes</div><p class="sec-title">Blog & Learning Notes</p>', unsafe_allow_html=True)
    for post in BLOG_POSTS:
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in post["tags"])
        with st.expander(f"📄  {post['title']}   ·   {post['date']}"):
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown(f"""
            <div class='blog-body-inner'>
              {post['body']}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# DATA PLAYGROUND
# ══════════════════════════════════════════════════════════════════
elif page == "Playground":
    st.markdown('<div class="sec-eyebrow">// interactive</div><p class="sec-title">Data Playground</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='dp-card'>
      <div style='font-size:13px; color:#4a6080; line-height:1.7'>
        Upload any CSV file and get instant EDA — shape, data types, missing values,
        distributions, correlations, and smart charts. No code needed.
      </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop a CSV file", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown('<div class="sec-eyebrow">// dataset overview</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        for col, val, lbl in zip([m1, m2, m3, m4],
            [df.shape[0], df.shape[1], df.isnull().sum().sum(), df.select_dtypes(include=np.number).shape[1]],
            ["Rows", "Columns", "Missing Values", "Numeric Cols"]):
            col.markdown(f"""
            <div class='stat-card'>
              <div class='stat-num'>{val:,}</div>
              <div class='stat-label'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["📋 Data Preview", "📊 Auto Charts"])
        with t1:
            st.dataframe(df.head(50), use_container_width=True)
            buf = io.StringIO()
            df.info(buf=buf)
            st.markdown(f"<pre style='background:#080f1e;border:1px solid #1a2744;border-radius:10px;padding:12px;font-size:11px;color:#4a6080;font-family:JetBrains Mono,monospace'>{buf.getvalue()}</pre>", unsafe_allow_html=True)
        with t2:
            figs = auto_eda(df)
            if not figs:
                st.info("No numeric columns found to chart.")
            for i in range(0, len(figs), 2):
                fc1, fc2 = st.columns(2)
                with fc1:
                    st.plotly_chart(figs[i][1], use_container_width=True, key=f"eda_{i}")
                if i + 1 < len(figs):
                    with fc2:
                        st.plotly_chart(figs[i + 1][1], use_container_width=True, key=f"eda_{i+1}")
    else:
        st.markdown("""
        <div style='text-align:center; padding: 3rem; color: #2a3a55;
             border: 1px dashed #1a2744; border-radius: 12px; margin-top: 1rem;'>
          <div style='font-size: 2.5rem; margin-bottom: 12px;'>📂</div>
          <div style='font-family: JetBrains Mono, monospace; font-size: 12px;'>
            Drag & drop a CSV file above
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# AI CHAT
# ══════════════════════════════════════════════════════════════════
elif page == "AI Chat":
    st.markdown('<div class="sec-eyebrow">// powered by claude</div><p class="sec-title">Ask My Portfolio</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='dp-card' style='margin-bottom:1rem'>
      <div style='font-size:13px; color:#4a6080;'>
        Ask anything about Nabin's projects, skills, or background. Powered by Claude AI.
        Try: <em style='color:#3b82f6'>"What ML projects has he done?"</em> or
        <em style='color:#3b82f6'>"How many rows did he analyze?"</em>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Chat display
    if st.session_state.chat_history:
        chat_html = "<div class='chat-wrap'>"
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"<div class='chat-label user'>you</div><div class='chat-msg-user'>{msg['content']}</div>"
            else:
                chat_html += f"<div class='chat-label ai'>nabin-ai</div><div class='chat-msg-ai'>{msg['content']}</div>"
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='chat-wrap' style='text-align:center; color:#2a3a55; padding: 2rem;'>
          <div style='font-size:1.8rem; margin-bottom:8px'>🤖</div>
          <div style='font-family: JetBrains Mono, monospace; font-size: 11px;'>
            Start the conversation below
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Your message", placeholder="What projects has Nabin built?", label_visibility="collapsed", key="chat_input")
    with col2:
        send = st.button("Send ↗", type="primary", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner(""):
            reply = ai_chat(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    # Quick prompts
    st.markdown("<br><div style='font-size:11px; color:#2a3a55; font-family: JetBrains Mono, monospace; margin-bottom:8px'>QUICK QUESTIONS</div>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    qs = ["What ML projects?", "What tools do you use?", "How many rows analyzed?", "Are you open to work?"]
    for col, q in zip([q1, q2, q3, q4], qs):
        with col:
            if st.button(q, key=f"quick_{q}"):
                st.session_state.chat_history.append({"role": "user", "content": q})
                with st.spinner(""):
                    reply = ai_chat(q)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

# ══════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown('<div class="sec-eyebrow">// get in touch</div><p class="sec-title">Contact</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"""
        <div class='contact-card'>
          <h3 style='color:#e8f0ff; margin-bottom: 6px'>Let's connect 👋</h3>
          <p style='color:#4a6080; font-size:14px; margin-bottom:20px'>
            Open to feedback, collaboration, or just chatting about data science.
          </p>
          <a class='contact-link' href='mailto:{EMAIL}'>
            <span class='contact-icon'>📧</span> {EMAIL}
          </a>
          <a class='contact-link' href='{LINKEDIN}'>
            <span class='contact-icon'>🔗</span> linkedin.com/in/nabin-kumar-thing
          </a>
          <a class='contact-link' href='{GITHUB}' style='border:none'>
            <span class='contact-icon'>💻</span> github.com/{GITHUB_USER}
          </a>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("#### Send a message")
        name    = st.text_input("Name",  key="c_name", placeholder="Your name")
        email   = st.text_input("Email", key="c_email", placeholder="your@email.com")
        message = st.text_area("Message", height=110, key="c_msg", placeholder="Hi Nabin, I'd like to...")
        if st.button("Send Message 🚀", type="primary"):
            if name and email and message:
                st.success(f"✅ Thanks {name}! I'll reply to {email} soon.")
                st.balloons()
            else:
                st.warning("Please fill in all fields.")

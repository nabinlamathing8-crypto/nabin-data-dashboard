import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import io

# ── Anthropic (optional — only if installed + key present) ────────────────────
try:
    from anthropic import Anthropic as _Anthropic
    _ANTHROPIC_LIB = True
except ImportError:
    _ANTHROPIC_LIB = False

# ── Constants ─────────────────────────────────────────────────────────────────
GITHUB_USER = "nabinlamathing8-crypto"
GITHUB_REPO = "nabin-data-dashboard"
GITHUB      = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}"
LINKEDIN    = "https://www.linkedin.com/in/nabin-kumar-thing-b92406393"
EMAIL       = "nabinlamathing8@gmail.com"

try:
    ANTHROPIC_KEY = st.secrets.get("ANTHROPIC_API_KEY", "")
except Exception:
    ANTHROPIC_KEY = ""

client = _Anthropic(api_key=ANTHROPIC_KEY) if (_ANTHROPIC_LIB and ANTHROPIC_KEY) else None

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nabin · Data Science",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #050a14; }

[data-testid="stSidebar"] { background: #070d1a !important; border-right: 1px solid #131f35; }
[data-testid="stSidebar"] * { color: #6b82a8 !important; }

.main .block-container { background: #050a14; padding-top: 2rem; }
.stApp { background: #050a14; }
h1,h2,h3,h4 { color: #e8f0ff; font-family: 'Inter', sans-serif; }

/* HERO */
.hero-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: #3b82f6; letter-spacing: 0.2em;
  text-transform: uppercase; margin-bottom: 14px; display: block;
}
.hero-name {
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  font-weight: 800; line-height: 1.05;
  letter-spacing: -0.025em; margin: 0 0 10px; color: #ffffff;
}
.hero-name span {
  background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-role { font-size: 1.05rem; color: #4a6080; margin-bottom: 24px; line-height: 1.65; }

/* STATUS PILL */
.status-pill {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(16,185,129,0.07); border: 1px solid rgba(16,185,129,0.18);
  color: #10b981; border-radius: 99px; padding: 5px 15px;
  font-size: 12px; font-weight: 500; margin-bottom: 28px;
}
.pulse {
  width: 7px; height: 7px; border-radius: 50%; background: #10b981;
  animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.35;transform:scale(0.75)} }

/* SECTION */
.sec-eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px; color: #3b82f6; letter-spacing: 0.15em;
  text-transform: uppercase; margin-bottom: 6px; display: block;
}
.sec-title { font-size: 1.65rem; font-weight: 700; color: #e8f0ff; margin-bottom: 1.3rem; line-height: 1.2; }

/* STAT CARDS */
.stat-card { background: #080f1e; border: 1px solid #131f35; border-radius: 12px; padding: 18px 14px; text-align: center; }
.stat-num { font-family: 'JetBrains Mono', monospace; font-size: 1.75rem; font-weight: 700; color: #fff; }
.stat-lbl { font-size: 10px; color: #2e4060; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 5px; }

/* GITHUB STAT */
.gh-stat { background: #080f1e; border: 1px solid #131f35; border-radius: 10px; padding: 14px; text-align: center; }
.gh-num { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 700; color: #fff; }
.gh-lbl { font-size: 10px; color: #2e4060; margin-top: 4px; }

/* PROJECT CARDS */
.proj-card {
  background: #080f1e; border: 1px solid #131f35;
  border-radius: 16px; padding: 1.6rem; margin-bottom: 1.2rem;
  position: relative; transition: border-color 0.2s, transform 0.18s;
}
.proj-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, #3b82f6 50%, transparent);
  border-radius: 16px 16px 0 0;
}
.proj-card:hover { border-color: #1e3a6e; transform: translateY(-2px); }
.proj-title { font-size: 1.05rem; font-weight: 700; color: #e8f0ff; margin: 0 0 8px; }
.proj-meta { font-size: 12px; color: #2e4060; margin-bottom: 10px; font-family: 'JetBrains Mono', monospace; }

/* BADGES */
.badge {
  display: inline-block; background: #0a1628; color: #4d8ef7;
  border: 1px solid #1a3060; border-radius: 6px;
  padding: 2px 10px; font-size: 11px; font-weight: 500; margin: 2px;
  font-family: 'JetBrains Mono', monospace;
}
.badge-green  { background: #061510; color: #34d399; border-color: #0a2e1e; }
.badge-purple { background: #10082a; color: #a78bfa; border-color: #231050; }
.badge-amber  { background: #160f00; color: #fbbf24; border-color: #2e2000; }

/* SKILL BARS */
.skill-row { margin-bottom: 16px; }
.skill-top { display: flex; justify-content: space-between; margin-bottom: 6px; }
.skill-name { font-size: 13px; color: #8899bb; font-weight: 500; }
.skill-pct  { font-size: 12px; color: #3b82f6; font-family: 'JetBrains Mono', monospace; font-weight: 700; }
.skill-track { background: #0d1a2e; border-radius: 99px; height: 6px; overflow: hidden; }
.skill-fill  { height: 6px; border-radius: 99px; background: linear-gradient(90deg, #2563eb, #7c3aed); }

/* TIMELINE */
.timeline-item { display: flex; gap: 16px; margin-bottom: 24px; position: relative; }
.timeline-dot  {
  width: 36px; height: 36px; border-radius: 50%;
  background: #0d1f3c; border: 2px solid #3b82f6;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; flex-shrink: 0; z-index: 1;
}
.timeline-line {
  position: absolute; left: 17px; top: 36px; width: 2px; height: calc(100% + 8px);
  background: linear-gradient(to bottom, #1a2744, transparent);
}
.timeline-content { padding-top: 4px; }
.timeline-date  { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #3b82f6; margin-bottom: 4px; }
.timeline-title { font-size: 14px; font-weight: 600; color: #e8f0ff; margin-bottom: 4px; }
.timeline-desc  { font-size: 13px; color: #4a6080; line-height: 1.5; }

/* BLOG */
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

/* CHAT */
.chat-wrap {
  background: #080f1e; border: 1px solid #1a2744;
  border-radius: 16px; padding: 1.2rem; max-height: 440px; overflow-y: auto;
}
.chat-msg-user {
  background: #0d1f3c; border: 1px solid #1a3060;
  border-radius: 12px 12px 4px 12px; padding: 10px 14px;
  margin: 8px 0 8px 20%; font-size: 13px; color: #c8d8ff;
}
.chat-msg-ai {
  background: #0a1220; border: 1px solid #1a2744;
  border-radius: 12px 12px 12px 4px; padding: 10px 14px;
  margin: 8px 20% 8px 0; font-size: 13px; color: #8899bb; line-height: 1.7;
}
.chat-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; margin-bottom: 2px; }
.chat-label.user { color: #3b82f6; text-align: right; margin-right: 4px; }
.chat-label.ai   { color: #10b981; margin-left: 4px; }

/* ABOUT BOXES */
.about-box {
  background: #080f1e; border: 1px solid #1a2744; border-left: 3px solid #3b82f6;
  border-radius: 0 10px 10px 0; padding: 1rem 1.2rem; margin-bottom: 1rem;
  font-size: 14px; color: #8899bb; line-height: 1.7;
}
.about-box strong { color: #e8f0ff; }

/* CONTACT */
.contact-card { background: #080f1e; border: 1px solid #1a2744; border-radius: 16px; padding: 2rem; margin-bottom: 1rem; }
.contact-link {
  display: flex; align-items: center; gap: 10px;
  color: #8899bb; text-decoration: none; font-size: 14px;
  padding: 10px 0; border-bottom: 1px solid #0d1a2e; transition: color 0.15s;
}
.contact-link:hover { color: #3b82f6; }
.contact-icon { font-size: 18px; width: 24px; }

/* DP CARD */
.dp-card { background: #080f1e; border: 1px solid #1a2744; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem; }

/* INPUTS */
.stTextInput input, .stTextArea textarea {
  background: #080f1e !important; color: #e8f0ff !important; border: 1px solid #1a2744 !important;
}
div[data-testid="stMetricValue"] { color: #ffffff !important; }

/* DIVIDER */
.fancy-divider {
  border: none; height: 1px;
  background: linear-gradient(90deg, transparent, #1a2744, transparent);
  margin: 2rem 0;
}

a { text-decoration: none !important; }
header[data-testid="stHeader"] { background: transparent; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page_views" not in st.session_state:
    st.session_state.page_views = {}
if "tag_filter" not in st.session_state:
    st.session_state.tag_filter = "All"

# ── Data ───────────────────────────────────────────────────────────────────────
SKILLS = {
    "Python": 75, "Pandas": 70, "Matplotlib / Seaborn": 65,
    "Plotly / Streamlit": 60, "SQL": 50, "Scikit-learn (ML)": 45, "Git & GitHub": 55,
}

PROJECTS = [
    {
        "title": "Student Performance Analysis",
        "tags": ["Pandas", "Matplotlib", "Seaborn", "Python"],
        "year": "2026",
        "problem": "Analyzed 500 student records to find what factors most affect academic scores.",
        "method": "6 charts: scatter (hours vs score), grade bars, subject scores, pass/fail pie, GPA histogram, age boxplot.",
        "result": "Avg score 64.1 | Pass rate 88.4% | Students studying 6–9 hrs scored highest.",
        "github": GITHUB, "chart": "student",
    },
    {
        "title": "Heart Attack Incidence Analysis",
        "tags": ["Pandas", "Seaborn", "Healthcare", "Python"],
        "year": "2026",
        "problem": "Analyzed 275,644 patient records to find risk factors across Germany (2015–2023).",
        "method": "6 charts: annual trend, incidence by state, smoking status, stress level, age group, correlation heatmap.",
        "result": "15.01% avg incidence | Top state: Hesse | High stress + poor diet = peak risk.",
        "github": GITHUB, "chart": "heart",
    },
    {
        "title": "BMW Sales + ML Price Prediction",
        "tags": ["Pandas", "Scikit-learn", "ML", "GradientBoosting"],
        "year": "2026",
        "problem": "Analyzed BMW vehicle sales across regions & models, built ML price predictor.",
        "method": "EDA + Random Forest classifier + Gradient Boosting regressor. One-hot encoding, feature engineering.",
        "result": "Electric vehicles trending | Price predictor built with GradientBoostingRegressor.",
        "github": GITHUB, "chart": "bmw",
    },
    {
        "title": "Nepal Household Survey Analysis",
        "tags": ["Pandas", "Seaborn", "Python"],
        "year": "2025",
        "problem": "Understand income distribution and education access across Nepal's provinces.",
        "method": "Cleaned 10,000+ rows, grouped by province, built heatmaps and bar charts.",
        "result": "Province 2 had lowest literacy — gap visualized clearly.",
        "github": GITHUB, "chart": "bar",
    },
    {
        "title": "Nabin Data Dashboard",
        "tags": ["Streamlit", "Plotly", "Python"],
        "year": "2026",
        "problem": "Build a personal data science portfolio showcasing projects and skills interactively.",
        "method": "Multi-page Streamlit app with Plotly charts, AI chatbot, data playground, GitHub live stats.",
        "result": "Live portfolio deployed on Streamlit Cloud.",
        "github": GITHUB, "chart": "scatter",
    },
]

TIMELINE = [
    {"date": "May 2026",          "icon": "📊", "title": "First real data project — Student Analysis",    "desc": "500 rows, 6 charts, learned groupby + matplotlib subplots from scratch."},
    {"date": "May 2026",          "icon": "🧠", "title": "First ML project — BMW price predictor",       "desc": "Random Forest + Gradient Boosting. Learned one-hot encoding and feature engineering."},
    {"date": "June 2026",         "icon": "🏥", "title": "Heart attack analysis (275K rows)",             "desc": "Large real-world healthcare dataset. Learned performance optimization with groupby."},
    {"date": "June 2026",         "icon": "🚀", "title": "Deployed portfolio on Streamlit Cloud",         "desc": "First live web deployment. Added CI/CD pipeline via GitHub."},
    {"date": "June 2026",         "icon": "🤖", "title": "Added AI chatbot to portfolio",                 "desc": "Integrated Claude API. Visitors can now ask about my projects and skills."},
    {"date": "July 2026 (goal)",  "icon": "🎯", "title": "Deep Learning with PyTorch",                   "desc": "CNN image classification. First Kaggle competition entry planned."},
]

BLOG_POSTS = [
    {
        "date": "June 21, 2026", "read": "5 min read",
        "title": "Heart Attack Incidence Analysis — 275,644 Patients, 6 Charts",
        "tags": ["Pandas", "Seaborn", "Real Project", "Healthcare Data"],
        "body": """<h4>The Dataset</h4>
<p>275,644 patient records from Germany (2015–2023). Columns: Year, State, Age_Group, Smoking_Status, Stress_Level, BMI, Hypertension, Heart_Attack_Incidence.</p>
<h4>Key Stats</h4>
<pre>Overall avg incidence: 15.01%
Top risk state:        Hesse
Hypertension rate:     40.1%
Diabetes rate:         20.0%</pre>
<h4>Building the 6-Chart Report</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
annual = df.groupby('Year')['Heart_Attack_Incidence'].mean()
axes[0,0].plot(annual.index, annual.values, color='green', marker='o')
sns.heatmap(df[risk_cols].corr(), annot=True, fmt=".2f", cmap="RdYlGn", ax=axes[1,2])</pre>
<h4>Key Insight</h4>
<p>High stress + poor diet yields the <code>peak</code> incidence combination. Smokers show elevated risk regardless of other factors.</p>""",
    },
    {
        "date": "June 20, 2026", "read": "6 min read",
        "title": "BMW Sales Analysis + ML Price Prediction (2010–2024)",
        "tags": ["Pandas", "Matplotlib", "Scikit-learn", "ML", "Real Project"],
        "body": """<h4>Data Cleaning</h4>
<pre>df["Fuel_Type"] = df["Fuel_Type"].str.replace(r'\\+', '', regex=True).str.strip()
df["Car_Age"] = 2024 - df['Year']</pre>
<h4>Random Forest Classifier</h4>
<pre>from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
print(classification_report(y_test, clf.predict(X_test)))</pre>
<h4>Gradient Boosting Regressor</h4>
<pre>from sklearn.ensemble import GradientBoostingRegressor
reg = GradientBoostingRegressor(n_estimators=200, random_state=42)
print(f"R²: {r2_score(y_test, preds):.3f}")</pre>
<h4>What I Learned</h4>
<p>One-hot encoding text columns is critical. <code>GradientBoostingRegressor</code> outperforms linear regression on real-world pricing data.</p>""",
    },
    {
        "date": "June 21, 2026", "read": "6 min read",
        "title": "Student Performance — From Raw CSV to 6 Charts",
        "tags": ["Pandas", "Matplotlib", "Seaborn", "Real Project"],
        "body": """<h4>Key Stats Computed</h4>
<pre>avg_score  = df['Average_Score'].mean()           # 64.1
pass_rate  = len(df[df['Result']=="Pass"]) / 500  # 88.4%
top_grade  = df['Grade'].value_counts().idxmax()  # B</pre>
<h4>All 6 Charts in One Figure</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes[0,0].scatter(df['Hours_Studied'], df['Average_Score'], color='green')
axes[1,0].pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')
sns.boxplot(data=df, x='Age', y='Average_Score', ax=axes[1,2], palette='Greens')</pre>
<h4>Biggest Insight</h4>
<p>Students studying <code>6–9 hours</code> scored highest. Below 4 hours → much lower scores. A clear signal in the data.</p>""",
    },
    {
        "date": "June 15, 2026", "read": "4 min read",
        "title": "Cleaning Messy Survey Data with Pandas",
        "tags": ["Pandas", "Data Cleaning"],
        "body": """<h4>4-Step Pipeline</h4>
<pre># Step 1 — Fix column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Step 2 — Handle missing values
df["income"].fillna(df["income"].median(), inplace=True)
df.dropna(subset=["province", "age"], inplace=True)

# Step 3 — Remove duplicates
df.drop_duplicates(inplace=True)

# Result: 10,847 → 10,203 clean rows</pre>
<p>Always clean before you visualize. That 644-row difference contained 3 different error types.</p>""",
    },
    {
        "date": "May 28, 2026", "read": "3 min read",
        "title": "My first Seaborn heatmap — 3 mistakes I made",
        "tags": ["Seaborn", "Visualization"],
        "body": """<h4>The code that finally worked</h4>
<pre>corr = df[["study_hours","attendance","sleep","score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, square=True)</pre>
<h4>Mistake 1 — forgot .corr()</h4>
<p>Pass the correlation matrix, not the raw dataframe.</p>
<h4>Mistake 2 — no fmt=".2f"</h4>
<p>Without it: <code>0.7283746...</code> — always add fmt.</p>
<h4>Mistake 3 — wrong colormap</h4>
<p><code>"rainbow"</code> looks colorful but is hard to read. Use <code>"Blues"</code> or <code>"coolwarm"</code>.</p>
<p><strong>Biggest insight:</strong> Study hours vs score = 0.81 correlation. Very strong.</p>""",
    },
    {
        "date": "May 10, 2026", "read": "5 min read",
        "title": "Linear regression explained simply",
        "tags": ["ML", "Scikit-learn"],
        "body": """<h4>What is it?</h4>
<p>Drawing the best straight line through your data: <code>score = m × hours + b</code></p>
<h4>Code</h4>
<pre>from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

model = LinearRegression()
model.fit(X_train, y_train)
print(f"R² score: {r2_score(y_test, model.predict(X_test)):.2f}")</pre>
<p>My model got R² = 0.82 — study hours explain 82% of score variation.</p>
<h4>Predict a new student</h4>
<pre>model.predict([[7]])  # 7 study hours → predicted score</pre>""",
    },
]

PORTFOLIO_CONTEXT = """You are an AI assistant on Nabin Kumar Thing's data science portfolio website.
Nabin is an aspiring data scientist from Nepal.

Projects:
1. Student Performance Analysis — 500 records, 88.4% pass rate, study hours vs score correlation
2. Heart Attack Incidence Analysis — 275,644 German patient records, 15.01% avg incidence
3. BMW Sales + ML Price Prediction — Random Forest + Gradient Boosting regressor
4. Nepal Household Survey — 10,000+ rows, province-level literacy and income analysis
5. This portfolio — Streamlit app with AI chat, data playground, GitHub stats, deployed on Streamlit Cloud

Skills: Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, SQL, Scikit-learn, Git
Email: nabinlamathing8@gmail.com | GitHub: github.com/nabinlamathing8-crypto

Answer questions about Nabin's work concisely and helpfully. Keep answers under 150 words unless asked for detail."""

# ── Helpers ────────────────────────────────────────────────────────────────────
def fetch_github_stats():
    try:
        r = requests.get(f"https://api.github.com/users/{GITHUB_USER}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {"repos": d.get("public_repos", "8+"), "followers": d.get("followers", "—"), "following": d.get("following", "—")}
    except Exception:
        pass
    return {"repos": "8+", "followers": "—", "following": "—"}

def style_fig(fig, h=185):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a6080", size=10), height=h,
        margin=dict(l=8, r=8, t=30, b=8),
        showlegend=False, coloraxis_showscale=False,
        title_font=dict(color="#8899bb", size=11),
    )
    fig.update_xaxes(gridcolor="#0d1a2e", color="#4a6080")
    fig.update_yaxes(gridcolor="#0d1a2e", color="#4a6080")

def ai_chat(user_msg):
    if not client:
        return "⚠️ AI chat not available — add ANTHROPIC_API_KEY to Streamlit secrets to enable."
    msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[-8:]]
    msgs.append({"role": "user", "content": user_msg})
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=400,
        system=PORTFOLIO_CONTEXT, messages=msgs
    )
    return resp.content[0].text

def ai_summarize_project(project):
    if not client:
        return "Add ANTHROPIC_API_KEY to Streamlit secrets to enable AI summaries."
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=120,
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
        fig = px.scatter(x=hours, y=sc, height=180, labels={"x": "Hours", "y": "Score"},
                         title="Study hrs vs Score", color=sc, color_continuous_scale="Blues")
        fig.update_traces(marker=dict(size=3))
        style_fig(fig); return [fig]
    elif p["chart"] == "heart":
        years = list(range(2015, 2024))
        rates = [0.1487, 0.1494, 0.1534, 0.1471, 0.1519, 0.1519, 0.1510, 0.1498, 0.1471]
        fig = px.area(x=years, y=rates, height=180, title="Incidence Trend",
                      color_discrete_sequence=["#3b82f6"])
        style_fig(fig); return [fig]
    elif p["chart"] == "bmw":
        years = list(range(2010, 2025))
        prices = [28000 + i * 800 + np.random.randint(-500, 500) for i in range(15)]
        fig = px.line(x=years, y=prices, markers=True, height=180, title="BMW Avg Price",
                      color_discrete_sequence=["#8b5cf6"])
        style_fig(fig); return [fig]
    elif p["chart"] == "bar":
        df_n = pd.DataFrame({"Province": [f"P{i}" for i in range(1, 8)],
                             "Literacy": np.random.randint(55, 90, 7)})
        fig = px.bar(df_n, x="Province", y="Literacy", height=180, title="Literacy by Province",
                     color="Literacy", color_continuous_scale="Blues")
        style_fig(fig); return [fig]
    else:
        df_s = pd.DataFrame({"Study": np.random.randint(1, 10, 50), "Score": np.random.randint(40, 100, 50)})
        fig = px.scatter(df_s, x="Study", y="Score", height=180, title="Study vs Score",
                         color="Score", color_continuous_scale="Blues")
        style_fig(fig); return [fig]

def build_eda_package(df):
    """
    Returns a dict with:
      summary   – dict of stat strings ready to render
      charts    – list of (tab_label, chart_type, fig) tuples
    """
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    # ── Summary stats ──────────────────────────────────────────────
    summary = {}
    summary["shape"]       = f"{df.shape[0]:,} rows × {df.shape[1]} columns"
    summary["num_cols"]    = num_cols
    summary["cat_cols"]    = cat_cols
    summary["missing"]     = int(df.isnull().sum().sum())
    summary["missing_pct"] = f"{df.isnull().mean().mean()*100:.1f}%"
    summary["duplicates"]  = int(df.duplicated().sum())
    summary["dtypes"]      = df.dtypes.value_counts().to_dict()

    # Per-column missing
    col_missing = df.isnull().sum()
    summary["col_missing"] = col_missing[col_missing > 0].to_dict()

    # Numeric describe
    if num_cols:
        desc = df[num_cols].describe().round(3)
        summary["describe"] = desc
    else:
        summary["describe"] = None

    # ── Charts ─────────────────────────────────────────────────────
    charts = []   # (section, label, fig)

    # 1. Correlation heatmap
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                        color_continuous_scale="RdBu_r",
                        title="Correlation Heatmap",
                        zmin=-1, zmax=1)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="#4a6080", size=10), height=320,
                          margin=dict(l=8,r=8,t=36,b=8),
                          title_font=dict(color="#8899bb", size=12),
                          coloraxis_colorbar=dict(tickfont=dict(color="#4a6080")))
        charts.append(("📊 Heatmap", "heatmap", fig))

    # 2. Histograms for every numeric col
    for col in num_cols:
        fig = px.histogram(df, x=col, nbins=35,
                           color_discrete_sequence=["#3b82f6"],
                           title=f"Histogram — {col}",
                           marginal="box")
        style_fig(fig)
        fig.update_layout(height=220)
        charts.append(("📈 Histograms", f"hist_{col}", fig))

    # 3. Box plots for every numeric col
    for col in num_cols:
        fig = px.box(df, y=col, color_discrete_sequence=["#8b5cf6"],
                     title=f"Box Plot — {col}", points="outliers")
        style_fig(fig)
        fig.update_layout(height=220)
        charts.append(("📦 Box Plots", f"box_{col}", fig))

    # 4. Bar charts for every categorical col
    for col in cat_cols:
        vc = df[col].value_counts().head(15)
        fig = px.bar(x=vc.index.astype(str), y=vc.values,
                     labels={"x": col, "y": "Count"},
                     color=vc.values, color_continuous_scale="Blues",
                     title=f"Bar Chart — {col} (top 15)")
        style_fig(fig)
        fig.update_layout(height=250)
        charts.append(("📊 Bar Charts", f"bar_{col}", fig))

    # 5. Pie charts for low-cardinality categorical cols (≤ 12 unique)
    for col in cat_cols:
        n_unique = df[col].nunique()
        if n_unique <= 12:
            vc = df[col].value_counts()
            fig = px.pie(values=vc.values, names=vc.index.astype(str),
                         title=f"Pie Chart — {col}",
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_traces(textinfo="percent+label",
                              hovertemplate="%{label}: %{value} (%{percent})<extra></extra>")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",
                              font=dict(color="#4a6080", size=10), height=280,
                              margin=dict(l=8,r=8,t=36,b=8), showlegend=False,
                              title_font=dict(color="#8899bb", size=12))
            charts.append(("🥧 Pie Charts", f"pie_{col}", fig))

    # 6. Scatter plots for every numeric pair (up to 6 pairs)
    pairs = [(num_cols[i], num_cols[j])
             for i in range(len(num_cols))
             for j in range(i+1, len(num_cols))][:6]
    for (cx, cy) in pairs:
        color_col = cat_cols[0] if cat_cols else None
        if color_col and df[color_col].nunique() <= 15:
            fig = px.scatter(df, x=cx, y=cy, color=color_col,
                             title=f"Scatter — {cx} vs {cy}",
                             opacity=0.7)
        else:
            fig = px.scatter(df, x=cx, y=cy,
                             color=cy, color_continuous_scale="Blues",
                             title=f"Scatter — {cx} vs {cy}",
                             opacity=0.7)
        fig.update_traces(marker=dict(size=5))
        style_fig(fig)
        fig.update_layout(height=250)
        charts.append(("🔵 Scatter Plots", f"scatter_{cx}_{cy}", fig))

    # 7. Line chart for time-like or ordered numeric (first numeric as x if >20 rows)
    if len(num_cols) >= 2 and len(df) >= 10:
        x_col = num_cols[0]
        df_sorted = df.sort_values(x_col)
        for y_col in num_cols[1:4]:
            fig = px.line(df_sorted, x=x_col, y=y_col,
                          title=f"Line — {y_col} over {x_col}",
                          color_discrete_sequence=["#06b6d4"])
            style_fig(fig)
            fig.update_layout(height=220)
            charts.append(("📉 Line Charts", f"line_{x_col}_{y_col}", fig))

    # 8. Violin plots for numeric (grouped by cat if available)
    if num_cols:
        for nc in num_cols[:3]:
            if cat_cols and df[cat_cols[0]].nunique() <= 10:
                fig = px.violin(df, y=nc, x=cat_cols[0], box=True,
                                color=cat_cols[0],
                                title=f"Violin — {nc} by {cat_cols[0]}")
            else:
                fig = px.violin(df, y=nc, box=True,
                                color_discrete_sequence=["#3b82f6"],
                                title=f"Violin — {nc}")
            style_fig(fig)
            fig.update_layout(height=240, showlegend=False)
            charts.append(("🎻 Violin Plots", f"violin_{nc}", fig))

    return summary, charts


def generate_python_report(df, summary, filename="dataset.csv"):
    """
    Builds a complete EDA report from pure Python/Pandas — no API key needed.
    100% matched to the actual uploaded file.
    """
    num_cols = summary["num_cols"]
    cat_cols = summary["cat_cols"]
    lines = []
    a = lines.append

    a(f"EDA REPORT — {filename.upper()}")
    a("=" * 60)
    a(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")
    a("")

    # ── Section 1: Overview ──────────────────────────────────────
    a("## 1. DATASET OVERVIEW")
    a(f"  File            : {filename}")
    a(f"  Shape           : {df.shape[0]:,} rows × {df.shape[1]} columns")
    a(f"  Numeric columns : {len(num_cols)}  → {', '.join(num_cols) if num_cols else 'none'}")
    a(f"  Categorical cols: {len(cat_cols)}  → {', '.join(cat_cols) if cat_cols else 'none'}")
    a(f"  Missing values  : {summary['missing']:,} cells ({summary['missing_pct']})")
    a(f"  Duplicate rows  : {summary['duplicates']:,}")
    a(f"  Memory usage    : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    a("")

    # ── Section 2: Data Quality ──────────────────────────────────
    a("## 2. DATA QUALITY ASSESSMENT")
    if summary["col_missing"]:
        a("  Columns with missing values:")
        for col, cnt in sorted(summary["col_missing"].items(), key=lambda x: -x[1]):
            pct = cnt / len(df) * 100
            a(f"    • {col:<30} {cnt:>6,} missing  ({pct:.1f}%)")
    else:
        a("  ✓ No missing values found — dataset is complete.")
    a(f"  ✓ Duplicates: {summary['duplicates']} row(s)")
    a(f"  Column dtypes: { {str(k): int(v) for k,v in summary['dtypes'].items()} }")
    a("")

    # ── Section 3: Numeric Stats ─────────────────────────────────
    if num_cols:
        a("## 3. NUMERIC COLUMN STATISTICS")
        desc = df[num_cols].describe()
        for col in num_cols:
            s = desc[col]
            skew = df[col].skew()
            kurt = df[col].kurtosis()
            q1   = s["25%"]; q3 = s["75%"]; iqr = q3 - q1
            outliers = int(((df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)).sum())
            a(f"  ── {col}")
            a(f"     Count   : {int(s['count']):,}   |  Nulls: {int(df[col].isnull().sum()):,}")
            a(f"     Mean    : {s['mean']:.4f}   |  Std Dev: {s['std']:.4f}")
            a(f"     Min     : {s['min']:.4f}   |  Max: {s['max']:.4f}")
            a(f"     Q1      : {q1:.4f}   |  Median: {s['50%']:.4f}   |  Q3: {q3:.4f}")
            a(f"     IQR     : {iqr:.4f}   |  Outliers (IQR): {outliers}")
            a(f"     Skewness: {skew:.4f}   |  Kurtosis: {kurt:.4f}")
            skew_note = "right-skewed (tail right)" if skew > 0.5 else "left-skewed (tail left)" if skew < -0.5 else "approximately symmetric"
            a(f"     Shape   : {skew_note}")
            a("")

    # ── Section 4: Categorical Stats ────────────────────────────
    if cat_cols:
        a("## 4. CATEGORICAL COLUMN ANALYSIS")
        for col in cat_cols:
            vc = df[col].value_counts()
            top3 = vc.head(3)
            a(f"  ── {col}")
            a(f"     Unique values : {df[col].nunique():,}")
            a(f"     Missing       : {df[col].isnull().sum():,}")
            a(f"     Most common   : {top3.index[0]} ({top3.iloc[0]:,} rows, {top3.iloc[0]/len(df)*100:.1f}%)")
            if len(top3) > 1:
                a(f"     2nd           : {top3.index[1]} ({top3.iloc[1]:,} rows, {top3.iloc[1]/len(df)*100:.1f}%)")
            if len(top3) > 2:
                a(f"     3rd           : {top3.index[2]} ({top3.iloc[2]:,} rows, {top3.iloc[2]/len(df)*100:.1f}%)")
            a("")

    # ── Section 5: Correlations ──────────────────────────────────
    if len(num_cols) >= 2:
        a("## 5. CORRELATION ANALYSIS")
        corr = df[num_cols].corr()
        # Find strongest pairs
        pairs = []
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                c1, c2 = num_cols[i], num_cols[j]
                r = corr.loc[c1, c2]
                pairs.append((abs(r), r, c1, c2))
        pairs.sort(reverse=True)
        a("  Strongest correlations:")
        for _, r, c1, c2 in pairs[:8]:
            strength = "strong" if abs(r) > 0.7 else "moderate" if abs(r) > 0.4 else "weak"
            direction = "positive" if r > 0 else "negative"
            a(f"    • {c1}  ↔  {c2}:  r = {r:.3f}  ({strength} {direction})")
        a("")

    # ── Section 6: Recommendations ──────────────────────────────
    a("## 6. RECOMMENDATIONS & NEXT STEPS")
    recs = []
    if summary["missing"] > 0:
        recs.append("Handle missing values: use median/mode imputation or drop rows depending on % missing.")
    if summary["duplicates"] > 0:
        recs.append(f"Remove {summary['duplicates']} duplicate row(s) with df.drop_duplicates().")
    for col in num_cols:
        skew = abs(df[col].skew())
        if skew > 1.5:
            recs.append(f"Column '{col}' is highly skewed (skew={skew:.2f}) — consider log transform.")
    if len(num_cols) >= 2:
        for _, r, c1, c2 in pairs[:3]:
            if abs(r) > 0.7:
                recs.append(f"Strong correlation between '{c1}' and '{c2}' (r={r:.2f}) — potential multicollinearity if used in ML.")
    if not recs:
        recs.append("Dataset looks clean. Ready for modeling or deeper analysis.")
    for rec in recs:
        a(f"  → {rec}")
    a("")
    a("=" * 60)
    a("END OF REPORT")

    return "\n".join(lines)


def generate_ai_report(df, summary):
    """Ask Claude to write a full analyst-style report based on the real data."""
    if not client:
        return None
    num_cols  = summary["num_cols"]
    cat_cols  = summary["cat_cols"]
    desc_str  = summary["describe"].to_string() if summary["describe"] is not None else "N/A"
    missing   = summary["col_missing"]
    dups      = summary["duplicates"]

    head_str  = df.head(5).to_string()
    col_types = df.dtypes.to_string()

    prompt = f"""You are a senior data analyst. Analyze this dataset and write a structured EDA report.

DATASET OVERVIEW:
- Shape: {summary['shape']}
- Numeric columns: {num_cols}
- Categorical columns: {cat_cols}
- Missing values: {summary['missing']} ({summary['missing_pct']})
- Duplicate rows: {dups}
- Columns with missing: {missing}

COLUMN DTYPES:
{col_types}

FIRST 5 ROWS:
{head_str}

DESCRIPTIVE STATISTICS:
{desc_str}

Write a professional EDA report with these exact sections (use markdown headers ##):
## 1. Dataset Overview
## 2. Data Quality Assessment
## 3. Key Statistical Insights  
## 4. Column-by-Column Analysis
## 5. Relationships & Correlations
## 6. Recommendations & Next Steps

Be specific — use the actual column names, real numbers from the stats, and give actionable insights.
Keep it concise but data-driven. Max 600 words."""

    try:
        resp = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=900,
            messages=[{"role": "user", "content": prompt}]
        )
        return resp.content[0].text
    except Exception as e:
        return f"Report generation failed: {e}"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem'>
      <div style='font-family:JetBrains Mono,monospace;font-size:9px;color:#3b82f6;letter-spacing:0.18em;margin-bottom:7px'>PORTFOLIO</div>
      <div style='font-size:15px;font-weight:700;color:#e8f0ff'>Nabin Kumar Thing</div>
      <div style='font-size:11px;color:#2e4060;margin-top:2px'>Data Science Learner</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#131f35;margin:10px 0'>", unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["🏠  Home", "💼  Projects", "⚡  Skills", "📅  Timeline",
         "📝  Blog", "🧪  Playground", "🤖  AI Chat", "📬  Contact"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#131f35;margin:10px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:10px;color:#2e4060;font-family:JetBrains Mono,monospace;margin-bottom:8px'>CONNECT</div>
    <a href='{GITHUB}'         style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ GitHub</a>
    <a href='{LINKEDIN}'       style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ LinkedIn</a>
    <a href='mailto:{EMAIL}'   style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ Email</a>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#131f35;margin:10px 0'>", unsafe_allow_html=True)
    clean_page = page.split("  ")[1]
    st.session_state.page_views[clean_page] = st.session_state.page_views.get(clean_page, 0) + 1
    total_views = sum(st.session_state.page_views.values())
    st.markdown(f"""
    <div style='font-size:9px;color:#1a2a40;font-family:JetBrains Mono,monospace'>
      SESSION · {total_views} page views
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
        <span class='hero-eyebrow'>// data scientist in training</span>
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
        <div style='text-align:center;padding:2rem 1rem'>
          <div style='width:120px;height:120px;border-radius:50%;
            background:linear-gradient(135deg,#1e3a8a,#7c3aed);
            display:flex;align-items:center;justify-content:center;
            font-size:3rem;margin:0 auto;
            box-shadow:0 0 0 2px #1a2744,0 0 40px rgba(59,130,246,0.15)'>🧑‍💻</div>
          <div style='margin-top:14px;font-family:JetBrains Mono,monospace;font-size:11px;color:#3b82f6'>
            LEARNING SINCE 2026
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Live GitHub stats
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// github · live stats</span>', unsafe_allow_html=True)
    gh = fetch_github_stats()
    g1, g2, g3, g4, g5 = st.columns(5)
    for col, val, lbl in zip(
        [g1, g2, g3, g4, g5],
        [gh["repos"], gh["followers"], gh["following"], "4+", "275K+"],
        ["Public Repos", "Followers", "Following", "Projects Built", "Rows Analyzed"]
    ):
        col.markdown(f"""
        <div class='gh-stat'>
          <div class='gh-num'>{val}</div>
          <div class='gh-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

    # Quick stats
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// quick stats</span>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)
    for col, num, lbl in zip([s1, s2, s3, s4],
        ["275K+", "7", "88.4%", "2026"],
        ["Rows Analyzed", "Tools Mastered", "Student Pass Rate", "Learning Since"]):
        col.markdown(f"""
        <div class='stat-card'>
          <div class='stat-num'>{num}</div>
          <div class='stat-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

    # About
    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// about</span><p class="sec-title">Who I Am</p>', unsafe_allow_html=True)
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
    st.markdown('<span class="sec-eyebrow">// skills snapshot</span>', unsafe_allow_html=True)
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
    st.markdown('<span class="sec-eyebrow">// work</span><p class="sec-title">Projects</p>', unsafe_allow_html=True)

    all_tags = ["All"] + sorted(set(t for p in PROJECTS for t in p["tags"]))
    filter_cols = st.columns(len(all_tags))
    for i, tag in enumerate(all_tags):
        with filter_cols[i]:
            if st.button(tag, key=f"tag_{tag}",
                         type="primary" if st.session_state.tag_filter == tag else "secondary"):
                st.session_state.tag_filter = tag
                st.rerun()

    filtered = PROJECTS if st.session_state.tag_filter == "All" else \
               [p for p in PROJECTS if st.session_state.tag_filter in p["tags"]]

    for idx, p in enumerate(filtered):
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in p["tags"])
        with st.container():
            st.markdown("<div class='proj-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.6, 1])
            with col1:
                st.markdown(f"""
                <p class='proj-meta'>{p['year']} · {p['tags'][0]}</p>
                <h3 class='proj-title'>{p['title']}</h3>
                <div style='margin-bottom:12px'>{tags_html}</div>
                <table style='font-size:12px;width:100%;border-collapse:collapse'>
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
                for fi, f in enumerate(figs):
                    st.plotly_chart(f, use_container_width=True, key=f"proj_{idx}_{fi}")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SKILLS
# ══════════════════════════════════════════════════════════════════
elif page == "Skills":
    st.markdown('<span class="sec-eyebrow">// abilities</span><p class="sec-title">Skills Dashboard</p>', unsafe_allow_html=True)
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
    cats = list(SKILLS.keys()); vals = list(SKILLS.values())
    fig_radar = go.Figure(go.Scatterpolar(
        r=vals + [vals[0]], theta=cats + [cats[0]],
        fill="toself", line_color="#3b82f6", fillcolor="rgba(59,130,246,0.1)"
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], color="#4a6080"),
                   angularaxis=dict(color="#4a6080"), bgcolor="rgba(0,0,0,0)"),
        showlegend=False, height=420, paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8899bb"), margin=dict(l=50, r=50, t=20, b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")

# ══════════════════════════════════════════════════════════════════
# TIMELINE
# ══════════════════════════════════════════════════════════════════
elif page == "Timeline":
    st.markdown('<span class="sec-eyebrow">// journey</span><p class="sec-title">Learning Timeline</p>', unsafe_allow_html=True)
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
    st.markdown('<span class="sec-eyebrow">// session analytics</span>', unsafe_allow_html=True)
    if st.session_state.page_views:
        pages_list = list(st.session_state.page_views.keys())
        views_list = list(st.session_state.page_views.values())
        fig_pv = px.bar(x=pages_list, y=views_list, color=views_list,
                        color_continuous_scale="Blues",
                        labels={"x": "Page", "y": "Views"},
                        title="Pages visited this session")
        style_fig(fig_pv, 260)
        st.plotly_chart(fig_pv, use_container_width=True, key="analytics_chart")

# ══════════════════════════════════════════════════════════════════
# BLOG
# ══════════════════════════════════════════════════════════════════
elif page == "Blog":
    st.markdown('<span class="sec-eyebrow">// notes</span><p class="sec-title">Blog & Learning Notes</p>', unsafe_allow_html=True)
    for post in BLOG_POSTS:
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in post["tags"])
        with st.expander(f"📄  {post['title']}   —   {post['date']}  ·  {post['read']}"):
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown(f"<div class='blog-body-inner'>{post['body']}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PLAYGROUND
# ══════════════════════════════════════════════════════════════════
elif page == "Playground":
    st.markdown('<span class="sec-eyebrow">// interactive eda</span><p class="sec-title">Data Playground</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='dp-card'>
      <div style='font-size:13px;color:#4a6080;line-height:1.8'>
        Upload any CSV → instant full EDA report. Histograms, scatter plots, bar charts,
        pie charts, box plots, violin plots, line charts, correlation heatmap, missing value
        analysis, and an AI-written analyst report — all matched 100% to your file.
      </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop a CSV file here", type=["csv"], key="pg_upload")

    if uploaded:
        df = pd.read_csv(uploaded)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()

        # ── Top stat bar ──────────────────────────────────────────
        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown('<span class="sec-eyebrow">// dataset overview</span>', unsafe_allow_html=True)
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        missing_total = int(df.isnull().sum().sum())
        missing_pct   = df.isnull().mean().mean() * 100
        dups          = int(df.duplicated().sum())
        for col, val, lbl in zip(
            [m1, m2, m3, m4, m5, m6],
            [df.shape[0], df.shape[1], len(num_cols), len(cat_cols),
             f"{missing_total} ({missing_pct:.1f}%)", dups],
            ["Rows", "Columns", "Numeric Cols", "Categorical Cols", "Missing Values", "Duplicate Rows"]
        ):
            col.markdown(f"""
            <div class='stat-card'>
              <div class='stat-num' style='font-size:1.2rem'>{val}</div>
              <div class='stat-lbl'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Build everything ──────────────────────────────────────
        summary, charts = build_eda_package(df)

        # ── Separate charts into named buckets ────────────────────
        heatmap_charts  = [(l,f) for s,l,f in charts if s == "📊 Heatmap"]
        hist_charts     = [(l,f) for s,l,f in charts if s == "📈 Histograms"]
        box_charts      = [(l,f) for s,l,f in charts if s == "📦 Box Plots"]
        bar_charts      = [(l,f) for s,l,f in charts if s == "📊 Bar Charts"]
        pie_charts      = [(l,f) for s,l,f in charts if s == "🥧 Pie Charts"]
        scatter_charts  = [(l,f) for s,l,f in charts if s == "🔵 Scatter Plots"]
        line_charts     = [(l,f) for s,l,f in charts if s == "📉 Line Charts"]
        violin_charts   = [(l,f) for s,l,f in charts if s == "🎻 Violin Plots"]

        def render_chart_grid(chart_list, key_prefix):
            """Render charts 2-per-row."""
            if not chart_list:
                st.info("No charts available for this column type in your dataset.")
                return
            for i in range(0, len(chart_list), 2):
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(chart_list[i][1], use_container_width=True,
                                    key=f"{key_prefix}_{i}_a")
                if i + 1 < len(chart_list):
                    with c2:
                        st.plotly_chart(chart_list[i+1][1], use_container_width=True,
                                        key=f"{key_prefix}_{i}_b")

        # ── Fixed tab list — always the same order ─────────────────
        (tab_data, tab_stats, tab_hist, tab_box,
         tab_bar, tab_pie, tab_scatter, tab_line,
         tab_violin, tab_heatmap, tab_report) = st.tabs([
            "📋 Data",
            "📊 Summary Stats",
            f"📈 Histograms ({len(hist_charts)})",
            f"📦 Box Plots ({len(box_charts)})",
            f"📊 Bar Charts ({len(bar_charts)})",
            f"🥧 Pie Charts ({len(pie_charts)})",
            f"🔵 Scatter ({len(scatter_charts)})",
            f"📉 Line ({len(line_charts)})",
            f"🎻 Violin ({len(violin_charts)})",
            f"🌡️ Heatmap ({len(heatmap_charts)})",
            "🤖 AI Report",
        ])

        # ── TAB: Data ─────────────────────────────────────────────
        with tab_data:
            st.markdown('<span class="sec-eyebrow">// first 100 rows</span>', unsafe_allow_html=True)
            st.dataframe(df.head(100), use_container_width=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<span class="sec-eyebrow">// column info</span>', unsafe_allow_html=True)
            info_df = pd.DataFrame({
                "Column":   list(df.columns),
                "Dtype":    [str(df[c].dtype) for c in df.columns],
                "Non-Null": [int(df[c].count()) for c in df.columns],
                "Null":     [int(df[c].isnull().sum()) for c in df.columns],
                "Null %":   [f"{df[c].isnull().mean()*100:.1f}%" for c in df.columns],
                "Unique":   [int(df[c].nunique()) for c in df.columns],
                "Sample":   [str(df[c].dropna().iloc[0]) if df[c].count() > 0 else "—" for c in df.columns],
            })
            st.dataframe(info_df, use_container_width=True, hide_index=True)
            if missing_total > 0:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<span class="sec-eyebrow">// missing values per column</span>', unsafe_allow_html=True)
                miss_s = df.isnull().sum()
                miss_s = miss_s[miss_s > 0].sort_values(ascending=False)
                fig_miss = px.bar(x=miss_s.index.tolist(), y=miss_s.values,
                                  labels={"x": "Column", "y": "Missing Count"},
                                  color=miss_s.values, color_continuous_scale="Reds",
                                  title="Missing Values per Column")
                style_fig(fig_miss, 260)
                st.plotly_chart(fig_miss, use_container_width=True, key="miss_bar")

        # ── TAB: Summary Stats ────────────────────────────────────
        with tab_stats:
            if summary["describe"] is not None:
                st.markdown('<span class="sec-eyebrow">// descriptive statistics — numeric columns</span>', unsafe_allow_html=True)
                st.dataframe(summary["describe"].style.format("{:.3f}"), use_container_width=True)
            if cat_cols:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<span class="sec-eyebrow">// categorical value counts</span>', unsafe_allow_html=True)
                for cc in cat_cols:
                    vc = df[cc].value_counts().head(15).reset_index()
                    vc.columns = [cc, "Count"]
                    vc["Percent"] = (vc["Count"] / len(df) * 100).round(1).astype(str) + "%"
                    with st.expander(f"📂  {cc}  —  {df[cc].nunique()} unique values"):
                        st.dataframe(vc, use_container_width=True, hide_index=True)

        # ── TAB: Histograms ───────────────────────────────────────
        with tab_hist:
            st.markdown('<span class="sec-eyebrow">// distribution of every numeric column</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(hist_charts, "hist")

        # ── TAB: Box Plots ────────────────────────────────────────
        with tab_box:
            st.markdown('<span class="sec-eyebrow">// outliers & spread — numeric columns</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(box_charts, "box")

        # ── TAB: Bar Charts ───────────────────────────────────────
        with tab_bar:
            st.markdown('<span class="sec-eyebrow">// frequency — categorical columns</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(bar_charts, "bar")

        # ── TAB: Pie Charts ───────────────────────────────────────
        with tab_pie:
            st.markdown('<span class="sec-eyebrow">// proportion — low-cardinality categorical cols (≤12 unique)</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(pie_charts, "pie")

        # ── TAB: Scatter Plots ────────────────────────────────────
        with tab_scatter:
            st.markdown('<span class="sec-eyebrow">// relationships between numeric column pairs</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(scatter_charts, "sc")

        # ── TAB: Line Charts ──────────────────────────────────────
        with tab_line:
            st.markdown('<span class="sec-eyebrow">// trends along ordered numeric axis</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(line_charts, "ln")

        # ── TAB: Violin Plots ─────────────────────────────────────
        with tab_violin:
            st.markdown('<span class="sec-eyebrow">// distribution shape + density — numeric columns</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(violin_charts, "vl")

        # ── TAB: Heatmap ──────────────────────────────────────────
        with tab_heatmap:
            st.markdown('<span class="sec-eyebrow">// correlation between all numeric columns</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            render_chart_grid(heatmap_charts, "hm")

        # ── TAB: AI Report ────────────────────────────────────────
        with tab_report:
            st.markdown('<span class="sec-eyebrow">// analyst report — auto-generated from your file</span>', unsafe_allow_html=True)
            st.markdown("""
            <div class='dp-card' style='margin-bottom:1.2rem'>
              <div style='font-size:13px;color:#4a6080;line-height:1.7'>
                Generates a full professional EDA report using the real column names,
                actual statistics, and values from your uploaded file. Works instantly —
                no API key needed. Claude AI adds deeper insights if key is available.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📄 Generate Report", type="primary", key="gen_report"):
                with st.spinner("Building your report..."):
                    # Always generate the pure-Python report first
                    py_report = generate_python_report(df, summary, uploaded.name)
                    # Try AI enhancement if available
                    if client:
                        ai_text = generate_ai_report(df, summary)
                        final_report = py_report + "\n\n" + "─"*60 + "\n\n## 🤖 AI ANALYST INSIGHTS (Claude)\n\n" + ai_text
                    else:
                        final_report = py_report
                st.session_state["pg_report"] = final_report
                st.session_state["pg_report_name"] = uploaded.name

            if st.session_state.get("pg_report"):
                report = st.session_state["pg_report"]
                fname  = st.session_state.get("pg_report_name", "dataset")

                # Render as styled dark card
                rendered = report.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                # Re-apply headings
                lines_r = []
                for ln in rendered.split("\n"):
                    if ln.startswith("## "):
                        lines_r.append(f"<h4 style='color:#3b82f6;font-family:JetBrains Mono,monospace;font-size:13px;letter-spacing:0.1em;margin:20px 0 8px;text-transform:uppercase'>{ln[3:]}</h4>")
                    elif ln.startswith("### "):
                        lines_r.append(f"<h4 style='color:#e8f0ff;font-size:13px;margin:14px 0 6px'>{ln[4:]}</h4>")
                    elif ln.startswith("─"):
                        lines_r.append("<hr style='border-color:#1a2744;margin:16px 0'>")
                    elif ln.strip() == "":
                        lines_r.append("<br>")
                    else:
                        lines_r.append(f"<span style='font-size:13px;color:#8899bb;line-height:1.8'>{ln}</span><br>")
                st.markdown(
                    f"<div class='blog-body-inner' style='font-size:13px;line-height:1.8;padding:1.4rem'>{''.join(lines_r)}</div>",
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Full Report (.txt)",
                    data=report,
                    file_name=f"eda_report_{fname.replace('.csv','')}.txt",
                    mime="text/plain",
                    key="dl_report"
                )
    else:
        st.markdown("""
        <div style='text-align:center;padding:4rem 2rem;color:#2a3a55;
             border:1px dashed #1a2744;border-radius:14px;margin-top:1rem'>
          <div style='font-size:3rem;margin-bottom:14px'>📂</div>
          <div style='font-family:JetBrains Mono,monospace;font-size:12px;color:#2e4060;margin-bottom:8px'>
            drag & drop a CSV above
          </div>
          <div style='font-size:12px;color:#1a2a40'>
            Histograms · Scatter · Bar · Pie · Box · Violin · Line · Heatmap · AI Report
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# AI CHAT
# ══════════════════════════════════════════════════════════════════
elif page == "AI Chat":
    st.markdown('<span class="sec-eyebrow">// powered by claude</span><p class="sec-title">Ask My Portfolio</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='dp-card' style='margin-bottom:1rem'>
      <div style='font-size:13px;color:#4a6080'>
        Ask anything about Nabin's projects, skills, or background. Powered by Claude AI.<br>
        Try: <em style='color:#3b82f6'>"What ML projects has he done?"</em> or
        <em style='color:#3b82f6'>"How many rows did he analyze?"</em>
      </div>
    </div>
    """, unsafe_allow_html=True)

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
        <div class='chat-wrap' style='text-align:center;color:#2a3a55;padding:2rem'>
          <div style='font-size:1.8rem;margin-bottom:8px'>🤖</div>
          <div style='font-family:JetBrains Mono,monospace;font-size:11px'>Start the conversation below</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([4, 1])
    with c1:
        user_input = st.text_input("Your message", placeholder="What projects has Nabin built?",
                                   label_visibility="collapsed", key="chat_input")
    with c2:
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

    st.markdown("<br><div style='font-size:11px;color:#2a3a55;font-family:JetBrains Mono,monospace;margin-bottom:8px'>QUICK QUESTIONS</div>", unsafe_allow_html=True)
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
    st.markdown('<span class="sec-eyebrow">// get in touch</span><p class="sec-title">Contact</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"""
        <div class='contact-card'>
          <h3 style='color:#e8f0ff;margin-bottom:6px'>Let's connect 👋</h3>
          <p style='color:#4a6080;font-size:14px;margin-bottom:20px'>
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
        name    = st.text_input("Name",    key="c_name",  placeholder="Your name")
        email   = st.text_input("Email",   key="c_email", placeholder="your@email.com")
        message = st.text_area("Message",  key="c_msg",   height=110, placeholder="Hi Nabin, I'd like to...")
        if st.button("Send Message 🚀", type="primary"):
            if name and email and message:
                st.success(f"✅ Thanks {name}! I'll reply to {email} soon.")
                st.balloons()
            else:
                st.warning("Please fill in all fields.")

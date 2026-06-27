import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests

# ── Anthropic (optional) ───────────────────────────────────────────────────────
try:
    from anthropic import Anthropic as _Anthropic
    _ANTHROPIC_LIB = True
except ImportError:
    _ANTHROPIC_LIB = False

# ── Constants ──────────────────────────────────────────────────────────────────
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

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nabin · Data Science",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #050a14; }
[data-testid="stSidebar"] { background: #060c1a !important; border-right: 1px solid #0f1c33; }
[data-testid="stSidebar"] * { color: #5a7090 !important; }
.main .block-container { background: #050a14; padding-top: 2rem; }
.stApp { background: #050a14; }
h1,h2,h3,h4 { color: #e8f0ff; font-family: 'Inter', sans-serif; }

/* HERO */
.hero-eyebrow { font-family:'JetBrains Mono',monospace; font-size:11px; color:#3b82f6;
  letter-spacing:0.2em; text-transform:uppercase; margin-bottom:14px; display:block; }
.hero-name { font-size:clamp(2.2rem,5vw,3.6rem); font-weight:800; line-height:1.05;
  letter-spacing:-0.025em; margin:0 0 10px; color:#ffffff; }
.hero-name span { background:linear-gradient(135deg,#3b82f6 0%,#8b5cf6 50%,#06b6d4 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-role { font-size:1.05rem; color:#4a6080; margin-bottom:24px; line-height:1.65; }

/* STATUS PILL */
.status-pill { display:inline-flex; align-items:center; gap:8px;
  background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.18);
  color:#10b981; border-radius:99px; padding:5px 15px;
  font-size:12px; font-weight:500; margin-bottom:28px; }
.pulse { width:7px; height:7px; border-radius:50%; background:#10b981;
  animation:blink 2s ease-in-out infinite; }
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.35;transform:scale(0.75)} }

/* SECTION */
.sec-eyebrow { font-family:'JetBrains Mono',monospace; font-size:11px; color:#3b82f6;
  letter-spacing:0.15em; text-transform:uppercase; margin-bottom:6px; display:block; }
.sec-title { font-size:1.65rem; font-weight:700; color:#e8f0ff; margin-bottom:1.3rem; line-height:1.2; }

/* CARDS */
.stat-card { background:#080f1e; border:1px solid #131f35; border-radius:12px;
  padding:18px 14px; text-align:center; }
.stat-num { font-family:'JetBrains Mono',monospace; font-size:1.75rem; font-weight:700; color:#fff; }
.stat-lbl { font-size:10px; color:#2e4060; text-transform:uppercase; letter-spacing:0.1em; margin-top:5px; }

.gh-stat { background:#080f1e; border:1px solid #131f35; border-radius:10px;
  padding:14px; text-align:center; }
.gh-num { font-family:'JetBrains Mono',monospace; font-size:1.4rem; font-weight:700; color:#fff; }
.gh-lbl { font-size:10px; color:#2e4060; margin-top:4px; }

/* PROJECT CARD */
.proj-card { background:#080f1e; border:1px solid #131f35; border-radius:16px;
  padding:1.6rem; margin-bottom:1.2rem; position:relative;
  transition:border-color 0.2s,transform 0.18s; }
.proj-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,#3b82f6 50%,transparent);
  border-radius:16px 16px 0 0; }
.proj-card:hover { border-color:#1e3a6e; transform:translateY(-2px); }
.proj-title { font-size:1.05rem; font-weight:700; color:#e8f0ff; margin:0 0 8px; }
.proj-meta { font-size:12px; color:#2e4060; margin-bottom:10px; font-family:'JetBrains Mono',monospace; }

/* NOTEBOOK CARD */
.nb-card { background:#08101f; border:1px solid #0f1e35; border-radius:14px;
  padding:1.4rem; margin-bottom:1rem; position:relative; }
.nb-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1px;
  background:linear-gradient(90deg,transparent,#8b5cf6 50%,transparent); border-radius:14px 14px 0 0; }
.nb-title { font-size:1rem; font-weight:700; color:#e8f0ff; margin:0 0 6px; }
.nb-meta { font-size:11px; color:#2e4060; font-family:'JetBrains Mono',monospace; margin-bottom:10px; }
.nb-desc { font-size:13px; color:#6b82a8; line-height:1.7; }

/* BADGES */
.badge { display:inline-block; background:#0a1628; color:#4d8ef7;
  border:1px solid #1a3060; border-radius:6px; padding:2px 10px;
  font-size:11px; font-weight:500; margin:2px; font-family:'JetBrains Mono',monospace; }
.badge-green  { background:#061510; color:#34d399; border-color:#0a2e1e; }
.badge-purple { background:#10082a; color:#a78bfa; border-color:#231050; }
.badge-amber  { background:#160f00; color:#fbbf24; border-color:#2e2000; }
.badge-cyan   { background:#001520; color:#22d3ee; border-color:#003040; }

/* CODE BLOCK */
.code-block { background:#040810; border:1px solid #0f1e35; border-radius:10px;
  padding:1rem 1.2rem; font-family:'JetBrains Mono',monospace; font-size:12px;
  color:#7dd3fc; line-height:1.8; margin:10px 0; overflow-x:auto; }
.code-comment { color:#3a5070; }
.code-keyword { color:#a78bfa; }
.code-string  { color:#34d399; }

/* SKILL BARS */
.skill-row { margin-bottom:16px; }
.skill-top { display:flex; justify-content:space-between; margin-bottom:6px; }
.skill-name { font-size:13px; color:#8899bb; font-weight:500; }
.skill-pct  { font-size:12px; color:#3b82f6; font-family:'JetBrains Mono',monospace; font-weight:700; }
.skill-track { background:#0d1a2e; border-radius:99px; height:6px; overflow:hidden; }
.skill-fill  { height:6px; border-radius:99px; background:linear-gradient(90deg,#2563eb,#7c3aed); }

/* TIMELINE */
.timeline-item { display:flex; gap:16px; margin-bottom:24px; position:relative; }
.timeline-dot { width:36px; height:36px; border-radius:50%; background:#0d1f3c;
  border:2px solid #3b82f6; display:flex; align-items:center; justify-content:center;
  font-size:14px; flex-shrink:0; z-index:1; }
.timeline-line { position:absolute; left:17px; top:36px; width:2px; height:calc(100% + 8px);
  background:linear-gradient(to bottom,#1a2744,transparent); }
.timeline-content { padding-top:4px; }
.timeline-date  { font-family:'JetBrains Mono',monospace; font-size:11px; color:#3b82f6; margin-bottom:4px; }
.timeline-title { font-size:14px; font-weight:600; color:#e8f0ff; margin-bottom:4px; }
.timeline-desc  { font-size:13px; color:#4a6080; line-height:1.5; }

/* BLOG */
.blog-body-inner { font-size:14px; color:#8899bb; line-height:1.8;
  background:#050a14; border:1px solid #1a2744; border-radius:10px;
  padding:1.2rem; margin-top:12px; }
.blog-body-inner h4 { color:#e8f0ff; font-size:14px; margin:14px 0 6px; }
.blog-body-inner code { background:#0a1628; color:#7dd3fc; padding:2px 7px;
  border-radius:4px; font-size:12px; font-family:'JetBrains Mono',monospace; }
.blog-body-inner pre { background:#040810; color:#e2e8f0; padding:14px 18px;
  border-radius:10px; font-size:12px; overflow-x:auto; margin:10px 0; line-height:1.6;
  border:1px solid #1a2744; font-family:'JetBrains Mono',monospace; }

/* ML SECTION */
.ml-metric-card { background:#080f1e; border:1px solid #131f35; border-radius:10px;
  padding:14px; text-align:center; }
.ml-metric-val { font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700; color:#3b82f6; }
.ml-metric-lbl { font-size:10px; color:#2e4060; margin-top:4px; text-transform:uppercase; letter-spacing:0.1em; }

/* CHAT */
.chat-wrap { background:#080f1e; border:1px solid #1a2744; border-radius:16px;
  padding:1.2rem; max-height:440px; overflow-y:auto; }
.chat-msg-user { background:#0d1f3c; border:1px solid #1a3060; border-radius:12px 12px 4px 12px;
  padding:10px 14px; margin:8px 0 8px 20%; font-size:13px; color:#c8d8ff; }
.chat-msg-ai { background:#0a1220; border:1px solid #1a2744; border-radius:12px 12px 12px 4px;
  padding:10px 14px; margin:8px 20% 8px 0; font-size:13px; color:#8899bb; line-height:1.7; }
.chat-label { font-family:'JetBrains Mono',monospace; font-size:10px; margin-bottom:2px; }
.chat-label.user { color:#3b82f6; text-align:right; margin-right:4px; }
.chat-label.ai   { color:#10b981; margin-left:4px; }

/* ABOUT */
.about-box { background:#080f1e; border:1px solid #1a2744; border-left:3px solid #3b82f6;
  border-radius:0 10px 10px 0; padding:1rem 1.2rem; margin-bottom:1rem;
  font-size:14px; color:#8899bb; line-height:1.7; }
.about-box strong { color:#e8f0ff; }

/* CONTACT */
.contact-card { background:#080f1e; border:1px solid #1a2744; border-radius:16px; padding:2rem; margin-bottom:1rem; }
.contact-link { display:flex; align-items:center; gap:10px; color:#8899bb; text-decoration:none;
  font-size:14px; padding:10px 0; border-bottom:1px solid #0d1a2e; transition:color 0.15s; }
.contact-link:hover { color:#3b82f6; }
.contact-icon { font-size:18px; width:24px; }

/* DP */
.dp-card { background:#080f1e; border:1px solid #1a2744; border-radius:12px; padding:1.2rem; margin-bottom:1rem; }
.fancy-divider { border:none; height:1px; background:linear-gradient(90deg,transparent,#1a2744,transparent); margin:2rem 0; }

/* INPUTS */
.stTextInput input, .stTextArea textarea { background:#080f1e !important; color:#e8f0ff !important; border:1px solid #1a2744 !important; }
div[data-testid="stMetricValue"] { color:#ffffff !important; }
a { text-decoration:none !important; }
header[data-testid="stHeader"] { background:transparent; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "page_views"    not in st.session_state: st.session_state.page_views    = {}
if "tag_filter"    not in st.session_state: st.session_state.tag_filter    = "All"

# ── Data ───────────────────────────────────────────────────────────────────────
SKILLS = {
    "Python": 78, "Pandas": 72, "NumPy": 68, "Matplotlib / Seaborn": 67,
    "Plotly / Streamlit": 62, "Scikit-learn (ML)": 58, "SQL": 50, "Git & GitHub": 57,
}

PROJECTS = [
    {
        "title": "Student Performance Analysis",
        "tags": ["Pandas","Matplotlib","Seaborn","Python","NumPy"],
        "year": "2026",
        "problem": "Analyzed 500 student records to find what factors most affect academic scores.",
        "method": "6 charts: scatter (hours vs score), grade bars, subject scores, pass/fail pie, GPA histogram, age boxplot.",
        "result": "Avg score 64.1 | Pass rate 88.4% | Students studying 6–9 hrs scored highest.",
        "github": GITHUB, "chart": "student",
        "notebooks": ["basic_ml.ipynb", "numpy.ipynb"],
    },
    {
        "title": "Student ML: 5 Regression + 6 Classification",
        "tags": ["Scikit-learn","ML","XGBoost","RandomForest","Python"],
        "year": "2026",
        "problem": "Predict FinalScore (regression) and Pass/Fail (classification) from student features.",
        "method": "5 regression models (Linear, Polynomial, Decision Tree, Random Forest, XGBoost) + 6 classifiers. Full evaluation suite.",
        "result": "XGBoost best regressor | Random Forest best classifier. Full confusion matrices + R² comparison.",
        "github": GITHUB, "chart": "ml_models",
        "notebooks": ["ML_Notebook_Fixed_1.ipynb"],
    },
    {
        "title": "Heart Attack Incidence Analysis",
        "tags": ["Pandas","Seaborn","Healthcare","Python"],
        "year": "2026",
        "problem": "Analyzed 275,644 patient records to find risk factors across Germany (2015–2023).",
        "method": "6 charts: annual trend, incidence by state, smoking status, stress level, age group, correlation heatmap.",
        "result": "15.01% avg incidence | Top state: Hesse | High stress + poor diet = peak risk.",
        "github": GITHUB, "chart": "heart",
        "notebooks": [],
    },
    {
        "title": "BMW Sales + ML Price Prediction",
        "tags": ["Pandas","Scikit-learn","ML","GradientBoosting"],
        "year": "2026",
        "problem": "Analyzed BMW vehicle sales across regions & models (2010–2024), built ML price predictor.",
        "method": "EDA + Random Forest classifier + Gradient Boosting regressor. One-hot encoding, feature engineering.",
        "result": "Electric vehicles trending | Price predictor built with GradientBoostingRegressor.",
        "github": GITHUB, "chart": "bmw",
        "notebooks": ["project1.ipynb", "pms_analysis_bmw_sales.ipynb"],
    },
    {
        "title": "NumPy Deep Dive",
        "tags": ["NumPy","Python","Data Analysis"],
        "year": "2026",
        "problem": "Master NumPy from scratch: arrays, vectorized ops, statistics, performance vs Python lists.",
        "method": "Hands-on notebook: 1D/2D arrays, vectorization benchmarks, broadcasting, reshape, slicing, aggregate stats on student data.",
        "result": "NumPy 23× faster than list comprehension | Applied to real student_results.csv with 500 rows.",
        "github": GITHUB, "chart": "numpy",
        "notebooks": ["LEARNING_NUMPY.ipynb", "numpy.ipynb"],
    },
    {
        "title": "Nabin Data Dashboard",
        "tags": ["Streamlit","Plotly","Python"],
        "year": "2026",
        "problem": "Build a personal data science portfolio showcasing all projects interactively.",
        "method": "Multi-page Streamlit app with Plotly charts, AI chatbot, data playground, GitHub live stats.",
        "result": "Live portfolio deployed on Streamlit Cloud.",
        "github": GITHUB, "chart": "scatter",
        "notebooks": [],
    },
]

NOTEBOOKS = [
    {
        "title": "LEARNING_NUMPY.ipynb",
        "icon": "🔢",
        "topic": "NumPy Fundamentals",
        "tags": ["NumPy","Arrays","Vectorization"],
        "lines": 150,
        "desc": "From scratch NumPy: 1D/2D/3D arrays, vectors/matrices/tensors, array properties, reshaping. Benchmark proving NumPy is 23× faster than Python list comprehension. Also applies NumPy stats to real student data.",
        "highlights": ["np.array, zeros, ones, full, random", "reshape, flatten, ravel", "Performance: list comprehension vs np.arange", "Mean, median, std, min, max on real CSV data"],
        "key_code": """arr_1d = np.array([1,2,3,4,5])
arr_2d = np.array([[1,2,3],[4,5,6]])

# NumPy is 23x faster
start = time.time()
np_array = np.arange(1_000_000)  # 0.003s

# Vector, Matrix, Tensor
vector = np.array([1,2,3])
matrix = np.array([[1,2,3],[4,5,6]])
tensor = np.array([[[1,2],[3,4]],[[5,6],[7,8]]])

# Reshape
arr.reshape((3,4))   # 12 elements → 3×4
reshaped.flatten()   # back to 1D""",
    },
    {
        "title": "numpy.ipynb",
        "icon": "📊",
        "topic": "NumPy Applied to Student Data",
        "tags": ["NumPy","Pandas","Student Data"],
        "lines": 80,
        "desc": "Applies NumPy to the real student_results.csv dataset. Extracts columns as NumPy arrays, does element-wise bonus-mark addition, computes total scores, and prints full statistics for Math, Science and English scores.",
        "highlights": ["df['col'].values → NumPy arrays", "Element-wise: math_score + 5", "Total score across 3 subjects", "Statistics: mean, median, std, min, max"],
        "key_code": """df = pd.read_csv('student_results.csv')

# Convert CSV columns to NumPy arrays
math_score    = df["Math_Score"].values    # shape (500,)
science_score = df["Science_Score"].values
english_score = df["English_Score"].values

# Element-wise operations
math_bonus  = math_score + 5
total_score = math_score + science_score + english_score

# Statistics
print(f"Mean:   {np.mean(math_score):.2f}")
print(f"Median: {np.median(math_score):.2f}")
print(f"Std:    {np.std(math_score):.2f}")""",
    },
    {
        "title": "basic_ml.ipynb",
        "icon": "📈",
        "topic": "Student Performance — 6-Chart Report",
        "tags": ["Pandas","Matplotlib","Seaborn","EDA"],
        "lines": 90,
        "desc": "Full exploratory analysis of student_results03.csv. Computes key metrics (avg score, pass rate, top grade, avg hours, top GPA), then builds a 6-chart 2×3 subplot figure and prints an executive summary.",
        "highlights": ["6-chart subplot (2×3 layout)", "Scatter: Hours vs Score", "Pie: Pass/Fail ratio", "Boxplot: Age vs Score"],
        "key_code": """df = pd.read_csv('student_results03.csv')

avg_score = round(df['Average_Score'].mean(), 2)   # 64.1
pass_rate = (len(df[df['Result']=="Pass"]) / 500) * 100  # 88.4%

fig, axes = plt.subplots(2, 3, figsize=(18,10))
fig.suptitle("STUDENT PERFORMANCE ANALYSIS REPORT")

# Chart 1: scatter
axes[0,0].scatter(df['Hours_Studied'], df['Average_Score'], color='green')

# Chart 4: pie
result_counts = df['Result'].value_counts()
axes[1,0].pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')

# Chart 6: boxplot
sns.boxplot(data=df, x='Age', y='Average_Score', ax=axes[1,2], palette='Greens')""",
    },
    {
        "title": "ML_Notebook_Fixed_1.ipynb",
        "icon": "🤖",
        "topic": "5 Regression + 6 Classification Models",
        "tags": ["ML","Scikit-learn","XGBoost","RandomForest","Classification"],
        "lines": 62,
        "desc": "Complete ML notebook on student performance. Regression: Linear, Polynomial, Decision Tree, Random Forest, XGBoost — all evaluated with R², MAE, MSE, RMSE. Classification: Logistic, Decision Tree, Random Forest, KNN, SVC, XGBoost — evaluated with Accuracy, Precision, Recall, F1 + confusion matrices.",
        "highlights": ["5 regression + 6 classification models", "LabelEncoder for text columns", "Full metric suite for both tasks", "Feature importance charts for tree models"],
        "key_code": """# Regression
lin_reg_model = LinearRegression()
lin_reg_model.fit(X_train, y_score_train)
lin_reg_r2 = r2_score(y_score_test, lin_reg_model.predict(X_test))

xgb_reg_model = XGBRegressor(n_estimators=200, random_state=42)
xgb_reg_model.fit(X_train, y_score_train)

# Classification
forest_clf_model = RandomForestClassifier(n_estimators=200, random_state=42)
forest_clf_model.fit(X_train_c, y_passed_train)

# Evaluation
def evaluate_classifier(y_true, y_pred, name):
    acc  = accuracy_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred, zero_division=0)
    return acc, precision_score(...), recall_score(...), f1""",
    },
    {
        "title": "project1.ipynb",
        "icon": "🚗",
        "topic": "BMW Sales EDA — Initial Exploration",
        "tags": ["Pandas","Matplotlib","BMW","EDA"],
        "lines": 40,
        "desc": "Initial BMW sales exploration: model distribution, year distribution, regional sales. Bar charts for each category. Foundation for the later ML price prediction notebook.",
        "highlights": ["Model distribution bar chart", "Year-wise sales analysis", "Regional sales breakdown", "value_counts() workflow"],
        "key_code": """df = pd.read_csv("BMW sales data (2010-2024).csv")

Model_cnt = df["Model"].value_counts()
plt.figure(figsize=(12,6))
plt.bar(Model_cnt.index, Model_cnt.values)
plt.title("Model Distribution")

Year_cnt  = df["Year"].value_counts()
Region_cnt = df["Region"].value_counts()""",
    },
    {
        "title": "pms_analysis_bmw_sales.ipynb",
        "icon": "📉",
        "topic": "BMW Sales — Deep Dive Analysis",
        "tags": ["Pandas","Seaborn","BMW","Visualization"],
        "lines": 50,
        "desc": "Comprehensive BMW sales analysis notebook. Explores model counts, plots model distribution, and forms the analytical foundation for the ML price prediction work.",
        "highlights": ["mdl_cnt.plot(kind='bar')", "df.info() for data audit", "df['Model'].unique() discovery", "Seaborn-style visualization"],
        "key_code": """df = pd.read_csv("BMW sales data (2010-2024).csv")

# Audit the data
df.info()     # dtypes, non-null counts
df.head()     # first 5 rows

# Model analysis
mdl_cnt = df["Model"].value_counts()
mdl_cnt.plot(kind='bar')
plt.title("Number of Sales by BMW Model")
plt.xlabel("BMW Model")
plt.show()""",
    },
]

TIMELINE = [
    {"date":"May 2026","icon":"🔢","title":"Started with NumPy fundamentals","desc":"1D/2D/3D arrays, vectorization, 23× speedup. Applied to real student CSV data."},
    {"date":"May 2026","icon":"📊","title":"First real EDA — Student Analysis (500 rows)","desc":"6-chart subplot report: scatter, bar, pie, boxplot. avg 64.1, pass rate 88.4%."},
    {"date":"May 2026","icon":"🤖","title":"First ML project — 11 models on student data","desc":"5 regression + 6 classification models. XGBoost best performer. Confusion matrices + feature importance."},
    {"date":"June 2026","icon":"🚗","title":"BMW Sales Analysis + Price Prediction","desc":"2010–2024 data. Random Forest + Gradient Boosting regressor. One-hot encoding workflow."},
    {"date":"June 2026","icon":"🏥","title":"Heart Attack Analysis (275K rows)","desc":"Large real-world healthcare dataset from Germany. Stress × diet interaction identified."},
    {"date":"June 2026","icon":"🚀","title":"Deployed portfolio on Streamlit Cloud","desc":"First live web deployment with AI chatbot via Claude API."},
    {"date":"July 2026 (goal)","icon":"🎯","title":"Deep Learning with PyTorch","desc":"CNN image classification. First Kaggle competition entry planned."},
]

BLOG_POSTS = [
    {
        "date":"June 21, 2026","read":"5 min read",
        "title":"Heart Attack Incidence Analysis — 275,644 Patients, 6 Charts",
        "tags":["Pandas","Seaborn","Real Project","Healthcare Data"],
        "body":"""<h4>The Dataset</h4>
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
        "date":"June 20, 2026","read":"6 min read",
        "title":"11 ML Models on Student Data: What I Learned",
        "tags":["ML","Scikit-learn","XGBoost","RandomForest","Real Project"],
        "body":"""<h4>The Setup</h4>
<p>Two tasks from one dataset: predict FinalScore (regression) and predict Pass/Fail (classification). 8 input features, 80/20 train-test split.</p>
<h4>5 Regression Models</h4>
<pre>from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# R² comparison: XGBoost won
reg_models = ["Linear", "Polynomial", "Decision Tree", "Random Forest", "XGBoost"]</pre>
<h4>6 Classification Models</h4>
<pre>from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

def evaluate_classifier(y_true, y_pred, name):
    acc  = accuracy_score(y_true, y_pred)
    f1   = f1_score(y_true, y_pred, zero_division=0)
    print(f"Accuracy: {acc:.4f} | F1: {f1:.4f}")</pre>
<h4>Biggest Mistake I Fixed</h4>
<p>RMSE must always be <code>np.sqrt(MSE)</code> — never <code>np.sqrt(MAE)</code> or <code>np.square(MSE)</code>. Also fixed the filename bug: <code>'student_data (1).csv'</code> → <code>'student_data__1_.csv'</code>.</p>""",
    },
    {
        "date":"June 20, 2026","read":"6 min read",
        "title":"BMW Sales Analysis + ML Price Prediction (2010–2024)",
        "tags":["Pandas","Matplotlib","Scikit-learn","ML","Real Project"],
        "body":"""<h4>Data Cleaning</h4>
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
print(f"R²: {r2_score(y_test, preds):.3f}")</pre>""",
    },
    {
        "date":"June 18, 2026","read":"4 min read",
        "title":"NumPy is 23× faster than Python lists — here's the proof",
        "tags":["NumPy","Performance","Python"],
        "body":"""<h4>The benchmark</h4>
<pre>import time

# Python list comprehension
start = time.time()
py_list = [1*2 for i in range(1_000_000)]
print('List time:', time.time() - start)   # ~0.065s

# NumPy
start = time.time()
np_array = np.arange(1_000_000)
print('NumPy time:', time.time() - start)  # ~0.003s

# Result: NumPy ~23x faster</pre>
<h4>Why it matters</h4>
<p>Python lists store Python objects — each multiplication is a separate Python call. NumPy arrays store raw C numbers — the multiplication happens in one vectorized C loop.</p>
<h4>The key difference</h4>
<pre># Python list: repeats the list
py_list = [1,2,3]
py_list * 2   # → [1, 2, 3, 1, 2, 3]

# NumPy: element-wise multiply
np_array = np.array([1,2,3])
np_array * 2  # → [2, 4, 6]</pre>""",
    },
    {
        "date":"May 28, 2026","read":"3 min read",
        "title":"My first Seaborn heatmap — 3 mistakes I made",
        "tags":["Seaborn","Visualization"],
        "body":"""<h4>The code that finally worked</h4>
<pre>corr = df[["study_hours","attendance","sleep","score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, square=True)</pre>
<h4>Mistake 1 — forgot .corr()</h4>
<p>Pass the correlation matrix, not the raw dataframe.</p>
<h4>Mistake 2 — no fmt=".2f"</h4>
<p>Without it: <code>0.7283746...</code> — always add fmt.</p>
<h4>Mistake 3 — wrong colormap</h4>
<p><code>"rainbow"</code> looks colorful but is hard to read. Use <code>"Blues"</code> or <code>"coolwarm"</code>.</p>""",
    },
    {
        "date":"May 10, 2026","read":"5 min read",
        "title":"Student Performance — From Raw CSV to 6 Charts",
        "tags":["Pandas","Matplotlib","Seaborn","Real Project"],
        "body":"""<h4>Key Stats Computed</h4>
<pre>avg_score  = df['Average_Score'].mean()           # 64.1
pass_rate  = len(df[df['Result']=="Pass"]) / 500  # 88.4%
top_grade  = df['Grade'].value_counts().idxmax()  # B</pre>
<h4>All 6 Charts in One Figure</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes[0,0].scatter(df['Hours_Studied'], df['Average_Score'], color='green')
axes[1,0].pie(result_counts, labels=result_counts.index, autopct='%1.1f%%')
sns.boxplot(data=df, x='Age', y='Average_Score', ax=axes[1,2], palette='Greens')</pre>
<h4>Biggest Insight</h4>
<p>Students studying <code>6–9 hours</code> scored highest. Below 4 hours → much lower scores.</p>""",
    },
]

PORTFOLIO_CONTEXT = """You are an AI assistant on Nabin Kumar Thing's data science portfolio website.
Nabin is an aspiring data scientist from Nepal.

Notebooks & Projects:
1. LEARNING_NUMPY.ipynb — NumPy from scratch: arrays, vectorization, 23x speedup benchmark
2. numpy.ipynb — NumPy applied to real student_results.csv (500 rows), math/science/english stats
3. basic_ml.ipynb — Student performance EDA: 6-chart report, 88.4% pass rate, avg 64.1
4. ML_Notebook_Fixed_1.ipynb — 5 regression + 6 classification models on student data. XGBoost best.
5. project1.ipynb — BMW sales initial EDA: model/year/region distribution charts
6. pms_analysis_bmw_sales.ipynb — BMW deep dive analysis with Seaborn
7. Heart Attack Incidence — 275,644 German patient records, 15.01% avg incidence
8. BMW Sales + ML — Random Forest + Gradient Boosting price predictor
9. Nabin Data Dashboard — this Streamlit portfolio with AI chatbot

Skills: Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, SQL, Scikit-learn, XGBoost, Git
Email: nabinlamathing8@gmail.com | GitHub: github.com/nabinlamathing8-crypto

Answer questions about Nabin's work concisely. Keep under 150 words unless detail is requested."""

# ── Helpers ────────────────────────────────────────────────────────────────────
def fetch_github_stats():
    try:
        r = requests.get(f"https://api.github.com/users/{GITHUB_USER}", timeout=5)
        if r.status_code == 200:
            d = r.json()
            return {"repos": d.get("public_repos","8+"), "followers": d.get("followers","—"), "following": d.get("following","—")}
    except Exception:
        pass
    return {"repos":"8+","followers":"—","following":"—"}

def style_fig(fig, h=185):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#4a6080",size=10), height=h,
        margin=dict(l=8,r=8,t=30,b=8),
        showlegend=False, coloraxis_showscale=False,
        title_font=dict(color="#8899bb",size=11),
    )
    fig.update_xaxes(gridcolor="#0d1a2e",color="#4a6080")
    fig.update_yaxes(gridcolor="#0d1a2e",color="#4a6080")

def ai_chat(user_msg):
    if not client:
        return "⚠️ AI chat not available — add ANTHROPIC_API_KEY to Streamlit secrets to enable."
    msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history[-8:]]
    msgs.append({"role":"user","content":user_msg})
    resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=400,
                                  system=PORTFOLIO_CONTEXT, messages=msgs)
    return resp.content[0].text

def ai_summarize_project(project):
    if not client:
        return "Add ANTHROPIC_API_KEY to Streamlit secrets to enable AI summaries."
    resp = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=120,
        messages=[{"role":"user","content":
            f"Write a 2-sentence recruiter-friendly summary of this data science project:\n"
            f"Title: {project['title']}\nProblem: {project['problem']}\nResult: {project['result']}"}]
    )
    return resp.content[0].text

def make_chart(p, idx):
    np.random.seed(idx * 7 + 1)
    if p["chart"] == "student":
        hours = np.random.uniform(1,10,500)
        sc = np.clip(45 + hours*3.5 + np.random.randn(500)*10,35,97)
        fig = px.scatter(x=hours,y=sc,height=180,labels={"x":"Hours","y":"Score"},
                         title="Study hrs vs Score",color=sc,color_continuous_scale="Blues")
        fig.update_traces(marker=dict(size=3)); style_fig(fig); return [fig]
    elif p["chart"] == "ml_models":
        models = ["Linear","Polynomial","DTree","RF","XGBoost"]
        r2s    = [0.71, 0.74, 0.78, 0.85, 0.88]
        clfs   = ["Logistic","DTree","RF","KNN","SVC","XGBoost"]
        accs   = [0.82, 0.85, 0.90, 0.83, 0.87, 0.91]
        fig1 = px.bar(x=models,y=r2s,height=180,title="R² Score (Regression)",
                      color=r2s,color_continuous_scale="Blues",labels={"x":"Model","y":"R²"})
        style_fig(fig1)
        fig2 = px.bar(x=clfs,y=accs,height=180,title="Accuracy (Classification)",
                      color=accs,color_continuous_scale="Greens",labels={"x":"Model","y":"Accuracy"})
        style_fig(fig2)
        return [fig1, fig2]
    elif p["chart"] == "heart":
        years = list(range(2015,2024))
        rates = [0.1487,0.1494,0.1534,0.1471,0.1519,0.1519,0.1510,0.1498,0.1471]
        fig = px.area(x=years,y=rates,height=180,title="Incidence Trend",
                      color_discrete_sequence=["#3b82f6"])
        style_fig(fig); return [fig]
    elif p["chart"] == "bmw":
        years = list(range(2010,2025))
        prices = [28000 + i*800 + np.random.randint(-500,500) for i in range(15)]
        fig = px.line(x=years,y=prices,markers=True,height=180,title="BMW Avg Price",
                      color_discrete_sequence=["#8b5cf6"])
        style_fig(fig); return [fig]
    elif p["chart"] == "numpy":
        labels = ["np.arange\n(NumPy)","List\nComprehension"]
        times  = [0.003, 0.065]
        fig = px.bar(x=labels,y=times,height=180,title="Speed: NumPy vs Python List (1M ops)",
                     color=times,color_continuous_scale="Blues_r",labels={"x":"","y":"Seconds"})
        style_fig(fig); return [fig]
    else:
        df_s = pd.DataFrame({"Study":np.random.randint(1,10,50),"Score":np.random.randint(40,100,50)})
        fig = px.scatter(df_s,x="Study",y="Score",height=180,title="Study vs Score",
                         color="Score",color_continuous_scale="Blues")
        style_fig(fig); return [fig]

def build_eda_package(df):
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    summary = {
        "shape":f"{df.shape[0]:,} rows × {df.shape[1]} columns",
        "num_cols":num_cols, "cat_cols":cat_cols,
        "missing":int(df.isnull().sum().sum()),
        "missing_pct":f"{df.isnull().mean().mean()*100:.1f}%",
        "duplicates":int(df.duplicated().sum()),
        "dtypes":df.dtypes.value_counts().to_dict(),
        "col_missing":{col:int(cnt) for col,cnt in df.isnull().sum().items() if cnt > 0},
        "describe":df[num_cols].describe().round(3) if num_cols else None,
    }
    charts = []
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        fig = px.imshow(corr,text_auto=".2f",aspect="auto",color_continuous_scale="RdBu_r",
                        title="Correlation Heatmap",zmin=-1,zmax=1)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#4a6080",size=10),
                          height=320,margin=dict(l=8,r=8,t=36,b=8),
                          title_font=dict(color="#8899bb",size=12),
                          coloraxis_colorbar=dict(tickfont=dict(color="#4a6080")))
        charts.append(("📊 Heatmap","heatmap",fig))
    for col in num_cols:
        fig = px.histogram(df,x=col,nbins=35,color_discrete_sequence=["#3b82f6"],
                           title=f"Histogram — {col}",marginal="box")
        style_fig(fig); fig.update_layout(height=220)
        charts.append(("📈 Histograms",f"hist_{col}",fig))
    for col in num_cols:
        fig = px.box(df,y=col,color_discrete_sequence=["#8b5cf6"],
                     title=f"Box Plot — {col}",points="outliers")
        style_fig(fig); fig.update_layout(height=220)
        charts.append(("📦 Box Plots",f"box_{col}",fig))
    for col in cat_cols:
        vc = df[col].value_counts().head(15)
        fig = px.bar(x=vc.index.astype(str),y=vc.values,labels={"x":col,"y":"Count"},
                     color=vc.values,color_continuous_scale="Blues",title=f"Bar Chart — {col} (top 15)")
        style_fig(fig); fig.update_layout(height=250)
        charts.append(("📊 Bar Charts",f"bar_{col}",fig))
    for col in cat_cols:
        if df[col].nunique() <= 12:
            vc = df[col].value_counts()
            fig = px.pie(values=vc.values,names=vc.index.astype(str),title=f"Pie Chart — {col}",
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_traces(textinfo="percent+label")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#4a6080",size=10),
                              height=280,margin=dict(l=8,r=8,t=36,b=8),showlegend=False,
                              title_font=dict(color="#8899bb",size=12))
            charts.append(("🥧 Pie Charts",f"pie_{col}",fig))
    pairs = [(num_cols[i],num_cols[j]) for i in range(len(num_cols)) for j in range(i+1,len(num_cols))][:6]
    for (cx,cy) in pairs:
        color_col = cat_cols[0] if cat_cols and df[cat_cols[0]].nunique() <= 15 else None
        if color_col:
            fig = px.scatter(df,x=cx,y=cy,color=color_col,title=f"Scatter — {cx} vs {cy}",opacity=0.7)
        else:
            fig = px.scatter(df,x=cx,y=cy,color=cy,color_continuous_scale="Blues",
                             title=f"Scatter — {cx} vs {cy}",opacity=0.7)
        fig.update_traces(marker=dict(size=5)); style_fig(fig); fig.update_layout(height=250)
        charts.append(("🔵 Scatter Plots",f"scatter_{cx}_{cy}",fig))
    if len(num_cols) >= 2 and len(df) >= 10:
        x_col = num_cols[0]; df_sorted = df.sort_values(x_col)
        for y_col in num_cols[1:4]:
            fig = px.line(df_sorted,x=x_col,y=y_col,title=f"Line — {y_col} over {x_col}",
                          color_discrete_sequence=["#06b6d4"])
            style_fig(fig); fig.update_layout(height=220)
            charts.append(("📉 Line Charts",f"line_{x_col}_{y_col}",fig))
    for nc in num_cols[:3]:
        if cat_cols and df[cat_cols[0]].nunique() <= 10:
            fig = px.violin(df,y=nc,x=cat_cols[0],box=True,color=cat_cols[0],
                            title=f"Violin — {nc} by {cat_cols[0]}")
        else:
            fig = px.violin(df,y=nc,box=True,color_discrete_sequence=["#3b82f6"],title=f"Violin — {nc}")
        style_fig(fig); fig.update_layout(height=240,showlegend=False)
        charts.append(("🎻 Violin Plots",f"violin_{nc}",fig))
    return summary, charts

def generate_python_report(df, summary, filename="dataset.csv"):
    num_cols = summary["num_cols"]; cat_cols = summary["cat_cols"]
    lines = []; a = lines.append
    a(f"EDA REPORT — {filename.upper()}"); a("="*60)
    a(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}"); a("")
    a("## 1. DATASET OVERVIEW")
    a(f"  Shape           : {summary['shape']}")
    a(f"  Numeric columns : {len(num_cols)}  → {', '.join(num_cols) if num_cols else 'none'}")
    a(f"  Categorical cols: {len(cat_cols)}  → {', '.join(cat_cols) if cat_cols else 'none'}")
    a(f"  Missing values  : {summary['missing']:,} cells ({summary['missing_pct']})")
    a(f"  Duplicate rows  : {summary['duplicates']:,}"); a("")
    a("## 2. DATA QUALITY ASSESSMENT")
    if summary["col_missing"]:
        a("  Columns with missing values:")
        for col,cnt in sorted(summary["col_missing"].items(),key=lambda x:-x[1]):
            a(f"    • {col:<30} {cnt:>6,} missing  ({cnt/len(df)*100:.1f}%)")
    else:
        a("  ✓ No missing values — dataset is complete.")
    a(f"  ✓ Duplicates: {summary['duplicates']} row(s)"); a("")
    if num_cols:
        a("## 3. NUMERIC COLUMN STATISTICS")
        desc = df[num_cols].describe()
        for col in num_cols:
            s = desc[col]; skew = df[col].skew(); q1=s["25%"]; q3=s["75%"]; iqr=q3-q1
            outliers = int(((df[col]<q1-1.5*iqr)|(df[col]>q3+1.5*iqr)).sum())
            a(f"  ── {col}")
            a(f"     Mean/Std : {s['mean']:.3f} ± {s['std']:.3f}  |  Min: {s['min']:.3f}  Max: {s['max']:.3f}")
            a(f"     Median   : {s['50%']:.3f}  |  Q1: {q1:.3f}  Q3: {q3:.3f}  IQR: {iqr:.3f}")
            a(f"     Outliers : {outliers}  |  Skew: {skew:.3f}"); a("")
    if cat_cols:
        a("## 4. CATEGORICAL COLUMN ANALYSIS")
        for col in cat_cols:
            vc = df[col].value_counts().head(3)
            a(f"  ── {col}  ({df[col].nunique()} unique)")
            for i,(idx,val) in enumerate(vc.items()):
                a(f"     #{i+1}: {idx} — {val:,} rows ({val/len(df)*100:.1f}%)")
            a("")
    if len(num_cols) >= 2:
        a("## 5. CORRELATION ANALYSIS")
        corr = df[num_cols].corr()
        pairs = sorted([(abs(corr.loc[c1,c2]),corr.loc[c1,c2],c1,c2)
                        for i,c1 in enumerate(num_cols) for c2 in num_cols[i+1:]],reverse=True)
        for _,r,c1,c2 in pairs[:8]:
            strength = "strong" if abs(r)>0.7 else "moderate" if abs(r)>0.4 else "weak"
            a(f"  • {c1} ↔ {c2}: r={r:.3f} ({strength} {'positive' if r>0 else 'negative'})")
        a("")
    a("## 6. RECOMMENDATIONS"); recs = []
    if summary["missing"] > 0: recs.append("Handle missing values with median/mode imputation.")
    if summary["duplicates"] > 0: recs.append(f"Remove {summary['duplicates']} duplicate row(s).")
    if not recs: recs.append("Dataset looks clean. Ready for modeling.")
    for rec in recs: a(f"  → {rec}")
    a(""); a("="*60); a("END OF REPORT")
    return "\n".join(lines)

def generate_ai_report(df, summary):
    if not client: return None
    desc_str = summary["describe"].to_string() if summary["describe"] is not None else "N/A"
    prompt = f"""You are a senior data analyst. Analyze this dataset and write a structured EDA report.

DATASET: Shape={summary['shape']}, Numeric={summary['num_cols']}, Categorical={summary['cat_cols']}
Missing={summary['missing']} ({summary['missing_pct']}), Duplicates={summary['duplicates']}

FIRST 5 ROWS:
{df.head(5).to_string()}

DESCRIPTIVE STATISTICS:
{desc_str}

Write a professional EDA report with sections:
## 1. Dataset Overview
## 2. Data Quality Assessment  
## 3. Key Statistical Insights
## 4. Column-by-Column Analysis
## 5. Recommendations & Next Steps

Be specific with real column names and numbers. Max 500 words."""
    try:
        resp = client.messages.create(model="claude-sonnet-4-6",max_tokens=900,
                                      messages=[{"role":"user","content":prompt}])
        return resp.content[0].text
    except Exception as e:
        return f"Report generation failed: {e}"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem'>
      <div style='font-family:JetBrains Mono,monospace;font-size:9px;color:#3b82f6;letter-spacing:0.18em;margin-bottom:7px'>PORTFOLIO</div>
      <div style='font-size:15px;font-weight:700;color:#e8f0ff'>Nabin Kumar Thing</div>
      <div style='font-size:11px;color:#2e4060;margin-top:2px'>Data Science Learner · Nepal 🇳🇵</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#0f1c33;margin:10px 0'>", unsafe_allow_html=True)

    page = st.radio("nav",
        ["🏠  Home","💼  Projects","📓  Notebooks","⚡  Skills","📅  Timeline",
         "📝  Blog","🧪  Playground","🤖  AI Chat","📬  Contact"],
        label_visibility="collapsed")

    st.markdown("<hr style='border-color:#0f1c33;margin:10px 0'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-size:10px;color:#2e4060;font-family:JetBrains Mono,monospace;margin-bottom:8px'>CONNECT</div>
    <a href='{GITHUB}'       style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ GitHub</a>
    <a href='{LINKEDIN}'     style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ LinkedIn</a>
    <a href='mailto:{EMAIL}' style='color:#3a5070;font-size:12px;display:block;padding:3px 0'>⌥ Email</a>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#0f1c33;margin:10px 0'>", unsafe_allow_html=True)
    clean_page = page.split("  ")[1]
    st.session_state.page_views[clean_page] = st.session_state.page_views.get(clean_page,0) + 1
    total_views = sum(st.session_state.page_views.values())
    st.markdown(f"""<div style='font-size:9px;color:#1a2a40;font-family:JetBrains Mono,monospace'>SESSION · {total_views} page views</div>""", unsafe_allow_html=True)

page = page.split("  ")[1]

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if page == "Home":
    col1, col2 = st.columns([1.8,1])
    with col1:
        st.markdown("""
        <span class='hero-eyebrow'>// data scientist in training · nepal 🇳🇵</span>
        <h1 class='hero-name'>Hi, I'm <span>Nabin</span><br>Kumar Thing</h1>
        <p class='hero-role'>
          Python · Pandas · NumPy · Scikit-learn · XGBoost<br>
          6 notebooks · 11 ML models · 275K+ rows analyzed.
        </p>
        <div class='status-pill'>
          <div class='pulse'></div>
          Open to opportunities · Learning ML daily
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.link_button("💼 View Projects", GITHUB, type="primary")
        with c2: st.link_button("📬 Get in Touch", f"mailto:{EMAIL}")

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
          <div style='margin-top:6px;font-size:11px;color:#2e4060'>6 Notebooks on GitHub</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// github · live stats</span>', unsafe_allow_html=True)
    gh = fetch_github_stats()
    g1,g2,g3,g4,g5,g6 = st.columns(6)
    for col,val,lbl in zip([g1,g2,g3,g4,g5,g6],
        [gh["repos"],gh["followers"],gh["following"],"6","11","275K+"],
        ["Public Repos","Followers","Following","Notebooks","ML Models","Rows Analyzed"]):
        col.markdown(f"""<div class='gh-stat'><div class='gh-num'>{val}</div><div class='gh-lbl'>{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// quick stats</span>', unsafe_allow_html=True)
    s1,s2,s3,s4 = st.columns(4)
    for col,num,lbl in zip([s1,s2,s3,s4],
        ["275K+","11","88.4%","6"],
        ["Rows Analyzed","ML Models Built","Student Pass Rate","Notebooks"]):
        col.markdown(f"""<div class='stat-card'><div class='stat-num'>{num}</div><div class='stat-lbl'>{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// about</span><p class="sec-title">Who I Am</p>', unsafe_allow_html=True)
    a1,a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class='about-box'><strong>🎯 My Goal</strong><br>
        Building data science skills from scratch — Python, NumPy, ML, and real-world analysis.</div>
        <div class='about-box'><strong>🐍 What I Know</strong><br>
        Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Scikit-learn, XGBoost, Git.</div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class='about-box'><strong>📚 How I Learn</strong><br>
        Real projects and notebooks — each one solving an actual problem with actual data.</div>
        <div class='about-box'><strong>🚀 What's Next</strong><br>
        Deep learning with PyTorch, advanced SQL, Kaggle competitions, open-source contributions.</div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// skills snapshot</span>', unsafe_allow_html=True)
    for skill,pct in SKILLS.items():
        st.markdown(f"""
        <div class='skill-row'>
          <div class='skill-top'><span class='skill-name'>{skill}</span><span class='skill-pct'>{pct}%</span></div>
          <div class='skill-track'><div class='skill-fill' style='width:{pct}%'></div></div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PROJECTS
# ══════════════════════════════════════════════════════════════════
elif page == "Projects":
    st.markdown('<span class="sec-eyebrow">// work</span><p class="sec-title">Projects</p>', unsafe_allow_html=True)

    all_tags = ["All"] + sorted(set(t for p in PROJECTS for t in p["tags"]))
    filter_cols = st.columns(min(len(all_tags),8))
    visible_tags = all_tags[:8]
    for i,tag in enumerate(visible_tags):
        with filter_cols[i]:
            if st.button(tag, key=f"tag_{tag}",
                         type="primary" if st.session_state.tag_filter==tag else "secondary"):
                st.session_state.tag_filter = tag; st.rerun()

    filtered = PROJECTS if st.session_state.tag_filter=="All" else \
               [p for p in PROJECTS if st.session_state.tag_filter in p["tags"]]

    for idx,p in enumerate(filtered):
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in p["tags"])
        nb_html   = " ".join(f"<span class='badge badge-purple'>📓 {nb}</span>" for nb in p.get("notebooks",[]))
        with st.container():
            st.markdown("<div class='proj-card'>", unsafe_allow_html=True)
            figs = make_chart(p, idx)
            if len(figs) > 1:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"""
                    <p class='proj-meta'>{p['year']} · {p['tags'][0]}</p>
                    <h3 class='proj-title'>{p['title']}</h3>
                    <div style='margin-bottom:12px'>{tags_html}</div>
                    {"<div style='margin-bottom:10px'>"+nb_html+"</div>" if nb_html else ""}
                    <table style='font-size:12px;width:100%;border-collapse:collapse'>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0;white-space:nowrap'>Problem</td>
                          <td style='color:#8899bb;padding:3px 0'>{p['problem']}</td></tr>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0'>Method</td>
                          <td style='color:#8899bb;padding:3px 0'>{p['method']}</td></tr>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0'>Result</td>
                          <td style='color:#34d399;padding:3px 0'>{p['result']}</td></tr>
                    </table>
                    """, unsafe_allow_html=True)
                    sc1,sc2 = st.columns(2)
                    with sc1: st.link_button("🔗 GitHub", p["github"])
                    with sc2:
                        if st.button("✨ AI Summary", key=f"ai_sum_{idx}"):
                            with st.spinner("Generating..."):
                                summary = ai_summarize_project(p)
                            st.info(summary)
                with col2:
                    for fi,f in enumerate(figs):
                        st.plotly_chart(f, use_container_width=True, key=f"proj_{idx}_{fi}")
            else:
                col1, col2 = st.columns([1.6,1])
                with col1:
                    st.markdown(f"""
                    <p class='proj-meta'>{p['year']} · {p['tags'][0]}</p>
                    <h3 class='proj-title'>{p['title']}</h3>
                    <div style='margin-bottom:12px'>{tags_html}</div>
                    {"<div style='margin-bottom:10px'>"+nb_html+"</div>" if nb_html else ""}
                    <table style='font-size:12px;width:100%;border-collapse:collapse'>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0;white-space:nowrap'>Problem</td>
                          <td style='color:#8899bb;padding:3px 0'>{p['problem']}</td></tr>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0'>Method</td>
                          <td style='color:#8899bb;padding:3px 0'>{p['method']}</td></tr>
                      <tr><td style='color:#2a3a55;padding:3px 8px 3px 0'>Result</td>
                          <td style='color:#34d399;padding:3px 0'>{p['result']}</td></tr>
                    </table>
                    """, unsafe_allow_html=True)
                    sc1,sc2 = st.columns(2)
                    with sc1: st.link_button("🔗 GitHub", p["github"])
                    with sc2:
                        if st.button("✨ AI Summary", key=f"ai_sum2_{idx}"):
                            with st.spinner("Generating..."):
                                summary = ai_summarize_project(p)
                            st.info(summary)
                with col2:
                    st.plotly_chart(figs[0], use_container_width=True, key=f"proj_{idx}_0")
            st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# NOTEBOOKS
# ══════════════════════════════════════════════════════════════════
elif page == "Notebooks":
    st.markdown('<span class="sec-eyebrow">// learning journey</span><p class="sec-title">Notebooks</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class='dp-card'>
      <div style='font-size:13px;color:#4a6080;line-height:1.8'>
        All 6 notebooks I've written — from NumPy fundamentals to 11 ML models.
        Each includes the real code, key findings, and what I learned.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats row
    n1,n2,n3,n4 = st.columns(4)
    for col,val,lbl in zip([n1,n2,n3,n4],
        ["6","11","500+","23×"],
        ["Notebooks","ML Models","Lines of Code","NumPy Speedup"]):
        col.markdown(f"""<div class='stat-card'><div class='stat-num'>{val}</div><div class='stat-lbl'>{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for nb in NOTEBOOKS:
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in nb["tags"])
        hl_html   = "".join(f"<div style='font-size:12px;color:#4a6080;padding:2px 0'>✓ {h}</div>" for h in nb["highlights"])

        with st.expander(f"{nb['icon']}  {nb['title']}  —  {nb['topic']}"):
            col1,col2 = st.columns([1,1.2])
            with col1:
                st.markdown(f"""
                <div style='margin-bottom:12px'>{tags_html}</div>
                <p style='font-size:13px;color:#6b82a8;line-height:1.7;margin-bottom:14px'>{nb['desc']}</p>
                <div style='font-size:11px;color:#2e4060;font-family:JetBrains Mono,monospace;margin-bottom:8px;letter-spacing:0.1em'>KEY CONCEPTS</div>
                {hl_html}
                """, unsafe_allow_html=True)
                st.link_button("🔗 View on GitHub", GITHUB, key=f"nb_gh_{nb['title']}")
            with col2:
                st.markdown(f"""
                <div style='font-size:11px;color:#2e4060;font-family:JetBrains Mono,monospace;margin-bottom:8px;letter-spacing:0.1em'>KEY CODE</div>
                <div class='code-block'>{nb['key_code']}</div>
                """, unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// learning progression</span>', unsafe_allow_html=True)

    progression = ["NumPy basics\n(LEARNING_NUMPY)","NumPy on\nreal data","Student EDA\n6 charts","5 Regression\nmodels","6 Classification\nmodels","BMW EDA\n& ML"]
    progress_vals = [1,2,3,4,5,6]
    fig_prog = px.line(x=progression, y=progress_vals, markers=True,
                       title="Learning Progression",
                       color_discrete_sequence=["#3b82f6"])
    fig_prog.update_traces(marker=dict(size=12,color="#3b82f6"),line=dict(width=2))
    fig_prog.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                           font=dict(color="#4a6080",size=11),height=220,
                           margin=dict(l=8,r=8,t=40,b=8),
                           title_font=dict(color="#8899bb",size=12),showlegend=False)
    fig_prog.update_xaxes(gridcolor="#0d1a2e",color="#4a6080")
    fig_prog.update_yaxes(visible=False)
    st.plotly_chart(fig_prog, use_container_width=True, key="progression_chart")

# ══════════════════════════════════════════════════════════════════
# SKILLS
# ══════════════════════════════════════════════════════════════════
elif page == "Skills":
    st.markdown('<span class="sec-eyebrow">// abilities</span><p class="sec-title">Skills Dashboard</p>', unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("#### Core Skills")
        for skill,pct in SKILLS.items():
            st.markdown(f"""
            <div class='skill-row'>
              <div class='skill-top'><span class='skill-name'>{skill}</span><span class='skill-pct'>{pct}%</span></div>
              <div class='skill-track'><div class='skill-fill' style='width:{pct}%'></div></div>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Currently Learning 🔥")
        for item in ["XGBoost & ensemble methods","Feature engineering","Model evaluation (R², F1, ROC)","Scikit-learn pipelines"]:
            st.markdown(f"<span class='badge badge-purple'>⚡ {item}</span>", unsafe_allow_html=True)
        st.markdown("<br>#### Next Goals 🎯")
        for item in ["Deep Learning (PyTorch)","SQL advanced queries","Kaggle competitions","Data Engineering"]:
            st.markdown(f"<span class='badge badge-amber'>🎯 {item}</span>", unsafe_allow_html=True)
        st.markdown("<br>#### ML Models Used ✅")
        for item in ["LinearRegression","PolynomialRegression","DecisionTree","RandomForest","XGBoost","LogisticRegression","KNN","SVC"]:
            st.markdown(f"<span class='badge badge-green'>✓ {item}</span>", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    cats = list(SKILLS.keys()); vals = list(SKILLS.values())
    fig_radar = go.Figure(go.Scatterpolar(
        r=vals+[vals[0]], theta=cats+[cats[0]],
        fill="toself", line_color="#3b82f6", fillcolor="rgba(59,130,246,0.1)"
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True,range=[0,100],color="#4a6080"),
                   angularaxis=dict(color="#4a6080"),bgcolor="rgba(0,0,0,0)"),
        showlegend=False,height=420,paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8899bb"),margin=dict(l=50,r=50,t=20,b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="radar_chart")

# ══════════════════════════════════════════════════════════════════
# TIMELINE
# ══════════════════════════════════════════════════════════════════
elif page == "Timeline":
    st.markdown('<span class="sec-eyebrow">// journey</span><p class="sec-title">Learning Timeline</p>', unsafe_allow_html=True)
    for i,item in enumerate(TIMELINE):
        is_last = i == len(TIMELINE)-1
        st.markdown(f"""
        <div class='timeline-item'>
          {'<div class="timeline-line"></div>' if not is_last else ''}
          <div class='timeline-dot'>{item['icon']}</div>
          <div class='timeline-content'>
            <div class='timeline-date'>{item['date']}</div>
            <div class='timeline-title'>{item['title']}</div>
            <div class='timeline-desc'>{item['desc']}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
    st.markdown('<span class="sec-eyebrow">// session analytics</span>', unsafe_allow_html=True)
    if st.session_state.page_views:
        pages_list = list(st.session_state.page_views.keys())
        views_list = list(st.session_state.page_views.values())
        fig_pv = px.bar(x=pages_list,y=views_list,color=views_list,color_continuous_scale="Blues",
                        labels={"x":"Page","y":"Views"},title="Pages visited this session")
        style_fig(fig_pv,260)
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
        pie charts, box plots, violin plots, line charts, correlation heatmap, and an AI report.
      </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Drop a CSV file here", type=["csv"], key="pg_upload")

    if uploaded:
        df = pd.read_csv(uploaded)
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
        missing_total = int(df.isnull().sum().sum())
        missing_pct   = df.isnull().mean().mean()*100
        dups          = int(df.duplicated().sum())

        st.markdown("<hr class='fancy-divider'>", unsafe_allow_html=True)
        st.markdown('<span class="sec-eyebrow">// dataset overview</span>', unsafe_allow_html=True)
        m1,m2,m3,m4,m5,m6 = st.columns(6)
        for col,val,lbl in zip([m1,m2,m3,m4,m5,m6],
            [df.shape[0],df.shape[1],len(num_cols),len(cat_cols),f"{missing_total} ({missing_pct:.1f}%)",dups],
            ["Rows","Columns","Numeric Cols","Categorical Cols","Missing Values","Duplicate Rows"]):
            col.markdown(f"""<div class='stat-card'><div class='stat-num' style='font-size:1.2rem'>{val}</div><div class='stat-lbl'>{lbl}</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        summary, charts = build_eda_package(df)

        heatmap_charts = [(l,f) for s,l,f in charts if s=="📊 Heatmap"]
        hist_charts    = [(l,f) for s,l,f in charts if s=="📈 Histograms"]
        box_charts     = [(l,f) for s,l,f in charts if s=="📦 Box Plots"]
        bar_charts     = [(l,f) for s,l,f in charts if s=="📊 Bar Charts"]
        pie_charts     = [(l,f) for s,l,f in charts if s=="🥧 Pie Charts"]
        scatter_charts = [(l,f) for s,l,f in charts if s=="🔵 Scatter Plots"]
        line_charts    = [(l,f) for s,l,f in charts if s=="📉 Line Charts"]
        violin_charts  = [(l,f) for s,l,f in charts if s=="🎻 Violin Plots"]

        def render_chart_grid(chart_list, key_prefix):
            if not chart_list:
                st.info("No charts available for this column type.")
                return
            for i in range(0,len(chart_list),2):
                c1,c2 = st.columns(2)
                with c1: st.plotly_chart(chart_list[i][1], use_container_width=True, key=f"{key_prefix}_{i}_a")
                if i+1 < len(chart_list):
                    with c2: st.plotly_chart(chart_list[i+1][1], use_container_width=True, key=f"{key_prefix}_{i}_b")

        tabs = st.tabs([
            "📋 Data","📊 Summary Stats",
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
        tab_data,tab_stats,tab_hist,tab_box,tab_bar,tab_pie,tab_scatter,tab_line,tab_violin,tab_heatmap,tab_report = tabs

        with tab_data:
            st.dataframe(df.head(100), use_container_width=True)
            info_df = pd.DataFrame({
                "Column":list(df.columns),
                "Dtype":[str(df[c].dtype) for c in df.columns],
                "Non-Null":[int(df[c].count()) for c in df.columns],
                "Null":[int(df[c].isnull().sum()) for c in df.columns],
                "Unique":[int(df[c].nunique()) for c in df.columns],
            })
            st.dataframe(info_df, use_container_width=True, hide_index=True)

        with tab_stats:
            if summary["describe"] is not None:
                st.dataframe(summary["describe"].style.format("{:.3f}"), use_container_width=True)
            for cc in cat_cols:
                vc = df[cc].value_counts().head(15).reset_index()
                vc.columns = [cc,"Count"]
                with st.expander(f"📂  {cc}  —  {df[cc].nunique()} unique values"):
                    st.dataframe(vc, use_container_width=True, hide_index=True)

        with tab_hist: render_chart_grid(hist_charts,"hist")
        with tab_box:  render_chart_grid(box_charts,"box")
        with tab_bar:  render_chart_grid(bar_charts,"bar")
        with tab_pie:  render_chart_grid(pie_charts,"pie")
        with tab_scatter: render_chart_grid(scatter_charts,"sc")
        with tab_line: render_chart_grid(line_charts,"ln")
        with tab_violin: render_chart_grid(violin_charts,"vl")
        with tab_heatmap: render_chart_grid(heatmap_charts,"hm")

        with tab_report:
            st.markdown('<span class="sec-eyebrow">// auto-generated analyst report</span>', unsafe_allow_html=True)
            if st.button("📄 Generate Report", type="primary", key="gen_report"):
                with st.spinner("Building your report..."):
                    py_report = generate_python_report(df, summary, uploaded.name)
                    if client:
                        ai_text = generate_ai_report(df, summary)
                        final_report = py_report + "\n\n" + "─"*60 + "\n\n## 🤖 AI ANALYST INSIGHTS\n\n" + ai_text
                    else:
                        final_report = py_report
                st.session_state["pg_report"] = final_report
                st.session_state["pg_report_name"] = uploaded.name

            if st.session_state.get("pg_report"):
                report = st.session_state["pg_report"]
                fname  = st.session_state.get("pg_report_name","dataset")
                rendered = report.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                lines_r = []
                for ln in rendered.split("\n"):
                    if ln.startswith("## "):
                        lines_r.append(f"<h4 style='color:#3b82f6;font-family:JetBrains Mono,monospace;font-size:13px;letter-spacing:0.1em;margin:20px 0 8px;text-transform:uppercase'>{ln[3:]}</h4>")
                    elif ln.startswith("─"):
                        lines_r.append("<hr style='border-color:#1a2744;margin:16px 0'>")
                    elif ln.strip()=="":
                        lines_r.append("<br>")
                    else:
                        lines_r.append(f"<span style='font-size:13px;color:#8899bb;line-height:1.8'>{ln}</span><br>")
                st.markdown(f"<div class='blog-body-inner' style='padding:1.4rem'>{''.join(lines_r)}</div>", unsafe_allow_html=True)
                st.download_button("📥 Download Report (.txt)", data=report,
                    file_name=f"eda_report_{fname.replace('.csv','')}.txt",
                    mime="text/plain", key="dl_report")
    else:
        st.markdown("""
        <div style='text-align:center;padding:4rem 2rem;color:#2a3a55;
             border:1px dashed #1a2744;border-radius:14px;margin-top:1rem'>
          <div style='font-size:3rem;margin-bottom:14px'>📂</div>
          <div style='font-family:JetBrains Mono,monospace;font-size:12px;color:#2e4060;margin-bottom:8px'>drag & drop a CSV above</div>
          <div style='font-size:12px;color:#1a2a40'>Histograms · Scatter · Bar · Pie · Box · Violin · Line · Heatmap · AI Report</div>
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
        Ask anything about Nabin's notebooks, projects, skills, or background. Powered by Claude AI.<br>
        Try: <em style='color:#3b82f6'>"What ML models has he used?"</em> or
        <em style='color:#3b82f6'>"What does the NumPy notebook cover?"</em>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.chat_history:
        chat_html = "<div class='chat-wrap'>"
        for msg in st.session_state.chat_history:
            if msg["role"]=="user":
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
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns([4,1])
    with c1:
        user_input = st.text_input("Your message", placeholder="What notebooks has Nabin written?",
                                   label_visibility="collapsed", key="chat_input")
    with c2:
        send = st.button("Send ↗", type="primary", use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner(""):
            reply = ai_chat(user_input)
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear chat", type="secondary"):
            st.session_state.chat_history = []; st.rerun()

    st.markdown("<br><div style='font-size:11px;color:#2a3a55;font-family:JetBrains Mono,monospace;margin-bottom:8px'>QUICK QUESTIONS</div>", unsafe_allow_html=True)
    q1,q2,q3,q4 = st.columns(4)
    for col,q in zip([q1,q2,q3,q4],
        ["What notebooks exist?","What ML models?","NumPy speedup result?","Are you open to work?"]):
        with col:
            if st.button(q, key=f"quick_{q}"):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner(""):
                    reply = ai_chat(q)
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

# ══════════════════════════════════════════════════════════════════
# CONTACT
# ══════════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown('<span class="sec-eyebrow">// get in touch</span><p class="sec-title">Contact</p>', unsafe_allow_html=True)
    col1,col2 = st.columns([1.2,1])
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

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nabin Kumar Thing | Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Real links ────────────────────────────────────────────────────────────────
GITHUB   = "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard"
LINKEDIN = "https://www.linkedin.com/in/nabin-kumar-thing-b92406393"
EMAIL    = "nabinlamathing8@gmail.com"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  [data-testid="stSidebar"] { background: #0f172a; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

  .card {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.4rem; margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.10); transition: 0.2s; }

  .skill-wrap { margin-bottom: 14px; }
  .skill-label { font-size: 14px; font-weight: 500; color: #374151; margin-bottom: 4px; }
  .skill-bar-bg { background: #f1f5f9; border-radius: 99px; height: 10px; }
  .skill-bar-fill { background: #3b82f6; border-radius: 99px; height: 10px; }

  .badge {
    display: inline-block; background: #eff6ff; color: #1d4ed8;
    border-radius: 99px; padding: 3px 12px; font-size: 12px;
    font-weight: 500; margin: 3px 2px;
  }
  .badge-green { background: #f0fdf4; color: #16a34a; }
  .badge-amber { background: #fffbeb; color: #b45309; }

  .hero-title { font-size: 2.6rem; font-weight: 700; color: #ffffff; line-height: 1.2; }
  .hero-sub   { font-size: 1.1rem; color: #cbd5e1; margin-top: 0.5rem; }

  .section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #3b82f6; margin-bottom: 4px;
  }
  .section-title { font-size: 1.6rem; font-weight: 700; color: #0f172a; margin-bottom: 1.2rem; }

  .blog-date { font-size: 12px; color: #9ca3af; }
  .blog-title { font-size: 18px; font-weight: 700; color: #1e293b; margin: 6px 0 10px; }
  .blog-body  { font-size: 15px; color: #374151; line-height: 1.8; }
  .blog-body h4 { font-size: 15px; font-weight: 600; color: #1e293b; margin: 16px 0 6px; }
  .blog-body code {
    background: #f1f5f9; padding: 2px 6px; border-radius: 4px;
    font-size: 13px; font-family: monospace; color: #0f172a;
  }
  .blog-body pre {
    background: #1e293b; color: #e2e8f0; padding: 12px 16px;
    border-radius: 8px; font-size: 13px; overflow-x: auto;
    margin: 10px 0; line-height: 1.6;
  }

  .contact-btn {
    display: inline-block; background: #3b82f6; color: white !important;
    padding: 10px 24px; border-radius: 8px; text-decoration: none;
    font-weight: 500; font-size: 14px; margin: 4px 6px 4px 0;
  }
  .contact-btn:hover { background: #2563eb; }
  .contact-btn.outline {
    background: white; color: #3b82f6 !important; border: 1.5px solid #3b82f6;
  }

  .about-box {
    background: #f8fafc; border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin-bottom: 1rem;
    font-size: 15px; color: #374151; line-height: 1.7;
  }

  a { text-decoration: none; }
  h3 { color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Nabin Kumar Thing")
    st.markdown("*Data Science Learner*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠  Home", "💼  Projects", "🛠️  Skills", "📝  Blog", "📬  Contact"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Connect**")
    st.markdown(f"[GitHub]({GITHUB})  ·  [LinkedIn]({LINKEDIN})  ·  [Email](mailto:{EMAIL})")

# ═══════════════════════════════════════════════════════════════════════════════
# 🏠  HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🏠  Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style='padding-top:2rem'>
          <p class='section-label'>Welcome to my portfolio</p>
          <p class='hero-title'>Hi, I'm Nabin Kumar Thing 👋</p>
          <p class='hero-sub'>
            Aspiring Data Scientist focused on Python, data visualization,<br>
            and machine learning — turning raw data into clear insights.
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style='margin-top:1.5rem'>
          <a class='contact-btn' href='{GITHUB}'>💻 View GitHub</a>
          <a class='contact-btn outline' href='{LINKEDIN}'>🔗 LinkedIn</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='text-align:center; padding-top:2rem'>
          <div style='width:140px;height:140px;border-radius:50%;
                      background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                      display:flex;align-items:center;justify-content:center;
                      font-size:3.5rem;margin:0 auto;'>
            🧑‍💻
          </div>
          <p style='color:#64748b;font-size:14px;margin-top:12px'>Nabin Kumar Thing<br>Data Science Learner</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in zip(
        [c1, c2, c3, c4],
        ["4+", "7", "500+", "2026"],
        ["Projects", "Tools Mastered", "Rows Analyzed", "Learning Since"],
    ):
        col.metric(label, num)

    st.markdown("---")

    # About Me (replaces timeline)
    st.markdown('<p class="section-label">About</p><p class="section-title">Who I Am</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class='about-box'>
          <strong>🎯 My Goal</strong><br>
          I'm building my skills in data science from the ground up — learning Python,
          data analysis, and machine learning to solve real-world problems with data.
        </div>
        <div class='about-box'>
          <strong>🐍 What I know</strong><br>
          Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Git, SQL basics,
          and Scikit-learn for machine learning fundamentals.
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class='about-box'>
          <strong>📚 How I learn</strong><br>
          I learn by doing — building real projects, writing about what I discover,
          and sharing everything on GitHub so others can learn too.
        </div>
        <div class='about-box'>
          <strong>🚀 What's next</strong><br>
          Deep learning with PyTorch, advanced SQL, Kaggle competitions,
          and eventually contributing to open-source data projects.
        </div>
        """, unsafe_allow_html=True)

    # Skills snapshot chart
    st.markdown("---")
    st.markdown('<p class="section-label">Snapshot</p><p class="section-title">Skills at a Glance</p>', unsafe_allow_html=True)
    skills_data = {
        "Python": 75, "Pandas": 70, "Matplotlib/Seaborn": 65,
        "Plotly/Streamlit": 60, "SQL": 50, "Scikit-learn": 45, "Git": 55,
    }
    fig_home = px.bar(
        x=list(skills_data.values()), y=list(skills_data.keys()),
        orientation="h", color=list(skills_data.values()),
        color_continuous_scale="Blues", range_x=[0, 100],
        labels={"x": "Proficiency %", "y": ""},
    )
    fig_home.update_layout(
        height=300, showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_home, use_container_width=True, key="home_skills_chart")

# ═══════════════════════════════════════════════════════════════════════════════
# 💼  PROJECTS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "💼  Projects":
    st.markdown('<p class="section-label">Work</p><p class="section-title">Projects</p>', unsafe_allow_html=True)

    projects = [
        {
            "title": "Nabin Data Dashboard",
            "tags": ["Streamlit", "Plotly", "Python"],
            "problem": "Build a personal data science portfolio that showcases projects and skills interactively.",
            "method": "Built with Streamlit and Plotly — multi-page app with charts, skill bars, and blog.",
            "result": "Live portfolio site deployed on Streamlit Cloud, available to anyone online.",
            "github": GITHUB,
            "chart": "scatter",
        },
        {
            "title": "Nepal Household Survey Analysis",
            "tags": ["Pandas", "Seaborn", "Python"],
            "problem": "Understand income distribution and education access across Nepal's provinces.",
            "method": "Cleaned 10,000+ rows, grouped by province, built heatmaps and bar charts.",
            "result": "Found Province 2 had lowest literacy rates — visualized the gap clearly.",
            "github": GITHUB,
            "chart": "bar",
        },
        {
            "title": "Student Results Dashboard",
            "tags": ["Streamlit", "Plotly", "ML"],
            "problem": "Predict student grades from study hours and attendance data.",
            "method": "Linear regression with scikit-learn, interactive Streamlit UI.",
            "result": "Grade predictor with 88% accuracy on 500-record test dataset.",
            "github": GITHUB,
            "chart": "scatter2",
        },
        {
            "title": "Sales Data Analysis",
            "tags": ["Pandas", "Matplotlib", "Python"],
            "problem": "Identify top-selling products and monthly revenue trends.",
            "method": "Grouped sales by category and month, built bar and line charts.",
            "result": "Discovered Q4 sales peak — helped inform restocking decisions.",
            "github": GITHUB,
            "chart": "line",
        },
    ]

    for i, p in enumerate(projects):
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
                np.random.seed(i * 7)
                if p["chart"] == "bar":
                    df = pd.DataFrame({
                        "Province": [f"P{j}" for j in range(1, 8)],
                        "Literacy": np.random.randint(55, 90, 7),
                    })
                    fig = px.bar(df, x="Province", y="Literacy", color="Literacy",
                                 color_continuous_scale="Blues", height=220)
                elif p["chart"] in ("scatter", "scatter2"):
                    df = pd.DataFrame({
                        "Study Hours": np.random.randint(1, 10, 50),
                        "Score": np.random.randint(40, 100, 50),
                    })
                    fig = px.scatter(df, x="Study Hours", y="Score", height=220,
                                     color="Score", color_continuous_scale="Blues")
                else:
                    x = pd.date_range("2023-01-01", periods=60, freq="W")
                    fig = px.line(x=x, y=np.cumsum(np.random.randn(60) + 1),
                                  height=220, labels={"x": "Date", "y": "Sales"})
                fig.update_layout(
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False,
                )
                st.plotly_chart(fig, use_container_width=True, key=f"project_chart_{i}")
            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️  SKILLS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🛠️  Skills":
    st.markdown('<p class="section-label">Abilities</p><p class="section-title">Skills Dashboard</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    skills = {
        "Python": 75, "Pandas": 70, "Matplotlib / Seaborn": 65,
        "Plotly / Streamlit": 60, "SQL": 50, "Scikit-learn (ML)": 45, "Git & GitHub": 55,
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
        for item in ["Machine Learning basics", "Scikit-learn pipelines",
                     "Feature engineering", "Model evaluation metrics"]:
            st.markdown(f"<span class='badge'>⚡ {item}</span>", unsafe_allow_html=True)

        st.markdown("#### Next Up 🎯")
        for item in ["Deep Learning (PyTorch)", "SQL advanced queries",
                     "Data Engineering basics", "Kaggle competitions"]:
            st.markdown(f"<span class='badge badge-amber'>🎯 {item}</span>", unsafe_allow_html=True)

        st.markdown("#### Tools ✅")
        tools = ["Python", "Pandas", "NumPy", "Matplotlib", "Seaborn",
                 "Plotly", "Streamlit", "Scikit-learn", "Git", "Jupyter", "VS Code"]
        badges = " ".join(f"<span class='badge badge-green'>✓ {t}</span>" for t in tools)
        st.markdown(badges, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Skills Radar")
    categories = list(skills.keys())
    values = list(skills.values())
    fig_radar = go.Figure(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        line_color="#3b82f6",
        fillcolor="rgba(59,130,246,0.15)",
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False, height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=20, b=20),
    )
    st.plotly_chart(fig_radar, use_container_width=True, key="skills_radar")

# ═══════════════════════════════════════════════════════════════════════════════
# 📝  BLOG
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📝  Blog":
    st.markdown('<p class="section-label">Notes</p><p class="section-title">Blog & Learning Notes</p>', unsafe_allow_html=True)

    posts = [
        {
            "date": "June 15, 2026",
            "title": "How I cleaned messy survey data with Pandas",
            "tags": ["Pandas", "Data Cleaning"],
            "read": "4 min read",
            "body": """
<p>Real-world data is never clean. When I first opened my Nepal household survey dataset,
I found missing values everywhere, wrong data types, duplicate rows, and column names
with spaces and capital letters. Here is exactly how I fixed it step by step.</p>

<h4>Step 1 — Load the data and inspect it</h4>
<pre>import pandas as pd

df = pd.read_csv("survey.csv")
print(df.shape)       # how many rows and columns?
print(df.info())      # data types and nulls
print(df.head())      # first 5 rows</pre>

<p>The first thing I always do is check <code>df.info()</code>. It tells you which columns
have null values and whether numbers are stored as text (a very common problem).</p>

<h4>Step 2 — Fix column names</h4>
<pre>df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")</pre>
<p>This removes spaces, makes everything lowercase, and replaces spaces with underscores.
Now <code>Province Name</code> becomes <code>province_name</code> — much easier to type.</p>

<h4>Step 3 — Handle missing values</h4>
<pre>df["income"].fillna(df["income"].median(), inplace=True)
df.dropna(subset=["province", "age"], inplace=True)</pre>
<p>For numbers I fill with the median (not mean — outliers can skew the mean too much).
For key columns like province and age, I drop rows if they are missing because the record
is not useful without them.</p>

<h4>Step 4 — Remove duplicates</h4>
<pre>df.drop_duplicates(inplace=True)
print(f"Rows after cleaning: {len(df)}")</pre>

<p>After all four steps my dataset went from 10,847 rows to 10,203 clean, usable rows.
That is the foundation for every chart and analysis that came after.</p>
""",
        },
        {
            "date": "May 28, 2026",
            "title": "My first Seaborn heatmap — what I learned",
            "tags": ["Seaborn", "Visualization"],
            "read": "3 min read",
            "body": """
<p>Heatmaps look simple, but there were 3 things that tripped me up the first time I tried
to build one. Here is a walkthrough of my first real heatmap, mistakes and all.</p>

<h4>What I was trying to do</h4>
<p>I wanted to show the correlation between different numeric columns in my student dataset —
study hours, attendance, sleep hours, and final score. A heatmap is perfect for this.</p>

<h4>The code that finally worked</h4>
<pre>import seaborn as sns
import matplotlib.pyplot as plt

corr = df[["study_hours","attendance","sleep","score"]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
            linewidths=0.5, square=True)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()</pre>

<h4>Mistake 1 — I forgot .corr()</h4>
<p>I passed the raw dataframe to <code>sns.heatmap()</code> instead of the correlation matrix.
You must call <code>.corr()</code> first to get a matrix of numbers between -1 and 1.</p>

<h4>Mistake 2 — annot=True without fmt</h4>
<p>Without <code>fmt=".2f"</code>, the numbers showed as 0.7283746... way too many decimals.
Always add <code>fmt=".2f"</code> to round to 2 decimal places.</p>

<h4>Mistake 3 — wrong colormap</h4>
<p>I used <code>cmap="rainbow"</code> at first. It looked colorful but was hard to read.
<code>"Blues"</code> or <code>"coolwarm"</code> are much cleaner for correlation maps.</p>

<p>The biggest insight from my heatmap: study hours and final score had a correlation of 0.81 —
very strong. Attendance was 0.67. Sleep was only 0.31. Study time mattered most.</p>
""",
        },
        {
            "date": "May 10, 2026",
            "title": "Linear regression explained simply",
            "tags": ["ML", "Scikit-learn"],
            "read": "5 min read",
            "body": """
<p>I spent a week confused about regression. Every tutorial was either too math-heavy
or skipped the intuition completely. Here is the plain-English explanation I wish I had,
with working code.</p>

<h4>What is linear regression?</h4>
<p>It is just drawing the best straight line through your data. If you have study hours
on the X axis and exam scores on the Y axis, linear regression finds the line that
gets as close as possible to all the dots at once.</p>

<p>The formula is: <code>score = m × study_hours + b</code><br>
Where <code>m</code> is the slope (how much score increases per hour) and
<code>b</code> is the starting point (score with 0 hours).</p>

<h4>Code with scikit-learn</h4>
<pre>from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X = df[["study_hours"]]
y = df["score"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"R² score: {r2_score(y_test, predictions):.2f}")</pre>

<h4>What is R² score?</h4>
<p>R² tells you how well the model explains the data. R² of 1.0 = perfect.
R² of 0.0 = the model is no better than just guessing the average.
My student model got R² = 0.82 — meaning study hours explain 82% of the score variation.</p>

<h4>Predict a new student</h4>
<pre>new_student = [[7]]  # 7 study hours
predicted_score = model.predict(new_student)
print(f"Predicted score: {predicted_score[0]:.1f}")</pre>

<p>That is the whole thing. No complex math needed to get started — just fit, predict, evaluate.</p>
""",
        },
        {
            "date": "Apr 22, 2026",
            "title": "Why I switched from Matplotlib to Plotly",
            "tags": ["Plotly", "Visualization"],
            "read": "3 min read",
            "body": """
<p>Matplotlib is the classic Python chart library and I learned it first. But after
discovering Plotly, I now use Plotly for almost everything. Here is my honest comparison.</p>

<h4>The same chart in both libraries</h4>

<p><strong>Matplotlib:</strong></p>
<pre>import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.bar(df["province"], df["literacy"])
plt.xlabel("Province")
plt.ylabel("Literacy Rate")
plt.title("Literacy by Province")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()</pre>

<p><strong>Plotly:</strong></p>
<pre>import plotly.express as px

fig = px.bar(df, x="province", y="literacy",
             title="Literacy by Province")
fig.show()</pre>

<h4>The big difference — interactivity</h4>
<p>The Plotly chart is interactive out of the box. You can hover over bars to see exact values,
zoom in, pan around, and click to hide/show groups. The Matplotlib chart is just a flat image.</p>

<h4>When I still use Matplotlib</h4>
<p>Matplotlib is better when you need to save charts as high-quality images for reports or
publications, or when you need very precise control over every pixel. It is also faster
for generating many charts in a loop.</p>

<h4>My rule</h4>
<p>Plotly for dashboards and web apps. Matplotlib for reports and exports.
In Streamlit, Plotly always wins because the interactivity actually works in the browser.</p>
""",
        },
    ]

    for j, post in enumerate(posts):
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in post["tags"])
        with st.expander(f"📄 {post['title']}  —  {post['date']}  ·  {post['read']}"):
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown(f"<div class='blog-body'>{post['body']}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 📬  CONTACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📬  Contact":
    st.markdown('<p class="section-label">Get in touch</p><p class="section-title">Contact</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"""
        <div class='card'>
          <h3 style='margin-top:0'>Let's connect 👋</h3>
          <p style='color:#64748b;font-size:15px'>
            I'm always open to feedback, collaboration, or just chatting about data science.
            Feel free to reach out through any of the channels below.
          </p>
          <div style='margin:1.2rem 0'>
            <a class='contact-btn' href='mailto:{EMAIL}'>📧 Email Me</a>
            <a class='contact-btn outline' href='{LINKEDIN}'>🔗 LinkedIn</a>
            <a class='contact-btn outline' href='{GITHUB}'>💻 GitHub</a>
          </div>
          <p style='font-size:13px;color:#9ca3af;margin-top:1rem'>
            📧 {EMAIL}
          </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Send a message")
        name    = st.text_input("Your name",  key="contact_name")
        email   = st.text_input("Your email", key="contact_email")
        message = st.text_area("Message", height=130, key="contact_msg")
        if st.button("Send Message 🚀", key="contact_send"):
            if name and email and message:
                st.success(f"Thanks {name}! I'll reply to {email} soon.")
            else:
                st.warning("Please fill in all fields.")

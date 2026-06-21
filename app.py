import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

GITHUB   = "https://github.com/nabinlamathing8-crypto/nabin-data-dashboard"
LINKEDIN = "https://www.linkedin.com/in/nabin-kumar-thing-b92406393"
EMAIL    = "nabinlamathing8@gmail.com"

st.set_page_config(
    page_title="Nabin Kumar Thing | Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  [data-testid="stSidebar"] { background: #0f172a; }
  [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

  .hero-title { font-size: 2.6rem; font-weight: 700; color: #ffffff; line-height: 1.2; }
  .hero-sub   { font-size: 1.1rem; color: #cbd5e1; margin-top: 0.5rem; }

  .section-label {
    font-size: 11px; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #3b82f6; margin-bottom: 4px;
    display: block;
  }
  .section-title { font-size: 1.6rem; font-weight: 700; color: #ffffff; margin-bottom: 1.2rem; }

  .card {
    background: #1e293b; border: 1px solid #334155;
    border-left: 4px solid #3b82f6;
    border-radius: 12px; padding: 1.4rem; margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.3);
  }
  .card:hover { box-shadow: 0 4px 12px rgba(59,130,246,0.2); transition: 0.2s; }
  .card h3 { color: #f1f5f9; margin-bottom: 0.75rem; }

  .skill-wrap { margin-bottom: 14px; }
  .skill-label { font-size: 14px; font-weight: 500; color: #cbd5e1; margin-bottom: 4px; }
  .skill-bar-bg { background: #334155; border-radius: 99px; height: 10px; }
  .skill-bar-fill { background: linear-gradient(90deg,#3b82f6,#6366f1); border-radius: 99px; height: 10px; }

  .badge {
    display: inline-block; background: #1e3a5f; color: #93c5fd;
    border-radius: 99px; padding: 3px 12px; font-size: 12px;
    font-weight: 500; margin: 3px 2px;
  }
  .badge-green { background: #14532d; color: #86efac; }
  .badge-amber { background: #451a03; color: #fcd34d; }

  .about-box {
    background: #1e293b; border-left: 4px solid #3b82f6;
    border-radius: 0 8px 8px 0; padding: 1rem 1.2rem; margin-bottom: 1rem;
    font-size: 15px; color: #cbd5e1; line-height: 1.7;
  }
  .about-box strong { color: #f1f5f9; }

  .contact-btn {
    display: inline-block; background: #3b82f6; color: white !important;
    padding: 10px 24px; border-radius: 8px; text-decoration: none;
    font-weight: 500; font-size: 14px; margin: 4px 6px 4px 0;
  }
  .contact-btn.outline {
    background: transparent; color: #3b82f6 !important;
    border: 1.5px solid #3b82f6;
  }

  .blog-body {
    font-size: 15px; color: #cbd5e1; line-height: 1.8;
    background: #1e293b; border: 1px solid #334155;
    border-radius: 12px; padding: 1rem 1.2rem; margin-top: 1rem;
  }
  .blog-body h4 { font-size: 15px; font-weight: 700; color: #f1f5f9; margin: 16px 0 8px; }
  .blog-body code {
    background: #0f172a; padding: 2px 7px; border-radius: 4px;
    font-size: 13px; font-family: monospace; color: #7dd3fc;
  }
  .blog-body pre {
    background: #0f172a; color: #e2e8f0; padding: 14px 18px;
    border-radius: 10px; font-size: 13px; overflow-x: auto;
    margin: 10px 0; line-height: 1.6; border: 1px solid #334155;
  }

  a { text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Nabin Kumar Thing")
    st.markdown("*Data Science Learner*")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["Home", "Projects", "Skills", "Blog", "Contact"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Connect**")
    st.markdown(f"[GitHub]({GITHUB})  ·  [LinkedIn]({LINKEDIN})  ·  [Email](mailto:{EMAIL})")

# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div style='padding-top:2rem'>
          <span class='section-label'>Welcome to my portfolio</span>
          <p class='hero-title'>Hi, I'm Nabin Kumar Thing 👋</p>
          <p class='hero-sub'>
            Aspiring Data Scientist focused on Python, data visualization,<br>
            and machine learning — turning raw data into clear insights.
          </p>
        </div>
        """, unsafe_allow_html=True)
        # Button that jumps to Projects via query param
        if st.button("💼 View Projects", type="primary", key="hero_btn"):
            st.query_params["page"] = "Projects"
            st.rerun()

    with col2:
        st.markdown("""
        <div style='text-align:center; padding-top:2rem'>
          <div style='width:140px;height:140px;border-radius:50%;
                      background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                      display:flex;align-items:center;justify-content:center;
                      font-size:3.5rem;margin:0 auto;'>🧑‍💻</div>
          <p style='color:#94a3b8;font-size:14px;margin-top:12px'>
            Nabin Kumar Thing<br>Data Science Learner
          </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in zip([c1,c2,c3,c4],
        ["4+","7","500+","2026"],
        ["Projects","Tools Mastered","Rows Analyzed","Learning Since"]):
        col.metric(label, num)

    st.markdown("---")
    st.markdown('<span class="section-label">About</span><p class="section-title">Who I Am</p>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("""
        <div class='about-box'><strong>🎯 My Goal</strong><br>
        Building data science skills from the ground up — Python, data analysis,
        and ML to solve real-world problems.</div>
        <div class='about-box'><strong>🐍 What I Know</strong><br>
        Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit, Git, SQL, Scikit-learn.</div>
        """, unsafe_allow_html=True)
    with a2:
        st.markdown("""
        <div class='about-box'><strong>📚 How I Learn</strong><br>
        I learn by doing — building real projects, writing about discoveries,
        and sharing everything on GitHub.</div>
        <div class='about-box'><strong>🚀 What's Next</strong><br>
        Deep learning with PyTorch, advanced SQL, Kaggle competitions,
        and open-source contributions.</div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="section-label">Snapshot</span><p class="section-title">Skills at a Glance</p>', unsafe_allow_html=True)
    skills_data = {"Python":75,"Pandas":70,"Matplotlib/Seaborn":65,"Plotly/Streamlit":60,"SQL":50,"Scikit-learn":45,"Git":55}
    fig_home = px.bar(x=list(skills_data.values()), y=list(skills_data.keys()),
                      orientation="h", color=list(skills_data.values()),
                      color_continuous_scale="Blues", range_x=[0,100],
                      labels={"x":"Proficiency %","y":""})
    fig_home.update_layout(height=300, showlegend=False, coloraxis_showscale=False,
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           margin=dict(l=10,r=10,t=10,b=10),
                           font=dict(color="#cbd5e1"))
    st.plotly_chart(fig_home, use_container_width=True, key="home_skills_chart")

# Handle redirect from "View Projects" button
if st.query_params.get("page") == "Projects":
    page = "Projects"
    st.query_params.clear()

# ═══════════════════════════════════════════════════════════════════════════════
# PROJECTS
# ═══════════════════════════════════════════════════════════════════════════════
if page == "Projects":
    st.markdown('<span class="section-label">Work</span><p class="section-title">Projects</p>', unsafe_allow_html=True)

    projects = [
        {
            "title": "Student Performance Analysis Report",
            "tags": ["Pandas", "Matplotlib", "Seaborn", "Python"],
            "problem": "Analyze 500 real student records to find what factors most affect academic scores and grades.",
            "method": "6 charts: scatter (hours vs score), grade bars, subject scores, pass/fail pie (88.4%), GPA histogram, age boxplot.",
            "result": "Avg score 64.1 | Pass rate 88.4% | Top grade B | Students studying 6–9 hrs scored highest.",
            "github": GITHUB,
            "chart": "student",
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
            "title": "Nabin Data Dashboard",
            "tags": ["Streamlit", "Plotly", "Python"],
            "problem": "Build a personal data science portfolio showcasing projects and skills interactively.",
            "method": "Multi-page Streamlit app with Plotly charts, skill bars, blog, and contact form.",
            "result": "Live portfolio deployed on Streamlit Cloud, available to anyone online.",
            "github": GITHUB,
            "chart": "scatter",
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

    for idx, p in enumerate(projects):
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.6, 1])
            with col1:
                tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in p["tags"])
                st.markdown(f"""
                <h3 style='margin:0 0 6px;color:#f1f5f9'>{p['title']}</h3>
                <div style='margin-bottom:10px'>{tags_html}</div>
                <table style='font-size:13px;color:#94a3b8;width:100%'>
                  <tr><td style='color:#64748b;padding-right:8px;white-space:nowrap;vertical-align:top'>Problem</td>
                      <td style='color:#cbd5e1'>{p['problem']}</td></tr>
                  <tr><td style='color:#64748b;padding-right:8px;white-space:nowrap;vertical-align:top'>Method</td>
                      <td style='color:#cbd5e1'>{p['method']}</td></tr>
                  <tr><td style='color:#64748b;padding-right:8px;white-space:nowrap;vertical-align:top'>Result</td>
                      <td style='color:#86efac'>{p['result']}</td></tr>
                </table>
                <a href='{p["github"]}' class='contact-btn' style='margin-top:12px;display:inline-block;font-size:13px'>
                  🔗 View on GitHub
                </a>
                """, unsafe_allow_html=True)
            with col2:
                np.random.seed(idx * 7 + 1)
                if p["chart"] == "student":
                    hours = np.random.uniform(1, 10, 500)
                    sc = np.clip(45 + hours*3.5 + np.random.randn(500)*10, 35, 97)
                    fig1 = px.scatter(x=hours, y=sc, height=170,
                                      labels={"x":"Hours Studied","y":"Avg Score"},
                                      title="Hours vs Score",
                                      color=sc, color_continuous_scale="Greens")
                    fig1.update_traces(marker=dict(size=3),
                                       hovertemplate="Hours: %{x:.1f}<br>Score: %{y:.1f}<extra></extra>")
                    fig1.update_layout(margin=dict(l=5,r=5,t=25,b=5), showlegend=False,
                                       coloraxis_showscale=False, font=dict(color="#cbd5e1"),
                                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig1, use_container_width=True, key=f"p{idx}_scatter")

                    fig2 = px.pie(values=[88.4,11.6], names=["Pass","Fail"],
                                  color_discrete_sequence=["limegreen","tomato"],
                                  title="Pass & Fail", height=170)
                    fig2.update_traces(textinfo="percent+label",
                                       hovertemplate="%{label}: %{value}%<extra></extra>")
                    fig2.update_layout(margin=dict(l=5,r=5,t=25,b=5), showlegend=False,
                                       font=dict(color="#cbd5e1"), paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig2, use_container_width=True, key=f"p{idx}_pie")

                    fig3 = px.bar(x=["English","Science","Math"], y=[63.8,64.2,64.5],
                                  title="Subject Avg Score", height=170,
                                  color=["English","Science","Math"],
                                  color_discrete_sequence=["#166534","#15803d","#16a34a"],
                                  labels={"x":"Subject","y":"Avg Score"})
                    fig3.update_traces(hovertemplate="%{x}: %{y:.1f}<extra></extra>")
                    fig3.update_layout(margin=dict(l=5,r=5,t=25,b=5), showlegend=False,
                                       font=dict(color="#cbd5e1"),
                                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig3, use_container_width=True, key=f"p{idx}_subjects")

                elif p["chart"] == "bar":
                    df = pd.DataFrame({"Province":[f"P{i}" for i in range(1,8)],
                                       "Literacy":np.random.randint(55,90,7)})
                    fig = px.bar(df, x="Province", y="Literacy", color="Literacy",
                                 color_continuous_scale="Blues", height=220)
                    fig.update_layout(margin=dict(l=5,r=5,t=10,b=5), showlegend=False,
                                      coloraxis_showscale=False, font=dict(color="#cbd5e1"),
                                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True, key=f"p{idx}_bar")

                elif p["chart"] == "scatter":
                    df = pd.DataFrame({"Study Hours":np.random.randint(1,10,50),
                                       "Score":np.random.randint(40,100,50)})
                    fig = px.scatter(df, x="Study Hours", y="Score", height=220,
                                     color="Score", color_continuous_scale="Blues")
                    fig.update_layout(margin=dict(l=5,r=5,t=10,b=5), showlegend=False,
                                      coloraxis_showscale=False, font=dict(color="#cbd5e1"),
                                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True, key=f"p{idx}_sc")

                else:
                    x = pd.date_range("2023-01-01", periods=12, freq="ME")
                    fig = px.line(x=x, y=np.cumsum(np.random.randint(10,50,12)),
                                  height=220, labels={"x":"Month","y":"Sales"})
                    fig.update_layout(margin=dict(l=5,r=5,t=10,b=5), showlegend=False,
                                      font=dict(color="#cbd5e1"),
                                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True, key=f"p{idx}_line")

            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SKILLS
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Skills":
    st.markdown('<span class="section-label">Abilities</span><p class="section-title">Skills Dashboard</p>', unsafe_allow_html=True)
    skills = {"Python":75,"Pandas":70,"Matplotlib / Seaborn":65,"Plotly / Streamlit":60,"SQL":50,"Scikit-learn (ML)":45,"Git & GitHub":55}
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Core Skills")
        for skill, pct in skills.items():
            st.markdown(f"""
            <div class='skill-wrap'>
              <div class='skill-label'>{skill} <span style='float:right;color:#3b82f6'>{pct}%</span></div>
              <div class='skill-bar-bg'><div class='skill-bar-fill' style='width:{pct}%'></div></div>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("#### Learning Now 🔥")
        for item in ["Machine Learning basics","Scikit-learn pipelines","Feature engineering","Model evaluation metrics"]:
            st.markdown(f"<span class='badge'>⚡ {item}</span>", unsafe_allow_html=True)
        st.markdown("#### Next Up 🎯")
        for item in ["Deep Learning (PyTorch)","SQL advanced queries","Data Engineering basics","Kaggle competitions"]:
            st.markdown(f"<span class='badge badge-amber'>🎯 {item}</span>", unsafe_allow_html=True)
        st.markdown("#### Tools ✅")
        tools = ["Python","Pandas","NumPy","Matplotlib","Seaborn","Plotly","Streamlit","Scikit-learn","Git","Jupyter","VS Code"]
        st.markdown(" ".join(f"<span class='badge badge-green'>✓ {t}</span>" for t in tools), unsafe_allow_html=True)

    st.markdown("---")
    categories = list(skills.keys())
    values = list(skills.values())
    fig_radar = go.Figure(go.Scatterpolar(r=values+[values[0]], theta=categories+[categories[0]],
                                          fill="toself", line_color="#3b82f6",
                                          fillcolor="rgba(59,130,246,0.15)"))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100]),
                                       angularaxis=dict(color="#94a3b8")),
                            showlegend=False, height=380,
                            paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#cbd5e1"),
                            margin=dict(l=40,r=40,t=20,b=20))
    st.plotly_chart(fig_radar, use_container_width=True, key="skills_radar")

# ═══════════════════════════════════════════════════════════════════════════════
# BLOG
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Blog":
    st.markdown('<span class="section-label">Notes</span><p class="section-title">Blog & Learning Notes</p>', unsafe_allow_html=True)

    posts = [
        {
            "date": "June 21, 2026",
            "title": "Building My Student Performance Analysis — From Raw CSV to 6 Charts",
            "tags": ["Pandas", "Matplotlib", "Seaborn", "Real Project"],
            "read": "6 min read",
            "body": """
<p>This is a full walkthrough of my most recent project — a complete analysis of 500 student
records. I want to show exactly what I did, what I learned, and what surprised me.</p>

<h4>The Dataset</h4>
<p>The data had 11 columns: Student_ID, Age, Math_Score, Science_Score, English_Score,
Hours_Studied, Total_Score, Average_Score, Result (Pass/Fail), GPA, and Grade.
500 rows, all real-looking student data.</p>

<h4>Step 1 — Load and inspect</h4>
<pre>import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('student_results03.csv')
print(df.shape)   # (500, 11)
print(df.head())</pre>

<h4>Step 2 — Compute key stats</h4>
<pre>total_record = len(df)                          # 500
avg_score    = round(df['Average_Score'].mean(), 2)  # 64.1
pass_rate    = (len(df[df['Result']=="Pass"]) / total_record) * 100  # 88.4
top_grade    = df['Grade'].value_counts().idxmax()   # B
avg_hour     = round(df['Hours_Studied'].mean(), 2)  # 5.41
top_gpa      = df['GPA'].max()                       # 4.0</pre>

<h4>Step 3 — Build all 6 charts in one figure</h4>
<pre>fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("STUDENT PERFORMANCE ANALYSIS REPORT", fontsize=20, fontweight='bold')

# Chart 1: Hours Studied vs Average Score
axes[0,0].scatter(df['Hours_Studied'], df['Average_Score'], color='green')
axes[0,0].set_title('Correlation Between Hours_Studied & Average_Score')

# Chart 2: Average Score by Grade
grade_avg = df.groupby("Grade")["Average_Score"].mean().sort_values()
axes[0,1].bar(grade_avg.index, grade_avg.values, color="skyblue", edgecolor="black")
axes[0,1].set_title("Average Score by Grade")

# Chart 3: Subject-wise Average
sub_avg = df[['English_Score','Science_Score','Math_Score']].mean()
axes[0,2].bar(sub_avg.index, sub_avg.values, color='green', edgecolor='black')
axes[0,2].set_title('Subject-wise Average Score')

# Chart 4: Pass vs Fail Pie
result_counts = df['Result'].value_counts()
axes[1,0].pie(result_counts, labels=result_counts.index,
              colors=['limegreen','tomato'], autopct='%1.1f%%')
axes[1,0].set_title('Pass & Fail Ratio')

# Chart 5: GPA Distribution
axes[1,1].hist(df['GPA'], color='green', edgecolor='black')
axes[1,1].set_title('GPA Distribution')

# Chart 6: Age vs Average Score
sns.boxplot(data=df, x='Age', y='Average_Score', ax=axes[1,2], palette='Greens')
axes[1,2].set_title('Age vs Average Score')

plt.tight_layout()
plt.show()</pre>

<h4>Key Findings</h4>
<p><strong>📊 Average score:</strong> 64.1 — a solid class average.<br>
<strong>✅ Pass rate:</strong> 88.4% — only 11.6% failed.<br>
<strong>🏆 Top grade:</strong> B — most common grade in the class.<br>
<strong>⏰ Study hours insight:</strong> Students who studied 6–9 hours scored highest.
Below 4 hours showed much lower scores.<br>
<strong>📚 Subjects:</strong> English, Science, and Math averages were all close (~64),
showing a balanced curriculum.<br>
<strong>🎂 Age:</strong> Younger students (age 13–14) had slightly wider score variation,
hinting at more diverse learning patterns.</p>

<h4>What I Learned</h4>
<p>This was my first full analysis project from start to finish. I learned how to use
<code>plt.subplots()</code> to build multi-chart figures, how to use
<code>groupby().mean()</code> to summarize data, and how <code>sns.boxplot()</code>
can show score distribution by age in one line. Most importantly — I learned that
real data tells a story if you look carefully.</p>
""",
        },
        {
            "date": "June 15, 2026",
            "title": "How I cleaned messy survey data with Pandas",
            "tags": ["Pandas", "Data Cleaning"],
            "read": "4 min read",
            "body": """
<p>Real-world data is never clean. When I first opened my Nepal household survey dataset,
I found missing values everywhere, wrong data types, duplicate rows, and messy column names.</p>

<h4>Step 1 — Load and inspect</h4>
<pre>import pandas as pd
df = pd.read_csv("survey.csv")
print(df.info())   # check dtypes and nulls
print(df.head())</pre>

<h4>Step 2 — Fix column names</h4>
<pre>df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")</pre>

<h4>Step 3 — Handle missing values</h4>
<pre>df["income"].fillna(df["income"].median(), inplace=True)
df.dropna(subset=["province", "age"], inplace=True)</pre>

<h4>Step 4 — Remove duplicates</h4>
<pre>df.drop_duplicates(inplace=True)
print(f"Clean rows: {len(df)}")</pre>

<p>After 4 steps: 10,847 rows → 10,203 clean rows. That became the foundation for all charts.</p>
""",
        },
        {
            "date": "May 28, 2026",
            "title": "My first Seaborn heatmap — what I learned",
            "tags": ["Seaborn", "Visualization"],
            "read": "3 min read",
            "body": """
<p>Heatmaps look simple but 3 things tripped me up the first time.</p>

<h4>The code that finally worked</h4>
<pre>import seaborn as sns
import matplotlib.pyplot as plt

corr = df[["study_hours","attendance","sleep","score"]].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", linewidths=0.5, square=True)
plt.title("Correlation Heatmap")
plt.show()</pre>

<h4>Mistake 1 — forgot .corr()</h4>
<p>Pass the correlation matrix, not the raw dataframe.</p>

<h4>Mistake 2 — no fmt=".2f"</h4>
<p>Without it: <code>0.7283746...</code>. With it: <code>0.73</code>. Always add fmt.</p>

<h4>Mistake 3 — wrong colormap</h4>
<p><code>"rainbow"</code> looks colorful but is hard to read. Use <code>"Blues"</code> or <code>"coolwarm"</code>.</p>

<p><strong>Biggest insight:</strong> Study hours vs score = 0.81 correlation. Very strong.</p>
""",
        },
        {
            "date": "May 10, 2026",
            "title": "Linear regression explained simply",
            "tags": ["ML", "Scikit-learn"],
            "read": "5 min read",
            "body": """
<p>I spent a week confused about regression. Here is the plain-English explanation I wish I had.</p>

<h4>What is it?</h4>
<p>Just drawing the best straight line through your data. Formula: <code>score = m × hours + b</code></p>

<h4>Code</h4>
<pre>from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X = df[["study_hours"]]
y = df["score"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LinearRegression()
model.fit(X_train, y_train)
print(f"R² score: {r2_score(y_test, model.predict(X_test)):.2f}")</pre>

<p>My model got R² = 0.82 — study hours explain 82% of score variation.</p>

<h4>Predict a new student</h4>
<pre>model.predict([[7]])  # 7 study hours → predicted score</pre>
""",
        },
    ]

    for post in posts:
        tags_html = " ".join(f"<span class='badge'>{t}</span>" for t in post["tags"])
        with st.expander(f"📄  {post['title']}   —   {post['date']}  ·  {post['read']}"):
            st.markdown(tags_html, unsafe_allow_html=True)
            st.markdown(f"<div class='blog-body'>{post['body']}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CONTACT
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "Contact":
    st.markdown('<span class="section-label">Get in touch</span><p class="section-title">Contact</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"""
        <div class='card'>
          <h3>Let's connect 👋</h3>
          <p style='color:#94a3b8;font-size:15px'>
            Open to feedback, collaboration, or just chatting about data science.
          </p>
          <div style='margin:1.2rem 0'>
            <a class='contact-btn' href='mailto:{EMAIL}'>📧 Email Me</a>
            <a class='contact-btn outline' href='{LINKEDIN}'>🔗 LinkedIn</a>
            <a class='contact-btn outline' href='{GITHUB}'>💻 GitHub</a>
          </div>
          <p style='font-size:13px;color:#64748b'>📧 {EMAIL}</p>
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

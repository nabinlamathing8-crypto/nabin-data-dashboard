# Nabin Kumar Thing — Data Science Portfolio

A sleek, feature-rich data science portfolio built with Streamlit.

## Features

| Feature | Description |
|---|---|
|  Home | Hero section, live GitHub stats, skill bars |
|  Projects | Tag-filtered project cards with inline charts |
|  AI Summary | Claude AI generates recruiter-friendly project summaries |
|  Skills | Skill bars + radar chart |
|  Timeline | Learning journey + session analytics |
|  Blog | Expandable blog posts with code blocks |
|  Playground | Upload any CSV → instant auto-EDA (no code needed) |
| AI Chat | Ask-my-portfolio chatbot powered by Claude |
|  Contact | Contact card + message form |

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Anthropic API key (for AI features)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your key

# 3. Run locally
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to share.streamlit.io → New app → select your repo
3. Add `ANTHROPIC_API_KEY` in the Secrets section of the app settings
4. Deploy!

## AI Features Setup

The AI Chat and AI Project Summary require an Anthropic API key:
- Get one at https://console.anthropic.com
- Add it to `.streamlit/secrets.toml` as `ANTHROPIC_API_KEY`
- Without a key, the app still works — AI features show a friendly message

## Live Demo

https://nabin-thing.streamlit.app

[README-3.md](https://github.com/user-attachments/files/26410874/README-3.md)
# 🎬 IMDb Movie Success Analysis — Streamlit App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)

**Live Demo:** [Click Here](#) · **Author:** Adarsh Tripathi

---

## 📌 Overview
An interactive data analysis dashboard built with Streamlit, analyzing 19,000+ IMDb movies across genres, directors, ratings, and box office performance.

## 🚀 Features
- 📊 **Overview** — KPIs, rating distribution, yearly trends
- 🎭 **Genre Analysis** — Best genres by rating & revenue, debut director insights
- 🎬 **Director Insights** — Top directors by gross income and avg rating
- ⭐ **Ratings Deep Dive** — Correlations, heatmap, decade-wise trends
- 💰 **Box Office** — Revenue trends, top grossing movies, star impact
- 🔍 **Movie Explorer** — Search & filter 19K+ movies interactively

## 🛠️ Tech Stack
`Python` · `Streamlit` · `Pandas` · `Matplotlib` · `Seaborn`

## 📦 Run Locally

```bash
git clone https://github.com/Adarsh-T-04/IMDb-Movie-Success-Analysis.git
cd IMDb-Movie-Success-Analysis
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Click **Deploy** ✅

## 📂 File Structure
```
IMDb-Movie-Success-Analysis/
├── app.py                  ← Streamlit app
├── movies.csv              ← Dataset
├── requirements.txt
├── .streamlit/
│   └── config.toml         ← Dark theme config
└── README.md
```

---
*Part of Adarsh Tripathi's Data Science Portfolio · [GitHub](https://github.com/Adarsh-T-04)*

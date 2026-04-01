import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="IMDb Movie Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');

    .main { background-color: #0a0a0a; }
    .stApp { background-color: #0a0a0a; color: #f0f0f0; }

    h1, h2, h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }

    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #e50914;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px;
    }
    .metric-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.2rem;
        color: #e50914;
        display: block;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .section-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.8rem;
        color: #e50914;
        border-left: 4px solid #e50914;
        padding-left: 12px;
        margin: 20px 0 10px 0;
        letter-spacing: 2px;
    }
    .stSidebar { background-color: #111 !important; }
    .stSelectbox label, .stSlider label, .stMultiselect label {
        color: #ccc !important;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df["duration"] = pd.to_numeric(df["duration"].str.replace("min","").str.replace(",","").str.strip(), errors="coerce")
    df["votes"] = pd.to_numeric(df["votes"].str.replace(",",""), errors="coerce")
    df["gross_income"] = pd.to_numeric(df["gross_income"].str.replace(",",""), errors="coerce")
    df["gi_crores"] = df["gross_income"] / 10_000_000
    df["decade"] = (df["year"] // 10) * 10
    df["num_stars"] = df["stars_name"].str.count(",") + 1
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("## 🎬 IMDb Analysis")
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊 Overview",
        "🎭 Genre Analysis",
        "🎬 Director Insights",
        "⭐ Ratings Deep Dive",
        "💰 Box Office",
        "🔍 Movie Explorer"
    ])
    st.markdown("---")

    # Filters
    st.markdown("### Filters")
    year_range = st.slider("Year Range", int(df["year"].min()), int(df["year"].max()), (2000, 2023))
    min_votes = st.number_input("Min Votes", value=1000, step=1000)

    dff = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1]) & (df["votes"] >= min_votes)]
    st.markdown(f"**{len(dff):,}** movies selected")

# Header
st.markdown("""
<h1 style='font-family:Bebas Neue; font-size:3rem; color:#e50914; letter-spacing:4px; margin-bottom:0;'>
🎬 IMDb MOVIE SUCCESS ANALYSIS
</h1>
<p style='color:#888; font-size:0.95rem; margin-top:0;'>By Adarsh Tripathi · Data Science Portfolio Project</p>
<hr style='border-color:#e50914; margin-bottom:20px;'>
""", unsafe_allow_html=True)


# ─── PAGE: OVERVIEW ─────────────────────────────────────────────────────────
if page == "📊 Overview":
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (f"{len(dff):,}", "Total Movies"),
        (f"{dff['rating'].mean():.2f}", "Avg IMDb Rating"),
        (f"${dff['gross_income'].sum()/1e9:.1f}B", "Total Box Office"),
        (f"{dff['directors_name'].nunique():,}", "Unique Directors"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <span class="metric-value">{val}</span>
                <span class="metric-label">{label}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">MOVIES PER YEAR</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    vc = dff["year"].value_counts().sort_index()
    ax.fill_between(vc.index, vc.values, alpha=0.3, color="#e50914")
    ax.plot(vc.index, vc.values, color="#e50914", linewidth=2)
    ax.set_xlabel("Year", color="#aaa")
    ax.set_ylabel("Number of Movies", color="#aaa")
    ax.tick_params(colors="#aaa")
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">RATING DISTRIBUTION</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        sns.histplot(dff["rating"], bins=20, color="#e50914", ax=ax, kde=True)
        ax.set_xlabel("IMDb Rating", color="#aaa")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="section-title">CERTIFICATE BREAKDOWN</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        cert_counts = dff["certificate"].value_counts().head(8)
        colors = ["#e50914" if i == 0 else "#555" for i in range(len(cert_counts))]
        ax.barh(cert_counts.index, cert_counts.values, color=colors)
        ax.set_xlabel("Count", color="#aaa")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    st.markdown('<div class="section-title">TOP 10 HIGHEST RATED MOVIES</div>', unsafe_allow_html=True)
    top10 = dff.nlargest(10, "rating")[["name", "year", "rating", "votes", "directors_name", "genre"]].reset_index(drop=True)
    top10.index += 1
    st.dataframe(top10, use_container_width=True)


# ─── PAGE: GENRE ANALYSIS ───────────────────────────────────────────────────
elif page == "🎭 Genre Analysis":
    st.markdown('<div class="section-title">GENRE-WISE AVERAGE RATING</div>', unsafe_allow_html=True)

    genre_exploded = dff.assign(genre=dff["genre"].str.split(",")).explode("genre")
    genre_exploded["genre"] = genre_exploded["genre"].str.strip()

    genre_rating = genre_exploded.groupby("genre")["rating"].mean().sort_values(ascending=False).head(15)
    genre_income = genre_exploded.groupby("genre")["gross_income"].mean().sort_values(ascending=False).head(15)
    genre_count = genre_exploded["genre"].value_counts().head(15)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7, 6))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        colors = ["#e50914" if i < 3 else "#555" for i in range(len(genre_rating))]
        ax.barh(genre_rating.index[::-1], genre_rating.values[::-1], color=colors[::-1])
        ax.set_xlabel("Avg Rating", color="#aaa")
        ax.set_title("Avg Rating by Genre", color="#fff", fontsize=12)
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 6))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        colors2 = ["#e50914" if i < 3 else "#555" for i in range(len(genre_count))]
        ax.barh(genre_count.index[::-1], genre_count.values[::-1], color=colors2[::-1])
        ax.set_xlabel("Number of Movies", color="#aaa")
        ax.set_title("Most Common Genres", color="#fff", fontsize=12)
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    st.markdown('<div class="section-title">BEST GENRE FOR DEBUT DIRECTORS</div>', unsafe_allow_html=True)
    first_movies = dff.sort_values("year").groupby("directors_name").first().reset_index()
    debut_genre = first_movies.assign(genre=first_movies["genre"].str.split(",")).explode("genre")
    debut_genre["genre"] = debut_genre["genre"].str.strip()
    best_debut = debut_genre.groupby("genre")["rating"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    colors3 = ["#e50914" if i < 3 else "#555" for i in range(len(best_debut))]
    ax.bar(best_debut.index, best_debut.values, color=colors3)
    ax.set_ylabel("Avg Rating", color="#aaa")
    ax.set_title("Best Genre for Debut Directors", color="#fff")
    ax.tick_params(colors="#aaa", axis='x', rotation=30)
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)

    st.markdown('<div class="section-title">GENRE AVG BOX OFFICE</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    gi = genre_income.dropna()
    ax.bar(gi.index, gi.values / 1e6, color="#e50914", alpha=0.8)
    ax.set_ylabel("Avg Gross Income ($ Million)", color="#aaa")
    ax.tick_params(colors="#aaa", axis='x', rotation=30)
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)


# ─── PAGE: DIRECTOR INSIGHTS ────────────────────────────────────────────────
elif page == "🎬 Director Insights":
    st.markdown('<div class="section-title">TOP DIRECTORS BY GROSS INCOME</div>', unsafe_allow_html=True)

    top_directors = dff.groupby("directors_name").agg(
        total_gross=("gross_income", "sum"),
        avg_rating=("rating", "mean"),
        movie_count=("name", "count")
    ).sort_values("total_gross", ascending=False).head(15).reset_index()

    col1, col2 = st.columns([2, 1])
    with col1:
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        colors = ["#e50914" if i < 3 else "#444" for i in range(len(top_directors))]
        ax.barh(top_directors["directors_name"][::-1], top_directors["total_gross"][::-1] / 1e9, color=colors[::-1])
        ax.set_xlabel("Total Gross ($ Billion)", color="#aaa")
        ax.set_title("Top Directors — Total Box Office", color="#fff")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    with col2:
        st.markdown("**Top Directors Table**")
        top_directors["total_gross"] = top_directors["total_gross"].apply(lambda x: f"${x/1e9:.2f}B")
        top_directors["avg_rating"] = top_directors["avg_rating"].round(2)
        top_directors.columns = ["Director", "Gross", "Avg Rating", "Movies"]
        st.dataframe(top_directors.head(10), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">TOP DIRECTORS BY AVG RATING</div>', unsafe_allow_html=True)
    top_rated_dir = dff.groupby("directors_name").filter(lambda x: len(x) >= 3)
    top_rated_dir = top_rated_dir.groupby("directors_name")["rating"].mean().sort_values(ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    ax.bar(top_rated_dir.index, top_rated_dir.values, color="#e50914", alpha=0.85)
    ax.set_ylabel("Avg Rating", color="#aaa")
    ax.tick_params(colors="#aaa", axis='x', rotation=30)
    ax.set_ylim(7, top_rated_dir.max() + 0.5)
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)


# ─── PAGE: RATINGS DEEP DIVE ────────────────────────────────────────────────
elif page == "⭐ Ratings Deep Dive":
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">RATING VS VOTES</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        sample = dff.dropna(subset=["votes", "rating"]).sample(min(2000, len(dff)))
        ax.scatter(sample["rating"], sample["votes"], alpha=0.4, color="#e50914", s=15)
        ax.set_xlabel("IMDb Rating", color="#aaa")
        ax.set_ylabel("Votes", color="#aaa")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    with col2:
        st.markdown('<div class="section-title">RATING TREND BY YEAR</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        yearly = dff.groupby("year")["rating"].mean()
        ax.plot(yearly.index, yearly.values, color="#e50914", linewidth=2)
        ax.fill_between(yearly.index, yearly.values, alpha=0.15, color="#e50914")
        ax.set_xlabel("Year", color="#aaa")
        ax.set_ylabel("Avg Rating", color="#aaa")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    st.markdown('<div class="section-title">DURATION VS RATING BY DECADE</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    dec_data = dff[dff["decade"] >= 1980].dropna(subset=["duration"])
    sns.boxplot(data=dec_data, x="decade", y="duration", palette="Reds", ax=ax)
    ax.set_xlabel("Decade", color="#aaa")
    ax.set_ylabel("Duration (min)", color="#aaa")
    ax.tick_params(colors="#aaa")
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)

    st.markdown('<div class="section-title">CORRELATION HEATMAP</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    corr = dff[["rating", "votes", "gross_income", "duration", "year", "num_stars"]].corr()
    sns.heatmap(corr, annot=True, cmap="Reds", ax=ax, fmt=".2f",
                linewidths=0.5, linecolor="#222",
                annot_kws={"color": "white", "size": 9})
    ax.tick_params(colors="#aaa")
    st.pyplot(fig)


# ─── PAGE: BOX OFFICE ───────────────────────────────────────────────────────
elif page == "💰 Box Office":
    st.markdown('<div class="section-title">BOX OFFICE BY YEAR</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    yearly_gi = dff.groupby("year")["gi_crores"].sum().dropna()
    ax.fill_between(yearly_gi.index, yearly_gi.values, color="#e50914", alpha=0.3)
    ax.plot(yearly_gi.index, yearly_gi.values, color="#e50914", linewidth=2)
    ax.set_ylabel("Gross Income (Crores)", color="#aaa")
    ax.tick_params(colors="#aaa")
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">TOP 10 GROSSING MOVIES</div>', unsafe_allow_html=True)
        top_gross = dff.dropna(subset=["gross_income"]).nlargest(10, "gross_income")[["name", "year", "gross_income", "rating"]].reset_index(drop=True)
        top_gross.index += 1
        top_gross["gross_income"] = top_gross["gross_income"].apply(lambda x: f"${x/1e6:.0f}M")
        st.dataframe(top_gross, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">CERTIFICATE VS BOX OFFICE</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor('#111')
        ax.set_facecolor('#111')
        cert_gi = dff.groupby("certificate")["gross_income"].mean().sort_values(ascending=False).head(8).dropna()
        ax.barh(cert_gi.index[::-1], cert_gi.values[::-1] / 1e6, color="#e50914", alpha=0.8)
        ax.set_xlabel("Avg Gross ($ Million)", color="#aaa")
        ax.tick_params(colors="#aaa")
        for spine in ax.spines.values(): spine.set_edgecolor('#333')
        st.pyplot(fig)

    st.markdown('<div class="section-title">DO MORE STARS = MORE MONEY?</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    star_gi = dff.groupby("num_stars")["gross_income"].mean().dropna()
    ax.bar(star_gi.index.astype(str), star_gi.values / 1e6, color="#e50914", alpha=0.8)
    ax.set_xlabel("Number of Stars", color="#aaa")
    ax.set_ylabel("Avg Gross ($ Million)", color="#aaa")
    ax.tick_params(colors="#aaa")
    for spine in ax.spines.values(): spine.set_edgecolor('#333')
    st.pyplot(fig)


# ─── PAGE: MOVIE EXPLORER ───────────────────────────────────────────────────
elif page == "🔍 Movie Explorer":
    st.markdown('<div class="section-title">SEARCH & FILTER MOVIES</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("Search movie name", "")
    with col2:
        genres_all = sorted(set(g.strip() for gs in df["genre"].dropna() for g in gs.split(",")))
        genre_filter = st.selectbox("Filter by Genre", ["All"] + genres_all)
    with col3:
        cert_filter = st.selectbox("Certificate", ["All"] + sorted(df["certificate"].dropna().unique().tolist()))

    result = dff.copy()
    if search:
        result = result[result["name"].str.contains(search, case=False, na=False)]
    if genre_filter != "All":
        result = result[result["genre"].str.contains(genre_filter, na=False)]
    if cert_filter != "All":
        result = result[result["certificate"] == cert_filter]

    st.markdown(f"**{len(result):,}** results found")
    show_cols = ["name", "year", "rating", "certificate", "genre", "directors_name", "gross_income", "duration"]
    st.dataframe(result[show_cols].sort_values("rating", ascending=False).head(100).reset_index(drop=True),
                 use_container_width=True)

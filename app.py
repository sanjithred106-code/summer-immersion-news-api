import streamlit as st
import requests
import pandas as pd


# ----------------------------
# CONFIG
# ----------------------------

NEWS_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "45fc540501a64424a2da19b698e80989"


st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)


# ----------------------------
# CUSTOM CSS
# ----------------------------

st.markdown(
    """
    <style>

    .news-card {
        border-radius:15px;
        padding:20px;
        margin-bottom:20px;
        background:#f5f7fb;
        box-shadow:0px 3px 10px #cccccc;
    }

    .title {
        font-size:22px;
        font-weight:bold;
        color:#111;
    }

    .source {
        color:#555;
        font-size:14px;
    }

    .desc {
        color:#333;
        font-size:16px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



# ----------------------------
# FUNCTION FETCH NEWS
# ----------------------------

@st.cache_data(ttl=300)
def fetch_news(country, category, keyword, limit):

    params = {
        "apiKey": API_KEY,
        "country": country,
        "pageSize": limit
    }


    if category != "All":
        params["category"] = category


    if keyword.strip():
        params["q"] = keyword


    response = requests.get(
        NEWS_URL,
        params=params
    )


    data = response.json()


    if data.get("status") != "ok":
        return []


    return data["articles"]




# ----------------------------
# SIDEBAR
# ----------------------------

st.sidebar.title("⚙ News Filters")


countries = {
    "India":"in",
    "United States":"us",
    "United Kingdom":"gb",
    "Australia":"au",
    "Canada":"ca",
    "Germany":"de",
    "France":"fr"
}


country_name = st.sidebar.selectbox(
    "Select Location",
    list(countries.keys())
)


country = countries[country_name]



categories = [
    "All",
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology"
]


category = st.sidebar.selectbox(
    "Select Topic",
    categories
)



keyword = st.sidebar.text_input(
    "Search Keyword",
    placeholder="AI, cricket, economy..."
)



limit = st.sidebar.slider(
    "Number of Articles",
    5,
    100,
    20
)



refresh = st.sidebar.button(
    "🔄 Fetch Latest News"
)



# ----------------------------
# MAIN
# ----------------------------

st.title("📰 Advanced News Intelligence Dashboard")


st.write(
    "Live news explorer with filters, search and analytics"
)



if refresh:
    st.cache_data.clear()



articles = fetch_news(
    country,
    category,
    keyword,
    limit
)



if len(articles) == 0:

    st.warning(
        "No news found. Try changing filters."
    )

else:


    st.success(
        f"{len(articles)} articles loaded"
    )


    # ----------------------------
    # DATA PROCESSING
    # ----------------------------


    rows=[]


    for item in articles:

        rows.append(
            {
                "Source":
                    item.get("source",{}).get("name"),

                "Title":
                    item.get("title"),

                "Author":
                    item.get("author"),

                "Published":
                    item.get("publishedAt"),

                "Description":
                    item.get("description"),

                "URL":
                    item.get("url")
            }
        )


    df = pd.DataFrame(rows)



    # ----------------------------
    # METRICS
    # ----------------------------

    c1,c2,c3 = st.columns(3)


    with c1:
        st.metric(
            "Articles",
            len(df)
        )


    with c2:
        st.metric(
            "Sources",
            df["Source"].nunique()
        )


    with c3:
        st.metric(
            "Topic",
            category
        )



    st.divider()



    # ----------------------------
    # NEWS CARDS
    # ----------------------------

    st.subheader("Latest Headlines")


    for article in articles:


        title = article.get(
            "title",
            "No Title"
        )

        desc = article.get(
            "description",
            "No description"
        )


        source = article.get(
            "source",
            {}
        ).get(
            "name",
            "Unknown"
        )


        url = article.get(
            "url",
            ""
        )


        image = article.get(
            "urlToImage"
        )


        st.markdown(
            f"""
            <div class="news-card">

            <div class="title">
            {title}
            </div>

            <p class="source">
            Source: {source}
            </p>

            <p class="desc">
            {desc}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        if image:
            st.image(
                image,
                width=400
            )


        st.link_button(
            "Read Full Article",
            url
        )



    # ----------------------------
    # TABLE VIEW
    # ----------------------------


    st.divider()

    st.subheader(
        "📊 Data View"
    )


    st.dataframe(
        df,
        use_container_width=True
    )



    # ----------------------------
    # DOWNLOAD
    # ----------------------------


    csv = df.to_csv(
        index=False
    )


    st.download_button(
        "⬇ Download News CSV",
        csv,
        "news_data.csv",
        "text/csv"
    )



# ----------------------------
# FOOTER
# ----------------------------

st.sidebar.divider()

st.sidebar.info(
    "Powered by NewsAPI + Streamlit"
)
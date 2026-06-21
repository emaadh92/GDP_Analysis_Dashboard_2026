import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="GDP Analysis Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_gdp_data.csv")

    df.columns = df.columns.str.strip()

    numeric_cols = [
        "GDP_Short",
        "GDP_Full_USD",
        "GDP_Growth_Percent",
        "GDP_per_Capita_USD"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df.dropna(inplace=True)

    return df

df = load_data()

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("Filters")

countries = sorted(df["Country"].unique())

countries = sorted(df["Country"].unique())

# Search Box
country_search = st.sidebar.text_input(
    "🔍 Search Country",
    placeholder="Type country name..."
)

# Filter country list based on search
filtered_countries_list = [
    country
    for country in countries
    if country_search.lower() in country.lower()
]

# Country Selection
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    filtered_countries_list,
    default=filtered_countries_list
)

filtered_df = df[df["Country"].isin(selected_countries)]

if filtered_df.empty:
    st.warning("No data available.")
    st.stop()

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("🌍 Global GDP Analysis Dashboard")
st.markdown("Interactive dashboard for GDP, GDP Per Capita and Economic Growth.")

# ----------------------------
# KPI Cards
# ----------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Countries",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average GDP",
        f"${filtered_df['GDP_Full_USD'].mean():,.0f}"
    )

with col3:
    st.metric(
        "GDP Per Capita",
        f"${filtered_df['GDP_per_Capita_USD'].mean():,.0f}"
    )

with col4:
    st.metric(
        "Growth Rate",
        f"{filtered_df['GDP_Growth_Percent'].mean():.2f}%"
    )

st.divider()




# ----------------------------
# Top GDP Countries
# ----------------------------
st.subheader("Top 10 Countries by GDP")

top_gdp = (
    filtered_df
    .nlargest(10, "GDP_Full_USD")
    .sort_values("GDP_Full_USD")
)

fig1 = px.bar(
    top_gdp,
    x="GDP_Full_USD",
    y="Country",
    orientation="h",
    title="Top 10 Countries by GDP"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# Lowest GDP Countries
# ----------------------------
st.subheader("📉 Countries with Lowest GDP")

lowest_gdp = (
    filtered_df
    .nsmallest(15, "GDP_Full_USD")
    .sort_values("GDP_Full_USD")
)

fig_low_gdp = px.bar(
    lowest_gdp,
    x="GDP_Full_USD",
    y="Country",
    orientation="h",
    title="15 Countries with Lowest GDP"
)

st.plotly_chart(
    fig_low_gdp,
    use_container_width=True
)



# ----------------------------
# Economic Risk Categories
# ----------------------------
st.subheader("🥧 Economic Risk Categories")

risk_df = filtered_df.copy()

risk_df["Risk_Category"] = risk_df["GDP_Growth_Percent"].apply(
    lambda x:
    "High Risk (<0%)"
    if x < 0 else
    "Moderate Risk (0% - 2%)"
    if x < 2 else
    "Healthy Growth (>2%)"
)

fig_risk = px.pie(
    risk_df,
    names="Risk_Category",
    title="Distribution of Economic Risk Levels"
)

st.plotly_chart(
    fig_risk,
    use_container_width=True
)

# ----------------------------
# GDP Per Capita
# ----------------------------
st.subheader("Top 10 GDP Per Capita Countries")

top_pc = (
    filtered_df
    .nlargest(10, "GDP_per_Capita_USD")
    .sort_values("GDP_per_Capita_USD")
)

fig2 = px.bar(
    top_pc,
    x="GDP_per_Capita_USD",
    y="Country",
    orientation="h",
    title="Top GDP Per Capita Countries"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# Growth Rate
# ----------------------------
st.subheader("Fastest Growing Economies")

top_growth = (
    filtered_df
    .nlargest(10, "GDP_Growth_Percent")
    .sort_values("GDP_Growth_Percent")
)

fig3 = px.bar(
    top_growth,
    x="GDP_Growth_Percent",
    y="Country",
    orientation="h",
    title="Top 10 Fastest Growing Economies"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# Scatter Plot
# ----------------------------
st.subheader("GDP vs GDP Per Capita")

fig4 = px.scatter(
    filtered_df,
    x="GDP_Full_USD",
    y="GDP_per_Capita_USD",
    hover_name="Country",
    size="GDP_Full_USD",
    title="GDP vs GDP Per Capita"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# GDP Distribution
# ----------------------------
st.subheader("GDP Distribution")

fig5 = px.histogram(
    filtered_df,
    x="GDP_Full_USD",
    nbins=25,
    title="GDP Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# Top 20 Data Table
# ----------------------------
st.subheader("Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ----------------------------
# Download Button
# ----------------------------
csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data",
    data=csv,
    file_name="filtered_gdp_data.csv",
    mime="text/csv"
)

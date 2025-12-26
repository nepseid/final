import pandas as pd
import streamlit as st
import altair as alt

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Fundamentals Dashboard", layout="wide")

# ================= LOAD DATA =================
df = pd.read_excel("Fundamentals.xlsx", sheet_name="Sheet1")

# ================= CLEAN & PREP =================
excluded_sectors = ["zdelist", "Non List"]
df = df[~df["Sector"].isin(excluded_sectors)].copy()

# Ensure numeric columns
numeric_cols = [
    "Price", "BOOK VALUE", "EPS", "Dps", "PE",
    "ROE", "NPL", "Public Shares"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Sort by Year & Quarter to get latest
df = df.sort_values(["Year", "Quarter"])

latest_year = df["Year"].iloc[-1]
latest_quarter = df["Quarter"].iloc[-1]

# ================= HEADER =================


# ================= HELPERS =================
def parse_filter(val):
    try:
        return float(val)
    except:
        return None

# ================= FILTER UI =================
col1, col2, col3 = st.columns(3)

with col1:
    year_filter = st.selectbox(
        "Select Year",
        sorted(df["Year"].unique(), reverse=True),
        index=0
    )
    from_price = st.text_input("From Price (Rs)", value="All")

with col2:
    quarter_filter = st.selectbox(
        "Select Quarter",
        sorted(df["Quarter"].unique()),
        index=sorted(df["Quarter"].unique()).index(latest_quarter)
    )
    to_price = st.text_input("To Price (Rs)", value="All")

with col3:
    from_book = st.text_input("From Book Value", value="All")
    to_book = st.text_input("To Book Value", value="All")

col4, col5 = st.columns(2)

with col4:
    eps_filter = st.selectbox(
        "Select EPS Filter",
        ["All", "Positive", "Negative", "More than 0", "More than 5",
         "More than 10", "More than 20", "More than 50"]
    )

with col5:
    dps_filter = st.selectbox(
        "Select DPS Filter",
        ["All", "Positive", "Negative", "More than 0", "More than 5",
         "More than 10", "More than 20", "More than 50"]
    )

sector_options = sorted(df["Sector"].unique())
sector_filter = st.multiselect(
    "Select Sector",
    sector_options,
    default=sector_options
)

# ================= APPLY FILTERS =================
if st.button("Apply"):

    df_f = df[
        (df["Year"] == year_filter) &
        (df["Quarter"] == quarter_filter) &
        (df["Sector"].isin(sector_filter))
    ].copy()

    # Price filter
    fp, tp = parse_filter(from_price), parse_filter(to_price)
    if fp is not None:
        df_f = df_f[df_f["Price"] >= fp]
    if tp is not None:
        df_f = df_f[df_f["Price"] <= tp]

    # Book value filter
    fb, tb = parse_filter(from_book), parse_filter(to_book)
    if fb is not None:
        df_f = df_f[df_f["BOOK VALUE"] >= fb]
    if tb is not None:
        df_f = df_f[df_f["BOOK VALUE"] <= tb]

    # EPS / DPS logic
    ops = {
        "Positive": lambda x: x > 0,
        "Negative": lambda x: x < 0,
        "More than 0": lambda x: x > 0,
        "More than 5": lambda x: x > 5,
        "More than 10": lambda x: x > 10,
        "More than 20": lambda x: x > 20,
        "More than 50": lambda x: x > 50,
    }

    if eps_filter != "All":
        df_f = df_f[df_f["EPS"].apply(ops[eps_filter])]
    if dps_filter != "All":
        df_f = df_f[df_f["Dps"].apply(ops[dps_filter])]

    # ================= PBV =================
    df_f["PBV"] = (df_f["Price"] / df_f["BOOK VALUE"]).round(1)
    df_f = df_f.sort_values("Price")

    # ================= CHART BUILDER =================
    def bar_chart(data, y_col, title, fmt=None):
        y = alt.Y(f"{y_col}:Q", title=y_col)
        if fmt:
            y = y.axis(format=fmt)

        base = alt.Chart(data).encode(
            x=alt.X("SYMBOL:N", sort=None),
            y=y,
            tooltip=["SYMBOL", y_col],
            color=alt.Color("SYMBOL:N", legend=None),
        )

        # Bar with text overlay
        bars = base.mark_bar()
        text = base.mark_text(
            dy=-5,  # move text slightly above the bar
            color="black"
        ).encode(
            text=alt.Text(f"{y_col}:Q")
        )

        chart = (bars + text).properties(title=title, height=350)
        return chart

    # ================= CHARTS =================
    charts = [
        bar_chart(df_f, "Price", "Current Price"),
        bar_chart(df_f, "EPS", f"EPS {year_filter} Q{quarter_filter}"),
        bar_chart(df_f, "PE", f"PE {year_filter} Q{quarter_filter}"),
        bar_chart(df_f, "PBV", "PBV (Price / Book Value)", fmt=".1f"),
        bar_chart(df_f, "BOOK VALUE", "Book Value"),
        bar_chart(df_f, "Public Shares", "Public Shares"),
        bar_chart(df_f, "ROE", "ROE"),
        bar_chart(df_f, "NPL", "NPL"),
        bar_chart(df_f, "Dps", f"DPS {year_filter} Q{quarter_filter}"),
    ]

    # ================= DISPLAY =================
    for c in charts:
        st.altair_chart(c, use_container_width=True)

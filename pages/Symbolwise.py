import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Scrip Analysis",
    layout="wide"
)



# ================= LOAD DATA =================
df = pd.read_excel("Fundamentals.xlsx", sheet_name="Sheet1")
df = df.reset_index(drop=True)

df["Timeframe"] = df["Quarter"].astype(str) + "-" + df["Year"].astype(str)

# Latest quarter from file order
latest_quarter = df["Quarter"].iloc[-1]

# ================= FILTERS =================
col1, col2 = st.columns(2)

with col1:
    symbol = st.selectbox(
        "Select Symbol",
        sorted(df["SYMBOL"].unique())
    )

with col2:
    quarter_list = sorted(df["Quarter"].unique())
    quarter = st.selectbox(
        "Select Quarter",
        quarter_list,
        index=quarter_list.index(latest_quarter)
    )

# ================= FILTER DATA =================
df_filtered = df[(df["SYMBOL"] == symbol) & (df["Quarter"] == quarter)]

if df_filtered.empty:
    st.warning("No data available for the selected symbol and quarter.")
    st.stop()

# ================= CURRENT PRICE =================
st.markdown(
    f"""
    <p style="font-size:24px; font-weight:bold; text-align:center;">
    Current Price: Rs. {df_filtered["Price"].iloc[0]:.2f}
    </p>
    """,
    unsafe_allow_html=True
)

# ================= BASIC BAR CHARTS =================
def simple_bar(df_plot, y, title):
    fig = px.bar(
        df_plot,
        x="Timeframe",
        y=y,
        title=title,
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )
    fig.update_traces(texttemplate="%{y}", textposition="auto")
    fig.update_layout(
        showlegend=False,
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    return fig

fig_eps = simple_bar(df_filtered, "EPS", f"<b>EPS – {symbol}</b>")
fig_dps = simple_bar(df_filtered, "Dps", f"<b>DPS – {symbol}</b>")
fig_roe = simple_bar(df_filtered, "ROE", f"<b>ROE – {symbol}</b>")
fig_book = simple_bar(df_filtered, "BOOK VALUE", f"<b>Book Value – {symbol}</b>")

# ================= PAID-UP =================
df_paid = df_filtered.copy()
df_paid["Capital"] = df_paid["PAID-UP"] * 1000
fig_paid = simple_bar(df_paid, "Capital", f"<b>Paid-Up Capital – {symbol}</b>")

# ================= EPS + CAPITAL COMBO =================
fig_capeps = make_subplots(specs=[[{"secondary_y": True}]])

fig_capeps.add_trace(
    go.Bar(
        x=df_filtered["Timeframe"],
        y=df_filtered["EPS"],
        name="EPS",
        marker_color="#0083B8"
    ),
    secondary_y=False
)

fig_capeps.add_trace(
    go.Scatter(
        x=df_filtered["Timeframe"],
        y=df_filtered["PAID-UP"] * 1000,
        name="Capital",
        line=dict(color="#FBB13C")
    ),
    secondary_y=True
)

fig_capeps.update_layout(
    title=f"<b>EPS & Capital – {symbol}</b>",
    dragmode=False,
    template="plotly_white"
)

fig_capeps.update_xaxes(fixedrange=True)
fig_capeps.update_yaxes(title_text="EPS", fixedrange=True, secondary_y=False)
fig_capeps.update_yaxes(title_text="Capital", fixedrange=True, secondary_y=True)

# ================= LATEST YEAR =================
latest_year = df["Year"].iloc[-1]

df_year = df[(df["SYMBOL"] == symbol) & (df["Year"] == latest_year)]

# ================= NPL =================
fig_npl = None
if not df_year.empty:
    fig_npl = px.bar(
        df_year,
        x="Quarter",
        y="NPL",
        title=f"<b>NPL – {symbol} ({latest_year})</b>",
        template="plotly_white",
        color_discrete_sequence=["#0083B8"]
    )
    fig_npl.update_traces(texttemplate="%{y}", textposition="auto")
    fig_npl.update_layout(dragmode=False)

# ================= NET PROFIT =================
fig_profit = None
if not df_year.empty:
    df_year = df_year.copy()
    df_year["NetProfit"] = df_year["NET PROFIT"] * 1000

    fig_profit = px.bar(
        df_year,
        x="Quarter",
        y="NetProfit",
        title=f"<b>Net Profit – {symbol} ({latest_year})</b>",
        template="plotly_white",
        color_discrete_sequence=["#0083B8"]
    )
    fig_profit.update_traces(texttemplate="%{y:.2s}", textposition="auto")
    fig_profit.update_layout(dragmode=False)

# ================= BONUS / CASH =================
df_bonus = df[df["SYMBOL"] == symbol]

fig_bonus = None
if not df_bonus.empty:
    bonus_avg = df_bonus.groupby("Year")[["Bonus", "Cash"]].mean().reset_index()

    fig_bonus = px.bar(
        bonus_avg,
        x="Year",
        y=["Bonus", "Cash"],
        barmode="stack",
        title=f"<b>Bonus & Cash Dividend – {symbol}</b>",
        template="plotly_white",
        color_discrete_sequence=["#0083B8", "#FBB13C"]
    )
    fig_bonus.update_layout(dragmode=False)

# ================= DISPLAY =================
st.plotly_chart(fig_eps, width="stretch")
st.plotly_chart(fig_dps, width="stretch")
st.plotly_chart(fig_book, width="stretch")
st.plotly_chart(fig_roe, width="stretch")
st.plotly_chart(fig_paid, width="stretch")

if fig_profit:
    st.plotly_chart(fig_profit, width="stretch")

st.plotly_chart(fig_capeps, width="stretch")

if fig_npl:
    st.plotly_chart(fig_npl, width="stretch")

if fig_bonus:
    st.plotly_chart(fig_bonus, width="stretch")

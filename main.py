import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Fundamental Analysis",
    
    layout="wide"
)



# ================= LOAD DATA =================
df = pd.read_excel("Fundamentals.xlsx", sheet_name="Sheet1")
df = df.reset_index(drop=True)

# Auto-pick latest year & quarter from last row
latest_year = df["Year"].iloc[-1]
latest_quarter = df["Quarter"].iloc[-1]

# ================= FILTERS =================
st.header("Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    sector = st.selectbox(
        "Sector",
        sorted(df["Sector"].dropna().unique())
    )

with col2:
    year_list = sorted(df["Year"].unique())
    year = st.selectbox(
        "Year",
        year_list,
        index=year_list.index(latest_year)
    )

with col3:
    quarter_list = sorted(df["Quarter"].unique())
    quarter = st.selectbox(
        "Quarter",
        quarter_list,
        index=quarter_list.index(latest_quarter)
    )

symbols = df.query("Sector == @sector")["SYMBOL"].unique()
symbols = ["All"] + sorted(symbols)

selected_symbol = st.selectbox("Scripts", symbols)

# ================= FILTER DATA =================
if selected_symbol == "All":
    df_sel = df.query(
        "Sector == @sector & Year == @year & Quarter == @quarter"
    )
else:
    df_sel = df.query(
        "Sector == @sector & Year == @year & Quarter == @quarter & SYMBOL == @selected_symbol"
    )

# ================= HELPERS =================
def format_value(v):
    if abs(v) >= 1e9:
        return f"{v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"{v/1e6:.2f}M"
    if abs(v) >= 1e3:
        return f"{v/1e3:.2f}K"
    return f"{v:.2f}"

def bar_chart(series, title, decimals=2):
    df_plot = series.to_frame("value").copy()

    df_plot["label"] = df_plot["value"].round(decimals).astype(str)

    fig = px.bar(
        df_plot,
        x=df_plot.index,
        y="value",
        text="label",
        title=f"<b>{title}</b>",
        template="plotly_white",
        color_discrete_sequence=["#0083B8"]
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        margin=dict(t=60)
    )
    return fig

# ================= AGGREGATIONS =================
price = df_sel.groupby("SYMBOL")["Price"].mean().sort_values()
book_value = df_sel.groupby("SYMBOL")["BOOK VALUE"].mean().sort_values()

eps = df_sel.groupby("SYMBOL")["EPS"].mean().sort_values()
dps = df_sel.groupby("SYMBOL")["Dps"].mean().sort_values()
pe = df_sel.groupby("SYMBOL")["PE"].mean().sort_values()
npl = df_sel.groupby("SYMBOL")["NPL"].mean().sort_values()

paid_up = (df_sel.groupby("SYMBOL")["PAID-UP"].sum() * 1000).sort_values()
net_profit = (df_sel.groupby("SYMBOL")["NET PROFIT"].sum() * 1000).sort_values()
public_shares = df_sel.groupby("SYMBOL")["Public Shares"].sum().sort_values()
reserve = df_sel.groupby("SYMBOL")["RESERVE"].sum().sort_values()

# ================= PBV =================
pbv = (price / book_value).dropna().round(1).sort_values()

# ================= EPS vs DPS =================
eps_dps = df_sel.groupby("SYMBOL")[["EPS", "Dps"]].mean()

fig_eps_dps = go.Figure([
    go.Bar(name="EPS", x=eps_dps.index, y=eps_dps["EPS"]),
    go.Bar(name="DPS", x=eps_dps.index, y=eps_dps["Dps"])
])

fig_eps_dps.update_layout(
    title="<b>EPS vs DPS</b>",
    template="plotly_white",
    barmode="group",
    dragmode=False,
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True)
)

# ================= DISPLAY =================
st.plotly_chart(bar_chart(price, "Last Traded Price"), width="stretch")
st.plotly_chart(bar_chart(book_value, "Book Value"), width="stretch")
st.plotly_chart(bar_chart(pbv, "PBV (Price to Book Value)", decimals=1), width="stretch")

st.plotly_chart(bar_chart(public_shares, "Public Shares"), width="stretch")
st.plotly_chart(bar_chart(paid_up, "Paid-Up Capital"), width="stretch")
st.plotly_chart(fig_eps_dps, width="stretch")
st.plotly_chart(bar_chart(pe, "PE Ratio"), width="stretch")
st.plotly_chart(bar_chart(net_profit, "Net Profit"), width="stretch")
st.plotly_chart(bar_chart(reserve, "Reserve"), width="stretch")
st.plotly_chart(bar_chart(npl, "NPL"), width="stretch")
st.plotly_chart(bar_chart(eps, "EPS"), width="stretch")
st.plotly_chart(bar_chart(dps, "DPS"), width="stretch")

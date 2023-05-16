import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Fundamental Analysis",
                   page_icon="bar_chart:", layout="wide")
st.title("Fundamental Analysis")

df = pd.read_excel(
    '/Users/vuone/Desktop/Code/Fundamental Analysis/Fundamentals.xlsx', sheet_name='Sheet1')

st.sidebar.header("Parameters")

Sector = st.sidebar.selectbox(
    "Sector:", options=sorted(df["Sector"].unique()), index=0)
df_sector = df.query("Sector == @Sector")

Year = st.sidebar.selectbox("Year", sorted(df["Year"].unique()), index=6)
Quarter = st.sidebar.selectbox(
    "Quarter", sorted(df["Quarter"].unique()), index=0)
SYMBOL = st.sidebar.multiselect("Scips:", options=df_sector["SYMBOL"].unique(
), default=df_sector["SYMBOL"].unique())
df_selection = df.query(
    "Sector==@Sector & Year==@Year & Quarter==@Quarter & SYMBOL==@SYMBOL")


def format_value(value):
    if value >= 1e9:
        return f"{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{value/1e3:.2f}K"
    else:
        return f"{value:.2f}"


def create_bar_chart(data, x, y, title):
    data["formatted_value"] = data[y].apply(format_value)
    fig = px.bar(
        data,
        x=x,
        y=y,
        text=data["formatted_value"],
        orientation="v",
        title=f"<b>{title}</b>",
        color_discrete_sequence=["#0083B8"] * len(data),
        template="plotly_white"
    )
    fig.update_traces(textposition="outside")
    return fig


# Last Traded Price
price = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["Price"]].sort_values(by="Price")
fig_price = create_bar_chart(price, price.index, "Price", "Last Traded Price")

# Capital Framework
paid_up = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["PAID-UP"]].sort_values(by="PAID-UP")
paid_up["PAID-UP"] *= 1000  # Multiply the "PAID-UP" values by 1000
fig_paid_up = create_bar_chart(
    paid_up, paid_up.index, "PAID-UP", "Capital Framework")
fig_paid_up.update_traces(hovertemplate="<b>Capital:</b> %{y}")

# EPS
eps = df_selection.groupby(by=["SYMBOL"]).sum()[["EPS"]].sort_values(by="EPS")
fig_eps = create_bar_chart(eps, eps.index, "EPS", "EPS")

# Book Value
bookvalue = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["BOOK VALUE"]].sort_values(by="BOOK VALUE")
fig_bookvalue = create_bar_chart(
    bookvalue, bookvalue.index, "BOOK VALUE", "Book Value")

# DPS
dps = df_selection.groupby(by=["SYMBOL"]).sum()[["Dps"]].sort_values(by="Dps")
fig_dps = create_bar_chart(dps, dps.index, "Dps", "DPS")

# Net Profit
netprofit = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["NET PROFIT"]].sort_values(by="NET PROFIT")
netprofit["NET PROFIT"] *= 1000  # Multiply the "Net Profit" values by 1000
fig_netprofit = create_bar_chart(
    netprofit, netprofit.index, "NET PROFIT", "Net Profit")
fig_netprofit.update_traces(hovertemplate="<b>Net Profit:</b> %{y}")

# PE Ratio

pe = df_selection.groupby(by=["SYMBOL"]).sum()[["PE"]].sort_values(by="PE")
fig_pe = create_bar_chart(pe, pe.index, "PE", "PE Ratio")

# EPS and DPS

eps_dps = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["EPS", "Dps"]].sort_values(by="EPS")
fig_eps_dps = go.Figure()
fig_eps_dps.add_trace(go.Bar(
    x=eps_dps.index,
    y=eps_dps["EPS"],
    name="EPS",
    marker_color="#0083B8",
    hovertemplate="<b>EPS:</b> %{y}<extra></extra>",
    text=eps_dps["EPS"],
    textposition="auto",
))
fig_eps_dps.add_trace(go.Bar(
    x=eps_dps.index,
    y=eps_dps["Dps"],
    name="DPS",
    marker_color="#FFA15A",
    hovertemplate="<b>DPS:</b> %{y}<extra></extra>",
    text=eps_dps["Dps"],
    textposition="auto",
))
fig_eps_dps.update_layout(
    title="<b>EPS and DPS</b>",
    template="plotly_white",
    xaxis_title="Symbol",
    yaxis_title="Value",
    legend=dict(x=0.7, y=1),
)

# Display charts

st.plotly_chart(fig_price, use_container_width=True)
st.plotly_chart(fig_paid_up, use_container_width=True)
st.plotly_chart(fig_eps_dps, use_container_width=True)
st.plotly_chart(fig_bookvalue, use_container_width=True)
st.plotly_chart(fig_eps, use_container_width=True)
st.plotly_chart(fig_dps, use_container_width=True)
st.plotly_chart(fig_pe, use_container_width=True)
st.plotly_chart(fig_netprofit, use_container_width=True)

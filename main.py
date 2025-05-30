import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Fundamental Analysis",
                   page_icon="bar_chart:", layout="wide")
st.title("Fundamental Analysis")

df = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')

# Header for filters
st.header("Parameters")

# Create a row with 3 columns for the filters
col1, col2, col3 = st.columns(3)

with col1:
    Sector = st.selectbox("Sector:", options=sorted(
        df["Sector"].unique()), index=0)
    Quarter = st.selectbox("Quarter", sorted(df["Quarter"].unique()), index=2)

with col2:
    Year = st.selectbox("Year", sorted(df["Year"].unique()), index=8)

with col3:
    symbols = df.query("Sector == @Sector")["SYMBOL"].unique()
    symbols_with_all = ["All"] + list(symbols)  # Add "All" option
    selected_symbols = st.selectbox(
        "Scips:", options=symbols_with_all, index=0
    )

# Apply the selected filters to the dataframe
if selected_symbols == "All":
    df_selection = df.query(
        "Sector == @Sector & Year == @Year & Quarter == @Quarter")
else:
    df_selection = df.query(
        "Sector == @Sector & Year == @Year & Quarter == @Quarter & SYMBOL == @selected_symbols"
    )

# Helper function to format values


def format_value(value):
    if value >= 1e9:
        return f"{value/1e9:.2f}B"
    elif value >= 1e6:
        return f"{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{value/1e3:.2f}K"
    else:
        return f"{value:.2f}"

# Function to create bar charts


def create_bar_chart(data, x, y, title):
    data["v"] = data[y].apply(format_value)
    fig = px.bar(
        data,
        x=x,
        y=y,
        text=data["v"],
        orientation="v",
        title=f"<b>{title}</b>",
        color_discrete_sequence=["#0083B8"] * len(data),
        template="plotly_white"
    )
    fig.update_traces(textposition="outside")

    # Disable zooming
    fig.update_layout(
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    return fig


# Create charts
price = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["Price"]].sort_values(by="Price")
fig_price = create_bar_chart(price, price.index, "Price", "Last Traded Price")

paid_up = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["PAID-UP"]].sort_values(by="PAID-UP")
paid_up["PAID-UP"] *= 1000
fig_paid_up = create_bar_chart(
    paid_up, paid_up.index, "PAID-UP", "Capital Framework")

eps = df_selection.groupby(by=["SYMBOL"]).sum()[["EPS"]].sort_values(by="EPS")
fig_eps = create_bar_chart(eps, eps.index, "EPS", "EPS")

bookvalue = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["BOOK VALUE"]].sort_values(by="BOOK VALUE")
fig_bookvalue = create_bar_chart(
    bookvalue, bookvalue.index, "BOOK VALUE", "Book Value")

dps = df_selection.groupby(by=["SYMBOL"]).sum()[["Dps"]].sort_values(by="Dps")
fig_dps = create_bar_chart(dps, dps.index, "Dps", "DPS")

netprofit = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["NET PROFIT"]].sort_values(by="NET PROFIT")
netprofit["NET PROFIT"] *= 1000
fig_netprofit = create_bar_chart(
    netprofit, netprofit.index, "NET PROFIT", "Net Profit")

pe = df_selection.groupby(by=["SYMBOL"]).sum()[["PE"]].sort_values(by="PE")
fig_pe = create_bar_chart(pe, pe.index, "PE", "PE Ratio")

npl = df_selection.groupby(by=["SYMBOL"]).sum()[["NPL"]].sort_values(by="NPL")
fig_npl = create_bar_chart(npl, npl.index, "NPL", "NPL")

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
    dragmode=False,
    xaxis=dict(fixedrange=True),
    yaxis=dict(fixedrange=True)
)

ps = df_selection.groupby(by=["SYMBOL"]).sum(
)[["Public Shares"]].sort_values(by="Public Shares")
fig_ps = create_bar_chart(ps, ps.index, "Public Shares", "Public Shares")

reserve = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["RESERVE"]].sort_values(by="RESERVE")
fig_reserve = create_bar_chart(reserve, reserve.index, "RESERVE", "RESERVE")

# Display charts
st.plotly_chart(fig_price, use_container_width=True)
st.plotly_chart(fig_ps, use_container_width=True)
st.plotly_chart(fig_paid_up, use_container_width=True)
st.plotly_chart(fig_eps_dps, use_container_width=True)
st.plotly_chart(fig_bookvalue, use_container_width=True)
st.plotly_chart(fig_pe, use_container_width=True)
st.plotly_chart(fig_netprofit, use_container_width=True)
st.plotly_chart(fig_reserve, use_container_width=True)
st.plotly_chart(fig_npl, use_container_width=True)
st.plotly_chart(fig_eps, use_container_width=True)
st.plotly_chart(fig_dps, use_container_width=True)

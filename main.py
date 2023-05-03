import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.set_page_config(page_title="Fundamental Analysis",
                   page_icon="bar_chart:",
                   layout="wide"
                   )

st.title("Fundamental Analysis")

hide_menu_style = """
    <style>
        #MainMenu {display:none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

df = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')


st.sidebar.header("Parameters")


Sector = st.sidebar.selectbox(
    "Sector:",
    options=sorted(df["Sector"].unique()), index=0
)

df_sector = df.query("Sector == @Sector")

Year = st.sidebar.selectbox(
    "Year", sorted(df["Year"].unique()), index=6)

Quarter = st.sidebar.selectbox(
    "Quarter", sorted(df["Quarter"].unique()), index=0)


SYMBOL = st.sidebar.multiselect(
    "Scips:",
    options=df_sector["SYMBOL"].unique(),
    default=df_sector["SYMBOL"].unique()
)

df_selection = df.query(
    "Sector==@Sector & Year==@Year & Quarter==@Quarter & SYMBOL==@SYMBOL"


)

price = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["Price"]].sort_values(by="Price")
)
fig_price = px.bar(
    price,
    x=price.index,
    y=("Price"),
    orientation="v",
    title="<b>Last Traded Price </b>",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white",
)


paid_up = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["PAID-UP"]].sort_values(by="PAID-UP")
)
fig_paid_up = px.bar(
    paid_up,
    x=paid_up.index,
    y=("PAID-UP"),
    orientation="v",
    title="<b>Capital Framework</b>",
    color_discrete_sequence=["#0083B8"]*len(paid_up),
    template="plotly_white",
)

eps = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["EPS"]].sort_values(by="EPS")
)

fig_eps = px.bar(
    eps,
    x=eps.index,
    y=("EPS"),
    orientation="v",
    title="<b>EPS</b>",
    color_discrete_sequence=["#0083B8"]*len(eps),
    template="plotly_white",
)

bookvalue = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["BOOK VALUE"]].sort_values(by="BOOK VALUE")
)

fig_bookvalue = px.bar(
    bookvalue,
    x=bookvalue.index,
    y=("BOOK VALUE"),
    orientation="v",
    title="<b>Book Value</b>",
    color_discrete_sequence=["#0083B8"]*len(eps),
    template="plotly_white",
)
dps = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["Dps"]].sort_values(by="Dps")
)


fig_dps = px.bar(
    dps,
    x=dps.index,
    y=("Dps"),
    orientation="v",
    title="<b>Dps</b>",
    color_discrete_sequence=["#0083B8"]*len(dps),
    template="plotly_white",
)


netprofit = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["NET PROFIT"]].sort_values(by="NET PROFIT")
)


fig_netprofit = px.bar(
    netprofit,
    x=netprofit.index,
    y=("NET PROFIT"),
    orientation="v",
    title="<b>Net Profit</b>",
    color_discrete_sequence=["#0083B8"]*len(eps),
    template="plotly_white",
)

pe = (
    df_selection.groupby(by=["SYMBOL"]).sum()[
        ["PE"]].sort_values(by="PE")
)


fig_pe = px.bar(
    pe,
    x=pe.index,
    y=("PE"),
    orientation="v",
    title="<b>PE Ratio</b>",
    color_discrete_sequence=["#0083B8"]*len(eps),
    template="plotly_white",
)
eps_dps = df_selection.groupby(by=["SYMBOL"]).sum()[
    ["EPS", "Dps"]].sort_values(by="EPS")

fig_eps_dps = make_subplots(specs=[[{"secondary_y": True}]])

fig_eps_dps.add_trace(
    go.Bar(x=eps_dps.index, y=eps_dps["EPS"],
           name="EPS", marker_color="#0083B8",
           hovertemplate="<b>EPS:</b> %{y}<br><b>DPS:</b> %{text}<extra></extra>",
           text=eps_dps["Dps"].values),
    secondary_y=False
)

fig_eps_dps.add_trace(
    go.Bar(x=eps_dps.index, y=eps_dps["Dps"],
           name="DPS", marker_color="#FFA15A",
           hovertemplate="<b>DPS:</b> %{y}<br><b>EPS:</b> %{text}<extra></extra>",
           text=eps_dps["EPS"].values),
    secondary_y=True
)

fig_eps_dps.update_layout(
    title="<b>EPS and DPS</b>",
    template="plotly_white",
    xaxis_title="Symbol",
    yaxis_title="EPS",
    yaxis2_title="DPS",
    legend=dict(x=0.7, y=1),
    yaxis=dict(range=[0, max(eps_dps["EPS"].max(), eps_dps["Dps"].max())]),
    yaxis2=dict(range=[0, max(eps_dps["EPS"].max(), eps_dps["Dps"].max())]),
)

st.plotly_chart(fig_price, use_container_width=True,config={
        "modeBarButtonsToRemove": ["zoomIn2d", "zoomOut2d", "autoScale2d"],
        "dragmode": "pan"
    })
st.plotly_chart(fig_paid_up, use_container_width=True)
st.plotly_chart(fig_eps_dps, use_container_width=True)
st.plotly_chart(fig_bookvalue, use_container_width=True)
st.plotly_chart(fig_eps, use_container_width=True)
st.plotly_chart(fig_dps, use_container_width=True)
st.plotly_chart(fig_pe, use_container_width=True)
st.plotly_chart(fig_netprofit, use_container_width=True)

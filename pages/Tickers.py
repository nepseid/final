import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(
    page_title="Scrip Analysis",
    page_icon="bar_chart:",
    layout="wide"
)

st.title("Scrips")

df1 = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')


Timeframe = df1["Quarter"] + "-" + df1["Year"]
df1 = df1.assign(Timeframe=Timeframe)

# Create a sidebar with filter inputs
symbol = st.sidebar.selectbox(
    "Symbol", sorted(df1["SYMBOL"].unique()), index=1
)
quarter = st.sidebar.selectbox(
    "Quarter", sorted(df1["Quarter"].unique()), index=0
)

# Filter the dataframe based on the sidebar inputs
df_filtered = df1[(df1["SYMBOL"] == symbol) & (df1["Quarter"] == quarter)]

if not df_filtered.empty:
    Timeframe = df_filtered["Quarter"].astype(
        str) + "-" + df_filtered["Year"].astype(str)
    df_filtered = df_filtered.assign(Timeframe=Timeframe)

    fig_eps2 = px.bar(
        df_filtered,
        x="Timeframe",
        y="EPS",
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>EPS for {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_paidup2 = px.bar(
        df_filtered,
        x="Timeframe",
        y="PAID-UP",
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>Capital for {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_roe = px.bar(
        df_filtered,
        x="Timeframe",
        y="ROE",
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>ROE for {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )
    # Create a subplot with two y-axes
    fig_capeps = make_subplots(specs=[[{"secondary_y": True}]])

    # Add a bar chart to the primary y-axis
    fig_capeps.add_trace(
        px.bar(
            df_filtered,
            x="Timeframe",
            y="EPS",
            color="SYMBOL",
            facet_col="SYMBOL",
            facet_col_spacing=0.005,
            orientation="v",
            color_discrete_sequence=["#0083B8"],
            template="plotly_white"
        ).data[0],
        secondary_y=False
    )

    # Add a line chart to the secondary y-axis
    fig_capeps.add_trace(
        go.Scatter(
            x=df_filtered["Timeframe"],
            y=df_filtered["PAID-UP"],
            mode="lines",
            name="Capital",
            line=dict(color="#FBB13C")
        ),
        secondary_y=True
    )

    # Set the axis labels and titles
    fig_capeps.update_xaxes(title_text="Timeframe")
    fig_capeps.update_yaxes(title_text="EPS", secondary_y=False)
    fig_capeps.update_yaxes(title_text="PAID-UP", secondary_y=True)

    # Set the figure title
fig_capeps.update_layout(
    title=f"<b>EPS and Capital for {symbol}, {quarter}</b>"
)
fig_eps2.update_layout(showlegend=False)
fig_paidup2.update_layout(showlegend=False)
fig_roe.update_layout(showlegend=False)
fig_capeps.update_layout(showlegend=False)


# Filter the dataframe for cash and bonus combo chart (without quarter filter)
df_filtered_combo = df1[df1["SYMBOL"] == symbol]

if not df_filtered_combo.empty:
    # Calculate the average values of cash and bonus for each year
    avg_cash_bonus = df_filtered_combo.groupby("Year").agg(
        {"Bonus": "mean", "Cash": "mean"}).reset_index()

    # Create a combo bar chart with average values
    fig_combo = make_subplots(specs=[[{"secondary_y": True}]])

    # Add a bar chart with average bonus values to the primary y-axis
    fig_combo.add_trace(
        go.Bar(
            x=avg_cash_bonus["Year"],
            y=avg_cash_bonus["Bonus"],
            name="Bonus",
            marker_color="#0083B8",
            hovertemplate="Year: %{x}<br>Bonus: %{y}"
        ),
        secondary_y=False
    )

    # Add a line chart with average cash values to the secondary y-axis
    fig_combo.add_trace(
        go.Scatter(
            x=avg_cash_bonus["Year"],
            y=avg_cash_bonus["Cash"],
            name="Cash",
            line=dict(color="#FBB13C"),
            hovertemplate="Year: %{x}<br>Cash: %{y}"
        ),
        secondary_y=True
    )

    # Set the axis labels and titles
    fig_combo.update_xaxes(title_text="Year")
    fig_combo.update_yaxes(title_text="Bonus", secondary_y=False)
    fig_combo.update_yaxes(title_text="Cash", secondary_y=True)

    # Set the figure title
    fig_combo.update_layout(
        title=f"<b>Bonus Dividend {symbol}</b>",
        showlegend=False
    )

    # Create a combo bar chart with average values

    st.plotly_chart(fig_eps2, use_container_width=True)
    st.plotly_chart(fig_combo, use_container_width=True)
    st.plotly_chart(fig_roe, use_container_width=True)
    st.plotly_chart(fig_paidup2, use_container_width=True)
    st.plotly_chart(fig_capeps, use_container_width=True)

else:
    st.write("No data available for the selected symbol.")

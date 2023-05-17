import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

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

    # Display the Price
    st.markdown(
        f"<p style='font-size:24px; font-weight:bold; text-align:center;'>Current Price Rs. {df_filtered['Price'].values[0]:.2f}</p>", unsafe_allow_html=True)

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

    fig_eps2.update_layout(
        showlegend=False,
        dragmode=False,  # Disable zooming
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    fig_eps2.update_traces(
        hovertemplate='<br>EPS: %{y}',
        hoverlabel=dict(namelength=0),
        # Format values in thousands, millions, billions
        texttemplate='%{y:.2s}',
        textposition='auto'  # Show values on the bars
    )

    fig_paidup2 = px.bar(
        df_filtered,
        x="Timeframe",
        y=df_filtered["PAID-UP"] * 1000,
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>Capital for {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_paidup2.update_layout(
        showlegend=False,
        dragmode=False,  # Disable zooming
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    fig_paidup2.update_traces(
        hovertemplate='<br>Capital: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y}',  # Format values in thousands, millions, billions
        textposition='auto'  # Show values on the bars
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

    fig_roe.update_layout(
        showlegend=False,
        dragmode=False,  # Disable zooming
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    fig_roe.update_traces(
        hovertemplate='<br>ROE: %{y}',
        hoverlabel=dict(namelength=0),
        # Format values in thousands, millions, billions
        texttemplate='%{y}',
        textposition='auto'  # Show values on the bars
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
            y=df_filtered["PAID-UP"] * 1000,
            mode="lines",
            name="Capital",
            line=dict(color="#FBB13C")
        ),
        secondary_y=True
    )

# Set the axis labels and titles
    fig_capeps.update_xaxes(title_text="Timeframe", fixedrange=True)
    fig_capeps.update_yaxes(
        title_text="EPS", secondary_y=False, fixedrange=True)
    fig_capeps.update_yaxes(title_text="PAID-UP",
                            secondary_y=True, fixedrange=True)

# Set the figure title
    fig_capeps.update_layout(
        title=f"<b>EPS and Capital for {symbol}, {quarter}</b>",
        dragmode=False  # Disable zooming
    )


# Filter the dataframe for NPL chart (with the latest year at index 6)
# Get the latest year from the unique values
latest_year = df1["Year"].unique()[-1]
df_npl = df1[(df1["SYMBOL"] == symbol) & (df1["Year"] == latest_year)]

if not df_npl.empty:
    fig_npl = px.bar(
        df_npl,
        x="Quarter",
        y="NPL",
        title=f"<b>NPL for {symbol}, {df_npl['Year'].iloc[-1]}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )

    fig_npl.update_traces(
        hovertemplate='<br>NPL: %{y}',
        hoverlabel=dict(namelength=0),
        # Format values in thousands, millions, billions
        texttemplate='%{y:.2s}',
        textposition='auto'  # Show values on the bars
    )

    # Set the axis labels and disable zooming
    fig_npl.update_xaxes(fixedrange=True)
    fig_npl.update_yaxes(fixedrange=True)

    # Disable zooming
    fig_npl.update_layout(dragmode=False)


# Filter the dataframe for cash and bonus combo chart (without quarter filter)
df_filtered_combo = df1[df1["SYMBOL"] == symbol]

if not df_filtered_combo.empty:
    # Calculate the average values of cash and bonus for each year
    avg_cash_bonus = df_filtered_combo.groupby("Year").agg(
        {"Bonus": "mean", "Cash": "mean"}).reset_index()

    # Create a stacked column chart with average values
    fig_combo = px.bar(
        avg_cash_bonus,
        x="Year",
        y=["Bonus", "Cash"],
        title=f"<b>Bonus Dividend {symbol}</b>",
        barmode="stack",
        color_discrete_sequence=["#0083B8", "#FBB13C"],
        template="plotly_white"
    )

    fig_combo.update_layout(showlegend=False)
    fig_combo.update_traces(
        hovertemplate='Year: %{x}<br>Bonus: %{customdata[0]}<br>Cash: %{customdata[1]}',
        hoverlabel=dict(namelength=0),
        # Format values in thousands, millions, billions
        texttemplate='%{y}',
        textposition='auto',  # Show values on the bars
        customdata=np.stack(
            (avg_cash_bonus["Bonus"], avg_cash_bonus["Cash"]), axis=-1)
    )

    # Set the axis labels and disable zooming
    fig_combo.update_xaxes(fixedrange=True)
    fig_combo.update_yaxes(fixedrange=True)

    # Disable zooming
    fig_combo.update_layout(dragmode=False)

    # Create a combo bar chart with average values

    st.plotly_chart(fig_eps2, use_container_width=True)
    st.plotly_chart(fig_combo, use_container_width=True)
    st.plotly_chart(fig_roe, use_container_width=True)
    st.plotly_chart(fig_paidup2, use_container_width=True)
    st.plotly_chart(fig_capeps, use_container_width=True)
    if fig_npl is not None:
        st.plotly_chart(fig_npl, use_container_width=True)
    else:
        st.write("No NPL data available for the selected symbol and the latest year.")
else:
    st.write("No data available for the selected symbol.")

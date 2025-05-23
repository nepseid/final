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

# Create two columns for the filters
col1, col2 = st.columns(2)

with col1:
    symbol = st.selectbox(
        "Select Symbol",
        sorted(df1["SYMBOL"].unique()),
        index=1
    )

with col2:
    quarter = st.selectbox(
        "Select Quarter",
        sorted(df1["Quarter"].unique()),
        index=3
    )

# Filter the dataframe based on the inputs
df_filtered = df1[(df1["SYMBOL"] == symbol) & (df1["Quarter"] == quarter)]

if not df_filtered.empty:
    Timeframe = df_filtered["Quarter"].astype(
        str) + "-" + df_filtered["Year"].astype(str)
    df_filtered = df_filtered.assign(Timeframe=Timeframe)

    # Display the Price
    st.markdown(
        f"<p style='font-size:24px; font-weight:bold; text-align:center;'>Current Price Rs. {df_filtered['Price'].values[0]:.2f}</p>",
        unsafe_allow_html=True
    )

    # EPS Bar Chart
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
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig_eps2.update_traces(
        hovertemplate='<br>EPS: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y:.2s}',
        textposition='auto'
    )

    # DPS Bar Chart
    fig_dps2 = px.bar(
        df_filtered,
        x="Timeframe",
        y="Dps",
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>DPS for {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )
    fig_dps2.update_layout(
        showlegend=False,
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig_dps2.update_traces(
        hovertemplate='<br>DPS: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y:.2s}',
        textposition='auto'
    )

    # Capital Bar Chart
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
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig_paidup2.update_traces(
        hovertemplate='<br>Capital: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y}',
        textposition='auto'
    )

    # ROE Bar Chart
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
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig_roe.update_traces(
        hovertemplate='<br>ROE: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y}',
        textposition='auto'
    )

    # Book Value Bar Chart
    fig_bookvalue = px.bar(
        df_filtered,
        x="Timeframe",
        y=df_filtered["BOOK VALUE"],
        color="SYMBOL",
        facet_col="SYMBOL",
        facet_col_spacing=0.005,
        orientation="v",
        title=f"<b>Book Value {symbol}, {quarter}</b>",
        color_discrete_sequence=["#0083B8"],
        template="plotly_white"
    )
    fig_bookvalue.update_layout(
        showlegend=False,
        dragmode=False,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )
    fig_bookvalue.update_traces(
        hovertemplate='<br>Book Value: %{y}',
        hoverlabel=dict(namelength=0),
        texttemplate='%{y}',
        textposition='auto'
    )

    # EPS and Capital Combo Chart
    fig_capeps = make_subplots(specs=[[{"secondary_y": True}]])
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
    fig_capeps.update_xaxes(title_text="Timeframe", fixedrange=True)
    fig_capeps.update_yaxes(
        title_text="EPS", secondary_y=False, fixedrange=True)
    fig_capeps.update_yaxes(title_text="PAID-UP",
                            secondary_y=True, fixedrange=True)
    fig_capeps.update_layout(
        title=f"<b>EPS and Capital for {symbol}, {quarter}</b>",
        dragmode=False
    )

    # NPL Bar Chart
    latest_year = df1["Year"].unique()[-1]
    df_npl = df1[(df1["SYMBOL"] == symbol) & (df1["Year"] == latest_year)]

    fig_npl = None
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
            texttemplate='%{y}',
            textposition='auto'
        )
        fig_npl.update_xaxes(fixedrange=True)
        fig_npl.update_yaxes(fixedrange=True)
        fig_npl.update_layout(dragmode=False)

    # Net Profit Bar Chart
    df_profit = df1[(df1["SYMBOL"] == symbol) & (df1["Year"] == latest_year)]
    fig_profit = None
    if not df_profit.empty:
        fig_profit = px.bar(
            df_profit,
            x="Quarter",
            y=df_profit["NET PROFIT"] * 1000,
            title=f"<b>Net Profit for {symbol}, {df_profit['Year'].iloc[-1]}</b>",
            color_discrete_sequence=["#0083B8"],
            template="plotly_white"
        )
        fig_profit.update_traces(
            hovertemplate='<br>Net Profit: %{y}',
            hoverlabel=dict(namelength=0),
            texttemplate='%{y:.2s}',
            textposition='auto'
        )
        fig_profit.update_xaxes(fixedrange=True)
        fig_profit.update_yaxes(fixedrange=True)
        fig_profit.update_layout(dragmode=False)

    # Bonus Dividend Combo Chart
    df_filtered_combo = df1[df1["SYMBOL"] == symbol]
    if not df_filtered_combo.empty:
        avg_cash_bonus = df_filtered_combo.groupby("Year").agg(
            {"Bonus": "mean", "Cash": "mean"}).reset_index()

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
            texttemplate='%{y}',
            textposition='auto',
            customdata=np.stack(
                (avg_cash_bonus["Bonus"], avg_cash_bonus["Cash"]), axis=-1)
        )
        fig_combo.update_xaxes(fixedrange=True)
        fig_combo.update_yaxes(fixedrange=True)
        fig_combo.update_layout(dragmode=False)

    # Display all charts
    st.plotly_chart(fig_eps2, use_container_width=True)
    st.plotly_chart(fig_combo, use_container_width=True)
    st.plotly_chart(fig_bookvalue, use_container_width=True)
    st.plotly_chart(fig_roe, use_container_width=True)
    st.plotly_chart(fig_paidup2, use_container_width=True)

    if fig_profit is not None:
        st.plotly_chart(fig_profit, use_container_width=True)
    else:
        st.write(
            "No Net Profit data available for the selected symbol and the latest year.")

    st.plotly_chart(fig_capeps, use_container_width=True)

    if fig_npl is not None:
        st.plotly_chart(fig_npl, use_container_width=True)
    else:
        st.write("No NPL data available for the selected symbol and the latest year.")

    st.plotly_chart(fig_dps2, use_container_width=True)
else:
    st.write("No data available for the selected symbol and quarter.")

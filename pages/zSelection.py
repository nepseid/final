import pandas as pd
import streamlit as st
import altair as alt

# Load data from Excel file
df = pd.read_excel(
    r'/Users/vuone/Desktop/Code/Fundamental Analysis/Fundamentals.xlsx', sheet_name='Sheet1')

# Create EPS Filter and DPS Filter columns based on EPS and Dps values
df['EPS Filter'] = pd.cut(df['EPS'], bins=[-float('inf'), 0, 5, 10, 20, float(
    'inf')], labels=['Negative', '0-5', '5-10', '10-20', '20-200'])
df['DPS Filter'] = pd.cut(df['Dps'], bins=[-float('inf'), 0, 5, 10, 20, float(
    'inf')], labels=['Negative', '0-5', '5-10', '10-20', '20-200'])

# Sidebar filters
year_filter = st.sidebar.selectbox(
    'Select Year:', options=df['Year'].unique(), index=6)
quarter_filter = st.sidebar.selectbox(
    'Select Quarter:', options=df['Quarter'].unique(), index=1)

price_filter = st.sidebar.selectbox('Select Price Filter:', options=[
                                    'All', '0-100', '100-200', '200-300', '300-400', '400-500', '500-700', '700-900', '900-1200', '1200-1500', '1500-2500', '2500-40000'], index=2)
eps_filter = st.sidebar.selectbox('Select EPS Filter:', options=[
                                  'All', 'Negative', '0-5', '5-10', '10-20', '20-200'])
dps_filter = st.sidebar.selectbox('Select DPS Filter:', options=[
                                  'All', 'Negative', '0-5', '5-10', '10-20', '20-200'])

# Sector filter with dropdown list and checkboxes
sector_filter = st.sidebar.multiselect(
    'Select Sector:', df['Sector'].unique(), default=df['Sector'].unique())

# Apply filters to data
df_filtered = df[(df['Year'] == year_filter) &
                 (df['Quarter'] == quarter_filter)]

if price_filter != 'All':
    if price_filter == 'upto 200':
        df_filtered = df_filtered[df_filtered['Price'] < 200]
    else:
        price_range = price_filter.split('-')
        df_filtered = df_filtered[(df_filtered['Price'] >= int(price_range[0])) & (
            df_filtered['Price'] < int(price_range[1]))]

if eps_filter != 'All':
    df_filtered = df_filtered[df_filtered['EPS Filter'] == eps_filter]

if dps_filter != 'All':
    df_filtered = df_filtered[df_filtered['DPS Filter'] == dps_filter]

if sector_filter:
    df_filtered = df_filtered[df_filtered['Sector'].isin(sector_filter)]

# Bar charts

eps_chart = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X('SYMBOL', sort=alt.SortField(field='EPS', order='ascending')),
    y='EPS',
    tooltip=['SYMBOL', 'EPS'],
    text=alt.Text('EPS', format='.2f'),
    color=alt.Color('SYMBOL', legend=None)
)

dps_chart = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X('SYMBOL', sort=alt.SortField(field='Dps', order='ascending')),
    y='Dps',
    text=alt.Text('Dps', format='.2f'),
    color=alt.Color('SYMBOL', legend=None)
)

price_chart = alt.Chart(df_filtered).mark_bar().encode(
    x=alt.X('SYMBOL', sort=alt.SortField(field='Price', order='ascending')),
    y='Price',
    text=alt.Text('Price', format='.2f'),
    color=alt.Color('SYMBOL', legend=None)
)


# Render charts

st.write(f"#Price Bar Chart for {year_filter} Q{quarter_filter}")
st.altair_chart(price_chart, use_container_width=True)

st.write(f"#EPS Bar Chart for {year_filter} Q{quarter_filter}")
st.altair_chart(eps_chart, use_container_width=True)

st.write(f"#DPS Bar Chart for {year_filter} Q{quarter_filter}")
st.altair_chart(dps_chart, use_container_width=True)

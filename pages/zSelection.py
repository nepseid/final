import pandas as pd
import streamlit as st
import altair as alt

# Load data from Excel file
df = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')

# Sidebar filters
year_filter = st.sidebar.selectbox(
    'Select Year:', options=df['Year'].unique(), index=7)
quarter_filter = st.sidebar.selectbox(
    'Select Quarter:', options=df['Quarter'].unique(), index=0)

from_price = st.sidebar.number_input("From Price (Rs)", value=100)
to_price = st.sidebar.number_input("To Price (Rs)", value=400)

eps_filter = st.sidebar.selectbox('Select EPS Filter:', options=[
    'All', 'Positive', 'Negative', 'More than 0', 'More than 5', 'More than 10', 'More than 20', 'More than 50'])
dps_filter = st.sidebar.selectbox('Select DPS Filter:', options=[
    'All', 'Positive', 'Negative', 'More than 0', 'More than 5', 'More than 10', 'More than 20', 'More than 50'])

# Apply filters to data
df_filtered = df[(df['Year'] == year_filter) &
                 (df['Quarter'] == quarter_filter) &
                 (df['Price'] >= from_price) &
                 (df['Price'] <= to_price)]

if eps_filter != 'All':
    if eps_filter == 'Positive':
        df_filtered = df_filtered[df_filtered['EPS'] > 0]
    elif eps_filter == '20-200':
        df_filtered = df_filtered[(df_filtered['EPS'] >= 20) & (
            df_filtered['EPS'] <= 200)]
    else:
        df_filtered = df_filtered[df_filtered['EPS Filter'] == eps_filter]

if dps_filter != 'All':
    if dps_filter == 'Positive':
        df_filtered = df_filtered[df_filtered['Dps'] > 0]
    elif dps_filter == '20-200':
        df_filtered = df_filtered[(df_filtered['Dps'] >= 20) & (
            df_filtered['Dps'] <= 200)]
    else:
        df_filtered = df_filtered[df_filtered['DPS Filter'] == dps_filter]


# Get unique sector values excluding "Delist"
sector_options = df_filtered['Sector'].unique()
sector_options = [sector for sector in sector_options if sector != 'Delist']

# Sector filter with dropdown list and checkboxes
selected_sectors = st.sidebar.multiselect('Select Sectors:', options=sector_options, default=sector_options)



# Apply sector filter
if sector_filter:
    df_filtered = df_filtered[df_filtered['Sector'].isin(sector_filter)]

# Convert 'Price' column to numerical type
df_filtered['Price'] = pd.to_numeric(df_filtered['Price'], errors='coerce')

# Sort the filtered data frame by the 'Price' column in ascending order
df_filtered_sorted = df_filtered.sort_values('Price')

# Bar charts

eps_chart = alt.Chart(df_filtered_sorted).mark_bar().encode(
    x=alt.X('SYMBOL:N', sort=None),
    y='EPS',
    tooltip=['SYMBOL', 'EPS'],
    text=alt.Text('EPS'),
    color=alt.Color('SYMBOL', legend=None)
)

dps_chart = alt.Chart(df_filtered_sorted).mark_bar().encode(
    x=alt.X('SYMBOL:N', sort=None),
    y='Dps',
    text=alt.Text('Dps'),
    color=alt.Color('SYMBOL', legend=None)
)

price_chart = alt.Chart(df_filtered_sorted).mark_bar().encode(
    x=alt.X('SYMBOL:N', sort=None),
    y='Price',
    text=alt.Text('Price'),
    color=alt.Color('SYMBOL', legend=None)
)

# Multiply the 'PAID-UP' values by 1000 to convert them to billions
df_filtered_sorted['PAID-UP_B'] = df_filtered_sorted['PAID-UP'] * 1000

cap_chart = alt.Chart(df_filtered_sorted).mark_bar().encode(
    x=alt.X('SYMBOL:N', sort=None),
    y=alt.Y('PAID-UP_B:Q',
            axis=alt.Axis(title='Paid-Up (in billions G)', format='.2s')),
    text=alt.Text('PAID-UP_B:Q', format='.2sB'),
    color=alt.Color('SYMBOL', legend=None)
)


# Render charts

st.write(f"Price for {year_filter} Q{quarter_filter}")
price_chart_text = price_chart.mark_text(
    align='center',
    baseline='middle',
    dx=0,  # Nudges text to the right side of the bar
    dy=-10  # Nudges text above the bar
).encode(
    text=alt.Text('Price:Q', format='.2f'),
)
st.altair_chart(price_chart + price_chart_text, use_container_width=True)

st.write(f"EPS for {year_filter} Q{quarter_filter}")
eps_chart_text = eps_chart.mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-10
).encode(
    text=alt.Text('EPS:Q', format='.2f'),
)
st.altair_chart(eps_chart + eps_chart_text, use_container_width=True)

st.write(f"Capital for {year_filter} Q{quarter_filter}")
st.altair_chart(cap_chart, use_container_width=True)

st.write(f"DPS for {year_filter} Q{quarter_filter}")
dps_chart_text = dps_chart.mark_text(
    align='center',
    baseline='middle',
    dx=0,
    dy=-10
).encode(
    text=alt.Text('Dps:Q', format='.2f'),
)
st.altair_chart(dps_chart + dps_chart_text, use_container_width=True)

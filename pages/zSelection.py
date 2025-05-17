import pandas as pd
import streamlit as st
import altair as alt

# Load data from Excel file
df = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')

# Header for filters
st.header("Filters")

# Arrange filters in rows with 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    year_filter = st.selectbox(
        'Select Year:', options=df['Year'].unique(), index=7)
    from_price = st.number_input("From Price (Rs)", value=100)

with col2:
    quarter_filter = st.selectbox(
        'Select Quarter:', options=df['Quarter'].unique(), index=3)
    to_price = st.number_input("To Price (Rs)", value=400)

with col3:
    eps_filter = st.selectbox('Select EPS Filter:', options=[
        'All', 'Positive', 'Negative', 'More than 0', 'More than 5',
        'More than 10', 'More than 20', 'More than 50'])
    dps_filter = st.selectbox('Select DPS Filter:', options=[
        'All', 'Positive', 'Negative', 'More than 0', 'More than 5',
        'More than 10', 'More than 20', 'More than 50'])

# Apply filters to data
df_filtered = df[(df['Year'] == year_filter) &
                 (df['Quarter'] == quarter_filter) &
                 (df['Price'] >= from_price) &
                 (df['Price'] <= to_price)]

if eps_filter != 'All':
    filter_values = {
        'Positive': lambda x: x > 0,
        'Negative': lambda x: x < 0,
        'More than 0': lambda x: x > 0,
        'More than 5': lambda x: x > 5,
        'More than 10': lambda x: x > 10,
        'More than 20': lambda x: x > 20,
        'More than 50': lambda x: x > 50
    }
    df_filtered = df_filtered[df_filtered['EPS'].apply(
        filter_values[eps_filter])]

if dps_filter != 'All':
    df_filtered = df_filtered[df_filtered['Dps'].apply(
        filter_values[dps_filter])]

# Unique sectors excluding "Delist"
sector_options = df_filtered['Sector'].unique()
sector_options = [sector for sector in sector_options if sector != 'Delist']

# Sector filter
sector_filter = st.multiselect(
    'Select Sector:', sector_options, default=sector_options)

# Apply sector filter
if sector_filter:
    df_filtered = df_filtered[df_filtered['Sector'].isin(sector_filter)]

# Sort data by Price
df_filtered_sorted = df_filtered.sort_values('Price')

# Bar charts


def create_chart(data, x, y, tooltip, text_format, title):
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X(f'{x}:N', sort=None),
        y=y,
        tooltip=tooltip,
        text=alt.Text(f'{y}:Q', format=text_format),
        color=alt.Color(f'{x}:N', legend=None)
    ).properties(title=title)
    return chart


price_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Price', [
                           'SYMBOL', 'Price'], '.2f', 'Current Price')
eps_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'EPS', [
                         'SYMBOL', 'EPS'], '.2f', f'EPS for {year_filter} Q{quarter_filter}')
pe_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'PE', [
                        'SYMBOL', 'PE'], '.2f', f'PE for {year_filter} Q{quarter_filter}')
public_shares_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Public Shares', [
                                   'SYMBOL', 'Public Shares'], ',.0f', 'Public Shares')
book_value_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'BOOK VALUE', [
                                'SYMBOL', 'BOOK VALUE'], ',.0f', 'Book Value')
roe_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'ROE', [
                         'SYMBOL', 'ROE'], '.2f', 'ROE')
npl_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'NPL', [
                         'SYMBOL', 'NPL'], ',.0f', 'NPL')
dps_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Dps', [
                         'SYMBOL', 'Dps'], '.2f', f'DPS for {year_filter} Q{quarter_filter}')

# Render charts
st.altair_chart(price_chart, use_container_width=True)
st.altair_chart(eps_chart, use_container_width=True)
st.altair_chart(pe_chart, use_container_width=True)
st.altair_chart(public_shares_chart, use_container_width=True)
st.altair_chart(book_value_chart, use_container_width=True)
st.altair_chart(roe_chart, use_container_width=True)
st.altair_chart(npl_chart, use_container_width=True)
st.altair_chart(dps_chart, use_container_width=True)

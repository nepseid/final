import pandas as pd
import streamlit as st
import altair as alt
st.set_page_config(layout="wide")

# Load data from Excel file
df = pd.read_excel('Fundamentals.xlsx', sheet_name='Sheet1')

# Header for filters
st.header("Filters")

# Helper to parse 'All' or numeric values
def parse_filter(value):
    try:
        return float(value)
    except:
        return None

# Arrange filters in rows with 3 columns
col1, col2, col3 = st.columns(3)

with col1:
    year_filter = st.selectbox('Select Year:', options=sorted(df['Year'].unique(), reverse=True))
    from_price = st.text_input("From Price (Rs)", value="All")

with col2:
    quarter_filter = st.selectbox('Select Quarter:', options=sorted(df['Quarter'].unique()))
    to_price = st.text_input("To Price (Rs)", value="All")

with col3:
    from_book = st.text_input("From Book Value", value="All")
    to_book = st.text_input("To Book Value", value="All")

# EPS and DPS filters
col4, col5 = st.columns(2)

with col4:
    eps_filter = st.selectbox('Select EPS Filter:', options=[
        'All', 'Positive', 'Negative', 'More than 0', 'More than 5',
        'More than 10', 'More than 20', 'More than 50'])

with col5:
    dps_filter = st.selectbox('Select DPS Filter:', options=[
        'All', 'Positive', 'Negative', 'More than 0', 'More than 5',
        'More than 10', 'More than 20', 'More than 50'])

# Sector filter (always shown before apply)
sector_options = [sector for sector in df['Sector'].unique() if sector != 'Delist']
sector_filter = st.multiselect('Select Sector:', sector_options, default=sector_options)

# Apply button
if st.button("Apply"):
    # Apply base filters
    df_filtered = df[
        (df['Year'] == year_filter) &
        (df['Quarter'] == quarter_filter)
    ]

    # Price filters
    from_price_val = parse_filter(from_price)
    to_price_val = parse_filter(to_price)

    if from_price_val is not None:
        df_filtered = df_filtered[df_filtered['Price'] >= from_price_val]
    if to_price_val is not None:
        df_filtered = df_filtered[df_filtered['Price'] <= to_price_val]

    # Book value filters
    from_book_val = parse_filter(from_book)
    to_book_val = parse_filter(to_book)

    if from_book_val is not None:
        df_filtered = df_filtered[df_filtered['BOOK VALUE'] >= from_book_val]
    if to_book_val is not None:
        df_filtered = df_filtered[df_filtered['BOOK VALUE'] <= to_book_val]

    # EPS & DPS filters
    filter_values = {
        'Positive': lambda x: x > 0,
        'Negative': lambda x: x < 0,
        'More than 0': lambda x: x > 0,
        'More than 5': lambda x: x > 5,
        'More than 10': lambda x: x > 10,
        'More than 20': lambda x: x > 20,
        'More than 50': lambda x: x > 50
    }

    if eps_filter != 'All':
        df_filtered = df_filtered[df_filtered['EPS'].apply(filter_values[eps_filter])]
    if dps_filter != 'All':
        df_filtered = df_filtered[df_filtered['Dps'].apply(filter_values[dps_filter])]

    # Sector filter
    if sector_filter:
        df_filtered = df_filtered[df_filtered['Sector'].isin(sector_filter)]

    # Sort data
    df_filtered_sorted = df_filtered.sort_values('Price')

    # Chart builder with bold white vertical labels above bars
    def create_chart(data, x, y, tooltip, text_format, title):
        base = alt.Chart(data).encode(
            x=alt.X(f'{x}:N', sort=None),
            y=alt.Y(f'{y}:Q'),
            tooltip=tooltip,
            color=alt.Color(f'{x}:N', legend=None)
        )

        bars = base.mark_bar()

        text = base.mark_text(
            align='center',
            baseline='bottom',
            angle=270,
            dy=0,  # no offset here, handled by transform
            fontSize=16,
            fontWeight='bold',
            color='white'
        ).encode(
            text=alt.Text(f'{y}:Q', format=text_format),
            y=alt.Y(f"{y} + 5")  # 5 units above the bar's value
        )


        return (bars + text).properties(title=title)

    # Create charts
    price_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Price', ['SYMBOL', 'Price'], ',.0f', 'Current Price')
    eps_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'EPS', ['SYMBOL', 'EPS'], '.2f', f'EPS for {year_filter} Q{quarter_filter}')
    pe_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'PE', ['SYMBOL', 'PE'], '.2f', f'PE for {year_filter} Q{quarter_filter}')
    public_shares_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Public Shares', ['SYMBOL', 'Public Shares'], ',.0f', 'Public Shares')
    book_value_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'BOOK VALUE', ['SYMBOL', 'BOOK VALUE'], ',.0f', 'Book Value')
    roe_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'ROE', ['SYMBOL', 'ROE'], '.2f', 'ROE')
    npl_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'NPL', ['SYMBOL', 'NPL'], ',.0f', 'NPL')
    dps_chart = create_chart(df_filtered_sorted, 'SYMBOL', 'Dps', ['SYMBOL', 'Dps'], '.2f', f'DPS for {year_filter} Q{quarter_filter}')

    # Display charts
    st.altair_chart(price_chart, use_container_width=True)
    st.altair_chart(eps_chart, use_container_width=True)
    st.altair_chart(pe_chart, use_container_width=True)
    st.altair_chart(public_shares_chart, use_container_width=True)
    st.altair_chart(book_value_chart, use_container_width=True)
    st.altair_chart(roe_chart, use_container_width=True)
    st.altair_chart(npl_chart, use_container_width=True)
    st.altair_chart(dps_chart, use_container_width=True)

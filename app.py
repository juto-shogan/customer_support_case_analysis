import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Data Loading and Cleaning ---
# Using st.cache_data to cache the data loading and cleaning, so it runs only once when the app starts.
@st.cache_data
def load_and_clean_data():
    try:
        df = pd.read_csv('data/data.csv')
    except FileNotFoundError:
        st.error("Error: 'data.csv' not found. Please make sure the file is in the same directory as the Streamlit app.")
        st.stop()

    # Convert 'Opened Date' to datetime and drop NaT rows
    df['Opened Date'] = pd.to_datetime(df['Opened Date'], errors='coerce')
    df.dropna(subset=['Opened Date'], inplace=True)

    # Drop the 'Store' column (as it's entirely null)
    if 'Store' in df.columns and df['Store'].isnull().all():
        df.drop(columns=['Store'], inplace=True)
        st.sidebar.info("Dropped 'Store' column due to all null values.")

    # Remove duplicate rows
    initial_rows = df.shape[0]
    df.drop_duplicates(inplace=True)
    rows_after_duplicates = df.shape[0]
    if initial_rows > rows_after_duplicates:
        st.sidebar.info(f"Removed {initial_rows - rows_after_duplicates} duplicate rows.")
    else:
        st.sidebar.info("No duplicate rows found.")

    return df

df = load_and_clean_data()

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide", page_title="Customer Case Analysis")

# --- Streamlit App Title and Introduction ---
st.title("Customer Case Analysis Dashboard")

st.write("""
This interactive dashboard provides key insights into customer cases from the uploaded dataset.
Explore the distributions of case statuses, origins, top product brands, primary reasons for contact, and overall trends over time.
""")

st.markdown("---")

# --- Visualizations ---

st.header("1. Distribution of Case Status")
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Case Status', 'Number of Cases']
fig_status = px.bar(status_counts, x='Case Status', y='Number of Cases',
                    title='Distribution of Case Status',
                    color_discrete_sequence=px.colors.qualitative.Vivid)
st.plotly_chart(fig_status, use_container_width=True)
st.write("""
**Finding:** The majority of cases are **Closed**, indicating an effective resolution process. A significant portion are also `Closed as Duplicate`, suggesting possible overlaps or multiple entries for the same issue.
""")
st.markdown("---")


st.header("2. Distribution of Case Origin")
origin_counts = df['Case Origin'].value_counts().reset_index()
origin_counts.columns = ['Case Origin', 'Number of Cases']
fig_origin = px.bar(origin_counts, x='Case Origin', y='Number of Cases',
                    title='Distribution of Case Origin',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig_origin, use_container_width=True)
st.write("""
**Finding:** `Email` and `Phone` are the dominant channels for customer case initiation. This highlights the importance of robust support systems for these communication methods.
""")
st.markdown("---")


st.header("3. Top 10 Product Brands by Case Count")
top_brands = df['Product: Brand'].value_counts().head(10).reset_index()
top_brands.columns = ['Product Brand', 'Number of Cases']
fig_brands = px.bar(top_brands, x='Number of Cases', y='Product Brand', orientation='h',
                    title='Top 10 Product Brands by Case Count',
                    color_discrete_sequence=px.colors.qualitative.Bold)
fig_brands.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_brands, use_container_width=True)
st.write("""
**Finding:** `Unilever Corporate` has the highest number of cases, which could encompass general inquiries not tied to a specific product. Among specific brands, `Knorr`, `Pepsodent`, and `Close Up` generate the most cases.
""")
st.markdown("---")


st.header("4. Top 10 Reasons L1 Description by Case Count")
top_reasons = df['Reason L1 desc'].value_counts().head(10).reset_index()
top_reasons.columns = ['Reason L1 Description', 'Number of Cases']
fig_reasons = px.bar(top_reasons, x='Number of Cases', y='Reason L1 Description', orientation='h',
                     title='Top 10 Reasons L1 Description by Case Count',
                     color_discrete_sequence=px.colors.qualitative.Dark24)
fig_reasons.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_reasons, use_container_width=True)
st.write("""
**Finding:** `Others` and `Queries` are the most frequent top-level reasons for contact. This suggests an opportunity to refine reason categories for better insights into specific customer needs. `Feedback/Comment` and `Praises` are also significant.
""")
st.markdown("---")


st.header("5. Monthly Trend of Cases Over Time")
df['YearMonth'] = df['Opened Date'].dt.to_period('M').astype(str)
monthly_cases = df.groupby('YearMonth').size().reset_index(name='Number of Cases')
monthly_cases['YearMonth'] = pd.to_datetime(monthly_cases['YearMonth']) # Convert back for proper sorting
monthly_cases = monthly_cases.sort_values('YearMonth')

fig_time = px.line(monthly_cases, x='YearMonth', y='Number of Cases',
                   title='Monthly Trend of Cases Over Time',
                   markers=True)
fig_time.update_xaxes(dtick="M1", tickformat="%b\n%Y")
st.plotly_chart(fig_time, use_container_width=True)
st.write("""
**Finding:** The trend of cases over time shows fluctuations, which could be influenced by seasonal factors, marketing campaigns, or specific events. Analyzing these periods more closely could reveal underlying drivers.
""")
st.markdown("---")

st.info("Analysis and visualizations completed. This app provides a dynamic view of your customer case data.")
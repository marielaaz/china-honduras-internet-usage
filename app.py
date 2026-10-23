import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(
    page_title="Internet Usage: China vs. Honduras",
    page_icon="📈",
    layout="wide"
)

# 2. Header and Assignment Context
st.title("🌐 Share of Population Using the Internet: China vs. Honduras")
st.markdown("""
This interactive web application compares the internet adoption rate between **China** and **Honduras** 
using the exact data from the uploaded Our World in Data dataset. Use the interactive tools below to explore the data.
""")

# 3. Load and Filter Data
@st.cache_data
def load_data():
    df = pd.read_csv('share-of-individuals-using-the-internet.csv')
    # Filter strictly for China and Honduras
    filtered_df = df[df['Entity'].isin(['China', 'Honduras'])].copy()
    filtered_df.sort_values(by=['Entity', 'Year'], inplace=True)
    return filtered_df

df = load_data()

china_df = df[df['Entity'] == 'China']
honduras_df = df[df['Entity'] == 'Honduras']

# 4. Sidebar Controls for Interactivity
st.sidebar.header("🎛️ Interactive Controls")
min_year = int(df['Year'].min())
max_year = int(df['Year'].max())

# Year Range Slider
selected_years = st.sidebar.slider(
    "Select Year Range:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

show_markers = st.sidebar.checkbox("Show Data Point Markers", value=True)
show_table = st.sidebar.checkbox("Show Raw Data Table", value=False)

# Filter data based on selected year range
china_filtered = china_df[(china_df['Year'] >= selected_years[0]) & (china_df['Year'] <= selected_years[1])]
honduras_filtered = honduras_df[(honduras_df['Year'] >= selected_years[0]) & (honduras_df['Year'] <= selected_years[1])]

# 5. Quick Summary Metrics (KPI Cards)
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if not china_filtered.empty:
        latest_c = china_filtered.iloc[-1]
        st.metric(label=f"China ({int(latest_c['Year'])})", value=f"{latest_c['Share of the population using the Internet']:.2f}%")

with col2:
    if not honduras_filtered.empty:
        latest_h = honduras_filtered.iloc[-1]
        st.metric(label=f"Honduras ({int(latest_h['Year'])})", value=f"{latest_h['Share of the population using the Internet']:.2f}%")

with col3:
    st.metric(label="Dataset Range", value=f"{min_year} – {max_year}")

# 6. Interactive Plotly Line Chart
fig = go.Figure()

# China Line Trace
fig.add_trace(go.Scatter(
    x=china_filtered['Year'],
    y=china_filtered['Share of the population using the Internet'],
    mode='lines+markers' if show_markers else 'lines',
    name='China',
    line=dict(color='#E63946', width=3.5), # Distinct color
    marker=dict(size=7),
    hovertemplate='<b>Country:</b> China<br><b>Year:</b> %{x}<br><b>Internet Usage:</b> %{y:.2f}%<extra></extra>'
))

# Honduras Line Trace
fig.add_trace(go.Scatter(
    x=honduras_filtered['Year'],
    y=honduras_filtered['Share of the population using the Internet'],
    mode='lines+markers' if show_markers else 'lines',
    name='Honduras',
    line=dict(color='#457B9D', width=3.5), # Distinct color
    marker=dict(size=7),
    hovertemplate='<b>Country:</b> Honduras<br><b>Year:</b> %{x}<br><b>Internet Usage:</b> %{y:.2f}%<extra></extra>'
))

# Layout Configuration
fig.update_layout(
    title=dict(
        text=f"Share of Population Using the Internet ({selected_years[0]}–{selected_years[1]})",
        font=dict(size=18)
    ),
    xaxis=dict(title="Year", dtick=2, gridcolor='#e5e5e5'),
    yaxis=dict(title="Share of population using the internet (%)", range=[0, 100], gridcolor='#e5e5e5'),
    hovermode="x unified",
    legend=dict(title="Country", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    template="plotly_white",
    height=550
)

st.plotly_chart(fig, use_container_width=True)

# 7. Source Citation & Data Table Option
st.markdown("""
---
**Data Source Citation:**  
* Dataset: *Share of Individuals Using the Internet*, published by **Our World in Data**.  
* Note: Real values from the CSV are plotted as-is; missing historical years are excluded rather than estimated or set to zero.
""")

if show_table:
    st.subheader("📋 Raw Data Explorer")
    pivot_table = df[(df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])].pivot(
        index='Year', columns='Entity', values='Share of the population using the Internet'
    )[['China', 'Honduras']]
    st.dataframe(pivot_table.style.format("{:.2f}%", na_rep="No Data Available"))
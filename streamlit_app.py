import streamlit as st
import altair as alt
import pandas as pd
# pyright: ignore[reportMissingImports]
# Load data
data = pd.read_csv("sea_levels_with_years.csv")

st.set_page_config(layout="wide", page_title="Rising Waters: A Closer Look at Sea Level Changes")

# Sidebar
st.sidebar.header("Choose a Region To View")
#source = ["All"] + sorted(data["Indicator"].unique())
region = ["All"] + sorted(data["Measure"].unique())

st.sidebar.subheader("The first two charts are connected to the region selected and will display corresponding data.")
#selected_source = st.sidebar.selectbox("Data Source", source)
selected_region = st.sidebar.selectbox("Region", region)

# Apply filters for interactive views
data2 = data[data['Year'] <= 2024]

filtered = data2.copy()

#if selected_source != "All":
  #  filtered = filtered[filtered["Indicator"] == selected_source]
if selected_region != "All":
    filtered = filtered[filtered["Measure"] == selected_region]

# Introduction
st.title("🌊 Rising Waters: A Closer Look at Sea Level Changes")
st.subheader("A visual narrative exploring changes in global and regional sea levels.")

st.markdown("Sea levels have risen at an accelerating pace due to melting glaciers and thermal expansion, with wide variation across geographic regions. This dashboard combines global averages and regional trends to answer the question:")
st.markdown(
    '<div style="text-align: center; font-size: 32px; font-weight: bold;">How have sea levels changed over time? Where are these changes most dramatic?</div>',
    unsafe_allow_html=True
)
st.markdown("")

# Box Chart
st.header("📍 Annual Sea Level Changes by Region")
st.markdown("This heatmap shows how sea levels have shifted across regions and years. Darker colors represent **greater sea level increases**. Use the sidebar to select a specific region for closer inspection.")

st.markdown("""
***TIPS:***
1. *Use the sidebar to filter this chart by region. This filter only applies to the first two charts.*  
2. *You can zoom in on the chart by scrolling or pinching.*
""")

heatmap = alt.Chart(filtered).mark_bar().encode(
    x=alt.X("Year:O"),
    y=alt.Y("Measure:N", title="Region"),
    color=alt.Color("Value:Q", scale=alt.Scale(scheme="lightgreyred"), title="Change in Mean Sea Level")
).properties(
    title="Mean Sea Level Change by Year Across All Measured Regions"
).interactive()

st.altair_chart(heatmap, use_container_width=True)

st.markdown("The heatmap above displays sea level change across different regions over time. We observe that while most regions exhibit an upward trend, the **intensity and timing vary considerably**. Some regions like the Western Pacific show **early and consistent rises**, while others demonstrate **intermittent or delayed changes**.")

# Line / Frequency Chart
st.header("📈 Global Sea Level Trends Over Time")
st.markdown("The line chart below illustrates **overall sea level trends** across all measured regions. It provides a clearer view of how the global mean sea level has shifted each year.")

st.markdown("*This line chart also reflects the region you select in the sidebar.*")

overall = alt.Chart(filtered).mark_line().encode(
    x=alt.X("Date:T"),
    y=alt.Y("Value:Q"),
    tooltip=["Year", "Value"]
).properties(
    title="Sea Level Changes Over Time"
).interactive()

st.altair_chart(overall)

st.markdown("This line chart shows the **global average sea level change** over time. We see a **general upward trend**, with some years exhibiting sharper increases than others. This suggests that sea level rise is not only ongoing but **subject to short-term variability**, possibly due to climatic cycles or regional anomalies.")

year_average = filtered.groupby("Year", as_index=False)["Value"].mean()
year_average["Change"] = year_average["Value"].diff()

# Key Insights & Values - #1
st.header("🔍 Key Insights")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🌊 Global Avg. Change", "36.05 mm")
col2.metric("📈 Highest Rise", "511.93 mm", "Baltic Sea, 2015")
col3.metric("⚠️ Most Volatile Region", "Baltic Sea", "Std Dev: 155.91 mm")
col4.metric("🌐 Regions with Upward Trend", "100%")

# Volatility Bar Chart
st.header("🌐 Regional Volatility in Sea Level Change")
import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# Load data
data_path = 'covid_19_indonesia.csv'
data = pd.read_csv(data_path)

# Ensure 'Date' column is in datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Sidebar for filtering
title = "Visualisasi Data COVID-19 di Indonesia"
st.sidebar.title("Filter Data")
st.sidebar.markdown("Gunakan filter di bawah ini:")

# Filter by date
date_filter = st.sidebar.date_input(
    "Pilih tanggal:",
    value=(data['Date'].min(), data['Date'].max())
)

# Filter by province
provinsi_filter = st.sidebar.selectbox(
    "Pilih Provinsi:",
    options=["Semua"] + list(data['Location'].unique())
)

# Filter data
filtered_data = pd.DataFrame(columns=data.columns)
print(len(date_filter))
if provinsi_filter != "Semua":
    for i, item in data.iterrows():
        if(len(date_filter) > 1):
            if item['Location'] == provinsi_filter and item['Date'] >= pd.Timestamp(date_filter[0]) and item['Date'] <= pd.Timestamp(date_filter[1]):
                filtered_data.loc[i] = item 
        else:
            if item['Location'] == provinsi_filter:
                filtered_data.loc[i] = item
else:
    if len(date_filter) > 1:
        filtered_data = data[(data['Date'] >= pd.Timestamp(date_filter[0])) &
                              (data['Date'] <= pd.Timestamp(date_filter[1]))]
    else:
        filtered_data = data.copy()
        

# Main title
st.title(title)

# Summary statistics
st.header("Statistik COVID-19")
st.markdown(
    f"Total Kasus: **{filtered_data['New Cases'].sum():,}**, "
    f"Total Sembuh: **{filtered_data['New Recovered'].sum():,}**, "
    f"Total Meninggal: **{filtered_data['New Deaths'].sum():,}**"
)

# Display data table
if st.checkbox("Tampilkan Tabel Data"):
    st.dataframe(filtered_data)
    
# Heatmap visualization
location_name = "Indonesia"
# if provinsi_filter is not "Semua":
#     location_name = provinsi_filter
st.header(f"Heatmap Kasus COVID-19 di {location_name}")

# Filter data for heatmap (exclude "Indonesia")
heatmap_data = data[data['Location'] != "Indonesia"]
heatmap_data = heatmap_data[['Latitude', 'Longitude', 'Total Cases']].dropna()

heat_data = [
    [row['Latitude'], row['Longitude'], row['Total Cases']]
    for _, row in heatmap_data.iterrows()
]

# Create heatmap
heatmap = folium.Map(location=[-2.548926, 118.0148634], zoom_start=5)
if heat_data:
    HeatMap(heat_data).add_to(heatmap)

# Display heatmap
st_folium(heatmap, width=700, height=500)

# Map visualization for selected province
st.header("Peta Kasus COVID-19 Berdasarkan Provinsi")

# Create Folium map for province
province_map = folium.Map(location=[-2.548926, 118.0148634], zoom_start=5)

# get first location name from filtered data for default

if provinsi_filter != "Semua":
    location = filtered_data['Location'].iloc[0]
else:
    location = "Indonesia"
latitude = filtered_data['Latitude'].iloc[0]
longitude = filtered_data['Longitude'].iloc[0]

# get sum of cases, recovered, and deaths from latest index
cases_sum = filtered_data['Total Cases'].iloc[-1]
recovered_sum = filtered_data['Total Recovered'].iloc[-1]
deaths_sum = filtered_data['Total Deaths'].iloc[-1]

folium.Marker(
    location=[latitude, longitude],
    popup=folium.Popup(
        f"Location: {location}<br>"
        f"Kasus: {cases_sum}<br>"
        f"Sembuh: {recovered_sum}<br>"
        f"Meninggal: {deaths_sum}",
        max_width=300
    ),
    icon=folium.Icon(icon="info-sign")
).add_to(province_map)
# Display map for province
st_folium(province_map, width=700, height=500)



# Line chart visualization
st.header("Grafik Tren COVID-19")

grouped_data = filtered_data.groupby(['Date']).sum().reset_index()

st.line_chart(
    data=grouped_data,
    x='Date',
    y=['Total Cases', 'Total Recovered', 'Total Deaths'],
    use_container_width=True
)

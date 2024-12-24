# import streamlit as st
# import pandas as pd
# import folium
# from streamlit_folium import st_folium

# # Load data
# data_path = 'covid_19_indonesia.csv'
# data = pd.read_csv(data_path)

# # Ensure 'Date' column is in datetime format
# data['Date'] = pd.to_datetime(data['Date'])

# # Sidebar for filtering
# title = "Visualisasi Data COVID-19 di Indonesia"
# st.sidebar.title("Filter Data")
# st.sidebar.markdown("Gunakan filter di bawah ini:")

# # Filter by date
# date_filter = st.sidebar.date_input(
#     "Pilih tanggal:",
#     value=(data['Date'].min(), data['Date'].max())
# )

# # Filter by province
# provinsi_filter = st.sidebar.selectbox(
#     "Pilih Provinsi:",
#     options=["Semua"] + list(data['Location'].unique())
# )

# # Filter data
# filtered_data = data.copy()
# if provinsi_filter != "Semua":
#     filtered_data = filtered_data[filtered_data['Location'] == provinsi_filter]

# filtered_data = filtered_data[(filtered_data['Date'] >= pd.Timestamp(date_filter[0])) &
#                               (filtered_data['Date'] <= pd.Timestamp(date_filter[1]))]

# # Main title
# st.title(title)

# # Summary statistics
# st.header("Statistik COVID-19")
# st.markdown(
#     f"Total Kasus: **{filtered_data['Total Cases'].sum():,}**, "
#     f"Total Sembuh: **{filtered_data['Total Recovered'].sum():,}**, "
#     f"Total Meninggal: **{filtered_data['Total Deaths'].sum():,}**"
# )

# # Display data table
# if st.checkbox("Tampilkan Tabel Data"):
#     st.dataframe(filtered_data)

# # Map visualization
# st.header("Peta Indonesia")

# # Create Folium map
# m = folium.Map(location=[-2.548926, 118.0148634], zoom_start=5)

# for _, row in filtered_data.iterrows():
#     folium.Marker(
#         location=[row['Latitude'], row['Longitude']],
#         popup=folium.Popup(
#             f"Location: {row['Location']}<br>"
#             f"Kasus: {row['Total Cases']}<br>"
#             f"Sembuh: {row['Total Recovered']}<br>"
#             f"Meninggal: {row['Total Deaths']}",
#             max_width=300
#         ),
#         icon=folium.Icon(icon="info-sign")
#     ).add_to(m)

# # Display map
# st_folium(m, width=700, height=500)

# # Line chart visualization
# st.header("Grafik Tren COVID-19")

# grouped_data = filtered_data.groupby(['Date']).sum().reset_index()

# st.line_chart(
#     data=grouped_data,
#     x='Date',
#     y=['Total Cases', 'Total Recovered', 'Total Deaths'],
#     use_container_width=True
# )

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
filtered_data = data.copy()
if provinsi_filter != "Semua":
    filtered_data = filtered_data[filtered_data['Location'] == provinsi_filter]

filtered_data = filtered_data[(filtered_data['Date'] >= pd.Timestamp(date_filter[0])) &
                              (filtered_data['Date'] <= pd.Timestamp(date_filter[1]))]

# Main title
st.title(title)

# Summary statistics
st.header("Statistik COVID-19")
st.markdown(
    f"Total Kasus: **{filtered_data['Total Cases'].sum():,}**, "
    f"Total Sembuh: **{filtered_data['Total Recovered'].sum():,}**, "
    f"Total Meninggal: **{filtered_data['Total Deaths'].sum():,}**"
)

# Display data table
if st.checkbox("Tampilkan Tabel Data"):
    st.dataframe(filtered_data)
    
# Heatmap visualization
st.header("Heatmap Kasus COVID-19 di Indonesia")

# Filter data for heatmap (exclude "Indonesia")
heatmap_data = data[data['Location'] != "Indonesia"]
heatmap_data = heatmap_data[['Latitude', 'Longitude', 'Total Cases']].dropna()

# Prepare heatmap data
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

for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=folium.Popup(
            f"Location: {row['Location']}<br>"
            f"Kasus: {row['Total Cases']}<br>"
            f"Sembuh: {row['Total Recovered']}<br>"
            f"Meninggal: {row['Total Deaths']}",
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

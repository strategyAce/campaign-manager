import streamlit as st
import json
import geopandas as gpd
import plotly.express as px
import os

LOGO_PATH = "Campaign-Visualizer_Logo.png"

def main():

  st.set_page_config(layout="wide",page_title="Visualizer", page_icon=":globe_with_meridians:")

  col1,col2 = st.columns(2)
  with col1:
      st.title("Campaign Visualizer Tool")
      st.subheader("Map your campaign data to chart your path to victory.")
  with col2: 
      st.image(LOGO_PATH, width=250) 
  st.write("This is a product of Strategy Ace LLC")
  st.write("version: BETAv0.1")
  st.divider()
  
  # Define the Maps to be Displayed
  
  #Map1 script from mapbox
  map1_script = """
  <!DOCTYPE html>
  <html>
  <head>
  <meta charset="utf-8">
  <title>Display a map with click interaction</title>
  <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
  <link href="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.css" rel="stylesheet">
  <script src="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.js"></script>
  <style>
  body { margin: 0; padding: 0; }
  #map { position: absolute; top: 0; bottom: 0; width: 100%; }
  </style>
  </head>
  <body>
  <div id="map"></div>
  <script>
    mapboxgl.accessToken = 'pk.eyJ1IjoiYXNoMTgyNSIsImEiOiJjbTF2M3J5M3EwN3ZhMmpvZXI1MzRnbGIxIn0.Ahb-c79xp6uR9gEyGGWsgQ'; // Replace with your access token
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/ash1825/cm39ap0uk01mh01pd02x04lag', // Replace with your style URL
        center: [-81.379234, 28.567760], // starting position
        zoom: 11 // starting zoom
    });
  </script>
  </body>
  </html>
  """
  
  #Map2 script from mapbox
  map2_script = """
  <!DOCTYPE html>
  <html>
  <head>
  <meta charset="utf-8">
  <title>Display a map with click interaction</title>
  <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
  <link href="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.css" rel="stylesheet">
  <script src="https://api.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.js"></script>
  <style>
  body { margin: 0; padding: 0; }
  #map { position: absolute; top: 0; bottom: 0; width: 100%; }
  </style>
  </head>
  <body>
  <div id="map"></div>
  <script>
    mapboxgl.accessToken = 'pk.eyJ1IjoiYXNoMTgyNSIsImEiOiJjbTF2M3J5M3EwN3ZhMmpvZXI1MzRnbGIxIn0.Ahb-c79xp6uR9gEyGGWsgQ'; // Replace with your access token
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/ash1825/cm4663rzf00qt01s39jhmcrit', // Replace with your style URL
        center: [-81.379234, 28.567760], // starting position
        zoom: 11 // starting zoom
    });
  </script>
  </body>
  </html>
  """
  
  # Display the map in Streamlit
  st.subheader("Percentage of Registered Democrats")
  st.components.v1.html(map1_script, height=600)
  st.subheader(" ")
  st.divider()
  
  st.subheader("Total Registered Voters")
  st.components.v1.html(map2_script, height=600)
  st.subheader(" ")
  st.divider()
  
  st.subheader("2024 Election Performance")
  st.write("The map belows shows how well your candidate did relative to expected performance based on party demographics. Red circles indicate under-performance while blue indicates above-performance.")
  gdf = gpd.read_file(JSON_PATH)  #geoJSON file of election results
  fig = px.scatter_mapbox(
    gdf,
    lat="LATITUDE",
    lon="LONGITUDE",
    color="Performance",
    color_continuous_scale="RdBu",  # Use a diverging color scale for positive and negative values
    size=abs(gdf["Performance"]),  # Size the markers based on performance
    hover_name="PRECINCT",  # Show precinct name on hover
    hover_data=["Performance"],  # Show performance value on hover
    mapbox_style="carto-positron",
    zoom=11,  # Adjust the zoom level as needed
    center={"lat": 28.567760, "lon": -81.379234},  # Center the map
    height = 800,
    width = 1200
   )
  
  fig.update_layout(mapbox_style="carto-positron")
  st.plotly_chart(fig)
  
  #App Footer
  st.divider()
  st.image(BANNER_PATH,width=300)
  st.write(url)
      


if __name__ == "__main__":
    main()

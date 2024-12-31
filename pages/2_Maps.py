import streamlit as st
import json
import geopandas as gpd
import plotly.express as px
import os

st.set_page_config(layout="wide",page_title="Visualizer", page_icon=":globe_with_meridians:")

def main():

  st.image("Eskamani_Banner.png",width=700)
  col1,col2 = st.columns(2)
  with col1:
    st.title("Campaign Visualizer Tool")
  with col2:
    st.image("Campaign-Visualizer_Logo.png",width=150)
  st.subheader("Map your campaign data to chart your path to victory.")
  st.divider()
  
  # Define the Maps to be Displayed

  #Campaign Google Map
  #gmap_url = "https://www.google.com/maps/d/edit?mid=1AJzBf1DCR3d_quOVH2hMoJO_yjNvSKc&usp=sharing"
  gmap_script = """<iframe src="https://www.google.com/maps/d/u/0/embed?mid=1AJzBf1DCR3d_quOVH2hMoJO_yjNvSKc&ehbc=2E312F&noprof=1" width="1000" height="600"></iframe>"""
  
  #Map script from mapbox
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

          map.on('load', () => {
              // Add a click event for the existing data-driven-circles layer
              map.on('click', 'Data-driven circles, data-driven-circles', (e) => {
                  const coordinates = e.features[0].geometry.coordinates.slice();
                  const properties = e.features[0].properties;

                  new mapboxgl.Popup()
                      .setLngLat(coordinates)
                      .setHTML(
                          `<h3>Precinct: ${properties.precinct}</h3>` +
                          `<p>Address: ${properties.address}</p>` +
                          `<p>Data: ${properties.data}</p>`
                      )
                      .addTo(map);
              });

              // Change the cursor to a pointer when over the layer
              map.on('mouseenter', 'data-driven-circles', () => {
                  map.getCanvas().style.cursor = 'pointer';
              });

              // Change it back when it leaves
              map.on('mouseleave', 'data-driven-circles', () => {
                  map.getCanvas().style.cursor = '';
              });
          });
      </script>
  </body>
  </html>
  """
  
  #Map3 script from mapbox
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
  st.subheader("Your Custom Campaign Google Maps")
  st.components.v1.html(gmap_script, width=1000, height=600)
  st.write("This is an embedded custom Google Map customized for your campaign. You can zoom, click, and interact with the map. Google maps like these can contain specific data layers that can be toggled On and Off and can be easily shared with campaign personnel and volunteers. These maps can be accessed by any kind of device such as phones, tablets, and laptops.")
  st.subheader(" ")
  st.divider()
  
  st.subheader("Percentage of Registered Democrats")
  st.components.v1.html(map1_script, height=600)
  st.write("This is an embedded custom map created with the professional GIS tool called MapBox. You are seeing the official SoE GIS precinct border data displayed with data driven circles presenting curated SoE demographic data. Maps can be modified and tailored for your needs.")
  st.subheader(" ")
  st.divider()
  
  st.subheader("Total Registered Voters")
  st.components.v1.html(map2_script, height=600)
  st.write("This is an embedded custom map created with the professional GIS tool called MapBox. You are seeing the official SoE GIS precinct border data displayed with data driven circles presenting curated SoE demographic data. Maps can be modified and tailored for your needs.")
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

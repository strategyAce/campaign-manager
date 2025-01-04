import streamlit as st
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler
import os

st.set_page_config(page_title="Prioritizer", page_icon=":arrows_clockwise:")

#Read in Precinct Data from Session State from Maps Page
precinctData = st.session_state['shared_data'].get('page2')

# Streamlit app
def main():

   # Sidebar with expandable User Guide section
    with st.sidebar.title("📘 User Guide / Instructions"):
        st.sidebar.write("""
        Welcome to the Campaign Prioritizer Tool!

        **Tool Overview:**
           The tool was built to help your campaign determine which precinct to focus canvassing efforts on by strategic considerations important to your campaign.

        **File Input:**
           You will need to input a csv file with the list of precincts and detailed associated data like demographics and previous election turnout.

        **Decision Parameter Weights:**
           These values are percentages and range from 0 to 1.0 for each parameter. The goal is to distribute the wieght percentages across all the decision parameters in such a way they add up to 1.0. The higher the number given to a parameter, the more it will play into the ranking of precincts. 
           You should work with your campaign management Data, and Field teams to determine the appropriate canvass strategy and select the weight values to accurately align.
           
        **Results:**
        - The results should be a helful aid to the campaign to determine where to allocate resources and time. 
        - Feel free to experiment and re-run with the different weights to see how much the prioritized list changes. 
        - Its helpful to revisit at different parts of your campaign as factors and strategy may change.
        """)
        
    # Display the logo on the main page
    st.image("resources/client/Eskamani_Banner.png",width=700)
    col1,col2 = st.columns(2)
    with col1:
       st.title("Precinct Analysis Tool")
    with col2:
       st.image("resources/stratace/Campaign-Prioritizer_Logo.png",width=150)
    st.subheader("View key precinct data and create a priority list optimized for your campaign's strategy.")    
    st.divider()

    # Setup Page Tabs
    tab1, tab2 = st.tabs(["🔍Pricinct Explorer", "🔃 Pricinct Prioritizer"])
   
    #Precinct Explorer Tab
    with tab1:
       st.subheader("Select a precinct and explore its data")
       st.write("")
       precinctList =  precinctData['PRECINCT']
       selPrecinct = st.selectbox("Select a precinct from the following list",precinctList,index=None,help="Don't see the precinct you are looking for...? Contact your data team to have it added.")
       if selPrecinct != None:
          st.subheader("")
          st.subheader(f"Here is the data for precinct :blue[{selPrecinct}]")
          demogData = precinctData[precinctData['PRECINCT'] == selPrecinct]
          lat = demogData['LATITUDE']
          long = demogData['LONGITUDE']
          st.write(demogData)
          st.subheader("")
          # Pass selected precinct data to the HTML via a Streamlit event
          st.session_state.selected_coords = selected_coords
          #Map script from mapbox
           map_script = """
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
                    mapboxgl.accessToken = 'pk.eyJ1IjoiYXNoMTgyNSIsImEiOiJjbTF2M3J5M3EwN3ZhMmpvZXI1MzRnbGIxIn0.Ahb-c79xp6uR9gEyGGWsgQ'; 
                    const map = new mapboxgl.Map({{
                        container: 'map',
                        style: 'https://api.mapbox.com/styles/v1/ash1825/cm5hfbzgp002601qfezaz6ixn',
                        center: [{long}, {lat}],
                        zoom: 11
                    }});
            
                    window.addEventListener('message', (event) => {{
                        if (event.data && event.data.lat && event.data.lng) {{
                            map.flyTo({{
                                center: [event.data.lng, event.data.lat],
                                zoom: 14
                            }});
                        }}
                    }});
                </script>
           </body>
           </html>
           """
          st.subheader("TO-DO: place map here")
          st.components.v1.html(map_script, height=600)


   
    #Precinct Prioritizer Tab 
    with tab2:
       st.header("Set Weights to Match Your Campaign's Strategy")
       st.write("Use the sliders below to adjust each parameter weight. Please note that the total for all weights needs to equal 1.0.")
       # Inputs for weights
       total_registered_weight = st.slider("Weight for Total Registered Voters", min_value=0.0, max_value=1.0, step=0.05)
       dem_voter_weight = st.slider("Weight for Total Democrat Voters", min_value=0.0, max_value=1.0, step=0.05)
       rep_voter_weight = st.slider("Weight for Total Republican Voters", min_value=0.0, max_value=1.0, step=0.05)
       npa_voter_weight = st.slider("Weight for Total NPA/Other Voters", min_value=0.0, max_value=1.0, step=0.05)
       dem_turnout_weight = st.slider("Weight for Democrat Turnout", min_value=0.0, max_value=1.0, step=0.05)
       rep_turnout_weight = st.slider("Weight for Republican Turnout", min_value=0.0, max_value=1.0, step=0.05)
       npa_turnout_weight = st.slider("Weight for NPA/Other Turnout", min_value=0.0, max_value=1.0, step=0.05)
   
       # Calculate total weight
       total_weight = (total_registered_weight + dem_voter_weight + rep_voter_weight +
               npa_voter_weight + dem_turnout_weight + rep_turnout_weight + npa_turnout_weight)
   
       # Display total weight
       st.subheader(f"Current Total Weight: {total_weight:.2f}")
       if total_weight != 0.0 and total_weight != 1.0:
           st.warning("The sum of all weights must equal 1.0. Please adjust.")
       elif total_weight == 1.0:
           st.success("The sum of all weights is 1.0.")
       else:
           st.error("The sum of all weights must equal 1.0. Please adjust.")
       st.divider()
       
       # Initialize DataFrame
       newdf = pd.DataFrame()
       origdf = None
   
       with st.container(border=True):
           # Select data source
           st.subheader("Select Your Precinct Data File")
           data_source = st.radio("Choose the source of your CSV data file:", ["Local file upload", "Google Drive path"])
           if data_source == "Local file upload":
               # File upload
               uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
               if uploaded_file is not None:
                   origdf = pd.read_csv(uploaded_file)
           elif data_source == "Google Drive path":
               # Text input for Google Drive file path
               drive_path = st.text_input("Enter the full path to your CSV data file in Google Drive:")
               if drive_path:
                   if os.path.exists(drive_path):  # Check if the file exists
                       origdf = pd.read_csv(drive_path)
                   else:
                       st.error("The specified path does not exist. Please check the path and try again.")
   
       # Perform scoring if a valid DataFrame has been loaded and weights sum to 1.0
       if origdf is not None and total_weight == 1.0:
           # Ensure required columns are present in the CSV file
           required_columns = ["PRECINCT", "TOTAL REGISTERED", "PCT DEM", "PCT REP", "PCT NPA", "PCT OTHER", "DEM TURNOUT", "REP TURNOUT", "NPA TURNOUT"]
           score_columns = ["TOTAL REGISTERED", "PCT DEM", "PCT REP", "PCT NPA", "PCT OTHER", "DEM TURNOUT", "REP TURNOUT", "NPA TURNOUT"]
           if all(col in origdf.columns for col in required_columns):
               newdf['PRECINCT'] = origdf['PRECINCT']
               
               # Normalize each parameter column to a range of 0-1
               scaler = MinMaxScaler()
   
               newdf[score_columns] = scaler.fit_transform(origdf[score_columns])
   
               # Calculate weighted score for each precinct
               newdf['Score'] = (
                   total_registered_weight * newdf["TOTAL REGISTERED"] +
                   dem_voter_weight * newdf["PCT DEM"] +
                   rep_voter_weight * newdf["PCT REP"] +
                   npa_voter_weight * newdf["PCT NPA"] +
                   dem_turnout_weight * newdf["DEM TURNOUT"] + 
                   rep_turnout_weight * newdf["REP TURNOUT"] + 
                   npa_turnout_weight * newdf["NPA TURNOUT"]
               )
               
               # Sort by score in descending order
               sorted_indices = newdf["Score"].sort_values(ascending=False).index
               sorted_origdf = origdf.loc[sorted_indices]
               sorted_newdf = newdf.loc[sorted_indices]
   
               # Display sorted DataFrame
               st.divider()
               st.header("Prioritized Precincts List")
               numprecinct = st.number_input("How many Precincts would you like to focus on:", min_value=0, value=5)
       
               # Dynamically calculate stats for the top numprecinct precincts
               selected_origdf = sorted_origdf.head(numprecinct)
               selected_newdf = sorted_newdf.head(numprecinct)
       
               PrioritRegNum = selected_origdf["TOTAL REGISTERED"].sum()
               totaldem = (selected_origdf["PCT DEM"]*selected_origdf["TOTAL REGISTERED"]).sum()
               totalrep = (selected_origdf["PCT REP"]*selected_origdf["TOTAL REGISTERED"]).sum()
               totalnpa = (selected_origdf["PCT NPA"]*selected_origdf["TOTAL REGISTERED"]).sum()
       
               st.subheader(" ")
               st.write("Here is your full list of precincts in order from highest to lowest score:")
               st.write(selected_newdf)
               st.write(f"Here are the stats for the top {numprecinct} Precincts:")
               st.metric("Total Registered Voters", int(PrioritRegNum))
               col1, col2, col3 = st.columns(3)
               with col1:
                  st.metric("Total Dem Voters", int(totaldem))
               with col2:
                  st.metric("Total Rep Voters", int(totalrep))
               with col3:
                  st.metric("Total NPA Voters", int(totalnpa))
               st.divider()
   
           else:
               st.error(f"The CSV file must contain the following columns: {required_columns}")
       else:
           st.info("Please upload or specify a valid CSV file and ensure the weights sum to 1.0.")

   
    # App Footer
    st.divider()
    st.image("resources/stratace/StratAceBanner_Logo.png",width=300)
    st.write("https://strategyace.win/")
             
if __name__ == "__main__":
    main()

import streamlit as st
import geopandas as gpd
import pandas as pd

ELECTRES_PATH = "data/SD6_Election_Point_11082024.geojson"
VOTERUNI_PATH = "data/voter_universe.csv"

def initialize_shared():
  #Initialize Session State
  if 'shared_data' not in st.session_state:
    st.session_state['shared_data'] = {}

  #Read in Election Results GeoJSON
  electionDF = gpd.read_file(ELECTRES_PATH)  #geoJSON file of election results
  st.session_state['shared_data']['electionDF'] = electionDF

  #Read in Voter Universe Table
  voteruniverse = pd.read_csv(VOTERUNI_PATH)
  voterUniDF = pd.DataFrame(voteruniverse)
  st.session_state['shared_data']['voterUniDF'] = voterUniDF
    
  #calculated values:
  #winNum from page 1
  #date last update (mult.)

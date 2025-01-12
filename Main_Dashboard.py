import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from src.initializeshared import initialize_shared

st.set_page_config(page_title="Manager App", page_icon=":ballot_box_with_ballot:")

#initialize shared session state data
initialize_shared()

#Retrieve Session State Data
if 'shared_data' in st.session_state:
    winNum = st.session_state['shared_data'].get('winNum')
    voterUniDF = st.session_state['shared_data'].get('voterUniDF')

def main():
  
  #App Header
  st.image("resources/client/Eskamani_Banner.png",width=700)
  col1,col2 = st.columns(2)
  with col1:
    st.title("Orlando Mayoral Race")
  with col2:
    st.image("resources/client/Woman_User_Profile.png",width=150)
  
  # Input the future date (format: YYYY-MM-DD)
  future_date_str = "2027-11-02"
  future_date = datetime.strptime(future_date_str, "%Y-%m-%d")
  # Get today's date
  today = datetime.today()
  # Calculate the difference in days
  days_until = (future_date - today).days
  st.write("")
  st.subheader(f":blue[{days_until}] days until Election Day on 11/02/2027 !")
  st.subheader("")

  #Campaign Map
  st.image('resources/client/Orlando_City_Map.png')

  #Dashboard Values
  #Electorate Container
  with st.container(border=True):
    st.subheader("Electorate Overview")
    col1,col2 = st.columns(2)
    with col1:
      st.metric(label="Total Number of County Precincts", value="100")
    with col2:
      st.metric(label="Total Registered Voters", value="1000")
    col1,col2,col3 = st.columns(3)
    with col1:
      st.metric(label="Total Number Republicans", value="100")
    with col2:
      st.metric(label="Total Number Democrats", value="100")
    with col3:
      st.metric(label="Total Number NPAs/Others", value="100")
    st.write("")
    st.write(":green[*Data updated on 12/22/2024*]")
    
  #Voter Universe Container
  with st.container(border=True):
    st.subheader("Your Voter Universe")
    st.write("")
    if winNum != None:
      st.subheader("Your Campaign Win Number is  :blue[41,000] votes.")
    else:
      st.subheader("Navigate to the Win Analysis page to calculate your campaign's win #!")
        
    st.dataframe(voterUniDF, hide_index=True, width=800)
    st.markdown('''**Definitions**:\n\n **Hot**= Last 2 Gen & last 2 Prim....**Warmer**= Last 2 Gen & last Prim\n\n **Warm**= Last 2 Gen....**Infreq**= At least 1 vote in either last 2 Gen or 2 Prim
                ''')
    st.write(":green[*Data updated on 12/22/2024*]")
  
  
  #App Footer
  st.subheader("")
  st.divider()
  st.image("resources/stratace/StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")

if __name__ == "__main__":
    main()

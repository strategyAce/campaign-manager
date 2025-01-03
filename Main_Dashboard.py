import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

st.set_page_config(page_title="Manager App", page_icon=":ballot_box_with_ballot:")

def main():
  st.image("Eskamani_Banner.png",width=700)
  col1,col2 = st.columns(2)
  with col1:
    st.title("Orlando Mayoral Race")
  with col2:
    st.image("Woman_User_Profile.png",width=150)
  
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
  st.subheader("Your Campaign Win Number is  :blue[41,000] votes.")

  #Dashboard Values
  with st.container(border=True):
    st.subheader("Campaign Overview")
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
    st.subheader("Your Voter Universe")
    if os.path.exists("voter_universe.csv"):
      voteruniverse = pd.read_csv("voter_universe.csv")
      df = pd.DataFrame(voteruniverse)
      st.dataframe(df, hide_index=True)
    else:
      st.warning("No Voter Universe File Found")
    st.markdown('''**Definitions**:\n\n **Hot**= Last 2 Gen & last 2 Prim\n\n **Warmer**= Last 2 Gen & last Prim\n\n **Warm**= Last 2 Gen\n\n **Infreq**= At least 1 vote in either last 2 Gen or 2 Prim
                ''')
    st.write(":green[*Data updated on 12/22/2024*]")
  
  #Campaign Map
  st.image('Orlando_City_Map.png')
  
  #App Footer
  st.divider()
  st.image("StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")

if __name__ == "__main__":
    main()

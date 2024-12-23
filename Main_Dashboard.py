import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def main():
  col1,col2 = st.columns(2)
  with col1:
    st.title("TBD Mayoral Race")
  with col2:
    st.image("Woman_User_Profile.png",width=150)
  
  # Input the future date (format: YYYY-MM-DD)
  future_date_str = "2027-11-02"
  future_date = datetime.strptime(future_date_str, "%Y-%m-%d")
  # Get today's date
  today = datetime.today()
  # Calculate the difference in days
  days_until = (future_date - today).days
  
  st.subheader(f":blue[{days_until}] days until Election Day on 11/02/2027 !")
  

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
    st.write("*Data updated on 12/22/2024*")
    st.image('Orlando_City_Map.png')
    
  
  #App Footer
  st.divider()
  st.image("StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")

if __name__ == "__main__":
    main()

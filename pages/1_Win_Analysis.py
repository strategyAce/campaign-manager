import streamlit as st
import numpy as np

st.set_page_config(page_title="Win Analysis", page_icon=":arrows_clockwise:")

# Streamlit app
def main():

  #App Header
  st.image("Eskamani_Banner.png",width=700)
  st.title("Campaign Win Analysis")
  st.subheader("Easily calculate and keep track of your campaign's win number.")    
  st.divider()

  #Read in Data
  AvgTurnout = 33.3
  TotReg = 112000
  Date = "01/2025"

  #Calculated Values
  PredVoters = np.ceil((AvgTurnout/100)*TotReg)
  winNum = PredVoters+1

  st.subheader("The historical average percentage turnout for Orlando Mayoral race:")
  st.title(f"{AvgTurnout} %")
  st.write("")
  st.subheader(f"The total number of registered voters as of {Date} book closing:")
  st.title(f"{TotReg}")
  st.write("")
  st.subheader("Your Campaign Win Number:")
  st.title(f"{winNum}")
  st.write("")
  st.write("")
  buffer = st.slider("Select the percentage buffer you would like to add", 0.0,5.0,(2.0,3.0))
  votegoalL = PredVoters*((50+buffer[0])/100)
  votegoalH = PredVoters*((50+buffer[1])/100)
  st.subheader(f"Your vote goal range with the added buffer comes to:")
  st.title(f"{votegoalL} - {votegoalH}")
  
  
  # App Footer
  st.divider()
  st.image("StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")


if __name__ == "__main__":
    main()

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
  winNum = (PredVoters*0.5)+1

  st.subheader("The historical average percentage turnout for Orlando Mayoral race:")
  st.title(f":blue[{AvgTurnout} %]")
  st.write("")
  st.subheader(f"The total number of registered voters as of {Date} book closing:")
  st.title(f":blue[{TotReg}]")
  st.write("")
  st.subheader("Your Campaign Win Number:")
  st.title(f":blue[{winNum}]")
  st.write("")
  st.write("")
  buffer = st.slider("Select the percentage buffer you would like to add", 0.0,10.0,(2.0,5.0),step=1.0,help="These percentages are added to the Win # to provide a target goal range of votes your campaign hopes to achieve. Feel free to play with the sliders to see how the number of votes changes.")
  votegoalL = np.ceil(winNum*(1+(buffer[0]/100)))
  votegoalH = np.ceil(winNum*(1+(buffer[1]/100)))
  st.subheader(f"Your vote goal range with the added buffer comes to:")
  st.title(f":blue[{votegoalL} - {votegoalH}]")
  st.subheader("")
  st.subheader("")
  
  # App Footer
  st.divider()
  st.image("StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")


if __name__ == "__main__":
    main()

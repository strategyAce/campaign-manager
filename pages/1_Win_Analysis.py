import streamlit as st
import numpy as np

st.set_page_config(page_title="Win Analysis", page_icon=":arrows_clockwise:")

# Streamlit app
def main():

  # Sidebar with expandable User Guide section
  with st.sidebar.title("📘 User Guide / Instructions"):
    st.sidebar.write("""
    **Overview:**
       This webpage will help your campaign calculate your win number and vote goals/targets. 
       
       The page itself is smart and uses historical data curated by Strategy Ace to save you time and to make sure your team is up-to-date as registrations change over time")
    """)

  #App Header
  st.image("resources/client/Eskamani_Banner.png",width=700)
  st.title("Campaign Win Analysis")
  st.subheader("Easily calculate and keep track of your campaign's win number.")    
  st.divider()

  #Read in Data
  AvgTurnout = 33.3
  TotReg = 112000
  Date = "01/2025"

  #Calculated Values
  PredVoters = np.ceil((AvgTurnout/100)*TotReg)
  winNum = int((PredVoters*0.5)+1)
  #write to session state
  st.session_state['shared_data']['winNum'] = winNum

  #Report to user
  st.subheader("The historical average percentage turnout for Orlando Mayoral race:")
  st.title(f":blue[{AvgTurnout} %]")
  st.write("")
  st.write("")
  st.subheader(f"The total number of registered voters as of {Date} book closing:")
  st.title(f":blue[{TotReg}]")
  st.write("*Reported from Orange County Supervisor of Elections*")
  st.write("")
  st.subheader("Your Campaign Win Number:")
  st.title(f":blue[{winNum}]")
  st.write("*Win # = (Predicted # of Voters * 50%) + 1*")
  st.subheader("")
  st.subheader("Now lets calculate your vote goals with some buffer added:")
  buffer = st.slider("Select the percentage buffer you would like to add", 0.0,10.0,(2.0,5.0),step=1.0,help="These percentages are added to the Win # to provide a target goal range of votes your campaign hopes to achieve. Feel free to play with the sliders to see how the number of votes changes.")
  votegoalL = int(np.ceil(winNum*(1+(buffer[0]/100))))
  votegoalH = int(np.ceil(winNum*(1+(buffer[1]/100))))
  st.subheader(f"Your vote goal range with the added buffer comes to:")
  st.title(f":blue[{votegoalL} - {votegoalH}]")
  st.subheader("")
  
  
  st.empty()
  # App Footer
  st.divider()
  st.image("resources/stratace/StratAceBanner_Logo.png",width=300)
  st.write("https://strategyace.win/")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import numpy as np
from src.simulation import monte_carlo_simulation
from src.visualization import plot_election_results

st.set_page_config(page_title="Predictor", page_icon=":bar_chart:")


def main():
    
    # Sidebar with expandable User Guide section
    with st.sidebar.title("📘 User Guide / Instructions"):
        st.sidebar.write("""
        Welcome to the Campaign Predictor Tool!

        **Tool Overview:**
        The tool was built to simulate different election outcomes for 2 partisan candidates running against each other. The tool uses party demographic statistics from your election district as well as turnout data. It then runs as many simulations as you set and randomly alters the input parameters to give you a wide range of outcomes.

        **Simulation Inputs:**
        1. Input Fixed Simulation Variables
        1.1 Number of Runs
           This number dictates how many simulations are performed. The higher the number the longer the app may take to produce results. Its best practice to set to around 100 runs when doing a quick analysis and 1000 runs when looking for more accurate and thorough results.
        1.2 Number of Registered Voters
           These values should come directly from your official local government election officials.
           
        2. Define Monte Carlo Variables for Normal and Uniform distributions.
        2.1 Turnout Values
           These values are calculated from historical election data. Please consult with your data team to calculate these values.
           The values in the "Normal" section will be randomly selected based on a normal (or gaussian) probability distribution function.
        2.2 Vote Share Values
           These values are best guesses on how many voters from each political party will vote for you candidate. You will need to set a minimum and maximum percentage.
           The values in this "Uniform" section are randomly selected between the min and max. All values have equal probabiltiy of being selected between the min and max.

        **Results:**
        - Simulation results include win/loss probabilities and detailed statistics.
        - A vertical bar plot will visualize show how many simulations your candidate won a certain percentage of votes. All simulations where your candidate received 50%+1 vote will be considered a win.
        - WARNING: These result are probabilities!! Anything can happen in real life. It's important to take actions to increase the probabilities of your candidate winnning.
        """)
        
    # App Header
    col1,col2 = st.columns(2)
    with col1:
        st.title("Campaign Predictor Tool")
    with col2:
        st.image("Campaign-Predictor.png",width=200)
    st.subheader("Run predictions that can give your campaign an edge up on the competition")
    st.write("This is a product of Strategy Ace LLC")
    st.write("Version: BETAv0.1...date:09/29/2024")
    st.divider()

    # Initialize election_results to None
    election_results = None

    # Input Collection
    st.write("Enter Fixed Simulation Variables")
    num_runs = st.slider("Enter Number of Runs", 0, 2000, 1000,step=50)
    RegDems = st.number_input("Enter Number of Registered Democrats (fixed variable)", min_value=0, value=0, step=1)
    RegReps = st.number_input("Enter Number of Registered Republicans (fixed variable)", min_value=0, value=0, step=1)
    RegNPAs = st.number_input("Enter Number of Registered NPAs/Others (fixed variable)", min_value=0, value=0, step=1)
    st.divider()
    st.write("Enter Normal Distribution Monte Carlo Variables")
    # Create two columns
    col1, col2 = st.columns(2)
    # Add content to the first column
    with col1:
        DemMean = st.number_input("Enter mean value of Dem turnout %", min_value=0.00, max_value=100.00, value=0.00, step=1.00)
        RepMean = st.number_input("Enter mean value of Republican turnout %", min_value=0.00, max_value=100.00,value=0.00, step=1.00)            
        NPAMean = st.number_input("Enter mean value of NPA/Other turnout %", min_value=0.00, max_value=100.00, value=0.00, step=1.00)
    # Add content to the second column
    with col2:
        DemStd = st.number_input("Enter standard deviation of Dem turnout %", min_value=0.00, value=1.00, step=1.00)
        RepStd = st.number_input("Enter standard deviation of Republican turnout %", min_value=0.00, value=1.00, step=1.00)
        NPAStd = st.number_input("Enter standard deviation of NPA/Other turnout %", min_value=0.00, value=1.00, step=1.00)
    st.divider()
    st.write("Enter Uniform Distribution Monte Carlo Variables")
    Demvalues = st.slider("Enter the lower and upper % values of Democrats that vote for your candidate",0,100,(25,75))
    DemLow = Demvalues[0]
    DemHigh = Demvalues[1]
    Repvalues = st.slider("Enter the lower and upper % values of Republicans that vote for your candidate",0,100,(25,75))
    RepLow = Repvalues[0]
    RepHigh = Repvalues[1]
    NPAvalues = st.slider("Enter the lower and upper % values of NPA/Others that vote for your candidate",0,100,(25,75))
    NPALow = NPAvalues[0]
    NPAHigh = NPAvalues[1]

    if st.button("Run Simulation"):
        # Perform the Monte Carlo analysis
        election_results = monte_carlo_simulation(
            num_runs, DemLow, DemHigh, RepLow, RepHigh, NPALow, NPAHigh,
            DemMean, DemStd, RepMean, RepStd, NPAMean, NPAStd, 
            RegDems, RegReps, RegNPAs
        )
        
        if election_results is not None:
            st.write("Simulation Complete")
            st.divider()
            st.subheader("Simulation Results")
            # Calculate statistics
            Winvalues = election_results[election_results['% of Votes'] > 50.0]
            Lossvalues = election_results[election_results['% of Votes'] <= 50.0]
            
            # Display average votes
            win_stats = {
                'Win Mean Dem Votes': np.round(Winvalues['Dem Votes'].mean()),
                'Win Mean Rep Votes': np.round(Winvalues['Rep Votes'].mean()),
                'Win Mean NPA Votes': np.round(Winvalues['NPA Votes'].mean())
            }
            loss_stats = {
                'Loss Mean Dem Votes': np.round(Lossvalues['Dem Votes'].mean()),
                'Loss Mean Rep Votes': np.round(Lossvalues['Rep Votes'].mean()),
                'Loss Mean NPA Votes': np.round(Lossvalues['NPA Votes'].mean())
            }
            
            # Display results
            col1,col2 = st.columns(2)
            with col1:
                Pwin = len(Winvalues)/num_runs * 100
                st.write(f'Percentage of Wins = {Pwin:.2f}%')
                st.write(pd.DataFrame([win_stats]).T)
            with col2:
                Ploss = len(Lossvalues)/num_runs * 100
                st.write(f'Percentage of Loss = {Ploss:.2f}%')
                st.write(pd.DataFrame([loss_stats]).T)
            st.write("Full Simualtion Results Data")
            st.write(election_results)
            
            # Plot results
            fig = plot_election_results(election_results)
            st.pyplot(fig)


if __name__ == "__main__":
    main()

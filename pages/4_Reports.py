import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Reporter", page_icon=":page_facing_up:")

# Function to load CSV
def load_csv(data_source, uploaded_file=None, drive_path=None):
    try:
        if data_source == "Local file upload" and uploaded_file is not None:
            return pd.read_csv(uploaded_file)
        elif data_source == "Google Drive path" and drive_path:
            if os.path.exists(drive_path):
                return pd.read_csv(drive_path)
            else:
                st.error("The specified path does not exist.")
        else:
            st.error("No valid data source selected.")
    except Exception as e:
        st.error(f"Error loading file: {e}")
    return None

# Voter Engagement Report logic
def voter_engagement_report(df):
    st.divider()
    st.header("Voter Engagement Results Report")
    st.write("Select which engagements you would like included in the report")
    col1,col2,col3 = st.columns(3)
    with col1:
      textop = st.checkbox("Include Texts")
    with col2:
      callop = st.checkbox("Include Calls")
    with col3:
      canvassop = st.checkbox("Include Canvasses")
    st.divider()
    # Convert all columns except 'DATE' to numeric
    # Convert columns to numeric, handling non-numeric values
    allcolbutdate = df.columns.drop('DATE')
    df[allcolbutdate] = df[allcolbutdate].apply(pd.to_numeric, errors='coerce')
    totalsumcolumn = df[allcolbutdate].sum(axis=1)
    text_columns = [col for col in df.columns if col.startswith("TEXT-")]
    totaltextcolumn = df[text_columns].sum(axis=1)
    call_columns = [col for col in df.columns if col.startswith("CALL-")]
    totalcallcolumn = df[call_columns].sum(axis=1)
    canvas_columns = [col for col in df.columns if col.startswith("DOOR-")]
    totalcanvasscolumn = df[canvas_columns].sum(axis=1)
    Dem_columns = [col for col in df.columns if col.endswith("-DEM")]
    totalDemcolumn = df[Dem_columns].sum(axis=1)
    Rep_columns = [col for col in df.columns if col.endswith("-REP")]
    totalRepcolumn = df[Rep_columns].sum(axis=1)
    Npa_columns = [col for col in df.columns if col.endswith("-NPA")]
    totalNpacolumn = df[Npa_columns].sum(axis=1)
    
    lastrow = df.iloc[-1]
    secondlastrow = df.iloc[-2]
    st.subheader("Metrics At A Glance")
    prevTotalReached = int(secondlastrow.drop("DATE").sum())
    totalReached = int(lastrow.drop("DATE").sum())
    prevTotalcanvassed = int(totalcanvasscolumn.iloc[-2])
    totalcanvassed = int(totalcanvasscolumn.iloc[-1])
    col1,col2 =st.columns(2)
    with col1:
      st.write(f"Current update date: {df['DATE'].iloc[-1]}")
      st.metric("Total Voters Reached", value = totalReached, delta = totalReached-prevTotalReached)
    with col2:
      st.write(f"Previous update date: {df['DATE'].iloc[-2]}")
      st.metric("Total Canvassed", value = totalcanvassed, delta = totalcanvassed-prevTotalcanvassed)
    
    st.subheader(" ")
    # Create Engagement over Time Line Plot
    plt.figure(figsize=(10, 6))
    plt.plot(df["DATE"], totalsumcolumn, label="Total Engagements")
    plt.plot(df["DATE"], totaltextcolumn, label="Total Text")
    plt.plot(df["DATE"], totalcallcolumn, label="Total Call")
    plt.plot(df["DATE"], totalcanvasscolumn, label="Total Canvass")
    # Set labels and title
    plt.xlabel("Date")
    plt.ylabel("Voters Reached")
    plt.title("Voters Reached Over Time")
    # Add legend
    plt.legend()
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    
    st.subheader(" ")
    #Engagement Type By Pie Chart
    total_text = totaltextcolumn.sum()
    total_call = totalcallcolumn.sum()
    total_canvass = totalcanvasscolumn.sum()
    text_percentage = total_text/totalReached
    call_percentage = total_call/totalReached
    canvas_percentage = total_canvass/totalReached
    # Create the pie chart
    plt.figure(figsize=(6, 6))
    # Define the data for the pie chart
    data = [text_percentage, call_percentage, canvas_percentage]
    labels = ['Text', 'Call', 'Canvass']
    colors = ['cadetblue', 'powderblue', 'steelblue']
    # Create the pie chart
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    # Add title
    plt.title('Engagement Method Type')
    # Display the chart
    st.pyplot(plt)
    
    #Engagement Type By Party Vertical Bar Chart
    st.subheader("") # add spacing
    barchartdata = pd.DataFrame({
            "Party": ["Democrat", "Republican", "NPA/Other"],
            "Voters": [totalDemcolumn.sum(), totalRepcolumn.sum(), totalNpacolumn.sum()]
        })
    fig, ax = plt.subplots(figsize=(8, 6))
    barchartdata.plot(x="Party", y="Voters", kind="bar", ax=ax, color=["dodgerblue", "red", "goldenrod"])
    ax.set_title("Engagements By Party")
    ax.set_xlabel("Party")
    ax.set_ylabel("Voters")
    st.pyplot(fig)
    
    #Full data table
    st.subheader(" ")
    st.subheader("Full Engagement Data Table")
    st.write(df[allcolbutdate])
    
    st.subheader("") # add spacing
    st.write("Click here to produce a pdf file of this report:")
    st.button("Print Report", key=print, type="primary")
    st.divider()

# Election Runup Analysis Report logic
def election_runup_report(df):
    st.divider()
    st.header("Election Results Report")

    # Ensure required columns are present in the CSV file
    required_columns = ["DATE", "VBM-DEM", "VBM-REP", "VBM-NPA", "VBM-TOTAL", "VBM-CUM", "EV-DEM", "EV-REP", "EV-NPA","EV-TOTAL","EV-CUM","ED-DEM","ED-REP","ED-NPA","ED-TOTAL","TOTAL VOTES","CUM TOTAL"]
    if set(df.columns) == set(required_columns):
        col1,col2 =st.columns(2)
        with col1:
            st.write(f"Current update date: {df['DATE'].iloc[-1]}")
        with col2:
            st.write(f"Previous update date: {df['DATE'].iloc[-2]}")
        st.metric(label="Total Votes Cast This Election", value=int(df['CUM TOTAL'].iloc[-1]), delta=int(df['CUM TOTAL'].iloc[-1] - df['CUM TOTAL'].iloc[-2]))
        col1,col2,col3 = st.columns(3)
        with col1:
            total_dem = int(df['VBM-DEM'].iloc[-1] + df['EV-DEM'].iloc[-1])
            prev_dem = int(df['VBM-DEM'].iloc[-2] + df['EV-DEM'].iloc[-2])
            st.metric(label="Total DEM Votes", value=total_dem, delta=total_dem-prev_dem)
        with col2:
            total_rep = int(df['VBM-REP'].iloc[-1] + df['EV-REP'].iloc[-1])
            prev_rep = int(df['VBM-REP'].iloc[-2] + df['EV-REP'].iloc[-2])
            st.metric(label="Total REP Votes", value=total_rep, delta=total_rep-prev_rep)
        with col3:
            total_npa = int(df['VBM-NPA'].iloc[-1] + df['EV-NPA'].iloc[-1])
            prev_npa = int(df['VBM-NPA'].iloc[-2] + df['EV-NPA'].iloc[-2])
            st.metric(label="Total NPA/Other Votes", value=total_npa, delta=total_npa-prev_npa)
    
        st.subheader("")
        # Create Vote over Time Line Plot
        plt.figure(figsize=(10, 6))
        plt.plot(df["DATE"], df["CUM TOTAL"], label="Total Votes")
        plt.plot(df["DATE"], df["EV-CUM"], label="Total Early Votes")
        plt.plot(df["DATE"], df["VBM-CUM"], label="Total Vote By Mail Votes")
        # Set labels and title
        plt.xlabel("Date")
        plt.ylabel("Votes")
        plt.title("Election Votes Over Time")
        # Add legend
        plt.legend()
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        # Show the plot
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)
    
        st.subheader("")
        # VBM vs Early Vote Pie Chart
        # Calculate the percentage of each vote type
        vote_by_mail_percentage = (df['VBM-CUM'].iloc[-1] / df['CUM TOTAL'].iloc[-1]) * 100
        early_vote_percentage = (df['EV-CUM'].iloc[-1]/ df['CUM TOTAL'].iloc[-1]) * 100
        # Create the pie chart
        plt.figure(figsize=(6, 6))
        # Define the data for the pie chart
        data = [vote_by_mail_percentage, early_vote_percentage]
        labels = ['Vote By Mail', 'Early Vote']
        colors = ['lightblue', 'lightgreen']
        # Create the pie chart
        plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        # Add title
        plt.title('Vote By Mail vs. Early Vote')
        # Display the chart
        st.pyplot(plt)
    
        st.subheader("")
        # VBM Party Breadkdown Pie Chart
        # Calculate the percentage of each vote type
        vbm_dem = (df['VBM-DEM'].sum() / df['VBM-CUM'].iloc[-1]) * 100
        vbm_rep = (df['VBM-REP'].sum() / df['VBM-CUM'].iloc[-1]) * 100
        vbm_npa = (df['VBM-NPA'].sum() / df['VBM-CUM'].iloc[-1]) * 100
        # Create the pie chart
        plt.figure(figsize=(6, 6))
        # Define the data for the pie chart
        data = [vbm_dem, vbm_rep, vbm_npa]
        labels = ['Dem', 'Rep', 'NPA/Other']
        colors = ['blue', 'red', 'green']
        # Create the pie chart
        plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        # Add title
        plt.title('Vote By Mail by Party')
        # Display the chart
        st.pyplot(plt)
    
        st.subheader("")
        # EV Party Breadkdown Pie Chart
        # Calculate the percentage of each vote type
        ev_dem = (df['EV-DEM'].sum() / df['EV-CUM'].iloc[-1]) * 100
        ev_rep = (df['EV-REP'].sum() / df['EV-CUM'].iloc[-1]) * 100
        ev_npa = (df['EV-NPA'].sum() / df['EV-CUM'].iloc[-1]) * 100
        # Create the pie chart
        plt.figure(figsize=(6, 6))
        # Define the data for the pie chart
        data = [ev_dem, ev_rep, ev_npa]
        labels = ['Dem', 'Rep', 'NPA/Other']
        colors = ['blue', 'red', 'green']
        # Create the pie chart
        plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        # Add title
        plt.title('Early Voting by Party')
        # Display the chart
        st.pyplot(plt)
    
        st.divider()
        #Analysis tool for determining current race status
        st.header("The Guestimator Tool")
        st.write("Use the sliders below to guestimate how your candidate is performing. The tool uses the uploaded current vote data.")
        totaldemvotes = df['VBM-DEM'].sum() + df['EV-DEM'].sum()
        totalrepvotes = df['VBM-REP'].sum() + df['EV-REP'].sum()
        totalnpavotes = df['VBM-NPA'].sum() + df['EV-NPA'].sum()
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Good Guys")
            gooddem = st.slider("Est. percentage of DEM Vote for your candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
            goodrep = st.slider("Est. percentage of REP Vote for your candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
            goodnpa = st.slider("Est. percentage of NPA/Other Vote for your candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
        with col2:
            st.subheader("Bad Guys")
            baddem = st.slider("Est. percentage of DEM Vote for other candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
            badrep = st.slider("Est. percentage of REP Vote for other candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
            badnpa = st.slider("Est. percentage of NPA/Other Vote for other candidate",min_value=0.00,max_value=1.00,value=0.50,step=0.05)
        #Calculate Total Votes for each Candidate
        totalgood = (gooddem*totaldemvotes) + (goodrep*totalrepvotes) + (goodnpa*totalnpavotes)
        totalbad = (baddem*totaldemvotes) + (badrep*totalrepvotes) + (badnpa*totalnpavotes)
        barchartdata = pd.DataFrame({
            "Candidate": ["Your Candidate", "Opposing Candidate"],
            "Votes": [totalgood, totalbad]
        })
    
        #Guestimate Bar Chart
        st.subheader("") # add spacing
        fig, ax = plt.subplots(figsize=(8, 6))
        barchartdata.plot(x="Candidate", y="Votes", kind="bar", ax=ax, color=["blue", "red"])
        ax.set_title("Candidate Vote Totals")
        ax.set_xlabel("Candidate")
        ax.set_ylabel("Votes")
        st.pyplot(fig)
        #TO-DO: Add error bars
    
        st.subheader("") # add spacing
        st.write("Click here to produce a pdf file of this report:")
        st.button("Print Report", key=print, type="primary")

        st.markdown(
        """
        <style>
        .print-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
        </style>
        <button class="print-button" onclick="window.print()">Print this page</button>
        """,
        unsafe_allow_html=True)
        st.divider()

# Main application
def main():
    col1, col2 = st.columns(2)
    with col1:
        st.title("Campaign Reporter Tool")
    with col2:
        st.image("Campaign-Reporter_Logo.png",width=150)
    st.subheader("Review and generate tailored campaign reports")
    st.divider()

    # Report type selection
    report_type = st.selectbox("What kind of Report do you want to create?",
                               ["Voter Engagement", "Election Runup Analysis"])
    st.subheader(" ")
    with st.container(border=True):
        # Data source selection
        data_source = st.radio("Choose the source of your CSV file:", ["Local file upload", "Google Drive path"])
        uploaded_file = None
        drive_path = None

        if data_source == "Local file upload":
            uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        elif data_source == "Google Drive path":
            drive_path = st.text_input("Enter the path to your CSV file:")

    df = load_csv(data_source, uploaded_file, drive_path)

    if df is not None:
        if report_type == "Voter Engagement":
            voter_engagement_report(df)
        elif report_type == "Election Runup Analysis":
            election_runup_report(df)
    else:
        st.info("Please upload or specify a valid CSV file.")

    #App Footer
    st.divider()
    st.image("StratAceBanner_Logo.png",width=300)
    st.write("https://strategyace.win/")

if __name__ == "__main__":
    main()

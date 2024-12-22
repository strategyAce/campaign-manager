import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def main():
  st.title("TBD Mayoral Race")
  # Input the future date (format: YYYY-MM-DD)
  future_date_str = "2024-12-31"
  future_date = datetime.strptime(future_date_str, "%Y-%m-%d")

  # Get today's date
  today = datetime.today()
  
  # Calculate the difference in days
  days_until = (future_date - today).days
  
  st.subheader(f"{days_until} days until Election Day.")

  st.image('Orlando_City_Map.png')
    

if __name__ == "__main__":
    main()

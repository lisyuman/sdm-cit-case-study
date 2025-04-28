import pandas as pd
import streamlit as st

# Load forecast data
df = pd.read_csv('case1_forecast/SupermanPlus_Forecast.csv')

st.set_page_config(page_title="Superman Plus Demand Forecast", layout="wide")
st.title('📈 Superman Plus 15-Week Demand Forecast')

st.markdown('---')

# Regional selection
region = st.selectbox("Select Region:", ['AMR', 'Europe', 'PAC'])

st.subheader(f"Forecasted Demand for {region}")
st.line_chart(df.set_index('Week')[region])

# Table view
st.subheader("Full Forecast Data")
st.dataframe(df)
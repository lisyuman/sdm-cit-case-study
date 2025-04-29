import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
dwarf_plus_data = pd.DataFrame({
    'Week': [
        'Sept Wk3', 'Sept Wk4', 'Oct Wk1', 'Oct Wk2', 'Oct Wk3',
        'Oct Wk4', 'Oct Wk5', 'Nov Wk1', 'Nov Wk2', 'Nov Wk3',
        'Nov Wk4', 'Dec Wk1', 'Dec Wk2', 'Dec Wk3', 'Dec Wk4'
    ],
    'AMR': [320, 220, 170, 190, 200, 170, 160, 160, 140, 140, 180, 160, 160, 170, 190],
    'Europe': [80, 100, 60, 100, 100, 90, 80, 80, 80, 70, 90, 80, 80, 80, 70],
    'PAC': [230, 210, 140, 140, 140, 150, 140, 175, 140, 90, 90, 100, 110, 100, 90]
})

princess_plus_data = pd.DataFrame({
    'Week': [
        'Oct Wk4', 'Oct Wk5', 'Nov Wk1', 'Nov Wk2', 'Nov Wk3',
        'Nov Wk4', 'Dec Wk1', 'Dec Wk2', 'Dec Wk3', 'Dec Wk4',
        'Jan Wk1', 'Jan Wk2', 'Jan Wk3', 'Jan Wk4', 'Jan Wk5'
    ],
    'AMR': [240, 170, 130, 90, 110, 130, 110, 110, 110, 130, 70, 90, 100, 80, 90],
    'Europe': [100, 80, 90, 80, 70, 60, 60, 60, 50, 50, 50, 80, 80, 60, 50],
    'PAC': [150, 220, 240, 150, 130, 120, 110, 100, 110, 100, 120, 130, 160, 120, 100]
})

# Load forecast outputs
forecast_with_tech = pd.read_csv('../case1_forecast/case1_forecast_with_tech_sensitivity.csv')
forecast_without_tech = pd.read_csv('../case1_forecast/case1_forecast_without_tech_sensitivity.csv')

# Set up Streamlit page
st.set_page_config(page_title="Superman Plus Forecast Dashboard", layout="wide")

st.title("📊 Superman Plus Demand Forecast Dashboard")

# Create Tabs
tab1, = st.tabs(["📈 Forecast Visualization"])

with tab1:
    st.header("1️⃣ Historical Sales Data (Dwarf Plus vs Princess Plus)")

    # Plot historical data
    fig, ax = plt.subplots(figsize=(15,6))

    for region in ['AMR', 'Europe', 'PAC']:
        ax.plot(dwarf_plus_data['Week'], dwarf_plus_data[region], label=f'Dwarf Plus {region}', linestyle='--')
        ax.plot(princess_plus_data['Week'], princess_plus_data[region], label=f'Princess Plus {region}', marker='o')

    plt.xticks(rotation=45)
    plt.xlabel('Week')
    plt.ylabel('Units Sold')
    plt.title('Historical Sales Data Comparison')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

    st.markdown("---")

    st.header("2️⃣ Superman Plus Demand Forecast")

    # Parameter to switch "with or without tech sensitivity"
    tech_choice = st.radio(
        "Select Forecast Version:",
        ('With Tech Sensitivity (PAC +3%)', 'Without Tech Sensitivity'),
        index=0
    )

    if tech_choice == 'With Tech Sensitivity (PAC +3%)':
        selected_forecast = forecast_with_tech
    else:
        selected_forecast = forecast_without_tech

    # Plot forecast
    fig2, ax2 = plt.subplots(figsize=(15,6))

    for region in ['AMR', 'Europe', 'PAC']:
        ax2.plot(selected_forecast['Week'], selected_forecast[region], label=f'Superman Plus {region}', marker='o')

    plt.xticks(rotation=45)
    plt.xlabel('Week')
    plt.ylabel('Units Forecasted')
    plt.title(f'Superman Plus Forecast ({tech_choice})')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig2)

    st.dataframe(selected_forecast.style.format({'AMR': '{:.0f}', 'Europe': '{:.0f}', 'PAC': '{:.0f}'}))

st.success("✅ Dashboard loaded successfully!")

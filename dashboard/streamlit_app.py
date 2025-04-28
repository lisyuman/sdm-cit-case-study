import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Inject custom CSS for better styling
st.markdown("""
    <style>
    body, .stApp { background-color: #F7F7F7; color: #333333; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Helvetica', sans-serif; font-weight: 800; }
    .dataframe tbody tr:hover { background-color: #eef6ff; }
    </style>
""", unsafe_allow_html=True)

# Set page config
st.set_page_config(page_title="Superman Plus Planning Dashboard", layout="wide")

# Title
st.title("🚀 Superman Plus Planning Dashboard")

# --- Add a loading spinner ---
with st.spinner('Loading data and building dashboard...'):
    # Load data
    forecast_df = pd.read_csv('case1_forecast/case1_forecast.csv')
    allocation_df = pd.read_csv('case2_allocation/case2_allocation.csv')

    # Create raw data manually
    princess_plus_raw = {
        'Week': ['OctWk4', 'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1', 'DecWk2', 'DecWk3', 'DecWk4', 'JanWk1', 'JanWk2', 'JanWk3', 'JanWk4', 'JanWk5'],
        'AMR': [240, 170, 130, 90, 110, 130, 110, 110, 110, 130, 70, 90, 100, 80, 90],
        'Europe': [100, 80, 90, 80, 70, 60, 60, 60, 50, 50, 50, 80, 80, 60, 50],
        'PAC': [150, 220, 240, 150, 130, 120, 110, 100, 110, 100, 120, 130, 160, 120, 100]
    }
    dwarf_plus_raw = {
        'Week': ['SepWk3', 'SepWk4', 'OctWk1', 'OctWk2', 'OctWk3', 'OctWk4', 'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1', 'DecWk2', 'DecWk3', 'DecWk4'],
        'AMR': [320, 220, 170, 190, 200, 170, 160, 160, 140, 140, 180, 160, 160, 170, 190],
        'Europe': [80, 100, 60, 100, 100, 90, 80, 80, 80, 70, 90, 80, 80, 80, 70],
        'PAC': [230, 210, 140, 140, 140, 150, 140, 175, 140, 90, 90, 100, 110, 100, 90]
    }
    df_princess = pd.DataFrame(princess_plus_raw)
    df_dwarf = pd.DataFrame(dwarf_plus_raw)

# --- Tabs ---
tab1, tab2 = st.tabs(["Case 1: Demand Forecast", "Case 2: Material Allocation"])

# --- Case 1 ---
with tab1:
    st.header("📈 Case 1: Demand Forecast (15 Weeks)")

    with st.expander("🔎 View Raw Data for Case 1", expanded=False):
        raw_choice = st.selectbox("Select Raw Data:", ['Princess Plus Historical', 'Dwarf Plus Historical'])
        if raw_choice == 'Princess Plus Historical':
            st.dataframe(df_princess, use_container_width=True)
        elif raw_choice == 'Dwarf Plus Historical':
            st.dataframe(df_dwarf, use_container_width=True)

    st.subheader("📋 Forecasted Weekly Demand")
    st.dataframe(forecast_df, use_container_width=True)

    st.subheader("📊 Forecast Trend by Region")
    selected_region = st.selectbox("Select Region:", ['All', 'AMR', 'Europe', 'PAC'])

    fig, ax = plt.subplots(figsize=(10, 5))
    if selected_region == 'All':
        for region in ['AMR', 'Europe', 'PAC']:
            ax.plot(forecast_df['Week'], forecast_df[region], marker='o', label=region)
            for i, txt in enumerate(forecast_df[region]):
                ax.annotate(txt, (forecast_df['Week'][i], forecast_df[region][i]), fontsize=8, textcoords="offset points", xytext=(0,5), ha='center')
    else:
        ax.plot(forecast_df['Week'], forecast_df[selected_region], marker='o', label=selected_region)
        for i, txt in enumerate(forecast_df[selected_region]):
            ax.annotate(txt, (forecast_df['Week'][i], forecast_df[selected_region][i]), fontsize=8, textcoords="offset points", xytext=(0,5), ha='center')

    plt.title('Superman Plus Weekly Forecast', fontsize=20)
    plt.xlabel('Week', fontsize=14)
    plt.ylabel('Units Forecasted', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    st.pyplot(fig)

# --- Case 2 ---
with tab2:
    st.header("📦 Case 2: Material Allocation (Jan Wk4)")

    with st.expander("🔎 View Raw Data for Case 2", expanded=False):
        st.markdown("**Material Supply and Demand Overview**")
        st.write("""
        - Total Cumulative Supply at Jan Wk4: 320 units
        - Jan Wk1 Actual Builds: Superman 70, Superman Plus 70, Superman Mini 60
        - Jan Wk4 Cumulative Demand FCT:
          - Superman 110
          - Superman Plus 150
          - Superman Mini 70
        - PAC Reseller Critical Demand: 35 units
        """)

    st.subheader("📋 Final Allocation Table")
    st.dataframe(allocation_df, use_container_width=True)

    # Allow user to sort Allocation Chart
    st.subheader("🎨 Allocation Distribution (Artistic View)")
    sort_choice = st.radio("Sort Allocation by:", ['Original', 'Descending by Units'])
    
    plot_df = allocation_df.copy()
    if sort_choice == 'Descending by Units':
        plot_df = plot_df.sort_values(by='Allocated_Units', ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10,6))
    colors = ['#0077B6', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#023E8A', '#03045E']
    plot_df.plot(kind='bar', x='Channel', y='Allocated_Units', color=colors, legend=False, ax=ax2)

    plt.title('Material Allocation by Channel', fontsize=20, color='#0077B6')
    plt.xlabel('Channel', fontsize=14)
    plt.ylabel('Allocated Units', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', linewidth=0.7)

    for container in ax2.containers:
        ax2.bar_label(container, fmt='%d', label_type='edge', fontsize=10)

    st.pyplot(fig2)

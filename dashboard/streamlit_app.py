import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Supply-Demand Planning Dashboard", layout="wide")

# Inject custom CSS
st.markdown("""
    <style>
    body, .stApp { background-color: #000000; color: #e6d97e; font-family: 'Helvetica', sans-serif; }
    h1, h2, h3 { font-weight: 800; margin-bottom: 1rem; }
    .block-container { padding: 2rem; }
    .dataframe tbody tr:hover { background-color: #eef6ff; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚀 Supply-Demand Planning Dashboard")

# Loading spinner
with st.spinner('Loading dashboard...'):
    # Load data
    forecast_df = pd.read_csv('case1_forecast/case1_forecast.csv')
    allocation_df = pd.read_csv('case2_allocation/case2_allocation.csv')

    # Create manual raw data
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

# Tabs
tab1, tab2 = st.tabs(["📈 Case 1: Demand Forecast", "📦 Case 2: Material Allocation"])

# --- Case 1 Tab ---
with tab1:
    with st.container():
        st.header("Raw Data Overview")
        with st.expander("🔍 View Raw Historical Data", expanded=False):
            raw_choice = st.selectbox("Select Dataset:", ['Princess Plus', 'Dwarf Plus'])
            if raw_choice == 'Princess Plus':
                st.dataframe(df_princess, use_container_width=True)
            else:
                st.dataframe(df_dwarf, use_container_width=True)

    st.markdown("---")

    with st.container():
        st.header("Forecasted Weekly Demand")
        st.dataframe(forecast_df, use_container_width=True)

    st.markdown("---")

    with st.container():
        st.header("Forecast Trend by Region")
        selected_region = st.selectbox("Select Region to Plot:", ['All', 'AMR', 'Europe', 'PAC'])

        fig, ax = plt.subplots(figsize=(12, 6))
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
        plt.ylabel('Units', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.legend()
        st.pyplot(fig)

# --- Case 2 Tab ---
with tab2:
    with st.container():
        st.header("Material Supply and Demand Info")
        with st.expander("🔍 View Supply/Demand Key Data", expanded=False):
            st.write("""
            - Total Cumulative Supply at Jan Wk4: 320 units
            - Jan Wk1 Actual Builds: Superman 70, Superman Plus 70, Superman Mini 60
            - Jan Wk4 Cumulative Demand FCT:
              - Superman 110
              - Superman Plus 150
              - Superman Mini 70
            - PAC Reseller Critical Demand: 35 units
            """)

    st.markdown("---")

    with st.container():
        st.header("Final Allocation Table")
        st.dataframe(allocation_df, use_container_width=True)

    st.markdown("---")

    with st.container():
        st.header("Allocation Distribution")
        sort_choice = st.radio("Sort Allocation:", ['Original', 'Descending by Units'])

        plot_df = allocation_df.copy()
        if sort_choice == 'Descending by Units':
            plot_df = plot_df.sort_values(by='Allocated_Units', ascending=False)

        fig2, ax2 = plt.subplots(figsize=(12,6))
        colors = ['#0077B6', '#90E0EF', '#48CAE4', '#00B4D8', '#0096C7', '#023E8A', '#03045E']
        plot_df.plot(kind='bar', x='Channel', y='Allocated_Units', color=colors, legend=False, ax=ax2)

        plt.title('Material Allocation by Channel', fontsize=20)
        plt.xlabel('Channel', fontsize=14)
        plt.ylabel('Allocated Units', fontsize=14)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        for container in ax2.containers:
            ax2.bar_label(container, fmt='%d', label_type='edge', fontsize=10)

        st.pyplot(fig2)

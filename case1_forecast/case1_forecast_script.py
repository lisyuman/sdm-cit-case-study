import pandas as pd

# Princess Plus historical weekly sales
princess_plus = {
    'Week': ['OctWk4', 'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4',
             'DecWk1', 'DecWk2', 'DecWk3', 'DecWk4', 'JanWk1', 'JanWk2',
             'JanWk3', 'JanWk4', 'JanWk5'],
    'AMR': [240, 170, 130, 90, 110, 130, 110, 110, 110, 130, 70, 90, 100, 80, 90],
    'Europe': [100, 80, 90, 80, 70, 60, 60, 60, 50, 50, 50, 80, 80, 60, 50],
    'PAC': [150, 220, 240, 150, 130, 120, 110, 100, 110, 100, 120, 130, 160, 120, 100]
}

# Dwarf Plus historical weekly sales
dwarf_plus = {
    'Week': ['SepWk3', 'SepWk4', 'OctWk1', 'OctWk2', 'OctWk3', 'OctWk4',
             'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1',
             'DecWk2', 'DecWk3', 'DecWk4'],
    'AMR': [320, 220, 170, 190, 200, 170, 160, 160, 140, 140, 180, 160, 160, 170, 190],
    'Europe': [80, 100, 60, 100, 100, 90, 80, 80, 80, 70, 90, 80, 80, 80, 70],
    'PAC': [230, 210, 140, 140, 140, 150, 140, 175, 140, 90, 90, 100, 110, 100, 90]
}

df_princess = pd.DataFrame(princess_plus)
df_dwarf = pd.DataFrame(dwarf_plus)

# Calculate Price Elasticity (PE)

# Price change
price_dwarf = 120
price_princess = 200
price_change_pct = (price_princess - price_dwarf) / price_dwarf

# Demand change per region
pe_ratios = {}
for region in ['AMR', 'Europe', 'PAC']:
    demand_dwarf = df_dwarf[region].sum()
    demand_princess = df_princess[region].sum()
    demand_change_pct = (demand_princess - demand_dwarf) / demand_dwarf
    pe_ratios[region] = demand_change_pct / price_change_pct

print("Calculated Price Elasticity per Region:", pe_ratios)

# Build Superman Plus Forecast

# Superman Plus schedule weeks (correct week names)
weeks = ['SepWk3', 'SepWk4', 'OctWk1', 'OctWk2', 'OctWk3', 'OctWk4',
         'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1',
         'DecWk2', 'DecWk3', 'DecWk4']

# Seasonality factor per week
seasonality_factor = []
for i, week in enumerate(weeks):
    if week in ['SepWk3', 'SepWk4']:
        seasonality_factor.append(1.25)
    elif week in ['OctWk1', 'OctWk2']:
        seasonality_factor.append(1.15)
    else:
        seasonality_factor.append(1.0)

# Superman Plus price elasticity adjustment
price_new = 205
price_increase_pct = (price_new - price_princess) / price_princess  # 2.5% increase

# Adjustment multiplier per region
pe_adjustment_multiplier = {region: 1 + (pe_ratios[region] * price_increase_pct) for region in ['AMR', 'Europe', 'PAC']}

# Build forecast
forecast = {'Week': [], 'AMR': [], 'Europe': [], 'PAC': []}

for i in range(15):
    forecast['Week'].append(weeks[i])
    for region in ['AMR', 'Europe', 'PAC']:
        base_value = df_princess.loc[i, region]
        value = base_value * seasonality_factor[i] * pe_adjustment_multiplier[region]
        forecast[region].append(round(value))

forecast_df = pd.DataFrame(forecast)

print("\nSuperman Plus Forecast Table:\n")
print(forecast_df)

# Save to CSV
forecast_df.to_csv('SupermanPlus_Forecast.csv', index=False)
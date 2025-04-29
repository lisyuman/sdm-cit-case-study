import pandas as pd
import matplotlib.pyplot as plt

class SupermanPlusForecaster:
    def __init__(self, dwarf_plus_data, princess_plus_data):
        self.dwarf_data = dwarf_plus_data
        self.princess_data = princess_plus_data
        self.price_dwarf_plus = 120
        self.price_princess_plus = 200
        self.price_superman = 205

        self.regions = ['AMR', 'Europe', 'PAC']

        self.price_change_pct = (self.price_princess_plus - self.price_dwarf_plus) / self.price_dwarf_plus  # 66.67%
        self.small_price_change_pct = (self.price_superman - self.price_princess_plus) / self.price_princess_plus  # 2.5%

        self.pe_ratios = self.calculate_pe_ratios()

        self.price_adjustment = {region: self.pe_ratios[region] * self.small_price_change_pct for region in self.regions}
        self.tech_uplift = {'AMR': 0.0, 'Europe': 0.0, 'PAC': 0.03}
        self.special_weeks_adjustment = self.calculate_special_week_adjustments()

    def calculate_pe_ratios(self):
        pe_ratios = {}
        for region in self.regions:
            dwarf_avg = self.dwarf_data[region].mean()
            princess_avg = self.princess_data[region].mean()
            demand_change_pct = (princess_avg - dwarf_avg) / dwarf_avg
            pe = demand_change_pct / self.price_change_pct
            pe_ratios[region] = pe
        return pe_ratios

    def calculate_special_week_adjustments(self):
        adjustments = {region: {} for region in self.regions}

        # Define special weeks and calculate uplift/drop using 2 weeks before + 2 weeks after rule
        special_weeks = {
            'AMR': {'Nov Wk4': 'boost', 'Dec Wk4': 'boost', 'Oct Wk1': 'drop'},
            'Europe': {'Nov Wk4': 'boost', 'Oct Wk1': 'drop'},
            'PAC': {'Nov Wk1': 'boost', 'Jan Wk3': 'boost', 'Oct Wk1': 'drop'}
        }

        week_indices = {week: idx for idx, week in enumerate(self.dwarf_data['Week'])}

        for region, weeks in special_weeks.items():
            for week, effect in weeks.items():
                idx = week_indices.get(week)
                if idx is None or idx < 2 or idx > 12:
                    continue  # Skip if no enough data

                # Take 2 weeks before + 2 weeks after
                baseline = self.dwarf_data.loc[[idx-2, idx-1, idx+1, idx+2], region].mean()
                special_week_sales = self.dwarf_data.loc[idx, region]
                uplift_pct = (special_week_sales - baseline) / baseline

                if effect == 'boost' and uplift_pct > 0:
                    adjustments[region][idx] = uplift_pct
                elif effect == 'drop' and uplift_pct < 0:
                    adjustments[region][idx] = uplift_pct

        return adjustments

    def apply_forecast(self, apply_tech_sensitivity=True):
        forecasts = {'Week': [], 'AMR': [], 'Europe': [], 'PAC': []}

        for idx, week_label in enumerate(self.princess_data['Week']):
            forecasts['Week'].append(week_label)
            for region in self.regions:
                base_demand = self.princess_data.loc[idx, region]

                # Launch Seasonality Uplift: First 5 weeks +10%
                if idx < 5:
                    base_demand *= 1.10

                # Special Week Adjustment
                special_weeks = self.special_weeks_adjustment.get(region, {})
                if idx in special_weeks:
                    base_demand *= (1 + special_weeks[idx])

                # Price Elasticity Adjustment
                base_demand *= (1 + self.price_adjustment[region])

                # Tech Sensitivity Adjustment
                if apply_tech_sensitivity and region == 'PAC':
                    base_demand *= (1 + self.tech_uplift[region])

                forecasts[region].append(round(base_demand))

        return pd.DataFrame(forecasts)

    def save_forecast(self, df, filename):
        df.to_csv(filename, index=False)

    def plot_input_data(self):
        plt.figure(figsize=(15, 6))

        for region in self.regions:
            plt.plot(self.dwarf_data['Week'], self.dwarf_data[region], label=f'Dwarf Plus {region}', linestyle='--')
            plt.plot(self.princess_data['Week'], self.princess_data[region], label=f'Princess Plus {region}', marker='o')

        plt.xticks(rotation=45)
        plt.xlabel('Week')
        plt.ylabel('Units Sold')
        plt.title('Historical Sales Data: Dwarf Plus vs Princess Plus')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# ================================
# Main Execution
# ================================

# Input raw data
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

# Initialize forecaster
forecaster = SupermanPlusForecaster(dwarf_plus_data, princess_plus_data)

# Plot input raw sales data
forecaster.plot_input_data()

# Forecast with tech sensitivity (PAC +3%)
forecast_with_tech = forecaster.apply_forecast(apply_tech_sensitivity=True)
forecaster.save_forecast(forecast_with_tech, 'case1_forecast_with_tech_sensitivity.csv')

# Forecast without tech sensitivity
forecast_without_tech = forecaster.apply_forecast(apply_tech_sensitivity=False)
forecaster.save_forecast(forecast_without_tech, 'case1_forecast_without_tech_sensitivity.csv')

print("Forecasts generated and saved successfully!")

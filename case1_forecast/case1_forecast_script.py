import pandas as pd
import math
import matplotlib.pyplot as plt

class SupermanPlusForecast:
    def __init__(self):
        # Input raw data
        self.princess_plus = {
            'Week': ['OctWk4', 'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 
                     'DecWk1', 'DecWk2', 'DecWk3', 'DecWk4', 'JanWk1', 'JanWk2', 
                     'JanWk3', 'JanWk4', 'JanWk5'],
            'AMR': [240, 170, 130, 90, 110, 130, 110, 110, 110, 130, 70, 90, 100, 80, 90],
            'Europe': [100, 80, 90, 80, 70, 60, 60, 60, 50, 50, 50, 80, 80, 60, 50],
            'PAC': [150, 220, 240, 150, 130, 120, 110, 100, 110, 100, 120, 130, 160, 120, 100]
        }

        self.dwarf_plus = {
            'Week': ['SepWk3', 'SepWk4', 'OctWk1', 'OctWk2', 'OctWk3', 'OctWk4',
                     'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1',
                     'DecWk2', 'DecWk3', 'DecWk4'],
            'AMR': [320, 220, 170, 190, 200, 170, 160, 160, 140, 140, 180, 160, 160, 170, 190],
            'Europe': [80, 100, 60, 100, 100, 90, 80, 80, 80, 70, 90, 80, 80, 80, 70],
            'PAC': [230, 210, 140, 140, 140, 150, 140, 175, 140, 90, 90, 100, 110, 100, 90]
        }

        self.price_dwarf = 120
        self.price_princess = 200
        self.price_new = 205

    def calculate_pe_ratios(self):
        df_princess = pd.DataFrame(self.princess_plus)
        df_dwarf = pd.DataFrame(self.dwarf_plus)

        price_change_pct = (self.price_princess - self.price_dwarf) / self.price_dwarf

        pe_ratios = {}
        for region in ['AMR', 'Europe', 'PAC']:
            demand_dwarf = df_dwarf[region].sum()
            demand_princess = df_princess[region].sum()
            demand_change_pct = (demand_princess - demand_dwarf) / demand_dwarf
            pe_ratios[region] = demand_change_pct / price_change_pct

        return pe_ratios

    def build_forecast(self, pe_ratios):
        df_princess = pd.DataFrame(self.princess_plus)

        weeks = ['SepWk3', 'SepWk4', 'OctWk1', 'OctWk2', 'OctWk3', 'OctWk4',
                 'OctWk5', 'NovWk1', 'NovWk2', 'NovWk3', 'NovWk4', 'DecWk1',
                 'DecWk2', 'DecWk3', 'DecWk4']

        seasonality_factor = []
        for week in weeks:
            if week in ['SepWk3', 'SepWk4']:
                seasonality_factor.append(1.25)
            elif week in ['OctWk1', 'OctWk2']:
                seasonality_factor.append(1.15)
            else:
                seasonality_factor.append(1.0)

        price_increase_pct = (self.price_new - self.price_princess) / self.price_princess

        pe_adjustment_multiplier = {region: 1 + (pe_ratios[region] * price_increase_pct) for region in ['AMR', 'Europe', 'PAC']}

        forecast = {'Week': [], 'AMR': [], 'Europe': [], 'PAC': []}

        for i in range(15):
            forecast['Week'].append(weeks[i])
            for region in ['AMR', 'Europe', 'PAC']:
                base_value = df_princess.loc[i, region]
                value = base_value * seasonality_factor[i] * pe_adjustment_multiplier[region]
                forecast[region].append(round(value))

        forecast_df = pd.DataFrame(forecast)
        return forecast_df

    def visualize_inputs(self):
        print("Princess Plus Historical Sales:")
        print(pd.DataFrame(self.princess_plus))
        print("\nDwarf Plus Historical Sales:")
        print(pd.DataFrame(self.dwarf_plus))

    def visualize_forecast(self, forecast_df):
        print("\nSuperman Plus Forecast Table:\n")
        print(forecast_df)

        forecast_df.plot(x='Week', y=['AMR', 'Europe', 'PAC'], kind='line', marker='o')
        plt.title('Superman Plus Forecast by Region')
        plt.xlabel('Week')
        plt.ylabel('Units Forecasted')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_forecast(self, forecast_df, filename='case1_forecast.csv'):
        forecast_df.to_csv(filename, index=False)

if __name__ == "__main__":
    forecast_engine = SupermanPlusForecast()
    forecast_engine.visualize_inputs()
    pe_ratios = forecast_engine.calculate_pe_ratios()
    forecast_df = forecast_engine.build_forecast(pe_ratios)
    forecast_engine.visualize_forecast(forecast_df)
    forecast_engine.save_forecast(forecast_df)
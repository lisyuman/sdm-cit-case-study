import pandas as pd
import math
import matplotlib.pyplot as plt

class AllocationEngine:
    def __init__(self):
        # input data
        self.material_supply = {
            'Jan_Wk2': 230,
            'Jan_Wk3': 270,
            'Jan_Wk4': 320,
            'Jan_Wk5': 380
        }

        self.wk1_actual_build = {
            'Superman': 70,
            'Superman_Plus': 70,
            'Superman_Mini': 60
        }

        self.demand_fct = {
            'Jan_Wk2': {'Superman': 85, 'Superman_Plus': 85, 'Superman_Mini': 40},
            'Jan_Wk3': {'Superman': 100, 'Superman_Plus': 120, 'Superman_Mini': 60},
            'Jan_Wk4': {'Superman': 110, 'Superman_Plus': 150, 'Superman_Mini': 70},
            'Jan_Wk5': {'Superman': 120, 'Superman_Plus': 175, 'Superman_Mini': 75}
        }

        self.superman_plus_demand = {
            'Jan_Wk2': {'Online_Store': 20, 'Retail_Store': 15, 'Reseller_Partners': 50, 'PAC': 25, 'AMR': 20, 'Europe': 5},
            'Jan_Wk3': {'Online_Store': 30, 'Retail_Store': 25, 'Reseller_Partners': 65, 'PAC': 30, 'AMR': 25, 'Europe': 10},
            'Jan_Wk4': {'Online_Store': 40, 'Retail_Store': 30, 'Reseller_Partners': 80, 'PAC': 35, 'AMR': 30, 'Europe': 15},
            'Jan_Wk5': {'Online_Store': 50, 'Retail_Store': 35, 'Reseller_Partners': 90, 'PAC': 40, 'AMR': 35, 'Europe': 15}
        }

        self.final_allocation = {}

    def visualize_inputs(self):
        print("Table 1: Material Cumulative Supply")
        supply_df = pd.DataFrame(list(self.material_supply.items()), columns=['Week', 'Cumulative_Supply'])
        print(supply_df)

        print("\nTable 2: Wk1 Actual Build")
        build_df = pd.DataFrame.from_dict(self.wk1_actual_build, orient='index', columns=['Units_Built'])
        print(build_df)

        print("\nTable 3: Demand Forecast (Cumulative)")
        demand_df = pd.DataFrame(self.demand_fct).T
        print(demand_df)

        print("\nTable 4: Superman Plus Channel Demand (Cumulative)")
        plus_demand_df = pd.DataFrame(self.superman_plus_demand).T
        print(plus_demand_df)

    def allocate_material(self):
        available_material = self.material_supply['Jan_Wk4'] - sum(self.wk1_actual_build.values())

        # Step 1: Protect PAC Reseller Partner
        pac_reseller_allocation = min(self.superman_plus_demand['Jan_Wk4']['PAC'], available_material)
        remaining_material = available_material - pac_reseller_allocation

        # Step 2: Prioritize Superman and Superman Mini
        superman_demand = self.demand_fct['Jan_Wk4']['Superman']
        superman_mini_demand = self.demand_fct['Jan_Wk4']['Superman_Mini']

        total_priority_demand = superman_demand + superman_mini_demand

        superman_ratio = superman_demand / total_priority_demand
        superman_mini_ratio = superman_mini_demand / total_priority_demand

        superman_alloc = math.ceil(remaining_material * superman_ratio)
        superman_mini_alloc = math.ceil(remaining_material * superman_mini_ratio)

        total_allocated = superman_alloc + superman_mini_alloc
        surplus_material = 0

        if total_allocated > remaining_material:
            surplus_material = total_allocated - remaining_material
            if superman_mini_alloc >= surplus_material:
                superman_mini_alloc -= surplus_material
            else:
                superman_alloc -= (surplus_material - superman_mini_alloc)
                superman_mini_alloc = 0

        # Step 3: No surplus for Superman Plus channels in this setup
        online_alloc = 0
        retail_alloc = 0
        amr_alloc = 0
        europe_alloc = 0

        self.final_allocation = {
            'PAC_Reseller': pac_reseller_allocation,
            'Superman': superman_alloc,
            'Superman_Mini': superman_mini_alloc,
            'Superman_Plus_Online_Store': online_alloc,
            'Superman_Plus_Retail_Store': retail_alloc,
            'Superman_Plus_Reseller_AMR': amr_alloc,
            'Superman_Plus_Reseller_Europe': europe_alloc
        }

    def visualize_output(self):
        print("\nFinal Allocation at Jan Wk4:")
        df_output = pd.DataFrame(list(self.final_allocation.items()), columns=['Channel', 'Allocated_Units'])
        print(df_output)

        df_output.plot(x='Channel', y='Allocated_Units', kind='bar', legend=False)
        plt.title('Final Allocation Result')
        plt.ylabel('Units')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def save_output(self, filename='case2_allocation.csv'):
        df = pd.DataFrame(list(self.final_allocation.items()), columns=['Channel', 'Allocated_Units'])
        df.to_csv(filename, index=False)

if __name__ == "__main__":
    engine = AllocationEngine()
    engine.visualize_inputs()
    engine.allocate_material()
    engine.visualize_output()
    engine.save_output()

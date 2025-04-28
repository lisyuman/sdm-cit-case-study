import pandas as pd
import math

# Step 1: Input Raw Data
material_supply = 320
wk1_actual_build = {
    'Superman': 70,
    'Superman_Plus': 70,
    'Superman_Mini': 60
}

demand_fct = {
    'Superman': 110,
    'Superman_Plus': 150,
    'Superman_Mini': 70
}

superman_plus_demand = {
    'Online_Store': 40,
    'Retail_Store': 30,
    'Reseller_Partners_Total': 80, # PAC + AMR + Europe
    'PAC_Reseller': 35,
    'AMR_Reseller': 30,
    'Europe_Reseller': 15
}

# Step 2: Calculate Available Material A
available_material = material_supply - sum(wk1_actual_build.values())

# Step 3: Protect PAC Reseller Partner
pac_reseller_allocation = min(superman_plus_demand['PAC_Reseller'], available_material)
remaining_material = available_material - pac_reseller_allocation

# Step 4: Proportional Allocation to Superman and Mini
remaining_program_demand = {
    'Superman': demand_fct['Superman'],
    'Superman_Mini': demand_fct['Superman_Mini'],
    'Superman_Plus_Others': (superman_plus_demand['Online_Store'] +
                              superman_plus_demand['Retail_Store'] +
                              superman_plus_demand['AMR_Reseller'] +
                              superman_plus_demand['Europe_Reseller'])
}

total_remaining_demand = sum(remaining_program_demand.values())

# Initial allocation before rounding
initial_allocations = {}
for key, demand in remaining_program_demand.items():
    proportion = demand / total_remaining_demand
    allocated_units = remaining_material * proportion
    initial_allocations[key] = math.ceil(allocated_units)

# Step 5: Adjust if Over-Allocation
total_allocated_units = sum(initial_allocations.values())
while total_allocated_units > remaining_material:
    # Reduce from Superman_Plus_Others first, then Superman_Mini, then Superman
    for key in ['Superman_Plus_Others', 'Superman_Mini', 'Superman']:
        if initial_allocations[key] > 0:
            initial_allocations[key] -= 1
            break
    total_allocated_units = sum(initial_allocations.values())

# Step 6: Further split Superman Plus Others
plus_total_allocated = initial_allocations['Superman_Plus_Others']

# Channel ratio calculation
total_plus_channels = (superman_plus_demand['Online_Store'] +
                        superman_plus_demand['Retail_Store'] +
                        superman_plus_demand['AMR_Reseller'] +
                        superman_plus_demand['Europe_Reseller'])

online_ratio = superman_plus_demand['Online_Store'] / total_plus_channels
retail_ratio = superman_plus_demand['Retail_Store'] / total_plus_channels
reseller_ratio = (superman_plus_demand['AMR_Reseller'] + superman_plus_demand['Europe_Reseller']) / total_plus_channels

# Initial channel allocations
online_alloc = math.ceil(plus_total_allocated * online_ratio)
retail_alloc = math.ceil(plus_total_allocated * retail_ratio)
reseller_total_alloc = math.ceil(plus_total_allocated * reseller_ratio)

# Adjust channels if over-allocated
allocations = {
    'reseller_total_alloc': reseller_total_alloc,
    'retail_alloc': retail_alloc,
    'online_alloc': online_alloc
}

channel_total = sum(allocations.values())

while channel_total > plus_total_allocated:
    for key in ['reseller_total_alloc', 'retail_alloc', 'online_alloc']:
        if allocations[key] > 0:
            allocations[key] -= 1
            break
    channel_total = sum(allocations.values())

# Update individual allocations
reseller_total_alloc = allocations['reseller_total_alloc']
retail_alloc = allocations['retail_alloc']
online_alloc = allocations['online_alloc']

# Step 7: Further split Reseller Partners into AMR and Europe (2:1)
amr_alloc = math.floor(reseller_total_alloc * (2/3))
europe_alloc = reseller_total_alloc - amr_alloc

# Step 8: Final Output
final_allocation = {
    'PAC_Reseller': pac_reseller_allocation,
    'Superman': initial_allocations['Superman'],
    'Superman_Mini': initial_allocations['Superman_Mini'],
    'Superman_Plus_Online_Store': online_alloc,
    'Superman_Plus_Retail_Store': retail_alloc,
    'Superman_Plus_Reseller_AMR': amr_alloc,
    'Superman_Plus_Reseller_Europe': europe_alloc
}

# Output
print("Final Allocation at Jan Wk4:")
for key, value in final_allocation.items():
    print(f"{key}: {value} units")

# Save to CSV
df = pd.DataFrame(list(final_allocation.items()), columns=['Channel', 'Allocated_Units'])
df.to_csv('case2_final_allocation_refined.csv', index=False)
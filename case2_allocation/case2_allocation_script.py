from gurobipy import Model, GRB

# ---------- DATA ---------- #
weeks = ["wk2", "wk3", "wk4", "wk5"]
products = ["Superman", "SupermanPlus", "SupermanMini"]
channels = ["Online", "Retail", "Reseller"]
reseller_regions = ["AMR", "Europe", "PAC"]

# Initial total supply budget
initial_weekly_supply = {"wk2": 230, "wk3": 270, "wk4": 320, "wk5": 380}

# Demand forecast per product per week (cumulative)
cumulative_demand = {
    "Superman": [85, 100, 110, 120],
    "SupermanPlus": [85, 120, 150, 175],
    "SupermanMini": [40, 60, 70, 75]
}

# Incremental demand per week (for WOS)
incremental_demand = {
    "Superman":  [0, 15, 10, 10],
    "SupermanPlus": [0, 35, 30, 25],
    "SupermanMini": [0, 20, 10, 5]
}

# Channel demand for Superman Plus
channel_demand = {
    "Online":   [20, 30, 40, 50],
    "Retail":   [15, 25, 30, 35],
    "Reseller": [50, 65, 80, 90]
}

# Reseller region demand
reseller_demand = {
    "AMR":   [20, 25, 30, 35],
    "Europe": [5, 10, 15, 15],
    "PAC":    [25, 30, 35, 40]
}

# ---------- MODEL ---------- #
model = Model("ProductAllocation")
model.setParam('OutputFlag', 0)  # Silent solve

# Decision variables (integer)
alloc = {(p, w): model.addVar(vtype=GRB.INTEGER, name=f"alloc_{p}_{w}") for p in products for w in weeks}

# Slack for SupermanPlus soft demand constraint
slack = {w: model.addVar(lb=0, name=f"slack_SP_{w}") for w in weeks}

# Demand constraints
for i, w in enumerate(weeks):
    model.addConstr(alloc["Superman", w] >= cumulative_demand["Superman"][i], name=f"demand_S_{w}")
    model.addConstr(alloc["SupermanMini", w] >= cumulative_demand["SupermanMini"][i], name=f"demand_SM_{w}")
    model.addConstr(alloc["SupermanPlus", w] + slack[w] >= cumulative_demand["SupermanPlus"][i], name=f"demand_SP_soft_{w}")

# Total supply must be fully used
model.addConstr(sum(alloc[p, w] for p in products for w in weeks) == sum(initial_weekly_supply.values()), name="TotalSupply")

# Cumulative actual build = allocation + base buffer
base_build = {"Superman": 70, "SupermanPlus": 70, "SupermanMini": 60}

# WOS constraint (strict, WOS >= 4)
for p in products:
    for i in range(0, 4):  # wk3, wk4, wk5 (i=1,2,3)
        cum_build = sum(alloc[p, weeks[j]] for j in range(i+1)) + base_build[p]
        cum_demand = cumulative_demand[p][i]
        end_on_hand = cum_build - cum_demand
        avg_future_demand = incremental_demand[p][i] if i < 3 else incremental_demand[p][2]
        model.addConstr(end_on_hand >= 4 * avg_future_demand, name=f"WOS_ge4_{p}_{weeks[i]}")

# Objective: maximize use of supply with minimum slack penalty
model.setObjective(sum(alloc[p, w] for p in products for w in weeks) - 10 * sum(slack[w] for w in weeks), GRB.MAXIMIZE)

model.optimize()

if model.Status != GRB.OPTIMAL:
    print("Model infeasible or unbounded")
    model.computeIIS()
    model.write("infeasible.ilp")
    exit()

product_alloc = {p: {w: int(alloc[p, w].X) for w in weeks} for p in products}
superman_plus_alloc = {w: product_alloc["SupermanPlus"][w] for w in weeks}

# ---------- CHANNEL ALLOCATION MODEL ---------- #
model2 = Model("ChannelAllocation")
model2.setParam('OutputFlag', 0)

channel_alloc = {}
channel_dev = {}
for c in channels:
    for w in weeks:
        channel_alloc[c, w] = model2.addVar(lb=0, name=f"{c}_{w}")
        channel_dev[c, w] = model2.addVar(lb=0, name=f"dev_{c}_{w}")
        i = weeks.index(w)
        model2.addConstr(channel_alloc[c, w] - channel_demand[c][i] <= channel_dev[c, w])
        model2.addConstr(channel_demand[c][i] - channel_alloc[c, w] <= channel_dev[c, w])

for w in weeks:
    model2.addConstr(sum(channel_alloc[c, w] for c in channels) == superman_plus_alloc[w], name=f"channel_match_{w}")
    model2.addConstr(channel_alloc["Online", w] >= channel_alloc["Retail", w], name=f"prio_online_{w}")
    model2.addConstr(channel_alloc["Retail", w] >= channel_alloc["Reseller", w], name=f"prio_retail_{w}")

model2.setObjective(sum(channel_dev[c, w] for c in channels for w in weeks), GRB.MINIMIZE)
model2.optimize()

channel_output = {c: {w: channel_alloc[c, w].X for w in weeks} for c in channels}

# ---------- REGION-LEVEL RESELLER ALLOCATION ---------- #
model3 = Model("ResellerRegionAllocation")
model3.setParam('OutputFlag', 0)

reseller_alloc = {}
reseller_dev = {}
for r in reseller_regions:
    for w in weeks:
        reseller_alloc[r, w] = model3.addVar(lb=0, name=f"{r}_{w}")
        reseller_dev[r, w] = model3.addVar(lb=0, name=f"dev_{r}_{w}")
        i = weeks.index(w)
        model3.addConstr(reseller_alloc[r, w] - reseller_demand[r][i] <= reseller_dev[r, w])
        model3.addConstr(reseller_demand[r][i] - reseller_alloc[r, w] <= reseller_dev[r, w])

for w in weeks:
    model3.addConstr(sum(reseller_alloc[r, w] for r in reseller_regions) == channel_output["Reseller"][w], name=f"reseller_match_{w}")

model3.setObjective(sum(reseller_dev[r, w] for r in reseller_regions for w in weeks), GRB.MINIMIZE)
model3.optimize()

# ---------- PRINT RESULTS ---------- #
print("\n🎯 FINAL PRODUCT ALLOCATION PER WEEK:")
for p in products:
    print(f"\n{p}:")
    for w in weeks:
        print(f"  {w}: {product_alloc[p][w]}")

print("\n🧩 SUPERMAN PLUS CHANNEL ALLOCATION:")
for c in channels:
    print(f"\n{c}:")
    for w in weeks:
        print(f"  {w}: {channel_output[c][w]:.1f}")

print("\n🌍 SUPERMAN PLUS RESELLER REGION ALLOCATION:")
for r in reseller_regions:
    print(f"\n{r}:")
    for w in weeks:
        print(f"  {w}: {reseller_alloc[r, w].X:.1f}")

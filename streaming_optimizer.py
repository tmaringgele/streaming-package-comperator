import pulp
from datetime import datetime, timedelta


# Example Input Data
packages = ["P1", "P2"]
games = ["G1", "G2", "G3", "G4", "G5", 'G6', 'G7']
game_dates = {
    "G1": datetime(2023, 1, 15),
    "G2": datetime(2023, 2, 20),
    "G3": datetime(2023, 3, 25),
    "G4": datetime(2023, 4, 10),
    "G5": datetime(2023, 4, 20),
    "G6": datetime(2024, 1, 10),
    "G7": datetime(2024, 3, 15),
}
C_month = {'P1': 30, 'P2': 20}
C_year = {'P2': 180}
P_g = {'G1': ['P1'], 'G2': ['P1'], 'G3': ['P1', 'P2'], 'G4': ['P1', 'P2'], 'G5': ['P1', 'P2'],
    'G6': ['P1'], 'G7': ['P1', 'P2']}

# Filter out unavailable subscriptions
filtered_C_month = {p: C_month[p] for p in C_month if p in packages}
filtered_C_year = {p: C_year[p] for p in C_year if p in packages}

# Generate possible start dates for rolling subscriptions
start_dates = sorted(set(game_dates.values()))

# Compute coverage windows for rolling monthly and yearly subscriptions
coverage_month = {d: [g for g, gd in game_dates.items() if d <= gd <= d + timedelta(days=30)] for d in start_dates}
coverage_year = {d: [g for g, gd in game_dates.items() if d <= gd <= d + timedelta(days=365)] for d in start_dates}

# Model
model = pulp.LpProblem("Streaming_Package_Optimization", pulp.LpMinimize)

# Decision variables
z_month = {(p, d): pulp.LpVariable(f"z_month_{p}_{d.strftime('%Y-%m-%d')}", cat='Binary')
        for p in filtered_C_month for d in start_dates}
z_year = {(p, d): pulp.LpVariable(f"z_year_{p}_{d.strftime('%Y-%m-%d')}", cat='Binary')
        for p in filtered_C_year for d in start_dates}

# Objective function: Minimize total cost
model += pulp.lpSum(filtered_C_month[p] * z_month[p, d] for p in filtered_C_month for d in start_dates) + \
            pulp.lpSum(filtered_C_year[p] * z_year[p, d] for p in filtered_C_year for d in start_dates)

# Constraints
# 1. Game coverage
for g in games:
    model += pulp.lpSum(z_month[p, d] for p in P_g[g] if p in filtered_C_month for d in start_dates if g in coverage_month[d]) + \
            pulp.lpSum(z_year[p, d] for p in P_g[g] if p in filtered_C_year for d in start_dates if g in coverage_year[d]) >= 1

# Solve the model
status = model.solve(pulp.PULP_CBC_CMD())

# Process results
results = {
    "status": pulp.LpStatus[status],
    "total_cost": pulp.value(model.objective),
    "active_monthly_subscriptions": [],
    "active_yearly_subscriptions": []
}

for p in filtered_C_month:
    for d in start_dates:
        if z_month[p, d].varValue > 0:
            results["active_monthly_subscriptions"].append({"package": p, "start_date": d})
for p in filtered_C_year:
    for d in start_dates:
        if z_year[p, d].varValue > 0:
            results["active_yearly_subscriptions"].append({"package": p, "start_date": d})



# Print results
print("Status:", results["status"])
print("Total Cost:", results["total_cost"])
print("Active Monthly Subscriptions:")
for sub in results["active_monthly_subscriptions"]:
    print(f"  Package: {sub['package']}, Start Date: {sub['start_date'].strftime('%Y-%m-%d')}")
print("Active Yearly Subscriptions:")
for sub in results["active_yearly_subscriptions"]:
    print(f"  Package: {sub['package']}, Start Date: {sub['start_date'].strftime('%Y-%m-%d')}")

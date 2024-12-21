import pulp
from datetime import datetime, timedelta


def optimize_streaming_packages(packages, games, game_dates, C_month, C_year, P_g):
    """
    Optimizes the streaming package selection with rolling monthly and yearly subscriptions.

    Parameters:
        packages (list): List of package IDs.
        games (list): List of game IDs.
        game_dates (dict): Dictionary mapping game IDs to datetime objects of their start dates.
        C_month (dict): Dictionary of monthly subscription costs for each package.
        C_year (dict): Dictionary of yearly subscription costs for each package.
        P_g (dict): Dictionary mapping game IDs to a list of packages that can cover each game.

    Returns:
        dict: Optimization results, including total cost and active subscriptions.
    """
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

    return results




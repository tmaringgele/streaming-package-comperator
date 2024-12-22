import pulp
import pandas as pd
from datetime import datetime, timedelta


def preprocess_data(game_ids_of_interest, streaming_offers_raw, streaming_packages_raw, games_raw):

    ## Preprocess data (make everthing as small as possible)

    ### Filter packages to include only relevant ones
    # Identify relevant package IDs from offers
    relevant_package_ids = streaming_offers_raw[streaming_offers_raw['game_id'].isin(game_ids_of_interest)]['streaming_package_id'].unique()

    # Filter packages to include only relevant ones
    filtered_packages = streaming_packages_raw[streaming_packages_raw['id'].isin(relevant_package_ids)]

    filtered_packages['yearly_price'] = filtered_packages['monthly_price_yearly_subscription_in_cents'] * 12
    filtered_packages = filtered_packages.drop(columns=['monthly_price_yearly_subscription_in_cents'])


    games = games_raw[games_raw['id'].isin(game_ids_of_interest)]

    # Filter offers to include only the games of interest
    filtered_offers = streaming_offers_raw[streaming_offers_raw['game_id'].isin(game_ids_of_interest)]


    # Extract unique package IDs
    packages = filtered_packages['id'].unique().tolist()

    # Create game_dates dictionary
    games.loc[:, 'starts_at'] = pd.to_datetime(games['starts_at'])
    game_dates = games.set_index('id')['starts_at'].apply(lambda x: x.date()).to_dict()


    # Create C_month and C_year dictionaries, dropping packages with NA for the respective type
    C_month = filtered_packages.dropna(subset=['monthly_price_cents']) \
        .set_index('id')['monthly_price_cents'].to_dict()
    C_year = filtered_packages.dropna(subset=['yearly_price']) \
        .set_index('id')['yearly_price'].to_dict()


    # Create P_g dictionary
    P_g = filtered_offers.groupby('game_id')['streaming_package_id'].apply(list).to_dict()


    ## Remove all games with no offer
    games_with_no_offers = []
    for game_id in game_ids_of_interest:
        if game_id not in P_g:
            games_with_no_offers.append(game_id)

    game_ids_of_interest = [game_id for game_id in game_ids_of_interest if game_id in P_g]

    result = {
        "packages": packages,
        "games": game_ids_of_interest,
        "game_dates": game_dates,
        "C_month": C_month,
        "C_year": C_year,
        "P_g": P_g,
        'games_with_no_offers': games_with_no_offers
    }

    return result


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
            if z_month[p, d].varValue is not None and z_month[p, d].varValue > 0:
                results["active_monthly_subscriptions"].append({"package": p, "start_date": d})
    for p in filtered_C_year:
        for d in start_dates:
            if z_year[p, d].varValue is not None and z_year[p, d].varValue > 0:
                results["active_yearly_subscriptions"].append({"package": p, "start_date": d})

    return results




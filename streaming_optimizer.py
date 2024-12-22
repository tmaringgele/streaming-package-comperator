import pulp
import pandas as pd
from datetime import datetime, timedelta

def print_solver_results(results):
    """
    Prints the results of the streaming package optimization in a readable format.

    Parameters:
        results (dict): A dictionary containing the optimization results. Expected keys are:
            - "status" (str): Solver status (e.g., "Optimal", "Infeasible").
            - "total_cost" (float): Total cost of the selected subscriptions.
            - "active_monthly_subscriptions" (list): List of dictionaries with "package" and "start_date" for monthly subscriptions.
            - "active_yearly_subscriptions" (list): List of dictionaries with "package" and "start_date" for yearly subscriptions.
            - Any additional keys from the optimization output.

    Returns:
        None: Prints the formatted results to the console.
    """
    if results is not None:
        # Print solver status
        print("Solver Status:", results["status"])

        # Print total cost of the solution
        print("Total Cost of Selected Subscriptions:", results["total_cost"])

        # Print details of active monthly subscriptions
        print("\nActive Monthly Subscriptions:")
        if results["active_monthly_subscriptions"]:
            for sub in results["active_monthly_subscriptions"]:
                print(f"  Package: {sub['package']}, Start Date: {sub['start_date'].strftime('%Y-%m-%d')}")
        else:
            print("  No active monthly subscriptions.")

        # Print details of active yearly subscriptions
        print("\nActive Yearly Subscriptions:")
        if results["active_yearly_subscriptions"]:
            for sub in results["active_yearly_subscriptions"]:
                print(f"  Package: {sub['package']}, Start Date: {sub['start_date'].strftime('%Y-%m-%d')}")
        else:
            print("  No active yearly subscriptions.")
    else:
        # Handle case where no results are returned
        print("No results returned from the optimization function.")

def preprocess_data(game_ids_of_interest, streaming_offers_raw, streaming_packages_raw, games_raw):
    """
    Preprocesses raw streaming and game data to generate optimized inputs for a solver function.

    Parameters:
        game_ids_of_interest (list): List of game IDs to focus on.
        streaming_offers_raw (pd.DataFrame): Dataframe containing information on which streaming services offer which games.
        streaming_packages_raw (pd.DataFrame): Dataframe containing streaming package pricing and details.
        games_raw (pd.DataFrame): Dataframe containing information about games, including start times.

    Returns:
        dict: A dictionary containing:
            - "packages" (list): List of relevant streaming package IDs.
            - "games" (list): List of game IDs with at least one streaming offer.
            - "game_dates" (dict): Dictionary mapping game IDs to their start dates (as `date` objects).
            - "C_month" (dict): Dictionary mapping package IDs to monthly prices (in cents).
            - "C_year" (dict): Dictionary mapping package IDs to yearly prices (12 * monthly yearly subscription price in cents).
            - "P_g" (dict): Dictionary mapping game IDs to the list of streaming package IDs that cover them.
            - "games_with_no_offers" (list): List of game IDs that have no streaming offers.
    """

    ## Preprocess data (minimize the size of data for optimization)

    ### Step 1: Filter relevant packages
    # Identify package IDs that are relevant based on the offers for the selected games
    relevant_package_ids = streaming_offers_raw[streaming_offers_raw['game_id'].isin(game_ids_of_interest)]['streaming_package_id'].unique()

    # Filter streaming packages to include only those relevant to the selected games
    filtered_packages = streaming_packages_raw[streaming_packages_raw['id'].isin(relevant_package_ids)]

    # Compute yearly prices based on monthly price for yearly subscription and clean the dataframe
    filtered_packages['yearly_price'] = filtered_packages['monthly_price_yearly_subscription_in_cents'] * 12
    filtered_packages = filtered_packages.drop(columns=['monthly_price_yearly_subscription_in_cents'])

    ### Step 2: Filter relevant games and offers
    # Filter games to include only those in the list of interest
    games = games_raw[games_raw['id'].isin(game_ids_of_interest)]

    # Filter offers to include only those for the games of interest
    filtered_offers = streaming_offers_raw[streaming_offers_raw['game_id'].isin(game_ids_of_interest)]

    ### Step 3: Extract relevant data for the solver
    # Extract unique package IDs
    packages = filtered_packages['id'].unique().tolist()

    # Create game_dates dictionary mapping game IDs to start dates
    games.loc[:, 'starts_at'] = pd.to_datetime(games['starts_at'])  # Ensure dates are in datetime format
    game_dates = games.set_index('id')['starts_at'].apply(lambda x: x.date()).to_dict()

    # Create C_month dictionary: Maps package IDs to monthly prices (only for packages with a valid monthly price)
    C_month = filtered_packages.dropna(subset=['monthly_price_cents']) \
        .set_index('id')['monthly_price_cents'].to_dict()

    # Create C_year dictionary: Maps package IDs to yearly prices (only for packages with a valid yearly price)
    C_year = filtered_packages.dropna(subset=['yearly_price']) \
        .set_index('id')['yearly_price'].to_dict()

    # Create P_g dictionary: Maps game IDs to the list of streaming package IDs that can stream the game
    P_g = filtered_offers.groupby('game_id')['streaming_package_id'].apply(list).to_dict()

    ### Step 4: Remove games with no offers
    # Identify games from the input list that have no streaming offers
    games_with_no_offers = [game_id for game_id in game_ids_of_interest if game_id not in P_g]

    # Update the list of game IDs of interest to exclude those with no offers
    game_ids_of_interest = [game_id for game_id in game_ids_of_interest if game_id in P_g]

    ### Step 5: Return results
    result = {
        "packages": packages,  # List of relevant package IDs
        "games": game_ids_of_interest,  # Games with at least one streaming offer
        "game_dates": game_dates,  # Mapping of game IDs to their start dates
        "C_month": C_month,  # Monthly prices for relevant packages
        "C_year": C_year,  # Yearly prices for relevant packages
        "P_g": P_g,  # Mapping of games to the packages that can stream them
        "games_with_no_offers": games_with_no_offers  # Games with no streaming offers
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




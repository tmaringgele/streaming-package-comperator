import pandas as pd
from datetime import timedelta, datetime

def load_games():
    return pd.read_csv('data/games_cleaned.csv')

def load_freeTV():
    return pd.read_csv('data/freeTV_packages.csv')

def load_streaming_data():
    streaming_offers_raw = pd.read_csv('data/bc_streaming_offer.csv')
    streaming_packages_raw = pd.read_csv('data/bc_streaming_package.csv')
    return streaming_offers_raw, streaming_packages_raw

def add_package_coverage(filtered_games, optimization_results, streaming_offers, streaming_packages):
    """
    Adds package coverage information to the filtered games.

    Parameters:
        filtered_games (pd.DataFrame): DataFrame of filtered games.
        optimization_results (dict): Optimization results containing active subscriptions.
        streaming_offers (pd.DataFrame): DataFrame of streaming offers.

    Returns:
        tuple: A tuple containing:
            - list: List of filtered games with additional information about which packages cover the game.
            - str: Start date of the first game in the list.
            - str: End date of the last game in the list.
    """
    # Extract active subscriptions
    active_monthly_subscriptions = optimization_results.get("active_monthly_subscriptions", [])
    active_yearly_subscriptions = optimization_results.get("active_yearly_subscriptions", [])

    # Create a dictionary to map game IDs to the packages that cover them
    game_coverage = {game_id: [] for game_id in filtered_games['id'].tolist()}

    # Convert 'starts_at' to datetime if it's not already
    filtered_games['starts_at'] = pd.to_datetime(filtered_games['starts_at'])

    # Function to get live and highlights information
    def get_live_highlights(game_id, package_id, packages):
        offer = streaming_offers[(streaming_offers['game_id'] == game_id) & (streaming_offers['streaming_package_id'] == package_id)]
        if not offer.empty:
            package_info = packages[packages['id'] == package_id].iloc[0].to_dict()
            package_info.update({
                'live': offer.iloc[0]['live'].tolist(),
                'highlights': offer.iloc[0]['highlights'].tolist()
            })
            return package_info
        return None

    # Add monthly subscriptions to the coverage
    for sub in active_monthly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=30)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            coverage_info = get_live_highlights(game_id, package, streaming_packages)
            if coverage_info:
                game_coverage[game_id].append(coverage_info)

    # Add yearly subscriptions to the coverage
    for sub in active_yearly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=365)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            coverage_info = get_live_highlights(game_id, package, streaming_packages)
            if coverage_info:
                game_coverage[game_id].append(coverage_info)

    # Add coverage information to the filtered games
    filtered_games_with_coverage = filtered_games.copy()
    filtered_games_with_coverage['covered_by'] = filtered_games_with_coverage['id'].apply(lambda x: game_coverage[x])

    # Sort the filtered games by 'starts_at' in ascending order
    filtered_games_with_coverage = filtered_games_with_coverage.sort_values(by='starts_at')

    # Get start_date and end_date
    start_date = filtered_games_with_coverage['starts_at'].min().strftime('%Y-%m-%d')
    end_date = filtered_games_with_coverage['starts_at'].max().strftime('%Y-%m-%d')

    return filtered_games_with_coverage.to_dict(orient='records'), start_date, end_date

def get_subscription_details(packages_df, yearly_subscriptions, monthly_subscriptions):
    """
    Processes the subscription lists and returns detailed information.

    Parameters:
        packages_df (pd.DataFrame): DataFrame containing all package information.
        yearly_subscriptions (list): List of yearly subscription dictionaries.
        monthly_subscriptions (list): List of monthly subscription dictionaries.

    Returns:
        tuple: A tuple containing:
            - list: List of subscription details ordered by start_date.
            - int: Sum of all prices in the list.
    """
    subscription_details = []

    # Process yearly subscriptions
    for sub in yearly_subscriptions:
        package_id = sub["package"]
        start_date = pd.to_datetime(sub["start_date"])
        package_row = packages_df[packages_df["id"] == package_id].iloc[0].to_dict()
        price = package_row["monthly_price_yearly_subscription_in_cents"]
        subscription_details.append({
            "package": package_row,
            "start_date": start_date,
            "yearly": 1,
            "price": price
        })

    # Process monthly subscriptions
    for sub in monthly_subscriptions:
        package_id = sub["package"]
        start_date = pd.to_datetime(sub["start_date"])
        package_row = packages_df[packages_df["id"] == package_id].iloc[0].to_dict()
        price = package_row["monthly_price_cents"]
        subscription_details.append({
            "package": package_row,
            "start_date": start_date,
            "yearly": 0,
            "price": price
        })

    # Sort the list by start_date
    subscription_details.sort(key=lambda x: x["start_date"])

    # Calculate the sum of all prices
    total_price = sum(item["price"] for item in subscription_details)

    return subscription_details, total_price
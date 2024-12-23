import pandas as pd
from datetime import timedelta, datetime

def load_games():
    return pd.read_csv('data/bc_game.csv')

def load_freeTV():
    return pd.read_csv('data/freeTV_packages.csv')

def load_streaming_data():
    streaming_offers_raw = pd.read_csv('data/bc_streaming_offer.csv')
    streaming_packages_raw = pd.read_csv('data/bc_streaming_package.csv')
    return streaming_offers_raw, streaming_packages_raw

def add_package_coverage(filtered_games, optimization_results):
    """
    Adds package coverage information to the filtered games.

    Parameters:
        filtered_games (pd.DataFrame): DataFrame of filtered games.
        optimization_results (dict): Optimization results containing active subscriptions.

    Returns:
        list: List of filtered games with additional information about which packages cover the game.
    """
    # Extract active subscriptions
    active_monthly_subscriptions = optimization_results.get("active_monthly_subscriptions", [])
    active_yearly_subscriptions = optimization_results.get("active_yearly_subscriptions", [])

    # Create a dictionary to map game IDs to the packages that cover them
    game_coverage = {game_id: [] for game_id in filtered_games['id'].tolist()}

    # Convert 'starts_at' to datetime if it's not already
    filtered_games['starts_at'] = pd.to_datetime(filtered_games['starts_at'])

    # Add monthly subscriptions to the coverage
    for sub in active_monthly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=30)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            game_coverage[game_id].append(package)

    # Add yearly subscriptions to the coverage
    for sub in active_yearly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=365)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            game_coverage[game_id].append(package)

    # Add coverage information to the filtered games
    filtered_games_with_coverage = filtered_games.copy()
    filtered_games_with_coverage['covered_by'] = filtered_games_with_coverage['id'].apply(lambda x: game_coverage[x])

    return filtered_games_with_coverage.to_dict(orient='records')
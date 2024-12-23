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

def add_package_coverage(filtered_games, optimization_results, streaming_offers):
    """
    Adds package coverage information to the filtered games.

    Parameters:
        filtered_games (pd.DataFrame): DataFrame of filtered games.
        optimization_results (dict): Optimization results containing active subscriptions.
        streaming_offers (pd.DataFrame): DataFrame of streaming offers.

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

    # Function to get live and highlights information
    def get_live_highlights(game_id, package_id):
        offer = streaming_offers[(streaming_offers['game_id'] == game_id) & (streaming_offers['streaming_package_id'] == package_id)]
        if not offer.empty:
            return {
                'package_id': package_id,
                'live': offer.iloc[0]['live'].tolist(),
                'highlights': offer.iloc[0]['highlights'].tolist()
            }
        return None

    # Add monthly subscriptions to the coverage
    for sub in active_monthly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=30)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            coverage_info = get_live_highlights(game_id, package)
            if coverage_info:
                game_coverage[game_id].append(coverage_info)

    # Add yearly subscriptions to the coverage
    for sub in active_yearly_subscriptions:
        package = sub['package']
        start_date = pd.to_datetime(sub['start_date'])
        end_date = start_date + timedelta(days=365)
        covered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & (filtered_games['starts_at'] <= end_date)]
        for game_id in covered_games['id'].tolist():
            coverage_info = get_live_highlights(game_id, package)
            if coverage_info:
                game_coverage[game_id].append(coverage_info)

    # Add coverage information to the filtered games
    filtered_games_with_coverage = filtered_games.copy()
    filtered_games_with_coverage['covered_by'] = filtered_games_with_coverage['id'].apply(lambda x: game_coverage[x])

    # Sort the filtered games by 'starts_at' in ascending order
    filtered_games_with_coverage = filtered_games_with_coverage.sort_values(by='starts_at')

    return filtered_games_with_coverage.to_dict(orient='records')
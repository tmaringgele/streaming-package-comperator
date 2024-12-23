from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from service import load_games, load_streaming_data, add_package_coverage, get_subscription_details
from streaming_optimizer import preprocess_data, optimize_streaming_packages

app = Flask(__name__)
CORS(app)

# Load the games data
games_df = load_games()

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/getGames", methods=["GET"])
def get_games():
    name = request.args.get('name')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_games = games_df
    
    if name:
        filtered_games = filtered_games[(filtered_games['team_home'].str.contains(name, case=False)) | 
                                        (filtered_games['team_away'].str.contains(name, case=False))]
    
    if start_date and end_date:
        filtered_games = filtered_games[(filtered_games['starts_at'] >= start_date) & 
                                        (filtered_games['starts_at'] <= end_date)]
    
    return jsonify(filtered_games.to_dict(orient='records'))

@app.route("/optimizePackages", methods=["POST"])
def optimize_packages():
    data = request.json
    clubs = data.get('clubs', [])
    timespan = data.get('timespan', {})
    live_value = data.get('live_value', 0) / 100
    highlight_value = data.get('highlight_value', 0) / 100

    start_date = timespan.get('start_date')
    end_date = timespan.get('end_date')

    # Filter games based on the provided clubs and timespan
    filtered_games = games_df[
        ((games_df['team_home'].isin(clubs)) | (games_df['team_away'].isin(clubs)))
    ]

    if start_date:
        filtered_games = filtered_games[filtered_games['starts_at'] >= start_date]
    if end_date:
        filtered_games = filtered_games[filtered_games['starts_at'] <= end_date]

    game_ids_of_interest = filtered_games['id'].tolist()

    # Load streaming offers and packages data
    streaming_offers_raw, streaming_packages_raw = load_streaming_data()

    # Preprocess data
    preprocessed_data = preprocess_data(
        game_ids_of_interest, streaming_offers_raw, streaming_packages_raw, games_df, 0, 0)

    print("C_month without live:")
    print(preprocessed_data['C_month'])
    preprocessed_data = preprocess_data(
        game_ids_of_interest, streaming_offers_raw, streaming_packages_raw, games_df, live_value, highlight_value)

    print("C_month with live:")
    print(preprocessed_data['C_month'])

    # Optimize streaming packages
    results = optimize_streaming_packages(
        preprocessed_data['packages'],
        preprocessed_data['games'],
        preprocessed_data['game_dates'],
        preprocessed_data['C_month'],
        preprocessed_data['C_year'],
        preprocessed_data['P_g']
    )

    # Add package coverage information to the filtered games
    filtered_games_with_coverage, start, end = add_package_coverage(filtered_games, results, streaming_offers_raw, streaming_packages_raw.fillna('null'))

    packages, cost = get_subscription_details(streaming_packages_raw.fillna('null'), results['active_yearly_subscriptions'], results['active_monthly_subscriptions'])
    response = {
        "solver_status": results['status'],
        "start_date": start,
        "end_date": end,
        "cost": cost,
        "packages": packages,
        "games": filtered_games_with_coverage
    }


    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
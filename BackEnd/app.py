from flask import Flask, request, jsonify
import pandas as pd
from service import load_games

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
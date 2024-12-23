import pandas as pd

def load_games():
    return pd.read_csv('data/bc_game.csv')

def load_streaming_data():
    streaming_offers_raw = pd.read_csv('data/bc_streaming_offer.csv')
    streaming_packages_raw = pd.read_csv('data/bc_streaming_package.csv')
    return streaming_offers_raw, streaming_packages_raw
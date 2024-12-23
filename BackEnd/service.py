import pandas as pd

def load_games():
    return pd.read_csv('data/bc_game.csv')

def load_freeTV():
    return pd.read_csv('data/freeTV_packages.csv')

def load_streaming_data():
    streaming_offers_raw = pd.read_csv('data/bc_streaming_offer.csv')
    streaming_packages_raw = pd.read_csv('data/bc_streaming_package.csv')
    #streaming_packages_raw['monthly_price_cents'] = streaming_packages_raw['monthly_price_cents'] + 1
    #streaming_packages_raw['monthly_price_yearly_subscription_in_cents'] = streaming_packages_raw['monthly_price_yearly_subscription_in_cents'] +1
    return streaming_offers_raw, streaming_packages_raw
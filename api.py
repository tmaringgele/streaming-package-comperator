from streaming_optimizer import optimize_streaming_packages
from datetime import datetime, timedelta

# Example Input Data
packages = ["P1", "P2"]
games = ["G1", "G2", "G3", "G4", "G5", 'G6', 'G7']
game_dates = {
    "G1": datetime(2023, 1, 15),
    "G2": datetime(2023, 2, 20),
    "G3": datetime(2023, 3, 25),
    "G4": datetime(2023, 4, 10),
    "G5": datetime(2023, 4, 20),
    "G6": datetime(2024, 1, 10),
    "G7": datetime(2024, 3, 15),
}
C_month = {'P2': 20}
C_year = {'P1': 50, 'P2': 180}
P_g = {'G1': ['P1'], 'G2': ['P1'], 'G3': ['P1', 'P2'], 'G4': ['P1', 'P2'], 'G5': ['P1', 'P2'],
    'G6': ['P1'], 'G7': ['P1', 'P2']}
optimize_streaming_packages(packages, games, game_dates, C_month, C_year, P_g)


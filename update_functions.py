import pandas as pd

def compare_date(datapath):
    league_file = 'leagues.csv'
    df = pd.read_csv(datapath / league_file, usecols=["league_id", "current_date"])
    league_date = df.iat(0,1)

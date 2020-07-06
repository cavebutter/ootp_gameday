import sqlite3
import pandas as pd
from pathlib import Path
import os
from prettytable import PrettyTable

# datafiles = input("What is the location of your data files? ")
# path = Path(datafiles)
path = Path(r'/Users/jay/Desktop/new data')

# create sqlite db

try:
    cnx = sqlite3.connect('ootp.db')
    cursor = cnx.cursor()
    print("Successfully Connected to SQLite")


except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
# Load bare minimum of tables to database
# leagues
league_df = pd.read_csv(path / 'leagues.csv',
                        usecols=['league_id', 'name', 'start_date', 'league_level', 'parent_league_id', 'current_date'])
league_df.set_index('league_id', inplace=True)
league_df.rename(columns={'current_date': 'curr_date'}, inplace=True)
league_df.to_sql('leagues', con=cnx)

# teams
teams_df = pd.read_csv(path / 'teams.csv',
                       usecols=['team_id', 'name', 'nickname', 'league_id', 'sub_league_id', 'division_id',
                                'parent_team_id', 'level'])
teams_df.set_index('team_id', inplace=True)
teams_df.to_sql('teams', con=cnx)

###############################################
# Choose league and team to further trim load #
###############################################

# league
cursor.execute("SELECT league_id, name FROM leagues WHERE parent_league_id = 0")

league_list = cursor.fetchall()

# - Make a Pretty Table to display ID and League
x = PrettyTable()
x.field_names = ['ID', 'League']
for item in league_list:
    x.add_row(item)
print(x)

league_id = input("Enter the league ID of your choice: ")

# team
cursor.execute("""SELECT team_id, name || ' ' || nickname as team
                    FROM teams
                    WHERE league_id=?""", (league_id,))
teams_list = cursor.fetchall()

# Make a Pretty Table
x = PrettyTable()
x.field_names = ['ID', 'Team']
for item in teams_list:
    x.add_row(item)
print(x)
cursor.execute("SELECT * FROM teams")
listofteams = cursor.fetchall()
#  Get org param
org_param = input("Enter the ID of the organization you want for your depth chart: ")

# Get org name
cursor.execute("SELECT name || ' ' || nickname FROM teams WHERE team_id=?", (org_param,))
result = cursor.fetchall()
team_name = result[0][0]

# Get game year for trimming csv's
cursor.execute("SELECT max(curr_date) FROM leagues")
game_date = cursor.fetchone()
game_year = int(game_date[0][0:4])

##########################################################################
# These are the foundational tables for stats and the basis for trimming #
##########################################################################

# Trim and load players career batting stats
pcbs_df = pd.read_csv(path / 'players_career_batting_stats.csv')

# filter pcbs_df and load as table
pcbs_current = pcbs_df['year'] == game_year
pcbs_current_year = pcbs_df[pcbs_current]
pcbs_current_year.to_sql('players_career_batting_stats', con=cnx)

# add sub_league column to pcbs
cursor.execute("ALTER TABLE players_career_batting_stats ADD COLUMN sub_league_id INTEGER")
cnx.commit()
cursor.execute("""UPDATE players_career_batting_stats
                SET sub_league_id = (SELECT sub_league_id FROM teams WHERE team_id = players_career_batting_stats.team_id)""")
cnx.commit()

# Get list of distinct batter id's to compare against
cursor.execute("SELECT DISTINCT player_id FROM players_career_batting_stats")
current_batters_tuples = cursor.fetchall()
current_players = []  # We use this list to limit player records to load to db
for foo in current_batters_tuples:
    current_players.append(foo[0])

# Read players career pitching stats
pcps_df = pd.read_csv(path / 'players_career_pitching_stats.csv')
# filter players career pitching stats
pcps_current = pcps_df['year'] == game_year
pcps_current_year = pcps_df[pcps_current]
pcps_current_year.to_sql('players_career_pitching_stats', con=cnx)

# add sub_league column to pcps
cursor.execute("ALTER TABLE players_career_pitching_stats ADD COLUMN sub_league_id INTEGER")
cnx.commit()
cursor.execute("""UPDATE players_career_pitching_stats
                SET sub_league_id = (SELECT sub_league_id FROM teams WHERE team_id = players_career_pitching_stats.team_id)""")
cnx.commit()

# Add list of this year's pitchers to current_players
cursor.execute("SELECT DISTINCT player_id FROM players_career_pitching_stats")
current_pitchers_tuples = cursor.fetchall()
for foo in current_pitchers_tuples:
    current_players.append(foo[0])

# TODO thought about making the filtering and db loading a function, but it's only two lines of code and would still
# have to provide case specific params.

# load and filter players then create players table
players_df = pd.read_csv(path / 'players.csv',
                         usecols=['player_id', 'team_id', 'position', 'first_name', 'last_name', 'age',
                                  'organization_id'])
players_df.player_id.isin(current_players)
players_df = players_df[players_df.player_id.isin(current_players)]
players_df.to_sql('players', con=cnx)

# players batting
players_batting_df = pd.read_csv(path / "players_batting.csv")
players_batting_df.player_id.isin(current_players)
players_batting_df = players_batting_df[players_batting_df.player_id.isin(current_players)]
players_batting_df.to_sql('players_batting', con=cnx)

# players pitching
players_pitching_df = pd.read_csv(path / "players_pitching.csv")
players_pitching_df.player_id.isin(current_players)
players_pitching_df = players_pitching_df[players_pitching_df.player_id.isin(current_players)]
players_pitching_df.to_sql('players_pitching', con=cnx)

# players fielding
players_fielding_df = pd.read_csv(path / "players_fielding.csv")
players_fielding_df.player_id.isin(current_players)
players_fielding_df = players_fielding_df[players_fielding_df.player_id.isin(current_players)]
players_fielding_df.to_sql('players_fielding', con=cnx)

# create positions table
cursor.execute("""CREATE TABLE IF NOT EXISTS positions
(
 position   INTEGER,
 role       INTEGER,
 pos_name   VARCHAR (10),
 CONSTRAINT pos_pk PRIMARY KEY (position, role)
 )""")
cnx.commit()

cursor.execute(
    "INSERT INTO positions VALUES (1,11, 'SP'), (1,12,'RP'), (1,13,'CL'), (2,0,'C'), (3,0,'1B'), (4,0,'2B'), (5,0,"
    "'3B'), (6,0,'SS'), (7,0,'LF'), (8,0,'CF'), (9,0,'RF'), (10,0,'DH')")
cnx.commit()

#######################################
# Other tables needed for CalcBatting #
#######################################

# team relations
team_relations_df = pd.read_csv(path / 'team_relations.csv')
team_relations_df.to_sql('team_relations', con=cnx)

# parks
parks_df = pd.read_csv(path / 'parks.csv', usecols=['park_id', 'avg', 'name'])
parks_df.to_sql('parks', con=cnx)

#



# Testing section
cursor.execute("SELECT * FROM players LIMIT 20")
players = cursor.fetchall()
print(players)

cursor.execute("SELECT * FROM players_batting LIMIT 20")
players = cursor.fetchall()
print(players)

cursor.execute("SELECT * FROM players_pitching LIMIT 20")
players = cursor.fetchall()
print(players)

cursor.execute("SELECT * FROM players_fielding LIMIT 20")
players = cursor.fetchall()
print(players)

cursor.execute("SELECT * FROM positions LIMIT 20")
players = cursor.fetchall()
print(players)

print(team_name)

cnx.close()
os.remove('ootp.db')

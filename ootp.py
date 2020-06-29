import ootp_functions as ootp
import mysql.connector
import mysql.connector.errors
import csv
import os
from pathlib import Path
import CalcBatting as cb
import configparser
import mysql_db_config as msd

action = input("What are we doing today?\n(1) New Database\n(2) Update Database\nEnter a number: ")
input_path = input("What is the location of your data files?  (Full Path, please ")
path = Path(input_path)

##########################
#  Set up a new database #
##########################

if action == '1':
    database = input('''We are going to set up a connection file for your new database.
    What are we going to call it? ''')
    host = input('What is your database host? ')
    user = input('What is your username? ')
    password = input('What is your password? ')


    config = configparser.ConfigParser()
    config.add_section(database)
    config.set(database, 'host', host)
    config.set(database, 'database', database)
    config.set(database, 'user', user)
    config.set(database, 'password', password)
    with open('config.ini', 'a+') as configfile:
        config.write(configfile)

    try:
        mydb = mysql.connector.connect(host=host,user=user,password=password)
        mycursor = mydb.cursor()
        if mysql.connector.connection:
            message = 'Credentials Accepted.\nCreating Database...'
    except:
        print('Your credentials were not accepted. \nPlease check them and try again.')
        action = input("What are we doing today?\n(1) New Database\n(2) Update Database\nEnter a number: ")

    mycursor.execute("DROP DATABASE IF EXISTS " + database)

    mycursor.execute("CREATE DATABASE " + database)

    print("New database " + database + " created.\nCreating tables...")

####################
#  Update database #
####################

elif action == '2':
    database = input("What is the name of the database? ")
    config = configparser.ConfigParser()
    config.read('config.ini')
    if database in config.sections():
        print("Known Database\nConnecting...")
        host = config[database]['host']
        user = config[database]['user']
        password = config[database]['password']
        try:
            mydb = mysql.connector.connect(host=host, user=user, password=password)
            mycursor = mydb.cursor()
            if mysql.connector.connection:
                message = 'Credentials Accepted.\nUpdating Database...'
        except:
            print('Your credentials were not accepted. \nPlease check them and try again.')
            action = input("What are we doing today?\n(1) New Database\n(2) Update Database\nEnter a number: ")
    else:
        print("Database has not been configured")
        action = input("What are we doing today?\n(1) New Database\n(2) Update Database\nEnter a number: ")




mycursor.execute('USE ' + database)

# Create all of the tables
mycursor.execute("DROP TABLE IF EXISTS cities")
mydb.commit()
mycursor.execute(ootp.cities)

print("Cities created...")

mycursor.execute("DROP TABLE IF EXISTS league_history")
mydb.commit()
mycursor.execute(ootp.league_history)

print("League History created...")

mycursor.execute("DROP TABLE IF EXISTS game_score")
mydb.commit()
mycursor.execute(ootp.game_score)

print("Game Score created...")

# mycursor.execute(ootp.game_logs)

print("Game Logs skipped...")

mycursor.execute("DROP TABLE IF EXISTS nations")
mydb.commit()
mycursor.execute(ootp.nations)

print("Nations created...")


mycursor.execute("DROP TABLE IF EXISTS players_at_bat_batting_stats")
mydb.commit()
mycursor.execute(ootp.players_at_bat_batting_stats)

print("Players At Bat Batting Stats created...")

mycursor.execute("DROP TABLE IF EXISTS continents")
mydb.commit()
mycursor.execute(ootp.continents)

print("Continents created...")

mycursor.execute("DROP TABLE IF EXISTS leagues")
mydb.commit()
mycursor.execute(ootp.leagues)

print("Leagues created...")

mycursor.execute("DROP TABLE IF EXISTS sub_leages")
mydb.commit()
mycursor.execute(ootp.subleagues)

print("Sub_Leagues created...")

mycursor.execute("DROP TABLE IF EXISTS divisions")
mydb.commit()
mycursor.execute(ootp.divisions)

print("Divisions created...")

mycursor.execute("DROP TABLE IF EXISTS league_history_batting_stats")
mydb.commit()
mycursor.execute(ootp.league_history_batting_stats)

print("League History Batting Stats created...")

mycursor.execute("DROP TABLE IF EXISTS league_history_fielding_stats")
mydb.commit()
mycursor.execute(ootp.league_history_fielding_stats)

print("League History Fielding Stats created...")

mycursor.execute("DROP TABLE IF EXISTS league_history_pitching_stats")
mydb.commit()
mycursor.execute(ootp.league_history_pitching_stats)

print("League History Pitching Stats created...")

mycursor.execute("DROP TABLE IF EXISTS parks")
mydb.commit()
mycursor.execute(ootp.parks)

print("Parks created...")

mycursor.execute("DROP TABLE IF EXISTS teams")
mydb.commit()
mycursor.execute(ootp.teams)

print("Teams created...")
mycursor.execute("DROP TABLE IF EXISTS players")
mydb.commit()
mycursor.execute(ootp.players)

print("Players created...")

mycursor.execute("DROP TABLE IF EXISTS players_career_batting_stats")
mydb.commit()
mycursor.execute(ootp.players_career_batting_stats)

print("Players_Career_Batting_Stats created...")

mycursor.execute("DROP TABLE IF EXISTS players_career_fielding_stats")
mydb.commit()
mycursor.execute(ootp.players_career_fielding_stats)

print("Players_Career_Fielding_Stats created...")

mycursor.execute("DROP TABLE IF EXISTS players_career_pitching_stats")
mydb.commit()
mycursor.execute(ootp.players_career_pitching_stats)

print("Players_Career_Pitching_Stats created...")

mycursor.execute("DROP TABLE IF EXISTS players_individual_batting_stats")
mydb.commit()
mycursor.execute(ootp.players_individual_batting_stats)

print("Players_Individual_Batting_Stats created...")

mycursor.execute("DROP TABLE IF EXISTS states")
mydb.commit()
mycursor.execute(ootp.states)

print("States created...")

mycursor.execute("DROP TABLE IF EXISTS team_affiliations")
mydb.commit()
mycursor.execute(ootp.team_affiliations)

print("Team Affiliations created...")

mycursor.execute("DROP TABLE IF EXISTS team_history_financials")
mydb.commit()
mycursor.execute(ootp.team_history_financials)

print("Team History Financials created...")

mycursor.execute("DROP TABLE IF EXISTS team_relations")
mydb.commit()
mycursor.execute(ootp.team_relations)

print("Team Relations created...")

mycursor.execute("DROP TABLE IF EXISTS players_batting")
mydb.commit()
mycursor.execute(ootp.players_batting)

print("Players Batting created...")

mycursor.execute("DROP TABLE IF EXISTS players_contract")
mydb.commit()
mycursor.execute(ootp.players_contract)

print("Players Contract created...")

mycursor.execute("DROP TABLE IF EXISTS players_game_batting")
mydb.commit()
mycursor.execute(ootp.players_game_batting)

print("Players Game Batting created...")

mycursor.execute("DROP TABLE IF EXISTS players_game_pitching")
mydb.commit()
mycursor.execute(ootp.players_game_pitching)

print("Players Game Pitching created...")

mycursor.execute("DROP TABLE IF EXISTS team_fielding_stats")
mydb.commit()
mycursor.execute(ootp.team_fielding_stats)

print("Team Fielding Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_history_fielding_stats")
mydb.commit()
mycursor.execute(ootp.team_history_fielding_stats)

print("Team History Fielding Stats created...")

mycursor.execute("DROP TABLE IF EXISTS players_roster_status")
mydb.commit()
mycursor.execute(ootp.players_roster_status)

print("Player Roster Status created...")

mycursor.execute("DROP TABLE IF EXISTS team_history_batting_stats")
mydb.commit()
mycursor.execute(ootp.team_history_batting_stats)

print("Team History Batting Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_financials")
mydb.commit()
mycursor.execute(ootp.team_financials)

print("Team Financials created...")

mycursor.execute("DROP TABLE IF EXISTS team_batting_stats")
mydb.commit()
mycursor.execute(ootp.team_batting_stats)

print("Team Batting Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_bullpen_pitching_stats")
mydb.commit()
mycursor.execute(ootp.team_bullpen_pitching_stats)

print("Team Bullpen Pitching Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_pitching_stats")
mydb.commit()
mycursor.execute(ootp.team_pitching_stats)

print("Team Pitching Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_starting_pitching_stats")
mydb.commit()
mycursor.execute(ootp.team_starting_pitching_stats)

print("Team Starting Pitching Stats created...")

mycursor.execute("DROP TABLE IF EXISTS team_record")
mydb.commit()
mycursor.execute(ootp.team_record)

print("Team Record created...")

mycursor.execute("DROP TABLE IF EXISTS team_roster_staff")
mydb.commit()
mycursor.execute(ootp.team_roster_staff)

print("Team Roster Staff created...")

mycursor.execute("DROP TABLE IF EXISTS team_history_pitching_stats")
mydb.commit()
mycursor.execute(ootp.team_history_pitching_stats)

print("Team History Pitching Stats created...")

mycursor.execute("DROP TABLE IF EXISTS players_fielding")
mydb.commit()
mycursor.execute(ootp.players_fielding)

print("Players Fielding created...")

mycursor.execute("DROP TABLE IF EXISTS players_pitching")
mydb.commit()
mycursor.execute(ootp.players_pitching)

print("Players Pitching created...")

mycursor.execute("DROP TABLE IF EXISTS awards")
mydb.commit()
mycursor.execute(ootp.awards)

print("Awards created...")


mycursor.execute("DROP TABLE IF EXISTS games")
mydb.commit()
mycursor.execute(ootp.games)

print("Games created...")

#mycursor.execute(ootp.league_history_all_star)

print("League History All Star skipped...")


mycursor.execute("DROP TABLE IF EXISTS coaches")
mydb.commit()
mycursor.execute(ootp.coaches)

print("Coaches created...")

mycursor.execute("DROP TABLE IF EXISTS projected_starting_pitchers")
mydb.commit()
mycursor.execute(ootp.prob_starter)

print("Projected Starting Pitchers created...")

mycursor.execute("DROP TABLE IF EXISTS mgr_occupation")
mydb.commit()
mycursor.execute(ootp.mgr_occupation)
mycursor.execute(
    "INSERT INTO `mgr_occupation` VALUES (1, 'GM'), (2, 'Mgr'), (3, 'BC'), (4, 'PC'), (5, 'HC'), (6, 'Scout'), (12, 'Trainer'), (13, 'Owner')")
mydb.commit()

print("Manager Occupation created...")

mycursor.execute("DROP TABLE IF EXISTS mgr_personality")
mydb.commit()
mycursor.execute(ootp.mgr_personality)
mycursor.execute(
    "INSERT INTO `mgr_personality` VALUES (10, 'Personable'), (1, 'Easy Going'), (2, 'Normal'), (3, 'Tempermental'), (4, 'Controlling')")
mydb.commit()

print("Manager Personality created...")

mycursor.execute("DROP TABLE IF EXISTS management_style")
mydb.commit()
mycursor.execute(ootp.mgr_style)
mycursor.execute(
    "INSERT INTO `management_style` VALUES (0, '-'), (1, 'Conventional'), (2, 'Sabermetric'), (3, 'Smallball'), (4, 'Unorthodox'), (5, 'Tactician')")
mydb.commit()

print("Manager Style created...")

mycursor.execute("DROP TABLE IF EXISTS hitting_focus")
mydb.commit()
mycursor.execute(ootp.hitting_focus)
mycursor.execute("INSERT INTO `hitting_focus` VALUES (0, 'Contact'), (1, 'Power'), (2, 'Patience'), (3, 'Neutral')")
mydb.commit()

print("Hitting Focus created...")

mycursor.execute("DROP TABLE IF EXISTS pitching_focus")
mydb.commit()
mycursor.execute(ootp.pitching_focus)
mycursor.execute(
    "INSERT INTO `pitching_focus` VALUES (0, 'Power'), (1, 'Finesse'), (2, 'Groundball'), (3, 'Neutral')")
mydb.commit()

print("Hitting Focus created...")

mycursor.execute("DROP TABLE IF EXISTS team_history_record")
mydb.commit()
mycursor.execute(ootp.team_history_record)

print("Team History Record created...\nDatabase created!")

ootp.remove_cols(path)

# Just going to copy the db_load_new code in here becuase, fuck it.  I can't make it work as a function.

os.chdir(path)
files = os.listdir(path)
full_path_files = []
for file in files:
    new_name = str(path / file)
    full_path_files.append(new_name)

just_filenames = []
for file in full_path_files:
    strip = Path(file).stem
    just_filenames.append(strip)

mycursor.execute("SHOW tables")
tables = []
for table in mycursor:
    for item in table:
        tables.append(item)

for file in just_filenames:
    if file in tables:
        column_names = []
        file_name = str(file) + ".csv"
        values = "%s, "
        last_value = "%s)"
        mycursor.execute("Show columns FROM " + file)
        columns = [column[0] for column in mycursor.fetchall()]
        for column in columns:
            column_names.append(column)
        col_str = ","
        col_str = col_str.join(column_names)
        insert_statement = "INSERT INTO " + file + " (" + col_str + ") VALUES (" + values * (
                    len(column_names) - 1) + last_value
        print(insert_statement)
        with open(path / file_name, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
            data.pop(0)
            mycursor.executemany(insert_statement, data)
            mydb.commit()
            print(file + " data has been uploaded to database")

print("Raw data has been successfully loaded to the database!")
print("Modifying tables...")

mycursor.execute("""CREATE TABLE IF NOT EXISTS positions
(
 position   TINYINT,
 role       TINYINT,
 pos_name   VARCHAR (10),
 PRIMARY KEY (position, role)
)""")
mydb.commit()

mycursor.execute("INSERT INTO positions VALUES (1,11, 'SP'), (1,12,'RP'), (1,13,'CL'), (2,0,'C'), (3,0,'1B'), (4,0,'2B'), (5,0,'3B'), (6,0,'SS'), (7,0,'LF'), (8,0,'CF'), (9,0,'RF'), (10,0,'DH')")
mydb.commit()
print("Added positions table...")

print("Adding 'Free Agent' team to teams...")
mycursor.execute("INSERT INTO teams (team_id, name, abbr, league_id, level) VALUES (0,'Free Agent', 'FA', 100,1)")
mydb.commit()

print("Done...Setting ML teams to be their own parents...")
mycursor.execute("""UPDATE teams SET parent_team_id=team_id WHERE level=1""")
mydb.commit()
print("Done...Adding and populating Sub_League fields in tables...")
mycursor.execute("""ALTER TABLE players_career_batting_stats ADD COLUMN sub_league_id INT""")
mydb.commit()
mycursor.execute("UPDATE players_career_batting_stats AS b INNER JOIN team_relations AS t ON b.league_id=t.league_id AND b.team_id=t.team_id SET b.sub_league_id=t.sub_league_id")
mydb.commit()
mycursor.execute("ALTER TABLE players_career_pitching_stats ADD COLUMN sub_league_id INT")
mydb.commit()
mycursor.execute(
    "UPDATE players_career_pitching_stats AS b INNER JOIN team_relations AS t ON b.league_id=t.league_id AND b.team_id=t.team_id SET b.sub_league_id=t.sub_league_id")
mydb.commit()
print("Done...Creating Run Environment Tables...")
mycursor.execute(ootp.LeagueRunsPerOut)
mydb.commit()
print("League Runs Per Out Complete")
mycursor.execute(ootp.RunValues)
mydb.commit()
print("RunValues Complete")
mycursor.execute(ootp.RunValues1A)
mydb.commit()
print("Run Values 1A Complete")
mycursor.execute(ootp.RunValues2)
mydb.commit()
print("Run Values 2 Complete")
mycursor.execute(ootp.FIPConstant)
mydb.commit()
print("FIP Constant Complete")
mycursor.execute(ootp.sub_league_history_batting)
mydb.commit()
print("Sub_League History Batting Complete")
mycursor.execute(ootp.sub_league_history_pitching)
mydb.commit()
print("Sub_League History Pitching Complete")
print("Creating CalcBatting tables...this could take a while...")
mycursor.execute(cb.CalcBatting)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcBatting
ADD INDEX cb_ix1 (year),
ADD INDEX cb_ix2 (team_id),
ADD INDEX cb_ix3 (player_id),
ADD INDEX cb_ix4 (league_id)""")
mydb.commit()
print("Done!  Creating L/R Splits...")
mycursor.execute(cb.CalcBatting_L)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcBatting_L
    ADD INDEX cb_ix1 (year),
    ADD INDEX cb_ix2 (team_id),
    ADD INDEX cb_ix3 (player_id),
    ADD INDEX cb_ix4 (league_id)""")
mydb.commit()
print("Left Split Complete...")
mycursor.execute(cb.CalcBatting_R)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcBatting_R
        ADD INDEX cb_ix1 (year),
        ADD INDEX cb_ix2 (team_id),
        ADD INDEX cb_ix3 (player_id),
        ADD INDEX cb_ix4 (league_id)""")
mydb.commit()
print('Right Split Complete...\nCreating CalcPitching Tables...')
mycursor.execute(cb.CalcPitching)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcPitching
        ADD INDEX pit_ix1 (year),
        ADD INDEX pit_ix2 (team_id),
        ADD INDEX pit_ix3 (player_id)""")
print("Creating L/R Splits...")
mycursor.execute(cb.CalcPitching_L)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcPitching_L
            ADD INDEX pit_ix1 (year),
            ADD INDEX pit_ix2 (team_id),
            ADD INDEX pit_ix3 (player_id)""")
print("Left Split Complete...")
mycursor.execute(cb.CalcPitching_R)
mydb.commit()
mycursor.execute("""ALTER TABLE CalcPitching_R
            ADD INDEX pit_ix1 (year),
            ADD INDEX pit_ix2 (team_id),
            ADD INDEX pit_ix3 (player_id)""")
print("Right Split Complete...\nWe're all done!!")
mydb.close()


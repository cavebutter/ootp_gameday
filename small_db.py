import sqlite3
import pandas as pd
from pathlib import Path
from os import remove
#from prettytable import PrettyTable
#import sqlite_depth_chart_functions as dp
from _datetime import datetime
#import shutil
#import openpyxl
#from openpyxl.styles import Alignment, Font, Border, Side

#####################################################################################
#                                 WHAT THIS MODULE DOES                             #
#####################################################################################
#                                                                                   #
# Receives location of OOTP CSV Dump                                                #
# Creates a limited sqlite database in memory with the following characteristics    #
# 1. Filtered to include only batting and pitching stats from current year          #
# 2. Filtered to include only players with stat lines in the current year           #
# 3. Generate Run Value Tables for the current year for all leagues                 #
# 4. Generate CalcBatting and CalcPitching tables (with splits) for current year    #
# 5. Make the database available for Depth Chart and Gameday modules                #
#####################################################################################

#############################
# Get location of datafiles #
#############################

datafiles = input("What is the location of your data files? ")
path = Path(datafiles)


####################
# create sqlite db #
####################
try:
    cnx = sqlite3.connect('small_db')
    cursor = cnx.cursor()
    print("Successfully Connected to SQLite")


except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)

################################################################
# Leagues, , and getting game_year to limit other imports #
################################################################
try:

    # leagues
    league_df = pd.read_csv(path / 'leagues.csv',
                            usecols=['league_id', 'name', 'start_date', 'league_level', 'parent_league_id', 'current_date'])
    league_df.set_index('league_id', inplace=True)
    league_df.rename(columns={'current_date': 'curr_date'}, inplace=True)
    league_df.to_sql('leagues', con=cnx)

    # projected starting pitchers
    psp_df = pd.read_csv(path / "projected_starting_pitchers.csv")
    psp_df.to_sql('projected_starting_pitchers', con=cnx)

    # teams
    teams_df = pd.read_csv(path / 'teams.csv',
                           usecols=['team_id', 'name', 'nickname', 'abbr', 'league_id', 'sub_league_id', 'division_id',
                                    'parent_team_id', 'level', 'park_id'])
    teams_df.set_index('team_id', inplace=True)
    teams_df.to_sql('teams', con=cnx)

    # Get current league date
    cursor.execute("SELECT max(curr_date) FROM leagues")
    db_return = cursor.fetchone()
    db_date0 = db_return[0]
    game_date = datetime.strptime(db_date0, "%Y-%m-%d")


    # Get game year for trimming csv's
    cursor.execute("SELECT max(curr_date) FROM leagues")
    tempname = cursor.fetchone()
    game_year = int(tempname[0][0:4])

    ##########################################################################
    # These are the foundational tables for stats and the basis for trimming #
    ##########################################################################

    # Trim based on year and load players career batting stats
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
    # filter based on year players career pitching stats
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

    # TODO thought about making the filtering and db loading a function, but it's only two lines of code and would still have to provide case specific params.

    # load and filter players then create players table
    players_df = pd.read_csv(path / 'players.csv',
                             usecols=['player_id', 'team_id', 'bats', 'throws', 'position', 'role', 'first_name', 'last_name', 'age',
                                      'organization_id'])
    players_df.player_id.isin(current_players) # TODO is this line necessary?  Don't think so
    players_df = players_df[players_df.player_id.isin(current_players)]
    players_df.to_sql('players', con=cnx)

    #players roster stats
    prs_df = pd.read_csv(path / 'players_roster_status.csv')
    prs_df.player_id.isin(current_players)
    prs_df = prs_df[prs_df.player_id.isin(current_players)]
    prs_df.to_sql('players_roster_status', con=cnx)

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

    # players individual batting stats
    pibs_df = pd.read_csv(path / "players_individual_batting_stats.csv")
    pibs_df.player_id.isin(current_players)
    pibs_df = pibs_df[pibs_df.player_id.isin(current_players)]
    pibs_df.to_sql('players_individual_batting_stats', con=cnx)

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

    ########################################################
    # Other tables needed for CalcBatting and CalcPitching #
    ########################################################

    # team relations
    team_relations_df = pd.read_csv(path / 'team_relations.csv')
    team_relations_df.to_sql('team_relations', con=cnx)

    # parks
    parks_df = pd.read_csv(path / 'parks.csv', usecols=['park_id', 'avg', 'name'])
    parks_df.to_sql('parks', con=cnx)



    # FIPConstant
    cursor.execute("""CREATE TABLE IF NOT EXISTS FIPConstant AS
    
    SELECT
          year
        , league_id
        , hra_totals/fb_totals AS hr_fb_pct
        , 13*hra_totals AS Adjusted_HR
        , 3*bb_totals AS Adjusted_BB
        , 3*hp_totals AS Adjusted_HP
        , 2*k_totals AS Adjusted_K
        , ((ip_totals*3)+ipf_totals)*1.0/3 AS InnPitch
        , round((er_totals/(((ip_totals*3)+ipf_totals)*1.0/3))*9,2) AS lgERA
        , round(((er_totals/(((ip_totals*3)+ipf_totals)*1.0/3))*9) - (((13*hra_totals)+(3*bb_totals)+(3*hp_totals)-(2*k_totals))/(((ip_totals*3)+ipf_totals)*1.0/3)),2) AS FIPConstant
    FROM (
             SELECT year
                    , league_id
                    , sum(hra) AS hra_totals
                    , sum(bb) AS bb_totals
                    , sum(hp) AS hp_totals
                    , sum(k) AS k_totals
                    , sum(er) AS er_totals
                    , sum(ip) AS ip_totals
                    , sum(ipf) AS ipf_totals
                    , sum(fb) AS fb_totals
              FROM players_career_pitching_stats
              WHERE league_id<>0
              GROUP BY year, league_id
          ) AS x""")
    cnx.commit()

    # sub_league_history_batting
    cursor.execute("""CREATE TABLE sub_league_history_batting AS 
                        SELECT year
                        , league_id
                        , sub_league_id
                        , slg_PA
                        , slg_R
                        FROM (
                        SELECT p.year
                        , p.league_id
                        , p.sub_league_id
                        , sum(pa) AS slg_PA
                        , sum(r) AS slg_r
                        FROM players_career_batting_stats as p INNER JOIN players ON p.player_id = players.player_id
                        WHERE p.split_id = 1 AND players.position <> 1
                        GROUP BY year, league_id, sub_league_id) AS x""")
    cnx.commit()

    # sub_league_history_pitching
    cursor.execute("""CREATE TABLE IF NOT EXISTS sub_league_history_pitching AS
    
    SELECT
           x.year
         , x.league_id
         , x.sub_league_id
         , CASE WHEN x.totIP=0 THEN x.totER*9 ELSE round((x.totER *1.0/x.totIP)*9,2) END AS slgERA
         , CASE WHEN x.totIP=0 THEN x.adjHRA + x.adjBB + x.adjHP - x.adjK ELSE round((x.adjHRA + x.adjBB + x.adjHP - x.adjK)*1.0/x.totIP+f.FIPConstant,2) END AS slgFIP
         
    FROM  (
         SELECT p.year
              , p.league_id
              , p.sub_league_id
              , ((sum(ip)*3)+sum(ipf))/3 AS totIP
              , sum(er) AS totER
              , 13*sum(hra) AS adjHRA
              , 3*sum(bb) AS adjBB
              , 3*sum(hp) AS adjHP
              , 2*sum(k) AS adjK
          FROM players_career_pitching_stats AS p
          WHERE p.league_id<>0
         GROUP BY year, league_id, sub_league_id
          ) AS x
            INNER JOIN FIPConstant AS f ON x.year=f.year AND x.league_id=f.league_id""")
    cnx.commit()
    ####################
    # Run Value Tables #
    ####################

    # LeagueRunsPerOut
    cursor.execute("""CREATE TABLE IF NOT EXISTS LeagueRunsPerOut AS SELECT p.year
    , p.league_id
    , p.sub_league_id
    , sum(p.r) AS `totR`
    , sum(p.outs) AS `totOuts`
    , sum(p.outs) + sum(p.ha) + sum(p.bb)+ sum(p.iw) + sum(p.sh)
       + sum(p.sf) AS `totPA`
    , CASE WHEN sum(p.outs)=0 THEN sum(p.r) ELSE sum(p.r) * 1.000 /sum(p.outs) END AS `RperOut`
    , CASE WHEN sum(p.outs) + sum(p.ha) + sum(p.bb) + sum(p.iw) + sum(p.sh) + sum(p.sf) = 0
    THEN sum(p.r) ELSE round(sum(p.r) * 1.000000 /(sum(p.outs)+sum(p.ha)+sum(p.bb)+ sum(p.iw)+ sum(p.sh)
       + sum(p.sf)),8) END AS `RperPA`
    FROM players_career_pitching_stats p
    GROUP BY p.year, p.league_id, p.sub_league_id""")
    cnx.commit()

    # tblRunValues
    cursor.execute("""CREATE TABLE IF NOT EXISTS tblRunValues
    AS SELECT year
    , league_id
    , sub_league_id
    , RperOut
    , round(RperOut+0.14,4) AS runBB
    , round((RperOut+0.14)+0.025,4) AS runHB
    , round((RperOut+0.14)+0.155,4) AS run1B
    , round((RperOut+0.295)+0.3,4) AS run2B
    , round((RperOut+0.595)+0.27,4) AS run3B
    , 1.4 AS runHR
    , 0.2 AS runSB
    , 2*RperOut+0.075 AS runCS
    FROM LeagueRunsPerOut""")
    cnx.commit()

    # RunValues1A
    cursor.execute("""CREATE TABLE IF NOT EXISTS tblRunValues1A AS
    SELECT r.year
    , r.league_id
    , r.sub_league_id
    , r.RperOut
    , r.runBB
    , r.runHB
    , r.run1B
    , r.run2B
    , r.run3B
    , r.runHR
    , r.runSB
    , r.runCS
    , SUM(runBB*(BB-IBB) + runHB * HP + run1B * s + run2B * d
       + run3B * t + 1.4 * HR + runSB * SB - runCS * CS) * 1.0
       / SUM(AB - H + SF) AS runMinus
    
    , SUM(runBB * (BB-IBB) + runHB * HP + run1B * s + run2B * d
       + run3B * t + 1.4 * HR + runSB * SB - runCS * CS) * 1.0
       / SUM(BB-IBB + HP + H) AS runPlus
    
    , SUM(H+BB-IBB+HP) * 1.0 / SUM(AB+BB-IBB+HP+SF) AS wOBA
    
    FROM tblRunValues r
    INNER JOIN (
          SELECT year
               , league_id
               , sub_league_id
               , sum(ab) AS ab
               , sum(bb) AS BB
               , sum(ibb) AS IBB
               , sum(hp) AS HP
               , sum(h) AS h
               , sum(h)-sum(d)-sum(t)-sum(hr) AS s
               , sum(d) AS d
               , sum(t) AS t
               , sum(hr) AS hr
               , sum(sb) AS SB
               , sum(cs) AS CS
               , sum(sf) AS SF
           FROM players_career_batting_stats
           GROUP BY year, league_id, sub_league_id
               ) AS x ON r.year=x.year AND r.league_id=x.league_id AND r.sub_league_id=x.sub_league_id
    
    GROUP BY
    r.year
    , r.league_id
    , r.sub_league_id
    , r.RperOut
    , r.runBB
    , r.runHB
    , r.run1B
    , r.run2B
    , r.run3B
    , r.runHR
    , r.runSB
    , r.runCS""")
    cnx.commit()

    # tblRunValues2
    cursor.execute("""CREATE TABLE tblRunValues2 AS
    SELECT year
    , league_id
    , sub_league_id
    , RperOut
    , runBB
    , runHB
    , run1B
    , run2B
    , run3B
    , runHR
    , runSB
    , runCS
    , runMinus
    , runPlus
    , wOBA
    , 1.0/(runPlus+runMinus) AS wOBAScale
    , (runBB+runMinus)* (1.0/(runPlus+runMinus)) AS wobaBB
    , (runHB+runMinus)* (1.0/(runPlus+runMinus)) AS wobaHB
    , (run1B+runMinus)* (1.0/(runPlus+runMinus)) AS woba1B
    , (run2B+runMinus)* (1.0/(runPlus+runMinus)) AS woba2B
    , (run3B+runMinus)* (1.0/(runPlus+runMinus)) AS woba3B
    , (runHR+runMinus)* (1.0/(runPlus+runMinus)) AS wobaHR
    , runSB* (1.0/(runPlus+runMinus)) AS wobASB
    , runCS* (1.0/(runPlus+runMinus)) AS wobaCS
    FROM tblRunValues1A""")
    cnx.commit()

    ###############
    # CalcBatting #
    ###############
    # TODO wRC+ is broken.  Produces a NONE result.
    # Overall
    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcBatting AS
        SELECT b.year
        , b.level_id
        , b.league_id
        , b.player_id
        , b.stint
        , b.split_id
        , b.team_id
        , b.sub_league_id
        , b.g
        , b.ab
        , b.ab+b.bb+b.sh+b.sf+b.hp AS PA -- used to be variable.  copy this line wherever PA is needed
        , b.r
        , b.h
        , b.d
        , b.t
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , round((b.h * 1.0)/b.ab,3) AS ba
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp)=0 THEN 0 ELSE round((b.k * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS krate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp) = 0 THEN 0 ELSE round((b.bb * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS bbrate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci) = 0 THEN 0 ELSE round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3) END AS obp
        , CASE WHEN r.woba = 0 THEN 0 ELSE round(100 * ((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci)) * 1.0 / r.woba,0) END as OBPplus
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) as slg
        , round((round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3))+(round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3)),3) as ops
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) - round((b.h * 1.0)/b.ab,3) AS iso
        , CASE WHEN b.ab-b.k-b.hr+b.sf=0 THEN 0 ELSE round((b.h-b.hr * 1.0) /(b.ab-b.k-b.hr+b.sf),3) END AS babip
        , round(((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
        , round((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)),1) as wRAA
        , round(((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp))-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*(b.ab+b.bb+b.sh+b.sf+b.hp),1) as wRC
        , (((((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)))/(b.ab+b.bb+b.sh+b.sf+b.hp) + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100 as 'wRC+'
    
        FROM
          players_career_batting_stats b
          INNER JOIN teams t ON b.team_id=t.team_id
          INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
          INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
          INNER JOIN parks p ON t.park_id=p.park_id
          INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year
        WHERE b.ab<>0 AND b.split_id=1 AND b.league_id<>0 AND b.team_id<>0
        """)
    cnx.commit()
    #test
    cursor.execute("SELECT * FROM LeagueRunsPerOut")
    lrpo = cursor.fetchall()

    cursor.execute("SELECT * FROM CalcBatting LIMIT 20")
    calcb = cursor.fetchall()

    # CalcBatting L Split
    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcBatting_l AS
        SELECT b.year
        , b.level_id
        , b.league_id
        , b.player_id
        , b.stint
        , b.split_id
        , b.team_id
        , b.sub_league_id
        , b.g
        , b.ab
        , b.ab+b.bb+b.sh+b.sf+b.hp AS PA -- used to be variable.  copy this line wherever PA is needed
        , b.r
        , b.h
        , b.d
        , b.t
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , round((b.h * 1.0)/b.ab,3) AS ba
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp)=0 THEN 0 ELSE round((b.k * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS krate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp) = 0 THEN 0 ELSE round((b.bb * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS bbrate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci) = 0 THEN 0 ELSE round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3) END AS obp
        , CASE WHEN r.woba = 0 THEN 0 ELSE round(100 * ((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci)) * 1.0 / r.woba,0) END as OBPplus
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) as slg
        , round((round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3))+(round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3)),3) as ops
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) - round((b.h * 1.0)/b.ab,3) AS iso
        , CASE WHEN b.ab-b.k-b.hr+b.sf=0 THEN 0 ELSE round((b.h-b.hr * 1.0) /(b.ab-b.k-b.hr+b.sf),3) END AS babip
        , round(((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
        , round((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)),1) as wRAA
        , round(((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp))-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*(b.ab+b.bb+b.sh+b.sf+b.hp),1) as wRC
        , ROUND((((((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)))/(b.ab+b.bb+b.sh+b.sf+b.hp) + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100,0) as 'wRC+'
    
        FROM
          players_career_batting_stats b
          INNER JOIN teams t ON b.team_id=t.team_id
          INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
          INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
          INNER JOIN parks p ON t.park_id=p.park_id
          INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year
        WHERE b.ab<>0 AND b.split_id=2 AND b.league_id<>0 AND b.team_id<>0
        """)
    cnx.commit()

    # CalcBatting R Split
    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcBatting_r AS
        SELECT b.year
        , b.level_id
        , b.league_id
        , b.player_id
        , b.stint
        , b.split_id
        , b.team_id
        , b.sub_league_id
        , b.g
        , b.ab
        , b.ab+b.bb+b.sh+b.sf+b.hp AS PA -- used to be variable.  copy this line wherever PA is needed
        , b.r
        , b.h
        , b.d
        , b.t
        , b.hr
        , b.rbi
        , b.sb
        , b.cs
        , b.bb
        , b.k
        , b.ibb
        , b.hp
        , b.sh
        , b.sf
        , b.gdp
        , b.ci
        , b.war
        , round((b.h * 1.0)/b.ab,3) AS ba
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp)=0 THEN 0 ELSE round((b.k * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS krate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp) = 0 THEN 0 ELSE round((b.bb * 1.0) / (b.ab+b.bb+b.sh+b.sf+b.hp),3) END AS bbrate
        , CASE WHEN (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci) = 0 THEN 0 ELSE round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3) END AS obp
        , CASE WHEN r.woba = 0 THEN 0 ELSE round(100 * ((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci)) * 1.0 / r.woba,0) END as OBPplus
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) as slg
        , round((round((b.h + b.bb + b.hp) * 1.0 / (b.ab+b.bb+b.sh+b.sf+b.hp-b.sh-b.ci),3))+(round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3)),3) as ops
        , round((b.h+b.d+2*b.t+3*b.hr) * 1.0 / b.ab,3) - round((b.h * 1.0)/b.ab,3) AS iso
        , CASE WHEN b.ab-b.k-b.hr+b.sf=0 THEN 0 ELSE round((b.h-b.hr * 1.0) /(b.ab-b.k-b.hr+b.sf),3) END AS babip
        , round(((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp),3) as woba
        , round((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)),1) as wRAA
        , round(((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp))-r.woba)/r.wOBAscale)+(lro.totr/lro.totpa))*(b.ab+b.bb+b.sh+b.sf+b.hp),1) as wRC
        , ROUND((((((((((r.wobaBB*(b.bb-b.ibb) + r.wobaHB*b.hp + r.woba1B*(b.h-b.d-b.t-b.hr) + r.woba2B*b.d + r.woba3B*b.t + r.wobaHR*b.hr) * 1.0) / (b.ab+b.bb-b.ibb+b.sf+b.hp) - r.woba * 1.0) / r.wobascale)*(b.ab+b.bb+b.sh+b.sf+b.hp)))/(b.ab+b.bb+b.sh+b.sf+b.hp) + lro.RperPA) + (lro.RperPA - p.avg*lro.RperPA))/(slg.slg_r/slg.slg_pa))*100,0) as 'wRC+'
    
        FROM
          players_career_batting_stats b
          INNER JOIN teams t ON b.team_id=t.team_id
          INNER JOIN tblRunValues2 r ON b.year=r.year AND b.league_id=r.league_id AND b.sub_league_id=r.sub_league_id
          INNER JOIN LeagueRunsPerOut lro ON b.year=lro.year AND b.league_id=lro.league_id AND b.sub_league_id=lro.sub_league_id
          INNER JOIN parks p ON t.park_id=p.park_id
          INNER JOIN sub_league_history_batting slg ON b.sub_league_id=slg.sub_league_id AND b.league_id=slg.league_id AND b.year=slg.year
        WHERE b.ab<>0 AND b.split_id=3 AND b.league_id<>0 AND b.team_id<>0
        """)
    cnx.commit()

    ################
    # CalcPitching #
    ################
    # Overall
    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcPitching AS
    SELECT
        i.player_id
        , i.year
        , i.stint
        , i.team_id
        , i.level_id
        , i.league_id
        , i.sub_league_id
        , i.split_id
        , i.ip
        , i.ab
        , i.tb
        , i.ha
        , i.k
        , i.bf
        , i.rs
        , i.bb
        , i.r
        , i.er
        , i.gb
        , i.fb
        , i.pi
        , i.ipf
        , i.g
        , i.gs
        , i.w
        , i.l
        , i.s
        , i.sa
        , i.da
        , i.sh
        , i.sf
        , i.ta
        , i.hra
        , i.bk
        , i.ci
        , i.iw
        , i.wp
        , i.hp
        , i.gf
        , i.dp
        , i.qs
        , i.svo
        , i.bs
        , i.ra
        , i.cg
        , i.sho
        , i.sb
        , i.cs
        , i.hld
        , i.ir
        , i.irs
        , i.wpa
        , i.li
        , i.outs
        , i.war
        , ((3*ip)+ipf)*1.0/3 AS InnPitch
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.k)/(((3*ip)+ipf)*1.0/3),1) END as `k9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.bb)/(((3*ip)+ipf)*1.0/3),1) END AS `bb9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.hra)/(((3*ip)+ipf)*1.0/3),1) END AS `HR9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.bb+i.ha)*1.0/(((3*ip)+ipf)*1.0/3),2) END AS `WHIP`
        , CASE WHEN i.bb=0 THEN 0 ELSE round(i.k*1.0/i.bb,2) END AS `K/BB`
        , CASE WHEN i.fb=0 THEN 0 ELSE i.gb * 1.0 / i.fb END AS `gb/fb`
        , CASE WHEN i.ab-i.k-i.hra-i.sh+i.sf=0 THEN 0 ELSE round((i.ha-i.hra)*1.0/(i.ab-i.k-i.hra-i.sh+i.sf),3) END AS `BABIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END AS `ERA`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `FIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `xFIP`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END)*(p.avg)))/slg.slgERA),0) AS `ERAminus`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END)*(p.avg)))/slg.slgFIP),0) AS `FIPminus`
        FROM players_career_pitching_stats AS i
        INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
        INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
        INNER JOIN teams AS t ON i.team_id=t.team_id
        INNER JOIN parks AS p ON t.park_id=p.park_id
    WHERE i.split_id=1 AND i.league_id<>0 AND i.team_id<>0""")
    cnx.commit()

    # Left Split
    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcPitching_l AS
    SELECT
        i.player_id
        , i.year
        , i.stint
        , i.team_id
        , i.level_id
        , i.league_id
        , i.sub_league_id
        , i.split_id
        , i.ip
        , i.ab
        , i.tb
        , i.ha
        , i.k
        , i.bf
        , i.rs
        , i.bb
        , i.r
        , i.er
        , i.gb
        , i.fb
        , i.pi
        , i.ipf
        , i.g
        , i.gs
        , i.w
        , i.l
        , i.s
        , i.sa
        , i.da
        , i.sh
        , i.sf
        , i.ta
        , i.hra
        , i.bk
        , i.ci
        , i.iw
        , i.wp
        , i.hp
        , i.gf
        , i.dp
        , i.qs
        , i.svo
        , i.bs
        , i.ra
        , i.cg
        , i.sho
        , i.sb
        , i.cs
        , i.hld
        , i.ir
        , i.irs
        , i.wpa
        , i.li
        , i.outs
        , i.war
        , ((3*ip)+ipf)*1.0/3 AS InnPitch
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.k)/(((3*ip)+ipf)*1.0/3),1) END as `k9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.bb)/(((3*ip)+ipf)*1.0/3),1) END AS `bb9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.hra)/(((3*ip)+ipf)*1.0/3),1) END AS `HR9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.bb+i.ha)*1.0/(((3*ip)+ipf)*1.0/3),2) END AS `WHIP`
        , CASE WHEN i.bb=0 THEN 0 ELSE round(i.k*1.0/i.bb,2) END AS `K/BB`
        , CASE WHEN i.fb=0 THEN 0 ELSE i.gb * 1.0 / i.fb END AS `gb/fb`
        , CASE WHEN i.ab-i.k-i.hra-i.sh+i.sf=0 THEN 0 ELSE round((i.ha-i.hra)*1.0/(i.ab-i.k-i.hra-i.sh+i.sf),3) END AS `BABIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END AS `ERA`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `FIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `xFIP`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END)*(p.avg)))/slg.slgERA),0) AS `ERAminus`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END)*(p.avg)))/slg.slgFIP),0) AS `FIPminus`
        FROM players_career_pitching_stats AS i
        INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
        INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
        INNER JOIN teams AS t ON i.team_id=t.team_id
        INNER JOIN parks AS p ON t.park_id=p.park_id
    WHERE i.split_id=2 AND i.league_id<>0 AND i.team_id<>0""")
    cnx.commit()

    # Right Split

    cursor.execute("""CREATE TABLE IF NOT EXISTS CalcPitching_r AS
    SELECT
        i.player_id
        , i.year
        , i.stint
        , i.team_id
        , i.level_id
        , i.league_id
        , i.sub_league_id
        , i.split_id
        , i.ip
        , i.ab
        , i.tb
        , i.ha
        , i.k
        , i.bf
        , i.rs
        , i.bb
        , i.r
        , i.er
        , i.gb
        , i.fb
        , i.pi
        , i.ipf
        , i.g
        , i.gs
        , i.w
        , i.l
        , i.s
        , i.sa
        , i.da
        , i.sh
        , i.sf
        , i.ta
        , i.hra
        , i.bk
        , i.ci
        , i.iw
        , i.wp
        , i.hp
        , i.gf
        , i.dp
        , i.qs
        , i.svo
        , i.bs
        , i.ra
        , i.cg
        , i.sho
        , i.sb
        , i.cs
        , i.hld
        , i.ir
        , i.irs
        , i.wpa
        , i.li
        , i.outs
        , i.war
        , ((3*ip)+ipf)*1.0/3 AS InnPitch
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.k)/(((3*ip)+ipf)*1.0/3),1) END as `k9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.bb)/(((3*ip)+ipf)*1.0/3),1) END AS `bb9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((9.0*i.hra)/(((3*ip)+ipf)*1.0/3),1) END AS `HR9`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.bb+i.ha)*1.0/(((3*ip)+ipf)*1.0/3),2) END AS `WHIP`
        , CASE WHEN i.bb=0 THEN 0 ELSE round(i.k*1.0/i.bb,2) END AS `K/BB`
        , CASE WHEN i.fb=0 THEN 0 ELSE i.gb * 1.0 / i.fb END AS `gb/fb`
        , CASE WHEN i.ab-i.k-i.hra-i.sh+i.sf=0 THEN 0 ELSE round((i.ha-i.hra)*1.0/(i.ab-i.k-i.hra-i.sh+i.sf),3) END AS `BABIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END AS `ERA`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `FIP`
        , CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*(i.fb*f.hr_fb_pct))+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END AS `xFIP`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round((i.er*1.0/(((3*ip)+ipf)*1.0/3))*9,2) END)*(p.avg)))/slg.slgERA),0) AS `ERAminus`
        , round(100*(((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) + ((CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END) - (CASE WHEN (((3*ip)+ipf)*1.0/3)=0 THEN 0 ELSE round(((13*i.hra)+(3*(i.bb+i.hp))-(2*i.k))*1.0/(((3*ip)+ipf)*1.0/3)+f.FIPConstant,2) END)*(p.avg)))/slg.slgFIP),0) AS `FIPminus`
        FROM players_career_pitching_stats AS i
        INNER JOIN FIPConstant AS f ON i.year=f.year AND i.league_id=f.league_id
        INNER JOIN sub_league_history_pitching AS slg ON i.year=slg.year AND i.league_id=slg.league_id AND i.sub_league_id=slg.sub_league_id
        INNER JOIN teams AS t ON i.team_id=t.team_id
        INNER JOIN parks AS p ON t.park_id=p.park_id
    WHERE i.split_id=3 AND i.league_id<>0 AND i.team_id<>0""")
    cnx.commit()

except FileNotFoundError:
    print("There was a problem with your data files.\nPlease double-check the path to your data files.")
    print("""Please ensure that the following files exist in your directory:
    leagues.csv
    teams.csv
    projected_starting_pitchers.csv
    players_career_batting_stats.csv
    players_career_pitching_stats.csv
    players.csv
    players_roster_status.csv
    players_batting.csv
    players_pitching.csv
    players_fielding.csv
    players_individual_batting_stats.csv
    team_relations.csv
    parks.csv""")
    terminate = input("Press any key to exit.")
    if terminate == True:
        cnx.close()
        #remove('small_db')
        exit()
except sqlite3.OperationalError:
    print("There was a problem with your data files.\nPlease double-check the path to your data files.")
    print("""Please ensure that the following files exist in your directory:
    leagues.csv
    teams.csv
    projected_starting_pitchers.csv
    players_career_batting_stats.csv
    players_career_pitching_stats.csv
    players.csv
    players_roster_status.csv
    players_batting.csv
    players_pitching.csv
    players_fielding.csv
    players_individual_batting_stats.csv
    team_relations.csv
    parks.csv""")
    terminate = input("Press any key to exit.")
    if terminate == True:
        cnx.close()
        #remove('small_db')
        exit()

# Testing section
#print("TESTING SECTION:")
#print("Game Date: " + str(game_date))
#print("Game Year: " + str(game_year))
#cursor.execute("SELECT count(*) FROM players_career_batting_stats")
#pcbs_test = cursor.fetchone()
#print("Count of PCBS records: " + str(pcbs_test[0]))
#cursor.execute("SELECT count(*) FROM players_career_pitching_stats")
#pcps_test = cursor.fetchone()
#print("Count of PCPS records: " + str(pcps_test[0]))
#print("Number of current players: " + str(len(current_players)))
#cursor.execute("SELECT * FROM sub_league_history_batting LIMIT 10")
#slhb = cursor.fetchall()
#print("sub_league_history_batting = " + str(slhb))
#cursor.execute("SELECT * FROM LeagueRunsPerOut")
#lrpo = cursor.fetchall()
#cursor.execute("SELECT * FROM CalcBatting LIMIT 20")
#calcb = cursor.fetchall()
#cursor.execute("SELECT * FROM CalcBatting_l LIMIT 20")
#calcbl = cursor.fetchall()
#cursor.execute("SELECT * FROM CalcBatting_r LIMIT 20")
#calcbr = cursor.fetchall()
#cursor.execute("SELECT * from sub_league_history_pitching LIMIT 10")
#slhp = cursor.fetchall()
#cursor.execute("SELECT * FROM FIPConstant LIMIT 10")
#fip = cursor.fetchall()
#cursor.execute("SELECT * FROM CalcPitching LIMIT 10")
#calcp = cursor.fetchall()

#print("League Runs Per Out: ")
#print(lrpo)
#print("CalcBatting:")
#print(calcb)
#print("CalcBatting_L:")
#print(calcbl)
#print("CalcBatting_R:")
#print(calcbr)
#print("sub_league_history_pitching = " + str(slhp))
#print("FIP:")
#print(fip)
#print("CalcPitching:")
#print(calcp)
#cursor.execute("SELECT COUNT(*) FROM players_individual_batting_stats")
#pibs_total = cursor.fetchone()
#print("Count of total records in pibs: " + str(pibs_total[0]))
#cursor.execute("SELECT COUNT(DISTINCT player_id) FROM players_individual_batting_stats")
#pibs_distinct = cursor.fetchone()
#print("Distinct IDs in PIBS: " + str(pibs_distinct[0]))
print("Small Database Created!\nOn to the next thing...")
cnx.close()
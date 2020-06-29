import os.path
import mysql.connector
import mysql.connector.errors
import pandas as pd
from pathlib import Path


#  Create a file that stores database connection data
def store_connection(connection_name, connection_data):
    connection_file = connection_name + ".txt"
    path = Path.cwd() / 'db_config'
    if os.path.isfile(path / connection_file):
        message = 'This connection already exists. \nStart over with a different name.'
    else:
        with open(path / connection_file, 'w') as f:
            f.write(connection_data)
        message = 'Connection file saved.\nTesting database server credentials...'
    return message


# This is not being used because I cannot figure out how to call the config files
# function is being handled in ootp.py
def test_db_credentials(connection_name):
    import db_config.connection_name
    mydb = mysql.connector.connect(host=connection_name.host, user=connection_name.user,
                                   password=connection_name.password)
    mycursor = mydb.cursor()
    if mysql.connector.is_connected():
        message = 'Credentials Accepted.\nCreating Database...'
    else:
        message = 'Credentials Rejected.\nCheck your credentials and try again.'
    return message


# Create a new OOTP database with string variables passed to ootp.py
# Assumes connection is already established

cities = '''CREATE TABLE IF NOT EXISTS `cities` (
    `city_id` INT PRIMARY KEY,
    `nation_id` INT,
    `state_id` INT,
    `name` VARCHAR (50),
    `abbreviation` VARCHAR (50),
    `lattitude` DOUBLE (7,4),
    `longitude` DOUBLE (7,4),
    `population` INT
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

league_history = '''CREATE TABLE IF NOT EXISTS `league_history` (
    `league_id` INT,
    `sub_league_id` INT,
    `year` INT,
    `best_hitter_id` INT,
    `best_pitcher_id` INT,
    `best_rookie_id` INT,
    `best_manager_id` INT,
    `best_fileder_id0` INT,
    `best_fileder_id1` INT,
    `best_fileder_id2` INT,
    `best_fileder_id3` INT,
    `best_fileder_id4` INT,
    `best_fileder_id5` INT,
    `best_fileder_id6` INT,
    `best_fileder_id7` INT,
    `best_fileder_id8` INT,
    `best_fileder_id9` INT,
    PRIMARY KEY (`league_id`, `sub_league_id`, `year`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

game_score = '''CREATE TABLE IF NOT EXISTS `game_score` (
    `gs_id` INT AUTO_INCREMENT PRIMARY KEY,
    `game_id` INT,
    `team` INT,
    `inning` INT,
    `score` INT
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

game_logs = '''CREATE TABLE IF NOT EXISTS `game_logs` (
    `game_id` INT,
    `type` INT(1),
    `line` INT,
    `text` text,
    PRIMARY KEY (`game_id`, `type`, `line`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

nations = '''CREATE TABLE IF NOT EXISTS `nations` (
  `nation_id` INT,
  `name` VARCHAR(50),
  `short_name` VARCHAR(50),
  `abbreviation` VARCHAR(50),
  `demonym` VARCHAR(50),
  `population` INT,
  `gender` INT,
  `baseball_quality` INT,
  `continent_id` INT,
  `main_language_id` INT,
  `quality_total` INT,
  `capital_id` INT,
  `use_hardcoded_ml_player_origins` TINYINT,
  `this_is_the_usa` TINYINT,
  PRIMARY KEY (`nation_id`)
  ) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_at_bat_batting_stats = '''CREATE TABLE IF NOT EXISTS players_at_bat_batting_stats (
    `pabbs_id` INT AUTO_INCREMENT PRIMARY KEY,
    `player_id` INT,
    `game_id` INT,
    `opponent_player_id` INT,
    `team_id` INT,
    `sac` INT (1),
    `balls` INT(1),
    `strikes` INT(1),
    `result` INT,
    `base1` INT(1),
    `base2` INT(1),
    `base3` INT(1),
    `close` INT(1),
    `pinch` INT (1),
    `inning` INT(2),
    `run_diff` INT(2),
    `outs` INT(1),
    `sb` INT(1),
    `cs` INT(1),
    `rbi` INT(1),
    `r` INT(1),
    `spot` INT(1),
    `hit_loc`INT(1),
    `hit_xy` INT(1),
    `exit_velo` INT(1),
    `launch_angle` INT(1)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

continents = '''CREATE TABLE IF NOT EXISTS `continents` (
    `continent_id` INT PRIMARY KEY,
    `name` VARCHAR (30),
    `abbreviation` VARCHAR (3),
    `demonym` VARCHAR(30),
    `population` bigint,
    `main_language_id` INT
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

leagues = '''CREATE TABLE IF NOT EXISTS `leagues` (
  `league_id` INT,
  `name` VARCHAR(50),
  `abbr` VARCHAR(50),
  `nation_id` INT,
  `language_id` INT,
  `historical_league` TINYINT,
  `start_date` DATE,
  `preferred_start_date` DATE,
  `pitcher_award_name` VARCHAR(50),
  `mvp_award_name` VARCHAR(50),
  `rookie_award_name` VARCHAR(50),
  `defense_award_name` VARCHAR(50),
  `draft_date` DATE,
  `rule_5_draft_date` DATE,
  `roster_expand_date` DATE,
  `trade_deadline_date` DATE,
  `allstar_date` DATE,
  `parent_league_id` INT,
  `season_year` INT,
  `historical_year` SMALLINT,
  `league_level` SMALLINT,
  `curr_date` DATE,
  PRIMARY KEY (`league_id`))
 ENGINE=InnoDB DEFAULT CHARSET=latin1'''

subleagues = '''CREATE TABLE IF NOT EXISTS `sub_leagues` (
  `league_id` INT,
  `sub_league_id` INT,
  `name` VARCHAR(50),
  `abbr` VARCHAR(50),
  `gender` INT,
  `designated_hitter` TINYINT,
  PRIMARY KEY (`league_id`, `sub_league_id`))
   ENGINE=InnoDB DEFAULT CHARSET=latin1'''

divisions = '''CREATE TABLE IF NOT EXISTS `divisions` (
  `league_id` INT,
  `sub_league_id` INT,
  `division_id` INT,
  `name` VARCHAR(50),
  `gender` INT,
  PRIMARY KEY (`league_id`, `sub_league_id`, `division_id`))
   ENGINE=InnoDB DEFAULT CHARSET=latin1'''

league_history_batting_stats = '''CREATE TABLE IF NOT EXISTS `league_history_batting_stats` (
`year` SMALLINT,
`team_id` INT,
`game_id` INT,
`league_id` INT,
`level_id` SMALLINT,
`split_id` SMALLINT,
`pa` INT,
`ab` INT,
`h` INT,
`k` INT,
`tb` INT,
`s` INT,
`d` INT,
`t` INT,
`hr` INT,
`sb` INT,
`cs` INT,
`rbi` INT,
`r` INT,
`bb` INT,
`ibb` INT,
`hp` INT,
`sh` INT,
`sf` INT,
`ci` INT,
`gdp` INT,
`g` INT,
`gs` INT,
`ebh` INT,
`pitches_seen` INT,
`avg` DOUBLE,
`obp` DOUBLE,
`slg` DOUBLE,
`rc` DOUBLE,
`rc27` DOUBLE,
`iso` DOUBLE,
`woba` DOUBLE,
`ops` DOUBLE,
`sbp` DOUBLE,
`kp` DOUBLE,
`bbp` DOUBLE,
`wpa` DOUBLE,
`babip` DOUBLE)
ENGINE=InnoDB DEFAULT CHARSET=latin1'''

league_history_fielding_stats = '''CREATE TABLE IF NOT EXISTS `league_history_fielding_stats` (`year` SMALLINT, `team_id` INT, `league_id` INT, `sub_league_id` INT, `level_id` SMALLINT, `split_id` SMALLINT, `position` SMALLINT, `g` INT, `gs` INT, `tc` INT, `a` INT, `po` INT, `e` INT, `dp` INT, `tp` INT, `pb` INT, `sba` INT, `rto` INT, `er` INT, `ip` INT, `ipf` INT, `pct` DOUBLE, `def_range` DOUBLE, `rtop` DOUBLE, `cera` DOUBLE, `zr` DOUBLE, `plays` INT, `plays_base` INT, `roe` INT, `eff` INT, `opps_0` INT, `opps_made_0` INT, `opps_1` INT, `opps_made_1` INT, `opps_2` INT, `opps_made_2` INT, `opps_3` INT, `opps_made_3` INT, `opps_4` INT, `opps_made_4` INT, `opps_5` INT, `opps_made_5` INT) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

league_history_pitching_stats = '''CREATE TABLE IF NOT EXISTS `league_history_pitching_stats` (`year` SMALLINT, `team_id` INT, `game_id` INT, `league_id` INT, `level_id` SMALLINT, `split_id` SMALLINT, `ab` INT, `ip` INT, `bf` INT, `tb` INT, `ha` INT, `k` INT, `rs` INT, `bb` INT, `r` INT, `er` INT, `gb` INT, `fb` INT, `pi` INT, `ipf` INT, `g` INT, `gs` INT, `w` INT, `l` INT, `s` INT, `sa` INT, `da` INT, `sh` INT, `sf` INT, `ta` INT, `hra` INT, `bk` INT, `ci` INT, `iw` INT, `wp` INT, `hp` INT, `gf` INT, `dp` INT, `qs` INT, `svo` INT, `bs` INT, `ra` INT, `ir` INT, `irs` INT, `cg` INT, `sho` INT, `sb` INT, `cs` INT, `hld` INT, `r9` DOUBLE, `avg` DOUBLE, `obp` DOUBLE, `slg` DOUBLE, `ops` DOUBLE, `h9` DOUBLE, `k9` DOUBLE, `hr9` DOUBLE, `bb9` DOUBLE, `cgp` DOUBLE, `fip` DOUBLE, `qsp` DOUBLE, `winp` DOUBLE, `rsg` DOUBLE, `svp` DOUBLE, `bsvp` DOUBLE, `irsp` DOUBLE, `gfp` DOUBLE, `era` DOUBLE, `pig` DOUBLE, `whip` DOUBLE, `gbfbp` DOUBLE, `kbb` DOUBLE, `babip` DOUBLE) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

parks = '''CREATE TABLE IF NOT EXISTS `parks` (`park_id` INT, `avg` FLOAT, `name` VARCHAR(100), `capacity` INT, PRIMARY KEY (`park_id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

teams = '''CREATE TABLE IF NOT EXISTS `teams` (`team_id` INT, `name` VARCHAR(50), `abbr` VARCHAR(50), `nickname` 
VARCHAR(50), `city_id` INT, `park_id` INT, `league_id` INT, `sub_league_id` INT, `division_id` INT, `nation_id` INT, 
`parent_team_id` INT, `level` INT,  PRIMARY KEY (`team_id`), INDEX `teams_ix1` (`park_id`), INDEX `teams_ix2` (
`league_id`), INDEX `teams_ix3` (`sub_league_id`), INDEX `teams_ix4` (`division_id`) ) ENGINE=InnoDB DEFAULT 
CHARSET=latin1 '''

players = '''CREATE TABLE IF NOT EXISTS `players` (`player_id` INT, `team_id` INT, `league_id` INT, `position` SMALLINT, `role` SMALLINT, `first_name` VARCHAR(50), `last_name` VARCHAR(50), `nick_name` VARCHAR(50), `age` SMALLINT, `date_of_birth` DATE, `city_of_birth_id` INT, `nation_id` INT, `second_nation_id` INT, `weight` SMALLINT, `height` SMALLINT, `retired` TINYINT, `free_agent` TINYINT, `last_league_id` INT, `last_team_id` INT, `organization_id` INT, `last_organization_id` INT, `language_ids0` INT, `language_ids1` INT, `uniform_number` SMALLINT, `experience` SMALLINT, `person_type` SMALLINT, `bats` SMALLINT, `throws` SMALLINT, `personality_greed` SMALLINT, `personality_loyalty` SMALLINT, `personality_play_for_winner` SMALLINT, `personality_work_ethic` SMALLINT, `personality_intelligence` SMALLINT, `personality_leader` SMALLINT, `historical_id` VARCHAR(50), `historical_team_id` VARCHAR(50), `best_contract_offer_id` INT, `injury_is_injured` TINYINT, `injury_dtd_injury` TINYINT, `injury_career_ending` TINYINT, `injury_dl_left` SMALLINT, `injury_dl_playoff_round` SMALLINT, `injury_left` SMALLINT, `dtd_injury_effect` SMALLINT, `injury_id` INT, `prone_overall` SMALLINT, `prone_leg` SMALLINT, `prone_back` SMALLINT, `prone_arm` SMALLINT, `fatigue_pitches0` SMALLINT, `fatigue_pitches1` SMALLINT, `fatigue_pitches2` SMALLINT, `fatigue_pitches3` SMALLINT, `fatigue_pitches4` SMALLINT, `fatigue_pitches5` SMALLINT, `fatigue_points` SMALLINT, `fatigue_played_today` TINYINT, `running_ratings_speed` SMALLINT, `running_ratings_stealing` SMALLINT, `running_ratings_baserunning` SMALLINT, `college` TINYINT, `draft_year` SMALLINT, `draft_round` SMALLINT, `draft_supplemental` TINYINT, `draft_pick` SMALLINT, `draft_overall_pick` SMALLINT, `draft_eligible` TINYINT, `hidden` TINYINT, `draft_league_id` INT, `draft_team_id` INT, `turned_coach` TINYINT, `hall_of_fame` TINYINT, `local_pop` SMALLINT, `national_pop` SMALLINT, `draft_protected` TINYINT, `morale` SMALLINT, `morale_player_performance` SMALLINT, `morale_team_performance` SMALLINT, `morale_team_transactions` SMALLINT, `expectation` SMALLINT, `morale_player_role` SMALLINT,
  PRIMARY KEY (`player_id`),
  INDEX `players_ix1` (`team_id`),
  INDEX `players_ix2` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_career_batting_stats = '''CREATE TABLE IF NOT EXISTS `players_career_batting_stats` (`player_id` INT, `year` SMALLINT, `team_id` INT, `game_id` INT, `league_id` INT, `level_id` SMALLINT, `split_id` SMALLINT, `position` SMALLINT, `ab` SMALLINT, `h` SMALLINT, `k` SMALLINT, `pa` SMALLINT, `pitches_seen` SMALLINT, `g` SMALLINT, `gs` SMALLINT, `d` SMALLINT, `t` SMALLINT, `hr` SMALLINT, `r` SMALLINT, `rbi` SMALLINT, `sb` SMALLINT, `cs` SMALLINT, `bb` SMALLINT, `ibb` SMALLINT, `gdp` SMALLINT, `sh` SMALLINT, `sf` SMALLINT, `hp` SMALLINT, `ci` SMALLINT, `wpa` DOUBLE, `stint` SMALLINT, `ubr` DOUBLE, `war` DOUBLE,
  PRIMARY KEY (`player_id`,`year`,`team_id`,`split_id`,`stint`),
  INDEX `pcbs_ix1` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_career_fielding_stats = '''CREATE TABLE IF NOT EXISTS `players_career_fielding_stats` (`player_id` INT, `year` SMALLINT, `team_id` INT, `league_id` INT, `level_id` SMALLINT, `split_id` SMALLINT, `position` SMALLINT, `tc` SMALLINT, `a` SMALLINT, `po` SMALLINT, `er` SMALLINT, `ip` SMALLINT, `g` SMALLINT, `gs` SMALLINT, `e` SMALLINT, `dp` SMALLINT, `tp` SMALLINT, `pb` SMALLINT, `sba` SMALLINT, `rto` SMALLINT, `ipf` SMALLINT, `plays` SMALLINT, `plays_base` SMALLINT, `roe` SMALLINT, `opps_0` SMALLINT, `opps_made_0` SMALLINT, `opps_1` SMALLINT, `opps_made_1` SMALLINT, `opps_2` SMALLINT, `opps_made_2` SMALLINT, `opps_3` SMALLINT, `opps_made_3` SMALLINT, `opps_4` SMALLINT, `opps_made_4` SMALLINT, `opps_5` SMALLINT, `opps_made_5` SMALLINT, `zr` DOUBLE,
  PRIMARY KEY (`player_id`,`year`,`team_id`,`position`),
  INDEX `pcfs_ix1` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_career_pitching_stats = '''CREATE TABLE IF NOT EXISTS `players_career_pitching_stats` (`player_id` INT, `year` SMALLINT, `team_id` INT, `game_id` INT, `league_id` INT, `level_id` SMALLINT, `split_id` SMALLINT, `ip` SMALLINT, `ab` SMALLINT, `tb` SMALLINT, `ha` SMALLINT, `k` SMALLINT, `bf` SMALLINT, `rs` SMALLINT, `bb` SMALLINT, `r` SMALLINT, `er` SMALLINT, `gb` SMALLINT, `fb` SMALLINT, `pi` SMALLINT, `ipf` SMALLINT, `g` SMALLINT, `gs` SMALLINT, `w` SMALLINT, `l` SMALLINT, `s` SMALLINT, `sa` SMALLINT, `da` SMALLINT, `sh` SMALLINT, `sf` SMALLINT, `ta` SMALLINT, `hra` SMALLINT, `bk` SMALLINT, `ci` SMALLINT, `iw` SMALLINT, `wp` SMALLINT, `hp` SMALLINT, `gf` SMALLINT, `dp` SMALLINT, `qs` SMALLINT, `svo` SMALLINT, `bs` SMALLINT, `ra` SMALLINT, `cg` SMALLINT, `sho` SMALLINT, `sb` SMALLINT, `cs` SMALLINT, `hld` SMALLINT, `ir` DOUBLE, `irs` DOUBLE, `wpa` DOUBLE, `li` DOUBLE, `stint` SMALLINT, `outs` SMALLINT, `war` DOUBLE,
  PRIMARY KEY (`player_id`,`year`,`team_id`,`split_id`,`stint`),
  INDEX `pcps_ix1` (`league_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_individual_batting_stats = '''CREATE TABLE IF NOT EXISTS `players_individual_batting_stats` (`player_id` INT, `opponent_id` INT, `ab` SMALLINT, `h` SMALLINT, `hr` SMALLINT,
  PRIMARY KEY (`player_id`,`opponent_id`),
  INDEX `pibs_ix1` (`opponent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

states = '''CREATE TABLE IF NOT EXISTS `states` (`state_id` INT, `nation_id` INT, `name` VARCHAR(50), `abbreviation` VARCHAR(50), `population` INT, `main_language_id` INT, PRIMARY KEY (`state_id`, `nation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_affiliations = '''CREATE TABLE IF NOT EXISTS `team_affiliations` (`team_id` INT, `affiliated_team_id` INT, PRIMARY KEY (`team_id`, `affiliated_team_id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

team_history_financials = '''CREATE TABLE IF NOT EXISTS `team_history_financials` (`team_id` INT, `year` SMALLINT, `league_id` INT, `sub_league_id` INT, `division_id` INT, `gate_revenue` INT, `season_ticket_revenue` INT, `media_revenue` INT, `merchandising_revenue` INT, `revenue_sharing` INT, `playoff_revenue` INT, `cash` INT, `cash_owner` INT, `cash_trades` INT, `previous_balance` INT, `player_expenses` INT, `staff_expenses` INT, `stadium_expenses` INT, `season_tickets` INT, `attendance` INT, `fan_interest` SMALLINT, `fan_loyalty` SMALLINT, `fan_modifier` SMALLINT, `ticket_price` DOUBLE, `local_media_contract` INT, `local_media_contract_expires` INT, `national_media_contract` INT, `national_media_contract_expires` INT, `development_budget` INT, `draft_budget` INT, `draft_expenses` INT, `budget` INT, `market` SMALLINT, `owner_expectation` SMALLINT, `scouting_budget` INT, `scouting_amateur` INT, `scouting_major` INT, `scouting_minor` INT, `scouting_international` INT, PRIMARY KEY (`team_id`, `year`)) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

team_relations = '''CREATE TABLE IF NOT EXISTS `team_relations` (`league_id` INT, `sub_league_id` INT, `division_id` INT, `team_id` INT, PRIMARY KEY (`league_id`, `sub_league_id`, `division_id`, `team_id`)) ENGINE=InnoDB DEFAULT CHARSET=latin1
'''

players_batting = '''CREATE TABLE IF NOT EXISTS `players_batting` (`player_id` INT, `team_id` INT, `league_id` INT, `position` SMALLINT, `role` SMALLINT, `batting_ratings_overall_contact` SMALLINT, `batting_ratings_overall_gap` SMALLINT, `batting_ratings_overall_eye` SMALLINT, `batting_ratings_overall_strikeouts` SMALLINT, `batting_ratings_overall_hp` SMALLINT, `batting_ratings_overall_power` SMALLINT, `batting_ratings_overall_babip` SMALLINT, `batting_ratings_vsr_contact` SMALLINT, `batting_ratings_vsr_gap` SMALLINT, `batting_ratings_vsr_eye` SMALLINT, `batting_ratings_vsr_strikeouts` SMALLINT, `batting_ratings_vsr_hp` SMALLINT, `batting_ratings_vsr_power` SMALLINT, `batting_ratings_vsr_babip` SMALLINT, `batting_ratings_vsl_contact` SMALLINT, `batting_ratings_vsl_gap` SMALLINT, `batting_ratings_vsl_eye` SMALLINT, `batting_ratings_vsl_strikeouts` SMALLINT, `batting_ratings_vsl_hp` SMALLINT, `batting_ratings_vsl_power` SMALLINT, `batting_ratings_vsl_babip` SMALLINT, `batting_ratings_talent_contact` SMALLINT, `batting_ratings_talent_gap` SMALLINT, `batting_ratings_talent_eye` SMALLINT, `batting_ratings_talent_strikeouts` SMALLINT, `batting_ratings_talent_hp` SMALLINT, `batting_ratings_talent_power` SMALLINT, `batting_ratings_talent_babip` SMALLINT, `batting_ratings_misc_bunt` SMALLINT, `batting_ratings_misc_bunt_for_hit` SMALLINT, `batting_ratings_misc_gb_hitter_type` SMALLINT, `batting_ratings_misc_fb_hitter_type` SMALLINT, 
   PRIMARY KEY (player_id)
   )'''

players_contract = '''CREATE TABLE IF NOT EXISTS players_contract (
    `player_id` INT PRIMARY KEY,
    `team_id` INT,
    `league_id` INT,
    `position` INT(2),
    `role` INT (2),
    `is_major` INT(1),
    `no_trade` INT(1),
    `last_year_team_option` INT(1),
    `last_year_player_option` INT(1),
    `last_year_vesting_option` INT(1),
    `next_last_year_team_option` INT(1),
    `next_last_year_player_option` INT(1),
    `next_last_year_vesting_option` INT(1),
    `contract_team_id` INT (4),
    `contract_league_id` INT(4),
    `season_year` INT(4),
    `salary0` INT,
    `salary1` INT,
    `salary2` INT,
    `salary3` INT,
    `salary4` INT,
    `salary5` INT,
    `salary6` INT,
    `salary7` INT,
    `salary8` INT,
    `salary9` INT,
    `years` INT,
    `current_year` INT,
    `minimum_pa` INT,
    `minimum_pa_bonus` INT,
    `minimum_ip` INT,
    `minimum_ip_bonus` INT,
    `mvp_bonus` INT,
    `cyyoung_bonus` INT,
    `allstar_bonus` INT,
    `next_last_year_option_buyout` INT,
    `last_year_option_buyout` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_game_batting = '''CREATE TABLE IF NOT EXISTS players_game_batting (
`pgb_id` INT AUTO_INCREMENT PRIMARY KEY,
`player_id` INT,
`year` INT,
`team_id` INT,
`game_id` INT,
`league_id` INT,
`level_id` INT,
`split_id` INT,
`position` INT,
`ab` INT,
`h` INT,
`k` INT,
`pa` INT,
`pitches_seen` INT,
`g` INT,
`gs` INT,
`d` INT,
`t` INT,
`hr` INT,
`r` INT,
`rbi` INT,
`sb` INT,
`cs` INT,
`bb` INT,
`ibb` INT,
`gdp` INT,
`sh` INT,
`sf` INT,
`hp` INT,
`ci` INT,
`wpa` float,
`stint` INT,
`ubr` FLOAT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_game_pitching = '''CREATE TABLE IF NOT EXISTS players_game_pitching (
`pgp_id` INT AUTO_INCREMENT PRIMARY KEY,
`player_id` INT,
`year` INT,
`team_id` INT,
`game_id` INT,
`league_id` INT,
`level_id` INT,
`split_id` INT,
`ip` INT,
`ab` INT,
`tb` INT,
`ha` INT,
`k` INT,
`bf` INT,
`rs` INT,
`bb` INT,
`r` INT,
`er` INT,
`gb` INT,
`fb` INT,
`pi` INT,
`ipf` INT,
`g` INT,
`gs` INT,
`w` INT,
`l` INT,
`s` INT,
`sa` INT,
`da` INT,
`sh` INT,
`sf` INT,
`ta` INT,
`hra` INT,
`bk` INT,
`ci`INT,
`iw` INT,
`wp` INT,
`hp` INT,
`gf` INT,
`dp` INT,
`qs` INT,
`svo` INT,
`bs` INT,
`ra` INT,
`cg` INT,
`sho` INT,
`sb` INT,
`cs` INT,
`hld` INT,
`ir` INT,
`irs` INT,
`wpa` float,
`li` INT,
`stint` INT,
`outs` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_fielding_stats = '''CREATE TABLE IF NOT EXISTS team_fielding_stats (
`team_id` INT,
`year` INT,
`league_id` INT,
`level_id` INT,
`split_id` INT,
`position` INT,
`g` INT,
`gs` INT,
`tc` INT,
`a` INT,
`po` INT,
`e` INT,
`dp` INT,
`tp` INT,
`pb` INT,
`sba` INT,
`rto` INT,
`er` INT,
`ip` INT,
`ipf` INT,
`pct` float,
`range` float,
`rtop` float,
`cera` INT,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_history_fielding_stats = '''CREATE TABLE IF NOT EXISTS team_history_fielding_stats (
`team_id` INT,
`year` INT,
`league_id` INT,
`subleague_id` INT,
`division_id` iNT,
`level_id` INT,
`split_id` INT,
`position` INT,
`g` INT,
`gs` INT,
`tc` INT,
`a` INT,
`po` INT,
`e` INT,
`dp` INT,
`tp` INT,
`pb` INT,
`sba` INT,
`rto` INT,
`er` INT,
`ip` INT,
`ipf` INT,
`pct` float,
`range` float,
`rtop` float,
`cera` INT,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_roster_status = '''CREATE TABLE IF NOT EXISTS players_roster_status (
`player_id` INT PRIMARY KEY,
`team_id` INT,
`league_id` INT,
`position` INT,
`role` INT,
`uniform_number` INT,
`playing_level` INT,
`is_active` INT,
`is_on_secondary` INT,
`is_on_dl` INT,
`is_on_dl60` INT,
`must_be_active` INT,
`just_signed` INT,
`was_on_active` INT,
`was_on_secondary` INT,
`was_on_dl` INT,
`mlb_service_years` INT,
`secondary_service_years` INT,
`pro_service_years` INT,
`mlb_service_days` INT,
`secondary_service_days` INT,
`pro_service_days` INT,
`mlb_service_days_this_year` INT,
`secondary_service_days_this_year` INT,
`pro_service_days_this_year` INT,
`dl_days_this_year` INT,
`years_protected_from_rule_5` INT,
`is_on_waivers` INT,
`designated_for_assignment` INT,
`irrevocable_waivers` INT,
`days_on_waivers` INT,
`days_on_waivers_left` INT,
`days_on_dfa_left` INT,
`claimed_team_id` INT,
`last_day_on_waivers` INT,
`options_used` INT,
`option_used_this_year` INT,
`has_received_arbitration` INT,
`was_traded` INT,
`trade_status` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_history_batting_stats = '''CREATE TABLE IF NOT EXISTS team_history_batting_stats (
`team_id` INT,
`year` INT,
`league_id` INT,
`sub_league_id` INT,
`division_id` INT,
`level_id` INT,
`split_id` INT,
`pa` INT,
`ab` INT,
`h` INT,
`k` INT,
`tb` INT,
`s` INT,
`d` INT,
`t` INT,
`hr` INT,
`sb` INT,
`cs` INT,
`rbi` INT,
`r` INT,
`bb` INT,
`ibb` INT,
`hp` INT,
`sh` INT,
`sf` INT,
`ci` INT,
`gdp` INT,
`g` INT,
`gs` INT,
`ebh` INT,
`pitches_seen` INT,
`avg` float,
`obp` float,
`slg` float,
`rc` float,
`rc27` float,
`iso` float,
`woba` float,
`ops` float,
`sbp` float,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_financials = '''CREATE TABLE IF NOT EXISTS team_financials (
`team_id` INT PRIMARY KEY,
`gate_revenue` INT,
`season_ticket_revenue` INT,
`media_revenue` INT,
`merchandising_revenue` INT,
`revenue_sharing` INT,
`playoff_revenue` INT,
`cash` INT,
`cash_owner` INT,
`cash_trades` INT,
`previous_balance` INT,
`player_expenses` INT,
`staff_expenses` INT,
`stadium_expenses` INT,
`season_tickets` INT,
`attendance` INT,
`fan_interest` INT,
`fan_loyalty` INT,
`fan_modifier` INT,
`ticket_price` INT,
`local_media_contract` INT,
`local_media_contract_expires` INT,
`national_media_contract` INT,
`national_media_contract_expires` INT,
`scouting_budget` INT,
`development_budget` INT,
`draft_budget` INT,
`draft_expenses` INT,
`intl_fa_budget` INT,
`spent_in_intl` INT,
`budget` INT,
`market` INT,
`owner_expectation` INT,
`total_revenue` INT,
`total_expenses` INT,
`financial_balance` INT,
`budget_balance` INT,
`player_payroll` INT,
`player_payroll_next_season` INT,
`player_payroll_offered` INT,
`mode` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_batting_stats = '''CREATE TABLE IF NOT EXISTS team_batting_stats (
`team_id` INT(4),
`year` INT,
`league_id` INT,
`level_id` INT,
`split_id` INT,
`pa` INT,
`ab` INT,
`h` INT,
`k` INT,
`tb` INT,
`s` INT,
`d` INT,
`t` INT,
`hr` INT,
`sb` INT,
`cs` INT,
`rbi` INT,
`r` INT,
`bb` INT,
`ibb` INT,
`hp` INT,
`sh` INT,
`sf` INT,
`ci` INT,
`gdp` INT,
`g` INT,
`gs` INT,
`ebh` INT,
`pitches_seen` INT,
`avg` float,
`obp` float,
`slg` float,
`rc` float,
`rc27` float,
`iso` float,
`woba` float,
`ops` float,
`sbp` float,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_bullpen_pitching_stats = '''CREATE TABLE IF NOT EXISTS team_bullpen_pitching_stats (
`team_id` INT,
`year` INT,
`league_id` INT,
`level_id` INT,
`split_id` INT,
`ab` INT,
`ip` INT,
`bf` INT,
`tb` INT,
`ha` INT,
`k` INT,
`rs` INT,
`bb` INT,
`r` INT,
`er` INT,
`gb` INT,
`fb` INT,
`pi` INT,
`ipf` INT,
`g` INT,
`gs` INT,
`w` INT,
`l` INT,
`s` INT,
`sa` INT,
`da` INT,
`sh` INT,
`sf` INT,
`ta` INT,
`hra` INT,
`bk` INT,
`ci` INT,
`iw` INT,
`wp` INT,
`hp` INT,
`gf` INT,
`dp` INT,
`qs` INT,
`svo` INT,
`bs` INT,
`ra` INT,
`cg` INT,
`sho` INT,
`sb` INT,
`cs` INT,
`hld` INT,
`r9` INT,
`avg` INT,
`obp` INT,
`slg` INT,
`ops` INT,
`h9` float,
`k9` float,
`hr9` float,
`bb9` float,
`cgp` INT,
`fip` float,
`qsp` INT,
`winp` float,
`rsg` INT,
`svp` float,
`bsvp` float,
`gfp` float,
`era` float,
`pig` float,
`ws` INT,
`whip` float,
`gbfbp` float,
`kbb` float,
`babip` float,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_pitching_stats = '''CREATE TABLE team_pitching_stats LIKE team_bullpen_pitching_stats'''

team_starting_pitching_stats = '''CREATE TABLE team_starting_pitching_stats LIKE team_bullpen_pitching_stats'''

team_record = '''CREATE TABLE IF NOT EXISTS team_record (
`team_id` INT PRIMARY KEY,
`g` INT,
`w` INT,
`l` INT,
`pos` INT,
`pct` float,
`gb` float,
`streak` INT,
`magic_number` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_roster_staff = '''CREATE TABLE IF NOT EXISTS team_roster_staff (

`team_id` INT PRIMARY KEY,
`head_scout` INT,
`manager` INT,
`general_manager` INT,
`pitching_coach` INT,
`hitting_coach` INT,
`bench_coach` INT,
`owner` INT,
`doctor` INT
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

team_history_pitching_stats = '''CREATE TABLE IF NOT EXISTS team_history_pitching_stats (
`team_id` INT,
`year` INT,
`league_id` INT,
`sub_league_id` INT,
`division_id` INT,
`level_id` INT,
`split_id` INT,
`ab` INT,
`ip` INT,
`bf` INT,
`tb` INT,
`ha` INT,
`k` INT,
`rs` INT,
`bb` INT,
`r` INT,
`er` INT,
`gb` INT,
`fb` INT,
`pi` INT,
`ipf` INT,
`g` INT,
`gs` INT,
`w` INT,
`l` INT,
`s` INT,
`sa` INT,
`da` INT,
`sh` INT,
`sf` INT,
`ta` INT,
`hra` INT,
`bk` INT,
`ci` INT,
`iw` INT,
`wp` INT,
`hp` INT,
`gf` INT,
`dp` INT,
`qs` INT,
`svo` INT,
`bs` INT,
`ra` INT,
`cg` INT,
`sho` INT,
`sb` INT,
`cs` INT,
`hld` INT,
`r9` INT,
`avg` INT,
`obp` INT,
`slg` INT,
`ops` INT,
`h9` float,
`k9` float,
`hr9` float,
`bb9` float,
`cgp` INT,
`fip` float,
`qsp` INT,
`winp` float,
`rsg` INT,
`svp` float,
`bsvp` float,
`gfp` float,
`era` float,
`pig` float,
`ws` INT,
`whip` float,
`gbfbp` float,
`kbb` float,
`babip` float,
PRIMARY KEY(team_id, year)
)ENGINE=InnoDB DEFAULT CHARSET=latin1'''

players_fielding = '''CREATE TABLE IF NOT EXISTS `players_fielding` (`player_id` INT, `team_id` INT, `league_id` INT, `position` SMALLINT, `role` SMALLINT, `fielding_ratings_infield_range` SMALLINT, `fielding_ratings_infield_arm` SMALLINT, `fielding_ratings_turn_doubleplay` SMALLINT, `fielding_ratings_outfield_range` SMALLINT, `fielding_ratings_outfield_arm` SMALLINT, `fielding_ratings_catcher_arm` SMALLINT, `fielding_ratings_catcher_ability` SMALLINT, `fielding_ratings_infield_error` SMALLINT, `fielding_ratings_outfield_error` SMALLINT, `fielding_experience0` SMALLINT, `fielding_experience1` SMALLINT, `fielding_experience2` SMALLINT, `fielding_experience3` SMALLINT, `fielding_experience4` SMALLINT, `fielding_experience5` SMALLINT, `fielding_experience6` SMALLINT, `fielding_experience7` SMALLINT, `fielding_experience8` SMALLINT, `fielding_experience9` SMALLINT, `fielding_rating_pos1` SMALLINT, `fielding_rating_pos2` SMALLINT, `fielding_rating_pos3` SMALLINT, `fielding_rating_pos4` SMALLINT, `fielding_rating_pos5` SMALLINT, `fielding_rating_pos6` SMALLINT, `fielding_rating_pos7` SMALLINT, `fielding_rating_pos8` SMALLINT, `fielding_rating_pos9` SMALLINT,   PRIMARY KEY (player_id)
   )'''

players_pitching = '''CREATE TABLE IF NOT EXISTS `players_pitching` (`player_id` INT, `team_id` INT, `league_id` INT, `position` SMALLINT, `role` SMALLINT, `pitching_ratings_overall_stuff` SMALLINT, `pitching_ratings_overall_control` SMALLINT, `pitching_ratings_overall_movement` SMALLINT, `pitching_ratings_overall_balk` SMALLINT, `pitching_ratings_overall_hp` SMALLINT, `pitching_ratings_overall_wild_pitch` SMALLINT, `pitching_ratings_vsr_stuff` SMALLINT, `pitching_ratings_vsr_control` SMALLINT, `pitching_ratings_vsr_movement` SMALLINT, `pitching_ratings_vsr_balk` SMALLINT, `pitching_ratings_vsr_hp` SMALLINT, `pitching_ratings_vsr_wild_pitch` SMALLINT, `pitching_ratings_vsl_stuff` SMALLINT, `pitching_ratings_vsl_control` SMALLINT, `pitching_ratings_vsl_movement` SMALLINT, `pitching_ratings_vsl_balk` SMALLINT, `pitching_ratings_vsl_hp` SMALLINT, `pitching_ratings_vsl_wild_pitch` SMALLINT, `pitching_ratings_talent_stuff` SMALLINT, `pitching_ratings_talent_control` SMALLINT, `pitching_ratings_talent_movement` SMALLINT, `pitching_ratings_talent_balk` SMALLINT, `pitching_ratings_talent_hp` SMALLINT, `pitching_ratings_talent_wild_pitch` SMALLINT, `pitching_ratings_pitches_fastball` SMALLINT, `pitching_ratings_pitches_slider` SMALLINT, `pitching_ratings_pitches_curveball` SMALLINT, `pitching_ratings_pitches_screwball` SMALLINT, `pitching_ratings_pitches_forkball` SMALLINT, `pitching_ratings_pitches_changeup` SMALLINT, `pitching_ratings_pitches_sinker` SMALLINT, `pitching_ratings_pitches_splitter` SMALLINT, `pitching_ratings_pitches_knuckleball` SMALLINT, `pitching_ratings_pitches_cutter` SMALLINT, `pitching_ratings_pitches_circlechange` SMALLINT, `pitching_ratings_pitches_knucklecurve` SMALLINT, `pitching_ratings_pitches_talent_fastball` SMALLINT, `pitching_ratings_pitches_talent_slider` SMALLINT, `pitching_ratings_pitches_talent_curveball` SMALLINT, `pitching_ratings_pitches_talent_screwball` SMALLINT, `pitching_ratings_pitches_talent_forkball` SMALLINT, `pitching_ratings_pitches_talent_changeup` SMALLINT, `pitching_ratings_pitches_talent_sinker` SMALLINT, `pitching_ratings_pitches_talent_splitter` SMALLINT, `pitching_ratings_pitches_talent_knuckleball` SMALLINT, `pitching_ratings_pitches_talent_cutter` SMALLINT, `pitching_ratings_pitches_talent_circlechange` SMALLINT, `pitching_ratings_pitches_talent_knucklecurve` SMALLINT, `pitching_ratings_misc_velocity` SMALLINT, `pitching_ratings_misc_arm_slot` SMALLINT, `pitching_ratings_misc_stamina` SMALLINT, `pitching_ratings_misc_ground_fly` SMALLINT, `pitching_ratings_misc_hold` SMALLINT,
   PRIMARY KEY (player_id)
   )'''

awards = '''CREATE TABLE IF NOT EXISTS `awards` (
    `league_id` INT, `sub_league_id` SMALLINT, `year` SMALLINT, `best_hitter_id` INT, `best_pitcher_id` INT, `best_rookie_id` INT,`best_manager_id` INT,	`best_fielder_id0` INT,	`best_fielder_id1` INT, 	`best_fielder_id2`	INT, `best_fielder_id3` INT,	`best_fielder_id4` INT,	`best_fielder_id5` INT,	`best_fielder_id6` INT,	`best_fielder_id7` INT,	`best_fielder_id8` INT,	`best_fielder_id9` INT,
PRIMARY KEY (`league_id`, `sub_league_id`, `year`)
  )'''

games = '''CREATE TABLE IF NOT EXISTS `games` (
    `game_id` INT NOT NULL
    , `league_id` INT
    , `home_team` INT
    , `away_team` INT
    , `attendance` INT
    , `date` DATE
    , `time` INT
    , `game_type` TINYINT(1)
    , `played` TINYINT(1)
    , `dh` TINYINT(1)
    , `innings` TINYINT
    , `runs0` TINYINT
    , `runs1` TINYINT
    , `hits0` TINYINT
    , `hits1` TINYINT
    , `errors0` TINYINT
    , `errors1` TINYINT
    , `winning_pitcher` INT
    , `losing_pitcher` INT
    , `save_pitcher` INT
    , `starter0` INT
    , `starter1` INT,
PRIMARY KEY (`game_id`, `date`),
INDEX gix1 (`home_team`),
INDEX gix2 (`away_team`)
)'''

league_history_all_star = '''CREATE TABLE IF NOT EXISTS league_history_all_star (
    lh_as_id INT AUTO_INCREMENT PRIMARY KEY,
    `league_id` INT,
    `sub_league_id` INT,
    `year` INT (4),
    `all_star_pos` INT,
    `all_star` INT
) ENGINE=InnoDB DEFAULT CHARSET=latin1'''

coaches = '''CREATE TABLE IF NOT EXISTS `coaches` (
    `coach_id` INT NOT NULL PRIMARY KEY
    , `first_name` VARCHAR (50)
    , `last_name` VARCHAR (50)
    , `nick_name` VARCHAR (50)
    , `age` INT (2)
    , `date_of_birth` DATE
    , `city_of_birth_id` INT
    , `nation_id` INT
    , `weight` INT (3)
    , `height` INT (4)
    , `position` TINYINT (2)
    , `experience` TINYINT (2)
    , `occupation` TINYINT (2)
    , `team_id` INT
    , `former_player_id` INT
    , `contract_salary` INT
    , `contract_years` INT
    , `contract_extension_salary` INT
    , `contract_extension_years` INT
    , `scout_major` INT
    , `scout_minor` INT
    , `scout_international` INT
    , `scout_amateur` INT
    , `scout_amateur_preference` INT
    , `teach_hitting` INT
    , `teach_pitching` INT
    , `teach_fielding` INT
    , `handle_veterans` INT
    , `handle_rookies` INT
    , `handle_players` INT
    , `strategy_knowledge` INT
    , `heal_legs` INT
    , `heal_arms` INT
    , `heal_back` INT
    , `heal_other` INT
    , `heal_rest` INT
    , `management_style` INT
    , `personality` INT
    , `hitting_focus` INT
    , `pitching_focus` INT
    , `training_focus` INT
    , `teach_running` INT
    , `prevent_legs` INT
    , `prevent_arms` INT
    , `prevent_back` INT
    , `prevent_other` INT
    , `stealing` INT
    , `running` INT
    , `pinchrun` INT
    , `pinchhit_pos` INT
    , `pinchhit_pitch` INT
    , `hook_start` INT
    , `hook_relief` INT
    , `closer` INT
    , `lr_matchup` INT
    , `bunt_hit` INT
    , `bunt` INT
    , `hit_run` INT
    , `run_hit` INT
    , `squeeze` INT
    , `pitch_around` INT
    , `intentional_walk` INT
    , `hold_runner` INT
    , `guard_lines` INT
    , `infield_in` INT
    , `outfield_in` INT
    , `corners_in` INT
    , `shift_if` INT
    , `shift_of` INT
    , `opener` INT
    , `num_pitchers` INT
    , `num_hitters` INT
    , `favor_speed_to_power` INT
    , `favor_avg_to_obp` INT
    , `favor_defense_to_offense` INT
    , `favor_pitching_to_hitting` INT
    , `favor_veterans_to_prospects` INT
    , `trade_aggressiveness` INT
    , `player_loyalty` INT
    , `trade_frequency` INT
    , `trade_preference` INT
    , `value_stats` INT
    , `value_this_year` INT
    , `value_last_year` INT
    , `value_two_years` INT
    , `draft_value` INT
    , `intl_fa_value` INT
    , `develop_value` INT
    , `ratings_value` INT
    , `manager_value` INT
    , `pitching_coach_value` INT
    , `hitting_coach_value` INT
    , `scout_value` INT
    , `doctor_value` INT
    , INDEX c_ix1 (`team_id`)
    , INDEX c_ix2 (`former_player_id`)
    , INDEX c_ix3 (`occupation`)
    )'''

mgr_occupation = '''CREATE TABLE IF NOT EXISTS `mgr_occupation` (
    `occupation` TINYINT NOT NULL PRIMARY KEY
    , `occupation_name` VARCHAR (50)
    )'''

mgr_personality = '''CREATE TABLE IF NOT EXISTS `mgr_personality` (
    `personality` TINYINT NOT NULL PRIMARY KEY,
    `personality_name` VARCHAR (30)
    )'''

mgr_style = '''CREATE TABLE IF NOT EXISTS `management_style` (
    `management_style` INT NOT NULL PRIMARY KEY
    , `management_style_name` VARCHAR (30)
    )'''

hitting_focus = '''CREATE TABLE IF NOT EXISTS `hitting_focus` (
    `hitting_focus` INT NOT NULL PRIMARY KEY
    , `hitting_focus_name` VARCHAR (30)
    )'''

pitching_focus = '''CREATE TABLE IF NOT EXISTS `pitching_focus` (
    `pitching_focus` INT NOT NULL PRIMARY KEY
    , `pitching_focus_name` VARCHAR (30)
    )'''

team_history_record = '''CREATE TABLE IF NOT EXISTS `team_history_record` (
    `team_id` INT
    , `year` INT
    , `league_id` INT
    , `sub_league_id` INT
    , `division_id` INT
    , `g` INT
    , `w` INT
    , `l` INT
    , `pos` INT
    , `pct` DOUBLE
    , `gb` DOUBLE
    , `streak` INT
    , `magic_number` INT,
    CONSTRAINT pk_thr PRIMARY KEY (`team_id`, `year`)
    )'''

prob_starter = """CREATE TABLE IF NOT EXISTS `projected_starting_pitchers` (
    `team_id` INT PRIMARY KEY
    , starter_0 INT
    , starter_1 INT
    , starter_2 INT
    , starter_3 INT
    , starter_4 INT
    , starter_5 INT
    , starter_6 INT
    , starter_7 INT
    )"""

#  Remove columns from csv files prior to load
def remove_cols(path):
    path = Path(path)
    files = os.listdir(path)
    os.chdir(path)
    for file in files:
        if file == "cities.csv":
            columns_to_skip = ['main_language_id']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)
            print(file + ' modified...')

        if file == "league_history_pitching_stats.csv":
            columns_to_skip = ['kp', 'bbp', 'kbbp', 'ra9war', 'wpa', 'ws']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)
            print(file + ' modified...')

        elif file == "coaches.csv":
            columns_to_skip = ['quick_left', 'busy', 'type', 'data', 'days_left']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)
            print(file + ' modified...')
        elif file == "leagues.csv":
            columns_to_skip = ['language', 'gender', 'historical', 'logo_file_name', 'players_path',
                               'fictional_players', 'start_fantasy_draft', 'trading_deadline', 'winter_meetings',
                               'arbitration_offering', 'show_draft_pool', 'rosters_expanded', 'days_until_deadline',
                               'next_draft_type', 'league_state', 'stats_detail', 'historical_import_path',
                               'foreigner_percentage', 'was_ootp6', 'was_65', 'allstar_game', 'auto_schedule_allstar',
                               'allstar_team_id0', 'allstar_team_id1', 'schedule_file_1', 'schedule_file_2',
                               'rules_rule_5', 'rules_minor_league_options', 'rules_trading',
                               'rules_draft_pick_trading', 'rules_financials', 'rules_amateur_draft',
                               'rules_fa_compensation', 'rules_schedule_balanced', 'rules_schedule_inter_league',
                               'rules_schedule_force_start_day', 'rules_trades_other_leagues',
                               'rules_free_agents_from_other_leagues', 'rules_free_agents_leave_other_leagues',
                               'rules_allstar_game', 'rules_spring_training', 'rules_active_roster_limit',
                               'rules_secondary_roster_limit', 'rules_expanded_roster_limit', 'rules_min_service_days',
                               'rules_waiver_period_length', 'rules_dfa_period_length',
                               'rules_salary_arbitration_minimum_years', 'rules_minor_league_fa_minimum_years',
                               'rules_fa_minimum_years', 'rules_foreigner_limit', 'rules_foreigner_pitcher_limit',
                               'rules_foreigner_hitter_limit', 'rules_schedule_games_per_team',
                               'rules_schedule_typical_series', 'rules_schedule_preferred_start_day',
                               'rules_amateur_draft_rounds', 'rules_minimum_salary', 'rules_salary_cap',
                               'rules_player_salary0', 'rules_player_salary1', 'rules_player_salary2',
                               'rules_player_salary3', 'rules_player_salary4', 'rules_player_salary5',
                               'rules_player_salary6', 'rules_player_salary7', 'rules_average_coach_salary',
                               'rules_average_attendance', 'rules_average_national_media_contract',
                               'rules_cash_maximum', 'rules_average_ticket_price', 'rules_revenue_sharing',
                               'rules_national_media_contract_fixed', 'rules_owner_decides_budget',
                               'rules_schedule_auto_adjust_dates', 'rules_historical_import_rookies',
                               'avg_rating_contact', 'avg_rating_gap', 'avg_rating_power', 'avg_rating_eye',
                               'avg_rating_strikeouts', 'avg_rating_stuff', 'avg_rating_movement', 'avg_rating_control',
                               'avg_rating_fielding0', 'avg_rating_fielding1', 'avg_rating_fielding2',
                               'avg_rating_fielding3', 'avg_rating_fielding4', 'avg_rating_fielding5',
                               'avg_rating_fielding6', 'avg_rating_fielding7', 'avg_rating_fielding8',
                               'avg_rating_fielding9', 'avg_rating_overall', 'avg_rating_age', 'league_totals_ab',
                               'league_totals_h', 'league_totals_d', 'league_totals_t', 'league_totals_hr',
                               'league_totals_bb', 'league_totals_hp', 'league_totals_k', 'league_totals_pa',
                               'league_totals_babip', 'league_totals_mod_h', 'league_totals_mod_d',
                               'league_totals_mod_t', 'league_totals_mod_hr', 'league_totals_mod_bb',
                               'league_totals_mod_hp', 'league_totals_mod_k', 'league_totals_mod_babip',
                               'ml_equivalencies_avg', 'ml_equivalencies_hr', 'ml_equivalencies_eb',
                               'ml_equivalencies_bb', 'ml_equivalencies_k', 'ml_equivalencies_hp',
                               'player_creation_modifier_contact', 'player_creation_modifier_gap',
                               'player_creation_modifier_power', 'player_creation_modifier_eye',
                               'player_creation_modifier_strikeouts', 'player_creation_modifier_stuff',
                               'player_creation_modifier_movement', 'player_creation_modifier_control',
                               'player_creation_modifier_speed', 'player_creation_modifier_fielding',
                               'financial_coefficient', 'world_start_year', 'background_color_id', 'text_color_id',
                               'scouting_coach_id']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        elif file == "parks.csv":
            df = pd.read_csv(file, usecols=["park_id", "avg", "name", "capacity"])
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        elif file == "players.csv":
            columns_to_skip = ['rust', 'inducted', 'strategy_override_team', 'strategy_stealing', 'strategy_running',
                               'strategy_bunt_for_hit', 'strategy_sac_bunt', 'strategy_hit_run', 'strategy_hook_start',
                               'strategy_hook_relief', 'strategy_pitch_count', 'strategy_pitch_around',
                               'strategy_no_pinch_if_rested', 'strategy_never_pinch_hit', 'strategy_defensive_sub',
                               'strategy_dtd_sit_min', 'strategy_dtd_allow_ph']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)
            print(file + ' modified...')

        elif file == "teams.csv":
            df = pd.read_csv(file, usecols=["team_id", "name", "abbr", "nickname", "city_id", "park_id", "league_id", "sub_league_id", "division_id", "nation_id", "parent_team_id", "level"])
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')


        elif file == "players_at_bat_batting_stats.csv":
            df = pd.read_csv(file)
            df.insert(0, 'pabbs_id', range(1, 1+len(df)))
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        elif file == "players_game_batting.csv":
            df = pd.read_csv(file)
            df.insert(0, 'pgb_id', range(1, 1 + len(df)))
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        elif file == "players_game_pitching.csv":
            df = pd.read_csv(file)
            df.insert(0, 'pgp_id', range(1, 1 + len(df)))
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        elif file == "team_history_financials.csv":
            columns_to_skip = ['other_revenue']
            df = pd.read_csv(file, usecols=lambda x: x not in columns_to_skip)
            df.to_csv(file, index=False, header=True)

            print(file + ' modified...')

        else:
            print(file + ' unchanged...')

LeagueRunsPerOut = """CREATE TABLE IF NOT EXISTS LeagueRunsPerOut AS
SELECT p.year
, p.league_id
, p.sub_league_id
, sum(p.r) AS "totR"
, sum(p.outs) AS "totOuts"
, sum(p.outs)+sum(p.ha)+sum(p.bb)+ sum(p.iw)+ sum(p.sh)
   + sum(p.sf) AS "totPA"
, IF(sum(p.outs)=0,sum(p.r),SUM(p.r)/sum(p.outs)) AS "RperOut"
, IF(sum(p.outs)+sum(p.ha)+sum(p.bb)+ sum(p.iw)+ sum(p.sh)
   + sum(p.sf)=0,sum(p.r), round(sum(p.r)/(sum(p.outs)+sum(p.ha)+sum(p.bb)+ sum(p.iw)+ sum(p.sh)
   + sum(p.sf)),8)) AS "RperPA"
FROM players_career_pitching_stats AS p
GROUP BY p.year, p.league_id, p.sub_league_id"""

RunValues = """CREATE TABLE IF NOT EXISTS tblRunValues
AS SELECT year
, league_id
, sub_league_id
, RperOut
, @rb := round(RperOut+0.14,4) AS runBB
, round(@rb+0.025,4) AS runHB
, @rs := round(@rb+0.155,4) AS run1B
, @rd := round(@rs+0.3,4) AS run2B
, round(@rd+0.27,4) AS run3B
, 1.4 AS runHR
, 0.2 AS runSB
, 2*RperOut+0.075 AS runCS
FROM LeagueRunsPerOut"""

RunValues1A = """CREATE TABLE IF NOT EXISTS tblRunValues1A AS
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
   + run3B * t + 1.4 * HR + runSB * SB - runCS * CS)
   / SUM(AB - H + SF) AS runMinus

, SUM(runBB * (BB-IBB) + runHB * HP + run1B * s + run2B * d
   + run3B * t + 1.4 * HR + runSB * SB - runCS * CS)
   / SUM(BB-IBB + HP + H) AS runPlus

, SUM(H+BB-IBB+HP) / SUM(AB+BB-IBB+HP+SF) AS wOBA

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
, r.runCS

ORDER BY
r.year DESC"""

RunValues2 = """CREATE TABLE tblRunValues2 AS
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
, @ws := 1/(runPlus+runMinus) AS wOBAScale
, (runBB+runMinus)*@ws AS wobaBB
, (runHB+runMinus)*@ws AS wobaHB
, (run1B+runMinus)*@ws AS woba1B
, (run2B+runMinus)*@ws AS woba2B
, (run3B+runMinus)*@ws AS woba3B
, (runHR+runMinus)*@ws AS wobaHR
, runSB*@ws AS wobASB
, runCS*@ws AS wobaCS
FROM tblRunValues1A"""

FIPConstant = """CREATE TABLE IF NOT EXISTS FIPConstant AS

SELECT
      year
    , league_id
    , hra_totals/fb_totals AS hr_fb_pct
    , @HRAdj := 13*hra_totals AS Adjusted_HR
    , @BBAdj := 3*bb_totals AS Adjusted_BB
    , @HPAdj := 3*hp_totals AS Adjusted_HP
    , @KAdj  := 2*k_totals AS Adjusted_K
    , @InnPitch := ((ip_totals*3)+ipf_totals)/3 AS InnPitch
    , @lgERA := round((er_totals/@InnPitch)*9,2) AS lgERA
    , round(@lgERA - ((@HRAdj+@BBAdj+@HPAdj-@KAdj)/@InnPitch),2) AS FIPConstant
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
      ) AS x"""

sub_league_history_batting = """CREATE TABLE IF NOT EXISTS sub_league_history_batting AS

SELECT
       year
     , league_id
     , sub_league_id
     , slg_PA
     , slg_r

     FROM  (
     SELECT p.year
          , p.league_id
          , p.sub_league_id
          , sum(pa) AS slg_PA
          , sum(r) AS slg_r
     FROM players_career_batting_stats AS p INNER JOIN players ON p.player_id=players.player_id
     WHERE p.split_id=1 AND players.position<>1
     GROUP BY year, league_id, sub_league_id
      ) AS x """

sub_league_history_pitching = """CREATE TABLE IF NOT EXISTS sub_league_history_pitching AS

SELECT
       x.year
     , x.league_id
     , x.sub_league_id
     , IF(x.totIP=0,x.totER*9,round((x.totER/x.totIP)*9,2)) AS slgERA
     , IF(x.totIP=0,x.adjHRA + x.adjBB + x.adjHP - x.adjK, round((x.adjHRA + x.adjBB + x.adjHP - x.adjK)/x.totIP+f.FIPConstant,2)) AS slgFIP

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
        INNER JOIN FIPConstant AS f ON x.year=f.year AND x.league_id=f.league_id"""

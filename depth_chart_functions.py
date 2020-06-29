#  Functions to support depth charts

############################################
# SQL Statements for Depth Chart Functions #
############################################
#
# 1b
first_base = """SELECT 
      concat(p.first_name, " ", p.last_name) AS player
     ,p.age
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.pa
     , b.ba
     , b.obp
     , b.slg
     , b.woba
     , round(b.war,1) AS war
     , b.OBPplus
     , b.`wRC+`
     , f.fielding_ratings_infield_range AS `IF Range`
     , f.fielding_ratings_infield_arm AS `IF Arm`
     , f.fielding_ratings_turn_doubleplay AS `DP`
     , f.fielding_ratings_infield_error AS `IF Error`
     , f.fielding_rating_pos3 AS `1B Rating`
     , pb.batting_ratings_overall_contact AS `OVR Con`
     , pb.batting_ratings_overall_power AS `OVR Pwr`
     , pb.batting_ratings_overall_gap AS `OVR Gap`
     , pb.batting_ratings_overall_eye AS `OVR Eye`
     , pb.batting_ratings_overall_strikeouts AS `OVR K`
     , pb.batting_ratings_vsr_contact AS `Con VR`
     , pb.batting_ratings_vsr_power AS `Pow VR`
     , pb.batting_ratings_vsr_gap AS `Gap VR`
     , pb.batting_ratings_vsr_eye AS `Eye VR`
     , pb.batting_ratings_vsr_strikeouts AS `K VR`
     , pb.batting_ratings_vsl_contact AS `Con VL`
     , pb.batting_ratings_vsl_power AS `Pow VL`
     , pb.batting_ratings_vsl_gap AS `Gap VL`
     , pb.batting_ratings_vsl_eye AS `Eye VL`
     , pb.batting_ratings_vsl_strikeouts AS `K VL`
     FROM players AS p 
        INNER JOIN CalcBatting AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_fielding AS f ON p.player_id=f.player_id
        INNER JOIN players_batting AS pb ON p.player_id=pb.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
     WHERE b.year="""

org_language = " AND p.organization_id="

pos_language_1b = """ AND (p.position=3 OR f.fielding_rating_pos3 >=.5*(SELECT avg(f.fielding_rating_pos3) 
        FROM players_fielding f INNER JOIN players p ON f.player_id = p.player_id
        WHERE p.position=3))"""

order_language = " ORDER BY positions.pos_name, level_id, war desc"

#OF
outfield = """SELECT 
       concat(p.first_name, " ", p.last_name) AS player
     , p.age
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.pa
     , b.ba
     , b.obp
     , b.slg
     , b.woba
     , round(b.war,1) AS war
     , b.OBPplus
     , b.`wRC+`
     , f.fielding_ratings_outfield_range AS `OF Range`
     , f.fielding_ratings_outfield_arm AS `OF Arm`
     , f.fielding_ratings_outfield_error AS `OF Error`
     , f.fielding_experience7 AS `LF Rating`
     , f.fielding_experience8 AS `CF Rating`
     , f.fielding_experience9 AS `RF Rating`
     , pb.batting_ratings_overall_contact AS `OVR Con`
     , pb.batting_ratings_overall_power AS `OVR Pwr`
     , pb.batting_ratings_overall_gap AS `OVR Gap`
     , pb.batting_ratings_overall_eye AS `OVR Eye`
     , pb.batting_ratings_overall_strikeouts AS `OVR K`
     , pb.batting_ratings_vsr_contact AS `Con VR`
     , pb.batting_ratings_vsr_power AS `Pow VR`
     , pb.batting_ratings_vsr_gap AS `Gap VR`
     , pb.batting_ratings_vsr_eye AS `Eye VR`
     , pb.batting_ratings_vsr_strikeouts AS `K VR`
     , pb.batting_ratings_vsl_contact AS `Con VL`
     , pb.batting_ratings_vsl_power AS `Pow VL`
     , pb.batting_ratings_vsl_gap AS `Gap VL`
     , pb.batting_ratings_vsl_eye AS `Eye VL`
     , pb.batting_ratings_vsl_strikeouts AS `K VL`
     FROM players AS p 
     
        INNER JOIN CalcBatting AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_fielding AS f ON p.player_id=f.player_id
        INNER JOIN players_batting AS pb ON p.player_id=pb.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
        WHERE b.year=
     """
pos_language_of = """ AND p.position IN (7,8,9)"""

catcher = """SELECT concat(p.first_name, " ", p.last_name) AS player
     , p.age
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.pa
     , b.ba
     , b.obp
     , b.slg
     , b.woba
     , round(b.war,1) AS war
     , b.OBPplus
     , b.`wRC+`
     , f.fielding_ratings_catcher_arm AS `C Arm`
     , f.fielding_ratings_catcher_ability AS `C Abl`
     , f.fielding_rating_pos2 AS `C Rating`
     , pb.batting_ratings_overall_contact AS `OVR Con`
     , pb.batting_ratings_overall_power AS `OVR Pwr`
     , pb.batting_ratings_overall_gap AS `OVR Gap`
     , pb.batting_ratings_overall_eye AS `OVR Eye`
     , pb.batting_ratings_overall_strikeouts AS `OVR K`
     , pb.batting_ratings_vsr_contact AS `Con VR`
     , pb.batting_ratings_vsr_power AS `Pow VR`
     , pb.batting_ratings_vsr_gap AS `Gap VR`
     , pb.batting_ratings_vsr_eye AS `Eye VR`
     , pb.batting_ratings_vsr_strikeouts AS `K VR`
     , pb.batting_ratings_vsl_contact AS `Con VL`
     , pb.batting_ratings_vsl_power AS `Pow VL`
     , pb.batting_ratings_vsl_gap AS `Gap VL`
     , pb.batting_ratings_vsl_eye AS `Eye VL`
     , pb.batting_ratings_vsl_strikeouts AS `K VL`
     FROM players AS p 
        INNER JOIN CalcBatting AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_fielding AS f ON p.player_id=f.player_id
        INNER JOIN players_batting AS pb ON p.player_id=pb.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
        WHERE b.year="""

pos_language_c = " AND p.position=2"

#  Starting Pitcher
sp = """SELECT      
       concat(p.first_name, " ", p.last_name) AS player
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.g
     , round(b.InnPitch,1) AS IP
     , b.WHIP
     , b.k9
     , b.bb9
     , FIP
     , b.ERA
     , b.ERAminus AS `ERA-`
     , b.FIPminus AS `FIP-`
     , round(b.war,1) AS war
     , pp.pitching_ratings_misc_stamina AS `STA`
     , pp.pitching_ratings_overall_stuff AS `OVR Stu`
     , pp.pitching_ratings_overall_control AS `OVR Con`
     , pp.pitching_ratings_overall_movement AS `OVR Mov`
     , pp.pitching_ratings_vsr_stuff AS `Stu VR`
     , pp.pitching_ratings_vsr_control AS `Con VR`
     , pp.pitching_ratings_vsr_movement AS `Mov VR`
     , pp.pitching_ratings_vsl_stuff AS `Stu VL`
     , pp.pitching_ratings_vsl_control AS `Con VL`
     , pp.pitching_ratings_vsl_movement AS `Mov VL`
FROM players AS p 
        INNER JOIN CalcPitching AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_pitching AS pp ON p.player_id=pp.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
        WHERE b.year="""

pos_language_sp = " AND p.position=1 AND p.role=11"

pos_language_bp = " AND p.position=1 AND p.role IN (12,13)"

mi = """SELECT 
      concat(p.first_name, " ", p.last_name) AS player
     ,p.age
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.pa
     , b.ba
     , b.obp
     , b.slg
     , b.woba
     , round(b.war,1) AS war
     , b.OBPplus
     , b.`wRC+`
     , f.fielding_ratings_infield_range AS `IF Range`
     , f.fielding_ratings_infield_arm AS `IF Arm`
     , f.fielding_ratings_turn_doubleplay AS `DP`
     , f.fielding_ratings_infield_error AS `IF Error`
     , f.fielding_rating_pos4 AS `2B Rating`
     , f.fielding_rating_pos6 AS `SS Rating`
     , pb.batting_ratings_overall_contact AS `OVR Con`
     , pb.batting_ratings_overall_power AS `OVR Pwr`
     , pb.batting_ratings_overall_gap AS `OVR Gap`
     , pb.batting_ratings_overall_eye AS `OVR Eye`
     , pb.batting_ratings_overall_strikeouts AS `OVR K`
     , pb.batting_ratings_vsr_contact AS `Con VR`
     , pb.batting_ratings_vsr_power AS `Pow VR`
     , pb.batting_ratings_vsr_gap AS `Gap VR`
     , pb.batting_ratings_vsr_eye AS `Eye VR`
     , pb.batting_ratings_vsr_strikeouts AS `K VR`
     , pb.batting_ratings_vsl_contact AS `Con VL`
     , pb.batting_ratings_vsl_power AS `Pow VL`
     , pb.batting_ratings_vsl_gap AS `Gap VL`
     , pb.batting_ratings_vsl_eye AS `Eye VL`
     , pb.batting_ratings_vsl_strikeouts AS `K VL`
     FROM players AS p 
        INNER JOIN CalcBatting AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_fielding AS f ON p.player_id=f.player_id
        INNER JOIN players_batting AS pb ON p.player_id=pb.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
        WHERE b.year="""

pos_language_mi = " AND p.position IN (4,6)"

third_base = """SELECT 
      concat(p.first_name, " ", p.last_name) AS player
     ,p.age
     , positions.pos_name
     , teams.abbr
     , b.level_id
     , b.pa
     , b.ba
     , b.obp
     , b.slg
     , b.woba
     , round(b.war,1) AS war
     , b.OBPplus
     , b.`wRC+`
     , f.fielding_ratings_infield_range AS `IF Range`
     , f.fielding_ratings_infield_arm AS `IF Arm`
     , f.fielding_ratings_turn_doubleplay AS `DP`
     , f.fielding_ratings_infield_error AS `IF Error`
     , f.fielding_rating_pos5 AS `3B Rating`
     , pb.batting_ratings_overall_contact AS `OVR Con`
     , pb.batting_ratings_overall_power AS `OVR Pwr`
     , pb.batting_ratings_overall_gap AS `OVR Gap`
     , pb.batting_ratings_overall_eye AS `OVR Eye`
     , pb.batting_ratings_overall_strikeouts AS `OVR K`
     , pb.batting_ratings_vsr_contact AS `Con VR`
     , pb.batting_ratings_vsr_power AS `Pow VR`
     , pb.batting_ratings_vsr_gap AS `Gap VR`
     , pb.batting_ratings_vsr_eye AS `Eye VR`
     , pb.batting_ratings_vsr_strikeouts AS `K VR`
     , pb.batting_ratings_vsl_contact AS `Con VL`
     , pb.batting_ratings_vsl_power AS `Pow VL`
     , pb.batting_ratings_vsl_gap AS `Gap VL`
     , pb.batting_ratings_vsl_eye AS `Eye VL`
     , pb.batting_ratings_vsl_strikeouts AS `K VL`
 FROM players AS p      
        INNER JOIN CalcBatting AS b ON p.player_id=b.player_id AND p.team_id=b.team_id
        INNER JOIN leagues AS l ON b.league_id=l.league_id
        INNER JOIN positions ON p.position=positions.position AND p.role=positions.role
        INNER JOIN players_fielding AS f ON p.player_id=f.player_id
        INNER JOIN players_batting AS pb ON p.player_id=pb.player_id
        INNER JOIN teams ON p.team_id=teams.team_id AND b.team_id=teams.team_id
        WHERE b.year="""

pos_language_3b = pos_language_1b = """ AND (p.position=5 OR f.fielding_rating_pos5 >=.5*(SELECT avg(f.fielding_rating_pos5) 
        FROM players_fielding f INNER JOIN players p ON f.player_id = p.player_id
        WHERE p.position=5))"""

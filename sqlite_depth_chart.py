from prettytable import PrettyTable
import sqlite3
import xlsxwriter
from pathlib import Path
from _datetime import datetime
import sqlite_depth_chart_functions as dp
from os import remove

######################################
#        WHAT THIS MODULE DOES       #
######################################
#                                    #
# 1. Imports small_db.py and creates #
#    a small database in memory      #
# 2. Has the user select League and  #
#    organization for the depth chart#
# 3. Copies excel template with new  #
#    new name to output              #
# 4. Retrieves db data for depth chart
# 5. Writes to Excel and Formats     #
######################################

###################
# Create small_db #
###################
import small_db

#######################
# Connect to small_db #
#######################
try:
    cnx = sqlite3.connect('small_db')
    cursor = cnx.cursor()
    print("Successfully Connected to small_db")


except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)

##########################
# Select League and Team #
##########################
try:
    cursor.execute("SELECT league_id, name FROM leagues WHERE parent_league_id = 0")
except sqlite3.OperationalError:
    print("Exiting...")
    cnx.close()
    remove('small_db')
    exit()

league_list = cursor.fetchall()
valid_leagues = []
for pair in league_list:
    valid_leagues.append(str(pair[0]))

# - Make a Pretty Table to display ID and League
x = PrettyTable()
x.field_names = ['ID', 'League']
for item in league_list:
    x.add_row(item)
print(x)

# This bit to ensure that league_id is in league_list
league_id = ''
while league_id not in valid_leagues:
    if league_id == "quit" or league_id == "Quit":
        cnx.close()
        remove('small_db')
        exit()
    else:
        league_id = input("Enter the league of your choice (or 'Quit' to quit): ")

#  Get list of parent teams to select from
cursor.execute("""SELECT team_id, name || ' ' || nickname AS team
                    FROM teams
                    WHERE parent_team_id = 0 AND league_id=""" + str(league_id))
teams_list = cursor.fetchall()
valid_teams = []
for team in teams_list:
    valid_teams.append(str(team[0]))

# Make a Pretty Table
x = PrettyTable()
x.field_names = ['ID', 'Team']
for item in teams_list:
    x.add_row(item)
print(x)

#  Get org param
org_param = ''
while org_param not in valid_teams:
    if org_param == "quit" or org_param == "Quit":
        cnx.close()
        remove('small_db')
        exit()
    else:
        org_param = input("Enter the ID of the organization you want for your depth chart\n(Or 'quit' to exit) : ")

# Get org name
cursor.execute("SELECT name || ' ' || nickname FROM teams WHERE team_id=" + org_param)
result = cursor.fetchall()
team_name = result[0][0]

# Copy New xlsx with the Date and Org Name
str_date = datetime.strftime(small_db.game_date, '%m-%d-%Y')
new_file_name = team_name + "-" + str_date + '_depth_chart.xlsx'
# src_file = Path.cwd() / 'depth_chart_template.xlsx' # Not needed because xlswriter will create new workbook
dest_path = Path.cwd() / 'output'

# copy(src_file, dest_path)  # Not needed because xlswriter will create new workbook

###############################
#  xlsxwriter create workbook #
###############################
wb = xlsxwriter.Workbook(dest_path / new_file_name)

#####################
# xlsxwriter styles #
#####################
visible_header = wb.add_format({'bold': True, 'align': 'center', 'font_color': '#4472C4', 'bg_color': '#E7E6E6'})
invisible_header = wb.add_format({'font_color': '#D9D9D9', 'align': 'center'})
vis_table_style = wb.add_format({'align': 'center'})
vis_table_style.set_border(1)
invis_table_style = wb.add_format({'font_color': "white"})


#############################
#  Write to Excel Functions #
#############################

def write_depth(vis_headers, invis_headers, depth_chart):
    j = len(vis_headers)
    visible_table = []
    invisible_table = []
    for row in depth_chart:
        visible_table.append(row[0:j])
        invisible_table.append(row[j:])
    for k, data in enumerate(vis_headers):
        ws.write(0, k, data, visible_header)
    for k, data in enumerate(invis_headers):
        ws.write(0, j + k, data, invisible_header)
    for i, row_data in enumerate(visible_table):
        for k, col_data in enumerate(row_data):
            ws.write(i + 1, k, col_data, vis_table_style)
    for i, row_data in enumerate(invisible_table):
        for k, col_data in enumerate(row_data):
            ws.write(i + 1, j + k, col_data, invis_table_style)


##############
# First Base #
##############
ws = wb.add_worksheet('depthcahrt_1B')
cursor.execute(
    dp.first_base + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_1b + dp.order_language)
first_base_depth = cursor.fetchall()
batter_vis_header = ['player', 'age', 'pos_name', 'abbr', 'level_id', 'pa', 'ba', 'obp', 'slg', 'woba', 'war',
                     'OBPplus', 'wRAA']
first_base_invis_header = ['IF Range', 'IF Arm', 'DP', 'IF Error', '1B Rating', 'OVR Con', 'OVR Pwr',
                           'OVR Gap', 'OVR Eye', 'OVR K', 'Con VR', 'Pow VR', 'Gap VR', 'Eye VR', 'K VR', 'Con VL',
                           'Pow VL',
                           'Gap VL', 'Eye VL', 'K VL']

#  Write data beginning at Row 2
write_depth(batter_vis_header, first_base_invis_header, first_base_depth)

########################
#  Get OF Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_of')
cursor.execute(
    dp.outfield + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_of + dp.order_language)
of_depth = cursor.fetchall()
of_invis_header = ['OF Range', 'OF Arm', 'OF Error', 'LF Rating', 'CF Rating', 'RF Rating', 'OVR Con', 'OVR Pwr',
                   'OVR Gap', 'OVR Eye', 'OVR K', 'Con VR', 'Pow VR', 'Gap VR', 'Eye VR', 'K VR', 'Con VL', 'Pow VL',
                   'Gap VL', 'Eye VL', 'K VL']
#  Write Data
write_depth(batter_vis_header, of_invis_header, of_depth)

########################
#  Get C Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_c')
cursor.execute(
    dp.catcher + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_c + dp.order_language)
c_depth = cursor.fetchall()
c_invis_header = ['C Arm', 'C Abl', 'C Rating', 'OVR Con', 'OVR Pwr',
                  'OVR Gap', 'OVR Eye', 'OVR K', 'Con VR', 'Pow VR', 'Gap VR', 'Eye VR', 'K VR', 'Con VL', 'Pow VL',
                  'Gap VL', 'Eye VL', 'K VL']
#  Write Data
write_depth(batter_vis_header, c_invis_header, c_depth)


########################
#  Get MI Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_MI')
cursor.execute(dp.mi + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_mi + dp.order_language)
mi_depth = cursor.fetchall()
mi_invis_header = ['IF Range', 'IF Arm', 'DP', 'IF Error', '2B Rating', 'SS Rating', 'OVR Con', 'OVR Pwr',
                   'OVR Gap', 'OVR Eye', 'OVR K', 'Con VR', 'Pow VR', 'Gap VR', 'Eye VR', 'K VR', 'Con VL', 'Pow VL',
                   'Gap VL', 'Eye VL', 'K VL']
#  Write Data
write_depth(batter_vis_header, mi_invis_header, mi_depth)

########################
#  Get 3B Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_3B')
cursor.execute(
    dp.third_base + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_3b + dp.order_language)
third_base_depth = cursor.fetchall()
third_invis_header = ['IF Range', 'IF Arm', 'DP', 'IF Error', '3B Rating', 'OVR Con', 'OVR Pwr',
                      'OVR Gap', 'OVR Eye', 'OVR K', 'Con VR', 'Pow VR', 'Gap VR', 'Eye VR', 'K VR', 'Con VL', 'Pow VL',
                      'Gap VL', 'Eye VL', 'K VL']
#  Write Data
write_depth(batter_vis_header, third_invis_header, third_base_depth)

########################
#  Get SP Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_sp')
cursor.execute(dp.sp + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_sp + dp.order_language)
sp_depth = cursor.fetchall()
pitcher_vis_header = ['player', 'pos_name', 'abbr', 'level_id', 'g', 'IP', 'WHIP', 'k9', 'bb9', 'FIP', 'ERA', 'ERA-',
                      'FIP-', 'war']
p_invis_header = ['STA', 'OVR Stu', 'OVR Con', 'OVR Mov', 'Stu VR', 'Con VR', 'Mov VR', 'Stu VL', 'Con VL', 'Mov VL']
#  Write Data
write_depth(pitcher_vis_header, p_invis_header, sp_depth)

########################
#  Get BP Depth Chart  #
########################
ws = wb.add_worksheet('depthcahrt_bp')
cursor.execute(dp.sp + str(small_db.game_year) + dp.org_language + org_param + dp.pos_language_bp + dp.order_language)
bp_depth = cursor.fetchall()
#  Write Data
write_depth(pitcher_vis_header, p_invis_header, bp_depth)

# TEST SECTION
# print("TEST SECTION:")
# print(small_db.game_year)
# print(small_db.game_date)
# print("League ID: " + str(league_id))
# print("Org Param: " + str(org_param))
# print("Team Name: " + team_name)
# print("str_date: " + str_date)
# print("new file name: " + new_file_name)
# print(first_base_depth)
# print(wb.sheetnames)

# Close Everything Out
cnx.close()
remove('small_db')
wb.close()
terminate = input("All set!  Your depthchart is located in the 'output' directory.\nHit enter to exit. ")
if terminate:
    exit()

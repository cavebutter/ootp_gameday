import csv
import pandas as pd
import ootp_functions as ootp
import mysql.connector
from pathlib import Path
from _datetime import datetime


#  Look for the db configuration file and use the info to establish db connection\
path = Path.cwd() / 'db_config'
connection = input("What is the name of your database? ")
update_data = input("What is the location of your updated files? ")
datapath = Path(update_data)
config_file = connection + '.txt'
config = {}
with open(path / config_file) as f:
    for line in f:
        (key, val) = line.split(" ")
        config[key] = val

new_config = {'host': 'localhost', 'user': 'root','password': 'root', 'database': 'snoopy'}

try:
    mydb = mysql.connector.connect(**new_config)
    mycursor = mydb.cursor()

except mysql.connector.Error as err:
  print("Something went wrong: {}".format(err))

print("Formatting data files...")
#  ootp.remove_cols(datapath)   #  Uncomment this line when it's ready for production
print("Comparing Game Time Stamps")
league_file = 'leagues.csv'
df = pd.read_csv(datapath / league_file, usecols=["league_id", "current_date"])
league_date = df._get_value(0,'current_date')
league_date = datetime.strptime(league_date, '%Y-%m-%d').date()
mycursor.execute("SELECT max(curr_date) FROM leagues")
db_return = mycursor.fetchall()  # Is there a more elegant way to do this
db_date0 = db_return[0]          # This too
db_date = db_date0[0]            # This too
print("Your league's current date is " + str(league_date))
print("Your database's current date is " + str(db_date))
if league_date == db_date:
    print("You are current.  No update is needed.")
else:
    print("Let's update the database...")
    mycursor.execute("SHOW tables")
    tables = []
    for table in mycursor:
        for item in table:
            tables.append(item)

    print(tables)



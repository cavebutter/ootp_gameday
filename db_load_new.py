import mysql.connector
import os
from pathlib import Path
import csv


def db_load_new(connection_name, datapath):
    str_path = Path(datapath)

    mydb = mysql.connector.connect(host='localhost', user='root', password='root', database=connection_name)
    mycursor = mydb.cursor()

    os.chdir(str_path)
    # Get list of all files in the data directory
    files = [os.listdir(str_path)]
    full_path_files = []
    for file in files:
        for item in file:
            new_name = str(str_path) + item
            full_path_files.append(new_name)

    # Make list of filenames stripped of extensions - to be compared
    # against database table names
    just_filenames = []
    for file in full_path_files:
        strip = Path(file).stem
        just_filenames.append(strip)

    # Get list of tables in db
    mycursor.execute("SHOW tables")
    tables = []
    for table in mycursor:
        for item in table:
            tables.append(item)

    # Get the column names for each table that has a csv in the datasource
    for file in just_filenames:
        if file in tables:
            column_names = []
            values = "%s, "
            last_value = "%s)"
            mycursor.execute("SHOW columns FROM " + file)
            columns = [column[0] for column in mycursor.fetchall()]
            for column in columns:
                column_names.append(column)
            col_str = ","
            col_str = col_str.join(column_names)
            insert_statement = "INSERT INTO " + file + " (" + col_str + ") VALUES (" + values * (
                        len(column_names) - 1) + last_value
            with open(str_path / file, 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
                data.pop(0)
            print(insert_statement)
            mydb.commit()
            print(file + " data has been uploaded to database")



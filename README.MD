# OOTP Game Day Tools

## Description
OOTP Game Day Tools is a set of utilities to enhance the gameplay of Out of the Park Baseball. It was developed to work with OOTP 21 and forward, though it should work with version XX as well.

There are 3 utilities in this package:
* **Database** - Creates and updates a MySQL database for your OOTP save 
* **Depth Charts** - Creates an Excel Workbook showing organizational depth at each position
* **Game Day Workbooks** - Creates an Excel Workbook showing a team's stats against their next 7 probable starting pitchers, against their opponents' bullpens, and their current year L/R splits overall

**NOTE:** This is alpha software.  I have tested it on Windows and Mac and nothing has blown up.  However, I have not included much in the way of error handling.  This means, essentially, that if you fat finger a selection or enter a wrong path to your data, the application will just abend and you'll have to start over.  Nothing catastrophic, but just a heads up that this is less-than professional grade error handling at the moment.
## Specs and Requirements
* Version 0.9 is built in Python and does not have its own executable.  It requires the following non-standard libraries:
    - openpyxl
    - mysql.connector
    - prettytable
    - pandas
* MySQL Server
* Excel or comparable spreadsheet application

## Setup
1.  Ensure that Python and the above modules are installed.  
    - All modules are available to install via `pip` 
2. Ensure that you have access to a MySQL server
    - These utilities have been tested on both local and remote servers
    - *HOWEVER*, I strongly recommend a localhost, or at least a MySQL server where you have permission to set `max_allowed_packet`.  See MySQL section below.
3. Download the Game Day files and directories to your computer.
    - Either download or clone from GitHub

## Walkthru
1. Launch START_HERE.py
    - You will be presented with 3 options:
        - Database Stuff
        - Depth Charts
        - Game Day Workbook
    - If you're just starting out, you will need to set up your database, so enter "1"
    - You'll be asked if you are setting up a *NEW* database or updating an *EXISTING* one.
    - Enter "1" for New.
    
#### Create a New Database
* Enter the location of your data files.  
    - Data files refers to all of the csv's that the game generates when you export to CSV.  (See the game manual for information on how to dump data - I encourage you to NOT split large files, and to make sure that OSA ratings are included, and to export all tables.
    - Mac and Windows allow you to select a directory and copy its path.  I recommend you do this and paste it at the prompt.
* Enter a name for the new database.  This will be the actual name of the database as well as how you refer to it when you're making updates, depth charts, and game day books
* Enter the rest of your database credentials.
* The application will proceed to create the database, make some changes to the csv files and load the data to the database
* The application will create run value tables and use those tables to calculate advanced batting and pitching stats
* You're done!  You're now able to create depth charts, game day books, or just query the database to learn interesting things about your league.

#### Update a Database
*  Same process as for NEW with the following differences:
    1. You are not asked for database credentials - when you create a new database, your credentials are stored in a config file
    2. The tables in the current database are dropped and rebuilt.
    
**IMPORTANT NOTE ABOUT THE CONFIG FILE:** This file is not secure and is not meant to be.  Anyone with access to your computer can find this application directory, read the `config.ini` file and get the credentials to your database server.

#### Depth Charts
*  Enter the name of your database.
*  Once you're connected, you will be asked to choose the league that your team is in.  Enter the league ID.  Entering anything other than a league ID will cause an error
*  Once you choose your league, you will be asked to choose your team.  You may also see options for All-Star teams or Futures teams.  Selecting these probably won't produce results.  Again, enter the team id number only.  Anything else will cause an error.
*  An Excel workbook with the name format: `team name-YYYY-mm-dd_depth_chart.xlsx` will be created in the `output` sub-directory.

#### Game Day Workbooks
* Before you start, export the schedule for your team's league from the OOTP game.  Make a note of, and copy, the location.
* Enter the name of your database
* Once you're connected to the database, you'll choose your team's league by entering the league id...
* Then choose your team's id
* Paste the location of the schedule file when prompted
* An Excel workbook with the name format `team name_mm_dd_YYYY-mm_dd_YYYY.xlsx` will be created in the `output` subdirectory.


    
### MySQL Considerations
OOTP is a very data intensive game, and the OOTP development team makes much more efficient use of data within the application than it does with the data dumps it generates.  This creates some complications and forces some choices between performance and completeness of data.

In testing on a modern Windows 10 laptop, for example, a test data load of 5 years worth of data for 2 major leagues with full minors took just over 3 minutes for a localhost.  I was unable to complete a load or update on a remote host programmatically, becuase the packet size exceeded the server's limit and I do not have permission to change that limit.

This is the reason for the strong recommendation for a local MySQL server.  The other utilities will work fine with a remote server, but you will have to get your data into it outside of this toolset.

Future versions of this application may make some concessions in terms of completeness to accommodate remote servers.

If you don't already have MySQL server set up on your machine, and are interested in an easy, no-fuss implementation, I recommend MAMP.
This is a free tool that installs an Apache Web Server and MySQL server on your machine and makes the server accessible with an easy default login:
*localhost = 127.0.0.1 ; user = root ; password = root*.

##### Feedback
This application will continue to develop based on feedback I get from YOU.  I only want to help make this game that I love to be more enjoyable by increasing the nerd-factor.  Please reach out in the following ways:
* OOTP forums - user: cavebutter
* via Github
* via Twitter: @JayACohen

##### Support
If you find this application useful, please consider supporting independent open-source development.  
Venmo - @JayCo613
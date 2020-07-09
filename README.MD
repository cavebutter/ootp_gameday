# OOTP Game Day Tools

## Description
OOTP Game Day Tools is a set of utilities to enhance the gameplay of Out of the Park Baseball. It was developed to work with OOTP 21 and forward, though it should work with version XX as well.

There are 2 utilities in this package:
* **Depth Charts** - Creates an Excel Workbook showing organizational depth at each position
* **Game Day Workbooks** - Creates an Excel Workbook showing a team's stats against their next 7 probable starting pitchers, against their opponents' bullpens, and their current year L/R splits overall

**NOTE:** This is alpha software.  I have tested it on Windows and Mac and nothing has blown up.  However, I have not included only basic error handling.  This means, essentially, that you will likely find a way to error out it if you try to get too creative.  Nothing catastrophic, but just a heads up that this is less-than professional grade error handling at the moment.
## Specs and Requirements
* Excel or comparable spreadsheet application

## Setup
1. Download the Gameday zip file and extract it somewhere on your computer.

2. Double-click on gameday_utilities_home.exe

## Walkthru
1. Launch gameday_utilities_home.exe
    - You will be presented with 2 options:
        - Depth Charts
        - Game Day Workbook
    
#### Depth Charts
*  You will be asked for the location of your datafiles.  Copy/Paste it in.
*  Once you're connected, you will be asked to choose the league that your team is in.  Enter the league ID.  
*  Once you choose your league, you will be asked to choose your team.  You may also see options for All-Star teams or Futures teams.  Selecting these probably won't produce results.  
*  An Excel workbook with the name format: `team name-YYYY-mm-dd_depth_chart.xlsx` will be created in the `output` sub-directory.
*  All of charts on the depth chart tabs pull data from the first several rows of the tables on the left.  These can be sorted by any field by (in Excel) clicking the Data section of the ribbon and choosing Sort.  This will open a dialog box to choose the sorting fields.
*  Tip:  You can highlight cells and then sort by highlight color.

#### Game Day Workbooks
* Before you start, export the schedule for your team's league from the OOTP game.  Make a note of, and copy, the location.
*  You will be asked for the location of your datafiles.  Copy/Paste it in.
* Once you're connected to the database, you'll choose your team's league by entering the league id...
* Then choose your team's id
* Paste the location of the schedule file when prompted
* An Excel workbook with the name format `team name_mm_dd_YYYY-mm_dd_YYYY.xlsx` will be created in the `output` subdirectory.


##### Feedback
This application will continue to develop based on feedback I get from YOU.  I only want to help make this game that I love to be more enjoyable by increasing the nerd-factor.  Please reach out in the following ways:
* OOTP forums - user: cavebutter
* via Github
* via Twitter: @JayACohen

##### Support
If you find this application useful, please consider supporting independent open-source development.
Venmo - @JayCo613
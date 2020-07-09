action = '0'
while action not in ('1','2','3'):

    action = input("""What are we doing today?
    1 - Depth Charts
    2 - Gameday Workbook
    Enter a number 1-2 or 'quit' to quit:  """)

    if action == "1":
        import sqlite_depth_chart
    elif action == "2":
        import sqlite_gameday
    elif action == 'Quit' or action == 'quit':
        exit()

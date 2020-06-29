action = input("""What are we doing today?
1 - Database Stuff
2 - Depth Charts
3 - Gameday Workbook
Enter a number 1-3:  """)

if action == "1":
    import ootp
elif action == "2":
    import depth_chart
elif action == "3":
    import game_day
else:
    action = input("""What are we doing today?
    1 - Database Stuff
    2 - Depth Charts
    3 - Gameday Workbook
    Enter a number 1-3  """)
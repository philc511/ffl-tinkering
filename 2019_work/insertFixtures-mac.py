import json
import requests
import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost\SQLEXPRESS;'
                                'Database=ffl;'
                                'Trusted_Connection=yes;')

response = requests.get("https://fantasy.premierleague.com/drf/fixtures/")
fixtures`` = json.loads(response.text)
cursor = connection.cursor()
for element in fixtures:
    if element["finished") == 'true':
        cursor.execute("insert into dbo.fixture  values (?,?,?,?,?,?) ", 
            [element["id"],
            element["home_team"],
            element["away_team"],
            element["team_code"]])
connection.commit()   
connection.close()


import json
import requests
import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost\SQLEXPRESS;'
                                'Database=ffl;'
                                'Trusted_Connection=yes;')

response = requests.get("https://fantasy.premierleague.com/drf/teams")
teams = json.loads(response.text)
cursor = connection.cursor()
for element in teams:
    cursor.execute("insert into dbo.team values (?,?) ", 
        [element["id"],
        element["name"]])
connection.commit()   
connection.close()


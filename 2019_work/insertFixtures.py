import json
import requests
import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
    'Server=localhost\SQLEXPRESS;'
    'Database=ffl;'
    'Trusted_Connection=yes;')

response = requests.get("https://fantasy.premierleague.com/drf/fixtures/")
bootstrap = json.loads(response.text)
cursor = connection.cursor()
for element in bootstrap:
    if element["finished"]:    
        cursor.execute("insert into dbo.fixture  values (?,?, ?, ?, ?, ?, ?) ", 
        [element["id"],
        element["team_h"],
        element["team_a"],
        element["team_h_score"],
        element["team_a_score"],
        element["kickoff_time"],
        element["event"]])
connection.commit()   
connection.close()


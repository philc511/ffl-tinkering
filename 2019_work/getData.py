import json
import requests
import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
    'Server=localhost\SQLEXPRESS;'
    'Database=ffl;'
    'Trusted_Connection=yes;')

bootstrapResponse = requests.get("https://fantasy.premierleague.com/drf/bootstrap-static")
bootstrap = json.loads(bootstrapResponse.text)
cursor = connection.cursor()

for element in bootstrap["elements"]:
    print(element["id"])
    response = requests.get("https://fantasy.premierleague.com/drf/element-summary/"+str(element["id"]))
    summary = json.loads(response.text)
    for element in summary["history"]:
        if element["minutes"] > 0:    
            was_home = (element["was_home"] == 'True')
            cursor.execute("insert into dbo.player_fixture  values (?,?, ?, ?, ?) ", 
            [element["fixture"],
            element["element"],
            element["total_points"],
            element["minutes"],
            element["was_home"]])
connection.commit()   
connection.close()


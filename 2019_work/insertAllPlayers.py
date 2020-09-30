import json
import requests
import pypyodbc

connection = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost\SQLEXPRESS;'
                                'Database=ffl;'
                                'Trusted_Connection=yes;')

response = requests.get("https://fantasy.premierleague.com/drf/bootstrap-static")
bootstrap = json.loads(response.text)
cursor = connection.cursor()
for element in bootstrap["elements"]:
    cursor.execute("insert into dbo.player values (?,?, ?, ?, ?, ?) ", 
        [element["id"],
        element["first_name"],
        element["second_name"],
        element["team_code"],
        element["element_type"],
        element["now_cost"]])
connection.commit()   
connection.close()


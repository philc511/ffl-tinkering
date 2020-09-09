import json
import requests
import csv

response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
bootstrap = json.loads(response.text)
with open('2021_player_list.csv', mode='w') as player_list:
    player_writer = csv.writer(player_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    player_writer.writerow(["name", "playerid", "team", "cost", "position"])
    for element in bootstrap["elements"]:
        playerid = str(element["id"])
        name=element["first_name"] + "_" + element["second_name"]
        team=str(element["team"])
        cost=str(element["now_cost"])
        position=str(element["element_type"])
        player_writer.writerow([name, playerid, team, cost, position])

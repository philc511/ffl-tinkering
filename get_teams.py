import json
import requests
import csv
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_name = 'teams_' + now + '.csv'


response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
bootstrap = json.loads(response.text)
with open(output_name, mode='w') as team_list:
    team_writer = csv.writer(team_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    count = 0

    for team in bootstrap["teams"]:
        if count == 0:
            team_writer.writerow(team.keys())
            count += 1
        team_writer.writerow(team.values())

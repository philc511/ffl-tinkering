import json
import requests
import csv
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_name = 'players' + now + '.csv'


response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
bootstrap = json.loads(response.text)
with open(output_name, mode='w') as player_list:
    player_writer = csv.writer(player_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    count = 0

    for player in bootstrap["elements"]:
        if count == 0:
            player_writer.writerow(player.keys())
            count += 1
        player_writer.writerow(player.values())

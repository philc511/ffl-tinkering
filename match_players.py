import csv
players = {}
with open('2021_player_list.csv', mode='r') as player_list:
    with open('lockdown.csv', mode='r') as lockdown_list:
        with open('players_with_lockdown_points.csv', mode='w') as new_list:
            player_writer = csv.writer(new_list, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            player_writer.writerow(['name', 'playerid', 'team', 'cost', 'position', 'lockdown_points'])
            for player in csv.DictReader(player_list):
                players[player['name']]=player
            for lockdown_player in csv.DictReader(lockdown_list, fieldnames=['old_name','lockdown_points']):
                name = lockdown_player['old_name'].rsplit("_",1)[0]
                if name in players:
                    row = players[name]
                    player_writer.writerow([name, row['playerid'], row['team'], row['cost'], row['position'], lockdown_player['lockdown_points']])



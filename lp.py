import pulp 
import pandas
import re

players = pandas.read_csv('players_with_lockdown_points.csv', index_col=['playerid'])
players['goalkeeper'] = [int(players.loc[playerid, 'position'] == 1) for playerid in players.index]
players['defender'] = [int(players.loc[playerid, 'position'] == 2) for playerid in players.index]
players['midfielder'] = [int(players.loc[playerid, 'position'] == 3) for playerid in players.index]
players['forward'] = [int(players.loc[playerid, 'position'] == 4) for playerid in players.index]
players['not_playing'] = [int(
        players.loc[playerid, 'team'] == 2 
        or players.loc[playerid, 'team'] == 4 
        or players.loc[playerid, 'team'] == 12 
        or players.loc[playerid, 'team'] == 13  
        ) for playerid in players.index]
print(players)
print(players.loc[playerid,'lockdown_points'] for playerid in players.index)

prob = pulp.LpProblem("Fantasy", pulp.LpMaximize)
player_chosen = pulp.LpVariable.dicts("player_chosen", (playerid for playerid in players.index), cat='Binary')
    
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid,'lockdown_points'] for playerid in players.index])
prob += pulp.lpSum([player_chosen[playerid] for playerid in players.index]) == 15
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'goalkeeper'] for playerid in players.index]) == 2
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'defender'] for playerid in players.index]) == 5
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'midfielder'] for playerid in players.index]) == 5
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'forward'] for playerid in players.index]) == 3
prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'cost'] for playerid in players.index]) <= 1000

prob += pulp.lpSum([player_chosen[playerid] * players.loc[playerid, 'not_playing'] for playerid in players.index]) <= 0

prob.solve()

# summary(prob)
print(pulp.LpStatus[prob.status])
for player in player_chosen:
    if player_chosen[player].varValue == 1:
        print(players.loc[player, 'name'], players.loc[player, 'position'], players.loc[player, 'team'])

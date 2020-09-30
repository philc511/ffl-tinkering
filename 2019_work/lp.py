from pulp import *
import pandas
import re
import json
import requests

def summary(prob):
    div = '---------------------------------------\n'
    print("Variables:\n")
    score = str(prob.objective)
    constraints = [str(const) for const in prob.constraints.values()]
    for v in prob.variables():
        score = score.replace(v.name, str(v.varValue))
        constraints = [const.replace(v.name, str(v.varValue)) for const in constraints]
        if v.varValue != 0:
            print(v.name, "=", v.varValue)
    print(div)
    print("Constraints:")
    for constraint in constraints:
        constraint_pretty = " + ".join(re.findall("[0-9\.]*\*1.0", constraint))
        if constraint_pretty != "":
            print("{} = {}".format(constraint_pretty, eval(constraint_pretty)))
    print(div)
    print("Score:")
    score_pretty = " + ".join(re.findall("[0-9\.]+\*1.0", score))
    #print("{} = {}".format(score_pretty, eval(score)))
    print(score)

# element_type
# web_name
# now_cost
# total_points
response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
bootstrap = json.loads(response.text)

already_in_team = ["Pukki"]

data = {1: ['d', 'van dijk', 6, 9], 
        2: ['d', 'robertson', 5, 8],
        3: ['m', 'sterling', 7, 13],
        4: ['m', 'salah', 10, 15],
        5: ['f', 'firminho', 6, 10],
        6: ['f', 'pukki', 8, 12]
        }
elements = pandas.DataFrame.from_dict(bootstrap["elements"])
elements = elements.astype({"element_type": str})
elements = elements[elements["web_name"] != "Cantwell"]

#, columns=['pos','displayName','fee','points'])        
availables = elements[["element_type", "web_name", "now_cost",
  "total_points"]].groupby(["element_type", "web_name", "now_cost",
  "total_points"]).agg("count")
availables = availables.reset_index()
print(availables.head(3))


fees = {}
points = {}
for pos in availables.element_type.unique():
    available_pos = availables[availables.element_type == pos]
    fee = list(available_pos[["web_name","now_cost"]].set_index("web_name").to_dict().values())[0]
    point = list(available_pos[["web_name","total_points"]].set_index("web_name").to_dict().values())[0]
    fees[pos] = fee
    points[pos] = point
    
pos_num_available = {
    "1": 0,
    "2": 1,
    "3": 1,
    "4": 0
}
FEE_CAP = 127

_vars = {k: LpVariable.dict(k, v, cat="Binary") for k, v in points.items()}

prob = LpProblem("Fantasy", LpMaximize)
rewards = []
costs = []
position_constraints = []
for k, v in _vars.items():
    costs += lpSum([fees[k][i] * _vars[k][i] for i in v])
    rewards += lpSum([points[k][i] * _vars[k][i] for i in v])
    prob += lpSum([_vars[k][i] for i in v]) == pos_num_available[k]
    
prob += lpSum(rewards)
prob += lpSum(costs) <= FEE_CAP

prob.solve()

summary(prob)
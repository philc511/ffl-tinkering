import json
import requests

response = requests.get("https://fantasy.premierleague.com/drf/bootstrap-static")
bootstrap = json.loads(response.text)
for element in bootstrap["elements"]:
    print(element["first_name"])


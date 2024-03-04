import requests
import json

url = 'https://trade.erd.ai/robot/api/v1/portfolio/000/1032887'
headers = {'X-API-KEY': '907E0507067041318FBD5248250E4EF1'}
response = requests.get(url, headers=headers)

print(json.dumps(response.json(), indent=4))

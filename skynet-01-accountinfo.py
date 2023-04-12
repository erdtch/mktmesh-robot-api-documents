import requests
import json

url = 'http://122.8.148.106/api/v1/account/000/1032887'
headers = {'X-API-KEY': '907E0507067041318FBD5248250E4EF1'}
response = requests.get(url, headers=headers)

print(json.dumps(response.json(), indent=4))

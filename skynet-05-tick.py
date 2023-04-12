import requests


url = 'http://122.8.148.106/api/v1/data/tick/000/1032887/?symbol=PTT&startTime=2018-08-01 00:00:00&endTime=2018-08-10 00:00:00'
headers = {'X-API-KEY': '907E0507067041318FBD5248250E4EF1'}
response = requests.get(url, headers=headers)

print(response.text)
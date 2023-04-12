import requests

# http://122.8.148.106/api/v1/symbol/{brokerCode}/{accountNo}?symbol=<symbol>
my_headers = {'X-API-KEY' : '1AFD14813B4EC7AC52FF93B380FAB2891'}
response = requests.get("http://122.8.148.106/api/v1/symbol/900/1032887?symbol=PTT", headers=my_headers)
print(response.json())
print(response.json()['orderBookId'])

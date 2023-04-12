import requests
import json

# real url content with key
endpoint = 'http://122.8.148.106/api/v1/cancelOrder/000'
headers = {
        'Content-Type' : 'application/json',
        'X-API-KEY': '907E0507067041318FBD5248250E4EF1',
        }

data = {}
data['accountNo'] = '1032887'
data['orderNo'] = '5213'
data['symbol'] = 'AOT'
data['side'] = 'LONG'
data['priceType'] = 'LIMIT'
print(data)
json_data = json.dumps(data)

response = requests.post(url = endpoint, headers=headers, data=json_data)
print(json.dumps(response.json(), indent=4))
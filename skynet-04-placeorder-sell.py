import requests
import json

# real url content with key
endpoint = 'https://trade.erd.ai/robot/api/v1/placeOrder/000'
headers = {
        'Content-Type' : 'application/json',
        'X-API-KEY': '907E0507067041318FBD5248250E4EF1',
        }

data = {}
data['accountNo'] = '1032887'
data['symbol'] = 'AOT'
data['volume'] = 100
data['position'] = 'C'
data['side'] = 'SHORT'
data['price'] = 50.50
data['priceType'] = 'LIMIT'
print(data)
json_data = json.dumps(data)

response = requests.post(url = endpoint, headers=headers, data=json_data)
print(json.dumps(response.json(), indent=4))
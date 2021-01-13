import requests
#yc iam create-token
url = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
payload = open("body.json")
headers = {'Content-type': 'application/json', 'Authorization': 'Api-Key AQVNwMEN67VR3B6aNrk-1PG5SBA9KtDeeKRxtzGo'}
r = requests.post(url, data=payload, headers=headers)
print (r.text)
print (r.json)
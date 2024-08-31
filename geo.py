import requests
import json

send_url = "http://api.ipstack.com/check?access_key=54fb9b7572msh379005da4331487p1e99d0jsn5583a3aa2af4"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
latitude = geo_json['latitude']
longitude = geo_json['longitude']
city = geo_json['city']

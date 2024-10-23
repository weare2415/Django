import requests
import json

def get_location():
    API_KEY = ""

    url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}'

    data = {
        'considerIp': True,
    }

    result = requests.post(url, data) 
    location = json.loads(result.text)

    lat = location["location"]["lat"]
    lng = location["location"]["lng"]
    
    return lat, lng
    # print(lat, lng)
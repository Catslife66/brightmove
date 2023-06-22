import requests
from urllib.parse import urlencode


def get_location_coordinates(address, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {'address': address, 'key': api_key}
    url_params = urlencode(params)
    url = f"{endpoint}{url_params}"
    response = requests.get(url)
    if response.status_code in range(200, 299):
        data = response.json()
        result = data['results'][0]['geometry']['location']
        return result
    else:
        return None
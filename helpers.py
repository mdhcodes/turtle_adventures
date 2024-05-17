# Install requests
# https://requests.readthedocs.io/en/latest/user/install/
import requests
import urllib
import uuid


def get_parks():
    """Search NYC Parks Properties API"""

    # API request - Parks Properties
    url = "https://data.cityofnewyork.us/resource/enfh-gkve.json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    return data


# https://stackoverflow.com/questions/11479816/what-is-the-python-equivalent-for-a-case-switch-statement
# https://stackoverflow.com/questions/72808275/using-python-functions-in-a-flask-template
# Display full Borough name
def borough_name(name):
    match name:
        case 'B':
            return 'Brooklyn'
        case 'X':
            return 'Bronx'
        case 'M':
            return 'Manhattan'
        case 'Q':
            return 'Queens'
        case 'R':
            return 'Staten Island'


def find_borough(name):
    """Search NYC Parks Properties API by Borough"""

    print('Name:', name)

    # API request - Parks Properties
    url = f"https://data.cityofnewyork.us/resource/enfh-gkve.json?borough={urllib.parse.quote_plus(name)}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
        
    data = response.json()
        
    return data
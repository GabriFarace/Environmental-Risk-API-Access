import requests
from utility.constants import *

def get_coordinates(city: str, state: str, country: str)-> tuple:
    ''' Return the geographic coordinates (Latitude, Longitude) of a city by calling the Openweathermap API'''
    try:
        # Prepare the request URL
        params = {
            'q': f"{city},{country}",
            'limit': 1,
            'appid': OPENWHEATHER_API_KEY
        }

        # Send the GET request
        response = requests.get(OPENWHEATHER_BASE_URL, params=params)

        # If the response is successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Return the latitude and longitude
                return data[0]['lat'], data[0]['lon']
            else:
                print(f"Coordinates not found for {city}, {state}, {country}")
                return None, None
        else:
            print(f"Failed to fetch data for {city}, {state}, {country}")
            return None, None
    except Exception as e:
        print(f"Error fetching data for {city}, {state}, {country}: {e}")
        return None, None
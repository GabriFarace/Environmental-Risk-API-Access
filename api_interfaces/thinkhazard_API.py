import requests
from utility.cities_coordinates import find_closest_city
from utility.constants import *



def get_risk_level(longitude: float, latitude: float, risk_type: str):
    ''' Return the hazard data of the geographic location given by (latitude, longitude) by accessing the ThinkHazard API'''

    # Step 1: Find the closest city and get its ADM2 code
    closest_city = find_closest_city(latitude, longitude, CITIES_WITH_COORDINATES)

    if closest_city:
        adm2_code, city_name = closest_city
        print(f"Closest City: {city_name}, ADM2 Code: {adm2_code}")

        # Step 2: Use the ADM2 code to get hazard data from the ThinkHazard API
        hazard_data = get_hazard_data(adm2_code)

        # Step 3: return the hazard level associated to the requested risk_type
        if hazard_data:
            hazard_level = None
            for hazard in hazard_data:
                hazard_type = hazard['hazardtype']['hazardtype']
                if hazard_type == risk_type:
                    hazard_level = hazard['hazardlevel']['title']
                    break
            if hazard_level:
                return hazard_level
            else:
                return None
        else:
            # No hazard data found.
            return None
    else:
        # No closest city found
        return None

def get_hazard_data(adm2_code):
    ''' Call the ThinkHazardAPI and return the hazard data'''
    url = f"{THINKHAZARD_BASE_URL}/report/{adm2_code}.json"

    try:
        # Make the GET request to the ThinkHazard API
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            # Return the JSON data
            return response.json()
        else:
            # Failed to fetch hazard data for ADM2 code {adm2_code}
            return None
    except Exception as e:
        # Error fetching hazard data for ADM2 code {adm2_code}
        return None
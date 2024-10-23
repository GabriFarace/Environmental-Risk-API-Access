import requests
import threading
from risk_getters.enumerations import EnvironmentalRisk
from utility.cities_coordinates import find_closest_city
from utility.constants import *


class ThinkHazardAPI:
    def __init__(self):
        # current data mantains for a day the hazard risk indicators for a particular location given by (longitude, latitude)
        self.current_data = {} # Keys = (longitude, latitude) values = {risk_type : hazard_level,...}
        self.hazard_level_enum_map = {"Very Low" : EnvironmentalRisk.VERY_LOW, "Low" : EnvironmentalRisk.LOW, "Medium" : EnvironmentalRisk.MEDIUM, "High" : EnvironmentalRisk.HIGH}

    def get_risk_level(self, longitude: float, latitude: float, risk_type: str):
        ''' Return the risk level of a specific risk_type of the geographic location given by (latitude, longitude) by accessing the ThinkHazard API'''

        # If data is not already available then fetch it from the API
        if  (longitude, latitude) not in self.current_data.keys():

            # Step 1: Find the closest city to the location given by (latitude, longitude) and get its ADM2 code
            closest_city = find_closest_city(latitude, longitude, CITIES_WITH_COORDINATES)

            if closest_city:
                adm2_code, city_name = closest_city
                print(f"Closest City: {city_name}, ADM2 Code: {adm2_code}")

                # Step 2: Use the ADM2 code to get hazard data from the ThinkHazard API
                hazard_data = self._get_hazard_data(adm2_code)

                # Step 3: extract and return the hazard level associated to the requested risk_type
                if hazard_data:
                    hazard_dict = {item['hazardtype']['hazardtype']: self.hazard_level_enum_map[item['hazardlevel']['title']] for item in hazard_data}
                    self.current_data[(longitude, latitude)] =  hazard_dict

                    # Reset the current data for this location after 1 day
                    timer = threading.Timer(86400, self.reset_value, [(longitude, latitude)])
                    timer.start()
                    if not risk_type in hazard_dict.keys():
                        return EnvironmentalRisk.NO_DATA
                    else:
                        return hazard_dict[risk_type]
                else:
                    # No hazard data found.
                    return EnvironmentalRisk.NO_DATA
            else:
                # No closest city found
                return EnvironmentalRisk.NO_DATA

        else:
            if not risk_type in self.current_data[(longitude, latitude)].keys():
                return EnvironmentalRisk.NO_DATA
            else:
                return self.current_data[(longitude, latitude)][risk_type]

    def reset_value(self, location):
        ''' Reset the value for a location after 1 day'''
        del self.current_data[location]

    def _get_hazard_data(self, adm2_code):
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
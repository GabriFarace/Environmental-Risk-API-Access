import requests
from utility.constants import *


def get_carbon_intensity(longitude, latitude):
    ''' Get the carbon emission factors of the geographic location associated to (longitude, latitude) by calling
        The Electricity Maps API'''

    # Set the URL for the Electricity Maps API
    url = ELECTRICITYMAPS_BASE_URL + '/v3/carbon-intensity/latest'

    # Define the query parameters (longitude and latitude)
    params = {
        'lon': longitude,
        'lat': latitude
    }

    # Define the headers, including the auth-token with the API key
    headers = {
        'auth-token': ELECTRICITYMAPS_API_KEY
    }

    try:
        # Send the GET request to the API
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the carbon intensity factor from the response
            carbon_intensity = data.get('carbonIntensity', None)

            if carbon_intensity is not None:
                return carbon_intensity
            else:
                print("Carbon intensity data not available for this region.")
                return None
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}, Message: {response.text}")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None



def main():

    done = False
    while not done:
        latitude = float(input("\n Insert Latitude : "))
        longitude = float(input("\n Insert Longitude : "))

        # Call the function
        carbon_intensity = get_carbon_intensity(longitude, latitude)
        print(f"Carbon Intensity: {carbon_intensity} gCO2eq/kWh")

        choice = input("Do you want to continue? [Y/N] ")
        done = True if choice == "N" else False



if __name__ == "__main__":
    main()
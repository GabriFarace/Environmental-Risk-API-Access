import csv
import requests
from haversine import haversine, Unit
import time
from constants import *



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



def process_csv(input_csv: str, output_csv: str):
    ''' Process the input csv and write the output csv which contains the coordinates for each city '''
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='',
                                                                            encoding='utf-8') as outfile:
        # Read the CSV
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        # Write the header for the output CSV
        writer.writerow(['ADM2 Code', 'City', 'ADM1 Code', 'State', 'ADM0 Code', 'Country', 'Latitude', 'Longitude'])

        # Iterate through each row in the input CSV
        for row in reader:
            adm2_code, city, adm1_code, state, adm0_code, country = row

            if country == "Italy":
                # Fetch the coordinates using the OpenWeather API
                latitude, longitude = get_coordinates(city, state, "IT")

                if not any(l is None for l in (latitude, longitude)):
                # Add the coordinates to the row
                    writer.writerow([adm2_code, city, adm1_code, state, adm0_code, country, latitude, longitude])


            #time.sleep(1)  # Sleep for 1 second between requests to avoid hitting API limits



def find_closest_city(latitude: float, longitude: float, cities_file: str) -> tuple[str, str]:
    ''' Return the closest city (and associated administrative unit code) to the geographical coordinates (longitude,latitude)'''
    closest_city = None
    min_distance = float('inf')  # Initialize with a very large number

    with open(cities_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip the header row

        for row in reader:
            adm2_code, city, adm1_code, state, adm0_code, country, city_latitude, city_longitude = row
            # Convert latitude and longitude to float
            city_latitude = float(city_latitude)
            city_longitude = float(city_longitude)

            # Calculate the distance between the input coordinates and the city's coordinates
            distance = haversine((latitude, longitude), (city_latitude, city_longitude), unit=Unit.KILOMETERS)

            # Check if this city is closer than the previous closest one
            if distance < min_distance:
                min_distance = distance
                closest_city = (adm2_code, city)

    # Return the closest city's administrative unit 2 code and city name
    return closest_city

def read_file_main():
    input_csv = CITIES  # Input CSV file containing the cities
    output_csv = CITIES_WITH_COORDINATES  # Output CSV file to store cities with coordinates
    process_csv(input_csv, output_csv)

def find_city_main():
    latitude = 45.611946 #Castellanza (Varese)
    longitude = 8.898276 #Castellanza (Varese)
    cities_file = CITIES_WITH_COORDINATES
    print(find_closest_city(latitude, longitude, cities_file))

# Main function to run the script
if __name__ == '__main__':
    read_file_main()

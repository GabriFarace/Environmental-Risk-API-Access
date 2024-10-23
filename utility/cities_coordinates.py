import csv
import requests
import time

# Replace with your actual OpenWeather API key
API_KEY = '4c4853d32ca66defd0f20d907498dc2c'

# Base URL for the OpenWeather Geocoding API
BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"


# Function to get coordinates for a given city, state, and country
def get_coordinates(city, state, country):
    try:
        # Prepare the request URL
        params = {
            'q': f"{city},{country}",
            'limit': 1,
            'appid': API_KEY
        }

        # Send the GET request
        response = requests.get(BASE_URL, params=params)

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


# Function to process the CSV and get coordinates for each city
def process_csv(input_csv, output_csv):
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
            if (country == "Italy"):

                # Fetch the coordinates using the OpenWeather API
                latitude, longitude = get_coordinates(city, state, "IT")

                # Add the coordinates to the row
                writer.writerow([adm2_code, city, adm1_code, state, adm0_code, country, latitude, longitude])

            # Respect the API rate limit (you may need to adjust this based on your API plan)
            #time.sleep(1)  # Sleep for 1 second between requests to avoid hitting API limits


# Main function to run the script
if __name__ == '__main__':
    input_csv = 'ADM2_TH.csv'  # Input CSV file containing the cities
    output_csv = 'cities_with_coordinates.csv'  # Output CSV file to store results
    process_csv(input_csv, output_csv)

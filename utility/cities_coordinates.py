import csv
from api_interfaces.openwheather_API import get_coordinates
from constants import *
from haversine import haversine, Unit


def process_csv_codes(input_csv: str, output_csv: str):
    ''' Process the input csv and write the output csv which contains the coordinates for each city '''
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, open(output_csv, 'w', newline='',
                                                                            encoding='utf-8') as outfile:
        # Read the CSV
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        # read the code mapper csv
        with open("../iso_3166_1_alpha_2.csv", 'r', newline='', encoding='utf-8') as codes_file:
            # Read the CSV
            reader_codes = csv.reader(codes_file, delimiter=',')
            mapper = {}
            for row in reader_codes:
                country_name, code = row
                mapper[country_name] = code


        # Write the header for the output CSV
        writer.writerow(['ADM2 Code', 'City', 'ADM1 Code', 'State', 'ADM0 Code', 'Country', 'Country Code'])

        # Iterate through each row in the input CSV
        for row in reader:
            adm2_code, city, adm1_code, state, adm0_code, country = row

            country_code = mapper.get(country, None)
            if country_code is None:
                print(f"No country code for the following country : {country}")
            else:
                writer.writerow([adm2_code, city, adm1_code, state, adm0_code, country, country_code])


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

def find_closest_city(latitude: float, longitude: float) -> tuple[str, str]:
    ''' Return the closest city (and associated administrative unit code) to the geographical coordinates (longitude,latitude)'''
    closest_city = None
    min_distance = float('inf')  # Initialize with a very large number

    with open(CITIES_WITH_COORDINATES, 'r', newline='', encoding='utf-8') as file:
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


def find_city_main():
    latitude = 45.611946 #Castellanza (Varese)
    longitude = 8.898276 #Castellanza (Varese)
    cities_file = CITIES_WITH_COORDINATES
    print(find_closest_city(latitude, longitude))


def read_file_main():
    input_csv = CITIES  # Input CSV file containing the cities
    output_csv = CITIES_WITH_COORDINATES  # Output CSV file to store cities with coordinates
    process_csv(input_csv, output_csv)


# Main function to run the script
if __name__ == '__main__':
    process_csv_codes(CITIES, "cities_with_codes.csv")

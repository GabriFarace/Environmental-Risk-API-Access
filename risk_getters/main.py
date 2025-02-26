from api_interfaces.electricitymaps_API import get_carbon_intensity
from utility.loaders import FilePathLoaderFromGdrive
from risk_getters.riskInterfaces import RiskManager
from risk_getters.seismic_risk_getters import SeismicRiskMap, SeismicRiskThAPI
from risk_getters.landslide_risk_getters import LandslideRiskMap, LandslideRiskThAPI
from risk_getters.flood_risk_getters import FloodRiskMap, RiverFloodRiskThAPI, UrbanFloodRiskThAPI
from constants import *
from api_interfaces.thinkhazard_API import ThinkHazardAPI
from risk_getters.enumerations import EnvironmentalRiskType, EnvironmentalRisk
import json

def map_risk_level(risk: EnvironmentalRisk):
    if risk == EnvironmentalRisk.LOW or risk == EnvironmentalRisk.NO_DATA or risk == EnvironmentalRisk.VERY_LOW:
        return "low"
    elif risk == EnvironmentalRisk.MEDIUM:
        return "medium"
    elif risk == EnvironmentalRisk.HIGH:
        return "high"
    else:
        raise ValueError(f"Invalid risk level: {risk}")

def map_risk_level_2(risk: EnvironmentalRisk):
    if risk == EnvironmentalRisk.NO_DATA:
        return 0
    elif risk == EnvironmentalRisk.VERY_LOW:
        return 1
    elif risk == EnvironmentalRisk.LOW:
        return 2
    elif risk == EnvironmentalRisk.MEDIUM:
        return 3
    elif risk == EnvironmentalRisk.HIGH:
        return 4
    else:
        raise ValueError(f"Invalid risk level: {risk}")

def main():
    thAPI = ThinkHazardAPI()
    #file_path_loader = FilePathLoaderFromGdrive()
    ufl1 = UrbanFloodRiskThAPI(thAPI)
    rfl1 = RiverFloodRiskThAPI(thAPI)
    #fl2 = FloodRiskMap(FLOOD_SHAPEFILE_LOW_DATA, FLOOD_SHAPEFILE_MEDIUM_DATA, FLOOD_SHAPEFILE_HIGH_DATA, file_path_loader)
    land1 = LandslideRiskThAPI(thAPI)
    #land2 = LandslideRiskMap(LANDSLIDE_SHAPEFILE_DATA, file_path_loader)
    seis1 = SeismicRiskThAPI(thAPI)
    #seis2 = SeismicRiskMap(SEISMIC_RASTERFILE_DATA, file_path_loader)

    risk_getters_per_type = { EnvironmentalRiskType.SEISMIC_RISK : [seis1],
                              EnvironmentalRiskType.LANDSLIDE_RISK : [land1],
                              EnvironmentalRiskType.FLOOD_RIVER_RISK : [rfl1],
                              EnvironmentalRiskType.FLOOD_URBAN_RISK : [ufl1]}

    risk_manager = RiskManager(risk_getters_per_type)


    done = False
    while not done:
        lat = float(input("\n Insert Latitude : "))
        lon = float(input("\n Insert Longitude : "))

        risk_indicators = risk_manager.get_indicators(lon, lat)

        print(f" River Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]}")
        print(f" Urban Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_URBAN_RISK]}")
        print(f" Seismic Risk Level: {risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]}")
        print(f" Landslide Risk Level: {risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]}")

        choice = input("Do you want to continue? [Y/N] ")
        done = True if choice == "N" else False


def extract_cities_data():
    thAPI = ThinkHazardAPI()
    #file_path_loader = FilePathLoaderFromGdrive()
    ufl1 = UrbanFloodRiskThAPI(thAPI)
    rfl1 = RiverFloodRiskThAPI(thAPI)
    #fl2 = FloodRiskMap(FLOOD_SHAPEFILE_LOW_DATA, FLOOD_SHAPEFILE_MEDIUM_DATA, FLOOD_SHAPEFILE_HIGH_DATA, file_path_loader)
    land1 = LandslideRiskThAPI(thAPI)
    #land2 = LandslideRiskMap(LANDSLIDE_SHAPEFILE_DATA, file_path_loader)
    seis1 = SeismicRiskThAPI(thAPI)
    #seis2 = SeismicRiskMap(SEISMIC_RASTERFILE_DATA, file_path_loader)

    risk_getters_per_type = { EnvironmentalRiskType.SEISMIC_RISK : [seis1],
                              EnvironmentalRiskType.LANDSLIDE_RISK : [land1],
                              EnvironmentalRiskType.FLOOD_RIVER_RISK : [rfl1],
                              EnvironmentalRiskType.FLOOD_URBAN_RISK : [ufl1]}

    risk_manager = RiskManager(risk_getters_per_type)


    cities_data_generated = []
    done = False
    while not done:
        city_name = input("\n Insert City Name : ")
        lat = float(input("\n Insert Latitude : "))
        lon = float(input("\n Insert Longitude : "))

        risk_indicators = risk_manager.get_indicators(lon, lat)

        print(f" River Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]}")
        print(f" Urban Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_URBAN_RISK]}")
        print(f" Seismic Risk Level: {risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]}")
        print(f" Landslide Risk Level: {risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]}")

        carbon_intensity = get_carbon_intensity(lon, lat)
        print(f"Carbon Intensity: {carbon_intensity} gCO2eq/kWh")

        city = {
            "name" : city_name,
            "lat" : lat,
            "lon" : lon,
            "flood_hazard" : map_risk_level(risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]),
            "landslide_hazard" : map_risk_level(risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]),
            "climatic_hazard" : map_risk_level(risk_indicators[EnvironmentalRiskType.FLOOD_URBAN_RISK]),
            "seismic_hazard" : map_risk_level(risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]),
            "carbon_intensity_gCO2eq_kWh" : carbon_intensity
        }
        cities_data_generated.append(city)

        with open('cities_data.json', 'w') as json_file:
            json.dump(cities_data_generated, json_file, indent=4)

        choice = input("Do you want to continue? [Y/N] ")
        if choice == "N":
            done = True


def extract_cities_data_2():
    thAPI = ThinkHazardAPI()
    #file_path_loader = FilePathLoaderFromGdrive()
    ufl1 = UrbanFloodRiskThAPI(thAPI)
    rfl1 = RiverFloodRiskThAPI(thAPI)
    #fl2 = FloodRiskMap(FLOOD_SHAPEFILE_LOW_DATA, FLOOD_SHAPEFILE_MEDIUM_DATA, FLOOD_SHAPEFILE_HIGH_DATA, file_path_loader)
    land1 = LandslideRiskThAPI(thAPI)
    #land2 = LandslideRiskMap(LANDSLIDE_SHAPEFILE_DATA, file_path_loader)
    seis1 = SeismicRiskThAPI(thAPI)
    #seis2 = SeismicRiskMap(SEISMIC_RASTERFILE_DATA, file_path_loader)

    risk_getters_per_type = { EnvironmentalRiskType.SEISMIC_RISK : [seis1],
                              EnvironmentalRiskType.LANDSLIDE_RISK : [land1],
                              EnvironmentalRiskType.FLOOD_RIVER_RISK : [rfl1],
                              EnvironmentalRiskType.FLOOD_URBAN_RISK : [ufl1]}

    risk_manager = RiskManager(risk_getters_per_type)

    with open("cities_data.json", "r") as f:
        cities_data = json.load(f)

    cities_data_generated = []
    for city_data in cities_data:
        city_name = city_data["name"]
        lat = city_data["lat"]
        lon = city_data["lon"]

        risk_indicators = risk_manager.get_indicators(lon, lat)

        print(f" River Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]}")
        print(f" Urban Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_URBAN_RISK]}")
        print(f" Seismic Risk Level: {risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]}")
        print(f" Landslide Risk Level: {risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]}")

        carbon_intensity = get_carbon_intensity(lon, lat)
        print(f"Carbon Intensity: {carbon_intensity} gCO2eq/kWh")

        city = {
            "name" : city_name,
            "lat" : lat,
            "lon" : lon,
            "flood_hazard" : map_risk_level_2(risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]),
            "landslide_hazard" : map_risk_level_2(risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]),
            "climatic_hazard" : map_risk_level_2(risk_indicators[EnvironmentalRiskType.FLOOD_URBAN_RISK]),
            "seismic_hazard" : map_risk_level_2(risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]),
            "carbon_intensity_gCO2eq_kWh" : carbon_intensity
        }
        cities_data_generated.append(city)

    with open('cities_data2.json', 'w') as json_file:
        json.dump(cities_data_generated, json_file, indent=4)


if __name__ == "__main__":
    extract_cities_data_2()
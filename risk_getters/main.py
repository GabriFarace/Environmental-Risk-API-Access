from utility.loaders import FilePathLoaderFromGdrive
from risk_getters.riskInterfaces import RiskManager
from risk_getters.seismic_risk_getters import SeismicRiskMap
from risk_getters.landslide_risk_getters import LandslideRiskMap
from risk_getters.flood_risk_getters import FloodRiskMap
from constants import *
from api_interfaces.thinkhazard_API import ThinkHazardAPI
from risk_getters.enumerations import EnvironmentalRiskType


def main():
    thAPI = ThinkHazardAPI()
    file_path_loader = FilePathLoaderFromGdrive()
    # fl1 = FloodRiskThAPI(thAPI)
    fl2 = FloodRiskMap(FLOOD_SHAPEFILE_LOW_DATA, FLOOD_SHAPEFILE_MEDIUM_DATA, FLOOD_SHAPEFILE_HIGH_DATA, file_path_loader)
    # land1 = LandslideRiskThAPI(thAPI)
    land2 = LandslideRiskMap(LANDSLIDE_SHAPEFILE_DATA, file_path_loader)
    # seis1 = SeismicRiskThAPI(thAPI)
    seis2 = SeismicRiskMap(SEISMIC_RASTERFILE_DATA, file_path_loader)

    risk_getters_per_type = { EnvironmentalRiskType.SEISMIC_RISK : [seis2],
                              EnvironmentalRiskType.LANDSLIDE_RISK : [land2],
                              EnvironmentalRiskType.FLOOD_RIVER_RISK : [fl2]}

    risk_manager = RiskManager(risk_getters_per_type)


    done = False
    while not done:
        lat = float(input("\n Insert Latitude : "))
        lon = float(input("\n Insert Longitude : "))

        risk_indicators = risk_manager.get_indicators(lon, lat)

        print(f" Flood Risk Level: {risk_indicators[EnvironmentalRiskType.FLOOD_RIVER_RISK]}")
        print(f" Seismic Risk Level: {risk_indicators[EnvironmentalRiskType.SEISMIC_RISK]}")
        print(f" Landslide Risk Level: {risk_indicators[EnvironmentalRiskType.LANDSLIDE_RISK]}")

        choice = input("Do you want to continue? [Y/N] ")
        done = True if choice == "N" else False


if __name__ == "__main__":
    main()
import geopandas as gpd
from abc import ABC
import matplotlib.pyplot as plt
from numpy.ma.core import argmax
from shapely.geometry import Polygon, Point
from risk_getters.enumerations import EnvironmentalRisk, EnvironmentalRiskType
from risk_getters.riskInterfaces import RiskGetter
from api_interfaces.thinkhazard_API import ThinkHazardAPI
from utility.loaders import FilePathLoader

class FloodRiskGetter(RiskGetter, ABC):
    pass



class FloodRiskMap(FloodRiskGetter):
    ''' Class that return the flood risk indicator for a specific location using 3 shapefile representing the low, medium and high risk geographic map areas '''

    def __init__(self, file_data_low: str, file_data_medium: str, file_data_high: str, file_path_loader : FilePathLoader):
        self.map_low = gpd.read_file(file_path_loader.load_path(file_data_low))
        self.map_medium = gpd.read_file(file_path_loader.load_path(file_data_medium))
        self.map_high = gpd.read_file(file_path_loader.load_path(file_data_high))



    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the flood risk by joining the 3 maps with a bounding box surrounding the geographic location given by (latitude, longitude) and using majority voting based on the number of matches'''

        bounding_box_gdf = self._get_bounding_box_dataframe(longitude, latitude)

        # Perform a spatial join with the three maps
        result = [None, None, None]  #LOW, MEDIUM, HIGH
        result[0] = gpd.sjoin(bounding_box_gdf, self.map_low, how="inner", predicate="intersects")
        result[1] = gpd.sjoin(bounding_box_gdf, self.map_medium, how="inner", predicate="intersects")
        result[2] = gpd.sjoin(bounding_box_gdf, self.map_high, how="inner", predicate="intersects")

        # Majority vote
        if all(r.empty for r in result):
            return EnvironmentalRisk.NO_DATA
        else:
            votes = [len(r) for r in result]
            index_max = argmax(votes)
            if index_max == 0:
                return EnvironmentalRisk.LOW
            elif index_max == 1:
                return EnvironmentalRisk.MEDIUM
            else:
                return EnvironmentalRisk.HIGH


    def _get_bounding_box_dataframe(self, longitude: float, latitude: float) -> gpd.GeoDataFrame:
        '''Create a rectangular bounding box surrounding the geographic location given by (latitude, longitude) an return it as a geopandas geodataframe'''
        bounding_box_coords = [(longitude - 0.01, latitude - 0.01),  # Bottom-left (Longitude, Latitude)
                               (longitude + 0.01, latitude - 0.01),  # Bottom-right (Longitude, Latitude)
                               (longitude + 0.01, latitude + 0.01),  # Top-right (Longitude, Latitude)
                               (longitude - 0.01, latitude + 0.01)]  # Top-left (Longitude, Latitude)

        # Create the polygon
        bounding_box = Polygon(bounding_box_coords)

        # Create a GeoDataFrame for the bounding box
        bounding_box_gdf = gpd.GeoDataFrame(geometry=[bounding_box], crs="EPSG:4326")

        # Adjust reference system
        bounding_box_gdf = bounding_box_gdf.to_crs(self.map_low.crs)

        return bounding_box_gdf


    def plot(self, longitude: float, latitude: float):
        ''' Get the risk associated to the location given by (latitude, longitude) and plot the map of that risk level and the location'''

        risk = self.get_risk(longitude, latitude)

        # Create the point associated to the location
        point = Point(longitude, latitude)
        point_gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[point])

        # Adjust the reference system
        point_gdf = point_gdf.to_crs(self.map_low.crs)

        # Plot the shapefile
        ax = None
        if risk == EnvironmentalRisk.VERY_LOW or risk == EnvironmentalRisk.LOW or EnvironmentalRisk.NO_DATA:
            ax = self.map_low.plot(color='lightblue', figsize=(10, 10))
        elif risk == EnvironmentalRisk.MEDIUM:
            ax = self.map_medium.plot(color='lightblue', figsize=(10, 10))
        elif risk == EnvironmentalRisk.HIGH:
            ax = self.map_high.plot(color='lightblue', figsize=(10, 10))

        # Plot the point
        point_gdf.plot(ax=ax, color='red', markersize=50)
        plt.title("Shapefile and Point Location")
        plt.show()



class RiverFloodRiskThAPI(FloodRiskGetter):
    ''' Class that return the flood risk by accessing the ThinkHazard API'''

    def __init__(self, api: ThinkHazardAPI):
        self.RISK_TYPE = EnvironmentalRiskType.FLOOD_RIVER_RISK
        self.api = api

    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the flood risk of the geographic location given by (latitude, longitude) by accessing the ThinkHazard API'''

        risk = self.api.get_risk_level(longitude, latitude, self.RISK_TYPE)


        return risk

class UrbanFloodRiskThAPI(FloodRiskGetter):
    ''' Class that return the flood risk by accessing the ThinkHazard API'''

    def __init__(self, api: ThinkHazardAPI):
        self.RISK_TYPE = EnvironmentalRiskType.FLOOD_URBAN_RISK
        self.api = api

    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the flood risk of the geographic location given by (latitude, longitude) by accessing the ThinkHazard API'''

        risk = self.api.get_risk_level(longitude, latitude, self.RISK_TYPE)

        return risk



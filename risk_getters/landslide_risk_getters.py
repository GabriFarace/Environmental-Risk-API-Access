from abc import ABC
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from numpy.ma.core import argmax
from shapely.geometry import Polygon, Point
from utility.loaders import FilePathLoader
from api_interfaces.thinkhazard_API import ThinkHazardAPI
from risk_getters.enumerations import EnvironmentalRisk, EnvironmentalRiskType
from risk_getters.riskInterfaces import RiskGetter


class LandslideRiskGetter(RiskGetter, ABC):
    pass

class LandslideRiskMap(LandslideRiskGetter):
    ''' Return the landslide risk indicator for a specific location using a shapefile representing the geographic map areas and associated risk values'''

    def __init__(self, file_data: dict, file_path_loader: FilePathLoader):

        # Get the geodataframe
        self.map = gpd.read_file(file_path_loader.load_path(file_data))

        self.risk_levels = ['Aree di Attenzione AA', 'Moderata P1', 'Media P2', 'Elevata P3', 'Molto elevata P4']
        # Convert 'per_fr_ita' column to a categorical type with the defined order
        self.map['per_fr_ita'] = self.map['per_fr_ita'].astype(pd.CategoricalDtype(categories=self.risk_levels, ordered=True))



    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the landslide risk by joining the map with a bounding box surrounding the geographic location given by (latitude, longitude) and using majority voting based on the number of matches'''

        bounding_box_gdf = self._get_bounding_box_dataframe(longitude, latitude)

        # Perform a spatial join with the map
        result = gpd.sjoin(bounding_box_gdf, self.map, how="inner", predicate="intersects")


        # Majority vote
        if result.empty:
            return EnvironmentalRisk.NO_DATA
        else:
            votes_series = result["per_fr_ita"].value_counts()
            votes = [votes_series[self.risk_levels[0]], votes_series[self.risk_levels[1]],
                     votes_series[self.risk_levels[2]],
                     votes_series[self.risk_levels[3]] + votes_series[self.risk_levels[4]]]

            index_max = argmax(votes)
            if index_max == 0:
                return EnvironmentalRisk.VERY_LOW
            elif index_max == 1:
                return EnvironmentalRisk.LOW
            elif index_max == 2:
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
        bounding_box_gdf = bounding_box_gdf.to_crs(self.map.crs)

        return bounding_box_gdf


    def plot(self, longitude: float, latitude: float):
        ''' Plot the map and the location'''

        # Create the point associated to the location
        point = Point(longitude, latitude)
        point_gdf = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[point])

        # Adjust the reference system
        point_gdf = point_gdf.to_crs(self.map.crs)

        # Plot the map
        ax = self.map.plot(color='lightblue', cmap='OrRd', legend=True, figsize=(10, 10))

        # Plot the point
        point_gdf.plot(ax=ax, color='blue', markersize=10)
        plt.title("Shapefile and Point Location")
        plt.show()


class LandslideRiskThAPI(LandslideRiskGetter):
    ''' Class that return the landslide risk by accessing the ThinkHazard API'''

    def __init__(self, api: ThinkHazardAPI):
        self.RISK_TYPE = EnvironmentalRiskType.LANDSLIDE_RISK
        self.api = api


    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the landslide risk of the geographic location given by (latitude, longitude) by accessing the ThinkHazard API'''

        return self.api.get_risk_level(longitude, latitude, self.RISK_TYPE)




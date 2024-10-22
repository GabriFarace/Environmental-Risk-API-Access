import geopandas as gpd
import matplotlib.pyplot as plt
from numpy.ma.core import argmax
from shapely.geometry import Polygon, Point
from utility.enumerations import EnvironmentalRisk
from utility.riskInterfaces import RiskGetter


# Load the shapefile (this automatically loads the .dbf file as well)
FLOOD_SHAPEFILE_PATH_LOW = r"C:\Users\farac\Downloads\Mosaicatura_ISPRA_2020_aree_pericolosita_idraulica\LPH_Mosaicatura_ISPRA_2020_pericolosita_idraulica_bassa.shp"
FLOOD_SHAPEFILE_PATH_MEDIUM = r"C:\Users\farac\Downloads\Mosaicatura_ISPRA_2020_aree_pericolosita_idraulica\MPH_Mosaicatura_ISPRA_2020_pericolosita_idraulica_media.shp"
FLOOD_SHAPEFILE_PATH_HIGH = r"C:\Users\farac\Downloads\Mosaicatura_ISPRA_2020_aree_pericolosita_idraulica\HPH_Mosaicatura_ISPRA_2020_pericolosita_idraulica_elevata.shp"


class FloodRiskMap(RiskGetter):
    ''' Return the flood risk indicator for a specific location using 3 shapefile representing the low, medium and high risk geographic map areas '''

    def __init__(self, map_path_low: str, map_path_medium: str, map_path_high: str):
        self.map_low = gpd.read_file(map_path_low)
        self.map_medium = gpd.read_file(map_path_medium)
        self.map_high = gpd.read_file(map_path_high)



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






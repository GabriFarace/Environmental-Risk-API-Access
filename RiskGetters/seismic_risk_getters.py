import rasterio
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from utility.enumerations import EnvironmentalRisk
from utility.riskInterfaces import RiskGetter

SEISMIC_RASTERFILE_PATH = r"C:\Users\farac\Downloads\GEM-GSHM_PGA-475y-rock_v2023\v2023_1_pga_475_rock_3min.tif"

class SeismicRiskMap(RiskGetter):
    ''' Return the seismic risk indicator for a specific location using a raster file representing the geographic map areas and associated risk values'''

    def __init__(self, map_path: str):
        self.map_path = map_path

        # Define the PGA ranges and labels
        self.pga_ranges = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.13, 0.20, 0.35, 0.55, 0.90, 1.50]
        self.labels = [
            "Very Low 1", "Very Low 2", "Very Low 3", "Low 1", "Low 2",
            "Low 3", "Medium 1", "Medium 2", "High 1", "High 2", "High 3"
        ]

        # Define variables for plots
        # Define and convert RGB to values between 0 and 1 for matplotlib
        self.rgb_colors = [
            [255, 255, 255],  # 0.00-0.01
            [215, 227, 238],  # 0.01-0.02
            [181, 202, 255],  # 0.02-0.03
            [143, 179, 255],  # 0.03-0.05
            [127, 151, 255],  # 0.05-0.08
            [171, 207, 99],  # 0.08-0.13
            [232, 245, 158],  # 0.13-0.20
            [255, 250, 20],  # 0.20-0.35
            [255, 209, 33],  # 0.35-0.55
            [255, 163, 10],  # 0.55-0.90
            [255, 76, 0]  # 0.90-1.50
        ]
        self.rgb_colors = np.array(self.rgb_colors) / 255.0

        # Create a ListedColormap
        self.cmap = mcolors.ListedColormap(self.rgb_colors)

        # Normalize the PGA ranges to [0, 1]
        self.norm = mcolors.BoundaryNorm(boundaries=self.pga_ranges, ncolors=len(self.rgb_colors))



    def get_risk(self, longitude: float, latitude: float) -> EnvironmentalRisk:
        ''' Return the seismic risk by extracting the Peak Ground Acceleration for the geographic location given by (latitude, longitude) from the map and using thresholds similar to those used by the ThinkHazard API to assess the risk level'''

        with rasterio.open(self.map_path) as src:
            transform = src.transform

            # Calculate the column and row using the affine transformation
            col = int((longitude - transform.c) / transform.a)
            row = int((latitude - transform.f) / transform.e)

            # Ensure the row and col are within bounds of the raster
            if not (0 <= col < src.width and 0 <= row < src.height):
                return EnvironmentalRisk.NO_DATA
            else:
                # Convert world coordinates to raster pixel coordinates
                row, col = src.index(longitude, latitude)

                # Read the raster value at the specific location
                pga_value = src.read(1)[row, col]

                if pga_value == src.nodata:
                    return EnvironmentalRisk.NO_DATA
                else:
                    if pga_value < 0.03:
                        return EnvironmentalRisk.VERY_LOW
                    elif pga_value < 0.13:
                        return EnvironmentalRisk.LOW
                    elif pga_value < 0.35:
                        return EnvironmentalRisk.MEDIUM
                    else:
                        return EnvironmentalRisk.HIGH



    def plot(self, longitude: float, latitude: float):
        ''' Plot the map and the location given by (latitude, longitude) '''


        # Read the first band of the raster
        with rasterio.open(self.map_path) as src:

            fig, ax = plt.subplots(figsize=(10, 10))

            # Read raster data
            raster_data = src.read(1)

            # Get raster bounds
            bounds = src.bounds  # (left, bottom, right, top) in degrees

            # Plot the raster using imshow with the correct extent and aspect ratio
            img = ax.imshow(raster_data, cmap=self.cmap, norm=self.norm,
                            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
                            origin='upper')

            # Add a colorbar with custom tick labels
            cbar = plt.colorbar(img, ax=ax, boundaries=self.pga_ranges[:-1], ticks=self.pga_ranges[:-1],
                                spacing='uniform')
            cbar.ax.set_yticklabels(self.labels)
            cbar.set_label('Risk Levels', rotation=270, labelpad=20)

            # Plot the point (in geographic coordinates) on the map
            ax.plot(longitude, latitude, 'ro', markersize=4)  # 'ro' for red circle

            plt.title("PGA Location on the GEM Seismic Hazard Map")
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.show()


    def plot_from_bounds(self, lower_bound: float, upper_bound: float):
        ''' Plot the map and the points for which the PGA (Peak Ground Acceleration) is in the interval [lower_bound, upper_bound]'''

        with rasterio.open(self.map_path) as src:
            # Read the raster data
            raster_data = src.read(1)
            transform = src.transform

            # Identify the NoData value (if applicable)
            nodata_value = src.nodata

            # Mask the NoData values (if needed)
            if nodata_value is not None:
                raster_data = np.ma.masked_equal(raster_data, nodata_value)

            # Find indices where the values are within the specified range
            target_indices = np.where((raster_data >= lower_bound) & (raster_data <= upper_bound))

            # Convert pixel indices to geographical coordinates
            coordinates = []
            for row, col in zip(*target_indices):
                # Convert row, col (pixel) to x, y (coordinates)
                x, y = transform * (col, row)  # (col, row) to (x, y)
                coordinates.append((x, y))

            # Set up the plot with a larger figure size
            fig, ax = plt.subplots(figsize=(15, 15))  # Increased size

            # Plot the raster using the custom colormap and normalization
            img = ax.imshow(raster_data, cmap=self.cmap, norm=self.norm,
                            extent=(src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top))

            # Add a colorbar with non-proportional tick spacing
            cbar = plt.colorbar(img, ax=ax, boundaries=self.pga_ranges, ticks=self.pga_ranges[:-1], spacing='uniform')
            cbar.ax.set_yticklabels(self.labels)  # Set the correct number of labels

            # Add a title to the colorbar for risk levels
            cbar.set_label('Risk Levels', rotation=270, labelpad=20)

            # Plot the extracted points on the map
            if coordinates:  # Check if any coordinates were found
                lon, lat = zip(*coordinates)
                ax.scatter(lon, lat, color='red', marker='o', label='PGA > 0.90', s=0.0001)  # Plot points in red
                ax.legend()  # Show legend

            # Set plot labels
            plt.title("Seismic Hazard Map with PGA Levels", fontsize=18)
            plt.xlabel("Longitude", fontsize=14)
            plt.ylabel("Latitude", fontsize=14)

            # Show the plot
            plt.show()



risk_getter = SeismicRiskMap(SEISMIC_RASTERFILE_PATH)
lat = 39.298263
lon = 16.253736
#risk = risk_getter.get_risk(lon, lat)
#print(f" Seismic Risk Level: {risk}")

risk_getter.plot_from_bounds(0.5, 1.5)









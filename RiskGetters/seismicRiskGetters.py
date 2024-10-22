import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import numpy as np
import matplotlib.colors as colors
# Define the PGA ranges and RGB colors
pga_ranges = [0.00, 0.01, 0.02, 0.03, 0.05, 0.08, 0.13, 0.20, 0.35, 0.55, 0.90, 1.50]
rgb_colors = [
    [255, 255, 255],  # 0.00-0.01
    [215, 227, 238],  # 0.01-0.02
    [181, 202, 255],  # 0.02-0.03
    [143, 179, 255],  # 0.03-0.05
    [127, 151, 255],  # 0.05-0.08
    [171, 207, 99],   # 0.08-0.13
    [232, 245, 158],  # 0.13-0.20
    [255, 250, 20],   # 0.20-0.35
    [255, 209, 33],   # 0.35-0.55
    [255, 163, 10],   # 0.55-0.90
    [255, 76, 0]      # 0.90-1.50
]

labels = [
    "No Danger 1", "No Danger 2", "No Danger 3", "Very-Low", "Low",
    "Medium-Low", "Medium", "Medium-High", "High", "Very-High", "Danger level High"
]

# Convert RGB to values between 0 and 1 for matplotlib
rgb_colors = np.array(rgb_colors) / 255.0

# Create a ListedColormap
cmap = mcolors.ListedColormap(rgb_colors)

# Normalize the PGA ranges to [0, 1]
norm = mcolors.BoundaryNorm(boundaries=pga_ranges, ncolors=len(rgb_colors))

def get_and_show(src, lon, lat):
    transform = src.transform

    # Get raster bounds
    bounds = src.bounds  # (left, bottom, right, top) in degrees

    # Calculate the column and row using the affine transformation
    col = int((lon - transform.c) / transform.a)
    row = int((lat - transform.f) / transform.e)

    print(f"Pixel coordinates: row={row}, col={col}")

    # Ensure the row and col are within bounds of the raster
    if not (0 <= col < src.width and 0 <= row < src.height):
        print("The coordinates are outside the raster bounds.")
    else:

        # Convert world coordinates to raster pixel coordinates
        row, col = src.index(lon, lat)

        # Read the raster value at the specific location
        pga_value = src.read(1)[row, col]

        if pga_value == src.nodata:
            print("No data available for this location")
        else:

            print(f"Peak Ground Acceleration (PGA) value: {pga_value}")
            fig, ax = plt.subplots(figsize=(10, 10))

            # Read the first band of the raster
            raster_data = src.read(1)

            # Plot the raster using imshow with the correct extent and aspect ratio
            img = ax.imshow(raster_data, cmap=cmap, norm=norm,
                      extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
                      origin='upper')

            # Add a colorbar with custom tick labels
            cbar = plt.colorbar(img, ax=ax, boundaries=pga_ranges[:-1], ticks=pga_ranges[:-1], spacing='uniform')
            cbar.ax.set_yticklabels(labels)
            cbar.set_label('Risk Levels', rotation=270, labelpad=20)

            # Plot the point (in geographic coordinates) on the map
            ax.plot(lon, lat, 'ro', markersize=4)  # 'ro' for red circle

            plt.title("PGA Location on the GEM Seismic Hazard Map")
            plt.xlabel('Longitude')
            plt.ylabel('Latitude')
            plt.show()

def get_coordinates(src, lower_bound, upper_bound):
    # Read the first band of the raster data
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
    img = ax.imshow(raster_data, cmap=cmap, norm=norm,
                    extent=(src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top))

    # Add a colorbar with non-proportional tick spacing
    cbar = plt.colorbar(img, ax=ax, boundaries=pga_ranges, ticks=pga_ranges[:-1], spacing='uniform')
    cbar.ax.set_yticklabels(labels)  # Set the correct number of labels

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

    return coordinates

# Path to the raster file (update to match your file location)
raster_file = r"C:\Users\farac\Downloads\GEM-GSHM_PGA-475y-rock_v2023\v2023_1_pga_475_rock_3min.tif"

# Open the raster file
with rasterio.open(raster_file) as src:
        #print(src.profile)  # Check metadata and projection info

        # Assuming your location coordinates are in latitude and longitude (EPSG:4326)
        lat = -31.05193000000081
        lon = -71.35
        #get_and_show(src, lon, lat)

        # Define the target value range for extraction
        lower_bound = 0.30
        upper_bound = 1.50

        coordinates = get_coordinates(src, lower_bound, upper_bound)
        #for coord in coordinates:
         #   print(f"Longitude: {coord[0]}, Latitude: {coord[1]}")








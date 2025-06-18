import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import pyproj
import os

def csv_to_shapefile(csv_file, shapefile_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create a geometry column from EASTING and NORTHING
    geometry = [Point(xy) for xy in zip(df['EASTING'], df['NORTHING'])]

    # Set the Geometry column in your GeoDataFrame
    gdf = gpd.GeoDataFrame(df, crs="EPSG:32629", geometry=geometry)

    # Save the GeoDataFrame to a Shapefile
    gdf.to_file(shapefile_path, driver='ESRI Shapefile')


if __name__ == "__main__":
    # Example usage

    for file in os.listdir(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst"):
        if file.endswith(".csv"):
            print(file)
            csv_file_path = os.path.join(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst", file)
            shapefile_output_path = os.path.join(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\06 - GIS\1 Vectors\2- Culture", file) + ".shp"
            csv_to_shapefile(csv_file_path, shapefile_output_path)

    # csv_file_path = r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst\Culture_no-device_ncastioni_2025-06-17_ dwB- cement begins here- steps start on this line.csv"  # Update this with your CSV file path
    # shapefile_output_path = r'Culture_no-device_ncastioni_2025-06-17_ dwB- cement begins here- steps start on this line.csv.shp'  # Output shapefile path

    # csv_to_shapefile(csv_file_path, shapefile_output_path)

import pandas as pd
import geopandas as gpd
import pyproj
import os
import re
from shapely.geometry import Point

MOROCCO_CRS = "EPSG:32629" # UTM Zone 29N
UKW_CRS = "EPSG:32630" # UTM Zone 30N
UKE_CRS = "EPSG:32629"  # UTM Zone 29N

def csv_to_shapefile(csv_file, shapefile_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    df["Z"] = pd.to_numeric(df["ELEV"], errors='coerce')
    filtered = filter_out_origin_points(df, tolerance=0.00001)

    df["geometry"] = [Point(xy) for xy in zip(df['EASTING'], df['NORTHING'])]

    gdf = gpd.GeoDataFrame(df, crs=UKW_CRS, geometry='geometry')

    gdf.to_file(shapefile_path, driver='ESRI Shapefile')

    # # Create a geometry column from EASTING and NORTHING
    # geometry = [Point(xy) for xy in zip(df['EASTING'], df['NORTHING'])]
    #
    # # Set the Geometry column in your GeoDataFrame
    # # gdf = gpd.GeoDataFrame(df, crs="EPSG:32629", geometry=geometry)
    # gdf = gpd.GeoDataFrame(df, crs=UKW_CRS, geometry=geometry)
    #
    # # Save the GeoDataFrame to a Shapefile
    # gdf.to_file(shapefile_path, driver='ESRI Shapefile')

def transform_coordinates(easting, northing):
    # Assuming the input CRS is UTM Zone 33N (EPSG:32633)
    input_crs = 'EPSG:32633'
    output_crs = 'EPSG:4326'

    transformer = pyproj.Transformer.from_crs(input_crs, output_crs)

    # Transforming coordinates
    return transformer.transform(easting, northing)

def filter_out_origin_points(df, tolerance):

    df['LONGITUDE'], df['LATITUDE'] = zip(*df.apply(lambda row: transform_coordinates(row['EASTING'], row['NORTHING']), axis=1))
    mask = ~ (abs(df['LATITUDE']) < tolerance)
    filtered_df = df[mask]

    return filtered_df

def combine_to_shp(csv_folder, shapefile_path, label_filter=""):
    """
    Combine multiple CSV files into a single shapefile.

    Parameters:
    csv_files (list): List of paths to CSV files.
    shapefile_path (str): Path to the output shapefile.
    """

    combined_dfs = []
    csv_files = [os.path.join(csv_folder, file) for file in os.listdir(csv_folder) if file.endswith('.csv')]

    # csv_files.remove(r'Z:\\Shared\\ActiveProjects\\25772 - Aoulouz Dam - Morocco - 2025\\03 - Field Data\\3- Culture etc\\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst\\combined_csv_files.csv')


    # combined_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
    for file in csv_files:

        if "combined" in file:
            continue

        df = pd.read_csv(file)
        df["ELEV"] = pd.to_numeric(df["ELEV"], errors='coerce')
        filtered = filter_out_origin_points(df, tolerance=0.00001)

        if filtered.empty:
            continue

        filtered["LABEL"] = file.split(os.sep)[-1].replace(label_filter, "").replace(".csv", "")
        combined_dfs.append(filtered)

    combined_df = pd.concat(combined_dfs, ignore_index=True)

    # filter_df = filter_out_origin_points(combined_df, tolerance=0.00001)
    combined_df["geometry"] = [Point(xy) for xy in zip(combined_df['EASTING'], combined_df['NORTHING'])]

    gdf = gpd.GeoDataFrame(combined_df, crs="EPSG:32629", geometry='geometry')

    gdf.to_file(shapefile_path, driver='ESRI Shapefile')

def convert_to_indv_shps(folder_name, write_folder, label_type = "wire"):

    files = [f for f in os.listdir(folder_name) if f.endswith('.csv')]

    for file in files:

        csv_file_path = os.path.join(folder_name, file)
        file_name = file.replace(".csv", ".shp")
        shapefile_output_path = os.path.join(write_folder, file_name)

        csv_to_shapefile(csv_file_path, shapefile_output_path)
        print(f"Converted {file} to {file_name}")



if __name__ == "__main__":

    point = r"E:\JGS\Willowstick\Processing\25789 - Watertech - Thames -Knight&Bessborough Reservoir - COMPARE - 2025\Willowstick UK__25789 - Knight&Bessborough Reservoir - COMPARE - Group 1__wst\02- _Electrode_Geode 383553_greg-tickner_2025-07-17_.csv"
    write = r"E:\JGS\Willowstick\Processing\electrode_02"

    csv_to_shapefile(point, write)

    # source_folder = r"E:\JGS\Willowstick\Processing\25789 - Watertech - Thames -Knight&Bessborough Reservoir - COMPARE - 2025\Willowstick UK__25789 - Knight&Bessborough Reservoir - COMPARE - Group 1__wst\Wire"
    # write_folder = r"E:\JGS\Willowstick\Processing\25789 - Watertech - Thames -Knight&Bessborough Reservoir - COMPARE - 2025\Converted Files"
    label = "wire"

    # convert_to_indv_shps(source_folder, write_folder, label_type=label)

    # source_folder = r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst"
    # write_file = r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\06 - GIS\1 Vectors\2- Culture\combined_culture.shp"
    # label_filter = "Culture_no-device_ncastioni_2025-06-17_"



    # combine_to_shp(source_folder, write_file, label_filter=label_filter)

    # for file in os.listdir(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst"):
    #     if file.endswith(".csv"):
    #         print(file)
    #         csv_file_path = os.path.join(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst", file)
    #         file_name = file.replace(".csv", ".shp")
    #         shapefile_output_path = os.path.join(r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\06 - GIS\1 Vectors\2- Culture", file_name)
    #         csv_to_shapefile(csv_file_path, shapefile_output_path)

    # csv_file_path = r"Z:\Shared\ActiveProjects\25772 - Aoulouz Dam - Morocco - 2025\03 - Field Data\3- Culture etc\Aoulouz Dam - Morocco__25772 - Aoulouz Dam - Morocco__wst\Culture_no-device_ncastioni_2025-06-17_ dwB- cement begins here- steps start on this line.csv"  # Update this with your CSV file path
    # shapefile_output_path = r'Culture_no-device_ncastioni_2025-06-17_ dwB- cement begins here- steps start on this line.csv.shp'  # Output shapefile path

    # csv_to_shapefile(csv_file_path, shapefile_output_path)

import shapefile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os

def filter_points_within_polygon(polygon_shp, points_shps, output_shp):
    import geopandas as gpd
    import pandas as pd

    polygons = gpd.read_file(polygon_shp)
    required_cols = ['EASTING', 'NORTHING', 'ELEV']

    filtered_points_all = []

    for point_shp in points_shps:
        if point_shp == polygon_shp:
            continue

        points = gpd.read_file(point_shp)
        # Select only required columns if they exist
        cols_to_keep = [col for col in required_cols if col in points.columns]
        cols_to_keep = ['geometry'] + cols_to_keep

        filtered_points = gpd.sjoin(points, polygons, how="inner", predicate='intersects')
        filtered_points = filtered_points[cols_to_keep]

        if not filtered_points.empty:
            filtered_points_all.append(filtered_points)

    if filtered_points_all:
        merged = pd.concat(filtered_points_all, ignore_index=True)
        merged_gdf = gpd.GeoDataFrame(merged, geometry='geometry', crs=polygons.crs)
        merged_gdf.to_file(output_shp, driver='ESRI Shapefile')
        print(f"Filtered points have been written to {output_shp}.")
    else:
        print("No points were found within the polygons.")

# def filter_points_within_polygon(polygon_shp, points_shps, output_shp):
#     # Read polygon shapefile
#     polygons = gpd.read_file(polygon_shp)
#     # filter_points_all = gpd.GeoDataFrame()
#
#     # Ensure it's a GeoDataFrame
#     if not isinstance(polygons, gpd.GeoDataFrame):
#         raise ValueError("Polygon input is not a valid shapefile or the file could not be read correctly.")
#
#     # Iterate through each points shapefile and filter points within polygons
#     for point_shp in points_shps:
#
#         if point_shp == polygon_shp:
#             continue
#
#         points = gpd.read_file(point_shp)
#
#         if not isinstance(points, gpd.GeoDataFrame):
#             raise ValueError(f"Point input {point_shp} is not a valid shapefile or the file could not be read correctly.")
#
#         # Perform spatial join to filter points within polygons
#         filtered_points = gpd.sjoin(polygons, points, how="inner", predicate='intersects')
#
#         if len(filtered_points) > 0:
#             print(f"Found {len(filtered_points)} points in {point_shp} that lie within the polygon.")
#
#             # Append to list of filtered points
#             if 'filtered_points_all' not in locals():
#                 filtered_points_all = filtered_points[['geometry'] + points.columns.tolist()]
#             else:
#                 filtered_points_all = gpd.GeoDataFrame(pd.concat([filtered_points_all, filtered_points[['geometry'] + points.columns.tolist()]]), crs=polygons.crs)
#
#     # Write the resulting GeoDataFrame to a new shapefile
#     if 'filtered_points_all' in locals():
#         filtered_points_all.to_file(output_shp, driver='ESRI Shapefile')
#         print(f"Filtered points have been written to {output_shp}.")
#     else:
#         print("No points were found within the polygons.")

if __name__ == "__main__":
    folder = r"E:\JGS\Willowstick\Processing\S07"
    polygon_shp = os.path.join(folder, "07 circuit wire outline.shp")
    point_shps = [os.path.join(folder, file) for file in os.listdir(r"E:\JGS\Willowstick\Processing\S07") if file.endswith('.shp') and file != polygon_shp]
    output_shp = r"E:\JGS\Willowstick\Processing\S07\Survey 07 loop wire.shp"

    filter_points_within_polygon(polygon_shp, point_shps, output_shp)
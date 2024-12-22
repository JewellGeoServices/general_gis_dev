import matplotlib.pyplot as plt
from osgeo import gdal, osr
import json
import numpy as np
import pandas as pd
from pyproj import Proj

gt_path = r"E:\Datasets\Spectral Data\Sentinel - La-Guajira-Colombia\SkyFi_24514BEV-1_2024-11-18_1529Z_MULTISPECTRAL_MEDIUM_La-Guajira-Colombia.tif"
gtinfo_path = r"E:\Datasets\Spectral Data\Sentinel - La-Guajira-Colombia\SkyFi_24514BEV-1_2024-11-18_1529Z_MULTISPECTRAL_MEDIUM_La-Guajira-Colombia_metadata.json"
wells_path = r"E:\JGS\Willowstick\Development\Remote Sensing\Guajira Wells\wells and LS new.csv"

with open(gtinfo_path, "r") as f:
    meta = json.load(f)

wellsdf = pd.read_csv(wells_path)
wells = wellsdf.to_numpy()

rect_coords = meta["geometry"]["coordinates"][0]

def rectangleMinMax(rect):
    """
    Check if a point (lat, lon) is inside a rectangle defined by four corner points.

    Parameters:
    lat (float): Latitude of the point.
    lon (float): Longitude of the point.
    rect (list): List of four tuples representing the corners of the rectangle in (lat, lon) format.

    Returns:
    bool: True if the point is inside the rectangle, False otherwise.
    """
    min_lat = min(rect[0][0], rect[1][0], rect[2][0], rect[3][0])
    max_lat = max(rect[0][0], rect[1][0], rect[2][0], rect[3][0])
    min_lon = min(rect[0][1], rect[1][1], rect[2][1], rect[3][1])
    max_lon = max(rect[0][1], rect[1][1], rect[2][1], rect[3][1])

    return {"min_lat": min_lat, "min_lon": min_lon, "max_lat": max_lat, "max_lon": max_lon}

def is_point_in_rectangle(lat, lon, rects):

    return (rects["min_lat"] <= lat <= rects["max_lat"]) & (rects["min_lon"] <= lon <= rects["max_lon"])

def checkWellsContained():
    in_rect = []
    rect = rectangleMinMax(rect_coords)

    for lat, lon, _ in wells:
        in_rect.append(is_point_in_rectangle(lat, lon, rect))

    return in_rect


def latlon_to_pixel(coords, gdSet):

    trans_coords= []

    geot = gdSet.GetGeoTransform()
    p1 = Proj(init="EPSG:32618")

    for lat, lon in coords:

        xm, ym = p1(lon, lat, inverse=False)

        xp = int((xm - geot[0]) / 10)
        yp = int((geot[3] - ym) / 10)

        trans_coords.append([xp, yp])

    return np.array(trans_coords)

def extract_bands_data(dataset, coords):
    bands_data = []

    for x, y in coords:

        try:
            temp = dataset.ReadAsArray(xoff=x, yoff=y, xsize=1, ysize=1, band_list=list(range(1, 13)))
            bands_data.append(temp.flatten())
        except AttributeError:
            bands_data.append(np.zeros(12))

    return np.array(bands_data)

if __name__ == "__main__":

    # checkWellsContained()
    gt = gdal.Open(gt_path)

    lat = wells[0][0]
    lon = wells[0][1]

    sentineldat = gdal.Open(gt_path)
    geotransform = sentineldat.GetGeoTransform()
    projection = sentineldat.GetProjection()

    tcoords = latlon_to_pixel(wells[:, :2], gt)

    bands_data = extract_bands_data(gt, tcoords)

    bandsdf = pd.DataFrame(bands_data, columns=meta["properties"]["band_order"])
    newDf = pd.concat([wellsdf, bandsdf], axis=1)

    newDf.to_csv("guajira_wells_sentinel_data.csv", index=False)

    print(bands_data)
import pandas as pd
import numpy as np

aviris_sets = r"E:\Willowstick\Remote Sensing\AVIRIS sets.xlsx"
lat = 35.409983
lon = -115.73231

def find_nearby_sets():

    df = pd.read_excel(aviris_sets)
    lats = []
    lons = []

    for i in range(1, 5):

        lats.append(df[f"Lat{i}"])
        lons.append(df[f"Lon{i}"])

    lats = np.array(lats)
    lons = np.array(lons)

    maxLat = np.max(lats, axis=0)
    minLat = np.min(lats, axis=0)
    maxLon = np.max(lons, axis=0)
    minLon = np.min(lons, axis=0)

    centroids = np.sqrt(np.power(maxLat - minLat, 2) + np.power(maxLon + minLon, 2))

    diffs = np.sqrt(np.power(lat - ((maxLat + minLat) / 2), 2) + np.power(lon - ((maxLon + minLon) / 2), 2))

    df["Distance"] = diffs
    df.sort_values("Distance", ascending=True, inplace=True)

    print(df)


if __name__ == "__main__":

    find_nearby_sets()
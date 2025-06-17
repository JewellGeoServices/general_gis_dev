import zipfile
import os
from pykml import parser


def parse_points(pm):
    data = {"lat": [], "lon": [], "name": []}
    for place in pm.Placemark:
        data["lat"].append(float(place.Point.coordinates.text.split(",")[1]))
        data["lon"].append(float(place.Point.coordinates.text.split(",")[0]))
        data["name"].append(place.name.text)
    return data

def readKML(path, dumpCSV=False):
    if path.endswith('.kmz'):
        with zipfile.ZipFile(path, 'r') as kmz:
            kml_filename = [name for name in kmz.namelist() if name.endswith('.kml')][0]
            with kmz.open(kml_filename) as kml_file:
                root = parser.parse(kml_file)

                data = parse_points(root)

    else:
        with open(path) as kml_file:
            root = parser.parse(kml_file)

    pages = dict()

    for pm in root.getroot().Document.Folder:
        if getattr(pm, 'name') == "Boxes":
            data = parse_points(root)
            # pages["Boxes"] = parse_bins(pm)
        elif hasattr(pm, "name"):
            data = parse_points(root)
            # pages[pm.name.text] = parse_points(pm)

    if dumpCSV:
        for name, df in pages.items():
            df.to_csv(f"{name}.csv", index=False)

    return pages

if __name__ == "__main__":
    path = "E:\JGS\Willowstick\GIS\sketchup geo-location test.kmz"
    # path = r"E:\JGS\Willowstick\Remote Sensing\Ansync.kmz"
    pages = readKML(path, dumpCSV=True)
    print(pages.keys())
    print(pages["Boxes"].head())
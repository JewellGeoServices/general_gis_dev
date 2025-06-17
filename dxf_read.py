import ezdxf
import geopandas as gpd
from shapely.geometry import LineString

def adjust_dxf_coords(dxf_path, utm_origin, save_as_dxf=False, output_filename="polylines"):

    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    polylines = msp.query("POLYLINE")

    for polyline in polylines:
        for vertex in polyline.vertices:
            vertex.dxf.locations = (vertex.dxf.locations.x + utm_origin[0],
                                    vertex.dxf.locations.y + utm_origin[1],
                                    vertex.dxf.locations.z + utm_origin[2])

    if save_as_dxf:
        doc.saveas(output_filename + ".dxf")

    else:
        geometries = []
        for polyline in polylines:
            coords = [(vertex.dxf.locations.x, vertex.dxf.locations.y) for vertex in polyline.vertices]
            geometries.append(LineString(coords))

        crs = {"init": "epsg:32618"}

        gdf = gpd.GeoDataFrame(geometry=geometries, crs=crs)
        gdf.to_file(output_filename + ".shp")

if __name__ == "__main__":

    utm_origin = (your_known_x, your_known_y, your_known_z)
    adjust_dxf_coords
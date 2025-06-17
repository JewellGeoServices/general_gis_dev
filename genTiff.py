import numpy as np
from osgeo import gdal, osr
from PIL import Image


def png_to_geotiff(png_path, output_path):
    # Read the PNG file
    img = Image.open(png_path)
    img_array = np.flipud(np.array(img))

    # Read the polygon coordinates from the KML file

    # Calculate the geotransform
    min_lon = -121.059278
    max_lon = -121.057551
    min_lat = 38.621371
    max_lat = 38.622273

    pixel_width = (max_lon - min_lon) / img_array.shape[1]
    pixel_height = (max_lat - min_lat) / img_array.shape[0]

    # geotransform = (max_lon, pixel_width, 0, max_lat, 0, -pixel_height)
    geotransform = (max_lon, pixel_width, 0, max_lat, 0, -pixel_height)

    # Create the GeoTIFF file
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(output_path, img_array.shape[1], img_array.shape[0], 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(geotransform)

    # Set the projection (WGS84)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dataset.SetProjection(srs.ExportToWkt())

    # Write the image data
    dataset.GetRasterBand(1).WriteArray(img_array[:, :, 0])
    dataset.FlushCache()

def pngresize(png_path, output_path, pixel_size_cm=10):
    # Read the PNG file
    img = Image.open(png_path)
    img_array = np.array(img)

    # Calculate the new dimensions
    pixel_size_m = pixel_size_cm / 100.0
    min_lon = -98.323259
    max_lon = -98.32071
    min_lat = 29.638036
    max_lat = 29.639311

    width_m = (max_lon - min_lon) * 111320  # Approximate conversion from degrees to meters
    height_m = (max_lat - min_lat) * 110540  # Approximate conversion from degrees to meters

    new_width = int(width_m / pixel_size_m)
    new_height = int(height_m / pixel_size_m)

    # Resize the image
    img_resized = img.resize((new_width, new_height))
    img_array_resized = np.array(img_resized)

    # Calculate the new geotransform
    pixel_width = (max_lon - min_lon) / new_width
    pixel_height = (max_lat - min_lat) / new_height

    # geotransform = (min_lon, pixel_width, 0, max_lat, 0, -pixel_height)

    # Calculate the rotation matrix
    angle_rad = np.deg2rad(0)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)

    # Apply the rotation to the geotransform
    geotransform = (
        min_lon,
        pixel_width * cos_angle,
        -pixel_height * sin_angle,
        max_lat,
        pixel_width * sin_angle,
        -pixel_height * cos_angle
    )

    # Create the GeoTIFF file
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(output_path, new_width, new_height, 1, gdal.GDT_Byte)
    dataset.SetGeoTransform(geotransform)

    # Set the projection (WGS84)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    dataset.SetProjection(srs.ExportToWkt())

    # Write the image data
    dataset.GetRasterBand(1).WriteArray(img_array_resized[:, :, 0])
    dataset.FlushCache()

if __name__ == "__main__":

    kml_path = r"E:\JGS\Willowstick\Remote Sensing\Ansync.kmz"
    png_path = r"E:\JGS\Willowstick\Remote Sensing\izzy house.png"
    output_path = r"E:\JGS\Willowstick\Remote Sensing\house boosted.tif"

    # ng_to_geotiff(png_path, output_path)
    pngresize(png_path, output_path, pixel_size_cm=10)
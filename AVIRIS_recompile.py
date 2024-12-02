import numpy as np
import imageio
from spectral import *
import re
import matplotlib.pyplot as plt

from osgeo import gdal
gdal.UseExceptions()



def loadIMG(path, idx1, idx2):
    # imageio.plugins.freeimage.download()
    # img = imageio.imread(path, format="HDR-FI")

    dataset = gdal.Open(path)

    meta = dataset.GetMetadata()
    bands = list(meta.values())

    imgData = {bands[idx1]: dataset.GetRasterBand(idx1).ReadAsArray(),
               bands[idx2]: dataset.GetRasterBand(idx2).ReadAsArray()}

    srs = {"geotransform": dataset.GetGeoTransform(),
            "projection": dataset.GetProjection()}

    return dataset, imgData, srs


def calcNDWI(imgdata):
    """
    Normalized Difference Water Index (NDWI)

    General formula is:
    NDWI = (Green - NIR) / (Green + NIR)

    AVIRIS equivalent of Sentinel-2 bands:
    NWDI = (859.6471nm - 1611.640) / (859.6471nm + 1611.640)
    OR
    NWDI = (859.6471nm - 2196.777) / (859.6471nm + 2196.777)

    Bands:
    NWDI = (B[53] - B[132]) / (B[53] + B[132])

    """

    bands = list(imgdata.keys())

    band1 = imgdata[bands[0]]
    band2 = imgdata[bands[1]]

    ndwi = (band1 - band2) / (band1 + band2)

    return ndwi


def saveIMG(imgdata, path, img, srs):
    # imgLayer = imgdata[imgdata.keys()[0]]

    driver = gdal.GetDriverByName('GTiff')
    rows, cols = img.shape
    out_raster = driver.Create(path, cols, rows, 1, gdal.GDT_Float32)
    out_raster.SetGeoTransform(srs["geotransform"])
    out_raster.SetProjection(srs["projection"])
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(img)
    outband.SetNoDataValue(0)  # Set 0-values as NoData
    outband.FlushCache()

if __name__ == "__main__":

    # hdrpath = r"E:\Willowstick\Remote Sensing\f201006t01p00r11\f201006t01p00r11rdn_e\f201006t01p00r11rdn_e_sc01_ort_img.hdr"
    # hdrpath = r"E:\Willowstick\Remote Sensing\f201006t01p00r11\f201006t01p00r11rdn_e\f201006t01p00r11rdn_e_sc01_ort_img"
    hdrpath= r"E:\Willowstick\Remote Sensing\f230919t01p00r06rdn_g\f230919t01p00r06rdn_g\f230919t01p00r06rdn_g_sc01_ort_img"
    imgObj, imgdata, srs = loadIMG(hdrpath, 53, 132)
    processed = calcNDWI(imgdata)

    # plt.imshow(processed)
    # plt.colorbar()
    # plt.show()

    saveIMG(imgObj, "AVIRIS_calc_NWDI2.tiff", processed, srs)
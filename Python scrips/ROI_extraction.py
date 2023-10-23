import pylidc as pl
import numpy as np
import pandas as pd
import os
import matplotlib
matplotlib.use("Qt5Agg") # Set the desired backend
import matplotlib.pyplot as plt
import pydicom
from pydicom.encaps import encapsulate
from pydicom.uid import JPEG2000
from imagecodecs import jpeg2k_encode

store_path = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\ROI extraction"


def get_ROI_Dicom(pid):
    padding = [(30, 10), (10, 25), (0, 0)]
    ann = pl.query(pl.Annotation).first()
    mask = ann.boolean_mask(pad=padding)
    ds = pydicom.dcmread(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\Images\manifest-1600709154662\LIDC-IDRI\LIDC-IDRI-0001\01-01-2000-NA-NA-30178\3000566.000000-NA-03192\1-001.dcm")
    #paddingmask(pad=padding)
    bbox = ann.bbox(pad=padding)
    vol = ann.scan.to_volume()
    vol_crop = vol[bbox]
# jpeg2k_encode to perform JPEG2000 compression
    arr_jpeg2k = jpeg2k_encode(vol_crop)
# convert from bytearray to bytes before saving to PixelData
    arr_jpeg2k = bytes(arr_jpeg2k)
    ds.Rows = vol_crop.shape[0]
    ds.Columns = vol_crop.shape[1]
    ds.PixelData = encapsulate([arr_jpeg2k])
    outputpath = os.path.join(store_path, "test.dcm")
    ds.save_as(outputpath)


pid = 'LIDC-IDRI-0001'

get_ROI_Dicom(pid)
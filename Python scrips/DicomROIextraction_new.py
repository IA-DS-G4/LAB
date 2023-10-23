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

def get_ROI_Dicom(store_path):
    anns = pl.query(pl.Annotation).filter(pl.Annotation.malignancy != 3)
    for ann in anns:
        padding = [(30, 10), (10, 25), (0, 0)]
        mask = ann.boolean_mask(pad=padding)
        pid = ann.scan.patient_id
        if pid != "LIDC-IDRI-0001": # This makes the code only transform patient 1 files. if you want to make all of them, get rid of the if condition and the continue
            continue
        path = ann.scan.get_path_to_dicom_files()
        file_list = [f.path for f in os.scandir(path)]
        print(file_list)
        ds = pydicom.dcmread("{}".format(file_list[1]))
        bbox = ann.bbox(pad=padding)
        print(bbox)
        vol = ann.scan.to_volume()
        vol_crop = vol[bbox]

        ds.Rows = vol_crop.shape[0]
        ds.Columns = vol_crop.shape[1]
        for slice in range(vol_crop.shape[2]):
            arr_jpeg2k = jpeg2k_encode(vol_crop[:,:,slice])
            arr_jpeg2k = bytes(arr_jpeg2k)
            ds.PixelData = encapsulate([arr_jpeg2k])
            try:
                os.mkdir(os.path.join(store_path, "{}".format(pid)))
            except:
                pass
            try:
                os.mkdir(os.path.join(store_path, "{}/nodule{}".format(pid,ann.id)))
            except:
                pass
            outputpath = os.path.join(store_path, "{}/nodule{}/slice{}.dcm".format(pid,ann.id,slice))
            ds.save_as(outputpath)


store_path = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\ROI extraction"
#store_path = "/home/elias88348/PycharmProjects/LIDC/annotation_dicom#"
get_ROI_Dicom(store_path)
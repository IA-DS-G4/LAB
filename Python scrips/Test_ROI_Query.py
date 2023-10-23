import pylidc as pl
import numpy as np
import pandas as pd
import os
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use("Qt5Agg")  # Set the desired backend



def get_ROI_Dicom(pid):
    ann = pl.query(pl.Annotation).first()
    padding = [(30, 10), (10, 25), (0, 0)]
    mask = ann.boolean_mask(pad=padding)
    bbox = ann.bbox(pad=padding)
    vol = ann.scan.to_volume()
    fig, ax = plt.subplots(1, 2, figsize=(5, 3))

    ax[0].imshow(vol[bbox][:, :, 2], cmap=plt.cm.gray)
    ax[0].axis('off')

    ax[1].imshow(mask[:, :, 2], cmap=plt.cm.gray)
    ax[1].axis('off')

    plt.tight_layout()
    # plt.savefig("../images/mask_bbox.png", bbox_inches="tight")
    plt.show()


pid = 'LIDC-IDRI-0001'

get_ROI_Dicom(pid)
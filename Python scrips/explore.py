import pylidc as pl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as manim
from skimage.measure import find_contours
from pylidc.utils import consensus
from sqlalchemy import func
import numpy as np
import pandas as pd



# Query for all CT scans with desired traits.
scans = pl.query(pl.Scan)
#.filter(pl.Scan.slice_thickness <= 1,pl.Scan.pixel_spacing <= 0.6)
print('Scans count')
print(scans.count())



#data = np.array([['Patient_id','slice thickness', 'num anotations']])

df = pd.DataFrame({"Patient_id":0,"slice thickness":0, "N nods":0}, index=[0])

count=1
for s in scans:
    identity=s.patient_id

    thickness=s.slice_thickness

    number_nodes=len(s.cluster_annotations())

    dfnl=pd.DataFrame({"Patient_id":identity,"slice thickness":thickness, "N nods":number_nodes},index=[count])

    df = df._append(dfnl)
    count=count+1
    if count>2:
        break

print(df)
print('identity')
print(type(identity))
nods = s.cluster_annotations()
print('explorar')
print(len(nods))
for nod in nods:
    print(nod)
anns = pl.query(pl.Annotation).filter(pl.Scan.patient_id==identity)
print(anns.count())
'''
for ann in anns:
    print()
    print(ann.malignancy)
'''

##################################################
###################################################
pid = 'LIDC-IDRI-0078'
scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).first()

#print(type(pl.Scan.slice_thickness))
#print(type(pl.Scan.slice_spacing))
#print(len(scan.annotations))

nods = scan.cluster_annotations()
print('node cont')
print(len(nods))

print("%s has %d nodules." % (scan, len(nods)))


#for i,nod in enumerate(nods):
    #print("Nodule %d has %d annotations." % (i+1, len(nods[i])))
    

#vol = scan.to_volume()

#print(vol.shape)


#print("%.2f, %.2f" % (vol.mean(), vol.std()))

#scan.visualize(annotation_groups=nods)

# class annotation
#Here I do not know hou to identify the patient
#ann = pl.query(pl.Annotation).first()
#print(ann.scan.patient_id)

anns = pl.query(pl.Annotation).filter(pl.Annotation.spiculation == 5,
                                      pl.Annotation.malignancy == 5)
print(anns.count())
# => 91
print(type(pl.Annotation.lobulation))

ann = pl.query(pl.Annotation)\
        .filter(pl.Annotation.malignancy == 5).first()

print(ann.malignancy, ann.Malignancy)

print(ann.margin, ann.Margin)

#ann.print_formatted_feature_table()

#svals = pl.query(pl.Annotation.spiculation) .filter(pl.Annotation.spiculation > 3)




#print(all([s[0] > 3 for s in svals]))


#contours = ann.contours

#print(contours[0])

#print('Features')
#print("%.2f mm, %.2f mm^2, %.2f mm^3" % (ann.diameter,
                                     #    ann.surface_area,
                                      #   ann.volume))
#mask = ann.boolean_mask()
#print(mask.shape, mask.dtype)

#bbox = ann.bbox()
#print(bbox)


#vol = ann.scan.to_volume()
#print(vol[bbox].shape)

#print(ann.bbox_dims())

#Visualization of annotations
#import matplotlib.pyplot as plt

#ann = pl.query(pl.Annotation).first()
#vol = ann.scan.to_volume()

#padding = [(30,10), (10,25), (0,0)]

#mask = ann.boolean_mask(pad=padding)
#bbox = ann.bbox(pad=padding)

#fig,ax = plt.subplots(1,2,figsize=(5,3))

#ax[0].imshow(vol[bbox][:,:,2], cmap=plt.cm.gray)
#ax[0].axis('off')

#ax[1].imshow(mask[:,:,2], cmap=plt.cm.gray)
#ax[1].axis('off')

#plt.tight_layout()
#plt.savefig("../images/mask_bbox.png", bbox_inches="tight")
#plt.show()

#ann = pl.query(pl.Annotation).first()
#ann.visualize_in_scan()

#Consensus



# Query for a scan, and convert it to an array volume.
#scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == 'LIDC-IDRI-0078').first()
#vol = scan.to_volume()

# Cluster the annotations for the scan, and grab one.
#nods = scan.cluster_annotations()
#anns = nods[0]

# Perform a consensus consolidation and 50% agreement level.
# We pad the slices to add context for viewing.
#cmask,cbbox,masks = consensus(anns, clevel=0.5,
                              #pad=[(20,20), (20,20), (0,0)])

# Get the central slice of the computed bounding box.
#k = int(0.5*(cbbox[2].stop - cbbox[2].start))



#SQLalchemy

# Fetch all highly suspicious nodules
#anns = pl.query(pl.Annotation).filter(pl.Annotation.malignancy > 3)

#ann = anns.first()
#print(ann.id, ann.Malignancy)
# => 2516, 'Highly Suspicious'




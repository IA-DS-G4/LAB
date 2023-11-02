import pylidc as pl
import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import pydicom

def get_features(pid_start,pid_end):
    # put path of dataset here
    parent_dir = r"/home/elias88348/PycharmProjects/LIDC/downloads/TCIA_LIDC-IDRI_20200921"
    # get path of LIDC-IDRI directionary
    data_dir = os.path.join(root_path, "LIDC-IDRI")
    # give directory where docker saves files
    docker_save_dir = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD:/data
    # give the hash of the pyradiomnics docker
    docker_hash = "d95ce08239e3182d8631d3492a5e4a32096d28285c3d2f10dd570d7e6d06fd01"
    # path to the features dict
    features_dict = "/data/Docker build/labs/pyradiomics-dcm/resources/featuresDict_IBSIv7.tsv"
    # pyradiomics save folder
    pyradiomics_midsave_path = "/data/pyradiomics converter test"
    # temporal dir
    temp_dir = "/data/Pyrad temp folder"


    data = pd.read_csv("features.csv")
    df = pd.read_csv("Patientids_over3mm.csv")
    dataframe = pd.DataFrame(
        columns=['Patient_ID', 'Nodule', ' Annotation', 'Subtlety', 'InternalStructure', 'Calcification', 'Sphericity',
                 'Margin', 'Lobulation', 'Spiculation', 'Texture', 'Malignancy'])
    backup = 0
    for p_id in df['Patient_ID']:
        if os.path.isdir(os.path.join(root_path, str(p_id))) == False:
            print("Patient " + str(p_id) + " not found")
            continue  # if the patient folder doesn't exist, skip it

        scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == p_id).first()
        nods = scan.cluster_annotations()


        # path to the patient folder
        patient_dir = os.path.join(data_dir, str(p_id))
        # path to dicom ct-scans of patient
        patient_dicom_path = scan.get_path_to_dicom_files()
        # get all seg folders for nodules later
        patient_seg_folders = os.listdir(patient_dicom_path)

        if scan is None: # if the scan is not available we continue
            continue
        nod = 1
        annot = 0

        for nodule in nods:
            for ann in nodule:
                backup += 1 #backupcounter

                seg_folder = os.path.join(patient_dir, patient_seg_folders[annot])

                # check how many files are in the segmentation folder
                seg_files = os.listdir(seg_folder)
                if len(seg_files) == 0:
                    # add a row with NaN values to the dataframe
                    data.loc[len(data)] = [None] * len(data.columns)
                # iterating over each segmentation file
                for file in os.listdir(seg_dir):
                    if file.endswith(".dcm"):
                        seg_file_path = os.path.join(seg_dir, file)
                        os.system("docker run -v " + str(docker_save_dir)+ str(docker_hash) + " --input-image-dir " + str(patient_dicom_path) +  " --input-seg-file " + str(seg_file_path) + " --output-dir " + str(pyradiomics_midsave_path) + " --volume-reconstructor dcm2niix --features-dict " +str(features_dict) + " --temp-dir " + str(temp_dir) + " --correct-mask")
                        try:
                            testdata = pd.read_csv("{}/1.csv".format(pyradiomics_midsave_path, file))
                            # append data to features.csv
                            data = data.append(testdata)

                            # save the data dataframe to a csv file (backup for every iteration) in the main directory
                            # thisdir = os.getcwd()
                            # os.chdir(under_root)
                            # radio.to_csv("featuresBackup.csv", index=False)
                            # os.chdir(thisdir)
                        except:
                            # append a row with NaN values to the dataframe
                            data.loc[len(data)] = [None] * len(data.columns)
                            thisdir = os.getcwd()
                            os.chdir(parent_dir)
                            # write to a log file the patient name, the seg folder name and the file name
                            log = open("log.txt", "a")
                            log.write("Failed to extract features from: " + os.getcwd() + "\n")
                            log.write("SEG File: " + file_path + "\n\n")
                            os.chdir(thisdir)
                            continue
                        # delete temp folder
                        os.system("rmdir /s /q temp")
                        print("\n\n")
                    else:
                        # also append a row with NaN values to the dataframe
                        data.loc[len(data)] = [None] * len(data.columns)

                # create feature vector
                feature = list(ann.feature_vals())
                feature.insert(0, annot + 1)
                feature.insert(0, nod)
                feature.insert(0, p_id)
                dataframe.loc[len(dataframe)] = feature

                thisdir = os.getcwd()

                # create a backup of the dataframes every 10 iterations (every 10 annotations)
                if maisumcounter % 10 == 0:
                    # METAM AQUI O CAMINHO PARA A PASTA ONDE QUEREM QUE O BACKUP SEJA GUARDADO

                    os.chdir("C:\\Users\\pedro\\Documents\\Code\\LungCancerFound\\Backups")

                    data.to_csv("pyradiomicsBackup.csv", index=False)
                    dataframe.to_csv("pylidcBackup.csv", index=False)

                    df1 = pd.read_csv("pylidcBackup.csv")
                    df2 = pd.read_csv("pyradiomicsBackup.csv")

                    df3 = pd.concat([df1, df2], axis=1)
                    df3.to_csv("total_data_obliterationBackup.csv", index=False)
                os.chdir(thisdir)

                annot += 1
            nod += 1
    os.chdir(parent_dir)

dataframe.to_csv("pylidc.csv", index=False)
data.to_csv("pyradiomics.csv", index=False)

df1 = pd.read_csv("pylidc.csv")
df2 = pd.read_csv("pyradiomics.csv")

# concatenate the columns from both dataframes
df3 = pd.concat([df1, df2], axis=1)

df3.to_csv("total_data_obliteration.csv", index=False)
import pylidc as pl
import numpy as np
import pandas as pd
import os
import shutil
import time

def get_features():
    start_time = time.time()
    # put path of dataset here
    parent_dir = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\Images+seg\manifest-1698154951594"
    patient_dicom_path_mounted = r"/data/Images+seg/manifest-1698154951594/LIDC-IDRI"
    # get path of LIDC-IDRI directionary
    data_dir = os.path.join(parent_dir, "LIDC-IDRI")
    # give directory where docker saves files
    docker_save_dir = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD"
    # give the hash of the pyradiomnics docker
    docker_hash = r"d95ce08239e3182d8631d3492a5e4a32096d28285c3d2f10dd570d7e6d06fd01"
    # path to the features dict
    features_dict = r"/data/test/featuresDict_IBSIv7.tsv"
    # pyradiomics save folder
    pyradiomics_midsave_path = r"/data/pyradiomics converter test"
    # temporal dir
    temp_dir = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\temp file"
    parameter_file = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\Pyradiomics_Params_test.yaml"
    data = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\features.csv")
    df = pd.read_excel(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\nodule_counts_by_patient.xlsx")
    df = df.drop(df.columns[[4, 5]], axis=1)
    df.columns = ['Patient_ID', 'Total_Nodule_Count', 'NodG3','NodL3']
    dataframe = pd.DataFrame(
        columns=['Patient_ID', 'Nodule', ' Annotation', 'Subtlety', 'InternalStructure', 'Calcification', 'Sphericity',
                 'Margin', 'Lobulation', 'Spiculation', 'Texture', 'Malignancy'])
    backup = 0
    iteration_counter = 1
    for p_id in df['Patient_ID']:

        print("Patient " + str(p_id) + "Processing")
        if os.path.isdir(os.path.join(data_dir, str(p_id))) == False:
            print("Patient " + str(p_id) + " not found")
            continue  # if the patient folder doesn't exist, skip it

        scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == p_id).first()
        nods = scan.cluster_annotations()

        if scan is None: # if the scan is not available we continue
            continue

        # path to the patient folder
        patient_dir = os.path.join(data_dir, str(p_id))
        # path to dicom ct-scans of patient
        patient_dicom_path = scan.get_path_to_dicom_files()

        patient_folders = os.path.join(patient_dir, os.listdir(patient_dir)[0])
        if len(os.listdir(patient_folders))==1:
            shutil.rmtree(os.path.join(patient_dir, os.listdir(patient_dir)[0]))
            patient_folders = os.path.join(patient_dir, os.listdir(patient_dir)[0])
            print("wrong folder removed!")

        # listing all the folders from a patient
        patient_seg_folders = os.listdir(patient_folders)
        for folder in patient_seg_folders:
            if "evaluations" in folder:
                shutil.rmtree(os.path.join(patient_folders,folder))
        patient_seg_folders = os.listdir(patient_folders)
        # saving the dicom images folder path
        # get all seg folders for nodules later


        nod = 1
        annot = 0
        for nodule in nods:
            for ann in nodule:
                if annot >= len(patient_seg_folders):
                    continue
                backup += 1 #backupcounter

                iteration_counter += 1
                seg_folder = os.path.join(patient_folders, patient_seg_folders[annot+1])

                # check how many files are in the segmentation folder
                seg_files = os.listdir(seg_folder)
                if len(seg_files) <= 0:
                    # add a row with NaN values to the dataframe
                    data.loc[len(data)] = [None] * len(data.columns)
                # iterating over each segmentation file
                for file in os.listdir(seg_folder):
                    if file.endswith(".dcm"):
                        seg_file_path = os.path.join(seg_folder, file)
                        print("docker run -v \"" + docker_save_dir + ":/data\" " + docker_hash + " --input-image-dir \"/data/" + os.path.relpath(patient_dicom_path, docker_save_dir).replace(chr(92),"/") +  "\" --input-seg-file \"/data/" + os.path.relpath(seg_file_path, docker_save_dir).replace(chr(92),"/") + "\" --output-dir \"" + pyradiomics_midsave_path + "\" --volume-reconstructor dcm2niix --features-dict \"/data/" + os.path.relpath(features_dict, docker_save_dir).replace(chr(92),"/") + "\" --temp-dir \"/data/" + os.path.relpath(temp_dir, docker_save_dir).replace(chr(92),"/") + "\" --correct-mask --parameters \"/data/" + os.path.relpath(parameter_file, docker_save_dir).replace(chr(92),"/") + "\"")
                        os.system("docker run -v \"" + docker_save_dir + ":/data\" " + docker_hash + " --input-image-dir \"/data/" + os.path.relpath(patient_dicom_path, docker_save_dir).replace(chr(92),"/") +  "\" --input-seg-file \"/data/" + os.path.relpath(seg_file_path, docker_save_dir).replace(chr(92),"/") + "\" --output-dir \"" + pyradiomics_midsave_path + "\" --volume-reconstructor dcm2niix --features-dict \"/data/" + os.path.relpath(features_dict, docker_save_dir).replace(chr(92),"/") + "\" --temp-dir \"/data/" + os.path.relpath(temp_dir, docker_save_dir).replace(chr(92),"/") + "\" --correct-mask --parameters \"/data/" + os.path.relpath(parameter_file, docker_save_dir).replace(chr(92),"/") + "\"")

                        try:
                            testdata = pd.read_csv(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\temp file\Features\1.csv")
                            #print(testdata)
                            # append data to features.csv
                            #print(data.info())
                            #data = data.append(testdata)
                            data = pd.concat([data, testdata], ignore_index=True)
                            #print(data)


                        except:
                            # append a row with NaN values to the dataframe
                            data.loc[len(data)] = [None] * len(data.columns)
                            thisdir = os.getcwd()
                            os.chdir(parent_dir)
                            # write to a log file the patient name, the seg folder name and the file name
                            log = open("log.txt", "a")
                            log.write("Failed to extract features from: " + os.getcwd() + "\n")
                            log.write("SEG File: " + file + "\n\n")
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
                feature.insert(0, annot)
                feature.insert(0, nod)
                feature.insert(0, p_id)
                dataframe.loc[len(dataframe)] = feature

                thisdir = os.getcwd()

                # create a backup of the dataframes every 10 iterations (every 5 annotations)
                if backup % 10 == 0:
                    current_time = time.time()
                    runtime = (current_time - start_time)/60
                    print('Iteration: ' + str(iteration_counter) + '-----Backup create------------time:' + str(runtime))
                    os.chdir(r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\Backups")

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

get_features()

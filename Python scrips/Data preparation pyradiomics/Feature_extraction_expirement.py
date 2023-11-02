import pylidc as pl
import numpy as np
import pandas as pd
import os
import shutil
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_docker(docker_save_dir, docker_hash, patient_dicom_path, seg_file_path, pyradiomics_midsave_path,
               features_dict, temp_dir, parameter_file):
    docker_command = (
        f"docker run -v \"{docker_save_dir}:/data\" {docker_hash} "
        f"--input-image-dir \"/data/{os.path.relpath(patient_dicom_path, docker_save_dir).replace(chr(92), '/')}\" "
        f"--input-seg-file \"/data/{os.path.relpath(seg_file_path, docker_save_dir).replace(chr(92), '/')}\" "
        f"--output-dir \"{pyradiomics_midsave_path}\" "
        f"--volume-reconstructor dcm2niix "
        f"--features-dict \"/data/{os.path.relpath(features_dict, docker_save_dir).replace(chr(92), '/')}\" "
        f"--temp-dir \"/data/{os.path.relpath(temp_dir, docker_save_dir).replace(chr(92), '/')}\" "
        f"--correct-mask "
        f"--parameters \"/data/{os.path.relpath(parameter_file, docker_save_dir).replace(chr(92), '/')}\""
    )
    subprocess.run(docker_command, shell=True)

def process_nodule(p_id, nod, annot, data, dataframe, parent_dir, data_dir, docker_save_dir, docker_hash,
                    pyradiomics_midsave_path, features_dict, temp_dir, parameter_file):
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == p_id).first()
    nods = scan.cluster_annotations()

    patient_dir = os.path.join(data_dir, str(p_id))
    patient_dicom_path = scan.get_path_to_dicom_files()
    patient_folders = os.path.join(patient_dir, os.listdir(patient_dir)[0])

    if len(os.listdir(patient_folders)) == 1:
        shutil.rmtree(os.path.join(patient_dir, os.listdir(patient_dir)[0]))
        patient_folders = os.path.join(patient_dir, os.listdir(patient_dir)[0])
        print("wrong folder removed!")

    patient_seg_folders = os.listdir(patient_folders)
    for folder in patient_seg_folders:
        if "evaluations" in folder:
            shutil.rmtree(os.path.join(patient_folders, folder))
    patient_seg_folders = os.listdir(patient_folders)

    for nodule in nods:
        for ann in nodule:
            if annot >= len(patient_seg_folders):
                continue

            seg_folder = os.path.join(patient_folders, patient_seg_folders[annot + 1])

            seg_files = os.listdir(seg_folder)
            if len(seg_files) == 0:
                data.loc[len(data)] = [None] * len(data.columns)

            for file in os.listdir(seg_folder):
                if file.endswith(".dcm"):
                    seg_file_path = os.path.join(seg_folder, file)
                    run_docker(docker_save_dir, docker_hash, patient_dicom_path, seg_file_path,
                               pyradiomics_midsave_path, features_dict, temp_dir, parameter_file)

                    try:
                        testdata = pd.read_csv(
                            r"/test/temp file/Features/1.csv")
                        data = pd.concat([data, testdata], ignore_index=True)
                    except:
                        data.loc[len(data)] = [None] * len(data.columns)
                        thisdir = os.getcwd()
                        os.chdir(parent_dir)
                        log = open("log.txt", "a")
                        log.write("Failed to extract features from: " + os.getcwd() + "\n")
                        log.write("SEG File: " + file + "\n\n")
                        os.chdir(thisdir)
                        continue

                    os.system("rmdir /s /q temp")
                    print("\n\n")
                else:
                    data.loc[len(data)] = [None] * len(data.columns)

            feature = list(ann.feature_vals())
            feature.insert(0, annot)
            feature.insert(0, nod)
            feature.insert(0, p_id)
            dataframe.loc[len(dataframe)] = feature

            thisdir = os.getcwd()

            if backup % 20 == 0:
                current_time = time.time()
                runtime = (current_time - start_time) / 60
                print('Iteration: ' + str(iteration_counter) + '-----Backup create------------time:' + str(runtime))
                os.chdir(
                    r"/test/Backups")

                data.to_csv("pyradiomicsBackup.csv", index=False)
                dataframe.to_csv("pylidcBackup.csv", index=False)

                df1 = pd.read_csv("pylidcBackup.csv")
                df2 = pd.read_csv("pyradiomicsBackup.csv")

                df3 = pd.concat([df1, df2], axis=1)
                df3.to_csv("total_data_obliterationBackup.csv", index=False)
            os.chdir(thisdir)

            annot += 1

def get_features():
    start_time = time.time()
    parent_dir = r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\Images+seg\manifest-1698154951594"
    docker_save_dir = r"/"
    docker_hash = r"d95ce08239e3182d8631d3492a5e4a32096d28285c3d2f10dd570d7e6d06fd01"
    features_dict = r"/data/test/featuresDict_IBSIv7.tsv"
    pyradiomics_midsave_path = r"/data/pyradiomics converter test"
    temp_dir = r"/test/temp file"
    parameter_file = r"/test/Pyradiomics_Params_test.yaml"

    data_dir = os.path.join(parent_dir, "LIDC-IDRI")
    features_data = pd.read_csv(
        r"/test/features.csv")
    data = features_data.drop(0, axis=0)
    df = pd.read_excel(
        r"C:\Users\Diederik\OneDrive\Bureaublad\studie tn\Minor vakken Porto\IA CAD\test\nodule_counts_by_patient.xlsx")
    df = df.drop(df.columns[[4, 5]], axis=1)
    df.columns = ['Patient_ID', 'Total_Nodule_Count', 'NodG3', 'NodL3']
    dataframe = pd.DataFrame(
        columns=['Patient_ID', 'Nodule', ' Annotation', 'Subtlety', 'InternalStructure', 'Calcification', 'Sphericity',
                 'Margin', 'Lobulation', 'Spiculation', 'Texture', 'Malignancy'])
    backup = 0
    iteration_counter = 1

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_nodule, p_id, nod, 0, data, dataframe, parent_dir, data_dir, docker_save_dir, docker_hash,
                                   pyradiomics_midsave_path, features_dict, temp_dir, parameter_file) for p_id, nod in zip(df['Patient_ID'], range(1, len(df['Patient_ID']) + 1))]

        for future in futures:
            future.result()

    os.chdir(parent_dir)

    dataframe.to_csv("pylidc.csv", index=False)
    data.to_csv("pyradiomics.csv", index=False)

    df1 = pd.read_csv("pylidc.csv")
    df2 = pd.read_csv("pyradiomics.csv")

    df3 = pd.concat([df1, df2], axis=1)
    df3.to_csv("total_data_obliteration.csv", index=False)

get_features()

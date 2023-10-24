import os
import pandas as pd
import pylidc as pl

# iterate over every directory in the current directory
# move into the "LIDC-IDRI" directory

#if the directory im at right now is not BatchExtractor, print "idiot"
if os.getcwd().split("\\")[-1] != "BatchExtractor":
    print("Diretório errado idiota")
    exit()


data = pd.read_csv("features.csv")
print(data)
print()

# grab all the patient IDs
df = pd.read_excel("nodule_counts_by_patient.xlsx")
df = df.drop(df.columns[[4,5]], axis=1)
df.columns = ['Patient_ID', 'Total_Nodule_Count', 'NodG3', 'NodL3']

under_root = os.getcwd()

os.chdir("LIDC-IDRI")
root_path = os.getcwd()

# create the patients data using pylidc for further use
dataframe = pd.DataFrame(columns=['Patient_ID','Nodule',' Annotation', 'Subtlety', 'InternalStructure', 'Calcification', 'Sphericity', 'Margin', 'Lobulation', 'Spiculation', 'Texture', 'Malignancy'])

begin = int(input("Set beggining (including): "))
end = int(input("Set ending (including): "))

count = 0
maisumcounter = 0
for p_id in df['Patient_ID']:
    count += 1
    # begin and end are the indexes of the patients to be processed
    if count < begin or count > end:
        continue
    print("\n\nPatient " + str(p_id) + " - " + str(count) + "/" + str(len(df['Patient_ID'])))
    # escolher o dicom
    if os.path.isdir(os.path.join(root_path, str(p_id))) == False:
        print("Patient " + str(p_id) + " not found")
        continue # if the patient folder doesn't exist, skip it

    patient_dir = os.path.join(root_path, str(p_id))
    patient_folders = os.path.join(patient_dir, os.listdir(patient_dir)[0])

    # listing all the folders from a patient
    insides=os.listdir(patient_folders)
    
    # saving the dicom images folder path
    dicom_dir=os.path.join(patient_folders,insides[-1])
    
    scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == p_id).first()
    if scan is None:
        continue
    nods = scan.cluster_annotations()
    nod=1
    annot=0
    for nodule in nods:
        for ann in nodule:
            maisumcounter += 1
            # criar uma entrada no dataframe
            # saving the segmentation path
            seg_dir = os.path.join(patient_folders,insides[annot])
            
            # check how many files are in the segmentation folder
            seg_files = os.listdir(seg_dir)
            if len(seg_files) == 0:
                # add a row with NaN values to the dataframe
                data.loc[len(data)] = [None] * len(data.columns)
            # saving the annotation file path
            for file in os.listdir(seg_dir):
                if file.endswith(".dcm"):
                    file_path = os.path.join(seg_dir, file)
                    print(file_path)
            
                    # running the pyradiomics extractions script using the paths saved before

                    # ALTEREM O CAMINHO PARA O VOSSO

                    os.system("python C:\\Users\\pedro\\Documents\\Code\\LungCancerFound\\BatchExtractor\\pyradiomics-dcm\\pyradiomics-dcm.py --input-image-dir " + dicom_dir + " --input-seg " + file_path + " --output-dir " + root_path +"/Output" + " --features-dict C:\\Users\\pedro\\Documents\\Code\\LungCancerFound\\BatchExtractor\\pyradiomics-dcm\\resources\\featuresDict.tsv --correct-mask --temp-dir " + root_path + "/temp")
                    
                    # grab the temp/Features/1.csv file and append the feature entry to a pandas dataframe
                    try:
                        testdata = pd.read_csv("temp/Features/1.csv")
                        # append data to features.csv
                        data = data.append(testdata)

                        # save the data dataframe to a csv file (backup for every iteration) in the main directory
                        #thisdir = os.getcwd()
                        #os.chdir(under_root)
                        #radio.to_csv("featuresBackup.csv", index=False)
                        #os.chdir(thisdir)
                    except:
                        # append a row with NaN values to the dataframe
                        data.loc[len(data)] = [None] * len(data.columns)
                        thisdir = os.getcwd()
                        os.chdir(under_root)
                        # write to a log file the pacient name, the seg folder name and the file name
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


            ##COMANDO DO PYRADIOMICS USANDO dicom COMO DICOM FILE e seg COMO SEGMENTATION FILE
            feature = list(ann.feature_vals())
            feature.insert(0,annot + 1)
            feature.insert(0,nod)
            feature.insert(0,p_id)
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

            annot+=1
        nod+=1
os.chdir(under_root)

dataframe.to_csv("pylidc.csv", index=False)
data.to_csv("pyradiomics.csv", index=False)

df1 = pd.read_csv("pylidc.csv")
df2 = pd.read_csv("pyradiomics.csv")

# concatenate the columns from both dataframes
df3 = pd.concat([df1, df2], axis=1)

df3.to_csv("total_data_obliteration.csv", index=False)
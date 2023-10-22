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
#Number of total scans
#print('Scans count')
print(scans.count())


#Construction of the dataframe with the first row with 0 values to be droped in the end 
df = pd.DataFrame({"Nod_id":0,"Patient_id":0,"slice thickness":0, "N nods":0, "Spiculation_Min":0, "Spiculation_Med":0, "Spiculation_Max":0,"Internal_Structure":0,"Calcification":0,"Sphericity":0,"Margin_min":0,"Margin_mean":0,"Margin_max":0,"Lobulation_min":0,"Lobulation_mean":0,"Lobulation_max":0,"Spiculation_Min":0, "Spiculation_Med":0, "Spiculation_Max":0,"Texture":0,"Malignancy_min":0,"Malignancy_mean":0,"Malignancy_max":0,"Malignancy_n4":0,"Malignancy_n5":0}, index=[0])

count=1
for s in scans:
    identity=s.patient_id

    thickness=s.slice_thickness

    nods=s.cluster_annotations()
    
    number_nodes=len(nods)

    for i,nod in enumerate(nods):
        print(count)
        l= len(nods[i]) #number of anotations for each node

        #to determine the values related to subtlety (mean, min, max)
        sb_sum=nods[i][0].subtlety
        sb_min=nods[i][0].subtlety
        sb_max=nods[i][0].subtlety

        
        for j in range(1,l):#since the element of order 0 is outside the cicle, the cicle starts at order 1
            sb_sum=sb_sum+nods[i][j].subtlety
            if(nods[i][j].subtlety>sb_max):
                sb_max=nods[i][j].subtlety
            if(nods[i][j].subtlety<sb_min):
                sb_min=nods[i][j].subtlety
        sb_mean=sb_sum/l
        



        #to determine the value related to internal structure (ni - value with more frequency)
        count1=0
        count2=0
        count3=0
        count4=0
        
        for j in range(0,l):
            if(nods[i][j].internalStructure==1):
                count1+=1
            if(nods[i][j].internalStructure==2):
                count2+=1
            if(nods[i][j].internalStructure==3):
                count3+=1
            if(nods[i][j].internalStructure==4):
                count4+=1
        internal=1
        if(count2>count1):
            internal=2
        if((count3>count2) & (count3>count1)):
            internal=3
        if((count4>count3) & (count4>count2) & (count4>count1)):
            internal=4

        #to determine the value related to calcification (ni - value with more frequency)
        count1=0
        count2=0
        count3=0
        count4=0
        count5=0
        count6=0
        
        
        for j in range(0,l):
            if(nods[i][j].calcification==1):
                count1+=1
            if(nods[i][j].calcification==2):
                count2+=1
            if(nods[i][j].calcification==3):
                count3+=1
            if(nods[i][j].calcification==4):
                count4+=1
            if(nods[i][j].calcification==5):
                count5+=1
            if(nods[i][j].calcification==6):
                count6+=1
           
        calcification=1
        if(count2>count1):
            calcification=2
        if((count3>count2) & (count3>count1)):
            calcification=3
        if((count4>count3) & (count4>count2) & (count4>count1)):
            calcification=4
        if((count5>count4) & (count5>count3) & (count5>count2) & (count5>count1)):
            calcification=5
        if((count6>count5) & (count6>count4) & (count6>count3) & (count6>count2) & (count6>count1)):
            calcification=6

        #to determine the value related to sphericity (ni - value with more frequency)
        count1=0
        count2=0
        count3=0
        count4=0
        count5=0
  
        
        
        for j in range(0,l):
            if(nods[i][j].sphericity==1):
                count1+=1
            if(nods[i][j].sphericity==2):
                count2+=1
            if(nods[i][j].sphericity==3):
                count3+=1
            if(nods[i][j].sphericity==4):
                count4+=1
            if(nods[i][j].sphericity==5):
                count5+=1
           
           
        sphericity=1
        if(count2>count1):
            sphericity=2
        if((count3>count2) & (count3>count1)):
            sphericity=3
        if((count4>count3) & (count4>count2) & (count4>count1)):
            sphericity=4
        if((count5>count4) & (count5>count3) & (count5>count2) & (count5>count1)):
            sphericity=5
            
        #to determine the values related to margin (mean, min, max)
        margin_sum=nods[i][0].margin
        margin_min=nods[i][0].margin
        margin_max=nods[i][0].margin

        
        for j in range(1,l):#since the element of order 0 is outside the cicle, the cicle starts at order 1
            margin_sum=margin_sum+nods[i][j].margin
            if(nods[i][j].margin>margin_max):
                margin_max=nods[i][j].margin
            if(nods[i][j].margin<margin_min):
                margin_min=nods[i][j].margin
        margin_mean=margin_sum/l



        #to determine the values related to lobulation (mean, min, max)
        lobulation_sum=nods[i][0].lobulation
        lobulation_min=nods[i][0].lobulation
        lobulation_max=nods[i][0].lobulation

        
        for j in range(1,l):#since the element of order 0 is outside the cicle, the cicle starts at order 1
            lobulation_sum=lobulation_sum+nods[i][j].lobulation
            if(nods[i][j].lobulation>lobulation_max):
                lobulation_max=nods[i][j].lobulation
            if(nods[i][j].lobulation<lobulation_min):
                lobulation_min=nods[i][j].lobulation
        lobulation_mean=lobulation_sum/l
       
        
        
        #to determine the values related to spiculation (mean, min, max)
        spi_sum=nods[i][0].spiculation
        spi_min=nods[i][0].spiculation
        spi_max=nods[i][0].spiculation

        
        for j in range(1,l):#since the element of order 0 is outside the cicle, the cicle starts at order 1
            spi_sum=spi_sum+nods[i][j].spiculation
            if(nods[i][j].spiculation>spi_max):
                spi_max=nods[i][j].spiculation
            if(nods[i][j].spiculation<spi_min):
                spi_min=nods[i][j].spiculation
        spi_mean=spi_sum/l



        #to determine the value related to texture (ni - value with more frequency)
        count1=0
        count2=0
        count3=0
        count4=0
        count5=0
  
        
        
        for j in range(0,l):
            if(nods[i][j].texture==1):
                count1+=1
            if(nods[i][j].texture==2):
                count2+=1
            if(nods[i][j].texture==3):
                count3+=1
            if(nods[i][j].texture==4):
                count4+=1
            if(nods[i][j].texture==5):
                count5+=1
           
           
        texture=1
        if(count2>count1):
            texture=2
        if((count3>count2) & (count3>count1)):
            texture=3
        if((count4>count3) & (count4>count2) & (count4>count1)):
            texture=4
        if((count5>count4) & (count5>count3) & (count5>count2) & (count5>count1)):
            texture=5




        #to determine the value related to texture malignancy (min, mean, max, n4, n5)

        malignancy_sum=nods[i][0].malignancy
        malignancy_min=nods[i][0].malignancy
        malignancy_max=nods[i][0].malignancy
    
  
        for j in range(1,l):#since the element of order 0 is outside the cicle, the cicle starts at order 1
            malignancy_sum=malignancy_sum+nods[i][j].malignancy
            if(nods[i][j].malignancy>malignancy_max):
                malignancy_max=nods[i][j].malignancy
            if(nods[i][j].malignancy<malignancy_min):
                malignancy_min=nods[i][j].malignancy
        malignancy_mean=malignancy_sum/l
        
       
        
        count4=0
        count5=0
        for j in range(0,l):
            if(nods[i][j].malignancy==4):
                count4+=1
            if(nods[i][j].malignancy==5):
                count5+=1
        

        #Create an ID for each node concatenating the Patient ID with the number of its node
        nod_id=identity+'-'+str(i+1)
       
    
    

        dfnl=pd.DataFrame({"Nod_id":nod_id,"Patient_id":identity,"slice thickness":thickness, "N nods":number_nodes, "Subtlety_Min":sb_min, "Subtlety_Med":sb_mean, "Subtlety_Max":sb_max,"Internal_Structure":internal,"Calcification":calcification,"Sphericity":sphericity,"Margin_min":margin_min,"Margin_mean":margin_mean,"Margin_max":margin_max,"Lobulation_min":lobulation_min,"Lobulation_mean":lobulation_mean,"Lobulation_max":lobulation_max,"Spiculation_Min":spi_min, "Spiculation_Med":spi_mean, "Spiculation_Max":spi_max,"Texture":texture,"Malignancy_min":malignancy_min,"Malignancy_mean":malignancy_mean,"Malignancy_max":malignancy_max,"Malignancy_n4":count4,"Malignancy_n5":count5},index=[count])

        df = df._append(dfnl)
        count=count+1
    #if count>100:
        #break

df.drop(index=df.index[0], axis=0, inplace=True)
#print(df[["Malignancy_min","Malignancy_mean","Malignancy_max","Malignancy_n4","Malignancy_n5"]])

df.to_csv("pylidc_csv.csv")

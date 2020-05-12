# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 13:44:25 2020

@author: fcosta
"""
#Header:
#04272020 - Francisco Costa
#SWE - Stuttgart

#Calculation Hardware uncertainties:
#This code calculates uncertainties related with hardware in lidar devices, classifying them in different classes which are the different hardware modules the lidar is divided in.

#Definition of classes:
#Amplifier: figure noise.

#%% Modules to import: 
from ImportModules import *
#from LiUQ_inputs import flag_plot_signal_noise
import pandas as pd
import UQ_Hardware  # script with all calculations of hardware unc are done
import UQ_Data_processing # script with all calculations of data processing methods unc are done
import numpy as np
import pdb
#import pickle
import itertools
import matplotlib.pyplot as plt
#%% Read data from the GUI script:#######################
#with open('I_D.pickle', 'rb') as c_data:
#    ImpDATA = pickle.load(c_data)
#    modules=ImpDATA[0]
#    DP=ImpDATA[1]
#    temperature=ImpDATA[2]
#    humidity=ImpDATA[3]
#    noise_amp=ImpDATA[4]
#    o_c_amp=ImpDATA[5]
#    o_c_photo=ImpDATA[6]
#    noise_photo=ImpDATA[7]
#    curvature_lens=ImpDATA[8]
#    o_c_tele=ImpDATA[9]
#    aberration=ImpDATA[10]
#########################################################

modules = [each_string.lower() for each_string in modules] #lower case
DP      = [each_string.lower() for each_string in DP] #lower case


#Definig the lists we fill later on within the process;
H_UQ={}
DP_UQ=[] # To work on in the future
subcolumns=[]# columns of the dataframe
#%% Hardware:

class Hardware_U():  # creating a function to call each different module. HAve to add an if for a new module
    Res={}# Dictionary outcome stored in Res
    if 'amplifier' in modules:
            class amplifier(): # Create class amplifier
                def Amp_noise(self,Atmospheric_inputs,Amplifier_uncertainty_inputs): # Calculation of losses in amplifier
                    UQ_Amp=UQ_Hardware.UQ_Amplifier(Atmospheric_inputs,Amplifier_uncertainty_inputs)
                    return UQ_Amp
                def Amp_losses(self): # Calculation of losses in amplifier                   
                    self.amp_losses=[0.6]
                    return self.amp_losses
                def Amp_others(self):                    
                    self.amp_others=[0,99]
                    return self.amp_others
                def Amp_Failures(self):
                    self.ampli_failures=[0.01]
                    return self.ampli_failures 
            Obj=amplifier()#Create instance of object amplifier
            # Every calculation method ("def whatever...") included in "class amplifier()" should be added also in "RES['amplifier']" as a new dictionary key:value pair
            Res['amplifier']=({'Ampli_noise':Obj.Amp_noise(Atmospheric_inputs,Amplifier_uncertainty_inputs),'Ampli_losses':Obj.Amp_losses(),'Ampli_DELTA':Obj.Amp_others(),'Ampli_Failures':Obj.Amp_Failures()})# Creating a nested dictionary
            subcolumns.append([Obj.Amp_losses(),Obj.Amp_others(),Obj.Amp_Failures()])
    if 'photodetector' in modules:
            class photodetector():
                def Photo_noise(self,Atmospheric_inputs,Photodetector_uncertainty_inputs):
                    UQ_Photo=UQ_Hardware.UQ_Photodetector(Atmospheric_inputs,Photodetector_uncertainty_inputs)#function calculating amplifier uncertainties ((UQ_Photodetector.py))
                    return UQ_Photo   
                def Photo_losses(self):                   
                    self.photo_losses=[1.1]
                    return self.photo_losses
                def Photo_Failures(self):
                    self.photo_failures=[1,0]
                    return self.photo_failures               
            Obj=photodetector()
            Res['photodetector']=({'Photo_noise':Obj.Photo_noise(Atmospheric_inputs,Photodetector_uncertainty_inputs),'Photo_losses':Obj.Photo_losses(),'Photo_Failures':Obj.Photo_Failures()})                                         
            subcolumns.append([Obj.Photo_losses(), Obj.Photo_Failures()])
    if 'telescope' in modules:
            class telescope():
                def Tele_noise(self,Atmospheric_inputs,Telescope_uncertainty_inputs):
                    UQ_Tele=UQ_Hardware.UQ_Telescope(Atmospheric_inputs,Telescope_uncertainty_inputs)#function calculating amplifier uncertainties ((UQ_Telescope.py))
                    return UQ_Tele
                def Tele_losses(self):                   
                    self.tele_losses=[0.8]
                    return self.tele_losses
                def Tele_others(self):                    
                    self.tele_others=[0.3]
                    return self.tele_others
                def Tele_Failures(self):                    
                    self.tele_failures=[1.2,0.7]
                    return self.tele_failures   
            Obj=telescope()
            Res['telescope']=({'Tele_noise':Obj.Tele_noise(Atmospheric_inputs,Telescope_uncertainty_inputs),'Tele_losses':Obj.Tele_losses(),'Tele_DELTA':Obj.Tele_others(),'Tele_Failures':Obj.Tele_Failures()})
            subcolumns.append([Obj.Tele_losses(),Obj.Tele_Failures(),Obj.Tele_others()])

#Create H_UQ dictionary of values: 
H_Obj=Hardware_U()# HArdware instance
for i in modules:       
    H_UQ[i]=(H_Obj.Res[i])
#    count_index+=1
#If want to make fast calculations can apply: Hardware_U().amplifier().Amp_noise(25,20,5,.005)
    
#%% Data processing:
for method in DP:
    def Data_Processing_U(method=method):
        if method=='los': 
            UQ_LineOfSight= UQ_Data_processing.UQ_LOS() #function calculating amplifier uncertainties ((UQ_Amplifier.py))
            return UQ_LineOfSight
        elif method=='filtering_methods': 
            UQ_Filtering= UQ_Data_processing.UQ_FilterMethods() #function calculating amplifier uncertainties ((UQ_Amplifier.py))
            return UQ_Filtering
    DP_UQ.append(Data_Processing_U(method=method))

#%% Create a complete data frame (Hardware+data processing uncertainties): 

#Generate list of keys and values to loop over
Values_errors = [list(itertools.chain((H_UQ[ind_error_val].values()))) for ind_error_val in H_UQ.keys()]
Keys_errors   = [list(itertools.chain((H_UQ[ind_error_key].keys()))) for ind_error_key in H_UQ.keys()]

#Generate indexes and columns of the data frame:
subindices = list((itertools.chain(*Keys_errors)))
# These three rows explain step by step how subcolumns is achieved:
#Errors_inputVal       = list(itertools.product(*list(itertools.chain(*subcolumns))))
#Atmospheric_inputsVal = list(itertools.product(*list(itertools.chain(*list([Atmospheric_inputs.values()])))))
#subcolumns            = list(itertools.chain(itertools.product(Atmospheric_inputsVal,Errors_inputVal)))
subcolumns = list(itertools.chain(itertools.product(list(itertools.product(*list(itertools.chain(*list([Atmospheric_inputs.values()]))))),list(itertools.product(*list(itertools.chain(*subcolumns)))))))
subcolumns = [str(list(itertools.chain(*subcolumns [indSub]))) for indSub in range(len(subcolumns))]

#Flattening the error values not including noise errors because noise errors are not repeated for all the scenarios
Values_errors_removed    = [list(itertools.product(*Values_errors[i][1:])) for i in range (len (Values_errors))] # values of the rest of errors (not related with atmospheric conditions) 
fl_Values_errors_removed = list(itertools.product(*Values_errors_removed)) #Flatted values errors removed

#extract noise errors. Is [0] hardcoded because noise errors are always the first position of "Values_errors" list
Values_errors_noise      = [Values_errors[i][0] for i in range (len (Values_errors))]
Values_errors_noise_DEF  = list(map(list,list(zip(*Values_errors_noise))))
fl_Values_errors_removed = list(map(list,fl_Values_errors_removed))
List_Scenarios           = []
Final_Scenarios          = []
for indc in range(len(Values_errors_noise_DEF)):
    List_Scenarios.append(([list(zip(Values_errors_noise_DEF[indc],fl_Values_errors_removed[indc2])) for indc2 in range(len(fl_Values_errors_removed))]))
List_Scenarios = list(itertools.chain.from_iterable(List_Scenarios))
for indIter in range(len(List_Scenarios)):
    Final_Scenarios.append(list(itertools.chain(*(i if isinstance(i, tuple) else (i,) for i in list(itertools.chain(*(i if isinstance(i, tuple) else (i,) for i in List_Scenarios[indIter])))))))

df_UQ=pd.DataFrame(np.transpose(Final_Scenarios),index=subindices,columns=subcolumns)    

#Sum af decibels:
in_dB=0
Sum_decibels= []
for valcols in range(0,df_UQ.shape[1]):
    Sum_in_dB     = sum([(10**(df_UQ.iloc[valrows,valcols]/10)) for valrows in range(0,df_UQ.shape[0])])
#    Sum_in_dB = sum(in_dB)
    Sum_decibels.append(10*np.log10(Sum_in_dB) )


df_UQ.loc['Total UQ']= Sum_decibels# for now sum the uncertainties. Here have to apply Uncertainty expansion.

#transform in watts. We supose that raw data is in dB:
#df_UQ['Hardware (w)']=(10**(df_UQ['Hardware (dB)']/10))



## GUI Stuff ############################################
#with open ('DF.pickle','wb') as DATAFRAME:
#    pickle.dump([df_H_UQ,df_DP_UQ,df_UQ],DATAFRAME)
#######################################################

#%% Plotting:
flag_plot_signal_noise=True
if flag_plot_signal_noise==True: #Introduce this flag in the gui    
    #Create original received power signal in watts (for now this is necessary):
    t           = np.linspace(0,100,1000)
    O_signal_W  = (6*np.sin(t/(2*np.pi)))**2 #original in w (**2 because is supoused original signal are volts)
    O_signal_dB = 10*np.log10(O_signal_W) # original in dB
    #Plotting:
    # Plotting original signal in (w)
    #plt.subplot(1,2,1)
    
    

    
    #adding Hardware noise in a loop over all error for all different scenarios
    #np.shape(df_UQ)[1]):
    noise_H_dB=[df_UQ.iloc[ind_Scen,0] for ind_Scen in range(np.shape(df_UQ)[0])] # in dB
    noise_H_W=[10**(noise_H_dB[i]/10)  for i in range (len(noise_H_dB)) ]#convert into watts    
    mean_noise=0
    stdv=np.sqrt(noise_H_W)
    noise_W=[np.random.normal(mean_noise,stdv[ind_stdv],len(O_signal_W)) for ind_stdv in range(len(stdv)) ]#add normal noise centered in 0 and stdv
    Noisy_signal_W=[O_signal_W+noise_W[ind_fociflama] for ind_fociflama in range(len(noise_W))]
    Noisy_signal_dB=[10*np.log10(Noisy_signal_W[in_noise]) for in_noise in range(len(Noisy_signal_W))]#Summmm od DB
    
    #Plotting:
    plt.figure()
    plt.plot(t,O_signal_W)
    plt.plot(t,Noisy_signal_W[-1],'g') 
    plt.title('Signal + noise [watts]')
    plt.xlabel('time [s]')
    plt.ylabel('power intensity [dB]')
    
    plt.show() #original + noise (w) 
    for ind_plot_W in [0,2,4]:
        plt.plot(t,Noisy_signal_W[ind_plot_W],'--') 
        plt.legend(['original','Total Noise'+str(),'Ampli_noise','Ampli_losses','Ampli_DELTA','Ampli_Failures','Tele_Noise'])#,'Total error [w]'])
    
    plt.show() 
        
    #Plotting original signal in  (dB)
    plt.figure()
    plt.plot(t,O_signal_dB)
    plt.title('Signal + noise [dB]')
    plt.ylabel('power intensity [dB]')
    plt.xlabel('time [s]')
    plt.plot(t,Noisy_signal_dB[-1],'go-') 

    # original + noise (dB)        
    for ind_plot_dB in [0,2,4]:
        plt.plot(t,Noisy_signal_dB[ind_plot_dB],'--')        
        
        plt.legend(['original','Total Noise'+str(),'Ampli_noise','Ampli_losses','Ampli_DELTA','Ampli_Failures','Tele_Noise'])#,'Total error [w]'])
    
    plt.show()  

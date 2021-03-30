# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:03:43 2020
@author: fcosta

Francisco Costa García
University of Stuttgart(c) 
"""

from Utils.Qlunc_ImportModules import *
import pdb

#%%# used to flatt at some points along the code:
flatten = lambda *n: (e for a in n for e in (flatten(*a) if isinstance(a, (list,tuple)) else (a,))) 

#%% sum dB:

def sum_dB(data,uncorrelated):
    """
    Add up dB's. Location: Qlunc_Help_standAlone.py
    
    Parameters
    ----------
    
    * SNR_data
        Signal to noise ratio
        
    * Bool
        Uncorrelated noise (default): True
        
    Returns
    -------
    
    Sum of dBW
    
    """
    Sum_decibels=[] 
    # Sum_in_watts=[]
    to_watts=[]
    if uncorrelated:
        for ind in range(len(data)):
            to_watts.append(10**(data[ind]/10))
        Sum_in_watts=sum(to_watts)
        Sum_decibels=10*np.log10(Sum_in_watts)         
    else:
        print('correlated noise use case is not included yet')
        # Sumat= []
        # Sum_decibels=[]
        # for ii in data:
        #     watts=10**(ii/10)   
        #     Sumat.append (watts)
        # Sum_in_watts = sum(Sumat)
        # Sum_decibels.append(10*np.log10(Sum_in_watts) )        
    return Sum_decibels

#%% Combine uncertainties:
# The uncertainty combination is made following GUM
def unc_comb(data): 
    """
    Add up dB's. Location: Qlunc_Help_standAlone.py
    
    Parameters
    ----------
    
    * data
        data is provided as a list of elements want to add on. Data is expected to be in dB (within this functions dB are transformed into watts).
        
    Returns
    -------
    
    list
    
    """
    data_watts  = []
    res_dB      = []
    res_watts   = []
    zipped_data = []
    if not isinstance (data,np.ndarray):
        data=np.array(data)    
    for data_row in range(np.shape(data)[0]):# transform into watts
        
        try:    
            data_db=data[data_row,:]
        except:
            data_db=data[data_row][0]
             
        data_watts.append(10**(data_db/10))
    for i in range(len(data_watts[0])): # combining all uncertainties making sum of squares and the sqrt of the sum
        zipped_data.append(list(zip(*data_watts))[i])
        res_watts.append(np.sqrt(sum(map (lambda x: x**2,zipped_data[i]))))
        res_dB=10*np.log10(res_watts) #Convert into dB 
    del data_db
    return np.array(res_dB)

#%% Spherical into cartesian  coordinate transformation
    #    xcart = rho * cos(phi)*sin(theta) 
    #    ycart = rho * sin(phi)*sin(theta)
    #    zcart = rho * cos(theta)
    
def sph2cart(Lidar): 
    x=[]
    y=[]
    z=[]
    
    for i in range(len(Lidar.optics.scanner.focus_dist)):
        x=Lidar.optics.scanner.focus_dist[i]*np.cos(np.deg2rad(Lidar.optics.scanner.phi))*np.sin(np.deg2rad(Lidar.optics.scanner.theta))
        y=Lidar.optics.scanner.focus_dist[i]*np.sin(np.deg2rad(Lidar.optics.scanner.phi))*np.sin(np.deg2rad(Lidar.optics.scanner.theta)) 
        z=Lidar.optics.scanner.focus_dist[i]*np.cos(np.deg2rad(Lidar.optics.scanner.theta)) 
    return(x,y,z)

   
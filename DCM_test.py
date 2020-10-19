#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:33:32 2020

@author: glatt
"""

from DCM.DCM import DCM
import numpy as np

DCM_test_results=[]
#Build an only-Basal resources ecosystem to test the Lotka-Volterra equation
Eco_system_test=DCM()
start_biomass=Eco_system_test.N[0]
#Run a simulation with 0 migration flux to observe the exponential growth of Basal resources
Eco_system_test.Evolve(20,0)

if (start_biomass<Eco_system_test.N[0]):
    DCM_test_results.append(True)
else:
    DCM_test_results.append(False)
    

#Run a simulation with both Resources and Migration flux and check if population grows
Eco_system_test=DCM()
Eco_system_test.Evolve(25,1)
if (len(Eco_system_test.Livings()[0])>1):
    DCM_test_results.append(True)
else:
    DCM_test_results.append(False)




DCM_test_results=np.array(DCM_test_results)
err_idx=DCM_test_results[DCM_test_results==False]
if(err_idx.size==0):
    print("Test succedeed!")
else:
    print("Test failed with these follow index:",err_idx)
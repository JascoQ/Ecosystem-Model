#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 20:33:32 2020

@author: glatt
"""



from DCM.DCM import DCM
import numpy as np
import pytest 



#Testing new_species function
def test_new_species():

    Eco_system_test=DCM()
    Eco_system_test.new_species()
    
    assert Eco_system_test.N.any(), "DCM.new_species() method failed"


############################################################################################
#Testing get_parameters()/set_parameters(arr) 
def test_get_set_params_DCM():
    
    Eco_system_test=DCM()
    assert Eco_system_test.get_params()==Eco_system_test.default_params, "DCM.get_params() method failed"
    test_params=range(1,9)
    Eco_system_test.set_params(test_params)
    
    assert (Eco_system_test.get_params()==np.array(test_params)).all(), "set_params() method failed"

############################################################################################
#Testing livings(pop) method
def test_livings():
    Eco_system_test=DCM()
    
    Eco_system_test.new_species()
    
    assert (Eco_system_test.livings()[0]==np.where(Eco_system_test.N!=0)[0]).all(), "DCM.livings() method failed"
    test_pop=Eco_system_test.N
    #Recreating an empty ecosystem
    Eco_system_test=DCM()
    assert (Eco_system_test.livings(pop=test_pop)[0]==np.where(test_pop!=0)[0]).all(),"DCM.livings(pop=test_pop) method failed"


############################################################################################
#testing animals() method
def test_animals():
    Eco_system_test=DCM()
    
    Eco_system_test.new_species()
    assert Eco_system_test.animals()==np.setdiff1d(Eco_system_test.livings(),0),"DCM.animals() method failed"
############################################################################################
#testing get_interaction() method
def test_get_interaction():
    
    Eco_system_test=DCM()
    Eco_system_test.new_species()
    species=Eco_system_test.livings()[0][1]
    
    new_species_preys=np.where(Eco_system_test.gamma[species]>0)
    new_species_predators=np.where(Eco_system_test.gamma[species]<0)
    
    #predators list is empty since there is only one predator in the ecosystem
    assert Eco_system_test.get_interaction(species)[0]==new_species_preys,"DCM.get_interaction() method failed"

############################################################################################
#testing extinction() method
def test_extinction():
    
    Eco_system_test=DCM()
    Eco_system_test.new_species()
    species=Eco_system_test.livings()[0][1]
    
    Eco_system_test.N[species]=Eco_system_test.N_c-1e-6   #associo all'unica specie vivente un energia minore del minimo N_c
    
    Eco_system_test.extinction()
    
    assert Eco_system_test.N[species]==0,"DCM.extinction() method failed to remove the extincted biomass"
    assert not (Eco_system_test.gamma[species]).any(),"DCM.extinction() method failed to remove interactions from gamma"


############################################################################################
#testing f() method
def test_f():
    
    Eco_system_test=DCM()
    starting_energy=np.copy(Eco_system_test.N[0])
    Eco_system_test.evolve(T=5,I=0,dt=1)
    assert starting_energy<Eco_system_test.N[0],"DCM.f() failed to provide the correct dN/dt to scipy.odeint"
    
    Eco_system_test.new_species()
    species=Eco_system_test.livings()[0][1]
    starting_energy=np.copy(Eco_system_test.N[species])
    #Added a new animal species and then let basal goes extincted, so that once the system evolves without migration flux, we expect the new species to goes extincted as well
    
    Eco_system_test.N[0]=Eco_system_test.N_c-1e-6
    Eco_system_test.extinction()
    Eco_system_test.evolve(T=20,I=0,dt=1)
    
    assert Eco_system_test.N[species]<starting_energy,"DCM.f() failed to provide the correct dN/dt to scipy.odeint"
    

############################################################################################
#testing migration() method
def test_migration():
    

    Eco_system_test=DCM()
    
    
    Eco_system_test.migration(I=5)
    
    assert len(Eco_system_test.livings()[0]==6),"DCM.migration(I) method failed"
    








"""    
#Build an only-Basal resources ecosystem to test the Lotka-Volterra equation
Eco_system_test=DCM()
start_biomass=Eco_system_test.N[0]
#Run a simulation with 0 migration flux to observe the exponential growth of Basal resources
Eco_system_test.Evolve(20,0)

if (start_biomass<Eco_system_test.N[0]):
    DCM_test_results.append(True)
else:
    DCM_test_results.append(False)

############################################################################################


#Run a simulation with both Resources and Migration flux and check if population grows
Eco_system_test=DCM()
Eco_system_test.Evolve(25,1)
if (len(Eco_system_test.Livings()[0])>1):
    DCM_test_results.append(True)
else:
    DCM_test_results.append(False)
############################################################################################


#Testing the extinction function inside an Evolve session
Eco_system_test=DCM()
Eco_system_test.New_species()
species=Eco_system_test.Livings()[0][1]
#Setting its energy to minimum
Eco_system_test.N[species]=0.5
Eco_system_test.Evolve(1,0)
if(Eco_system_test.N[species]==0):
    DCM_test_results.append(True)
else:
    DCM_test_results.append(False)
############################################################################################


#Print out test results 
DCM_test_results=np.array(DCM_test_results)
err_idx=DCM_test_results[DCM_test_results==False]
if(err_idx.size==0):
    print("Test succedeed!")
else:
    print("Test failed with these follow index:",err_idx)
    
"""
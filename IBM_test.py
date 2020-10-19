#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 18:54:04 2020

@author: glatt
"""

from IBM.IBM import IBM
import numpy as np

IBM_test_passed=[]

#A=Animal species, B=Basal species, -> = paired with

#err_idx=[0]
#A1 -> A2 ---- No interaction
Eco_system_test=IBM(100,"RM_test")
A1=Eco_system_test.Basals[-1]+1

predators_list=Eco_system_test.get_predators(A1)
preys_list=Eco_system_test.get_preys(A1)
basal_list=Eco_system_test.Basals

A1_interactions=np.append(predators_list,preys_list)
A1_interactions=np.append(A1_interactions,basal_list)
A1_no_interact=np.setdiff1d(Eco_system_test.all_species,A1_interactions)

A2=A1_no_interact[0]

Eco_system_test.Add_individual(Species=A1)
Eco_system_test.Add_individual(Species=A2)
starting_energy=Eco_system_test.Individuals[0][0]
Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)

A1_energy=Eco_system_test.Get_individual(0)[0]
A2_energy=Eco_system_test.Get_individual(1)[0]

if(A1_energy<starting_energy and A2_energy<starting_energy):
    IBM_test_passed.append(True)
###################################################################
#err_idx=[1]
#B1 -> B2 ----- no interaction
    
Eco_system_test=IBM(100,"RM_test")

Eco_system_test.Add_individual(Species=0)
Eco_system_test.Add_individual(Species=1)

Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)
B1_energy=Eco_system_test.Get_individual(0)[0]
B2_energy=Eco_system_test.Get_individual(1)[0]

if (B1_energy>starting_energy and B2_energy>starting_energy):
    IBM_test_passed.append(True)
else:
    IBM_test_passed.append(False)


###################################################################    
#err_idx=[2]
#A1 -> A2 ----- A1 predate A2
    
Eco_system_test=IBM(100,"RM_test")
A1=Eco_system_test.Basals[-1]+1

A1_preys=Eco_system_test.get_preys(A1)
A1_preys=np.setdiff1d(A1_preys,Eco_system_test.Basals)

A2=A1_preys[0]

Eco_system_test.Add_individual(Species=A1)
Eco_system_test.Add_individual(Species=A2)
starting_energy=Eco_system_test.Individuals[0][0]
Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)

A1_energy=Eco_system_test.Get_individual(0)[0]

if(Eco_system_test.N_deaths>0):
    IBM_test_passed.append(True)
else:
    IBM_test_passed.append(False)
###################################################################    
#err_idx=[3]
#A1->B1 ----- No interaction, Basals_energy>=E_rep
    
Eco_system_test=IBM(100,"RM_test")
A1=Eco_system_test.Basals[-1]+1
A1_preys=Eco_system_test.get_preys(A1)

A1_no_interact=np.setdiff1d(Eco_system_test.Basals,A1_preys)
B1=A1_no_interact[0]

Eco_system_test.Add_individual(Species=A1)
Eco_system_test.Add_individual(Species=B1,energy=200)

Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)

A1_energy=Eco_system_test.Get_individual(0)[0]

if (A1_energy<starting_energy and Eco_system_test.N_births==1):
    IBM_test_passed.append(True)
else:
    IBM_test_passed.append(False)
###################################################################    
#err_idx[4]
#A1->B1 ------- No interaction , Basal_energy>=E_rep but Basals_counts>=Area
    
Eco_system_test=IBM(area=1,method="RM_test")
A1=Eco_system_test.Basals[-1]+1
A1_preys=Eco_system_test.get_preys(A1)

A1_no_interact=np.setdiff1d(Eco_system_test.Basals,A1_preys)
B1=A1_no_interact[0]

Eco_system_test.Add_individual(Species=A1)
Eco_system_test.Add_individual(Species=B1,energy=200)
Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)

A1_energy=Eco_system_test.Get_individual(0)[0]

if (A1_energy<starting_energy and Eco_system_test.N_births==0):
    IBM_test_passed.append(True)
else:
    IBM_test_passed.append(False)
###################################################################    
#err_idx[5]
#A1->B1 ----- A1 predate B1
Eco_system_test=IBM(100,method="RM_test")
B1=1
B1_predators=Eco_system_test.get_predators(1)
A1=B1_predators[0][0]

Eco_system_test.Add_individual(Species=A1)
Eco_system_test.Add_individual(Species=B1,energy=150)
Eco_system_test.Evolve(Time=1,I=1,dt=2,verbose=False)

A1_energy=Eco_system_test.Get_individual(0)[0]

if(A1_energy>starting_energy and Eco_system_test.N_deaths>0):
    IBM_test_passed.append(True)
else:
    IBM_test_passed.append(False)
####################################################################
IBM_test_passed=np.array(IBM_test_passed)
err_idx=IBM_test_passed[IBM_test_passed==False]
if(err_idx.size==0):
    print("Test succedeed!")
else:
    print("Test failed with these follow index:",err_idx)












    
    

    







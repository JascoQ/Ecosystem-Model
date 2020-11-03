#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 18:54:04 2020

@author: glatt
"""

from IBM.IBM import IBM
import numpy as np
import pytest

Area=1000
RM_method="RM_test"
CM_method="CM_test"

def test_build_interactions():
    Eco_system_test=IBM(Area,RM_method)
    for rows in Eco_system_test.C[Eco_system_test.Basals[-1]+1:]:
        assert rows.any(),"Found a species with no interactions assigned: IBM.build_interaction() for RM method failed"
            
    Eco_system_test=IBM(Area,CM_method)
    for species in Eco_system_test.Predators:
        assert Eco_system_test.C[species].any()," Found a species with no interactions assigned: IBM.build_interaction() for CM method failed"
        
    
############################################################################################
#Testing get_parameters()/set_parameters(arr) 
        
def test_get_set_params_IBM():
    
    Eco_system_test=IBM(Area,RM_method)
    assert Eco_system_test.get_params()==Eco_system_test.default_par, "IBM.get_params() method failed"
    test_params=range(1,9)
    Eco_system_test.set_params(test_params)
    
    assert (Eco_system_test.get_params()==np.array(test_params)).all(), "set_params() method failed"

############################################################################################
#testing add_individual()
    
def test_add_individual():
    Eco_system_test=IBM(Area,RM_method)
    Eco_system_test.add_individual(Species=10,energy=100)
    
    assert Eco_system_test.species_alive().any()," IBM.add_individual() failed to add a new species to the ecosystem"
    assert Eco_system_test.Individuals[0][0] == 100, "IBM.add_individual() failed to give starting energy to new species"
    
    
def test_deaths():
    Eco_system_test=IBM(Area,RM_method)
    Eco_system_test.add_individual()
    
    
    Eco_system_test.Individuals[0][0]=0
    Eco_system_test.deaths()
    assert Eco_system_test.Individuals.size==0,"IBM.deaths() failed to remove 0 energy individuals"
    

############################################################################################
#Testing basals_counts()
    
def test_basals_counts():
    methods=[RM_method,CM_method]
    
    for method in methods:
        Eco_system_test=IBM(Area,method)
        spec1=Eco_system_test.Basals[1]
        spec2=Eco_system_test.Basals[2]
        
        Eco_system_test.add_individual(Species=spec1)
        Eco_system_test.add_individual(Species=spec2)
        
        assert Eco_system_test.basals_counts()==2,"IBM.basals_count failed to returns the correct number of living basals"
     
############################################################################################
#Testing births()  
        
def test_births():
    Eco_system_test=IBM(Area,RM_method)
    #testing for predator species
    spec=Eco_system_test.Predators[0]
    Eco_system_test.add_individual(Species=spec)
    Eco_system_test.Individuals[0][0]=Eco_system_test.E_rep+1e-1
    
    Eco_system_test.births()
    
    assert Eco_system_test.Individuals[:,1].size==2, " IBM.births() failed to add new individual from species with Energy>E_rep"
    assert Eco_system_test.species_alive().size==1, "IBM.births() failed to add a new individual belonging to the parent's same species"
    
    #testing for basals species (Area limitation)
    Area_test=1
    Eco_system_test=IBM(Area_test,RM_method)
    spec=Eco_system_test.Basals[1]
    Eco_system_test.add_individual(Species=spec,energy=Eco_system_test.E_rep+1e-1)
    
    Eco_system_test.births()
    #aborting birth due the full capacity of the ecosystem
    assert Eco_system_test.Individuals[:,1].size==1,"IBM.births() failed to abort births, when ecosystem Area is satured."

############################################################################################
#testing create_pairs()
    
def test_create_pairs():
    Eco_system_test=IBM(Area,RM_method)
    #adding 7 individuals
    for new_species in range(0,7):
        Eco_system_test.add_individual()
        
    pairs=Eco_system_test.create_pairs()
    
    assert np.shape(pairs)==(3,2),"IBM.create_pairs() failed"
    #check if any pair has duplicate item 
    for pair in pairs:
        assert len(set(list(pair)))==len(pair),"IBM.create_pairs() failed to create pairs of distinct individuals"
        
############################################################################################
#testing get_individual(ID)
        
def test_get_individual():
    Eco_system_test=IBM(Area,RM_method)
    Eco_system_test.add_individual(Species=Eco_system_test.Predators[1],energy=50)
    new_species_ID=Eco_system_test.Individuals[0][2]
    
    assert (Eco_system_test.get_individual(ID=new_species_ID)==Eco_system_test.Individuals[0]).all(),"IBM.get_individual(ID) failed to returns info array about specified individual"
    
    species_alive=Eco_system_test.species_alive()[0][0]
    
    not_living_species=species_alive+1
    #test if when get_individual is feed with not existing species, return False
    assert not Eco_system_test.get_individual(ID=not_living_species),"IBM.get_individual() failed to return False in not-existing species case"
    
############################################################################################
#testing all the interaction dynamics cases
    
#A=Animal species, B=Basal species, -> = paired with      
def test_interaction_dynamics():
        
#A1 -> A2 ---- No interaction
    
    Eco_system_test=IBM(Area,RM_method)
    A1=Eco_system_test.Basals[-1]+1
    
    predators_list=Eco_system_test.get_predators(A1)
    preys_list=Eco_system_test.get_preys(A1)
    basal_list=Eco_system_test.Basals
    
    A1_interactions=np.append(predators_list,preys_list)
    A1_interactions=np.append(A1_interactions,basal_list)
    A1_no_interact=np.setdiff1d(Eco_system_test.all_species,A1_interactions)
    
    A2=A1_no_interact[0]
    
    Eco_system_test.add_individual(Species=A1)
    Eco_system_test.add_individual(Species=A2)
    starting_energy=Eco_system_test.Individuals[0][0]
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    
    A1_energy=Eco_system_test.get_individual(0)[0]
    A2_energy=Eco_system_test.get_individual(1)[0]
    
    assert (A1_energy<starting_energy and A2_energy<starting_energy),"IBM.interaction_dynamics fail with A-A no interaction dynamics"

###################################################################
#B1 -> B2 ----- no interaction
    
    Eco_system_test=IBM(Area,RM_method)
    
    Eco_system_test.add_individual(Species=0)
    Eco_system_test.add_individual(Species=1)
    
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    B1_energy=Eco_system_test.get_individual(0)[0]
    B2_energy=Eco_system_test.get_individual(1)[0]
    
    assert (B1_energy>starting_energy and B2_energy>starting_energy),"IBM.interaction_dynamics fail with B-B no interact dynamics"
    
###################################################################    
#A1 -> A2 ----- A1 predate A2
    
    Eco_system_test=IBM(Area,RM_method)
    A1=Eco_system_test.Basals[-1]+1
    
    A1_preys=Eco_system_test.get_preys(A1)
    A1_preys=np.setdiff1d(A1_preys,Eco_system_test.Basals)
    
    A2=A1_preys[0]
    
    Eco_system_test.add_individual(Species=A1)
    Eco_system_test.add_individual(Species=A2)
    starting_energy=Eco_system_test.Individuals[0][0]
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    
    A1_energy=Eco_system_test.get_individual(0)[0]
    
    assert (Eco_system_test.N_deaths>0),"IBM.interaction_dynamics failed with A_pred-A_prey interact dynamics"

###################################################################    
#A1->B1 ----- No interaction, Basals_energy>=E_rep
    
    Eco_system_test=IBM(Area,RM_method)
    A1=Eco_system_test.Basals[-1]+1
    A1_preys=Eco_system_test.get_preys(A1)
    
    A1_no_interact=np.setdiff1d(Eco_system_test.Basals,A1_preys)
    B1=A1_no_interact[0]
    
    Eco_system_test.add_individual(Species=A1)
    Eco_system_test.add_individual(Species=B1,energy=200)
    
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    
    A1_energy=Eco_system_test.get_individual(0)[0]
    
    assert (A1_energy<starting_energy and Eco_system_test.N_births==1),"IBM.interaction_dynamics faild with A-B no interaction dynamics"
    
    
###################################################################    
#A1->B1 ------- No interaction , Basal_energy>=E_rep but Basals_counts>=Area
    
    Eco_system_test=IBM(area=1,method=RM_method)
    A1=Eco_system_test.Basals[-1]+1
    A1_preys=Eco_system_test.get_preys(A1)
    
    A1_no_interact=np.setdiff1d(Eco_system_test.Basals,A1_preys)
    B1=A1_no_interact[0]
    
    Eco_system_test.add_individual(Species=A1)
    Eco_system_test.add_individual(Species=B1,energy=200)
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    
    A1_energy=Eco_system_test.get_individual(0)[0]
    
    assert (A1_energy<starting_energy and Eco_system_test.N_births==0),"IBM.interaction_dynamics failed with A-B No interact, Basal_energy>=E_rep but Basals_counts>=Area"

###################################################################    
#A1->B1 ----- A1 predate B1
    
    Eco_system_test=IBM(Area,RM_method)
    B1=1
    B1_predators=Eco_system_test.get_predators(1)
    A1=B1_predators[0][0]
    
    Eco_system_test.add_individual(Species=A1)
    Eco_system_test.add_individual(Species=B1,energy=150)
    Eco_system_test.evolve(Time=1,I=1,dt=2,verbose=False)
    
    A1_energy=Eco_system_test.get_individual(0)[0]
    
    assert (A1_energy>starting_energy and Eco_system_test.N_deaths>0),"IBM.interaction_dynamics failed with A_pred-B_prey dynamic"

        
    











    
    

    







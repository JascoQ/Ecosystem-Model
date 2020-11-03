#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 16:06:27 2020

@author: glatt
"""

import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx

#COSTANTS
max_E=200           #Max value for interactions matrix
l=8                 #Average preys for predator
b=5                 #Energy gain for basal 
d=2.5               #Energy dissipation for timestep
delta=20            #Energy for new born
P_death=0.002       #Death chance for timestep
E_rep=200           #Energy needed for reproducing

class IBM:
    
    def __init__(self,area,method):
        
        self.Area=area
        self.method=method
        self.max_E=200
        self.l=8
        self.b=5
        self.d=2.5
        self.delta=20
        self.P_death=0.002
        self.E_rep=200
        
        
        self.default_par=[self.Area,E_rep,P_death,max_E,delta,l,d,b]
        
        if(method=="RM"):
            animal_species=Animal_species
            basal_species=Basal_species
            #inizializzo un array con le specie dei predatori a partire dalle specie animali
            self.Predators=list(range(basal_species,basal_species+animal_species))
        
            #inizializzo allo stesso modo una lista di tutte le specie possibili prede
            self.all_species=list(range(animal_species+basal_species))
            self.Basals=np.setdiff1d(self.all_species,self.Predators)
            self.C=np.zeros((basal_species+animal_species,basal_species+animal_species))
            
            self.build_interactions()
        
        if(method=="CM"):
            num_species=int(input("Input how many overall species : "))
            self.all_species=list(range(num_species))
            self.C=np.zeros((num_species,num_species))
            self.build_interactions()
            
        #add two methods to allows default TEST models without console interaction
        if(method=="RM_test"):
            animal_species=50
            basal_species=5
            
            self.Predators=list(range(basal_species,basal_species+animal_species))
            self.all_species=list(range(animal_species+basal_species))
            self.Basals=np.setdiff1d(self.all_species,self.Predators)
            self.C=np.zeros((basal_species+animal_species,basal_species+animal_species))
            
            self.method="RM"
            self.build_interactions()
            
        if(method=="CM_test"):
            num_species=50
            self.all_species=list(range(num_species))
            self.C=np.zeros((num_species,num_species))
            self.method="CM"
            self.build_interactions()
        
        allowed_methods=["RM","CM","RM_test","CM_test"]
        if (method not in allowed_methods):
            print("Wrong input for method arg. Allowed inputs are strings:",allowed_methods)
            
            
            
        #creo dataframe vuoto in cui ogni riga conterrò
        #l'energia e la specie dell'i-esimo individuo
        #Individuals[individual_energy][species][ID]
        self.Individuals=np.empty((0,3))
        
        self.last_ID=0
        #creo dataframe contenente le info sull'evoluzione del sistema in funz. del tempo
        self.Population_t=np.empty((0,3),dtype=int)
        self.N_deaths=0
        self.N_births=0
        self.G=nx.DiGraph()
        
    #allowed method : "RM" and "CM"
    def build_interactions(self):
        '''It builds an interaction matrix for all the species, depending on which methods has been chosen'''
        if (self.method=="RM"):
            
            for pred in self.Predators:
                #Inizialmente tutte le specie diverse da pred sono potenziali prede
                preys=np.setdiff1d(self.all_species,pred)
            
                
                #RIMUOVO DALLE POSSIBILI PREYS DI PREDATORE GLI ANIMALI DI CUI LUI È PREDA
                preys=np.setdiff1d(preys,self.get_predators(pred))
                        
                #controllo se il num. max di prede l è minore delle prede disponibili
                if (len(preys)>=self.l):
                    
                    #estraggo l prede casualmente e inizializzo i coefficienti di interazione predatore-preda     
                    for idx in random.sample(list(preys),k=self.l):
                        self.C[pred][idx]=np.random.uniform(0,self.max_E)
                        
                else:
                    #ridefinisco il max numero di prede
                    max_n=len(preys)
                    for idx in random.sample(list(preys),max_n):
                        self.C[pred][idx]=np.random.uniform(0,self.max_E)
                    
        elif(self.method=="CM"):
            #defining prey probability as costant/num. of species
            prob=self.l/len(self.all_species)
            
            for predator in self.all_species:
                
                #randomly choosing the number of preys
                chances=np.random.uniform(0,1,size=len(self.all_species[:predator]))
                n_preys=len(chances[chances<prob])
                
                #choosing only preys of species below the predator one
                preys=np.random.choice(self.all_species[:predator],size=n_preys,replace=False)
                
                for prey in preys:
                    self.C[predator][prey]=np.random.uniform(0,self.max_E)
            #Categorizza le basals species e le animals affinchè il resto del codice sia coerente
            self.Basals=[]
            i=0
            
            for row in self.C:
                
                if (row.any()==0):
                    self.Basals=np.append(self.Basals,i)
                i+=1
            self.Predators=np.setdiff1d(self.all_species,self.Basals)

            
    def get_params(self):
        '''It prints and return all the ecosystem parameters'''
        
        print("Area=",self.Area,",Method:",self.method)
        print("E_rep=",self.E_rep,",Death probability=",self.P_death,",Max E=",self.max_E,",delta=",self.delta)
        print("l=",self.l,",dissipation=",self.d,",basals growth=",self.b)
        return [self.Area,self.E_rep,self.P_death,self.max_E,self.delta,self.l,self.d,self.b]
    
    def set_params(self,par_arr):
        '''The given argument array modifies all the ecosystem parameters in this order: Area, E_rep, P_death, max_E, delta, l, d, b'''
        
        self.Area=par_arr[0]
        self.E_rep=par_arr[1]
        self.P_death=par_arr[2]
        self.max_E=par_arr[3]
        self.delta=par_arr[4]
        self.l=par_arr[5]
        self.d=par_arr[6]
        self.b=par_arr[7]
        print("Parameters has been succesfully changed")
        print("New parameters are:")
        self.get_params()
        
    
    def set_default(self):
        '''sets ecosystem parameters with prefixed default values'''
        
        self.set_params(self.default_par)
        
    def basals_counts(self):
        '''Returns the number of living Basals individuals'''
        #Esegui solo se vi è almeno una specie animale
        if(len(self.Basals)!=len(self.all_species)):
            if (self.method=="CM"):
                count=0
                for species in self.Individuals[:,1]:
                    if (species in self.Basals):
                        count+=1
            elif(self.method=="RM"):
                count=np.shape(np.where(self.Individuals[:,1]<self.Predators[0]))[1]
        else:
            count=len(self.Individuals)
        return count
    


    def species_alive(self):
        '''Return an array filled with all the unique species ID living in the ecosystem'''
        return np.unique(self.Individuals[:,1])
    
    def current_situation(self):
        '''It prints out all the information about the evolution and the current status of the ecosystem'''
        
        print("Population number :",len(self.Individuals))
        print("Different species alive :",len(self.species_alive()))
        if (len(self.Population_t)>0):
            print("Animals/Basals number= ",self.Population_t[-1][0],"/",self.Population_t[-1][1])
        else:
            print("Ecosystem at time=0 is empty; first call Evolve function")
        print("Number of births: ",self.N_births)
        print("Number of deaths: ",self.N_deaths)
        print("Time passed: ",len(self.Population_t))
        
    def add_individual(self,Species=-1,energy=b):
        '''If arg Species=-1, then the species added to the ecosystem is randomly extracted from the pool of allowed species. If Species = some_species_ID, then it adds an individual belonging to that species with the desired energy'''
        
        if (energy==b):
            energy=self.b 
        if(Species==-1):
            Species=np.random.choice(self.all_species,1)
            self.Individuals=np.append(self.Individuals,[[energy,Species,self.last_ID]],axis=0)
            self.last_ID+=1
        elif( (np.shape(Species)==()) or (Species in self.all_species) or np.shape(Species)==(1,)):
            Species=np.reshape(np.array([Species]),(1,))
            self.Individuals=np.append(self.Individuals,[[energy,Species,self.last_ID]],axis=0)
            self.last_ID+=1
        else:
            print("Input args error: insert a valid species number")

            
        
            
    def get_predators(self,species):
        '''It returns an array filled with all the predators of a certain species'''
        return np.where(self.C[:,species]!=0)
    def get_preys(self,species):
        '''It returns an array filled with all the preys of a certain species'''

        return np.where(self.C[species]!=0)
        
    def deaths(self):
        '''It computes a random die chance for each living individual, then check if any individuals has energy below a certain threshold and if yes, set that individual as died'''
        
        #estraggo un numero per ogni specie
        chances=np.random.uniform(0,1,size=len(self.Individuals))
        n_deaths=len(chances[chances<=self.P_death])
        daily_deaths=n_deaths+len(self.Individuals[self.Individuals[:,0]<=0])
        self.N_deaths+=daily_deaths
        death_ID=np.random.choice(self.Individuals[:,2],n_deaths)
        #per ognuno degli ID estratti pongo la loro energia a 0 (morte)
        for ID in death_ID:
            idx=int(np.reshape(np.where(self.Individuals[:,2]==ID),()))
            self.Individuals[idx][0]=0
        
        #Tutti gli individui con energia<=0 muoiono
        self.Individuals=self.Individuals[self.Individuals[:,0]>0]
        return daily_deaths
        
        
    
    def births(self):
        '''It checks if any individual has an energy above a certain reproduction threshold and when yes, it adds to the ecosystem as many new individual as the pregnant individuals'''
        pregnant_index=np.where(self.Individuals[:,0]>self.E_rep)
        pregnant_index=np.reshape(pregnant_index,(len(pregnant_index[0]),))
        
        aborts=0
        #daily_space finchè è >0 garantisce che ci sia spazio available for basals reproduction
        #daily_space=self.Area-self.basals_counts()
        
        for i in pregnant_index:
            
            #if (self.Individuals[i][1] in self.Basals and not daily_space):
            if (self.Individuals[i][1] in self.Basals and self.basals_counts()>=self.Area):
                aborts+=1
                
            else:
                #print("Species",self.Individuals[i][1],"is reproducing!")
                self.Individuals[i][0]-=self.delta
                self.add_individual(Species=self.Individuals[i][1],energy=self.delta)
                #if (self.Individuals[i][1] in self.Basals):
                    #daily_space-=1
                
                
        self.N_births+=len(pregnant_index)-aborts

        return (len(pregnant_index)-aborts)
            
    def plot_pop(self,Animals=True,Basals=True,Species=True,Area=False):
        '''Plots the counts of Individuals through time. Arguments can be changed in order to show more curves to the plot.'''
        
        plt.xlabel("Time")
        plt.ylabel("Counts")
        
        if (Animals):
            plt.plot(range(len(self.Population_t)),self.Population_t[:,0],label="Animals",alpha=0.7)
        if (Basals):
            plt.plot(range(len(self.Population_t)),self.Population_t[:,1],label="Basals",alpha=0.7)
            if(Area):
                plt.axhline(y=self.Area,label="Area",linestyle='--')
        if (Species):
            plt.plot(range(len(self.Population_t)),self.Population_t[:,2],label="Species",alpha=0.3)
            
        plt.legend()
        return plt.show()  
    
    def food_web(self,draw=False):
        '''It prints, when draw=True, a graphic visualization of the food web related to the ecosystem interactions. Also it prints a set of network measurements about the food web.'''
        
        
        self.G=nx.from_numpy_matrix(self.C,create_using=nx.DiGraph)
        if (draw):
        #The out_degree value for a species represent its number of preys
            d = dict(self.G.out_degree)
            low, *_, high = sorted(d.values())
            norm = mpl.colors.Normalize(vmin=low, vmax=high, clip=True)
            mapper = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.coolwarm)
            nx.draw_shell(self.G, 
                      nodelist=d,
            node_size=500,
            node_color=[mapper.to_rgba(i) 
                        for i in d.values()], 
            with_labels=True,
            font_color='white')
            plt.show()
        
        out_degree=self.G.out_degree
        in_degree=self.G.in_degree
        n_predators=len(self.Predators)
        print("Average predators for species:",np.average(in_degree,0)[1])
        print("Average preys for predator :",(np.sum(out_degree,0)[1])/n_predators)
        print("Number of edges in the foodweb: ", nx.number_of_edges(self.G))
                

        
    
    def individuals_per_species(self):
        '''It plots and returns an array filled with the individual counts per each species'''
        
        counts=[]
        for spec in self.Individuals[:,1]:
            counts=np.append(counts,spec[0])
            
        #plt.plot(species,counts)
        plt.hist(counts,bins=len(self.all_species),alpha=0.6)
        
        if(self.method=="RM"):
            plt.axvline(x=self.Basals[-1],linestyle='--',label="Basals|Animals",color='r')
            
        plt.legend()
        plt.xlabel("Species")
        plt.ylabel("Counts")
        return counts
        


    def create_pairs(self):
        '''Randomly pairs each living individual with another. If number of individuals is odd, then one individual is left unpaired'''
        
        individuals_index=np.copy(self.Individuals[:,2])
        individuals_index=np.random.choice(individuals_index,len(individuals_index),replace=False)
        
        if(len(individuals_index)%2!=0):
            individuals_index=individuals_index[:-1]
                    
        return individuals_index.reshape(len(individuals_index)//2,2)
    
    def get_individual(self,ID):
        '''Returns the info array (Energy, Species, ID)) about a specified individual.'''
                
        if (ID not in self.Individuals[:,2]):
            print("ID specified does not exist")
            return False
        elif(ID==0):
            return self.Individuals[0]
        else:
            idx=int(np.reshape(np.where(self.Individuals[:,2]==ID),()))
            return self.Individuals[idx]
    
    def interaction_dynamics(self,spec_1,spec_2,is_there_space=True):
        '''It computes the interaction dynamics between two individuals given as args.'''
        
        #CASES:
                    
        #Sono entrambi vegetali e vi è abbastanza spazio, entrambi sopravvivono con un energy gain
        if((spec_1[1] in self.Basals) and is_there_space):
            spec_1[0]+=b
        if((spec_2[1] in self.Basals) and is_there_space):
            spec_2[0]+=b
            
        #Specie1 è predatore di Specie2
        if(self.C[int(spec_1[1])][int(spec_2[1])]!=0 and self.C[int(spec_2[1])][int(spec_1[1])]==0):
            #CONTROLLO AFFINCHÈ NESSUN E(i)>E_rep+E
            if(spec_2[0]/self.E_rep>=1):
                spec_1[0]+=self.C[int(spec_1[1])][int(spec_2[1])]-self.d
            else:
                spec_1[0]+=(self.C[int(spec_1[1])][int(spec_2[1])]*spec_2[0]/self.E_rep)-self.d

            spec_2[0]=0
                        
        #Specie2 è predatore di Specie1
        if(self.C[int(spec_2[1])][int(spec_1[1])]!=0 and self.C[int(spec_1[1])][int(spec_2[1])]==0):
            #CONTROLLO AFFINCHÈ NESSUN E(i)>E_rep+E
            if(spec_1[0]/E_rep<1):
                spec_2[0]+=(self.C[int(spec_2[1])][int(spec_1[1])]*spec_1[0]/self.E_rep)-self.d
            else:
                spec_2[0]+=self.C[int(spec_2[1])][int(spec_1[1])]-self.d
            spec_1[0]=0
            
        #Nel caso nessuna delle condizioni precedenti sia soddisfatta
        #la coppia è formata da animali che non si predano che dissipano energia
        else:
            spec_1[0]-=self.d
            spec_2[0]-=self.d
        
          
    #Time : tempo di evoluzione del sistema
    #I : specie che migrano nell'isola randomicamente ogni dt
    #Es: I=2, dt=1 --> ogni step arrivano 2 specie
    #Es2: I=1, dt=3 --> ogni 3 step arriva 1 specie
    #verbose : mostra in tempo reale l'evoluzione del sistema
    def evolve(self,Time,I,dt=1,verbose="days",show_results=False):
        '''It evolves the system for a fixed number of timesteps (Time). Argument I represent the migration flux for dt.
            Example: I=2, dt=1 --> each time step, two random individuals arrives to the ecosystem
            Example 2: I=1, dt=3 --> each 3 time steps, 1 random individual arrives to the ecosystem
            Argument verbose is set 'days' as default, so it will print the timesteps count.
            When verbose='full' or True, then it will prints all the information about the ecosystem for each timestep.'''
            
            
        t_step=0
        
        if(len(self.Individuals)==0):
            #first born in the island
            self.add_individual(energy=self.delta)
            
        for t in range(Time):
            t_step+=1
            #FLUSSO MIGRAZIONE 
            if(t_step==dt):
                for migrants in range(I):
                    self.add_individual(Species=-1,energy=self.delta)
                t_step=0

            #estraggo len(Individuals)//2 coppie di individui
            if(len(self.Individuals)>1):
                
                is_there_space=self.basals_counts()<self.Area
                pairs=self.create_pairs()
                for p in pairs:
                    spec_1=self.get_individual(p[0])
                    spec_2=self.get_individual(p[1])
                    
                    #Controlla tutte le possibili dinamiche preda predatore
                    #e aggiorna lo stato delle due specie accoppiate
                    self.interaction_dynamics(spec_1,spec_2,is_there_space) 
                      
            #La funzione deaths() rimuove gli individui con energia nulla
            #ed estrae randomicamente una percentuale di individui che muoiono
            daily_deaths=self.deaths()

            #births() si occupa di computare nuove nascite in caso di individui
            #con energia>E_rep
            daily_births=self.births()

            N_species=len(self.species_alive())
            daily_basals=self.basals_counts()
            self.Population_t=np.append(self.Population_t,[[len(self.Individuals)-daily_basals,daily_basals,N_species]],axis=0)

            if(verbose=="full" or verbose==True):
                print("-------- Day = ",t,"-------------")
                print("Daily Births = ",daily_births)
                print("Daily Deaths = ",daily_deaths)
                print("Animals/Basals number= ",self.Population_t[-1][0],"/",self.Population_t[-1][1])
                print("There are ",N_species," different species alive")
            elif(verbose=="days"):
                print("\rDay = ",t,"", end= '',flush=True)
        if(show_results):
            self.plot_pop()
                
                
            
            
class RM_IBM (IBM):
    
    def __init__(self,Area,Animal_species,Basal_species):
        self.method="RM"
                
        self.Area=Area
        self.max_E=200
        self.l=8
        self.b=5
        self.d=2.5
        self.delta=20
        self.P_death=0.002
        self.E_rep=200
        
        self.default_par=[self.Area,max_E,l,b,d,delta,P_death,E_rep]

        animal_species=Animal_species
        basal_species=Basal_species
        #inizializzo un array con le specie dei predatori a partire dalle specie animali
        self.Predators=list(range(basal_species,basal_species+animal_species))
        #inizializzo allo stesso modo una lista di tutte le specie possibili prede
        self.all_species=list(range(animal_species+basal_species))
        self.Basals=np.setdiff1d(self.all_species,self.Predators)
        self.C=np.zeros((basal_species+animal_species,basal_species+animal_species))
            
            
        self.build_interactions()
        
        #creo dataframe vuoto in cui ogni riga conterrò
        #l'energia e la specie dell'i-esimo individuo
        #Individuals[individual_energy][species][ID]
        self.Individuals=np.empty((0,3))
        
        self.last_ID=0
        #creo dataframe contenente le info sull'evoluzione del sistema in funz. del tempo
        self.Population_t=np.empty((0,3),dtype=int)
        self.N_deaths=0
        self.N_births=0
        self.G=nx.DiGraph()
        
        
class CM_IBM(IBM):
    
    def __init__(self,Area,overall_species):
        self.method="CM"
                
        self.Area=Area
        self.max_E=200
        self.l=8
        self.b=5
        self.d=2.5
        self.delta=20
        self.P_death=0.002
        self.E_rep=200
        
        self.default_par=[self.Area,max_E,l,b,d,delta,P_death,E_rep]
        
        num_species=overall_species
        self.all_species=list(range(num_species))
        self.C=np.zeros((num_species,num_species))
        self.build_interactions()
        
        #creo dataframe vuoto in cui ogni riga conterrò
        #l'energia e la specie dell'i-esimo individuo
        #Individuals[individual_energy][species][ID]
        self.Individuals=np.empty((0,3))
        
        self.last_ID=0
        #creo dataframe contenente le info sull'evoluzione del sistema in funz. del tempo
        self.Population_t=np.empty((0,3),dtype=int)
        self.N_deaths=0
        self.N_births=0
        self.G=nx.DiGraph()
        
        
    
    
        
        
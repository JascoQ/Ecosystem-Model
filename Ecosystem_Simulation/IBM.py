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
E=200               #Max value for interactions matrix
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
        if(method=="RM"):
            animal_species=int(input("Input how many animal species : "))
            basal_species=int(input("Input how many basal species : "))
            #inizializzo iun array con le specie dei predatori a partire dalle specie animali
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
        if (self.method=="RM"):
            
            for pred in self.Predators:
                #Inizialmente tutte le specie diverse da pred sono potenziali prede
                preys=np.setdiff1d(self.all_species,pred)
            
                
                #RIMUOVO DALLE POSSIBILI PREYS DI PREDATORE GLI ANIMALI DI CUI LUI È PREDA
                preys=np.setdiff1d(preys,self.get_predators(pred))
                        
                #controllo se il num. max di prede l è minore delle prede disponibili
                if (len(preys)>=l):
                    
                    #estraggo l prede casualmente e inizializzo i coefficienti di interazione predatore-preda     
                    for idx in random.sample(list(preys),k=l):
                        self.C[pred][idx]=np.random.uniform(0,E)
                        
                else:
                    #ridefinisco il max numero di prede
                    max_n=len(preys)
                    for idx in random.sample(list(preys),max_n):
                        self.C[pred][idx]=np.random.uniform(0,E)
                    
        elif(self.method=="CM"):
            #defining prey probability as costant/num. of species
            prob=l/len(self.all_species)
            
            for predator in self.all_species:
                
                #randomly choosing the number of preys
                chances=np.random.uniform(0,1,size=len(self.all_species[:predator]))
                n_preys=len(chances[chances<prob])
                
                #choosing only preys of species below the predator one
                preys=np.random.choice(self.all_species[:predator],size=n_preys,replace=False)
                
                for prey in preys:
                    self.C[predator][prey]=np.random.uniform(0,E)
            #Categorizza le basals species e le animals affinchè il resto del codice sia coerente
            self.Basals=[]
            i=0
            
            for row in self.C:
                
                if (row.any()==0):
                    self.Basals=np.append(self.Basals,i)
                i+=1
            self.Predators=np.setdiff1d(self.all_species,self.Basals)
        else:
            print("Wrong input for method arg. Allowed inputs are strings: RM and CM")
            
    def get_params(self):
        print("Area=",self.Area,",Method:",self.method)
        print("E_rep=",E_rep,",Death probability=",P_death,",Max E=",E,",delta=",delta)
        print("l=",l,",dissipation=",d,",basals growth=",b)
    
    def Basals_counts(self):
        if (self.method=="CM"):
            count=0
            for species in self.Individuals[:,1]:
                if (species in self.Basals):
                    count+=1
        elif(self.method=="RM"):
            count=np.shape(np.where(self.Individuals[:,1]<self.Predators[0]))[1]
        return count
    
    
    def species_alive(self):
        return np.unique(self.Individuals[:,1])
    
    def current_situation(self):
        print("Population number :",len(self.Individuals))
        print("Different species alive :",len(self.species_alive()))
        print("Animals/Basals number= ",self.Population_t[-1][0],"/",self.Population_t[-1][1])
        print("Number of births: ",self.N_births)
        print("Number of deaths: ",self.N_deaths)
        print("Time passed: ",len(self.Population_t))
        
    def Add_individual(self,Species=False,energy=b):
        if (Species):
            self.Individuals=np.append(self.Individuals,[[energy,Species,self.last_ID]],axis=0)
            
        else:
            Species=np.random.choice(self.all_species,1)
            self.Individuals=np.append(self.Individuals,[[energy,Species,self.last_ID]],axis=0)
        self.last_ID+=1
            
    def get_predators(self,species):
        return np.where(self.C[:,species]!=0)
    def get_preys(self,species):
        return np.where(self.C[species]!=0)
        
    def Deaths(self):
        #estraggo un numero per ogni specie
        chances=np.random.uniform(0,1,size=len(self.Individuals))
        n_deaths=len(chances[chances<=P_death])
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
        
        
    
    def Births(self):
        pregnant_index=np.where(self.Individuals[:,0]>E_rep)
        pregnant_index=np.reshape(pregnant_index,(len(pregnant_index[0]),))
        
        aborts=0
        #daily_space finchè è >0 garantisce che ci sia spazio available for basals reproduction
        #daily_space=self.Area-self.Basals_counts()
        
        for i in pregnant_index:
            
            #if (self.Individuals[i][1] in self.Basals and not daily_space):
            if (self.Individuals[i][1] in self.Basals and self.Basals_counts()>=self.Area):
                aborts+=1
                
            else:
                #print("Species",self.Individuals[i][1],"is reproducing!")
                self.Individuals[i][0]-=delta
                self.Add_individual(Species=self.Individuals[i][1],energy=delta)
                #if (self.Individuals[i][1] in self.Basals):
                    #daily_space-=1
                
                
        self.N_births+=len(pregnant_index)-aborts

        return (len(pregnant_index)-aborts)
            
    def plot_pop(self,Animals=True,Basals=True,Species=True,Area=False):
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
    
    def food_web(self):
        self.G=nx.from_numpy_matrix(self.C,create_using=nx.DiGraph)
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
        return plt.show()

        
    
    def Individuals_per_species(self):
        species=self.species_alive()
        counts=[]
        for s in species:
            counts=np.append(counts,len(self.Individuals[self.Individuals[:,1]==s]))
            
        #plt.plot(species,counts)
        plt.hist(self.Individuals[:,1])
        if(self.method=="RM"):
            plt.axvline(x=self.Basals[-1],linestyle='--',label="Basals|Animals")
        plt.xlabel("Species")
        plt.ylabel("Counts")
        #returna la lista che plotti pure già che stai zì
        #return counts
        


    def Create_Pairs(self):
        individuals_index=np.copy(self.Individuals[:,2])
        individuals_index=np.random.choice(individuals_index,len(individuals_index),replace=False)
        
        if(len(individuals_index)%2!=0):
            individuals_index=individuals_index[:-1]
                    
        return individuals_index.reshape(len(individuals_index)//2,2)
    
    def Get_individual(self,ID):
        idx=int(np.reshape(np.where(self.Individuals[:,2]==ID),()))
        return self.Individuals[idx]
    
    def Interaction_dynamics(self,spec_1,spec_2,is_there_space=True):
        
        #CASES:
                    
        #Sono entrambi vegetali e vi è abbastanza spazio, entrambi sopravvivono con un energy gain
        if((spec_1[1] in self.Basals) and is_there_space):
            spec_1[0]+=b
        if((spec_2[1] in self.Basals) and is_there_space):
            spec_2[0]+=b
            
        #Specie1 è predatore di Specie2
        if(self.C[int(spec_1[1])][int(spec_2[1])]!=0 and self.C[int(spec_2[1])][int(spec_1[1])]==0):
            #CONTROLLO AFFINCHÈ NESSUN E(i)>E_rep+E
            if(spec_2[0]/E_rep>=1):
                spec_1[0]+=self.C[int(spec_1[1])][int(spec_2[1])]-d
            else:
                spec_1[0]+=(self.C[int(spec_1[1])][int(spec_2[1])]*spec_2[0]/E_rep)-d

            spec_2[0]=0
                        
        #Specie2 è predatore di Specie1
        if(self.C[int(spec_2[1])][int(spec_1[1])]!=0 and self.C[int(spec_1[1])][int(spec_2[1])]==0):
            #CONTROLLO AFFINCHÈ NESSUN E(i)>E_rep+E
            if(spec_1[0]/E_rep<1):
                spec_2[0]+=(self.C[int(spec_2[1])][int(spec_1[1])]*spec_1[0]/E_rep)-d
            else:
                spec_2[0]+=self.C[int(spec_2[1])][int(spec_1[1])]-d
            spec_1[0]=0
            
        #Nel caso nessuna delle condizioni precedenti sia soddisfatta
        #la coppia è formata da animali che non si predano che dissipano energia
        else:
            spec_1[0]-=d
            spec_2[0]-=d
        
          
    #Time : tempo di evoluzione del sistema
    #I : specie che migrano nell'isola randomicamente ogni dt
    #Es: I=2, dt=1 --> ogni step arrivano 2 specie
    #Es2: I=1, dt=3 --> ogni 3 step arriva 1 specie
    #verbose : mostra in tempo reale l'evoluzione del sistema
    def Evolve(self,Time,I,dt=1,verbose=False,show_results=False):
        t_step=0
        
        if(len(self.Individuals)==0):
            #first born in the island
            self.Add_individual(energy=delta)
            
        for t in range(Time):
            t_step+=1
            #FLUSSO MIGRAZIONE 
            if(t_step==dt):
                for migrants in range(I):
                    species=np.random.choice(self.all_species,1)
                    self.Add_individual(Species=species,energy=delta)
                t_step=0

            #estraggo len(Individuals)//2 coppie di individui
            if(len(self.Individuals)>1):
                
                is_there_space=self.Basals_counts()<self.Area
                pairs=self.Create_Pairs()
                for p in pairs:
                    spec_1=self.Get_individual(p[0])
                    spec_2=self.Get_individual(p[1])
                    
                    #Controlla tutte le possibili dinamiche preda predatore
                    #e aggiorna lo stato delle due specie accoppiate
                    self.Interaction_dynamics(spec_1,spec_2,is_there_space) 
                      
            #La funzione Deaths() rimuove gli individui con energia nulla
            #ed estrae randomicamente una percentuale di individui che muoiono
            daily_deaths=self.Deaths()

            #Births() si occupa di computare nuove nascite in caso di individui
            #con energia>E_rep
            daily_births=self.Births()

            N_species=len(self.species_alive())
            daily_basals=self.Basals_counts()
            self.Population_t=np.append(self.Population_t,[[len(self.Individuals)-daily_basals,daily_basals,N_species]],axis=0)

            if(verbose):
                print("-------- Day = ",t,"-------------")
                print("Daily Births = ",daily_births)
                print("Daily Deaths = ",daily_deaths)
                print("Animals/Basals number= ",self.Population_t[-1][0],"/",self.Population_t[-1][1])
                print("There are ",N_species," different species alive")
            else:
                print("\rDay = ",t,"", end= '',flush=True)
        if(show_results):
            self.plot_pop()
                
                
                
        
        
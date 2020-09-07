#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:53:06 2020

@author: glatt
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#Ðeterministic Continuous Model

#FUNZIONA TUTTO BENINO MA SE I BASALS VANNO ESTINTI ACCADE CHE UNA VOLTA RIPESCATI
#ESSENDO PRIVI DI PREDATORI INIZIANO A CRESCERE A DISMISURA
#e non capisco perchè fa estinguere le altre specie!

class DCM:
    
    def __init__(self):
        self.S=2000
        self.N=np.zeros(self.S)
        self.l_max=8

        self.R=100
        self.gamma0=0.2
        self.gamma_max=5
        self.N_c=0.5
        self.N_i=10
        self.alpha=0.5
        self.beta=0.1

        
        self.gamma=np.zeros((self.S,self.S))
        #self.gamma[0]=np.random.uniform(-self.gamma_max,0,size=self.S)
        #self.gamma[0][0]=0
        #self.gamma[:,0]=-self.gamma[0]
        
        self.pool=list(range(self.S))
        #Adding basal species
        self.N[0]=self.N_i
        self.population_t=np.empty((0,self.S))
        self.population_t=np.append(self.population_t,[self.N],axis=0)
        self.N_species=[]
        self.N_species=np.append(self.N_species,1)
        
    def Livings(self,pop=None):
        if (pop==None):
            living_list=np.where(self.N!=0)
        else:
            living_list=np.where(pop!=0)
        return living_list
    
    def Beings(self):
        being_list=np.where(self.N!=0)
        being_list=np.setdiff1d(being_list,0) 
        return being_list
            
    def New_species(self):
        N_livings=len(self.Livings()[0])
        daily_pool=np.setdiff1d(self.pool,self.Livings())
        
        #SE DAILY POOL NON È VUOTA, ALLORA PROCEDI ALL'ESTRAZIONE 
        if (np.any(daily_pool)):
            new_species=np.random.choice(daily_pool)
        
            if (N_livings<self.l_max and N_livings):
            
                if (N_livings==1):
                    n_preys=1
                
                else:
                    n_preys= np.random.randint(1,N_livings)
                
                preys=np.random.choice(self.Livings()[0],n_preys,replace=False)
           
                for prey in preys:
                   
                    self.gamma[new_species][prey]=np.random.uniform(0,self.gamma_max)
                    self.gamma[prey][new_species]=-self.gamma[new_species][prey]
                    
            elif(N_livings>=self.l_max):
            
                n_preys=np.random.randint(0,self.l_max)
                preys=np.random.choice(self.Livings()[0],n_preys,replace=False)
            
                for prey in preys:
                
                    self.gamma[new_species][prey]=np.random.uniform(0,self.gamma_max)
                    self.gamma[prey][new_species]=-self.gamma[new_species][prey]
                
            self.N[new_species]=self.N_i

                
            
        
    def get_index(self,ID,prey=False,predator=False):
        
        if (prey):
            idx=np.where(self.gamma[ID]>0)
        elif (predator):
            idx=np.where(self.gamma[ID]<0)
                        
        else:
            print("Specify which kind of index for the ID")
        return idx
        
    
    def Extinction(self):
        ext_idx=np.where(self.N<self.N_c)
        for i in ext_idx:
            self.gamma[i]=0
            self.gamma[:,i]=0
            self.N[i]=0
        
    def f(self,N_sel,t):
        dNdt=[]
        N0=np.copy(self.N)
        #Se il primo degli esseri viventi sono le risorse esterne, allora computane l'ODE
        if(self.Livings()[0][0]==0):
            basals_func=N_sel[0]*self.gamma0*self.R+N_sel[0]*np.dot(self.gamma[0],N0)
            dNdt=np.append(dNdt,basals_func)
        for i in range(len(self.Beings())):
            func=-self.alpha*N_sel[i]-self.beta*N_sel[i]**2+N_sel[i]*np.dot(self.gamma[i],N0)
            
            dNdt=np.append(dNdt,func)
            
        return dNdt
    
    def plot_pop(self,Livings_only=True,N_species=True,yuplimit=200):
        t=len(self.population_t)
        if (Livings_only):
            for i in self.Livings()[0]:
                if(i==0):
                    plt.plot(range(t),self.population_t[:,i],linestyle='--',label="Resources")
                    plt.legend()
                                       
                else:
                    plt.plot(range(t),self.population_t[:,i])
                    plt.title("Livings Species Biomasses")

        else:
            for i in range(self.S):
                if(i==0):
                    plt.plot(range(t),self.population_t[:,i],linestyle='--',label="Resources")
                else:
                    plt.plot(range(t),self.population_t[:,i])
                    plt.title("All Species Biomasses history")
        if (N_species):
            plt.plot(range(len(self.N_species)),self.N_species,label="N.Species",linestyle="dotted")
            
        plt.xlabel("Time")
        plt.ylabel("Species Biomass")
        plt.ylim(self.N_c,yuplimit)
        plt.legend()
    
    def migration(self,I):
        for migrant in range(I):
            self.New_species()
        self.population_t=np.append(self.population_t,[self.N],axis=0)
        self.N_species=np.append(self.N_species,len(self.Livings()[0]))

            
            

    def Evolve(self,T,I,dt=1):
        t_step=0
        time=np.linspace(0,0.01,2)
        
        for day in range(T):
            
            if(len(self.Livings()[0])!=self.S):
                #MIGRATION SECTION
                t_step+=1
                if(t_step==dt):
                    self.migration(I)
                    t_step=0
                    
            Ns=odeint(self.f,self.N[self.Livings()],time)[1]
            self.N[self.Livings()]=Ns
            #self.population_t=np.append(self.population_t,[self.N],axis=0)

            self.Extinction()
            self.population_t=np.append(self.population_t,[self.N],axis=0)
            self.N_species=np.append(self.N_species,len(self.Livings()[0]))
            
            print("\r Day = ",day,end='',flush=True)
            
            
            
        
    
    
        
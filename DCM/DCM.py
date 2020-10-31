#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 18:53:06 2020

@author: glatt
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import networkx as nx
import matplotlib as mpl


#Ðeterministic Continuous Model

class DCM:
    
    def __init__(self,species_number=2500):
        self.S=species_number
        self.N=np.zeros(self.S)
        
        self.l_max=8
        self.R=100
        self.gamma0=0.2
        self.gamma_max=5
        self.N_c=0.5
        self.N_i=10
        self.alpha=0.5
        self.beta=0.1
        
        self.default_params=[self.l_max,self.R,self.gamma0,self.gamma_max,self.N_c,self.N_i,self.alpha,self.beta]

        
        self.gamma=np.zeros((self.S,self.S))
        #self.gamma[0]=np.random.uniform(-self.gamma_max,0,size=self.S)
        #self.gamma[0][0]=0
        #self.gamma[:,0]=-self.gamma[0]
        
        self.pool=list(range(self.S))
        
        #Adding basal species
        self.N[0]=self.N_i
        self.population_t=np.empty((0,self.S))
        self.population_t=np.append(self.population_t,[self.N],axis=0)
        self.species_t=[]
        self.species_t=np.append(self.species_t,1)
        self.G=nx.DiGraph()

    
    def get_params(self):
        '''Prints and returns all the currents ecosystem parameters.'''
        
        print("l_max=",self.l_max,"R=",self.R,"gamma0=",self.gamma0,"gamma_max=",self.gamma_max,"N_c=",self.N_c,"N_i=",self.N_i,"alpha=",self.alpha,"beta=",self.beta)
        
        return [self.l_max,self.R,self.gamma0,self.gamma_max,self.N_c,self.N_i,self.alpha,self.beta]
    
    def set_params(self,params_arr):
        '''The given argument array modifies all the ecosystem parameters in this order: l_max, R, gamma0, gamma_max, N_c, N_i, alpha, beta.'''

        
        self.l_max=params_arr[0]
        self.R=params_arr[1]
        self.gamma0=params_arr[2]
        self.gamma_max=params_arr[3]
        self.N_c=params_arr[4]
        self.N_i=params_arr[5]
        self.alpha=params_arr[6]
        self.beta=params_arr[7]
        
        print("Ecosystem paramters has been modified.")
        self.get_params()
    
    def set_default(self):
        '''set all ecosystem parameters with prefixed values'''
        self.set_params(self.default_params)
    
    
    def livings(self,pop=None):
        '''Returns an array filled with all the species ID which have a biomass value greater than zero.'''
        none_type=type(None)
        if (type(pop)==none_type):
            living_list=np.where(self.N!=0)
        else:
            living_list=np.where(pop!=0)
        return living_list
    
    def animals(self,pop=None):
        '''Returns an array filled with all the species ID which are alive but without counting the basal species.'''
        
        being_list=self.livings(pop)
        being_list=np.setdiff1d(being_list,0)
        return being_list
            
    def new_species(self):
        '''This function is called in the migration section and when allowed to execute it extracts a not yet aliving species from the pool and randomly assigns preys from the set of ecosystem livings species. The new species will have a fixed starting biomass.'''
        
        N_livings=len(self.livings()[0])
        daily_pool=np.setdiff1d(self.pool,self.livings())
        
        #SE DAILY POOL NON È VUOTA, ALLORA PROCEDI ALL'ESTRAZIONE 
        if (np.any(daily_pool)):
            new_species=np.random.choice(daily_pool)
        
            if (N_livings<self.l_max and N_livings):
            
                if (N_livings==1):
                    n_preys=1
                
                else:
                    n_preys= np.random.randint(1,N_livings)
                
                preys=np.random.choice(self.livings()[0],n_preys,replace=False)
           
                for prey in preys:
                   
                    self.gamma[new_species][prey]=np.random.uniform(0,self.gamma_max)
                    self.gamma[prey][new_species]=-self.gamma[new_species][prey]
                    
            elif(N_livings>=self.l_max):
            
                n_preys=np.random.randint(0,self.l_max)
                preys=np.random.choice(self.livings()[0],n_preys,replace=False)
            
                for prey in preys:
                
                    self.gamma[new_species][prey]=np.random.uniform(0,self.gamma_max)
                    self.gamma[prey][new_species]=-self.gamma[new_species][prey]
                
            self.N[new_species]=self.N_i

                
            
        
    def get_interaction(self,ID):
        '''Returns two array filled with the ID.respectively of preys species and predator species of the species ID given as first argument.'''
        
        print("Preys idx/Predators idx")
        preys_idx=np.where(self.gamma[ID]>0)
        predators_idx=np.where(self.gamma[ID]<0)
                        
        return [preys_idx,predators_idx]
        
    
    def extinction(self):
        '''It checks if any species has biomass equal or below zero and when happens deletes all the relative species interactions from the gamma matrix.'''
        
        ext_idx=np.where(self.N<self.N_c)
        for i in ext_idx:
            self.gamma[i]=0
            self.gamma[:,i]=0
            self.N[i]=0
        
    def f(self,N_sel,t):
        '''This function encloses the symbolic computation of the Lotka-Volterra equation for each species. It builds an array in which each component describes the relative species Lotka-Volterra equation.'''
        
        dNdt=[]
        N0=np.copy(self.N)
        #Se il primo degli esseri viventi sono le risorse esterne, allora computane l'ODE
        if(self.livings()[0][0]==0):
            basals_func=N_sel[0]*self.gamma0*self.R+N_sel[0]*np.dot(self.gamma[0],N0)
            dNdt=np.append(dNdt,basals_func)
        for i in range(len(self.animals())):
            func=-self.alpha*N_sel[i]-self.beta*N_sel[i]**2+N_sel[i]*np.dot(self.gamma[i],N0)
            
            dNdt=np.append(dNdt,func)
            
        return dNdt
    
    def plot_pop(self,Livings_only=True,species_t=True,yuplimit=False):
        
        '''It returns a plot of all species biomasses over time if Livings_only is set True. species_t when set True add to the plot a curve with the number of different species alive over time. yuplimit allows to adjust the y-axis upper limit useful when species biomasses have huge value differences. When left to False, it assumed the biggest biomass value found in the population array.'''
        
        t=len(self.population_t)
        if (Livings_only):
            for i in self.livings()[0]:
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
        if (species_t):
            plt.plot(range(len(self.species_t)),self.species_t,label="N.Species",linestyle="dotted")
        if(yuplimit==False):
            yuplimit=np.max(self.population_t)
        plt.xlabel("Time")
        plt.ylabel("Species Biomass")
        plt.ylim(self.N_c,yuplimit)
        plt.legend()
    
    def migration(self,I):
        '''This function iterates the New_species() function over I value. It then update the Population array with the new species ID and starting biomass.'''
        
        for migrant in range(I):
            self.new_species()
        self.population_t=np.append(self.population_t,[self.N],axis=0)
        self.species_t=np.append(self.species_t,len(self.livings()[0]))

            
            

    def evolve(self,T,I,dt=1):
        '''the Evolve function encloses all the other function calls in a proper sequence in order to simulate a random migration flux.'''
        
        t_step=0
        time=np.linspace(0,0.01,2)
        
        for day in range(T):
            
            if(len(self.livings()[0])!=self.S):
                
                #MIGRATION SECTION
                t_step+=1
                if(t_step==dt):
                    self.migration(I)
                    t_step=0
            #Lotka-Volterra computation      
            Ns=odeint(self.f,self.N[self.livings()],time)[1]
            self.N[self.livings()]=Ns
            #self.population_t=np.append(self.population_t,[self.N],axis=0)

            self.extinction()
            self.population_t=np.append(self.population_t,[self.N],axis=0)
            self.species_t=np.append(self.species_t,len(self.livings()[0]))
            
            print("\r Day = ",day,end='',flush=True)
            
            
    def food_web(self,labels=False):
        '''returns the graphic visualization of the graph associated to the interaction matrix referred only to living species. Since the species ID for DCM are unsuitable for nodes label in the plot, they will be labelled starting from 0. When argument labels is True, a dictionary is printed with all the relationship between plot labels and species ID.'''
        
        #Creating an adjacency matrix with only Living species values
        gamma_adj=np.copy(self.gamma)
        gamma_adj=gamma_adj[self.livings()]
        gamma_adj=gamma_adj[:,self.livings()]
        
        #make the adjacency matrix square
        dim=np.shape(gamma_adj)[0]
        gamma_adj=np.reshape(gamma_adj,(dim,dim))
        
        #remove all the negative values
        gamma_adj[gamma_adj<0]=0
        self.G=nx.from_numpy_matrix(gamma_adj,create_using=nx.DiGraph)
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
        
        if(labels):
            #Associate each living species ID to the node labels.
            labels={}
            for i in range(len(self.livings()[0])):
                labels[i]=self.livings()[0][i]
            print(labels)
            
    
        return plt.show()
        
    
    
        
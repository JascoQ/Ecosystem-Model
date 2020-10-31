![ecosystem-services-definition-examples](https://user-images.githubusercontent.com/68162006/94708885-5fcf9b00-0345-11eb-8925-4edc05b09be8.jpg)


**What is an Ecology model?**

An ecology model is a representation of a natural environment using math and few assumptions.
The set initial conditions for an environment, along with a set of costant, is made up of the number of different species, the allowed area and the interaction matrix which we'll see rules all the prey-predator relationships.

**Library goal**

The main goal of this library is to provide a set of functions capable of set up an environment and monitoring its evolution through time.
Also there's an option to add a constant migration flux to the system to study the relationship between the latter and the population size.

**Two approaches** 

The algorithm is based on a 2018 article written by _U. Bastolla, M. Lässig, S.C. Manrubia and A. Valleriani_ called _Diversity patterns from ecological models at dynamical equilibrium_ and it proposes two different approaches:
* **I**ndividual **B**ased **M**odel 
* **D**eterministic **C**ontinuous **M**odel.

The first one consider each species individual as one separate array with its relative energy, the species number and a unique **ID** number to keep track of its evolution. 
The latter treats each species as a singular individual with its biomass and uses Lotka-Volterra equations to compute biomass values over time.

**Interaction Matrix**

To rules interaction dynamics between species a *N*x*N* matrix called *gamma* is build, where *N* is the overall species number which represent the sum between basal species and animal species. 

The former includes all the species which occupy the lowest trophic level in the food chain.
They can be thought as the species which convert solar energy into resources for the environment.

In the case of **DCM** there's no need of specify the overall number of species because it is considered infinite. Of course there's no such things in computer science, so a significantly great number **S** (>2000) is taken to represent the number of species.
Each time a species enter the system, a specific number of preys (N_preys) is randomly extracted between 1 and a costant **l**, then N_preys are randomly chosen among the present species, so that the relative gamma components are initialized randomly between 0 and a costant **E**, representing the maximum value of energy gain that a predator can achieve eating a prey.


In the particular case of **IBM** there are two method to build the interaction matrix:

* Random mode (**RM**)
* Cascade mode (**CM**)

**RM** ask for two more arguments: basal species and animal species number.
Then for each species, a random number between 1 and a costant **l** representing the maximum number of preys for a predator is assigned.
So, the relative gamma components are initialized with a random number between 0 and **E**.

**CM** ask only for a number representing the overall number of species allowed in the ecosystem (**N.species**).
Since all the species are encapsulated in a sorted numbered array, it treats all the species as potential predators of all the species with a lower species number S.
First, it computes a chance rate of being a predator as the ratio **l/N. species**, where **l** is a prefixed costant.
Consider a species number **S<sub>x</sub>**, then for each species with **S<sub>i</sub>**<**S<sub>x</sub>** there's a chance that **S<sub>x</sub>** individuals became predator of **S<sub>i</sub>** species.

![flussodiag (1)](https://user-images.githubusercontent.com/68162006/94003189-39d15600-fd9b-11ea-9bc7-9d70b8d61afd.png)


**IBM**
The individual approach treats all the species as discrete units with unique ID and energy value. 
To initialize an IBM object from its class, you must decide which interaction method you want for your ecosystem between Random and Cascade methods.

Then, you can initialize an object from an hereditary class that could be RM_IBM or CM_IBM.

```ruby

eco_system=RM_IBM(Area, Animal_species,Basals_species)
```

```ruby

eco_system=CM_IBM(Area, Overall_species)
```

Area argument accept only each kind of numerical type. Any input with decimal digit will be rounded to integer.
Interaction method accept only two strings already explained above: **RM** and **CM**.

Each time step a set of rules is implemented:
* Pair formation - random pair creation among all the alive individuals (if N is odd, an individual remains unpaired).

* Couple interactions - for each couple a different dynamic is implemented based on the interaction matrix and the individuals energy (more on this later when Interaction_dynamics() method is described.

* Basal growth - to simulate conversion from chemical energy to resources for the environment a fixed energy gain (**d** costant) for all basal species is computed each time step.

* Dissipation - for each animal alive is applied a reduction of his energy in order to simulate his tiredness due the daily "hunt" activity.

* Reproduction - when an individual energy exceeds a certain threshold (**E_rep*** costant), a birth occurs. The "parent" individual adds a same species individual to the roster with starting energy equal to a **b** costant, while the former has a energy loss of **b**. 
In the case of basal species, the birth occurs only if the Basal counts is below the Area value.

* Death - when an individual energy decreases below 0 (it occurs only when the individual is paired with a predator or if its energy over time is completely dissipated), death occurs for the individual. It means that the individual array is deleted.


**Class Methods**

```ruby
get_params():
```
just prints all the IBM arguments with the current costants values.

```ruby
basals_counts():
```
prints the integer number representing the count of basal species alive.

```ruby
species_alive():
```
returns a list of all species ID alive in the ecosystem.
```ruby
get_predators(prey_species):
```
returns a list with all the species ID who predate the species given as argument.
```ruby
get_preys(predator_species):
```
returns a list with all the species ID of species predator preys.
```ruby
current_situation():
```
prints all the different counts (Individuals alive, different species alive, Animals/Basal species alive, number of births, number of deaths, days passed by.
```ruby
add_invidual(Species=-1,energy=b): 
```
this function adds a species individual to the ecosystem. When Species is specified as an integer number the method will add that specified species to the ecosystem, while when the arg is negative, the individual species is randomly draw. 
The energy arg likewise act as the species arg. When specified, the newborn will have a start energy equal to the input, otherwise it will have an energy equal to the b costant.
```ruby
deaths(): 
```
This function is called each time step and it computes a death chance among all the living individuals. Also it checks if any energy's individual is below 0, then deletes from the living individuals all the death ones and returns the total number of deaths.
```ruby
births()
```
As explained above, each time step checks if any individual energy is above a fixed threshold (**E_rep**). If an individual with species=S has its energy above **E_rep**, then Add_Individual(Species=S) is called in order to add a newborn individual with fixed energy.
In the case of basals species, the birth occurs only if Num. Basals < Area.

```ruby
get_params()
```
It prints and returns all the currents ecosystem parameters

```ruby
set_params(params_arr)
```
It changes all the ecosystem parameters with the params_arr components in this order:  Area, E_rep, P_death, E_max, delta, l, d, b

```ruby
set_default()
```
It calls set_params method with params_arr argument set as self.default_params.


```ruby
individuals_per_species()
```
Computes and plot an histogram representing the individuals count for each different species in the ecosystem.

```ruby
create_Pairs():
```
As we will see later, each time step is necessary to pair all the alive individuals in the ecosystem. The Create_Pairs() method, once called returns an array with shape (L//2, 2) filled with couple of individual IDs. sThe L//2 notation stands for the rounded result of L/2.

```ruby
get_individual(ID):
```
Returns an array containing all the ID individual features: Energy, species number, ID.
Any edit to those values will change the actual individual parameters.

This function is usually called after Create_Pairs() in a loop as the following:
```ruby
pairs=eco_system.Create_Pairs()
for p in pairs:
    spec_1=eco_system.Get_individual(p[0])
    spec_2=eco_system.Get_individual(p[1])
```
```ruby
interaction_dynamics(species_1,species_2,is_there_space=True):
```
This function is called inside the main loop and encloses all the different cases of interaction which can occur between two species.
is_there_space is a boolean argument given each time step by the condition Num.Basals<Area.

Possible interactions:
* Prey (i) - Predator (j): the former individual energy is set to 0, while the predator energy is increased by the interaction coefficient multiplied to the prey energy. 

**e(i) → 0** ; **e(j) → e(j) + C<sub>i</sub><sub>j</sub>  e(i)**

* C<sub>i</sub><sub>j</sub>=0 : this lead to a null interaction and the individuals involved (if not basals will only dissipate energy):

**e(i) → e(i)-d** ; **e(j) → e(j) -d**

* Basal-Basal : basals individuals doesn't interact between them, so each individual is given an energy gain called **basal growth**. To damp basals reproducing, the basal growth is applied only when is_there_space=True.

**e(i) → e(i)+b** ; **e(j) → e(j)+b** 


```ruby
evolve(Time,I,dt=1,verbose='days',show_results=False):
```

evolve is the main class function that enclose all the above methods in order to properly simulate the time evolution.

**Args:**
* Time: it accepts only integers representing the desired time steps number.
* I: immigration flux number. it accepts only integers representing how many individual migrate to the ecosystem each **dt**.
* dt: set the time step for the migrated individual to arrive.

Examples:

I=2, dt=1 →
Each time step two random individuals migrate to the ecosystem.

I=2, dt=3 →
Each 3 time step two random individuals migrate to the ecosystem.

* verbose: When set to "True" or "full" it will prints, for each timestep, information on ecosystem evolution. If set to 'days' as default, it will print only how many timesteps (days) have passed. Also, if set to "False", no information will be printed.
* show_results: if True, prints after the last time step, a plot representing the counts of Animal/Basal species in the ecosystem through time.


```ruby
plot_pop(Animals=True,Basals=True,Species=True,Area=False):
```
Returns a plot of the Basals/Animals/Species counts over time based on the given arguments.
It's the function called with default args inside **Evolve** function when "show_results" arg is set True.

```ruby
food_web(draw=False):
```
It returns a graphic visualization of the network **G** associated to the interaction matrix along with the average number of preys for predator, the average number of predators for prey and the total number of edges in the network. All these measurements are computed through NetworkX methods on the food web.

A foodweb network associated to an ecosystem has the nodes as species, while the edges represents the prey-predator relationship between species.

**IBM script example**

```ruby
Area=10000
Animal_species=1000
Basal_species=100

eco_system=RM_IBM(Area,Animal_species,Basal_species)

I=1
eco_system.evolve(200,I,dt=1,verbose=False,show_results=True)
```
![plot_test](https://user-images.githubusercontent.com/68162006/94047174-0231d080-fdd2-11ea-8cb5-69562f236efa.png)

**IBM Variables**

* **Area**: it represents the ecosystem area.
* **all the single ecosystem paramters**
* **default_params**: an array with all the default ecosystem parameters.
* **Basals**: an array with all the basal species ID
* **Predators**: an array with all the non basal species ID
* **all_species**: an array with all the species ID
* **C**: interaction matrix
* **Individuals[Energy][Species_ID][ID]**: an array in which each row represents an individual with 3 components which stands for Energy, Species, individual unique ID.

* **Population_t**: it's an array which each time step stores the whole Individuals array. So, once the ecosystem has evolved, it is possible to keeping track of all the individuals evolution.

* **N_births**: It counts the total number of births in an ecosystem
* **N_deaths**: same as above, but for the deaths count.
* **G**: the graph associated to the **gamma** matrix when intended as adjacency matrix.


**DCM**

The Deterministic Continuous Model class has no argument. The goal is to get an approximation of an ecosystem with an infinite number of possible species. In order to achieve this we fix a arbitrary huge number for the number of different species allowed (**S>2000**).
Then, once called the Evolve function, each time step a fixed number of new species enter the ecosystem and randomly get assigned a set of preys.
To avoid early extinction no predators are assigned to new species. The latters became potential preys starting from the next time step.

In this model basal species are gathered all in one species (for simplicity the 0 species).
Then, for each time step, the Lotka-Volterra equation are computed based on the random interaction matrix built until that step.
Lotka-Volterra equation describes how the biomass of a species change over time based on the interaction with other species and all the currently biomasses.

![lotkavolterra](https://user-images.githubusercontent.com/68162006/94476185-6c7eb280-01d0-11eb-93d0-6db7f0274c6d.png)

where it is assumed that α and β are fixed constant equivalents for all species (so, for each _i_ belonging to the set of species ID).

```ruby
import DCM
Eco_system=DCM()
```

![Untitled Diagram](https://user-images.githubusercontent.com/68162006/94601463-d744f200-0293-11eb-9979-fb7ebf5815e9.png)

**Class Methods**
```ruby
livings(pop=None):
```
Returns an array filled with all the species ID which have a biomass value greater than zero.

```ruby
animals(pop=None):
```
Returns an array filled with all the species ID which are alive but without counting the basal species.

```ruby
get_index(ID,prey=False,predator=False):
```
Returns one or two array filled with the ID.respectively of preys species and predator species of the species ID given as first argument.

```ruby
get_params()
```
It prints and returns all the currents ecosystem parameters

```ruby
set_params(params_arr)
```
It changes all the ecosystem parameters with the params_arr components in this order:  l_max, R, gamma0, gamma_max, N_c, N_i, alpha, beta.

```ruby
set_default()
```
It calls set_params method with params_arr argument set as self.default_params.


```ruby
new_species():
```
This function is called in the migration section and when allowed to execute it extracts a not yet aliving species from the pool and randomly assigns preys from the set of ecosystem livings species. 
The new species will have a fixed starting biomass.

```ruby
migration(I):
```
This function iterates the New_species() function over **I** value. It then update the Population array with the new species ID and starting biomass.

```ruby
f(N_sel,t):
```
This function encloses the symbolic computation of the Lotka-Volterra equation for each species. It builds an array in which each component describes the relative species Lotka-Volterra equation. It is optimized to solve the equations only for the species with non-zero biomass (N_sel).
Also it is computed in order to obtain a suitable array for the **scipy.integrate.odeint** function. 

```ruby
Extinction():
```
It simply checks if any species has biomass equal or below zero and when happens deletes all the relative species interactions from the gamma matrix.

```ruby
Evolve(T,I,dt=1):
```
As for the **IBM** case, the Evolve function encloses all the other function calls. The above flowchart give an overview on the script approach. 
It checks first if the number of species alive is equal to the maximum number of species allowed; if False, proceeds to the migration process. Then the Lotka-Volterra equations are computed.
The last step is to call Extinction() and then update the population array with the current biomasses value.

```ruby
plot_pop(Livings_only=True,species_t=True,yuplimit=200):
```
It returns a plot of all species biomasses over time if **Livings_only** is set True. **species_t** when set True add to the plot a curve with the number of different species alive over time.
**yuplimit** allows to adjust the y-axis upper limit useful when species biomasses have huge value differences. When left to False, it assumed the biggest biomass value found in the population array.

```ruby
food_web(labels==False):
```
returns the graphic visualization of the graph associated to the interaction matrix referred only to living species.
Since the species ID for DCM are unsuitable for nodes label in the plot, they will be labelled starting from 0. When argument labels is True, a dictionary is printed with all the relationship between plot labels and species ID.

**DCM script example**

```ruby
import DCM
eco_system=DCM()
eco_system.Evolve(150,1)
eco_system.plot_pop(Livings_only=True,species_t=False,yuplimit=False)
```
![DCM_plot](https://user-images.githubusercontent.com/68162006/94610158-255ff280-02a0-11eb-8552-cfbb63e89ab4.png)

**DCM Variables**
* **Costants**: Lotka-Volterra equations can be tuned through adjusting a set of costant which are listed below (the associated value is the default one):

> S = 2500

Maximum number of different species.
> l_max = 8

Maximum number of preys which can be assigned to a new species arrived to the ecosystem
> R = 100

Basal species external resources intake.
> gamma0 = 0.2
 
It represents a sort of efficiency in absorbing external resources .
> gamma_max = 5

Maximum value that can be extracted for a interaction matrix component.

>N_c = 0.5

Threshold value for surviving. Any species whose biomass value goes below N_c goes extincted.
>N_i = 10

Starting biomass value for new species.
>alpha = 0.5

It represents a dissipation term in the Lotka-Volterra equation.
>beta = 0.1

Add stability to the system by expressing a negative feedback to the growth rate of each species.

* **default_params**: an array with all the default ecosystem parameters. 
* **gamma**: Interaction matrix
* **pool** : an array filled with all the possible species ID.
* **N** : an array in which each component contain the relative species ID current biomass value.
* **population_t**:  an array which each time step stores the whole N array. So, once the ecosystem has evolved, it is possible to keeping track of all the species biomass evolution.
* **species_t**: it keeps track of the number of different species alive through time.

* **G**: the graph associated to the **gamma** matrix when intended as adjacency matrix.
**Workflow**

The algorithm follows few initial steps and then allows to "play" with the ecosystem:
* initialize an **IBM** or **DCM** object
* choose their relative argument values (if any)
* The interaction matrix is build
* Evolve ecosystem for an arbitrary number of time steps.
* Visualize and adjust plots describing the ecosystem evolution



![Mitchell_et_al_Press_Release_Fig_1](https://user-images.githubusercontent.com/68162006/94708718-2eef6600-0345-11eb-8d11-a42087dc76d7.png)






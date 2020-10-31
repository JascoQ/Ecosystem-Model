![impacts-ecosystem-services-definition-examples](https://user-images.githubusercontent.com/68162006/94956800-0bffb600-04ed-11eb-8728-3d4d656e6590.jpg)


# Ecosystem-Model
## Individual based model (IBM) and Deterministic Continuous model (DCM)

Two python classes with few library dependencies built in order to give a set of function to create and evolve an ecosystem with two different approaches.

TAGS:
> IBM, DCM, Lotka-Volterra, Ecosystem, Migration Flux

## Installation

In order to get a clone just launch this command:

```
git clone https://github.com/JascoQ/Ecosystem-Model.git
cd Ecosystem-Model
python setup.py install
```
This will download the package on your computer along with all the needed library dependencies.

## Usage 

The IBM class allow for two interaction methods. To properly handle with both methods at initializing, there are two hereditary classes called RM_IBM and CM_IBM which encloses the different interaction rules.

IBM script example:
```
from IBM import IBM.IBM

area=1000
animals=100
basals=10
migration=2

my_ecosyst=RM_IBM(area,animals,basals)
my_ecosyst.evolve(Time=100,I=migration,dt=1)
my_ecosyst.plot_pop()
```



DCM script example:

```
from DCM import DCM.DCM

my_ecosyst=DCM()
my_ecosyst.evolve(Time=100,I=1)
my_ecosyst.plot_pop()

```



Consult the wiki to get better documentation about class and methods.
# FOAMySees
First public release of Python+preCICE-based coupling driver for OpenSees models. This tool was developed specifically for the purpose of simulation of centerline-extruded finite element models of civil engineering structures. 

Note: I intend to add more example cases, as they are created. Let me know if you are trying something different than what is provided here and I can maybe help figure it out. 

# Dependencies
Python 3.7 or higher

OpenFOAM (any version which can be used with preCICE)

preCICE v2.5.0 (if you change this version, you will need to modify the FOAMySeesCouplingDriver.py file to change the Python language bindings. I think the functions change from preCICE v2.5 to preCICE v3.0. I have not incorporated the v3.0 bindings into the coupling driver yet.)

OpenSeesPy 

# Required Python packages: (install with pip)
pip3 install os

pip3 install concurrent.futures

pip3 install logging

pip3 install queue

pip3 install random

pip3 install subprocess

pip3 install time

pip3 install argparse

pip3 install copy

pip3 install sys

#math and matrices

pip3 install numpy 

pip3 install pandas

pip3 install re

pip3 install csv

pip3 install math

#meshes and visualization

pip3 install meshio

pip3 install matplotlib

pip3 install scipy

pip3 install vtk

pip3 install pyvista 

#openseespy

pip3 install openseespy 

#precice

pip3 install pyprecice

# Author
This code was developed by Nicolette S. Lewis, PhD, at the University of Washington, from 2021 to 2023. For specific questions, please email me.  

# Legal Disclaimer
By using this code, you agree that the author, Nicolette S. Lewis, NHERI, the NHERI SimCenter, the University of Washington, and all others associated with this research assume no responsibility for results obtained with this tool or the applications of such results. Please 

As always, the person, person(s), or otherwise conducting simulations or calculations with this code holds responsibility for ensuring that their solution is physically correct. 

The code as-is was intended to be used specifically for investigating the resilience of civil engineering structures when subject to flows resembling those of natural hazards, such as floods, tsunamis, windstorms, and otherwise. Any use of the code beyond these applications is not verified, and as such caution must be taken when utilizing these procedures in cases not investigated within the doctoral thesis for which the code originally was developed and tested. 

Please do not use this code as the only means of analysis for a given problem. Any design or conclusion originating from analyses conducted with this code should be validated through independent hand calculations, an alternative software (preferably something validated), or should be subject to rigorous investigation by experts of a given problem of interest. 
Due to the large possibility of errors in modelling complicated coupled systems, it is imperative that independent analyses are conducted to ensure that the results obtained from analyses with the offered code are accurate or reasonable. Any findings or otherwise obtained utilizing this code or one of its derivatives is the sole responsibility of the person who constructed and ran the analysis from which such findings were obtained. 

**More specifically, and more clearly, for anyone not well-versed in what the above means: what the user does with this code is up to them, and as such, the consequences of what the user does with this code rest solely on the user, and the user alone. **
**
This code is offered AS-IS at the time of completion of my Doctoral Disseration, December 15th, 2023. I make no assurances that this code will work for future versions of preCICE, OpenSees, or OpenFOAM, but I will try my best to keep this alive as long as I can. Feel free to take this research and do other things with it, including update it for future versions of preCICE, OpenFOAM, or OpenSees.
**
# Acknowlegdments
The work which led to development of this tool was funded by the National Science Foundation (NSF) and Joy Pauschke (program manager) through Grants CMMI-1726326, CMMI-1933184, and CMMI-2131111. Thank you to NHERI Computational Modeling and Simulation Center (SimCenter), as well as their developers, funding sources, and staff for their continued support. It was a great experience to work with the SimCenter to implement this tool allowing for partitioned coupling of OpenSees and OpenFOAM as part of a digital-twin module within the NHERI SimCenter Hydro-UQ framework. Much of the development work of the research tool presented was conducted using University of Washington's HYAK Supercomputing resources. Thank you to UW HYAK and to the support staff of the UW HPC resources for their maintenance of the supercomputer cluster and for offering a stable platform for HPC development and computation, as well as for all of the great support over the last few years.  

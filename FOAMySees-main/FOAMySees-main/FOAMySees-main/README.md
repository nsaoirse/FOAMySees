# FOAMySees
First public release of Python+preCICE-based coupling driver for OpenSees models. This tool was developed specifically for the purpose of coupled simulation of centerline-extruded finite element models of civil engineering structures constructed within the OpenSees framework through the OpenSeesPy and preCICE Python Language bindings. 

I intend to add example cases, as they are created. Let me know if you are trying something different than what is provided here and I can maybe help figure it out. 

# Dependencies
Python 3.7 or higher

OpenFOAM (any version which can be used with preCICE)

preCICE v2.5.0 (if you use a different version, you will need to modify the FOAMySeesCouplingDriver.py file to change the Python language bindings. I think the functions change from preCICE v2.5 to preCICE v3.0. I have not incorporated the v3.0 bindings into the coupling driver yet. Seems like the code will work with v2.4 as well, but 2.5 is recommended)

OpenSeesPy 

# Required Python packages: (install with pip, will install automatically with provided bash installation script)

os
concurrent.futures
logging
queue
random
subprocess
time
argparse
copy
sys

#math and matrices

numpy 
pandas
re
csv
math

#meshes and visualization

meshio
matplotlib
scipy
vtk
pyvista 

#openseespy

openseespy 

#precice

pyprecice

# Author
This code was developed by Nicolette S. Lewis, PhD, at the University of Washington, from 2021 to 2023. For specific questions, please email me at nicolette.s.lewis@outlook.com with "FOAMySees" in the subject line. I will respond to messages as I can.  

# Disclaimer
By using this code, you agree that the author, Nicolette S. Lewis, NHERI, the NHERI SimCenter, the University of Washington, and all others associated with this research assume no responsibility for results obtained with this tool or the applications of such results. 

As always, the person, person(s), or group, otherwise conducting simulations or calculations with this code holds responsibility for ensuring that their solution is physically correct. 

The code as-is was intended to be used specifically for investigating the resilience of civil engineering structures when subject to flows resembling those of natural hazards, such as floods, tsunamis, windstorms, and otherwise. Any use of the code beyond these applications is not verified, and as such caution must be taken when utilizing these procedures in cases not investigated within the doctoral thesis for which the code originally was developed and tested. 

Please do not use this code as the only means of analysis for a given problem. Any design or conclusion originating from analyses conducted with this code should be validated through independent hand calculations, an alternative software (preferably something validated), or should be subject to rigorous investigation by experts of a given problem of interest. Due to the large possibility of errors in modelling complicated coupled systems, it is imperative that independent analyses are conducted to ensure that the results obtained from analyses with the offered code are accurate or reasonable. Any findings or otherwise obtained utilizing this code or one of its derivatives is the sole responsibility of the person who constructed and ran the analysis from which such findings were obtained. 

This code is offered AS-IS. I make no assurances that this code will work for future or past versions of preCICE, OpenSees, or OpenFOAM, but I will try my best to keep the code generally functional for as long as I can/have the energy. Feel free to take this research and do other things with it, including update it for future versions of preCICE, OpenFOAM, or OpenSees.

# Acknowlegdments
The work which led to development of this tool was funded by the National Science Foundation (NSF) and Joy Pauschke (program manager) through Grants CMMI-1726326, CMMI-1933184, and CMMI-2131111. Thank you to NHERI Computational Modeling and Simulation Center (SimCenter), as well as their developers, funding sources, and staff for their continued support. It was a great experience to work with the SimCenter to implement this tool allowing for partitioned coupling of OpenSees and OpenFOAM as part of a digital-twin module within the NHERI SimCenter Hydro-UQ framework. Much of the development work of the research tool presented was conducted using University of Washington's HYAK Supercomputing resources. Thank you to UW HYAK and to the support staff of the UW HPC resources for their maintenance of the supercomputer cluster and for offering a stable platform for HPC development and computation, as well as for all of the great support over the last few years.  


# Instructions
Download the Github repository

navigate to the folder containing the repository files and the 'installFOAMySees' file 

run 'chmod u+x installFOAMySees; ./installFOAMySees' within the repository directory 

If successful:
startFOAMySees should be available as a command after running the installation script

In order to run a case, you will need an OpenFOAM case folder, and an OpenSees model

Some example cases are provided. 

One could modify these cases to perform various types of analysis. 

Alternatively, https://precice.org/adapter-openfoam-config.html#fsi
Configure your OpenFOAM case according to the above link. 

The controlDict, preciceDict, and precice-config.xml files will be automatically generated for your case depending on the settings you have chosen.

The boundary conditions will need to be modified automatically, within the 0.org folder of the OpenFOAM case with which you would like to run a case. 



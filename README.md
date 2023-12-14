#FOAMySees
First public release of Python+preCICE-based coupling driver for OpenSees models. This tool was developed specifically for the purpose of simulation of centerline-extruded finite element models of civil engineering structures. 

Note: I intend to add more example cases, as they are created. Let me know if you are trying something different than what is provided here and I can maybe help figure it out. 

#Author
This code was developed by Nicolette S. Lewis, PhD, at the University of Washington, from 2021 to 2023. For specific questions, please email me. 

#Legal Disclaimer
By using this code, you agree that the author, NHERI, the NHERI SimCenter, the Univeristy of Washington, and all others associated with this research assume no responsibility for the accuracy of models coupled with this tool, or the purposes for which any model with this tool was utilized. Any person or person(s) conducting simulations with this code holds responsibility for ensuring that their solution is physically correct. 

More specifically, and more clearly, for anyone not well-versed in what the above means: what you do with this code is up to you, and as such, the consequences of what you do with this code rest solely on you. 

Due to the large possibility of errors in modelling complicated coupled systems, any engineering design, analysis result, parametric study, academic or commercial finding, application, future application, or otherwise obtained utilizing this code or one of its derivatives is the sole responsibility of the person who constructed and ran the analysis using this code. 

This code is offered AS-IS at the time of completion of my Doctoral Disseration, December 15th, 2023. I make no assurances that this code will work for future versions of preCICE, OpenSees, or OpenFOAM, but I will try my best to keep this alive as long as I can. Feel free to take this research and do other things with it, including update it for future versions of preCICE, OpenFOAM, or OpenSees.

#Acknowlegdments
The work which led to development of this tool was funded by the National Science Foundation (NSF) and Joy Pauschke (program manager) through Grants CMMI-1726326, CMMI-1933184, and CMMI-2131111. Thank you to NHERI Computational Modeling and Simulation Center (SimCenter), as well as their developers, funding sources, and staff for their continued support. It was a great experience to work with the SimCenter to implement this tool allowing for partitioned coupling of OpenSees and OpenFOAM as part of a digital-twin module within the NHERI SimCenter Hydro-UQ framework. Much of the development work of the research tool presented was conducted using University of Washington's HYAK Supercomputing resources. Thank you to UW HYAK and to the support staff of the UW HPC resources for their maintenance of the supercomputer cluster and for offering a stable platform for HPC development and computation, as well as for all of the great support over the last few years.  

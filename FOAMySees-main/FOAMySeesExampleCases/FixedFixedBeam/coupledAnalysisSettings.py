
oneWay=0 # if this is 1, then the displacements calculated by OpenSees are not transferred to OpenFOAM
#also..  # if this is 2, then the forces calculated by OpenFOAM are not transferred to OpenSees


############      NOTE : If FOAMySees if run 'as a part of HydroUQ', most if not all of these settings
############		will likely be overwritten! 
############
############
############
############
############
############  Input the settings for your coupled analysis below 

numOpenSeesStepsPerCouplingTimestep=1
numOpenFOAMStepsPerCouplingTimestep=1



#### Timing Settings #####
############ BOTH OpenFOAM and OpenSees
SolutionDT=1e-4 # this is the coupling timestep length
runPrelim='yes' # run the preliminary analysis defined (maybe remove this???)
startOFSimAt=0.0
endTime=1



###########################################################################################################
###########################################################################################################
###########################################################################################################
# openSees settings
ApplyGravity='yes'
g=[0,0,-9.81]

###########################################################################################################
###########################################################################################################
###########################################################################################################
OpenSeesconvergenceTol=1e-8
#'EnergyIncr', Tol, maxNumIter
Test=["NormUnbalance",1e-8,1000]
Integration=["Newton",0.5,0.25]
Algorithm="KrylovNewton"
OpenSeesSystem='BandGen'
OpenSeesConstraints='Transformation'
Numberer='RCM'
OSndm=3
OSndf=6
Analysis=["VariableTransient","-numSubLevels",2,"-numSubSteps",10]

###########################################################################################################
###########################################################################################################
###########################################################################################################


# OpenFOAM...
AdjustTimeStep='no'
SimDuration=endTime
Turbulence="No"
interfaceSurface="interface.stl"
DecompositionMethod="scotch"


###########################################################################################################
###########################################################################################################
###########################################################################################################

###########################################################################################################
###########################################################################################################
###########################################################################################################
#### Coupling Settings #####
CouplingScheme="Implicit" # "Explicit"
timeWindowsReused=3		# number of past time windows used to approximate secant behavior
iterationsReused=5		# number of iterations used to accelerate coupling data
couplingConvergenceTol=5e-3     # coupling data relative residual convergence value
initialRelaxationFactor=0.1     # initial relaxation factor used in dynamic relaxation scheme

couplingDataAccelerationMethod="IQN-ILS" #Constant Aitken IQN-IMVJ Broyden

maximumCouplingIterations=100 #set this to a high value

mapType='nearest-neighbor' #'rbf-thin-plate-splines'# either or - nearest-neighbor is faster, rbf is more robust...

###########################################################################################################
###########################################################################################################
###########################################################################################################
#### OUTPUT SETTINGS ######
#OpenFOAM Write Frequency
writeDT=0.1 # seconds

#OpenSeesPy Write Frequency
SeesVTKOUTRate=0.1 # seconds

# This is to output data during the coupling iterations from preCICE library data transfers. Could help with debugging, but generally is best to leave as "No"
outputDataFromCouplingIterations="No"
couplingIterationOutputDataFrequency="1000"

###########################################################################################################
###########################################################################################################
# /*--------------------------------*- C++ -*----------------------------------*\
# | =========                                               ____/_________\____     _.*_*.             |
# | \\      /      F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \\.           |
# |  \\    /       O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | | \._        |
# |   \\  /        A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\.__... |
# |    \\/         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___...     |
# |_________________________________________________________||  |/\| | |/\|  ||__/,_/__,_____/...______|
	# \*---------------------------------------------------------------------------*/

# The work within this thesis was funded by the National Science Foundation (NSF) and Joy Pauschke (program manager) through Grants CMMI-1726326, CMMI-1933184, and CMMI-2131111. 
# Thank you to NHERI Computational Modeling and Simulation Center (SimCenter), as well as their developers, funding sources, and staff for their continued support. 
# It was a great experience to work with the SimCenter to implement this tool allowing for partitioned coupling of OpenSees and OpenFOAM as part of a digital-twin module within the NHERI SimCenter Hydro-UQ framework.
# Much of the development work of the research tool presented was conducted using University of Washington's HYAK Supercomputing resources. 
# Thank you to UW HYAK and to the support staff of the UW HPC resources for their maintenance of the supercomputer cluster and for offering a stable platform for HPC development 
# and computation, as well as for all of the great support over the last few years.  



###########################################################################################################
###########################################################################################################


# Set fixity options
########################### only use if you want to
fixXat=[0.0] # this is a list
fixYat=[0.0] # this is a list
fixZat=[0.0]# this is a list
###########################################################################################################
fixX='no' # change this to yes to apply a fixity BC along the domain at the coordinates within 'fixXat' list
fixY='no'# change this to yes to apply a fixity BC along the domain at the coordinates within 'fixYat' list
fixZ='no'# change this to yes to apply a fixity BC along the domain at the coordinates within 'fixZat' list

###########################################################################################################
fixXatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixXat' list
fixYatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixYat' list
fixZatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixZat' list


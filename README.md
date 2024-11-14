# FOAMySees development Version
This version uses preCICE v3 for additional functionality and stability.
Code changes include 
-port from preCICE v2 to v3. 
-improved code compactness and functionality
-minor bug fixes in coupling driver.
-additional logging of solution status and progress
-fixed broken preprocessing scripts
Tested on Ubuntu 24.04.1 LTS 
In this branch, I used precice-3.1.2, OpenFOAM v2406, and Python 3.12, along with a pip-installed version of openseespy and the python precice bindings

The best approach I have found to compile all the dependencies is to use something like Spack as a package manager, or to install
*everything* with sudo/root priveleges. The installation shell scripts for the various dependencies are great,
but I recommend using something like ccmake and cmake in addition to these to configure your makefiles with some sort of GUI.
Some of the required packages will be found through pkg-config, some through the PATH variable, and some will need a specific environment
variable to be defined to locate the .H files required to compile shared objects. Thus, preliminary attempts at constructing a dockerized container of all required libraries are in progress...

# Dependencies
Python 3 (3.6 or higher, likely. I used 3.12)

OpenFOAM (any version which can be used with preCICE)

preCICE v3.1.2

OpenSeesPy 

/ Required Python packages: (import or install with pip, will install automatically with provided bash installation script)

Don't worry about these. Follow the instructions below and everything _should_ install properly...


# Installation Instructions
Download the Github repository to somewhere you'd like it to stay. 
The files within the repository are largely Python and bash files which will construct a coupled analysis case, depending on the inputs to the program provided. (the files are needed for case setup, and this directory is added to your user .bashrc profile, as well as a few aliases)

cd {folder where you're keeping the source files }
git clone thisrepo
unzip FOAMySees-main.zip

navigate to the folder containing the repository files and the 'installFOAMySees' file 

cd FOAMySees-main/

run the installation bash script, which modifies your .bashrc file (doesn't do much else)

./installFOAMySees

If you don't have permission, run
chmod u+x installFOAMySees; ./installFOAMySees
within the repository directory 

./setFOAMySeesEnvironment

If successful:
**startFOAMySees** should be available as an alias command after running the installation script
as well as other aliases:
**createFOAMySeesInputFiles** - which will copy files necessary to start a coupled analysis with FOAMySees to the current directory

_**Attempt at a full-install script (probably will error out at some point, but if you know what you're doing, this should get you most of the way to a complete environment**_


**Update and install dependencies**

sudo apt-get update

sudo apt-get install -y libhdf5-serial-dev python3-full build-essential cmake git ca-certificates flex

sudo apt update 

sudo apt install -y build-essential cmake libeigen3-dev libxml2-dev libboost-all-dev petsc-dev python3-dev python3-numpy gfortran g++ git cmake gcc python3-pip liblapack-devlibopenmpi-dev libmkl-rt libmkl-blacs-openmpi-lp64 libscalapack-openmpi-dev tcl-dev tk-dev libeigen3-dev

sudo pip install -y --break-system-packages conan==1.60

**Install MUMPS for massively parallel simulation**

git clone https://github.com/OpenSees/mumps.git

cd mumps

mkdir build

cd build

cmake .. -Darith=d

cmake --build . --config Release --parallel 4

cd ../..

**Install OpenSees from source, or....**

git clone https://github.com/OpenSees/OpenSees.git

cd OpenSees

rm -rf build

mkdir build

cd build

conan profile detect

$HOME/.local/bin/conan install .. --build missing

cmake .. -DMUMPS_DIR=$PWD/../../mumps/build

cmake --build .. --target OpenSees -j8

cmake --build .. --target OpenSeesPy -j8

mv ./lib/OpenSeesPy.so ./opensees.so

cd ../..

_at this point in the installation of opensees, i had some trouble with conan. might not be worth installing from source for this purpose, since we are just using it to build openseespy anyway. The intent of attempting this would be to allow for MPI communication between the Python initialized OpenSeesPy model and the preCICE coupling library. Would be worth it, if you had a million degrees of freedom to couple!_

**......you could probably just use pip**
pip install openseespy

** Install OpenFOAM from source ( you will need the header files to install the OpenFOAM preCICE adapter)**

git clone https://develop.openfoam.com/Development/openfoam.git

cd openfoam

sudo sh -c "wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc"

sudo add-apt-repository http://dl.openfoam.org/ubuntu

source etc/bashrc

git clone https://github.com/OpenFOAM/ThirdParty-dev.git

cd ThirdParty*

export WM_THIRD_PARTY_DIR=$PWD

cd ..

foamSystemCheck

./Allwmake

cd ..

**Link to the header files for Eigen3**

mkdir Eigen3

cd Eigen3

wget https://gitlab.com/libeigen/eigen/-/archive/3.3.9/eigen-3.3.9.tar.gz

tar -xvf eig*

cd eig*

export Eigen3_ROOT=$PWD

cd ../..

**download preCICE and install it**

git clone https://github.com/precice/precice.git

cd precice* # Enter the preCICE source directory

cmake --list-presets

cd precice-3.1.2 # Enter the preCICE source directory

cmake --preset=production # Configure using the production preset

mkdir build 

cd build

cmake ..; make -j; sudo make install

cd ..

git clone https://github.com/precice/openfoam-adapter.git

cd openfoam-adapter

./Allwmake

cd ..

pip install pyprecice --break-system-packages

---------------------------------------

# Running the Code

**Examples**

Some example cases are provided. 

One could modify these cases to perform various types of analysis. 

Running the command 'startFOAMySees' will initialize the cases within the provided Examples folder.

Navigate to the case directory and submit 'startFOAMySees' into the terminal
(e.g. 
cd FOAMySeesExampleCases/FixedFixedBeam
startFOAMySees
)

If the required files are not in the folder, FOAMySees will tell you that it cannot be run

______________________________________
**Making your own case**

Navigate to your analysis directory
In order to run a case, you will need an OpenFOAM case folder, and an OpenSees model

_**OpenFOAM Case Folder**_

If you haven't done so, create an OpenFOAM model, or find a model with which to couple a structure. There are plenty in the OpenFOAM tutorials directory which could be modified!
The boundary conditions of the OpenFOAM will need to be modified manually, within the 0.org folder of the OpenFOAM case with which you would like to run a case. 
Configure your OpenFOAM case according to the preCICE guidelines.   https://precice.org/adapter-openfoam-config.html#fsi 
The controlDict, preciceDict, and precice-config.xml files will be automatically generated for your case depending on the settings you have chosen by the FOAMySees code.

_**OpenSees Model**_

Construct an OpenSees model geometrically near, or within the volume of, the coupled surface of the OpenFOAM model.

_**Running a Coupled Case**_

Put the OpenFOAM Case folder and OpenSees Model into a new folder alone, and run 'createFOAMySeesInputFiles' within that folder. Two files should be generated,

These files are:
**caseSetup.sh**
and
**coupledAnalysisSettings.py**
______________

Currently, the inputs to an analysis are managed through these two additional files placed in a folder along with the case files.

Modify the settings in both files, caseSetup.sh, and coupledAnalysisSettings.py
______
Run 'startFOAMySees'


---------------------------------------

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



#!/bin/bash

# unzip FOAMySees.zip 
# unzip FOAMySeesExampleCases.zip 
cd FOAMySees
FOAMySeesSrcDir=$(pwd)

echo "export FOAMySeesSrcDir=$FOAMySeesSrcDir">>~/.bashrc

chmod u+x startFOAMySees 
chmod u+x createFOAMySeesInputFiles

echo "alias startFOAMySees=$FOAMySeesSrcDir/startFOAMySees">>~/.bashrc


# # load OpenFOAM, add preCICE library to path in the right places, install all the python things you need... 

sudo apt install python3-pip
sudo apt-get install libxrender1
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

# ## math and matrices
pip3 install numpy 
pip3 install pandas
pip3 install re
pip3 install csv
pip3 install math

# ### meshes and visualization
pip3 install meshio
pip3 install matplotlib
pip3 install scipy
pip3 install vtk
pip3 install pyvista 

# ## openseespy
pip3 install openseespy

pip3 install pyprecice

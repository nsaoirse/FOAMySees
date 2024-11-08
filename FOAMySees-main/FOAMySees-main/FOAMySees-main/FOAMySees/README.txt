startFOAMySees should be available as a command after running the installation script

In order to run a case, you will need an OpenFOAM case folder, and an OpenSees model

https://precice.org/adapter-openfoam-config.html#fsi
Configure your OpenFOAM case according to the above link. 

The controlDict, preciceDict, and precice-config.xml files will be automatically generated for your case depending on the settings you have chosen.

The boundary conditions will need to be modified automatically, within the 0.org folder of the OpenFOAM case with which you would like to run a case. 


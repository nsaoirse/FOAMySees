intialize with ./StartCase

this creates a directory RunCase

HYDROUQINPUTS.json is placed into the fromUser folder <- this could be changed, not sure where you want to send this 

it then copies the fromUser folder into the RunCase directory, along with the contents of the DigitalTwinFiles folder

the RunCase folder is where the simulation happens


Allclean and Allrun bash scripts are run 

python handles the configuration of the case via configuration_file.py (this is pretty messy at the moment, but it works!)

the results are copied at the end of the Allrun script into a results folder within ./RunCase/

this folder is zipped into a zip file in the parent folder of /RunCase/

done? Not sure what else needs to be completed for the scope of this work
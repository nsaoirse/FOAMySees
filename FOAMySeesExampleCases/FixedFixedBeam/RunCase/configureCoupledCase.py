import os 
import sys
import json
import numpy as np
import json
from subprocess import Popen, DEVNULL
sys.path.append('./')
sys.path.append('../')
sys.path.append('./config_helpers')
sys.path.append('./OpenSeesSettings')


import argparse
import pickle


from coupledAnalysisSettings import *
#Program Defaults (will convert to inputs later) 
timeWindowsReused=3
iterationsReused=5

try:
	with open('FOAMySeesSavefile.pkl', 'rb') as file: 
		# Call load method to deserialze 
		args = pickle.load(file) 
		print(args) 
	with open('FOAMySees.log', 'a+') as f:
			print('loaded input arguments from a pickle file',file=f)	
except:
	with open('FOAMySees.log', 'a+') as f:
		print('nothing saved yet;',file=f)
	

UserLoadApplyFile='userLoadApply.txt'
UserLoadRemoveFile='userLoadRemove.txt' # the python functions for applying and removing loadings will be built from this set of files
copyCaseFilesTo='./'
preliminaryAnalysisFile=''# initializing this, it will be overwritten if the json file says to
prelimAnalysisExists=0 # initializing this, it will be overwritten if the json file says to
doSnappy=0 # initializing this, will be overwritten if case is 'part of HydroUQ'. I plan to make a preprocessor for openfoam which whill allow for visualization, whereupon the mesh settings will be saved to the HydroUQ json format along with additional fields to allow for easy case setup outside of hydro applications. 
#import argparse
#parser = argparse.ArgumentParser()
#parser.add_argument("jsonfile", help="Name of the json config file.", nargs='?', type=str,#
#					default="scInput.json")
#					default="FluidCouplingSurface.obj")
#try:
#	args = parser.parse_args()
#except SystemExit:#
#	print("Something is wrong! Exiting. The argument parser is telling you that you need to include something...")

if __name__=="__main__":

	parser = argparse.ArgumentParser()

	## add arguments as needed


						
	parser.add_argument("nameOfCoupledPatchOrSurfaceFile", help="Which OpenFOAM solver executable to use", type=str,
						default="interface")					

	parser.add_argument("CouplingDataProjectionMesh", help="Name of the file to load as the Coupling Data Projection Mesh", type=str,
						default="FluidCouplingSurface.obj")				

	parser.add_argument("makeCouplingDataProjectionMesh", help="Make Coupling Data Projection Mesh",  type=int,
						default=1)
						
	parser.add_argument("OpenSeesPyFile", help="Name of the OpenSeesPy model file", type=str,
						default="fromUser/OpenSeesModel.py")
		
	parser.add_argument("OpenFOAMCaseFolder", help="OpenFOAM Case Folder within RunCase",  type=str,
						default="OpenFOAMCase")
							
	parser.add_argument("OpenFOAMSolver", help="Which OpenFOAM solver executable to use",  type=str,
						default="interFoam")
		
	parser.add_argument("NPROC", help="Number of Processors for Parallel OpenFOAM Case (if 1, not parallel)",  type=int,
						default=2)

	parser.add_argument("OpenFOAMFileHandler", help="Which OpenFOAM file handler to use", type=str,
						default="collated")
												
	parser.add_argument("useExistingOpenFOAMCaseFolder", help="Use the Existing OpenFOAM Case Folder (builds FSI domain and maps fields to FSI domain from CFD domain)",  type=int,
						default=0)
		
	parser.add_argument("existingOpenFOAMCase", help="Name of the Existing OpenFOAM Case Folder", type=str,
						default="existingOpenFOAMCase")
	#					# not implemented yet, but will be useful once set up. The goal is to use this to run an openfoam case for a bit and then
	#					map the case to a FSI model which is identical in geometry or a smaller domain
						

	parser.add_argument("numOpenSeesStepsPerCouplingTimestep", help="number of OpenSees Steps to perform Per Coupling Timestep (data is time-interpolated)",  type=int,
						default=1) 
						
	parser.add_argument("numOpenFOAMStepsPerCouplingTimestep", help="number of OpenFOAM Steps to perform Per Coupling Timestep (data is time-interpolated)", type=int,
						default=1) 
						
	parser.add_argument("useHydroUQInputs", help="Is This Part of HydroUQ", type=str,
						default="No")	

	parser.add_argument("HydroUQInputs", help="HydroUQ Input json file", type=str,
						default="Input.json")					 

	args = parser.parse_args()


# Open a file and use dump() 
with open('FOAMySeesSavefile.pkl', 'wb') as file: 
	  
	# A new file will be created 
	pickle.dump(args, file) 
with open('FOAMySees.log', 'a+') as f:	
		print('saved input arguments to a pickle file',file=f)	


## load the arguments into strings like so
CouplingDataProjectionMesh = args.CouplingDataProjectionMesh
with open('FOAMySees.log', 'a+') as f:	
		print('CouplingDataProjectionMesh', args.CouplingDataProjectionMesh,file=f)	
OpenFOAMFileHandler=args.OpenFOAMFileHandler
with open('FOAMySees.log', 'a+') as f:	
		print('OpenFOAMFileHandler',args.OpenFOAMFileHandler,file=f)	
makeCouplingDataProjectionMesh=args.makeCouplingDataProjectionMesh
with open('FOAMySees.log', 'a+') as f:	
		print('makeCouplingDataProjectionMesh',args.makeCouplingDataProjectionMesh,file=f)	
nameOfCoupledPatchOrSurfaceFile=args.nameOfCoupledPatchOrSurfaceFile
with open('FOAMySees.log', 'a+') as f:	
		print('nameOfCoupledPatchOrSurfaceFile',args.nameOfCoupledPatchOrSurfaceFile,file=f)	
writeOpenFOAMHere=args.OpenFOAMCaseFolder
with open('FOAMySees.log', 'a+') as f:	
		print('writeOpenFOAMHere',args.OpenFOAMCaseFolder,file=f)	
readOpenFOAMFromHere=args.OpenFOAMCaseFolder
with open('FOAMySees.log', 'a+') as f:	
		print('readOpenFOAMFromHere',args.OpenFOAMCaseFolder,file=f)	
NPROCRUN=args.NPROC
with open('FOAMySees.log', 'a+') as f:	
		print('NPROCRUN',args.NPROC,file=f)	


openSeesPyScript= args.OpenSeesPyFile
with open('FOAMySees.log', 'a+') as f:	
		print('OpenSees Python Input Script: ', args.OpenSeesPyFile,file=f)	

OFCaseExists=args.useExistingOpenFOAMCaseFolder
# OFCaseExists="False"
with open('FOAMySees.log', 'a+') as f:	
		print('OFCaseExists',args.useExistingOpenFOAMCaseFolder,file=f)	

OpenFOAMSolver=args.OpenFOAMSolver
with open('FOAMySees.log', 'a+') as f:	
		print('OpenFOAMSolver',args.OpenFOAMSolver,file=f)	

numOpenFOAMStepsPerCouplingTimestep=args.numOpenFOAMStepsPerCouplingTimestep
with open('FOAMySees.log', 'a+') as f:	
		print('number of OpenFOAM Steps Per Coupling Timestep: ',args.numOpenFOAMStepsPerCouplingTimestep,file=f)	

numOpenSeesStepsPerCouplingTimestep=args.numOpenSeesStepsPerCouplingTimestep
with open('FOAMySees.log', 'a+') as f:	
		print('number of OpenSees Steps Per Coupling Timestep: ',args.numOpenSeesStepsPerCouplingTimestep,file=f)	

jsonfile=args.HydroUQInputs	
isPartOfHydro=args.useHydroUQInputs

runPreliminaryAnalysis="No"
bathExists=0


if isPartOfHydro=="Yes":
	with open('FOAMySees.log', 'a+') as f:	
		print("THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ//////THIS CASE IS PART OF HYDROUQ",file=f)	
	# Loads all the json variables from HydroUQ Digital Twin Output
	f = open(jsonfile)
	AllJSONVars=[]
	# returns JSON object as 
	# a dictionary
	data = json.load(f)
	for keys , values in data.items():
	#	print(keys, values) 
		if (keys=='GeneralInformation'):	
			for xx in values:
	#			print(xx,data[keys][xx])
				if xx=='NumberOfStories':
					numStories=data[keys][xx]


		if (keys=='Events'):
			for x in values[0]:
	#			print(x,values[0][x])
				AllJSONVars.append([x,values[0][x]])

	# Closing file
	f.close()
	#print('All JSON Variables ',AllJSONVars)
	doSnappy=1

	for idx, x in enumerate(AllJSONVars[:]): 
	
		if x[0]=='numProcessors':									#
			NPROC=x[1]
			NPROCRUN=x[1]
			AllJSONVars.remove(x)
	
		if x[0]=='Turbulence':									#
			Turbulence=x[1]
			AllJSONVars.remove(x)
			
		if x[0]=='FOAMVTKOUT':									#
			FOAMVTKOUT=x[1]
			AllJSONVars.remove(x)
		
		if x[0]=='FOAMVTKOUTRate':								#
			FOAMVTKOUTRate=float(x[1])
			AllJSONVars.remove(x)
							
		if x[0]=='SeesVTKOUT':									#
			SeesVTKOUT=x[1]
			AllJSONVars.remove(x)
		
		if x[0]=='SeesVTKOUTRate':								#
			SeesVTKOUTRate=float(x[1])
			AllJSONVars.remove(x)
			
		if x[0]=='writeDT':									   #
			writeDT=float(x[1])
			AllJSONVars.remove(x)

		if x[0]=='SimDuration':								   #
			endTime=float(x[1])
			AllJSONVars.remove(x)

		if x[0]=='SolutionDT':									#
			SolutionDT=float(x[1])		
			AllJSONVars.remove(x)  

		if x[0]=='AdjustTimeStep':								#
			AdjustTimeStep="false"   
			if x[1]=="Yes":
				AdjustTimeStep="true"
			AllJSONVars.remove(x)
		
		if x[0]=='ApplyGravity':								  #
			ApplyGravity=x[1]	   
			AllJSONVars.remove(x)   
			
		# if x[0]=='PreliminaryAnalysis':								  #
			# runPreliminaryAnalysis=x[1]	   
			# AllJSONVars.remove(x)   
		# if x[0]=='preliminaryAnalysisFilePath': 
			# preliminaryAnalysisFilePath=x[1].strip('.')
			# AllJSONVars.remove(x)
		
		if x[0]=='preliminaryAnalysisFile':
			preliminaryAnalysisFile=x[1]
			AllJSONVars.remove(x)
			prelimAnalysisExists=1
			
		if x[0]=='CouplingScheme':								#
			CouplingScheme=x[1]	   
			if CouplingScheme=='Implicit':
				implicit=1
			else:
				implicit=0
			AllJSONVars.remove(x)
			
		if x[0]=='bathType':									  #
			bathType=x[1]	   
			bathExists=1
			AllJSONVars.remove(x)  

		if x[0]=='bathXZData':									#
			bathXZData=x[1]	   
			AllJSONVars.remove(x)
			
		if x[0]=='bathSTL':									#
			bathSTL=x[1]	   
			AllJSONVars.remove(x)
			
		if x[0]=='bathSTLPath':									#
			bathSTLPath=x[1]	   
			AllJSONVars.remove(x)
			
		if x[0]=='couplingConvergenceTol':						#
			couplingConvergenceTol=float(x[1])	   
			AllJSONVars.remove(x)	   
			
		if x[0]=='couplingDataAccelerationMethod':				#
			couplingDataAccelerationMethod=x[1]
			AllJSONVars.remove(x)
				
		if x[0]=='couplingIterationOutputDataFrequency':		  #
			couplingIterationOutputDataFrequency=x[1]
			AllJSONVars.remove(x)
				   
		if x[0]=='cutSurfaceLocsDirsFields':					  #
			cutSurfaceLocsDirsFields=x[1]
			AllJSONVars.remove(x)			   
			
		if x[0]=='cutSurfaceOutput':							  #
			cutSurfaceOutput=x[1]
			AllJSONVars.remove(x)
		
		if x[0]=='domainSubType':								 #
			domainSubType=x[1]
			AllJSONVars.remove(x)  
			
		if x[0]=='fieldProbeLocs':								#
			fieldProbeLocs=x[1]
			AllJSONVars.remove(x)
			
		if x[0]=='fieldProbes':								   #
			fieldProbes=x[1]
			AllJSONVars.remove(x)		   
			
		if x[0]=='freeSurfProbeLocs':								#
			freeSurfProbeLocs=x[1]
			AllJSONVars.remove(x)
			
		if x[0]=='freeSurfOut':								   #
			freeSurfOut=x[1]
			AllJSONVars.remove(x)		
					
		if x[0]=='freeSurfProbes':								   #
			freeSurfProbes=x[1]
			AllJSONVars.remove(x)		
			
		if x[0]=='flumeHeight':								   #
			flumeHeight=float(x[1])
			AllJSONVars.remove(x)	 
			
		if x[0]=='flumeLength':								   #
			flumeLength=float(x[1])
			AllJSONVars.remove(x)		
			
		if x[0]=='flumeWidth':								   #
			flumeWidth=float(x[1])
			AllJSONVars.remove(x)	
			
		if x[0]=='cellSize':								   #
			cellSize=float(x[1])
			AllJSONVars.remove(x)	
		if x[0]=='flumeCellSize':								   #
			cellSize=float(x[1])
			AllJSONVars.remove(x)	
			
		if x[0]=='g':								   #
			g=[0,0,float(x[1])]
			AllJSONVars.remove(x)
					
		if x[0]=='initVelocity':								   #
			initVelocity=float(x[1])
			AllJSONVars.remove(x)				
			
		if x[0]=='initialRelaxationFactor':								   #
			initialRelaxationFactor=float(x[1])
			AllJSONVars.remove(x)   
		
		if x[0]=="interfaceSurfacePath":
			interfaceSurfacePath=x[1]	
			AllJSONVars.remove(x)  
			
		if x[0]=="interfaceSurface":
			interfaceSurface=x[1]
			AllJSONVars.remove(x)  
			
		if x[0]=='interfaceSurfaceOutput':								   #
			interfaceSurfaceOutput=x[1]
			AllJSONVars.remove(x) 
			
		if x[0]=='mapType':								   #
			if x[1] == "Nearest Neighbor":
				mapType='nearest-neighbor'
			elif x[1] == "RBF Thin Plate Splines":
				mapType='rbf-thin-plate-splines'
			AllJSONVars.remove(x)	  

		if x[0]=='maximumCouplingIterations':								   #
			maximumCouplingIterations=x[1]
			AllJSONVars.remove(x)			
			
		if x[0]=='outputDataFromCouplingIterations':								   #
			outputDataFromCouplingIterations=x[1]
			AllJSONVars.remove(x)
			
		if x[0]=='runPrelim':								   #
			if x[1]=="Yes":
				runPreliminaryAnalysis="Yes"
			else:
				runPreliminaryAnalysis="No"
			AllJSONVars.remove(x)
			
		if x[0]=='periodicWaveCelerity':								   #
			periodicWaveCelerity=float(x[1])
			AllJSONVars.remove(x)		
					
		if x[0]=='periodicWaveMagnitude':								   #
			periodicWaveMagnitude=float(x[1])
			AllJSONVars.remove(x)		
					
		if x[0]=='periodicWaveRepeatPeriod':								   #
			periodicWaveRepeatPeriod=float(x[1])
			AllJSONVars.remove(x)
			
		if x[0]=='refPressure':								   #
			refPressure=float(x[1])
			AllJSONVars.remove(x)						

		if x[0]=='stillWaterLevel':								   #
			stillWaterLevel=float(x[1])
			AllJSONVars.remove(x)		

		if x[0]=='turbIntensity':								   #
			turbIntensity=float(x[1])
			AllJSONVars.remove(x)		

		if x[0]=='turbRefLength':								   #
			turbRefLength=float(x[1])
			AllJSONVars.remove(x)		

		if x[0]=='turbReferenceVel':								   #
			turbReferenceVel=float(x[1])
			AllJSONVars.remove(x)		
			
		if x[0]=='openSeesPyScript':
			openSeesPyScript=x[1]
			AllJSONVars.remove(x)	
			
		if x[0]=='openSeesPyScriptPath':
			openSeesPyScriptPath=x[1]
			AllJSONVars.remove(x)

			
		if x[0]=='waveType':								   #
			waveType=x[1]
			if waveType=='Paddle Generated Waves':
				PADDLETH=1
			AllJSONVars.remove(x)
			
		if x[0]=='velocityFile': 
			if x[1]!="":
				velocityFile=x[1]
				VELTH=1
			AllJSONVars.remove(x)  
				
		if x[0]=='velocityFilePath': 
			if x[1]!="":
				velocityFilePath=x[1]
			AllJSONVars.remove(x)	  
					
		if x[0]=="paddleDispFilePath": 
			if x[1]!="":
				paddleDispFilePath=x[1]
			AllJSONVars.remove(x)  
			
		if x[0]=='paddleDispFile':  
			if x[1]!="":
				paddleDispFile=x[1]
			AllJSONVars.remove(x)  
				

		###################################################################
		
		if x[0]=='fileName':										#
			prelimAnalysisFile=x[1]
			AllJSONVars.remove(x)
			
		if x[0]=='filePath':										#
			prelimAnalysisFilePathPrefix=x[1]
			AllJSONVars.remove(x)
			
		######################################################### 



	x1SetField=0.
	x2SetField=flumeLength*1.1
	y1SetField=-flumeWidth/1.5
	y2SetField=flumeWidth/1.5
	z1SetField=0.
	z2SetField=stillWaterLevel

	outputRateUQForcesAndPressures=1
	VELTH=0
	PADDLETH=0
	useBranches=1
	DiffBranchesAcrossParts=0
	KDTreeClusteringToFluidMesh=1

	if prelimAnalysisExists==0:
		runPreliminaryAnalysis="No"
	else:
		runPreliminaryAnalysis="Yes"
		
writeOpenSeesHere='OpenSeesSettings'	

DomainDecomposition=NPROCRUN
if __name__=="__main__":
	doSnappyHexMesh=[doSnappy,bathExists] # 'structure'

	
	from configuration_helpers import *

	# run configuration file subfunctions
	writeOpenFOAMDecomposition(DomainDecomposition,writeOpenFOAMHere)
	
	writeOpenFOAMpreCICEDict(nameOfCoupledPatchOrSurfaceFile,writeOpenFOAMHere)
	preliminaryAnalysis=[]
	preliminaryAnalysis.append(prelimAnalysisExists)
	if prelimAnalysisExists==1:
		preliminaryAnalysis.append(preliminaryAnalysisFile)
	buildOpenSeesPreliminaryAnalysisFile(preliminaryAnalysis,writeOpenSeesHere,copyCaseFilesTo)
	buildOpenSeesModelFile(openSeesPyScript,writeOpenSeesHere,copyCaseFilesTo)


	# CONFIGURE PRECICE 
	configurePrecice(CouplingScheme,outputDataFromCouplingIterations,couplingIterationOutputDataFrequency,couplingConvergenceTol,initialRelaxationFactor,couplingDataAccelerationMethod,mapType,SolutionDT,endTime,maximumCouplingIterations,timeWindowsReused,iterationsReused)
		
	# Moving the analysis files to the run directory
	Popen('echo " Moving the analysis files to the run directory"', shell=True, stdout=DEVNULL).wait()
	Popen('cp -r '+copyCaseFilesTo+'* .', shell=True, stdout=DEVNULL).wait()
	# copying the constructed OpenSees model file to the place it needs to be
	Popen('pwd', shell=True, stdout=DEVNULL).wait()
	Popen('cp -r '+copyCaseFilesTo+openSeesPyScript+' '+writeOpenSeesHere+'/OpenSeesModel.py', shell=True, stdout=DEVNULL).wait()

	# copying the surface file to the place it needs to be
	Popen('mkdir '+writeOpenFOAMHere+'/constant/triSurface', shell=True, stdout=DEVNULL).wait()

	Popen('cp -r '+copyCaseFilesTo+interfaceSurface+' '+writeOpenFOAMHere+'/constant/triSurface/'+nameOfCoupledPatchOrSurfaceFile+'.stl', shell=True, stdout=DEVNULL).wait()

		# making a list for pressure sensor locations
		
	pLocations=[]

	bestGuess=[0,0,0]
		# Popen('mv fromUserDefaults userInputs').wait()
	allFunctionObjects=['''			preCICE_Adapter
	{
	   type preciceAdapterFunctionObject;
		libs ("libpreciceAdapterFunctionObject.so");
	}
	''']
	
	flag=0
	if isPartOfHydro=="Yes":	

	
		if (OFCaseExists==0) or (OFCaseExists=="False") or (OFCaseExists==False):
			if waveType=="Periodic Waves":			
				waveProperties=[periodicWaveRepeatPeriod, periodicWaveCelerity, periodicWaveMagnitude]	
				domainSubType="WAVES"

			if waveType=="No Waves":
				flag=VELTH
				if VELTH==0:
					waveProperties=initVelocity
				elif VELTH==1:
					waveProperties=velocityFile
				
			if waveType=="Paddle Generated Waves":
				flag=PADDLETH
				waveProperties=paddleDispFile


			buildDomain(domainSubType,readOpenFOAMFromHere,writeOpenFOAMHere)
		
			buildBlockMesh(waveType,flumeLength,flumeWidth,flumeHeight,stillWaterLevel,cellSize,writeOpenFOAMHere)

			buildInletProperties(waveType,waveProperties,flag,writeOpenFOAMHere)

			if bathExists==1:
				if bathType=="Point List":
					secondaryInput=[flumeWidth,bathXZData]
				elif bathType=="STL File":
					secondaryInput=bathSTL
				buildBathymetry(bathType,secondaryInput,writeOpenFOAMHere)
		

			try:
				TurbulenceProperties=[Turbulence,turbRefLength,turbReferenceVel,turbIntensity]
			except:
				TurbulenceProperties=[Turbulence]
			
			buildInitialConditions(flumeWidth, refPressure, initVelocity, stillWaterLevel, TurbulenceProperties, writeOpenFOAMHere)
		
		
			if 'initPressure' in locals():
				initPressureDict=["Yes", initPressure]
			else: 
				initPressureDict=["No", refPressure]
		
			if 'initVelocity' in locals():
				initVelocityDict=["Yes", initVelocity]
			else:
				initVelocityDict=["No", 0.]
		
			buildSetFields(x1SetField,x2SetField,y1SetField,y2SetField,z1SetField,z2SetField,refPressure,initVelocityDict,initPressureDict,writeOpenFOAMHere)
					


		writeControlDict(OpenFOAMSolver,startOFSimAt,endTime,SolutionDT,writeDT,writeOpenFOAMHere,allFunctionObjects,AdjustTimeStep,OpenFOAMFileHandler)
	time.sleep(1)
	
	
	writeUserLoadRoutines(copyCaseFilesTo,UserLoadApplyFile,UserLoadRemoveFile)
	
	copyUserInputsToCase(copyCaseFilesTo)
#	write0Folder(OpenFOAMSolver,OFCaseExists, nameOfCoupledPatchOrSurfaceFile,writeOpenFOAMHere)
	ifsnappy=''''''
	
	if doSnappyHexMesh[0]==1:
		ifsnappy='''

		echo surfaceFeatureExtract extracting...
		surfaceFeatureExtract > log.surfFeatExt
		echo doing snappyHexMesh 
		snappyHexMesh -overwrite -fileHandler uncollated > log.sHM
		#echo decomposePar setting up parallel case...
		#decomposePar -force -fileHandler uncollated -copyZero > log.decomp_sHM

		#echo snappyHex meshing flume floor and/or structure planes...
		#mpirun -np $NPROC snappyHexMesh -parallel -overwrite -fileHandler uncollated > log.sHM

		#echo checking mesh quality...
		#mpirun -np $NPROC checkMesh -parallel > log.checkMesh

		#echo reconstructParMesh rebuilding mesh...
		#reconstructParMesh -constant -mergeTol 1e-06 > log.reconMesh_sHM

		#echo reconstructPar rebuilding fields...
		#reconstructPar > log.recon_sHM

		#echo eliminate meshing time step and processor directories...
		#rm -r processor*
		'''
	with open('FOAMySees.log', 'a+') as f:	
		print('Building OpenFOAM Case',file=f)	   
	Popen('''
		cd '''+writeOpenFOAMHere+''' 
		echo blockMesh meshing...
		blockMesh > log.blockMesh   
		
		''', shell=True).wait()
	with open('FOAMySees.log', 'a+') as f:	
		print('Base of CFD mesh built')
	if bathExists==1:
		with open('FOAMySees.log', 'a+') as f:	
			print('Building bathymetry',file=f)	
		buildSnappyHexMeshAndSurfaceFeatureExtractDictionariesBathymetry(bathExists,writeOpenFOAMHere)
		Popen('''cd '''+writeOpenFOAMHere+ifsnappy, shell=True).wait()
		with open('FOAMySees.log', 'a+') as f:	
			print('Bathymetry Built',file=f)	


	if Turbulence=="No":
		ifnotTurbulence='''
		rm -rf 0/epsilon*
		rm -rf 0/nut*
		rm -rf 0/omega*
		rm -rf 0/k*'''
	else:
		ifnotTurbulence=''' '''
	
	with open('FOAMySees.log', 'a+') as f:	
		print('Preparing the 0 time folder, Meshing the structure, Setting Fields',file=f)	
 
	buildSnappyHexMeshAndSurfaceFeatureExtractDictionariesStructure(nameOfCoupledPatchOrSurfaceFile,writeOpenFOAMHere)




	Popen('''cd '''+writeOpenFOAMHere+''' 
		echo "  Preparing the mesh..."

		echo preparing 0 folder...
		if [ -d '0' ]; then
		rm -r 0
		fi
		cp -r 0.org 0
		'''+ifnotTurbulence+'''

		'''+ifsnappy+'''
		echo Setting the fields...
		setFields > log.setFields

		echo decomposePar setting up parallel case...

		echo Mesh built, ICs set

cd ..

setFields -case '''+writeOpenFOAMHere+''' > setFields.log 2>&1 &

''', shell=True).wait()  
	with open('FOAMySees.log', 'a+') as f:	
		print('Structure Meshed, writing OpenFOAM Case Settings and functionObjects',file=f)	
	resultantForceCenterOfRotation=findResultantCenterOfRotation(OFCaseExists,nameOfCoupledPatchOrSurfaceFile,CouplingDataProjectionMesh,makeCouplingDataProjectionMesh,bestGuess,writeOpenFOAMHere)
	if isPartOfHydro=="Yes":	

		cutSurfaceOutputList=[cutSurfaceOutput,cutSurfaceLocsDirsFields]
		freeSurfProbesList=[freeSurfProbes,freeSurfProbeLocs]
		fieldProbesList=[fieldProbes,fieldProbeLocs]
		allFunctionObjects=makeFuctionObjectsFromInputs(OFCaseExists,CouplingDataProjectionMesh,resultantForceCenterOfRotation,numStories,freeSurfOut,cutSurfaceOutputList,interfaceSurfaceOutput,freeSurfProbesList,fieldProbesList,outputRateUQForcesAndPressures, writeOpenFOAMHere)

	writeControlDict(OpenFOAMSolver,startOFSimAt,endTime,SolutionDT,writeDT,writeOpenFOAMHere,allFunctionObjects,AdjustTimeStep,OpenFOAMFileHandler)
	
	with open('FOAMySees.log', 'a+') as f:	
		print('				   %%%%%%%%%%%%% <<<<<<<<<<<<<<<<<<FOAMySEES CONFIGURED>>>>>>>>>>>>>>>>>> %%%%%%%%%%%%%				   ',file=f)	

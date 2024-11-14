from subprocess import Popen, DEVNULL
def findResultantCenterOfRotation(fluidExists,nameOfCoupledPatchOrSurfaceFile,CouplingDataProjectionMesh,makeCouplingDataProjectionMesh,bestGuess,writeHere):
	if makeCouplingDataProjectionMesh==1:
		Popen("surfaceMeshExtract -case "+writeHere+" -patches "+nameOfCoupledPatchOrSurfaceFile+" -latestTime "+CouplingDataProjectionMesh, shell=True, stdout=DEVNULL).wait()
		
	Popen('surfaceInertia '+writeHere+'/'+CouplingDataProjectionMesh, shell=True, stdout=DEVNULL).wait()
	
	Popen('cp '+writeHere+'/'+CouplingDataProjectionMesh+' ..', shell=True, stdout=DEVNULL).wait()
	counter=0
	try:
		with open("axes.obj", "r") as f:
			for line in f:
				counter+=1
				if counter==1:
					resultantForceCenterOfRotation=line.strip('\n') #this location needs to be calculated somehow from the input surface file, or should be specified in the Hydro UQ inputs...
					resultantForceCenterOfRotation=resultantForceCenterOfRotation.strip('v')
					resultantForceCenterOfRotation=resultantForceCenterOfRotation.split(' ')
					resultantForceCenterOfRotation=resultantForceCenterOfRotation[1:]
					print(resultantForceCenterOfRotation)
	except: 
		resultantForceCenterOfRotation=bestGuess #this location needs to be calculated somehow from the input surface file, or should be specified in the Hydro UQ inputs...				
	return resultantForceCenterOfRotation

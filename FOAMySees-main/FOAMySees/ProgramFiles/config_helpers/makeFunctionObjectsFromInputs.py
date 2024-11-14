from findResultantCenterOfRotation import *
def makeFuctionObjectsFromInputs(fluidExists,CouplingDataProjectionMesh,resultantForceCenterOfRotation,numStories,freeSurfOut,cutSurfaceOutputList,interfaceSurfaceOutput,freeSurfProbesList,fieldProbesList,outputRateUQForcesAndPressures, writeHere):

	print('Making all function objects for OpenFOAM')
	allFunctionObjects=''''''

	if freeSurfOut=='Yes':
		allFunctionObjects+='''
		freeSurfaceVTK
	   {   
		   type			surfaces;
		   functionObjectLibs
		   (   
			   "libsampling.so" 
		   );  
		   outputControl   outputTime;
		   outputInterval  1;  
		   surfaceFormat  vtk;
		   fields
		   (   
			   alpha.water
		   );  
		   surfaces
		   (   
			   freeSurface
			   {   
				   type		isoSurfaceCell;
				   isoField	alpha.water;
				   isoValue	0.5;
				   interpolate false;
				   regularise  false;
			   }   
			   
		   );  
		   interpolationScheme cell;
	   }
	   '''
	   
	count=0   
	   # OpenFOAM Cut Surface Output
	if cutSurfaceOutputList[0]=='Yes':
		cutSurfaceLocsDirsFields=cutSurfaceOutputList[1]
		for cutSurface in cutSurfaceLocsDirsFields:
			fieldsCurr=''''''
			for xx in cutSurface[7].split(','):
				fieldsCurr+='''{}
					   '''.format(xx)
			allFunctionObjects+=cutSurface[6]+'''
			{   
			   type			surfaces;
			   functionObjectLibs
			   (   
				   "libsampling.so" 
			   );  
			   outputControl   outputTime;
			   outputInterval  1;  
			   surfaceFormat  vtk;
			   fields
			   (   
				   '''+fieldsCurr+'''
			   );  
			   surfaces
			   (   
				interpolatedSurface
				{
					// Cutingplane using iso surface
					type			cuttingPlane;
					planeType	   pointAndNormal;
					pointAndNormalDict
					{'''+'''
						basePoint	   ({} {} {});
						normalVector	({} {} {});'''.format(cutSurface[0],cutSurface[1],cutSurface[2],cutSurface[3],cutSurface[4],cutSurface[5])+'''
						}
					interpolate	 true;	   
					}	
			   );  
			   interpolationScheme cell;
		   }
		   '''
		count+=1
	   
	count=0
	   # OpenFOAM Cut Surface Output
	if interfaceSurfaceOutput=='Yes':

		allFunctionObjects+='''structureInterface
		{   
		   type			surfaces;
		   functionObjectLibs
		   (   
			   "libsampling.so" 
		   );  
		   outputControl   outputTime;
		   outputInterval  1;  
		   surfaceFormat  vtk;
		   fields
		   (   
			   '''+fieldsCurr+'''
		   );  
		   surfaces
		   (   
			interface
			{
				type			patch;
				patches	   (interface);	
				}	
		   );  
		   interpolationScheme cell;
	   }
	   '''

	# Free Surface Probes
	probeLocs=''''''
	if freeSurfProbesList[0]=='Yes':
		freeSurfProbeLocs=freeSurfProbesList[1]
		for probeloc in freeSurfProbeLocs:

			allFunctionObjects+='''
			{}'''.format(probeloc[3])+'''
			{
				type			interfaceHeight;
				libs			("libfieldFunctionObjects.so");
				writeControl	timeStep; 
				writeInterval   1; 
				locations
				('''+'''({} {} {})'''.format(probeloc[0],probeloc[1],probeloc[2])+'''
				);
				alpha		   alpha.water;
			}
		'''	

	# Field Probes
	pLocations=[]
	probeLocs=''''''
	if fieldProbesList[0]=='Yes':
		fieldProbeLocs=fieldProbesList[1]
		for probeloc in fieldProbeLocs:

			if probeloc[4]==('u') or probeloc[4]==('U') or probeloc[4]==('V')  or probeloc[4]==('Velocity'):
				allFunctionObjects+='''
					{}'''.format(probeloc[3])+'''
				{ 
					type				probes; 
					libs				("libsampling.so"); 
					writeControl		timeStep; 
					writeInterval		1; 
					probeLocations 
					('''+'''({} {} {})'''.format(probeloc[0],probeloc[1],probeloc[2])+'''
					); 
					fields 
					( 
					U
					); 	}
				'''
			if probeloc[4]==('p') or probeloc[4]==('P') or probeloc[4]==('pressure')  or probeloc[4]==('Pressure'):
				allFunctionObjects+='''
					{}'''.format(probeloc[3])+'''
				{ 
					type				probes; 
					libs				("libsampling.so"); 
					writeControl		timeStep; 
					writeInterval		1; 
					probeLocations 
					('''+'''({} {} {})'''.format(probeloc[0],probeloc[1],probeloc[2])+'''
					); 
					fields 
					( 
					p
					); 	}
				'''
				pLocations.append([probeloc[0],probeloc[1],probeloc[2]])

	# Resultant Forces


	allFunctionObjects+='''
	interface
		{
		type		  forces;
		libs		  ("libforces.so");
		writeControl  timeStep;
		timeInterval  1;
		log		   yes;
		patches	   (interface);
		rho		   rhoInf;	 // Indicates incompressible
		log		   true;
		rhoInf		1000;		  // Redundant for incompressible'''+'''
		CofR		  ({} {} {})'''.format(resultantForceCenterOfRotation[0],resultantForceCenterOfRotation[1],resultantForceCenterOfRotation[2])+''';	// Rotation around centroid of group
		pitchAxis	 (0 1 0);
		}
	'''

	allFunctionObjects+='''
		#includeFunc  pressureSamplingPoints 
		#includeFunc  baseForces 
		#includeFunc  storyForces 
	'''

	pressureSamplingPoints='''
	/*--------------------------------*- C++ -*----------------------------------*\
	  =========				 |
	  \\	  /  F ield		 | OpenFOAM: The Open Source CFD Toolbox
	   \\	/   O peration	 | Website:  https://openfoam.org
		\\  /	A nd		   | Version:  10
		 \\/	 M anipulation  |
	\*----------------------------------------------------------------------------

	Description
		Writes out values of fields from cells nearest to specified locations.

	\*---------------------------------------------------------------------------*/

	type			probes;
	libs			("libsampling.so");
	writeControl	timeStep;'''+'''
	writeInterval 	{};'''.format(outputRateUQForcesAndPressures)+'''

	fields 		(p);

	probeLocations
	(
	'''
	for x in pLocations:
		pressureSamplingPoints+='''({} {} {})
		'''.format(x[0],x[1],x[2])

	pressureSamplingPoints+=''');

	// ************************************************************************* //

	'''

	with open(writeHere+'/system/pressureSamplingPoints','w') as f:
		f.seek(0)
		for x in pressureSamplingPoints:
			for line in x:
				f.write(line)
				f.truncate()

	baseForces='''
	/*--------------------------------*- C++ -*----------------------------------*\
	  =========				 |
	  \\	  /  F ield		 | OpenFOAM: The Open Source CFD Toolbox
	   \\	/   O peration	 | Website:  https://openfoam.org
		\\  /	A nd		   | Version:  10
		 \\/	 M anipulation  |
	\*---------------------------------------------------------------------------*/

	type			forces;
	libs			("libforces.so");
	patches 	(interface);
	writeControl 	timeStep;'''+'''
	writeInterval 	{};'''.format(outputRateUQForcesAndPressures)+'''
	porosity	 	no;
	log		   	yes;
	pRef	   	0.0;
	rho			rhoInf;	
	log	   	yes;		 
	rhoInf 		1000.0000;'''+'''
	CofR 		({} {} {})'''.format(resultantForceCenterOfRotation[0],resultantForceCenterOfRotation[1],resultantForceCenterOfRotation[2])+''';

	// ************************************************************************* //
	'''

	with open(writeHere+'/system/baseForces','w') as f:
		f.seek(0)
		for x in baseForces:
			for line in x:
				f.write(line)
				f.truncate()


	storyForces='''
	/*--------------------------------*- C++ -*----------------------------------*\
	  =========				 |
	  \\	  /  F ield		 | OpenFOAM: The Open Source CFD Toolbox
	   \\	/   O peration	 | Website:  https://openfoam.org
		\\  /	A nd		   | Version:  10
		 \\/	 M anipulation  |
	\*---------------------------------------------------------------------------*/

	type			forces;
	libs			("libforces.so");
	patches 	(interface);
	writeControl 	timeStep;'''+'''
	writeInterval 	{};'''.format(outputRateUQForcesAndPressures)+'''
	porosity	 	no;
	log		   	yes;
	pRef	   	0.0;
	rho			rhoInf;	
	log	   	yes;		 
	rhoInf 		1000.0000;'''+'''
	CofR 		({} {} {})'''.format(resultantForceCenterOfRotation[0],resultantForceCenterOfRotation[1],resultantForceCenterOfRotation[2])+''';

	binData
	{'''+'''
		nBin 	{};'''.format(numStories)+'''
		direction 	(0.0000 0.0000 1.0000);
		cumulative	no;
	}
	// ************************************************************************* //
	'''

	with open(writeHere+'/system/storyForces','w') as f:
		f.seek(0)
		for x in storyForces:
			for line in x:
				f.write(line)
				f.truncate()
	return allFunctionObjects

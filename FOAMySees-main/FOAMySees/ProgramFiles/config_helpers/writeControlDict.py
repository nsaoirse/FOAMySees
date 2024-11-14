import os
def writeControlDict(OpenFOAMSolver,startOFSimAt,endTime,SolutionDT,writeDT,writeHere,allFunctionObjects='''''',AdjustTimeStep="no",fileHandler="collated"):
	if os.path.exists('functionObjects'):
		with open('functionObjects') as f:
			lines=f.read()
			allFunctionObjects+=lines
	
	print('writing OpenFOAM controlDict')
	controlDict=['''/*--------------------------------*- C++ -*----------------------------------*\
| =========											    ____/_________\____	 _.*_*.			    |
| \\	  /	  F ield          |   |  S tructural     ||__|/\|___|/\|__||	  \ \ \\.		    |
|  \\	 /    O peration      |___|  E ngineering &  ||__|/\|___|/\|__||	   | | | \._		|
|   \\  /     A nd                |  E arthquake     ||__|/\|___|/\|__||	  _/_/_/ | .\.__... |
|	 \\/      M anipulation   |___|  S imulation     ||__|/\|___|/\|__||   __/, / _ \___...	    |
|____________________________________________________||  |/\| | |/\|  ||__/,_/__,_____/...______|
	\*---------------------------------------------------------------------------*/
	FoamFile{
		version	 2.0;
		format	  ascii;
		class	   dictionary;
		location	"system";
		object	  controlDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	libs
	(
		"libOpenFOAM.so"
		"libforces.so"
		"libOpenFOAM.so"
	);
	''','''
	application	 {};'''.format(OpenFOAMSolver),'''

	startFrom	   latestTime;
	''','''
	startTime	   {};'''.format(startOFSimAt),'''

	stopAt		  endTime;

	endTime		 {};'''.format(endTime+startOFSimAt),'''

	deltaT		  {};'''.format(SolutionDT),'''

	writeControl	adjustable;

	writeInterval   {};'''.format(writeDT),'''

	writeFormat	 ascii;

	writePrecision  6;

	writeCompression off;

	timeFormat	  general;

	timePrecision   12;

	runTimeModifiable {}'''.format(AdjustTimeStep),''';
	adjustTimeStep {}'''.format(AdjustTimeStep),''';

	DebugSwitches
	{
	  level	2;
	  lduMatrix 2;
	  libs 2;
	}
	OptimisationSwitches
	{''','''
	fileHandler {}'''.format(fileHandler),''';
	maxThreadFileBufferSize 5e9; // v1712 default is 0;
	maxMasterFileBufferSize 5e9;
	}


	maxCo		   0.5;
	maxAlphaCo	  0.5;''','''
	maxDeltaT {};'''.format(SolutionDT),'''
	functions 
	{
				preCICE_Adapter
		{
		   type preciceAdapterFunctionObject;
			libs ("libpreciceAdapterFunctionObject.so");
		}
		''',
		allFunctionObjects,
		'''
	}
	// ************************************************************************* //''']


	with open(writeHere+'/system/controlDict','w') as f:
		f.seek(0)
		for x in controlDict:
			for line in x:
				f.write(line)
				f.truncate()
				

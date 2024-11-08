import os
from subprocess import Popen, DEVNULL
def makeVelocityInletTHBC(VELTH,secondaryInput,writeHere):
	print(os.system('pwd'))
	print('Making Velocity Inlet Time History BCs')
	if VELTH==0:
		initVelocity=secondaryInput
		fixedStartPatch='''
		fixedStart
			{
				type			fixedValue;
				value uniform ''','''({} 0 0);'''.format(initVelocity)+'''
			}		
		'''			
	elif VELTH==1:
		velocityFile=secondaryInput
		import csv
		with open(velocityFile,'r') as dest_f:
			data_iter = csv.reader(dest_f,
								   delimiter = ',',
								   quotechar = '"')
			data = [data for data in data_iter]
		velTimeData = np.asarray(data, dtype = np.float32)

		velTimeList=[]
		for y in velTimeData:
			velTimeList.append('''({} '''.format(y[0])+'''({} 0 0) )
				'''.format(y[1]))
			lastTime=y[0]
			lastVel=y[1]
		velTimeList.append('''({} '''.format(lastTime*10)+'''({} 0 0) )
				'''.format(lastVel))
		fixedStartPatch='''
							fixedStart
			{
				type			uniformFixedValue;
				uniformValue table
				(
				'''+velTimeList+'''
				);
				value		$internalField;
			}		
		'''
	UFILE=['''/*--------------------------------*- C++ -*----------------------------------*\
| =========                                               ____/_________\____     _.*_*.             |
| \\      /      F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \\.           |
|  \\    /       O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | | \._        |
|   \\  /        A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\.__... |
|    \\/         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___...     |
|_________________________________________________________||  |/\| | |/\|  ||__/,_/__,_____/...______|
	\*---------------------------------------------------------------------------*/
	FoamFile
	{
		version	 2.0;
		format	  ascii;
		class	   volVectorField;
		location	"0";
		object	  U;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	#include	  "ICfiles/initialConditions"


	dimensions	[0 1 -1 0 0 0 0];
	internalField uniform (0 0 0);

	calculatedFlowRate #eval "$Wflume*$SWL*$initialVel";

	boundaryField
	{
	 ''',fixedStartPatch,'''
		fixedEnd
		{
		type		inletOutlet;
		inletValue	$internalField;
		value		$internalField;
		}
		fixedBottom
		{
			type			noSlip;
		}   
		flumeFloor
		{
			type			noSlip;
		}
		fixedRight
		{
			type			noSlip;
		}
		fixedLeft
		{
			type			noSlip;
		}
		interface
		{
		   // type			noSlip;
			type			movingWallVelocity;
			value		  uniform (0 0 0);
		}
		fixedAtmosphere
		{
			type			pressureInletOutletVelocity;
			value		   uniform (0 0 0);
		}
		fixedStartTop
		{
			type			pressureInletOutletVelocity;
			value		   uniform (0 0 0);
		}
	}


	// ************************************************************************* //''']
	with open('whatisthis.log','w+') as f:
		print(os.getcwd(),file=f)
	try:
		with open(writeHere+'/0.org/U','w') as f:
			f.seek(0)
			for x in UFILE:
				for line in x:
					f.write(line)
					f.truncate()
	except: 
		Popen('mkdir '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		with open(writeHere+'/0.org/U','w') as f:
			f.seek(0)
			for x in UFILE:
				for line in x:
					f.write(line)
					f.truncate()				



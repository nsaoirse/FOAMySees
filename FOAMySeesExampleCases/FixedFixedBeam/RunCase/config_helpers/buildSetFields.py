def buildSetFields(x1SetField,x2SetField,y1SetField,y2SetField,z1SetField,z2SetField,refPressure,initVelocityDict,initPressureDict,writeHere):

	print('Building OpenFOAM setFieldsDict')
	print("x1SetField,x2SetField,y1SetField,y2SetField,z1SetField,z2SetField,refPressure,initVelocityDict,initPressureDict")
	print(x1SetField,x2SetField,y1SetField,y2SetField,z1SetField,z2SetField,refPressure,initVelocityDict,initPressureDict)
	if initVelocityDict[0]=="Yes":
		initVelocity=initVelocityDict[1]
	else: 
		initVelocity=0

	if initPressureDict[0]=="Yes":
		initPressure=initPressureDict[1]
	else: 
		initPressure=refPressure
	
	setFieldsDict=['''
	FoamFile
	{
		version	 2.0;
		format	  ascii;
		class	   dictionary;
		location	"system";
		object	  setFieldsDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	#include	  "../0.org/ICfiles/initialConditions"

	defaultFieldValues
	(
		volScalarFieldValue alpha.water 0
		volScalarFieldValue U 0	
	);


	regions
	(
		boxToCell
		{
			box (''','''{} {} {}'''.format(x1SetField,y1SetField,z1SetField),''') (''','''{} {} {}'''.format(x2SetField,y2SetField,z2SetField),''');

			fieldValues
			(
				volScalarFieldValue alpha.water 1
				volVectorFieldValue U ({} 0 0)'''.format(initVelocity),'''
			);
		}
	);
	''']

	with open(writeHere+'/system/setFieldsDict','w') as f:
		f.seek(0)
		for x in setFieldsDict:
			for line in x:
				f.write(line)


def buildBlockMesh(waveType,flumeLength,flumeWidth,flumeHeight,stillWaterLevel,cellSize,writeHere="OpenFOAMCase"):
	print('Building BlockMesh')
	print("waveType,flumeLength,flumeWidth,flumeHeight,stillWaterLevel,cellSize,")
	print(waveType,flumeLength,flumeWidth,flumeHeight,stillWaterLevel,cellSize)
	
	
	X=flumeLength
	Y=flumeWidth
	Z=flumeHeight

	xBlockCt=int(X//cellSize)
	yBlockCt=int(Y//cellSize)
	zBlockCt=int(Z//cellSize)
	zBlockCtSWL=int(stillWaterLevel//cellSize)

	LCOMP=X//4		
	########## BLOCK MESH EDIT ################

	if waveType=="Paddle Generated Waves": 
		blockMeshDict=['''
	FoamFile
	{
		version		 2.0;
		format		  ascii;
		class		   dictionary;
		object		  blockMeshDict;
	}

	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	convertToMeters 1;

	// User-defined parameters
	stroke 4.0; // wavemaker piston stroke''','''
	SWL {}; // still water level'''.format(stillWaterLevel),'''
	Wflume {}; // actual flume width'''.format(Y),'''
	Lflume {}; // truncated flume length'''.format(X),'''
	Lcomp {}; // compressible mesh region length'''.format(LCOMP),'''
	zK ''','''{};'''.format(Z),'''

	// Vertex coordinates
	xI #calc "-$stroke/2.0"; // initial paddle position
	xJ #calc "$xI+$Lcomp"; // compressible mesh region end
	xK $Lflume; // flume end
	yI #calc "-$Wflume/2.0"; // right flume wall
	yJ #calc "$Wflume/2.0"; // left flume wall
	zI 0.0; // flume bottom
	zJ ''','''{};'''.format(stillWaterLevel),''' // still water level


	vertices
	(
		($xI $yI $zI) // 0
		($xI $yI $zJ) // 1
		($xI $yI $zK) // 2
		($xJ $yI $zI) // 3
		($xJ $yI $zJ) // 4
		($xJ $yI $zK) // 5
		($xK $yI $zI) // 6
		($xK $yI $zJ) // 7
		($xK $yI $zK) // 8
		($xI $yJ $zI) // 9
		($xI $yJ $zJ) // 10
		($xI $yJ $zK) // 11
		($xJ $yJ $zI) // 12
		($xJ $yJ $zJ) // 13
		($xJ $yJ $zK) // 14
		($xK $yJ $zI) // 15
		($xK $yJ $zJ) // 16
		($xK $yJ $zK) // 17
	);

	blocks		  
	(''','''
		hex (0 3 12 9  1 4 13 10) (''','''{} {} {}'''.format(LCOMP//cellSize,Y//cellSize,stillWaterLevel//cellSize),''')	simpleGrading (1 1 0.5) // compressible water-filled block
		hex (1 4 13 10 2 5 14 11) (''','''{} {} {}'''.format(LCOMP//cellSize,Y//cellSize,(Z-stillWaterLevel)//cellSize),''')	simpleGrading (1 1 2) // compressible air-filled block
		hex (3 6 15 12 4 7 16 13) (''','''{} {} {}'''.format((X-LCOMP)//cellSize,Y//cellSize,stillWaterLevel//cellSize),''')   simpleGrading (1 1 0.5) // fixed water-filled block
		hex (4 7 16 13 5 8 17 14) (''','''{} {} {}'''.format((X-LCOMP)//cellSize,Y//cellSize,(Z-stillWaterLevel)//cellSize),''')  simpleGrading (1 1 2) // fixed air-filled block''','''
	);

	edges		   
	(
	);

	boundary
	(
		paddle
		{
			type wall;
			faces
			(
				(0 1 10 9) // compressible water-filled block DM...out of the box
				(1 2 11 10) // compressi1ble air-filled block
			);
		}
		comprBottom
		{
			type wall;
			faces
			(
				(0 9 12 3) // compressible water-filled block
			);
		}
		comprRight
		{
			type wall;
			faces
			(
				(0 3 4 1) // compressible water-filled block
				(1 4 5 2) // compressible air-filled block
			);
		}
		comprLeft
		{
			type wall;
			faces
			(
				(9  10 13 12) // compressible water-filled block
				(10 11 14 13) // compressible air-filled block
			);
		}
		comprAtmosphere
		{
			type patch;
			faces
			(
				(2 5 14 11) // compressible air-filled block
			);
		}
		fixedEnd
		{
			type wall;
			faces
			(
				(6 15 16 7) // fixed water-filled block
				(7 16 17 8) // fixed air-filled block
			);
		}
		fixedBottom
		{
			type wall;
			faces
			(
				(3 12 15 6) // fixed water-filled block
			);
		}
		fixedRight
		{
			type wall;
			faces
			(
				(3 6 7 4) // fixed water-filled block
				(4 7 8 5) // fixed air-filled block
			);
		}
		fixedLeft
		{
			type wall;
			faces
			(
				(12 13 16 15) // fixed water-filled block
				(13 14 17 16) // fixed air-filled block
			);
		}
		fixedAtmosphere
		{
			type patch;
			faces
			(
				(5 8 17 14) // fixed air-filled block
			);
		}
	);

	mergePatchPairs
	(
	);
	// ************************************************************************* //'''
	]
	elif waveType=="No Waves": 
		blockMeshDict=['''
	FoamFile
	{
		version		 2.0;
		format		  ascii;
		class		   dictionary;
		object		  blockMeshDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	convertToMeters 1;
	vertices
	(''','''
	   (0.0 -{} 0.0) // 0
		(0.0 {} 0.0) // 1
		(0.0 {} {}) // 2
		(0.0 -{} {}) // 3
		({} -{} 0.0) // 4
		({} {} 0.0) // 5
		({} {} {}) // 6
		({} -{} {}) // 7
	   (0.0 -{} {}) // 8
		(0.0 {} {}) // 9
		(0.0 {} {}) // 10
		(0.0 -{} {}) // 11
		({} -{} {}) // 12
		({} {} {}) // 13
		({} {} {}) // 14
		({} -{} {}) // 15	
	'''.format(Y/2,Y/2,Y/2,stillWaterLevel,Y/2,stillWaterLevel,X,Y/2,X,Y/2,X,Y/2,stillWaterLevel,X,Y/2,stillWaterLevel,Y/2,stillWaterLevel,Y/2,stillWaterLevel,Y/2,Z,Y/2,Z,X,Y/2,stillWaterLevel,X,Y/2,stillWaterLevel,X,Y/2,Z,X,Y/2,Z),''');
	blocks		  
	(
		hex (0 4 5 1 3 7 6 2) (''','''{} {} {}'''.format(xBlockCt,yBlockCt,zBlockCtSWL),''')  
		simpleGrading
	   (1 1 0.5)
		hex (8 12 13 9 11 15 14 10) (''','''{} {} {}'''.format(xBlockCt,yBlockCt,zBlockCt-zBlockCtSWL),''')  
		simpleGrading
	   (1 1 2)
	);
	edges		   
	(
	);

	boundary
	(
		fixedStart
		{
			type patch;
			faces
			(
				(3 2 1 0) // fixed air-filled block
			);
		}	
		fixedStartTop
		{
			type wall;
			faces
			(
				 (11 10 9 8) // fixed air-filled block
			);
		}
		fixedEnd
		{
			type patch;
			faces
			(
				(7 6 5 4) // fixed water-filled block
				(15 14 13 12) // fixed water-filled block
			);
		}
		fixedBottom
		{
			type wall;
			faces
			(
				(0 1 5 4) // fixed water-filled block
			);
		}
		fixedRight
		{
			type wall;
			faces
			(
				(0 4 7 3) // fixed air-filled block
				(8 12 15 11) // fixed air-filled block
			);
		}
		fixedLeft
		{
			type wall;
			faces
			(
				(1 2 6 5) // fixed air-filled block
				(9 10 14 13) // fixed air-filled block
			);
		}
		fixedAtmosphere
		{
			type patch;
			faces
			(
				(14 11 15 10) // fixed air-filled block

			);
		}
			defaultFaces1
		{
			type patch;
			faces
			(
			(2 3 7 6) // fixed air-filled block

			);
		}
				defaultFaces2
		{
			type patch;
			faces
			(
			(8 9 12 13) // fixed air-filled block

			);
		}
	);
	mergePatchPairs
	(
	(defaultFaces1 defaultFaces2)
	);
	// ************************************************************************* //
	''']
	elif waveType=="Periodic Waves": 
		blockMeshDict=['''
	FoamFile
	{
		version		 2.0;
		format		  ascii;
		class		   dictionary;
		object		  blockMeshDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	convertToMeters 1;
	vertices
	(''','''
	   (0.0 -{} 0.0) // 0
		(0.0 {} 0.0) // 1
		(0.0 {} {}) // 2
		(0.0 -{} {}) // 3
		({} -{} 0.0) // 4
		({} {} 0.0) // 5
		({} {} {}) // 6
		({} -{} {}) // 7
	'''.format(Y/2,Y/2,Y/2,Z,Y/2,Z,X,Y/2,X,Y/2,X,Y/2,Z,X,Y/2,Z),''');
	blocks		  
	(
		hex (0 4 5 1 3 7 6 2) (''','''{} {} {}'''.format(xBlockCt,yBlockCt,zBlockCt),''')  
		simpleGrading
	   (1 1 1)

	);
	edges		   
	(
	);

	boundary
	(
		fixedStart
		{
			type patch;
			faces
			(
				(0 1 2 3) // fixed air-filled block
			);
		}
		fixedEnd
		{
			type patch;
			faces
			(
				(4 5 6 7) // fixed air-filled block
			);
		}
		fixedBottom
		{
			type wall;
			faces
			(
				(0 1 5 4) // fixed water-filled block
			);
		}
		fixedRight
		{
			type wall;
			faces
			(
				(0 4 7 3) // fixed air-filled block
			);
		}
		fixedLeft
		{
			type wall;
			faces
			(
				(1 2 6 5) // fixed air-filled block
			);
		}
		fixedAtmosphere
		{
			type patch;
			faces
			(
				(6 3 7 2) // fixed air-filled block
			);
		}
	);
	mergePatchPairs
	(
	);
	// ************************************************************************* //
	''']	 
	with open(writeHere+'/system/blockMeshDict','w') as f:
		f.seek(0)
		for x in blockMeshDict:
			for line in x:
				f.write(line)
				f.truncate()
					


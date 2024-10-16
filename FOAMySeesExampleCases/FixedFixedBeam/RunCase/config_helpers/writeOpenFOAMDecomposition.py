def writeOpenFOAMDecomposition(DomainDecomposition,writeHere):
	print('Writing OpenFOAM decomposeParDict file')
	DecompositionMethod='simple'
		 
	decomposeParDict=['''/*---------------------------------------------------------------------------*\
| =========                                               ____/_________\____     _.*_*.             |
| \\      /      F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \\.           |
|  \\    /       O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | | \._        |
|   \\  /        A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\.__... |
|    \\/         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___...     |
|_________________________________________________________||  |/\| | |/\|  ||__/,_/__,_____/...______|
	\*---------------------------------------------------------------------------*/
	FoamFile
	{
		version		 2.0;
		format		  ascii;
		location		"system";
		class		   dictionary;
		object		  decomposeParDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
	numberOfSubdomains  ''',''' {};
	method			   {};'''.format(DomainDecomposition,DecompositionMethod),'''

	simpleCoeffs
	{''','''
		n			   ({} {} 1);'''.format(DomainDecomposition,1),'''
		delta		   0.001;
	}

	 constraints
	{
	   patches
		{
			type	preservePatches;
			patches (interface);
			enabled true;
		}
	}
		distributed false;
		roots
		(
		);


	// ************************************************************************* //
	''']
	with open(writeHere+'/system/decomposeParDict','w') as f:
		f.seek(0)
		for x in decomposeParDict:
			for line in x:
				f.write(line)		


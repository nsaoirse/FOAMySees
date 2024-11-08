def writeOpenFOAMpreCICEDict(coupledPatchName,writeHere):
	print('Writing OpenFOAM preciceDict file')
	print( 'name of coupled surface(s) :', coupledPatchName)
	OFpreCICEDict=['''/*--------------------------------*- C++ -*----------------------------------*\
| =========                                               ____/_________\____     _.*_*.             |
| \\      /      F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \\.           |
|  \\    /       O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | | \._        |
|   \\  /        A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\.__... |
|    \\/         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___...     |
|_________________________________________________________||  |/\| | |/\|  ||__/,_/__,_____/...______|
	\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      preciceDict;
}

preciceConfig "./precice-config.xml";

participant OpenFOAMCase;

modules (FSI);

interfaces
{

  Interface1
  {
    mesh              OpenFOAM-Mesh;
    locations         faceCenters;
    connectivity      false;
    patches           (''','''{}'''.format(coupledPatchName),''');
	   readData
   (
      Displacement
    );
    writeData
    (
      Force
    );
  };
};


FSI
{
 namePointDisplacement pointDisplacement;
 nameT p_rgh;
 nameP p;
// solverType incompressible;
// nu              nu [ 0 2 -1 0 0 0 0 ] 1e-03;
//rho             rho [1 -3 0 0 0 0 0] 1000;
}
''']

	with open(writeHere+'/system/preciceDict','w') as f:
		f.seek(0)
		for x in OFpreCICEDict:
			for line in x:
				f.write(line)	

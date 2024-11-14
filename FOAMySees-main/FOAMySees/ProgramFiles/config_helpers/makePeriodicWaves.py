def makePeriodicWaves(periodicWaveRepeatPeriod, periodicWaveCelerity, periodicWaveMagnitude,writeHere):
	print('Making Periodic Waves')
	WAVEDICT=['''
	FoamFile
	{
		version	 2.0;
		format	  ascii;
		class	   dictionary;
		location	"constant";
		object	  waveDict;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	waveType		regular;

	waveTheory	  StokesIII;

	genAbs		  1;

	absDir		  0.0;

	nPaddles		1;

	wavePeriod		''','''{}'''.format(periodicWaveRepeatPeriod),''';
	wavePhase		''','''{}'''.format(periodicWaveCelerity/periodicWaveRepeatPeriod),''';

	waveHeight		''','''{}'''.format(periodicWaveMagnitude),''';
	waveDir		 0.0;

	tSmooth		 0.0;

	// ************************************************************************* //
		''']

	with open(writeHere+'/constant/waveDict','w') as f:
		f.seek(0)
		for x in WAVEDICT:
			for line in x:
				f.write(line)
				f.truncate()


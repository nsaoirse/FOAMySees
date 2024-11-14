def configurePrecice(implicitOrExplicit,outputDataFromCouplingIterations,couplingIterationOutputDataFrequency,couplingConvergenceTol,initialRelaxationFactor,couplingDataAccelerationMethod,mapType,SolutionDT,endTime,maximumCouplingIterations,timeWindowsReused,iterationsReused):
	print('Configuring preCICE')
	print("implicitOrExplicit,outputDataFromCouplingIterations,couplingIterationOutputDataFrequency,couplingConvergenceTol,initialRelaxationFactor,couplingDataAccelerationMethod,mapType,SolutionDT,endTime,maximumCouplingIterations")
	print(implicitOrExplicit,outputDataFromCouplingIterations,couplingIterationOutputDataFrequency,couplingConvergenceTol,initialRelaxationFactor,couplingDataAccelerationMethod,mapType,SolutionDT,endTime,maximumCouplingIterations)
	
	implicit=0
	if implicitOrExplicit=='Implicit':
		implicit=1
	FluidWatchPoints=''''''
	SolidWatchPoints=''''''

	if outputDataFromCouplingIterations=="No":
		doWeOutputPreCICEData=''''''
	else:
		doWeOutputPreCICEData='''<export:vtk every-n-time-windows="{}" directory="preCICE-output" />'''.format(couplingIterationOutputDataFrequency)

	exchangeWhatData='''
			<exchange data="Force" mesh="Coupling-Data-Projection-Mesh" from="OpenFOAMCase" to="FOAMySeesCouplingDriver" />
			<exchange data="Displacement" mesh="Coupling-Data-Projection-Mesh" from="FOAMySeesCouplingDriver" to="OpenFOAMCase" />
				'''

	accelWhatData='''
			<data name="Displacement" mesh="Coupling-Data-Projection-Mesh" />
			<data name="Force" mesh="Coupling-Data-Projection-Mesh" />
				'''

	relConvMeasures=''' />
	 		<relative-convergence-measure limit="{}" data="Displacement" mesh="Coupling-Data-Projection-Mesh" />
	 		<relative-convergence-measure limit="{}" data="Force" mesh="Coupling-Data-Projection-Mesh" />'''.format(couplingConvergenceTol,couplingConvergenceTol)
			

	accelTypes=['''<acceleration:aitken>
	'''+accelWhatData+'''
		<initial-relaxation value="{}"/>
	</acceleration:aitken>'''.format(initialRelaxationFactor),
	'''<acceleration:constant>
		<relaxation value="{}"/>
	</acceleration:constant>'''.format(initialRelaxationFactor),
	'''
			<acceleration:IQN-ILS>
	'''+accelWhatData+'''		
				<filter type="QR2" limit="5e-3" />
				<initial-relaxation value="{}" />
				<max-used-iterations value="{}" />
				<time-windows-reused value="{}" />
		</acceleration:IQN-ILS>'''.format(initialRelaxationFactor,str(iterationsReused),str(timeWindowsReused)),
		'''<acceleration:IQN-IMVJ always-build-jacobian="0">
		<initial-relaxation value="{}" enforce="0"/>
		<imvj-restart-mode truncation-threshold="0.0001" chunk-size="8" reused-time-windows-at-restart="8" type="RS-SVD"/>
	'''.format(initialRelaxationFactor)+accelWhatData+'''
		<filter type="QR2" limit="1e-3" />
				<max-used-iterations value="{}" />
				<time-windows-reused value="{}" />
	 </acceleration:IQN-IMVJ>
		'''.format(str(iterationsReused),str(timeWindowsReused)),
		'''<acceleration:broyden>'''+accelWhatData+'''
		<initial-relaxation value="{}" />
				<max-used-iterations value="{}" />
				<time-windows-reused value="{}" />
	</acceleration:broyden>'''.format(initialRelaxationFactor,str(iterationsReused),str(timeWindowsReused)),]

	if couplingDataAccelerationMethod=="Constant":
		accelType=accelTypes[1]
	elif couplingDataAccelerationMethod=="Aitken":
		accelType=accelTypes[0]
	elif couplingDataAccelerationMethod=="IQN-ILS":
		accelType=accelTypes[2]
	elif couplingDataAccelerationMethod=="IQN-IMVJ":
		accelType=accelTypes[3]
	elif couplingDataAccelerationMethod=="Broyden":
		accelType=accelTypes[4]
	else:
		pass


	#	<sink
	#		filter="%Severity% > debug and %Rank% = 0"
	#		format="---[precice] %ColorizedSeverity% %Message%"
	#		enabled="true" />
			
	preCICEdict=['''<?xml version="1.0" encoding="UTF-8" ?>
<precice-configuration>
	<log>

	</log>
	<data:vector name="Force" />
	<data:vector name="Displacement" />

	<mesh name="OpenFOAM-Mesh" dimensions="3">
		<use-data name="Displacement" />
		<use-data name="Force" />
	</mesh>

	<mesh name="Coupling-Data-Projection-Mesh" dimensions="3">
		<use-data name="Displacement" />
		<use-data name="Force" />
	</mesh>

	<participant name="FOAMySeesCouplingDriver">
	''',doWeOutputPreCICEData,'''
		<provide-mesh name="Coupling-Data-Projection-Mesh"/>
		<write-data name="Displacement" mesh="Coupling-Data-Projection-Mesh" />
		<read-data name="Force" mesh="Coupling-Data-Projection-Mesh" />
	</participant>
		
	<participant name="OpenFOAMCase">
					''',FluidWatchPoints,'''
	''',doWeOutputPreCICEData,'''
		<receive-mesh name="Coupling-Data-Projection-Mesh" from="FOAMySeesCouplingDriver" />
		<provide-mesh name="OpenFOAM-Mesh" />
		<write-data name="Force" mesh="OpenFOAM-Mesh" />
		<read-data name="Displacement" mesh="OpenFOAM-Mesh" />
		<mapping:{}'''.format(mapType),'''
		direction="write"
		from="OpenFOAM-Mesh"
		to="Coupling-Data-Projection-Mesh"
		constraint="conservative" />
		<mapping:{}'''.format(mapType),'''
		direction="read"
		from="Coupling-Data-Projection-Mesh"
		to="OpenFOAM-Mesh"
		constraint="consistent" />
	</participant>
	<m2n:sockets acceptor="OpenFOAMCase" connector="FOAMySeesCouplingDriver" exchange-directory="."/>
				''']
        # <m2n:mpi acceptor="OpenFOAMCase" connector="FOAMySeesCouplingDriver"/>
        # <m2n:sockets port="10101" acceptor="OpenFOAMCase" connector="FOAMySeesCouplingDriver" exchange-directory=".." enforce-gather-scatter="1"/>
	
        # <mapping:{}'''.format(mapType),'''
			# direction="read"
			# from="Coupling-Data-Projection-Mesh"
			# to="OpenFOAM-Mesh"
		 # constraint="consistent" />
		 
		 
					 # <mapping:{}'''.format(mapType),'''
			# direction="read"
			# to="Coupling-Data-Projection-Mesh"
			# from="OpenFOAM-Mesh"
		 # constraint="consistent" />
			 # <mapping:{}'''.format(mapType),'''
			# direction="write"
			# to="OpenFOAM-Mesh"
			# from="Coupling-Data-Projection-Mesh"
			# constraint="conservative" />

	if implicit==1:
		preCICEdict.append(
		'''
		<coupling-scheme:parallel-implicit>
			<time-window-size value="{}"'''.format(SolutionDT)),
		preCICEdict.append(''' />
			<max-time value="{}"/>'''.format(endTime))
		preCICEdict.append('''
			<participants first="OpenFOAMCase" second="FOAMySeesCouplingDriver"/>'''+exchangeWhatData+'''
			<max-iterations value="{}"'''.format(maximumCouplingIterations))
		preCICEdict.append(relConvMeasures)
		preCICEdict.append('''		
				
			''')
		preCICEdict.append(accelType)
		preCICEdict.append('''
		</coupling-scheme:parallel-implicit>
	</precice-configuration>
	''')
	else:
		preCICEdict.append(''' 
			<coupling-scheme:parallel-explicit>
				<time-window-size value="{}"'''.format(SolutionDT))
		preCICEdict.append(''' />
				<max-time value="{}"/>'''.format(endTime))
		preCICEdict.append('''
				<participants first="OpenFOAMCase" second="FOAMySeesCouplingDriver"/>'''+exchangeWhatData+'''
			</coupling-scheme:parallel-explicit>
	</precice-configuration>
		''')
	print('Writing the precice config.xml file')
	with open('precice-config.xml','w') as f:
		f.seek(0)
		for x in preCICEdict:
			for line in x:
				f.write(line)
				f.truncate()
		

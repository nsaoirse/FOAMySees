from dependencies import *
import os.path
import time

#| ============================================== ____/__\___/__\____	 _.*_*.	             |
#|	F ield		|   |  S tructural	  ||__|/\|___|/\|__||	  \ \ \ \.	     |
#|      O peration	|___|  E ngineering &     ||__|/\|___|/\|__||	   | | |  \._ CESG   |  
#|	A nd		    |  E arthquake	  ||__|/\|___|/\|__||	  _/_/_/ | .\. UW    |
#|	M anipulation	|___|  S imulation	  ||__|/\|___|/\|__||   __/, / _ \___.. 2023 |
#| ==============================================_||  |/\| | |/\|  ||__/,_/__,_____/..__ nsl_|

# The work within this thesis was funded by the National Science Foundation (NSF) and Joy Pauschke (program manager) through Grants CMMI-1726326, CMMI-1933184, and CMMI-2131111. 
# Thank you to NHERI Computational Modeling and Simulation Center (SimCenter), as well as their developers, funding sources, and staff for their continued support. 
# It was a great experience to work with the SimCenter to implement this tool allowing for partitioned coupling of OpenSees and OpenFOAM as part of a digital-twin module within the NHERI SimCenter Hydro-UQ framework.
# Much of the development work of the research tool presented was conducted using University of Washington's HYAK Supercomputing resources. 
# Thank you to UW HYAK and to the support staff of the UW HPC resources for their maintenance of the supercomputer cluster and for offering a stable platform for HPC development 
# and computation, as well as for all of the great support over the last few years.  

fys_couplingdriver_log_location='fys_logs/FOAMySeesCouplingDriver.log'
work_log_location='fys_logs/WorkInAndOut.log'
branch_log='fys_logs/BranchesLOCS.log'
opensees_log_location='fys_logs/What is Happening With OpenSees.log'


sys.path.insert(0, './FOAMySees')
#########################################################################################
OpenSees_dt=config.SolutionDT
with open(fys_couplingdriver_log_location, 'a+') as f:
	print('OpenSees Solution Maximum dT=',config.SolutionDT,file=f)
	print("Initializing FOAMySees Coupling Driver",file=f)

#################################################################################################	
parser = argparse.ArgumentParser()
parser.add_argument("configurationFileName", help="Name of the xml config file.", nargs='?', type=str,
					default="precice-config.xml")
parser.add_argument("CouplingDataProjectionMesh", help="Name of the file to load as the Coupling Data Projection Mesh", nargs='?', type=str,
					default="CouplingDataProjectionMesh.obj")
try:
	args = parser.parse_args()
except SystemExit:
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("Something is wrong! Exiting. The argument parser is telling you that you need to include something...",file=f)
	exit

#################################################################################################	
#################################################################################################
FOAMySees=FOAMySeesInstance(OpenSees_dt,config)

noOpenSeessubsteps=FOAMySees.config.numOpenSeesStepsPerCouplingTimestep
noOpenFOAMsubsteps=FOAMySees.config.numOpenFOAMStepsPerCouplingTimestep
with open(fys_couplingdriver_log_location, 'a+') as f:
	print(noOpenSeessubsteps,noOpenFOAMsubsteps,"noOpenSeessubsteps,noOpenFOAMsubsteps",file=f)


#################################################################################################
configFileName = args.configurationFileName

CouplingDataProjectionMesh = args.CouplingDataProjectionMesh

with open(fys_couplingdriver_log_location, 'a+') as f:
	print('configFileName',configFileName, 'CouplingDataProjectionMesh',CouplingDataProjectionMesh, file=f)
#################################################################################################
if __name__ == '__main__':# and rank==0:

	solverName = "FOAMySeesCouplingDriver"  
	#################################################################################################	
	# measuring the length of the coupled nodes list 
	N = len(FOAMySees.coupledNodes) # number of coupled ops.nodes
	# reporting
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("Number of Coupled OpenSees Nodes: " + str(N),file=f)
	#################################################################################################
	# reporting
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("Configuring preCICE library",file=f)
		# precice v2
	# interface = precice.Interface(solverName, configFileName, 0, 1)
		# precice v3
	interface = precice.Participant(solverName, configFileName, 0, 1)
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("preCICE successfully configured",file=f)
	#################################################################################################

	
	#################################################################################################
	# returning the dimensions defined by the coupling library
	#dimensions = interface.get_mesh_dimensions("OpenFOAM-Mesh")
	dimensions=3 # overruling that #	bounding_box : array_like
	while not os.path.exists(CouplingDataProjectionMesh):
		time.sleep(1)

	if os.path.isfile(CouplingDataProjectionMesh):
		with open(CouplingDataProjectionMesh) as f:
			lines=f.read()
	else:
		raise ValueError("%s could not be found" % CouplingDataProjectionMesh)
	lines=lines.split('\n')
	points=[]
	facets=[]
	Branches=[]
	# for obj
	if '.obj' in CouplingDataProjectionMesh:
		for line in lines:
			#print(line[:])
			if '#' in str(line[:]):
				pass
			elif 'g' in line:
				pass
			elif 'v' in line:
				points.append(line.strip('v ').split(' '))
			elif 'f' in line:
				facets.append(line.strip('f ').split(' '))
		#print(points)
		#print(facets)
		for facet in facets:
			if ('#' in facet) or ('g' in facet) or ('o' in facet):
				pass
			else:
				branch=np.zeros([1,3],dtype=float)
				ptfacet=0
				for i in facet:
					if i=='':
						pass
					else:
						pt=points[int(i)-1]
						for iin in pt:
							iin=float(iin)
						pt=np.array(pt,dtype=float)
						branch+=pt
						ptfacet+=1
				with open(fys_couplingdriver_log_location, 'a+') as f:
					print(branch/ptfacet,file=f)
				Branches.append(branch[0]/ptfacet)

	Branches=np.array(Branches)					   


		
		
	vertexIDsDisplacement = interface.set_mesh_vertices("Coupling-Data-Projection-Mesh", Branches)
				
	# force and displacement are currently applied and calculated at the face centers of the OpenFOAM patch cells
	vertexIDsForce = vertexIDsDisplacement


	#################################################################################################		  
	# using SciPy to calculate the K-means clustering  
		#   .... from scipy.spatial import KDTree
	Tree=KDTree(FOAMySees.nodeLocs)
	BranchToNodeRelationships=Tree.query(Branches)[1]
	CellToNodeRelationships=Tree.query(Branches)[1]		
	
	with open('./fys_logs/FOAMySees_node_locations.log','w+') as f:
		for nodeLoc in FOAMySees.nodeLocs:
			print("{} {} {}".format(nodeLoc[0],nodeLoc[1],nodeLoc[2]), file=f)
	with open('./fys_logs/branches_locations.log','w+') as f:
		for branch in Branches:
			print("{} {} {}".format(branch[0],branch[1],branch[2]), file=f)


	#################################################################################################
	# initializing a bunch of arrays of the same size
	verticesDisplacement=Branches
	verticesForce=Branches
	verticesDisplacement=np.array(verticesDisplacement)
	verticesForce=np.array(verticesForce)
	FOAMySees.verticesDisplacement=verticesDisplacement
	FOAMySees.verticesForce=verticesForce
	BranchTransform=np.zeros(np.shape(verticesDisplacement))
	Displacement = np.zeros(np.shape(verticesDisplacement))	
	Forces = np.zeros(np.shape(verticesForce))
	FOAMySees.moment = np.zeros([len(FOAMySees.coupledNodes),3])
	#################################################################################################
	# building the FEM node to Branch Group relationships	

	NodeToBranchNodeRelationships=[]
	NodeToCellFaceCenterRelationships=[]
	for n in range(len(FOAMySees.nodeLocs)):
		NodeToCellFaceCenterRelationships.append([n])
	for node in range(len(CellToNodeRelationships)):
		NodeToCellFaceCenterRelationships[CellToNodeRelationships[node]].append(node)		
	for n in range(len(FOAMySees.nodeLocs)):
		NodeToBranchNodeRelationships.append([n])
	for node in range(len(BranchToNodeRelationships)):
		NodeToBranchNodeRelationships[BranchToNodeRelationships[node]].append(node)
	FOAMySees.NodeToBranchNodeRelationships=NodeToBranchNodeRelationships

	with open('./fys_logs/BranchToNodeRelationships.log','w+') as f:
		for BranchToNodeRelationship in NodeToBranchNodeRelationships:
			print(BranchToNodeRelationship)
			if type(branch[1]) is list():
				for branchnode in branch[1]:
					print(FOAMySees.nodeLocs[branch[0]],Branches[branchnode], file=f)
	
	FOAMySees.NodeToCellFaceCenterRelationships=NodeToCellFaceCenterRelationships		
	#################################################################################################	
	# reporting to file
	with open(branch_log, 'a+') as f:
		f.seek(0)
		f.truncate()
		print(NodeToBranchNodeRelationships,file=f)
		print(verticesDisplacement,file=f)
		print(np.shape(verticesDisplacement),file=f)
		print(NodeToCellFaceCenterRelationships,file=f)
		print(verticesForce,file=f)
		print(np.shape(verticesForce),file=f)
	
	
	#################################################################################################		
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("FOAMySees Coupling Driver: Initializing Coupling with preCICE",file=f)

	# preCICE action - returns ID of mesh 
	# deprecated in precice v3
	# meshID = interface.get_mesh_id("Coupling-Data-Projection-Mesh")


	#################################################################################################

	# reporting
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print('OpenSeesPy (FOAMySees Projected) Initial Displacements (from preliminary analysis)',Displacement,file=f)

	
	#################################################################################################	
	# creating a PVD file for the initial state of the OpenSees model
	FOAMySees.createRecorders.createPVDRecorder(FOAMySees)
	
	#################################################################################################
	# creating all recorders for the initial state of the OpenSees model
	FOAMySees.createRecorders.createNodeRecorders(FOAMySees,FOAMySees.nodeRecInfoList)				

	#if interface.is_action_required(action_read_initial_data()):
	#	print('Initial Force',Force)
	#	interface.read_block_vector_data(forceID, vertexIDsForce, Force)
	#	interface.mark_action_fulfilled(action_read_initial_data())
	
	#################################################################################################	
	# intializing some things
	stepOut=1
	oneWay=1
	oneWayD=1
	onewaystatus="this is a fully-coupled simulation: if work errors occur, adjust (1) timestep, (2) coupling settings, and/or (3) spatial discretization at the interface"
	with open(work_log_location, 'a+') as f:
				print(FOAMySees.config.oneWay,onewaystatus,file=f)
	if FOAMySees.config.oneWay==1:
		oneWay*=0
		onewaystatus="this is a one-way-coupled simulation: OpenSees Displacements are not transferred to OpenFOAM"
	if FOAMySees.config.oneWay==2:
		oneWayD*=0
		onewaystatus="this is a one-way-coupled simulation. OpenFOAM Forces are not transferred to OpenSees"
	
	FOAMySees.lastForces=copy.deepcopy(FOAMySees.force)
	FOAMySees.lastMoments=copy.deepcopy(FOAMySees.moment)
	observe_node_num=1
	tOUT=0
	tLIST=[]
	StepCheck=1
	newStep=1
	FOAMySees.lastForceandmoment=copy.deepcopy(FOAMySees.forceandmoment)
	LastForces=copy.deepcopy(Forces)
	LastDisplacement=copy.deepcopy(Displacement)
	iteration=1
	#################################################################################################
	# creating the OpenSees analysis objects, if they have not been created already	
	FOAMySees.timeInt()

	#################################################################################################	
	# defining the number of OpenSees substeps
	FOAMySees.CurrSteps=noOpenSeessubsteps
	#################################################################################################
	# preCICE action
	if interface.requires_initial_data():
		#with open(fys_couplingdriver_log_location, 'a+') as f:
		#	print('Initial Displacement',Displacement,file=f)
		interface.write_block_vector_data(displacementID, vertexIDsDisplacement, Displacement)

	#################################################################################################

	# preCICE action - gives initial coupling timestep, initializes DATA and pointers between solvers
	precice_dt = interface.initialize()


	#################################################################################################
	# preCICE action	
	if interface.requires_writing_checkpoint ():
		ops.database('File',"SeesCheckpoints/checkpoint")
		ops.save(0)
		thisTime=copy.deepcopy(ops.getTime())
		with open(opensees_log_location, 'a+') as f:
			print('Wrote a checkpoint at opensees time = ',thisTime,file=f)		
		
	
	#################################################################################################	
	# Cleaning up and making storage directories for OpenSees
	Popen('rm -rf SeesCheckpoints', shell=True, stdout=DEVNULL).wait()
	Popen('mkdir SeesCheckpoints', shell=True, stdout=DEVNULL).wait()
	Popen('mkdir SeesCheckpoints/checkpoints/', shell=True, stdout=DEVNULL).wait()
	
	
	#################################################################################################	
	# preCICE action	
	force = oneWayD*interface.read_data("Coupling-Data-Projection-Mesh","Force", vertexIDsForce,0)
	
	DT=float(FOAMySees.config.SolutionDT)
	FOAMySees.thisTime=0
	FOAMySees.stepNumber=0
	FOAMySees.iteration=0
	
	#################################################################################################
	# preCICE action - entering the coupling loop
	while interface.is_coupling_ongoing():
		if FOAMySees.thisTime<FOAMySees.config.couplingStartTime:					
			with open('./fys_logs/tlog', 'a+') as f:
				print("{} {} {} {}".format(ops.getTime(),FOAMySees.stepNumber,FOAMySees.totalSteps,FOAMySees.iteration),file=f)

			interface.write_data("Coupling-Data-Projection-Mesh","Displacement", vertexIDsDisplacement, LastDisplacement)
			interface.requires_reading_checkpoint()
			FOAMySees.stepForward(DT)			
			interface.advance(DT)
			FOAMySees.thisTime+=DT
			print("Uncoupled Simulation Time: {}s, {}% to coupling start time at {}s".format(FOAMySees.thisTime,100*FOAMySees.thisTime/FOAMySees.config.couplingStartTime,FOAMySees.config.couplingStartTime))
			interface.requires_writing_checkpoint()
			FOAMySees.stepNumber+=1
                        
		else:
			print("Coupled Simulation Time: {}s, {}% to termination time at {}s".format(FOAMySees.thisTime,100*FOAMySees.thisTime/FOAMySees.config.endTime,FOAMySees.config.endTime))
			#################################################################################################
			# preCICE action - checking if a database needs to be written (implicit only)
			if (interface.requires_writing_checkpoint()) or newStep==1:

				# summons database save in OpenSees
				FOAMySees.writeCheckpoint(stepOut)

			if (interface.requires_reading_checkpoint()):

				# summons database save in OpenSees
				FOAMySees.readCheckpoint(stepOut)

			#################################################################################################		
			# creating OpenSees recorders for the timestep				
			FOAMySees.createRecorders.createNodeRecorders(FOAMySees,FOAMySees.nodeRecInfoList)


			#################################################################################################

			# gathering forces from preCICE
			Forces=oneWayD*interface.read_data("Coupling-Data-Projection-Mesh","Force", vertexIDsForce,0)

			ForcePrediction=FOAMySees.TSExpPredict(tOUT+DT)
			with open('./fys_logs/plog', 'a+') as f:
                                #print(Forces,ForcePrediction,file=f)
                                print('Force Prediction Ratio= ',np.linalg.norm(FOAMySees.forceandmoment)/np.linalg.norm(ForcePrediction),file=f)
		
			for substep in range(1,noOpenSeessubsteps+1):						
				currForces=(copy.deepcopy(Forces)-LastForces)*(substep/noOpenSeessubsteps) + LastForces

				#################################################################################################		
				# looping through the branch groups and determining applied FEM nodal forces
				for node in FOAMySees.NodeToCellFaceCenterRelationships:
					FOAMySees.force[node[0],:]=np.sum(currForces[node[1:],:],axis=0)
				#################################################################################################		
				# looping through the branch groups and determining applied FEM nodal moments
				FOAMySees.calculateUpdatedMoments(currForces)

				#################################################################################################		
				# stepping forward in time with a variableTransient time integration
				# the forces and moments are applied to the coupled nodes here
				StepCheck=FOAMySees.stepForward(FOAMySees.dt/noOpenSeessubsteps)

				#################################################################################################		
				# reporting
				with open(fys_couplingdriver_log_location, 'a+') as f:
					print(ops.getTime(),' = OpenSees time\n', substep,'/',noOpenSeessubsteps, ' = substep/noOpenSeessubsteps',file=f)

				#################################################################################################
				# did the step converge?
				if (StepCheck!=0):
					with open(fys_couplingdriver_log_location, 'a+') as f:
						print(' OpenSeesPy Step did not converge :(',FOAMySees.thisTime,file=f)
					
			#################################################################################################			
			# projecting the displacement field from OpenSees to the coupling data projection mesh				
			Displacement=oneWay*FOAMySees.projectDisplacements(Displacement)
			
			#################################################################################################			
			# calculating the Work
					
			FOAMySees.WorkIn=np.sum(FOAMySees.forceandmoment*(FOAMySees.displacement-FOAMySees.lastDisplacements))
			FOAMySees.WorkOut=0
			with open(work_log_location, 'a+') as f:
							print(FOAMySees.config.oneWay,onewaystatus,file=f)
			for substep in range(1,noOpenFOAMsubsteps+1):
				FOAMySees.WorkOut+=np.sum((Forces)*(Displacement-LastDisplacement)*(1/noOpenFOAMsubsteps))
				with open(fys_couplingdriver_log_location, 'a+') as f:
					print('iteration:',iteration,', Time: ',ops.getTime(),'Work Transfer -- error (%)',100*(FOAMySees.WorkIn-FOAMySees.WorkOut)/FOAMySees.WorkIn,' W(f->s)/W(s->f)  (Ratio)',FOAMySees.WorkIn/FOAMySees.WorkOut,', W(f->s) (Joules): ',FOAMySees.WorkIn,', W(s->f) (Joules): ',FOAMySees.WorkOut,file=f)
			
				#################################################################################################
				# sending the projected displacements to preCICE to be mapped to OpenFOAM during the next iteration or timestep
				interface.write_data("Coupling-Data-Projection-Mesh","Displacement", vertexIDsDisplacement, oneWay*(LastDisplacement+(Displacement-LastDisplacement)*(substep/noOpenFOAMsubsteps)))
				#################################################################################################		
				# Advancing the coupling scheme -
				# precice_dt=interface.advance(precice_dt)			
				precice_dt_return=interface.advance(DT/noOpenFOAMsubsteps)
				with open(fys_couplingdriver_log_location, 'a+') as f:
					print('OpenFOAM substep ', substep,' of ', noOpenFOAMsubsteps, 'OpenSees time: ', ops.getTime(), 'OpenFOAM time: ', ops.getTime() -(noOpenFOAMsubsteps-(substep))*DT/noOpenFOAMsubsteps ,file=f)
			
			#  checking if residuals<tolerances & performing accleration (implicit), no accel/iter (explicit)	
			#################################################################################################		
			# checking with preCICE to see if we have converged, or if we need to try the timestep again with new coupling data
			if interface.requires_reading_checkpoint():
				#FOAMySees.CurrSteps+=1				
				FOAMySees.readCheckpoint(stepOut)
				# reading the previously saved database
				StepCheck=0
				# adding one to the iteration counter
				FOAMySees.iteration+=1
				
				# letting preCICE know we are finished going back in time			
			else:
				LastForces=copy.deepcopy(Forces)
				LastDisplacement=copy.deepcopy(Displacement)
				FOAMySees.StepsPerFluidStep=1

				with open('./fys_logs/verticesForce.log','w') as f:
					for force in Forces:
						print("{} {} {}".format(force[0],force[1],force[2]),file=f)
				with open('./fys_logs/verticesDisplacement.log','w') as f:
					for delta in Displacement:
						print("{} {} {}".format(delta[0],delta[1],delta[2]),file=f)				
				
				#################################################################################################
				# saving these for some sort of surrogate model?
				FOAMySees.lastForceandmoment=copy.deepcopy(FOAMySees.forceandmoment)
				FOAMySees.lastForces=copy.deepcopy(FOAMySees.force)
				FOAMySees.lastDisplacements=copy.deepcopy(FOAMySees.displacement)	
				FOAMySees.stepNumber+=1
				FOAMySees.iteration=1
				
				FOAMySees.Flast5times[:,4]=FOAMySees.Flast5times[:,3]
				FOAMySees.Flast5times[:,3]=FOAMySees.Flast5times[:,2]
				FOAMySees.Flast5times[:,2]=FOAMySees.Flast5times[:,1]
				FOAMySees.Flast5times[:,1]=FOAMySees.Flast5times[:,0]
				FOAMySees.Flast5times[:,0]=np.reshape(FOAMySees.forceandmoment,[FOAMySees.ndofs,])[:]
				
				
				# we are converged, or have given up!
				#################################################################################################			
				# doing some house keeping
				Popen("ls -t SeesCheckpoints/checkpoints/*| tail -n +100 | xargs -d '\n' rm", shell=True, stdin=None, stdout=None, stderr=None,)
				newStep=1
				tOUT += DT
				FOAMySees.CurrSteps=1
				stepOut+=1
				FOAMySees.StepsPerFluidStep=1
	
			#################################################################################################
			#ops.wipe()
			# calling all the recorders made

			ops.record()
			
			FOAMySees.writeLogs()
			
			FOAMySees.createRecorders.appendRecords(FOAMySees,FOAMySees.nodeRecInfoList)		
			if tOUT>=FOAMySees.config.SeesVTKOUTRate:
				tOUT=0
				FOAMySees.createRecorders.createPVDRecorder(FOAMySees)

			#################################################################################################
	with open(fys_couplingdriver_log_location, 'a+') as f:
		print("Exiting FOAMySees Coupling Driver",file=f)

	interface.finalize()

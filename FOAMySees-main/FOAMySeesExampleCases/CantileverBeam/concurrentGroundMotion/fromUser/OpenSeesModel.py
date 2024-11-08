
#import openseespy.opensees as ops
#import numpy as np
#import os

#FOAMySeesInstance.osi=
ops.model('basic','-ndm',3,'-ndf',6)

RunEQ=1

nElem=48

nu=0.45

EScaleFactor=1
E=1000000*EScaleFactor #10^7 dyne or 1MPa


structuralDensity=2500
MASS=structuralDensity*0.08*0.012*0.01

beamNormal=[1., 0., 0.]


structuralDensity=2500
node1=[0.006,0.00,0.005]
node2=[0.006,0.08,0.005]
I=0.01*(0.012**3)/12
A = .01*0.012
Iz = I
Iy = Iz
J =  0.333
beamLength=node2[1]-node1[1]

G=E/(2*(1+nu))

sigmaY=1e6
H_iso=0.5 
H_kin=0.25


matTag=1

# ops.nDMaterial('ElasticIsotropic', matTag, E, nu, 0.0)

node1=[0.006,0.00,0.005]
node2=[0.006,0.08,0.005]

# node1=[2.0,0.0,0.0]
# node2=[2.0,0.0,0.25]

beamNormal=[-1,0,0]


xNodeList=np.linspace(node1[0],node2[0],nElem+1)
yNodeList=np.linspace(node1[1],node2[1],nElem+1)
zNodeList=np.linspace(node1[2],node2[2],nElem+1)


for nodeNum in range(0, len(xNodeList)):
	ops.node(nodeNum, xNodeList[nodeNum],yNodeList[nodeNum],zNodeList[nodeNum])

# ##################
# ELEMENTS
# ##################


matTag=1
K=E*G/(3*(3*G - E))



#ops.uniaxialMaterial('Elastic', matTag, E) 
#ops.uniaxialMaterial('ElasticPP', matTag, E, 0.05)

#ops.uniaxialMaterial('ElasticMultiLinear', matTag, 0.0, '-strain', *[-0.3,-0.2,-0.1,0,0.1,0.2,0.3], '-stress', *[-0.3*E,-0.2*E,-0.1*E,0,0.1*E,0.2*E,0.3*E])

#ops.uniaxialMaterial('MultiLinear', matTag, *[0.001, E*0.001, 0.2, E*0.15])

ops.uniaxialMaterial('Hardening', matTag, E, sigmaY, H_iso, H_kin)
#ops.nDMaterial('ElasticIsotropic', matTag, E, nu, 1000.0)
#ops.nDMaterial('J2Plasticity', matTag, K, G, sig0, sigInf, delta, H)

# coordTransf = 'Corotational'
#coordTransf='PDelta'
coordTransf='Linear'
#############################

nodeList=ops.getNodeTags()

nodeLocs=np.zeros([len(nodeList),3])

nodalMass=MASS/len(nodeLocs)
secTag=1
matTag=1

#ops.section('Elastic', secTag, E, A, Iz, Iy, G, J)

ops.section('Fiber', secTag, '-GJ', G*J)

ops.patch('rect', matTag, 2,12, *[-0.005,-0.006], *[0.005,0.006])

for node in range(1,len(nodeList)):
	
	nodeLocs[node,:]=ops.nodeCoord(nodeList[node])

integTag=1
ops.beamIntegration('Legendre', integTag, secTag, 2)

leme=10/(len(xNodeList)-1)
nodRotMass=0 #(1/12)*nodalMass*(leme**2)
for node_num in range(len(nodeLocs)):
	ops.mass(nodeList[node_num],*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])		
for nodeNum in range(1,len(nodeLocs)):
	ops.geomTransf(coordTransf, nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	
	#ops.element('forceBeamColumn', nodeNum, *[nodeNum-1, nodeNum], nodeNum+100000, integTag, '-iter', 10, 1e-12)#, '-mass', mass=0.0)
	#ops.element('elasticBeamColumn', nodeNum, *[nodeNum-1, nodeNum], secTag, nodeNum+100000)
	#ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum], nodeNum+100000, secTag) #, '-cMass', '-mass', mass=0.0)
	ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, A, E, G, J, Iy, Iz, nodeNum+100000)
	#ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],5,secTag,nodeNum+100000,'-iter', secTag)

ops.fixY(0.00,*[1,1,1,1,1,1])


nodeRecInfoList=[['reactionBase.out',0,'reaction'],['tipDisplacement.out',nElem,'disp'],['displacementBase.out',0,'disp']]


res=['disp','vel','accel','incrDisp','reaction','pressure','unbalancedLoad','mass']

#fibery,fiberz = 0.005, 0.006
#ops.recorder('Element','-ele',1,'-file','fiber.out','section', secTag, fibery,fiberz,matTag,'stressStrain')

# ops.recorder('Element', '-ele', 1, 'section', str(1), 'fiber', str(y), str(z), 'stress')
args='force'
#args=['section', secTag, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#args=[0, 'section', secTag, fibery,fiberz,'stressStrain']		# fibre y- and z-coordinates
							# responseType]
eleTags=[0,1]
#ops.recorder('Element', '-file', ElementOut, '-precision', 6,  '-time', '-dT', deltaT=0.001, '-ele', *eleTags=[], '-eleRange', 0, 1,  *args)
ops.recorder('Element', '-file', 'ElementOut.txt', '-precision', 6,  '-time', '-dT', 0.001, '-ele', *eleTags,   *args)

os.system('rm -rf SeesoutPrelim')
os.system('mkdir SeesoutPrelim')
os.system('touch SeesoutPrelim.pvd')
ops.recorder('PVD', 'SeesoutPrelim', '-precision', 4, '-dT', 0.01, *res)

if RunEQ==1:

	Tol=1e-3
	maxNumIter = 10
	#ops.pattern('UniformExcitation', IDloadTag, GMdirection, '-accel', 2) 

	ops.recorder('Node', '-file', 'DFree.out','-time', '-node', 48, '-dof', 1,2,3, 'disp')
	ops.recorder('Node', '-file', 'DBase.out','-time', '-node', 0, '-dof', 1,2,3, 'disp')
	ops.constraints('Transformation')
	ops.numberer('Plain')
	ops.system('BandGeneral')
	ops.test('EnergyIncr', Tol, maxNumIter)
	ops.algorithm('ModifiedNewton')
	NewmarkGamma = 0.5
	NewmarkBeta = 0.25
	ops.integrator('Newmark', NewmarkGamma, NewmarkBeta)
	ops.analysis('VariableTransient')
	DtAnalysis = 0.001
	TmaxAnalysis = 10
	Nsteps =  int(TmaxAnalysis/ DtAnalysis)
	ok=1
	# for i in test:
	ops.algorithm('KrylovNewton')
	
ops.database('File',"SeesCheckpoint"+str(0))
ops.save(0)
ops.restore(0)


# ok = ops.analyze(Nsteps, DtAnalysis,DtAnalysis/10,DtAnalysis,1)	


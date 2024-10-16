ops.wipe()



E=2e11

nu=0.3
G=E/(2*(1+nu))
numDOF=6

ops.model('basic','-ndm',3,'-ndf',numDOF)


nElem=80


density=100
domainThickness=0.1
nNodes=nElem+1

node1=[0. , 0.0, 0.0]
node2=[10., 0.0, 0.0]

beamNormal=[0., 0., 1.]

beamLength=node2[0]-node1[0]

A =0.1

b=0.1
h=1

beamThickness=h


Iz =b*(h**3)/12

Iy = Iz
J =  0.333

matTag=1
	
ops.nDMaterial('ElasticIsotropic', matTag, E, nu, 1000.0)



xNodeList=np.linspace(node1[0],node2[0],nElem+1)
yNodeList=np.linspace(node1[1],node2[1],nElem+1)
zNodeList=np.linspace(node1[2],node2[2],nElem+1)

MASS=density*beamLength*domainThickness*beamThickness

for nodeNum in range(0, len(xNodeList)):
	ops.node(nodeNum, xNodeList[nodeNum],yNodeList[nodeNum],zNodeList[nodeNum])


coordTransf = 'Corotational'
coordTransf='PDelta'
#############################
 
nodeList=ops.getNodeTags()

nodalMass=MASS/nNodes
secTag=1
integTag=1
ops.section('Elastic', secTag, E, A, Iz, Iy, G, J)

ops.beamIntegration('Legendre', integTag, secTag, 2)

nodRotMass=0 #(1/12)*nodalMass*(leme**2)

for node_num in range(nNodes):
	ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])		

for nodeNum in range(1,nNodes):
	ops.geomTransf(coordTransf, nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	
	ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum], nodeNum+100000, integTag) #, '-cMass', '-mass', mass=0.0)
	
	#ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, A, E, G, J, Iy, Iz, nodeNum+100000)
	#ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,nodeNum+100000,'-iter', 1)

ops.fixX(0.0,*[1, 1, 1, 1, 1, 1])
ops.fixX(10.0,*[1, 1, 1, 1, 1, 1])


ops.recorder('Node', '-file', 'reactionNodeLHS.out','-time', '-node', 0, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'reactionNodeRHS.out','-time', '-node', nNodes-1, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'dispNodeCenter.out','-time', '-node', nNodes//2, '-dof', 1,2,3,4,5,6, 'disp')
f1= 9.39
f2=f1*5 

       # 0.42          0.94          1.33          2.97          4.20          9.39         13.29         29.71         59.42        187.90
    # 1000000.00    5000000.00   10000000.00   50000000.00  100000000.00  500000000.00 1000000000.00 5000000000.00 20000000000.00 200000000000.00
z1=0.1
z2=0.1

alphaM = 0.000 # (4*3.1415*f1*f2)*((z1*f2 - z2*f1)/(f2**2 - f1**2))               # M-prop. damping; D = alphaM*M    

betaKcurr = 00.00 # K-proportional damping;      +beatKcurr*KCurrent <- not this

betaKinit = ((z1*f2 - z2*f1)/(3.1415*(f2**2 - f1**2))) # initial-stiffness proportional damping      +beatKinit*Kini <<<<<<<<<------------------------------ use this 
betaKcomm = 0.0
ops.rayleigh(alphaM,betaKcurr, betaKinit, betaKcomm) # RAYLEIGH damping
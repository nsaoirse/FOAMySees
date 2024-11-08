
ops.wipe()


FOAMySeesInstance.coupledNodes=[]

nElemBOTTOM=16
nElem2nd=4
nElemTOP=4

numX=2
numY=2

ColumnConnectionLength=0.05
BeamConnLength=0.0254*4

BuildingLocation=[(40.88230+41.89830)/2, 0.0]
BuildingDepth=41.89830-40.88230
BuildingWidth=0.508*2
Xmin=BuildingLocation[0]-BuildingDepth/2
Xmax=BuildingLocation[0]+BuildingDepth/2
Ymin=BuildingLocation[1]-BuildingWidth/2
Ymax=BuildingLocation[1]+BuildingWidth/2

zPileBase=1.0
zBase=2.0
z1stFloor=2.6180000
z2ndFloor=2.6180000+(27.1*0.0254)
z3rdFloor=2.6180000+(27.1*0.0254)+(18*0.0254)
z4thFloor=2.6180000+(27.1*0.0254)+(18*0.0254)*2

beamType='NLBeamCol'
beamType='forceBeamCol'


beamType='elastic'
beamType='dispBeamCol'






noBraces=0
useBeams=1

constraintType='EQDOFMIXED'
constraintType='RIGIDLINK'	
constraintType='EQDOF'

useSlabs=1

BaseIsolated=0

zBumpDebug=0.0

numDOF=6
rcdofs=[1,1,2,2,3,3,4,4,5,5,6,6]
dofs=[1,2,3,4,5,6]
soildofs=[1,3]
FOAMySeesInstance.osi=ops.model('basic','-ndm',3,'-ndf',numDOF)


A=0.49*0.00064516
Iz=0.118*0.00064516*0.00064516
Iy=0.118*0.00064516*0.00064516
Jxx=0.237*0.00064516*0.00064516
E=29000*6895000 #ksi*conversion
G=E/(2*(1.3))
secTag=101
ops.section('Elastic', secTag, E, A, Iz, Iy, G, Jxx)

ops.beamIntegration('Lobatto', 3,secTag, 2)
# section('Elastic', secTag, E_mod, A, Iz, G_mod=None)
A=0.84*0.00064516
Iz=0.486*0.00064516*0.00064516
Iy=0.486*0.00064516*0.00064516
Jxx=0.796*0.00064516*0.00064516
E=29000*6895000 #ksi*conversion
G=E/(2*(1.3))
secTag=15
ops.section('Elastic', secTag, E, A, Iz, Iy, G, Jxx)


ops.beamIntegration('Lobatto', 2, secTag, 2)

## Materials
matTag=600
Fy=56*6895000 #ksi*conversion
E0=29000*6895000 #ksi*conversion
b=0.01
params=[18.00000, 0.92500, 0.15000]
ops.uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params)
matTag=601
Fy=50*6895000 #ksi*conversion
E0=29000*6895000 #ksi*conversion
b=0.01
params=[18.00000, 0.92500, 0.15000]
ops.uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params)

matTag=650
fpc=-7.2*6895000 #ksi*conversion
epsc0=-0.00326
fpcu=-1.44000*6895000 #ksi*conversion
epsU=-0.01631
lambda1=0.10000
ft=0.63640*6895000 #ksi*conversion
Ets=290.47375*6895000 #ksi*conversion
ops.uniaxialMaterial('Concrete02', matTag, fpc, epsc0, fpcu, epsU, lambda1, ft, Ets)
OuterRad=2
OuterDiam=OuterRad*2
CFTWallT=0.25

## Sections]
secTag=501
ops.section('Fiber', secTag, '-GJ', 10000000000.00000)

matTag=650
numSubdivCirc=8
numSubdivRad=8
center=[0.00000, 0.00000]
rad=[0.00000, (OuterRad-CFTWallT)*0.0254] #INCH*conversionToMeters
ang=[0.00000, 360.00000]
ops.patch('circ', matTag, numSubdivCirc, numSubdivRad, *center, *rad, *ang)

matTag=600
numSubdivCirc=8
numSubdivRad=4
center=[0.00000, 0.00000]
rad=[(OuterRad-CFTWallT)*0.0254, OuterRad*0.0254] #INCH*conversionToMeters
ang=[0.00000, 360.00000]
ops.patch('circ', matTag, numSubdivCirc, numSubdivRad, *center, *rad, *ang)
ops.beamIntegration('Lobatto', 1, secTag, 2)




# below Grade Beams

# SUB STORY COLUMNS
##################################################################################################################################################################


slabMass=1000

nElem=nElemBOTTOM
Zbase=zPileBase+ColumnConnectionLength
Ztop=zBase-ColumnConnectionLength
sectionLength=Ztop-Zbase
pileMass=sectionLength*7840*((0.5*OuterDiam*0.0254)**2 - (0.5*(OuterDiam-CFTWallT)*0.0254)**2)*(0.6180000)*3.141519 + 2400*((0.5*(OuterDiam-CFTWallT)*0.0254)**2)*3.141519

subStoryColumnNodes=[]

subStoryColumnBaseNodes=[]
pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]

ops.node(123456780,Xmin,Ymin,1.0) 
ops.node(123456781,Xmin,Ymax,1.0)
ops.node(123456782,Xmax,Ymax,1.0)
ops.node(123456783,Xmax,Ymin,1.0)
bottombottomnodes=[123456780,123456781,123456782,123456783]
pc=100
startElem=90000000
startNode=90000000
soilnodes=[]
for location in pileLocs:

	node1=[location[0], location[1],  Zbase]
	node2=[location[0], location[1], Ztop]

	beamNormal=[-1,0,0]
	startElem+=pc
	startNode+=pc
	count=0
	xNodeList=np.linspace(node1[0],node2[0],nElemBOTTOM+1)
	yNodeList=np.linspace(node1[1],node2[1],nElemBOTTOM+1)
	zNodeList=np.linspace(node1[2],node2[2],nElemBOTTOM+1)
	nodalMass=(pileMass)/len(xNodeList)

	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.node(nodeNum, xNodeList[nodeNum-pc*1000],yNodeList[nodeNum-pc*1000],zNodeList[nodeNum-pc*1000])
		
	coordTransf = 'Corotational'

	coordTransf='Linear'
	coordTransf='PDelta'
	#############################

	## Model
	subStoryColumnBaseNodes.append(pc*1000)

	subStoryColumnNodes.append(pc*1000+len(xNodeList)-1)

	nodRotMass=0.
	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])

	for nodeNum in range(1 + pc*1000, pc*1000+len(xNodeList)):
		ops.geomTransf(coordTransf, pc*1000+nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
		
		if beamType=='elastic':
			ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, 501, pc*1000+nodeNum+100000)
		elif beamType=='dispBeamCol':
			ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum],pc*1000+nodeNum+100000, 1,'-mass', 3000)
		elif beamType=='forceBeamCol':
			ops.element('forceBeamColumn', pc*1000+nodeNum, *[nodeNum-1, nodeNum], pc*1000+nodeNum+100000, 1)		
		elif beamType=='NLBeamCol':
			ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,pc*1000+nodeNum+100000,'-iter', 1)
	pc+=1
ct=0



# FIRST STORY COLUMNS
##################################################################################################################################################################

slabMass=1000

nElem=nElemBOTTOM
Zbase=zBase
Ztop=z1stFloor
sectionLength=Ztop-Zbase
pileMass=sectionLength*7840*((0.5*OuterDiam*0.0254)**2 - (0.5*(OuterDiam-CFTWallT)*0.0254)**2)*(0.6180000)*3.141519 + 2400*((0.5*(OuterDiam-CFTWallT)*0.0254)**2)*3.141519


firstStoryColumnNodes=[]
firstStoryColumnBaseNodes=[]

pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]




pc=1000
for location in pileLocs:

	node1=[location[0], location[1],  Zbase]
	node2=[location[0], location[1], Ztop]

	beamNormal=[-1,0,0]


	xNodeList=np.linspace(node1[0],node2[0],nElem2nd+1)
	yNodeList=np.linspace(node1[1],node2[1],nElem2nd+1)
	zNodeList=np.linspace(node1[2],node2[2],nElem2nd+1)
	nodalMass=(pileMass)/len(xNodeList)

	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.node(nodeNum, xNodeList[nodeNum-pc*1000],yNodeList[nodeNum-pc*1000],zNodeList[nodeNum-pc*1000])
		FOAMySeesInstance.coupledNodes.append(nodeNum)
	coordTransf = 'Corotational'

	coordTransf='Linear'
	coordTransf='PDelta'
	#############################

	## Model
	firstStoryColumnBaseNodes.append(pc*1000)

	firstStoryColumnNodes.append(pc*1000+len(xNodeList)-1)

	nodRotMass=0.
	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])

	for nodeNum in range(1 + pc*1000, pc*1000+len(xNodeList)):
		ops.geomTransf(coordTransf, pc*1000+nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
		
		if beamType=='elastic':
			ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, 501, pc*1000+nodeNum+100000)
		elif beamType=='dispBeamCol':
			ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum],pc*1000+nodeNum+100000, 1,'-mass', 3000)
		elif beamType=='forceBeamCol':
			ops.element('forceBeamColumn', nodeNum, *[nodeNum-1, nodeNum], pc*1000+nodeNum+100000, 1)		
		elif beamType=='NLBeamCol':
			ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,pc*1000+nodeNum+100000,'-iter', 1)
	pc+=1
    
ct=0

StrainGaugeElements=[]


bottombottomnodes=[123456780,123456781,123456782,123456783]

# beamEndNode=firstSlabCornerNodeNums[-1][0]
for corner in bottombottomnodes:
	columnTopNode=subStoryColumnBaseNodes[ct]
	print(columnTopNode,'columnTopNode')
	columnBottomNode=corner
	print(columnBottomNode,'columnBottomNode')
	ct+=1	
	beamNormal=[-1,0,0]
	ops.geomTransf(coordTransf, pc*1000+ct+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	nodeNum+=1

	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, columnBottomNode, columnTopNode, 501, pc*1000+ct+100000)  		
	elif beamType=='dispBeamCol':
  		ops.element('dispBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],pc*1000+ct+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
  		ops.element('forceBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode], pc*1000+ct+100000, 1)		
	elif beamType=='NLBeamCol':
  		ops.element('nonlinearBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],3,secTag,pc*1000+ct+100000,'-iter', 1)
	StrainGaugeElements.append(nodeNum)
ct=0
pc+=1
# beamEndNode=firstSlabCornerNodeNums[-1][0]
for corner in subStoryColumnNodes:
	columnTopNode=firstStoryColumnBaseNodes[ct]
	print(columnTopNode,'columnTopNode')
	columnBottomNode=corner
	print(columnBottomNode,'columnBottomNode')
	ct+=1	
	beamNormal=[-1,0,0]
	ops.geomTransf(coordTransf, pc*1000+ct+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	nodeNum+=1

	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, columnBottomNode, columnTopNode, 501, pc*1000+ct+100000)  		
	elif beamType=='dispBeamCol':
  		ops.element('dispBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],pc*1000+ct+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
  		ops.element('forceBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode], pc*1000+ct+100000, 1)		
	elif beamType=='NLBeamCol':
  		ops.element('nonlinearBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],3,secTag,pc*1000+ct+100000,'-iter', 1)
	StrainGaugeElements.append(nodeNum)

numEigenvalues=1
#print('Eigen ',ops.eigen('-genBandArpack', numEigenvalues))

# render the model after defining all the nodes and elements
#vfo.plot_model()




firstStoryBeamEndNodes=[]
	
	

print('I am here beams are made')

#vfo.plot_model()


# 2nd STORY COLUMNS
##################################################################################################################################################################



Zbase=z1stFloor

Ztop=z2ndFloor
sectionLength=Ztop-Zbase
pileMass=sectionLength*7840*((0.5*OuterDiam*0.0254)**2 - (0.5*(OuterDiam-CFTWallT)*0.0254)**2)*(0.6180000)*3.141519 + 2400*((0.5*(OuterDiam-CFTWallT)*0.0254)**2)*3.141519


secondStoryColumnTopNodes=[]

secondStoryColumnBaseNodes=[]
pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]

pc=5
for location in pileLocs:

	node1=[location[0], location[1],  Zbase+ColumnConnectionLength]
	node2=[location[0], location[1], Ztop]

	beamNormal=[-1,0,0]


	xNodeList=np.linspace(node1[0],node2[0],nElem2nd+1)
	yNodeList=np.linspace(node1[1],node2[1],nElem2nd+1)
	zNodeList=np.linspace(node1[2],node2[2],nElem2nd+1)
	nodalMass=(pileMass)/len(xNodeList)

	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.node(nodeNum, xNodeList[nodeNum-pc*1000],yNodeList[nodeNum-pc*1000],zNodeList[nodeNum-pc*1000])
		FOAMySeesInstance.coupledNodes.append(nodeNum)

	coordTransf = 'Corotational'

	coordTransf='Linear'
	coordTransf='PDelta'
	#############################

	## Model
	secondStoryColumnBaseNodes.append(pc*1000)
	secondStoryColumnTopNodes.append(pc*1000+len(xNodeList)-1)



	nodRotMass=0.
	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])

	for nodeNum in range(1 + pc*1000, pc*1000+len(xNodeList)):
		ops.geomTransf(coordTransf, pc*1000+nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
		
		if beamType=='elastic':
			ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, 501, pc*1000+nodeNum+100000)
		elif beamType=='dispBeamCol':
			ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum],pc*1000+nodeNum+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
		elif beamType=='forceBeamCol':
			ops.element('forceBeamColumn', pc*1000+nodeNum, *[nodeNum-1, nodeNum], pc*1000+nodeNum+100000, 1)		
		elif beamType=='NLBeamCol':
			ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,pc*1000+nodeNum+100000,'-iter', 1)
	pc+=1

nodeNum+=1
ct=0
secondStoryColumnBaseNodes.append(secondStoryColumnBaseNodes[0])
secondStoryColumnTopNodes.append(secondStoryColumnTopNodes[0])

# beamEndNode=firstSlabCornerNodeNums[-1][0]
for corner in firstStoryColumnNodes:
	columnTopNode=secondStoryColumnBaseNodes[ct]
	print(columnTopNode,'columnTopNode')
	columnBottomNode=corner
	print(columnBottomNode,'columnBottomNode')
	ct+=1	
	beamNormal=[-1,0,0]
	ops.geomTransf(coordTransf, pc*1000+ct+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	nodeNum+=1

	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, columnBottomNode, columnTopNode, 501, pc*1000+ct+100000)  		
	elif beamType=='dispBeamCol':
  		ops.element('dispBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],pc*1000+ct+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
  		ops.element('forceBeamColumn', pc*1000+ct, *[ columnBottomNode, columnTopNode], pc*1000+ct+100000, 1)		
	elif beamType=='NLBeamCol':
  		ops.element('nonlinearBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],3,secTag,pc*1000+ct+100000,'-iter', 1)





ct+=1


numEigenvalues=1
# print('Eigen ',ops.eigen('-genBandArpack', numEigenvalues))

# render the model after defining all the nodes and elements
#vfo.plot_model()






integTag=15
	


thirdStoryColumnTopNodes=[]

thirdStoryColumnBaseNodes=[]
	
ops.beamIntegration('Lobatto', integTag, secTag, 2)
slabMass=1000

# 3rd STORY COLUMNS
##################################################################################################################################################################


Zbase=z2ndFloor+ColumnConnectionLength
#Ztop=1.8288
Ztop=z3rdFloor
sectionLength=Ztop-Zbase
pileMass=sectionLength*7840*((0.5*OuterDiam*0.0254)**2 - (0.5*(OuterDiam-CFTWallT)*0.0254)**2)*(0.6180000)*3.141519 + 2400*((0.5*(OuterDiam-CFTWallT)*0.0254)**2)*3.141519


thirdStoryColumnTopNodes=[]

thirdStoryColumnBaseNodes=[]
pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]

pc=25
for location in pileLocs:

	node1=[location[0], location[1],  Zbase]
	node2=[location[0], location[1], Ztop]

	beamNormal=[-1,0,0]


	xNodeList=np.linspace(node1[0],node2[0],nElem2nd+1)
	yNodeList=np.linspace(node1[1],node2[1],nElem2nd+1)
	zNodeList=np.linspace(node1[2],node2[2],nElem2nd+1)
	nodalMass=(pileMass)/len(xNodeList)

	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.node(nodeNum, xNodeList[nodeNum-pc*1000],yNodeList[nodeNum-pc*1000],zNodeList[nodeNum-pc*1000])
		FOAMySeesInstance.coupledNodes.append(nodeNum)

	coordTransf = 'Corotational'

	coordTransf='Linear'
	coordTransf='PDelta'
	#############################

	## Model
	thirdStoryColumnBaseNodes.append(pc*1000)
	thirdStoryColumnTopNodes.append(pc*1000+len(xNodeList)-1)



	nodRotMass=0.
	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])

	for nodeNum in range(1 + pc*1000, pc*1000+len(xNodeList)):
		ops.geomTransf(coordTransf, pc*1000+nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
		
		if beamType=='elastic':
			ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, 501, pc*1000+nodeNum+100000)
		elif beamType=='dispBeamCol':
			ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum],pc*1000+nodeNum+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
		elif beamType=='forceBeamCol':
			ops.element('forceBeamColumn', pc*1000+nodeNum, *[nodeNum-1, nodeNum], pc*1000+nodeNum+100000, 1)		
		elif beamType=='NLBeamCol':
			ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,pc*1000+nodeNum+100000,'-iter', 1)
	pc+=1

nodeNum+=1
ct=0
thirdStoryColumnBaseNodes.append(thirdStoryColumnBaseNodes[0])
thirdStoryColumnTopNodes.append(thirdStoryColumnTopNodes[0])

# beamEndNode=firstSlabCornerNodeNums[-1][0]
for corner in secondStoryColumnTopNodes:
	columnTopNode=thirdStoryColumnBaseNodes[ct]
	print(columnTopNode,'columnTopNode')
	columnBottomNode=corner
	print(columnBottomNode,'columnBottomNode')
	ct+=1	
	beamNormal=[-1,0,0]
	ops.geomTransf(coordTransf, pc*1000+ct+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	nodeNum+=1

	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, columnBottomNode, columnTopNode, 501, pc*1000+ct+100000)  		
	elif beamType=='dispBeamCol':
  		ops.element('dispBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],pc*1000+ct+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
  		ops.element('forceBeamColumn', pc*1000+ct, *[ columnBottomNode, columnTopNode], pc*1000+ct+100000, 1)		
	elif beamType=='NLBeamCol':
  		ops.element('nonlinearBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],3,secTag,pc*1000+ct+100000,'-iter', 1)


#vfo.plot_model()



#vfo.plot_model()
# TOP STORY COLUMNS
##################################################################################################################################################################

Zbase=z3rdFloor+ColumnConnectionLength
#Ztop=1.8288
Ztop=z4thFloor
sectionLength=Ztop-Zbase
pileMass=sectionLength*7840*((0.5*OuterDiam*0.0254)**2 - (0.5*(OuterDiam-CFTWallT)*0.0254)**2)*(0.6180000)*3.141519 + 2400*((0.5*(OuterDiam-CFTWallT)*0.0254)**2)*3.141519



topStoryColumnBaseNodes=[]

topStoryColumnTopNodes=[]


pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]

pc=35
for location in pileLocs:

	node1=[location[0], location[1],  Zbase]
	node2=[location[0], location[1], Ztop]

	beamNormal=[-1,0,0]


	xNodeList=np.linspace(node1[0],node2[0],nElemTOP+1)
	yNodeList=np.linspace(node1[1],node2[1],nElemTOP+1)
	zNodeList=np.linspace(node1[2],node2[2],nElemTOP+1)
	nodalMass=(pileMass)/len(xNodeList)

	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.node(nodeNum, xNodeList[nodeNum-pc*1000],yNodeList[nodeNum-pc*1000],zNodeList[nodeNum-pc*1000])
		FOAMySeesInstance.coupledNodes.append(nodeNum)

	coordTransf = 'Corotational'

	coordTransf='Linear'
	coordTransf='PDelta'
	#############################

	## Model
	topStoryColumnBaseNodes.append(pc*1000)
	topStoryColumnTopNodes.append(pc*1000+len(xNodeList)-1)



	nodRotMass=0.
	for nodeNum in range(pc*1000, pc*1000+len(xNodeList)):
		ops.mass(nodeNum,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])

	for nodeNum in range(1 + pc*1000, pc*1000+len(xNodeList)):
		ops.geomTransf(coordTransf, pc*1000+nodeNum+100000, beamNormal[0],beamNormal[1],beamNormal[2])
		
		if beamType=='elastic':
			ops.element('elasticBeamColumn', nodeNum, nodeNum-1, nodeNum, 501, pc*1000+nodeNum+100000)
		elif beamType=='dispBeamCol':
			ops.element('dispBeamColumn', nodeNum, *[nodeNum-1, nodeNum],pc*1000+nodeNum+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
		elif beamType=='forceBeamCol':
			ops.element('forceBeamColumn', pc*1000+nodeNum, *[nodeNum-1, nodeNum], pc*1000+nodeNum+100000, 1)		
		elif beamType=='NLBeamCol':
			ops.element('nonlinearBeamColumn', nodeNum, *[nodeNum-1, nodeNum],3,secTag,pc*1000+nodeNum+100000,'-iter', 1)
	pc+=1

ct=0
topStoryColumnBaseNodes.append(topStoryColumnBaseNodes[0])
topStoryColumnTopNodes.append(topStoryColumnTopNodes[0])

# beamEndNode=firstSlabCornerNodeNums[-1][0]
for corner in thirdStoryColumnTopNodes:
	columnTopNode=topStoryColumnBaseNodes[ct]
	print(columnTopNode,'columnTopNode')
	columnBottomNode=corner
	print(columnBottomNode,'columnBottomNode')
	ct+=1	
	beamNormal=[-1,0,0]
	ops.geomTransf(coordTransf, pc*1000+ct+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	nodeNum+=1

	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, columnBottomNode, columnTopNode, 501, pc*1000+ct+100000)  		
	elif beamType=='dispBeamCol':
  		ops.element('dispBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],pc*1000+ct+100000, 1)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
  		ops.element('forceBeamColumn', pc*1000+ct, *[ columnBottomNode, columnTopNode], pc*1000+ct+100000, 1)		
	elif beamType=='NLBeamCol':
  		ops.element('nonlinearBeamColumn', nodeNum, *[ columnBottomNode, columnTopNode],3,secTag,pc*1000+ct+100000,'-iter', 1)


BeamCenterNodesFirstFloor=[]
firstStoryColumnNodes.append(firstStoryColumnNodes[0])
ct=0
Gct=0
NnumMiddleStart=10000000
for nodeCurrent in firstStoryColumnNodes[0:4]:
	node2=firstStoryColumnNodes[ct+1]
	node1=nodeCurrent
	print(nodeCurrent)
	node1Loc=ops.nodeCoord(node1)
	node2Loc=ops.nodeCoord(node2)
    
    
    
	middleLoc=(np.array(node2Loc)+np.array(node1Loc))/2
    
	beamNormal=np.cross(np.array(node2Loc)-np.array(node1Loc),[0,0,1])
    

    
	ops.node(NnumMiddleStart, middleLoc[0],middleLoc[1],middleLoc[2])
	BeamCenterNodesFirstFloor.append(NnumMiddleStart)
	ops.geomTransf(coordTransf, pc*1000+NnumMiddleStart+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node2, NnumMiddleStart, 15, pc*1000+NnumMiddleStart+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],pc*1000+NnumMiddleStart+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node2, NnumMiddleStart], pc*1000+NnumMiddleStart+100000, 2)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],3,15,pc*1000+NnumMiddleStart+100000,'-iter', 1)	   

	NnumMiddleStart+=1	
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node1, (NnumMiddleStart-1), 15, pc*1000+(NnumMiddleStart-1)+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],pc*1000+(NnumMiddleStart-1)+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node1, (NnumMiddleStart-1)], pc*1000+(NnumMiddleStart-1)+100000, 1)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],3,15,pc*1000+(NnumMiddleStart-1)+100000,'-iter', 1)	   
	NnumMiddleStart+=1   	
	ct+=1		  
	#vfo.plot_model()


BeamCenterNodesSecondFloor=[]

ct=0
NnumMiddleStart=20000000
for nodeCurrent in secondStoryColumnTopNodes[0:4]:
	node2=secondStoryColumnTopNodes[ct+1]
	node1=nodeCurrent
	print(nodeCurrent)
	node1Loc=ops.nodeCoord(node1)
	node2Loc=ops.nodeCoord(node2)
	middleLoc=(np.array(node2Loc)+np.array(node1Loc))/2

	beamNormal=np.cross(np.array(node2Loc)-np.array(node1Loc),[0,0,1])
    
	print(NnumMiddleStart,middleLoc,beamNormal) 
	ops.node(NnumMiddleStart, middleLoc[0],middleLoc[1],middleLoc[2])
	ops.mass(NnumMiddleStart,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])
	BeamCenterNodesSecondFloor.append(NnumMiddleStart)
	ops.geomTransf(coordTransf, pc*1000+NnumMiddleStart+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node2, NnumMiddleStart, 15, pc*1000+NnumMiddleStart+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],pc*1000+NnumMiddleStart+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node2, NnumMiddleStart], pc*1000+NnumMiddleStart+100000, 2)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],3,15,pc*1000+NnumMiddleStart+100000,'-iter', 1)	   



	NnumMiddleStart+=1	
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node1, (NnumMiddleStart-1), 15, pc*1000+(NnumMiddleStart-1)+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],pc*1000+(NnumMiddleStart-1)+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node1, (NnumMiddleStart-1)], pc*1000+(NnumMiddleStart-1)+100000, 1)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],3,15,pc*1000+(NnumMiddleStart-1)+100000,'-iter', 1)	   
	NnumMiddleStart+=1   			  
	#vfo.plot_model()

  
	ct+=1
    
BeamCenterNodesThirdFloor=[]

ct=0
NnumMiddleStart=30000000
for nodeCurrent in thirdStoryColumnTopNodes[0:4]:
	node2=thirdStoryColumnTopNodes[ct+1]
	node1=nodeCurrent
	print(nodeCurrent)
    
    
	node1Loc=ops.nodeCoord(node1)
	node2Loc=ops.nodeCoord(node2)
    
    
	middleLoc=(np.array(node2Loc)+np.array(node1Loc))/2

	beamNormal=np.cross(np.array(node2Loc)-np.array(node1Loc),[0,0,1])
    
	print(NnumMiddleStart,middleLoc,beamNormal) 
	ops.node(NnumMiddleStart, middleLoc[0],middleLoc[1],middleLoc[2])
	ops.mass(NnumMiddleStart,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])
	BeamCenterNodesThirdFloor.append(NnumMiddleStart)
	ops.geomTransf(coordTransf, pc*1000+NnumMiddleStart+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node2, NnumMiddleStart, 15, pc*1000+NnumMiddleStart+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],pc*1000+NnumMiddleStart+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node2, NnumMiddleStart], pc*1000+NnumMiddleStart+100000, 2)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],3,15,pc*1000+NnumMiddleStart+100000,'-iter', 1)	   

	NnumMiddleStart+=1	
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node1, (NnumMiddleStart-1), 15, pc*1000+(NnumMiddleStart-1)+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],pc*1000+(NnumMiddleStart-1)+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node1, (NnumMiddleStart-1)], pc*1000+(NnumMiddleStart-1)+100000, 1)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],3,15,pc*1000+(NnumMiddleStart-1)+100000,'-iter', 1)	   
	NnumMiddleStart+=1   			  

	ct+=1 

BeamCenterNodesTopFloor=[]
ct=0
NnumMiddleStart=40000000
for nodeCurrent in topStoryColumnTopNodes[0:4]:
	node2=topStoryColumnTopNodes[ct+1]
	node1=nodeCurrent
	print(nodeCurrent)
	node1Loc=ops.nodeCoord(node1)
	node2Loc=ops.nodeCoord(node2)
	middleLoc=(np.array(node2Loc)+np.array(node1Loc))/2

	beamNormal=np.cross(np.array(node2Loc)-np.array(node1Loc),[0,0,1])
    
	print(NnumMiddleStart,middleLoc,beamNormal) 
	ops.node(NnumMiddleStart, middleLoc[0],middleLoc[1],middleLoc[2])
	ops.mass(NnumMiddleStart,*[nodalMass,nodalMass,nodalMass,nodRotMass,nodRotMass,nodRotMass])
	BeamCenterNodesTopFloor.append(NnumMiddleStart)
	ops.geomTransf(coordTransf, pc*1000+NnumMiddleStart+100000, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node2, NnumMiddleStart, 15, pc*1000+NnumMiddleStart+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],pc*1000+NnumMiddleStart+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node2, NnumMiddleStart], pc*1000+NnumMiddleStart+100000, 2)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node2, NnumMiddleStart],3,15,pc*1000+NnumMiddleStart+100000,'-iter', 1)	   



	NnumMiddleStart+=1	
	if beamType=='elastic':
		ops.element('elasticBeamColumn', NnumMiddleStart, node1, (NnumMiddleStart-1), 15, pc*1000+(NnumMiddleStart-1)+100000)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],pc*1000+(NnumMiddleStart-1)+100000, 2)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+NnumMiddleStart, *[node1, (NnumMiddleStart-1)], pc*1000+(NnumMiddleStart-1)+100000, 1)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', NnumMiddleStart, *[node1,(NnumMiddleStart-1)],3,15,pc*1000+(NnumMiddleStart-1)+100000,'-iter', 1)	   
	NnumMiddleStart+=1   			  
	#vfo.plot_model()
	ct+=1



print('I am here columns are made')
#vfo.plot_model()


Zbase=zBase
Ztop=z1stFloor


pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]

if useSlabs==1:
	# Breakaway first STORY SLAB
	##################################################################################################################################################################
	zBumpDebug=0.0
	pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]
	eleType='shell'
	eleArgs=[100]

	matTag=625

	h=0.0254*1/2	 #SLAB THICKNESS IN METERS> WHAT IS THIS? CHECK KENS THESIS

	nu=0.3

	E=8e9 #plywood panel

	E=2e11 #steel panel

	rho=1000   #SLAB DENSITY > WHAT IS THIS? CHECK KENS THESIS

	ops.nDMaterial('ElasticIsotropic', matTag, E, nu)

	secTag=100

	ops.section('ElasticMembranePlateSection', secTag, E, nu, h, rho)


	coooords=[1,pileLocs[0][0],pileLocs[0][1],pileLocs[0][2],2,pileLocs[1][0],pileLocs[1][1],pileLocs[1][2],3,pileLocs[2][0],pileLocs[2][1],pileLocs[2][2],4, pileLocs[3][0],pileLocs[3][1],pileLocs[3][2]]


	# block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *crds)
	eleType='shell'
	eleArgs=[100]
	startNode=1
	startEle=1

	ops.block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *coooords)
	firstSlabCornerNodeNums=[startNode,startNode+numX, -1 + startNode+(numX+1)*(numY+1),-1+startNode+(numX+1)*(numY+1) - numX]
	firstSlabEdgeMidNodeNums=[startNode+numY/2,startNode+(((numX+1)*(numY+1))-1)-(numX/2*(numY+1)), startNode+(((numX+1)*(numY+1))-1)-numY/2,startNode+(((numX+1)*(numY+1))-1)-((numX/2+1)*(numY+1))+1]

	SlabNodes=np.linspace(startNode,startNode+((numX+1)*(numY+1))-1,((numX+1)*(numY+1)))
	for nodeNum in SlabNodes:
		FOAMySeesInstance.coupledNodes.append(int(nodeNum))



#vfo.plot_model()
Zbase=z1stFloor
#Ztop=1.8288
Ztop=z2ndFloor


if useSlabs==1:
	# 2nd STORY SLAB
	##################################################################################################################################################################

	zBumpDebug=0.0
	Ztop+=zBumpDebug
	pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]



	coooords=[1,pileLocs[0][0],pileLocs[0][1],pileLocs[0][2],2,pileLocs[1][0],pileLocs[1][1],pileLocs[1][2],3,pileLocs[2][0],pileLocs[2][1],pileLocs[2][2],4, pileLocs[3][0],pileLocs[3][1],pileLocs[3][2]]


	# block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *crds)
	eleType='shell'
	eleArgs=[100]
	startNode=1000
	startEle=1000

	ops.block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *coooords)
	secondSlabCornerNodeNums=[startNode,startNode+numX, -1 + startNode+(numX+1)*(numY+1),-1+startNode+(numX+1)*(numY+1) - numX]
	secondSlabEdgeMidNodeNums=[startNode+numY/2,startNode+(((numX+1)*(numY+1))-1)-(numX/2*(numY+1)), startNode+(((numX+1)*(numY+1))-1)-numY/2,startNode+(((numX+1)*(numY+1))-1)-((numX/2+1)*(numY+1))+1]



#vfo.plot_model()	
Zbase=z2ndFloor
#Ztop=1.8288
Ztop=z3rdFloor


if useSlabs==1:
	# Third STORY SLAB
	##################################################################################################################################################################

	zBumpDebug=0.0
	Ztop+=zBumpDebug

	pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]




	coooords=[1,pileLocs[0][0],pileLocs[0][1],pileLocs[0][2],2,pileLocs[1][0],pileLocs[1][1],pileLocs[1][2],3,pileLocs[2][0],pileLocs[2][1],pileLocs[2][2],4, pileLocs[3][0],pileLocs[3][1],pileLocs[3][2]]



	# block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *crds)
	eleType='shell'
	eleArgs=[100]
	startNode=222000
	startEle=222000

	ops.block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *coooords)
	thirdSlabCornerNodeNums=[startNode,startNode+numX, -1 + startNode+(numX+1)*(numY+1),-1+startNode+(numX+1)*(numY+1) - numX]
	thirdSlabEdgeMidNodeNums=[startNode+numY/2,startNode+(((numX+1)*(numY+1))-1)-(numX/2*(numY+1)), startNode+(((numX+1)*(numY+1))-1)-numY/2,startNode+(((numX+1)*(numY+1))-1)-((numX/2+1)*(numY+1))+1]

ct=0

    
Zbase=z3rdFloor
#Ztop=1.8288
Ztop=z4thFloor


if useSlabs==1:
	# Top STORY SLAB
	##################################################################################################################################################################

	zBumpDebug=0.0
	Ztop+=zBumpDebug

	pileLocs=[[Xmin,Ymin,Ztop],[Xmin,Ymax,Ztop],[Xmax,Ymax,Ztop],[Xmax,Ymin,Ztop]]




	coooords=[1,pileLocs[0][0],pileLocs[0][1],pileLocs[0][2],2,pileLocs[1][0],pileLocs[1][1],pileLocs[1][2],3,pileLocs[2][0],pileLocs[2][1],pileLocs[2][2],4, pileLocs[3][0],pileLocs[3][1],pileLocs[3][2]]



	# block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *crds)
	eleType='shell'
	eleArgs=[100]
	startNode=1222000
	startEle=1222000
	ops.block2D(numX, numY, startNode, startEle, eleType, *eleArgs, *coooords)
	topSlabCornerNodeNums=[startNode,startNode+numX, -1 + startNode+(numX+1)*(numY+1),-1+startNode+(numX+1)*(numY+1) - numX]
	topSlabEdgeMidNodeNums=[startNode+numY/2,startNode+(((numX+1)*(numY+1))-1)-(numX/2*(numY+1)), startNode+(((numX+1)*(numY+1))-1)-numY/2,startNode+(((numX+1)*(numY+1))-1)-((numX/2+1)*(numY+1))+1]


ct=0
for corner in firstSlabCornerNodeNums:
	columnTopNode=firstStoryColumnNodes[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1

ct=0
for corner in secondSlabCornerNodeNums:
	columnTopNode=secondStoryColumnTopNodes[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1
    
ct=0
for corner in thirdSlabCornerNodeNums:
	columnTopNode=thirdStoryColumnTopNodes[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1

ct=0
for corner in topSlabCornerNodeNums:
	columnTopNode=topStoryColumnTopNodes[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1


ct=0
for corner in firstSlabEdgeMidNodeNums:
	columnTopNode=BeamCenterNodesFirstFloor[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1

ct=0
for corner in secondSlabEdgeMidNodeNums:
	columnTopNode=BeamCenterNodesSecondFloor[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1
    
ct=0
for corner in thirdSlabEdgeMidNodeNums:
	columnTopNode=BeamCenterNodesThirdFloor[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1

ct=0
for corner in topSlabEdgeMidNodeNums:
	columnTopNode=BeamCenterNodesTopFloor[ct]
	beamStartNode=corner
	rNodeTag=columnTopNode
	cNodeTag=beamStartNode
	if constraintType=='EQDOF': 
		ops.equalDOF(rNodeTag, cNodeTag, *dofs)
	elif constraintType=='RIGIDLINK':	
		ops.rigidLink('bar', rNodeTag, cNodeTag)
	elif constraintType=='EQDOFMIXED':
		ops.equalDOF_Mixed(rNodeTag, cNodeTag, numDOF, *rcdofs)
	ct+=1



#vfo.plot_model()
# if useBeams==1:

    
if noBraces==1:
	pass
else:
	############### Chevron braces #####################


	# corner nodes nElemBOTTOM  x 1000+nElemBOTTOM  y  2000+nElemBOTTOM  x  3000+nElemBOTTOM   y   nElemBOTTOM

	# mid nodes			   20000+numX/2	 21000+numX/2	 22000+numX/2		  23000+numX/2
			
	pc+=1

	CT=101010101
	eleNo=CT
	beamNormal=[1,0,0]
	nodeNum+=1	
	ops.beamIntegration('Lobatto', 16, secTag, 2)
	Nodes=[25000,BeamCenterNodesThirdFloor[0]]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
		
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    
	nodeNum+=1
	CT=101010102
	eleNo=CT
	beamNormal=[1,0,0]
	Nodes=[BeamCenterNodesThirdFloor[0],26000]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
		
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1

	nodeNum+=1
	CT=101010105
	eleNo=CT
	beamNormal=[0,1,0]
	Nodes=[26000,BeamCenterNodesThirdFloor[1]]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
		
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    
	nodeNum+=1
	CT=101010106
	eleNo=CT
	beamNormal=[0,1,0]
	Nodes=[BeamCenterNodesThirdFloor[1],27000]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    


	nodeNum+=1
	CT=101010103
	eleNo=CT
	beamNormal=[1,0,0]
	Nodes=[27000,BeamCenterNodesThirdFloor[2]]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    

	nodeNum+=1
	CT=101010104
	eleNo=CT
	beamNormal=[1,0,0]
	Nodes=[BeamCenterNodesThirdFloor[2],28000]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    
	nodeNum+=1
	CT=101010107
	eleNo=CT
	beamNormal=[0,1,0]
	Nodes=[28000,BeamCenterNodesThirdFloor[3]]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1

	nodeNum+=1
	CT=101010108
	eleNo=CT
	beamNormal=[0,1,0]
	Nodes=[BeamCenterNodesThirdFloor[3],25000]
	TransfTag=pc*1000+nodeNum+100000
	ops.geomTransf(coordTransf, TransfTag, beamNormal[0],beamNormal[1],beamNormal[2])
	if beamType=='elastic':
		ops.element('elasticBeamColumn', nodeNum, Nodes[0], Nodes[1], 101, TransfTag)  		
	elif beamType=='dispBeamCol':
		ops.element('dispBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		 #, '-cMass', '-mass', mass=0.0)
	elif beamType=='forceBeamCol':
		ops.element('forceBeamColumn', pc*1000+nodeNum, *[Nodes[0], Nodes[1]],TransfTag, 3)		
	elif beamType=='NLBeamCol':
		ops.element('nonlinearBeamColumn', nodeNum, *[Nodes[0], Nodes[1]],3,101,TransfTag,'-iter', 1)	   
		pc+=1
    


#vfo.plot_model()	
print(FOAMySeesInstance.coupledNodes)

if BaseIsolated==1:
	###############################################################################################################################################
	#   BASE ISOLATOR ELEMENTS #
	###############################################################################################################################################



	ops.node(9000000, *[Xmin,Ymin,zBase])
	ops.node(9001000, *[Xmin,Ymax,zBase])
	ops.node(9002000, *[Xmax,Ymax,zBase])
	ops.node(9003000, *[Xmax,Ymin,zBase])


	# eleTag=			 #(int)	unique element object tag
	# eleNodes=		   #(list (int))	a list of two element nodes

	kInit=50000			  #(float)	initial elastic stiffness in local shear direction
	qd=500				 #(float)	characteristic strength
	alpha1=0.01			#(float)	post yield stiffness ratio of linear hardening component
	alpha2=0.1			 #(float)	post yield stiffness ratio of non-linear hardening component
	mu=2				#(float)	exponent of non-linear hardening component

	matTag=222
	E=100000
	ops.uniaxialMaterial('Elastic', matTag, E) #, eta=0.0, Eneg=E)

	PMatTag=222			#(int)	tag associated with previously-defined UniaxialMaterial in axial direction
	TMatTag=222			#(int)	tag associated with previously-defined UniaxialMaterial in torsional direction
	MyMatTag=222		   #(int)	tag associated with previously-defined UniaxialMaterial in moment direction around local y-axis
	MzMatTag=222		   #(int)	tag associated with previously-defined UniaxialMaterial in moment direction around local z-axis

	# x1 x2 x3 (float)	vector components in global coordinates defining local x-axis (optional)
	# y1 y2 y3 (float)	vector components in global coordinates defining local y-axis (optional)
	# sDratio (float)	shear distance from iNode as a fraction of the element length (optional, default = 0.5)
	# '-doRayleigh' (str)	to include Rayleigh damping from the bearing (optional, default = no Rayleigh damping contribution)
	# m (float)	element mass (optional, default = 0.0)



	ops.element('elastomericBearingPlasticity', 9000001, *[0, 9000000], kInit, qd, alpha1, alpha2, mu, '-P', PMatTag, '-T', TMatTag, '-My', MyMatTag, '-Mz', MzMatTag) #, <'-orient', <x1, x2, x3>, y1, y2, y3>, <'-shearDist', sDratio>, <'-doRayleigh'>, <'-mass', m>)
	ops.element('elastomericBearingPlasticity', 9000002, *[1000, 9001000], kInit, qd, alpha1, alpha2, mu, '-P', PMatTag, '-T', TMatTag, '-My', MyMatTag, '-Mz', MzMatTag) #, <'-orient', <x1, x2, x3>, y1, y2, y3>, <'-shearDist', sDratio>, <'-doRayleigh'>, <'-mass', m>)
	ops.element('elastomericBearingPlasticity', 9000003, *[2000, 9002000], kInit, qd, alpha1, alpha2, mu, '-P', PMatTag, '-T', TMatTag, '-My', MyMatTag, '-Mz', MzMatTag) #, <'-orient', <x1, x2, x3>, y1, y2, y3>, <'-shearDist', sDratio>, <'-doRayleigh'>, <'-mass', m>)
	ops.element('elastomericBearingPlasticity', 9000004, *[3000, 9003000], kInit, qd, alpha1, alpha2, mu, '-P', PMatTag, '-T', TMatTag, '-My', MyMatTag, '-Mz', MzMatTag) #, <'-orient', <x1, x2, x3>, y1, y2, y3>, <'-shearDist', sDratio>, <'-doRayleigh'>, <'-mass', m>)

	ops.fix(9000000,*[1,1,1,1,1,1])
	ops.fix(9001000,*[1,1,1,1,1,1])
	ops.fix(9002000,*[1,1,1,1,1,1])
	ops.fix(9003000,*[1,1,1,1,1,1])
else:
	pass


ops.fixZ(1.0,*[1,1,1,1,1,1])

ops.recorder('Node', '-file', 'frontRightCFTReactionAtFlumeFloor.out','-time', '-node', 1000000, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'frontLeftCFTReactionAtFlumeFloor.out','-time', '-node',1001000, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'backLeftCFTReactionAtFlumeFloor.out','-time', '-node', 1002000, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'backRightCFTReactionAtFlumeFloor.out','-time', '-node',1003000, '-dof', 1,2,3,4,5,6, 'reaction')


ops.recorder('Node', '-file', 'frontRightCFTReaction.out','-time', '-node', 123456780, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'frontLeftCFTReaction.out','-time', '-node',123456781, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'backLeftCFTReaction.out','-time', '-node', 123456782, '-dof', 1,2,3,4,5,6, 'reaction')
ops.recorder('Node', '-file', 'backRightCFTReaction.out','-time', '-node',123456783, '-dof', 1,2,3,4,5,6, 'reaction')
res=['disp','vel','accel','incrDisp','reaction','pressure','unbalancedLoad','mass']

ops.recorder('PVD', 'output', '-precision', 4, '-dT', .05, *res)
beep=0
for SGE in StrainGaugeElements:
    beep+=1
    ops.recorder('Element','-ele',SGE,'-file',str(beep)+'fiber.out','section','fiber',OuterRad,0,600,'stressStrain')

for soiln in soilnodes:
    
    ops.recorder('Node', '-file', 'SoilNode'+str(soiln)+'Reaction.out','-time', '-node',soiln, '-dof', 1,2,3,4,5,6, 'reaction')



#maxNumIter = 10

#Tol=1e-3

#ops.test('EnergyIncr', Tol, maxNumIter)
	
import numpy as np
from subprocess import Popen,DEVNULL
def buildBathymetry(bathType,secondaryInput,writeHere):
	print('Building Bathymetry')
	print("bathType,secondaryInput")
	print(bathType,secondaryInput)
	if bathType=="Point List":
		flumeWidth=secondaryInput[0]
		bathXZData=secondaryInput[1]
		bathpointsneg=[]
		bathpointspos=[]
		
		bathpointsneg.append([-bathXZData[0][0],-flumeWidth,bathXZData[0][1]])
		bathpointspos.append([-bathXZData[0][0],flumeWidth,bathXZData[0][1]])
			
		for xzBath in bathXZData:
			bathpointsneg.append([xzBath[0],-flumeWidth,xzBath[1]])
			bathpointspos.append([xzBath[0],flumeWidth,xzBath[1]])
			
		bathpointsneg.append([bathpointsneg[-1][0]*2,-flumeWidth,bathpointsneg[-1][2]])	
		bathpointspos.append([bathpointspos[-1][0]*2,flumeWidth,bathpointspos[-1][2]])


		trilist1=[]
		trilist2=[]
		normlist=[]

		bathSTLFile=['''solid auto2''']

		for x in range(0,len(bathpointsneg)-1):
			trilist1.append([bathpointsneg[x+1],bathpointsneg[x],bathpointspos[x]]) #tri 1
			trilist2.append([bathpointspos[x+1],bathpointsneg[x+1],bathpointspos[x]]) #tri 2
			vec3=-(np.array(bathpointspos[x+1][:]) - np.array(bathpointsneg[x+1][:]))
			vec4=-(np.array(bathpointspos[x+1][:]) - np.array(bathpointspos[x][:]))
			vec1=(np.array(bathpointspos[x][:]) - np.array(bathpointsneg[x][:]))
			vec2=(np.array(bathpointsneg[x+1][:]) - np.array(bathpointsneg[x][:]))
			
			bathSTLFile.append('''
		facet normal  {} {} {}		 
			outer loop
			   vertex {} {} {}
			   vertex {} {} {}
			   vertex {} {} {}
			endloop
		endfacet'''.format(np.cross(vec1, vec2)[0],np.cross(vec1, vec2)[1],np.cross(vec1, vec2)[2], bathpointsneg[x+1][0], bathpointsneg[x+1][1],  bathpointsneg[x+1][2], bathpointsneg[x][0],bathpointsneg[x][1],bathpointsneg[x][2], bathpointspos[x][0],bathpointspos[x][1],bathpointspos[x][2]))
			bathSTLFile.append('''
		facet normal  {} {} {}		 
			outer loop
			   vertex {} {} {}
			   vertex {} {} {}
			   vertex {} {} {}
			endloop
		endfacet'''.format(np.cross(vec3, vec4)[0],np.cross(vec3, vec4)[1],np.cross(vec3, vec4)[2], bathpointspos[x+1][0], bathpointspos[x+1][1],  bathpointspos[x+1][2], bathpointsneg[x+1][0],bathpointsneg[x+1][1],bathpointsneg[x+1][2], bathpointspos[x][0],bathpointspos[x][1],bathpointspos[x][2]))

		bathSTLFile.append('''
		endsolid
		''')


		with open(writeHere+'/constant/triSurface/flumeFloor.stl','w') as f:
			f.seek(0)
			for x in bathSTLFile:
				for line in x:
					f.write(line)
	else: 
		bathSurfaceFile=secondaryInput
		print('Surface file for bathymetry ',bathSurfaceFile)
		Popen("cp -rf "+bathSurfaceFile+" "+writeHere+"/constant/triSurface/flumeFloor.stl", shell=True, stdout=DEVNULL).wait()

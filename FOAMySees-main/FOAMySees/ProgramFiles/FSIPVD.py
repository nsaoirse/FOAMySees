import glob
F=glob.glob("SeesOutput/*")
P0Exists=0
P1Exists=0
P2Exists=0
P3Exists=0


F= [i.replace('SeesOutput/SeesOutput_T','') for i in F]

if any('P0' in x for x in F):
	F= [i.replace('_P0.vtu','') for i in F]
	P0Exists=1
if any('P1' in x for x in F):
	F= [i.replace('_P1.vtu','') for i in F]
	P1Exists=1
if any('P2' in x for x in F):
	F= [i.replace('_P2.vtu','') for i in F]
	P2Exists=1
if any('P3' in x for x in F):
	F= [i.replace('_P3.vtu','') for i in F]
	P3Exists=1	
	
F= [i.replace('.vtm','') for i in F]

F=set(F)

VTKFILE=['''<?xml version="1.0"?>
<VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  <Collection>
    ''']
for ff in F:

	if P0Exists==1:
		VTKFILE.append('''<DataSet timestep="{}" group="" part="0" file="SeesOutput/SeesOutput_T{}_P0.vtu"/>
		'''.format(ff,ff))
    
	if P1Exists==1:
		VTKFILE.append('''<DataSet timestep="{}" group="" part="1" file="SeesOutput/SeesOutput_T{}_P1.vtu"/>
		'''.format(ff,ff))
    
	if P2Exists==1:
		VTKFILE.append('''<DataSet timestep="{}" group="" part="2" file="SeesOutput/SeesOutput_T{}_P2.vtu"/>
		'''.format(ff,ff))
    
	if P3Exists==1:
		VTKFILE.append('''<DataSet timestep="{}" group="" part="3" file="SeesOutput/SeesOutput_T{}_P3.vtu"/>
		'''.format(ff,ff))
    
    
VTKFILE.append('''  </Collection>
</VTKFile>''')

with open('OpenSeesOutput.pvd','w') as f:
    f.seek(0)
    for x in VTKFILE:
        for line in x:
            f.write(line)
            f.truncate()


# VTKFILE=['''
# </VTKFile>
# <VTKFile type='vtkMultiBlockDataSet' version='1.0' byte_order='LittleEndian' header_type='UInt64' compressor="vtkZLibDataCompressor">
    # <vtkMultiBlockDataSet>''']

I=glob.glob("OpenFOAMCaseFolder/postProcessing/XSec1/*")

I= [i.replace('OpenFOAMCaseFolder/VTK/','') for i in I]
I= [i.replace('OpenFOAMCaseFolder_','') for i in I]

I= [i.replace('OpenFOAMCaseFolderBoundary_','') for i in I]
I= [i.replace('OpenFOAMCaseFolder_Boundary_','') for i in I]
I= [i.replace('OpenFOAMCaseFolder_Boundary','') for i in I]

I= [i.replace('Boundary','') for i in I]


I= [i.replace('OpenFOAMCaseFolder','') for i in I]

I= [i.replace('/postProcessing/XSec1/','') for i in I]

I= set([i.replace('yCut.vtp','') for i in I])

print(I)

#G.remove('')



# G2=['Fluid/VTK/Fluid_'+i+'.vtm' for i in G]

# print(G2)


# for ff in G2:
    # with open(ff.replace("Fluid_","FluidBoundary_"),'w') as f:
        # for line in open(ff,'r'):
            # if "name='internal'" in line:
                # pass
            # else:
                # print(line,file=f)

VTKFILE=['''<?xml version="1.0"?>
<VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  <Collection>''']

for ff in I:
    VTKFILE.append('''
    <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCaseFolder/postProcessing/XSec1/'''+str(ff)+'''/interpolatedSurface.vtp"/>''')
    
    
    
VTKFILE.append('''
  </Collection>

</VTKFile>''')
with open('InterpSurface.pvd','w') as f:
    f.seek(0)
    for x in VTKFILE:
        for line in x:
            f.write(line)
            f.truncate()


G=glob.glob("OpenFOAMCaseFolder/postProcessing/freeSurfaceVTK/*")

G= [i.replace('OpenFOAMCaseFolder/VTK/','') for i in G]
G= [i.replace('OpenFOAMCaseFolder_','') for i in G]

G= [i.replace('OpenFOAMCaseFolderBoundary_','') for i in G]
G= [i.replace('OpenFOAMCaseFolder_Boundary_','') for i in G]
G= [i.replace('OpenFOAMCaseFolder_Boundary','') for i in G]
G= [i.replace('Boundary','') for i in G]


G= [i.replace('OpenFOAMCaseFolder','') for i in G]

G= [i.replace('/postProcessing/freeSurfaceVTK/','') for i in G]

G= set([i.replace('yCut.vtp','') for i in G])

print(G)

#G.remove('')



# G2=['Fluid/VTK/Fluid_'+i+'.vtm' for i in G]

# print(G2)


# for ff in G2:
    # with open(ff.replace("Fluid_","FluidBoundary_"),'w') as f:
        # for line in open(ff,'r'):
            # if "name='internal'" in line:
                # pass
            # else:
                # print(line,file=f)

VTKFILE=['''<?xml version="1.0"?>
<VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  <Collection>''']

for ff in G:
    VTKFILE.append('''
    <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCaseFolder/postProcessing/freeSurfaceVTK/'''+str(ff)+'''/freeSurface.vtp"/>''')
    
    
    
VTKFILE.append('''
  </Collection>
</VTKFile>''')
with open('FreeSurface.pvd','w') as f:
    f.seek(0)
    for x in VTKFILE:
        for line in x:
            f.write(line)
            f.truncate()

  

# H=glob.glob("preCICE-output/*")

# H= [i.replace('preCICE-output/','') for i in H]
# H= [i.replace('.pvtu','') for i in H]
# H= [i.replace('_r32','') for i in H]
# H= [i.replace('_r31','') for i in H]
# H= [i.replace('_r30','') for i in H]
# H= [i.replace('_r25','') for i in H]
# H= [i.replace('_r26','') for i in H]
# H= [i.replace('_r36','') for i in H]
# H= [i.replace('_r32','') for i in H]
# H= [i.replace('_r33','') for i in H]
# H= [i.replace('_r34','') for i in H]
# H= [i.replace('_r35','') for i in H]
# H= [i.replace('_r36','') for i in H]


# H= [i.replace('Fluid-Mesh-Fluid','') for i in H]
# H= [i.replace('-Fluid','') for i in H]
# H= [i.replace('-Solid1','') for i in H]
# H= [i.replace('-Centers','') for i in H]
# H= [i.replace('-Nodes','') for i in H]
# H= [i.replace('-Displacement','') for i in H]
# H= [i.replace('-Force','') for i in H]
# H= [i.replace('Fluid-Mesh','') for i in H]
# H= [i.replace('Fluid-Mesh-Solid1','') for i in H]
# H= [i.replace('Solid1-Mesh','') for i in H]
# H= [i.replace('Solid1-Mesh-Fluid','') for i in H]
# H= [i.replace('.dt','') for i in H]
# H= [i.replace('vtk','') for i in H]
# H= [i.replace('vtu','') for i in H]
# H= [i.replace('_master','') for i in H]
# H= [i.replace('.','') for i in H]
# H= [i.replace('init','') for i in H]
# H= [i.replace('final','') for i in H]
# H= [i.replace('s','') for i in H]
# H= set([i.replace('.vtu','') for i in H])

# H.remove('')

# print(H)






# VTKFILE=['''<?xml version="1.0"?>
# <VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  # <Collection>''']

# for ff in ['.init']:
    # VTKFILE.append('''
# <DataSet timestep="0"  file="preCICE-output/Solid1-Mesh-Force-Fluid'''+str(ff)+'''_master.pvtu"/>''')

# for ff in ['.init']:
    # VTKFILE.append('''
# <DataSet timestep="0"  file="preCICE-output/Solid1-Mesh-Displacement-Fluid'''+str(ff)+'''_master.pvtu"/>''')


# for ff in H:
    # VTKFILE.append('''
# <DataSet timestep="'''+str(float(ff)/2000)+'''"  file="preCICE-output/Solid1-Mesh-Force-Fluid.dt'''+str(ff)+'''_master.pvtu"/>''')

# for ff in H:
    # VTKFILE.append('''
# <DataSet timestep="'''+str(float(ff)/2000)+'''"  file="preCICE-output/Solid1-Mesh-Displacement-Fluid.dt'''+str(ff)+'''_master.pvtu"/>''')


# VTKFILE.append('''
  # </Collection>
  # </VTKFile>''')
# with open('Solid1CouplingMesh.pvd','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()



# VTKFILE=['''<?xml version="1.0"?>
# <VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  # <Collection>''']
  

# for ff in ['.init']:
    # VTKFILE.append('''
# <DataSet timestep="0"  file="preCICE-output/Fluid-Mesh-Centers-Fluid'''+str(ff)+'''_master.pvtu"/>''')
# for ff in ['.init']:
    # VTKFILE.append('''
# <DataSet timestep="0"  file="preCICE-output/Fluid-Mesh-Nodes-Fluid'''+str(ff)+'''_master.pvtu"/>''')
    
# for ff in H:
    # VTKFILE.append('''
# <DataSet timestep="'''+str(float(ff)/2000)+'''"  file="preCICE-output/Fluid-Mesh-Centers-Fluid.dt'''+str(ff)+'''_master.pvtu"/>''')
    
# for ff in H:
    # VTKFILE.append('''
# <DataSet timestep="'''+str(float(ff)/2000)+'''"  file="preCICE-output/Fluid-Mesh-Nodes-Fluid.dt'''+str(ff)+'''_master.pvtu"/>''')
    
      
# VTKFILE.append('''
  # </Collection>
  # </VTKFile>''')
  
# with open('FluidCouplingMesh.pvd','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()


# VTKFILE=['''{
  # "file-series-version" : "1.0",
  # "files" : [''']
  

# for ff in H:
    # VTKFILE.append('''
    # { "name" : "preCICE-output/vtks/Fluid-Mesh-Centers-Solid1.dt'''+ff+'''.vtk", "time" :'''+ str(float(ff)/2000)+'''}''')
    # VTKFILE.append(''',''')

    
# VTKFILE[-1]='''
  # ]
# }'''
  
# with open('FluidCouplingMeshCenters.vtk.series','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()


         
# VTKFILE=['''{
  # "file-series-version" : "1.0",
  # "files" : [''']
  

# for ff in H:
    # VTKFILE.append('''
    # { "name" : "preCICE-output/vtks/Fluid-Mesh-Nodes-Solid1.dt'''+ff+'''.vtk", "time" :'''+ str(float(ff)/2000)+'''}''')
    # VTKFILE.append(''',''')

    
# VTKFILE[-1]='''
  # ]
# }'''
  
# with open('FluidCouplingMeshNodes.vtk.series','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()


         
# VTKFILE=['''{
  # "file-series-version" : "1.0",
  # "files" : [''']
  

# for ff in H:
    # VTKFILE.append('''
    # { "name" : "preCICE-output/vtks/Solid1-Mesh-Displacement-Solid1.dt'''+ff+'''.vtk", "time" :'''+ str(float(ff)/2000)+'''}''')
    # VTKFILE.append(''',''')

    
# VTKFILE[-1]='''
  # ]
# }'''
  
# with open('SolidCouplingMeshDisplacement.vtk.series','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()
   
            
                    
# VTKFILE=['''{
  # "file-series-version" : "1.0",
  # "files" : [''']
  

# for ff in H:
    # VTKFILE.append('''
    # { "name" : "preCICE-output/vtks/Solid1-Mesh-Force-Solid1.dt'''+ff+'''.vtk", "time" :'''+ str(float(ff)/2000)+'''}''')
    # VTKFILE.append(''',''')

    
# VTKFILE[-1]='''
  # ]
# }'''
  
# with open('SolidCouplingMeshForce.vtk.series','w') as f:
    # f.seek(0)
    # for x in VTKFILE:
        # for line in x:
            # f.write(line)
            # f.truncate()

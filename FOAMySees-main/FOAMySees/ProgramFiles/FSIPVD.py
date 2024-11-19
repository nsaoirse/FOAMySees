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

print(F)

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

I=glob.glob("OpenFOAMCase/postProcessing/XSec1/*")

I= [i.replace('OpenFOAMCase/VTK/','') for i in I]
I= [i.replace('OpenFOAMCase_','') for i in I]

I= [i.replace('OpenFOAMCaseBoundary_','') for i in I]
I= [i.replace('OpenFOAMCase_Boundary_','') for i in I]
I= [i.replace('OpenFOAMCase_Boundary','') for i in I]

I= [i.replace('Boundary','') for i in I]


I= [i.replace('OpenFOAMCase','') for i in I]

I= [i.replace('/postProcessing/XSec1/','') for i in I]

I= [i.replace('yCut.vtp','') for i in I]

I=set(I)
print(I)

VTKFILE=['''<?xml version="1.0"?>
<VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  <Collection>''']

for ff in I:
    VTKFILE.append('''
    <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCase/postProcessing/XSec1/'''+str(ff)+'''/interpolatedSurface.vtp"/>''')
    
VTKFILE.append('''
  </Collection>

</VTKFile>''')
with open('InterpSurface.pvd','w') as f:
    f.seek(0)
    for x in VTKFILE:
        for line in x:
            f.write(line)
            f.truncate()

G=glob.glob("OpenFOAMCase/postProcessing/freeSurfaceVTK/*")

G= [i.replace('OpenFOAMCase/VTK/','') for i in G]
G= [i.replace('OpenFOAMCase_','') for i in G]

G= [i.replace('OpenFOAMCaseBoundary_','') for i in G]
G= [i.replace('OpenFOAMCase_Boundary_','') for i in G]
G= [i.replace('OpenFOAMCase_Boundary','') for i in G]
G= [i.replace('Boundary','') for i in G]


G= [i.replace('OpenFOAMCase','') for i in G]

G= [i.replace('/postProcessing/freeSurfaceVTK/','') for i in G]

G= [i.replace('yCut.vtp','') for i in G]


G=set(G)
print(G)

VTKFILE=['''<?xml version="1.0"?>
<VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
  <Collection>''']

for ff in G:
    VTKFILE.append('''
    <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCase/postProcessing/freeSurfaceVTK/'''+str(ff)+'''/freeSurface.vtp"/>''')
    
    
    
VTKFILE.append('''
  </Collection>
</VTKFile>''')
with open('FreeSurface.pvd','w') as f:
    f.seek(0)
    for x in VTKFILE:
        for line in x:
            f.write(line)
            f.truncate()

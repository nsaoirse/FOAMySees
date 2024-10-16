import pyvista as pv

import matplotlib as mpl

import FSIPVD


from threading import Thread
import time
import numpy as np
import pyvista as pv
import pyvistaqt as pvqt

def makeActors():
	[plotOpenSeesModel,plotOpenFOAMFreeSurface,plotXSec]=["yes","yes","yes"]
	if plotXSec=="yes":
		OpenFOAMXSecmesh=reader.read()[0]
		#warped=OpenFOAMXSecmesh.warp_by_vector('pointDisplacement')
		dargs = dict(
	#		    scalars="p",
		    cmap="rainbow",
		    show_scalar_bar=True,
		)

		actor3=plotter.add_mesh(OpenFOAMXSecmesh, **dargs)
		
	if plotOpenSeesModel=="yes":

	#		reader.active_time_value
	#		print(reader.datasets)
		OpenSeesmesh=reader.read()[0]
		warped=OpenSeesmesh.warp_by_vector('Displacement')
		dargs = dict(
		    scalars="Displacement",
		    cmap="jet",
		    show_scalar_bar=False,
		)

		actor1=plotter.add_mesh(warped, **dargs)
		
	#		pl.add_mesh(mesh.copy(), component=0, **dargs)
	#		actor1=plotter.add_mesh(warped, lighting=False, show_edges=False,vectors='Displacement')
		
	if plotOpenFOAMFreeSurface=="yes":

	#		reader2.active_time_value
	#		print(reader2.datasets)
		FreeSurf=reader2.read()[0]
		actor2=plotter.add_mesh(FreeSurf, lighting=False, show_edges=False)
	return [actor1,actor2,actor3]
def update_time_window(value):
    """Callback to set the time."""
    timeWindow = round(value)
    readers=[reader,reader2,reader3]
    plotter.remove_actor(x for x in AllActiveActorsNotSlider)
    set_time(timeWindow,readers,AllActiveActorsNotSlider)

def set_time(point,readers,AllActiveActorsNotSlider):

	AllActiveActorsNotSlider.append(x for x in makeActors())

	updateReaders(point,readers)

	plotter.camera.up = (0.0, 0.0, 1.0)
	plotter.camera_position = 'xy'
	#pl.camera.roll += 10

	plotter.update()
	plotter.render()

	print('Time Window: ', point)


def updateReaders(point,readers):

	reader=readers[0]
	reader2=readers[1]
	reader3=readers[2]
	
	reader.set_active_time_point(point)
	reader2.set_active_time_point(point)
	
	reader3.set_active_time_point(point)
	

	

plotter = pvqt.BackgroundPlotter()
#plotter = pv.Plotter(window_size=[1000,1000])

point=0
plotter.show()
plotter.view_isometric()



point=0

[plotOpenSeesModel,plotOpenFOAMFreeSurface,plotXSec]=["yes","yes","yes"]
	

if plotXSec=="yes":
	reader3=pv.get_reader('InterpSurface.pvd')
	reader3.time_values
	reader3.set_active_time_point(0)
	reader3.active_time_value
	print(reader3.datasets, 'OpenFOAM Data Sets')

		
if plotOpenSeesModel=="yes":

	reader=pv.get_reader('OpenSeesOutput.pvd')
	print('OpenSees, times:', reader.time_values)
	reader.set_active_time_point(0)
	reader.active_time_value
	print(reader.datasets, 'OpenSees Data Sets')

if plotOpenFOAMFreeSurface=="yes":

	reader2=pv.get_reader('FreeSurface.pvd')
	reader2.time_values
	reader2.set_active_time_point(0)
	reader2.active_time_value
	print(reader2.datasets, 'OpenFOAM Data Sets')
	


AllActiveActorsNotSlider=[]	
AllActiveActorsNotSlider=makeActors()
	
	

len1=len(reader.time_values)
len2=len(reader2.time_values)
len3=len(reader3.time_values)

minlen=np.min([len1,len2,len3])
readers=[reader,reader2,reader3]


for u in range(0,minlen):
	set_time(u,readers,AllActiveActorsNotSlider)
	plotter.clear()


plotter.close()

plotter = pv.Plotter(window_size=[1000,1000])

point=0

#plotter.view_isometric()





point=0

[plotOpenSeesModel,plotOpenFOAMFreeSurface,plotXSec]=["yes","yes","yes"]
	

#plotter.add_mesh(algo, color='red')

plotter.add_slider_widget(update_time_window, [0, minlen], title='Time Window')

plotter.show()




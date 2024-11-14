from subprocess import Popen, DEVNULL
import openseespy.opensees as ops
from openseespy.opensees import *

def createPVDRecorder(self):		
    res=['disp','vel','accel','incrDisp','reaction','pressure','unbalancedLoad','mass']
    
    ops.recorder('PVD', 'SeesOutput', '-precision', 5, '-dT', self.config.SeesVTKOUTRate, *res)

def createNodeRecorders(self,nodeRecInfoList):		        
    for nodeRecInfo in nodeRecInfoList:
        ops.recorder('Node', '-file', nodeRecInfo[0],'-time', '-node', nodeRecInfo[1],'-closeOnWrite', '-dof', 1,2,3,4,5,6, nodeRecInfo[2])
    
def appendRecords(self,nodeRecInfoList):

   
    for nodeRecInfo in nodeRecInfoList:
        #Popen('cat '+nodeRecInfo[0]+' >> '+nodeRecInfo[0]+'agglom', shell=True, stdin=None, stdout=None, stderr=None,)
        #Popen('cat '+nodeRecInfo[0]+' >> '+nodeRecInfo[0]+'agglom', shell=True, stdin=None, stdout=None, stderr=None,).wait()
        Popen('tail -1 '+nodeRecInfo[0]+' >> '+nodeRecInfo[0]+'agglom', shell=True, stdin=None, stdout=None, stderr=None,) #.wait()
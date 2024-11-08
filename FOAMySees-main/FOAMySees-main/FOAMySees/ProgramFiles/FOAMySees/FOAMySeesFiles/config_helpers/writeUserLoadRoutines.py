import time
from subprocess import Popen, DEVNULL
def writeUserLoadRoutines(writeHere,applyLoad='pass',removeLoad='pass'):
    
    Popen("pwd",shell=True)
    userLoads=['''import openseespy.opensees as ops
# FOAMySees GUI Generated User Loads, time written={}'''.format(time.time()),'''
def applyGM(time):
''']
    with open(applyLoad) as f:
        for line in f:
                userLoads.append('    '+line)

                                        
    userLoads.append('''

def removeGM():
''')
    with open(removeLoad) as f:
        for line in f:
                userLoads.append('    '+line)
                
    with open(writeHere+'userLoadRoutines.py','w') as f:
        for line in userLoads:
            print(line,file=f)


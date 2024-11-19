
def handleButtonOpenSees():
    handleOpenSeesButtonOpenSees()

def handleButtonOpenFOAM():
    handleOpenFOAMButtonOpenFOAM()

def handleButtonCouplingDataProjectionMesh():
    with open(LogFile,'a') as f:
        print('Testing Plot Branches',file=f) 
    branchVis()
                
def handleOpenSeesButtonOpenSees():
    with open(LogFile,'a') as f:
        print('Testing Plot OpenSees Model',file=f) 
    getLog()
    
def handleOpenSeesRunPreliminaryOpenSeesAnalysis():
    with open(LogFile,'a') as f:
        print('Testing Run OpenSees Preliminary Analysis',file=f)        
    getLog()

def handleOpenSeesRunPreliminaryOpenSeesGravityAnalysis():
    with open(LogFile,'a') as f:
        print('Testing Run OpenSees Gravity Analysis',file=f)         
    getLog()

def handleOpenSeesButtonOpenSeesModes():
    with open(LogFile,'a') as f:
        print('Testing Plot OpenSees Modal Analysis',file=f)         
    getLog()
    
def handleOpenFOAMRunPreliminaryOpenFOAMAnalysis():
    with open(LogFile,'a') as f:
        print('Testing OpenFOAM Run to Coupling Start Time',file=f)         
    getLog()

def handleOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis():
    with open(LogFile,'a') as f:
        print('Testing OpenFOAM potentialFoam',file=f)         
    getLog()
            
def handleOpenFOAMButtonOpenFOAM():
    with open(LogFile,'a') as f:
        print('Testing OpenFOAM Plot Mesh',file=f)   
    getLog()

def handleOpenFOAMButtonOpenFOAMFields():
    with open(LogFile,'a') as f:
        print('Testing OpenFOAM Plot Fields',file=f)        
    getLog() 

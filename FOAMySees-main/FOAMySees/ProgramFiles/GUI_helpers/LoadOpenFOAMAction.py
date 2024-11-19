
def LoadOpenFOAMAction():
    filename = QFileDialog.getExistingDirectory("Select an OpenFOAM case folder " ,"Folder (*/)",options=QFileDialog.DontUseNativeDialog)
    connstr='FOAMySees - Connected to OpenFOAM Case: ' + str(filename)

    setWindowTitle(connstr)

    OpenFOAMConnect(filename)
    

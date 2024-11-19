

def LoadOpenSeesAction():
    filename = QFileDialog.getOpenFileName("Select an OpenSeesPy file ", "Python Files (*.py)",options=QFileDialog.DontUseNativeDialog)
    connstr='FOAMySees - Connected to OpenSees File: ' + str(filename[0])

    setWindowTitle(connstr)

    OpenSeesConnect(filename[0])

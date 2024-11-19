def SetFigure(self,w=5, h=3.5):
    # FIGURE 1
    sysplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

    sysplotax = sysplot.add_subplot()
    F1 = FigureCanvas(sysplot)
    self.Canvas1.addWidget(F1)

    # FIGURE 2
    resplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

    resplotax = resplot.add_subplot()
    F2 = FigureCanvas(resplot)
    self.Canvas2.addWidget(F2)

    F1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #
    F2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    show()
    #
def OpenFOAMConnect(self,filename):
    OpenFOAMCaseFolder = filename
    scl2text='Current OpenFOAM Folder \n' + str(OpenFOAMCaseFolder)
    self.scl2ind.setText(str(OpenFOAMCaseFolder))
        
def OpenSeesConnect(self,filename):
    OpenSeesFile = filename
    scl1text='Current OpenSees File \n' + str(OpenSeesFile)
    self.scl1ind.setText(str(OpenSeesFile))

def JSONConnect(self,filename):
    HydroUQFile = filename
    scl1text='Current JSON File \n' + str(HydroUQFile)
    sclHydroUQind.setText(str(HydroUQFile))

def clearLog(self):
    try:
     #Popen("cd "+GUIRootLocation).wait()
        with open("FOAMySeesGUILog", "w") as fileInput: 
            fileInput.seek(0)
            fileInput.truncate()
        
    except: 
            self.textEdit.append('no log file - run python3 FOAMySeesGUI.py >> FOAMySeesGUILog')

def plotSys(self):
    doAthing=0
    if doAthing==0:
        pass
    else:
        pass

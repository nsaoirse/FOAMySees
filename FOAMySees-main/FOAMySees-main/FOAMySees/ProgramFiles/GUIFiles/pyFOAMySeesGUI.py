
from importblock import *
import logging
sys.path.append('./FOAMySees/FOAMySeesFiles')
sys.path.append('./')
sys.path.append('./FOAMySees/FOAMySeesFiles/FOAMySees')
sys.path.append('./FOAMySees/fromUser/')
sys.path.append('./FOAMySees/FOAMySeesFiles/config_helpers')
sys.path.append('./FOAMySees/FOAMySeesFiles/OpenSeesSettings')

from dependencies import *
import pickle 

# import libraries

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,\
    QMainWindow, QStatusBar, QFileDialog, QRadioButton,QTextBrowser, QScrollBar
from PyQt5.QtGui import QPixmap
import os.path as osp
#| ===============================================  ____/__\___/__\____     _.*_*.             |
#|         F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \ \.          |
#|         O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | |  \._ CESG  | 
#|         A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\. UW   |
#|         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___.. 2023 |
#| =============================================== _||  |/\| | |/\|  ||__/,_/__,_____/..__ nsl_|
#| Funded by NSF, Joy P., CMMI-something or other
#| Developed by Nikki Lewis at UW (nicolette.s.lewis@outlook.com)
#| Please don't use this for anything other than good, if you do, you are a bad person and I take no blame for your actions
#| Legal disclaimer
#| FOAM is a registered trademark for some reason, I am not claiming to have made up that acronym
#| Same with SEES - I literally took two names and put them together, didn't come up with either
#| Anyway,  have fun!
#| This code and the GUI are offered 'as-is' - I might update this in the future, but I am not looking forward to it


class pyFOAMySeesGUI(QMainWindow):

    def __init__(self, parent=QMainWindow):

        super().__init__()  # Inheriting the constructor from QMainWindow

        self.initUI()  # Adding some things to the constructor

    def clearLog(self):
        try:
         #Popen("cd "+self.GUIRootLocation).wait()
            with open("FOAMySeesLog", "w") as fileInput: 
                fileInput.seek(0)
                fileInput.truncate()
            
        except: 
                self.textEdit.append('no log file - run python3 FOAMySeesGUI.py >> FOAMySeesLog')
        
    def getLog(self):
        self.textEdit.clear()
        try:
         #Popen("cd "+self.GUIRootLocation).wait()
            with open("FOAMySeesLog", "r") as fileInput: 
                self.textEdit.append(fileInput.read())   
        except: 
                self.textEdit.append('no log file - run python3 FOAMySeesGUI.py >> FOAMySeesLog')
        self.clearLog()
    def getAnalysisLog(self):

        try:
         #Popen("cd "+self.GUIRootLocation).wait()
            Popen("tail Run/RunCase/FOAMySeesLog >>FOAMySeesLog")
            Popen("tail Run/RunCase/FOAMySeesLog >>FOAMySeesLog")
        except: 
            self.textEdit.append('no log file - run python3 FOAMySeesGUI.py >> FOAMySeesLog')
        self.getLog()
                                           
    def runProcessAndWait(self,process):

        Popen(process, shell=True).wait()
        
    def runProcess(self,process):

        Popen(process, shell=True)
   
                
    def initUI(self):
    
        
        self.GUIRootLocation=os.getcwd()
        try:
            self.GUIRootLocation=self.GUIRootLocation.strip('/home/vagrant/')
            self.GUIRootLocation="~/"+self.GUIRootLocation
        except:
            pass
        print(self.GUIRootLocation)
        self.HydroUQFile="/ProgramFiles/FOAMySees/FOAMySeesFiles/fromUserDefaults/scInput.json"
        
        self.LogFile='FOAMySeesLog'
        self.OpenSeesFile="/ProgramFiles/FOAMySees/FOAMySeesFiles/fromUserDefaults/OpenSeesModel.py"
        self.OpenFOAMCaseFolder="/ProgramFiles/FOAMySees/OpenFOAMexampleCase"
        """ The following is added to the constructor by calling self.initUI() within __init__"""
        self.ProgramDetails = """
        -To get started, ....
        *****************************************************************************************************
            Written by Nicolette Lewis in December 2023 at the University of Washington, Seattle Campus
            for the purpose of a GUI for constructing coupled CFD+FEA models with OpenFOAM and OpenSees
        *****************************************************************************************************
        """
        self.setWindowTitle('FOAMySees - Load an OpenSees model to get started. ')
        TopMenu = self.menuBar()
        ## DATABASE BUTTON WITH TOOLBAR STUFF

        LoadOpenSees=QAction("Load OpenSees File",self)
        LoadOpenFOAM = QAction("Load OpenFOAM Model",self)
        Settings = QAction("Export settings to file",self)
        LoadSettings = QAction("Load settings from file",self)
        LoadJSON = QAction("Load Hydro UQ json file",self)
        CaseMenu = TopMenu.addMenu('&Case Settings')
        CaseMenu.addAction(LoadOpenSees)
        CaseMenu.addAction(LoadOpenFOAM)
        CaseMenu.addAction(LoadJSON)
        
        CaseMenu.addAction(Settings)
        CaseMenu.addAction(LoadSettings)

          
        HelpMenu = TopMenu.addMenu('&Help')
        aboutapp=QAction('About',self)
        HelpMenu.addAction(aboutapp)
        LoadJSON.triggered.connect(self.LoadJSONAction)     
        LoadOpenSees.triggered.connect(self.LoadOpenSeesAction)
        LoadOpenFOAM.triggered.connect(self.LoadOpenFOAMAction)
        Settings.triggered.connect(self.SaveSettingsAction)
        LoadSettings.triggered.connect(self.LoadSettingsAction)
        aboutapp.triggered.connect(self.about)
       

        self.initialValues()
        

        ## RESULTS BUTTON IN TOOLBAR

        #PNGExport = QAction("Export as PNG self)
        #PDFExport = QAction("Export as PDF self)
        #CSVExport = QAction("Export as CSV self)

        #ResMenu = TopMenu.addMenu('&Results')

        #ResMenu.addAction(PNGExport)
        #ResMenu.addAction(PDFExport)
        #ResMenu.addAction(CSVExport)
        ###
        self.tabswrapper=QWidget()
         
        self.layoutwrapper = QHBoxLayout(self)
         
        self.tabs = QTabWidget() 
        self.tab0 = QWidget() 
        
        self.tab1 = QWidget() 
        self.tab2 = QWidget() 
        self.tab3 = QWidget() 
        self.tab4 = QWidget() 
        
        self.tabs.resize(300, 200) 

        self.layoutinner0 = QVBoxLayout(self) 
        self.layoutinner0.addWidget(self.CSViewer())
        self.tab0.setLayout(self.layoutinner0)        

        self.layoutinner1 = QVBoxLayout(self) 
        self.layoutinner1.addWidget(self.mainWidgetOpenFOAM())
        self.tab1.setLayout(self.layoutinner1)
        
 
        self.layoutinner2 = QVBoxLayout(self) 
        self.layoutinner2.addWidget(self.mainWidgetOpenSees())
        self.tab2.setLayout(self.layoutinner2)
        
        
        self.layoutinner3 = QVBoxLayout(self) 
        self.layoutinner3.addWidget(self.mainWidget())
        self.tab3.setLayout(self.layoutinner3)
        
        self.layoutinner4 = QVBoxLayout(self) 
        self.layoutinner4.addWidget(self.mainWidgetVisualize())
        self.tab4.setLayout(self.layoutinner4)
        # Add tabs 
        
        self.tabs.addTab(self.tab3, "Settings")       
        
        self.tabs.addTab(self.tab1, "Setup OpenFOAM") 
        self.tabs.addTab(self.tab2, "Setup OpenSees") 
            
        self.tabs.addTab(self.tab4, "Visualize Results")

        self.tabs.addTab(self.tab0, "File Reader") 
        self.layoutwrapper.addWidget(self.tabs)

        self.textBrowser=QWidget(self)
        self.textEdit=QTextBrowser(self)
        self.layout = QVBoxLayout(self) 
        # Add tabs to widget 
        self.buttonRunFOAMySees = QPushButton('Run FOAMySees')
        self.buttonGetLog = QPushButton('Get Setup Log')
        self.buttonGetAnalysisLog = QPushButton('Get Analysis Log')
        
        self.buttonClearLog = QPushButton('Clear Log')
        
        self.layout.addWidget(self.buttonRunFOAMySees)
        
        self.layout.addWidget(self.buttonGetLog) 
        self.layout.addWidget(self.buttonGetAnalysisLog) 
        
        self.layout.addWidget(self.buttonClearLog) 
        
        self.layout.addWidget(self.textEdit) 
        self.textBrowser.setLayout(self.layout)
        self.setCentralWidget(self.textBrowser) 
        self.allLogs=[]


        self.buttonClearLog.clicked.connect(self.clearLog)
        
        self.buttonGetAnalysisLog.clicked.connect(self.getAnalysisLog)
        
        self.buttonGetLog.clicked.connect(self.getLog)
        self.buttonRunFOAMySees.clicked.connect(self.handleButtonRunFOAMySees)
        
        self.layoutwrapper.addWidget(self.textBrowser)
               
        # Create first tab 
        self.layout = QVBoxLayout(self) 
    
        self.tabswrapper.setLayout(self.layoutwrapper)
        # Add tabs to widget 
        self.layout.addWidget(self.tabswrapper)  

        self.setCentralWidget(self.tabswrapper) 
        self.show() 
         
  
       
    

##########################################################################################################
    def mainWidget(self):
        self.Settingtabs = QTabWidget() 
        self.settingtab0 = QWidget() 
        
        self.settingtab1 = QWidget() 
        
 
   
    
        # Vertical Layouts
        mainHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for load scaling

        # Horizontal Layouts
        Hlyt1 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt2 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt3 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hbtnlyt = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    
        emp = QLabel('')
        Empty = QVBoxLayout(emp)
       
        
        HLine = QFrame()
        HLine.setFrameShape(QFrame.HLine)
        #HLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        HLine.setLineWidth(3)
        VLine = QFrame()
        VLine.setFrameShape(QFrame.VLine)
        #HLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
        VLine.setLineWidth(3)        
        




        radbutCouplingTypeVlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        radbutCouplingTypeVlyt.addWidget(QLabel('Coupling DT (s)'))
        self.DTSpinBox=QDoubleSpinBox(self)
        self.DTSpinBox.setRange(1e-10,1e4)


        self.DTSpinBox.setDecimals(6)

        self.DTSpinBox.setValue(1e-3)
        radbutCouplingTypeVlyt.addWidget(self.DTSpinBox)

        radbutCouplingTypeVlyt.addWidget(QLabel('Coupling Settings'))
        # radio buttons
        self.ExplicitRB = QRadioButton('Explicit')
        radbutCouplingTypeVlyt.addWidget(self.ExplicitRB)

        self.ImplicitRB = QRadioButton('Implicit')
        radbutCouplingTypeVlyt.addWidget(self.ImplicitRB)
        radbutCouplingTypeVlyt.addWidget(QLabel('Implicit Coupling Type'))

        self.AitkenRB = QRadioButton('Aitken')
        radbutCouplingTypeVlyt.addWidget(self.AitkenRB)

        self.IQNILSRB = QRadioButton('IQN-ILS')
        radbutCouplingTypeVlyt.addWidget(self.IQNILSRB)

        self.IQNIMVJRB = QRadioButton('IQN-IMVJ')
        radbutCouplingTypeVlyt.addWidget(self.IQNIMVJRB)

        self.ConstantRB = QRadioButton('Constant')
        radbutCouplingTypeVlyt.addWidget(self.ConstantRB)
        
        
        
         
        
        
        self.scl1text='Current OpenSees File \n' 
        self.scl2text='Current OpenFOAM Folder\n' 
        self.scl3text='OpenSees SubSteps' 
        self.scl4text='OpenFOAM SubSteps' 
        # Adding the Vertical layouts to the Horizontal Layouts
        self.scl1 = QLabel(self.scl1text,self)
        self.scl1ind = QLineEdit(self)
        self.scl1ind.setText("OpenSees Model NOT LOADED -> Case Settings>Load OpenSees Model")
                
        self.scl2 = QLabel(self.scl2text,self)
        self.scl2ind = QLineEdit(self)    
        self.scl2ind.setText("OpenFOAM Model NOT LOADED -> Case Settings>Load OpenFOAM Model")

        self.scl3 = QLabel(self.scl3text,self)
        self.scl3ind = QLineEdit(self)    
        self.scl3ind.setText(str(1))

        self.scl4ind = QLineEdit(self)    
        self.scl4ind.setText(str(1))
        self.scl4 = QLabel(self.scl4text,self)

        statusFilesVlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
  
        
        
        OFVlytL = QVBoxLayout() 
        
        OFVlytR = QVBoxLayout() 
        FilesOuterVLyt =QVBoxLayout() 
        FilesHlyt = QHBoxLayout() 
        FilesButHlyt = QHBoxLayout() 
        
        HydroFilesVlyt=QVBoxLayout() 
        self.sclHydroUQ = QLabel('Hydro UQ input.json',self)
        self.sclHydroUQind= QLineEdit(self)    
        self.sclHydroUQind.setText("json NOT LOADED -> Case Settings>Load Hydro UQ json")
        HydroFilesVlyt.addWidget(self.sclHydroUQ)
        HydroFilesVlyt.addWidget(self.sclHydroUQind)
        
        FilesVlyt2= QVBoxLayout() 
        self.RadbutUseHydroInputs=QRadioButton('Use HydroUQ Inputs')
        self.RadbutUseGUIInputs=QRadioButton('Use GUI Inputs')
        self.RADBUTGroup = QButtonGroup(self)  # Number group
        self.RADBUTGroup.addButton(self.RadbutUseGUIInputs)
        self.RADBUTGroup.addButton(self.RadbutUseHydroInputs)
        FilesButHlyt.addWidget(self.RadbutUseGUIInputs)
        FilesButHlyt.addWidget(VLine)
        FilesButHlyt.addWidget(self.RadbutUseHydroInputs)
        
        FilesOuterVLyt.addLayout(FilesButHlyt)
         
        FilesVlyt= QVBoxLayout() 
        FilesVlyt.addWidget(self.scl1)
        FilesVlyt.addWidget(self.scl1ind)
        
        OFHlyt = QHBoxLayout() 
        OFVlytL.addWidget(self.scl2)
        OFVlytL.addWidget(self.scl2ind)
        
        self.OpenFOAMRadbutUse=QRadioButton('Use Existing')
        self.OpenFOAMRadbutBuild=QRadioButton('Build New')
        
        
        self.OFRADBUTGroup = QButtonGroup(self)  # Number group
        self.OFRADBUTGroup.addButton(self.OpenFOAMRadbutUse)

        self.OFRADBUTGroup.addButton(self.OpenFOAMRadbutBuild)
        
        OFVlytR.addWidget(self.OpenFOAMRadbutUse)
        OFVlytR.addWidget(self.OpenFOAMRadbutBuild)
        
        OFHlyt.addLayout(OFVlytL)
        OFHlyt.addLayout(OFVlytR)
 
        
        FilesVlyt.addLayout(OFHlyt)

        
        self.settingtab0.setLayout(FilesVlyt)        
       
        self.settingtab1.setLayout(HydroFilesVlyt)
        self.Settingtabs.addTab(self.settingtab0, "GUI Inputs")
        self.Settingtabs.addTab(self.settingtab1, "HydroUQ Json Inputs")    
        

            
        
        FilesOuterVLyt.addWidget(self.Settingtabs)
        statusFilesVlyt.addLayout(FilesOuterVLyt)
        
        emp = QLabel('')
        Empty = QVBoxLayout()
        Empty.addWidget(emp)
        
        statusFilesVlyt.addLayout(Empty)
        
        statusFilesVlyt.addWidget(HLine)
        
        statusFilesVlyt.addWidget(self.scl3)
        statusFilesVlyt.addWidget(self.scl3ind)
        statusFilesVlyt.addWidget(self.scl4)
        statusFilesVlyt.addWidget(self.scl4ind)
        
        settings1Vlyt = QVBoxLayout()    
    #    settingsVlyt
        settings1Vlyt.addLayout(statusFilesVlyt)

        

        couplingSettingsVlyt = QVBoxLayout()
        self.scl8ind = QLineEdit(self)    
        self.scl8ind.setText(str(0))
        self.scl8 = QLabel('Coupling Start Time (s)',self)
        
        self.scl5ind = QLineEdit(self)    
        self.scl5ind.setText(str(10))
        self.scl5 = QLabel('# Iterations to Use to Approximate Residual Operator inv(J)',self)
        self.scl6ind = QLineEdit(self)    
        self.scl6ind.setText(str(3))
        self.scl6 = QLabel('# Time Windows Used to Guess Dirichlet-Neumann Interface Secants',self)
        self.scl7ind = QLineEdit(self)    
        self.scl7ind.setText(str(0.1))
        self.scl7 = QLabel('Initial Relaxation Factor',self)
        
        self.scl9ind = QLineEdit(self)    
        self.scl9ind.setText(str(0.005))
        self.scl9 = QLabel('Coupling Relative Residual Tolerance',self)        
        
        couplingSettingsVlyt.addWidget(self.scl9)
        couplingSettingsVlyt.addWidget(self.scl9ind)
        
        couplingSettingsVlyt.addWidget(self.scl8)
        couplingSettingsVlyt.addWidget(self.scl8ind)
        
        couplingSettingsVlyt.addWidget(self.scl5)
        couplingSettingsVlyt.addWidget(self.scl5ind)

        couplingSettingsVlyt.addWidget(self.scl6)
        couplingSettingsVlyt.addWidget(self.scl6ind)

        couplingSettingsVlyt.addWidget(self.scl7)
        couplingSettingsVlyt.addWidget(self.scl7ind)
       

        couplingSettingsHlyt = QHBoxLayout()
        couplingSettingsHlyt.addLayout(radbutCouplingTypeVlyt)
        couplingSettingsHlyt.addLayout(couplingSettingsVlyt)
        
        settings1Vlyt.addLayout(couplingSettingsHlyt)
        Hlyt1.addLayout(settings1Vlyt)
    
        # Hlyt1.addLayout(self.Canvas2)
        self.radioFixity = QButtonGroup(self)  # Number group

        self.radioFixity.addButton(self.ExplicitRB)
        self.radioFixity.addButton(self.ImplicitRB)
      
        self.radioFixity2 = QButtonGroup(self)  # Number group
        self.radioFixity2.addButton(self.AitkenRB)
        self.radioFixity2.addButton(self.IQNILSRB)
        self.radioFixity2.addButton(self.IQNIMVJRB)
        self.radioFixity2.addButton(self.ConstantRB)
   
        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        widget = QWidget(self)  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
        self.setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window

        QRadioButton.setChecked(self.ImplicitRB, True)
        QRadioButton.setChecked(self.IQNILSRB, True)
        QRadioButton.setChecked(self.OpenFOAMRadbutBuild,True)
        QRadioButton.setChecked(self.RadbutUseGUIInputs,True)
        
        # Connections
        self.ExplicitRB.clicked.connect(self.setVars)
        self.ImplicitRB.clicked.connect(self.setVars)
        self.AitkenRB.clicked.connect(self.setVars)
        self.IQNILSRB.clicked.connect(self.setVars)
        self.IQNIMVJRB.clicked.connect(self.setVars)
        self.ConstantRB.clicked.connect(self.setVars)
        
        self.OpenFOAMRadbutBuild.clicked.connect(self.setVars)
        self.OpenFOAMRadbutUse.clicked.connect(self.setVars)
        self.RadbutUseGUIInputs.clicked.connect(self.setVars)
        self.RadbutUseHydroInputs.clicked.connect(self.setVars)        
        
        self.scl1ind.editingFinished.connect(self.LoadOpenSeesAction2)
        self.scl2ind.editingFinished.connect(self.LoadOpenFOAMAction2)    
        
        self.scl3ind.editingFinished.connect(self.LoadOpenSeesAction3)
        self.scl4ind.editingFinished.connect(self.LoadOpenFOAMAction3)    

        #self.DTSpinBox.editingFinished.connect(self.Solver)
        #self.DTSpinBox.valueChanged.connect(self.Solver)


            
        return widget    

##########################################################################################################
    def mainWidgetVisualize(self):
        # Vertical Layouts
        self.Canvas1 = QVBoxLayout()  # Initializing the main vertical box layout for the System Figure
        self.Canvas2 = QVBoxLayout()  # Initializing the main vertical box layout for Results Figure
        mainHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for load scaling
        ScaleSliderHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for results scaling

        # Horizontal Layouts
        Hlyt1 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt2 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt3 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hbtnlyt = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    
        emp = QLabel('')
        Empty = QVBoxLayout(emp)
        

        self.buttonPlotOpenSees = QPushButton('Plot OpenSees Model')
        
        self.buttonPlotOpenFOAM = QPushButton('Plot OpenFOAM Model')

        
        self.buttonPlotCouplingDataProjectionMesh = QPushButton('Plot Coupling Data Projection Mesh')
        
        Hbtnlyt.addWidget(self.buttonPlotOpenSees)
        Hbtnlyt.addWidget(self.buttonPlotOpenFOAM)
        Hbtnlyt.addWidget(self.buttonPlotCouplingDataProjectionMesh)
        
        mainHolder.addLayout(Hbtnlyt)
        mainHolder.addLayout(self.Canvas1)

        Hlyt1.addLayout(mainHolder)
    


        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
  

        widget = QWidget(self)  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
        self.setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window
 
        self.SetFigure()




        # Connections
        self.buttonPlotOpenSees.clicked.connect(self.handleButtonOpenSees)
        self.buttonPlotOpenFOAM.clicked.connect(self.handleButtonOpenFOAM)
        self.buttonPlotCouplingDataProjectionMesh.clicked.connect(self.handleButtonCouplingDataProjectionMesh)


            
        return widget 

        
    def LoadSettingsAction(self):
            # Open the file in binary mode 
        with open('FOAMySeesGUISavefile.pkl', 'rb') as file: 
              
            # Call load method to deserialze 
            myvar = pickle.load(file) 
            
            print(myvar) 
        self.OpenSeesFile=myvar[0]
        self.OpenFOAMCaseFolder=myvar[1]
        self.numStepsOpenSees=myvar[2]
        self.numStepsOpenFOAM=myvar[3]    
        self.DT=myvar[4]
        self.scl3ind.setText(str(self.numStepsOpenSees))
        self.scl4ind.setText(str(self.numStepsOpenFOAM))
        self.OpenSeesConnect(self.OpenSeesFile)
        self.DTSpinBox.setValue(self.DT)
    #    self.DTSpinBox.setText(str(self.DT))
        self.OpenFOAMConnect(self.OpenFOAMCaseFolder)
        self.ExplicitOrImplicit=myvar[5][0]
        self.ImplicitMethod=myvar[5][1]    
        self.resetVars()

    def setVars(self):
        if self.ExplicitRB.isChecked():
            self.ExplicitOrImplicit="Explicit"
        if self.ImplicitRB.isChecked():
            self.ExplicitOrImplicit="Implicit"     
        if self.AitkenRB.isChecked():
            self.ImplicitMethod="Aitken"         
        if self.IQNILSRB.isChecked():
            self.ImplicitMethod="IQNILS"
        if self.IQNIMVJRB.isChecked():
            self.ImplicitMethod="IQNIMVJ"
        if self.ConstantRB.isChecked():
            self.ImplicitMethod="Constant"
        self.numStepsOpenSees=self.scl3ind.text()
        self.numStepsOpenFOAM=self.scl4ind.text()

    def resetVars(self):
        if self.ExplicitOrImplicit=="Explicit":
            self.ExplicitRB.setChecked(1)
        if self.ExplicitOrImplicit=="Implicit":
            self.ImplicitRB.setChecked(1)
        if self.ImplicitMethod=="Aitken":

            self.AitkenRB.setChecked(1)
        if self.ImplicitMethod=="IQNILS":
            self.IQNILSRB.setChecked(1)       
        if self.ImplicitMethod=="IQNIMVJ":
            self.IQNIMVJRB.setChecked(1)
        if self.ImplicitMethod=="Constant":
            self.ConstantRB.setChecked(1)        
        
    def SaveSettingsAction(self):
        self.DT=self.DTSpinBox.value()
        self.setVars()
        self.CouplingSettings=[self.ExplicitOrImplicit,self.ImplicitMethod]
         
        # Create a variable 
        myvar = [self.OpenSeesFile,self.OpenFOAMCaseFolder,self.numStepsOpenSees,self.numStepsOpenFOAM,self.DT,self.CouplingSettings] 
          
        # Open a file and use dump() 
        with open('FOAMySeesGUISavefile.pkl', 'wb') as file: 
              
            # A new file will be created 
            pickle.dump(myvar, file) 

    def LoadOpenSeesAction2(self):
        pass
    def LoadOpenFOAMAction2(self):
        pass
        
    def LoadOpenSeesAction3(self):
        try:
            self.numStepsOpenSees=int(self.scl3ind.text)
        except:
            self.numStepsOpenSees=1
        
    def LoadOpenFOAMAction3(self):

        try:
            self.numStepsOpenFOAM=int(self.scl4ind.text)
        except:
            self.numStepsOpenFOAM=1    
    def LoadJSONAction(self):
        filename = QFileDialog.getOpenFileName(self, "Select a json file ","JSON Files (*.json)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to Hydro UQ JSON File: ' + str(filename[0])

        self.setWindowTitle(connstr)

        self.JSONConnect(filename[0])



    def LoadOpenSeesAction(self):
        filename = QFileDialog.getOpenFileName(self, "Select an OpenSeesPy file ", "Python Files (*.py)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to OpenSees File: ' + str(filename[0])

        self.setWindowTitle(connstr)

        self.OpenSeesConnect(filename[0])
    def LoadOpenFOAMAction(self):
        filename = QFileDialog.getExistingDirectory(self, "Select an OpenFOAM case folder " ,"Folder (*/)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to OpenFOAM Case: ' + str(filename)

        self.setWindowTitle(connstr)

        self.OpenFOAMConnect(filename)
        
    def JSONConnect(self,filename):
        self.HydroUQFile = filename
        self.scl1text='Current JSON File \n' + str(self.HydroUQFile)
        self.sclHydroUQind.setText(str(self.HydroUQFile))

    def OpenSeesConnect(self,filename):
        self.OpenSeesFile = filename
        self.scl1text='Current OpenSees File \n' + str(self.OpenSeesFile)
        self.scl1ind.setText(str(self.OpenSeesFile))
        
    def OpenFOAMConnect(self,filename):
        self.OpenFOAMCaseFolder = filename
        self.scl2text='Current OpenFOAM Folder \n' + str(self.OpenFOAMCaseFolder)
        self.scl2ind.setText(str(self.OpenFOAMCaseFolder))
            
    def SetFigure(self, w=5, h=3.5):
        # FIGURE 1
        self.sysplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

        self.sysplotax = self.sysplot.add_subplot()
        self.F1 = FigureCanvas(self.sysplot)
        self.Canvas1.addWidget(self.F1)

        # FIGURE 2
        self.resplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

        self.resplotax = self.resplot.add_subplot()
        self.F2 = FigureCanvas(self.resplot)
        self.Canvas2.addWidget(self.F2)

        self.F1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #
        self.F2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.show()
        #
##########################################################################################################        
    def mainWidgetOpenSees(self):
        # Vertical Layouts
        self.Canvas3 = QVBoxLayout()  # Initializing the main vertical box layout for the System Figure
        
        mainHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for load scaling
        ScaleSliderHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for results scaling

        # Horizontal Layouts
        Hlyt1 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt2 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt3 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hbtnlyt = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    

        self.buttonOpenSeesPlotOpenSees = QPushButton('Plot OpenSees Model')
        self.buttonOpenSeesPlotOpenSeesModes = QPushButton('Plot OpenSees Model Eigenmodes')
        self.buttonOpenSeesRunPreliminaryOpenSeesAnalysis = QPushButton('Run Preliminary Analysis')
        self.buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis = QPushButton('Run Gravity Analysis')
        
        Vbtnlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Vbtnlyt.addWidget(self.buttonOpenSeesRunPreliminaryOpenSeesAnalysis)
        Vbtnlyt.addWidget(self.buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis)


        Hbtnlyt.addLayout(Vbtnlyt)
        Hbtnlyt.addWidget(self.buttonOpenSeesPlotOpenSees)
        Hbtnlyt.addWidget(self.buttonOpenSeesPlotOpenSeesModes)

        mainHolder.addLayout(Hbtnlyt)
        mainHolder.addLayout(self.Canvas3)
        Hlyt1.addLayout(mainHolder)
    
     
        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        widget = QWidget(self)  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
    
        self.SetFigureOpenSees()




        # Connections
        self.buttonOpenSeesRunPreliminaryOpenSeesAnalysis.clicked.connect(self.handleOpenSeesRunPreliminaryOpenSeesAnalysis)
        self.buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis.clicked.connect(self.handleOpenSeesRunPreliminaryOpenSeesGravityAnalysis)

        self.buttonOpenSeesPlotOpenSees.clicked.connect(self.handleOpenSeesButtonOpenSees)
        self.buttonOpenSeesPlotOpenSeesModes.clicked.connect(self.handleOpenSeesButtonOpenSeesModes)
   
    
        return widget    
 
    def SetFigureOpenSees(self, w=5, h=3.5):
        # FIGURE 1
        self.sysplotOpenSees = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

        self.sysplotaxOS = self.sysplotOpenSees.add_subplot()
        self.F1OS = FigureCanvas(self.sysplotOpenSees)
        self.Canvas3.addWidget(self.F1OS)

        self.F1OS.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #

        #

##########################################################################################     
##########################################################################################################        
    def mainWidgetOpenFOAM(self):
        # Vertical Layouts
        self.Canvas4 = QVBoxLayout()  # Initializing the main vertical box layout for the System Figure
        
        mainHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for load scaling
        ScaleSliderHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for results scaling

        # Horizontal Layouts
        Hlyt1 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt2 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hlyt3 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Hbtnlyt = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    

        self.buttonOpenFOAMPlotOpenFOAM = QPushButton('Plot OpenFOAM Model')
        self.buttonOpenFOAMPlotOpenFOAMFields = QPushButton('Plot OpenFOAM Model Fields')
        self.buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis = QPushButton('Run OpenFOAM ONLY Analysis')
        self.buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis = QPushButton('Run potentialFoam to Initialize Fields')
        

        Vbtnlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Vbtnlyt.addWidget(self.buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis)
        Vbtnlyt.addWidget(self.buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis)


        Hbtnlyt.addLayout(Vbtnlyt)
        Hbtnlyt.addWidget(self.buttonOpenFOAMPlotOpenFOAM)
        Hbtnlyt.addWidget(self.buttonOpenFOAMPlotOpenFOAMFields)


        mainHolder.addLayout(Hbtnlyt)
        mainHolder.addLayout(self.Canvas4)
        Hlyt1.addLayout(mainHolder)
    
     
        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        widget = QWidget(self)  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
    
        self.SetFigureOpenFOAM()




        # Connections
        self.buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis.clicked.connect(self.handleOpenFOAMRunPreliminaryOpenFOAMAnalysis)
        self.buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis.clicked.connect(self.handleOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis)

        self.buttonOpenFOAMPlotOpenFOAM.clicked.connect(self.handleOpenFOAMButtonOpenFOAM)
        self.buttonOpenFOAMPlotOpenFOAMFields.clicked.connect(self.handleOpenFOAMButtonOpenFOAMFields)
   
    
        return widget    
 
    def SetFigureOpenFOAM(self, w=5, h=3.5):
        # FIGURE 1
        self.sysplotOpenFOAM = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

        self.sysplotaxOF = self.sysplotOpenFOAM.add_subplot()
        self.F1OF = FigureCanvas(self.sysplotOpenFOAM)
        self.Canvas4.addWidget(self.F1OF)


        self.F1OF.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #

        #


    def plotSys(self):
        doAthing=0
        if doAthing==0:
            pass
        else:
            pass
        #self.dispop()
        #self.Getxvec()
        #self.sysplotax.clear()
        #self.resplotax.clear()
        #self.sysplotax.text(self.L / 3, self.qo / 900, 'w = ' + str(self.qo) + '  lbf/foot')
        #self.sysplotax.plot(self.xvec, self.u, 'r')
        #self.sysplotax.plot(self.xvec, self.undeformed, 'k')

        #self.sysplotax.plot(self.xvec, np.ones(len(self.undeformed)) * self.qo / 1000, 'r')

        #for x in self.xvec[0::10]:
        #    self.sysplotax.annotate(" xy=(x, 0), xytext=(x, self.qo / 1000), arrowprops=dict(arrowstyle="-> color='r'))

        #self.sysplotax.axis([-self.L * 0.1, self.L * 1.1, -self.L / 100, 1 + self.L / 50])

        #self.sysplotax.set_xlabel('X (ft)')
        #self.sysplotax.set_ylabel('Y (ft)')
        #self.sysplotax.add_patch(self.bc1)
        #self.sysplotax.add_patch(self.bc2)

        #self.F1.draw()

        #self.show()




    def about(self):
        QMessageBox.about(self, "BeamSolverGUI - Information about the application", self.ProgramDetails)
        

#############################################################################################3

# class definition
    def CSViewer(self):

        """ The following is added to the constructor by calling self.initUI() within __init__"""
        self.ProgramDetails = """
         ___  ___ _   _      __ _   _   _  __  __
        ||     ||__  \\\\  /  o  ||_ \\\\  /\\\\  / ||_ ||_|
        ||__  __||  \\\\/  ||| ||_  \\\\/  \\\\/  ||_ ||  \\
        
        CSViewer: A simple application to view CSV and text files.                      
                         Version 1.0
                         
        Open a .csv or .txt file by either entering its full path in the field above or by 
        selecting a file via the "Choose File" dialogue in the upper right of the window.
        
        The field separator of the displayed csv can be selected below:
        
            Note, changing the field operator within the text browser does not modify the .csv or .txt file
            on disk, merely in the memory of the computer while the application in running. In other words,
                                THIS APPLICATION IS READ-ONLY.
                                
        Written by Nicolette Lewis in November 2019 at the University of Washington, Seattle Campus
        for the purpose of Assignment 5 in Engineering Computing: CESG 505
        """
        self.Icon= QLabel(self)                                 # initializing the QLabel which will be filled with a pixmap
        self.checkIcon = QPixmap('check.png').scaled(24, 24)    #initializing an icon from a png
        self.warnIcon = QPixmap('warn.png').scaled(24, 24)      #initializing an icon from a png


        self.browser = QTextBrowser(self)                # Initializing the text browser
        self.status = QStatusBar(self)                   # Initializing the status bar of the main window
        self.fileNameInput = QLineEdit(self)             # Initializing the filename Line Edit thing

        self.browser.setLineWrapMode(False)              # Turning linewrap off so the horizontal scrollbar is enabled
        horizbar = QScrollBar()                          # Initializing a scrollbar to be attached to the text browser
        horizbar.setVisible(True)                        # Switching the visibility of the scrollbar on
        self.browser.setHorizontalScrollBar(horizbar)    # Finally attaching the scrollbar to horizontal movement
                                                            # within the text browser
        self.browser.setMinimumSize(300,100)
        widget = QWidget(self)                           # Creating a widget to store layouts in

        self.radbtnComma = QRadioButton('Comma (,)')     # Initializing the Radio Buttons which control which field
        self.radbtnSmiCln = QRadioButton('Semicolon (;)')    # operator the csv will be displayed in
        self.radbtnCln = QRadioButton('Colon (:)')
        self.radbtnTab = QRadioButton('Tab (\\t)')

        filebutton = QPushButton('Choose File', self)    # Initializing a button to select the file to be opened using
                                                            # a dialogue
        # Horizontal Layouts
        layout1 = QHBoxLayout()                          # Initializing the horizontal box layouts for various buttons
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()

        # Adding widgets to layout 1
        layout1.addWidget(QLabel('File:'))              # Adding a label to the first horizontal layout before the
        layout1.addWidget(self.fileNameInput)           # Line Edit field is added to the layout here
        layout1.addWidget(filebutton)                   # Adding the file selection dialogue button to layout 1
        layout1.addWidget(self.Icon)
        # Adding widgets to layout 2
        layout2.addWidget(self.browser)                 # Adding the text browser to layout 2

        # Adding widgets to layout 3
        layout3.addWidget(QLabel("Field Separator"))    # Adding a label to the layout just above the selection field
                                                            # separator Radio Buttons
        # Adding wdigets to layout 4
        layout4.addWidget(self.radbtnComma)             # Adding the field separator radio buttons to the layout
        layout4.addWidget(self.radbtnSmiCln)
        layout4.addWidget(self.radbtnCln)
        layout4.addWidget(self.radbtnTab)

        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()                          # Initializing the vertical layout
        layout.addLayout(layout1)                       # Adding layouts to the vertical layout
        layout.addLayout(layout2)                       # .
        layout.addLayout(layout3)                       # .
        layout.addLayout(layout4)                       # .
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)                        # Setting layout of the widget
        # Setting commas as the default field separator of the input file
        QRadioButton.setChecked(self.radbtnComma, True)

        # Creating connections :)
        filebutton.clicked.connect(self.getFile)                # Connecting the Open File button to the file dialogue
        self.radbtnComma.toggled.connect(self.getFieldsep)      # Connecting the Radio Buttons to a method acquiring
        self.radbtnSmiCln.toggled.connect(self.getFieldsep)      # the current selected field separator and calling the
        self.radbtnCln.toggled.connect(self.getFieldsep)      # file parsing method
        self.radbtnTab.toggled.connect(self.getFieldsep)
        
        self.fileNameInput.editingFinished.connect(self.getName)    # Connecting the filename LineEdit field input
                                                            # "editingFinished" signal to the method associated with
                                                           # loading the file and then sending it to be parsed
        self.setCentralWidget(widget)             # Assigning the dummy widget to the central widget of the main window

        self.setStatusBar(self.status)            # Setting the status bar to the default message
#        self.setWindowTitle('CSV Viewer: Please select a file to open')
                                                  # Setting the window title to the default message
        self.getFieldsep()                        # Initializing field separator attribute
        # Printing the program details in the text browser until a file has been opened
        self.browser.setText(self.ProgramDetails)
        self.Icon.setPixmap(self.checkIcon)  # Setting the initial Icon
        
        return widget

    def getFieldsep(self):
        """ Checks to see if a field separator radio button has been toggled and sets the current field separator
            to be that of the radio button that is toggled and then parses the file to be displayed with that
            field separator """

        if self.radbtnComma.isChecked():        # checking to see if the radio button is toggled
            self.fieldsep = ','

        if self.radbtnSmiCln.isChecked():        # checking to see if the radio button is toggled
            self.fieldsep = ';'

        if self.radbtnCln.isChecked():        # checking to see if the radio button is toggled
            self.fieldsep = ':'

        if self.radbtnTab.isChecked():        # checking to see if the radio button is toggled
            self.fieldsep = '\t'

        if hasattr(self, 'filename'):           # if the window has opened a file, then parse it again to be shown with
            self.parseFile()                    # the selected field separator by sending to the parsing method
        else:
            self.error(0)                       # if the application hasn't opened a file, then an error is shown


    def getName(self):
        if osp.isfile(self.fileNameInput.text()) and self.fileNameInput.text() != '':   # if the file exists
            self.filename = self.fileNameInput.text()     # assign the filename string to the variable self.filename
            self.parseFile()                               # then parse the file
        else:
            self.error(1)                                  # if the file doesn't exist, then a different error is shown


    def getFile(self):
        """ This method opens the file selection dialogue, and assigns the name of the file that was selected to the variable self.filename and then calls the parsing method"""
        self.filename = QFileDialog.getOpenFileName(self,"","",\
                                                    "All Files (*);; CSV Files (*.csv);; Text Files (*.txt)",\
                                                    options=QFileDialog.DontUseNativeDialog)[0]
                                                    # reads the file name of the file object read
        self.parseFile()                            # assigns it to self.filename, calls the parsing method


    def parseFile(self):
        """ This is the parsing method. It works by finding the first common delimiter in the file provided
            (if the file is a csv) then parses the file into components and returns those components delimited by
            the field separator selected by the user via the radio buttons in the application
            If the file is not a csv but instead a text file, the program just prints the text in the browser window
            If the file is not a txt or csv, or is a csv and cannot be broken into its components because of an uncommon
            delimitation (not , ; or :), then the program returns an error telling the user that the file cannot be read """

        try:
            if '.csv' or '.txt' in self.filename:           # then the file is parsed. otherwise an error is shown.
                self.browser.clear()                        # Clearing the text browser window

                currentfile = open(self.filename, 'r')      # Opening the file of interest

                text = currentfile.read()                   # Reading the file

                for i in [',', ';', ':', '\\t']:            # Finding the first delimiter in the file
                    if i in text:                               # If the delimiter is in the file
                        inputfieldsep = i                           # the delimiter is set as the input delimiter
                if '.csv' in self.filename:                 # If the file is a csv...
                    for lines in text.split('\n'):              # Split it up into lines,
                        curr=self.fieldsep+' '                  # Then further split by input delimiter
                                                                # and append the output to the text browser (below)
                        self.browser.append(curr.join((x.strip(inputfieldsep)) for x in lines.split(inputfieldsep)))
                else:                                       # If the file isn't a csv...
                    self.browser.setText(text)              # just print it in the browser
                self.fileNameInput.setText(self.filename)   # Setting the Line Edit field to the name of the file path
                # Setting the window title and the status bar message to the full path and abridged path respectively
                self.setWindowTitle('CSV Viewer: ' + self.filename)             # main window title, full path
                self.status.showMessage('Viewing ' + self.filename.split('/')[-1])  # status bar, abridged path
                self.Icon.setPixmap(self.checkIcon)
        except:
            self.error(2)                   # delimited with something wonky


    def error(self,input):
        """
        This method holds all of the error messaging of the application
        """
        if input==0:
            self.status.showMessage(
                "Please open a file.")
            self.browser.setText(self.ProgramDetails)
            self.Icon.setPixmap(self.warnIcon)
        elif input==1:
            self.status.showMessage(
                "Please enter a valid file name.")
            self.Icon.setPixmap(self.warnIcon)
        elif input==2:
            self.status.showMessage(
                "ERROR: File cannot be read")
            self.Icon.setPixmap(self.warnIcon)
     # Creating tab widgets 
     
    def initialValues(self):
        self.AdjustTimeStep="No"
        self.ApplyGravity="Yes"
        self.CouplingScheme="Implicit"
        self.SeesVTKOUT="Yes"
        self.SeesVTKOUTRate=0.01
        self.FOAMVTKOUT="Yes"
        self.FOAMVTKOUTRate=0.01
        self.SimDuration=1
        self.SolutionDT=5e-4
        self.Turbulence="No"
        self.couplingConvergenceTol=5e-2
        self.bathType="Point List"
        self.bathSTL="flumeFloor.stl"
        self.bathXZData=[
            [
                19.908,
                -1
            ],
            [
                19.908,
                0.152
            ],
            [
                23.568,
                0.152
            ],
            [
                31.8,
                0.838
            ],
            [
                83,
                0.838
            ],
            [
                101.5,
                2
            ]  ]
        self.couplingDataAccelerationMethod="IQN-ILS"
        self.couplingIterationOutputDataFrequency=100
        self.cutSurfaceLocsDirsFields=[[
                0.1,
                0.01,
                0.01,
                0,

                0,
                1,
                "XSec1",
                "p,U,alpha.water"
            ]  ]
        self.cutSurfaceOutput="Yes"
        self.domainSubType="UW WASIRF"
        self.fieldProbeLocs=[    ]
        self.fieldProbes="No"
        self.flumeHeight=0.4
        self.flumeLength=4
        self.flumeWidth=0.4
        self.flumeCellSize=0.1
        self.freeSurfOut="Yes"
        self.freeSurfProbeLocs=[    ]
        self.freeSurfProbes="No"
        self.g=-9.81
        self.initVelocity=0
        self.initialRelaxationFactor=0.1666
        self.interfaceSurface="interface.stl"
        self.interfaceSurfaceOutput="Yes"
        self.mapType="Nearest Neighbor"
        self.maximumCouplingIterations=100
        self.openSeesPyScript="OpenSeesModel.py"
        self.preliminaryAnalysisFile="preliminarystructuralanalysis.py"
        self.outputDataFromCouplingIterations="No"
        self.paddleDispFile="paddleDisplacement.csv"
        self.periodicWaveCelerity=1
        self.periodicWaveMagnitude=1
        self.periodicWaveRepeatPeriod=1
        self.refPressure=0
        self.runPrelim="No"
        self.stillWaterLevel=0.2
        self.turbIntensity=0.25
        self.turbRefLength=0.125
        self.turbReferenceVel=0.5
        self.velocityFile=""
        self.waveType="No Waves"
        self.writeDT=0.01
    def branchVis(self):
        try:
                with open(self.LogFile) as f:
                        print('Making Case Setup Directory', file=f)
                Popen('mkdir CaseSetup').wait()
                Popen('cd CaseSetup').wait()
                rank=0

                OpenSees_dt=1e-3
                pid= rank 
                
                Sees=FOAMySeesInstance(OpenSees_dt,config)





                N = len(Sees.coupledNodes) # number of ops.nodes
                with open(self.LogFile) as f:        
                        print("N: " + str(N), file=f)
   
                CouplingDataProjectionMesh=Sees.config.CouplingDataProjectionMesh

                solverName = "Solid1"

                dimensions=3

                try:
                        #Using PyVista to Read STL or OBJ containing points of Coupling Surface for CFD Mesh 

                        # Branches = pv.read("FluidCouplingSurface.obj").points
                        
                        #Using PyVista to Calculate Cell Centers of faces 
                        Branches= pv.read(CouplingDataProjectionMesh).cell_centers().points
                        isSurfLoaded=1        # woo! we are good to move forward
                except: 
                        # still not loaded
                        isSurfLoaded=0

                # print(Branches)                      
                Tree=KDTree(Sees.nodeLocs)
                BranchToNodeRelationships=Tree.query(Branches)[1]

                vertices=Branches
                # print(BranchToNodeRelationships[1],np.shape(BranchToNodeRelationships[1]))
                NodeToBranchNodeRelationships=[]
                # with open('BranchesLOCS.log', 'a+') as f:
                # for vertex in verticesBranchesDB:
                    # print(vertex,file=f)       
                for n in range(len(Sees.nodeLocs)):

                        NodeToBranchNodeRelationships.append([n])
                # vertices=[]
                nodeCount=0
                for node in range(len(BranchToNodeRelationships)):
                        NodeToBranchNodeRelationships[BranchToNodeRelationships[node]].append(node)
                with open(self.LogFile) as f:
                    print(NodeToBranchNodeRelationships,file=f)
                vertices=np.array(vertices)
                with open('BranchesLOCS.log', 'a+') as f:
                        f.seek(0)
                        f.truncate()
                        print(NodeToBranchNodeRelationships,file=f)
                        print(vertices,file=f)
                        print(np.shape(vertices),file=f)

                Sees.NodeToBranchNodeRelationships=NodeToBranchNodeRelationships

                Force = np.zeros(np.shape(vertices))
                Displacement = np.zeros(np.shape(vertices))
                BranchTransform=np.zeros(np.shape(vertices))
                Sees.moment=np.zeros(np.shape(vertices))
                    
                ncc=10000000
                BNOD=[]
                for nodeC in vertices:

                    
                    ops.node(10000000+ncc,float(nodeC[0]),float(nodeC[1]),float(nodeC[2]))

                    BNOD.append(10000000+ncc)
                    ncc+=1
                    
                A=0.84*0.00064516
                Iz=0.486*0.00064516*0.00064516        
                Iy=0.486*0.00064516*0.00064516        
                Jxx=0.796*0.00064516*0.00064516
                E_mod=29000*6895000 #ksi*conversion
                G_mod=E_mod/(2*(1.3))
                secTag=15000
                ops.section('Elastic', secTag, E_mod, A, Iz, Iy, G_mod, Jxx)

                ops.beamIntegration('Lobatto', 15000, secTag, 2)


                matTag=601
                beamNormal=[1,1,1]
                for Relationship in Sees.NodeToBranchNodeRelationships:
                    print(Relationship)
                    fN=Sees.nodeList[Relationship[0]]
                    oN=Relationship[1:]
                    for oNC in oN:
                        #ops.geomTransf('PDelta', ncc, beamNormal[0],beamNormal[1],beamNormal[2])
                        #ops.element('forceBeamColumn', ncc, *[fN, BNOD[oNC]], ncc, 15000) 
                        #print(ncc)


                        ops.rigidLink('beam', fN, BNOD[oNC])
                        ops.element('Truss', ncc, *[fN, BNOD[oNC]], 1, matTag)
                        ncc+=1
                    
                    
                    
                    
                ops.wipeAnalysis()

                res=['disp','vel','accel','incrDisp','reaction','pressure','unbalancedLoad','mass']
                # fibre_stressStrain = op.eleResponse(eleTag,               # element tag
                                                # 'section', secTag,    # section tag
                                                # fibre_coords,         # fibre y- and z-coordinates
                                                # responseType)         # response type
                #recorder('Element', '-ele', 1, 'section', str(1), 'fiber', str(y), str(z), 'stress')
                #ops.recorder('Node', '-file', 'DFree.out','-time', '-node', 11, '-dof', 1,2,3, 'disp')

                os.system('rm -rf BranchVisualization')
                os.system('mkdir BranchVisualization')
                os.system('touch BranchVisualization.pvd')
                recorder('PVD', 'BranchVisualization', '-precision', 4, '-dT', 0.001, *res)


                IDloadTag = 400            # load tag
                dt = 0.001            # time step for input ground motion
                GMfact = 386           # data in input file is in g Unifts -- ACCELERATION TH
                maxNumIter = 10

                Tol=1e-3




                ops.timeSeries('Constant', 1, '-factor',1)

                ops.pattern('Plain', 1, 1)


                FX=Sees.config.g[0]
                FY=Sees.config.g[1]
                FZ=Sees.config.g[2]   
                for node_num in range(0,len(Sees.nodeList)):
                    NM=ops.nodeMass(Sees.nodeList[node_num], 1)    
                    if Sees.config.SeesModelType=="solid":
                        ops.load(Sees.nodeList[node_num], NM*FX, NM*FY, NM*FZ)
                    else:
                        ops.load(Sees.nodeList[node_num], NM*FX, NM*FY, NM*FZ, 0.0, 0., 0.0) 




                ops.constraints('Transformation')
                ops.numberer('Plain')
                ops.system('BandGeneral')
                ops.test('EnergyIncr', Tol, maxNumIter)
                ops.algorithm('ModifiedNewton')
                NewmarkGamma = 0.666
                NewmarkBeta = 0.333
                ops.integrator('Newmark', NewmarkGamma, NewmarkBeta)
                ops.analysis('VariableTransient')
                DtAnalysis = 0.001
                TmaxAnalysis = 0.001
                Nsteps =  int(TmaxAnalysis/ DtAnalysis)
                ok=1
                # for i in test:
                ops.algorithm('KrylovNewton')



                ok = ops.analyze(Nsteps, DtAnalysis,DtAnalysis/10,100)   
        except:
                with open(self.LogFile,'a') as f:
                    print('The Coupling Data Projection Mesh or the OpenSees Model does not exist. Make sure everything else is set up',file=f)
        self.getLog()
                

##########################################################################################     






# button handles
    def writeStartScript(self,Participant1,Participant2,configfile,CouplingDataProjectionMesh,makeCouplingDataProjectionMesh,OpenSeesPyModelFile,OpenFOAMCaseFolder,OpenFOAMSolver,nameOfCoupledPatchOrSurfaceFile,isPartOfHydro,HydrojsonFile,NPROC,OpenFOAMFileHandler,useExistingOpenFOAMCaseFolder,inputFilesLocation,ExistingOpenFOAMCase):

         
         startScript=['''#!/bin/sh''','''
parallel=1
solverroot="./"
Participant1="{}"
Participant2="{}"
configfile="{}"

CouplingDataProjectionMesh="{}"
makeCouplingDataProjectionMesh={}
OpenSeesPyModelFile="{}"

OpenFOAMCaseFolder={}
OpenFOAMSolver={}

nameOfCoupledPatchOrSurfaceFile={}


isPartOfHydro="{}"
HydrojsonFile="{}"

NPROC={}
OpenFOAMFileHandler="{}"
useExistingOpenFOAMCaseFolder="{}"

inputFilesLocation="{}"
ExistingOpenFOAMCase="{}"
'''.format(Participant1,Participant2,configfile,CouplingDataProjectionMesh,makeCouplingDataProjectionMesh,OpenSeesPyModelFile,OpenFOAMCaseFolder,OpenFOAMSolver,nameOfCoupledPatchOrSurfaceFile,isPartOfHydro,HydrojsonFile,NPROC,OpenFOAMFileHandler,useExistingOpenFOAMCaseFolder,inputFilesLocation,ExistingOpenFOAMCase),'''

# preparing the case folder
rm -rf RunCase
mkdir RunCase

# entering the case folder
cd RunCase
mkdir userInputs
cp -r ../FOAMySeesFiles/* .
cp -r ${ExistingOpenFOAMCase}/* ./OpenFOAMCaseFolder
mv fromUserDefaults/* userInputs
cp -r ${inputFilesLocation}/* ./userInputs
cp -r ${HydrojsonFile}/* ./userInputs
# echo determining parallel processing parameters...
. $WM_PROJECT_DIR/bin/tools/RunFunctions    # Tutorial run functions


# configuring the case
python3 configureCoupledCase.py ${isPartOfHydro} ${HydrojsonFile} ${nameOfCoupledPatchOrSurfaceFile} ${CouplingDataProjectionMesh} ${makeCouplingDataProjectionMesh} ${OpenSeesPyModelFile} ${OpenFOAMCaseFolder} ${OpenFOAMSolver} ${NPROC} ${OpenFOAMFileHandler} ${useExistingOpenFOAMCaseFolder} ${ExistingOpenFOAMCase}

# starting the OpenSees model preliminary analysis and waiting for coupling to initialize
echo "Starting ${Participant2} participant..."
mpirun -np 1 python3 ${solverroot}${Participant2}.py ${solverroot}${configfile} ${CouplingDataProjectionMesh} > ${Participant2}.log 2>&1 &
PIDParticipant2=$!        

# starting the OpenFOAM model
echo "Preparing the ${Participant1} participant..."
cd ${OpenFOAMCaseFolder}
        nproc=$(getNumberOfProcessors)
        Solver1=$(getApplication)    # solver
cd ..

surfaceMeshExtract -case ${OpenFOAMCaseFolder} -patches ${nameOfCoupledPatchOrSurfaceFile} -latestTime ${CouplingDataProjectionMesh}
cp ${OpenFOAMCaseFolder}/${CouplingDataProjectionMesh} .

mpirun -np ${nproc} ${Solver1} -parallel -fileHandler ${OpenFOAMFileHandler} -case ${OpenFOAMCaseFolder} > ${Participant1}.log 2>&1 &
PIDParticipant1=$!

# tailing the OpenSees output (OpenFOAM is verbose)
tail -f ${Participant2}.log &

# waiting for input to cancel
while [ -e /proc/${PIDParticipant1} ]; do
    read -r  input
    if [ "$input" = "c" ]; then
        kill ${PIDParticipant1}
        kill ${PIDParticipant2}
        false
    fi
done

# if anything went wrong, do this
if [ $? -ne 0 ] || [ "$(grep -c -E "error:" ${Participant1}.log)" -ne 0 ] || [ "$(grep -c -E "error:" ${Participant2}.log)" -ne 0 ]; then
    echo ""
    echo "Something went wrong... See the log files for more."
    # Precaution
    kill ${PIDParticipant1}
    kill ${PIDParticipant2}
else # nothing went wrong, but double check to make sure
    echo ""
    echo "The simulation seems to be complete, but make sure by looking at the log files and output!"
    if [ $parallel -eq 1 ]; then
        echo "Reconstructing fields..."
        reconstructPar -case ${Participant1} > ${Participant1}_reconstructPar.log 2>&1 & 
    fi
        wait 
        foamToVTK -case ${PIDParticipant1}
        wait
        
        python3 FSIPVD.py
        python3 FOAMySeesPlotter.py
        wait
        mkdir results
        cp -r SeesOutput results
        cp -r OpenSeesOutput.pvd results
        cp -r ${PIDParticipant1}/VTK results
        cp -r ${PIDParticipant1}/postProcessing results        
        zip -r ../results.zip results

fi

echo ""

cd ..

echo 'Analysis Complete, results stored in results.zip'
''']
         with open('./Run/newStartFOAMySees', 'w') as f:
             f.seek(0)
             f.truncate()
             for line in startScript:
                 print(line,file=f)
                
    def handleButtonRunFOAMySees(self):

        self.runProcessAndWait("rm -rf OldRuns;")

        self.runProcessAndWait("mv -f ./Run OldRuns; mkdir ./Run")

        self.runProcessAndWait("cp -r ./ProgramFiles/FOAMySees/* ./Run")
        Participant1="OpenFOAMCaseFolder" # don't change this, unless you feel like you don't need the preprocessor
        
        Participant2="FOAMySeesCouplingDriver" # don't change this
        
        configfile="precice-config.xml" # don't change this
        
        CouplingDataProjectionMesh="CouplingDataProjectionMesh.obj" # this will be the default, can be changed - affects the name of the coupling data projection mesh files 
        makeCouplingDataProjectionMesh=1 # this will be the default, right now there is not another option but I'm leaving this here as a reminder to add    
        isPartOfHydro="No" # this will be the default, changes if the radio button is checked (see below)
        
        OpenFOAMSolver="interFoam" # NEED TO CREATE AN INPUT FOR THIS
        
        nameOfCoupledPatchOrSurfaceFile="interface" # NEED TO CREATE AN INPUT FOR THIS
        
        NPROC=2  # NEED TO CREATE AN INPUT FOR THIS
        if self.RadbutUseGUIInputs.isChecked():
            self.runProcessAndWait("cp -r "+self.OpenFOAMCaseFolder+" ./Run/existingCase")   
        useExistingOpenFOAMCaseFolder=0 # connect this to the radio button
        if self.OpenFOAMRadbutUse.isChecked():    
            useExistingOpenFOAMCaseFolder=1 # connected this to the radio button
                       
        ExistingOpenFOAMCase="../existingCase"
        
        OpenFOAMFileHandler="collated"       # change this if you want...
        inputFilesLocation="../../userInputs" # don't change this, I will add an option later to change the location of the input files folder
        
        OpenSeesPyModelFile="OpenSeesModel.py" # add copy opensees model to file location
        self.runProcessAndWait("cp -r "+self.OpenSeesFile+" ./userInputs/"+OpenSeesPyModelFile)        
        
        OpenFOAMCaseFolder="OpenFOAMCaseFolder" # don't change this 
        HydrojsonFile="./userInputs/scInput.json" # don't change this
        if self.RadbutUseHydroInputs.isChecked():
            self.runProcessAndWait("cp -r "+self.HydroUQFile+" "+HydrojsonFile)
            isPartOfHydro="Yes"       


        


        self.writeStartScript(Participant1,Participant2,configfile,CouplingDataProjectionMesh,makeCouplingDataProjectionMesh,OpenSeesPyModelFile,OpenFOAMCaseFolder,OpenFOAMSolver,nameOfCoupledPatchOrSurfaceFile,isPartOfHydro,HydrojsonFile,NPROC,OpenFOAMFileHandler,useExistingOpenFOAMCaseFolder,inputFilesLocation,ExistingOpenFOAMCase)            
        self.runProcess("cd ./Run/; chmod u+x newStartFOAMySees; ./newStartFOAMySees")
                
        
    def handleButtonOpenSees(self):
        self.handleOpenSeesButtonOpenSees()

    def handleButtonOpenFOAM(self):
        self.handleOpenFOAMButtonOpenFOAM()
    
    def handleButtonCouplingDataProjectionMesh(self):
        with open(self.LogFile,'a') as f:
            print('Testing Plot Branches',file=f) 

        self.branchVis()

                    
    def handleOpenSeesButtonOpenSees(self):
        with open(self.LogFile,'a') as f:
            print('Testing Plot OpenSees Model',file=f) 
        self.getLog()
        
    def handleOpenSeesRunPreliminaryOpenSeesAnalysis(self):
        with open(self.LogFile,'a') as f:
            print('Testing Run OpenSees Preliminary Analysis',file=f)        
        self.getLog()
   
    def handleOpenSeesRunPreliminaryOpenSeesGravityAnalysis(self):
        with open(self.LogFile,'a') as f:
            print('Testing Run OpenSees Gravity Analysis',file=f)         
        self.getLog()
    
    def handleOpenSeesButtonOpenSeesModes(self):
        with open(self.LogFile,'a') as f:
            print('Testing Plot OpenSees Modal Analysis',file=f)         
        self.getLog()
        
    def handleOpenFOAMRunPreliminaryOpenFOAMAnalysis(self):
        with open(self.LogFile,'a') as f:
            print('Testing OpenFOAM Run to Coupling Start Time',file=f)         
        self.getLog()
   
    def handleOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis(self):
        with open(self.LogFile,'a') as f:
            print('Testing OpenFOAM potentialFoam',file=f)         
        self.getLog()
                
    def handleOpenFOAMButtonOpenFOAM(self):
        with open(self.LogFile,'a') as f:
            print('Testing OpenFOAM Plot Mesh',file=f)   
        self.getLog()
   
    def handleOpenFOAMButtonOpenFOAMFields(self):
        with open(self.LogFile,'a') as f:
            print('Testing OpenFOAM Plot Fields',file=f)        
        self.getLog() 
    






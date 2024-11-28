import matplotlib as mpl
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
import pyqtgraph as pg
import subprocess
from threading import Thread
import pyvista as pv
import pyvistaqt as pvqt
import glob

from importblock import *
import logging
### FOAMySees
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./.."))
from dependencies import *
import pickle

import coupledAnalysisSettings as config

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./GUI_helpers"))
import GUI_helpers as GUI_helpers
# import libraries

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,\
    QMainWindow, QStatusBar, QFileDialog, QRadioButton,QTextBrowser, QScrollBar, QCheckBox
from PyQt5.QtGui import QPixmap
import os.path as osp
#| ===============================================  ____/__\___/__\____     _.*_*.             |
#|         F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \ \.          |
#|         O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | |  \._ CESG  | 
#|         A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\. UW   |
#|         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___.. 2023 |
#| =============================================== _||  |/\| | |/\|  ||__/,_/__,_____/..__ nsl_|


class pyFOAMySeesGUI(QMainWindow):

    def __init__(self, parent=QMainWindow):

        super().__init__()  # Inheriting the constructor from QMainWindow
        self.LogFile="FOAMySeesGUILog"
        


        self.initUI()  # Adding some things to the constructor


    def about(self):
        QMessageBox.about('''
#| ===============================================  ____/__\___/__\____     _.*_*.             |
#|         F ield           |   |  S tructural      ||__|/\|___|/\|__||      \ \ \ \.          |
#|         O peration       |___|  E ngineering &   ||__|/\|___|/\|__||       | | |  \._ CESG  | 
#|         A nd                 |  E arthquake      ||__|/\|___|/\|__||      _/_/_/ | .\. UW   |
#|         M anipulation    |___|  S imulation      ||__|/\|___|/\|__||   __/, / _ \___.. 2023 |
#| =============================================== _||  |/\| | |/\|  ||__/,_/__,_____/..__ nsl_|
''', ProgramDetails)
    
        
    def initUI(self):

        HydroUQFile="/ProgramFiles/FOAMySees/FOAMySeesFiles/fromUserDefaults/scInput.json"
        
        LogFile='FOAMySeesGUILog'
        OpenSeesFile="/ProgramFiles/FOAMySees/FOAMySeesFiles/fromUserDefaults/OpenSeesModel.py"
        OpenFOAMCaseFolder="/ProgramFiles/FOAMySees/OpenFOAMexampleCase"
        """ The following is added to the constructor by calling initUI() within __init__"""
        ProgramDetails = """
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

        #PNGExport = QAction("Export as PNG )
        #PDFExport = QAction("Export as PDF )
        #CSVExport = QAction("Export as CSV )

        #ResMenu = TopMenu.addMenu('&Results')

        #ResMenu.addAction(PNGExport)
        #ResMenu.addAction(PDFExport)
        #ResMenu.addAction(CSVExport)
        ###
        tabswrapper=QWidget()
         
        layoutwrapper = QHBoxLayout()
         
        tabs = QTabWidget() 
        tab0 = QWidget() 

        layoutinner0 = QVBoxLayout() 

        layoutinner0.addWidget(self.residualPlotterWidget())

        tab0.setLayout(layoutinner0)
        
        tab1 = QWidget() 
        tab2 = QWidget() 
        tab3 = QWidget() 
        tab4 = QWidget() 
        
        tabs.resize(300, 200) 
      

        layoutinner1 = QVBoxLayout() 
        layoutinner1.addWidget(self.mainWidgetOpenFOAM())
        tab1.setLayout(layoutinner1)
        

        layoutinner2 = QVBoxLayout() 
        layoutinner2.addWidget(self.mainWidgetOpenSees())
        tab2.setLayout(layoutinner2)
        
        
        layoutinner3 = QVBoxLayout() 
        layoutinner3.addWidget(self.mainWidget())
        tab3.setLayout(layoutinner3)
        
        layoutinner4 = QVBoxLayout() 
        layoutinner4.addWidget(self.mainWidgetVisualize())
        tab4.setLayout(layoutinner4)
        # Add tabs 
        
        tabs.addTab(tab3, "Settings")       
        tabs.addTab(tab2, "Setup OpenSees")         
        tabs.addTab(tab1, "Setup OpenFOAM") 
        tabs.addTab(tab4, "Plot Solution")
        tabs.addTab(tab0, "Plot Residuals")

        
        
        layoutwrapper.addWidget(tabs)

        textBrowser=QWidget()
        self.textEdit=QTextBrowser()
        layout = QVBoxLayout() 
        # Add tabs to widget 
        buttonRunFOAMySees = QPushButton('Run FOAMySees')
        buttonGetLog = QPushButton('Get Setup Log')
        buttonGetAnalysisLog = QPushButton('Get Analysis Log')
        
        buttonCheckLibsExist = QPushButton('Check Installation')
        
        layout.addWidget(buttonRunFOAMySees)
        
        layout.addWidget(buttonGetLog) 
        layout.addWidget(buttonGetAnalysisLog) 
        
        layout.addWidget(buttonCheckLibsExist) 
        
        layout.addWidget(self.textEdit) 
        textBrowser.setLayout(layout)
        self.setCentralWidget(textBrowser) 
        allLogs=[]


        buttonCheckLibsExist.clicked.connect(self.checkLibsExist)
        
        buttonGetAnalysisLog.clicked.connect(self.getAnalysisLog)
        
        buttonGetLog.clicked.connect(self.getLog)
        buttonRunFOAMySees.clicked.connect(self.handleButtonRunFOAMySees)
        
        layoutwrapper.addWidget(textBrowser)
               
        # Create first tab 
        layout = QVBoxLayout() 

        tabswrapper.setLayout(layoutwrapper)
        # Add tabs to widget 
        layout.addWidget(tabswrapper)  

        self.setCentralWidget(tabswrapper) 
        self.show() 

    def checkLibsExist(self):
        returnCode=0
        returnCode+=os.system("blockMesh >> checkEnv")
        returnCode+=os.system("pkg-config --cflags libprecice >> checkEnv")
        
        if returnCode>0:
            self.textEdit.append('Environment not configured properly. Make sure you have installed and loaded everything.')
            print('Environment not configured properly. Make sure you have installed and loaded everything.')

    def residualPlotterWidget(self):
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
        fig_work = QVBoxLayout()



######
        # Create a PlotWidget for the graph
        self.plotWorkWidget = pg.PlotWidget()
        # Set up the plot
        self.workplot = self.plotWorkWidget.plot([0], [0])  # Initialize with a single point
        # Start updating the plot in a separate thread
        self.worktimer = pg.QtCore.QTimer()
        self.worktimer.timeout.connect(self.updateWorkPlot)
        self.worktimer.start(100)  # Update every 100ms



        self.plotResidualWidget = pg.PlotWidget()
        # Set up the plot
        self.residualplot = self.plotResidualWidget.plot([0], [0])  # Initialize with a single point
        # Start updating the plot in a separate thread
        self.residualtimer = pg.QtCore.QTimer()
        self.residualtimer.timeout.connect(self.updateResidualPlot)
        self.residualtimer.start(100)  # Update every 100ms



        self.plotTotalWorkWidget = pg.PlotWidget()
        # Set up the plot
        self.totalworkplotFtS = self.plotTotalWorkWidget.plot([0], [0],pen='g',name="Fluid to Structure")  # Initialize with a single point
        self.totalworkplotStF = self.plotTotalWorkWidget.plot([0], [0],pen='r',name="Structure to Fluid")  # Initialize with a single point
        # Start updating the plot in a separate thread
        self.totalworktimer = pg.QtCore.QTimer()
        self.totalworktimer.timeout.connect(self.updateTotalWorkWidget)
        self.totalworktimer.start(100)  # Update every 100ms



        self.plotCumulativeWorkWidget = pg.PlotWidget()
        # Set up the plot
        self.cumulativeworkplotFtS = self.plotCumulativeWorkWidget.plot([0], [0],pen='g',name="Fluid to Structure")  # Initialize with a single point
        self.cumulativeworkplotStF = self.plotCumulativeWorkWidget.plot([0], [0],pen='r',name="Structure to Fluid")  # Initialize with a single point
        # Start updating the plot in a separate thread
        self.cumulativeworktimer = pg.QtCore.QTimer()
        self.cumulativeworktimer.timeout.connect(self.updateCumulativeWorkWidget)
        self.cumulativeworktimer.start(100)  # Update every 100ms


        fig_work.addWidget(self.plotWorkWidget)
        fig_work.addWidget(self.plotResidualWidget)
        fig_work.addWidget(self.plotTotalWorkWidget)
        fig_work.addWidget(self.plotCumulativeWorkWidget)

        
        mainHolder.addLayout(fig_work)        
        Hlyt1.addLayout(mainHolder)

        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout

        widget = QWidget()  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
        self.setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window

        # Connections
        #buttonPlotResiduals = QPushButton('Plot Coupling Residuals')
        
        #buttonPlotWork = QPushButton('Plot Work In and Out')

        #buttonPlotCouplingDataProjectionMeshErrors = QPushButton('Plot Work Error by Node')
        
        #Hbtnlyt.addWidget(buttonPlotResiduals)
        #Hbtnlyt.addWidget(buttonPlotWork)
        #Hbtnlyt.addWidget(buttonPlotCouplingDataProjectionMeshErrors)
        
        #mainHolder.addLayout(Hbtnlyt)

        #buttonPlotResiduals.clicked.connect(self.handleButtonPlotResiduals)
        #buttonPlotCouplingDataProjectionMeshErrors.clicked.connect(self.buttonPlotCouplingDataProjectionMeshErrors)

        return widget

    def updateWorkPlot(self):
        try:
            self.getResidualsAndWork()

            self.workTime=self.ResidualArray[:,2]
            self.workError=self.ResidualArray[:,3]
            # Update the plot
            self.workplot.setData(self.workTime, self.workError)
            self.plotWorkWidget.setTitle("Work Transfer Error vs Time (%)")

            # Set axis labels
            self.plotWorkWidget.setLabel('left', 'Work Transfer Error (%)')
            self.plotWorkWidget.setLabel('bottom', 'Time (s)')
        except:
            print('Nothing to plot yet. Moving on.')
        
    def updateResidualPlot(self):
        try:
            self.getResidualsAndWork()

            self.resTime=self.ResidualArray[:,2]
            self.res1=self.ResidualArray[:,4]
            
            # Update the plot
            self.residualplot.setData(self.resTime, self.res1)
            self.plotResidualWidget.setTitle("Work Ratio (Fluid to Structure) vs Time")

            # Set axis labels
            self.plotResidualWidget.setLabel('left', 'Work Ratio')
            self.plotResidualWidget.setLabel('bottom', 'Time (s)')
        except:
            print('Nothing to plot yet. Moving on.')        
        
    def updateTotalWorkWidget(self):
        try:
            self.getResidualsAndWork()

            self.resTime=self.ResidualArray[:,2]
            self.WFtS=self.ResidualArray[:,5]
            self.WStF=self.ResidualArray[:,6]
            
            # Update the plot
            self.totalworkplotFtS.setData(self.resTime, self.WFtS)
            
            self.totalworkplotStF.setData(self.resTime, self.WStF)
            
            # Update the plot
            self.plotTotalWorkWidget.setTitle("Work vs Time [F->S = green], [S->F = red]")

            # Set axis labels
            self.plotTotalWorkWidget.setLabel('left', 'Work')
            self.plotTotalWorkWidget.setLabel('bottom', 'Time (s)')
            self.plotTotalWorkWidget.addLegend(offset=(0, 30))
        except:
            print('Nothing to plot yet. Moving on.')

    def updateCumulativeWorkWidget(self):
        try:
            self.getResidualsAndWork()
            
            self.resTime=self.ResidualArray[:,2]
            
            last_indices = {}
            
            for i, value in enumerate(self.resTime):
                last_indices[value] = i
            uniq=list(last_indices.values())

            resTime=self.resTime[uniq]

            WFtS=self.ResidualArray[uniq,5]

            WStF=self.ResidualArray[uniq,6]

            WFtScumul=[]
            WStFcumul=[]
            for StF, FtS in zip(WStF, WFtS):
                smWStF=sum(WStFcumul)+StF
                WStFcumul.append(smWStF)
                
            for FtS in WFtS:
                smWFtS=sum(WFtScumul)+FtS
                WFtScumul.append(smWFtS)
                
            WFtScumul/=WStFcumul[-1]
            
            WStFcumul/=WStFcumul[-1]
            
            # Update the plot
            self.cumulativeworkplotFtS.setData(resTime, WFtScumul)
            
            self.cumulativeworkplotStF.setData(resTime, WStFcumul)
            
            # Update the plot
            self.plotCumulativeWorkWidget.setTitle("Cumulative Work Ratio vs Time [F->S = green], [S->F = red]")

            # Set axis labels
            self.plotCumulativeWorkWidget.setLabel('left', 'Cumulative Work')
            self.plotCumulativeWorkWidget.setLabel('bottom', 'Time (s)')
            self.plotCumulativeWorkWidget.addLegend(offset=(0, 30))
        except:
            pass

    def updateCouplingDataProjectionMeshPlot(self):
        
        doesMeshExist=0
        while doesMeshExist==0:
            try:
                # Load the OBJ file
                mesh = pv.read('./RunCase/CouplingDataProjectionMesh.obj')
                
                # Add the mesh to the view
                self.CouplingMeshView.addItem(mesh)
                doesMeshExist=1
            except:
                print('No surface file available to plot. Trying again.')


    def updateForcePlots(self):

        #self.updateCouplingDataProjectionMeshPlot()
                
        try:
            self.getInterfaceForce()
            
            self.forceTime=self.ForceArray[:,0]
        
            last_indices = {}
            
            for i, value in enumerate(self.forceTime):
                last_indices[value] = i
                
            uniq=list(last_indices.values())

            forceTime=self.forceTime[uniq]

            totFX=self.ForceArray[uniq,1]
            totFY=self.ForceArray[uniq,2]
            totFZ=self.ForceArray[uniq,3]
            
            preFX=self.ForceArray[uniq,4]
            preFY=self.ForceArray[uniq,5]
            preFZ=self.ForceArray[uniq,6]
            
            visFX=self.ForceArray[uniq,7]
            visFY=self.ForceArray[uniq,8]
            visFZ=self.ForceArray[uniq,9]
            
            # Update the plot
            self.totalFXplot.setData(forceTime, totFX)
            self.pressureFXplot.setData(forceTime, preFX)
            self.viscousFXplot.setData(forceTime, visFX)
            self.totalFYplot.setData(forceTime, totFY)
            self.pressureFYplot.setData(forceTime, preFY)
            self.viscousFYplot.setData(forceTime, visFY)
            self.totalFZplot.setData(forceTime, totFZ)
            self.pressureFZplot.setData(forceTime, preFZ)
            self.viscousFZplot.setData(forceTime, visFZ)
            
            
            # Update the plot
            self.plotCumulativeWorkWidget.setTitle("Cumulative Work Ratio vs Time [F->S = green], [S->F = red]")

            # Set axis labels
            self.plotCumulativeWorkWidget.setLabel('left', 'Cumulative Work')
            self.plotCumulativeWorkWidget.setLabel('bottom', 'Time (s)')
            self.plotCumulativeWorkWidget.addLegend(offset=(0, 30))

        except:
            pass    

    def getInterfaceForce(self):

        self.ForceArray=np.loadtxt('./RunCase/OpenFOAMCase/postProcessing/interface/0/force.dat', dtype='float', skiprows=4)
    
        
    def handleButtonPlotResiduals(self):
        pass
        
    def buttonPlotCouplingDataProjectionMeshErrors(self):
        pass
            
    def getResidualsAndWork(self):

        self.ResidualArray=np.loadtxt('./RunCase/fys_logs/WorkInAndOutArray.log', dtype='float', delimiter=' ')
        
    ##########################################################################################################
    def mainWidget(self):
        Settingtabs = QTabWidget() 
        settingtab0 = QWidget() 
        
        settingtab1 = QWidget() 
        
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
        DTSpinBox=QDoubleSpinBox()
        DTSpinBox.setRange(1e-10,1e4)

        DTSpinBox.setDecimals(6)

        DTSpinBox.setValue(1e-3)
        radbutCouplingTypeVlyt.addWidget(DTSpinBox)

        radbutCouplingTypeVlyt.addWidget(QLabel('Coupling Settings'))
        
        # radio buttons
        ExplicitRB = QRadioButton('Explicit')
        radbutCouplingTypeVlyt.addWidget(ExplicitRB)

        ImplicitRB = QRadioButton('Implicit')
        radbutCouplingTypeVlyt.addWidget(ImplicitRB)
        radbutCouplingTypeVlyt.addWidget(QLabel('Implicit Coupling Type'))

        AitkenRB = QRadioButton('Aitken')
        radbutCouplingTypeVlyt.addWidget(AitkenRB)

        IQNILSRB = QRadioButton('IQN-ILS')
        radbutCouplingTypeVlyt.addWidget(IQNILSRB)

        IQNIMVJRB = QRadioButton('IQN-IMVJ')
        radbutCouplingTypeVlyt.addWidget(IQNIMVJRB)

        ConstantRB = QRadioButton('Constant')
        radbutCouplingTypeVlyt.addWidget(ConstantRB)
        
        scl1text='Current OpenSees File \n' 
        scl2text='Current OpenFOAM Folder\n' 
        scl3text='OpenSees SubSteps' 
        scl4text='OpenFOAM SubSteps' 
        # Adding the Vertical layouts to the Horizontal Layouts
        scl1 = QLabel(scl1text,)
        scl1ind = QLineEdit()
        scl1ind.setText("OpenSees Model NOT LOADED -> Case Settings>Load OpenSees Model")
                
        scl2 = QLabel(scl2text,)
        scl2ind = QLineEdit()    
        scl2ind.setText("OpenFOAM Model NOT LOADED -> Case Settings>Load OpenFOAM Model")

        scl3 = QLabel(scl3text,)
        scl3ind = QLineEdit()    
        scl3ind.setText(str(1))

        scl4ind = QLineEdit()    
        scl4ind.setText(str(1))
        scl4 = QLabel(scl4text,)

        statusFilesVlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        
        OFVlytL = QVBoxLayout() 
        
        OFVlytR = QVBoxLayout() 
        FilesOuterVLyt =QVBoxLayout() 
        FilesHlyt = QHBoxLayout() 
        FilesButHlyt = QHBoxLayout() 
        
        HydroFilesVlyt=QVBoxLayout() 
        sclHydroUQ = QLabel('Hydro UQ input.json',)
        sclHydroUQind= QLineEdit()    
        sclHydroUQind.setText("json NOT LOADED -> Case Settings>Load Hydro UQ json")
        HydroFilesVlyt.addWidget(sclHydroUQ)
        HydroFilesVlyt.addWidget(sclHydroUQind)
        
        FilesVlyt2= QVBoxLayout() 
        RadbutUseHydroInputs=QRadioButton('Use HydroUQ Inputs')
        RadbutUseGUIInputs=QRadioButton('Use GUI Inputs')
        RADBUTGroup = QButtonGroup()  # Number group
        RADBUTGroup.addButton(RadbutUseGUIInputs)
        RADBUTGroup.addButton(RadbutUseHydroInputs)
        FilesButHlyt.addWidget(RadbutUseGUIInputs)
        FilesButHlyt.addWidget(VLine)
        FilesButHlyt.addWidget(RadbutUseHydroInputs)
        
        FilesOuterVLyt.addLayout(FilesButHlyt)
         
        FilesVlyt= QVBoxLayout() 
        FilesVlyt.addWidget(scl1)
        FilesVlyt.addWidget(scl1ind)
        
        OFHlyt = QHBoxLayout() 
        OFVlytL.addWidget(scl2)
        OFVlytL.addWidget(scl2ind)
        
        OpenFOAMRadbutUse=QRadioButton('Use Existing')
        OpenFOAMRadbutBuild=QRadioButton('Build New')        
        
        OFRADBUTGroup = QButtonGroup()  # Number group
        OFRADBUTGroup.addButton(OpenFOAMRadbutUse)

        OFRADBUTGroup.addButton(OpenFOAMRadbutBuild)
        
        OFVlytR.addWidget(OpenFOAMRadbutUse)
        OFVlytR.addWidget(OpenFOAMRadbutBuild)
        
        OFHlyt.addLayout(OFVlytL)
        OFHlyt.addLayout(OFVlytR)

        FilesVlyt.addLayout(OFHlyt)
        
        settingtab0.setLayout(FilesVlyt)        
       
        settingtab1.setLayout(HydroFilesVlyt)
        Settingtabs.addTab(settingtab0, "GUI Inputs")
        Settingtabs.addTab(settingtab1, "HydroUQ Json Inputs")    
        

            
        
        FilesOuterVLyt.addWidget(Settingtabs)
        statusFilesVlyt.addLayout(FilesOuterVLyt)
        
        emp = QLabel('')
        Empty = QVBoxLayout()
        Empty.addWidget(emp)
        
        statusFilesVlyt.addLayout(Empty)
        
        statusFilesVlyt.addWidget(HLine)
        
        statusFilesVlyt.addWidget(scl3)
        statusFilesVlyt.addWidget(scl3ind)
        statusFilesVlyt.addWidget(scl4)
        statusFilesVlyt.addWidget(scl4ind)
        
        settings1Vlyt = QVBoxLayout()    
    #    settingsVlyt
        settings1Vlyt.addLayout(statusFilesVlyt)

        

        couplingSettingsVlyt = QVBoxLayout()
        scl8ind = QLineEdit()    
        scl8ind.setText(str(0))
        scl8 = QLabel('Coupling Start Time (s)',)
        
        scl5ind = QLineEdit()    
        scl5ind.setText(str(10))
        scl5 = QLabel('# Iterations to Use to Approximate Residual Operator inv(J)',)
        scl6ind = QLineEdit()    
        scl6ind.setText(str(3))
        scl6 = QLabel('# Time Windows Used to Guess Dirichlet-Neumann Interface Secants',)
        scl7ind = QLineEdit()    
        scl7ind.setText(str(0.1))
        scl7 = QLabel('Initial Relaxation Factor',)
        
        scl9ind = QLineEdit()    
        scl9ind.setText(str(0.005))
        scl9 = QLabel('Coupling Relative Residual Tolerance',)        
        
        couplingSettingsVlyt.addWidget(scl9)
        couplingSettingsVlyt.addWidget(scl9ind)
        
        couplingSettingsVlyt.addWidget(scl8)
        couplingSettingsVlyt.addWidget(scl8ind)
        
        couplingSettingsVlyt.addWidget(scl5)
        couplingSettingsVlyt.addWidget(scl5ind)

        couplingSettingsVlyt.addWidget(scl6)
        couplingSettingsVlyt.addWidget(scl6ind)

        couplingSettingsVlyt.addWidget(scl7)
        couplingSettingsVlyt.addWidget(scl7ind)
       

        couplingSettingsHlyt = QHBoxLayout()
        couplingSettingsHlyt.addLayout(radbutCouplingTypeVlyt)
        couplingSettingsHlyt.addLayout(couplingSettingsVlyt)
        
        settings1Vlyt.addLayout(couplingSettingsHlyt)
        Hlyt1.addLayout(settings1Vlyt)

        # Hlyt1.addLayout(Canvas2)
        radioFixity = QButtonGroup()  # Number group

        radioFixity.addButton(ExplicitRB)
        radioFixity.addButton(ImplicitRB)
      
        radioFixity2 = QButtonGroup()  # Number group
        radioFixity2.addButton(AitkenRB)
        radioFixity2.addButton(IQNILSRB)
        radioFixity2.addButton(IQNIMVJRB)
        radioFixity2.addButton(ConstantRB)

        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        widget = QWidget()  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
        self.setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window

        QRadioButton.setChecked(ImplicitRB, True)
        QRadioButton.setChecked(IQNILSRB, True)
        QRadioButton.setChecked(OpenFOAMRadbutBuild,True)
        QRadioButton.setChecked(RadbutUseGUIInputs,True)
        
        # Connections
        ExplicitRB.clicked.connect(self.setVars)
        ImplicitRB.clicked.connect(self.setVars)
        AitkenRB.clicked.connect(self.setVars)
        IQNILSRB.clicked.connect(self.setVars)
        IQNIMVJRB.clicked.connect(self.setVars)
        ConstantRB.clicked.connect(self.setVars)
        
        OpenFOAMRadbutBuild.clicked.connect(self.setVars)
        OpenFOAMRadbutUse.clicked.connect(self.setVars)
        RadbutUseGUIInputs.clicked.connect(self.setVars)
        RadbutUseHydroInputs.clicked.connect(self.setVars)        
            
        return widget    

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

        buttonOpenSeesPlotOpenSees = QPushButton('Plot OpenSees Model')
        buttonOpenSeesPlotOpenSeesModes = QPushButton('Plot OpenSees Model Eigenmodes')
        buttonOpenSeesRunPreliminaryOpenSeesAnalysis = QPushButton('Run Preliminary Analysis')
        buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis = QPushButton('Run Gravity Analysis')
        
        Vbtnlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Vbtnlyt.addWidget(buttonOpenSeesRunPreliminaryOpenSeesAnalysis)
        Vbtnlyt.addWidget(buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis)


        Hbtnlyt.addLayout(Vbtnlyt)
        Hbtnlyt.addWidget(buttonOpenSeesPlotOpenSees)
        Hbtnlyt.addWidget(buttonOpenSeesPlotOpenSeesModes)

        mainHolder.addLayout(Hbtnlyt)
        mainHolder.addLayout(self.Canvas3)
        Hlyt1.addLayout(mainHolder)

     
        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        widget = QWidget()  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
                # FIGURE 1
        # Connections
        buttonOpenSeesRunPreliminaryOpenSeesAnalysis.clicked.connect(self.handleOpenSeesRunPreliminaryOpenSeesAnalysis)
        buttonOpenSeesRunPreliminaryOpenSeesGravityAnalysis.clicked.connect(self.handleOpenSeesRunPreliminaryOpenSeesGravityAnalysis)

        buttonOpenSeesPlotOpenSees.clicked.connect(self.handleOpenSeesButtonOpenSees)
        buttonOpenSeesPlotOpenSeesModes.clicked.connect(self.handleOpenSeesButtonOpenSeesModes)


        return widget    

    def SetFigureOpenSees(self,w=5, h=3.5):
        self.OpenSeesreader.set_active_time_point(reader.time_values[-1])
        self.OpenSeesreader.active_time_value        


    def SetFigureOpenFOAM(self,w=5, h=3.5):
        # FIGURE 1
        reader=pv.get_reader('./RunCase/CouplingDataProjectionMesh.obj')
        CouplingMeshViewReader=reader.read()

        self.CouplingMeshView.add_mesh(CouplingMeshViewReader)
        # self.CouplingMeshView.add_axes_at_origin()
        self.CouplingMeshView.show_axes()
        #self.CouplingMeshView.clear()
        self.CouplingMeshView.show()
        #self.CouplingMeshView.update()
        #self.CouplingMeshView.render()


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

        buttonOpenFOAMPlotOpenFOAM = QPushButton('Plot OpenFOAM Model')
        buttonOpenFOAMPlotOpenFOAMFields = QPushButton('Plot OpenFOAM Model Fields')
        buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis = QPushButton('Run OpenFOAM ONLY Analysis')
        buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis = QPushButton('Run potentialFoam to Initialize Fields')

        Vbtnlyt = QVBoxLayout()  # Initializing the main horizontal box layout for various buttons
        Vbtnlyt.addWidget(buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis)
        Vbtnlyt.addWidget(buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis)

        Hbtnlyt.addLayout(Vbtnlyt)
        Hbtnlyt.addWidget(buttonOpenFOAMPlotOpenFOAM)
        Hbtnlyt.addWidget(buttonOpenFOAMPlotOpenFOAMFields)

        mainHolder.addLayout(Hbtnlyt)
        mainHolder.addLayout(self.Canvas4)
        Hlyt1.addLayout(mainHolder)

        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
        layout.addLayout(Hlyt2)  # .
        layout.addLayout(Hlyt3)  # .

        layout2= QHBoxLayout()  # Initializing the horizontal layout

        layout2.addLayout(layout)
        
        widget = QWidget()  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window

        # Create a 3D view window for the coupling data projection mesh...
        
        self.CouplingMeshView = pvqt.QtInteractor()
        
        layout2.addWidget(self.CouplingMeshView)
        
        widget.setLayout(layout2)  # Setting layout of the widget


        self.ofplottimer = pg.QtCore.QTimer()
        self.ofplottimer.timeout.connect(self.SetFigureOpenFOAM)
        self.ofplottimer.start(500)  # Update every 100ms

        # Connections
        buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis.clicked.connect(self.handleOpenFOAMRunPreliminaryOpenFOAMAnalysis)
        buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis.clicked.connect(self.handleOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis)

        buttonOpenFOAMPlotOpenFOAM.clicked.connect(self.handleOpenFOAMButtonOpenFOAM)
        buttonOpenFOAMPlotOpenFOAMFields.clicked.connect(self.handleOpenFOAMButtonOpenFOAMFields)
        
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
        fig_force = QVBoxLayout()
        
        # Start updating the plot in a separate thread
        self.forceplottimer = pg.QtCore.QTimer()
        self.worktimer.timeout.connect(self.updateForcePlots)
        self.worktimer.start(100)  # Update every 100ms


        # Create a PlotWidget for the graph
        self.plotForceXWidget = pg.PlotWidget()
        self.plotForceXWidget.setTitle("X Force vs Time (g=total, b=pressure, r=viscous)")
        # Set axis labels
        self.plotForceXWidget.setLabel('left', 'Force')
        self.plotForceXWidget.setLabel('bottom', 'Time (s)')

        
        self.plotForceYWidget = pg.PlotWidget()
        self.plotForceYWidget.setTitle("Y Force vs Time (g=total, b=pressure, r=viscous)")
        # Set axis labels
        self.plotForceYWidget.setLabel('left', 'Force')
        self.plotForceYWidget.setLabel('bottom', 'Time (s)')


        self.plotForceZWidget = pg.PlotWidget()
        self.plotForceZWidget.setTitle("Z Force vs Time (g=total, b=pressure, r=viscous)")
        # Set axis labels
        self.plotForceZWidget.setLabel('left', 'Force')
        self.plotForceZWidget.setLabel('bottom', 'Time (s)')
        
        # Set up the plot pen='g',name="Fluid to Structure"

        # Set up the plot
        self.totalFXplot = self.plotForceXWidget.plot([0], [0],pen='g',name="Total")  # Initialize with a single point

        self.totalFYplot = self.plotForceYWidget.plot([0], [0],pen='g',name="Total")  # Initialize with a single point
                
        self.totalFZplot = self.plotForceZWidget.plot([0], [0],pen='g',name="Total")  # Initialize with a single point

        self.pressureFXplot = self.plotForceXWidget.plot([0], [0],pen='b',name="Pressure")  # Initialize with a single point

        self.pressureFYplot = self.plotForceYWidget.plot([0], [0],pen='b',name="Pressure")  # Initialize with a single point
                
        self.pressureFZplot = self.plotForceZWidget.plot([0], [0],pen='b',name="Pressure")  # Initialize with a single point

        self.viscousFXplot = self.plotForceXWidget.plot([0], [0],pen='r',name="Viscous")  # Initialize with a single point

        self.viscousFYplot = self.plotForceYWidget.plot([0], [0],pen='r',name="Viscous")  # Initialize with a single point
                
        self.viscousFZplot = self.plotForceZWidget.plot([0], [0],pen='r',name="Viscous")  # Initialize with a single point
        
        fig_force.addWidget(self.plotForceXWidget)
        fig_force.addWidget(self.plotForceYWidget)
        fig_force.addWidget(self.plotForceZWidget)
        
        layout.addLayout(fig_force)        

                
        # Connections
        #buttonPlotResiduals = QPushButton('Plot Coupling Residuals')
        
        #buttonPlotWork = QPushButton('Plot Work In and Out')

        #buttonPlotCouplingDataProjectionMeshErrors = QPushButton('Plot Work Error by Node')
        
        #Hbtnlyt.addWidget(buttonPlotResiduals)
        #Hbtnlyt.addWidget(buttonPlotWork)
        #Hbtnlyt.addWidget(buttonPlotCouplingDataProjectionMeshErrors)
        
        #mainHolder.addLayout(Hbtnlyt)

        #buttonPlotResiduals.clicked.connect(self.handleButtonPlotResiduals)
        #buttonPlotCouplingDataProjectionMeshErrors.clicked.connect(self.buttonPlotCouplingDataProjectionMeshErrors)

        return widget
    
    def makeActors(self,readers):
        actors=[]
        if self.checkboxPlotOS.isChecked():
            reader=readers[0]
            #   reader.active_time_value
            #   print(reader.datasets)
            OpenSeesmesh=reader.read()[0]
            warped=OpenSeesmesh.warp_by_vector('Displacement')
            dargs = dict(
                scalars="Displacement",
                show_scalar_bar=True,
            )
            actor1=self.FYSplotter.add_mesh(warped, **dargs)
            actors.append(actor1)
            
        if self.checkboxPlotFreeSurf.isChecked():
            if not self.checkboxPlotOS.isChecked():
                reader2=readers[0]
            else:
                reader2=readers[1]
        #   reader2.active_time_value
        #   print(reader2.datasets)
            FreeSurf=reader2.read()[0]
            actor2=self.FYSplotter.add_mesh(FreeSurf, lighting=False, show_edges=False)
            actors.append(actor2)
            
        if self.checkboxPlotxSec.isChecked():
            if self.checkboxPlotOS.isChecked():
                if self.checkboxPlotFreeSurf.isChecked():
                    reader3=readers[2]
                else:
                    reader3=readers[1]
            else:
                if self.checkboxPlotFreeSurf.isChecked():
                    reader3=readers[1]
                else:
                    reader3=readers[0]

            OpenFOAMXSecmesh=reader3.read()[0]
            #warped=OpenFOAMXSecmesh.warp_by_vector('pointDisplacement')
            dargs = dict(
            scalars="p",
                cmap="rainbow",
                show_scalar_bar=True,
            show_edges=True,
            opacity=0.5,
            )

            actor3=self.FYSplotter.add_mesh(OpenFOAMXSecmesh, **dargs)
            actors.append(actor3)
        return actors

    def update_time_window(self,value):
        """Callback to set the time."""
        timeWindow = round(value)
        self.FYSplotter.remove_actor(x for x in self.FYSplotter.activeactors)
        self.set_time(timeWindow)

    def set_time(self,value):
        self.FYSplotter.activeactors=[x for x in self.makeActors(self.FYSplotter.readers)]

        for readerCurr in self.FYSplotter.readers:
            readerCurr.set_active_time_point(value)

        #pl.camera.roll += 10
        #self.FYSplotter.add_text('Time: '+str(point)+' s')

        minlen=np.min(self.lens)
        
          
        self.textEdit.append('Time: '+str(value))
        self.FYSplotter.update()
        
        
        self.FYSplotter.render()

        self.FYSplotter.camera.up = (0.0, 0.0, 1.0)
        self.FYSplotter.camera_position = 'xy'
        
    def handlePlotFOAMySeesModel(self):
        
        self.FYSplotter.clear()

        self.parseOpenSeesOutput()
        self.parseOpenFOAMXsecOutput()
        self.parseOpenFOAMFSOutput()
        self.createFOAMySeesFigure()
        
    def parseOpenSeesOutput(self):    
        F=glob.glob("RunCase/SeesOutput/*")
        P0Exists=0
        P1Exists=0
        P2Exists=0
        P3Exists=0

        F= [i.replace('RunCase/SeesOutput/SeesOutput_T','') for i in F]

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
        self.ospvdtimes=list(F)

   
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

        with open('RunCase/OpenSeesOutput.pvd','w') as f:
            f.seek(0)
            for x in VTKFILE:
                for line in x:
                    f.write(line)
                    f.truncate()

    def parseOpenFOAMXsecOutput(self):
        
        I=glob.glob("RunCase/OpenFOAMCase/postProcessing/XSec1/*")
        I= [i.replace('RunCase/OpenFOAMCase/VTK/','') for i in I]
        I= [i.replace('RunCase/OpenFOAMCase_','') for i in I]
        I= [i.replace('RunCase/OpenFOAMCaseBoundary_','') for i in I]
        I= [i.replace('RunCase/OpenFOAMCase_Boundary_','') for i in I]
        I= [i.replace('RunCase/OpenFOAMCase_Boundary','') for i in I]
        I= [i.replace('Boundary','') for i in I]
        I= [i.replace('RunCase/OpenFOAMCase','') for i in I]
        I= [i.replace('/postProcessing/XSec1/','') for i in I]
        I= [i.replace('interpolatedSurface.vtp','') for i in I]

        I=set(I)
        print(I)

        II=[]
        tol=1e-4
        # remove the times which are 'near' the output increment
        for ii in I:
            print(float(ii),config.writeDT,float(ii)%config.writeDT)
            if float(ii)%config.writeDT<tol:
                II.append(ii)
            elif float(ii)%config.writeDT+tol>config.writeDT:
                II.append(ii)
            else:
                pass
            
        self.xsectimes=list(II)
        
        VTKFILE=['''<?xml version="1.0"?>
        <VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
          <Collection>''']

        for ff in II:
            VTKFILE.append('''
            <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCase/postProcessing/XSec1/'''+str(ff)+'''/interpolatedSurface.vtp"/>''')
            
        VTKFILE.append('''
          </Collection>

        </VTKFile>''')
        with open('RunCase/InterpSurface.pvd','w') as f:
            f.seek(0)
            for x in VTKFILE:
                for line in x:
                    f.write(line)
                    f.truncate()

    def parseOpenFOAMFSOutput(self): 

        G=glob.glob("RunCase/OpenFOAMCase/postProcessing/freeSurfaceVTK/*")
        G= [i.replace('RunCase/OpenFOAMCase/VTK/','') for i in G]
        G= [i.replace('RunCase/OpenFOAMCase_','') for i in G]
        G= [i.replace('RunCase/OpenFOAMCaseBoundary_','') for i in G]
        G= [i.replace('RunCase/OpenFOAMCase_Boundary_','') for i in G]
        G= [i.replace('RunCase/OpenFOAMCase_Boundary','') for i in G]
        G= [i.replace('Boundary','') for i in G]
        G= [i.replace('RunCase/OpenFOAMCase','') for i in G]
        G= [i.replace('/postProcessing/freeSurfaceVTK/','') for i in G]
        G= [i.replace('yCut.vtp','') for i in G]

        I=set(G)
        print(I)


        II=[]
        tol=1e-4
        # remove the times which are 'near' the output increment
        for ii in I:
            print(float(ii),config.writeDT,float(ii)%config.writeDT)
            if float(ii)%config.writeDT<tol:
                II.append(ii)
            elif float(ii)%config.writeDT+tol>config.writeDT:
                II.append(ii)
            else:
                pass
            
        
        self.ofpvdtimes=list(II)
        VTKFILE=['''<?xml version="1.0"?>
        <VTKFile type="Collection" compressor="vtkZLibDataCompressor" >
          <Collection>''']

        for ff in II:
            VTKFILE.append('''
            <DataSet timestep="'''+str(float(ff))+'''"  file="OpenFOAMCase/postProcessing/freeSurfaceVTK/'''+str(ff)+'''/freeSurface.vtp"/>''')

        VTKFILE.append('''
          </Collection>
        </VTKFile>''')
        with open('RunCase/FreeSurface.pvd','w') as f:
            f.seek(0)
            for x in VTKFILE:
                for line in x:
                    f.write(line)
                    f.truncate()


    def createFOAMySeesFigure(self):

        point=0
        readers=[]
        self.lens=[]
        
        if self.checkboxPlotOS.isChecked():

                reader=pv.get_reader('RunCase/OpenSeesOutput.pvd')
                reader.set_active_time_point(0)
                reader.active_time_value
                readers.append(reader)
                #self.textEdit.append('OpenSees Data Sets')
                #for ds in reader.datasets:
                #    self.textEdit.append(str(ds))
                self.lens.append(len(reader.time_values))
                
        if self.checkboxPlotFreeSurf.isChecked():

                reader2=pv.get_reader('RunCase/FreeSurface.pvd')
                reader2.time_values
                reader2.set_active_time_point(0)
                reader2.active_time_value
                readers.append(reader2)
                #self.textEdit.append('OpenFOAM Data Sets')
                #for ds in reader2.datasets:
                #    self.textEdit.append(str(ds))
                self.lens.append(len(reader2.time_values))
                
        if self.checkboxPlotxSec.isChecked():
                reader3=pv.get_reader('RunCase/InterpSurface.pvd')
                reader3.time_values
                reader3.set_active_time_point(0)
                reader3.active_time_value
                readers.append(reader3)
                self.lens.append(len(reader3.time_values))
                #self.textEdit.append('OpenFOAM Data Sets')
                #for ds in reader3.datasets:
                #    self.textEdit.append(str(ds))
        
        self.FYSplotter.readers=readers
        self.FYSplotter.activeactors=self.makeActors(readers)
        
        minlen=np.min(self.lens)
        for time in [self.xsectimes[:],self.ofpvdtimes[:],self.ospvdtimes[:]]:
        
            self.textEdit.append(str(time))
      
        for u in range(0,minlen):
            if self.checkboxPlotClear.isChecked():
                self.FYSplotter.clear()
            self.set_time(u)
            self.FYSplotter.show()
            self.FYSplotter.update()
            self.FYSplotter.render()   
            self.FYSplotter.show()

    ##########################################################################################################
    def mainWidgetVisualize(self):
        self.checkboxPlotOS = QCheckBox('Plot OpenSees Model', self)
        self.checkboxPlotFreeSurf = QCheckBox('Plot Free Surface', self)
        self.checkboxPlotxSec = QCheckBox('Plot OpenFOAM Cross-Section', self)
        self.checkboxPlotClear = QCheckBox('Clear Previous Timesteps', self)
        
        self.checkboxPlotOS.setChecked(True)
        self.checkboxPlotFreeSurf.setChecked(True)
        self.checkboxPlotxSec.setChecked(False)
        
        self.checkboxPlotClear.setChecked(True)
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
        fig_int = QVBoxLayout()

        buttonPlotFOAMySees = QPushButton('Plot FOAMySees Model')
        
        #buttonPlotOpenFOAM = QPushButton('Plot OpenFOAM Model')

        
        #buttonPlotCouplingDataProjectionMesh = QPushButton('Plot Coupling Data Projection Mesh')
        
        Hbtnlyt.addWidget(buttonPlotFOAMySees)
        Hbtnlyt.addWidget(self.checkboxPlotOS)
        Hbtnlyt.addWidget(self.checkboxPlotFreeSurf)
        Hbtnlyt.addWidget(self.checkboxPlotxSec)
        Hbtnlyt.addWidget(self.checkboxPlotClear)
        #Hbtnlyt.addWidget(buttonPlotCouplingDataProjectionMesh)
        
        mainHolder.addLayout(Hbtnlyt)

        self.FYSplotter = pvqt.QtInteractor()
        fig_int.addWidget(self.FYSplotter)

        mainHolder.addLayout(fig_int)

        self.FYSplotter.show()
        
        Hlyt1.addLayout(mainHolder)

        # Creating a vertical layout within which layouts 1-4 will reside
        layout = QVBoxLayout()  # Initializing the vertical layout
        layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout


        widget = QWidget()  # Creating a widget to store layouts in
        # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
        widget.setLayout(layout)  # Setting layout of the widget
        self.setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window

        #self.SetFigure()

        # Connections
        buttonPlotFOAMySees.clicked.connect(self.handlePlotFOAMySeesModel)
        #buttonPlotOpenFOAM.clicked.connect(self.handleButtonOpenFOAM)
        #buttonPlotCouplingDataProjectionMesh.clicked.connect(self.handleButtonCouplingDataProjectionMesh)

        return widget




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
        self.scl3ind.setText(str(numStepsOpenSees))
        self.scl4ind.setText(str(numStepsOpenFOAM))
        self.OpenSeesConnect(OpenSeesFile)
        self.DTSpinBox.setValue(DT)
    #    DTSpinBox.setText(str(DT))
        self.OpenFOAMConnect(OpenFOAMCaseFolder)
        self.ExplicitOrImplicit=myvar[5][0]
        self.ImplicitMethod=myvar[5][1]    
        self.resetVars()




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
        import FSIPVD
        self.plotModel()
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
        self.show()
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
                self.textEdit.append('no log file ')

    def plotSys(self):
        doAthing=0
        if doAthing==0:
            pass
        else:
            pass

    def getAnalysisLog(self):

        try:
         #Popen("cd "+GUIRootLocation).wait()
            Popen("tail -f RunCase/fys_logs/FOAMySeesCouplingDriver.log")
            
        except: 
            self.textEdit.append('no log file exists yet')
        self.getLog()

    def getLog(self):
        self.textEdit.clear()
        try:
         #Popen("cd "+GUIRootLocation).wait()
            with open("RunCase/fys_logs/FOAMySeesCouplingDriver.log", "r") as fileInput: 
                self.textEdit.append(fileInput.read())   
        except: 
                self.textEdit.append('no log file yet')
        self.clearLog()
        
    def runProcess(self,process):
        Popen(process, shell=True)

    def runProcessAndWait(self,process):
        Popen(process, shell=True).wait()


    def handleButtonRunFOAMySees(self):

        os.system("cleanFYS")
        os.system("startFOAMySees")
        self.textEdit.append('started FOAMySees analysis')
        Popen("tail -f RunCase/fys_logs/FOAMySeesCouplingDriver.log")
        
    def LoadJSONAction(self):
        filename = QFileDialog.getOpenFileName("Select a json file ","JSON Files (*.json)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to Hydro UQ JSON File: ' + str(filename[0])

        self.setWindowTitle(connstr)

        self.JSONConnect(filename[0])
        


        #

        #
    def SaveSettingsAction(self):
        DT=DTSpinBox.value()
        self.setVars()
        CouplingSettings=[ExplicitOrImplicit,ImplicitMethod]
         
        # Create a variable 
        myvar = [OpenSeesFile,OpenFOAMCaseFolder,numStepsOpenSees,numStepsOpenFOAM,DT,CouplingSettings] 
          
        # Open a file and use dump() 
        with open('FOAMySeesGUISavefile.pkl', 'wb') as file: 
              
            # A new file will be created 
            pickle.dump(myvar, file) 

    def LoadOpenFOAMAction(self):
        filename = QFileDialog.getExistingDirectory("Select an OpenFOAM case folder " ,"Folder (*/)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to OpenFOAM Case: ' + str(filename)
        self.setWindowTitle(connstr)
        self.OpenFOAMConnect(filename)
        
    def LoadOpenSeesAction(self):
        filename = QFileDialog.getOpenFileName("Select an OpenSeesPy file ", "Python Files (*.py)",options=QFileDialog.DontUseNativeDialog)
        connstr='FOAMySees - Connected to OpenSees File: ' + str(filename[0])
        self.setWindowTitle(connstr)
        self.OpenSeesConnect(filename[0])
            
    def branchVis(self):
        LogFile="FOAMySeesGUILog"
        try:
                
                Sees=FOAMySeesInstance(1,config)

                N = len(Sees.coupledNodes) # number of ops.nodes
                with open(LogFile) as f:        
                        print("N: " + str(N), file=f)

                CouplingDataProjectionMesh=Sees.config.CouplingDataProjectionMesh

                solverName = "Solid1"

                dimensions=3

                dimensions=3 # overruling that #	bounding_box : array_like
                while not os.path.exists(CouplingDataProjectionMesh):
                        time.sleep(1)

                if os.path.isfile(CouplingDataProjectionMesh):
                        with open(CouplingDataProjectionMesh) as f:
                                lines=f.read()
                else:
                        raise ValueError("%s could not be found" % CouplingDataProjectionMesh)
                lines=lines.split('\n')
                points=[]
                facets=[]
                Branches=[]
                # for obj
                if '.obj' in CouplingDataProjectionMesh:
                        for line in lines:
                                #print(line[:])
                                if '#' in str(line[:]):
                                        pass
                                elif 'g' in line:
                                        pass
                                elif 'v' in line:
                                        points.append(line.strip('v ').split(' '))
                                elif 'f' in line:
                                        facets.append(line.strip('f ').split(' '))
                        #print(points)
                        #print(facets)
                        for facet in facets:
                                if ('#' in facet) or ('g' in facet) or ('o' in facet):
                                        pass
                                else:
                                        branch=np.zeros([1,3],dtype=float)
                                        ptfacet=0
                                        for i in facet:
                                                if i=='':
                                                        pass
                                                else:
                                                        pt=points[int(i)-1]
                                                        for iin in pt:
                                                                iin=float(iin)
                                                        pt=np.array(pt,dtype=float)
                                                        branch+=pt
                                                        ptfacet+=1
                                        with open(fys_couplingdriver_log_location, 'a+') as f:
                                                print(branch/ptfacet,file=f)
                                        Branches.append(branch[0]/ptfacet)

                Branches=np.array(Branches)					   

                # print(Branches)                      
                Tree=KDTree(Sees.nodeLocs)
                BranchToNodeRelationships=Tree.query(Branches)[1]
                vertices=Branches
                NodeToBranchNodeRelationships=[]
     
                for n in range(len(Sees.nodeLocs)):

                        NodeToBranchNodeRelationships.append([n])
                # vertices=[]
                nodeCount=0
                for node in range(len(BranchToNodeRelationships)):
                        NodeToBranchNodeRelationships[BranchToNodeRelationships[node]].append(node)
                with open(LogFile) as f:
                    print(NodeToBranchNodeRelationships,file=f)
                vertices=np.array(vertices)
                with open('BranchesLOCS.log', 'a+') as f:
                        f.seek(0)
                        f.truncate()
                        print(NodeToBranchNodeRelationships,file=f)
                        print(vertices,file=f)
                        print(np.shape(vertices),file=f)

                Sees.NodeToBranchNodeRelationships=NodeToBranchNodeRelationships


        except:
                with open(LogFile,'a') as f:
                    print('The Coupling Data Projection Mesh or the OpenSees Model does not exist. Make sure everything else is set up',file=f)
        self.getLog()
        
    def initialValues(self):
        
        #hydro UQ
        self.AdjustTimeStep="" # Yes No
        self.ApplyGravity="" # Yes No
        self.CouplingScheme="" #Implicit Explicit
        self.SeesVTKOUT=""  # Yes No
        self.SeesVTKOUTRate=0.0 #float
        self.FOAMVTKOUT="" # Yes No
        self.FOAMVTKOUTRate=0.0 #float
        self.SimDuration=0 #float
        self.SolutionDT=0 #float
        self.Turbulence=""  # Yes No
        self.couplingConvergenceTol=0 #float
        self.bathType="" #Point List / Surface / not sure what else, would have to look
        self.bathSTL="" # the name of the surface
        self.bathXZData=[
            [
                0,
                0
            ],
            [
                0,
                0
            ]  ]
        self.couplingDataAccelerationMethod="" # IQN-ILS Aitken Broyden Constant
        self.couplingIterationOutputDataFrequency=0 # integer
        #self.cutSurfaceLocsDirsFields=[[
        #        0.1,
        #        0.01,
        #        0.01,
        #        0,
        #        0,
        #        1,
        #        "XSec1",
        #        "p,U,alpha.water"
        #    ]  ]
        self.cutSurfaceLocsDirsFields=[[]]
        self.cutSurfaceOutput=""   # Yes No
        self.domainSubType="" # UW WASIRF etc etc
        self.fieldProbeLocs=[    ] # this is a list of lists
        self.fieldProbes=""   # Yes No
        self.flumeHeight=0.0 # float Z coords
        self.flumeLength=0.0 # float X coords
        self.flumeWidth=0.0  # float Y cooords
        self.flumeCellSize=0.0 #float
        self.freeSurfOut="" # Yes No
        self.freeSurfProbeLocs=[    ] # this is a list of lists
        self.freeSurfProbes="" # Yes No
        self.g=0.0 #float
        self.initVelocity=0.0 #float
        self.initialRelaxationFactor=0.0 #float
        
        self.interfaceSurface="" # interface.stl
        self.interfaceSurfaceOutput="" # Yes No
        self.mapType="" # Nearest neigbor, rbf etx
        self.maximumCouplingIterations=0 #integer
        self.openSeesPyScript="" # name of the pythons 
        
        self.outputDataFromCouplingIterations="" # Yes No
        self.paddleDispFile="" # this is a csv file
        self.periodicWaveCelerity=0 #float
        self.periodicWaveMagnitude=0 #float
        self.periodicWaveRepeatPeriod=0 #float
        self.refPressure=0 #float

        self.stillWaterLevel=0 #float
        self.turbIntensity=0 #float
        self.turbRefLength=0 #float
        self.turbReferenceVel=0 #float
        self.velocityFile="" # this is a csv file
        self.waveType="" # No Waves, etcs
        self.writeDT=0 #float
        
        #coupledAnalysisSettings.py
        oneWay=0 # if this is 1, then the displacements calculated by OpenSees are not transferred to OpenFOAM
        numOpenSeesStepsPerCouplingTimestep=1
        numOpenFOAMStepsPerCouplingTimestep=1
        SolutionDT=1e-4 # this is the coupling timestep length
        runPrelim='no' # run the preliminary analysis defined (maybe remove this???)
        startOFSimAt=0.0
        endTime=1
        runSnappyHexMesh="No"
        couplingStartTime=0.00
        ApplyGravity='yes'
        g=[0,0,-9.81]
        OpenSeesconvergenceTol=1e-8
        Test=["NormUnbalance",OpenSeesconvergenceTol,1000]
        Integration=["Newmark",0.5,0.25]
        Algorithm="KrylovNewton"
        OpenSeesSystem='BandGen'
        OpenSeesConstraints='Plain'
        Numberer='RCM'
        OSndm=3
        OSndf=6
        Analysis=["VariableTransient","-numSubLevels",2,"-numSubSteps",1000]
        AdjustTimeStep='no'
        SimDuration=endTime
        Turbulence="No"
        interfaceSurface="interface.stl"
        DecompositionMethod="scotch"
        CouplingScheme="Implicit" # "Explicit"
        timeWindowsReused=3		# number of past time windows used to approximate secant behavior
        iterationsReused=5		# number of iterations used to accelerate coupling data
        couplingConvergenceTol=5e-3     # coupling data relative residual convergence value
        initialRelaxationFactor=0.1     # initial relaxation factor used in dynamic relaxation scheme
        couplingDataAccelerationMethod="IQN-ILS" #Constant Aitken IQN-IMVJ Broyden
        maximumCouplingIterations=100 #set this to a high value
        mapType='nearest-neighbor' #'rbf-thin-plate-splines'# either or - nearest-neighbor is faster, rbf is more robust...
        writeDT=0.01 # seconds
        SeesVTKOUTRate=0.01 # seconds
        outputDataFromCouplingIterations="No"
        couplingIterationOutputDataFrequency="1000"
        # Set fixity options
        ########################### only use if you want to
        fixXat=[0.0] # this is a list
        fixYat=[0.0] # this is a list
        fixZat=[0.0]# this is a list
        ###########################################################################################################
        fixX='no' # change this to yes to apply a fixity BC along the domain at the coordinates within 'fixXat' list
        fixY='no'# change this to yes to apply a fixity BC along the domain at the coordinates within 'fixYat' list
        fixZ='no'# change this to yes to apply a fixity BC along the domain at the coordinates within 'fixZat' list
        ###########################################################################################################
        fixXatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixXat' list
        fixYatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixYat' list
        fixZatFixity=[1,1,1,1,1,1] # this is the fixity BC which will be applied at the coordinates within 'fixZat' list


        
                

        

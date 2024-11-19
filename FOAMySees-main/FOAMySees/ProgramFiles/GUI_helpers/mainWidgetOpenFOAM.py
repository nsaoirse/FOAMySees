def mainWidgetOpenFOAM():
    # Vertical Layouts
    Canvas4 = QVBoxLayout()  # Initializing the main vertical box layout for the System Figure
    
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
    mainHolder.addLayout(Canvas4)
    Hlyt1.addLayout(mainHolder)

 
    # Creating a vertical layout within which layouts 1-4 will reside
    layout = QVBoxLayout()  # Initializing the vertical layout
    layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout
    layout.addLayout(Hlyt2)  # .
    layout.addLayout(Hlyt3)  # .

    widget = QWidget()  # Creating a widget to store layouts in
    # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
    widget.setLayout(layout)  # Setting layout of the widget

    SetFigureOpenFOAM()




    # Connections
    buttonOpenFOAMRunPreliminaryOpenFOAMAnalysis.clicked.connect(handleOpenFOAMRunPreliminaryOpenFOAMAnalysis)
    buttonOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis.clicked.connect(handleOpenFOAMRunPreliminaryOpenFOAMGravityAnalysis)

    buttonOpenFOAMPlotOpenFOAM.clicked.connect(handleOpenFOAMButtonOpenFOAM)
    buttonOpenFOAMPlotOpenFOAMFields.clicked.connect(handleOpenFOAMButtonOpenFOAMFields)


    return widget    

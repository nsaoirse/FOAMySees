##########################################################################################################
def mainWidgetVisualize():
    # Vertical Layouts
    Canvas1 = QVBoxLayout()  # Initializing the main vertical box layout for the System Figure
    Canvas2 = QVBoxLayout()  # Initializing the main vertical box layout for Results Figure
    mainHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for load scaling
    ScaleSliderHolder = QVBoxLayout()  # Initializing the vertical box layout for the slider for results scaling

    # Horizontal Layouts
    Hlyt1 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    Hlyt2 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    Hlyt3 = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons
    Hbtnlyt = QHBoxLayout()  # Initializing the main horizontal box layout for various buttons

    emp = QLabel('')
    Empty = QVBoxLayout(emp)
    

    buttonPlotOpenSees = QPushButton('Plot OpenSees Model')
    
    buttonPlotOpenFOAM = QPushButton('Plot OpenFOAM Model')

    
    buttonPlotCouplingDataProjectionMesh = QPushButton('Plot Coupling Data Projection Mesh')
    
    Hbtnlyt.addWidget(buttonPlotOpenSees)
    Hbtnlyt.addWidget(buttonPlotOpenFOAM)
    Hbtnlyt.addWidget(buttonPlotCouplingDataProjectionMesh)
    
    mainHolder.addLayout(Hbtnlyt)
    mainHolder.addLayout(Canvas1)

    Hlyt1.addLayout(mainHolder)



    # Creating a vertical layout within which layouts 1-4 will reside
    layout = QVBoxLayout()  # Initializing the vertical layout
    layout.addLayout(Hlyt1)  # Adding layouts to the vertical layout


    widget = QWidget()  # Creating a widget to store layouts in
    # Assigning layout to a dummy widget which will be assigned to be the Central Widget of the QMainWindow window
    widget.setLayout(layout)  # Setting layout of the widget
    setCentralWidget(widget)  # Assigning the dummy widget to the central widget of the main window

    SetFigure()




    # Connections
    buttonPlotOpenSees.clicked.connect(handleButtonOpenSees)
    buttonPlotOpenFOAM.clicked.connect(handleButtonOpenFOAM)
    buttonPlotCouplingDataProjectionMesh.clicked.connect(handleButtonCouplingDataProjectionMesh)


        
    return widget 

def LoadSettingsAction():
        # Open the file in binary mode 
    with open('FOAMySeesGUISavefile.pkl', 'rb') as file: 
          
        # Call load method to deserialze 
        myvar = pickle.load(file) 
        
        print(myvar) 
    OpenSeesFile=myvar[0]
    OpenFOAMCaseFolder=myvar[1]
    numStepsOpenSees=myvar[2]
    numStepsOpenFOAM=myvar[3]    
    DT=myvar[4]
    scl3ind.setText(str(numStepsOpenSees))
    scl4ind.setText(str(numStepsOpenFOAM))
    OpenSeesConnect(OpenSeesFile)
    DTSpinBox.setValue(DT)
#    DTSpinBox.setText(str(DT))
    OpenFOAMConnect(OpenFOAMCaseFolder)
    ExplicitOrImplicit=myvar[5][0]
    ImplicitMethod=myvar[5][1]    
    resetVars()

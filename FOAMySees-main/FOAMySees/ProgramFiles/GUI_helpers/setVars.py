
def setVars():
    if ExplicitRB.isChecked():
        ExplicitOrImplicit="Explicit"
    if ImplicitRB.isChecked():
        ExplicitOrImplicit="Implicit"     
    if AitkenRB.isChecked():
        ImplicitMethod="Aitken"         
    if IQNILSRB.isChecked():
        ImplicitMethod="IQNILS"
    if IQNIMVJRB.isChecked():
        ImplicitMethod="IQNIMVJ"
    if ConstantRB.isChecked():
        ImplicitMethod="Constant"
    numStepsOpenSees=scl3ind.text()
    numStepsOpenFOAM=scl4ind.text()

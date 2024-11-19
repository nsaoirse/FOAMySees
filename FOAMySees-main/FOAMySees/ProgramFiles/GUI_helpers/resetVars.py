


def resetVars():
    if ExplicitOrImplicit=="Explicit":
        ExplicitRB.setChecked(1)
    if ExplicitOrImplicit=="Implicit":
        ImplicitRB.setChecked(1)
    if ImplicitMethod=="Aitken":

        AitkenRB.setChecked(1)
    if ImplicitMethod=="IQNILS":
        IQNILSRB.setChecked(1)       
    if ImplicitMethod=="IQNIMVJ":
        IQNIMVJRB.setChecked(1)
    if ImplicitMethod=="Constant":
        ConstantRB.setChecked(1)        

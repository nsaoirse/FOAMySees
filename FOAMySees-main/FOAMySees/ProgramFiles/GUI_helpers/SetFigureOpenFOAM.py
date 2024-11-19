
def SetFigureOpenFOAM(w=5, h=3.5):
    # FIGURE 1
    sysplotOpenFOAM = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

    sysplotaxOF = sysplotOpenFOAM.add_subplot()
    F1OF = FigureCanvas(sysplotOpenFOAM)
    Canvas4.addWidget(F1OF)


    F1OF.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #

    #


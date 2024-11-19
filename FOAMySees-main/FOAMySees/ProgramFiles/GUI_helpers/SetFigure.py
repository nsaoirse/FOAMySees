
def SetFigure(w=5, h=3.5):
    # FIGURE 1
    sysplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

    sysplotax = sysplot.add_subplot()
    F1 = FigureCanvas(sysplot)
    Canvas1.addWidget(F1)

    # FIGURE 2
    resplot = Figure(figsize=(5, 4), linewidth=1.0, frameon=True, tight_layout=True)

    resplotax = resplot.add_subplot()
    F2 = FigureCanvas(resplot)
    Canvas2.addWidget(F2)

    F1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #
    F2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    show()
    #

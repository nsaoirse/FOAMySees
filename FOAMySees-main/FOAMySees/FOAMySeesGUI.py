import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./ProgramFiles"))
from pyFOAMySeesGUI import *
sys.stderr = open('./error.log', 'w')
if __name__ == "__main__":
    app = QApplication(sys.argv)


    w = pyFOAMySeesGUI()
    w.show()

    sys.exit(app.exec_())

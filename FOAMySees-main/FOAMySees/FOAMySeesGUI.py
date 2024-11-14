
# import additional libraries
import sys
sys.path.insert(0, './ProgramFiles/FOAMySees')
sys.path.insert(0, './ProgramFiles/FOAMySees/FOAMySeesFiles')
sys.path.insert(0, './ProgramFiles/FOAMySees/FOAMySeesFiles/OpenSeesSettings')
sys.path.insert(0, './ProgramFiles/FOAMySees/FOAMySeesFiles/FOAMySees')
sys.path.insert(0, './ProgramFiles/FOAMySees/FOAMySeesFiles/fromUserDefaults')

sys.path.insert(0, './ProgramFiles/GUIFiles')

from pyFOAMySeesGUI import *

if __name__ == "__main__":
    app = QApplication(sys.argv)


    w = pyFOAMySeesGUI()
    w.show()

    sys.exit(app.exec_())

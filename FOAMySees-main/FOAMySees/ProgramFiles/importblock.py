from PyQt5.QtCore import Qt, QProcess


from PyQt5.QtWidgets import QAction, QWidget, QFileDialog, QLabel, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, \
    QMainWindow, QRadioButton, QSizePolicy, QSlider, QComboBox, QButtonGroup, QPushButton, QApplication, QStatusBar,QMessageBox, QLineEdit, QTabWidget, QFrame



from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as pat
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication
import csv
import os
import sys
from contextlib import redirect_stdout
import io
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas)
    

import logging
### FOAMySees
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./.."))
from dependencies import *
import pickle 

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./GUI_helpers"))
import GUI_helpers as GUI_helpers
# import libraries

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,\
    QMainWindow, QStatusBar, QFileDialog, QRadioButton,QTextBrowser, QScrollBar
from PyQt5.QtGui import QPixmap
import os.path as osp

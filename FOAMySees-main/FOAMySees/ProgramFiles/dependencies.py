
### system management
import os
import concurrent.futures
import logging
import queue
import random
import subprocess
import time
from subprocess import Popen, DEVNULL
import argparse
import copy
import sys

## math and matrices
import numpy as np
import pandas as pd
import re, csv
import math as m

### meshes and visualization
import meshio
import matplotlib
from scipy.spatial import KDTree
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import pyvista as pv

## openseespy
import openseespy.opensees as ops
### FOAMySees
FOAMySeesSrcDir = os.environ.get("FOAMySeesSrcDir")
cwdd=os.getcwd()
caseFolder = os.environ.get("whereWasScriptExecutedFrom")
if caseFolder is None:
    caseFolder='.'
sys.path.append(caseFolder)
sys.path.append(caseFolder+"/RunCase")
sys.path.append(FOAMySeesSrcDir+"/ProgramFiles/config_helpers")
sys.path.append(FOAMySeesSrcDir+"/ProgramFiles/FOAMySees")

import configureCoupledCase as config
try:
    import buildOpenSeesModelInThisFile as userModel
except:
    pass
from FOAMySeesObjects import *

## precice
import precice
from precice import *

if os.path.exists('extraImports.py'):
    import extraImports

import sys
import os
FOAMySeesSrcDir = os.environ.get("FOAMySeesSrcDir")
cwdd=os.getcwd()
caseFolder = os.environ.get("whereWasScriptExecutedFrom")
sys.path.append(caseFolder)
sys.path.append(cwdd)
sys.path.append(FOAMySeesSrcDir+"/ProgramFiles/config_helpers")
syspath = os.environ.get("PATH")
os.environ["PATH"] = syspath+":"+FOAMySeesSrcDir+"/ProgramFiles/config_helpers"+":"+FOAMySeesSrcDir+"/FOAMySees"+":"+cwdd+"/OpenSeesSettings"+":"+cwdd+":"+caseFolder
os.environ.get("PATH")
print(os.environ.get("PATH"))

from buildBathymetry import *
from buildBlockMesh import *
from writeOpenFOAMpreCICEDictSinglePhase import *
from buildInitialConditions import *
from buildInletProperties import *
from buildOpenSeesModelFile import *
from buildOpenSeesPreliminaryAnalysisFile import *
from buildSetFields import *
from buildSnappyHexMeshAndSurfaceFeatureExtractDictionariesBathymetry import *
from buildSnappyHexMeshAndSurfaceFeatureExtractDictionariesStructure import *
from configurePrecice import *
from copyUserInputsToCase import *
from findResultantCenterOfRotation import *
from makeFunctionObjectsFromInputs import *
from makePaddleGeneratedWave import *
from makePeriodicWaves import *
from makeVelocityInletTHBC import *
from writeControlDict import *
from writeOpenFOAMDecomposition import *
from writeOpenFOAMpreCICEDict import *

from writeUserLoadRoutines import *

from buildDomain import *

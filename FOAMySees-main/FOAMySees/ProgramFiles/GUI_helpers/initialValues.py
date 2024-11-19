
def initialValues():
    AdjustTimeStep="No"
    ApplyGravity="Yes"
    CouplingScheme="Implicit"
    SeesVTKOUT="Yes"
    SeesVTKOUTRate=0.01
    FOAMVTKOUT="Yes"
    FOAMVTKOUTRate=0.01
    SimDuration=1
    SolutionDT=5e-4
    Turbulence="No"
    couplingConvergenceTol=5e-2
    bathType="Point List"
    bathSTL="flumeFloor.stl"
    bathXZData=[
        [
            19.908,
            -1
        ],
        [
            19.908,
            0.152
        ],
        [
            23.568,
            0.152
        ],
        [
            31.8,
            0.838
        ],
        [
            83,
            0.838
        ],
        [
            101.5,
            2
        ]  ]
    couplingDataAccelerationMethod="IQN-ILS"
    couplingIterationOutputDataFrequency=100
    cutSurfaceLocsDirsFields=[[
            0.1,
            0.01,
            0.01,
            0,

            0,
            1,
            "XSec1",
            "p,U,alpha.water"
        ]  ]
    cutSurfaceOutput="Yes"
    domainSubType="UW WASIRF"
    fieldProbeLocs=[    ]
    fieldProbes="No"
    flumeHeight=0.4
    flumeLength=4
    flumeWidth=0.4
    flumeCellSize=0.1
    freeSurfOut="Yes"
    freeSurfProbeLocs=[    ]
    freeSurfProbes="No"
    g=-9.81
    initVelocity=0
    initialRelaxationFactor=0.1666
    interfaceSurface="interface.stl"
    interfaceSurfaceOutput="Yes"
    mapType="Nearest Neighbor"
    maximumCouplingIterations=100
    openSeesPyScript="OpenSeesModel.py"
    preliminaryAnalysisFile="preliminarystructuralanalysis.py"
    outputDataFromCouplingIterations="No"
    paddleDispFile="paddleDisplacement.csv"
    periodicWaveCelerity=1
    periodicWaveMagnitude=1
    periodicWaveRepeatPeriod=1
    refPressure=0
    runPrelim="No"
    stillWaterLevel=0.2
    turbIntensity=0.25
    turbRefLength=0.125
    turbReferenceVel=0.5
    velocityFile=""
    waveType="No Waves"
    writeDT=0.01

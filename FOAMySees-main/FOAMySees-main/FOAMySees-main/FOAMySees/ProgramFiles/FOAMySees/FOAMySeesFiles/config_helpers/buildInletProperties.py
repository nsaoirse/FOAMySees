from makeVelocityInletTHBC import *
from makePaddleGeneratedWave import *
from makePeriodicWaves import *
def buildInletProperties(waveType,secondaryInput,flag,writeHere='OpenFOAMCase'):
	print('Building inlet properties')
	print("waveType,secondaryInput,flag")
	print(waveType,secondaryInput,flag)

	if waveType=="Periodic Waves":			
		[periodicWaveRepeatPeriod, periodicWaveCelerity, periodicWaveMagnitude]=[secondaryInput[0],secondaryInput[1],secondaryInput[2]]	
		makePeriodicWaves(periodicWaveRepeatPeriod, periodicWaveCelerity, periodicWaveMagnitude,writeHere)
						
	if waveType=="Paddle Generated Waves":
		PADDLETH=flag
		paddleDispFile=secondaryInput
		makePaddleGeneratedWave(PADDLETH,paddleDispFile,writeHere)
		
	if waveType=="No Waves":
		VELTH=flag
		makeVelocityInletTHBC(VELTH,secondaryInput,writeHere)

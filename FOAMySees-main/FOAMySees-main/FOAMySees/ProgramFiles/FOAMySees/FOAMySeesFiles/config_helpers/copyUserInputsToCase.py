from subprocess import Popen
def copyUserInputsToCase(fromHere='../userInputs'):
	Popen("cp "+fromHere+"/* .",shell=True)
	print('copied input case files to RunCase directory')


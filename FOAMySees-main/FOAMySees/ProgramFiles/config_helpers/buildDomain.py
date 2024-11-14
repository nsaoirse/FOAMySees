
from subprocess import Popen, DEVNULL

def buildDomain(domainSubType,retrieveFromHere,writeHere):
	print('Building domain')
	print("domainSubType")
	print(domainSubType)


	if (domainSubType=="UW WASIRF") or (domainSubType=="INLETOUTLET"):
		Popen('rm -rf '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		Popen('cp -r '+retrieveFromHere+'/0.org-WASIRF  '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()

	if domainSubType=="WAVES":	
		Popen('rm -rf '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		Popen('cp -r  '+retrieveFromHere+'/0.org-WAVES '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		
	if domainSubType=="CLOSED":
		Popen('rm -rf '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		Popen('cp -r  '+retrieveFromHere+'/0.org-CLOSEDWASIRF  '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		
	if domainSubType=="OSU LWF":
		Popen('rm -rf '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
		Popen('cp -r  '+retrieveFromHere+'/0.org-OSULWF  '+writeHere+'/0.org', shell=True, stdout=DEVNULL).wait()
	
	

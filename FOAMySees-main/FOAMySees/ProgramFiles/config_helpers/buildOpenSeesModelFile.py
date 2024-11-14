def buildOpenSeesModelFile(openSeesPyScript,writeHere,copyInputFilesTo='./'):
    print('Building OpenSees Model')
    print(openSeesPyScript)


    with open(copyInputFilesTo+openSeesPyScript,'r') as file:
        lines = [line.rstrip() for line in file]
        
    with open(writeHere+'/buildOpenSeesModelInThisFile.py','w') as f:
        f.seek(0)
        f.write('''from dependencies import *
if os.path.exists('extraImports.py'):
    from extraImports import *
def defineYourModelWithinThisFunctionUsingOpenSeesPySyntax(FOAMySeesInstance):
''')
                
        for line2 in lines:
            f.write('\t')
            f.write(line2)
            f.write('\n')
        for lineline in ['\t','''try:''','\n','\t','\t','''FOAMySeesInstance.coupledNodes=coupledNodes''','\n','\t','''except:''','\n','\t','\t','''FOAMySeesInstance.coupledNodes=ops.getNodeTags()''','\n','\t','''try:''','\n','\t','\t','''FOAMySeesInstance.nodeRecInfoList=nodeRecInfoList''','\n','\t','''except:''','\n','\t','\t','''FOAMySeesInstance.nodeRecInfoList=[]''']:
            f.write(lineline)
            f.truncate()



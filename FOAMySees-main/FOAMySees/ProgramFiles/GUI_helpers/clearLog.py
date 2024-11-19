def clearLog():
    try:
     #Popen("cd "+GUIRootLocation).wait()
        with open("FOAMySeesGUILog", "w") as fileInput: 
            fileInput.seek(0)
            fileInput.truncate()
        
    except: 
            textEdit.append('no log file - run python3 FOAMySeesGUI.py >> FOAMySeesGUILog')

def parseFile():
    """ This is the parsing method. It works by finding the first common delimiter in the file provided
        (if the file is a csv) then parses the file into components and returns those components delimited by
        the field separator selected by the user via the radio buttons in the application
        If the file is not a csv but instead a text file, the program just prints the text in the browser window
        If the file is not a txt or csv, or is a csv and cannot be broken into its components because of an uncommon
        delimitation (not , ; or :), then the program returns an error telling the user that the file cannot be read """

    try:
        if '.csv' or '.txt' in filename:           # then the file is parsed. otherwise an error is shown.
            browser.clear()                        # Clearing the text browser window

            currentfile = open(filename, 'r')      # Opening the file of interest

            text = currentfile.read()                   # Reading the file

            for i in [',', ';', ':', '\\t']:            # Finding the first delimiter in the file
                if i in text:                               # If the delimiter is in the file
                    inputfieldsep = i                           # the delimiter is set as the input delimiter
            if '.csv' in filename:                 # If the file is a csv...
                for lines in text.split('\n'):              # Split it up into lines,
                    curr=fieldsep+' '                  # Then further split by input delimiter
                                                            # and append the output to the text browser (below)
                    browser.append(curr.join((x.strip(inputfieldsep)) for x in lines.split(inputfieldsep)))
            else:                                       # If the file isn't a csv...
                browser.setText(text)              # just print it in the browser
            fileNameInput.setText(filename)   # Setting the Line Edit field to the name of the file path
            # Setting the window title and the status bar message to the full path and abridged path respectively
            setWindowTitle('CSV Viewer: ' + filename)             # main window title, full path
            status.showMessage('Viewing ' + filename.split('/')[-1])  # status bar, abridged path
            Icon.setPixmap(checkIcon)
    except:
        error(2)                   # delimited with something wonky

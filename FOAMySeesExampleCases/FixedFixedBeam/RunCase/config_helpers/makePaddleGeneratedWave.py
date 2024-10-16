def makePaddleGeneratedWave(PADDLETH,paddleDispFile, writeHere):
	print('Making a Paddle Generated Wave')
	if PADDLETH==1:
		import csv
		with open(paddleDispFile,'r') as dest_f:
			data_iter = csv.reader(dest_f,
								   delimiter = ',',
								   quotechar = '"')
			data = [data for data in data_iter]
		data_array = np.asarray(data, dtype = np.float32)
		print(data_array)
		listOfWMTimes=[]
		listOfWMPos=[]
		# print('paddle disp TH', data)#
		for y in data:
			listOfWMTimes.append(y[0])
			listOfWMPos.append(y[1])
		# Export
		fid = open(writeHere+'/constant/wavemakerMovement.txt', 'w')

		fid.write('wavemakerType   Piston;\n')
		fid.write('tSmooth		 1.5;\n')
		fid.write('genAbs		  0;\n\n')

		fid.write('timeSeries {0}(\n'.format( len(listOfWMTimes) ))
		for t in listOfWMTimes:
			fid.write('{0}\n'.format(t))
		fid.write(');\n\n'.format( len(listOfWMTimes) ))

		fid.write('paddlePosition 1(\n')

		fid.write('{0}(\n'.format( len(listOfWMTimes) ))
		for Disp in listOfWMPos:
			fid.write('{0}\n'.format(Disp))	   
		fid.write(')\n')
		fid.write(');\n\n')


		fid.close()		

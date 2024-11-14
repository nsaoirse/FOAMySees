from subprocess import Popen, DEVNULL
def buildInitialConditions(flumeWidth,refPressure,initVelocity,stillWaterLevel,TurbulenceProperties,writeHere):

	print('Building initial conditions, turbulence properties')
	print("refPressure,initVelocity,stillWaterLevel,TurbulenceProperties")
	print(refPressure,initVelocity,stillWaterLevel,TurbulenceProperties)

	if TurbulenceProperties[0]=='Yes':
		turbType='''simulationType  RAS;
		RAS
		{
			RASModel		kOmegaSST;
			turbulence	  on;
			printCoeffs	 on;
		}'''	   
	else:
		turbType='''simulationType  laminar;
	'''			


	turbulenceProperties=['''
	FoamFile
	{
		version	 2.0;
		format	  ascii;
		class	   dictionary;
		location	"constant";
		object	  turbulenceProperties;
	}
	// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

	''',turbType,'''


	// ************************************************************************* //''']
							   
	with open(writeHere+'/constant/turbulenceProperties','w') as f:
		f.seek(0)
		for x in turbulenceProperties:
			for line in x:
				f.write(line)  

		
	ICFILE=['''
// User-defined parameters
''','''
Wflume {};
initialVel {};
SWL {};
pref {};'''.format(flumeWidth,initVelocity,stillWaterLevel,refPressure)]
		
	if TurbulenceProperties[0]=="Yes":
		[turbRefLength,turbReferenceVel,turbIntensity]=[TurbulenceProperties[1],TurbulenceProperties[2],TurbulenceProperties[3]]
		ICFILE.append('''
// Turbulence Calcs
// p_rghIC  #calc "$pref- (0.5*$rho*$initialVel*$initialVel)"; // [Pa] dynamic pressure, p_rgh=p-1/2*rho*U^2
p_rghIC  {}; // [Pa] dynamic pressure, p_rgh=p-1/2*rho*U^2
L_REF	{}; // [m]
U_REF   {}; // [m/s]
INTENSITY  {};
'''.format(refPressure,turbRefLength,turbReferenceVel,turbIntensity)+'''
C_mu 0.09; // [unitless] 
kIC #eval "(3*($INTENSITY*$U_REF)*($INTENSITY*$U_REF))/2"; // [m^2/s^2] turbulent kinetic energy, TKE or k
omegaIC #eval "(1/$L_REF)*pow($kIC,0.5)/pow($C_mu,0.25)"; // [s^-1] specific turbulence frequency, omega
epsilonIC #eval "(1/$L_REF)*pow($kIC,1.5)*pow($C_mu,0.75)"; // [m^2/s^3] TKE dissipation rate, epsilon
// ************************************************************************* //
''')
	Popen('mkdir '+writeHere+'/0.org/ICfiles', shell=True, stdout=DEVNULL).wait()
	with open(writeHere+'/0.org/ICfiles/initialConditions','w') as f:
		f.seek(0)
		for x in ICFILE:
			for line in x:
				f.write(line)

import os
import concurrent.futures
import logging
import queue
import random
import subprocess
from subprocess import Popen, DEVNULL, STDOUT
import time
import logging
#logging.basicConfig(filename='errors.log', level=logging.ERROR)

import pandas as pd
import re, csv
import matplotlib
import argparse
import numpy as np
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '.')
sys.path.insert(0, '../OpenSeesPySettings')
sys.path.insert(0, '../fromUser')
sys.stderr = open('./fys_logs/What is Happening With OpenSees.log', 'a+')
import configureCoupledCase as config

try:
    import buildOpenSeesModelInThisFile as userModel
except:
    pass

try:
    import userLoadRoutines as userLoadRoutines
except:
    pass

import math as m

import copy


import math

import meshio

# from openseespy.postprocessing.Get_Rendering import * 
from openseespy.opensees import *
import openseespy.opensees as ops


try:
    import preliminaryAnalysis as prelimAnalysis
except:
    pass

import createRecorders as createRecorders

import time

if os.path.exists('extraImports.py'):
    import extraImports
    
class FOAMySeesInstance():
	def __init__(self, dt, config, parent=None):
	
		# Define properties
		self.dt = dt
		self.time=[0]
		self.step=0
		
		self.whatTimeIsIt=0
		self.config=config
		if self.config.TaylorSeriesStabilize=='no':
			self.ForcePredictionAlpha=0.0
		else:
			self.ForcePredictionAlpha=self.config.alphaTS
			
		if self.config.stagger=='yes':
		        self.PredictionTend=1.5*self.dt*self.config.betaTS
		else:
		        self.PredictionTend=2*self.dt*self.config.betaTS
		        
		self.totalSteps=self.config.endTime/self.dt
		self.currentTStackPositionF=1
		self.currentTStackPositionD=1
                		
		self.fys_couplingdriver_log_location='fys_logs/FOAMySeesCouplingDriver.log'
		self.work_log_location='fys_logs/WorkInAndOut.log'
		self.work_array_location='fys_logs/WorkInAndOutArray.log'
		self.branch_log='fys_logs/BranchesLOCS.log'
		self.opensees_log_location='fys_logs/What is Happening With OpenSees.log'

		self.createRecorders=createRecorders
		try:
		    
		    self.prelimAnalysis=prelimAnalysis
		except:
		    pass
		
		self.OmegaDamp=1
		Popen('rm -rf SeesCheckpoints', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('mkdir SeesCheckpoints', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('rm -rf SeesOutput', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('mkdir SeesOutput', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('touch SeesOutput.pvd', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		self.userModel=userModel.defineYourModelWithinThisFunctionUsingOpenSeesPySyntax(self)
		self.makeDataArrays()
			
	def calculateUpdatedMoments(self,Forces):
		self.currentTStackPositionF+=1
		for node_num in range(len(self.coupledNodes)):
			
			self.displacement[node_num][0:6]=ops.nodeDisp(self.nodeList[node_num])
			[phi,theta,psi]=self.displacement[node_num][3:6]
			

			originalBranchGroup=self.verticesForce[self.NodeToCellFaceCenterRelationships[node_num][1:],:]-self.nodeLocs[node_num]
			
			rotatedBranchGroup=self.RotateTreeBranch(originalBranchGroup,phi,theta,psi)
			
			[RBGDX,RBGDY,RBGDZ]=[rotatedBranchGroup[:,0],rotatedBranchGroup[:,1],rotatedBranchGroup[:,2]]
			[FXx,FYy,FZz]=[Forces[self.NodeToCellFaceCenterRelationships[node_num][1:],:][:,0],Forces[self.NodeToCellFaceCenterRelationships[node_num][1:],:][:,1],Forces[self.NodeToCellFaceCenterRelationships[node_num][1:],:][:,2]]

			self.moment[node_num,:]=[np.dot(FZz,RBGDY)-np.dot(FYy,RBGDZ), np.dot(FXx,RBGDZ)-np.dot(FZz,RBGDX), np.dot(FYy,RBGDX)-np.dot(FXx,RBGDY)]
			self.forceandmoment[node_num,3:6]=self.moment[node_num,:]
			self.forceandmoment[node_num,0:3]=self.force[node_num,:]
		if self.config.betaTS<self.currentTStackPositionF:				        
                    self.Flast5times[:,4]=self.Flast5times[:,3]
                    self.Flast5times[:,3]=self.Flast5times[:,2]
                    self.Flast5times[:,2]=self.Flast5times[:,1]
                    self.Flast5times[:,1]=self.Flast5times[:,0]
                    self.Flast5times[:,0]=np.reshape(self.forceandmoment,[self.ndofs,])[:]
                    self.currentTStackPosition=1	
	def projectDisplacements(self,Displacement,project=0):
		
		for node_num in range(len(self.coupledNodes)):
			
			self.displacement[node_num][0:6]=ops.nodeDisp(self.nodeList[node_num])
			[phi,theta,psi]=self.displacement[node_num][3:6]
			
			self.phithetapsi[node_num][0:3]=[phi,theta,psi]
			self.velocity[node_num][0:6]=ops.nodeVel(self.nodeList[node_num])
			self.acceleration[node_num][0:6]=ops.nodeAccel(self.nodeList[node_num])
			
			originalBranchGroup=self.verticesDisplacement[self.NodeToBranchNodeRelationships[node_num][1:],:]-self.nodeLocs[node_num]

			rotatedBranchGroup=self.RotateTreeBranch(originalBranchGroup,phi,theta,psi)
			rotatedBranchDeltas=rotatedBranchGroup-originalBranchGroup
			

			Displacement[self.NodeToBranchNodeRelationships[node_num][1:]]=rotatedBranchDeltas+self.displacement[node_num,0:3]

		if self.config.betaTS<self.currentTStackPositionD:
			self.Dlast5times[:,4]=self.Dlast5times[:,3]
			self.Dlast5times[:,3]=self.Dlast5times[:,2]
			self.Dlast5times[:,2]=self.Dlast5times[:,1]
			self.Dlast5times[:,1]=self.Dlast5times[:,0]
			self.Dlast5times[:,0]=np.reshape(self.displacement,[self.ndofs,])[:]
			self.currentTStackPositionD=1
			
		if project==0:
                	pass
		else:
                	self.TSExpPredict(self.Dlast5times)

                	Displacement=self.projectDisplacements(Displacement)
		return Displacement
	    
	def TSExpPredict(self,predictWhat):

		dt=self.dt*self.config.betaTS

		N=self.ndofs

		ysel=predictWhat # this is a Nx5 array with the DOF's last 5 values

		#####
		# in the solution loop

		dt_t=self.PredictionTend

		result=np.array(np.einsum('mnp,mp->mn', self.CinvStar, ysel))

		D1=result[:,0]
		D2=result[:,1]
		D3=result[:,2]
		D4=result[:,3]
		D5=result[:,4]

		prediction=D1 + D2*dt_t + D3*(dt_t**2)/math.factorial(2) + D4*(dt_t**3)/math.factorial(3) + D5*(dt_t**4)/math.factorial(4) #https://arxiv.org/pdf/2002.11438

		#print('real value', inp[4])
		#print('prediction', prediction)

		return np.reshape(np.array(prediction),[len(self.coupledNodes),6])
			
	def readCheckpoint(self,stepOut):
		ops.database('File',"SeesCheckpoints/checkpoints/"+str(stepOut))
		#ops.wipeAnalysis()
		ops.restore(stepOut)
		
		with open(self.opensees_log_location, 'a+') as f:
			print('read a checkpoint from opensees time = ',self.thisTime,file=f)
		ops.setTime(self.thisTime)	
		
	def writeCheckpoint(self,stepOut):
		ops.database('File',"SeesCheckpoints/checkpoints/"+str(stepOut))
		ops.save(stepOut)
		newStep=0
		self.thisTime=copy.deepcopy(ops.getTime())
		with open(self.opensees_log_location, 'a+') as f:

			print('Wrote a checkpoint at opensees time = ',self.thisTime,file=f)	

	def fixitySet(self):
		if self.config.fixX=='yes':
			for xLoc in self.config.fixXat:
				fixX(xLoc,*[1,1,1,1,1,1])
		if self.config.fixY=='yes':
			for yLoc in self.config.fixYat:
				fixY(yLoc,*[1,1,1,1,1,1])
		if self.config.fixZ=='yes':
			for zLoc in self.config.fixZat:
				fixZ(zLoc,*[1,1,1,1,1,1])
				
	def makeDataArrays(self):
		dt=self.dt*self.config.betaTS	
		self.time = []
		try: 	
			print("trying to find a coupled nodes list...")
			self.NNODES=len(self.coupledNodes)
		except: 
			print("making a coupled nodes list from all nodes *this might include nodes which are constrained within the finite element domain*...")
			self.coupledNodes=ops.getNodeTags()
			self.NNODES=len(self.coupledNodes)
		print(nodeBounds())

		nodeList=self.coupledNodes
		self.nodeList=self.coupledNodes
		self.nodeLocs=np.zeros([len(self.coupledNodes),3])
		self.printThis=np.zeros([len(self.coupledNodes),3])

		for node in range(0,len(nodeList)):		  
			self.nodeLocs[node,:]=nodeCoord(nodeList[node])
			
		self.NodalReactionForces=np.zeros([len(self.coupledNodes),3])
		self.lastForces=np.zeros([len(self.coupledNodes),3])
		self.lastDisplacements=np.zeros([len(self.coupledNodes),6])

		self.ndofs=len(self.coupledNodes)*6
		
		self.Flast5times=np.zeros([self.ndofs,5])
		self.Dlast5times=np.zeros([self.ndofs,5])
		
		self.phithetapsi=np.zeros([len(self.coupledNodes),3])

		self.force=np.zeros([len(self.coupledNodes),3])
		self.displacement=np.zeros([len(self.coupledNodes),6])

		self.velocity=np.zeros([len(self.coupledNodes),6])
		self.acceleration=np.zeros([len(self.coupledNodes),6])
		self.forceandmoment=np.zeros([len(self.coupledNodes),6])

		###########
		# in initialization

		C=np.zeros([5,5])
		C[0,:]=[1, -2*dt,		     2*dt**2, -(8/math.factorial(3))*dt**3, (16/math.factorial(4))*dt**4]
		C[1,:]=[1,   -dt, (1/math.factorial(2))*dt**2, -(1/math.factorial(3))*dt**3,  (1/math.factorial(4))*dt**4]
		C[2,:]=[1,     0,			   0,			    0,			    0]
		C[3,:]=[1,    dt, (1/math.factorial(2))*dt**2,  (1/math.factorial(3))*dt**3,  (1/math.factorial(4))*dt**4]
		C[4,:]=[1,  2*dt,		     2*dt**2,  (8/math.factorial(3))*dt**3, (16/math.factorial(4))*dt**4]

		Cinv=np.linalg.inv(C)
		#print(C)
		#print(Cinv)

		CinvStar=[]
		for _ in range(0,self.ndofs):
		    CinvStar.append(np.array(Cinv))
		    
		self.CinvStar=np.array(CinvStar)

		print('OpenSees Model Initialized...')
		
	def timeInt(self):
		#ops.constraints('Transformation')
		ops.numberer(self.config.Numberer)
		ops.system(self.config.OpenSeesSystem)	
		ops.test(self.config.Test[0],self.config.Test[1],self.config.Test[2])
		ops.algorithm(self.config.Algorithm)
		ops.integrator(self.config.Integration[0],self.config.Integration[1],self.config.Integration[2])
		ops.analysis(self.config.Analysis[0])
		#ops.analysis('Transient')

	def stepForward(self,stepDT):
	
		maxNumIter = 10

		self.appliedForceX=0
		self.appliedForceY=0
		self.appliedForceZ=0
		
		StepCheck=0

		noSteps=1
		
		userLoadRoutines.applyGM(self.thisTime)
	
		ops.timeSeries('Constant', 10001+self.step)
		ops.pattern('Plain', 10000+self.step, 10001+self.step)
	
		StepCheck=self.iterate(self.CurrSteps,stepDT)
	
		ops.remove('loadPattern',10000+self.step)
		ops.remove('timeSeries', 10001+self.step)  
		
		userLoadRoutines.removeGM()
			
		ops.reactions('-dynamic')
		

		self.time.append(ops.getTime())
		
		self.step+=1

		return StepCheck
		
	def iterate(self,CurrSteps,stepDT):
		
		ForcePrediction=self.TSExpPredict(self.Flast5times)
		Currdt=stepDT/CurrSteps
                
		for node_num in range(self.NNODES):
			FX=self.force[node_num][0]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][0]
			FY=self.force[node_num][1]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][1] 
			FZ=self.force[node_num][2]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][2]	   
			MX=self.moment[node_num][0]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][3] 
			MY=self.moment[node_num][1]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][4] 
			MZ=self.moment[node_num][2]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][5]
			#print( FX, FY, FZ, MX, MY, MZ)
			ops.load(self.nodeList[node_num], FX, FY, FZ, MX, MY, MZ)
			
	
		# ops.partition()
		self.timeInt()

		StepCheck=ops.analyze(CurrSteps, Currdt, 1e-10, Currdt, 1000)
		# StepCheck=ops.analyze(CurrSteps,Currdt,1e-10,Currdt, 100)
		
		with open(self.opensees_log_location, 'a+') as f:
			print('analyzing t={} num steps={} subStepDT={} status={}'.format(self.thisTime,CurrSteps,Currdt,StepCheck),file=f)				
	
		return StepCheck
		
	def rampIterate(self,increment):

		for node_num in range(self.NNODES):
			FX=(self.force[node_num][0]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][0])*increment + self.lastForces[node_num][0]*(1-increment) 
			FY=(self.force[node_num][1]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][1])*increment + self.lastForces[node_num][1]*(1-increment)
			#FY=self.force[node_num][1]*increment + self.lastForces[node_num][1]*(1-increment) 
			FZ=(self.force[node_num][2]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][2])*increment + self.lastForces[node_num][2]*(1-increment)
			#FZ=self.force[node_num][2]*increment + self.lastForces[node_num][2]*(1-increment)
			#*increment 
			MX=(self.moment[node_num][0]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][3])*increment + self.lastMoments[node_num][0]*(1-increment) 
			#self.moment[node_num][0]*increment + self.lastMoments[node_num][0]*(1-increment)
			
			MY=(self.moment[node_num][1]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][4])*increment + self.lastMoments[node_num][1]*(1-increment) 
			#MY=self.moment[node_num][1]*increment + self.lastMoments[node_num][1]*(1-increment)  

			MZ=(self.moment[node_num][2]*(1-self.ForcePredictionAlpha) + self.ForcePredictionAlpha*ForcePrediction[node_num][5])*increment + self.lastMoments[node_num][2]*(1-increment) 
			#MZ=self.moment[node_num][2]*increment + self.lastMoments[node_num][2]*(1-increment) 	   
			ops.load(self.nodeList[node_num], FX, FY, FZ, MX, MY, MZ)

		StepCheck=ops.analyze(1, self.dt/self.CurrSteps, 1e-10, self.dt/self.CurrSteps, 100)
		return StepCheck
		

	def RotateTreeBranch(self, vectorOrTallArray, alpha, beta, gamma):
		vec=vectorOrTallArray	
		ca=np.cos(alpha)
		cb=np.cos(beta)
		cg=np.cos(gamma)
		sa=np.sin(alpha)
		sb=np.sin(beta)
		sg=np.sin(gamma)
		
		rotMat=np.zeros((3,3))
		rotMat[0,:]=[cb*cg, sa*sb*cg-ca*sg, ca*sb*cg+sa*sg]
		rotMat[1,:]=[cb*sg, sa*sb*sg+ca*cg, ca*sb*sg-sa*cg]
		rotMat[2,:]=[-sb, sa*cb, ca*cb]
		vec2=np.dot(rotMat,np.transpose(vec))
		return np.transpose(vec2)

	def writeLogs(self):
		with open('./fys_logs/tlog', 'a+') as f:
			print("{} {} {} {}".format(ops.getTime(),self.stepNumber,self.totalSteps,self.iteration),file=f)
		with open(self.fys_couplingdriver_log_location, 'a+') as f:
			print(' Time: ',ops.getTime(),'Work Transfer -- error (%)',100*(self.WorkIn-self.WorkOut)/self.WorkIn,' W(f->s)/W(s->f) (Ratio)',self.WorkIn/self.WorkOut,', W(f->s) (Joules): ',self.WorkIn,', W(s->f) (Joules): ',self.WorkOut,file=f)
		with open(self.work_log_location, 'a+') as f:
			print(' Time: ',ops.getTime(),'Work Transfer -- error (%)',100*(self.WorkIn-self.WorkOut)/self.WorkIn,' W(f->s)/W(s->f) (Ratio)',self.WorkIn/self.WorkOut,', W(f->s) (Joules): ',self.WorkIn,', W(s->f) (Joules): ',self.WorkOut,file=f)
		with open(self.work_array_location, 'a+') as f:
			print(self.stepNumber,self.iteration, ops.getTime(),100*(self.WorkIn-self.WorkOut)/self.WorkIn,self.WorkIn/self.WorkOut,self.WorkIn,self.WorkOut,file=f)
		

		
	

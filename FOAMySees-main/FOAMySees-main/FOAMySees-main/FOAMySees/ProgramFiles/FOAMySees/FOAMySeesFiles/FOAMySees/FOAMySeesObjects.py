import os
import concurrent.futures
import logging
import queue
import random
import subprocess
from subprocess import Popen, DEVNULL, STDOUT
import time

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

import configureCoupledCase as config

import buildOpenSeesModelInThisFile as userModel

import userLoadRoutines as userLoadRoutines

import math as m

import copy


import math


import meshio

import openseespy.opensees as ops
# from openseespy.postprocessing.Get_Rendering import * 
from openseespy.opensees import *

		
		
import preliminaryAnalysis as prelimAnalysis
import createRecorders as createRecorders
import time

class FOAMySeesInstance():
	def __init__(self, dt, config, parent=None):
	
		# Define properties
		self.dt = dt
		self.time=[0]
		self.step=0
		self.whatTimeIsIt=0
		self.config=config
		
		self.createRecorders=createRecorders
		
		self.prelimAnalysis=prelimAnalysis
		
		self.OmegaDamp=1
		Popen('rm -rf SeesCheckpoints', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('mkdir SeesCheckpoints', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()

		Popen('rm -rf SeesOutput', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('mkdir SeesOutput', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		Popen('touch SeesOutput.pvd', shell=True, stdout=DEVNULL,stderr=STDOUT).wait()
		self.userModel=userModel.defineYourModelWithinThisFunctionUsingOpenSeesPySyntax(self)
		self.makeDataArrays()
			
	def calculateUpdatedMoments(self,Forces):
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
			
	def projectDisplacements(self,Displacement):
		
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
		return Displacement
	
	def readCheckpoint(self,stepOut):
		ops.database('File',"SeesCheckpoints/checkpoints/"+str(stepOut))
		#ops.wipeAnalysis()
		ops.restore(stepOut)
		
		with open('What is Happening With OpenSees.log', 'a+') as f:
			print('read a checkpoint from opensees time = ',self.thisTime,file=f)
		ops.setTime(self.thisTime)	
		
	def writeCheckpoint(self,stepOut):
		ops.database('File',"SeesCheckpoints/checkpoints/"+str(stepOut))
		ops.save(stepOut)
		newStep=0
		self.thisTime=copy.deepcopy(ops.getTime())
		with open('What is Happening With OpenSees.log', 'a+') as f:

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
		
		self.phithetapsi=np.zeros([len(self.coupledNodes),3])

		self.force=np.zeros([len(self.coupledNodes),3])
		self.displacement=np.zeros([len(self.coupledNodes),6])

		self.velocity=np.zeros([len(self.coupledNodes),6])
		self.acceleration=np.zeros([len(self.coupledNodes),6])
		self.forceandmoment=np.zeros([len(self.coupledNodes),6])

		print('OpenSees Model Initialized...')
		
	def timeInt(self):
		ops.constraints('Transformation')
		ops.numberer(self.config.Numberer)
		ops.system(self.config.OpenSeesSystem)	
		ops.test(self.config.Test[0],self.config.Test[1],self.config.Test[2])
		ops.algorithm(self.config.Algorithm)
		ops.integrator('Newmark', 0.5, 0.25)
		ops.analysis('VariableTransient')
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
		for node_num in range(self.NNODES):
			FX=self.force[node_num][0] 
			FY=self.force[node_num][1] 
			FZ=self.force[node_num][2]	   
			MX=self.moment[node_num][0] 
			MY=self.moment[node_num][1] 
			MZ=self.moment[node_num][2]	   
			ops.load(self.nodeList[node_num], FX, FY, FZ, MX, MY, MZ)
				
		Currdt=stepDT/CurrSteps
		# ops.partition()
		#self.timeInt()

		StepCheck=ops.analyze(CurrSteps, Currdt, 1e-10, Currdt, 100)
		# StepCheck=ops.analyze(CurrSteps,Currdt,1e-10,Currdt, 100)
		

		return StepCheck
		
	def rampIterate(self,increment):

		for node_num in range(self.NNODES):
			FX=self.force[node_num][0]*increment + self.lastForces[node_num][0]*(1-increment) 
			FY=self.force[node_num][1]*increment + self.lastForces[node_num][1]*(1-increment) 
			FZ=self.force[node_num][2]*increment + self.lastForces[node_num][2]*(1-increment)	
			MX=self.moment[node_num][0]*increment + self.lastMoments[node_num][0]*(1-increment) 
			MY=self.moment[node_num][1]*increment + self.lastMoments[node_num][1]*(1-increment)  
			MZ=self.moment[node_num][2]*increment + self.lastMoments[node_num][2]*(1-increment) 	   
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
		
	

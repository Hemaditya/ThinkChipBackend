'''
This app.py is responsible for setting up the BCI with pyOpenBCI package.
This app.py will have all the configurations of how the data will be read from OpenBCI
'''
from pyOpenBCI import OpenBCICyton as BCI
import numpy as np
import os
import pickle
import time

class OpenBCI(object):

	def __init__(self,port=None,daisy=None,chunk_size=250,method=1,path=None,createSession=True):
		'''
			Initialize all the variables
		'''
		self.port = port
		self.daisy = daisy
		self.chunk_size = chunk_size
		self.method = method # Read data continously or in chunks of chunk_size
		print("Starting creating streamer....")
		self.streamer = BCI(self.port,self.daisy)
		self.uVolts_per_count = (4.5)/24/(2**23-1)*1000000 # scalar factor to convert raw data into real world signal data
		
		#Saving data and naming conventions
		self.homeFolder = os.getcwd()
		self.sessionFolder = self.homeFolder+"/SessionData"
		self.sessionId = time.strftime("SESSION_%Y%m%d_%H%M%S")
		if(path == None):
			self.currentSession = self.sessionFolder+"/"+self.sessionId
		else:
			self.currentSession = self.sessionFolder+"/"+path
		print("Building Session Folders....")
		if(createSession == True):
			self.makeSessionFolder()

	def makeSessionFolder(self):
		if(os.path.isdir(self.sessionFolder) == False):
			os.mkdir(self.sessionFolder)
		if(os.path.isdir(self.currentSession) == False):
			os.mkdir(self.currentSession)
	
	def read_chunk(self,n_chunks=1,verbose=False,data_only=True,exit_after=False,save_data=False):
		'''
			- Each chunk is defined by "chunk_size".
			- "n_chunks" defines how many chunks of data you want.
			- "data_only" is to say whether you want only the numeric
			  signal data or you want the entire sample points.
			- "exit_after" is for if you want to close the stream after 
			  reading the data.
			- "save_data" if you want to save the raw data some where

			Create a numpy array if the user is requesting for data only
			Use lists if you entire object of the sample.

			The output of this function is an array of shape:
				(n_chunks,chunk_size,n_channels)
		'''
		if(data_only == True):
			t = 0
			data = np.zeros(shape=(1,self.chunk_size,8))
			for i in range(n_chunks):
                                if verbose:
                                    print("Reading Chunk: %d "%(i+1))
				sample = self.streamer.start_stream_ext(method=self.method,chunk_size=self.chunk_size,data_only=data_only)
				sample = np.expand_dims(np.asarray(sample),0)
				data = np.append(data,sample,0)
			data = data[1:]
			data = data*self.uVolts_per_count
			if(exit_after == True):
				self.streamer.stop_stream()
			if(save_data == True):
				t = time.strftime("%Y%m%d_%H%M%S")
				np.save(self.currentSession+"/RawData_"+t,data)	
			
			#return (data.transpose(0,2,1),self.currentSession,t)
			return data.transpose(0,2,1)
		else:
			data = []
			for i in range(n_chunks):
				print("Reading Chunk: %d "%(i+1))
				sample = self.streamer.start_stream_ext(method=self.method,chunk_size=self.chunk_size,data_only=data_only)
				data.append(sample)
			if(exit_after == True):
				self.streamer.stop_stream()
			if(save_data == True):
				t = time.strftime("%Y%m%d_%H%M%D")
				with open(self.currentSession+"/RawData_"+t+".pickle",'w') as f:
					pickle.dump(data,f)
			return data

		

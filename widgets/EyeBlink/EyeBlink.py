import config
import filters
import threading
import numpy as np
import pickle
import time
import config
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

class EyeBlink():
	''' Module to detect/read data for Eye Blinks '''

	def __init__(self,widget_path,name="Blinks",trails=120):
		''' Initialize stuff '''
		self.path = widget_path
		self.name = name
		if type(widget_path) == str:
			self.path = Path(self.path)
		self.trails = trails
		self.name = name
		self.t = time.strftime("%d%m%y_%H%M%S")
		self.data_buffer = np.zeros(shape=(1,config.CHANNELS,config.CHUNK_SIZE))

	def run_browser(self):
		self.driver = webdriver.Firefox(executable_path='./geckodriver')
		path = os.getcwd()+'/index.html'
		self.driver.get('file://'+path)

	def save_data(self,data,f=0,verbose=False):
		''' This function is called whenever you want to save the data '''
		"""
			Inputs:
				data: np.ndarray
				- the data that you wanna save.
				f: int
				- 1 if you want to filter the data
				- 0 if you want to save raw data
		"""
		flag = '[r]'
		if(f == 1):
			flag = '[f]'
			if verbose:
				print(f"CONSOLE: Filtering the data")
			data = filters.apply_dc_offset(data)
			data = filters.apply_notch_filter(data)

		self.data_buffer = np.vstack((self.data_buffer,data))
		file_name = flag+self.name+self.t+".pickle"
		file_path = self.path/file_name
		if verbose:
			print(f"CONSOLE: Saving data{self.data_buffer[1:].shape}")
		with open(file_path,'wb+') as f:
			pickle.dump(self.data_buffer[1:],f)

	def detect_energy(self,data,channels=[0]):
		data = filters.apply_dc_offset(data)
		data = filters.apply_notch_filter(data)
		data = filters.apply_bandpass_filter(data,1,10)
		data = data[:,channels,:].reshape(-1)
		
		print(data.sum())
	
	def detect_blinks(self,data, channels=[0]):
		''' Detect eye blinks here '''
		data = filters.apply_dc_offset(data)
		data = filters.apply_notch_filter(data)
		data = filters.apply_bandpass_filter(data,1,10)
		data = data[:,channels,:].reshape(-1)

		if(data.max() <= 200.0 and data.max() >= 100.0):
			print("Blink Detected")
			self.driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
		else:
			print("No Blink Detected")
		

	def run_real_time(self,channels=0):
		while True:
			data = config.data_reader.read_chunk(n_chunks=1)
			self.detect_blinks(data,channels)

	
	def collect(self,verbose=False):
		self.t = time.strftime("%d%m%y_%H%M%S")
		config.reset_filter_states()
		for i in range(int(self.trails/4)):
			print("Blink: ",i)
			data = config.data_reader.read_chunk(n_chunks=4)
			t = threading.Thread(target=self.save_data,args=(data,1,verbose))
			t.start()

		print("Data Collection finished")

			


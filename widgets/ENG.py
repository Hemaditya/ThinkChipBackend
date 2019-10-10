"""
	This module is for ENG widget, command line version
"""
import filters
import time
import config
import pickle
import numpy as np
import threading
import features as ft


class ENG():
	''' The base class for ENG module '''

	def __init__(self,widget_path,trails=120):
		''' Each of the widgets will be initialized with a path to their widget '''

		self.path = widget_path
		self.data_buffer = np.zeros(shape=(1,config.CHANNELS,config.CHUNK_SIZE))
		self.t = time.strftime("%d%m%y_%H%M%S")
		# This is the defult and can be reset
		self.trails = trails
		self.games = np.load(config.ROOT_DIR/'widgets/games.npy')

		self.attention_matrix = []

	def save_data(self,data,game,f=0,verbose=False):
		''' This function is called whenever you want to save the data '''
		"""
			Inputs:
				data: np.ndarray
				- the data that you wanna save.
				game: string
				- Name of the game
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
		file_name = flag+game+"|"+self.t+".pickle"
		file_path = self.path/file_name
		if verbose:
			print(f"CONSOLE: Saving data")
		with open(file_path,'wb+') as f:
			pickle.dump(self.data_buffer[1:],f)

	def attention_per_channel(self, bandpower):
		"""bandpower - numpy array of length 5"""
		# Do something to return attention given bandpower for
		# a single channel for a single epoch

		# temporary fix change this appropriately
		return bandpower[3]/np.mean(bandpower)

	def attention_overall(self, attention_per_channel):
		"""attention_per_channel - np.array(num_of_channels)"""
		# Do something to generate
		# self.attention
		return np.mean(attention_per_channel)

	def test_start_session(self, game_name, channels=[0], read_length=10):
		"""This function starts the widget and calls the functions to get data from cyton board
		using self.data_reader. Length of data section (temp_data) that is read at a single time
		is determined by read_length. This data section (temp_data) is passed to get_attention
		(in a different thread) which calculates the attention matrix for this data.
		channels: list of channels to use"""
		while True:
			temp_data = config.data_reader.read_chunk(read_length)

			# Thread because the below has too many loops
			# We don't have to drop data, as data will get dropped if
			# data_reader.read_chunk cannot be called for too long.
			t = threading.Thread(target=self.get_attention, args=(temp_data, channels,))
			t.start()

	def get_attention(self, temp_data, channel_mask=[0], threshold=100):
		"""This function gets the attention matrix from a section of data.
		length of this data section is determined by read_length.
		temp_data: np.array(epochs, channels, chunk_size)"""
		# Remove bad blocks
		temp_data = filters.apply_dc_offset(temp_data)
		temp_data = filters.apply_notch_filter(temp_data)
		blocks_data = ft.remove_bad_epochs(temp_data, threshold=threshold,
										   channels=channel_mask, sliding_window=True)

		blocks_bandpower = []
		for block in blocks_data:
			blocks_bandpower.append(ft.get_bandpower(block.reshape(1, block.shape[0], block.shape[1]),
													 channel_mask))

		attention_per_channel = np.zeros((len(blocks_bandpower), len(channel_mask)))
		for idx, block in enumerate(blocks_bandpower):
			for channel in channel_mask:
				attention_per_channel[idx, channel] = self.attention_per_channel(block[channel])
			attention_per_epoch = self.attention_overall(attention_per_channel[idx])
			self.attention_matrix.append(attention_per_epoch)

			# For testing. Remove later
			print(attention_per_epoch)

	def run(self):
		''' This function will be called whenever you want to start the widget '''

		# First reset the states variables
		config.reset_filter_states()

		x = 0
		while x != 'q':
			for i,g in enumerate(self.games):
				print(i+1,".",g)
			print("Press q to go back ")
			x = input("Enter the game you wanna play: ")
			if x == 'q':
				return
			if x != 'q':
				x = int(x) - 1
				if(x < 0 or x >= self.games.shape[0]):
					print(f"CONSOLE: Enter proper varible")
					continue
				self.t = time.strftime("%d%m%y_%H%M%S")
				for i in range(int(self.trails/5)):
					print(f"CONSOLE: {int(self.trails/5)-i} trails left")
					data = config.data_reader.read_chunk(5)
					t = threading.Thread(target=self.save_data, args=(data,self.games[x],1))
					t.start()

# ThinkChipBackend

This will be the backend Engine for all the widgets we will be building. 
We will seperate different modules and keep them seperately.

## [MODULE] - test
This module has jupyter notebooks which are used to test different modules.

## [MODULE] - filters
This is the module which will hold all the filters that are applied to the raw signal as a processing step.

## [MODULE] - core
This is the module which will hold the code which is responsible to read the data from the device and stream it to 
either a port or a socket.

## [MOUDLE] - features
This is the module responsible for detecting and/or certain features in the filtered signal, based on some threshold.

## [MODULE] - data
This is the module responsible for handling data.

## [MODULE] - session
This is the module which is responsible for creating different sessions for different users.

## [MODULE] - widgets
This is the module which holds all the Widgets that we will experiment on.

# TODO 
- [x] Split incoming data into overlapping blocks.
		- Created an Iterator for this.
- [] Functions - to get energy from a chunk, to do thresholding
- [] Run the incoming blinks with these functions and output Blink or No Blink
- [] Store incoming chunks as an array and delete eye blink chunks from the array.
- [] Pass the resultant chunks array 

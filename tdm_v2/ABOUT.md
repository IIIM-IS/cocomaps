Second iteration of the task dialogue manager for the CoCoMaps project,
based on previous iterations and accumulated experience of working the
second iteration can be optimized and connectors created for relevant 
items.

File structure of system 
	├── ABOUT.md
	├── Actions
	│   └── __init__.py
	├── __init__.py
	├── MEx
	│   └── __init__.py
	├── TaskBuilder
	│   ├── __init__.py
	│   └── tasks
	└── YTTM_connector
	    └── __init__.py

	5 directories, 6 files

Objective of each module: 
	Actions : A library of executable actions the robot can 
		call. It can be the response string for a specific
		question or a function calling something specific. 
		The action library is the main "control" feature of 
		the TDM. Other modules focus on selectin control
		directions, creating file structure, connecting to
		outside objects
	MEx : Meaning Extractor, takes in a string and current object
		location, w.r.t. task, and tries to spit out a probability
		of what is the return value and/or the next action to
		take
	TaskBuilder : Builds the tasks from json structures stored in folder
		tasks. 
	YTTM_connector : Takes care of the connections to and from the 
		Ymir turn taking module. 


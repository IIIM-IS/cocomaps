The task files are json structured file that can be used to represent taks, 
questions or other objectives that the robot needs to evaluate and/or 
perform. 
The task fields are as follows:
	_name = Name of the task
	_description = "Long string explaining what the objective of the
			task is and what its output should be"
	
 	{keywords, value} = string keywords, float 0<x<=1 representing words 
				that are hevily influenced by this keyword
	question_template = {Dict} of objects that need to be fulfilled 
				before continuing. 
	misc 		= Special definitions, e.g. who = 1;
	fail_action	= define what to do if task is failed or is aborted
	pass_action	= define what to do if task is failed or is aborted

# Info fields, fields in struct that are dynamic and are used more for 
	_max_time	= time allowed until task is aborted





# Fields established during runtime, can be output in file to debug
 	_parent 	= What task called, availible for all tasks except
 				greet task. Greet task is parent
 	_start_time 	= Starting time
 	_elapsed 	= elapsed time since task started

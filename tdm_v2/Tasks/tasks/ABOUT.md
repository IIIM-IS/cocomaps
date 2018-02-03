The task files are json structured file that can be used to represent taks, 
questions or other objectives that the robot needs to evaluate and/or 
perform. The task fields are documented in the tables below.

# Instruction fields
  Task field | Meaning
  ----------:|:-------
  name       | Name of the task.
  description| Long string explaining what the objective of the task is and what its output should be.
  keywords   | Keywords that give the possible template output. MEx gives these keywords probabalistic values based on input strings.
  question_template | Vector of possible output strings, will be randomized to get more entertainment from robot.
  misc        | Special definitions. Example: who = 1.
  fail_action | Define what to do if task is failed or is aborted.
  pass_action | Define what to do if task is failed or is aborted.

# Info fields, fields in struct that are dynamic and are used more for
  Task field | Meaning
  ----------:|:-------
  max_time      | Time allowed until task is aborted.

# Fields established during runtime, can be output in file to debug
  Task field | Meaning
  ----------:|:-------
  parent | What task called, availible for all tasks except greet task. Greet task is parent.
  start_time | Starting time.
  elapsed | Elapsed time since task started.

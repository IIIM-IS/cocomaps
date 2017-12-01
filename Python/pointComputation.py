#!/usr/bin/env python
# pointComputation.py
"""
The cocomaps project uses point definition in the xml files, <vantagepoint>. These points define 
the lookout points of the robots, however the method of implimentation has so far been trial and
error, in this file the objective is to examine how the points are used and create a compuational
algorithm to select other points, as well as overlap.

Author
        David Orn
        david@iiim.is
(c)
        IIIM
Date Created
        29.11.17
"""
import matplotlib.pyplot as plt
import pickle
import sys
import numpy as np


#TODO move to class orientation, map self.points-> skip phi, try to notice a mehtod (mark self.points)
# Add raw data to class to compare if self.points are numbered correctly

class Point_Examination():
    def __init__(self, file_name):
        """
        Loads the data from a pkl dictionary, returns a more suitable format for
        further processing
        """
        self.y = []
        self.x = []
        self.oz = []
        self.ow = []
        self.figure = None
        self.ax = None

        self.datavals = ['x', 'y', 'oz', 'ow']
        self.raw_data =  pickle.load(open(file_name, 'rb'))
        self.n = len(self.raw_data) # Number of self.points in file
        self.points = np.zeros((self.n, 4))
        self.overlaps = np.zeros((self.n,self.n))
        
        for idx, struct in enumerate(self.raw_data.iteritems()):
            # Split data structure from keys
            sstruct = struct[1]
            # Split self.points and overlap from datastructure
            self.points[idx, :] = np.array(sstruct[0].split(',')).astype(np.float)
            self.overlaps[idx, :] = np.array(sstruct[1].split(',')).astype(np.float)

        self.make_points()
        self.make_image()


    def __str__(self):
        print "Points"
        print self.points
        print "Overlap"
        print self.overlaps

        return ""

    def make_points(self):
        """
        Make x,y point arrays from data, print values specifically
        """
        self.x = self.points[:,0]
        self.y = self.points[:,1]
        self.oz = self.points[:,2]
        self.ow = self.points[:,3]

    def make_image(self):
        """
        Star a simple figure and plot each point
        """
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

        for i in range(self.n):
            self.ax.plot(self.x[i], self.y[i], 'bo')
            self.ax.annotate(str(i+1), xy=(self.x[i], self.y[i]))



        plt.show()





if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        EX = Point_Examination(file_name)


    else:
        print "Missing input file"
        

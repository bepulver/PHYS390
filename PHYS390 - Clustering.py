#----------------------------------------------HOUSEKEEPING-----------------------------------------------------------------------#

import dwave
import dimod
import numpy
import json
import math
import minorminer
import dwavebinarycsp
import dwave.inspector
from dwave.system.samplers import DWaveSampler
from dwavebinarycsp.core import csp
sampler = DWaveSampler(token='DEV-176c67d38a18f8e993b4bd11b99aae4d68ab85a3', solver='DW_2000Q_6')

#---------------------------------------------JSON READER-------------------------------------------------------------------------#

trackList = [] #This is just a big list of the unclustered data this will be the input to the function to actually cluster them
errorList = [] #List of all error in the same order as the previous list.
numOfClusters = int #This will be an input for now. This is how many clusters the program will organize points into
numOftracks = int #This is also an input. I'm not sure what I will actually do with this, but it exists now


#---------------------------------------------METHODS (QUBO?)-----------------------------------------------------------------------------#

Q = {}

def errorAdjust(input, error): #takes the lists for tracks and error and takes tracks[index] and divides it by errors[index] and returns that to a new list[index]
    adjustedTracks = []
    for i in range(len(input)-1): #The minus 1 is because python starts its indexing at 0. No clue why we need range you just do.
        adjustedTracks[i] = input/error 
    return adjustedTracks



def clusterPoints(points):
    i = j = 0
    while i < len(points) & j < len(points):
        if i == j:
            i += 1
        else if i != len(points) & j != len(points):
            while j < len(points):    
                #Q.addinteraction(clusterThese[i], clusterThese[j], "weight") #Placeholder for now
                Q[(i, j)] = abs(points[i] - points[j])
                j +=1
            j = 0
        else:
            break






#clusterCode = {} #This should be a dict with keys that look like (0, 1, 0, 0) gotta be honest, I have no clue why they made this a dict
#class Coordinate:
#    def __init__(self, x, y):
#        self.x = x
#        self.y = y

#        for i in len(numOfClusters): #Creating the amount of clusters to reference as to variable numOfClusters
#            self.i = "Cluster " + str(i) #Probably breaking python rules
#            clusterCode = {} #I want to take the number of clusters and fill this with the cluster codes that look like this: (0, 1, 0, 0)

#def clusterThem(tracks, )

#---------------------------------------------SOLVING SECTION-----------------------------------------------------------------------#

clusterThese = errorAdjust(trackList, errorList) #This is a list of error adjusted values

#csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
#bqm = dwavebinarycsp.stitch(csp)
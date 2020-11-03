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

trackList = [0.3578421714920063, 0.35763199025343234, 0.4378207965666029, 0.4375708301205863] #This is just a big list of the unclustered data this will be the input to the function to actually cluster them
#                     0                     1                  2                   3
errorList = [0.010000000000000002, 0.010000000000000002, 0.017499999999999998, 0.0125] #List of all error in the same order as the previous list.
numOfClusters = int #This will be an input for now. This is how many clusters the program will organize points into
numOftracks = int #This is also an input. I'm not sure what I will actually do with this, but it exists now


#---------------------------------------------METHODS (QUBO?)-----------------------------------------------------------------------------#

Q = {}

def errorAdjust(input, error): #takes the lists for tracks and error and takes tracks[index] and divides it by errors[index] and returns that to a new list[index]
    adjustedTracks = []
    i = 0
    while i <= (len(input)-1): #The minus 1 is because python starts its indexing at 0. 
        adjustedTracks.append(input[i]/error[i]) #This is how we account for error. we take our location and divide it by the error.
        i += 1
    return adjustedTracks



def clusterPoints(points):
    j = 0
    while j < len(points):
        i = j + 1 #This is so we dont get a distance of 0 because if i=j then we get i-i which = 0
        while i < len(points):    
            Q[(j, i)] = points[i] - points[j] #we might want an abs so we dont get a negative
            i += 1
        j += 1

#---------------------------------------------SOLVING SECTION-----------------------------------------------------------------------#

clusterThese = errorAdjust(trackList, errorList) #This is a list of error adjusted values
print(clusterThese)
clusterPoints(clusterThese)
print(str(Q))


#{(0, 1): -0.02101812385739521, (0, 2): -10.765885916823311, (0, 3): -0.7785507395537223, (1, 2): -10.744867792965916, (1, 3): -0.7575326156963271, (2, 3): 9.987335177269589}
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
sampler = DWaveSampler(token='TOKEN', solver='QPU')

#---------------------------------------------JSON READER-------------------------------------------------------------------------#

inputFile = [[0.3576734259547776, [[0.3578421714920063, 0.0003333333333333334], [0.35763199025343234, 0.0003333333333333334]]], [0.43751589332926805, [[0.4378207965666029, 0.0005833333333333333], [0.4375708301205863, 0.0004166666666666667]]]]


trackList = [] #This is just a big list of the unclustered data this will be the input to the function to actually cluster them
errorList = [] #List of all error in the same order as the previous list.
location = []

for set in inputFile:
    location.append(set[0])
    for track in set[1]:
        trackList.append(track[0])
        errorList.append(track[1])
numOfClusters = len(location) #This is the variable for how many clusters will be calculated. This can either be an input or decided from
#print(numOfClusters)
#print(location)
#print(trackList)
#print(errorList)

#---------------------------------------------METHODS-----------------------------------------------------------------------------#

Q = {}

def calcDist(input1, input2):
    distance = abs(trackList[input1] - trackList[input2])
    totalError = math.sqrt((errorList[input1])**2 + (errorList[input2])**2)
    return distance / totalError

def makeQUBO(points, howManyClusters, strengthOfConstraint):
    numberOfQubits = 0 #Just a counter so we can assign all the keys of the dict Q to the corresponding qubit number
 #This set of loops represents the first term of sigmas in the Hamiltonian
    j = 0
    while j < len(points):
        i = j + 1 #This is so we dont get a distance of 0 because if i=j then we get i-i which = 0
        while i < len(points):    
            k = 0
            while k < howManyClusters:
                x = (k*(len(points))+i)
                y = (k*(len(points))+j)
                Q[(y,x)] = calcDist(i, j)
                k += 1
            i += 1
        j += 1
 #Adjusts all the tracks by a max distance and adds a cosine. This is so that a coupling can be distinguised from noise in the annealer
    maxDist = max(Q.values())
    for i in Q.keys():
        Q[i] = -math.cos((Q[i] * math.pi) / maxDist)
 #This set of loops represents the second term of sigmas in the Hamiltonian
    j = 0
    while j < len(points):
        i = j + 1 #This is so we dont get a distance of 0 because if i=j then we get i-i which = 0
        while i < len(points): 
            x_0 = (0*(len(points))+i) #This is x and y for when k,m = 0
            y_0 = (0*(len(points))+j)
            x_1 = (1*(len(points))+i) #This is x and y for when k,m = 1
            y_1 = (1*(len(points))+j)
         #Example cpupling that this if-statement adds: i=0, j=1, k=0, m=1
             #This checks if there is already an interaction in the QUBO. If so it adds to it instead of overriding it.
            Q[(y_0,x_1)] = math.tanh(1/calcDist(i, j))
         #Example cpupling that this if-statement adds: i=0, j=1, k=1, m=0
            Q[(y_1,x_0)] = math.tanh(1/calcDist(i, j))
            i += 1
        j += 1
    
 #This is adding the biases to make sure each point only picks one cluster. It is the thrid group of sigmas in the Hamiltonian
    i = 0
    while i < len(points):
        k = 0
        while k < howManyClusters:
            x = (k*(len(points))+i)
            Q[(x,x)] = -(strengthOfConstraint)
            k += 1
        m = 0
        l = m + 1
        x = (m*(len(points))+i)
        y = (l*(len(points))+i)
        while m < howManyClusters:
            while l < howManyClusters:
                Q[(x,y)] = 2*(strengthOfConstraint) 
                l += 1
            m += 1
        i += 1

def cluster(reads):
    embedding = minorminer.find_embedding(Q.keys(),sampler.edgelist)
    target_Q = dwave.embedding.embed_qubo(Q, embedding, sampler.adjacency, chain_strength=1.0)
    embedded_response = sampler.sample_qubo(target_Q, num_reads=reads, answer_mode="raw")
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    response = dwave.embedding.unembed_sampleset(embedded_response, embedding, bqm)
    return response.record.sample

def tabulate(data, printBool):
    tabulatedData = {str: int}
    for i in data:
        if str(i) in tabulatedData.keys():
            tabulatedData[str(i)] += 1
        else:
            tabulatedData[str(i)] = 1
        #print(i)
    print(tabulatedData)
    if printBool:
        print(str(data))

#---------------------------------------------FINAL SOLVE-----------------------------------------------------------------------#

makeQUBO(trackList, numOfClusters, 1) #This generates a Hamiltonian with the error adjusted points, the amount of cluster specified at the beginning, and with a stregth of constraint of 1
tabulate(cluster(10), False) #This tabulates the results from the QPU with 10 reads. It does not print the raw output from the QPU
#print(str(Q)) #prints the qubo

#'[0 0 1 1 1 1 0 0]': 9, '[1 1 0 0 0 0 1 1]': 1

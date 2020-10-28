#----------------------------------------------HOUSEKEEPING-----------------------------------------------------------------------#

import dwave
import dimod
import numpy
import minorminer
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler(token="PLACEHOLDER", solver='DW_2000Q_6')

#-----------------------------------------------QUBO------------------------------------------------------------------------------#

Q = {}
Q[(0,1)] = 1
Q[(1,2)] = -2
Q[(0,2)] = -2
Q[(2,2)] = 3
Q

#-----------------------------------------------COMPUTING-------------------------------------------------------------------------#

embedding = minorminer.find_embedding(Q.keys(),sampler.edgelist)
target_Q = dwave.embedding.embed_qubo(Q, embedding, sampler.adjacency, chain_strength=1.0)
embedded_response = sampler.sample_qubo(target_Q, num_reads=10, answer_mode="raw")
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
response = dwave.embedding.unembed_sampleset(embedded_response, embedding, bqm)
#print(type(response)) #dimod.sampleset.Sampleset
#print(response)

#-----------------------------------------------DIVIDING RESPONSE-----------------------------------------------------------------#

energyArray = response.record.energy
inputArray = response.record.sample
#print(energyArray)
#print(type(energyArray)) #numpy.ndarray
#print(inputArray)
#print(type(inputArray)) #numpy.ndarry

#-----------------------------------------------TABULATION------------------------------------------------------------------------#

correct = 0
incorrect = 0
tabulatedData = {str: int}
for i in inputArray:
    if str(i) in tabulatedData.keys():
        tabulatedData[str(i)] += 1
        #print("I was in the keys already")
    else:
        tabulatedData[str(i)] = 1
        #print("I got added to the keys just now")
    print(i)
print(tabulatedData)

#[1 0 0]': 1, '[0 1 0]': 5, '[0 0 0]': 2, '[1 1 1]': 2

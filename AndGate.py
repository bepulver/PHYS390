#----------------------------------------------HOUSEKEEPING-----------------------------------------------------------------------#

import dwave
import dimod
import numpy
import minorminer
from dwave.system.samplers import DWaveSampler
sampler = DWaveSampler(token="TOKEN", solver="QPU")

#-----------------------------------------------QUBO------------------------------------------------------------------------------#

Q = {}
Q[(0,1)] = 1
Q[(1,2)] = -2
Q[(0,2)] = -2
Q[(2,2)] = 3

#-----------------------------------------------COMPUTING-------------------------------------------------------------------------#

embedding = minorminer.find_embedding(Q.keys(),sampler.edgelist)
target_Q = dwave.embedding.embed_qubo(Q, embedding, sampler.adjacency, chain_strength=1.0)
embedded_response = sampler.sample_qubo(target_Q, num_reads=10, answer_mode="raw")
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
response = dwave.embedding.unembed_sampleset(embedded_response, embedding, bqm)

#-----------------------------------------------DIVIDING RESPONSE-----------------------------------------------------------------#

inputArray = response.record.sample

#-----------------------------------------------TABULATION------------------------------------------------------------------------#

correct = 0
incorrect = 0
tabulatedData = {str: int}
for i in inputArray:
    if str(i) in tabulatedData.keys():
        tabulatedData[str(i)] += 1
    else:
        tabulatedData[str(i)] = 1
    print(i)
print(tabulatedData)

#Outputs for 10 samples and 1000 samples respectively
#'[1 0 0]': 1, '[0 1 0]': 5, '[0 0 0]': 2, '[1 1 1]': 2
#'[0 1 0]': 319, '[0 0 0]': 329, '[1 0 0]': 224, '[1 1 1]': 128

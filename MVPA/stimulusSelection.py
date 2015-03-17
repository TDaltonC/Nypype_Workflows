# -*- coding: utf-8 -*-
"""
GA based stimulus selector
 
Created on Sat Feb 21 13:10:50 2015
@author: Calvin Leather

To do-
Crossover algorithm is somehow producing a few repeats -done, fixed
Consider single-item/hetero 'buddy' term in fitness function
Stick with 2pop ks test or use JS divergence? Or its square? - done, yes stick with it

"""

#%%==========imports and constants=================%%#
import numpy as np
import pandas as pd
from deap import base, creator, tools
import matplotlib.pyplot as plt
from scipy.stats import kstest, ks_2samp
from scoop import futures
import random, operator, seaborn

print 'defining variables'

# Define the location of the csv file with modeled preferences, should make relative
# Three col CSV (Item-Code, Option-Type, Value)
csv_filepath='/Users/Dalton/Documents/Projects/BundledOptionsExp/BehavioralValueMeasurements/records/options.csv'


#%% Magic Numbers
#nepochs-number of epochs, ngen-number of generations in an epoch
#cxpb- probability of a cross over occuring in one chromosome of a mating pair
#mutpb- probability of at each nucleotide of a mutation
#number of individuals to put in HOF in each epoc
nepochs, ngen, npop, cxpb, mutpb = 4,60,250, 0.4, 0.1
HOFsize=1 

HallOfFame=[]

SID='a03'
n_single=20 #1 number of possibilities for singleton
n_hetero=15 #2 number of possibilities for the heterogenous bundle
n_homo=22 #3 number of possibilities for the homogeneous scaling
n_genome=n_single+n_hetero+n_homo #total number of possibilities for all cases
n_target=10 #Desired number in each chromosome

chromosomeDict={0:n_single, 1:n_hetero, 2:n_homo}

#Define the seed for the random number generator for replication purposes
random.seed()

#%%===========define fitness and functions=================%%#
print 'defining functions'


def evalMax(individual):
 """ A weighted total of fitness scores to be maximized
 RangeCost-maximum to minimum
 SimilarityCost - number of items in both singleton and homogenous scaling
 UniformCost- Uses KS divergence to indicate distance of distribution of values from uniform distribution
 DistanceCost- Uses KS divergence to indicate differences between distributions
 Cost currently is a simple weightable summation, might be changed to F score
 """
    indiv=dictionaryLookup(individual)
    #similarityCost= 15/np.sum(np.in1d(individual[0][0],bundleLookup(individual[0][1]))
    similarityCost= 15/np.sum(np.in1d(individual[0][0],individual[0][1]))
    rangeCost=1/(np.ptp(indiv[0])+np.ptp(indiv[1])+np.ptp(indiv[2]))
    uniformCost=1/(kstest(indiv[0],'uniform')[1]+kstest(indiv[1],'uniform')[1]+kstest(indiv[2],'uniform')[1]+.00001)
    distanceCost=1/(ks_2samp(indiv[0], indiv[1])[1]+ks_2samp(indiv[1], indiv[2])[1]+ks_2samp(indiv[2], indiv[0])[1])
    cost=rangeCost+1.5*uniformCost+distanceCost+similarityCost
    return (cost,)

# Creates the initial generation      
def createIndividual():
 """Creates a random individual with 11 singleton, 10 het. bundle, 10 hom. scale"""
    return[np.random.choice(valueDictionary[1].keys(),n_target+1),
               np.random.choice(valueDictionary[2].keys(),n_target),
                np.random.choice(valueDictionary[3].keys(),n_target)]


# Crossover algorithm          
def nonReplicatingCross(ind1, ind2):
 """Performs a crossover in-place"""
    chromosomeNumber = random.randint(0,2)
    indLength = len(ind1[chromosomeNumber])
    cxpoint = random.randint(1,indLength-1)
    child1 = np.zeros(indLength) #create a child array to use
    child2 = np.zeros(indLength)
    child1[0:cxpoint]=ind2[chromosomeNumber][0:cxpoint] #do the first half of the crossover
    child2[0:cxpoint]=ind1[chromosomeNumber][0:cxpoint]
    index1, index2=0,0
    cont1, cont2=1,1
    for item1 in ind1[chromosomeNumber]: #loop to fill in the second half of the crossover w/out replications
        if cxpoint+index1==indLength:
            break
        try:
            np.where(child1==item1)[0][0]
            continue
        except IndexError: #if there is an error, it means there is no replications, so add the item to the child
            child1[cxpoint+index1]= item1
            index1=index1+1
            cont1==0
    x=np.where(child1==0)[0] #current catch-all incase somehow there is a copy
    for i in x:
        child1[i]=np.random.choice(valueDictionary[chromosomeNumber+1].keys())
    for item2 in ind2[chromosomeNumber]:
        if cxpoint+index2==indLength:
            break
        try:
            np.where(child2==item2)[0][0]
        except IndexError:
            child2[cxpoint+index2]= item2
            index2=index2+1
            cont2==0
    x=np.where(child2==0)[0]
    for i in x:
        child2[i]=np.random.choice(valueDictionary[chromosomeNumber+1].keys())
    ind1[chromosomeNumber]=child1  #copy the child array onto the parent array (in place modification)
    ind2[chromosomeNumber]=child2
    index1, index2=0,0
    
    return ind1, ind2
  
#Mutation algorithm      
def nonReplicatingMutate(ind,indpb):
"""Mutates an individual in place"""
    ind=np.asarray(ind) #copy indiviudal into numpy array
    for chro in range(0,3):
        for i in range(1,len(ind[chro])):
                if random.random() < indpb: #for each nucleotide, use roulette to see if there is a mutation
                    working = True 
                    while working: #intoduce a mutation at point repeatedly until there is no replication
                        randomN=np.random.choice(valueDictionary[chro+1].keys())
                        if randomN in valueDictionary[chro+1].keys()==0:
                            print 'error, replication'
                        try:
                            np.where(ind[0]==randomN)[0][0]
                        except IndexError:
                            ind[chro][i]=randomN
                            working=False        
    return ind
    del ind

#Maps genotype onto phenotype (item number onto value)    
def dictionaryLookup(individual):
    indiv=[np.zeros(n_target+1), np.zeros(n_target), np.zeros(n_target)]
    for chro in range(0,3):
        for i in range(len(individual[0][chro])):
            indiv[chro][i]=valueDictionary[chro+1][individual[0][chro][i]]
    return indiv

#stores top n individuals of an epoch in a list    
def custHallOfFame(population,maxaddsize):
    for i in tools.selBest(population, k=maxaddsize): 
        HallOfFame.append(i)
    
        
#%%==============import data from csv======================%%#
raw_choice_dataset = pd.read_csv(csv_filepath, sep=',', header=None)
print raw_choice_dataset

raw_choice_dataset=raw_choice_dataset[raw_choice_dataset[0]==SID]

valueDictionary={}
for x in range(1,4):
  #Create a dictionary/hashtable associating the unique ID assigned to each singleton or bundle to its modeled value
    placeholderValueDictionary={}
    for rows in raw_choice_dataset[raw_choice_dataset[3].astype(int)==x].iterrows():
        rows[1][6]=random.randint(100,140) # change this once modeling is done
        placeholderValueDictionary[int(rows[1][1])] =float(rows[1][1])
    valueDictionary[x]=placeholderValueDictionary

bundleLookup={}
for x in raw_choice_dataset[raw_choice_dataset[3].astype(int)==3].iterrows():
 #create a dictionary/hastable that gives constituent item in homogeneous bundles
    bundleLookup[int(x[1][1])]=int(x[1][4]),int(x[1][5])

#%%===============initialize toolbox=======================%%#

print 'initializing'
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode="d", fitness=creator.FitnessMax)

stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
stats.register("max", np.max)
stats.register("mean", np.mean)
stats.register("min", np.min)

toolbox = base.Toolbox()

toolbox.register("HOF", custHallOfFame, maxaddsize=3)
toolbox.register("create_individual", createIndividual)
toolbox.register("individuals", tools.initRepeat, creator.Individual,
                 toolbox.create_individual, n=1) 
toolbox.register("population", tools.initRepeat, list, toolbox.individuals)

toolbox.register("evaluate", evalMax)

toolbox.register("mate", nonReplicatingCross)
toolbox.register("mutate", nonReplicatingMutate, indpb=.1)
toolbox.register("select", tools.selTournament, tournsize=2)

toolbox.register("map", futures.map)

#%%======================main==============================%%#

print 'main'

if __name__ == "__main__":
    for epoch in xrange(nepochs):
        print 'beginning epoch %s of %s' %(epoch+1,nepochs)
        pop = toolbox.population(n=npop) #create initial pop
        
        
        fitnesses = toolbox.map(toolbox.evaluate, pop) # eval. fitness of pop
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        for g in range(ngen):  
            if g%5==0:
                print g        
            offspring = toolbox.select(pop, len(pop)) #select which individuals to mate
            offspring = map(toolbox.clone, offspring)
            
            for child1, child2 in zip(offspring[::2], offspring[1::2]): #determine whether to have a cross over
                if random.random() < cxpb:
                    child1[0], child2[0] = toolbox.mate(child1[0], child2[0])
                    del child1.fitness.values, child2.fitness.values
        
            for mutant in offspring: #determine whether to mutate
                if random.random() < mutpb:
                    mutant[0]=toolbox.mutate(mutant[0])
                    del mutant.fitness.values      
            
            invalids = [ind for ind in offspring if not ind.fitness.valid] #assign fitness scores to new offspring
            fitnesses = toolbox.map(toolbox.evaluate, invalids)
            for ind, fit in zip(invalids, fitnesses):
                ind.fitness.values = fit  
                
            pop[:] = offspring #update population with offspring
            
        a=dictionaryLookup(tools.selBest(pop,k=1)[0])

        toolbox.HOF(pop)
        del pop


#%%===============reporting and graphing======================%%#
#Graph, color order - blue green red purple gold light_blue
f, axes=plt.subplots(len(HallOfFame),1, figsize=(7,2*len(HallOfFame)))
plt.tight_layout(pad=3)
num=0

with open('output.txt', 'w') as output_text:
    output_text.write("Results for %s individuals, %s generations and %s epochs\n%s\n" %(npop,ngen,nepochs, SID))
    for x in HallOfFame:
        for i in dictionaryLookup(x):
            seaborn.kdeplot(i, shade=True, 
                            bw=3, 
                            ax=axes[num])
            
        axes[num].set_title("{0:.3f}".format(evalMax(x)[0]))
        if num==0:
            axes[num].set_title("Graphs of Possible Solutions\n{0} individuals, {1} generations, {2} epoch \n\n\n\n{3:.3f}".format(npop,ngen, nepochs,evalMax(x)[0]))    
        output_text.write('%s. Similarity- %s, %s\n'%(num,np.sum(np.in1d(x[0][0],x[0][1])),np.sum(np.in1d(x[0][1],x[0][2]))))
        output_text.write("%s\n\n" %x[0])
        num=num+1

plt.savefig('/Users/Dalton/Documents/Projects/BundledOptionsExp/BehavioralValueMeasurements/records/multipage.pdf', format='pdf', bbox_inches='tight', pad_inches=1)

print 'Program complete'

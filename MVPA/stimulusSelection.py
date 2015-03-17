# -*- coding: utf-8 -*-
"""
GA based stimulus selector
 
Created on Sat Feb 21 13:10:50 2015
@author: Calvin Leather

To do-
Crossover algorithm is somehow producing a few repeats
Consider single-item/hetero 'buddy' term in fitness function
Stick with 2pop ks test or use JS divergence? Or its square?

"""

#%% Imports
import numpy as np
import pandas as pd
from deap import base, creator, tools
import matplotlib.pyplot as plt
from scipy.stats import kstest, ks_2samp
from scoop import futures
import random, operator, seaborn


print 'defining variables'

# Three col CSV (Item-Code, Option-Type, Value)
csv_filepath='/Users/Dalton/Documents/Projects/BundledOptionsExp/BehavioralValueMeasurements/records/options.csv'

#%% Magic Numbers
nepochs, ngen, npop, cxpb, mutpb = 4,60,250, 0.4, 0.2
HOFsize=1 #number of individuals to put in each epoc
HallOfFame=[]

SID='a03'
n_single=20 #1 
n_hetero=15 #2
n_homo=22 #3
n_genome=n_single+n_hetero+n_homo
n_target=10 #Desired number in each catagory
chromosomeDict={0:n_single, 1:n_hetero, 2:n_homo}

random.seed()

#%%===========define fitness and functions=================%%#

print 'defining functions'

# Fitness Function
def evalMax(individual):
    indiv=dictionaryLookup(individual)
    
    similarityCost= 15/np.sum(np.in1d(individual[0][0],individual[0][1]))
    rangeCost=1/(np.ptp(indiv[0])+np.ptp(indiv[1])+np.ptp(indiv[2]))
    uniformCost=1/(kstest(indiv[0],'uniform')[1]+kstest(indiv[1],'uniform')[1]+kstest(indiv[2],'uniform')[1]+.00001)
    distanceCost=1/(ks_2samp(indiv[0], indiv[1])[1]+ks_2samp(indiv[1], indiv[2])[1]+ks_2samp(indiv[2], indiv[0])[1])
    cost=rangeCost+1.5*uniformCost+distanceCost+similarityCost
    return (cost,)

# Creates the initial generation      
def createIndividual():
    #Creates an individual with unique sample
    x=[np.random.choice(valueDictionary[1].keys(),n_target+1),
               np.random.choice(valueDictionary[2].keys(),n_target),
                np.random.choice(valueDictionary[3].keys(),n_target)]
               
    return[np.random.choice(valueDictionary[1].keys(),n_target+1),
               np.random.choice(valueDictionary[2].keys(),n_target),
                np.random.choice(valueDictionary[3].keys(),n_target)]


# Crossover algorithm          
def nonReplicatingCross(ind1, ind2):
    chromosomeNumber = random.randint(0,2)
    indLength = len(ind1[chromosomeNumber])
    cxpoint = random.randint(1,indLength-1)
    child1 = np.zeros(indLength)
    child2 = np.zeros(indLength)
    child1[0:cxpoint]=ind2[chromosomeNumber][0:cxpoint]
    child2[0:cxpoint]=ind1[chromosomeNumber][0:cxpoint]
    index1, index2=0,0
    cont1, cont2=1,1
    for item1 in ind1[chromosomeNumber]:
        if cxpoint+index1==indLength:
            break
        try:
            np.where(child1==item1)[0][0]
            continue
        except IndexError:
            child1[cxpoint+index1]= item1
            index1=index1+1
            cont1==0
    x=np.where(child1==0)[0]
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
    ind1[chromosomeNumber]=child1  
    ind2[chromosomeNumber]=child2
    index1, index2=0,0

           
    return ind1, ind2
  
#Mutation algorithm      
def nonReplicatingMutate(ind,indpb):

    ind=np.asarray(ind)
    for chro in range(0,3):
        for i in range(1,len(ind[chro])):
                if random.random() < indpb:
                    working = True 
                    while working:
                        randomN=np.random.choice(valueDictionary[chro+1].keys())
                        if randomN in valueDictionary[chro+1].keys()==0:
                            print 'noooooooo'
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
    placeholderValueDictionary={}
    for rows in raw_choice_dataset[raw_choice_dataset[3].astype(int)==x].iterrows():
        rows[1][6]=random.randint(100,140) # change this once modeling is done
        placeholderValueDictionary[int(rows[1][1])] =float(rows[1][1])
    valueDictionary[x]=placeholderValueDictionary

bundleLookup={}
for x in raw_choice_dataset[raw_choice_dataset[3].astype(int)==3].iterrows():
    bundleLookup[int(x[1][1])]=int(x[1][4]),int(x[1][5])



"""
raw_choice_dataset = pd.read_csv(csv_filepath, sep=',', header=None)
raw_choice_dataset.dropna()

valueDictionary={}
for x in range(1,4):
    placeholderValueDictionary={}
    for i in raw_choice_dataset[(raw_choice_dataset[1]==x)].index:
        placeholderValueDictionary[raw_choice_dataset[0][i]] = random.random()
    valueDictionary[x]=placeholderValueDictionary
"""
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
        pop = toolbox.population(n=npop)
        
        
        fitnesses = toolbox.map(toolbox.evaluate, pop)
        
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        
        for g in range(ngen):  
            if g%5==0:
                print g        
            offspring = toolbox.select(pop, len(pop))
            offspring = map(toolbox.clone, offspring)
            
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < cxpb:
                    child1[0], child2[0] = toolbox.mate(child1[0], child2[0])
                    del child1.fitness.values, child2.fitness.values
        
            for mutant in offspring:
                if random.random() < mutpb:
                    mutant[0]=toolbox.mutate(mutant[0])
                    del mutant.fitness.values      
            
            invalids = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalids)
            for ind, fit in zip(invalids, fitnesses):
                ind.fitness.values = fit  
                
            pop[:] = offspring
            
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
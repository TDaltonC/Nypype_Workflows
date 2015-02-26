# -*- coding: utf-8 -*-
"""
GA based stimulus selector
Creates a population of wowasaurus rex
3 chromosomes, each with 10 'proteins'
Permutation based CX and mutation (preserves uniqueness)
 
Created on Sat Feb 21 13:10:50 2015
@author: Calvin Leather
"""
#%% Imorts
import numpy as np
import pandas as pd
from deap import base, creator, tools
import random, operator
from sklearn.neighbors.kde import KernelDensity
import matplotlib.pyplot as plt
from scipy.stats import mstats
from scoop import futures

print 'defining variables'

# Three col CSV (Item-Code, Option-Type, Value)
csv_filepath='/home/brain/Desktop/Custom MVPA Workflow/SampleData.csv'

#%% Magic Numbers
population_size=20

# SALT

n_single=20 #1
n_hetero=15 #2
n_homo=22 #3
n_genome=n_single+n_hetero+n_homo
n_target=10 #Desired number in each catagory (maybe make this 11 options for the single items)

#%%"""===========define fitness and functions================="""

print 'defining functions'

# Fitness Function
def evalMax(individual):
    indiv=dictionaryLookup(individual)
    
    rangeCost=np.power((np.ptp(indiv[0])+np.ptp(indiv[1])+np.ptp(indiv[2])), 2)
    distanceCost=0
    normalityCost=mstats.normaltest(indiv[0])[1]+mstats.normaltest(indiv[1])[1]+mstats.normaltest(indiv[2])[1]
    cost=400*rangeCost+distanceCost+100*normalityCost
    return (cost,)

# Creates the initial generation     
def createIndividual(species):
    #Creates an individual with unique sample
    return [random.sample(range(n_single),n_target), 
                   random.sample(range(n_hetero),n_target),
                    random.sample(range(n_homo), n_target)]

# Crossover algo
def nonReplicatingCross(ind1, ind2):
    chromosomeNumber = random.randint(0,2)
    indLength = len(ind1[chromosomeNumber])
    cxpoint = random.randint(1,indLength-1)
    child1 = np.zeros(indLength)
    child2 = np.zeros(indLength)
    child1[0:cxpoint]=ind2[chromosomeNumber][0:cxpoint]
    child2[0:cxpoint]=ind1[chromosomeNumber][0:cxpoint]
    index1=0
    index2=0
    for item1 in ind1[chromosomeNumber]:
        if cxpoint+index1==indLength:
            break
        try:
            np.where(child1==item1)[0][0]
        except IndexError:
            child1[cxpoint+index1]= item1
            index1=index1+1

            
    for item2 in ind2[chromosomeNumber]:
        if cxpoint+index2==indLength:
            break
        try:
            np.where(child2==item2)[0][0]
        except IndexError:
            child2[cxpoint+index2]= item2
            index2=index2+1
    ind1[chromosomeNumber]=child1  
    ind2[chromosomeNumber]=child2
    index1=0
    index2=0
    
    return ind1, ind2
        
# Mutation fucntion
def nonReplicatingMutate(ind,indpb):
    ind=np.asarray(ind)
    for i in range(1,len(ind[0])):
        if random.random() < indpb:
            working = True 
            while working:
                randomN=random.randint(0,n_single)
                try:
                    np.where(ind[0]==randomN)[0][0]
                except IndexError:
                    ind[0][i]=randomN
                    working=False
    for i in range(1,len(ind[1])):
        if random.random() < indpb:
            working = True 
            while working:
                randomN=random.randint(0,n_hetero)
                try:
                    np.where(ind[1]==randomN)[0][0]
                except IndexError:
                    ind[1][i]=randomN
                    working=False
    for i in range(1,len(ind[2])):
        if random.random() < indpb:
            working = True 
            while working:
                randomN=random.randint(0,n_homo)
                try:
                    np.where(ind[2]==randomN)[0][0]
                except IndexError:
                    ind[2][i]=randomN
                    working=False
    return ind
    del ind


def dictionaryLookup(individual):
    indiv=np.ndarray(shape=(3,10), dtype=float)
    for chro in range(0,3):
        for i in range(len(individual[0][chro])):
            indiv[chro][i]=valueDictionary[chro+1][individual[0][chro][i]]
    return indiv
        
#%%"""==============import data from csv======================"""

raw_choice_dataset = pd.read_csv(csv_filepath, sep=',', header=None)
raw_choice_dataset.dropna()

valueDictionary={}
for x in range(1,4):
    placeholderValueDictionary={}
    for i in raw_choice_dataset[(raw_choice_dataset[1]==x)].index:
        placeholderValueDictionary[raw_choice_dataset[0][i]] = raw_choice_dataset[2][i]
    valueDictionary[x]=placeholderValueDictionary

#%%"""===============initialize toolbox======================="""
print 'initializing'
creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, typecode="d", fitness=creator.FitnessMax)

stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
stats.register("max", np.max)
stats.register("mean", np.mean)
stats.register("min", np.min)

HOF = tools.HallOfFame(maxsize=10)

toolbox = base.Toolbox()

toolbox.register("create_individual", createIndividual, 1)
toolbox.register("individuals", tools.initRepeat, creator.Individual,
                 toolbox.create_individual, n=1) 
toolbox.register("population", tools.initRepeat, list, toolbox.individuals)

toolbox.register("evaluate", evalMax)

toolbox.register("mate", nonReplicatingCross)
toolbox.register("mutate", nonReplicatingMutate, indpb=.1)
toolbox.register("select", tools.selTournament, tournsize=2)

toolbox.register("map", futures.map)
#%%"""======================main=============================="""
print 'main'
if __name__ == "__main__":
    pop = toolbox.population(n=200)   
    ngen, cxpb, mutpb = 80, 0.4, 0.2
    
    fitnesses = toolbox.map(toolbox.evaluate, pop)
    
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print 'beginning'
    
    for g in range(ngen):  
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
        
        a=tools.selBest(pop,k=1)[0][0]
        print a
        print np.sum(tools.selBest(pop,k=1)[0][0])
        a=dictionaryLookup(tools.selBest(pop,k=1)[0])
        
        for i in range(0,3):
            ones=np.ones(1000)
            kde=KernelDensity(kernel='gaussian', bandwidth=.05).fit(zip(a[i], ones))
            x_grid=np.linspace(0, 1, 1000)
            pdf = np.exp(kde.score_samples(zip(x_grid, ones)))  
            plt.plot(x_grid, pdf, linewidth=3, alpha=.5)


#%% TO-DO's

# make the single chromisome 11 long
# add a term to the fitness function for the "buddy" items.
# Jensen-Shannon? 
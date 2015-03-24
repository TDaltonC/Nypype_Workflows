# -*- coding: utf-8 -*-
"""
GA based stimulus selector
 
Created on Sat Feb 21 13:10:50 2015
@author: Calvin Leather
To do-
Look into uniformity metric in evalFit()
Explore different types of means
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
nepochs, ngen, npop, cxpb, mutpb =4,250,500, 0.1, 0.05
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
random.seed(1)
np.random.seed(1)


#%%===========define fitness and functions=================%%#
print 'defining functions'

uni=np.random.uniform(0,60,500)

def evalFit(individual):
    
    """ A weighted total of fitness scores to be maximized
    RangeCost-maximum to minimum
    SimilarityCost - number of items in both singleton and homogenous scaling
    UniformCost- Uses KS divergence to indicate distance of distribution of values from uniform distribution
    DistanceCost- Uses KS divergence to indicate differences between distributions
    Cost currently is a simple weightable summation, might be changed to F score"""
    indiv=genoToPheno(individual)
    similarityCost=np.sum(np.in1d(individual[0][0],[ bundleLookup[k] for k in individual[0][1] ]))
    #similarityCost=   np.sum([np.sum(c)>1 for c in [np.in1d(k,x) for k in y]])
    #x is singelton, y is array of tuples of constituent items
    similarity2=np.sum([np.sum(c)>1 for c in [np.in1d(p,individual[0][0]) for p in [ bundleLookup2[w] for w in individual[0][2] ]]])
    rangeCost=(np.ptp(indiv[0])+np.ptp(indiv[1])+np.ptp(indiv[2]))/125
    uniformCost=1/(kstest(indiv[0],'uniform')[0]+kstest(indiv[1],'uniform')[0]+kstest(indiv[2],'uniform')[0])
    #uniformCost=(ks_2samp(indiv[0], uni)[1]+ks_2samp(indiv[1], uni)[1]+ks_2samp(indiv[2], uni)[1])    
    distanceCost=(ks_2samp(indiv[0], indiv[1])[1]+ks_2samp(indiv[1], indiv[2])[1]+ks_2samp(indiv[2], indiv[0])[1])
    cost=rangeCost+uniformCost+distanceCost+*similarityCost+similarity2
    return (cost,)

# Creates the initial generation      
def createIndividual():
    """Creates a random individual with 11 singleton, 10 het. bundle, 10 hom. scale"""    
    return [random.sample(valueDictionary[1].keys(),n_target+1),
               random.sample(valueDictionary[2].keys(),n_target),
                random.sample(valueDictionary[3].keys(),n_target)]


# Crossover algorithm          
def nonReplicatingCross(ind1, ind2):
    """Performs a crossover in-place"""
    """Highly in need of new documentation"""
    chromosomeNumber = random.randint(0,2)
    indLength = len(ind1[chromosomeNumber])
    cxpoint = random.randint(1,indLength-1)
    child1 = np.zeros(indLength) #create a child array to use
    child2 = np.zeros(indLength)
    child1[0:cxpoint]=ind1[chromosomeNumber][0:cxpoint] #do the first half of the crossover
    child2[0:cxpoint]=ind2[chromosomeNumber][0:cxpoint]
    try:
        child1[child1==0]=[x for x in ind2[chromosomeNumber] if x not in child1][0:len(child1[child1==0])]
    except ValueError:
        pass
    if (child1[child1==0]!=[]) or (child1[child1==0]==[0]):
        child1[child1==0]=random.sample([x for x in valueDictionary[chromosomeNumber+1].keys() if x not in child1], np.sum(np.where(child1==0, 1, 0)))
    try:
        child2[child2==0]=[x for x in ind1[chromosomeNumber] if x not in child2][0:len(child2[child2==0])]
    except ValueError:
        pass
    if (child2[child2==0]!=[]) or (child2[child2==0]==[0]):
        child2[child2==0]=random.sample([x for x in valueDictionary[chromosomeNumber+1].keys() if x not in child2], np.sum(np.where(child2==0, 1, 0)))
    ind1[chromosomeNumber]=child1  #copy the child array onto the parent array (in place modification)
    ind2[chromosomeNumber]=child2
    
    return ind1, ind2
  
#Mutation algorithm      
def nonReplicatingMutate(ind,indpb):
    """Mutates an individual in place"""
    ind=np.asarray(ind) #copy indiviudal into numpy array
    for chro in range(0,3):
        for i in range(1,len(ind[chro])):
                if random.random() < indpb: #for each nucleotide, use roulette to see if there is a mutation
                            ind[chro][i]=(random.sample([x for x in valueDictionary[chro+1].keys() if x not in ind[chro]],1))[0]                                
    return ind
    del ind
    
#Maps genotype onto phenotype (item number onto value)    
def genoToPheno(individual):
    #print individual
    indiv=[np.zeros(n_target+1), np.zeros(n_target), np.zeros(n_target)]
    for chro in range(0,3):
        for i in range(len(individual[0][chro])):
            indiv[chro][i]=valueDictionary[chro+1][int(individual[0][chro][i])]
    return indiv

#stores top n individuals of an epoch in a list    
def custHallOfFame(population,maxaddsize):
    for i in tools.selBest(population, k=maxaddsize): 
        HallOfFame.append(i)

def getSim(genome):
    return [ bundleLookup[k] for k in genome]
        
#%%==============import data from csv======================%%#
raw_choice_dataset = pd.read_csv(csv_filepath, sep=',', header=None)

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
for x in raw_choice_dataset[raw_choice_dataset[3].astype(int)==2].iterrows():
 #create a dictionary/hastable that gives constituent item in homogeneous bundles
    bundleLookup[int(x[1][1])]=int(x[1][4])
    
bundleLookup2={}
for x in raw_choice_dataset[raw_choice_dataset[3].astype(int)==3].iterrows():
    bundleLookup2[int(x[1][1])]=(int(x[1][4]),int(x[1][5]))
#%%===============initialize toolbox=======================%%#

print 'initializing'
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, typecode="d", fitness=creator.FitnessMax)

stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
stats.register("max", np.max)
stats.register("mean", np.mean)
stats.register("min", np.min)

toolbox = base.Toolbox()

toolbox.register("HOF", custHallOfFame, maxaddsize=HOFsize)
toolbox.register("create_individual", createIndividual)
toolbox.register("individuals", tools.initRepeat, creator.Individual,
                 toolbox.create_individual, n=1) 
toolbox.register("population", tools.initRepeat, list, toolbox.individuals)

toolbox.register("evaluate", evalFit)

toolbox.register("mate", nonReplicatingCross)
toolbox.register("mutate", nonReplicatingMutate, indpb=.1)
toolbox.register("select", tools.selTournament, tournsize=2)

toolbox.register("map", futures.map)

s= tools.Statistics()
s.register("max", np.max)
s.register("mean", np.mean)

log=tools.Logbook()

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
            
            log.record(gen=g,**stats.compile(pop))
            pop[:] = offspring #update population with offspring
            
        a=genoToPheno(tools.selBest(pop,k=1)[0])

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
        for i in genoToPheno(x):
            seaborn.kdeplot(i, shade=True, 
                            bw=2, 
                            ax=axes[num])
            
        axes[num].set_title("{0:d}- Score={1:.3f}".format(num,evalFit(x)[0]))
        if num==0:
            axes[num].set_title("Graphs of Possible Solutions\n{0} individuals, {1} generations, {2} epoch \n\n\n\n{3:.3f}".format(npop,ngen, nepochs,evalFit(x)[0]))    
        output_text.write('%s. Similarity- %s, %s\n'%(num,np.sum(np.in1d(x[0][0],[ bundleLookup[k] for k in x[0][1] ])),
                                                      np.sum([np.sum(c)>1 for c in [np.in1d(p,x[0][0]) for p in [ bundleLookup2[w] for w in x[0][2] ]]])))
        output_text.write("%s\n\n" %x[0])
        num=num+1

plt.savefig('/Users/Dalton/Documents/Projects/BundledOptionsExp/BehavioralValueMeasurements/records/multipage.pdf', format='pdf',
    bbox_inches='tight', pad_inches=1)

print 'Program complete'

#%%===============plot stats======================%%#
if 1==0:
    fit_max = log.select("max")
    gen=log.select('gen')
    plt.plot(gen, fit_max)
    

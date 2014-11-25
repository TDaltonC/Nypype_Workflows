Description & Goal

This model is designed to assess the differences between the three tasks. It should be compared to model 1 (uses value instead of e^value).

Value Modle -- This model used uses a version of MLE value calculated using only control and scaling trials, then it takes that number and calulates e^value for each item and uses that as value. This model is't vary "valid" but it was the first one we ran on the pilot data so it has historical value. 

Regressors

0: Value - Parametric value (as provided by the max-likelihood model) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the max-likelihood model) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials

Contrasts

# Contrasts
cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['Scaling','T', ['Scaling'],[1]]
cont4 = ['Bundling','T', ['Bundling'],[1]]
cont5 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont6 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont7 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont8 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont9 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
contrasts = [cont0,cont1,cont2,cont3,cont4,cont5,cont6,cont7,cont8,cont9]
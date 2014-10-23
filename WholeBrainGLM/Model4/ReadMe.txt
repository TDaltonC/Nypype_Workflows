Description & Goal

This model is designed to assess the differences between the three tasks. It should be compared to model 3 (same as this but it has a diff regressor) and model 2 (same as this but uses the max-likelihood estimate as Value).

Regressors

0: Value - Parametric value (as provided by the distance measure) of the on screen option
1: Control - Task regressor for Control trials
2: Scaling - Task regressor for Scaling trials
3: Bundling - Task regressor for Bundling trials

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont3 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont4 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont5 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont6 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
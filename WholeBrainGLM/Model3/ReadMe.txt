Description & Goal

This model is designed to assess the differences between the three tasks. It should be compared to model 4 (same as this but without a diff regressor) and model 1 (same as this but uses the max-likelihood estimate as Value).

Regressors

0: Value - Parametric value (as provided by the distance measure) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the distance measure) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont4 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont5 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont6 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont7 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
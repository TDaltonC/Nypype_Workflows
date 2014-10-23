Description & Goal

This model is designed to assess where brain activity is praportional to the number of items on the screen.

Regressors

0: Value - Parametric value (as provided by the max-likelihood model) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the max-likelihood model) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials
5: ItemCount - Parametric regressor for the number of items on the screen

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['ItemCount', 'T', ['ItemCount'],[1]]
cont4 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont5 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont6 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont7 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont8 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
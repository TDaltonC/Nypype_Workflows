Description & Goal

This model is designed to look for taste as defined by the measured distance task. The taste of scaling and bunding tasks are assumed to be the average of their parts.

Regressors

0: Taste - Parametric taste (as provided by the distance measure) of the on screen option. Scaling and bundling tasks are modeled as the average of the taste of thier parts.
1: TsteDiff - Parametric difference in tastes (as provided by the distance measure) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Taste','T', ['Taste'],[1]]
cont2 = ['TasteDiff','T', ['TasteDiff'],[1]]
cont3 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont4 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont5 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont6 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont7 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
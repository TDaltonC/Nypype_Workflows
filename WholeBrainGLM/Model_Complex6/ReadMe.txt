Description & Goal

This model is designed to assess how many on screen items are requred to see dlPFC activity. 
Is 2 items enough? What about 3 items? Does it only work with a parametric regressor?
This should be compaired to model_Complex1

Regressors

0: Value - Parametric value (as provided by the DDM model (model8)) of the on screen option
1: Difficulty - Parametric difference in values (as provided by the DDM model (model8)) of the on screen option and the off screen option
2: Control - Task regressor for Control trials
3: Scaling - Task regressor for Scaling trials
4: Bundling - Task regressor for Bundling trials
5: ScalingItmCount - Parametric regressor for the number of items on the screen. Then should be proportional to dlPFC activity
6: BundlingItmCount - Parametric regressor for the number of items on the screen. Then should be proportional to dlPFC activity

Contrasts

cont0 = ['Control','T', ['Control'],[1]]
cont1 = ['Value','T', ['Value'],[1]]
cont2 = ['Difficulty','T', ['Difficulty'],[1]]
cont3 = ['ScalingItmCount','T', ['ScalingItmCount'],[1]]
cont4 = ['BundlingItmCount','T', ['BundlingItmCount'],[1]]
cont5 = ['Scaling>Control','T', ['Scaling','Control'],[1,-1]]
cont6 = ['Bundling>Control','T', ['Bundling','Control'],[1,-1]]
cont7 = ['Bundling>Scaling','T', ['Bundling','Scaling'],[1,-1]]
cont8 = ['Scaling>Bundling','T', ['Scaling','Bundling'],[1,-1]]
cont9 = ['Scaling+Bundling>Control','T', ['Scaling','Bundling','Control'],[.5,.5,-1]]
